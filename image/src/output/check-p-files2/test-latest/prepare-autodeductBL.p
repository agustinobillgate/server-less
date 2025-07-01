DEFINE TEMP-TABLE t-l-lager
    FIELD lager-nr LIKE l-lager.lager-nr
    FIELD bezeich  LIKE l-lager.bezeich.
DEFINE TEMP-TABLE t-l-hauptgrp
    FIELD endkum   LIKE l-hauptgrp.endkum
    FIELD bezeich  LIKE l-hauptgrp.bezeich.

DEFINE OUTPUT PARAMETER billdate        AS DATE.
DEFINE OUTPUT PARAMETER mat-grp         AS INTEGER.
DEFINE OUTPUT PARAMETER transdate       AS DATE.
DEFINE OUTPUT PARAMETER p-221           AS DATE.
DEFINE OUTPUT PARAMETER p-224           AS DATE.
DEFINE OUTPUT PARAMETER TABLE FOR t-l-lager.
DEFINE OUTPUT PARAMETER TABLE FOR t-l-hauptgrp.

FIND FIRST htparam WHERE htparam.paramnr = 110 NO-LOCK. 
billdate = htparam.fdate. 
 
FIND FIRST htparam WHERE htparam.paramnr = 268 NO-LOCK. 
mat-grp = htparam.finteger. 
 
FIND FIRST htparam WHERE paramnr = 224 NO-LOCK. 
transdate = htparam.fdate.        /* Rulita 211024 | Fixing for serverless */

FOR EACH l-lager:
    CREATE t-l-lager.
    ASSIGN
        t-l-lager.lager-nr = l-lager.lager-nr
        t-l-lager.bezeich  = l-lager.bezeich.
END.

FOR EACH l-hauptgrp:
    CREATE t-l-hauptgrp.
    ASSIGN
    t-l-hauptgrp.endkum   = l-hauptgrp.endkum
    t-l-hauptgrp.bezeich  = l-hauptgrp.bezeich.
END.

FIND FIRST htparam WHERE htparam.paramnr = 221 NO-LOCK.
p-221 = htparam.fdate.
FIND FIRST htparam WHERE htparam.paramnr = 224 NO-LOCK.
p-224 = htparam.fdate.

