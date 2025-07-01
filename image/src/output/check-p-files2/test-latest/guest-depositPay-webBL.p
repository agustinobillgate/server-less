
DEFINE INPUT PARAMETER pvILanguage      AS INTEGER NO-UNDO.
DEFINE INPUT PARAMETER user-init        AS CHARACTER.
DEFINE INPUT PARAMETER guest-number     AS INTEGER.
DEFINE INPUT PARAMETER guest-name       AS CHARACTER.
DEFINE INPUT PARAMETER deposit-pay-num  AS INTEGER.
DEFINE INPUT PARAMETER deposit-pay-desc AS CHARACTER.
DEFINE INPUT PARAMETER deposit-pay-amt  AS DECIMAL.
DEFINE INPUT PARAMETER voucher-number   AS CHARACTER.
DEFINE OUTPUT PARAMETER error-desc      AS CHARACTER.

{SupertransBL.i} 
DEFINE VARIABLE lvCAREA AS CHAR INITIAL "guest-depositPay-web". 

DEFINE VARIABLE exchg-rate          AS DECIMAL NO-UNDO INIT 1. 
DEFINE VARIABLE foreign-payment     AS DECIMAL NO-UNDO.
DEFINE VARIABLE deposit-amount      AS DECIMAL NO-UNDO.
DEFINE VARIABLE deposit-foreign     AS DECIMAL NO-UNDO.
DEFINE VARIABLE local-depo-pay      AS DECIMAL NO-UNDO.
DEFINE VARIABLE price-decimal       AS INTEGER NO-UNDO.
DEFINE VARIABLE bill-date           AS DATE    NO-UNDO. 
DEFINE VARIABLE depoart             AS INTEGER NO-UNDO.
DEFINE VARIABLE depobez             AS CHARACTER NO-UNDO.
DEFINE VARIABLE sys-id              AS CHARACTER NO-UNDO.

FIND FIRST htparam WHERE htparam.paramnr EQ 1068 NO-LOCK NO-ERROR. 
IF AVAILABLE htparam THEN
DO:
    FIND FIRST artikel WHERE artikel.artnr EQ htparam.finteger AND artikel.departement EQ 0 NO-LOCK NO-ERROR.
    IF NOT AVAILABLE artikel OR artikel.artart NE 5 THEN
    DO:           
        error-desc = translateExtended ("Deposit article not defined.",lvCAREA,"").        
        RETURN. 
    END.
    ASSIGN 
        depoart = artikel.artnr
        depobez = artikel.bezeich
        .
END.

FIND FIRST artikel WHERE artikel.departement EQ 0 AND 
    (artikel.artart EQ 6 OR artikel.artart EQ 7) AND artikel.artnr EQ deposit-pay-num NO-LOCK NO-ERROR. 
IF NOT AVAILABLE artikel THEN 
DO: 
    error-desc = translateExtended ("Payment article not defined.",lvCAREA,"").        
    RETURN.  
END. 

/* Dzikri D53481 - Validasi untuk new profile */
IF guest-number EQ ? OR guest-number EQ 0 THEN 
DO: 
    error-desc = translateExtended ("Guest number is not yet defined. Please save the guest card first.",lvCAREA,"").        
    RETURN.  
END. 
/* Dzikri D53481 - Validasi untuk new profile */

FIND FIRST htparam WHERE htparam.paramnr EQ 110 NO-LOCK. 
bill-date = htparam.fdate.

FIND FIRST htparam WHERE htparam.paramnr EQ 491 NO-LOCK. 
price-decimal = htparam.finteger.

FIND FIRST htparam WHERE htparam.paramnr EQ 144 NO-LOCK. 
FIND FIRST waehrung WHERE waehrung.wabkurz EQ htparam.fchar NO-LOCK NO-ERROR. 
IF AVAILABLE waehrung THEN exchg-rate = waehrung.ankauf / waehrung.einheit.

deposit-pay-amt = deposit-pay-amt.

RUN calculate-amount(INPUT deposit-pay-amt).

RUN create-journal.

