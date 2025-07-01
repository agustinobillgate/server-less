DEF BUFFER l-op1    FOR l-op.

DEF INPUT PARAMETER lscheinnr AS CHAR.
DEF OUTPUT PARAMETER err-code AS INT INIT 0.

FIND FIRST l-op1 WHERE l-op1.op-art = 1 AND l-op1.loeschflag LE 1
AND l-op1.lscheinnr = lscheinnr NO-LOCK NO-ERROR.
IF AVAILABLE l-op1 THEN
DO:
    err-code = 1.
    RETURN NO-APPLY. 
END.
