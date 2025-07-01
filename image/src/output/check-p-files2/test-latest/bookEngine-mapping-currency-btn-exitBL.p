
DEF TEMP-TABLE t-mapping-currency
    FIELD currencyVHP   AS CHAR
    FIELD currencyBE    AS CHAR
    FIELD descr         AS CHAR
    FIELD nr            AS INT
    .

DEF INPUT  PARAMETER TABLE FOR t-mapping-currency.
DEF INPUT  PARAMETER bookengID AS INT.

FOR EACH t-mapping-currency NO-LOCK:
    FIND FIRST queasy WHERE queasy.KEY = 164 
        AND queasy.number1 = bookengID
        AND queasy.number2 = t-mapping-currency.nr
        NO-ERROR.
    IF AVAILABLE queasy THEN queasy.char2 = t-mapping-currency.currencyBE.
    ELSE
    DO:
        CREATE queasy.
        ASSIGN
            queasy.KEY = 164
            queasy.number1 = bookengID
            queasy.number2 = t-mapping-currency.nr
            queasy.char1   = t-mapping-currency.currencyVHP.
    END.
END.
