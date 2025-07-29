DEFINE TEMP-TABLE periode-list
    FIELD counter       AS INTEGER
    FIELD periode1      AS DATE
    FIELD periode2      AS DATE
    FIELD diff-day      AS INTEGER
    FIELD amt-periode   AS DECIMAL FORMAT "->>>,>>>,>>>,>>9.99"
    FIELD tamount       AS DECIMAL FORMAT "->>>,>>>,>>>,>>9.99"
.

DEFINE INPUT PARAMETER qrecid           AS INTEGER NO-UNDO.
DEFINE INPUT PARAMETER user-init        AS CHAR    NO-UNDO.


DEFINE VARIABLE log-artnr      AS INTEGER NO-UNDO.
DEFINE VARIABLE ar-ledger      AS INTEGER NO-UNDO.
DEFINE VARIABLE divered-rental AS INTEGER NO-UNDO.
DEFINE VARIABLE bill-date      AS DATE    NO-UNDO.
DEFINE VARIABLE tot-amount     AS DECIMAL NO-UNDO.
DEFINE VARIABLE tot-nettamount AS DECIMAL NO-UNDO.
DEFINE VARIABLE tot-serv       AS DECIMAL NO-UNDO.
DEFINE VARIABLE tot-tax        AS DECIMAL NO-UNDO.
DEFINE VARIABLE datum          AS DATE    NO-UNDO.

DEFINE VARIABLE netto    AS DECIMAL INITIAL 0. 
DEFINE VARIABLE service  AS DECIMAL INITIAL 0. 
DEFINE VARIABLE tax      AS DECIMAL INITIAL 0. 
DEFINE VARIABLE tax2     AS DECIMAL INITIAL 0. 
DEFINE VARIABLE serv     AS DECIMAL. 
DEFINE VARIABLE vat      AS DECIMAL. 
DEFINE VARIABLE vat2     AS DECIMAL. 
DEFINE VARIABLE fact     AS DECIMAL. 
DEFINE VARIABLE loopi    AS INTEGER NO-UNDO.
DEFINE VARIABLE serv-acctno AS CHAR NO-UNDO.
DEFINE VARIABLE vat-acctno  AS CHAR NO-UNDO.
DEFINE VARIABLE vat-fibu    AS CHAR. 
DEFINE VARIABLE vat2-fibu   AS CHAR. 
DEFINE VARIABLE serv-fibu   AS CHAR. 
DEFINE VARIABLE div-fibu    AS CHAR.
DEFINE VARIABLE del-mainres AS LOGICAL NO-UNDO.
DEFINE VARIABLE msg-str     AS CHAR    NO-UNDO.

DEFINE BUFFER bartikel FOR artikel.

DEFINE VARIABLE month-str1 AS INTEGER EXTENT 12 NO-UNDO
    INITIAL [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31].


DEFINE VARIABLE month-str2 AS INTEGER EXTENT 12 NO-UNDO
    INITIAL [31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31].


FIND FIRST htparam WHERE htparam.paramnr = 1051 NO-LOCK NO-ERROR.
IF AVAILABLE htparam THEN ASSIGN ar-ledger = htparam.finteger.

FIND FIRST htparam WHERE htparam.paramnr = 1052 NO-LOCK NO-ERROR.
IF AVAILABLE htparam THEN ASSIGN divered-rental = htparam.finteger.

FIND FIRST htparam WHERE htparam.paramnr = 110 NO-LOCK NO-ERROR.
IF AVAILABLE htparam THEN ASSIGN bill-date = htparam.fdate.

FIND FIRST htparam WHERE htparam.paramnr = 119 NO-LOCK NO-ERROR.
IF AVAILABLE htparam THEN log-artnr = htparam.finteger.

/********* default Account Number FOR SERVICE *******/ 
FIND FIRST htparam WHERE paramnr = 133 NO-LOCK. 
FIND FIRST artikel WHERE artikel.artnr = finteger 
  AND artikel.departement = 0 NO-LOCK NO-ERROR. 
IF AVAILABLE artikel THEN serv-acctno = artikel.fibukonto. 

/********* default Account Number FOR VAT *******/ 
FIND FIRST htparam WHERE paramnr = 132 NO-LOCK. 
FIND FIRST artikel WHERE artikel.artnr = finteger 
  AND artikel.departement = 0 NO-LOCK NO-ERROR. 
