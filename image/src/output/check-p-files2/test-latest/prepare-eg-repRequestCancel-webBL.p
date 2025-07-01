
DEFINE TEMP-TABLE tsource
    FIELD source-nr AS INTEGER
    FIELD source-nm AS CHAR FORMAT "x(24)"
    FIELD source-selected AS LOGICAL INITIAL NO.

DEFINE TEMP-TABLE tsubtask
    FIELD sub-nr AS CHAR
    FIELD sub-nm AS CHAR   FORMAT "x(24)"
    FIELD sub-selected AS LOGICAL INITIAL NO.

DEFINE TEMP-TABLE tpic
    FIELD pic-nr        AS INTEGER
    FIELD pic-nm        AS CHAR FORMAT "x(24)" COLUMN-LABEL "Pic"
    FIELD pic-selected  AS LOGICAL INITIAL NO
    FIELD pic-Dept      AS INTEGER.

DEFINE TEMP-TABLE tproperty
    FIELD prop-nr       AS INTEGER
    FIELD prop-nm       AS CHAR FORMAT "x(30)" COLUMN-LABEL "Object Item"
    FIELD prop-selected AS LOGICAL INITIAL NO
    FIELD pmain-nr      AS INTEGER
    FIELD pmain         AS CHAR
    FIELD pcateg-nr     AS INTEGER
    FIELD pcateg        AS CHAR
    FIELD ploc-nr       AS INTEGER
    FIELD ploc          AS CHAR
    FIELD pzinr         AS CHAR.

DEFINE TEMP-TABLE tMaintask
    FIELD Main-nr  AS INTEGER 
    FIELD Main-nm  AS CHAR FORMAT "x(24)" COLUMN-LABEL "Object"
    FIELD main-selected AS LOGICAL INITIAL NO
    /*gerald kebutuhan filter WEB API*/
    FIELD categ-nr AS INTEGER
    FIELD categ-nm AS CHAR
    .

DEFINE TEMP-TABLE troom
    FIELD room-nm AS CHAR FORMAT "x(24)" COLUMN-LABEL "Room"
    FIELD room-Selected AS LOGICAL INITIAL NO.

DEFINE TEMP-TABLE tStatus
    FIELD stat-nr AS INTEGER
    FIELD stat-nm AS CHAR       FORMAT "x(24)"
    FIELD stat-selected AS LOGICAL INITIAL NO.

DEFINE TEMP-TABLE tLocation
    FIELD loc-nr  AS INTEGER 
    FIELD loc-nm  AS CHAR FORMAT "x(24)" COLUMN-LABEL "Location"
    FIELD loc-selected AS LOGICAL INITIAL YES
    FIELD loc-guest    AS LOGICAL INITIAL NO.

DEFINE TEMP-TABLE tcategory
    FIELD categ-nr AS INTEGER
    FIELD categ-nm AS CHAR  FORMAT "x(24)"
    FIELD categ-selected AS LOGICAL INITIAL NO.

DEF INPUT PARAMETER all-maintask AS LOGICAL.
DEF INPUT PARAMETER all-room AS LOGICAL.
DEF INPUT PARAMETER user-init AS CHAR.
DEF OUTPUT PARAMETER EngID AS INT.
DEF OUTPUT PARAMETER GroupID AS INT.
DEF OUTPUT PARAMETER ci-date AS DATE.
DEF OUTPUT PARAMETER TABLE FOR tsource.
DEF OUTPUT PARAMETER TABLE FOR tsubtask.
DEF OUTPUT PARAMETER TABLE FOR tpic.
DEF OUTPUT PARAMETER TABLE FOR tproperty.
DEF OUTPUT PARAMETER TABLE FOR tMaintask.
DEF OUTPUT PARAMETER TABLE FOR troom.
DEF OUTPUT PARAMETER TABLE FOR tStatus.
DEF OUTPUT PARAMETER TABLE FOR tLocation.
DEF OUTPUT PARAMETER TABLE FOR tcategory.

RUN define-group.
RUN define-engineering.

RUN create-status.

RUN create-location.
RUN create-room.
RUN create-property.
RUN create-pic.
RUN create-subtask.
RUN create-source.
RUN create-category.

FOR EACH tcategory :
    ASSIGN tcategory.categ-selected = YES.
