
DEF TEMP-TABLE t-l-hauptgrp
    FIELD endkum   LIKE l-hauptgrp.endkum
    FIELD bezeich  LIKE l-hauptgrp.bezeich.

DEF OUTPUT PARAMETER ci-date AS DATE.
DEF OUTPUT PARAMETER TABLE FOR t-l-hauptgrp.

RUN htpdate.p (87, OUTPUT ci-date).

FOR EACH l-hauptgrp:
    CREATE t-l-hauptgrp.
    ASSIGN
    t-l-hauptgrp.endkum   = l-hauptgrp.endkum
    t-l-hauptgrp.bezeich  = l-hauptgrp.bezeich.
END.
