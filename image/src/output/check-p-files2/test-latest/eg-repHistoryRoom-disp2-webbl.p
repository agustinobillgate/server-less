/*FD Dec 25, 2021 => BL for vhpweb Based convert STR to Temp-Table*/

DEFINE TEMP-TABLE t-hisroom
    FIELD itemno    AS CHAR FORMAT "x(8)"
    FIELD bezeich   AS CHAR FORMAT "x(48)"
    FIELD reqno     AS CHAR FORMAT "x(8)"
    FIELD opend     AS CHAR FORMAT "x(10)"
    FIELD processd  AS CHAR FORMAT "x(10)"
    FIELD doned     AS CHAR FORMAT "x(10)"
    FIELD subtask   AS CHAR FORMAT "x(48)"
    FIELD reqstat   AS CHAR FORMAT "x(20)"
    FIELD flag      AS CHAR
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
DEFINE OUTPUT PARAMETER TABLE FOR t-hisroom.
DEFINE OUTPUT PARAMETER TABLE FOR tprop.

DEFINE BUFFER tbuff FOR l-artikel.

DEFINE VARIABLE tot AS DECIMAL.
DEFINE VARIABLE curr-gtotal AS DECIMAL.
DEFINE VARIABLE int-str AS CHAR EXTENT 5 INITIAL
    ["New","Processed","Done","Postponed","Closed"].

RUN create-history.

/*****************************************************************************************/
PROCEDURE create-history:
    DEFINE VARIABLE char4       AS CHAR.
    DEFINE VARIABLE a           AS CHAR.
    DEFINE VARIABLE b           AS CHAR.
    DEFINE VARIABLE c           AS CHAR.   
    DEFINE VARIABLE itotal      AS DECIMAL.
    DEFINE VARIABLE nm-prop1    AS CHAR.    

    FOR EACH t-hisroom:
        DELETE t-hisroom.
    END.     

    FOR EACH tprop:
        DELETE tprop.
    END.    
           
    FOR EACH eg-request WHERE eg-request.zinr EQ room-nr AND eg-request.opened-date >= fdate AND eg-request.opened-date <= tdate OR 
        eg-request.propertynr EQ prop-nr AND eg-request.closed-date >= fdate AND eg-request.closed-date <= tdate OR 
        eg-request.propertynr EQ prop-nr AND eg-request.process-date >= fdate AND eg-request.process-date <= tdate 
        USE-INDEX prop_ix NO-LOCK:
        
        FIND FIRST tprop WHERE tprop.nr EQ eg-request.propertynr NO-LOCK NO-ERROR.
        IF NOT AVAILABLE tprop THEN
        DO:
            FIND FIRST eg-property WHERE eg-property.nr EQ eg-request.propertynr NO-LOCK NO-ERROR.
            IF AVAILABLE eg-property THEN nm-prop1 = eg-property.bezeich.
            ELSE nm-prop1 = "".

            CREATE tprop.
            ASSIGN tprop.nr = eg-request.propertynr
                   tprop.nm = nm-prop1.            

            CREATE t-hisroom.
            ASSIGN
                t-hisroom.itemno   = STRING(eg-request.propertynr, "->>>>>>9")
                t-hisroom.bezeich  = nm-prop1
                t-hisroom.flag     = "0"
            .            
        END.

        IF eg-request.opened-date = ? THEN a = "-".
        ELSE a = STRING(eg-request.opened-date ,"99/99/99").

        IF eg-request.closed-date = ? THEN b = "-".
        ELSE b = STRING(eg-request.closed-date ,"99/99/99").

        IF eg-request.done-date = ? THEN c = "-".
        ELSE c = STRING(eg-request.done-date ,"99/99/99").

        FIND FIRST eg-subtask WHERE eg-subtask.sub-CODE EQ eg-request.sub-task NO-LOCK NO-ERROR.
        IF AVAILABLE eg-subtask THEN char4 = STRING(eg-subtask.bezeich).
        ELSE char4 = "".
        
        CREATE t-hisroom.
        ASSIGN             
            t-hisroom.itemno   = STRING(eg-request.propertynr, "->>>>>>9")
            t-hisroom.bezeich  = nm-prop1
            t-hisroom.reqno    = STRING(eg-request.reqnr , "->>>>>>9")
            t-hisroom.opend    = a
            t-hisroom.processd = b
            t-hisroom.doned    = c
            t-hisroom.subtask  = char4
            t-hisroom.reqstat  = int-str[eg-request.reqstatus]     
            t-hisroom.flag     = "1"
        .

        FIND FIRST eg-queasy WHERE eg-queasy.KEY EQ 1 AND eg-queasy.reqnr EQ eg-request.reqnr NO-LOCK NO-ERROR.
        IF AVAILABLE eg-queasy THEN
        DO:              
            FOR EACH eg-queasy WHERE eg-queasy.KEY EQ 1 AND eg-queasy.reqnr EQ eg-request.reqnr NO-LOCK:    
                FIND FIRST tbuff WHERE tbuff.artnr = eg-queasy.stock-nr NO-LOCK NO-ERROR.
                IF AVAILABLE tbuff THEN
                DO:
                    itotal  = eg-queasy.deci1 * eg-queasy.price.                                       
                END. 
                tot = tot + itotal.
            END.            
        END.

        FIND FIRST eg-vperform WHERE eg-vperform.reqnr EQ eg-request.reqnr NO-LOCK NO-ERROR.
        IF AVAILABLE eg-vperform THEN
        DO:                        
            FOR EACH eg-vperform WHERE eg-vperform.reqnr EQ eg-request.reqnr NO-LOCK:                
                tot = tot + eg-vperform.price.                 
            END.                      
        END.

        IF tot NE 0 THEN
        DO:            
            curr-gtotal = curr-gtotal + tot. 
            tot = 0.
        END.
    END. 

    IF curr-gtotal NE 0 THEN gtotal = STRING(curr-gtotal, "->>>,>>>,>>>,>>9.99").
END PROCEDURE.