IF AVAILABLE artikel THEN vat-acctno = artikel.fibukonto. 

FOR EACH periode-list:
    DELETE periode-list.
END.

FIND FIRST queasy WHERE queasy.KEY = 329
    AND RECID(queasy) = qrecid
    AND queasy.char2 NE "" 
    AND queasy.logi1 = NO NO-LOCK NO-ERROR.
IF AVAILABLE queasy THEN DO:
    RUN calc-periode.

    FIND FIRST res-line WHERE res-line.resnr = queasy.number1
        AND res-line.reslinnr = queasy.number2 NO-LOCK NO-ERROR.
    IF AVAILABLE res-line THEN DO:
        FIND FIRST arrangement WHERE arrangement.arrangement = res-line.arrangement
            NO-LOCK NO-ERROR.
        IF AVAILABLE arrangement THEN ASSIGN log-artnr = arrangement.artnr-logis.

        FOR EACH reslin-queasy WHERE key = "arrangement"
          AND reslin-queasy.resnr = queasy.number1
          AND reslin-queasy.reslinnr = queasy.number2 NO-LOCK BY reslin-queasy.date1:
    
              FIND FIRST periode-list WHERE reslin-queasy.date1 GE periode-list.periode1 
                  AND reslin-queasy.date1 LE periode-list.periode2 NO-ERROR.
              IF AVAILABLE periode-list THEN DO:
    
                  ASSIGN service = 0
                         tax     = 0
                         tax2    = 0
                         netto   = 0                   
                    .
        
                 FIND FIRST artikel WHERE artikel.artnr = log-artnr NO-LOCK NO-ERROR.
                 IF AVAILABLE artikel THEN DO:
                    RUN calc-servtaxesbl.p (1, artikel.artnr, artikel.departement, datum, 
                                            OUTPUT serv, OUTPUT vat, OUTPUT vat2, OUTPUT fact).
                 END.
        
                 ASSIGN netto   = reslin-queasy.deci1 / fact
                        service = netto * serv
                        tax     = netto * vat
                        tax2    = netto * vat2
                 .
    
                 ASSIGN 
                     tot-nettamount = tot-nettamount + netto
                     tot-serv       = tot-serv + service
                     tot-tax        = tot-tax + tax
                     tot-amount     = tot-amount + reslin-queasy.deci1
                  .
    
              END.
        END.
       
        ASSIGN 
             tot-nettamount = ROUND(tot-nettamount, 0)
             tot-serv       = ROUND(tot-serv, 0)
             tot-tax        = ROUND(tot-tax, 0)
             tot-amount     = ROUND(tot-amount, 0)
          .
    
        RUN create-bill.
        RUN create-ar.
        /*RUN create-journal.*/

        FIND CURRENT queasy EXCLUSIVE-LOCK.
        ASSIGN queasy.logi1 = YES. /*indikator cancel*/
        FIND CURRENT queasy NO-LOCK.
        RELEASE queasy.
    END.
END.

PROCEDURE create-bill:
    DEFINE VARIABLE billnr AS INTEGER NO-UNDO.

    FIND FIRST counters WHERE counters.counter-no = 3 EXCLUSIVE-LOCK NO-ERROR. 
    IF NOT AVAILABLE counters THEN 
    DO: 
      CREATE counters. 
      ASSIGN 
        counters.counter-no = 3
        counters.counter-bez = "Counter for Bill No" 
      . 
    END. 
    ASSIGN
        counters.counter = counters.counter + 1
        billnr = counters.counter.

    FIND CURRENT counter NO-LOCK. 
    RELEASE counter.

    FIND FIRST res-line WHERE res-line.resnr = queasy.number1
        AND res-line.reslinnr = queasy.number2 NO-LOCK NO-ERROR.
    IF AVAILABLE res-line THEN DO:
        FIND FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK NO-ERROR.
        FIND FIRST guest WHERE guest.gastnr = res-line.gastnr NO-LOCK NO-ERROR.
        FIND FIRST bediener WHERE bediener.userinit = user-init NO-LOCK NO-ERROR. 

        CREATE bill. 
        ASSIGN 
          bill.flag        = 1
          bill.billnr      = 1 
          bill.rgdruck     = 1 
          bill.zinr        = res-line.zinr 
          bill.gastnr      = res-line.gastnrpay 
          bill.resnr       = res-line.resnr 
          bill.reslinnr    = res-line.reslinnr 
          bill.parent-nr   = res-line.reslinnr 
          bill.name        = guest.NAME 
          bill.kontakt-nr  = bediener.nr 
          bill.segmentcode = reservation.segmentcode
          bill.datum       = bill-date
          bill.rechnr      = billnr
        .

        RUN create-bill-line(billnr).
    END.
