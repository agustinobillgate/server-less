DEFINE TEMP-TABLE l-list LIKE l-hauptgrp.

DEF INPUT PARAMETER TABLE FOR l-list.
DEF INPUT PARAMETER case-type AS INT.

FIND FIRST l-list NO-ERROR.
IF NOT AVAILABLE l-list THEN RETURN.

IF case-type = 1 THEN        /*add*/
DO:
    CREATE l-hauptgrp.
    l-hauptgrp.endkum = l-list.endkum. 
    l-hauptgrp.bezeich = l-list.bezeich. 
END.
ELSE IF case-type = 2 THEN   /*chg*/
DO:
    FIND FIRST l-hauptgrp WHERE l-hauptgrp.endkum = l-list.endkum.
    l-hauptgrp.bezeich = l-list.bezeich.
END.
