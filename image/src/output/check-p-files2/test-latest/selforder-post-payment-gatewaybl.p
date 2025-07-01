DEFINE INPUT PARAMETER outletNo AS INT.
DEFINE INPUT PARAMETER billNo AS INT.
DEFINE INPUT PARAMETER paymentString AS CHAR.
DEFINE INPUT PARAMETER session-parameter AS CHAR.

DEFINE OUTPUT PARAMETER result-message AS CHAR NO-UNDO.

DEF VAR mestoken         AS CHAR.
DEF VAR meskeyword       AS CHAR.
DEF VAR mesvalue         AS CHAR.
DEF VAR loop-i           AS INT.
DEF VAR payment-type     AS CHAR.
DEF VAR found-flag       AS LOGICAL.
DEF VAR do-it            AS LOGICAL.
DEF VAR paymentcode      AS INT.
DEF VAR bankName         AS CHAR.
DEF VAR noRef            AS CHAR.
DEF VAR resultMsg        AS CHAR.
DEF VAR ccNumber         AS CHAR.
DEF VAR amount           AS CHAR.
DEF VAR transdat         AS CHAR.
DEF VAR transid-merchant AS CHAR.

IF paymentString EQ ? THEN paymentString = "".

IF paymentString NE "" THEN
DO:
    do-it = NO.
    payment-type = ENTRY(1,paymentString,";").
    paymentString = SUBSTRING(paymentString,6).
    CASE payment-type:
        WHEN "DOKU" THEN
        DO:
            paymentcode = 1.
            do-it = YES.
            DO loop-i = 1 TO NUM-ENTRIES(paymentString,";"):
                mestoken   = ENTRY(loop-i, paymentString,";").
                meskeyword = ENTRY(1,mestoken,"=").
                mesvalue   = ENTRY(2,mestoken,"=").
        
                CASE meskeyword:
                    WHEN "BANK"            THEN bankName  = mesvalue.
                    WHEN "RESULTMSG"       THEN resultMsg = mesvalue.
                    WHEN "MCN"             THEN ccNumber  = mesvalue.
                    WHEN "AMOUNT"          THEN amount    = mesvalue.
                    WHEN "TRANSIDMERCHANT" THEN transid-merchant  = mesvalue.
                    WHEN "PAYMENTDATETIME" THEN transdat  = mesvalue.
                END CASE.
            END.
        END.
        WHEN "QRIS" THEN
        DO:
            paymentcode = 2.
            do-it = YES.
            DO loop-i = 1 TO NUM-ENTRIES(paymentString,";"):
                mestoken   = ENTRY(loop-i, paymentString,";").
                meskeyword = ENTRY(1,mestoken,"=").
                mesvalue   = ENTRY(2,mestoken,"=").
        
                CASE meskeyword:
                    WHEN "DPMALLID"        THEN bankName  = mesvalue.
                    WHEN "RESULTMSG"       THEN resultMsg = mesvalue.
                    WHEN "CLIENTID"        THEN ccNumber  = mesvalue.
                    WHEN "AMOUNT"          THEN amount    = mesvalue.
                    WHEN "TRANSIDMERCHANT"   THEN transid-merchant  = mesvalue.
                    WHEN "TRANSACTIONDATETIME" THEN transdat  = mesvalue.
                END CASE.
            END.
        END.
    END CASE.

    IF do-it THEN
    DO:
        FIND FIRST queasy WHERE queasy.KEY EQ 223
        AND queasy.number1 EQ outletNo AND queasy.char3 EQ session-parameter EXCLUSIVE-LOCK NO-ERROR.
        IF AVAILABLE queasy THEN
        DO:
            ASSIGN
            queasy.char1 = resultMsg
            queasy.char2 = transid-merchant + "|" + ENTRY(2,queasy.char2,"|")
            queasy.char3 = session-parameter
            .
        END.
        ELSE
        DO:
            CREATE queasy.
            ASSIGN 
            queasy.KEY     = 223
            queasy.number1 = outletNo
            queasy.number2 = billNo
            queasy.number3 = paymentcode
            queasy.char1   = resultMsg
            queasy.char2   = transid-merchant
            queasy.char3   = session-parameter
            queasy.date1   = TODAY
            .
        END.
        result-message = "0 - Update Payment Success!".
    END.
    ELSE
    DO:
        result-message = "1 - Update Payment FAILED! check your paymentString.".
    END.  
END.
ELSE
DO:
    result-message = "2 - paymentString cannot be empty string.".
END.
