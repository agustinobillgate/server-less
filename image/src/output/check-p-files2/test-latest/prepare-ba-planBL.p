
DEF TEMP-TABLE t-bk-raum LIKE bk-raum.

DEF OUTPUT PARAMETER ci-date AS DATE.
DEF OUTPUT PARAMETER ba-dept AS INT.
DEF OUTPUT PARAMETER run-beowarning AS LOGICAL INIT NO.
DEF OUTPUT PARAMETER p-900   AS INT.
DEF OUTPUT PARAMETER TABLE FOR t-bk-raum.

FIND FIRST htparam WHERE htparam.paramnr = 87 NO-LOCK. 
ci-date = htparam.fdate. 

FIND FIRST htparam WHERE htparam.paramnr = 900 NO-LOCK. 
ba-dept = htparam.finteger. 

FOR EACH bk-raum NO-LOCK:
    CREATE t-bk-raum.
    BUFFER-COPY bk-raum TO t-bk-raum.
END.

FIND FIRST bk-reser WHERE bk-reser.datum = ci-date AND bk-reser.fakturiert = 1 NO-ERROR.
IF AVAILABLE bk-reser THEN run-beowarning = YES.

FIND FIRST htparam WHERE htparam.paramnr = 900 USE-INDEX paramnr_ix 
    NO-LOCK NO-ERROR.
IF AVAILABLE htparam THEN p-900 = htparam.finteger.
