/*FD Dec 15, 2020 => BL for vhpweb based move from ui to BL*/

DEF TEMP-TABLE t-eg-request LIKE eg-request.

DEFINE TEMP-TABLE sRequest
    FIELD reqnr             AS INTEGER
    FIELD opendate          AS DATE
    FIELD status-str        AS CHAR     FORMAT "x(20)"
    FIELD Source-str        AS CHAR     FORMAT "x(20)"
    FIELD source-name       AS CHAR     FORMAT "x(30)"
    FIELD process-date      AS DATE
    FIELD closed-date       AS DATE  
    FIELD urgency           AS CHAR     FORMAT "x(20)"  
    FIELD category-str      AS CHAR     FORMAT "x(24)"
    FIELD deptnum           AS INTEGER
    FIELD pmaintask         AS INTEGER
    FIELD maintask          AS CHAR     FORMAT "x(24)"   
    FIELD plocation         AS INTEGER
    FIELD location          AS CHAR     FORMAT "x(24)"
    FIELD zinr              AS CHAR     FORMAT "x(20)"
    FIELD property          AS INTEGER
    FIELD property-nm       AS CHAR     FORMAT "x(30)"
    FIELD pic-str           AS CHAR     FORMAT "x(24)" 
    FIELD sub-str           AS CHAR     FORMAT "x(24)"
    FIELD ex-finishdate     AS DATE
    FIELD ex-finishtime     AS CHAR
    FIELD ex-Finish         AS CHAR     FORMAT "x(20)"
    FIELD done-date         AS DATE
    FIELD done-time         AS CHAR
    FIELD done              AS CHAR     FORMAT "x(20)"
    FIELD memo              AS CHAR     FORMAT "x(50)"
    FIELD task-def          AS CHAR     FORMAT "x(50)"
    FIELD task-solv         AS CHAR     FORMAT "x(50)"
    FIELD SOURCE            AS INTEGER
    FIELD category          AS INTEGER
    FIELD reqstatus         AS INTEGER
    FIELD sub-task          AS CHAR
    FIELD assign-to         AS INTEGER
    FIELD reason            AS CHAR     FORMAT "x(60)".

DEFINE TEMP-TABLE copyRequest
    FIELD reqnr             AS INTEGER
    FIELD opendate          AS DATE
    FIELD status-str        AS CHAR     FORMAT "x(20)" 
    FIELD Source-str        AS CHAR     FORMAT "x(20)"
    FIELD source-name       AS CHAR     FORMAT "x(30)"
    FIELD process-date      AS DATE
    FIELD closed-date       AS DATE  
    FIELD urgency           AS CHAR     FORMAT "x(20)"  
    FIELD category-str      AS CHAR     FORMAT "x(24)"
    FIELD deptnum           AS INTEGER
    FIELD pmaintask         AS INTEGER
    FIELD maintask          AS CHAR     FORMAT "x(24)"   
    FIELD plocation         AS INTEGER
    FIELD location          AS CHAR     FORMAT "x(24)"
    FIELD zinr              AS CHAR     FORMAT "x(20)"
    FIELD property          AS INTEGER
    FIELD property-nm       AS CHAR     FORMAT "x(30)"
    FIELD pic-str           AS CHAR     FORMAT "x(24)" 
    FIELD sub-str           AS CHAR     FORMAT "x(24)"
    FIELD ex-finishdate     AS DATE
    FIELD ex-finishtime     AS CHAR
    FIELD ex-finish         AS CHAR     FORMAT "x(20)"
    FIELD done-date         AS DATE
    FIELD done-time         AS CHAR
    FIELD done              AS CHAR     FORMAT "x(20)"
    FIELD memo              AS CHAR     FORMAT "x(50)"
    FIELD task-def          AS CHAR     FORMAT "x(50)"
    FIELD task-solv         AS CHAR     FORMAT "x(50)"
    FIELD SOURCE            AS INTEGER
    FIELD category          AS INTEGER
    FIELD reqstatus         AS INTEGER
    FIELD sub-task          AS CHAR
    FIELD assign-to         AS INTEGER
    FIELD reason            AS CHAR     FORMAT "x(60)"
    FIELD str               AS CHAR     FORMAT "x(2)" INITIAL "".

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

