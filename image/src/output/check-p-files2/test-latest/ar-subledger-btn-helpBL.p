
DEF INPUT  PARAMETER gastNo     AS INT.
DEF OUTPUT PARAMETER guest-name AS CHAR.

FIND FIRST guest WHERE guest.gastnr = gastNo NO-LOCK.
guest-name = guest.NAME.
