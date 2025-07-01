/*Alder - BFEC0F - 05/11/2024*/

DEFINE TEMP-TABLE t-mapping-sales
    FIELD articleVHP AS CHARACTER
    FIELD articleBE AS CHARACTER
    FIELD descr AS CHARACTER
    FIELD nr AS INTEGER.

DEFINE INPUT PARAMETER TABLE FOR t-mapping-sales.
DEFINE INPUT PARAMETER bookengID AS INTEGER.

MESSAGE bookengID VIEW-AS ALERT-BOX INFO.
FOR EACH t-mapping-sales NO-LOCK:
    FIND FIRST queasy WHERE queasy.KEY EQ 323
        AND queasy.number1 EQ bookengID
        AND queasy.number2 EQ t-mapping-sales.nr
        NO-ERROR.
    IF AVAILABLE queasy THEN
    DO:
        ASSIGN queasy.char2 = t-mapping-sales.articleBE.
    END.
    ELSE
    DO:
        CREATE queasy.
        ASSIGN
            queasy.KEY = 323
            queasy.number1 = bookengID
            queasy.number2 = t-mapping-sales.nr
            queasy.char1 = t-mapping-sales.articleVHP.
    END.
END.