END.

PROCEDURE create-bill-line:
    DEFINE INPUT PARAMETER billno AS INTEGER NO-UNDO.

        FIND FIRST bartikel WHERE bartikel.artnr = divered-rental
            AND bartikel.departement = 0 NO-LOCK NO-ERROR.
        IF AVAILABLE bartikel THEN DO:
            CREATE bill-line.
            ASSIGN
                bill-line.rechnr        = billno
                bill-line.artnr         = divered-rental
                bill-line.anzahl        = 1
                bill-line.betrag        = - tot-amount
                bill-line.bezeich       = bartikel.bezeich
                bill-line.departement   = bartikel.departement 
                bill-line.zeit          = TIME
                bill-line.userinit      = user-init
                bill-line.bill-datum    = bill-date
                bill-line.bezeich       = bill-line.bezeich + "[" + "Cancel Service Apartment #" + STRING(queasy.number1) + "]"
                .
            RELEASE bill-line.
        END.


        FIND FIRST bartikel WHERE bartikel.artnr = ar-ledger
            AND bartikel.departement = 0 NO-LOCK NO-ERROR.
        IF AVAILABLE bartikel THEN DO:
            CREATE bill-line.
            ASSIGN
                bill-line.rechnr        = billno
                bill-line.artnr         = ar-ledger
                bill-line.anzahl        = 1
                bill-line.betrag        = tot-amount
                bill-line.bezeich       = bartikel.bezeich
                bill-line.departement   = bartikel.departement 
                bill-line.zeit          = TIME
                bill-line.userinit      = user-init
                bill-line.bill-datum    = bill-date
                bill-line.bezeich       = bill-line.bezeich + "[" + "Cancel Service Apartment #" + STRING(queasy.number1) + "]"
                .
            RELEASE bill-line.
        END.
END.


