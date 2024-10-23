
DEF TEMP-TABLE t-l-lager
    FIELD lager-nr LIKE l-lager.lager-nr
    FIELD bezeich  LIKE l-lager.bezeich.

DEF TEMP-TABLE t-l-hauptgrp
    FIELD endkum   LIKE l-hauptgrp.endkum
    FIELD bezeich  LIKE l-hauptgrp.bezeich.

DEF OUTPUT PARAMETER billdate AS DATE.
DEF OUTPUT PARAMETER mat-grp AS INT.
DEF OUTPUT PARAMETER early-adjust AS LOGICAL.
DEF OUTPUT PARAMETER inv-postdate AS DATE.
DEF OUTPUT PARAMETER transdate AS DATE.
DEF OUTPUT PARAMETER TABLE FOR t-l-hauptgrp.
DEF OUTPUT PARAMETER TABLE FOR t-l-lager.

FIND FIRST htparam WHERE htparam.paramnr = 110 NO-LOCK. 
billdate = htparam.fdate. 
 
FIND FIRST htparam WHERE htparam.paramnr = 268 NO-LOCK. 
mat-grp = htparam.finteger. 
 
FIND FIRST htparam WHERE paramnr = 401 NO-LOCK. 
IF htparam.paramgruppe = 21 THEN early-adjust = htparam.flogical.

FIND FIRST htparam WHERE htparam.paramnr = 474 NO-LOCK. 
inv-postdate = htparam.fdate. 

FIND FIRST htparam WHERE paramnr = 224 NO-LOCK. 
transdate = htparam.fdate.         /* Rulita 211024 | Fixing for serverless */

FOR EACH l-hauptgrp:
    CREATE t-l-hauptgrp.
    ASSIGN
    t-l-hauptgrp.endkum   = l-hauptgrp.endkum
    t-l-hauptgrp.bezeich  = l-hauptgrp.bezeich.
END.

FOR EACH l-lager:
    CREATE t-l-lager.
    ASSIGN
    t-l-lager.lager-nr = l-lager.lager-nr
    t-l-lager.bezeich  = l-lager.bezeich.
END.
