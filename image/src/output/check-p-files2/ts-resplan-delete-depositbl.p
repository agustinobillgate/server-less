
DEFINE INPUT PARAMETER curr-dept    AS INTEGER.
DEFINE INPUT PARAMETER curr-date    AS DATE.
DEFINE INPUT PARAMETER s-recid      AS INTEGER.
DEFINE INPUT PARAMETER user-init    AS CHARACTER.
DEFINE OUTPUT PARAMETER ok-flag     AS LOGICAL INITIAL NO.

DEFINE VARIABLE active-deposit  AS LOGICAL.
DEFINE VARIABLE depoart         AS INTEGER.
DEFINE VARIABLE depobez         AS CHARACTER NO-UNDO.
DEFINE VARIABLE exchg-rate      AS DECIMAL NO-UNDO INIT 1. 
DEFINE VARIABLE deposit-foreign AS DECIMAL NO-UNDO.
DEFINE VARIABLE foreign-payment AS DECIMAL NO-UNDO.
DEFINE VARIABLE sys-id          AS CHARACTER NO-UNDO.

FIND FIRST htparam WHERE htparam.paramnr EQ 588 NO-LOCK NO-ERROR. 
IF AVAILABLE htparam THEN active-deposit = htparam.flogical.

FIND FIRST htparam WHERE htparam.paramnr EQ 1361 NO-LOCK NO-ERROR. 
IF AVAILABLE htparam THEN
DO:
    depoart = htparam.finteger.
    FIND FIRST artikel WHERE artikel.artnr EQ htparam.finteger AND artikel.departement EQ 0 NO-LOCK NO-ERROR.
    IF AVAILABLE artikel THEN depobez = artikel.bezeich.
END.

FIND FIRST htparam WHERE htparam.paramnr EQ 144 NO-LOCK. 
FIND FIRST waehrung WHERE waehrung.wabkurz EQ htparam.fchar NO-LOCK NO-ERROR. 
IF AVAILABLE waehrung THEN exchg-rate = waehrung.ankauf / waehrung.einheit.

IF active-deposit THEN
DO:
    RUN create-rsv-table.

    FIND FIRST queasy WHERE RECID(queasy) EQ s-recid NO-LOCK NO-ERROR.
    IF AVAILABLE queasy THEN
    DO:
        FIND CURRENT queasy EXCLUSIVE-LOCK.
        ASSIGN
            queasy.logi3 = NO
            queasy.date3 = TODAY
            queasy.deci3 = TIME
            queasy.char3 = queasy.char3 + user-init + ";"
            queasy.betriebsnr = 2
        .
        FIND CURRENT queasy NO-LOCK.
        RELEASE queasy.
    END.
END.

