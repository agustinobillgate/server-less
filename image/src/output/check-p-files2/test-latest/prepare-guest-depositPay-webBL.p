DEFINE TEMP-TABLE guest-deposit-list
    FIELD guest-number      AS INTEGER
    FIELD article-number    AS INTEGER
    FIELD article-desc      AS CHARACTER
    FIELD trans-amount      AS DECIMAL
    FIELD trans-date        AS CHARACTER
    FIELD trans-remark      AS CHARACTER
    FIELD res-number        AS CHARACTER
    FIELD bill-number       AS INTEGER
    FIELD bill-type         AS CHARACTER
    FIELD user-init         AS CHARACTER
    FIELD flag              AS CHARACTER
    .

DEFINE INPUT PARAMETER pvILanguage      AS INTEGER NO-UNDO.
DEFINE INPUT PARAMETER user-init        AS CHARACTER.
DEFINE INPUT PARAMETER guest-number     AS INTEGER.
DEFINE INPUT PARAMETER guest-name       AS CHARACTER.
DEFINE OUTPUT PARAMETER deposit-balance AS DECIMAL.
DEFINE OUTPUT PARAMETER error-desc      AS CHARACTER.
DEFINE OUTPUT PARAMETER TABLE FOR guest-deposit-list.

{SupertransBL.i} 
DEFINE VARIABLE lvCAREA AS CHAR INITIAL "prepare-guest-depositPay-web". 

DEFINE VARIABLE depoart-guest       AS INTEGER NO-UNDO.
DEFINE VARIABLE depobez-guest       AS CHARACTER NO-UNDO.
DEFINE VARIABLE depoart-rsv         AS INTEGER NO-UNDO.
DEFINE VARIABLE depoart-bqt         AS INTEGER NO-UNDO.
DEFINE VARIABLE depoart-pos         AS INTEGER NO-UNDO.
DEFINE VARIABLE str                 AS CHARACTER NO-UNDO.
DEFINE VARIABLE uniq-str            AS CHARACTER NO-UNDO.

FIND FIRST htparam WHERE htparam.paramnr EQ 1068 AND htparam.finteger NE 0 NO-LOCK NO-ERROR. 
IF AVAILABLE htparam THEN
DO:
    FIND FIRST artikel WHERE artikel.artnr EQ htparam.finteger AND artikel.departement EQ 0 NO-LOCK NO-ERROR.
    IF NOT AVAILABLE artikel OR artikel.artart NE 5 THEN
    DO:
        error-desc = translateExtended ("Deposit article not defined.",lvCAREA,"").        
        RETURN. 
    END.
    ASSIGN 
        depoart-guest = artikel.artnr
        depobez-guest = artikel.bezeich
        .
END.
ELSE RETURN.

FIND FIRST htparam WHERE htparam.paramnr EQ 120 NO-LOCK NO-ERROR. 
IF AVAILABLE htparam THEN depoart-rsv = htparam.finteger.

FIND FIRST htparam WHERE htparam.paramnr EQ 117 NO-LOCK NO-ERROR. 
IF AVAILABLE htparam THEN depoart-bqt = htparam.finteger.

FIND FIRST htparam WHERE htparam.paramnr EQ 1361 NO-LOCK NO-ERROR. 
IF AVAILABLE htparam THEN depoart-pos = htparam.finteger.

/* Get All Deposit Payment */
FIND FIRST billjournal WHERE billjournal.billjou-ref EQ guest-number
    AND billjournal.artnr NE 0
    AND billjournal.artnr NE depoart-guest
    AND billjournal.artnr NE depoart-rsv
    AND billjournal.artnr NE depoart-bqt
    AND billjournal.artnr NE depoart-pos        
    AND NUM-ENTRIES(billjournal.bezeich,"[") GT 1
    AND SUBSTR(ENTRY(2,billjournal.bezeich,"["),1,13) EQ "Guest Deposit" NO-LOCK NO-ERROR.
