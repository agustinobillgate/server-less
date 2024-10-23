
DEF INPUT  PARAMETER a-int AS INT.
DEF OUTPUT PARAMETER guestname AS CHAR.

FIND FIRST guest WHERE guest.gastnr = a-int NO-LOCK NO-ERROR.
IF AVAILABLE guest THEN guestname = guest.NAME.
