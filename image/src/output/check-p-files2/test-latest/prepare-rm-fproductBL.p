

DEF OUTPUT PARAMETER bfast-art          AS INT.
DEF OUTPUT PARAMETER lunch-art          AS INT.
DEF OUTPUT PARAMETER dinner-art         AS INT.
DEF OUTPUT PARAMETER lundin-art         AS INT.
DEF OUTPUT PARAMETER local-curr         AS INT.
DEF OUTPUT PARAMETER new-contrate       AS LOGICAL.
DEF OUTPUT PARAMETER curr-date          AS DATE.
DEF OUTPUT PARAMETER double-currency    AS LOGICAL.
DEF OUTPUT PARAMETER exchg-rate         AS DECIMAL.
DEF OUTPUT PARAMETER price-decimal      AS INT.

DEFINE buffer wrung FOR waehrung. 

FIND FIRST htparam WHERE htparam.paramnr = 87 NO-LOCK.
curr-date = htparam.fdate.

FIND FIRST htparam WHERE paramnr = 125 NO-LOCK. 
bfast-art = htparam.finteger.               /* Rulita 211024 | Fixing for serverless */  
FIND FIRST htparam WHERE paramnr = 227 NO-LOCK. 
lunch-art = htparam.finteger.               /* Rulita 211024 | Fixing for serverless */  
FIND FIRST htparam WHERE paramnr = 228 NO-LOCK. 
dinner-art = htparam.finteger.               /* Rulita 211024 | Fixing for serverless */  
FIND FIRST htparam WHERE paramnr = 229 NO-LOCK. 
lundin-art = htparam.finteger.               /* Rulita 211024 | Fixing for serverless */  
FIND FIRST htparam WHERE paramnr = 152 NO-LOCK.
FIND FIRST wrung WHERE wrung.wabkurz = htparam.fchar.
local-curr = wrung.waehrungsnr.
FIND FIRST htparam WHERE htparam.paramnr = 550 NO-LOCK.
IF htparam.feldtyp = 4 THEN new-contrate = htparam.flogical.


FIND FIRST htparam WHERE paramnr = 240 NO-LOCK. 
double-currency = htparam.flogical. 
 
FIND FIRST htparam WHERE htparam.paramnr = 144 NO-LOCK. 
FIND FIRST waehrung WHERE waehrung.wabkurz = htparam.fchar NO-LOCK NO-ERROR. 
IF AVAILABLE waehrung THEN exchg-rate = waehrung.ankauf / 
waehrung.einheit. 
ELSE exchg-rate = 1. 
 
FIND FIRST htparam WHERE htparam.paramnr = 491. 
price-decimal = htparam.finteger. 

