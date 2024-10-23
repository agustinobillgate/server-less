
DEF OUTPUT PARAMETER day1 AS INT.
DEF OUTPUT PARAMETER day2 AS INT.
DEF OUTPUT PARAMETER day3 AS INT.
DEF OUTPUT PARAMETER to-date AS DATE.
DEF OUTPUT PARAMETER price-decimal AS INT.

FIND FIRST htparam WHERE paramnr = 330 NO-LOCK. 
IF finteger NE 0 THEN day1 = htparam.finteger.               /* Rulita 211024 | Fixing for serverless */  
FIND FIRST htparam WHERE paramnr = 331 NO-LOCK. 
IF finteger NE 0 THEN day2 = htparam.finteger.               /* Rulita 211024 | Fixing for serverless */  
FIND FIRST htparam WHERE paramnr = 332 NO-LOCK. 
IF finteger NE 0 THEN day3 = htparam.finteger.               /* Rulita 211024 | Fixing for serverless */  
day2 = day2 + day1. 
day3 = day3 + day2. 
to-date = today. 
FIND FIRST htparam WHERE htparam.paramnr = 491. 
price-decimal = htparam.finteger. 
