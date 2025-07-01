
DEFINE OUTPUT PARAMETER vipnr1 AS INTEGER INITIAL 999999999. 
DEFINE OUTPUT PARAMETER vipnr2 AS INTEGER INITIAL 999999999. 
DEFINE OUTPUT PARAMETER vipnr3 AS INTEGER INITIAL 999999999. 
DEFINE OUTPUT PARAMETER vipnr4 AS INTEGER INITIAL 999999999. 
DEFINE OUTPUT PARAMETER vipnr5 AS INTEGER INITIAL 999999999. 
DEFINE OUTPUT PARAMETER vipnr6 AS INTEGER INITIAL 999999999. 
DEFINE OUTPUT PARAMETER vipnr7 AS INTEGER INITIAL 999999999. 
DEFINE OUTPUT PARAMETER vipnr8 AS INTEGER INITIAL 999999999. 
DEFINE OUTPUT PARAMETER vipnr9 AS INTEGER INITIAL 999999999. 

RUN get-vipnr.

PROCEDURE get-vipnr: 
  FIND FIRST htparam WHERE paramnr = 700 NO-LOCK. 
  IF finteger NE 0 THEN vipnr1 = htparam.finteger.               /* Rulita 211024 | Fixing for serverless */  
  FIND FIRST htparam WHERE paramnr = 701 NO-LOCK. 
  IF finteger NE 0 THEN vipnr2 = htparam.finteger.               /* Rulita 211024 | Fixing for serverless */  
  FIND FIRST htparam WHERE paramnr = 702 NO-LOCK. 
  IF finteger NE 0 THEN vipnr3 = htparam.finteger.               /* Rulita 211024 | Fixing for serverless */  
  FIND FIRST htparam WHERE paramnr = 703 NO-LOCK. 
  IF finteger NE 0 THEN vipnr4 = htparam.finteger.               /* Rulita 211024 | Fixing for serverless */  
  FIND FIRST htparam WHERE paramnr = 704 NO-LOCK. 
  IF finteger NE 0 THEN vipnr5 = htparam.finteger.               /* Rulita 211024 | Fixing for serverless */  
  FIND FIRST htparam WHERE paramnr = 705 NO-LOCK. 
  IF finteger NE 0 THEN vipnr6 = htparam.finteger.               /* Rulita 211024 | Fixing for serverless */  
  FIND FIRST htparam WHERE paramnr = 706 NO-LOCK. 
  IF finteger NE 0 THEN vipnr7 = htparam.finteger.               /* Rulita 211024 | Fixing for serverless */  
  FIND FIRST htparam WHERE paramnr = 707 NO-LOCK. 
  IF finteger NE 0 THEN vipnr8 = htparam.finteger.               /* Rulita 211024 | Fixing for serverless */  
  FIND FIRST htparam WHERE paramnr = 708 NO-LOCK. 
  IF finteger NE 0 THEN vipnr9 = htparam.finteger.               /* Rulita 211024 | Fixing for serverless */  
END. 
 
