
DEFINE TEMP-TABLE t-currency
    FIELD currNr    AS INT
    FIELD currID    AS CHAR
    FIELD exrate    AS DEC .

DEF OUTPUT PARAMETER TABLE FOR t-currency.

FIND FIRST htparam WHERE htparam.paramnr = 152 NO-LOCK. 
FIND FIRST waehrung WHERE waehrung.wabkurz = htparam.fchar NO-LOCK NO-ERROR. 
IF AVAILABLE waehrung THEN 
DO: 
    CREATE t-currency.
    ASSIGN t-currency.currNr = waehrung.waehrungsnr
           t-currency.currID = waehrung.wabkurz
           t-currency.exrate = waehrung.ankauf / waehrung.einheit.
END.

FOR EACH waehrung WHERE waehrung.wabkurz NE htparam.fchar 
    AND waehrung.ankauf GT 0 NO-LOCK BY waehrung.wabkurz: 
    CREATE t-currency.
    ASSIGN t-currency.currNr = waehrung.waehrungsnr
           t-currency.currID = waehrung.wabkurz
           t-currency.exrate = waehrung.ankauf / waehrung.einheit.
END.
