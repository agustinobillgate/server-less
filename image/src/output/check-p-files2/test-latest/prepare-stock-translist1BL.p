
DEF TEMP-TABLE t-l-lager LIKE l-lager.
DEF TEMP-TABLE t-l-hauptgrp
    FIELD endkum  LIKE l-hauptgrp.endkum
    FIELD bezeich LIKE l-hauptgrp.bezeich.

DEF OUTPUT PARAMETER show-price AS LOGICAL.
DEF OUTPUT PARAMETER avail-queasy AS LOGICAL INIT NO.
DEF OUTPUT PARAMETER TABLE FOR t-l-lager.
DEF OUTPUT PARAMETER TABLE FOR t-l-hauptgrp.

FIND FIRST htparam WHERE htparam.paramnr = 43 NO-LOCK. 
show-price = htparam.flogical. 

FIND FIRST queasy WHERE queasy.KEY = 121 NO-LOCK NO-ERROR.
IF AVAILABLE queasy THEN avail-queasy = YES.

FOR EACH l-lager NO-LOCK:
    CREATE t-l-lager.
    BUFFER-COPY l-lager TO t-l-lager.
END.
FOR EACH l-hauptgrp:
    CREATE t-l-hauptgrp.
    BUFFER-COPY l-hauptgrp TO t-l-hauptgrp.
END.
