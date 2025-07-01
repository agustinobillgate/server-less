/*FD Dec 17, 2020 => BL for vhpweb Based convert STR to Temp-Table*/

DEFINE TEMP-TABLE t-hisroom-head
    FIELD itemno    AS CHAR FORMAT "x(8)"
    FIELD bezeich   AS CHAR FORMAT "x(32)"
    FIELD flag      AS CHAR
.

DEFINE TEMP-TABLE t-hisroom-line
    FIELD itemno    AS CHAR FORMAT "x(8)"
    FIELD bezeich   AS CHAR FORMAT "x(32)"
    FIELD reqno     AS CHAR FORMAT "x(8)"
    FIELD opend     AS CHAR FORMAT "x(10)"
    FIELD processd  AS CHAR FORMAT "x(10)"
    FIELD doned     AS CHAR FORMAT "x(10)"
    FIELD subtask   AS CHAR FORMAT "x(30)"
    FIELD reqstat   AS CHAR FORMAT "x(20)"
    FIELD flag      AS CHAR
.

DEFINE TEMP-TABLE t-hisroom-line-cost
    FIELD itemno    AS CHAR FORMAT "x(8)"
    FIELD bezeich   AS CHAR FORMAT "x(32)"
    FIELD reqno     AS CHAR FORMAT "x(8)"
    FIELD flag      AS CHAR 
    FIELD artno     AS CHAR FORMAT "x(8)"
    FIELD bezeich2  AS CHAR FORMAT "x(32)"
    FIELD qty       AS CHAR FORMAT "x(8)"
    FIELD price     AS CHAR FORMAT "x(19)"
    FIELD tot-dtl   AS CHAR FORMAT "x(19)"
.

DEFINE TEMP-TABLE t-hisroom-line-vendor
    FIELD itemno        AS CHAR FORMAT "x(8)"
    FIELD bezeich       AS CHAR FORMAT "x(32)"
    FIELD reqno         AS CHAR FORMAT "x(8)"
    FIELD flag          AS CHAR 
    FIELD outsource     AS CHAR FORMAT "x(8)"
    FIELD vendor-nm     AS CHAR FORMAT "x(32)"
    FIELD startdate     AS CHAR FORMAT "x(10)"
    FIELD finishdate    AS CHAR FORMAT "x(10)"        
    FIELD price         AS CHAR FORMAT "x(19)"
    FIELD tot-dtl       AS CHAR FORMAT "x(19)"
.

DEFINE TEMP-TABLE tprop
    FIELD nr AS INTEGER
    FIELD nm AS CHAR
.

DEFINE INPUT PARAMETER room-nr  AS CHAR.
DEFINE INPUT PARAMETER fdate    AS DATE.
DEFINE INPUT PARAMETER tdate    AS DATE.
DEFINE INPUT PARAMETER prop-nr  AS INT.

DEFINE OUTPUT PARAMETER gtotal  AS CHAR FORMAT "x(19)".
DEFINE OUTPUT PARAMETER tot-cost AS CHAR FORMAT "x(19)".
DEFINE OUTPUT PARAMETER tot-vend AS CHAR FORMAT "x(19)".
DEFINE OUTPUT PARAMETER TABLE FOR t-hisroom-head.
DEFINE OUTPUT PARAMETER TABLE FOR t-hisroom-line.
DEFINE OUTPUT PARAMETER TABLE FOR t-hisroom-line-cost.
DEFINE OUTPUT PARAMETER TABLE FOR t-hisroom-line-vendor.
DEFINE OUTPUT PARAMETER TABLE FOR tprop.

DEFINE BUFFER tbuff FOR l-artikel.

DEFINE VARIABLE tot AS DECIMAL.
DEFINE VARIABLE curr-tot1 AS DECIMAL.
DEFINE VARIABLE curr-tot2 AS DECIMAL.
DEFINE VARIABLE curr-gtotal AS DECIMAL.
DEFINE VARIABLE int-str AS CHAR EXTENT 5 INITIAL
    ["New",  "Processed", "Done",  "Postponed", "Closed"].

RUN create-history.

