
DEF TEMP-TABLE t-mc-types          LIKE mc-types.

DEF INPUT  PARAMETER case-type  AS INTEGER NO-UNDO.
DEF INPUT  PARAMETER curr-i     AS INTEGER NO-UNDO.
DEF OUTPUT PARAMETER TABLE      FOR t-mc-types.

CASE case-type:
  WHEN 1 THEN 
  DO:
    FIND FIRST mc-types WHERE mc-types.nr = curr-i NO-LOCK NO-ERROR.
    IF AVAILABLE mc-types THEN
    DO:
      CREATE t-mc-types.
      BUFFER-COPY mc-types TO t-mc-types.
    END.
  END.
  WHEN 2 THEN
  FOR EACH mc-types WHERE mc-types.activeflag = YES NO-LOCK:
      CREATE t-mc-types.
      BUFFER-COPY mc-types TO t-mc-types.
  END.
END CASE.
