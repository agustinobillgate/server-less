
DEFINE TEMP-TABLE t-head /*Display to Table UI Reparation History*/
    FIELD reqno     AS CHAR FORMAT "x(8)"
    FIELD datum     AS CHAR FORMAT "x(10)"
    FIELD task      AS CHAR FORMAT "x(36)"
    FIELD str-stat  AS CHAR FORMAT "x(10)"
.

DEFINE TEMP-TABLE t-line-cost /*Display to Table UI Reparation History*/
    FIELD reqno     AS CHAR FORMAT "x(8)"
    FIELD artno     AS CHAR FORMAT "x(8)"
    FIELD bezeich2  AS CHAR FORMAT "x(32)"
    FIELD qty       AS CHAR FORMAT "x(8)"
    FIELD price     AS CHAR FORMAT "x(19)"
    FIELD tot-dtl   AS CHAR FORMAT "x(19)"
.

DEFINE TEMP-TABLE t-line-vendor /*Display to Table UI Reparation History*/
    FIELD reqno         AS CHAR FORMAT "x(8)"
    FIELD outsource     AS CHAR FORMAT "x(8)"
    FIELD vendor-nm     AS CHAR FORMAT "x(32)"
    FIELD startdate     AS CHAR FORMAT "x(10)"
    FIELD finishdate    AS CHAR FORMAT "x(10)"        
    FIELD price         AS CHAR FORMAT "x(19)"
    FIELD tot-dtl       AS CHAR FORMAT "x(19)"
.

DEFINE TEMP-TABLE MainAction
    FIELD Maintainnr    AS INTEGER
    FIELD action-nr     AS INTEGER
    FIELD action-nm     AS CHAR        FORMAT "x(30)"
    FIELD create-date   AS DATE
    FIELD create-time   AS INTEGER
    FIELD time-str      AS CHAR
    FIELD create-by     AS CHAR.

DEFINE TEMP-TABLE tMaintain 
    FIELD maintainnr    AS INTEGER
    FIELD workdate      AS DATE
    FIELD donedate      AS DATE
    FIELD estworkdate   AS DATE
    FIELD type          AS INTEGER
    FIELD type-nm       AS CHAR         FORMAT "x(30)"
    FIELD typework      AS INTEGER
    FIELD typework-nm   AS CHAR         FORMAT "x(30)"
    FIELD location      AS INTEGER
    FIELD location-nm   AS CHAR         FORMAT "x(30)"
    FIELD zinr          AS CHAR
    FIELD propertynr    AS INTEGER
    FIELD property-nm   AS CHAR         FORMAT "x(30)"
    FIELD maintask      AS INTEGER
    FIELD maintask-nm   AS CHAR         FORMAT "x(30)"
    FIELD category      AS INTEGER
    FIELD category-nm   AS CHAR         FORMAT "x(30)"
    FIELD pic           AS INTEGER
    FIELD pic-nm        AS CHAR         FORMAT "x(30)"
    FIELD comments      AS CHAR         FORMAT "x(30)"
    FIELD create-by     AS CHAR
    FIELD create-date   AS DATE
    FIELD memo          AS CHAR         FORMAT "x(30)".

DEFINE TEMP-TABLE fLocation
    FIELD loc-nr  AS INTEGER 
    FIELD loc-nm AS CHAR FORMAT "x(36)" COLUMN-LABEL "Location".

DEFINE TEMP-TABLE tLocation
    FIELD loc-nr  AS INTEGER 
    FIELD loc-nm AS CHAR FORMAT "x(36)" COLUMN-LABEL "Location".

DEFINE TEMP-TABLE q1-list
    FIELD datum     LIKE eg-moveproperty.datum
    FIELD fr-room   LIKE eg-moveproperty.fr-room
    FIELD f-loc-nm  AS CHAR FORMAT "x(36)"
    FIELD t-loc-nm  AS CHAR FORMAT "x(36)"
    FIELD to-room   LIKE eg-moveproperty.to-room.

