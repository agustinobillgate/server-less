
DEFINE TEMP-TABLE t-eg-location LIKE eg-location.
DEFINE TEMP-TABLE t-zimmer LIKE zimmer
    FIELD gname-str AS CHAR  FORMAT "x(60)". /*For web*/

DEFINE TEMP-TABLE t-queasy      LIKE queasy. /*For web*/

DEFINE TEMP-TABLE send-alert
    FIELD alert-date          AS DATE
    FIELD alert-time          AS INTEGER   
    FIELD alert-str           AS CHAR 
    FIELD alert-reqnr         AS INTEGER
    FIELD alert-msg           AS CHAR  FORMAT "x(200)"  
    FIELD alert-sendto        AS INTEGER
    FIELD alert-sendnm        AS CHAR
    FIELD alert-sendnr        AS CHAR
    FIELD alert-msgstatus     AS INTEGER
    FIELD alert-mstat         AS CHAR FORMAT "x(30)".

DEFINE TEMP-TABLE his-action
    FIELD action-mainnr AS INTEGER /*FD for web*/
    FIELD action-nr     AS INTEGER
    FIELD action-nm     AS CHAR        FORMAT "x(64)"
    FIELD create-date   AS DATE
    FIELD create-time   AS INTEGER
    FIELD time-str      AS CHAR
    FIELD create-by     AS CHAR.

DEFINE TEMP-TABLE mobile
    FIELD nr                 AS INTEGER
    FIELD NAME               AS CHAR     FORMAT "x(30)"
    FIELD POSITION           AS CHAR     FORMAT "x(30)"
    FIELD mobilenr           AS CHAR     FORMAT "x(30)"
    FIELD mobile-SELECTED    AS LOGICAL.

DEFINE TEMP-TABLE action LIKE eg-action
    FIELD SELECTED AS LOGICAL INITIAL NO.

DEFINE TEMP-TABLE maintain LIKE eg-maintain.
DEFINE BUFFER mbuff FOR eg-maintain.

DEFINE BUFFER resline1 FOR res-line.              
DEFINE BUFFER guest1 FOR guest.

DEFINE TEMP-TABLE t-property
    FIELD prop-nr AS INTEGER
    FIELD prop-nm AS CHAR FORMAT "x(40)" COLUMN-LABEL "Object Item"
    FIELD prop-selected AS LOGICAL INITIAL NO
    FIELD pcateg-nr AS INTEGER
    FIELD pcateg AS CHAR
    FIELD pmain-nr AS INTEGER
    FIELD pmain AS CHAR
    FIELD ploc-nr AS INTEGER
    FIELD ploc  AS CHAR
    FIELD pzinr    AS CHAR.

DEFINE TEMP-TABLE tpic
    FIELD pic-nr AS INTEGER
    FIELD pic-nm AS CHAR FORMAT "x(24)" COLUMN-LABEL "Pic"
    FIELD pic-Dept AS INTEGER.

DEF INPUT  PARAMETER pvILanguage AS INTEGER          NO-UNDO.
DEF INPUT  PARAMETER mainno AS INT.
DEF INPUT  PARAMETER user-init AS CHAR.
DEF OUTPUT PARAMETER sguestflag AS LOGICAL.
DEF OUTPUT PARAMETER GroupID AS INT.
DEF OUTPUT PARAMETER EngID AS INT.
DEF OUTPUT PARAMETER sms-flag AS LOGICAL INIT NO.
DEF OUTPUT PARAMETER avail-eg-location AS LOGICAL INIT NO.
DEF OUTPUT PARAMETER h-category AS INTEGER  NO-UNDO.
DEF OUTPUT PARAMETER h-maintask AS INTEGER  NO-UNDO.
DEF OUTPUT PARAMETER h-location AS INTEGER  NO-UNDO. 
DEF OUTPUT PARAMETER h-zinr     AS CHAR     NO-UNDO.
DEF OUTPUT PARAMETER str-property AS CHAR.
DEF OUTPUT PARAMETER str-maintask AS CHAR.
DEF OUTPUT PARAMETER str-categ AS CHAR.
DEF OUTPUT PARAMETER ci-date AS DATE.

