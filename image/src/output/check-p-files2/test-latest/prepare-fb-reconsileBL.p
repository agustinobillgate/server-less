
DEF OUTPUT PARAMETER food AS INT.
DEF OUTPUT PARAMETER bev AS INT.
DEF OUTPUT PARAMETER to-date AS DATE.

FIND FIRST htparam WHERE paramnr = 257 NO-LOCK. 
food = htparam.finteger.     /* Rulita 211024 | Fixing for serverless */
FIND FIRST htparam WHERE paramnr = 258 NO-LOCK. 
bev = htparam.finteger.      /* Rulita 211024 | Fixing for serverless */
FIND FIRST htparam WHERE paramnr = 474 NO-LOCK. 
to-date = htparam.fdate.     /* Rulita 211024 | Fixing for serverless */
