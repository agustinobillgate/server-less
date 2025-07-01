
DEF TEMP-TABLE t-kellner
    FIELD kellnername LIKE kellner.kellnername
    FIELD kellner-nr LIKE kellner.kellner-nr
    FIELD departement LIKE kellner.departement
    FIELD rec-id AS INT.
DEF TEMP-TABLE t-hoteldpt
    FIELD num LIKE hoteldpt.num
    FIELD depart LIKE hoteldpt.depart.

DEF OUTPUT PARAMETER exchg-rate     AS DECIMAL.
DEF OUTPUT PARAMETER curr-local     AS CHAR.
DEF OUTPUT PARAMETER curr-foreign   AS CHAR.
DEF OUTPUT PARAMETER from-date      AS DATE.
DEF OUTPUT PARAMETER h-art-coupon   AS INT.
DEF OUTPUT PARAMETER TABLE FOR t-hoteldpt.
DEF OUTPUT PARAMETER TABLE FOR t-kellner.

FIND FIRST htparam WHERE htparam.paramnr = 144 NO-LOCK. 
FIND FIRST waehrung WHERE waehrung.wabkurz = htparam.fchar NO-LOCK NO-ERROR. 
IF AVAILABLE waehrung THEN exchg-rate = waehrung.ankauf / waehrung.einheit. 
ELSE exchg-rate = 1. 
 
FIND FIRST htparam WHERE paramnr = 152 NO-LOCK. 
curr-local = fchar. 
FIND FIRST htparam WHERE paramnr = 144 NO-LOCK. 
curr-foreign = fchar. 
FIND FIRST htparam WHERE paramnr = 110 NO-LOCK.  /*Invoicing Date */ 
from-date = htparam.fdate. 
FIND FIRST htparam WHERE paramnr = 1001 NO-LOCK.
h-art-coupon = htparam.finteger. /* Malik Serverless 581 htparam.fINTEGER -> htparam.finteger */

FOR EACH hoteldpt WHERE hoteldpt.num GT 0:
    CREATE t-hoteldpt.
    ASSIGN
        t-hoteldpt.num = hoteldpt.num
        t-hoteldpt.depart = hoteldpt.depart.
END.

FOR EACH kellner:
    CREATE t-kellner.
    ASSIGN
        t-kellner.kellnername = kellner.kellnername
        t-kellner.kellner-nr = kellner.kellner-nr
        t-kellner.departement = kellner.departement
        t-kellner.rec-id = RECID(kellner).
END.
