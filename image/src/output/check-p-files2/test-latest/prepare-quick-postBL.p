
DEF TEMP-TABLE t-hoteldpt
    FIELD num LIKE hoteldpt.num.


DEF OUTPUT PARAMETER foreign-rate       AS LOGICAL.
DEF OUTPUT PARAMETER double-currency    AS LOGICAL.
DEF OUTPUT PARAMETER price-decimal      AS INTEGER.
DEF OUTPUT PARAMETER exchg-rate         AS DECIMAL.
DEF OUTPUT PARAMETER curr-local         AS CHAR.
DEF OUTPUT PARAMETER curr-foreign       AS CHAR.
DEF OUTPUT PARAMETER TABLE FOR t-hoteldpt.

FIND FIRST htparam WHERE htparam.paramnr = 143 NO-LOCK. 
foreign-rate = htparam.flogical.
FIND FIRST htparam WHERE paramnr = 240 NO-LOCK. 
double-currency = htparam.flogical.
FIND FIRST htparam WHERE htparam.paramnr = 491 NO-LOCK. 
price-decimal = htparam.finteger.

FIND FIRST htparam WHERE htparam.paramnr = 144 NO-LOCK. 
FIND FIRST waehrung WHERE waehrung.wabkurz = htparam.fchar NO-LOCK NO-ERROR. 
IF AVAILABLE waehrung THEN exchg-rate = waehrung.ankauf / waehrung.einheit.

FIND FIRST htparam WHERE paramnr = 152 NO-LOCK. 
curr-local = fchar. 
FIND FIRST htparam WHERE paramnr = 144 NO-LOCK. 
curr-foreign = fchar. 

FOR EACH hoteldpt:
    CREATE t-hoteldpt.
    ASSIGN t-hoteldpt.num = hoteldpt.num.
END.
