
DEF TEMP-TABLE t-l-hauptgrp
    FIELD endkum  LIKE l-hauptgrp.endkum
    FIELD bezeich LIKE l-hauptgrp.bezeich.
DEF TEMP-TABLE t-l-lager LIKE l-lager.

DEF OUTPUT PARAMETER food AS INT.
DEF OUTPUT PARAMETER bev AS INT.
DEF OUTPUT PARAMETER date2 AS DATE.
DEF OUTPUT PARAMETER date1 AS DATE.
DEF OUTPUT PARAMETER bill-date AS DATE.
DEF OUTPUT PARAMETER double-currency AS LOGICAL.
DEF OUTPUT PARAMETER foreign-nr AS INT INITIAL 0.
DEF OUTPUT PARAMETER exchg-rate AS DECIMAL INITIAL 1.
DEF OUTPUT PARAMETER TABLE FOR t-l-lager.
DEF OUTPUT PARAMETER TABLE FOR t-l-hauptgrp.

FIND FIRST htparam WHERE paramnr = 257 NO-LOCK. 
food = htparam.finteger.               /* Rulita 211024 | Fixing for serverless */  
FIND FIRST htparam WHERE paramnr = 258 NO-LOCK. 
bev = htparam.finteger.               /* Rulita 211024 | Fixing for serverless */  
 
FIND FIRST htparam WHERE paramnr = 474 NO-LOCK. 
date2 = htparam.fdate.        /* Rulita 211024 | Fixing for serverless */
date1 = DATE(month(date2), 1, year(date2)). 
FIND FIRST htparam WHERE paramnr = 110 NO-LOCK. 
bill-date = htparam.fdate.    /* Rulita 211024 | Fixing for serverless */
 
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

FOR EACH l-lager NO-LOCK:
    CREATE t-l-lager.
    BUFFER-COPY l-lager TO t-l-lager.
END.

FOR EACH l-hauptgrp:
    CREATE t-l-hauptgrp.
    BUFFER-COPY l-hauptgrp TO t-l-hauptgrp.
END.
