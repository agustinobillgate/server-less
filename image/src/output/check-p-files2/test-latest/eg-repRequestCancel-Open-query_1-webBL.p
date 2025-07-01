
DEF TEMP-TABLE t-eg-request LIKE eg-request.
DEFINE TEMP-TABLE tStatus
    FIELD stat-nr AS INTEGER
    FIELD stat-nm AS CHAR       FORMAT "x(24)"
    FIELD stat-selected AS LOGICAL INITIAL NO.

DEFINE TEMP-TABLE tLocation
    FIELD loc-nr  AS INTEGER 
    FIELD loc-nm  AS CHAR FORMAT "x(24)" COLUMN-LABEL "Location"
    FIELD loc-selected AS LOGICAL INITIAL YES
    FIELD loc-guest    AS LOGICAL INITIAL NO.

DEFINE TEMP-TABLE tMaintask
    FIELD Main-nr  AS INTEGER 
    FIELD Main-nm  AS CHAR FORMAT "x(24)" COLUMN-LABEL "Object"
    FIELD main-selected AS LOGICAL INITIAL NO
    /*gerald kebutuhan filter WEB API*/
    FIELD categ-nr AS INTEGER
    FIELD categ-nm AS CHAR.

DEFINE TEMP-TABLE troom
    FIELD room-nm AS CHAR FORMAT "x(24)" COLUMN-LABEL "Room"
    FIELD room-Selected AS LOGICAL INITIAL NO.

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

DEFINE TEMP-TABLE tpic
    FIELD pic-nr        AS INTEGER
    FIELD pic-nm        AS CHAR FORMAT "x(24)" COLUMN-LABEL "Pic"
    FIELD pic-selected  AS LOGICAL INITIAL NO
    FIELD pic-Dept      AS INTEGER.

DEFINE TEMP-TABLE tsubtask
    FIELD sub-nr AS CHAR
    FIELD sub-nm AS CHAR   FORMAT "x(24)"
    FIELD sub-selected AS LOGICAL INITIAL NO.

DEFINE TEMP-TABLE tsource
    FIELD source-nr AS INTEGER
    FIELD source-nm AS CHAR FORMAT "x(24)"
    FIELD source-selected AS LOGICAL INITIAL NO.

DEFINE TEMP-TABLE tcategory
    FIELD categ-nr AS INTEGER
    FIELD categ-nm AS CHAR  FORMAT "x(24)"
    FIELD categ-selected AS LOGICAL INITIAL NO.

DEFINE TEMP-TABLE sRequest
    FIELD reqnr         AS INTEGER
    FIELD opendate      AS DATE
    FIELD canceldate    AS DATE    
    FIELD cancelby      AS CHAR 
    FIELD reason        AS CHAR     FORMAT "x(100)"
    FIELD status-str    AS CHAR     FORMAT "x(20)"
    FIELD Source-str    AS CHAR     FORMAT "x(20)"
    FIELD source-name   AS CHAR     FORMAT "x(30)"
    FIELD process-date  AS DATE
    FIELD closed-date   AS DATE  
    FIELD urgency       AS CHAR     FORMAT "x(20)"  
    FIELD category-str  AS CHAR     FORMAT "x(20)"
    FIELD deptnum       AS INTEGER
    FIELD pmaintask     AS INTEGER
    FIELD maintask      AS CHAR     FORMAT "x(24)" 
    FIELD plocation     AS INTEGER
    FIELD location      AS CHAR     FORMAT "x(24)"
    FIELD zinr          AS CHAR     FORMAT "x(8)"
    FIELD property      AS INTEGER
    FIELD property-nm   AS CHAR     FORMAT "x(24)"
    FIELD pic-str       AS CHAR     FORMAT "x(20)" 
    FIELD sub-str       AS CHAR     FORMAT "x(30)"
    FIELD ex-finishdate AS DATE
    FIELD memo          AS CHAR     FORMAT "x(50)"
    FIELD task-def      AS CHAR     FORMAT "x(50)"
    FIELD task-solv     AS CHAR     FORMAT "x(50)"
    FIELD SOURCE        AS INTEGER
    FIELD category      AS INTEGER
    FIELD reqstatus     AS INTEGER
    FIELD sub-task      AS CHAR
    FIELD assign-to     AS INTEGER.

