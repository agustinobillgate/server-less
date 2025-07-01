DEFINE TEMP-TABLE t-hoteldpt LIKE hoteldpt.

DEFINE OUTPUT PARAMETER from-date   AS DATE.
DEFINE OUTPUT PARAMETER to-date     AS DATE.
DEFINE OUTPUT PARAMETER min-dept    AS INTEGER INITIAL 99.
DEFINE OUTPUT PARAMETER max-dept    AS INTEGER INITIAL 0.
DEFINE OUTPUT PARAMETER from-dept   AS INTEGER.
DEFINE OUTPUT PARAMETER to-dept     AS INTEGER.
DEFINE OUTPUT PARAMETER curr-dept   AS INTEGER.
DEFINE OUTPUT PARAMETER depname1    AS CHARACTER.
DEFINE OUTPUT PARAMETER depname2    AS CHARACTER.
DEFINE OUTPUT PARAMETER depname3    AS CHARACTER.
DEFINE OUTPUT PARAMETER TABLE FOR t-hoteldpt.

FIND FIRST hoteldpt WHERE hoteldpt.num GT 0 NO-LOCK NO-ERROR.
IF NOT AVAILABLE hoteldpt THEN RETURN NO-APPLY.

FIND FIRST htparam WHERE paramnr EQ 110 NO-LOCK.  /*Invoicing DATE */ 
from-date = htparam.fdate. 
to-date = htparam.fdate. 

min-dept = 999.
max-dept = 1.
FOR EACH hoteldpt WHERE hoteldpt.num GE 1 NO-LOCK BY hoteldpt.num: 
    IF min-dept GT hoteldpt.num THEN min-dept = hoteldpt.num.
    IF max-dept LT hoteldpt.num THEN max-dept = hoteldpt.num. 
END.
curr-dept = min-dept.
from-dept = min-dept. 
to-dept = max-dept. 

FIND FIRST hoteldpt WHERE hoteldpt.num EQ from-dept NO-LOCK. 
depname1 = hoteldpt.depart. 
FIND FIRST hoteldpt WHERE hoteldpt.num EQ to-dept NO-LOCK. 
depname2 = hoteldpt.depart. 
FIND FIRST hoteldpt WHERE hoteldpt.num EQ curr-dept NO-LOCK. 
depname3 = hoteldpt.depart. 

FOR EACH hoteldpt:
    CREATE t-hoteldpt.
    BUFFER-COPY hoteldpt TO t-hoteldpt.
END.



