
DEF INPUT PARAMETER resources-nr AS INT.
DEF OUTPUT PARAMETER avail-req AS LOGICAL INIT NO.

DEF BUFFER req FOR eg-cost.

FIND FIRST req WHERE req.resource-nr = resources-nr NO-LOCK NO-ERROR.
IF AVAILABLE req THEN avail-req = YES.