DEFINE TEMP-TABLE copyRequest
    FIELD reqnr         AS INTEGER
    FIELD opendate      AS DATE
    FIELD canceldate    AS DATE    
    FIELD cancelby      AS CHAR   
    FIELD reason        AS CHAR     FORMAT "x(100)"
    FIELD status-str    AS CHAR     FORMAT "x(20)"
    FIELD Source-str    AS CHAR     FORMAT "x(20)"
    FIELD source-name   AS CHAR     FORMAT "x(30)"
    FIELD process-date  AS DATE
    FIELD closed-date   AS DATE  
    FIELD urgency       AS CHAR     FORMAT "x(20)"  
    FIELD category-str  AS CHAR     FORMAT "x(24)"
    FIELD deptnum       AS INTEGER
    FIELD pmaintask     AS INTEGER
    FIELD maintask      AS CHAR     FORMAT "x(24)"   
    FIELD plocation     AS INTEGER
    FIELD location      AS CHAR     FORMAT "x(24)"
    FIELD zinr          AS CHAR     FORMAT "x(20)"
    FIELD property      AS INTEGER
    FIELD property-nm   AS CHAR     FORMAT "x(24)"
    FIELD pic-str       AS CHAR     FORMAT "x(20)" 
    FIELD sub-str       AS CHAR     FORMAT "x(24)"
    FIELD ex-finishdate AS DATE
    FIELD memo          AS CHAR     FORMAT "x(50)"
    FIELD task-def      AS CHAR     FORMAT "x(50)"
    FIELD task-solv     AS CHAR     FORMAT "x(50)"
    FIELD SOURCE        AS INTEGER
    FIELD category      AS INTEGER
    FIELD reqstatus     AS INTEGER
    FIELD sub-task      AS CHAR
    FIELD assign-to     AS INTEGER
    FIELD str           AS CHAR FORMAT "x" INITIAL "".


DEF BUFFER comProperty FOR tproperty.
DEF BUFFER comStatus FOR tStatus.
DEF BUFFER comPIC FOR tpic.
DEF BUFFER comsource FOR tsource.
DEF BUFFER comSubtask FOR tSubtask.
DEF BUFFER comcategory FOR tcategory.
DEF BUFFER commaintask FOR tmaintask.
DEF BUFFER comlocation FOR tlocation.
DEF BUFFER comroom FOR troom.

DEF INPUT PARAMETER fdate AS DATE.
DEF INPUT PARAMETER tdate AS DATE.
DEF INPUT PARAMETER TABLE FOR tsource.
DEF INPUT PARAMETER TABLE FOR tsubtask.
DEF INPUT PARAMETER TABLE FOR tpic.
DEF INPUT PARAMETER TABLE FOR tproperty.
DEF INPUT PARAMETER TABLE FOR tMaintask.
DEF INPUT PARAMETER TABLE FOR troom.
DEF INPUT PARAMETER TABLE FOR tStatus.
DEF INPUT PARAMETER TABLE FOR tLocation.
DEF INPUT PARAMETER TABLE FOR tcategory.
DEF OUTPUT PARAMETER TABLE FOR copyRequest.

DEFINE VARIABLE int-str AS CHAR EXTENT 3
    INITIAL ["Low", "Medium", "High"].

FOR EACH eg-request WHERE 
    eg-request.cancel-date GE fdate AND 
    eg-request.cancel-date LE tdate AND 
    eg-request.delete-flag = YES NO-LOCK:
    CREATE t-eg-request.
    BUFFER-COPY eg-request TO t-eg-request.
END.


FOR EACH t-eg-request NO-LOCK:
    IF t-eg-request.propertynr = 0 THEN
    DO:
            CREATE sRequest.

            ASSIGN sRequest.reqnr       = t-eg-request.reqnr
               sRequest.opendate        = t-eg-request.opened-date
               sRequest.process-date    = t-eg-request.process-date
               sRequest.closed-date     = t-eg-request.closed-date
               sRequest.urgency         = string(t-eg-request.urgency)
               srequest.source-name     = t-eg-request.source-name
               /*sRequest.deptnum       = t-eg-request.de*/
               sRequest.ex-finishdate   = t-eg-request.ex-finishdate
               sRequest.memo            = t-eg-request.memo
               sRequest.task-def        = t-eg-request.task-def
               sRequest.task-solv       = t-eg-request.task-solv
               sRequest.pmaintask       = t-eg-request.maintask
               sRequest.plocation       = t-eg-request.reserve-int
               srequest.zinr            = t-eg-request.zinr
               srequest.SOURCE          = t-eg-request.SOURCE
               srequest.category        = t-eg-request.category
               srequest.reqstatus       = t-eg-request.reqstatus
               srequest.sub-task        = t-eg-request.sub-task
               srequest.assign-to       = t-eg-request.assign-to
               srequest.property        = t-eg-request.propertynr
               srequest.canceldate      = t-eg-request.cancel-date
               srequest.cancelby        = t-eg-request.cancel-by
               srequest.reason          = t-eg-request.char1.
    END.
    ELSE
    DO: 
        FIND FIRST tproperty WHERE tproperty.prop-nr = t-eg-request.propertynr NO-LOCK NO-ERROR.
        IF AVAILABLE tproperty THEN
        DO:
            CREATE sRequest.
            ASSIGN sRequest.reqnr       = t-eg-request.reqnr
               sRequest.opendate        = t-eg-request.opened-date
               sRequest.process-date    = t-eg-request.process-date
               sRequest.closed-date     = t-eg-request.closed-date
               sRequest.urgency         = string(t-eg-request.urgency)
               srequest.source-name     = t-eg-request.source-name
               /*sRequest.deptnum       = t-eg-request.de*/
               sRequest.ex-finishdate   = t-eg-request.ex-finishdate
               sRequest.memo            = t-eg-request.memo
               sRequest.task-def        = t-eg-request.task-def
               sRequest.task-solv       = t-eg-request.task-solv
               sRequest.pmaintask       = tproperty.pmain-nr
               sRequest.plocation       = t-eg-request.reserve-int /*tproperty.ploc-nr*/
               srequest.zinr            = t-eg-request.zinr /*tproperty.pzinr*/ /*t-eg-request.zinr*/
               srequest.SOURCE          = t-eg-request.SOURCE
               srequest.category        = tproperty.pcateg-nr /*t-eg-request.category*/
               srequest.reqstatus       = t-eg-request.reqstatus
               srequest.sub-task        = t-eg-request.sub-task
               srequest.assign-to       = t-eg-request.assign-to
               srequest.property        = t-eg-request.propertynr
               srequest.canceldate      = t-eg-request.cancel-date
               srequest.cancelby        = t-eg-request.cancel-by
               srequest.reason          = t-eg-request.char1.
        END.        
    END.
