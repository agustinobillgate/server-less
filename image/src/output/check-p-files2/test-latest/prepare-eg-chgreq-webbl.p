
DEFINE TEMP-TABLE t-zimmer LIKE zimmer
    FIELD gname-str AS CHAR  FORMAT "x(60)".
DEFINE TEMP-TABLE t-queasy LIKE queasy.
DEFINE TEMP-TABLE t-queasy130 LIKE queasy.
DEFINE TEMP-TABLE t-eg-property LIKE eg-property.
DEFINE TEMP-TABLE t-eg-request LIKE eg-request.
DEFINE TEMP-TABLE treqdetail
    FIELD reqnr AS INTEGER
    FIELD actionnr AS INTEGER
    FIELD action AS CHAR FORMAT "x(256)"
    FIELD create-date AS DATE
    FIELD create-time AS INTEGER
    FIELD create-str  AS CHAR
    FIELD create-by AS CHAR
    FIELD flag AS LOGICAL.

DEFINE TEMP-TABLE sVendor
    FIELD nr           AS CHAR FORMAT "x(2)"
    FIELD vendor-nr    AS INTEGER
    FIELD docno         AS CHAR
    FIELD reqnr       AS INTEGER
    FIELD startdate   AS DATE
    FIELD estfinishdate  AS DATE
    FIELD finishdate    AS DATE
    FIELD price         AS DECIMAL FORMAT "->>,>>>,>>>,>>9"  
    FIELD bezeich       AS CHAR     FORMAT "x(30)"
    FIELD pic           AS CHAR     FORMAT "x(30)"
    FIELD created-by    AS CHAR
    FIELD created-date   AS DATE
    FIELD created-time   AS INTEGER
    FIELD perform-nr     AS CHAR
    FIELD stat           AS CHAR.

DEFINE BUFFER rbuff FOR eg-request.
DEFINE TEMP-TABLE request1 LIKE eg-request.

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

DEFINE TEMP-TABLE tvendor
    FIELD ven-nr AS INTEGER
    FIELD ven-nm AS CHAR FORMAT "x(30)".

DEF TEMP-TABLE t-eg-location LIKE eg-location.

DEF INPUT PARAMETER pvILanguage AS INTEGER          NO-UNDO.
DEF INPUT PARAMETER reqno AS INT.
DEF INPUT PARAMETER view-first AS LOGICAL.
DEF INPUT PARAMETER user-init AS CHAR.

DEF OUTPUT PARAMETER GroupID AS INT.
DEF OUTPUT PARAMETER EngID AS INT.
DEF OUTPUT PARAMETER source-str AS CHAR.
DEF OUTPUT PARAMETER dept-str AS CHAR.
DEF OUTPUT PARAMETER strproperty AS CHAR.
DEF OUTPUT PARAMETER main-str AS CHAR.
DEF OUTPUT PARAMETER categ-str AS CHAR.
DEF OUTPUT PARAMETER sub-str AS CHAR.
DEF OUTPUT PARAMETER usr-str AS CHAR.
DEF OUTPUT PARAMETER guestname AS CHAR.
DEF OUTPUT PARAMETER sguestflag AS LOGICAL.
DEF OUTPUT PARAMETER flag1 AS INT INIT 0.
DEF OUTPUT PARAMETER flag2 AS INT INIT 0.
DEF OUTPUT PARAMETER flag3 AS INT INIT 0.
DEF OUTPUT PARAMETER s-othersflag AS LOGICAL.
DEF OUTPUT PARAMETER subtask-bez AS CHAR.
DEF OUTPUT PARAMETER avail-eg-request AS LOGICAL INIT NO.
DEF OUTPUT PARAMETER avail-eg-subtask AS LOGICAL INIT NO.
DEF OUTPUT PARAMETER avail-subtask AS LOGICAL INIT NO.
DEF OUTPUT PARAMETER t-fStat AS INT.

