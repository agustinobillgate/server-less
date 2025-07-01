DEF TEMP-TABLE t-hoteldpt LIKE hoteldpt.

DEF OUTPUT PARAMETER TABLE  FOR t-hoteldpt.
FOR EACH hoteldpt NO-LOCK:
    CREATE t-hoteldpt.
    BUFFER-COPY hoteldpt TO t-hoteldpt.
END.
