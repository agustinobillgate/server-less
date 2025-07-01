
DEFINE TEMP-TABLE t-zimmer LIKE zimmer.

DEFINE TEMP-TABLE maintain
    FIELD maintainnr    AS INTEGER      FORMAT ">>>>>>9"
    FIELD workdate      AS DATE
    FIELD estworkdate   AS DATE
    FIELD donedate      AS DATE
    FIELD TYPE          AS INTEGER
    FIELD maintask      AS INTEGER
    FIELD location      AS INTEGER
    FIELD zinr          AS CHAR
    FIELD propertynr    AS INTEGER
    FIELD pic           AS INTEGER
    FIELD cancel-date   AS DATE
    FIELD cancel-time   AS INTEGER
    FIELD cancel-str    AS CHAR     FORMAT "x(24)"
    FIELD cancel-by     AS CHAR
    FIELD categnr       AS INTEGER

    INDEX alldatum  estworkdate workdate.

DEFINE TEMP-TABLE tproperty
    FIELD prop-nr AS INTEGER
    FIELD prop-nm AS CHAR FORMAT "x(24)" COLUMN-LABEL "Object Item"
    FIELD prop-selected AS LOGICAL INITIAL NO
    FIELD pcateg-nr AS INTEGER
    FIELD pcateg AS CHAR
    FIELD pmain-nr AS INTEGER
    FIELD pmain AS CHAR
    FIELD ploc-nr AS INTEGER
    FIELD ploc  AS CHAR
    FIELD pzinr    AS CHAR.

DEFINE TEMP-TABLE troom
    FIELD room-nm AS CHAR FORMAT "x(24)" COLUMN-LABEL "Room"
    FIELD room-Selected AS LOGICAL INITIAL NO.

DEFINE TEMP-TABLE tMaintask
    FIELD Main-nr  AS INTEGER 
    FIELD Main-nm  AS CHAR FORMAT "x(24)" COLUMN-LABEL "Object"
    FIELD categ-nr AS INTEGER               /*FD for web*/
    FIELD categ-nm AS CHAR  FORMAT "x(24)"  /*FD for web*/
    FIELD main-selected AS LOGICAL INITIAL NO.

DEFINE TEMP-TABLE tpic
    FIELD pic-nr AS INTEGER
    FIELD pic-nm AS CHAR FORMAT "x(24)" COLUMN-LABEL "Pic"
    FIELD pic-selected AS LOGICAL INITIAL NO
    FIELD pic-Dept AS INTEGER.

DEFINE TEMP-TABLE tStatus
    FIELD stat-nr AS INTEGER
    FIELD stat-nm AS CHAR       FORMAT "x(24)"
    FIELD stat-selected AS LOGICAL INITIAL NO.

DEFINE TEMP-TABLE dept-link 
    FIELD dept-nr AS INTEGER
    FIELD dept-nm AS CHAR.

DEFINE TEMP-TABLE tLocation
    FIELD loc-nr  AS INTEGER 
    FIELD loc-nm  AS CHAR FORMAT "x(24)" COLUMN-LABEL "Location"
    FIELD loc-selected AS LOGICAL INITIAL NO
    FIELD loc-guest    AS LOGICAL INITIAL NO.

DEFINE TEMP-TABLE tcategory
    FIELD categ-nr AS INTEGER
    FIELD categ-nm AS CHAR  FORMAT "x(24)"
    FIELD categ-selected AS LOGICAL INITIAL NO.

DEFINE TEMP-TABLE t-eg-maintain LIKE eg-maintain.

DEF INPUT PARAMETER user-init AS CHAR.
DEF INPUT PARAMETER all-room AS LOGICAL.

DEF OUTPUT PARAMETER GroupID AS INT.
DEF OUTPUT PARAMETER EngID AS INT.
DEF OUTPUT PARAMETER p-992 AS LOGICAL.
DEF OUTPUT PARAMETER TABLE FOR maintain.
DEF OUTPUT PARAMETER TABLE FOR tproperty.
DEF OUTPUT PARAMETER TABLE FOR troom.
DEF OUTPUT PARAMETER TABLE FOR tMaintask.
DEF OUTPUT PARAMETER TABLE FOR tpic.
DEF OUTPUT PARAMETER TABLE FOR tStatus.
DEF OUTPUT PARAMETER TABLE FOR dept-link.
DEF OUTPUT PARAMETER TABLE FOR tLocation.
DEF OUTPUT PARAMETER TABLE FOR tcategory.
DEF OUTPUT PARAMETER TABLE FOR t-eg-maintain.
DEF OUTPUT PARAMETER TABLE FOR t-zimmer.

