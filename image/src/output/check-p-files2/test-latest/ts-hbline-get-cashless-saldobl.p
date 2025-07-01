
DEFINE INPUT PARAMETER cashless-code AS CHARACTER.
DEFINE OUTPUT PARAMETER cashless-saldo AS DECIMAL.
DEFINE OUTPUT PARAMETER ok-flag AS LOGICAL INITIAL NO.

DEFINE VARIABLE str-code AS CHARACTER NO-UNDO.

str-code = TRIM(cashless-code).

IF str-code NE "" THEN
DO:
    FIND FIRST bill WHERE bill.flag EQ 0 AND bill.rechnr GT 0    
        AND bill.resnr EQ 0 AND bill.reslinnr EQ 1 
        AND bill.vesrdepot2 EQ str-code NO-LOCK NO-ERROR.
    IF AVAILABLE bill THEN
    DO:
        cashless-saldo = bill.saldo.
        ok-flag = YES.
    END.
END.
