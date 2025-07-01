
DEF INPUT PARAMETER lscheinnr AS CHAR.
DEF INPUT PARAMETER docu-nr AS CHAR.
DEF OUTPUT PARAMETER fl-code AS INT INIT 0 NO-UNDO.

FIND FIRST l-op WHERE l-op.op-art = 1 AND l-op.loeschflag LE 1
    AND l-op.lscheinnr = lscheinnr AND l-op.docu-nr NE docu-nr
    NO-LOCK NO-ERROR.
IF AVAILABLE l-op THEN
DO:
    fl-code = 1.
    RETURN NO-APPLY. 
END.