DEF OUTPUT PARAMETER flag1 AS INT INIT 0.
DEF OUTPUT PARAMETER flag2 AS INT INIT 0.
DEF OUTPUT PARAMETER flag3 AS INT INIT 0.
DEF OUTPUT PARAMETER flag4 AS INT INIT 0.
DEF OUTPUT PARAMETER flag5 AS INT INIT 0.
DEF OUTPUT PARAMETER flag6 AS INT INIT 0.
DEF OUTPUT PARAMETER flag7 AS INT INIT 0.
DEF OUTPUT PARAMETER flag8 AS INT INIT 0.

DEF OUTPUT PARAMETER TABLE FOR send-alert.
DEF OUTPUT PARAMETER TABLE FOR his-action.
DEF OUTPUT PARAMETER TABLE FOR mobile.
DEF OUTPUT PARAMETER TABLE FOR action.
DEF OUTPUT PARAMETER TABLE FOR maintain.
DEF OUTPUT PARAMETER TABLE FOR t-eg-location.
DEF OUTPUT PARAMETER TABLE FOR t-zimmer.
DEF OUTPUT PARAMETER TABLE FOR t-queasy. /*For web*/
DEF OUTPUT PARAMETER TABLE FOR t-property.
DEF OUTPUT PARAMETER TABLE FOR tpic.


{SupertransBL.i} 
DEF VAR lvCAREA AS CHAR INITIAL "eg-mainscheduleEd". 
DEFINE VARIABLE alert-str AS CHAR FORMAT "x(30)" EXTENT 3.
alert-str[1] = translateextended("Successfully", lvcarea, "").
alert-str[2] = translateextended("Failed", lvcarea, "").
alert-str[3] = translateextended("Pending", lvcarea, "").

DEFINE VARIABLE guestname AS CHAR.

FIND FIRST eg-location WHERE eg-location.guestflag = YES NO-LOCK NO-ERROR.
IF AVAILABLE eg-location THEN avail-eg-location = YES.

FIND FIRST htparam WHERE htparam.paramnr = 87 NO-LOCK.
/* ci-date = fdate. */                                              /* Rulita 211024 | Fixing for serverless */
IF AVAILABLE htparam THEN ci-date = htparam.fdate.                  /* Rulita 240225 | Fixing if avail for serverless issue git 678 */

RUN define-group.
RUN define-engineering.
RUN GetMaintain.
RUN create-mobile.
RUN GetPrevAction.
RUN create-alert.
RUN create-property.
RUN create-pic.
FIND FIRST eg-maintain WHERE eg-maintain.maintainnr = mainno NO-LOCK NO-ERROR.
IF AVAILABLE eg-maintain THEN
DO:
    IF eg-maintain.TYPE = 1 OR eg-maintain.TYPE = 2 THEN
    DO:
        flag8 = 1.
    END.
END.

FOR EACH eg-location:
    CREATE t-eg-location.
    BUFFER-COPY eg-location TO t-eg-location.
END.

FOR EACH zimmer:
    RUN get-guestname(zimmer.zinr).
    CREATE t-zimmer.
    BUFFER-COPY zimmer TO t-zimmer.
    ASSIGN t-zimmer.gname-str = guestname.
END.

FOR EACH queasy WHERE queasy.KEY = 135: /*For web*/
    CREATE t-queasy.
    BUFFER-COPY queasy TO t-queasy.
END.

PROCEDURE Define-Group:
    FIND FIRST bediener WHERE bediener.userinit = user-init NO-LOCK NO-ERROR.
    IF AVAILABLE bediener THEN
    DO:
        ASSIGN GroupID = bediener.user-group.
    END.
END.

PROCEDURE Define-engineering:
    FIND FIRST htparam WHERE htparam.paramnr = 1200 AND htparam.feldtyp = 1 NO-LOCK NO-ERROR.
    IF AVAILABLE htparam THEN
    DO:
        ASSIGN EngID = htparam.finteger.
    END.
    ELSE
    DO:
        /*MTHIDE MESSAGE NO-PAUSE.
        MESSAGE translateExtended("Group No for Engineering Modul not yet defined.", lvCAREA, "":U) 
            SKIP 
            translateExtended( "Please contact your next VHP Support for further Information.", lvCAREA, "":U) 
            VIEW-AS ALERT-BOX INFORMATION.*/
    END.
END.

