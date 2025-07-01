DEFINE INPUT PARAMETER session-parameter AS CHAR.
DEFINE INPUT PARAMETER trans-id-merchant AS CHAR.
DEFINE INPUT PARAMETER outletNo          AS INTEGER.
DEFINE INPUT PARAMETER payment-type      AS INTEGER.
DEFINE INPUT PARAMETER payment-channel   AS CHAR.
DEFINE OUTPUT PARAMETER trans-status     AS CHAR.
DEFINE OUTPUT PARAMETER result-message   AS CHAR.

IF trans-id-merchant EQ ? THEN trans-id-merchant = "".
IF payment-type EQ ? THEN payment-type = 0.
IF outletNo EQ ? THEN outletNo = 0.
IF session-parameter EQ ? THEN session-parameter = "".
IF payment-channel EQ ? THEN payment-channel = "".

IF trans-id-merchant EQ "" THEN
DO:
    result-message = "1-Transaction Id Merchant can't be Null".
    RETURN.
END.

DEFINE VARIABLE paymentmethod AS CHAR.
DEFINE VARIABLE paymentcode   AS INT.

IF payment-type EQ 1 THEN 
    ASSIGN paymentmethod = "MIDTRANS"
           paymentcode   = 1.
ELSE IF payment-type EQ 2 THEN
    ASSIGN paymentmethod = "DOKU"
           paymentcode   = 2.
ELSE IF payment-type EQ 3 THEN
    ASSIGN paymentmethod = "QRIS"
           paymentcode   = 3.
ELSE IF payment-type EQ 4 THEN
    ASSIGN paymentmethod = "XENDIT"
           paymentcode   = 4.
ELSE
DO:
    result-message = "2-Wrong Case Type should be 1=MIDTRANS, 2=QRIS, 3=DOKU, 4=XENDIT".
    RETURN.
END.

IF session-parameter EQ "" THEN
DO:
    result-message = "3-sessionParameter can't be Null".
    RETURN.
END.

IF outletNo EQ 0 THEN
DO:
    result-message = "4-outletNo can't be set to 0".
    RETURN.
END.

IF payment-channel EQ "" THEN
DO:
    result-message = "5-paymentChannel can't be Null".
    RETURN.
END.

DEFINE BUFFER bqsy FOR queasy.

trans-status = "PENDING".
FIND FIRST queasy WHERE queasy.KEY EQ 223 
AND queasy.number1 EQ outletNo   
AND queasy.char3 EQ session-parameter NO-LOCK NO-ERROR.
IF AVAILABLE queasy THEN
DO:
    FIND CURRENT queasy EXCLUSIVE-LOCK.

    ASSIGN
    queasy.char1 = trans-status /*"PENDING"*/
    queasy.char2 = paymentmethod + "|" + payment-channel + "|" + trans-id-merchant
    queasy.date1 = TODAY.

    result-message = "0-Operation Success".
    trans-status   = queasy.char1 + " transID=" + queasy.char2.
    FIND CURRENT queasy.
    RELEASE queasy.
END.
ELSE
DO:
    FIND FIRST bqsy WHERE bqsy.KEY EQ 223 
    AND bqsy.number1 EQ outletNo   
    AND bqsy.betriebsnr EQ INT(session-parameter) NO-LOCK NO-ERROR.
    IF AVAILABLE bqsy THEN
    DO:
        FIND CURRENT bqsy EXCLUSIVE-LOCK.
    
        ASSIGN
        bqsy.char1 = trans-status /*"PENDING"*/
        bqsy.char2 = paymentmethod + "|" + payment-channel + "|" + trans-id-merchant
        bqsy.date1 = TODAY.
    
        result-message = "0-Operation Success".
        trans-status   = bqsy.char1 + " transID=" + bqsy.char2.
        FIND CURRENT bqsy.
        RELEASE bqsy.
    END.
    ELSE
    DO:
        CREATE queasy.
        ASSIGN 
        queasy.KEY     = 223
        queasy.number1 = outletNo
        queasy.number3 = paymentcode
        queasy.char1   = trans-status /*"PENDING"*/
        queasy.char2   = paymentmethod + "|" + payment-channel + "|" + trans-id-merchant
        queasy.char3   = session-parameter
        queasy.date1   = TODAY.
    
        result-message = "0-Operation Success".
        trans-status   = queasy.char1 + " transID=" + queasy.char2.
    END.
END.