END.
/*
FOR EACH t-eg-request:
    MESSAGE "t-eg-request" SKIP
        t-eg-request.reqnr SKIP 
        t-eg-request.propertynr
        VIEW-AS ALERT-BOX INFO BUTTONS OK.
END.

FOR EACH tproperty:
    MESSAGE "tproperty" SKIP
        tproperty.prop-nr SKIP
        tproperty.prop-selected SKIP
        VIEW-AS ALERT-BOX INFO BUTTONS OK.
END.
*/
FOR EACH srequest /*WHERE srequest.opendate >= fdate AND srequest.opendate <= tdate*/ NO-LOCK  , 
    FIRST tStatus WHERE tStatus.stat-nr = srequest.reqstatus AND tStatus.stat-selected = YES NO-LOCK ,
    FIRST tsource WHERE tsource.source-nr = srequest.SOURCE AND tsource.source-selected = YES NO-LOCK  ,
    FIRST tcategory WHERE tcategory.categ-nr = srequest.category AND tcategory.categ-selected = YES NO-LOCK,
    FIRST tSubtask WHERE tSubtask.sub-nr = srequest.sub-task AND tSubtask.sub-selected = YES NO-LOCK,
    FIRST tpic WHERE tpic.pic-nr = srequest.assign-to AND tpic.pic-selected = YES NO-LOCK,
    FIRST tmaintask WHERE tmaintask.main-nr = srequest.pmaintask AND tmaintask.main-selected = YES NO-LOCK,
    FIRST tlocation WHERE tlocation.loc-nr = srequest.plocation AND tlocation.loc-selected = YES NO-LOCK,
    FIRST tproperty WHERE tproperty.prop-nr = srequest.property AND tproperty.prop-selected = YES NO-LOCK  :

    CREATE copyRequest.
    ASSIGN 
        copyRequest.reqnr          = srequest.reqnr
        copyRequest.opendate       = srequest.opendate
        copyRequest.status-str     = tStatus.stat-nm
        copyRequest.Source-str     = tsource.source-nm
        copyRequest.process-date   = srequest.process-date
        copyRequest.closed-date    = srequest.closed-date
        copyRequest.urgency        = int-str[int(srequest.urgency)]
        copyRequest.category-str   = tcategory.categ-nm
        /*copyRequest.deptnum       AS INTEGER = srequest.*/
        copyRequest.pmaintask      = srequest.pmaintask
        copyRequest.maintask       = tmaintask.main-nm
        copyRequest.plocation      = srequest.plocation
        copyRequest.location       = tlocation.loc-nm
        copyRequest.zinr           = srequest.zinr
        copyRequest.property       = srequest.property
        copyRequest.property-nm    = tproperty.prop-nm
        copyRequest.pic-str        = tpic.pic-nm
        copyRequest.sub-str        = tSubtask.sub-nm
        copyRequest.ex-finishdate  = srequest.ex-finishdate
        copyRequest.memo           = srequest.memo
        copyRequest.task-def       = srequest.task-def
        copyRequest.task-solv      = srequest.task-solv
        copyRequest.SOURCE         = srequest.source
        copyRequest.category       = srequest.category
        copyRequest.reqstatus      = srequest.reqstatus
        copyRequest.sub-task       = srequest.sub-task
        copyRequest.assign-to      = srequest.assign-to
        copyrequest.canceldate     = srequest.canceldate 
        copyrequest.cancelby       = srequest.cancelby  
        copyrequest.reason         = srequest.reason 
        copyrequest.source-name     = srequest.source-name.
END.
