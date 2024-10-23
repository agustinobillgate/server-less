
DEF TEMP-TABLE t-hoteldpt LIKE hoteldpt.
DEF TEMP-TABLE t-kellner LIKE kellner
    FIELD rec-id AS INT.

DEF INPUT  PARAMETER curr-dept AS INT.
DEF INPUT  PARAMETER kname     AS CHAR.
DEF OUTPUT PARAMETER TABLE FOR t-hoteldpt.
DEF OUTPUT PARAMETER TABLE FOR t-kellner.

FOR EACH kellner:
    CREATE t-kellner.
    BUFFER-COPY kellner TO t-kellner.
    ASSIGN t-kellner.rec-id = RECID(kellner).
END.

FOR EACH hoteldpt:
    CREATE t-hoteldpt.
    BUFFER-COPY hoteldpt TO t-hoteldpt.
END.
