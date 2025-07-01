
DEF INPUT  PARAMETER gastnr         AS INT.
DEF OUTPUT PARAMETER lname          AS CHAR.
DEF OUTPUT PARAMETER guest-gastnr   AS INT.

FIND FIRST guest WHERE guest.gastnr = gastnr NO-LOCK. 
lname = guest.NAME + ", " + guest.anredefirma. 
guest-gastnr = guest.gastnr
