DEFINE TEMP-TABLE payment-gateway-list
    FIELD pg-art-no         AS INT FORMAT ">>>" LABEL "No"
    FIELD pg-art-name       AS CHARACTER FORMAT "x(35)" LABEL "PG Artikel Name"
    FIELD pg-grp-no         AS INT FORMAT ">>>" LABEL "Group No"
    FIELD pg-grp-name       AS CHARACTER FORMAT "x(35)" LABEL "PG Group Name"
    FIELD pg-art-activate   AS LOGICAL LABEL "Active"
    FIELD vhp-art-no        AS INT FORMAT ">>>" LABEL "VHP Article No"
    FIELD vhp-art-name      AS CHARACTER FORMAT "x(35)" LABEL "VHP Artikel Name" 
    FIELD vhp-art-dept      AS INT
    .

DEFINE TEMP-TABLE vhp-payment-list
    FIELD vhp-art-no         AS INT FORMAT ">>>" LABEL "No"
    FIELD vhp-art-name       AS CHARACTER FORMAT "x(35)" LABEL "VHP Artikel Name"
    .

DEF TEMP-TABLE t-hoteldpt LIKE hoteldpt.
FOR EACH hoteldpt NO-LOCK:
    CREATE t-hoteldpt.
    BUFFER-COPY hoteldpt TO t-hoteldpt.
END.

DEFINE INPUT PARAMETER case-type AS INT.
DEFINE INPUT PARAMETER load-type AS INT.
DEFINE INPUT PARAMETER pg-number AS INT.
DEFINE INPUT PARAMETER pg-name   AS CHAR.
DEFINE INPUT PARAMETER art-dept  AS INT.
DEFINE INPUT PARAMETER art-name  AS CHAR.
DEFINE OUTPUT PARAMETER TABLE FOR payment-gateway-list.
DEFINE OUTPUT PARAMETER TABLE FOR vhp-payment-list.

IF case-type EQ 1 THEN
DO:
    IF load-type EQ 1 THEN
    DO:
        FIND FIRST queasy WHERE queasy.KEY EQ 224 AND queasy.number1 EQ pg-number NO-LOCK NO-ERROR.
        IF NOT AVAILABLE queasy THEN
        DO:
            RUN create-queasy.
        END.
        FOR EACH queasy WHERE queasy.KEY EQ 224 AND queasy.number1 EQ pg-number NO-LOCK:
            CREATE payment-gateway-list.
            ASSIGN 
                payment-gateway-list.pg-art-no = INT(ENTRY(1,queasy.char1,"-"))
                payment-gateway-list.pg-art-name = ENTRY(2,queasy.char1,"-").

                IF queasy.number1 EQ 2 THEN
                DO:
                    payment-gateway-list.pg-grp-no = INT(ENTRY(1,queasy.char2,"-")).
                    payment-gateway-list.pg-grp-name = ENTRY(2,queasy.char2,"-").
                END.
                payment-gateway-list.pg-art-activate = queasy.logi1.
                IF NUM-ENTRIES(queasy.char3,"-") GE 2 THEN
                DO:
                    payment-gateway-list.vhp-art-no = INT(ENTRY(1,queasy.char3,"-")).
                    payment-gateway-list.vhp-art-name = ENTRY(2,queasy.char3,"-").
                END.
                payment-gateway-list.vhp-art-dept = queasy.number2
                .
        END.
    END.
    ELSE IF load-type EQ 2 THEN
    DO:
        IF art-dept EQ 0 THEN
        DO:
            FOR EACH artikel WHERE artikel.departement = art-dept 
                AND (artikel.artart = 2 OR artikel.artart = 5 OR artikel.artart = 6 
                OR artikel.artart = 7) AND artikel.activeflag = YES 
                NO-LOCK BY artikel.artnr:
                CREATE vhp-payment-list. 
                ASSIGN
                    vhp-payment-list.vhp-art-no   = artikel.artnr
                    vhp-payment-list.vhp-art-name = artikel.bezeich
                    .
            END.
        END.
        ELSE
        DO:
            FOR EACH h-artikel WHERE h-artikel.departement = art-dept 
                AND (h-artikel.artart = 2 OR h-artikel.artart = 5 OR h-artikel.artart = 6 
                OR h-artikel.artart = 7) AND h-artikel.activeflag = YES 
                NO-LOCK BY h-artikel.artnr:
                CREATE vhp-payment-list. 
                ASSIGN
                    vhp-payment-list.vhp-art-no   = h-artikel.artnr
                    vhp-payment-list.vhp-art-name = h-artikel.bezeich
                    .
            END.
        END.
    END.
