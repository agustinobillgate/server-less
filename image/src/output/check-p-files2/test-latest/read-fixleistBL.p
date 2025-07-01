DEF TEMP-TABLE t-fixleist LIKE fixleist.

DEF INPUT PARAMETER case-type AS INTEGER NO-UNDO.
DEF INPUT PARAMETER resNo     AS INTEGER NO-UNDO.
DEF INPUT PARAMETER reslinNo  AS INTEGER NO-UNDO.
DEF INPUT PARAMETER fixNum    AS INTEGER NO-UNDO.

DEF OUTPUT PARAMETER TABLE FOR t-fixleist.

CASE case-type:
  WHEN 1 THEN
  FOR EACH fixleist WHERE fixleist.resnr = resNo
    AND fixleist.reslinnr = reslinNo 
    AND fixleist.number GE fixNum NO-LOCK:
    CREATE t-fixleist.
    BUFFER-COPY fixleist TO t-fixleist.
  END.
  WHEN 2 THEN .
END CASE.