PROCEDURE GetMaintain:
DEF BUFFER bProp FOR eg-property.
DEF BUFFER quesbuff     FOR queasy.
DEF BUFFER quesbuff1    FOR queasy.

    FOR EACH  maintain:
        DELETE maintain.
    END.

    FIND FIRST mbuff WHERE mbuff.maintainnr =  mainNo EXCLUSIVE-LOCK NO-ERROR.
    IF NOT AVAILABLE mbuff THEN RETURN.
    ELSE
    DO:
        BUFFER-COPY mbuff TO maintain.

        IF maintain.smsflag = YES THEN ASSIGN sms-flag = YES.

        FIND FIRST bProp WHERE bProp.nr =  maintain.propertynr NO-LOCK NO-ERROR.
        IF AVAILABLE bprop THEN
        DO:
            ASSIGN 
                h-maintask  = bprop.maintask
                h-location  = bprop.location
                h-zinr      = bprop.zinr
                str-property = bprop.bezeich
                maintain.propertynr = bprop.nr.

           FIND FIRST quesbuff WHERE quesbuff.KEY = 133 AND quesbuff.number1 = bprop.maintask NO-LOCK NO-ERROR.
           IF AVAILABLE quesbuff THEN
           DO:
               str-maintask = quesbuff.char1.
               h-maintask = quesbuff.number1.

               FIND FIRST action WHERE action.maintask =  h-maintask NO-ERROR.
               IF AVAILABLE action THEN
               DO:
                   flag1 = 1.
                   /*MTOPEN QUERY q1 FOR EACH action WHERE action.maintask =  h-maintask NO-LOCK.
    
                   ENABLE b1 all-act WITH FRAME frame1.
                   DISP str-Maintask b1 WITH FRAME frame1.  
                   
                   b1:DESELECT-FOCUSED-ROW().*/
               END.
               ELSE
               DO:
                   flag1 = 2.
                   /*MTOPEN QUERY q1 FOR EACH action WHERE action.maintask =  maintain.maintask NO-LOCK.
    
                   ENABLE b1 all-act WITH FRAME frame1.
                   DISP str-Maintask b1 WITH FRAME frame1.*/
                   
               END.

               FIND FIRST quesbuff1 WHERE quesbuff1.KEY = 132 AND quesbuff1.number1 = quesbuff.number2 NO-LOCK NO-ERROR.
               IF AVAILABLE quesbuff1 THEN
               DO:
                   ASSIGN h-category   = quesbuff1.number1
                       str-categ = quesbuff1.char1.
               END.
               ELSE
               DO:
                   ASSIGN h-category  = 0
                       str-categ = "".
               END.

           END.
           ELSE
           DO:
               ASSIGN h-maintask = 0
                      str-maintask = "".
           END.

           flag2 = 1.
           /*MTAPPLY "RETURN" TO maintain.propertynr IN FRAME frame1.*/

           FIND FIRST eg-location WHERE eg-location.nr = bprop.location AND eg-location.guestflag = YES NO-LOCK NO-ERROR.  
           IF AVAILABLE eg-location THEN
           DO:
               flag3 = 1.
               ASSIGN sguestflag = YES
                   h-location = 0.
    
               /*MTDISPLAY h-location sguestflag WITH FRAME frame1.*/
           END.
           ELSE
           DO:
               flag3 = 2.
               ASSIGN sguestflag = NO.
               /*MTDISPLAY sguestflag WITH FRAME frame1.*/
           END.
        END.
        ELSE
        DO:
            ASSIGN 
                h-maintask  = 0
                h-location  = 0
                h-zinr      = "0".
            flag4 = 1.
            /*MTDISPLAY h-maintask  h-location  h-zinr  WITH FRAME frame1.*/
        END.

        IF sguestflag = NO THEN
        DO:
            flag5 = 1.
            /*MTAPPLY "RETURN" TO h-maintask  IN FRAME frame1. 
            APPLY "RETURN" TO h-location  IN FRAME frame1.
            APPLY "RETURN" TO maintain.propertynr IN FRAME frame1.
            
            DISP str-property WITH FRAME frame1.*/
        END.
        ELSE
        DO:
            flag5 = 2.
            /*MTAPPLY "value-changed" TO sguestflag IN FRAME frame1.*/
        END.

        flag6 = 1.
        /*MTAPPLY "return" TO maintain.pic IN FRAME frame1.*/

        RUN getaction (h-maintask).

        /*MTOPEN QUERY q1 FOR EACH action NO-LOCK.*/

        IF maintain.TYPE = 3 THEN
        DO:
            flag7 = 1.
            /*MTHIDE MESSAGE NO-PAUSE.
            MESSAGE translateExtended("Edit not posibble for Done Maintenance.", lvCAREA, "")
                VIEW-AS ALERT-BOX INFORMATION.

            RUN mk-ReadOnly(YES).
            APPLY "ENTRY" TO btn-stop.*/
            RETURN NO-APPLY.
        END.
        ELSE
        DO:
            flag7 = 2.
            /*MTRUN mk-ReadOnly(NO).
            APPLY "entry" TO maintain.TYPE.*/
        END.
    END.
