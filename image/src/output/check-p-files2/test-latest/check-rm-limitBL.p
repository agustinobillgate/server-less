
DEF OUTPUT PARAMETER room-limit AS INT.
DEF OUTPUT PARAMETER curr-anz AS INT.

RUN check-rm-limit. 


PROCEDURE check-rm-limit: 
DEF BUFFER rbuff FOR zimmer.
  FIND FIRST htparam WHERE htparam.paramnr = 975 NO-LOCK. 
  IF htparam.finteger GT 0 THEN room-limit = htparam.finteger. 
  curr-anz = 0. 
  FOR EACH rbuff NO-LOCK: 
     curr-anz = curr-anz + 1. 
   END. 
END. 
