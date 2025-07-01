
DEF INPUT-OUTPUT PARAMETER from-art AS INTEGER.
DEF INPUT-OUTPUT PARAMETER to-art   AS INTEGER.
DEF OUTPUT PARAMETER long-digit     AS LOGICAL.
DEF OUTPUT PARAMETER day1           AS INTEGER INITIAL 30.
DEF OUTPUT PARAMETER day2           AS INTEGER INITIAL 30.
DEF OUTPUT PARAMETER day3           AS INTEGER INITIAL 30.
DEF OUTPUT PARAMETER price-decimal  AS INTEGER INITIAL 0.
DEF OUTPUT PARAMETER default-fcurr  AS CHAR     INITIAL "".
DEF OUTPUT PARAMETER dollar-rate    AS DECIMAL. 

FIND FIRST htparam WHERE paramnr = 330 NO-LOCK. 
IF finteger NE 0 THEN day1 = htparam.finteger.               /* Rulita 211024 | Fixing for serverless */  
FIND FIRST htparam WHERE paramnr = 331 NO-LOCK. 
IF finteger NE 0 THEN day2 = htparam.finteger.               /* Rulita 211024 | Fixing for serverless */  
FIND FIRST htparam WHERE paramnr = 332 NO-LOCK. 
IF finteger NE 0 THEN day3 = htparam.finteger.               /* Rulita 211024 | Fixing for serverless */  
ASSIGN
    day2 = day2 + day1
    day3 = day3 + day2
.

RUN htplogic.p (246, OUTPUT long-digit).
RUN htpint.p   (491, OUTPUT price-decimal).
RUN htpchar.p  (144, OUTPUT default-fcurr).
 
FOR EACH artikel WHERE artikel.departement = 0 
     AND (artikel.artart = 2 OR artikel.artart = 7) 
     AND artikel.activeflag = YES NO-LOCK: 
  IF from-art GT artikel.artnr THEN from-art = artikel.artnr. 
  IF to-art LT artikel.artnr THEN to-art = artikel.artnr. 
END. 

FIND FIRST htparam WHERE htparam.paramnr = 144 NO-LOCK. 
FIND FIRST waehrung WHERE waehrung.wabkurz = htparam.fchar NO-LOCK NO-ERROR. 
IF AVAILABLE waehrung THEN dollar-rate = waehrung.ankauf.


