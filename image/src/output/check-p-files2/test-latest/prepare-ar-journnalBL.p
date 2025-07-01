
DEFINE VARIABLE min-dept AS INTEGER INITIAL 99. 
DEFINE VARIABLE max-dept AS INTEGER INITIAL 0. 
DEFINE VARIABLE min-art  AS INTEGER INITIAL 9999. 
DEFINE VARIABLE max-art  AS INTEGER INITIAL 0. 

DEF OUTPUT PARAMETER from-date AS DATE.
DEF OUTPUT PARAMETER to-date AS DATE.
DEF OUTPUT PARAMETER from-art AS INT.
DEF OUTPUT PARAMETER to-art AS INT.
DEF OUTPUT PARAMETER from-dept AS INT.
DEF OUTPUT PARAMETER to-dept AS INT.
DEF OUTPUT PARAMETER depname1 AS CHAR.
DEF OUTPUT PARAMETER depname2 AS CHAR.

FIND FIRST htparam WHERE paramnr = 110 no-lock.  /*Invoicing DATE */ 
from-date = htparam.fdate. 
to-date = htparam.fdate. 
 
FOR EACH artikel WHERE artikel.activeflag = YES 
  AND (artart = 2 OR artart = 7) NO-LOCK: 
  IF min-art GT artikel.artnr THEN min-art = artikel.artnr. 
  IF max-art LT artikel.artnr THEN max-art = artikel.artnr. 
END. 
 
FOR EACH hoteldpt NO-LOCK: 
  IF min-dept GT hoteldpt.num THEN min-dept = hoteldpt.num. 
  IF max-dept LT hoteldpt.num THEN max-dept = hoteldpt.num. 
END. 
 
from-art = min-art. 
to-art = max-art. 
from-dept = min-dept. 
to-dept = min-dept. 
 
FIND FIRST hoteldpt WHERE hoteldpt.num = from-dept NO-LOCK. 
depname1 = hoteldpt.depart. 
FIND FIRST hoteldpt WHERE hoteldpt.num = to-dept NO-LOCK. 
depname2 = hoteldpt.depart. 
