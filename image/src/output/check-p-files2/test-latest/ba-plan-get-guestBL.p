
DEF INPUT  PARAMETER t-gastnr        AS INT.
DEF OUTPUT PARAMETER avail-guest     AS LOGICAL INIT NO.
DEF OUTPUT PARAMETER guest-gastnr    AS INT.
DEF OUTPUT PARAMETER recid-guest     AS INT.
DEF OUTPUT PARAMETER guest-full-name AS CHAR.
FIND FIRST guest WHERE guest.gastnr = t-gastnr NO-LOCK NO-ERROR.
IF AVAILABLE guest THEN
    ASSIGN
    avail-guest     = YES
    guest-gastnr    = guest.gastnr
    recid-guest     = RECID(guest)
    guest-full-name = guest.name + ", " + guest.vorname1 + " " + 
                      guest.anrede1 + guest.anredefirma.
