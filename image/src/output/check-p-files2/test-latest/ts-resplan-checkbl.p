
DEFINE INPUT PARAMETER v-key        AS INTEGER.
DEFINE INPUT PARAMETER s-recid      AS INTEGER.
DEFINE INPUT PARAMETER curr-dept    AS INTEGER.
DEFINE INPUT PARAMETER table-no     AS INTEGER.
DEFINE OUTPUT PARAMETER msg-str     AS CHARACTER INITIAL "".

DEFINE BUFFER queasy251 FOR queasy.

IF v-key EQ 1 THEN
DO:
    FIND FIRST h-bill WHERE h-bill.flag EQ 0
        AND h-bill.tischnr EQ table-no
        AND h-bill.departement EQ curr-dept NO-LOCK NO-ERROR.
    IF AVAILABLE h-bill THEN
    DO:
        IF h-bill.rechnr NE 0 THEN
        DO:
            FIND FIRST queasy251 WHERE queasy251.KEY EQ 251
                AND queasy251.number1 EQ INT(RECID(h-bill))
                AND queasy251.number2 EQ s-recid NO-LOCK NO-ERROR.
            IF AVAILABLE queasy251 THEN
            DO:            
                msg-str = "Bill already open for this table.".
                RETURN.    
            END.
        END.
    END.
END.
