
DEF INPUT PARAMETER price-list-artnr AS INT.

FIND FIRST queasy WHERE KEY = 142 AND queasy.number1 = price-list-artnr NO-LOCK NO-ERROR.
IF AVAILABLE queasy THEN 
DO:
    FIND CURRENT queasy EXCLUSIVE-LOCK.
    ASSIGN
        queasy.number1 = 0
        queasy.number2 = 0
        queasy.deci1 = 0
        queasy.deci2 = 0
        queasy.date1 = ?
        queasy.date2 = ?
        queasy.char2 = "".
    FIND CURRENT queasy NO-LOCK.
    RELEASE queasy.
END.

/* DEF INPUT PARAMETER price-list-artnr AS INT.

FIND FIRST queasy WHERE KEY = 142 
    AND queasy.number1 = price-list-artnr NO-ERROR.
ASSIGN
    queasy.number1 = 0
    queasy.number2 = 0
    queasy.deci1 = 0
    queasy.deci2 = 0
    queasy.date1 = ?
    queasy.date2 = ?
    queasy.char2 = "".
*/
