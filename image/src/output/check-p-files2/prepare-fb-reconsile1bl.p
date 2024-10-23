
DEF TEMP-TABLE t-l-hauptgrp
    FIELD endkum  LIKE l-hauptgrp.endkum
    FIELD bezeich LIKE l-hauptgrp.bezeich.

DEF OUTPUT PARAMETER food       AS INT.
DEF OUTPUT PARAMETER bev        AS INT.
DEF OUTPUT PARAMETER ldry       AS INT.
DEF OUTPUT PARAMETER dstore     AS INT.
DEF OUTPUT PARAMETER to-date    AS DATE.
DEF OUTPUT PARAMETER from-date  AS DATE.
DEF OUTPUT PARAMETER bill-date  AS DATE.
DEF OUTPUT PARAMETER foreign-nr AS INT INIT 0.
DEF OUTPUT PARAMETER double-currency AS LOGICAL INIT NO.
DEF OUTPUT PARAMETER exchg-rate      AS DECIMAL INITIAL 1.
DEF OUTPUT PARAMETER TABLE FOR t-l-hauptgrp.

FIND FIRST htparam WHERE paramnr = 257 NO-LOCK. 
food = htparam.finteger.               /* Rulita 211024 | Fixing for serverless */  
FIND FIRST htparam WHERE paramnr = 258 NO-LOCK. 
bev = htparam.finteger.               /* Rulita 211024 | Fixing for serverless */  
 
FIND FIRST htparam WHERE paramnr = 1081 NO-LOCK. 
ldry = htparam.finteger.               /* Rulita 211024 | Fixing for serverless */  
FIND FIRST htparam WHERE paramnr = 1082 NO-LOCK. 
dstore = htparam.finteger.               /* Rulita 211024 | Fixing for serverless */  
 
FIND FIRST htparam WHERE paramnr = 474 NO-LOCK. 
to-date = htparam.fdate.          /* Rulita 211024 | Fixing for serverless */
from-date = DATE(month(to-date), 1, year(to-date)). 
FIND FIRST htparam WHERE paramnr = 110 NO-LOCK. 
bill-date = htparam.fdate.        /* Rulita 211024 | Fixing for serverless */

FIND FIRST htparam WHERE paramnr = 240 no-lock.  /* double currency flag */ 
IF htparam.flogical THEN 
DO: 
  double-currency = YES. 
  FIND FIRST htparam WHERE htparam.paramnr = 144 NO-LOCK. 
  FIND FIRST waehrung WHERE waehrung.wabkurz = htparam.fchar NO-LOCK NO-ERROR. 
  IF AVAILABLE waehrung THEN 
  DO: 
    foreign-nr = waehrung.waehrungsnr. 
    exchg-rate = waehrung.ankauf / waehrung.einheit. 
  END. 
  ELSE exchg-rate = 1. 
END. 

FOR EACH l-hauptgrp:
    CREATE t-l-hauptgrp.
    ASSIGN
      t-l-hauptgrp.endkum  = l-hauptgrp.endkum
      t-l-hauptgrp.bezeich = l-hauptgrp.bezeich.
END.
