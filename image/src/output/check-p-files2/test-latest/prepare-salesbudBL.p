
DEFINE TEMP-TABLE t-bediener LIKE bediener.
DEFINE TEMP-TABLE t-salesbud LIKE salesbud
    FIELD rec-id AS INT.

DEF OUTPUT PARAMETER bill-date AS DATE.
DEF OUTPUT PARAMETER from-date AS DATE.
DEF OUTPUT PARAMETER TABLE FOR t-bediener.
DEF OUTPUT PARAMETER TABLE FOR t-salesbud.

FIND FIRST htparam WHERE paramnr = 110 no-lock.  /*Invoicing DATE */ 
bill-date = htparam.fdate. 
from-date = DATE(month(bill-date), 1, year(bill-date)). 

FIND FIRST htparam WHERE paramnr = 547 NO-LOCK.
FOR EACH bediener WHERE bediener.user-group = htparam.finteger
    NO-LOCK BY bediener.username:
    CREATE t-bediener.
    BUFFER-COPY bediener TO t-bediener.
END.

FOR EACH salesbud:
    CREATE t-salesbud.
    BUFFER-COPY salesbud TO t-salesbud.
    ASSIGN t-salesbud.rec-id = RECID(salesbud).
END.