/*****************************************************************************************/
PROCEDURE create-history:
    DEFINE VARIABLE char4       AS CHAR.
    DEFINE VARIABLE a           AS CHAR.
    DEFINE VARIABLE b           AS CHAR.
    DEFINE VARIABLE c           AS CHAR.
    DEFINE VARIABLE vendo-nm    AS CHAR.
    DEFINE VARIABLE itotal      AS DECIMAL.
    DEFINE VARIABLE nm-prop1    AS CHAR.
    DEFINE VARIABLE nm-prop2    AS CHAR.
    DEFINE VARIABLE nm-prop3    AS CHAR.
    DEFINE VARIABLE nm-prop4    AS CHAR.

    FOR EACH t-hisroom-head:
        DELETE t-hisroom-head.
    END.

    FOR EACH t-hisroom-line:
        DELETE t-hisroom-line.
    END.

    FOR EACH t-hisroom-line-cost:
        DELETE t-hisroom-line-cost.
    END.

    FOR EACH t-hisroom-line-vendor:
        DELETE t-hisroom-line-vendor.
    END.

    FOR EACH tprop:
        DELETE tprop.
    END.    
           
    FOR EACH eg-request WHERE  eg-request.zinr = room-nr AND eg-request.opened-date >= fdate AND eg-request.opened-date <= tdate OR 
        eg-request.propertynr = prop-nr AND eg-request.closed-date >= fdate AND eg-request.closed-date <= tdate OR 
        eg-request.propertynr = prop-nr AND eg-request.process-date >= fdate AND eg-request.process-date <= tdate 
        USE-INDEX prop_ix NO-LOCK:
        
        FIND FIRST tprop WHERE tprop.nr = eg-request.propertynr NO-LOCK NO-ERROR.
        IF NOT AVAILABLE tprop THEN
        DO:
            FIND FIRST eg-property WHERE eg-property.nr = eg-request.propertynr NO-LOCK NO-ERROR.
            IF AVAILABLE eg-property THEN nm-prop1 = eg-property.bezeich.
            ELSE nm-prop1 = "".

            CREATE tprop.
            ASSIGN tprop.nr = eg-request.propertynr
                   tprop.nm = nm-prop1.            

            CREATE t-hisroom-head.
            ASSIGN
                t-hisroom-head.itemno   = STRING(eg-request.propertynr, "->>>>>>9")
                t-hisroom-head.bezeich  = nm-prop1
                t-hisroom-head.flag     = "0"
            .            
        END.

        IF eg-request.opened-date = ? THEN  a = "".
        ELSE a = STRING(eg-request.opened-date ,"99/99/99").

        IF eg-request.closed-date = ? THEN  b = "".
        ELSE b = STRING(eg-request.closed-date ,"99/99/99").

        IF eg-request.done-date = ? THEN  c =   "".
        ELSE c = STRING(eg-request.done-date ,"99/99/99").

        FIND FIRST eg-subtask WHERE eg-subtask.sub-CODE = eg-request.sub-task NO-LOCK NO-ERROR.
        IF AVAILABLE eg-subtask THEN char4 = STRING(eg-subtask.bezeich).
        ELSE char4 = "".

        CREATE t-hisroom-line.
        ASSIGN                       
            t-hisroom-line.itemno   = STRING(eg-request.propertynr, "->>>>>>9")
            t-hisroom-line.bezeich  = nm-prop1
            t-hisroom-line.reqno    = STRING(eg-request.reqnr , "->>>>>>9")
            t-hisroom-line.opend    = a
            t-hisroom-line.processd = b
            t-hisroom-line.doned    = c
            t-hisroom-line.subtask  = char4
            t-hisroom-line.reqstat  = int-str[eg-request.reqstatus]
            t-hisroom-line.flag     = "1"
        .

        FIND FIRST eg-queasy WHERE eg-queasy.KEY = 1 AND eg-queasy.reqnr = eg-request.reqnr NO-LOCK NO-ERROR.
        IF AVAILABLE eg-queasy THEN
        DO:  
            curr-tot1 = 0.
            FOR EACH eg-queasy WHERE eg-queasy.KEY = 1 AND eg-queasy.reqnr = eg-request.reqnr NO-LOCK:    
                FIND FIRST tbuff WHERE tbuff.artnr = eg-queasy.stock-nr NO-LOCK NO-ERROR.
                IF AVAILABLE tbuff THEN
                DO:
                    itotal  = eg-queasy.deci1 * eg-queasy.price.                   
    
                    CREATE t-hisroom-line-cost.
                    ASSIGN 
                        t-hisroom-line-cost.itemno   = STRING(eg-request.propertynr, "->>>>>>9")       
                        t-hisroom-line-cost.bezeich  = nm-prop1                                 
                        t-hisroom-line-cost.reqno    = STRING(eg-request.reqnr , "->>>>>>9")
                        t-hisroom-line-cost.flag    = "1"
                        t-hisroom-line-cost.artno    = STRING(eg-queasy.stock-nr, "9999999")
                        t-hisroom-line-cost.bezeich2 = tbuff.bezeich
                        t-hisroom-line-cost.qty      = STRING(eg-queasy.deci1 ,"->>>>>>9")
                        t-hisroom-line-cost.price    = STRING(eg-queasy.price, "->>>,>>>,>>>,>>9.99")
                        t-hisroom-line-cost.tot-dtl  = STRING(itotal , "->>>,>>>,>>>,>>9.99")
                    .
                END. 
                tot = tot + itotal.
                curr-tot1 = curr-tot1 + itotal.
            END.
            IF curr-tot1 NE 0 THEN tot-cost = STRING(curr-tot1 , "->>>,>>>,>>>,>>9.99").
        END.

        FIND FIRST eg-vperform WHERE eg-vperform.reqnr = eg-request.reqnr NO-LOCK NO-ERROR.
        IF AVAILABLE eg-vperform THEN
        DO:            
            curr-tot2 = 0.
            FOR EACH eg-vperform WHERE eg-vperform.reqnr = eg-request.reqnr NO-LOCK:
                FIND FIRST eg-vendor WHERE eg-vendor.vendor-nr = eg-vperform.vendor-nr NO-LOCK NO-ERROR.
                IF AVAILABLE eg-vendor THEN
                DO:
                    vendo-nm = eg-vendor.bezeich.
                END.
                ELSE
                DO:
                    vendo-nm = "Undefine".
                END.
                
                IF eg-vperform.startdate = ? THEN a = "".
                ELSE a = STRING(eg-vperform.startdate , "99/99/99").
    
                IF eg-vperform.finishdate = ? THEN b = "".
                ELSE b = STRING(eg-vperform.finishdate , "99/99/99").                
    
                CREATE t-hisroom-line-vendor.
                ASSIGN                                  
                    t-hisroom-line-vendor.itemno        = STRING(eg-request.propertynr, "->>>>>>9")
                    t-hisroom-line-vendor.bezeich       = nm-prop1                                 
                    t-hisroom-line-vendor.reqno         = STRING(eg-request.reqnr , "->>>>>>9")    
                    t-hisroom-line-vendor.flag          = "0"                    
                    t-hisroom-line-vendor.outsource     = string(eg-vperform.perform-nr, "9999999")
                    t-hisroom-line-vendor.vendor-nm     = vendo-nm
                    t-hisroom-line-vendor.startdate     = a
                    t-hisroom-line-vendor.finishdate    = b   
                    t-hisroom-line-vendor.price         = STRING(eg-vperform.price , "->>>,>>>,>>>,>>9.99")
                    t-hisroom-line-vendor.tot-dtl       = t-hisroom-line-vendor.tot-dtl + STRING(eg-vperform.price , "->>>,>>>,>>>,>>9.99")
                .       

                tot = tot + eg-vperform.price. 
                curr-tot2 = curr-tot2 + eg-vperform.price.
            END.
            IF curr-tot2 NE 0 THEN tot-vend = STRING(curr-tot2, "->>>,>>>,>>>,>>9.99").           
        END.

        IF tot NE 0 THEN
        DO:            
            curr-gtotal = curr-gtotal + tot. 
            tot = 0.
        END.
    END. 

    IF curr-gtotal NE 0 THEN gtotal = STRING(curr-gtotal, "->>>,>>>,>>>,>>9.99").
END PROCEDURE.

