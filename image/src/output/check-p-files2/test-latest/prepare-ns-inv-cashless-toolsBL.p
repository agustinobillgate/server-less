DEFINE TEMP-TABLE code-list
    FIELD code-num  AS INTEGER
    FIELD img-name  AS CHARACTER
    FIELD code-str  AS CHARACTER
    FIELD code-type AS INTEGER
    FIELD type-name AS CHARACTER
    .

DEFINE OUTPUT PARAMETER license-cashless AS LOGICAL INITIAL NO.
DEFINE OUTPUT PARAMETER TABLE FOR code-list.

FIND FIRST htparam WHERE htparam.paramnr EQ 1022
    AND htparam.bezeich NE "not used"
    AND htparam.flogical NO-LOCK NO-ERROR.
IF AVAILABLE htparam THEN license-cashless = YES.

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
