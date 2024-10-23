
DEF INPUT PARAMETER lscheinnr AS CHAR.
DEF INPUT PARAMETER docu-nr AS CHAR.
DEF OUTPUT PARAMETER avail-l-op AS LOGICAL INIT NO.

FIND FIRST l-op WHERE l-op.op-art = 1 AND l-op.loeschflag LE 1
  AND l-op.lscheinnr = lscheinnr AND l-op.docu-nr NE docu-nr NO-LOCK NO-ERROR.
IF AVAILABLE l-op THEN avail-l-op = YES.