DEFINE TEMP-TABLE tpic
    FIELD pic-nr AS INTEGER
    FIELD pic-nm AS CHAR FORMAT "x(24)" COLUMN-LABEL "Pic"
    FIELD pic-selected AS LOGICAL INITIAL NO
    FIELD pic-Dept AS INTEGER.

DEFINE TEMP-TABLE tsubtask
    FIELD sub-nr AS CHAR
    FIELD sub-nm AS CHAR    FORMAT "x(24)"
    FIELD sub-selected AS LOGICAL INITIAL NO.

DEFINE TEMP-TABLE tsource
    FIELD source-nr AS INTEGER
    FIELD source-nm AS CHAR  FORMAT "x(24)"   
    FIELD source-selected AS LOGICAL INITIAL NO.

DEFINE TEMP-TABLE tcategory
    FIELD categ-nr AS INTEGER
    FIELD categ-nm AS CHAR  FORMAT "x(24)"
    FIELD categ-selected AS LOGICAL INITIAL NO.

DEFINE TEMP-TABLE tLocation
    FIELD loc-nr  AS INTEGER 
    FIELD loc-nm  AS CHAR FORMAT "x(24)" COLUMN-LABEL "Location"
    FIELD loc-selected AS LOGICAL INITIAL NO
    FIELD loc-guest    AS LOGICAL INITIAL NO.

DEFINE TEMP-TABLE tMaintask
    FIELD Main-nr  AS INTEGER 
    FIELD Main-nm  AS CHAR FORMAT "x(24)" COLUMN-LABEL "Object"
    FIELD main-selected AS LOGICAL INITIAL NO.

DEFINE TEMP-TABLE troom
    FIELD room-nm AS CHAR FORMAT "x(24)" COLUMN-LABEL "Room"
    FIELD room-Selected AS LOGICAL INITIAL NO.

DEFINE INPUT PARAMETER all-room     AS LOGICAL.
DEFINE INPUT PARAMETER all-property AS LOGICAL.
DEFINE INPUT PARAMETER all-pic      AS LOGICAL.
DEFINE INPUT PARAMETER all-subtask  AS LOGICAL.
DEFINE INPUT PARAMETER all-source   AS LOGICAL.
DEFINE INPUT PARAMETER all-category AS LOGICAL.
DEFINE INPUT PARAMETER all-location AS LOGICAL.
DEFINE INPUT PARAMETER all-maintask AS LOGICAL.
DEFINE INPUT PARAMETER cmb-operand  AS INTEGER.
DEFINE INPUT PARAMETER fdate        AS DATE.
DEFINE INPUT PARAMETER tdate        AS DATE.
DEFINE INPUT PARAMETER calctime     AS INTEGER.
DEFINE INPUT PARAMETER calctime1    AS INTEGER.
DEFINE INPUT-OUTPUT PARAMETER TABLE FOR tpic.
DEFINE INPUT-OUTPUT PARAMETER TABLE FOR tsubtask.
DEFINE INPUT-OUTPUT PARAMETER TABLE FOR tsource.
DEFINE INPUT-OUTPUT PARAMETER TABLE FOR tcategory.
DEFINE INPUT-OUTPUT PARAMETER TABLE FOR tLocation.
DEFINE INPUT-OUTPUT PARAMETER TABLE FOR tMaintask.
DEFINE OUTPUT PARAMETER TABLE FOR tproperty.
DEFINE OUTPUT PARAMETER TABLE FOR troom.
DEFINE OUTPUT PARAMETER TABLE FOR copyRequest.

DEFINE VARIABLE int-str AS CHAR EXTENT 3.
int-str[1] = "Low" .
int-str[2] = "Medium".
int-str[3] = "High".

RUN Open-query.