/*FD April 21, 2020*/
DEFINE VARIABLE ci-date AS DATE NO-UNDO.
RUN htpdate.p(87, OUTPUT ci-date).
/*End FD*/

RUN htplogic.p(992, OUTPUT p-992).
RUN define-engineering.
RUN define-group.
RUN create-Related-dept.

RUN create-status.
RUN create-category.
RUN create-pic.
RUN create-location.

FOR EACH tcategory :
    ASSIGN tcategory.categ-selected = YES.
END.

RUN create-maintask.

FOR EACH tlocation :
    ASSIGN tlocation.loc-selected = YES.
END.
RUN create-room.
RUN create-property.
RUN create-maintain.

FOR EACH eg-maintain:
    CREATE t-eg-maintain.
    BUFFER-COPY eg-maintain TO t-eg-maintain.
END.

FOR EACH zimmer:
    CREATE t-zimmer.
    BUFFER-COPY zimmer TO t-zimmer.
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
        ASSIGN EngID = 0.
        /*MTHIDE MESSAGE NO-PAUSE.
        MESSAGE translateExtended("Group No for Engineering Modul not yet defined.", lvCAREA, "":U) 
            SKIP 
            translateExtended( "Please contact your next VHP Support for further Information.", lvCAREA, "":U) 
            VIEW-AS ALERT-BOX INFORMATION. 
        */
    END.
END.

PROCEDURE create-Related-dept:
    DEF VAR i AS INTEGER NO-UNDO.
    DEF VAR c AS INTEGER NO-UNDO.
    DEF BUFFER qbuff FOR queasy.
        
    FOR EACH dept-link:
        DELETE dept-link.
    END.

    FIND FIRST queasy WHERE queasy.KEY = 19 AND queasy.number1 = EngId
        NO-LOCK NO-ERROR.
    IF AVAILABLE queasy THEN 
    DO: 
        CREATE dept-link.
        ASSIGN

            dept-link.dept-nr   = EngId
            dept-link.dept-nm   = queasy.char3
            .

        DO i = 1 TO NUM-ENTRIES(queasy.char2, ";"):
            c = INTEGER(ENTRY(i, queasy.char2, ";")).
            FIND FIRST qbuff WHERE qbuff.KEY = 19 AND qbuff.number1 = 
                INTEGER(ENTRY(i, queasy.char2, ";")) NO-LOCK NO-ERROR.
            IF AVAILABLE qbuff THEN
            DO:
                CREATE dept-link.
                ASSIGN 
                    dept-link.dept-nr   = c
                    dept-link.dept-nm   = qbuff.char3
                    .
            END.                
        END.
    END.
END.

PROCEDURE create-status:
    FOR EACH tStatus:
        DELETE tStatus. 
    END.
    CREATE tStatus.
    ASSIGN tStatus.stat-nr = 1
           tStatus.stat-nm = "Scheduled"
           tstatus.stat-selected = NO.

    CREATE tStatus.
    ASSIGN tStatus.stat-nr = 2
           tStatus.stat-nm = "Processed"
           tstatus.stat-selected = NO.

    CREATE tStatus.
    ASSIGN tStatus.stat-nr = 3
           tStatus.stat-nm = "Done"
           tstatus.stat-selected = NO.
END.

PROCEDURE create-category:
    DEF BUFFER qbuff FOR queasy.
    FOR EACH tcategory:
        DELETE tcategory.
    END.

    FOR EACH qbuff WHERE qbuff.KEY = 132 NO-LOCK:
        CREATE tcategory.
        ASSIGN tcategory.categ-nr = qbuff.number1
            tcategory.categ-nm = qbuff.char1
            tcategory.categ-selected = NO.
    END.
END.

PROCEDURE create-pic:
    DEF BUFFER qbuff FOR eg-staff.
    DEF BUFFER qbuff1 FOR bediener.

    FOR EACH tpic:
        DELETE tpic.
    END.
    
    CREATE tpic.
    ASSIGN  tpic.pic-nr = 0
            tpic.pic-nm = ""
            tpic.pic-selected = NO.

    FOR EACH qbuff WHERE qbuff.usergroup = EngID AND qbuff.activeflag = YES NO-LOCK BY qbuff.nr:
        CREATE tpic.
        ASSIGN 
            tpic.pic-nr = qbuff.nr
            tpic.pic-nm = qbuff.NAME
            tpic.pic-dept = qbuff.usergroup
            tpic.pic-selected = NO.
    END.

END.

