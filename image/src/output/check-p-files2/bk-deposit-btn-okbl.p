DEFINE INPUT PARAMETER paymentMode      AS INTEGER. /* 0 = Deposit | 1 = Payment | 2 = Refund */
DEFINE INPUT PARAMETER blockId          AS CHARACTER.
DEFINE INPUT PARAMETER deposit          AS DECIMAL.
DEFINE INPUT PARAMETER limitDate        AS DATE.
DEFINE INPUT PARAMETER nr               AS INTEGER. /*counter number for payment or refund*/
DEFINE INPUT PARAMETER artnr            AS INTEGER. /*artnr for payment or refund*/
DEFINE INPUT PARAMETER payment          AS DECIMAL. /*value for payment or refund*/
DEFINE INPUT PARAMETER foreign-payment  AS DECIMAL. /* throw always 0 - based on old gui (bk-depopayUI)*/
DEFINE INPUT PARAMETER userInit         AS CHARACTER.
DEFINE INPUT PARAMETER voucherNo        AS CHARACTER. /*value for voucher No*/

DEFINE VARIABLE depoart         AS INTEGER      NO-UNDO.
DEFINE VARIABLE depobezeich     AS CHARACTER    NO-UNDO.
DEFINE VARIABLE art-depo        AS INTEGER      NO-UNDO.
DEFINE VARIABLE bqt-dept        AS INTEGER      NO-UNDO.
DEFINE VARIABLE gastNr          AS INTEGER      NO-UNDO.
DEFINE VARIABLE billDate        AS DATE         NO-UNDO.

DEFINE BUFFER bartikel FOR artikel.
/*
DEFINE VARIABLE blockId         AS CHARACTER    NO-UNDO.
DEFINE VARIABLE artnr           AS INTEGER      NO-UNDO.
DEFINE VARIABLE payment         AS DECIMAL      NO-UNDO.
DEFINE VARIABLE depoart         AS INTEGER      NO-UNDO.
DEFINE VARIABLE depobezeich     AS CHARACTER    NO-UNDO.
DEFINE VARIABLE foreign-payment AS DECIMAL      NO-UNDO.
DEFINE VARIABLE user-init       AS CHARACTER    NO-UNDO.
*/

RUN htpdate.p(110, OUTPUT billDate).

FIND FIRST htparam WHERE htparam.paramnr EQ 900 NO-LOCK NO-ERROR.
IF AVAILABLE htparam THEN
DO:
    bqt-dept    = htparam.finteger.
END.

FIND FIRST htparam WHERE htparam.paramnr EQ 117 USE-INDEX paramnr_ix NO-LOCK NO-ERROR.
IF AVAILABLE htparam THEN
DO:
    art-depo    = htparam.finteger.
END.

FIND FIRST bk-master WHERE bk-master.block-id EQ blockId NO-LOCK NO-ERROR.
IF AVAILABLE bk-master THEN
DO:
    gastNr = bk-master.gastnr.
END.

IF paymentMode EQ 0 THEN
DO:
    FIND FIRST bk-deposit WHERE bk-deposit.blockId EQ blockID EXCLUSIVE-LOCK NO-ERROR.
    IF AVAILABLE bk-deposit THEN
    DO:
        ASSIGN
            bk-deposit.deposit  = deposit.
    END.
    ELSE
    DO:
        CREATE bk-deposit.
        ASSIGN
            bk-deposit.blockId      = blockID            
            bk-deposit.deposit      = deposit
            bk-deposit.limitDate    = limitDate
            bk-deposit.totalPaid    = 0
            bk-deposit.totalRefund  = 0
            bk-deposit.gastnr       = gastNr.
            
    END.