PROCEDURE create-ar:
    DEFINE BUFFER bdebt FOR debitor.

    FIND FIRST debitor WHERE debitor.vesrcod = queasy.char2
        AND debitor.zahlkonto = 0 NO-LOCK NO-ERROR.
    IF AVAILABLE debitor THEN DO:
        FIND FIRST bediener WHERE bediener.userinit EQ user-init NO-LOCK. 
        CREATE bdebt. 
        ASSIGN
          bdebt.artnr         = ar-ledger       
          bdebt.rechnr        = INTEGER(queasy.char2)
          bdebt.rgdatum       = bill-date 
          bdebt.saldo         = - tot-amount
          bdebt.vesrdep       = - tot-amount
          bdebt.bediener-nr   = bediener.nr
          bdebt.vesrdat       = TODAY
          bdebt.transzeit     = TIME
          /*debitor.verstat       = 9 /* AR manual 19/08/2010 */*/
          bdebt.vesrcod       = queasy.char2 + "|Cancel Service Apartment"
        . 
    
        FIND FIRST res-line WHERE res-line.resnr = queasy.number1
            AND res-line.reslinnr = queasy.number2 NO-LOCK NO-ERROR.
        IF AVAILABLE res-line THEN DO:
            FIND FIRST guest WHERE guest.gastnr = res-line.gastnr NO-LOCK NO-ERROR.
            IF AVAILABLE guest THEN 
                ASSIGN bdebt.NAME          = guest.NAME
                       bdebt.gastnr        = res-line.gastnr
                       bdebt.gastnrmember  = res-line.gastnrmember.    
        END.
    END.

    /*create billjournal dan Umsatz*/
    FIND FIRST artikel WHERE artikel.artnr = ar-ledger
        AND artikel.departement = 0 NO-LOCK NO-ERROR.
    IF NOT AVAILABLE artikel THEN RETURN.

    CREATE billjournal. 
    ASSIGN 
        billjournal.artnr           = ar-ledger 
        billjournal.anzahl          = 1 
        billjournal.fremdwaehrng    = tot-amount
        billjournal.betrag          = tot-amount
        billjournal.bezeich         = artikel.bezeich + "[" + "Cancel Service Apartment#" + STRING(queasy.number1) + "]"          
        billjournal.epreis          = 0 
        billjournal.zeit            = TIME 
        billjournal.billjou-ref     = artikel.artnr 
        billjournal.userinit        = user-init
        billjournal.bill-datum      = bill-date.
    FIND CURRENT billjournal NO-LOCK. 
    RELEASE billjournal.

    FIND FIRST umsatz WHERE umsatz.artnr EQ ar-ledger
        AND umsatz.departement EQ 0 
        AND umsatz.datum EQ bill-date EXCLUSIVE-LOCK NO-ERROR. 
    IF NOT AVAILABLE umsatz THEN 
    DO: 
        CREATE umsatz. 
        ASSIGN
            umsatz.artnr = ar-ledger
            umsatz.datum = bill-date
        . 
    END. 
    ASSIGN
        umsatz.anzahl = umsatz.anzahl + 1
        umsatz.betrag = umsatz.betrag + tot-amount          
        . 
    FIND CURRENT umsatz NO-LOCK. 
    RELEASE umsatz.

    FIND FIRST artikel WHERE artikel.artnr = divered-rental
        AND artikel.departement = 0 NO-LOCK NO-ERROR.
    IF NOT AVAILABLE artikel THEN RETURN.

    CREATE billjournal. 
    ASSIGN 
        billjournal.artnr           = divered-rental 
        billjournal.anzahl          = 1 
        billjournal.fremdwaehrng    = - tot-amount
        billjournal.betrag          = - tot-amount
        billjournal.bezeich         = artikel.bezeich + "[" + "Cancel Service Apartment#" + STRING(queasy.number1) + "]"          
        billjournal.epreis          = 0 
        billjournal.zeit            = TIME 
        billjournal.billjou-ref     = artikel.artnr 
        billjournal.userinit        = user-init
        billjournal.bill-datum      = bill-date.
    FIND CURRENT billjournal NO-LOCK. 
    RELEASE billjournal.

    FIND FIRST umsatz WHERE umsatz.artnr EQ divered-rental
        AND umsatz.departement EQ 0 
        AND umsatz.datum EQ bill-date EXCLUSIVE-LOCK NO-ERROR. 
    IF NOT AVAILABLE umsatz THEN 
    DO: 
        CREATE umsatz. 
        ASSIGN
            umsatz.artnr = divered-rental
            umsatz.datum = bill-date
        . 
    END. 
    ASSIGN
        umsatz.anzahl = umsatz.anzahl + 1
        umsatz.betrag = umsatz.betrag + ( - tot-amount)          
        . 
    FIND CURRENT umsatz NO-LOCK. 
    RELEASE umsatz.

END.

