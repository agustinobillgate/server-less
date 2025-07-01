DEFINE INPUT PARAMETER case-mode AS INTEGER.
DEFINE INPUT PARAMETER rec-id AS INTEGER.
DEFINE INPUT PARAMETER bill-no AS INTEGER.
DEFINE INPUT PARAMETER curr-tableno AS INTEGER.
DEFINE INPUT PARAMETER dept-no AS INTEGER.
DEFINE OUTPUT PARAMETER error-code AS INTEGER INITIAL 0.
DEFINE OUTPUT PARAMETER table-no AS INTEGER INITIAL 0.

DEFINE BUFFER buff-hbill FOR h-bill.
DEFINE BUFFER sp-bline   FOR h-bill-line.

IF case-mode EQ 1 THEN
DO:
    FIND FIRST h-bill WHERE h-bill.rechnr EQ bill-no
        AND h-bill.departement EQ dept-no
        AND h-bill.tischnr EQ curr-tableno NO-LOCK NO-ERROR.
    IF NOT AVAILABLE h-bill THEN
    DO:
        FIND FIRST buff-hbill WHERE RECID(buff-hbill) EQ rec-id NO-LOCK NO-ERROR.
        IF AVAILABLE buff-hbill THEN
        DO:
            table-no = buff-hbill.tischnr.
        END.
    
        error-code = 1.
        RETURN.
    END.
END.
ELSE IF case-mode EQ 2 THEN
DO:
    FIND FIRST sp-bline WHERE sp-bline.rechnr EQ bill-no
        AND sp-bline.departement EQ dept-no
        AND sp-bline.waehrungsnr GT 0 NO-LOCK NO-ERROR.
    IF AVAILABLE sp-bline THEN
    DO:
        error-code = 2.
        RETURN.
    END.
END.
ELSE IF case-mode EQ 3 THEN
DO:
    FIND FIRST h-bill WHERE RECID(h-bill) EQ rec-id NO-LOCK NO-ERROR.
    IF AVAILABLE h-bill THEN
    DO:
        IF h-bill.flag EQ 0 AND h-bill.saldo EQ 0 THEN
        DO:
            FIND FIRST h-bill-line WHERE h-bill-line.rechnr EQ h-bill.rechnr
                AND h-bill-line.departement EQ h-bill.departement
                AND h-bill-line.betrag EQ 0 NO-LOCK NO-ERROR.
            IF NOT AVAILABLE h-bill-line THEN 
            DO:
                error-code = 3.
                RETURN.
            END.
        END.
    END.
END.
