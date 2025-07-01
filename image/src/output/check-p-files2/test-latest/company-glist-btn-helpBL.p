
DEF INPUT  PARAMETER gastnr     AS INT.
DEF OUTPUT PARAMETER from-name  AS CHAR.

FIND FIRST guest WHERE guest.gastnr = gastnr NO-LOCK. 
from-name = guest.name. 
