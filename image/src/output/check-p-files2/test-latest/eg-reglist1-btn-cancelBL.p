DEFINE TEMP-TABLE tpic
    FIELD pic-nr        AS INTEGER
    FIELD pic-nm        AS CHAR FORMAT "x(20)" COLUMN-LABEL "Pic"
    FIELD pic-selected  AS LOGICAL INITIAL NO
    FIELD pic-Dept      AS INTEGER.

DEFINE TEMP-TABLE copyRequest
    FIELD reqnr         AS INTEGER      FORMAT ">>>>>>>>9"
    FIELD openby        AS CHAR 
    FIELD opendate      AS DATE
    FIELD opentime      AS INTEGER
    FIELD openstr       AS CHAR         FORMAT "x(20)"
    FIELD status-str    AS CHAR         FORMAT "x(20)"
    FIELD Source-str    AS CHAR         FORMAT "x(20)"
    FIELD source-name   AS CHAR         FORMAT "x(30)"
    FIELD process-date  AS DATE
    FIELD closed-date   AS DATE  
    FIELD urgency-nr    AS INTEGER      
    FIELD urgency       AS CHAR         FORMAT "x(20)"
    FIELD category-str  AS CHAR         FORMAT "x(20)"
    FIELD deptnum       AS INTEGER
    FIELD dept-nm       AS CHAR         FORMAT "x(20)"
    FIELD pmaintask     AS INTEGER
    FIELD maintask      AS CHAR         FORMAT "x(24)"
    FIELD plocation     AS INTEGER
    FIELD location      AS CHAR         FORMAT "x(24)"
    FIELD zinr          AS CHAR         FORMAT "x(8)"
    FIELD property      AS INTEGER
    FIELD property-nm   AS CHAR         FORMAT "x(40)"
    FIELD pic-str       AS CHAR         FORMAT "x(20)"
    FIELD sub-str       AS CHAR         FORMAT "x(40)"
    FIELD ex-finishdate AS DATE
    FIELD ex-finishtime AS INTEGER
    FIELD ex-finishstr  AS CHAR         FORMAT "x(20)"
    FIELD memo          AS CHAR         FORMAT "x(50)"
    FIELD task-def      AS CHAR         FORMAT "x(50)"
    FIELD task-solv     AS CHAR         FORMAT "x(50)"
    FIELD SOURCE        AS INTEGER
    FIELD category      AS INTEGER
    FIELD reqstatus     AS INTEGER
    FIELD sub-task      AS CHAR         
    FIELD subtask-bezeich    AS CHAR    FORMAT "x(30)"
    FIELD assign-to     AS INTEGER
    FIELD delete-flag   AS LOGICAL
    FIELD str           AS CHAR FORMAT "x(2)" initial ""
    FIELD rec          AS CHAR FORMAT "x(2)" INITIAL ""
    
    INDEX statOb           reqstatus pmaintask
    INDEX ObLoc            pmaintask plocation
    INDEX statObLoc        reqstatus pmaintask plocation
    INDEX ObZin            pmaintask zinr
    INDEX statObZin        reqstatus pmaintask zinr
    INDEX LocZin           plocation zinr
    INDEX statLocZin       reqstatus plocation zinr 
    INDEX statObLocZin     reqstatus pmaintask plocation Zinr.

DEFINE TEMP-TABLE tcategory
    FIELD categ-nr          AS INTEGER
    FIELD categ-nm          AS CHAR     FORMAT "x(20)"
    FIELD categ-selected    AS LOGICAL  INITIAL NO.

DEFINE TEMP-TABLE tsource
    FIELD source-nr         AS INTEGER
    FIELD source-nm         AS CHAR     FORMAT "x(20)"
    FIELD source-selected   AS LOGICAL  INITIAL NO.

DEFINE TEMP-TABLE tsubtask
    FIELD sub-nr        AS CHAR 
    FIELD sub-nm        AS CHAR     FORMAT "x(20)"
    FIELD sub-selected  AS LOGICAL  INITIAL NO.