DEF OUTPUT PARAMETER TABLE FOR sVendor.
DEF OUTPUT PARAMETER TABLE FOR request1.
DEF OUTPUT PARAMETER TABLE FOR send-alert.
DEF OUTPUT PARAMETER TABLE FOR tvendor.
DEF OUTPUT PARAMETER TABLE FOR t-eg-location.
DEF OUTPUT PARAMETER TABLE FOR treqdetail.
DEF OUTPUT PARAMETER TABLE FOR t-eg-request.
DEF OUTPUT PARAMETER TABLE FOR t-eg-property.
DEF OUTPUT PARAMETER TABLE FOR t-queasy130.
DEF OUTPUT PARAMETER TABLE FOR t-queasy.
DEF OUTPUT PARAMETER TABLE FOR t-zimmer.

{SupertransBL.i} 
DEF VAR lvCAREA AS CHAR INITIAL "eg-chgreq".
DEFINE VARIABLE alert-str AS CHAR FORMAT "x(30)" EXTENT 3.
alert-str[1] = translateextended("Successfully", lvcarea, "").
alert-str[2] = translateextended("Failed", lvcarea, "").
alert-str[3] = translateextended("Pending", lvcarea, "").
DEF BUFFER subtask1 FOR eg-subtask.
DEF BUFFER resline1 FOR res-line.              
DEF BUFFER guest1 FOR guest.              

RUN Define-Group.
RUN define-engineering.
RUN define-sms.

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

RUN create-tvendor.
RUN create-alert.
RUN create-request.
RUN getvendor.
RUN create-reqdetail.

FIND FIRST request1.   /* SY: 21/05/2013 */

IF view-first = NO THEN
DO:
    FIND FIRST eg-request WHERE 
        eg-request.reqnr = reqno AND eg-request.reqstatus = 1 NO-LOCK NO-ERROR.
    IF AVAILABLE eg-request THEN 
    DO:
        CREATE t-eg-request.
        BUFFER-COPY eg-request TO t-eg-request.
        avail-eg-request = YES.
    END.

    FIND FIRST eg-subtask WHERE eg-subtask.sub-code = request1.sub-task NO-LOCK NO-ERROR.
    IF AVAILABLE eg-subtask THEN 
    DO:
        s-othersflag = eg-subtask.othersflag.
        avail-eg-subtask = YES.
    END.
END.

/*FOR EACH eg-property:
    CREATE t-eg-property.
    BUFFER-COPY eg-property TO t-eg-property.
END.*/

FOR EACH queasy WHERE KEY = 130:
    CREATE t-queasy130.
    BUFFER-COPY queasy TO t-queasy130.
END.

FOR EACH queasy WHERE KEY = 132 OR KEY = 19 OR KEY = 135:
    CREATE t-queasy.
    BUFFER-COPY queasy TO t-queasy.
END.

FIND FIRST request1.
FIND FIRST subtask1 WHERE subtask1.dept-nr = request1.deptnum AND 
    subtask1.main-nr = request1.maintask AND subtask1.sub-code = 
    request1.sub-task NO-LOCK NO-ERROR.
IF AVAILABLE subtask1 THEN 
DO:
    avail-subtask = YES.
    subtask-bez = subtask1.bezeich.
END.
FIND FIRST eg-request WHERE eg-request.reqnr = reqno NO-LOCK NO-ERROR.
IF AVAILABLE eg-request THEN t-fStat = eg-request.reqstatus.    
ELSE t-fStat = 0.

PROCEDURE Define-sms:
 
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

PROCEDURE Define-Group:
    FIND FIRST bediener WHERE bediener.userinit = user-init NO-LOCK NO-ERROR.
    IF AVAILABLE bediener THEN
    DO:
        ASSIGN GroupID = bediener.user-group.
    END.
END.

PROCEDURE create-tvendor:
    FOR EACH tvendor:
        DELETE tvendor.
    END.

    FOR EACH eg-vendor NO-LOCK:
        CREATE tvendor.
        ASSIGN tvendor.ven-nr = eg-vendor.vendor-nr
               tvendor.ven-nm = eg-vendor.bezeich.
    END.
