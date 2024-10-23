
DEF INPUT PARAMETER l-hauptgrp-endkum AS INT.
DEF OUTPUT PARAMETER flag AS INT INIT 0.

FIND FIRST l-hauptgrp WHERE l-hauptgrp.endkum = l-hauptgrp-endkum.
FIND FIRST l-artikel WHERE l-artikel.endkum = l-hauptgrp-endkum NO-LOCK NO-ERROR. 
IF AVAILABLE l-artikel THEN flag = 1.
ELSE 
DO:
    FIND CURRENT l-hauptgrp EXCLUSIVE-LOCK. 
    delete l-hauptgrp. 
END.
