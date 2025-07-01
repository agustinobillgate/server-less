
DEF INPUT PARAMETER action-actionnr AS INT.
DEF OUTPUT PARAMETER avail-req AS LOGICAL INIT NO.

DEF BUFFER req FOR eg-mdetail.

FIND FIRST req WHERE req.KEY = 1 AND req.nr = action-actionnr NO-LOCK NO-ERROR.
IF AVAILABLE req THEN avail-req = YES.
