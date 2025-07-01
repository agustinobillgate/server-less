DEFINE INPUT  PARAMETER rechnr    AS INTEGER NO-UNDO.
DEFINE INPUT  PARAMETER dept      AS INTEGER NO-UNDO.
DEFINE INPUT  PARAMETER saldo     AS INTEGER NO-UNDO.
DEFINE OUTPUT PARAMETER avail-new AS LOGICAL INITIAL NO NO-UNDO.

FIND FIRST h-bill WHERE h-bill.rechnr EQ rechnr 
    AND h-bill.departement EQ dept NO-LOCK NO-ERROR.
IF AVAILABLE h-bill THEN
DO:
    IF h-bill.saldo NE saldo THEN
        ASSIGN avail-new = YES.
    ELSE IF h-bill.saldo EQ saldo THEN 
        ASSIGN avail-new = NO.      
END.