END.

PROCEDURE create-alert:
    DEF VAR b AS CHAR.
    DEF BUFFER qbuff FOR eg-alert.

    FOR EACH send-alert:
        DELETE send-alert.
    END.
    
    FOR EACH eg-alert WHERE eg-alert.fromfile = "1" AND eg-alert.reqnr = reqno  OR 
        eg-alert.fromfile = "2" AND eg-alert.reqnr = reqno  NO-LOCK:

        FIND FIRST eg-staff WHERE eg-staff.nr = eg-alert.sendto NO-LOCK NO-ERROR.
        IF AVAILABLE eg-staff THEN b = eg-staff.NAME.
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

PROCEDURE create-request:
    DEF VAR blzin AS INTEGER NO-UNDO.
    DEF BUFFER queasy1 FOR queasy.
    DEF BUFFER queasy2 FOR queasy.

    DEF BUFFER sbuff   FOR eg-subtask.
    DEF BUFFER usr     FOR eg-staff.
    DEF BUFFER gbuff   FOR guest.

    FOR EACH request1:
        DELETE request1.
    END.

    CREATE request1.
    FIND FIRST rbuff WHERE rbuff.reqnr = reqNo EXCLUSIVE-LOCK NO-ERROR.
    IF NOT AVAILABLE rbuff THEN RETURN.
    ELSE 
    DO:
        BUFFER-COPY rbuff TO request1.
        FIND FIRST queasy1 WHERE queasy1.KEY = 130 AND queasy1.number1 = request1.SOURCE
            AND queasy1.char1 NE "" AND queasy1.logi1 = NO AND queasy1.deci1 = 0
            AND queasy1.date1 = ? USE-INDEX queasyint_ix NO-LOCK NO-ERROR.
        IF AVAILABLE queasy1 THEN
            source-str = queasy1.char1.

        FIND FIRST queasy1 WHERE queasy1.KEY = 19 AND queasy1.number1 = request1.deptnum
            NO-LOCK NO-ERROR.
        IF AVAILABLE queasy1 THEN
            dept-str = queasy1.char3.
        
            FIND FIRST eg-property WHERE eg-property.nr = request1.propertynr NO-LOCK NO-ERROR.
            IF AVAILABLE eg-property THEN
            DO:
                strproperty = eg-property.bezeich.
                request1.maintask = eg-property.maintask.

                FIND FIRST queasy1 WHERE queasy1.KEY = 133 AND queasy1.number1 = eg-property.maintask
                    AND queasy1.char1 NE "" AND queasy1.logi1 = NO AND queasy1.deci1 = 0
                    AND queasy1.date1 = ? USE-INDEX queasyint_ix NO-LOCK NO-ERROR.
                IF AVAILABLE queasy1 THEN
                DO:
                    main-str  = queasy1.char1.

                    FIND FIRST queasy2 WHERE queasy2.KEY = 132 AND queasy2.number1 = queasy1.number2
                        AND queasy2.char1 NE "" AND queasy2.logi1 = NO AND queasy2.deci1 = 0
                        AND queasy2.date1 = ? USE-INDEX queasyint_ix NO-LOCK NO-ERROR.
                    IF AVAILABLE queasy2 THEN
                    do: 
                        request1.category = queasy2.number1.
                        categ-str  = queasy2.char1.
                    END.
                END.   
            END.
            ELSE
            DO:
                strproperty = "".
                main-str = "".

                FIND FIRST queasy1 WHERE queasy1.KEY = 133 AND queasy1.number1 = request1.maintask
                    AND queasy1.char1 NE "" AND queasy1.logi1 = NO AND queasy1.deci1 = 0
                    AND queasy1.date1 = ? USE-INDEX queasyint_ix NO-LOCK NO-ERROR.
                IF AVAILABLE queasy1 THEN
                DO:

                    main-str  = queasy1.char1.

                    FIND FIRST queasy2 WHERE queasy2.KEY = 132 AND queasy2.number1 = queasy1.number2
                        AND queasy2.char1 NE "" AND queasy2.logi1 = NO AND queasy2.deci1 = 0
                        AND queasy2.date1 = ? USE-INDEX queasyint_ix NO-LOCK NO-ERROR.
                    IF AVAILABLE queasy2 THEN
                    do: 
                        request1.category = queasy2.number1.
                        categ-str  = queasy2.char1.
                    END.
                END.
                flag1 = 1.
            END.
            
            flag2 = 1.

            FIND FIRST eg-location WHERE eg-location.nr = request1.reserve-int AND eg-location.guestflag = YES NO-LOCK NO-ERROR.  
            IF AVAILABLE eg-location THEN
            DO:
                ASSIGN sguestflag = YES
                    request1.reserve-int = 0.
                flag3 = 1.
            END.
            ELSE
            DO:
                ASSIGN sguestflag = NO.
                flag3 = 2.
            END.
            
        FIND FIRST sbuff WHERE 
            sbuff.sub-code = request1.sub-task NO-LOCK NO-ERROR.
        IF AVAILABLE sbuff THEN
        DO:
            IF sbuff.othersflag = YES THEN
            DO:
                sub-str =  rbuff.subtask-bezeich.
            END.
            ELSE
            DO:
                sub-str = sbuff.bezeich.
            END.
        END.

        FIND FIRST usr WHERE usr.nr = request1.assign-to NO-LOCK
            NO-ERROR.
        IF AVAILABLE usr THEN 
            usr-str = usr.name.

        FIND FIRST gbuff WHERE gbuff.gastnr = request1.gastnr USE-INDEX gastnr_index 
            NO-LOCK NO-ERROR.
        IF AVAILABLE gbuff THEN
            guestname = gbuff.NAME + " " + gbuff.vorname1 + ", " + 
                gbuff.anrede1 + gbuff.anredefirma.
    END.