END.

RUN create-maintask.

FOR EACH tlocation :
    ASSIGN tlocation.loc-selected = YES.
END.

FIND FIRST htparam WHERE htparam.paramnr = 87 NO-LOCK. 
ci-date = htparam.fdate. 


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

PROCEDURE Define-Group:
    FIND FIRST bediener WHERE bediener.userinit = user-init NO-LOCK NO-ERROR.
    IF AVAILABLE bediener THEN
    DO:
        ASSIGN GroupID = bediener.user-group.
    END.
END.

PROCEDURE create-status:
    FOR EACH tStatus:
        DELETE tStatus. 
    END.
    CREATE tStatus.
    ASSIGN tStatus.stat-nr = 1
           tStatus.stat-nm = "New"
           tstatus.stat-selected = NO.

    CREATE tStatus.
    ASSIGN tStatus.stat-nr = 2
           tStatus.stat-nm = "Processed"
           tstatus.stat-selected = NO.

    CREATE tStatus.
    ASSIGN tStatus.stat-nr = 3
           tStatus.stat-nm = "Done"
           tstatus.stat-selected = NO.

    CREATE tStatus.
    ASSIGN tStatus.stat-nr = 4
           tStatus.stat-nm = "Postponed"
           tstatus.stat-selected = NO.
    
    CREATE tStatus.
    ASSIGN tStatus.stat-nr = 5
           tStatus.stat-nm = "Closed"
           tstatus.stat-selected = NO.

END.

PROCEDURE create-Location:
    /*DEF BUFFER qbuff FOR eg-location. FT serverless*/

    FOR EACH tLocation:
        DELETE tLocation.
    END.

    CREATE tlocation.
    ASSIGN tlocation.loc-nr = 0
        tlocation.loc-nm = "Undefine"
        tlocation.loc-guest = NO.

    FOR EACH eg-location NO-LOCK:
        IF eg-location.guestflag = YES THEN
        DO:
            CREATE tLocation.
            ASSIGN tLocation.loc-nr = eg-location.nr
                tLocation.loc-nm = eg-location.bezeich
                tlocation.loc-selected = YES
                tlocation.loc-guest = YES.
        END.
        ELSE
        DO:
            CREATE tLocation.
            ASSIGN tLocation.loc-nr = eg-location.nr
                tLocation.loc-nm = eg-location.bezeich
                tlocation.loc-selected = YES
                tlocation.loc-guest = NO.
        END.
    END.                                    
END.

PROCEDURE create-room:
    DEF VAR i AS INTEGER NO-UNDO.
    /*DEF BUFFER qbuff FOR zimmer.
    DEF BUFFER qbuff1 FOR tlocation. FT serverless*/

    FOR EACH troom:
        DELETE troom.
    END.    

    FIND FIRST tlocation WHERE tlocation.loc-selected = YES AND tlocation.loc-guest = YES NO-LOCK NO-ERROR.
    IF AVAILABLE tlocation THEN
    DO:
        FOR EACH zimmer NO-LOCK:
            CREATE troom.
            ASSIGN 
                troom.room-nm = zimmer.zinr
                troom.room-SELECTED = NO.
        END.
    END.
    ELSE
    DO:
        /*ASSIGN all-room = NO.
        APPLY "VALUE-CHANGED" TO all-room IN FRAME frame2.*/
    END.
END.

