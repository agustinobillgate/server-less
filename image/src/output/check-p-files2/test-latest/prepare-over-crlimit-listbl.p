DEF TEMP-TABLE t-hoteldpt
    FIELD num       LIKE hoteldpt.num
    FIELD depart    LIKE hoteldpt.depart.

DEF OUTPUT PARAMETER from-dept       AS INT INIT 1.
DEF OUTPUT PARAMETER to-dept         AS INT INIT 99.
DEF OUTPUT PARAMETER depname1        AS CHAR.
DEF OUTPUT PARAMETER depname2        AS CHAR.
DEF OUTPUT PARAMETER billdate        AS DATE.
DEF OUTPUT PARAMETER TABLE FOR t-hoteldpt.

DEFINE VARIABLE min-dept AS INTEGER.
DEFINE VARIABLE max-dept AS INTEGER. 


RUN select-dept.

FIND FIRST hoteldpt WHERE hoteldpt.num GT 0 NO-LOCK NO-ERROR.
IF NOT AVAILABLE hoteldpt THEN RETURN NO-APPLY.

FIND FIRST htparam WHERE paramnr = 110 no-lock.  /* Invoicing DATE */ 
billdate = htparam.fdate.                                             

FOR EACH hoteldpt:
    CREATE t-hoteldpt.
    ASSIGN
        t-hoteldpt.num       = hoteldpt.num
        t-hoteldpt.depart    = hoteldpt.depart.
END.

PROCEDURE select-dept: 
  DEFINE VARIABLE ldry   AS INTEGER.
  DEFINE VARIABLE dstore AS INTEGER.

  FIND FIRST htparam WHERE paramnr = 1081 NO-LOCK. 
  ldry = htparam.finteger.               /* Rulita 211024 | Fixing for serverless */  
  FIND FIRST htparam WHERE paramnr = 1082 NO-LOCK. 
  dstore = htparam.finteger.               /* Rulita 211024 | Fixing for serverless */  
  ASSIGN
      min-dept = 999
      max-dept = 1
  . 
  FOR EACH hoteldpt WHERE hoteldpt.num GE 1 AND hoteldpt.num NE ldry 
      AND hoteldpt.num NE dstore NO-LOCK BY hoteldpt.num: 
      IF min-dept GT hoteldpt.num THEN min-dept = hoteldpt.num.
      IF max-dept LT hoteldpt.num THEN max-dept = hoteldpt.num. 
  END. 

  from-dept = min-dept. 
  to-dept = max-dept. 
  FIND FIRST hoteldpt WHERE hoteldpt.num = from-dept NO-LOCK. 
  depname1 = hoteldpt.depart. 
  FIND FIRST hoteldpt WHERE hoteldpt.num = to-dept NO-LOCK. 
  depname2 = hoteldpt.depart. 

END. 
