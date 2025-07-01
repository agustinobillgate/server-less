DEFINE TEMP-TABLE t-hoteldpt LIKE hoteldpt.

DEFINE OUTPUT PARAMETER bill-date AS DATE NO-UNDO.
DEFINE OUTPUT PARAMETER TABLE FOR t-hoteldpt.

RUN htpdate.p (110, OUTPUT bill-date).

FOR EACH hoteldpt WHERE hoteldpt.num GE 1 NO-LOCK:
    CREATE t-hoteldpt.
    BUFFER-COPY hoteldpt TO t-hoteldpt.
END.
