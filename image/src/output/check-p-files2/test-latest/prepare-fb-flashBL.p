
DEF OUTPUT PARAMETER food       AS INT.
DEF OUTPUT PARAMETER bev        AS INT.
DEF OUTPUT PARAMETER date2      AS DATE.
DEF OUTPUT PARAMETER date1      AS DATE.



FIND FIRST htparam WHERE paramnr = 257 NO-LOCK. 
food = htparam.finteger.         /* Rulita 211024 | Fixing for serverless */
FIND FIRST htparam WHERE paramnr = 258 NO-LOCK. 
bev = htparam.finteger.          /* Rulita 211024 | Fixing for serverless */
 
/*FIND FIRST htparam WHERE paramnr = 1081 NO-LOCK. 
ldry = htparam.finteger.               /* Rulita 211024 | Fixing for serverless */  
FIND FIRST htparam WHERE paramnr = 1082 NO-LOCK. 
dstore = htparam.finteger.               /* Rulita 211024 | Fixing for serverless */  */
 
FIND FIRST htparam WHERE paramnr = 474 NO-LOCK. 
date2 = htparam.fdate.            /* Rulita 211024 | Fixing for serverless */
date1 = DATE(month(date2), 1, year(date2)). 

