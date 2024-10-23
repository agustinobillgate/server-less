
DEFINE INPUT PARAMETER pvILanguage      AS INTEGER NO-UNDO.
DEFINE INPUT PARAMETER s-recid          AS INTEGER. 
DEFINE INPUT PARAMETER selected-gastnr  AS INTEGER.
DEFINE INPUT PARAMETER deposit-amt      AS DECIMAL.
DEFINE INPUT PARAMETER depo-artpay      AS INTEGER.
DEFINE INPUT PARAMETER depo-artpay-bez  AS CHARACTER.
DEFINE INPUT PARAMETER deposit-pay      AS DECIMAL.
DEFINE INPUT PARAMETER voucher-str      AS CHARACTER.
DEFINE INPUT PARAMETER user-init        AS CHARACTER.
DEFINE INPUT PARAMETER curr-dept        AS INTEGER.
DEFINE INPUT PARAMETER moved-tisch      AS INTEGER.
DEFINE INPUT PARAMETER pax              AS INTEGER.
DEFINE INPUT PARAMETER h1               AS INTEGER.
DEFINE INPUT PARAMETER m1               AS INTEGER.
DEFINE INPUT PARAMETER h2               AS INTEGER.
DEFINE INPUT PARAMETER m2               AS INTEGER.
DEFINE INPUT PARAMETER curr-date        AS DATE.
DEFINE OUTPUT PARAMETER error-flag      AS LOGICAL INIT NO.
DEFINE OUTPUT PARAMETER msg-str         AS CHARACTER.
DEFINE OUTPUT PARAMETER ns-billno       AS INTEGER.

{SupertransBL.i} 
DEFINE VARIABLE lvCAREA AS CHAR INITIAL "ts-restdeposit-pay". 

DEFINE VARIABLE exchg-rate          AS DECIMAL NO-UNDO INIT 1. 
DEFINE VARIABLE foreign-payment     AS DECIMAL NO-UNDO.
DEFINE VARIABLE local-payment       AS DECIMAL NO-UNDO.
DEFINE VARIABLE deposit-foreign     AS DECIMAL NO-UNDO.
DEFINE VARIABLE price-decimal       AS INTEGER NO-UNDO.
DEFINE VARIABLE bill-date           AS DATE    NO-UNDO. 
DEFINE VARIABLE depoart             AS INTEGER NO-UNDO.
DEFINE VARIABLE depobez             AS CHARACTER NO-UNDO.
DEFINE VARIABLE sys-id              AS CHARACTER NO-UNDO.

FIND FIRST htparam WHERE htparam.paramnr EQ 1361 NO-LOCK NO-ERROR. 
IF AVAILABLE htparam THEN
DO:
    FIND FIRST artikel WHERE artikel.artnr EQ htparam.finteger AND artikel.departement EQ 0 NO-LOCK NO-ERROR.
    IF NOT AVAILABLE artikel OR artikel.artart NE 5 THEN
    DO:
        ASSIGN
            error-flag = YES
            msg-str = translateExtended ("Deposit article not defined.",lvCAREA,"")
        .
        RETURN. 
    END.
    ASSIGN 
        depoart = artikel.artnr
        depobez = artikel.bezeich
        .
END.

FIND FIRST artikel WHERE artikel.departement EQ 0 AND 
    (artikel.artart EQ 6 OR artikel.artart EQ 7) AND artikel.artnr EQ depo-artpay NO-LOCK NO-ERROR. 
IF NOT AVAILABLE artikel THEN 
DO: 
    ASSIGN
        error-flag = YES
        msg-str = translateExtended ("Payment article not defined.",lvCAREA,"")
    .
    RETURN. 
END. 

FIND FIRST htparam WHERE htparam.paramnr EQ 110 NO-LOCK. 
bill-date = htparam.fdate.

FIND FIRST htparam WHERE htparam.paramnr EQ 491 NO-LOCK. 
price-decimal = htparam.finteger. 

