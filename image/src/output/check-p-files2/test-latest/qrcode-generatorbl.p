DEFINE TEMP-TABLE code-list
    FIELD code-num  AS INTEGER
    FIELD img-name  AS CHARACTER
    FIELD code-str  AS CHARACTER
    FIELD code-type AS INTEGER
    .

DEFINE INPUT PARAMETER case-type AS INTEGER.
DEFINE INPUT PARAMETER TABLE FOR code-list.
DEFINE OUTPUT PARAMETER q248-count AS INTEGER INITIAL 1.
DEFINE OUTPUT PARAMETER msg-result AS CHARACTER.

DEFINE VARIABLE found-bill  AS LOGICAL INITIAL NO.
DEFINE VARIABLE bill-no     AS INTEGER NO-UNDO.
DEFINE VARIABLE count-j     AS INTEGER NO-UNDO.
DEFINE VARIABLE str-code    AS CHARACTER NO-UNDO.

DEFINE BUFFER queasy248 FOR queasy.
DEFINE BUFFER qns-cashless FOR queasy.

IF case-type EQ 1 THEN
DO:   
    FOR EACH queasy WHERE queasy.KEY EQ 248 NO-LOCK BY queasy.number1 DESC:
        q248-count = queasy.number1 + 1.
        LEAVE.
    END.
    /*
    FOR EACH bill WHERE bill.flag EQ 0 AND bill.rechnr GT 0
        AND bill.resnr EQ 0 AND bill.reslinnr EQ 1 
        AND bill.vesrdepot2 NE "" NO-LOCK,
        FIRST qns-cashless WHERE qns-cashless.KEY EQ 248
        AND qns-cashless.char2 EQ bill.vesrdepot2 NO-LOCK:
    
        found-bill = YES.
        bill-no = bill.rechnr.
        str-code = bill.vesrdepot2.
        LEAVE.
    END.
    IF found-bill THEN
    DO:
        msg-result = "Bar/QR Code Cashless Nonstay Guest Bill is active with:" + CHR(10) +
            "Bill No: " + STRING(bill-no) + "  -  " + "Code: " + str-code + "." + CHR(10) +
            "Generating New Bar/QR Code not possible.".
        RETURN.
    END.
    */
END.
ELSE
DO:
    /*
    FIND FIRST queasy WHERE queasy.KEY EQ 248 NO-LOCK NO-ERROR.
    IF AVAILABLE queasy THEN
    DO:
        FOR EACH queasy WHERE queasy.KEY EQ 248 NO-LOCK:
            FIND FIRST queasy248 WHERE RECID(queasy248) EQ RECID(queasy) EXCLUSIVE-LOCK NO-ERROR.
            IF AVAILABLE queasy248 THEN
            DO:
                DELETE queasy248.
                RELEASE queasy248.
            END.
        END.
    END.
    */
    count-j = 0.
    FOR EACH queasy WHERE queasy.KEY EQ 248 NO-LOCK BY queasy.number1 DESC:
        count-j = queasy.number1.
        LEAVE.
    END.

    FOR EACH code-list NO-LOCK BY code-list.code-num:
        count-j = count-j + 1.
        CREATE queasy.
        ASSIGN
            queasy.KEY      = 248
            queasy.number1  = count-j
            queasy.number2  = code-list.code-type   /*Type Barcode / QR Code*/
            queasy.char1    = code-list.img-name    /*Image Name*/
            queasy.char2    = code-list.code-str    /*Barcode / QR Code*/
            .
    END.
END.
