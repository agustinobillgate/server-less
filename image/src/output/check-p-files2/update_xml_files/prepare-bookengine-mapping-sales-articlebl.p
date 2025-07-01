/*Alder - BFEC0F - 05/11/2024*/

DEFINE TEMP-TABLE t-mapping-sales
    FIELD articleVHP    AS CHARACTER
    FIELD articleBE     AS CHARACTER
    FIELD descr         AS CHARACTER
    FIELD nr            AS INTEGER.

DEFINE OUTPUT PARAMETER TABLE FOR t-mapping-sales.
DEFINE INPUT PARAMETER bookengID AS INTEGER.

FOR EACH artikel 
    WHERE artikel.departement EQ 0 /*Front Office*/
    AND artikel.artart EQ 0 /*Sales Article*/
    NO-LOCK BY artikel.bezeich:

    CREATE t-mapping-sales.
    ASSIGN
        t-mapping-sales.articleVHP  = STRING(artikel.artnr)
        t-mapping-sales.descr       = artikel.bezeich
        t-mapping-sales.nr          = artikel.artnr.

    FIND FIRST queasy WHERE queasy.KEY EQ 323
        AND queasy.number1 EQ bookengID
        AND queasy.number2 EQ artikel.artnr
        NO-LOCK NO-ERROR.
    IF AVAILABLE queasy THEN
    DO:
        ASSIGN t-mapping-sales.articleBE = queasy.char2.
    END.
    ELSE
    DO:
        CREATE queasy.
        ASSIGN
            queasy.KEY      = 323
            queasy.number1  = bookengID
            queasy.number2  = artikel.artnr
            queasy.char1    = STRING(artikel.artnr).
    END.
END.
