
DEF OUTPUT PARAMETER dept-limit AS INT.
DEF OUTPUT PARAMETER curr-anz AS INT.

RUN check-dept-limit.


PROCEDURE check-dept-limit:
  FIND FIRST htparam WHERE htparam.paramnr = 989 NO-LOCK. 
  IF htparam.finteger GT 0 THEN dept-limit = htparam.finteger. 
  curr-anz = -1. 
  FOR EACH hoteldpt NO-LOCK: 
     curr-anz = curr-anz + 1. 
   END. 
END. 