DEF INPUT PARAMETER pvILanguage AS INTEGER          NO-UNDO.
DEF INPUT PARAMETER prop-nr AS INT.
DEF OUTPUT PARAMETER e-price AS DECIMAL.
DEF OUTPUT PARAMETER e-datum AS DATE.
DEF OUTPUT PARAMETER avail-eg-property AS LOGICAL INIT NO.
DEF OUTPUT PARAMETER rec-meter AS INTEGER. 
DEF OUTPUT PARAMETER rec-hour  AS INTEGER. 
DEF OUTPUT PARAMETER rec-date  AS DATE.
DEF OUTPUT PARAMETER rec-time  AS CHAR.
DEF OUTPUT PARAMETER tot-cost AS CHAR FORMAT "x(19)".
DEF OUTPUT PARAMETER tot-vend AS CHAR FORMAT "x(19)".
DEF OUTPUT PARAMETER TABLE FOR t-head.
DEF OUTPUT PARAMETER TABLE FOR t-line-cost.
DEF OUTPUT PARAMETER TABLE FOR t-line-vendor.
DEF OUTPUT PARAMETER TABLE FOR q1-list.
DEF OUTPUT PARAMETER TABLE FOR tMaintain.
DEF OUTPUT PARAMETER TABLE FOR MainAction.


DEF BUFFER qbuff FOR eg-location.
DEF BUFFER tbuff FOR l-artikel.
DEF VAR atotal AS INTEGER.
DEF VAR tot AS INTEGER.
DEF VAR btotal AS DECIMAL.
DEFINE VARIABLE int-str AS CHAR EXTENT 5 INITIAL
    ["New",  "Processed", "Done",  "Postponed", "Closed"].
{SupertransBL.i} 
DEF VAR lvCAREA AS CHAR INITIAL "sel-lookMaintain-web".
DEFINE VARIABLE typestr  AS CHAR     EXTENT 3 FORMAT "x(16)" NO-UNDO.
typestr[1] = translateExtended("Scheduled", lvCAREA, "").
typestr[2] = translateExtended("Processed", lvCAREA, "").
typestr[3] = translateExtended("Done", lvCAREA, "").
DEFINE VARIABLE typeworkstr AS CHAR     EXTENT 6  FORMAT "x(16)" NO-UNDO.
typeworkstr[1] = translateExtended("Daily", lvCAREA, "").
typeworkstr[2] = translateExtended("Weekly", lvCAREA, "").
typeworkstr[3] = translateExtended("Monthly", lvCAREA, "").
typeworkstr[4] = translateExtended("Quarter", lvCAREA, "").
typeworkstr[5] = translateExtended("Half Yearly", lvCAREA, "").
typeworkstr[6] = translateExtended("Yearly", lvCAREA, "").


FOR EACH fLocation:
    DELETE fLocation.
END.

FOR EACH tLocation:
    DELETE tLocation.
END.

FOR EACH qbuff NO-LOCK:
    CREATE tLocation.
    ASSIGN tLocation.loc-nr = qbuff.nr
        tLocation.loc-nm = qbuff.bezeich.

    CREATE fLocation.
    ASSIGN fLocation.loc-nr = qbuff.nr
        fLocation.loc-nm = qbuff.bezeich.
END.

FOR EACH eg-moveproperty WHERE eg-moveproperty.property-nr = prop-nr NO-LOCK,
    FIRST flocation WHERE flocation.loc-nr = eg-moveproperty.fr-location NO-LOCK,
    FIRST tlocation WHERE tlocation.loc-nr = eg-moveproperty.to-location NO-LOCK:
    CREATE q1-list.
    ASSIGN
    q1-list.datum     = eg-moveproperty.datum
    q1-list.f-loc-nm  = flocation.loc-nm
    q1-list.fr-room   = eg-moveproperty.fr-room
    q1-list.t-loc-nm  = tlocation.loc-nm
    q1-list.to-room   = eg-moveproperty.to-room.
END.


FIND FIRST eg-property WHERE eg-property.nr = prop-nr NO-LOCK NO-ERROR.
IF AVAILABLE eg-property THEN
DO:
    avail-eg-property = YES.
    ASSIGN  e-price = eg-property.price
            e-datum = eg-property.datum.
END.

RUN create-history.
RUN create-maintain.
RUN if-meter.