PROCEDURE create-Location:
    DEF BUFFER qbuff FOR eg-location.

    FOR EACH tLocation:
        DELETE tLocation.
    END.

    CREATE tlocation.
    ASSIGN tlocation.loc-nr = 0
        tlocation.loc-nm = "Undefine"
        tlocation.loc-guest = NO.

    FOR EACH qbuff NO-LOCK:
        IF qbuff.guestflag = YES THEN
        DO:
            CREATE tLocation.
            ASSIGN tLocation.loc-nr = qbuff.nr
                tLocation.loc-nm = qbuff.bezeich
                tlocation.loc-selected = YES
                tlocation.loc-guest = YES.
        END.
        ELSE
        DO:
            CREATE tLocation.
            ASSIGN tLocation.loc-nr = qbuff.nr
                tLocation.loc-nm = qbuff.bezeich
                tlocation.loc-selected = YES
                tlocation.loc-guest = NO.
        END.
    END.                                    
END.

PROCEDURE create-maintask:
    DEF BUFFER qbuff FOR queasy.
    DEF BUFFER comCategory FOR tcategory.

    FOR EACH tMaintask:
        DELETE tMaintask.
    END.

    FOR EACH comCategory WHERE comCategory.categ-SELECTED NO-LOCK:
        FOR EACH qbuff WHERE qbuff.KEY = 133 AND qbuff.number2 = comcategory.categ-nr NO-LOCK:
            CREATE tMaintask.
            ASSIGN tMaintask.Main-nr = qbuff.number1
                tMaintask.Main-nm = qbuff.char1
                tMaintask.categ-nr = comcategory.categ-nr
                tMaintask.categ-nm = comcategory.categ-nm 
                tmaintask.main-selected = YES.
        END.
    END.                                    
END.

PROCEDURE create-room:
    DEF VAR i AS INTEGER NO-UNDO.
    DEF BUFFER qbuff FOR zimmer.
    DEF BUFFER qbuff1 FOR tlocation.

    FOR EACH troom:
        DELETE troom.
    END.    

    FIND FIRST qbuff1 WHERE qbuff1.loc-selected = YES AND qbuff1.loc-guest = YES NO-LOCK NO-ERROR.
    IF AVAILABLE qbuff1 THEN
    DO:
        FOR EACH qbuff NO-LOCK:
            CREATE troom.
            ASSIGN 
                troom.room-nm = qbuff.zinr
                troom.room-SELECTED = NO.
        END.
    END.
    ELSE
    DO:

    END.
END.

PROCEDURE create-property:
    DEF BUFFER qbuff FOR eg-property.
    DEF BUFFER comlocat FOR tlocation.
    DEF BUFFER comMain FOR tmaintask.
    DEF BUFFER comRoom FOR troom.
    DEF BUFFER ques FOR queasy.

    FOR EACH tproperty:
        DELETE tproperty.
    END.

    IF all-room THEN
        FOR EACH troom:
            ASSIGN troom.room-selected = YES.
        END.

    CREATE tproperty.
    ASSIGN tproperty.prop-nr = 0
        tproperty.prop-nm = "Undefine".

    FOR EACH comlocat WHERE comlocat.loc-selected NO-LOCK:

        IF comlocat.loc-guest = YES THEN
        DO:
            FOR EACH qbuff WHERE qbuff.location = comlocat.loc-nr USE-INDEX mtloczin_x NO-LOCK,
                FIRST commain WHERE commain.main-nr = qbuff.maintask AND commain.main-selected NO-LOCK,
                FIRST comroom WHERE comroom.room-nm = qbuff.zinr AND comroom.room-selected NO-LOCK:

                CREATE tproperty.
                ASSIGN tproperty.prop-nr = qbuff.nr
                       tproperty.prop-nm = qbuff.bezeich + "(" + trim(string(qbuff.nr , ">>>>>>9")) + ")"
                       tproperty.pzinr   = qbuff.zinr 
                       tproperty.pmain-nr = qbuff.maintask
                       tproperty.ploc-nr  = qbuff.location.
            
                FIND FIRST queasy WHERE queasy.KEY= 133 AND queasy.number1 = qbuff.maintask NO-LOCK NO-ERROR.
                IF AVAILABLE queasy THEN
                DO:
                    ASSIGN tproperty.pmain = queasy.char1
                           tproperty.pcateg-nr = queasy.number2.

                    FIND FIRST ques WHERE ques.KEY = 132 AND ques.number1 = queasy.number2 NO-LOCK NO-ERROR.
                    IF AVAILABLE ques THEN
                    DO:
                        ASSIGN tproperty.pcateg = ques.char1.
                    END.

                END.
                ELSE
                DO:
                    ASSIGN tproperty.pmain = ""
                           tproperty.pcateg-nr = 0
                           tproperty.pcateg = "".
                END.
            
                FIND FIRST eg-location WHERE eg-location.nr = qbuff.location NO-LOCK NO-ERROR.
                IF AVAILABLE eg-location THEN
                    ASSIGN tproperty.ploc = eg-location.bezeich.
                ELSE
                    ASSIGN  tproperty.ploc = "".
            END.
        END.
        ELSE
        DO:

            FOR EACH qbuff WHERE qbuff.location = comlocat.loc-nr USE-INDEX location_ix NO-LOCK,
                FIRST commain WHERE commain.main-nr = qbuff.maintask AND commain.main-selected NO-LOCK:

                CREATE tproperty.
                ASSIGN tproperty.prop-nr = qbuff.nr
                       tproperty.prop-nm = qbuff.bezeich + "(" + trim(string(qbuff.nr , ">>>>>>9")) + ")"
                       tproperty.pzinr   = qbuff.zinr 
                       tproperty.pmain-nr = qbuff.maintask
                       tproperty.ploc-nr  = qbuff.location.
            
                FIND FIRST queasy WHERE queasy.KEY= 133 AND queasy.number1 = qbuff.maintask NO-LOCK NO-ERROR.
                IF AVAILABLE queasy THEN
                DO:
                    ASSIGN tproperty.pmain = queasy.char1
                           tproperty.pcateg-nr = queasy.number2.

                    FIND FIRST ques WHERE ques.KEY = 132 AND ques.number1 = queasy.number2 NO-LOCK NO-ERROR.
                    IF AVAILABLE ques THEN
                    DO:
                        ASSIGN tproperty.pcateg = ques.char1.
                    END.

                END.
                ELSE
                DO:
                    ASSIGN tproperty.pmain = ""
                           tproperty.pcateg-nr = 0
                           tproperty.pcateg = "".
                END.
            
                FIND FIRST eg-location WHERE eg-location.nr = qbuff.location NO-LOCK NO-ERROR.
                IF AVAILABLE eg-location THEN
                    ASSIGN tproperty.ploc = eg-location.bezeich.
                ELSE
                    ASSIGN  tproperty.ploc = "".
            END.
        END.
    END.
