DEF TEMP-TABLE t-hoteldpt LIKE hoteldpt.

DEF INPUT  PARAMETER deptNo  AS INTEGER NO-UNDO.
DEF OUTPUT PARAMETER TABLE FOR t-hoteldpt.

FIND FIRST hoteldpt WHERE hoteldpt.num = deptNo NO-LOCK NO-ERROR.

IF AVAILABLE hoteldpt THEN
DO:
  CREATE t-hoteldpt.
  BUFFER-COPY hoteldpt TO t-hoteldpt.
END.
