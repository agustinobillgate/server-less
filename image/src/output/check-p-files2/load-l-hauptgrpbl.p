DEF TEMP-TABLE t-l-hauptgrp LIKE l-hauptgrp.

DEF OUTPUT PARAMETER TABLE  FOR t-l-hauptgrp.
FOR EACH l-hauptgrp NO-LOCK:
    CREATE t-l-hauptgrp.
    BUFFER-COPY l-hauptgrp TO t-l-hauptgrp.
END.
