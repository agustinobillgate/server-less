
DEFINE INPUT PARAMETER bill-date     AS DATE    NO-UNDO.
DEFINE OUTPUT PARAMETER avail-deduct AS LOGICAL NO-UNDO INIT NO.


FIND FIRST l-op WHERE l-op.datum = bill-date
    AND l-op.op-art = 3
    AND (SUBSTR(l-op.lscheinnr,1,3)) = "SAD"
    AND l-op.loeschflag LE 1
    AND l-op.anzahl NE 0 NO-LOCK NO-ERROR.
IF AVAILABLE l-op THEN ASSIGN avail-deduct = YES.
