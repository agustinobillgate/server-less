
DEF INPUT  PARAMETER b-zinr AS CHAR.
DEF OUTPUT PARAMETER from-date AS DATE.
DEF OUTPUT PARAMETER zinr AS CHAR.

DEF BUFFER room FOR zimmer.
FIND FIRST room WHERE room.zinr = b-zinr NO-LOCK. 
zinr = room.zinr. 

FIND FIRST htparam WHERE paramnr = 87 NO-LOCK. 
from-date = fdate. 