DEFINE TEMP-TABLE tMaintask
    FIELD Main-nr       AS INTEGER 
    FIELD Main-nm       AS CHAR FORMAT "x(24)" COLUMN-LABEL "Object"
    FIELD main-selected AS LOGICAL INITIAL NO.

DEFINE TEMP-TABLE tLocation
    FIELD loc-nr        AS INTEGER 
    FIELD loc-nm        AS CHAR FORMAT "x(24)" COLUMN-LABEL "Location"
    FIELD loc-selected  AS LOGICAL INITIAL NO
    FIELD loc-guest     AS LOGICAL INITIAL NO.

DEFINE TEMP-TABLE troom
    FIELD room-nm       AS CHAR FORMAT "x(15)" COLUMN-LABEL "Room"
    FIELD room-Selected AS LOGICAL INITIAL NO.

DEFINE TEMP-TABLE tStatus
    FIELD stat-nr       AS INTEGER
    FIELD stat-nm       AS CHAR FORMAT "x(15)"
    FIELD stat-selected AS LOGICAL INITIAL NO.


DEF INPUT-OUTPUT PARAMETER location     AS INT.
DEF INPUT-OUTPUT PARAMETER rmNo         AS CHAR.
DEF INPUT-OUTPUT PARAMETER main-nr      AS INT.
DEF INPUT-OUTPUT PARAMETER reqstatus    AS INT.
DEF INPUT  PARAMETER sguestflag AS LOGICAL.

DEF INPUT  PARAMETER copyrequest-reqnr AS INT.
DEF INPUT  PARAMETER user-init AS CHAR.
DEF INPUT  PARAMETER st-cancel AS CHAR.
DEF OUTPUT PARAMETER flag AS LOGICAL INIT NO.
DEF OUTPUT PARAMETER TABLE FOR copyRequest.

/*MT not yet*/

FIND FIRST eg-request WHERE eg-request.reqnr = copyrequest-reqnr NO-ERROR.
IF AVAILABLE eg-request THEN
DO: 
    ASSIGN eg-request.delete-flag = YES
           eg-request.cancel-date = TODAY
           eg-request.cancel-time = TIME
           eg-request.cancel-by   = user-init 
           eg-request.char1       = st-cancel.

    RUN create-request1.
    flag = YES.
    RUN create-status.
    RUN create-room.
    RUN create-maintask.
    RUN create-subtask.
    RUN create-source.
    RUN create-category.
    
    RUN open-query1. /*btn-cancel*/
    /*MTin-state = "".
    APPLY "entry" TO rmno.
    RETURN NO-APPLY.*/
END.


PROCEDURE create-request1 :
DEF VAR strdatetime AS CHAR NO-UNDO.
DEF VAR ex-finishstr AS CHAR NO-UNDO.
DEF BUFFER ques FOR queasy.

    FOR EACH eg-request WHERE eg-request.delete-flag = NO 
        AND eg-request.opened-date GE from-date
        AND eg-request.opened-date LE to-date
        EXCLUSIVE-LOCK:

        strdatetime  = string(eg-request.opened-date , "99/99/99") + " " + STRING(eg-request.opened-time , "HH:MM").
        IF eg-request.ex-finishdate = ? THEN
            ex-finishstr = "".
        ELSE 
            ex-finishstr = string(eg-request.ex-finishdate , "99/99/99") + " " + STRING(eg-request.Ex-finishtime , "HH:MM").

        IF eg-request.propertynr = 0 THEN
        DO:
            ASSIGN 
                eg-request.char2            = strdatetime
                eg-request.char3            = ex-finishstr
            .
        END.
        ELSE
        DO:
            FIND FIRST eg-property WHERE eg-property.nr = eg-request.propertynr NO-LOCK NO-ERROR.
            IF AVAILABLE eg-property THEN
            DO:  
                ASSIGN 
                    eg-request.char2            = strdatetime
                    eg-request.char3            = ex-finishstr
                    eg-request.maintask         = eg-property.maintask
                .
               FIND FIRST queasy WHERE queasy.KEY= 133 AND queasy.number1 = eg-property.maintask NO-LOCK NO-ERROR.
                IF AVAILABLE queasy THEN
                DO:
                    FIND FIRST ques WHERE ques.KEY = 132 AND ques.number1 = queasy.number2 NO-LOCK NO-ERROR.
                    IF AVAILABLE ques THEN
                    DO:
                        ASSIGN eg-request.category = queasy.number2.
                    END.
            
                END.
            END.        
        END.
    END.

