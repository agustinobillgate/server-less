
DEF TEMP-TABLE t-l-lager
    FIELD lager-nr LIKE l-lager.lager-nr
    FIELD bezeich  LIKE l-lager.bezeich.
DEF TEMP-TABLE t-l-hauptgrp
    FIELD endkum   LIKE l-hauptgrp.endkum
    FIELD bezeich  LIKE l-hauptgrp.bezeich.

DEF OUTPUT PARAMETER show-price AS LOGICAL.
DEF OUTPUT PARAMETER TABLE FOR t-l-lager.
DEF OUTPUT PARAMETER TABLE FOR t-l-hauptgrp.

RUN htplogic.p(43, OUTPUT show-price).
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