END.
ELSE IF paymentMode EQ 1 THEN
DO:
    
    FIND FIRST artikel WHERE artikel.artnr EQ art-depo
        AND artikel.departement EQ bqt-dept 
        AND artikel.artart EQ 5 NO-LOCK NO-ERROR.
    IF NOT AVAILABLE artikel THEN
    DO:
        FIND FIRST bartikel WHERE bartikel.artnr EQ art-depo
            AND bartikel.departement EQ 0
            AND bartikel.artart EQ 5 NO-LOCK NO-ERROR.
        IF NOT AVAILABLE bartikel THEN
        DO:
    
        END.
        ELSE
        DO:
            ASSIGN
                depoart     = bartikel.artnr
                depobezeich = bartikel.bezeich.
        END.
    END.
    ELSE
    DO:
        ASSIGN
            depoart         = artikel.artnr
            depobezeich     = artikel.bezeich.
    END.
    
    FIND FIRST bk-deposit WHERE bk-deposit.blockId EQ blockId EXCLUSIVE-LOCK NO-ERROR.
    IF AVAILABLE bk-deposit THEN
    DO:
        bk-deposit.totalPaid = bk-deposit.totalPaid + payment.
    END. 
    
    CREATE bk-deposit-line.
    ASSIGN
        bk-deposit-line.blockId         = blockId
        bk-deposit-line.nr              = nr
        bk-deposit-line.paymentAmount   = payment
        bk-deposit-line.paymentArtnr    = artNr
        bk-deposit-line.paymentUserinit = userInit
        bk-deposit-line.paymentDate     = TODAY
        bk-deposit-line.paymentType     = paymentMode
        bk-deposit-line.voucherNo       = voucherNo.
        
    RUN create-journal(billDate).
END.
ELSE IF paymentMode EQ 2 THEN
DO:
    FIND FIRST bk-deposit WHERE bk-deposit.blockId EQ blockId EXCLUSIVE-LOCK NO-ERROR.
    IF AVAILABLE bk-deposit THEN
    DO:
/*    
        bk-deposit.totalRefund = bk-deposit.totalRefund + payment.
*/
        bk-deposit.totalPaid = bk-deposit.totalPaid + payment.        
    END. 
    
    FIND FIRST bk-deposit-lines WHERE bk-deposit-lines.blockId EQ blockID 
        AND bk-deposit-lines.nr EQ nr EXCLUSIVE-LOCK NO-ERROR.
    IF AVAILABLE bk-deposit-lines THEN
    DO:
        DELETE bk-deposit-lines.
        RELEASE bk-deposit-lines.
    END.    
    
    FIND FIRST artikel WHERE artikel.artnr EQ art-depo
        AND artikel.departement EQ bqt-dept 
        AND artikel.artart EQ 5 NO-LOCK NO-ERROR.
    IF NOT AVAILABLE artikel THEN
    DO:
        FIND FIRST bartikel WHERE bartikel.artnr EQ art-depo
            AND bartikel.departement EQ 0
            AND bartikel.artart EQ 5 NO-LOCK NO-ERROR.
        IF NOT AVAILABLE bartikel THEN
        DO:
    
        END.
        ELSE
        DO:
            ASSIGN
                depoart     = bartikel.artnr
                depobezeich = bartikel.bezeich.
        END.
    END.
    ELSE
    DO:
        ASSIGN
            depoart         = artikel.artnr
            depobezeich     = artikel.bezeich.
    END.    
    
    RUN create-journal(billDate).    
END.

PROCEDURE create-journal:
    DEFINE INPUT PARAMETER billDate       AS DATE     NO-UNDO.   
    
    FIND FIRST artikel WHERE artikel.artnr EQ artnr NO-LOCK NO-ERROR.
    IF AVAILABLE artikel THEN
    DO:
        IF artikel.artart EQ 2 OR artikel.artart EQ 7 THEN
        DO:
            RUN inv-ar(billDate).
        END.

        FIND FIRST umsatz WHERE umsatz.departement EQ 0
            AND umsatz.artnr EQ artikel.artnr
            AND umsatz.datum EQ billDate EXCLUSIVE-LOCK NO-ERROR.
        IF NOT AVAILABLE umsatz THEN
        DO:
            CREATE umsatz.
            ASSIGN 
                umsatz.artnr        = artikel.artnr
                umsatz.datum        = billDate.
        END.

        ASSIGN 
            umsatz.anzahl   = umsatz.anzahl + 1
            umsatz.betrag   = umsatz.betrag - payment.