PROCEDURE create-history:
    DEF VAR str-date1 AS CHAR.
    DEF VAR str-date2 AS CHAR.
    DEF VAR char4 AS CHAR.
    DEF VAR a AS CHAR.
    DEF VAR b AS CHAR.
    DEF VAR vendo-nm AS CHAR.
    DEF VAR itotal AS DECIMAL.    

    FOR EACH eg-request WHERE eg-request.propertynr = prop-nr NO-LOCK BY eg-request.opened-date BY eg-request.reqnr :
        IF eg-request.opened-date = ? THEN  a = "".
        ELSE a = STRING(eg-request.opened-date ,"99/99/99").

        FIND FIRST eg-subtask WHERE eg-subtask.sub-CODE = eg-request.sub-task NO-LOCK NO-ERROR.
        IF AVAILABLE eg-subtask THEN char4 = eg-subtask.bezeich.
        ELSE char4 = "".

        CREATE t-head.
        ASSIGN
             t-head.reqno       = STRING(eg-request.reqnr , "->>>>>>9")
             t-head.datum       = a
             t-head.task        = char4
             t-head.str-stat    = int-str[eg-request.reqstatus]
        .

        FIND FIRST eg-queasy WHERE eg-queasy.KEY = 1 AND eg-queasy.reqnr = eg-request.reqnr NO-LOCK NO-ERROR.
        IF AVAILABLE eg-queasy THEN
        DO:                        
            FOR EACH eg-queasy WHERE eg-queasy.KEY = 1 AND eg-queasy.reqnr = eg-request.reqnr NO-LOCK:
    
                FIND FIRST tbuff WHERE tbuff.artnr = eg-queasy.stock-nr NO-LOCK NO-ERROR.
                IF AVAILABLE tbuff THEN
                DO:
                    itotal  = eg-queasy.deci1 * eg-queasy.price.
                    
                    /* Get from another API
                    CREATE t-line-cost.
                    ASSIGN
                        t-line-cost.reqno    = STRING(eg-request.reqnr , "->>>>>>9")
                        t-line-cost.artno    = STRING(eg-queasy.stock-nr, "9999999")
                        t-line-cost.bezeich2 = tbuff.bezeich
                        t-line-cost.qty      = STRING(eg-queasy.deci1 ,"->>>>>>9")
                        t-line-cost.price    = STRING(eg-queasy.price, "->>>,>>>,>>>,>>9.99")
                        t-line-cost.tot-dtl  = STRING(itotal , "->>>,>>>,>>>,>>9.99")        
                    .
                    */            
                END. 
                tot = tot + itotal.                
            END.
        END.

        FIND FIRST eg-vperform WHERE eg-vperform.reqnr = eg-request.reqnr NO-LOCK NO-ERROR.
        IF AVAILABLE eg-vperform THEN
        DO:            
            FOR EACH eg-vperform WHERE eg-vperform.reqnr = eg-request.reqnr NO-LOCK:
                /* Get from another API
                FIND FIRST eg-vendor WHERE eg-vendor.vendor-nr = eg-vperform.vendor-nr NO-LOCK NO-ERROR.
                IF AVAILABLE eg-vendor THEN
                DO:
                    vendo-nm = eg-vendor.bezeich.
                END.
                ELSE
                DO:
                    vendo-nm = "Undefine".
                END.
                
                IF eg-vperform.startdate = ? THEN str-date1 = "".
                ELSE str-date1 = STRING(eg-vperform.startdate , "99/99/99").
    
                IF eg-vperform.finishdate = ? THEN str-date2 = "".
                ELSE str-date2 = STRING(eg-vperform.finishdate , "99/99/99").

                CREATE t-line-vendor.
                ASSIGN                                                                                      
                    t-line-vendor.reqno         = STRING(eg-request.reqnr , "->>>>>>9")                        
                    t-line-vendor.outsource     = STRING(eg-vperform.perform-nr, "9999999")
                    t-line-vendor.vendor-nm     = vendo-nm
                    t-line-vendor.startdate     = str-date1
                    t-line-vendor.finishdate    = str-date2   
                    t-line-vendor.price         = STRING(eg-vperform.price , "->>>,>>>,>>>,>>9.99")
                    t-line-vendor.tot-dtl       = t-line-vendor.tot-dtl + STRING(eg-vperform.price , "->>>,>>>,>>>,>>9.99")
                .       
                */
                tot = tot + eg-vperform.price.                   
            END.
        END. 

        IF tot NE 0 THEN 
        DO:
            btotal = btotal + tot.
            tot = 0.
        END.            
    END.

    IF btotal NE 0 THEN tot-cost = STRING(btotal, "->>>,>>>,>>>,>>9.99").
END PROCEDURE.

