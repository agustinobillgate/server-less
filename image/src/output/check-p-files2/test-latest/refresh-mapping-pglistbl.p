DEFINE TEMP-TABLE t-queasy LIKE queasy.

DEFINE INPUT PARAMETER pg-number AS INT.
DEFINE INPUT PARAMETER pg-name AS CHAR.
DEFINE OUTPUT PARAMETER mess-str AS CHAR.

DEFINE VARIABLE count-i AS INTEGER.

DEF TEMP-TABLE t-hoteldpt LIKE hoteldpt.
FOR EACH hoteldpt NO-LOCK:
    CREATE t-hoteldpt.
    BUFFER-COPY hoteldpt TO t-hoteldpt.
END.

RUN create-t-queasy.

FOR EACH t-queasy:
    FIND FIRST queasy WHERE queasy.KEY EQ 224 
        AND queasy.number1 EQ pg-number 
        AND queasy.number2 EQ t-queasy.number2
        AND queasy.char1 EQ t-queasy.char1 NO-LOCK NO-ERROR.
    IF NOT AVAILABLE queasy THEN
    DO:
        CREATE queasy.
        BUFFER-COPY t-queasy TO queasy.
        count-i = 1.        
    END.
    FIND CURRENT queasy.
END.
IF count-i EQ 1 THEN mess-str = "Update Payment Gateway Article Done".
ELSE mess-str = "No New Article Found".

