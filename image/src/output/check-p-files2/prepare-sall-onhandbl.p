
DEF TEMP-TABLE t-l-lager LIKE l-lager.
DEF TEMP-TABLE t-l-hauptgrp
    FIELD endkum  LIKE l-hauptgrp.endkum
    FIELD bezeich LIKE l-hauptgrp.bezeich.

DEF OUTPUT PARAMETER show-price AS LOGICAL.
DEF OUTPUT PARAMETER avail-l-untergrup AS LOGICAL INIT NO.
DEF OUTPUT PARAMETER p-224 AS DATE.
DEF OUTPUT PARAMETER TABLE FOR t-l-lager.
DEF OUTPUT PARAMETER TABLE FOR t-l-hauptgrp.

FIND FIRST htparam WHERE htparam.paramnr = 43 NO-LOCK. 
show-price = htparam.flogical.

FIND FIRST htparam WHERE paramnr = 224 NO-LOCK. 
p-224 = htparam.fdate.         /* Rulita 211024 | Fixing for serverless */

FIND FIRST l-untergrup WHERE l-untergrup.betriebsnr = 1 NO-LOCK NO-ERROR. 
IF AVAILABLE l-untergrup THEN avail-l-untergrup = YES.


FOR EACH l-lager NO-LOCK:
    CREATE t-l-lager.
    BUFFER-COPY l-lager TO t-l-lager.
END.
FOR EACH l-hauptgrp:
    CREATE t-l-hauptgrp.
    BUFFER-COPY l-hauptgrp TO t-l-hauptgrp.
END.