FIND FIRST htparam WHERE htparam.paramnr = 104 NO-LOCK. 
sys-id = htparam.fchar. 

FIND FIRST htparam WHERE htparam.paramnr EQ 144 NO-LOCK. 
FIND FIRST waehrung WHERE waehrung.wabkurz EQ htparam.fchar NO-LOCK NO-ERROR. 
IF AVAILABLE waehrung THEN exchg-rate = waehrung.ankauf / waehrung.einheit.

ASSIGN
    deposit-foreign = deposit-amt / exchg-rate
    foreign-payment = deposit-pay / exchg-rate
    local-payment = deposit-pay
.

RUN create-close-ns-bill.

PROCEDURE create-close-ns-bill: 
DEFINE VARIABLE guest-name  AS CHARACTER    NO-UNDO.
DEFINE VARIABLE table-no    AS INTEGER      NO-UNDO.
DEFINE VARIABLE dept-no     AS INTEGER      NO-UNDO.
DEFINE VARIABLE curr-pax    AS INTEGER      NO-UNDO.
DEFINE VARIABLE ft-time     AS INTEGER      NO-UNDO.
DEFINE VARIABLE time-rsv-table AS CHARACTER NO-UNDO.
DEFINE VARIABLE date-rsv-table AS DATE      NO-UNDO.

    FIND FIRST guest WHERE guest.gastnr EQ selected-gastnr NO-LOCK NO-ERROR.
    IF AVAILABLE guest THEN
    DO:
        guest-name = guest.NAME + ",".

        IF guest.vorname1 NE "" AND guest.vorname1 NE ? THEN
        DO:
            guest-name = guest-name + guest.vorname1.
        END.
    END.

    ASSIGN
        dept-no         = curr-dept
        table-no        = moved-tisch            
        curr-pax        = pax
        ft-time         = h1 + m1 + h2 + m2
        time-rsv-table  = STRING(h1, "99") + STRING(m1, "99") + STRING(h2, "99") + STRING(m2, "99")
        date-rsv-table  = curr-date
    .    

    DO TRANSACTION:
        /*Create Bill, Bill-Line, Bill-Journal*/
        CREATE bill.
    
        FIND FIRST counters WHERE counters.counter-no EQ 3 EXCLUSIVE-LOCK NO-ERROR. 
        IF NOT AVAILABLE counters THEN
        DO:
            CREATE counters. 
            ASSIGN 
                counters.counter-no = 3
                counters.counter-bez = "Counter for Bill No" 
            . 
        END.
        counters.counter = counters.counter + 1. 
        ns-billno = counters.counter.
        FIND CURRENT counter NO-LOCK.
    
        ASSIGN
            bill.flag       = 1
            bill.rechnr     = ns-billno
            bill.datum      = bill-date
            bill.gastnr     = selected-gastnr
            bill.billtyp    = curr-dept
            bill.name       = guest-name
            bill.bilname    = bill.NAME
            bill.resnr      = 0
            bill.reslinnr   = 1
            bill.rgdruck    = 1 
            bill.saldo      = 0
        .
        IF AVAILABLE guest AND guest.anredefirma NE "" AND guest.anredefirma NE ? THEN
        DO:
            bill.NAME = bill.NAME + " " + guest.anredefirma.
        END.
    
        /*deposit article*/
        CREATE bill-line.
        ASSIGN
            bill-line.rechnr        = ns-billno
            bill-line.artnr         = depoart
            bill-line.bezeich       = depobez + "/" + voucher-str + " [" + artikel.bezeich + "]"
            bill-line.anzahl        = 1
            bill-line.betrag        = deposit-amt 
            bill-line.fremdwbetrag  = deposit-foreign
            bill-line.zeit          = TIME
            bill-line.userinit      = user-init         
            bill-line.bill-datum    = bill-date
        .
        FIND CURRENT bill-line NO-LOCK.
    
        CREATE billjournal. 
        ASSIGN 
            billjournal.rechnr          = ns-billno
            billjournal.artnr           = depoart 
            billjournal.anzahl          = 1 
            billjournal.betrag          = - local-payment 
            billjournal.fremdwaehrng    = - foreign-payment                 
            billjournal.epreis          = 0
            billjournal.zeit            = TIME
            billjournal.billjou-ref     = artikel.artnr /* payment ArtNo */ 
            billjournal.userinit        = user-init 
            billjournal.bill-datum      = bill-date
            billjournal.bezeich         = depobez 
                + " [#" + STRING(dept-no) + STRING(table-no) + time-rsv-table + " " + artikel.bezeich + "]" + voucher-str 
        . 
        FIND CURRENT billjournal NO-LOCK.
        
        FIND FIRST umsatz WHERE umsatz.artnr EQ depoart
            AND umsatz.departement EQ 0 
            AND umsatz.datum EQ bill-date NO-ERROR. 
        IF NOT AVAILABLE umsatz THEN 
        DO: 
            CREATE umsatz. 
            ASSIGN
                umsatz.artnr = depoart
                umsatz.datum = bill-date
            . 
        END. 
        ASSIGN
            umsatz.betrag = umsatz.betrag - local-payment
            umsatz.anzahl = umsatz.anzahl + 1
        . 
        RELEASE umsatz.
    
        /*payment article*/
        CREATE bill-line.
        ASSIGN
            bill-line.rechnr        = ns-billno
            bill-line.artnr         = artikel.artnr
            bill-line.bezeich       = artikel.bezeich + "/" + voucher-str
            bill-line.anzahl        = 1
            bill-line.betrag        = local-payment 
            bill-line.fremdwbetrag  = foreign-payment
            bill-line.zeit          = TIME
            bill-line.userinit      = user-init         
            bill-line.bill-datum    = bill-date
        .
        FIND CURRENT bill-line NO-LOCK.
    
        CREATE billjournal. 
        ASSIGN 
            billjournal.rechnr          = ns-billno
            billjournal.artnr           = artikel.artnr 
            billjournal.anzahl          = 1 
            billjournal.betrag          = local-payment
            billjournal.fremdwaehrng    = foreign-payment 
            billjournal.epreis          = 0 
            billjournal.zeit            = TIME 
            billjournal.userinit        = user-init 
            billjournal.bill-datum      = bill-date 
            billjournal.billjou-ref     = dept-no + table-no + ft-time                                     
        . 
        billjournal.bezeich = artikel.bezeich + "[" 
            + translateExtended("Restaurant Deposit",lvCAREA,"") + " #" + STRING(dept-no) + STRING(table-no) + time-rsv-table 
            + "]" + voucher-str.         
        FIND CURRENT billjournal NO-LOCK.  
    
        FIND FIRST umsatz WHERE umsatz.departement EQ 0 
            AND umsatz.artnr EQ artikel.artnr 
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
            umsatz.betrag = umsatz.betrag + local-payment
        . 
        RELEASE umsatz.
    
        /*Create Debitor*/
        IF artikel.artart EQ 7 THEN 
        DO: 
            FIND FIRST bediener WHERE bediener.userinit EQ user-init NO-LOCK. 
            CREATE debitor. 
            ASSIGN 
                debitor.rechnr       = ns-billno
                debitor.artnr        = artikel.artnr 
                debitor.gastnr       = selected-gastnr 
                debitor.gastnrmember = selected-gastnr 
                debitor.saldo        = - local-payment 
                debitor.vesrdep      = - foreign-payment 
                debitor.transzeit    = TIME 
                debitor.rgdatum      = bill-date 
                debitor.bediener-nr  = bediener.nr 
                debitor.name         = guest-name 
                debitor.vesrcod      = translateExtended ("Restaurant Deposit Payment #",lvCAREA,"") 
                                     + STRING(dept-no) + STRING(table-no) + time-rsv-table
                                    . 
            IF voucher-str NE "" THEN debitor.vesrcod = debitor.vesrcod + "; " + voucher-str. 
            RELEASE debitor. 
        END.     
    END.   
END PROCEDURE. 
