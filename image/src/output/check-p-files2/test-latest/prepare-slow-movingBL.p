
DEF TEMP-TABLE t-l-lager
    FIELD lager-nr LIKE l-lager.lager-nr
    FIELD bezeich  LIKE l-lager.bezeich.

DEF TEMP-TABLE t-l-hauptgrp
    FIELD endkum   LIKE l-hauptgrp.endkum
    FIELD bezeich  LIKE l-hauptgrp.bezeich.

DEF INPUT  PARAMETER LnL-prog AS CHAR.
DEF OUTPUT PARAMETER LnL-filepath AS CHAR.
DEF OUTPUT PARAMETER show-price AS LOGICAL.
DEF OUTPUT PARAMETER TABLE FOR t-l-lager.
DEF OUTPUT PARAMETER TABLE FOR t-l-hauptgrp.

FIND FIRST htparam WHERE htparam.paramnr = 417 NO-LOCK. 
IF htparam.fchar NE "" THEN 
DO: 
    LnL-filepath = htparam.fchar. 
    IF SUBSTR(LnL-filepath, LENGTH(LnL-filepath), 1) NE "\" THEN 
        LnL-filepath = LnL-filepath + "\". 
    LnL-filepath = LnL-filepath + LnL-prog. 
END. 
FIND FIRST htparam WHERE htparam.paramnr = 43 NO-LOCK. 
show-price = htparam.flogical. 

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
