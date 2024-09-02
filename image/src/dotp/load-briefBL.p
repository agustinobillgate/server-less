DEF TEMP-TABLE t-brief LIKE brief.

DEF INPUT  PARAMETER briefNo AS INTEGER NO-UNDO.
DEF OUTPUT PARAMETER TABLE  FOR t-brief.
FOR EACH brief WHERE brief.briefkateg = briefNo NO-LOCK:
    CREATE t-brief.
    BUFFER-COPY brief TO t-brief.
END.
