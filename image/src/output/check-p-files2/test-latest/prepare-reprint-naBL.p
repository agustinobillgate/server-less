  
DEFINE TEMP-TABLE b1-list  
    FIELD reihenfolge   LIKE nightaudit.reihenfolge  
    FIELD hogarest      LIKE nightaudit.hogarest  
    FIELD bezeichnun    LIKE nightaudit.bezeichnun  
    FIELD rec-id        AS INTEGER.  
  
DEFINE OUTPUT PARAMETER store-flag AS LOGICAL INIT NO.  
DEFINE OUTPUT PARAMETER na-date    AS DATE.  
DEFINE OUTPUT PARAMETER na-time    AS INT.  
DEFINE OUTPUT PARAMETER na-name    AS CHAR.  
DEFINE OUTPUT PARAMETER TABLE FOR b1-list.  
  
FIND FIRST htparam WHERE paramnr = 230 NO-LOCK.   
IF htparam.feldtyp = 4 AND htparam.flogical THEN store-flag = YES.   
   
FIND FIRST htparam WHERE paramnr = 110 NO-LOCK.   
na-date = htparam.fdate - 1.   
  
FIND FIRST htparam WHERE paramnr = 103 NO-LOCK.   
na-time = htparam.finteger.   
   
FIND FIRST htparam WHERE paramnr = 253 NO-LOCK.   
na-name = htparam.fchar.   
  
  
RUN reprint-nabl.p (OUTPUT TABLE b1-list).  