END.

PROCEDURE create-mobile:
    DEF BUFFER qbuff FOR eg-mobilenr.

    FOR EACH Mobile :
        DELETE mobile.
    END.

    FOR EACH qbuff WHERE qbuff.activeflag = YES AND qbuff.mobilenr NE "" NO-LOCK:       /* Rulita 240225 | Fixing from qbuff.mobile to qbuff.mobilenr serverless issue git 678 */
        CREATE mobile.
        ASSIGN mobile.nr          = qbuff.nr
           mobile.NAME            = qbuff.NAME
           mobile.POSITION        = qbuff.POSITION 
           mobile.mobilenr        = qbuff.mobilenr 
           mobile.mobile-SELECTED = NO. 
    END.                                    
END.

PROCEDURE GetPrevAction:
    DEF BUFFER dbuff FOR eg-mdetail. 
    DEFINE BUFFER buff-action FOR eg-action.

    FOR EACH his-action:
        DELETE his-action.
    END.
    
    FOR EACH dbuff WHERE dbuff.maintainnr EQ mainNo AND dbuff.KEY = 1 NO-LOCK,
        FIRST buff-action WHERE buff-action.actionnr EQ dbuff.nr NO-LOCK:
        CREATE his-action.
        ASSIGN 
            his-action.action-mainnr    = dbuff.maintainnr 
            his-action.action-nr        = dbuff.nr 
            his-action.action-nm        = buff-action.bezeich
            his-action.create-date      = dbuff.create-date
            his-action.create-time      = dbuff.create-time
            his-action.time-str         = STRING(dbuff.create-time , "HH:MM:SS")
            his-action.create-by        = dbuff.create-by 
        .
    END.
END.

PROCEDURE create-alert:
    DEF VAR b AS CHAR.
    DEF BUFFER qbuff FOR eg-alert.

    FOR EACH send-alert:
        DELETE send-alert.
    END.
    
    FOR EACH eg-alert WHERE eg-alert.fromfile = "3" AND eg-alert.reqnr = mainno NO-LOCK:
        FIND FIRST eg-mobilenr WHERE eg-mobilenr.nr = eg-alert.sendto NO-LOCK NO-ERROR.
        IF AVAILABLE eg-mobilenr THEN b = eg-mobilenr.NAME.
        ELSE b = "Staff Record Not Found".

        CREATE send-alert.
        ASSIGN  send-alert.alert-date      = eg-alert.create-date
                send-alert.alert-time      = eg-alert.create-time  
                send-alert.alert-str       = string(eg-alert.create-time , "HH:MM")   
                send-alert.alert-reqnr     = eg-alert.reqnr     
                send-alert.alert-msg       = eg-alert.msg    
                send-alert.alert-sendto    = eg-alert.sendto    
                send-alert.alert-sendnm    = b    
                send-alert.alert-sendnr    = eg-alert.sendnr    
                send-alert.alert-msgstatus = eg-alert.msgstatus
                send-alert.alert-mstat     = alert-str[eg-alert.msgstatus].    
    END.

END.

PROCEDURE GetAction:
    DEFINE INPUT PARAMETER rMaintask AS INTEGER NO-UNDO.
    DEF BUFFER qbuff FOR eg-Action.
    DEF BUFFER dbuff FOR eg-mdetail. 

    /*RUN create-action.*/

    FOR EACH action :
        DELETE action.
    END.

    /*FD for web*/
    FOR EACH qbuff WHERE qbuff.usefor NE 2 NO-LOCK:
        CREATE action.
        ASSIGN 
            action.actionnr = qbuff.actionnr
            action.bezeich = qbuff.bezeich
            action.maintask = qbuff.maintask
            action.SELECTED = NO
        .
    END.

    /* Comment FD
    FOR EACH qbuff WHERE qbuff.maintask = rMaintask AND qbuff.usefor NE 2 NO-LOCK :
        FIND FIRST dbuff WHERE dbuff.maintainnr = mainNo AND dbuff.KEY = 1 AND dbuff.nr = qbuff.actionnr NO-LOCK NO-ERROR.
        IF AVAILABLE dbuff THEN
        DO:
        END. 
        ELSE
        DO:
            CREATE action.
            ASSIGN action.actionnr = qbuff.actionnr
               action.bezeich = qbuff.bezeich
               action.maintask = qbuff.maintask.
        END.          
    END.
    */
