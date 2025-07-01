DEFINE INPUT PARAMETER zinr      AS CHAR    NO-UNDO.
DEFINE OUTPUT PARAMETER err-flag AS INTEGER NO-UNDO.

FIND FIRST res-line WHERE res-line.zinr = zinr 
    AND res-line.resstatus NE 8
    AND res-line.resstatus NE 9
    AND res-line.resstatus NE 12
    AND res-line.resstatus NE 99 NO-LOCK NO-ERROR.
IF AVAILABLE res-line THEN DO:
    ASSIGN err-flag = 1.
END.