END.
ELSE
DO:
    FOR EACH queasy WHERE queasy.KEY EQ 224 AND queasy.number1 EQ pg-number AND queasy.number2 EQ art-dept NO-LOCK:
        CREATE payment-gateway-list.
        ASSIGN 
            payment-gateway-list.pg-art-no = INT(ENTRY(1,queasy.char1,"-"))
            payment-gateway-list.pg-art-name = ENTRY(2,queasy.char1,"-").

            IF queasy.number1 EQ 2 THEN
            DO:
                payment-gateway-list.pg-grp-no = INT(ENTRY(1,queasy.char2,"-")).
                payment-gateway-list.pg-grp-name = ENTRY(2,queasy.char2,"-").
            END.
            payment-gateway-list.pg-art-activate = queasy.logi1.
            IF NUM-ENTRIES(queasy.char3,"-") GE 2 THEN
            DO:
                payment-gateway-list.vhp-art-no = INT(ENTRY(1,queasy.char3,"-")).
                payment-gateway-list.vhp-art-name = ENTRY(2,queasy.char3,"-").
            END.
            payment-gateway-list.vhp-art-dept = queasy.number2
            .
    END.
    IF art-dept EQ 0 THEN
    DO:
        FOR EACH artikel WHERE artikel.departement = art-dept 
            AND (artikel.artart = 2 OR artikel.artart = 5 OR artikel.artart = 6 
            OR artikel.artart = 7) AND artikel.activeflag = YES 
            NO-LOCK BY artikel.artnr:
            CREATE vhp-payment-list. 
            ASSIGN
                vhp-payment-list.vhp-art-no   = artikel.artnr
                vhp-payment-list.vhp-art-name = artikel.bezeich
                .
        END.
    END.
    ELSE
    DO:
        FOR EACH h-artikel WHERE h-artikel.departement = art-dept 
            AND (h-artikel.artart = 2 OR h-artikel.artart = 5 OR h-artikel.artart = 6 
            OR h-artikel.artart = 7) AND h-artikel.activeflag = YES 
            NO-LOCK BY h-artikel.artnr:
            CREATE vhp-payment-list. 
            ASSIGN
                vhp-payment-list.vhp-art-no   = h-artikel.artnr
                vhp-payment-list.vhp-art-name = h-artikel.bezeich
                .
        END.
    END.
END.