END.
/*
PROCEDURE create-action:
    DEF BUFFER qbuff FOR eg-action.

    FOR EACH action:
        DELETE action.
    END.

    FOR EACH qbuff NO-LOCK:
        CREATE action.
        ASSIGN action.actionnr = qbuff.actionnr
           action.bezeich = qbuff.bezeich
           action.maintask = qbuff.maintask
           action.SELECTED = NO.
    END.                                    
END.
*/
PROCEDURE get-guestname:
    DEF INPUT PARAM h-zinr AS CHAR.
    FIND FIRST resline1 WHERE resline1.active-flag = 1 AND resline1.zinr = h-zinr /*"415" h-zinr*/ 
        AND resline1.resstatus NE 13 USE-INDEX zinr_index NO-LOCK NO-ERROR.
    IF AVAILABLE resline1 THEN
    DO:

        FIND FIRST guest1 WHERE guest1.gastnr = resline1.gastnrmember
            USE-INDEX gastnr_index NO-LOCK NO-ERROR.
        IF AVAILABLE guest1 THEN
        DO:
            guestname = guest1.NAME + " " + guest1.vorname1 + ", " + 
                guest1.anrede1 + guest1.anredefirma.
        END.
    END.
    ELSE
    DO:
        FIND FIRST resline1 WHERE resline1.active-flag = 0 AND resline1.zinr = h-zinr /*"415" h-zinr*/ 
            AND resline1.resstatus NE 13 USE-INDEX zinr_index NO-LOCK NO-ERROR.
        IF AVAILABLE resline1 THEN
        DO:
            FIND FIRST guest1 WHERE guest1.gastnr = resline1.gastnrmember
                USE-INDEX gastnr_index NO-LOCK NO-ERROR.
            IF AVAILABLE guest1 THEN
            DO:
                guestname = guest1.NAME + " " + guest1.vorname1 + ", " + 
                    guest1.anrede1 + guest1.anredefirma.
            END.
        END.
        ELSE
        DO:
            guestname = "".
        END.
    END.
END.

PROCEDURE create-property:
    DEFINE BUFFER ques FOR queasy.

    FOR EACH eg-property NO-LOCK:
        CREATE t-property.
        ASSIGN 
            t-property.prop-nr = eg-property.nr
            t-property.prop-nm = eg-property.bezeich
            t-property.pzinr = eg-property.zinr
            t-property.pmain-nr = eg-property.maintask
            t-property.ploc-nr = eg-property.location.
        FIND FIRST queasy WHERE queasy.KEY = 133 
            AND queasy.number1 = eg-property.maintask NO-LOCK NO-ERROR.
        IF AVAILABLE queasy THEN
        DO:
            ASSIGN
                t-property.pmain = queasy.char1
                t-property.pcateg-nr = queasy.number2.

            FIND FIRST ques WHERE ques.KEY = 132 
                AND ques.number1 = queasy.number2 NO-LOCK NO-ERROR.
            IF AVAILABLE ques THEN t-property.pcateg = ques.char1.
        END.
        FIND FIRST eg-location WHERE eg-location.nr = eg-property.location NO-LOCK NO-ERROR.
        IF AVAILABLE eg-location THEN t-property.ploc = eg-location.bezeich.
        
    END.
END.

PROCEDURE create-pic:
    DEF BUFFER qbuff FOR eg-staff.

    DEF VAR engID AS INTEGER.

    FIND FIRST htparam WHERE htparam.paramnr = 1200 AND htparam.feldtyp = 1 NO-LOCK NO-ERROR.
    IF AVAILABLE htparam THEN
    DO:
        ASSIGN EngID = htparam.finteger.
    END.
    FOR EACH qbuff WHERE qbuff.usergroup = EngID AND qbuff.activeflag = YES NO-LOCK BY qbuff.nr:
        CREATE tpic.
        ASSIGN 
            tpic.pic-nr = qbuff.nr
            tpic.pic-nm = qbuff.NAME
            tpic.pic-dept = qbuff.usergroup.
    END.

END.

