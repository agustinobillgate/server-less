DEF TEMP-TABLE t-genlayout LIKE genlayout.

DEF INPUT PARAMETER keystr AS CHAR NO-UNDO.
DEF OUTPUT PARAMETER TABLE FOR t-genlayout.

FIND FIRST genlayout WHERE genlayout.KEY = keystr NO-LOCK NO-ERROR.
IF AVAILABLE genlayout THEN
DO:
  CREATE t-genlayout.
  BUFFER-COPY genlayout TO t-genlayout.
END.
