
DEF INPUT  PARAMETER akt-line1-gastnr AS INT.
DEF OUTPUT PARAMETER avail-guest AS LOGICAL INIT NO.

FIND FIRST guest WHERE guest.gastnr = akt-line1-gastnr NO-LOCK NO-ERROR.
IF NOT AVAILABLE guest THEN.
ELSE
DO :
    avail-guest = YES.
END.
