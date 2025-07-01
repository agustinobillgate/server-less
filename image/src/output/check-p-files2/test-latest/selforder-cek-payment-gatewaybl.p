DEFINE INPUT PARAMETER session-parameter AS CHAR.
DEFINE INPUT PARAMETER outletNo          AS INTEGER.
DEFINE OUTPUT PARAMETER payment-status   AS CHAR.
DEFINE OUTPUT PARAMETER payment-type     AS CHAR.
DEFINE OUTPUT PARAMETER payment-date     AS DATE.
DEFINE OUTPUT PARAMETER trans-id-merchant AS CHAR.
DEFINE OUTPUT PARAMETER payment-channel AS CHAR.
DEFINE OUTPUT PARAMETER result-message   AS CHAR.

IF outletNo EQ ? THEN outletNo = 0.
IF session-parameter EQ ? THEN session-parameter = "".

IF session-parameter EQ "" THEN
DO:
    result-message = "1-sessionParameter can't be Null".
    RETURN.
END.
IF outletNo EQ 0 THEN
DO:
    result-message = "2-outletNo can't be set to 0".
    RETURN.
END.

RUN check-payment.

IF result-message EQ "1-Data Not FOund" THEN
DO:
    FIND FIRST queasy WHERE queasy.KEY EQ 223 
        AND queasy.number1 EQ outletNo 
        AND queasy.betriebsnr EQ INT(session-parameter) NO-LOCK NO-ERROR.
    IF AVAILABLE queasy THEN
    DO:
        payment-status = queasy.char1.
        IF queasy.number3 EQ 1 THEN payment-type = "MIDTRANS".
        ELSE IF queasy.number3 EQ 2 THEN payment-type = "DOKU".
        ELSE IF queasy.number3 EQ 3 THEN payment-type = "QRIS".
        ELSE IF queasy.number3 EQ 4 THEN payment-type = "XENDIT".

        payment-date = queasy.date1.

        IF NUM-ENTRIES(queasy.char2,"|") GT 2 THEN
        DO:
            payment-channel   = ENTRY(2,queasy.char2,"|").
            trans-id-merchant = ENTRY(3,queasy.char2,"|").
            payment-type      = ENTRY(1,queasy.char2,"|").
        END.
        ELSE trans-id-merchant = queasy.char2.

        result-message = "0-Operation Success".
    END.
    ELSE
    DO:
        result-message = "1-Data Not FOund".
    END.
END.


PROCEDURE check-payment:
    FIND FIRST queasy WHERE queasy.KEY EQ 223 
        AND queasy.number1 EQ outletNo 
        AND queasy.char3 EQ session-parameter NO-LOCK NO-ERROR.
    IF AVAILABLE queasy THEN
    DO:
        payment-status = queasy.char1.
        IF queasy.number3 EQ 1 THEN payment-type = "MIDTRANS".
        ELSE IF queasy.number3 EQ 2 THEN payment-type = "DOKU".
        ELSE IF queasy.number3 EQ 3 THEN payment-type = "QRIS".
        ELSE IF queasy.number3 EQ 4 THEN payment-type = "XENDIT".

        payment-date = queasy.date1.

        IF NUM-ENTRIES(queasy.char2,"|") GT 2 THEN
        DO:
            payment-channel   = ENTRY(2,queasy.char2,"|").
            trans-id-merchant = ENTRY(3,queasy.char2,"|").
            payment-type      = ENTRY(1,queasy.char2,"|").
        END.
        ELSE trans-id-merchant = queasy.char2.

        result-message = "0-Operation Success".
    END.
    ELSE
    DO:
        result-message = "1-Data Not FOund".
    END.
END.


