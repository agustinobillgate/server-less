
DEFINE TEMP-TABLE t-hoteldpt  LIKE hoteldpt.

DEF OUTPUT PARAMETER from-date  AS DATE.
DEF OUTPUT PARAMETER TABLE FOR t-hoteldpt.

RUN htpdate.p (110, OUTPUT from-date).
FOR EACH hoteldpt NO-LOCK:
    CREATE t-hoteldpt.
    BUFFER-COPY hoteldpt TO t-hoteldpt.
END.
