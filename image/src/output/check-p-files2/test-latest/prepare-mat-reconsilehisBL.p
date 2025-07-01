
DEF TEMP-TABLE t-l-hauptgrp LIKE l-hauptgrp.
DEF TEMP-TABLE t-l-lager    LIKE l-lager.

DEF OUTPUT PARAMETER from-grp   AS INT.
DEF OUTPUT PARAMETER to-date    AS DATE.
DEF OUTPUT PARAMETER from-date  AS DATE.
DEF OUTPUT PARAMETER long-digit AS LOGICAL.
DEF OUTPUT PARAMETER TABLE FOR t-l-hauptgrp.
DEF OUTPUT PARAMETER TABLE FOR t-l-lager.

FIND FIRST htparam WHERE htparam.paramnr = 268 NO-LOCK. 
from-grp = htparam.finteger. 
FIND FIRST htparam WHERE htparam.paramnr = 221 NO-LOCK. 
to-date = htparam.fdate.         /* Rulita 211024 | Fixing for serverless */
from-date = DATE(month(to-date), 1, year(to-date)). 
FIND FIRST htparam WHERE paramnr = 246 NO-LOCK. 
long-digit = htparam.flogical. 

FOR EACH l-hauptgrp:
    CREATE t-l-hauptgrp.
    BUFFER-COPY l-hauptgrp TO t-l-hauptgrp.
END.

FOR EACH l-lager:
    CREATE t-l-lager.
    BUFFER-COPY l-lager TO t-l-lager.
END.

