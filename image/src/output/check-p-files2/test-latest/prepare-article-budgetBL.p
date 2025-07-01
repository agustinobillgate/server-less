
DEF TEMP-TABLE t-hoteldpt LIKE hoteldpt.
DEF TEMP-TABLE t-artikel  LIKE artikel.
DEF TEMP-TABLE t-budget   LIKE budget.

DEF INPUT  PARAMETER dept           AS INT.
DEF OUTPUT PARAMETER price-decimal  AS INT.
DEF OUTPUT PARAMETER bill-date      AS DATE.
DEF OUTPUT PARAMETER from-date      AS DATE.
DEF OUTPUT PARAMETER to-date        AS DATE.
DEF OUTPUT PARAMETER TABLE FOR t-hoteldpt.
DEF OUTPUT PARAMETER TABLE FOR t-artikel.
DEF OUTPUT PARAMETER TABLE FOR t-budget.

FIND FIRST htparam WHERE htparam.paramnr = 491 NO-LOCK. 
price-decimal = htparam.finteger. 
FIND FIRST htparam WHERE paramnr = 110 no-lock.  /*Invoicing DATE */ 
bill-date = htparam.fdate. 
from-date = bill-date. 
to-date = from-date.

FOR EACH hoteldpt NO-LOCK:
    CREATE t-hoteldpt.
    BUFFER-COPY hoteldpt TO t-hoteldpt.
END.

FOR EACH artikel WHERE artikel.departement = dept 
    AND (artikel.artart = 0 OR artart = 8) NO-LOCK BY artikel.bezeich:
    CREATE t-artikel.
    BUFFER-COPY artikel TO t-artikel.
END.

FOR EACH budget WHERE budget.departement = dept
    AND budget.datum GE from-date 
    AND budget.datum LE to-date BY budget.datum:
    CREATE t-budget.
    BUFFER-COPY budget TO t-budget.
END.