PROCEDURE create-maintain :
    DEF BUFFER mainbuff     FOR eg-maintain.
    DEF BUFFER mdetailBuff  FOR eg-mdetail.
    DEF BUFFER actionBuff   FOR eg-action.

    DEF VAR pic-nm          AS CHAR     FORMAT "x(30)".
    DEF VAR type-nm         AS CHAR     FORMAT "x(30)".
    DEF VAR typework-nm     AS CHAR     FORMAT "x(30)".

    DEF VAR action-nm       AS CHAR     FORMAT "x(30)".

     FOR EACH mainbuff WHERE mainbuff.propertynr = prop-nr USE-INDEX nr_ix NO-LOCK:

        FIND FIRST eg-staff WHERE eg-staff.nr = mainbuff.pic USE-INDEX nr_index NO-LOCK NO-ERROR.
        IF AVAILABLE eg-staff THEN pic-nm  = eg-staff.NAME .
        ELSE pic-nm  = "".

        CREATE tmaintain.
        ASSIGN tmaintain.maintainnr     = mainbuff.maintainnr
                tmaintain.workdate      = mainbuff.workdate
                tmaintain.donedate      = mainbuff.donedate
                tmaintain.estworkdate   = mainbuff.estworkdate
                tmaintain.type          = mainbuff.TYPE
                tmaintain.type-nm       = typestr[mainbuff.TYPE]
                tmaintain.typework      = mainbuff.typework
                tmaintain.typework-nm   = typeworkstr[mainbuff.TYPEwork]
                tmaintain.pic           = mainbuff.pic
                tmaintain.pic-nm        = pic-nm
                tmaintain.comments      = mainbuff.comments.

        FOR EACH mdetailbuff WHERE mdetailbuff.KEY = 1 AND mdetailbuff.maintainnr = mainbuff.maintainnr NO-LOCK:

            FIND FIRST actionbuff WHERE actionbuff.actionnr = mdetailbuff.nr NO-LOCK NO-ERROR.
            IF AVAILABLE actionBuff THEN
            DO:
                action-nm = actionbuff.bezeich.
            END.
            ELSE
            DO:
                action-nm = "".
            END.
            
            CREATE mainAction.
            ASSIGN mainaction.Maintainnr    = mdetailbuff.maintainnr
                    mainaction.action-nr    = mdetailbuff.nr 
                    mainaction.action-nm    = action-nm 
                    mainaction.create-date  = mdetailbuff.create-date 
                    mainaction.create-time  = mdetailbuff.create-time 
                    mainaction.time-str     = STRING(mdetailbuff.create-time , "HH:MM:SS")
                    mainaction.create-by    = mdetailbuff.create-by 
                .
        END.
     END.    
END.

PROCEDURE if-Meter:
    FIND FIRST eg-property WHERE eg-property.nr = prop-nr AND eg-property.meterrec = YES
        USE-INDEX nr_index NO-LOCK NO-ERROR.
    IF AVAILABLE eg-property THEN
    DO:
        FIND LAST eg-propmeter WHERE eg-propmeter.propertynr = prop-nr NO-LOCK NO-ERROR .
        IF AVAILABLE eg-propmeter THEN
        DO:
            ASSIGN rec-meter    = eg-propmeter.val-meter
                   rec-hour     = eg-propmeter.val-hour
                   rec-date     = eg-propmeter.rec-date
                   rec-time     = "" /*STRING (eg-propmeter.rec-time , "HH:MM")*/ .
        END.
        ELSE
        DO:
            ASSIGN rec-meter    = 0
                   rec-hour     = 0
                   rec-date     = ?
                   rec-time     = "".
        END.
    END.
    ELSE
    DO:
            ASSIGN rec-meter    = 0
                   rec-hour     = 0
                   rec-date     = ?
                   rec-time     = "" .
    END. 
    /*MT
    DISP rec-meter rec-hour rec-date /*rec-time*/ WITH FRAME frame1.
    ENABLE rec-meter rec-hour rec-date /*rec-time*/ WITH FRAME frame1.
    ASSIGN rec-meter:READ-ONLY IN FRAME frame1 =YES
           rec-hour:READ-ONLY IN FRAME frame1 = YES
           rec-date:READ-ONLY IN FRAME frame1 = YES
           /*rec-time:READ-ONLY IN FRAME frame1 =YES*/ .
    */
END.