PROCEDURE create-journal:
    DEFINE VARIABLE gname AS CHAR NO-UNDO.

    FIND FIRST counters WHERE counters.counter-no = 25 EXCLUSIVE-LOCK NO-ERROR. 
    IF NOT AVAILABLE counters THEN 
    DO: 
        CREATE counters. 
        counters.counter-no = 25. 
        counters.counter-bez = "G/L Transaction Journal". 
    END. 
    counters.counter = counters.counter + 1. 
    FIND CURRENT counter NO-LOCK. 

    FIND FIRST res-line WHERE res-line.resnr = queasy.number1
        AND res-line.reslinnr = queasy.number2 NO-LOCK NO-ERROR.
    IF AVAILABLE res-line THEN DO:
        FIND FIRST guest WHERE guest.gastnr = res-line.gastnr NO-LOCK NO-ERROR.
        IF AVAILABLE guest THEN ASSIGN gname = guest.NAME.
    END.
    
    CREATE gl-jouhdr. 
    ASSIGN 
        gl-jouhdr.jnr       = counters.counter 
        gl-jouhdr.refno     = "CANCEL-" + STRING(queasy.number1) + "-" + STRING(bill-date)
        gl-jouhdr.datum     = bill-date         
        gl-jouhdr.batch     = YES 
        gl-jouhdr.jtype     = 1
        . 
    FIND FIRST guest WHERE guest.gastnr = queasy.number2 NO-LOCK NO-ERROR.
    IF AVAILABLE guest THEN ASSIGN gl-jouhdr.bezeich  = "CANCEL-SERVICE RESIDENT-" + STRING(queasy.number1) + "-" + STRING(bill-date).

    
    CREATE gl-journal. 
    ASSIGN 
        gl-journal.jnr          = gl-jouhdr.jnr         
        gl-journal.userinit     = user-init 
        gl-journal.zeit         = TIME 
        gl-journal.bemerk       = gl-jouhdr.bezeich
        gl-journal.credit       = tot-amount. 

    
    FIND FIRST artikel WHERE artikel.artnr = ar-ledger
        AND artikel.departement = 0 NO-LOCK NO-ERROR.
    IF AVAILABLE artikel THEN ASSIGN gl-journal.fibukonto    = artikel.fibukonto.
    
    ASSIGN
        gl-jouhdr.credit = gl-jouhdr.credit + gl-journal.credit
        gl-jouhdr.debit = gl-jouhdr.debit + gl-journal.debit.

    FIND FIRST artikel WHERE artikel.artnr = divered-rental
        AND artikel.departement = 0 NO-LOCK NO-ERROR.
    IF AVAILABLE artikel THEN DO:
        ASSIGN div-fibu = artikel.fibukonto.

          IF artikel.service-code NE 0 THEN 
          DO: 
              FIND FIRST htparam WHERE htparam.paramnr = artikel.service-code NO-LOCK. 
              IF AVAILABLE htparam THEN serv-fibu = ENTRY(1, htparam.fchar, CHR(2)). 
          END. 
          IF artikel.mwst-code NE 0 THEN 
          DO: 
              FIND FIRST htparam WHERE htparam.paramnr = artikel.mwst-code NO-LOCK. 
              IF AVAILABLE htparam THEN vat-fibu = ENTRY(1, htparam.fchar, CHR(2)). 
          END.            
          IF artikel.prov-code NE 0 THEN 
          DO: 
              FIND FIRST htparam WHERE htparam.paramnr = artikel.prov-code NO-LOCK. 
              IF AVAILABLE htparam THEN 
              DO:    
                  vat2-fibu = ENTRY(1, htparam.fchar, CHR(2)).                  
              END.
          END.       
    END.

    DO loopi = 1 TO 3:
        CREATE gl-journal. 
        ASSIGN 
             gl-journal.jnr         = gl-jouhdr.jnr              
             gl-journal.userinit    = user-init 
             gl-journal.zeit        = TIME 
             gl-journal.bemerk      = gl-jouhdr.bezeich             
           . 

        IF loopi = 1 THEN
            ASSIGN gl-journal.debit       = tot-nettamount
                   gl-journal.fibukonto   = div-fibu .
        ELSE IF loopi = 2 THEN
            ASSIGN gl-journal.debit     = tot-serv
                   gl-journal.fibukonto = serv-fibu.
        ELSE IF loopi = 3 THEN
            ASSIGN gl-journal.debit     = tot-tax
                   gl-journal.fibukonto = vat-fibu.

        gl-jouhdr.credit = gl-jouhdr.credit + gl-journal.credit. 
        gl-jouhdr.debit = gl-jouhdr.debit + gl-journal.debit. 
        FIND CURRENT gl-journal NO-LOCK. 
     END.
     FIND CURRENT gl-jouhdr NO-LOCK.
END.



