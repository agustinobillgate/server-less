
DEF INPUT PARAMETER journ-no AS CHAR.
DEF OUTPUT PARAMETER avail-gl-jouhdr AS LOGICAL INIT NO.

FIND FIRST gl-jouhdr WHERE gl-jouhdr.refno = journ-no
     NO-LOCK NO-ERROR.
IF AVAILABLE gl-jouhdr THEN avail-gl-jouhdr = YES.
