DEFINE TEMP-TABLE payload-list
    FIELD v-mode        AS INTEGER
    FIELD art-number    AS INTEGER
    FIELD dept-number   AS INTEGER
    FIELD art-quantity  AS INTEGER
    .

DEFINE TEMP-TABLE response-list
    FIELD result-msg AS CHARACTER
    .

DEFINE INPUT PARAMETER TABLE FOR payload-list.
DEFINE OUTPUT PARAMETER TABLE FOR response-list.

DEFINE VARIABLE bill-date AS DATE NO-UNDO.
DEFINE VARIABLE max-soldout-qty AS INTEGER NO-UNDO.
DEFINE VARIABLE current-qty AS INTEGER NO-UNDO.
DEFINE VARIABLE remain-qty AS INTEGER NO-UNDO.
DEFINE VARIABLE posted-qty AS INTEGER NO-UNDO.
DEFINE VARIABLE soldout-flag AS LOGICAL NO-UNDO.
DEFINE VARIABLE art-desc AS CHARACTER. 

FIND FIRST htparam WHERE htparam.paramnr EQ 110 NO-LOCK NO-ERROR.
IF AVAILABLE htparam THEN bill-date = htparam.fdate.

CREATE response-list.

FIND FIRST payload-list.
IF NOT AVAILABLE payload-list THEN
DO:
    response-list.result-msg = "No data available.".
    RETURN.
END.

IF payload-list.v-mode EQ 1 THEN /*Check Soldout Menu*/
DO:
    FOR EACH payload-list:
        current-qty = 0.
        posted-qty = 0.

        FIND FIRST h-artikel WHERE h-artikel.artnr EQ payload-list.art-number
            AND h-artikel.departement EQ payload-list.dept-number NO-LOCK NO-ERROR.
        IF AVAILABLE h-artikel THEN
        DO:
            FIND FIRST queasy WHERE queasy.KEY EQ 222 
                 AND queasy.number1 EQ 2 
                 AND queasy.number2 EQ h-artikel.artnr
                 AND queasy.number3 EQ h-artikel.departement NO-LOCK NO-ERROR.
            IF AVAILABLE queasy THEN
            DO:
                ASSIGN
                    max-soldout-qty = INT(queasy.deci1)
                    soldout-flag = queasy.logi2
                    .
                art-desc = h-artikel.bezeich.
            END.    
        END.
        
        IF max-soldout-qty NE 0 THEN
        DO:
            FOR EACH h-journal WHERE h-journal.artnr EQ payload-list.art-number
                AND h-journal.departement EQ payload-list.dept-number
                AND h-journal.bill-datum EQ bill-date NO-LOCK:
                current-qty = current-qty + h-journal.anzahl.
                posted-qty = posted-qty + h-journal.anzahl.
            END.

            /*Debug
            MESSAGE 
                max-soldout-qty SKIP current-qty SKIP posted-qty SKIP payload-list.art-quantity
                VIEW-AS ALERT-BOX INFO BUTTONS OK.*/
            current-qty = current-qty + payload-list.art-quantity.        
            remain-qty = max-soldout-qty - posted-qty.

            /*MESSAGE current-qty SKIP remain-qty
                VIEW-AS ALERT-BOX INFO BUTTONS OK.*/
            IF current-qty GT max-soldout-qty THEN
            DO:
                response-list.result-msg = "Input qty greater than max soldout qty. Allowed qty = " + STRING(remain-qty) + "."
                                        + CHR(10) +
                                        STRING(payload-list.art-number) + " - " + art-desc + "."
                                        + CHR(10) + 
                                        "Confirm not possible.".
                RETURN.
            END.        
        END.    
    
        IF soldout-flag THEN
        DO:
            response-list.result-msg = "Soldout menu flag already update to be YES with another user. Article:"
                                    + CHR(10) +
                                    STRING(payload-list.art-number) + " - " + art-desc
                                    + CHR(10) + 
                                    "Please check it and refresh this page.".
            RETURN.
        END.           
    END.

    response-list.result-msg = "Success".
END.
ELSE IF payload-list.v-mode EQ 2 THEN   /*Check for refresh artikel after posting*/
DO:
    FOR EACH payload-list:
        current-qty = 0.
        FIND FIRST h-artikel WHERE h-artikel.artnr EQ payload-list.art-number
            AND h-artikel.departement EQ payload-list.dept-number NO-LOCK NO-ERROR.
        IF AVAILABLE h-artikel THEN
        DO:
            FIND FIRST queasy WHERE queasy.KEY EQ 222 
                 AND queasy.number1 EQ 2 
                 AND queasy.number2 EQ h-artikel.artnr
                 AND queasy.number3 EQ h-artikel.departement NO-LOCK NO-ERROR.
            IF AVAILABLE queasy THEN
            DO:
                ASSIGN
                    max-soldout-qty = INT(queasy.deci1)
                    soldout-flag = queasy.logi2
                    .
            END.    
    
            IF max-soldout-qty NE 0 THEN
            DO:
                FOR EACH h-journal WHERE h-journal.artnr EQ payload-list.art-number
                    AND h-journal.departement EQ payload-list.dept-number
                    AND h-journal.bill-datum EQ bill-date NO-LOCK:
                    current-qty = current-qty + h-journal.anzahl.
                END.
                IF current-qty GE max-soldout-qty THEN
                DO:
                    response-list.result-msg = "Transaction has article soldout. Please refresh article list.".
                    RETURN.
                END.
            END.
        END.
    END.

    response-list.result-msg = "Success".
END.
