
DEF TEMP-TABLE t-zimkateg LIKE zimkateg.
DEF TEMP-TABLE t-rmbudget LIKE rmbudget
    FIELD rec-id AS INT.

DEF OUTPUT PARAMETER price-decimal AS INT.
DEF OUTPUT PARAMETER p-110 AS DATE.
DEF OUTPUT PARAMETER TABLE FOR t-zimkateg.
DEF OUTPUT PARAMETER TABLE FOR t-rmbudget.

FIND FIRST htparam WHERE htparam.paramnr = 491 NO-LOCK. 
price-decimal = htparam.finteger. 
FIND FIRST htparam WHERE paramnr = 110 no-lock.  /*Invoicing DATE */ 
p-110 = htparam.fdate.

FOR EACH zimkateg NO-LOCK BY zimkateg.zikatnr:
    CREATE t-zimkateg.
    BUFFER-COPY zimkateg TO t-zimkateg.
END.

FOR EACH rmbudget:
    CREATE t-rmbudget.
    BUFFER-COPY rmbudget TO t-rmbudget.
    ASSIGN t-rmbudget.rec-id = RECID(rmbudget).
END.