/*            umsatz.betrag   = umsatz.betrag + payment.*/

        RELEASE umsatz.

        CREATE billjournal.
        ASSIGN
            billjournal.artnr           = artikel.artnr
            billjournal.anzahl          = 1
            billjournal.fremdwaehrng    = foreign-payment
            billjournal.epreis          = 0
            billjournal.zeit            = TIME
            billjournal.userinit        = userInit
            billjournal.bill-datum      = billDate.
        IF paymentMode EQ 1 THEN
        DO:
            billjournal.bezeich         = artikel.bezeich + " #" + blockId + "/" + voucherNo.        
        END.    
        ELSE IF paymentMode EQ 2 THEN
        DO:
            billjournal.bezeich         = artikel.bezeich + " [Refund #" + blockId + "]/" + voucherNo        .
        END.
            
        IF artikel.pricetab THEN
        DO:
            IF paymentMode EQ 1 THEN
            DO:
                billjournal.betrag = foreign-payment.
            END.
            ELSE IF paymentMode EQ 2 THEN
            DO:
                billjournal.betrag = - foreign-payment.
            END.
        END.
        ELSE
        DO:        
            IF paymentMode EQ 1 THEN
            DO:
                billjournal.betrag = - payment.
            END.
            ELSE IF paymentMode EQ 2 THEN
            DO:
                billjournal.betrag = - payment.
            END.
        END.

        FIND CURRENT billjournal NO-LOCK.

        FIND FIRST umsatz WHERE umsatz.artnr EQ depoart
            AND umsatz.departement EQ 0
            AND umsatz.datum EQ billDate NO-ERROR.
        IF NOT AVAILABLE umsatz THEN
        DO:
            CREATE umsatz.
            ASSIGN
                umsatz.departement  = 0
                umsatz.artnr        = depoart
                umsatz.datum        = billDate.
        END.

        ASSIGN
            umsatz.betrag   = umsatz.betrag + payment        
/*            umsatz.betrag   = umsatz.betrag - payment*/
            umsatz.anzahl   = umsatz.anzahl + 1.

        CREATE billjournal.
        ASSIGN
            billjournal.artnr           = depoart
            billjournal.departement     = artikel.departement
            billjournal.billjou-ref     = artikel.artnr
            billjournal.anzahl          = 1
            billjournal.fremdwaehrng    = foreign-payment
            billjournal.betrag          = payment
            billjournal.bezeich         = depobezeich + " #" + blockId + "/" + voucherNo
            billjournal.epreis          = 0
            billjournal.zeit            = TIME
            billjournal.userinit        = userInit
            billjournal.bill-datum      = billDate.
        FIND CURRENT billjournal NO-LOCK.
    END.
END PROCEDURE.

PROCEDURE inv-ar:
    DEFINE INPUT PARAMETER bill-date        AS DATE.   

    FIND FIRST htparam WHERE htparam.paramnr EQ 997 NO-LOCK NO-ERROR.
    IF NOT htparam.flogical THEN
    DO:
        RETURN.
    END.

    FIND FIRST bediener WHERE bediener.userinit EQ userInit NO-LOCK NO-ERROR.
    FIND FIRST guest WHERE guest.gastnr EQ gastNr USE-INDEX gastnr_index NO-LOCK NO-ERROR.
    FIND FIRST artikel WHERE artikel.artnr EQ artnr NO-LOCK NO-ERROR.
    
    CREATE debitor.
    ASSIGN
        debitor.artnr               = artikel.artnr
        debitor.gastnr              = bk-deposit.gastnr
        debitor.gastnrmember        = bk-deposit.gastnr
        debitor.saldo               = payment
        debitor.transzeit           = TIME
        debitor.rgdatum             = bill-date
        debitor.bediener-nr         = bediener.nr
        debitor.vesrcod             = "BQT DP - ResNo : " + blockId + ";" + voucherNo
        debitor.NAME                = guest.NAME + ", " + guest.vorname1 + " " + guest.anrede1 + guest.anredefirma.

    RELEASE debitor.
END PROCEDURE.