PROCEDURE calc-periode:
    DEFINE VARIABLE periode-rsv1 AS DATE NO-UNDO.
    DEFINE VARIABLE periode-rsv2 AS DATE NO-UNDO.
    DEFINE VARIABLE counter      AS INTEGER NO-UNDO.
    DEFINE VARIABLE periode      AS DATE NO-UNDO.
    DEFINE VARIABLE loopi        AS DATE NO-UNDO.
    DEFINE VARIABLE curr-amount  AS DECIMAL NO-UNDO.
    DEFINE VARIABLE loopdate     AS DATE NO-UNDO.


    DO:
        ASSIGN periode-rsv1 = queasy.date2
               periode-rsv2 = queasy.date3
         .


        IF MONTH(periode-rsv1) + 1 GT 12 THEN
            ASSIGN periode = DATE(1, DAY(periode-rsv1), YEAR(periode-rsv1) + 1) - 1.
        ELSE IF MONTH(periode-rsv1) + 1 = 2 THEN DO:
            IF DAY(periode-rsv1) GE 29 THEN DO:
                IF YEAR(periode-rsv1) MOD 4 NE 0 THEN
                    ASSIGN periode = DATE(MONTH(periode-rsv1) + 1, month-str1[MONTH(periode-rsv1) + 1], YEAR(periode-rsv1)).
                ELSE IF YEAR(periode-rsv1) MOD 4 = 0 THEN
                    ASSIGN periode = DATE(MONTH(periode-rsv1) + 1, month-str2[MONTH(periode-rsv1) + 1], YEAR(periode-rsv1)).
             END.
             ELSE ASSIGN periode = DATE(MONTH(periode-rsv1) + 1, DAY(periode-rsv1), YEAR(periode-rsv1)) - 1.
        END.
        ELSE DO: 
            ASSIGN periode = DATE(MONTH(periode-rsv1) + 1, DAY(periode-rsv1), YEAR(periode-rsv1)) - 1.
        END.
        
        DO loopi = periode-rsv1 TO periode-rsv2 - 1:
            IF loopi GT periode THEN DO:
                ASSIGN periode-rsv1 = loopi.
        
                
                IF MONTH(periode-rsv1) + 1 GT 12 THEN
                    ASSIGN periode = DATE(1, DAY(periode-rsv1), YEAR(periode-rsv1) + 1) - 1.
                ELSE IF MONTH(periode-rsv1) + 1 = 2 THEN DO:
                    IF DAY(periode-rsv1) GE 29 THEN DO:
                        IF YEAR(periode-rsv1) MOD 4 NE 0 THEN
                            ASSIGN periode = DATE(MONTH(periode-rsv1) + 1, month-str1[MONTH(periode-rsv1) + 1], YEAR(periode-rsv1)).
                        ELSE IF YEAR(periode-rsv1) MOD 4 = 0 THEN
                            ASSIGN periode = DATE(MONTH(periode-rsv1) + 1, month-str2[MONTH(periode-rsv1) + 1], YEAR(periode-rsv1)).
                     END.
                     ELSE ASSIGN periode = DATE(MONTH(periode-rsv1) + 1, DAY(periode-rsv1), YEAR(periode-rsv1)) - 1.
                END.
                ELSE DO: 
                    ASSIGN periode = DATE(MONTH(periode-rsv1) + 1, DAY(periode-rsv1), YEAR(periode-rsv1)) - 1.
                END.
            END.

             
        
            IF loopi LE periode THEN DO:
                FIND FIRST periode-list WHERE periode-list.periode1 = periode-rsv1 NO-ERROR.
                IF NOT AVAILABLE periode-list THEN DO:
                   CREATE periode-list.
                   ASSIGN periode-list.periode1 = periode-rsv1
                          counter               = counter + 1
                          periode-list.counter  = counter.
                END. 
                ASSIGN periode-list.periode2 = loopi.
            END.   
        END.
        
        FOR EACH periode-list:
            
            ASSIGN curr-amount = 0.
            DO loopdate = periode-list.periode1 TO periode-list.periode2:
                FIND FIRST reslin-queasy WHERE reslin-queasy.key  = "arrangement"
                    AND reslin-queasy.resnr       = queasy.number1
                    AND reslin-queasy.reslinnr    = queasy.number2
                    AND reslin-queasy.date1 LE loopdate
                    AND reslin-queasy.date2 LE loopdate NO-LOCK NO-ERROR.
                IF AVAILABLE reslin-queasy THEN DO:
                    ASSIGN curr-amount = curr-amount + reslin-queasy.deci1.
                END.
            END.


            ASSIGN periode-list.diff-day    = (periode-list.periode2 - periode-list.periode1) + 1
                   periode-list.amt-periode = curr-amount / periode-list.diff-day
                   periode-list.tamount     = periode-list.amt-periode * periode-list.diff-day.

        END.
    END.
END.