DO WHILE AVAILABLE billjournal:

    CREATE guest-deposit-list.
    ASSIGN
        guest-deposit-list.guest-number     = guest-number           
        guest-deposit-list.article-number   = billjournal.artnr        
        guest-deposit-list.trans-amount     = - billjournal.betrag
        guest-deposit-list.trans-date       = STRING(billjournal.bill-datum) + " " + STRING(billjournal.zeit, "HH:MM:SS")
        guest-deposit-list.trans-remark     = ENTRY(2, billjournal.bezeich, "]") 
        guest-deposit-list.user-init        = billjournal.userinit
        guest-deposit-list.flag             = "*"
        .
    deposit-balance = deposit-balance + guest-deposit-list.trans-amount.

    FIND FIRST artikel WHERE artikel.artnr EQ billjournal.artnr
        AND artikel.departement EQ 0 NO-LOCK NO-ERROR.
    IF AVAILABLE artikel THEN guest-deposit-list.article-desc = artikel.bezeich.

    FIND NEXT billjournal WHERE billjournal.billjou-ref EQ guest-number
        AND billjournal.artnr NE 0
        AND billjournal.artnr NE depoart-guest
        AND billjournal.artnr NE depoart-rsv
        AND billjournal.artnr NE depoart-bqt
        AND billjournal.artnr NE depoart-pos        
        AND NUM-ENTRIES(billjournal.bezeich,"[") GT 1
        AND SUBSTR(ENTRY(2,billjournal.bezeich,"["),1,13) EQ "Guest Deposit" NO-LOCK NO-ERROR.
END.

/* Get All Deposit Amount(-) From Bill */
FOR EACH bill WHERE bill.rechnr GT 0 AND bill.gastnr EQ guest-number NO-LOCK,
    EACH bill-line WHERE bill-line.rechnr EQ bill.rechnr
    AND bill-line.artnr EQ depoart-guest NO-LOCK:

    CREATE guest-deposit-list.
    ASSIGN
        guest-deposit-list.guest-number     = guest-number
        guest-deposit-list.article-number   = bill-line.artnr
        guest-deposit-list.article-desc     = bill-line.bezeich
        guest-deposit-list.trans-amount     = bill-line.betrag
        guest-deposit-list.trans-date       = STRING(bill-line.bill-datum) + " " + STRING(bill-line.zeit, "HH:MM:SS")
        guest-deposit-list.bill-number      = bill.rechnr                
        guest-deposit-list.user-init        = bill-line.userinit
        guest-deposit-list.flag             = "**"
        guest-deposit-list.trans-remark     = "BillNumber:" + " " + STRING(bill.rechnr)
        .
    deposit-balance = deposit-balance + guest-deposit-list.trans-amount. 

    IF bill.resnr GT 0 AND bill.reslinnr GT 0 THEN
    DO:
        ASSIGN
            guest-deposit-list.bill-type    = "GuestBill"
            guest-deposit-list.res-number   = STRING(bill.resnr) + "/" + STRING(bill.reslinnr)
            guest-deposit-list.trans-remark = guest-deposit-list.trans-remark + "|" 
                                            + "BillType:" + " " + guest-deposit-list.bill-type + "|"
                                            + "ResNumber:" + " " + guest-deposit-list.res-number 
            .
    END.
    ELSE IF bill.resnr GT 0 AND bill.reslinnr EQ 0 THEN
    DO:
        ASSIGN
            guest-deposit-list.bill-type    = "MasterBill"            
            guest-deposit-list.trans-remark = guest-deposit-list.trans-remark + "|" 
                                            + "BillType:" + " " + guest-deposit-list.bill-type                                           
            .
    END.
    ELSE IF bill.resnr EQ 0 AND bill.reslinnr GT 0 THEN
    DO:
        ASSIGN
            guest-deposit-list.bill-type    = "NonstayBill"            
            guest-deposit-list.trans-remark = guest-deposit-list.trans-remark + "|" 
                                            + "BillType:" + " " + guest-deposit-list.bill-type                                            
            .
    END.
END.
