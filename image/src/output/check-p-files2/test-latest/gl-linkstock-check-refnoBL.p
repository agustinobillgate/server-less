
DEF INPUT  PARAMETER refno AS CHAR.
DEF INPUT  PARAMETER jtype AS INTEGER.
DEF OUTPUT PARAMETER avail-gl-jouhdr AS LOGICAL INIT NO.

FIND FIRST gl-jouhdr WHERE gl-jouhdr.refno = refno 
    AND gl-jouhdr.jtype = jtype NO-LOCK NO-ERROR.
IF AVAILABLE gl-jouhdr THEN avail-gl-jouhdr = YES.