END.

PROCEDURE create-maintain:

    DEF BUFFER qbuff FOR eg-maintain.

    DEF VAR strdatetime     AS CHAR NO-UNDO.
    DEF VAR ex-finishstr    AS CHAR NO-UNDO.
    DEF VAR cancelstr       AS CHAR NO-UNDO.

    FOR EACH maintain:
        DELETE maintain.
    END.

    FOR EACH qbuff WHERE qbuff.delete-flag = YES AND qbuff.cancel-date = ci-date NO-LOCK:

        cancelstr  = string(qbuff.cancel-date , "99/99/99") + " " + STRING(qbuff.cancel-time , "HH:MM").

        IF qbuff.propertynr NE 0 THEN
        DO:
            FIND FIRST tproperty WHERE tproperty.prop-nr = qbuff.propertynr NO-LOCK NO-ERROR.
            IF AVAILABLE tproperty THEN
            DO:
                CREATE maintain.
                ASSIGN  maintain.maintainnr     = qbuff.maintainnr
                        maintain.workdate       = qbuff.workdate
                        maintain.estworkdate    = qbuff.estworkdate
                        maintain.donedate       = qbuff.donedate
                        maintain.TYPE           = qbuff.TYPE
                        maintain.maintask       = tproperty.pmain-nr
                        maintain.location       = tproperty.ploc-nr
                        maintain.propertynr     = qbuff.propertynr
                        maintain.pic            = qbuff.pic
                        maintain.cancel-date    = qbuff.cancel-date
                        maintain.cancel-time    = qbuff.cancel-time
                        maintain.cancel-str     = cancelstr
                        maintain.cancel-by      = qbuff.cancel-by. 

            END.
            ELSE
            DO:

            END.
        END.
        ELSE
        DO:
            CREATE maintain.
            ASSIGN  maintain.maintainnr     = qbuff.maintainnr
                    maintain.workdate       = qbuff.workdate
                    maintain.estworkdate    = qbuff.estworkdate
                    maintain.donedate       = qbuff.donedate
                    maintain.TYPE           = qbuff.TYPE
                    maintain.maintask       = tproperty.pmain-nr
                    maintain.location       = qbuff.location 
                    maintain.zinr           = qbuff.zinr
                    maintain.propertynr     = qbuff.propertynr
                    maintain.pic            = qbuff.pic
                    maintain.cancel-date    = qbuff.cancel-date
                    maintain.cancel-time    = qbuff.cancel-time
                    maintain.cancel-str     = cancelstr
                    maintain.cancel-by      = qbuff.cancel-by.            

        END.
    END.
END.