/************************************* PROCEDURE *************************************/
PROCEDURE create-t-queasy:
    FOR EACH t-hoteldpt NO-LOCK BY t-hoteldpt.num:
        IF pg-number EQ 1 THEN
        DO:    
            CREATE t-queasy.
            ASSIGN
            t-queasy.KEY     = 224
            t-queasy.number1 = pg-number
            t-queasy.number2 = t-hoteldpt.num
            t-queasy.char1   = "1-QRIS"
            t-queasy.char2   = "4-Digital Payment"
            t-queasy.logi1   = NO
            t-queasy.betriebsnr = 999.
            CREATE t-queasy.
            ASSIGN
            t-queasy.KEY     = 224
            t-queasy.number1 = pg-number
            t-queasy.number2 = t-hoteldpt.num
            t-queasy.char1   = "15-Debit/Credit Card Payment"
            t-queasy.char2   = "1-Debit/Credit Card"
            t-queasy.logi1   = NO
            t-queasy.betriebsnr = 999.
            CREATE t-queasy.
            ASSIGN
            t-queasy.KEY     = 224
            t-queasy.number1 = pg-number
            t-queasy.number2 = t-hoteldpt.num
            t-queasy.char1   = "16-Credit Card Authorization"
            t-queasy.char2   = "2-Credit Card Authorization"
            t-queasy.logi1   = NO
            t-queasy.betriebsnr = 999.
            CREATE t-queasy.
            ASSIGN
            t-queasy.KEY     = 224
            t-queasy.number1 = pg-number
            t-queasy.number2 = t-hoteldpt.num
            t-queasy.char1   = "22-Sinarmas VA"
            t-queasy.char2   = "3-Virtual Account"
            t-queasy.logi1   = NO
            t-queasy.betriebsnr = 999.
            CREATE t-queasy.
            ASSIGN
            t-queasy.KEY     = 224
            t-queasy.number1 = pg-number
            t-queasy.number2 = t-hoteldpt.num
            t-queasy.char1   = "29-BCA VA"
            t-queasy.char2   = "3-Virtual Account"
            t-queasy.logi1   = NO
            t-queasy.betriebsnr = 999.
            CREATE t-queasy.
            ASSIGN
            t-queasy.KEY     = 224
            t-queasy.number1 = pg-number
            t-queasy.number2 = t-hoteldpt.num
            t-queasy.char1   = "32-CIMB VA"
            t-queasy.char2   = "3-Virtual Account"
            t-queasy.logi1   = NO
            t-queasy.betriebsnr = 999.
            CREATE t-queasy.
            ASSIGN
            t-queasy.KEY     = 224
            t-queasy.number1 = pg-number
            t-queasy.number2 = t-hoteldpt.num
            t-queasy.char1   = "33-Danamon VA"
            t-queasy.char2   = "3-Virtual Account"
            t-queasy.logi1   = NO
            t-queasy.betriebsnr = 999.
            CREATE t-queasy.
            ASSIGN
            t-queasy.KEY     = 224
            t-queasy.number1 = pg-number
            t-queasy.number2 = t-hoteldpt.num
            t-queasy.char1   = "34-BRI VA"
            t-queasy.char2   = "3-Virtual Account"
            t-queasy.logi1   = NO
            t-queasy.betriebsnr = 999.
            CREATE t-queasy.
            ASSIGN
            t-queasy.KEY     = 224
            t-queasy.number1 = pg-number
            t-queasy.number2 = t-hoteldpt.num
            t-queasy.char1   = "36-Permata VA"
            t-queasy.char2   = "3-Virtual Account"
            t-queasy.logi1   = NO
            t-queasy.betriebsnr = 999.            
            CREATE t-queasy.
            ASSIGN
            t-queasy.KEY     = 224
            t-queasy.number1 = pg-number
            t-queasy.number2 = t-hoteldpt.num
            t-queasy.char1   = "38-BNI VA"
            t-queasy.char2   = "3-Virtual Account"
            t-queasy.logi1   = NO
            t-queasy.betriebsnr = 999.
            CREATE t-queasy.
            ASSIGN
            t-queasy.KEY     = 224
            t-queasy.number1 = pg-number
            t-queasy.number2 = t-hoteldpt.num
            t-queasy.char1   = "41-Mandiri VA"
            t-queasy.char2   = "3-Virtual Account"
            t-queasy.logi1   = NO
            t-queasy.betriebsnr = 999.
            CREATE t-queasy.
            ASSIGN
            t-queasy.KEY     = 224
            t-queasy.number1 = pg-number
            t-queasy.number2 = t-hoteldpt.num
            t-queasy.char1   = "42-QNB VA"
            t-queasy.char2   = "3-Virtual Account"
            t-queasy.logi1   = NO
            t-queasy.betriebsnr = 999.
            CREATE t-queasy.
            ASSIGN
            t-queasy.KEY     = 224
            t-queasy.number1 = pg-number
            t-queasy.number2 = t-hoteldpt.num
            t-queasy.char1   = "43-BTN VA"
            t-queasy.char2   = "3-Virtual Account"
            t-queasy.logi1   = NO
            t-queasy.betriebsnr = 999.
            CREATE t-queasy.
            ASSIGN
            t-queasy.KEY     = 224
            t-queasy.number1 = pg-number
            t-queasy.number2 = t-hoteldpt.num
            t-queasy.char1   = "44-Maybank VA"
            t-queasy.char2   = "3-Virtual Account"
            t-queasy.logi1   = NO
            t-queasy.betriebsnr = 999.
            CREATE t-queasy.
            ASSIGN
            t-queasy.KEY     = 224
            t-queasy.number1 = pg-number
            t-queasy.number2 = t-hoteldpt.num
            t-queasy.char1   = "47-Arta Jasa VA"
            t-queasy.char2   = "3-Virtual Account"
            t-queasy.logi1   = NO
            t-queasy.betriebsnr = 999.
            CREATE t-queasy.
            ASSIGN
            t-queasy.KEY     = 224
            t-queasy.number1 = pg-number
            t-queasy.number2 = t-hoteldpt.num
            t-queasy.char1   = "50-LinkAja!"
            t-queasy.char2   = "4-Digital Payment"
            t-queasy.logi1   = NO
            t-queasy.betriebsnr = 999.
            CREATE t-queasy.
            ASSIGN
            t-queasy.KEY     = 224
            t-queasy.number1 = pg-number
            t-queasy.number2 = t-hoteldpt.num
            t-queasy.char1   = "51-Jenius Pay"
            t-queasy.char2   = "4-Digital Payment"
            t-queasy.logi1   = NO
            t-queasy.betriebsnr = 999.
            CREATE t-queasy.
            ASSIGN
            t-queasy.KEY     = 224
            t-queasy.number1 = pg-number
            t-queasy.number2 = t-hoteldpt.num
            t-queasy.char1   = "53-OVO"
            t-queasy.char2   = "4-Digital Payment"
            t-queasy.logi1   = NO
            t-queasy.betriebsnr = 999.
        END.
        ELSE IF pg-number EQ 2 THEN
        DO:
            CREATE t-queasy.
            ASSIGN
            t-queasy.KEY     = 224
            t-queasy.number1 = pg-number
            t-queasy.number2 = t-hoteldpt.num
            t-queasy.char1   = "1-CREDIT_CARD"
            t-queasy.char2   = "1-Debit/Credit Card"
            t-queasy.logi1   = NO
            t-queasy.betriebsnr = 999.
            CREATE t-queasy.
            ASSIGN
            t-queasy.KEY     = 224
            t-queasy.number1 = pg-number
            t-queasy.number2 = t-hoteldpt.num
            t-queasy.char1   = "2-GOPAY"
            t-queasy.char2   = "2-Digital Payment"
            t-queasy.logi1   = NO
            t-queasy.betriebsnr = 999.
            CREATE t-queasy.
            ASSIGN
            t-queasy.KEY     = 224
            t-queasy.number1 = pg-number
            t-queasy.number2 = t-hoteldpt.num
            t-queasy.char1   = "3-QRIS"
            t-queasy.char2   = "2-Digital Payment"
            t-queasy.logi1   = NO
            t-queasy.betriebsnr = 999.
            CREATE t-queasy.
            ASSIGN
            t-queasy.KEY     = 224
            t-queasy.number1 = pg-number
            t-queasy.number2 = t-hoteldpt.num
            t-queasy.char1   = "4-SHOPEEPAY"
            t-queasy.char2   = "2-Digital Payment"
            t-queasy.logi1   = NO
            t-queasy.betriebsnr = 999.
            CREATE t-queasy.
            ASSIGN
            t-queasy.KEY     = 224
            t-queasy.number1 = pg-number
            t-queasy.number2 = t-hoteldpt.num
            t-queasy.char1   = "5-BANK_TRANSFER|PERMATA"
            t-queasy.char2   = "6-Bank Transfer"
            t-queasy.logi1   = NO
            t-queasy.betriebsnr = 999.
            CREATE t-queasy.
            ASSIGN
            t-queasy.KEY     = 224
            t-queasy.number1 = pg-number
            t-queasy.number2 = t-hoteldpt.num
            t-queasy.char1   = "6-BANK_TRANSFER|BCA"
            t-queasy.char2   = "6-Bank Transfer"
            t-queasy.logi1   = NO
            t-queasy.betriebsnr = 999.
            CREATE t-queasy.
            ASSIGN
            t-queasy.KEY     = 224
            t-queasy.number1 = pg-number
            t-queasy.number2 = t-hoteldpt.num
            t-queasy.char1   = "7-BANK_TRANSFER|BNI"
            t-queasy.char2   = "6-Bank Transfer"
            t-queasy.logi1   = NO
            t-queasy.betriebsnr = 999.
            CREATE t-queasy.
            ASSIGN
            t-queasy.KEY     = 224
            t-queasy.number1 = pg-number
            t-queasy.number2 = t-hoteldpt.num
            t-queasy.char1   = "8-BANK_TRANSFER|BRI"
            t-queasy.char2   = "6-Bank Transfer"
            t-queasy.logi1   = NO
            t-queasy.betriebsnr = 999.
            CREATE t-queasy.
            ASSIGN
            t-queasy.KEY     = 224
            t-queasy.number1 = pg-number
            t-queasy.number2 = t-hoteldpt.num
            t-queasy.char1   = "9-ECHANNEL"
            t-queasy.char2   = "3-Internet Banking"
            t-queasy.logi1   = NO
            t-queasy.betriebsnr = 999.
            CREATE t-queasy.
            ASSIGN
            t-queasy.KEY     = 224
            t-queasy.number1 = pg-number
            t-queasy.number2 = t-hoteldpt.num
            t-queasy.char1   = "10-BCA_KLIKPAY"
            t-queasy.char2   = "3-Internet Banking"
            t-queasy.logi1   = NO
            t-queasy.betriebsnr = 999.
            CREATE t-queasy.
            ASSIGN
            t-queasy.KEY     = 224
            t-queasy.number1 = pg-number
            t-queasy.number2 = t-hoteldpt.num
            t-queasy.char1   = "11-BCA_KLIKBCA"
            t-queasy.char2   = "3-Internet Banking"
            t-queasy.logi1   = NO
            t-queasy.betriebsnr = 999.
            CREATE t-queasy.
            ASSIGN
            t-queasy.KEY     = 224
            t-queasy.number1 = pg-number
            t-queasy.number2 = t-hoteldpt.num
            t-queasy.char1   = "12-CIMB_CLICKS"
            t-queasy.char2   = "3-Internet Banking"
            t-queasy.logi1   = NO
            t-queasy.betriebsnr = 999.
            CREATE t-queasy.
            ASSIGN
            t-queasy.KEY     = 224
            t-queasy.number1 = pg-number
            t-queasy.number2 = t-hoteldpt.num
            t-queasy.char1   = "13-DANAMON_ONLINE"
            t-queasy.char2   = "3-Internet Banking"
            t-queasy.logi1   = NO
            t-queasy.betriebsnr = 999.
            CREATE t-queasy.
            ASSIGN
            t-queasy.KEY     = 224
            t-queasy.number1 = pg-number
            t-queasy.number2 = t-hoteldpt.num
            t-queasy.char1   = "14-BRI_EPAY"
            t-queasy.char2   = "3-Internet Banking"
            t-queasy.logi1   = NO
            t-queasy.betriebsnr = 999.
            CREATE t-queasy.
            ASSIGN
            t-queasy.KEY     = 224
            t-queasy.number1 = pg-number
            t-queasy.number2 = t-hoteldpt.num
            t-queasy.char1   = "15-CSTORE|INDOMARET"
            t-queasy.char2   = "4-Other Payment"
            t-queasy.logi1   = NO
            t-queasy.betriebsnr = 999.
            CREATE t-queasy.
            ASSIGN
            t-queasy.KEY     = 224
            t-queasy.number1 = pg-number
            t-queasy.number2 = t-hoteldpt.num
            t-queasy.char1   = "16-CSTORE|ALFAMART"
            t-queasy.char2   = "4-Other Payment"
            t-queasy.logi1   = NO
            t-queasy.betriebsnr = 999.
            CREATE t-queasy.
            ASSIGN
            t-queasy.KEY     = 224
            t-queasy.number1 = pg-number
            t-queasy.number2 = t-hoteldpt.num
            t-queasy.char1   = "17-AKULAKU"
            t-queasy.char2   = "4-Other Payment"
            t-queasy.logi1   = NO
            t-queasy.betriebsnr = 999.
        END.
        ELSE IF pg-number EQ 3 THEN /*XENDIT*/
        DO:
            CREATE t-queasy.
            ASSIGN
            t-queasy.KEY        = 224
            t-queasy.number1    = pg-number
            t-queasy.number2    = t-hoteldpt.num
            t-queasy.char1      = "1-BRI"
            t-queasy.char2      = "1-BANK_TRANSFER" 
            t-queasy.logi1      = NO
            t-queasy.betriebsnr = 999.
            CREATE t-queasy.
            ASSIGN
            t-queasy.KEY        = 224
            t-queasy.number1    = pg-number
            t-queasy.number2    = t-hoteldpt.num
            t-queasy.char1      = "2-BNI"
            t-queasy.char2      = "1-BANK_TRANSFER" 
            t-queasy.logi1      = NO
            t-queasy.betriebsnr = 999.
            CREATE t-queasy.
            ASSIGN
            t-queasy.KEY        = 224
            t-queasy.number1    = pg-number
            t-queasy.number2    = t-hoteldpt.num
            t-queasy.char1      = "3-MANDIRI"
            t-queasy.char2      = "1-BANK_TRANSFER" 
            t-queasy.logi1      = NO
            t-queasy.betriebsnr = 999.
            CREATE t-queasy.
            ASSIGN
            t-queasy.KEY        = 224
            t-queasy.number1    = pg-number
            t-queasy.number2    = t-hoteldpt.num
            t-queasy.char1      = "4-PERMATA"
            t-queasy.char2      = "1-BANK_TRANSFER" 
            t-queasy.logi1      = NO
            t-queasy.betriebsnr = 999.
            CREATE t-queasy.
            ASSIGN
            t-queasy.KEY        = 224
            t-queasy.number1    = pg-number
            t-queasy.number2    = t-hoteldpt.num
            t-queasy.char1      = "5-BCA"
            t-queasy.char2      = "1-BANK_TRANSFER" 
            t-queasy.logi1      = NO
            t-queasy.betriebsnr = 999.
            CREATE t-queasy.
            ASSIGN
            t-queasy.KEY        = 224
            t-queasy.number1    = pg-number
            t-queasy.number2    = t-hoteldpt.num
            t-queasy.char1      = "1-SHOPEEPAY"
            t-queasy.char2      = "2-EWALLET" 
            t-queasy.logi1      = NO
            t-queasy.betriebsnr = 999.
            CREATE t-queasy.
            ASSIGN
            t-queasy.KEY        = 224
            t-queasy.number1    = pg-number
            t-queasy.number2    = t-hoteldpt.num
            t-queasy.char1      = "2-DANA"
            t-queasy.char2      = "2-EWALLET" 
            t-queasy.logi1      = NO
            t-queasy.betriebsnr = 999.
            CREATE t-queasy.
            ASSIGN
            t-queasy.KEY        = 224
            t-queasy.number1    = pg-number
            t-queasy.number2    = t-hoteldpt.num
            t-queasy.char1      = "3-OVO"
            t-queasy.char2      = "2-EWALLET" 
            t-queasy.logi1      = NO
            t-queasy.betriebsnr = 999.
            CREATE t-queasy.
            ASSIGN
            t-queasy.KEY        = 224
            t-queasy.number1    = pg-number
            t-queasy.number2    = t-hoteldpt.num
            t-queasy.char1      = "4-LINKAJA"
            t-queasy.char2      = "2-EWALLET" 
            t-queasy.logi1      = NO
            t-queasy.betriebsnr = 999.
            CREATE t-queasy.
            ASSIGN
            t-queasy.KEY        = 224
            t-queasy.number1    = pg-number
            t-queasy.number2    = t-hoteldpt.num
            t-queasy.char1      = "1-CREDIT_CARD"
            t-queasy.char2      = "3-CREDIT_CARD" 
            t-queasy.logi1      = NO
            t-queasy.betriebsnr = 999.
            CREATE t-queasy.
            ASSIGN
            t-queasy.KEY        = 224
            t-queasy.number1    = pg-number
            t-queasy.number2    = t-hoteldpt.num
            t-queasy.char1      = "1-QRIS"
            t-queasy.char2      = "4-DIGITAL PAYMENT" 
            t-queasy.logi1      = NO
            t-queasy.betriebsnr = 999.
        END.
    END.
END.