PROCEDURE create-property:
    /*DEF BUFFER qbuff FOR eg-property.FT serverless*/
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
            FOR EACH eg-property WHERE eg-property.location = comlocat.loc-nr USE-INDEX mtloczin_x NO-LOCK:
                /*FDL Comment => If Work Order Guest Room, data not shown*/
                /*FIRST commain WHERE commain.main-nr = qbuff.maintask AND commain.main-selected NO-LOCK,
                FIRST comroom WHERE comroom.room-nm = qbuff.zinr AND comroom.room-selected NO-LOCK:*/
                CREATE tproperty.
                ASSIGN tproperty.prop-nr = eg-property.nr
                       tproperty.prop-nm = eg-property.bezeich + "(" + string(eg-property.nr) + ")"
                       tproperty.pzinr   = eg-property.zinr 
                       tproperty.pmain-nr = eg-property.maintask
                       tproperty.ploc-nr  = eg-property.location.

                FIND FIRST queasy WHERE queasy.KEY= 133 AND queasy.number1 = eg-property.maintask NO-LOCK NO-ERROR.
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

                FIND FIRST eg-location WHERE eg-location.nr = eg-property.location NO-LOCK NO-ERROR.
                IF AVAILABLE eg-location THEN
                    ASSIGN tproperty.ploc = eg-location.bezeich.
                ELSE
                    ASSIGN  tproperty.ploc = "".
            END.
        END.
        ELSE
        DO:
            FOR EACH eg-property WHERE eg-property.location = comlocat.loc-nr USE-INDEX location_ix NO-LOCK :
                CREATE tproperty.
                ASSIGN tproperty.prop-nr = eg-property.nr
                       tproperty.prop-nm = eg-property.bezeich + "(" + string(eg-property.nr) + ")"
                       tproperty.pzinr   = eg-property.zinr 
                       tproperty.pmain-nr = eg-property.maintask
                       tproperty.ploc-nr  = eg-property.location.

                FIND FIRST queasy WHERE queasy.KEY= 133 AND queasy.number1 = eg-property.maintask NO-LOCK NO-ERROR.
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


                FIND FIRST eg-location WHERE eg-location.nr = eg-property.location NO-LOCK NO-ERROR.
                IF AVAILABLE eg-location THEN
                    ASSIGN tproperty.ploc = eg-location.bezeich.
                ELSE
                    ASSIGN  tproperty.ploc = "".
            END.
        END.
    END.
END.

PROCEDURE create-pic:
    /*DEF BUFFER qbuff FOR eg-staff.
    DEF BUFFER qbuff1 FOR bediener.FT serverless*/

    FOR EACH tpic:
        DELETE tpic.
    END.
    
    CREATE tpic.
    ASSIGN  tpic.pic-nr = 0
            tpic.pic-nm = ""
            tpic.pic-selected = NO.

    FOR EACH eg-staff WHERE eg-staff.usergroup = EngID AND eg-staff.activeflag = YES NO-LOCK BY eg-staff.nr:
        CREATE tpic.
        ASSIGN 
            tpic.pic-nr = eg-staff.nr
            tpic.pic-nm = eg-staff.NAME
            tpic.pic-dept = eg-staff.usergroup
            tpic.pic-selected = NO.
    END.

END.

PROCEDURE create-subtask:
    /*DEF BUFFER qbuff FOR eg-subtask.FT serverless*/

    FOR EACH tsubtask:
        DELETE tsubtask.
    END.
    
    CREATE tsubtask.
    ASSIGN tsubtask.sub-nr = "0"
        tsubtask.sub-nm = ""
        tsubtask.sub-selected =  NO.

    IF all-maintask THEN
    DO:
        FOR EACH eg-subtask NO-LOCK:
                CREATE tsubtask.
                ASSIGN tsubtask.sub-nr = eg-subtask.sub-code
                    tsubtask.sub-nm = eg-subtask.bezeich
                    tsubtask.sub-selected =  NO.
            END.
    END.
    ELSE
    DO:
        FOR EACH tmaintask WHERE tmaintask.main-selected NO-LOCK:
            FOR EACH eg-subtask WHERE eg-subtask.main-nr = tmaintask.main-nr NO-LOCK:
                CREATE tsubtask.
                ASSIGN tsubtask.sub-nr = eg-subtask.sub-code
                    tsubtask.sub-nm = eg-subtask.bezeich
                    tsubtask.sub-selected =  NO.
            END.
        END.
    END.
END.

PROCEDURE create-source:
    DEF BUFFER qbuff FOR queasy.
    FOR EACH tsource:
        DELETE tsource.
    END.  

    FOR EACH qbuff WHERE qbuff.KEY= 130 NO-LOCK:
        CREATE tsource.
        ASSIGN tsource.source-nr = qbuff.number1
            tsource.source-nm = qbuff.char1
            tsource.source-selected = NO.
    END.
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
                tmaintask.main-selected = YES.
                
                /*gerald kebutuhan filter WEB API*/
                tMaintask.categ-nr = comcategory.categ-nr.
                tMaintask.categ-nm = comcategory.categ-nm.
                
        END. 
    END.                             
END.