END.


PROCEDURE getVendor:
    DEFINE BUFFER vbuff FOR eg-vperform.
    DEFINE BUFFER qbuff FOR eg-vendor.

    FOR EACH vbuff WHERE vbuff.reqnr =  request1.reqnr AND vbuff.logi1 = NO NO-LOCK:
        CREATE svendor.
        ASSIGN svendor.reqnr = reqno
            svendor.vendor-nr = vbuff.vendor-nr
            svendor.docno   = vbuff.DOcumentno
            svendor.startdate = vbuff.startdate
            svendor.estfinishdate = vbuff.estfinishdate
            svendor.finishdate = vbuff.finishdate
            svendor.price = vbuff.price
            svendor.bezeich = vbuff.bezeich
            svendor.pic = vbuff.pic 
            svendor.perform-nr = vbuff.perform-nr 
            svendor.stat = "1".
    END.
END.

PROCEDURE create-reqdetail:
    DEF BUFFER actBuff FOR eg-action.
    DEF VAR str AS CHAR FORMAT "x(256)".

    FOR EACH treqdetail:
        DELETE treqdetail.
    END.

    FOR EACH eg-reqdetail WHERE eg-reqdetail.reqnr = reqno AND eg-reqdetail.action NE "" NO-LOCK:

        CREATE treqdetail.
        ASSIGN treqdetail.reqnr         = eg-reqdetail.reqnr 
               treqdetail.actionnr      = eg-reqdetail.actionnr
               treqdetail.action        = eg-reqdetail.action
                treqdetail.create-date  = eg-reqdetail.create-date
                treqdetail.create-time  = eg-reqdetail.create-time
                treqdetail.create-str   = STRING(eg-reqdetail.create-time, "HH:MM:SS")
                treqdetail.create-by    = eg-reqdetail.create-by
                treqdetail.flag         = YES .
    END.

END.

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
