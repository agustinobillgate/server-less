DEFINE INPUT PARAMETER post-tischnr AS INTEGER.
DEFINE INPUT PARAMETER post-curr-dept AS INTEGER.
DEFINE OUTPUT PARAMETER actv-flag AS LOGICAL INITIAL NO.

DEFINE VARIABLE pay-flag AS LOGICAL.

FIND FIRST h-bill WHERE h-bill.tischnr EQ post-tischnr
    AND h-bill.departement EQ post-curr-dept
    AND h-bill.flag EQ 0 
    AND h-bill.saldo EQ 0 NO-LOCK NO-ERROR.
IF AVAILABLE h-bill THEN
DO:
    FOR EACH h-bill-line WHERE h-bill-line.rechnr EQ h-bill.rechnr
        AND h-bill-line.departement EQ h-bill.departement NO-LOCK,
        FIRST h-artikel WHERE h-artikel.artnr EQ h-bill-line.artnr
        AND h-artikel.departement EQ h-bill-line.departement
        AND h-artikel.artart NE 0 NO-LOCK:
        
        pay-flag = YES.
        LEAVE.
    END.
    IF pay-flag THEN actv-flag = YES.
END.
