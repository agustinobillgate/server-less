DEFINE TEMP-TABLE t-h-bill LIKE h-bill
    FIELD rec-id AS INT.

DEFINE INPUT  PARAMETER rechnr AS INTEGER NO-UNDO.
DEFINE INPUT  PARAMETER dept   AS INTEGER NO-UNDO.
DEFINE OUTPUT PARAMETER amount AS DECIMAL NO-UNDO.

FOR EACH h-bill WHERE h-bill.rechnr EQ rechnr 
    AND h-bill.departement EQ dept NO-LOCK:
    CREATE t-h-bill.
    BUFFER-COPY h-bill TO t-h-bill.
END.
FIND FIRST t-h-bill NO-LOCK NO-ERROR.
IF AVAILABLE t-h-bill THEN
DO:
    ASSIGN 
        amount = t-h-bill.saldo.
END.