/*******************************************************************************************
                                        PROCEDURE
*******************************************************************************************/
PROCEDURE calculate-amount: 
    DEFINE INPUT PARAMETER amount AS DECIMAL. 
    DEFINE VARIABLE pay-exrate      AS DECIMAL INIT 1 NO-UNDO.
  
    IF artikel.pricetab THEN /*Payment Art*/
    DO:
        FIND FIRST waehrung WHERE waehrung.waehrungsnr = artikel.betriebsnr NO-LOCK NO-ERROR.
        IF AVAILABLE waehrung THEN ASSIGN pay-exrate = waehrung.ankauf / waehrung.einheit.
    END.       

    IF artikel.pricetab THEN  /* foreign currency */ 
    DO:
        ASSIGN 
            foreign-payment = amount
            deposit-foreign = - amount
            amount          = amount * exchg-rate 
            amount          = ROUND(amount, price-decimal)
            . 
    END.    
    ELSE
    DO:
        foreign-payment = amount / exchg-rate.
        deposit-foreign = - foreign-payment.
    END.
        
    local-depo-pay = amount.
    deposit-amount = - amount.
END PROCEDURE. 

PROCEDURE create-journal:
    DO TRANSACTION:
        /* deposit article */
        CREATE billjournal. 
        ASSIGN 
            billjournal.artnr = depoart 
            billjournal.anzahl = 1 
            billjournal.fremdwaehrng = deposit-foreign 
            billjournal.betrag = deposit-amount 
            billjournal.bezeich = depobez 
                + " [GuestNo#" + STRING(guest-number) + " " + artikel.bezeich + "]" + voucher-number 
            billjournal.epreis = 0 
            billjournal.zeit = TIME 
            billjournal.billjou-ref = artikel.artnr 
            billjournal.userinit = user-init
            billjournal.bill-datum = bill-date.
        FIND CURRENT billjournal NO-LOCK. 
        RELEASE billjournal.

        FIND FIRST umsatz WHERE umsatz.artnr EQ depoart
            AND umsatz.departement EQ 0 
            AND umsatz.datum EQ bill-date EXCLUSIVE-LOCK NO-ERROR. 
        IF NOT AVAILABLE umsatz THEN 
        DO: 
            CREATE umsatz. 
            ASSIGN
                umsatz.artnr = depoart
                umsatz.datum = bill-date
            . 
        END. 
        ASSIGN
            umsatz.anzahl = umsatz.anzahl + 1
            umsatz.betrag = umsatz.betrag + deposit-amount            
            . 
        FIND CURRENT umsatz NO-LOCK. 
        RELEASE umsatz.

        /* payment article */
        CREATE billjournal. 
        ASSIGN 
            billjournal.artnr = artikel.artnr 
            billjournal.anzahl = 1 
            billjournal.fremdwaehrng = foreign-payment 
            billjournal.betrag = local-depo-pay 
            billjournal.bezeich = artikel.bezeich 
                + "[" + translateExtended("Guest Deposit #",lvCAREA,"") + STRING(guest-number) + "]" + voucher-number 
            billjournal.epreis = 0
            billjournal.zeit = TIME
            billjournal.billjou-ref = guest-number 
            billjournal.userinit = user-init 
            billjournal.bill-datum = bill-date. 
        FIND CURRENT billjournal NO-LOCK. 
        RELEASE billjournal.

        FIND FIRST umsatz WHERE umsatz.artnr EQ artikel.artnr
            AND umsatz.departement EQ 0 
            AND umsatz.datum EQ bill-date EXCLUSIVE-LOCK NO-ERROR. 
        IF NOT AVAILABLE umsatz THEN 
        DO: 
            CREATE umsatz. 
            ASSIGN
                umsatz.artnr = artikel.artnr
                umsatz.datum = bill-date
            . 
        END. 
        ASSIGN
            umsatz.anzahl = umsatz.anzahl + 1
            umsatz.betrag = umsatz.betrag + local-depo-pay            
            . 
        FIND CURRENT umsatz NO-LOCK. 
        RELEASE umsatz.

        IF artikel.artart EQ 2 OR artikel.artart EQ 7 THEN 
        DO: 
            FIND FIRST bediener WHERE bediener.userinit EQ user-init NO-LOCK. 
            CREATE debitor. 
            ASSIGN 
                debitor.artnr        = artikel.artnr 
                debitor.gastnr       = guest-number 
                debitor.gastnrmember = guest-number 
                debitor.saldo        = deposit-amount 
                debitor.vesrdep      = deposit-foreign 
                debitor.transzeit    = TIME 
                debitor.rgdatum      = bill-date 
                debitor.bediener-nr  = bediener.nr 
                debitor.name         = guest-name 
                debitor.vesrcod      = translateExtended ("Guest Deposit Payment - GuestNo:",lvCAREA,"") 
                                     + " " + STRING(guest-number). 
            IF voucher-number NE "" THEN debitor.vesrcod = debitor.vesrcod + "; " + voucher-number. 
            RELEASE debitor. 
        END. 
    END.
END PROCEDURE.
