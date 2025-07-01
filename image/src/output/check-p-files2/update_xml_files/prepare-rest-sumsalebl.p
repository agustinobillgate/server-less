
DEF TEMP-TABLE tt-artnr
    FIELD curr-i AS INTEGER
    FIELD artnr  AS INTEGER
.
DEF TEMP-TABLE tt-bezeich
    FIELD curr-i  AS INTEGER
    FIELD bezeich AS CHAR
.

DEF INPUT PARAMETER curr-dept AS INT.
DEF OUTPUT PARAMETER ldry AS INT.
DEF OUTPUT PARAMETER dstore AS INT.
DEF OUTPUT PARAMETER clb AS INT.
DEF OUTPUT PARAMETER price-decimal AS INT.
DEF OUTPUT PARAMETER exchg-rate AS DECIMAL.
DEF OUTPUT PARAMETER curr-local AS CHAR.
DEF OUTPUT PARAMETER curr-foreign AS CHAR.
DEF OUTPUT PARAMETER anzahl AS INT.
DEF OUTPUT PARAMETER sep-line AS CHAR.
DEF OUTPUT PARAMETER dept-name AS CHAR.
DEF OUTPUT PARAMETER from-date AS DATE.

DEF OUTPUT PARAMETER TABLE FOR tt-bezeich.
DEF OUTPUT PARAMETER TABLE FOR tt-artnr.

DEF OUTPUT PARAMETER p-240 AS LOGICAL.


DEF VARIABLE bezeich    AS CHAR EXTENT 5    INIT ["","","","",""]. 
DEF VARIABLE artnr-list AS INTEGER EXTENT 5 INIT [0,0,0,0,0]. 

DEFINE VARIABLE i AS INTEGER. 
DEFINE VARIABLE paramnr-list AS INTEGER EXTENT 5 
  INITIAL [489, 490, 492, 553, 554]. 

FIND FIRST htparam WHERE paramnr = 240 no-lock. /* double currency */ 
p-240 = htparam.flogical.
FIND FIRST htparam WHERE paramnr = 1081 NO-LOCK. 
ldry = htparam.finteger.               /* Rulita 211024 | Fixing for serverless */  
FIND FIRST htparam WHERE paramnr = 1082 NO-LOCK. 
dstore = htparam.finteger.               /* Rulita 211024 | Fixing for serverless */  
FIND FIRST htparam WHERE paramnr = 1045 NO-LOCK. 
clb = htparam.finteger.               /* Rulita 211024 | Fixing for serverless */  

FIND FIRST htparam WHERE htparam.paramnr = 491. 
price-decimal = htparam.finteger.   /* non-digit OR digit version */ 
 
FIND FIRST htparam WHERE htparam.paramnr = 144 NO-LOCK. 
FIND FIRST waehrung WHERE waehrung.wabkurz = htparam.fchar NO-LOCK NO-ERROR. 
IF AVAILABLE waehrung THEN exchg-rate = waehrung.ankauf / waehrung.einheit. 
ELSE exchg-rate = 1. 
 
FIND FIRST htparam WHERE paramnr = 152 NO-LOCK. 
curr-local = fchar. 
FIND FIRST htparam WHERE paramnr = 144 NO-LOCK. 
curr-foreign = fchar. 
 
DO i = 1 TO 5: 
  FIND FIRST htparam WHERE htparam.paramnr = paramnr-list[i] NO-LOCK. 
  artnr-list[i] = htparam.finteger. 
  IF htparam.finteger NE 0 THEN 
  DO: 
    anzahl = anzahl + 1. 
    FIND FIRST artikel WHERE artikel.artnr = htparam.finteger 
        AND artikel.departement = 1 NO-LOCK NO-ERROR. 
    IF AVAILABLE artikel THEN bezeich[i] = artikel.bezeich. 
  END. 
  CREATE tt-artnr.
  ASSIGN
      tt-artnr.curr-i = i
      tt-artnr.artnr = artnr-list[i]
  .
  CREATE tt-bezeich.
  ASSIGN
      tt-bezeich.curr-i = i
      tt-bezeich.bezeich = bezeich[i]
  .
END. 
 
sep-line = "". 
DO i = 1 TO 116: 
  sep-line = sep-line + "-". 
END. 

FIND FIRST htparam WHERE paramnr = 110 no-lock.  /*Invoicing DATE */ 
from-date = htparam.fdate. 

FIND FIRST hoteldpt WHERE hoteldpt.num GT 0 AND hoteldpt.num = curr-dept
    NO-LOCK NO-ERROR. 
IF AVAILABLE hoteldpt THEN dept-name = hoteldpt.depart. 
