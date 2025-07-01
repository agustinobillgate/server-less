DEFINE TEMP-TABLE code-list
    FIELD code-num  AS INTEGER
    FIELD img-name  AS CHARACTER
    FIELD code-str  AS CHARACTER
    FIELD code-type AS INTEGER
    FIELD type-name AS CHARACTER
    .

DEFINE INPUT PARAMETER cashless-code    AS CHARACTER.
DEFINE INPUT PARAMETER type-code        AS INTEGER.
DEFINE OUTPUT PARAMETER ok-flag         AS LOGICAL INITIAL NO.
DEFINE OUTPUT PARAMETER TABLE FOR code-list.

DEFINE VARIABLE count-j AS INTEGER NO-UNDO.

DEFINE BUFFER queasy248 FOR queasy.

count-j = 0.
FOR EACH queasy248 WHERE queasy248.KEY EQ 248 NO-LOCK BY queasy248.number1 DESC:
    count-j = queasy248.number1 + 1.
    LEAVE.
END.

FIND FIRST queasy WHERE queasy.KEY EQ 248
    AND queasy.char2 EQ cashless-code NO-LOCK NO-ERROR.
IF AVAILABLE queasy THEN
DO:
    ok-flag = NO.
END.
ELSE
DO:
    CREATE queasy.
    ASSIGN
        queasy.KEY      = 248
        queasy.number1  = count-j
        queasy.number2  = type-code   /*Type Barcode / QR Code*/
        queasy.char1    = "C:\e1-vhp\Zint\BarcodeData\NSCashless" + STRING(count-j, "999") + ".png". /*Image Name*/
        queasy.char2    = TRIM(cashless-code)    /*Barcode / QR Code*/
        .
    FIND CURRENT queasy NO-LOCK.
    ok-flag = YES.
END.

FOR EACH queasy WHERE queasy.KEY EQ 248 NO-LOCK BY queasy.number1 DESC:
    CREATE code-list.
    ASSIGN
        code-list.code-num  = queasy.number1
        code-list.img-name  = queasy.char1
        code-list.code-str  = queasy.char2  
        code-list.code-type = queasy.number2  
        .

    IF queasy.number2 EQ 1 THEN code-list.type-name = "Barcode".
    ELSE code-list.type-name = "QR Code".
END.