PROCEDURE Open-query:
    DEF VAR d AS INTEGER.
    DEF VAR e AS INTEGER.
    DEF VAR calday AS INTEGER.

    DEF VAR full-Finish AS CHAR.
    DEF VAR full-done  AS CHAR.

    RUN eg-repduration-all-locationbl.p 
        (all-room, INPUT TABLE tLocation, INPUT TABLE tmaintask,
            OUTPUT TABLE troom, OUTPUT TABLE tproperty).

    IF all-property THEN
        FOR EACH tproperty:
            ASSIGN tproperty.prop-selected = YES.
        END.

    IF all-pic THEN
        FOR EACH tpic:
            ASSIGN tpic.pic-selected = YES.
        END.

     IF all-subtask THEN
        FOR EACH tsubtask:
            ASSIGN tsubtask.sub-selected = YES.
        END.

    IF all-source THEN
        FOR EACH tsource:
            ASSIGN tsource.source-selected = YES.
        END.

    IF all-category THEN
        FOR EACH tcategory:
            ASSIGN tcategory.categ-selected = YES.
        END.

    IF all-location THEN
        FOR EACH tLocation:
            ASSIGN tLocation.loc-selected = YES.
        END.

    IF all-maintask THEN
        FOR EACH tMaintask:
            ASSIGN tMaintask.main-selected = YES.
        END.    

    FOR EACH srequest:
        DELETE srequest.
    END.

    FOR EACH copyrequest:
        DELETE copyrequest.
    END.

    RUN eg-repduration-open-querybl.p (fdate, tdate, OUTPUT TABLE t-eg-request).

    IF cmb-operand = 1 THEN
    DO:
        FOR EACH t-eg-request :

            full-finish = string(t-eg-request.ex-finishdate , "99/99/99") + " " + string(t-eg-request.ex-finishtime ,"HH:MM:SS").
            full-done   = STRING(t-eg-request.done-date , "99/99/99") + " " + string(t-eg-request.done-time ,"HH:MM:SS").

            IF t-eg-request.ex-finishdate = t-eg-request.done-date THEN
            DO:
                
                IF (t-eg-request.ex-finishtime - t-eg-request.done-time) >= 0 AND (t-eg-request.ex-finishtime - t-eg-request.done-time) < calctime THEN
                DO:                    
                    FIND FIRST tproperty WHERE tproperty.prop-nr = t-eg-request.propertynr NO-LOCK NO-ERROR.
                    IF AVAILABLE tproperty THEN
                    DO:
                        CREATE sRequest.
                        ASSIGN sRequest.reqnr       = t-eg-request.reqnr
                                 sRequest.opendate      = t-eg-request.opened-date
                                 sRequest.process-date  = t-eg-request.process-date
                                 sRequest.closed-date   = t-eg-request.closed-date
                                 sRequest.urgency       = string(t-eg-request.urgency)
                                 srequest.source-name   = t-eg-request.source-name
                                 sRequest.ex-finish     = full-finish
                                 sRequest.done          = full-done  
                                 sRequest.ex-finishdate = t-eg-request.ex-finishdate
                                 sRequest.ex-finishtime = string(t-eg-request.ex-finishtime ,"HH:MM:SS") 
                                 sRequest.done-date     = t-eg-request.done-date
                                 sRequest.done-time     = string(t-eg-request.done-time, "HH:MM:SS")
                                 sRequest.memo          = t-eg-request.memo
                                 sRequest.task-def      = t-eg-request.task-def
                                 sRequest.task-solv     = t-eg-request.task-solv
                                 sRequest.pmaintask     = tproperty.pmain-nr
                                 sRequest.plocation     = tproperty.ploc-nr
                                 srequest.zinr          = t-eg-request.zinr
                                 srequest.SOURCE        = t-eg-request.SOURCE
                                 srequest.category      = tproperty.pcateg-nr /*t-eg-request.category*/
                                 srequest.reqstatus     = t-eg-request.reqstatus
                                 srequest.sub-task      = t-eg-request.sub-task
                                 srequest.assign-to     = t-eg-request.assign-to
                                 srequest.property      = t-eg-request.propertynr
                                 srequest.reason        = t-eg-request.reasondonetime.
                    END.        
                END.
            END.
            ELSE IF t-eg-request.ex-finishdate > t-eg-request.done-date THEN
            DO:
                calday = t-eg-request.ex-finishdate - t-eg-request.done-date .
                d = (calday * 86399) + t-eg-request.done-time.
                e = d - t-eg-request.ex-finishtime.

                IF e >= 0 AND e < calctime THEN
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
                               sRequest.ex-finish       = full-finish
                               sRequest.done            = full-done  
                               sRequest.ex-finishdate   = t-eg-request.ex-finishdate
                               sRequest.ex-finishtime   = string(t-eg-request.ex-finishtime , "HH:MM:SS")
                               sRequest.done-date       = t-eg-request.done-date
                               sRequest.done-time       = string(t-eg-request.done-time, "HH:MM:SS")
                               sRequest.memo            = t-eg-request.memo
                               sRequest.task-def        = t-eg-request.task-def
                               sRequest.task-solv       = t-eg-request.task-solv
                               sRequest.pmaintask       = tproperty.pmain-nr
                               sRequest.plocation       = tproperty.ploc-nr
                               srequest.zinr            = t-eg-request.zinr
                               srequest.SOURCE          = t-eg-request.SOURCE
                               srequest.category        = tproperty.pcateg-nr /*t-eg-request.category*/
                               srequest.reqstatus       = t-eg-request.reqstatus
                               srequest.sub-task        = t-eg-request.sub-task
                               srequest.assign-to       = t-eg-request.assign-to
                               srequest.property        = t-eg-request.propertynr
                               srequest.reason          = t-eg-request.reasondonetime.
                    END.        
                END.
            END.
        END.
    END.
    ELSE IF cmb-operand = 2 THEN
    DO:
        FOR EACH t-eg-request :

            full-finish = string(t-eg-request.ex-finishdate , "99/99/99") + " " + string(t-eg-request.ex-finishtime ,"HH:MM:SS").
            full-done   = STRING(t-eg-request.done-date , "99/99/99") + " " + string(t-eg-request.done-time ,"HH:MM:SS").

            IF t-eg-request.ex-finishdate = t-eg-request.done-date THEN
            DO:
                IF (t-eg-request.ex-finishtime - t-eg-request.done-time) >= 0 AND (t-eg-request.ex-finishtime - t-eg-request.done-time) <= calctime THEN
                DO: 
                    FIND FIRST tproperty WHERE tproperty.prop-nr = t-eg-request.propertynr NO-LOCK NO-ERROR.
                    IF AVAILABLE tproperty THEN
                    DO:
                        CREATE sRequest.
                        ASSIGN sRequest.reqnr       = t-eg-request.reqnr
                                 sRequest.opendate      = t-eg-request.opened-date
                                 sRequest.process-date  = t-eg-request.process-date
                                 sRequest.closed-date   = t-eg-request.closed-date
                                 sRequest.urgency       = string(t-eg-request.urgency)
                                 srequest.source-name   = t-eg-request.source-name  
                                 sRequest.ex-finish     = full-finish
                                 sRequest.done          = full-done  
                                 sRequest.ex-finishdate = t-eg-request.ex-finishdate
                                 sRequest.ex-finishtime = string(t-eg-request.ex-finishtime ,"HH:MM:SS") 
                                 sRequest.done-date     = t-eg-request.done-date
                                 sRequest.done-time     = string(t-eg-request.done-time, "HH:MM:SS")
                                 sRequest.memo          = t-eg-request.memo
                                 sRequest.task-def      = t-eg-request.task-def
                                 sRequest.task-solv     = t-eg-request.task-solv
                                 sRequest.pmaintask     = tproperty.pmain-nr
                                 sRequest.plocation     = tproperty.ploc-nr
                                 srequest.zinr          = t-eg-request.zinr
                                 srequest.SOURCE        = t-eg-request.SOURCE
                                 srequest.category      = tproperty.pcateg-nr /*t-eg-request.category*/
                                 srequest.reqstatus     = t-eg-request.reqstatus
                                 srequest.sub-task      = t-eg-request.sub-task
                                 srequest.assign-to     = t-eg-request.assign-to
                                 srequest.property      = t-eg-request.propertynr
                                 srequest.reason        = t-eg-request.reasondonetime.
                    END.        
                END.
            END.
            ELSE IF t-eg-request.ex-finishdate > t-eg-request.done-date THEN
            DO:
                calday = t-eg-request.ex-finishdate - t-eg-request.done-date .
                d = (calday * 86399) + t-eg-request.done-time.
                e = d - t-eg-request.ex-finishtime.

                IF e >= 0 AND e <= calctime THEN
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
                               sRequest.ex-finish       = full-finish
                               sRequest.done            = full-done  
                               sRequest.ex-finishdate   = t-eg-request.ex-finishdate
                               sRequest.ex-finishtime   = string(t-eg-request.ex-finishtime , "HH:MM:SS")
                               sRequest.done-date       = t-eg-request.done-date
                               sRequest.done-time       = string(t-eg-request.done-time, "HH:MM:SS")
                               sRequest.memo            = t-eg-request.memo
                               sRequest.task-def        = t-eg-request.task-def
                               sRequest.task-solv       = t-eg-request.task-solv
                               sRequest.pmaintask       = tproperty.pmain-nr
                               sRequest.plocation       = tproperty.ploc-nr
                               srequest.zinr            = t-eg-request.zinr
                               srequest.SOURCE          = t-eg-request.SOURCE
                               srequest.category        = tproperty.pcateg-nr /*t-eg-request.category*/
                               srequest.reqstatus       = t-eg-request.reqstatus
                               srequest.sub-task        = t-eg-request.sub-task
                               srequest.assign-to       = t-eg-request.assign-to
                               srequest.property        = t-eg-request.propertynr
                               srequest.reason          = t-eg-request.reasondonetime.
                    END.        
                END.
            END.
        END.
    END.
    ELSE IF cmb-operand = 3 THEN
    DO:

        FOR EACH t-eg-request :

            full-finish = string(t-eg-request.ex-finishdate , "99/99/99") + " " + string(t-eg-request.ex-finishtime ,"HH:MM:SS").
            full-done   = STRING(t-eg-request.done-date , "99/99/99") + " " + string(t-eg-request.done-time ,"HH:MM:SS").

            IF t-eg-request.ex-finishdate = t-eg-request.done-date THEN
            DO:
                IF (t-eg-request.done-time - t-eg-request.ex-finishtime) > calctime THEN
                DO: 
                    FIND FIRST tproperty WHERE tproperty.prop-nr = t-eg-request.propertynr NO-LOCK NO-ERROR.
                    IF AVAILABLE tproperty THEN
                    DO:
                        CREATE sRequest.
                        ASSIGN sRequest.reqnr       = t-eg-request.reqnr
                                 sRequest.opendate      = t-eg-request.opened-date
                                 sRequest.process-date  = t-eg-request.process-date
                                 sRequest.closed-date   = t-eg-request.closed-date
                                 sRequest.urgency       = string(t-eg-request.urgency)
                                 srequest.source-name   = t-eg-request.source-name  
                                 sRequest.ex-finish     = full-finish
                                 sRequest.done          = full-done  
                                 sRequest.ex-finishdate = t-eg-request.ex-finishdate
                                 sRequest.ex-finishtime = string(t-eg-request.ex-finishtime ,"HH:MM:SS") 
                                 sRequest.done-date     = t-eg-request.done-date
                                 sRequest.done-time     = string(t-eg-request.done-time, "HH:MM:SS")
                                 sRequest.memo          = t-eg-request.memo
                                 sRequest.task-def      = t-eg-request.task-def
                                 sRequest.task-solv     = t-eg-request.task-solv
                                 sRequest.pmaintask     = tproperty.pmain-nr
                                 sRequest.plocation     = tproperty.ploc-nr
                                 srequest.zinr          = t-eg-request.zinr
                                 srequest.SOURCE        = t-eg-request.SOURCE
                                 srequest.category      = tproperty.pcateg-nr /*t-eg-request.category*/
                                 srequest.reqstatus     = t-eg-request.reqstatus
                                 srequest.sub-task      = t-eg-request.sub-task
                                 srequest.assign-to     = t-eg-request.assign-to
                                 srequest.property      = t-eg-request.propertynr
                                 srequest.reason        = t-eg-request.reasondonetime.
                    END.        
                END.
            END.
            ELSE IF t-eg-request.ex-finishdate < t-eg-request.done-date THEN
            DO:
                calday = t-eg-request.done-date - t-eg-request.ex-finishdate .
                d = (calday * 86399) + t-eg-request.done-time.
                e = d - t-eg-request.ex-finishtime.

                IF e > calctime THEN
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
                               sRequest.ex-finish       = full-finish
                               sRequest.done            = full-done  
                               sRequest.ex-finishdate   = t-eg-request.ex-finishdate
                               sRequest.ex-finishtime   = string(t-eg-request.ex-finishtime , "HH:MM:SS")
                               sRequest.done-date       = t-eg-request.done-date
                               sRequest.done-time       = string(t-eg-request.done-time, "HH:MM:SS")
                               sRequest.memo            = t-eg-request.memo
                               sRequest.task-def        = t-eg-request.task-def
                               sRequest.task-solv       = t-eg-request.task-solv
                               sRequest.pmaintask       = tproperty.pmain-nr
                               sRequest.plocation       = tproperty.ploc-nr
                               srequest.zinr            = t-eg-request.zinr
                               srequest.SOURCE          = t-eg-request.SOURCE
                               srequest.category        = tproperty.pcateg-nr /*t-eg-request.category*/
                               srequest.reqstatus       = t-eg-request.reqstatus
                               srequest.sub-task        = t-eg-request.sub-task
                               srequest.assign-to       = t-eg-request.assign-to
                               srequest.property        = t-eg-request.propertynr
                               srequest.reason          = t-eg-request.reasondonetime.
                    END.        
                END.
            END.
        END.
    END.
    ELSE IF cmb-operand = 4 THEN
    DO:

        FOR EACH t-eg-request :

            full-finish = string(t-eg-request.ex-finishdate , "99/99/99") + " " + string(t-eg-request.ex-finishtime ,"HH:MM:SS").
            full-done   = STRING(t-eg-request.done-date , "99/99/99") + " " + string(t-eg-request.done-time ,"HH:MM:SS").

            IF t-eg-request.ex-finishdate = t-eg-request.done-date THEN
            DO:
                IF (t-eg-request.done-time - t-eg-request.ex-finishtime) >= calctime THEN
                DO: 
                    FIND FIRST tproperty WHERE tproperty.prop-nr = t-eg-request.propertynr NO-LOCK NO-ERROR.
                    IF AVAILABLE tproperty THEN
                    DO:
                        CREATE sRequest.
                        ASSIGN sRequest.reqnr       = t-eg-request.reqnr
                                 sRequest.opendate      = t-eg-request.opened-date
                                 sRequest.process-date  = t-eg-request.process-date
                                 sRequest.closed-date   = t-eg-request.closed-date
                                 sRequest.urgency       = string(t-eg-request.urgency)
                                 srequest.source-name   = t-eg-request.source-name  
                                 sRequest.ex-finish     = full-finish
                                 sRequest.done          = full-done  
                                 sRequest.ex-finishdate = t-eg-request.ex-finishdate
                                 sRequest.ex-finishtime = string(t-eg-request.ex-finishtime ,"HH:MM:SS") 
                                 sRequest.done-date     = t-eg-request.done-date
                                 sRequest.done-time     = string(t-eg-request.done-time, "HH:MM:SS")
                                 sRequest.memo          = t-eg-request.memo
                                 sRequest.task-def      = t-eg-request.task-def
                                 sRequest.task-solv     = t-eg-request.task-solv
                                 sRequest.pmaintask     = tproperty.pmain-nr
                                 sRequest.plocation     = tproperty.ploc-nr
                                 srequest.zinr          = t-eg-request.zinr
                                 srequest.SOURCE        = t-eg-request.SOURCE
                                 srequest.category      = tproperty.pcateg-nr /*t-eg-request.category*/
                                 srequest.reqstatus     = t-eg-request.reqstatus
                                 srequest.sub-task      = t-eg-request.sub-task
                                 srequest.assign-to     = t-eg-request.assign-to
                                 srequest.property      = t-eg-request.propertynr
                                 srequest.reason        =   t-eg-request.reasondonetime.
                    END.        
                END.
            END.
            ELSE IF t-eg-request.ex-finishdate < t-eg-request.done-date THEN
            DO:
              
                calday = t-eg-request.done-date - t-eg-request.ex-finishdate .
                d = (calday * 86399) + t-eg-request.done-time.
                e = d - t-eg-request.ex-finishtime.
                IF  e >= calctime THEN
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
                               sRequest.ex-finish       = full-finish
                               sRequest.done            = full-done  
                               sRequest.ex-finishdate   = t-eg-request.ex-finishdate
                               sRequest.ex-finishtime   = string(t-eg-request.ex-finishtime , "HH:MM:SS")
                               sRequest.done-date       = t-eg-request.done-date
                               sRequest.done-time       = string(t-eg-request.done-time, "HH:MM:SS")
                               sRequest.memo            = t-eg-request.memo
                               sRequest.task-def        = t-eg-request.task-def
                               sRequest.task-solv       = t-eg-request.task-solv
                               sRequest.pmaintask       = tproperty.pmain-nr
                               sRequest.plocation       = tproperty.ploc-nr
                               srequest.zinr            = t-eg-request.zinr
                               srequest.SOURCE          = t-eg-request.SOURCE
                               srequest.category        = tproperty.pcateg-nr /*t-eg-request.category*/
                               srequest.reqstatus       = t-eg-request.reqstatus
                               srequest.sub-task        = t-eg-request.sub-task
                               srequest.assign-to       = t-eg-request.assign-to
                               srequest.property        = t-eg-request.propertynr
                               srequest.reason          = t-eg-request.reasondonetime.
                    END.        
                END.
            END.
        END.
    END.
    ELSE IF cmb-operand = 5 THEN
    DO:
        FOR EACH t-eg-request :
            full-finish = string(t-eg-request.ex-finishdate , "99/99/99") + " " + string(t-eg-request.ex-finishtime ,"HH:MM:SS").
            full-done   = STRING(t-eg-request.done-date , "99/99/99") + " " + string(t-eg-request.done-time ,"HH:MM:SS").

            IF t-eg-request.ex-finishdate = t-eg-request.done-date THEN
            DO:
                IF (t-eg-request.done-time - t-eg-request.ex-finishtime) >= calctime AND (t-eg-request.done-time - t-eg-request.ex-finishtime) <= calctime1 THEN
                DO: 
                    FIND FIRST tproperty WHERE tproperty.prop-nr = t-eg-request.propertynr NO-LOCK NO-ERROR.
                    IF AVAILABLE tproperty THEN
                    DO:
                        CREATE sRequest.
                        ASSIGN sRequest.reqnr       = t-eg-request.reqnr
                                 sRequest.opendate      = t-eg-request.opened-date
                                 sRequest.process-date  = t-eg-request.process-date
                                 sRequest.closed-date   = t-eg-request.closed-date
                                 sRequest.urgency       = string(t-eg-request.urgency)
                                 srequest.source-name   = t-eg-request.source-name  
                                 sRequest.ex-finish     = full-finish
                                 sRequest.done          = full-done  
                                 sRequest.ex-finishdate = t-eg-request.ex-finishdate
                                 sRequest.ex-finishtime = string(t-eg-request.ex-finishtime ,"HH:MM:SS") 
                                 sRequest.done-date     = t-eg-request.done-date
                                 sRequest.done-time     = string(t-eg-request.done-time, "HH:MM:SS")
                                 sRequest.memo          = t-eg-request.memo
                                 sRequest.task-def      = t-eg-request.task-def
                                 sRequest.task-solv     = t-eg-request.task-solv
                                 sRequest.pmaintask     = tproperty.pmain-nr
                                 sRequest.plocation     = tproperty.ploc-nr
                                 srequest.zinr          = t-eg-request.zinr
                                 srequest.SOURCE        = t-eg-request.SOURCE
                                 srequest.category      = tproperty.pcateg-nr /*t-eg-request.category*/
                                 srequest.reqstatus     = t-eg-request.reqstatus
                                 srequest.sub-task      = t-eg-request.sub-task
                                 srequest.assign-to     = t-eg-request.assign-to
                                 srequest.property      = t-eg-request.propertynr
                                 srequest.reason        = t-eg-request.reasondonetime.
                    END.        
                END.
            END.
            ELSE IF t-eg-request.ex-finishdate < t-eg-request.done-date THEN
            DO:
              
                calday = t-eg-request.done-date - t-eg-request.ex-finishdate .
                d = (calday * 86399) + t-eg-request.done-time.
                e = d - t-eg-request.ex-finishtime.
                IF e >= calctime AND e <= calctime1 THEN
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
                               sRequest.ex-finish       = full-finish
                               sRequest.done            = full-done  
                               sRequest.ex-finishdate   = t-eg-request.ex-finishdate
                               sRequest.ex-finishtime   = string(t-eg-request.ex-finishtime , "HH:MM:SS")
                               sRequest.done-date       = t-eg-request.done-date
                               sRequest.done-time       = string(t-eg-request.done-time, "HH:MM:SS")
                               sRequest.memo            = t-eg-request.memo
                               sRequest.task-def        = t-eg-request.task-def
                               sRequest.task-solv       = t-eg-request.task-solv
                               sRequest.pmaintask       = tproperty.pmain-nr
                               sRequest.plocation       = tproperty.ploc-nr
                               srequest.zinr            = t-eg-request.zinr
                               srequest.SOURCE          = t-eg-request.SOURCE
                               srequest.category        = tproperty.pcateg-nr /*t-eg-request.category*/
                               srequest.reqstatus       = t-eg-request.reqstatus
                               srequest.sub-task        = t-eg-request.sub-task
                               srequest.assign-to       = t-eg-request.assign-to
                               srequest.property        = t-eg-request.propertynr
                               srequest.reason          = t-eg-request.reasondonetime.
                    END.        
                END.
            END.
        END.
    END.

    FOR EACH srequest WHERE srequest.opendate >= fdate AND srequest.opendate <= tdate NO-LOCK  , 
        /*FIRST comstatus WHERE comstatus.stat-nr = srequest.reqstatus AND comstatus.stat-selected NO-LOCK ,*/
        FIRST tsource WHERE tsource.source-nr = srequest.SOURCE AND tsource.source-selected NO-LOCK,
        FIRST tcategory WHERE tcategory.categ-nr = srequest.category AND tcategory.categ-selected NO-LOCK,
        FIRST tsubtask WHERE tsubtask.sub-nr = srequest.sub-task AND tsubtask.sub-selected NO-LOCK,
        FIRST tpic WHERE tpic.pic-nr = srequest.assign-to AND tpic.pic-selected NO-LOCK,
        FIRST tMaintask WHERE tMaintask.main-nr = srequest.pmaintask AND tMaintask.main-selected NO-LOCK,
        FIRST tLocation WHERE tLocation.loc-nr = srequest.plocation AND tLocation.loc-selected NO-LOCK,
        FIRST tproperty WHERE tproperty.prop-nr = srequest.property AND tproperty.prop-selected NO-LOCK:

        CREATE copyRequest.
        ASSIGN copyRequest.reqnr            = srequest.reqnr
               copyRequest.opendate         = srequest.opendate
                  /*copyRequest.status-str     = comstatus.stat-nm*/
               copyRequest.Source-str       = tsource.source-nm
               copyrequest.source-name      = srequest.source-name
               copyRequest.process-date     = srequest.process-date
               copyRequest.closed-date      = srequest.closed-date
               copyRequest.urgency          = int-str[int(srequest.urgency)]
               copyRequest.category-str     = tcategory.categ-nm
                  /*copyRequest.deptnum       AS INTEGER = srequest.*/
               copyRequest.pmaintask        = srequest.pmaintask
               copyRequest.maintask         = tMaintask.main-nm
               copyRequest.plocation        = srequest.plocation
               copyRequest.location         = tLocation.loc-nm
               copyRequest.zinr             = srequest.zinr
               copyRequest.property         = srequest.property
               copyRequest.property-nm      = tproperty.prop-nm
               copyRequest.pic-str          = tpic.pic-nm
               copyRequest.sub-str          = tsubtask.sub-nm
               copyRequest.ex-finish        = srequest.ex-finish
               copyRequest.done             = srequest.done                          
               copyRequest.ex-finishdate    = srequest.ex-finishdate
               copyRequest.ex-finishtime    = string(srequest.ex-finishtime , "HH:MM:SS")
               copyRequest.done-date        = srequest.done-date
               copyRequest.done-time        = string(srequest.done-time , "HH:MM:SS")
               copyRequest.memo             = srequest.memo
               copyRequest.task-def         = srequest.task-def
               copyRequest.task-solv        = srequest.task-solv
               copyRequest.SOURCE           = srequest.source
               copyRequest.category         = srequest.category
               copyRequest.reqstatus        = srequest.reqstatus
               copyRequest.sub-task         = srequest.sub-task
               copyRequest.assign-to        = srequest.assign-to
               copyRequest.reason           = srequest.reason.
    END.

    OPEN QUERY q1 FOR EACH copyrequest NO-LOCK.
END.