END PROCEDURE.


PROCEDURE open-query1 :
    
    FOR EACH copyrequest:
        DELETE copyrequest.
    END.
    IF sguestflag = YES THEN
    DO:
        FIND FIRST eg-location WHERE eg-location.guestflag = YES no-lock NO-ERROR.
        IF AVAILABLE eg-location THEN location = eg-location.nr.

        IF rmNo NE "" AND main-nr NE 0 THEN
        DO: 
            IF reqstatus = 0 THEN
            DO:
                FOR EACH eg-request WHERE eg-request.zinr = rmno 
                    AND eg-request.maintask = main-nr 
                    AND eg-request.deptnum GE 0
                    AND eg-request.delete-flag = NO /*USE-INDEX ObZin*/ 
                    AND eg-request.opened-date GE from-date
                    AND eg-request.opened-date LE to-date
                    NO-LOCK  , 
                    FIRST tstatus WHERE tstatus.stat-nr = eg-request.reqstatus NO-LOCK ,
                    FIRST tsource WHERE tsource.source-nr = eg-request.SOURCE NO-LOCK,
                    FIRST tcategory WHERE tcategory.categ-nr = eg-request.category NO-LOCK,
                    FIRST tsubtask WHERE tsubtask.sub-nr = eg-request.sub-task NO-LOCK,
                    FIRST tMaintask WHERE tmaintask.main-nr = eg-request.maintask NO-LOCK,
                    FIRST tpic WHERE tpic.pic-nr = eg-request.assign-to NO-LOCK,
                    FIRST eg-location WHERE eg-location.nr = eg-request.reserve-int NO-LOCK,
                    FIRST eg-property WHERE eg-property.nr = eg-request.property NO-LOCK 
                    BY eg-request.opened-date : 
                        RUN create-Copy1.
                END.
            END.
            ELSE
            DO:
                FOR EACH eg-request WHERE eg-request.zinr = rmno 
                    AND eg-request.maintask = main-nr 
                    AND eg-request.deptnum GE 0
                    AND eg-request.reqstatus = reqstatus 
                    AND eg-request.delete-flag = NO /*USE-INDEX ObZin*/ 
                    AND eg-request.opened-date GE from-date
                    AND eg-request.opened-date LE to-date
                    NO-LOCK  , 
                    FIRST tstatus WHERE tstatus.stat-nr = eg-request.reqstatus NO-LOCK ,
                    FIRST tsource WHERE tsource.source-nr = eg-request.SOURCE NO-LOCK,
                    FIRST tcategory WHERE tcategory.categ-nr = eg-request.category NO-LOCK,
                    FIRST tsubtask WHERE tsubtask.sub-nr = eg-request.sub-task NO-LOCK,
                    FIRST tMaintask WHERE tmaintask.main-nr = eg-request.maintask NO-LOCK,
                    FIRST tpic WHERE tpic.pic-nr = eg-request.assign-to NO-LOCK,
                    FIRST eg-location WHERE eg-location.nr = eg-request.reserve-int NO-LOCK,
                    FIRST eg-property WHERE eg-property.nr = eg-request.property NO-LOCK 
                    BY eg-request.opened-date : 
                        RUN create-Copy1.
                END.
            END.
          END.
        ELSE IF rmNo NE "" AND main-nr = 0 THEN 
        DO:
            IF reqstatus = 0 THEN
            DO:
                FOR EACH eg-request WHERE eg-request.zinr = rmno 
                    AND eg-request.deptnum GE 0
                    AND eg-request.delete-flag = NO /*USE-INDEX ObZin*/ 
                    AND eg-request.opened-date GE from-date
                    AND eg-request.opened-date LE to-date
                    NO-LOCK  , 
                    FIRST tstatus WHERE tstatus.stat-nr = eg-request.reqstatus NO-LOCK ,
                    FIRST tsource WHERE tsource.source-nr = eg-request.SOURCE NO-LOCK,
                    FIRST tcategory WHERE tcategory.categ-nr = eg-request.category NO-LOCK,
                    FIRST tsubtask WHERE tsubtask.sub-nr = eg-request.sub-task NO-LOCK,
                    FIRST tMaintask WHERE tmaintask.main-nr = eg-request.maintask NO-LOCK,
                    FIRST tpic WHERE tpic.pic-nr = eg-request.assign-to NO-LOCK,
                    FIRST eg-location WHERE eg-location.nr = eg-request.reserve-int NO-LOCK,
                    FIRST eg-property WHERE eg-property.nr = eg-request.property NO-LOCK 
                    BY eg-request.opened-date : 
                        RUN create-Copy1.
                END.
            END.
            ELSE
            DO:
                FOR EACH eg-request WHERE eg-request.zinr = rmno 
                   AND eg-request.delete-flag = NO AND eg-request.deptnum GE 0 
                   AND eg-request.reqstatus = reqstatus /*USE-INDEX statObZin*/ 
                   AND eg-request.opened-date GE from-date
                   AND eg-request.opened-date LE to-date
                   NO-LOCK  , 
                   FIRST tstatus WHERE tstatus.stat-nr = eg-request.reqstatus NO-LOCK ,
                   FIRST tsource WHERE tsource.source-nr = eg-request.SOURCE NO-LOCK,
                   FIRST tcategory WHERE tcategory.categ-nr = eg-request.category NO-LOCK,
                   FIRST tsubtask WHERE tsubtask.sub-nr = eg-request.sub-task NO-LOCK,
                   FIRST tMaintask WHERE tmaintask.main-nr = eg-request.maintask NO-LOCK,
                   FIRST tpic WHERE tpic.pic-nr = eg-request.assign-to NO-LOCK,
                   FIRST eg-location WHERE eg-location.nr = eg-request.reserve-int NO-LOCK,
                   FIRST eg-property WHERE eg-property.nr = eg-request.property NO-LOCK 
                   BY eg-request.opened-date : 
                        RUN create-Copy1.
               END. 
            END.
        END.
        ELSE IF rmNo = "" AND main-nr NE 0 THEN 
        DO: 
            IF reqstatus = 0 THEN
            DO:
                FOR EACH eg-request WHERE eg-request.reserve-int = location 
                    AND eg-request.maintask = main-nr
                    AND eg-request.deptnum GE 0 
                    AND eg-request.delete-flag = NO 
                    AND eg-request.opened-date GE from-date
                    AND eg-request.opened-date LE to-date
                    NO-LOCK, 
                    FIRST tstatus WHERE tstatus.stat-nr = eg-request.reqstatus NO-LOCK ,
                    FIRST tsource WHERE tsource.source-nr = eg-request.SOURCE NO-LOCK,
                    FIRST tcategory WHERE tcategory.categ-nr = eg-request.category NO-LOCK,
                    FIRST tsubtask WHERE tsubtask.sub-nr = eg-request.sub-task NO-LOCK,
                    FIRST tMaintask WHERE tmaintask.main-nr = eg-request.maintask NO-LOCK,
                    FIRST tpic WHERE tpic.pic-nr = eg-request.assign-to NO-LOCK,
                    FIRST eg-location WHERE eg-location.nr = eg-request.reserve-int NO-LOCK,
                    FIRST eg-property WHERE eg-property.nr = eg-request.property NO-LOCK 
                    BY eg-request.opened-date : 
                        RUN create-Copy1.
                END.
            END.
            ELSE
            DO:
                FOR EACH eg-request WHERE eg-request.reserve-int = location 
                    AND eg-request.maintask = main-nr 
                    AND eg-request.deptnum GE 0
                    AND eg-request.reqstatus = reqstatus 
                    AND eg-request.delete-flag = NO /*USE-INDEX statObLoc*/ 
                    AND eg-request.opened-date GE from-date
                    AND eg-request.opened-date LE to-date
                    NO-LOCK, 
                    FIRST tstatus WHERE tstatus.stat-nr = eg-request.reqstatus NO-LOCK ,
                    FIRST tsource WHERE tsource.source-nr = eg-request.SOURCE NO-LOCK,
                    FIRST tcategory WHERE tcategory.categ-nr = eg-request.category NO-LOCK,
                    FIRST tsubtask WHERE tsubtask.sub-nr = eg-request.sub-task NO-LOCK,
                    FIRST tMaintask WHERE tmaintask.main-nr = eg-request.maintask NO-LOCK,
                    FIRST tpic WHERE tpic.pic-nr = eg-request.assign-to NO-LOCK,
                    FIRST eg-location WHERE eg-location.nr = eg-request.reserve-int NO-LOCK,
                    FIRST eg-property WHERE eg-property.nr = eg-request.property NO-LOCK 
                    BY eg-request.opened-date : 
                        RUN create-Copy1.
                END.
            END.
        END.
        ELSE
        DO:
            IF reqstatus = 0 THEN
            DO:
                FOR EACH eg-request WHERE eg-request.reserve-int = location 
                    AND eg-request.delete-flag = NO
                    AND eg-request.deptnum GE 0 /*USE-INDEX statObLoc*/ 
                    AND eg-request.opened-date GE from-date
                    AND eg-request.opened-date LE to-date
                    NO-LOCK  , 
                    FIRST tstatus WHERE tstatus.stat-nr = eg-request.reqstatus NO-LOCK ,
                    FIRST tsource WHERE tsource.source-nr = eg-request.SOURCE NO-LOCK,
                    FIRST tcategory WHERE tcategory.categ-nr = eg-request.category NO-LOCK,
                    FIRST tsubtask WHERE tsubtask.sub-nr = eg-request.sub-task NO-LOCK,
                    FIRST tMaintask WHERE tmaintask.main-nr = eg-request.maintask NO-LOCK,
                    FIRST tpic WHERE tpic.pic-nr = eg-request.assign-to NO-LOCK,
                    FIRST eg-location WHERE eg-location.nr = eg-request.reserve-int NO-LOCK,
                    FIRST eg-property WHERE eg-property.nr = eg-request.property NO-LOCK 
                    BY eg-request.opened-date : 
                        RUN create-Copy1.
                END.
            END.
            ELSE
            DO:
                FOR EACH eg-request WHERE eg-request.reserve-int = location 
                     AND eg-request.deptnum GE 0 
                     AND eg-request.reqstatus = reqstatus
                     AND eg-request.delete-flag = NO /*USE-INDEX statloczin*/ 
                     AND eg-request.opened-date GE from-date
                     AND eg-request.opened-date LE to-date
                     NO-LOCK, 
                     FIRST tstatus WHERE tstatus.stat-nr = eg-request.reqstatus NO-LOCK ,
                     FIRST tsource WHERE tsource.source-nr = eg-request.SOURCE NO-LOCK,
                     FIRST tcategory WHERE tcategory.categ-nr = eg-request.category NO-LOCK,
                     FIRST tsubtask WHERE tsubtask.sub-nr = eg-request.sub-task NO-LOCK,
                     FIRST tpic WHERE tpic.pic-nr = eg-request.assign-to NO-LOCK,
                     FIRST tMaintask WHERE tmaintask.main-nr = eg-request.maintask NO-LOCK,
                     FIRST eg-location WHERE eg-location.nr = eg-request.reserve-int NO-LOCK,
                     FIRST eg-property WHERE eg-property.nr = eg-request.property NO-LOCK 
                     BY eg-request.opened-date : 
                         RUN create-Copy1.
                END.
            END.
        END.
    END.
    ELSE
    DO:
        IF location = 0 THEN
        DO:
            IF main-nr NE 0 THEN
            DO: 
                IF reqstatus = 0 THEN
                DO:    
                    FOR EACH eg-request WHERE eg-request.maintask = main-nr 
                        AND eg-request.deptnum GE 0 
                        AND eg-request.delete-flag = NO /*USE-INDEX statOblocZin*/ 
                        AND eg-request.opened-date GE from-date
                        AND eg-request.opened-date LE to-date
                        NO-LOCK, 
                        FIRST tstatus WHERE tstatus.stat-nr = eg-request.reqstatus NO-LOCK,
                        FIRST tsource WHERE tsource.source-nr = eg-request.SOURCE NO-LOCK ,
                        FIRST tcategory WHERE tcategory.categ-nr = eg-request.category NO-LOCK,
                        FIRST tsubtask WHERE tsubtask.sub-nr = eg-request.sub-task NO-LOCK,
                        FIRST tpic WHERE tpic.pic-nr = eg-request.assign-to NO-LOCK,
                        FIRST tMaintask WHERE tmaintask.main-nr = eg-request.maintask NO-LOCK,
                        FIRST eg-location WHERE eg-location.nr = eg-request.reserve-int NO-LOCK,
                        FIRST eg-property WHERE eg-property.nr = eg-request.property NO-LOCK 
                        BY eg-request.opened-date : 
                            RUN create-Copy1.
                    END.
                END.
                ELSE
                DO:
                    FOR EACH eg-request WHERE eg-request.maintask = main-nr 
                        AND eg-request.deptnum GE 0
                        AND eg-request.reqstatus = reqstatus 
                        AND eg-request.delete-flag = NO /*USE-INDEX statob*/ 
                        AND eg-request.opened-date GE from-date
                        AND eg-request.opened-date LE to-date
                        NO-LOCK, 
                        FIRST tstatus WHERE tstatus.stat-nr = eg-request.reqstatus NO-LOCK ,
                        FIRST tsource WHERE tsource.source-nr = eg-request.SOURCE NO-LOCK,
                        FIRST tcategory WHERE tcategory.categ-nr = eg-request.category NO-LOCK,
                        FIRST tsubtask WHERE tsubtask.sub-nr = eg-request.sub-task NO-LOCK,
                        FIRST tpic WHERE tpic.pic-nr = eg-request.assign-to NO-LOCK,
                        FIRST tMaintask WHERE tmaintask.main-nr = eg-request.maintask NO-LOCK,
                        FIRST eg-location WHERE eg-location.nr = eg-request.reserve-int NO-LOCK,
                        FIRST eg-property WHERE eg-property.nr = eg-request.property NO-LOCK 
                        BY eg-request.opened-date :
                            RUN create-Copy1.
                    END. 
                END.
            END.
            ELSE IF main-nr = 0 THEN 
            DO:
                IF reqstatus = 0 THEN
                DO:
                    FOR EACH eg-request WHERE eg-request.deptnum GE 0 
                        AND eg-request.delete-flag = NO 
                        AND eg-request.opened-date GE from-date
                        AND eg-request.opened-date LE to-date
                        NO-LOCK, 
                        FIRST tstatus WHERE tstatus.stat-nr = eg-request.reqstatus NO-LOCK ,
                        FIRST tsource WHERE tsource.source-nr = eg-request.SOURCE NO-LOCK,
                        FIRST tcategory WHERE tcategory.categ-nr = eg-request.category NO-LOCK,
                        FIRST tsubtask WHERE tsubtask.sub-nr = eg-request.sub-task NO-LOCK,
                        FIRST tMaintask WHERE tmaintask.main-nr = eg-request.maintask NO-LOCK,
                        FIRST tpic WHERE tpic.pic-nr = eg-request.assign-to NO-LOCK,
                        FIRST eg-location WHERE eg-location.nr = eg-request.reserve-int NO-LOCK,
                        FIRST eg-property WHERE eg-property.nr = eg-request.property NO-LOCK 
                        BY eg-request.opened-date : 
                            RUN create-Copy1.
                    END.
                END.
                ELSE
                DO:
                    FOR EACH eg-request WHERE eg-request.deptnum GE 0
                        AND eg-request.reqstatus = reqstatus  
                        AND eg-request.opened-date GE from-date
                        AND eg-request.opened-date LE to-date
                        NO-LOCK ,
                        FIRST tstatus WHERE tstatus.stat-nr = eg-request.reqstatus NO-LOCK ,
                        FIRST tsource WHERE tsource.source-nr = eg-request.SOURCE NO-LOCK,
                        FIRST tcategory WHERE tcategory.categ-nr = eg-request.category NO-LOCK,
                        FIRST tsubtask WHERE tsubtask.sub-nr = eg-request.sub-task NO-LOCK,
                        /*FIRST eg-staff WHERE eg-staff.nr = eg-request.assign-to NO-LOCK,*/
                        FIRST tpic WHERE tpic.pic-nr = eg-request.assign-to NO-LOCK,
                        FIRST tMaintask WHERE tmaintask.main-nr = eg-request.maintask NO-LOCK,
                        FIRST eg-location WHERE eg-location.nr = eg-request.reserve-int NO-LOCK,
                        FIRST eg-property WHERE eg-property.nr = eg-request.property  NO-LOCK
                        BY eg-request.reqnr : 
                            RUN create-copy1.
                    END.
                END.
           END.
        END.
        ELSE
        DO:
            IF main-nr NE 0 THEN
            DO: 
                IF reqstatus = 0 THEN
                DO:     
                    FOR EACH eg-request WHERE eg-request.reserve-int = location 
                        AND eg-request.maintask = main-nr
                        AND eg-request.deptnum GE 0 
                        AND eg-request.delete-flag = NO /*USE-INDEX obloc*/ 
                        AND eg-request.opened-date GE from-date
                        AND eg-request.opened-date LE to-date
                        NO-LOCK, 
                        FIRST tstatus WHERE tstatus.stat-nr = eg-request.reqstatus NO-LOCK ,
                        FIRST tsource WHERE tsource.source-nr = eg-request.SOURCE NO-LOCK,
                        FIRST tcategory WHERE tcategory.categ-nr = eg-request.category NO-LOCK,
                        FIRST tsubtask WHERE tsubtask.sub-nr = eg-request.sub-task NO-LOCK,
                        FIRST tpic WHERE tpic.pic-nr = eg-request.assign-to NO-LOCK,
                        FIRST tMaintask WHERE tmaintask.main-nr = eg-request.maintask NO-LOCK,
                        FIRST eg-location WHERE eg-location.nr = eg-request.reserve-int NO-LOCK,
                        FIRST eg-property WHERE eg-property.nr = eg-request.property NO-LOCK 
                        BY eg-request.opened-date : 
                            RUN create-Copy1.
                    END.
                END.
                ELSE
                DO:
                    FOR EACH eg-request WHERE eg-request.reserve-int = location  
                       AND eg-request.maintask = main-nr 
                       AND eg-request.deptnum GE 0 
                       AND eg-request.reqstatus = reqstatus 
                       AND eg-request.delete-flag = NO /*USE-INDEX statobloc*/ 
                       AND eg-request.opened-date GE from-date
                       AND eg-request.opened-date LE to-date
                       NO-LOCK  , 
                       FIRST tstatus WHERE tstatus.stat-nr = eg-request.reqstatus NO-LOCK ,
                       FIRST tsource WHERE tsource.source-nr = eg-request.SOURCE NO-LOCK,
                       FIRST tcategory WHERE tcategory.categ-nr = eg-request.category NO-LOCK,
                       FIRST tsubtask WHERE tsubtask.sub-nr = eg-request.sub-task NO-LOCK,
                       FIRST tpic WHERE tpic.pic-nr = eg-request.assign-to NO-LOCK,
                       FIRST tMaintask WHERE tmaintask.main-nr = eg-request.maintask NO-LOCK,
                       FIRST eg-location WHERE eg-location.nr = eg-request.reserve-int NO-LOCK,
                       FIRST eg-property WHERE eg-property.nr = eg-request.property NO-LOCK 
                       BY eg-request.opened-date : 
                            RUN create-Copy1.
                    END.        
                END.
              END.
            ELSE IF main-nr = 0 THEN 
            DO:
                IF reqstatus = 0 THEN
                DO:
                    FOR EACH eg-request WHERE eg-request.reserve-int = location 
                        AND eg-request.delete-flag = NO
                        AND eg-request.deptnum GE 0 
                        AND eg-request.opened-date GE from-date
                        AND eg-request.opened-date LE to-date
                        NO-LOCK, 
                        FIRST tstatus WHERE tstatus.stat-nr = eg-request.reqstatus NO-LOCK ,
                        FIRST tsource WHERE tsource.source-nr = eg-request.SOURCE NO-LOCK,
                        FIRST tcategory WHERE tcategory.categ-nr = eg-request.category NO-LOCK,
                        FIRST tsubtask WHERE tsubtask.sub-nr = eg-request.sub-task NO-LOCK,
                        FIRST tpic WHERE tpic.pic-nr = eg-request.assign-to NO-LOCK,
                        FIRST tMaintask WHERE tmaintask.main-nr = eg-request.maintask NO-LOCK,
                        FIRST eg-location WHERE eg-location.nr = eg-request.reserve-int NO-LOCK,
                        FIRST eg-property WHERE eg-property.nr = eg-request.property NO-LOCK 
                        BY eg-request.opened-date : 
                            RUN create-Copy1.
                    END.
                END.
                ELSE
                DO:
                    FOR EACH eg-request WHERE eg-request.reserve-int = location  
                       AND eg-request.deptnum GE 0 
                       AND eg-request.delete-flag = NO
                       AND eg-request.reqstatus = reqstatus 
                       AND eg-request.opened-date GE from-date
                       AND eg-request.opened-date LE to-date
                       NO-LOCK, 
                       FIRST tstatus WHERE tstatus.stat-nr = eg-request.reqstatus NO-LOCK ,
                       FIRST tsource WHERE tsource.source-nr = eg-request.SOURCE NO-LOCK,
                       FIRST tcategory WHERE tcategory.categ-nr = eg-request.category NO-LOCK,
                       FIRST tsubtask WHERE tsubtask.sub-nr = eg-request.sub-task NO-LOCK,
                       FIRST tpic WHERE tpic.pic-nr = eg-request.assign-to NO-LOCK,
                       FIRST tMaintask WHERE tmaintask.main-nr = eg-request.maintask NO-LOCK,
                       FIRST eg-location WHERE eg-location.nr = eg-request.reserve-int NO-LOCK,
                       FIRST eg-property WHERE eg-property.nr = eg-request.property NO-LOCK 
                       BY eg-request.opened-date : 
                            RUN create-Copy1.
                   END. 
                END.
            END.
        END.
    END.
    /*MT
    IF last-sort = "" THEN last-sort = "reqnr".
    RUN disp-it(last-sort). /*run open-query*/
    IF AVAILABLE copyrequest THEN
        ENABLE btn-print  WITH FRAME frame1.
    ELSE
        DISABLE btn-print WITH FRAME frame1.
    */
END PROCEDURE.


PROCEDURE create-status :
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

END PROCEDURE.

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
  
END.

PROCEDURE create-maintask :
DEF BUFFER qbuff FOR queasy.

    FOR EACH tMaintask:
        DELETE tMaintask.
    END.

    FOR EACH qbuff WHERE qbuff.KEY = 133 NO-LOCK:
        CREATE tMaintask.
        ASSIGN tMaintask.Main-nr = qbuff.number1
            tMaintask.Main-nm = qbuff.char1
            tmaintask.main-selected = NO.
    END.   

END PROCEDURE.

PROCEDURE create-subtask :
DEF BUFFER qbuff FOR eg-subtask.
    FOR EACH tsubtask:
        DELETE tsubtask.
    END.

    FOR EACH qbuff NO-LOCK:
        CREATE tsubtask.
        ASSIGN 
            tsubtask.sub-nr = qbuff.sub-code
            tsubtask.sub-nm = qbuff.bezeich
            tsubtask.sub-selected =  NO.
    END.

END PROCEDURE.

PROCEDURE create-source :
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

END PROCEDURE.

PROCEDURE create-category :
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

END PROCEDURE.
