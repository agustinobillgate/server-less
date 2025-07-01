DEF INPUT PARAMETER lscheinnr AS CHAR.
DEF INPUT PARAMETER docu-nr AS CHAR.
DEF OUTPUT PARAMETER avail-l-op AS LOGICAL.

avail-l-op = YES.

FIND FIRST l-op WHERE l-op.op-art = 1 AND l-op.loeschflag LE 1
  AND l-op.lscheinnr = lscheinnr /* AND l-op.docu-nr NE docu-nr */ NO-LOCK NO-ERROR.

IF AVAILABLE l-op THEN
  avail-l-op = NO.
ELSE
DO:
  FIND FIRST l-ophis WHERE l-ophis.op-art = 1
    AND l-ophis.lscheinnr = lscheinnr /* AND l-ophis.docu-nr NE docu-nr */ NO-LOCK NO-ERROR.

  IF AVAILABLE l-ophis THEN
    avail-l-op = NO.
END.
