
DEF TEMP-TABLE t-mapping-currency
    FIELD currencyVHP   AS CHAR
    FIELD currencyBE    AS CHAR
    FIELD descr         AS CHAR
    FIELD nr            AS INT
    .

DEF OUTPUT PARAMETER TABLE FOR t-mapping-currency.
DEF INPUT  PARAMETER bookengID AS INT.

FOR EACH waehrung:
    CREATE t-mapping-currency.
    ASSIGN
        t-mapping-currency.currencyVHP  = waehrung.wabkurz
        t-mapping-currency.descr        = waehrung.bezeich
        t-mapping-currency.nr           = waehrung.waehrungsnr.
    
    FIND FIRST queasy WHERE queasy.KEY = 164 
        AND queasy.number1 = bookengID
        AND queasy.number2 = waehrung.waehrungsnr
        NO-LOCK NO-ERROR.
    IF AVAILABLE queasy THEN t-mapping-currency.currencyBE = queasy.char2.
    ELSE
    DO:
        CREATE queasy.
        ASSIGN
            queasy.KEY = 164
            queasy.number1 = bookengID
            queasy.number2 = waehrung.waehrungsnr
            queasy.char1   = waehrung.wabkurz.
    END.
END.

