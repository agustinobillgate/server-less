
DEF INPUT  PARAMETER gastnr AS INT.
DEF OUTPUT PARAMETER guest-gastnr AS INT.
DEF OUTPUT PARAMETER avail-guest AS LOGICAL INIT NO.

FIND FIRST guest WHERE guest.gastnr = gastnr USE-INDEX gastnr_index 
    NO-LOCK NO-ERROR. 
IF AVAILABLE guest THEN 
    ASSIGN
    guest-gastnr = guest.gastnr
    avail-guest = YES.
