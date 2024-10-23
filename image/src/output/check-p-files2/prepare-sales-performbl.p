
DEF INPUT  PARAMETER user-init AS CHAR.
DEF OUTPUT PARAMETER price-decimal AS INT.
DEF OUTPUT PARAMETER from-date AS CHAR.
DEF OUTPUT PARAMETER to-date AS CHAR.
DEF OUTPUT PARAMETER usr-init AS CHAR.

FIND FIRST htparam WHERE htparam.paramnr = 491. 
price-decimal = htparam.finteger. 
 
FIND FIRST htparam WHERE paramnr = 110 no-lock.  /*Invoicing DATE */ 
from-date = STRING(month(fdate),"99") + STRING(year(fdate),"9999"). 
to-date = from-date. 

usr-init = user-init. 
FIND FIRST bediener WHERE bediener.userinit = user-init. 
