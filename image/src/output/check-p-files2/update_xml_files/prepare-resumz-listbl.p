
DEF TEMP-TABLE t-hoteldpt LIKE hoteldpt.

DEF OUTPUT PARAMETER long-digit AS LOGICAL.
DEF OUTPUT PARAMETER to-date    AS DATE.
DEF OUTPUT PARAMETER ldry       AS INT.
DEF OUTPUT PARAMETER dstore     AS INT.
DEF OUTPUT PARAMETER from-dept  AS INT.
DEF OUTPUT PARAMETER to-dept    AS INT.
DEF OUTPUT PARAMETER depname1   AS CHAR.
DEF OUTPUT PARAMETER depname2   AS CHAR.
DEF OUTPUT PARAMETER TABLE FOR t-hoteldpt.

DEFINE VARIABLE min-dept AS INTEGER /*INITIAL 0*/.
DEFINE VARIABLE max-dept AS INTEGER /*INITIAL 99*/.

FIND FIRST htparam WHERE paramnr = 246 NO-LOCK. 
long-digit = htparam.flogical. 

to-date = today. 
RUN select-dept. 
FOR EACH hoteldpt:
    CREATE t-hoteldpt.
    BUFFER-COPY hoteldpt TO t-hoteldpt.
END.


PROCEDURE select-dept: 
  FIND FIRST htparam WHERE paramnr = 1081 NO-LOCK. 
  ldry = htparam.finteger.               /* Rulita 211024 | Fixing for serverless */  
  FIND FIRST htparam WHERE paramnr = 1082 NO-LOCK. 
  dstore = htparam.finteger.               /* Rulita 211024 | Fixing for serverless */  

  /*MT 14/01/15*/
  min-dept = 0. 
  FOR EACH hoteldpt WHERE hoteldpt.num GE 1 AND hoteldpt.num NE ldry 
    AND hoteldpt.num NE dstore NO-LOCK BY hoteldpt.num: 
    IF max-dept LT hoteldpt.num THEN max-dept = hoteldpt.num. 
  END. 
  
 
  from-dept = min-dept. 
  to-dept = max-dept. 
 
  FIND FIRST hoteldpt WHERE hoteldpt.num = from-dept NO-LOCK NO-ERROR. 
  IF AVAILABLE hoteldpt THEN depname1 = hoteldpt.depart. 
  FIND FIRST hoteldpt WHERE hoteldpt.num = to-dept NO-LOCK NO-ERROR. 
  IF AVAILABLE hoteldpt THEN depname2 = hoteldpt.depart. 
END. 
