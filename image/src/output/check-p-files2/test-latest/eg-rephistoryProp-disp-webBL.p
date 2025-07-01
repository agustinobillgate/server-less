/*FD August 24, 2021 => BL for vhpweb Based convert STR to Temp-Table*/
DEFINE TEMP-TABLE tbrowse
    FIELD reqno AS CHAR FORMAT "x(10)"
    FIELD opend AS CHAR FORMAT "x(10)"
    FIELD processd AS CHAR FORMAT "x(10)"
    FIELD doned AS CHAR FORMAT "x(10)"
    FIELD subtask AS CHAR FORMAT "x(48)"
    FIELD reqstat AS CHAR FORMAT "x(15)"    
    FIELD tFlag AS CHAR 
.

DEFINE INPUT PARAMETER prop-nr AS INT.
DEFINE INPUT PARAMETER fdate AS DATE.
DEFINE INPUT PARAMETER tdate AS DATE.
DEFINE OUTPUT PARAMETER grand-total AS CHAR FORMAT "x(19)".
DEFINE OUTPUT PARAMETER TABLE FOR tbrowse.
/* Testing
DEFINE VARIABLE prop-nr AS INT.
DEFINE VARIABLE fdate   AS DATE.
DEFINE VARIABLE tdate   AS DATE.
DEFINE VARIABLE grand-total AS CHAR FORMAT "x(19)".

prop-nr = 14132.
fdate   = 08/01/21.
tdate   = 08/24/21.
*/
DEFINE VARIABLE atotal  AS INTEGER.
DEFINE VARIABLE btotal  AS DECIMAL.
DEFINE VARIABLE tot     AS DECIMAL.
DEFINE VARIABLE int-str AS CHAR EXTENT 5 INITIAL
    ["New", "Processed", "Done", "Postponed", "Closed"].

DEFINE BUFFER tbuff FOR l-artikel.

RUN create-history.

PROCEDURE create-history:
    DEFINE VARIABLE char1   AS CHAR.
    DEFINE VARIABLE str-op  AS CHAR.
    DEFINE VARIABLE str-cd  AS CHAR.
    DEFINE VARIABLE str-dd  AS CHAR.
    DEFINE VARIABLE itotal  AS DECIMAL.  

    FOR EACH tbrowse:
        DELETE tbrowse.
    END.

    atotal = 0.
    btotal = 0.       

    FOR EACH eg-request WHERE (eg-request.propertynr EQ prop-nr AND eg-request.opened-date >= fdate AND eg-request.opened-date <= tdate) OR 
        (eg-request.propertynr EQ prop-nr AND eg-request.closed-date >= fdate AND eg-request.closed-date <= tdate) OR 
        (eg-request.propertynr EQ prop-nr AND eg-request.process-date >= fdate AND eg-request.process-date <= tdate) NO-LOCK:
        
        IF eg-request.opened-date = ? THEN str-op = "-".
        ELSE str-op = STRING(eg-request.opened-date ,"99/99/99").

        IF eg-request.closed-date = ? THEN str-cd = "-".
        ELSE str-cd = STRING(eg-request.closed-date ,"99/99/99").

        IF eg-request.done-date = ? THEN str-dd = "-".
        ELSE str-dd = STRING(eg-request.done-date ,"99/99/99").

        FIND FIRST eg-subtask WHERE eg-subtask.sub-CODE EQ eg-request.sub-task NO-LOCK NO-ERROR.
        IF AVAILABLE eg-subtask THEN char1 = eg-subtask.bezeich.
        ELSE char1 = "".        

        CREATE tbrowse.
        ASSIGN             
            tbrowse.tflag       = "1"
            tbrowse.reqno       = STRING(eg-request.reqnr , "->>>>>>>>9")
            tbrowse.opend       = str-op
            tbrowse.processd    = str-cd
            tbrowse.doned       = str-dd
            tbrowse.subtask     = char1
            tbrowse.reqstat     = STRING(int-str[eg-request.reqstatus]).

        FIND FIRST eg-queasy WHERE eg-queasy.KEY EQ 1 AND eg-queasy.reqnr EQ eg-request.reqnr NO-LOCK NO-ERROR.
        IF AVAILABLE eg-queasy THEN
        DO:
            FOR EACH eg-queasy WHERE eg-queasy.KEY EQ 1 AND eg-queasy.reqnr EQ eg-request.reqnr NO-LOCK:    
                FIND FIRST tbuff WHERE tbuff.artnr EQ eg-queasy.stock-nr NO-LOCK NO-ERROR.
                IF AVAILABLE tbuff THEN itotal = eg-queasy.deci1 * eg-queasy.price.

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
            btotal = btotal + tot. 
            tot = 0.
        END.
    END.

    IF btotal NE 0 THEN grand-total = STRING(btotal, "->>>,>>>,>>>,>>9.99").
END PROCEDURE.
