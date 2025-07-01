
DEF TEMP-TABLE t-l-lager LIKE l-lager.
DEF TEMP-TABLE t-l-hauptgrp
    FIELD endkum  LIKE l-hauptgrp.endkum
    FIELD bezeich LIKE l-hauptgrp.bezeich.


DEF OUTPUT PARAMETER TABLE FOR t-l-lager.
DEF OUTPUT PARAMETER TABLE FOR t-l-hauptgrp.

DEF OUTPUT PARAMETER gst-flag AS LOGICAL INIT NO.

FOR EACH l-lager NO-LOCK:
    CREATE t-l-lager.
    BUFFER-COPY l-lager TO t-l-lager.
END.

FOR EACH l-hauptgrp:
    CREATE t-l-hauptgrp.
    BUFFER-COPY l-hauptgrp TO t-l-hauptgrp.
END.


/*gst for penang*/
FIND FIRST l-lieferant WHERE l-lieferant.firma = "GST" NO-LOCK NO-ERROR.
IF AVAILABLE l-lieferant THEN ASSIGN gst-flag = YES.
ELSE ASSIGN gst-flag = NO.

