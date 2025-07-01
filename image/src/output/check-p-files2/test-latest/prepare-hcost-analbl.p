
DEF OUTPUT PARAMETER long-digit     AS LOGICAL.
DEF OUTPUT PARAMETER price-decimal  AS INTEGER.
DEF OUTPUT PARAMETER to-date        AS DATE.
DEF OUTPUT PARAMETER from-date      AS DATE.
DEF OUTPUT PARAMETER bill-date      AS DATE.
DEF OUTPUT PARAMETER f-eknr         AS INTEGER.
DEF OUTPUT PARAMETER b-eknr         AS INTEGER.
DEF OUTPUT PARAMETER fL-eknr        AS INTEGER.
DEF OUTPUT PARAMETER bL-eknr        AS INTEGER.
DEF OUTPUT PARAMETER bev-food       AS CHAR. 
DEF OUTPUT PARAMETER food-bev       AS CHAR.
DEF OUTPUT PARAMETER price-type     AS INTEGER.

FIND FIRST htparam WHERE paramnr = 246 NO-LOCK. 
long-digit = htparam.flogical. 

FIND FIRST htparam WHERE htparam.paramnr = 491 NO-LOCK. 
price-decimal = htparam.finteger.   /* non-digit OR digit version */ 
/* 
price-decimal = 2. 
*/ 
FIND FIRST htparam WHERE paramnr = 224 NO-LOCK. 
to-date = htparam.fdate.        /* Rulita 211024 | Fixing for serverless */
from-date = DATE(month(to-date), 1, year(to-date)). 
FIND FIRST htparam WHERE paramnr = 110 NO-LOCK. 
bill-date = htparam.fdate.      /* Rulita 211024 | Fixing for serverless */
 
/** F&B Sales Articles */ 
FIND FIRST htparam WHERE paramnr = 862 NO-LOCK. 
f-eknr = htparam.finteger.        /* Rulita 211024 | Fixing for serverless */
FIND FIRST htparam WHERE paramnr = 892 NO-LOCK. 
b-eknr = htparam.finteger.        /* Rulita 211024 | Fixing for serverless */
 
/** F&B Inventory Articles */ 
FIND FIRST htparam WHERE paramnr = 257 NO-LOCK. 
fL-eknr = htparam.finteger.        /* Rulita 211024 | Fixing for serverless */
FIND FIRST htparam WHERE paramnr = 258 NO-LOCK. 
bL-eknr = htparam.finteger.        /* Rulita 211024 | Fixing for serverless */
 
FIND FIRST htparam WHERE paramnr = 272 NO-LOCK. 
bev-food = htparam.fchar.        /* Rulita 211024 | Fixing for serverless */
FIND FIRST htparam WHERE paramnr = 275 NO-LOCK. 
food-bev = htparam.fchar.        /* Rulita 211024 | Fixing for serverless */
 
FIND FIRST htparam WHERE paramnr = 1024 NO-LOCK. 
price-type = htparam.finteger. 