PROCEDURE create-queasy:
    FOR EACH t-hoteldpt NO-LOCK BY t-hoteldpt.num:
        IF pg-number EQ 1 THEN /*DOKU*/
        DO:    
            CREATE queasy.
            ASSIGN
            queasy.KEY     = 224
            queasy.number1 = pg-number
            queasy.number2 = t-hoteldpt.num
            queasy.char1   = "1-QRIS"
            queasy.char2   = "4-Digital Payment"
            queasy.logi1   = NO
            queasy.betriebsnr = 999.
            CREATE queasy.
            ASSIGN
            queasy.KEY     = 224
            queasy.number1 = pg-number
            queasy.number2 = t-hoteldpt.num
            queasy.char1   = "15-Debit/Credit Card Payment"
            queasy.char2   = "1-Debit/Credit Card"
            queasy.logi1   = NO
            queasy.betriebsnr = 999.
            CREATE queasy.
            ASSIGN
            queasy.KEY     = 224
            queasy.number1 = pg-number
            queasy.number2 = t-hoteldpt.num
            queasy.char1   = "16-Credit Card Authorization"
            queasy.char2   = "2-Credit Card Authorization"
            queasy.logi1   = NO
            queasy.betriebsnr = 999.
            CREATE queasy.
            ASSIGN
            queasy.KEY     = 224
            queasy.number1 = pg-number
            queasy.number2 = t-hoteldpt.num
            queasy.char1   = "22-Sinarmas VA"
            queasy.char2   = "3-Virtual Account"
            queasy.logi1   = NO
            queasy.betriebsnr = 999.
            CREATE queasy.
            ASSIGN
            queasy.KEY     = 224
            queasy.number1 = pg-number
            queasy.number2 = t-hoteldpt.num
            queasy.char1   = "29-BCA VA"
            queasy.char2   = "3-Virtual Account"
            queasy.logi1   = NO
            queasy.betriebsnr = 999.
            CREATE queasy.
            ASSIGN
            queasy.KEY     = 224
            queasy.number1 = pg-number
            queasy.number2 = t-hoteldpt.num
            queasy.char1   = "32-CIMB VA"
            queasy.char2   = "3-Virtual Account"
            queasy.logi1   = NO
            queasy.betriebsnr = 999.
            CREATE queasy.
            ASSIGN
            queasy.KEY     = 224
            queasy.number1 = pg-number
            queasy.number2 = t-hoteldpt.num
            queasy.char1   = "33-Danamon VA"
            queasy.char2   = "3-Virtual Account"
            queasy.logi1   = NO
            queasy.betriebsnr = 999.
            CREATE queasy.
            ASSIGN
            queasy.KEY     = 224
            queasy.number1 = pg-number
            queasy.number2 = t-hoteldpt.num
            queasy.char1   = "34-BRI VA"
            queasy.char2   = "3-Virtual Account"
            queasy.logi1   = NO
            queasy.betriebsnr = 999.
            CREATE queasy.
            ASSIGN
            queasy.KEY     = 224
            queasy.number1 = pg-number
            queasy.number2 = t-hoteldpt.num
            queasy.char1   = "36-Permata VA"
            queasy.char2   = "3-Virtual Account"
            queasy.logi1   = NO
            queasy.betriebsnr = 999.            
            CREATE queasy.
            ASSIGN
            queasy.KEY     = 224
            queasy.number1 = pg-number
            queasy.number2 = t-hoteldpt.num
            queasy.char1   = "38-BNI VA"
            queasy.char2   = "3-Virtual Account"
            queasy.logi1   = NO
            queasy.betriebsnr = 999.
            CREATE queasy.
            ASSIGN
            queasy.KEY     = 224
            queasy.number1 = pg-number
            queasy.number2 = t-hoteldpt.num
            queasy.char1   = "41-Mandiri VA"
            queasy.char2   = "3-Virtual Account"
            queasy.logi1   = NO
            queasy.betriebsnr = 999.
            CREATE queasy.
            ASSIGN
            queasy.KEY     = 224
            queasy.number1 = pg-number
            queasy.number2 = t-hoteldpt.num
            queasy.char1   = "42-QNB VA"
            queasy.char2   = "3-Virtual Account"
            queasy.logi1   = NO
            queasy.betriebsnr = 999.
            CREATE queasy.
            ASSIGN
            queasy.KEY     = 224
            queasy.number1 = pg-number
            queasy.number2 = t-hoteldpt.num
            queasy.char1   = "43-BTN VA"
            queasy.char2   = "3-Virtual Account"
            queasy.logi1   = NO
            queasy.betriebsnr = 999.
            CREATE queasy.
            ASSIGN
            queasy.KEY     = 224
            queasy.number1 = pg-number
            queasy.number2 = t-hoteldpt.num
            queasy.char1   = "44-Maybank VA"
            queasy.char2   = "3-Virtual Account"
            queasy.logi1   = NO
            queasy.betriebsnr = 999.
            CREATE queasy.
            ASSIGN
            queasy.KEY     = 224
            queasy.number1 = pg-number
            queasy.number2 = t-hoteldpt.num
            queasy.char1   = "47-Arta Jasa VA"
            queasy.char2   = "3-Virtual Account"
            queasy.logi1   = NO
            queasy.betriebsnr = 999.
            CREATE queasy.
            ASSIGN
            queasy.KEY     = 224
            queasy.number1 = pg-number
            queasy.number2 = t-hoteldpt.num
            queasy.char1   = "50-LinkAja!"
            queasy.char2   = "4-Digital Payment"
            queasy.logi1   = NO
            queasy.betriebsnr = 999.
            CREATE queasy.
            ASSIGN
            queasy.KEY     = 224
            queasy.number1 = pg-number
            queasy.number2 = t-hoteldpt.num
            queasy.char1   = "51-Jenius Pay"
            queasy.char2   = "4-Digital Payment"
            queasy.logi1   = NO
            queasy.betriebsnr = 999.
            CREATE queasy.
            ASSIGN
            queasy.KEY     = 224
            queasy.number1 = pg-number
            queasy.number2 = t-hoteldpt.num
            queasy.char1   = "53-OVO"
            queasy.char2   = "4-Digital Payment"
            queasy.logi1   = NO
            queasy.betriebsnr = 999.
        END.
        ELSE IF pg-number EQ 2 THEN /*MIDTRANS*/
        DO:
            CREATE queasy.
            ASSIGN
            queasy.KEY     = 224
            queasy.number1 = pg-number
            queasy.number2 = t-hoteldpt.num
            queasy.char1   = "1-CREDIT_CARD"
            queasy.char2   = "1-Debit/Credit Card"
            queasy.logi1   = NO
            queasy.betriebsnr = 999.
            CREATE queasy.
            ASSIGN
            queasy.KEY     = 224
            queasy.number1 = pg-number
            queasy.number2 = t-hoteldpt.num
            queasy.char1   = "2-GOPAY"
            queasy.char2   = "2-Digital Payment"
            queasy.logi1   = NO
            queasy.betriebsnr = 999.
            CREATE queasy.
            ASSIGN
            queasy.KEY     = 224
            queasy.number1 = pg-number
            queasy.number2 = t-hoteldpt.num
            queasy.char1   = "3-QRIS"
            queasy.char2   = "2-Digital Payment"
            queasy.logi1   = NO
            queasy.betriebsnr = 999.
            CREATE queasy.
            ASSIGN
            queasy.KEY     = 224
            queasy.number1 = pg-number
            queasy.number2 = t-hoteldpt.num
            queasy.char1   = "4-SHOPEEPAY"
            queasy.char2   = "2-Digital Payment"
            queasy.logi1   = NO
            queasy.betriebsnr = 999.
            CREATE queasy.
            ASSIGN
            queasy.KEY     = 224
            queasy.number1 = pg-number
            queasy.number2 = t-hoteldpt.num
            queasy.char1   = "5-BANK_TRANSFER|PERMATA"
            queasy.char2   = "6-Bank Transfer"
            queasy.logi1   = NO
            queasy.betriebsnr = 999.
            CREATE queasy.
            ASSIGN
            queasy.KEY     = 224
            queasy.number1 = pg-number
            queasy.number2 = t-hoteldpt.num
            queasy.char1   = "6-BANK_TRANSFER|BCA"
            queasy.char2   = "6-Bank Transfer"
            queasy.logi1   = NO
            queasy.betriebsnr = 999.
            CREATE queasy.
            ASSIGN
            queasy.KEY     = 224
            queasy.number1 = pg-number
            queasy.number2 = t-hoteldpt.num
            queasy.char1   = "7-BANK_TRANSFER|BNI"
            queasy.char2   = "6-Bank Transfer"
            queasy.logi1   = NO
            queasy.betriebsnr = 999.
            CREATE queasy.
            ASSIGN
            queasy.KEY     = 224
            queasy.number1 = pg-number
            queasy.number2 = t-hoteldpt.num
            queasy.char1   = "8-BANK_TRANSFER|BRI"
            queasy.char2   = "6-Bank Transfer"
            queasy.logi1   = NO
            queasy.betriebsnr = 999.
            CREATE queasy.
            ASSIGN
            queasy.KEY     = 224
            queasy.number1 = pg-number
            queasy.number2 = t-hoteldpt.num
            queasy.char1   = "9-ECHANNEL"
            queasy.char2   = "3-Internet Banking"
            queasy.logi1   = NO
            queasy.betriebsnr = 999.
            CREATE queasy.
            ASSIGN
            queasy.KEY     = 224
            queasy.number1 = pg-number
            queasy.number2 = t-hoteldpt.num
            queasy.char1   = "10-BCA_KLIKPAY"
            queasy.char2   = "3-Internet Banking"
            queasy.logi1   = NO
            queasy.betriebsnr = 999.
            CREATE queasy.
            ASSIGN
            queasy.KEY     = 224
            queasy.number1 = pg-number
            queasy.number2 = t-hoteldpt.num
            queasy.char1   = "11-BCA_KLIKBCA"
            queasy.char2   = "3-Internet Banking"
            queasy.logi1   = NO
            queasy.betriebsnr = 999.
            CREATE queasy.
            ASSIGN
            queasy.KEY     = 224
            queasy.number1 = pg-number
            queasy.number2 = t-hoteldpt.num
            queasy.char1   = "12-CIMB_CLICKS"
            queasy.char2   = "3-Internet Banking"
            queasy.logi1   = NO
            queasy.betriebsnr = 999.
            CREATE queasy.
            ASSIGN
            queasy.KEY     = 224
            queasy.number1 = pg-number
            queasy.number2 = t-hoteldpt.num
            queasy.char1   = "13-DANAMON_ONLINE"
            queasy.char2   = "3-Internet Banking"
            queasy.logi1   = NO
            queasy.betriebsnr = 999.
            CREATE queasy.
            ASSIGN
            queasy.KEY     = 224
            queasy.number1 = pg-number
            queasy.number2 = t-hoteldpt.num
            queasy.char1   = "14-BRI_EPAY"
            queasy.char2   = "3-Internet Banking"
            queasy.logi1   = NO
            queasy.betriebsnr = 999.
            CREATE queasy.
            ASSIGN
            queasy.KEY     = 224
            queasy.number1 = pg-number
            queasy.number2 = t-hoteldpt.num
            queasy.char1   = "15-CSTORE|INDOMARET"
            queasy.char2   = "4-Other Payment"
            queasy.logi1   = NO
            queasy.betriebsnr = 999.
            CREATE queasy.
            ASSIGN
            queasy.KEY     = 224
            queasy.number1 = pg-number
            queasy.number2 = t-hoteldpt.num
            queasy.char1   = "16-CSTORE|ALFAMART"
            queasy.char2   = "4-Other Payment"
            queasy.logi1   = NO
            queasy.betriebsnr = 999.
            CREATE queasy.
            ASSIGN
            queasy.KEY     = 224
            queasy.number1 = pg-number
            queasy.number2 = t-hoteldpt.num
            queasy.char1   = "17-AKULAKU"
            queasy.char2   = "4-Other Payment"
            queasy.logi1   = NO
            queasy.betriebsnr = 999.
        END.
        ELSE IF pg-number EQ 3 THEN /*XENDIT*/
        DO:
            CREATE queasy.
            ASSIGN
            queasy.KEY        = 224
            queasy.number1    = pg-number
            queasy.number2    = t-hoteldpt.num
            queasy.char1      = "1-BRI"
            queasy.char2      = "1-BANK_TRANSFER" 
            queasy.logi1      = NO
            queasy.betriebsnr = 999.
            CREATE queasy.
            ASSIGN
            queasy.KEY        = 224
            queasy.number1    = pg-number
            queasy.number2    = t-hoteldpt.num
            queasy.char1      = "2-BNI"
            queasy.char2      = "1-BANK_TRANSFER" 
            queasy.logi1      = NO
            queasy.betriebsnr = 999.
            CREATE queasy.
            ASSIGN
            queasy.KEY        = 224
            queasy.number1    = pg-number
            queasy.number2    = t-hoteldpt.num
            queasy.char1      = "3-MANDIRI"
            queasy.char2      = "1-BANK_TRANSFER" 
            queasy.logi1      = NO
            queasy.betriebsnr = 999.
            CREATE queasy.
            ASSIGN
            queasy.KEY        = 224
            queasy.number1    = pg-number
            queasy.number2    = t-hoteldpt.num
            queasy.char1      = "4-PERMATA"
            queasy.char2      = "1-BANK_TRANSFER" 
            queasy.logi1      = NO
            queasy.betriebsnr = 999.
            CREATE queasy.
            ASSIGN
            queasy.KEY        = 224
            queasy.number1    = pg-number
            queasy.number2    = t-hoteldpt.num
            queasy.char1      = "5-BCA"
            queasy.char2      = "1-BANK_TRANSFER" 
            queasy.logi1      = NO
            queasy.betriebsnr = 999.
            CREATE queasy.
            ASSIGN
            queasy.KEY        = 224
            queasy.number1    = pg-number
            queasy.number2    = t-hoteldpt.num
            queasy.char1      = "1-SHOPEEPAY"
            queasy.char2      = "2-EWALLET" 
            queasy.logi1      = NO
            queasy.betriebsnr = 999.
            CREATE queasy.
            ASSIGN
            queasy.KEY        = 224
            queasy.number1    = pg-number
            queasy.number2    = t-hoteldpt.num
            queasy.char1      = "2-DANA"
            queasy.char2      = "2-EWALLET" 
            queasy.logi1      = NO
            queasy.betriebsnr = 999.
            CREATE queasy.
            ASSIGN
            queasy.KEY        = 224
            queasy.number1    = pg-number
            queasy.number2    = t-hoteldpt.num
            queasy.char1      = "3-OVO"
            queasy.char2      = "2-EWALLET" 
            queasy.logi1      = NO
            queasy.betriebsnr = 999.
            CREATE queasy.
            ASSIGN
            queasy.KEY        = 224
            queasy.number1    = pg-number
            queasy.number2    = t-hoteldpt.num
            queasy.char1      = "4-LINKAJA"
            queasy.char2      = "2-EWALLET" 
            queasy.logi1      = NO
            queasy.betriebsnr = 999.
            CREATE queasy.
            ASSIGN
            queasy.KEY        = 224
            queasy.number1    = pg-number
            queasy.number2    = t-hoteldpt.num
            queasy.char1      = "1-CREDIT_CARD"
            queasy.char2      = "3-CREDIT_CARD" 
            queasy.logi1      = NO
            queasy.betriebsnr = 999.
            CREATE queasy.
            ASSIGN
            queasy.KEY        = 224
            queasy.number1    = pg-number
            queasy.number2    = t-hoteldpt.num
            queasy.char1      = "1-QRIS"
            queasy.char2      = "4-DIGITAL PAYMENT" 
            queasy.logi1      = NO
            queasy.betriebsnr = 999.
        END.
    END.
END.
