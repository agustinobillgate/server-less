DEF TEMP-TABLE t-gc-pi LIKE gc-pi.

DEF INPUT PARAMETER docu-nr AS CHAR.
DEF OUTPUT PARAMETER TABLE FOR t-gc-pi.

FIND FIRST gc-pi WHERE gc-pi.docu-nr = docu-nr NO-LOCK.
CREATE t-gc-pi.
BUFFER-COPY gc-pi TO t-gc-pi.
