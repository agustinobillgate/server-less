DEF TEMP-TABLE t-mast-art LIKE mast-art.

DEF INPUT PARAMETER case-type AS INTEGER NO-UNDO.
DEF INPUT PARAMETER int1      AS INTEGER NO-UNDO.
DEF INPUT PARAMETER int2      AS INTEGER NO-UNDO.
DEF INPUT PARAMETER int3      AS INTEGER NO-UNDO.
DEF INPUT PARAMETER int4      AS INTEGER NO-UNDO.
DEF INPUT PARAMETER int5      AS INTEGER NO-UNDO.

DEF OUTPUT PARAMETER TABLE FOR t-mast-art.

CASE case-type:
  WHEN 1 THEN
  FOR EACH mast-art WHERE mast-art.resnr = int1 NO-LOCK:
      CREATE t-mast-art.
      BUFFER-COPY mast-art TO t-mast-art.
  END.
  WHEN 2 THEN 
  DO:
      FIND FIRST mast-art WHERE mast-art.resnr = int1
        AND mast-art.departement = int2
        AND mast-art.artnr = int3 NO-LOCK NO-ERROR.
      IF AVAILABLE mast-art THEN
      DO:
          CREATE t-mast-art.
          BUFFER-COPY mast-art TO t-mast-art.
      END.
  END.

END CASE.
