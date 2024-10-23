DEF OUTPUT PARAMETER price-decimal AS INT.
DEF OUTPUT PARAMETER foreign-nr AS INT.
DEF OUTPUT PARAMETER f-log AS LOGICAL.

FIND FIRST htparam WHERE htparam.paramnr = 491. 
price-decimal = htparam.finteger.   /* non-digit OR digit version */ 
 
FIND FIRST htparam WHERE htparam.paramnr = 144 NO-LOCK. 
IF htparam.fchar NE "" THEN 
DO: 
  FIND FIRST waehrung WHERE waehrung.wabkurz = htparam.fchar NO-LOCK NO-ERROR. 
  IF AVAILABLE waehrung THEN foreign-nr = waehrung.waehrungsnr. 
END. 

FIND FIRST htparam WHERE paramnr = 143 NO-LOCK.
f-log = htparam.flogical.