PROCEDURE create-rsv-table:
    DEFINE VARIABLE it-exist        AS LOGICAL INITIAL NO.
    DEFINE VARIABLE guest-name      AS CHARACTER    NO-UNDO.
    DEFINE VARIABLE gastno          AS INTEGER.
    DEFINE VARIABLE ns-billno       AS INTEGER.
    DEFINE VARIABLE nsbill-number   AS INTEGER.
    DEFINE VARIABLE tot-deposit     AS DECIMAL.
    DEFINE VARIABLE depo-amount     AS DECIMAL.
    DEFINE VARIABLE dept-no         AS INTEGER      NO-UNDO.
    DEFINE VARIABLE curr-pax        AS INTEGER      NO-UNDO.
    DEFINE VARIABLE tableno         AS INTEGER      NO-UNDO.
    DEFINE VARIABLE ft-time         AS INTEGER      NO-UNDO.
    DEFINE VARIABLE time-rsv-table  AS CHARACTER    NO-UNDO.
    DEFINE VARIABLE date-rsv-table  AS DATE         NO-UNDO.
    DEFINE VARIABLE depopay-desc    AS CHARACTER    NO-UNDO.
    DEFINE VARIABLE voucher-str     AS CHARACTER    NO-UNDO.
    DEFINE VARIABLE depopay-art     AS INTEGER      NO-UNDO.

    DEFINE BUFFER buffq33 FOR queasy.        
    DEFINE BUFFER rsvtable-list FOR queasy.

    FIND FIRST buffq33 WHERE RECID(buffq33) EQ s-recid NO-LOCK NO-ERROR.
    IF AVAILABLE buffq33 THEN
    DO:
         nsbill-number = 0.
         it-exist = YES.

        ASSIGN
            gastno          = INTEGER(ENTRY(3, buffq33.char2, "&&"))
            dept-no         = buffq33.number1
            tableno         = buffq33.number2
            ft-time         = INT(SUBSTR(buffq33.char1,1,8))
            time-rsv-table  = SUBSTR(buffq33.char1,1,8)
            date-rsv-table  = buffq33.date1
            depo-amount     = - buffq33.deci1                      
            .
        deposit-foreign = depo-amount / exchg-rate.
        
        FIND FIRST guest WHERE guest.gastnr EQ gastno NO-LOCK NO-ERROR.
        IF AVAILABLE guest THEN
        DO:
            guest-name = guest.NAME + "," + guest.vorname1.
        END.

        FIND FIRST bill WHERE bill.rechnr EQ INTEGER(buffq33.deci2) 
            AND bill.gastnr EQ gastno AND bill.resnr EQ 0 
            AND bill.reslinnr EQ 1 AND bill.billtyp EQ buffq33.number1 
            AND bill.flag EQ 1 NO-LOCK NO-ERROR.
        IF AVAILABLE bill THEN
        DO:
            FIND FIRST bill-line WHERE bill-line.rechnr EQ bill.rechnr
                AND bill-line.artnr NE depoart NO-LOCK NO-ERROR.
            IF AVAILABLE bill-line THEN /*Payment Article Old/Close*/
            DO:
                depopay-desc = bill-line.bezeich.
                depopay-art = bill-line.artnr.

                IF NUM-ENTRIES(bill-line.bezeich, "/") GT 1 THEN
                DO:
                    voucher-str = ENTRY(2, bill-line.bezeich, "/").
                END.                    
            END.
        END.

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
            nsbill-number = counters.counter.
            FIND CURRENT counter NO-LOCK.

            ASSIGN
                bill.flag       = 0
                bill.rechnr     = nsbill-number
                bill.datum      = curr-date
                bill.gastnr     = gastno
                bill.billtyp    = dept-no
                bill.name       = guest-name + " " + guest.anredefirma
                bill.bilname    = bill.NAME
                bill.resnr      = 0
                bill.reslinnr   = 1
                bill.rgdruck    = 0 
                bill.saldo      = depo-amount
            .

            /*deposit article*/
            CREATE bill-line.
            ASSIGN
                bill-line.rechnr        = nsbill-number
                bill-line.artnr         = depoart
                bill-line.bezeich       = depobez + "/" + voucher-str
                bill-line.anzahl        = 1
                bill-line.betrag        = depo-amount 
                bill-line.fremdwbetrag  = deposit-foreign
                bill-line.zeit          = TIME
                bill-line.userinit      = user-init         
                bill-line.bill-datum    = curr-date
            .
            FIND CURRENT bill-line NO-LOCK.

            CREATE billjournal. 
            ASSIGN 
                billjournal.rechnr          = nsbill-number
                billjournal.artnr           = depoart 
                billjournal.anzahl          = 1 
                billjournal.betrag          = depo-amount 
                billjournal.fremdwaehrng    = deposit-foreign                 
                billjournal.epreis          = 0
                billjournal.zeit            = TIME
                billjournal.billjou-ref     = depopay-art /* payment ArtNo */ 
                billjournal.userinit        = user-init 
                billjournal.bill-datum      = curr-date
                billjournal.bezeich         = depobez 
                    + " [#" + STRING(dept-no) + STRING(tableno) + time-rsv-table + "]" + voucher-str 
            . 
            FIND CURRENT billjournal NO-LOCK.

            FIND FIRST umsatz WHERE umsatz.artnr EQ depoart
                AND umsatz.departement EQ 0 
                AND umsatz.datum EQ curr-date NO-ERROR. 
            IF NOT AVAILABLE umsatz THEN 
            DO: 
                CREATE umsatz. 
                ASSIGN
                    umsatz.artnr = depoart
                    umsatz.datum = curr-date
                . 
            END. 
            ASSIGN
                umsatz.betrag = umsatz.betrag + depo-amount
                umsatz.anzahl = umsatz.anzahl + 1
            . 
            RELEASE umsatz.

            /*Update NSBill-No in RSV Table to New Number*/
            FIND FIRST rsvtable-list WHERE RECID(rsvtable-list) EQ RECID(buffq33) EXCLUSIVE NO-ERROR.
            IF AVAILABLE rsvtable-list THEN
            DO:
                rsvtable-list.deci2 = nsbill-number.
                FIND CURRENT rsvtable-list NO-LOCK.
                RELEASE rsvtable-list.
            END.
        END.

        ok-flag = YES.
    END.    
END PROCEDURE.
