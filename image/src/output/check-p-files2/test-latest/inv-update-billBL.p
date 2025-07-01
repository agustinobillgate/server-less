

DEFINE TEMP-TABLE t-bill-line       LIKE bill-line
    FIELD bl-recid  AS INTEGER
    FIELD artart    AS INTEGER
    FIELD tool-tip  AS CHAR
.

DEF INPUT PARAMETER pvILanguage      AS INTEGER    NO-UNDO.
DEF INPUT PARAMETER bil-flag         AS INTEGER    NO-UNDO.
DEF INPUT PARAMETER invoice-type     AS CHAR       NO-UNDO.
DEF INPUT PARAMETER transdate        AS DATE       NO-UNDO.
DEF INPUT PARAMETER r-recid          AS INTEGER    NO-UNDO. 
DEF INPUT PARAMETER deptno           AS INTEGER    NO-UNDO.
DEF INPUT PARAMETER billart          AS INTEGER    NO-UNDO.
DEF INPUT PARAMETER qty              AS INTEGER    NO-UNDO.
DEF INPUT PARAMETER price            AS DECIMAL    NO-UNDO.
DEF INPUT PARAMETER amount           AS DECIMAL    NO-UNDO.
DEF INPUT PARAMETER amount-foreign   AS DECIMAL    NO-UNDO.
DEF INPUT PARAMETER DESCRIPTION      AS CHAR       NO-UNDO.
DEF INPUT PARAMETER voucher-nr       AS CHAR       NO-UNDO.
DEF INPUT PARAMETER cancel-str       AS CHAR       NO-UNDO.
DEF INPUT PARAMETER user-init        AS CHAR       NO-UNDO.

DEF INPUT-OUTPUT PARAMETER billno        AS INTEGER    NO-UNDO.
DEF INPUT-OUTPUT PARAMETER master-str    AS CHAR       NO-UNDO.
DEF INPUT-OUTPUT PARAMETER master-rechnr AS CHAR       NO-UNDO.
DEF INPUT-OUTPUT PARAMETER balance       AS DECIMAL    NO-UNDO.
DEF INPUT-OUTPUT PARAMETER balance-foreign AS DECIMAL  NO-UNDO.

DEF OUTPUT PARAMETER master-flag         AS LOGICAL INIT NO  NO-UNDO.  
DEF OUTPUT PARAMETER msg-str             AS CHAR INIT ""     NO-UNDO.
DEF OUTPUT PARAMETER success-flag        AS LOGICAL INIT YES NO-UNDO.
DEF OUTPUT PARAMETER TABLE FOR t-bill-line.

DEF VAR gastnrmember    AS INTEGER          NO-UNDO.
DEF VAR price-decimal   AS INTEGER          NO-UNDO.
DEF VAR double-currency AS LOGICAL          NO-UNDO.
DEF VAR foreign-rate    AS LOGICAL          NO-UNDO.
DEF VAR exchg-rate      AS DECIMAL INIT 1   NO-UNDO.
DEF VAR currZeit        AS INTEGER          NO-UNDO.
DEF VAR bill-date       AS DATE             NO-UNDO. 
DEF VAR curr-room       AS CHAR             NO-UNDO.

DEF BUFFER resline FOR res-line.

{SupertransBL.i} 
DEF VAR lvCAREA AS CHAR INITIAL "fo-invoice". 


FIND FIRST htparam WHERE htparam.paramnr = 491 NO-LOCK. 
price-decimal = htparam.finteger. 
 
FIND FIRST htparam WHERE paramnr = 240 NO-LOCK. 
double-currency = htparam.flogical. 

FIND FIRST htparam WHERE htparam.paramnr = 143 NO-LOCK. 
foreign-rate = htparam.flogical. 
IF foreign-rate OR double-currency THEN 
DO: 
  FIND FIRST htparam WHERE htparam.paramnr = 144 NO-LOCK. 
  FIND FIRST waehrung WHERE waehrung.wabkurz = htparam.fchar NO-LOCK NO-ERROR. 
  IF AVAILABLE waehrung THEN exchg-rate = waehrung.ankauf / waehrung.einheit. 
END. 

ASSIGN
  currZeit    = TIME
  master-flag = NO
.

RUN update-bill.

PROCEDURE update-bill: 
DEF BUFFER buf-artikel FOR artikel.
DEF BUFFER buf-bill-line FOR bill-line.
DEF VAR skip-it AS LOGICAL.    
  FIND FIRST artikel WHERE artikel.artnr = billart
      AND artikel.departement = deptno NO-LOCK NO-ERROR.
  IF NOT AVAILABLE artikel THEN
  FIND FIRST artikel WHERE artikel.artnr = billart
      AND artikel.departement = 0 
      AND (artikel.artart = 2 OR artikel.artart = 6
        OR artikel.artart = 7) 
      AND artikel.activeflag NO-LOCK NO-ERROR.

  FIND FIRST vhp.htparam WHERE vhp.htparam.paramnr = 110 NO-LOCK NO-ERROR. 
  bill-date = vhp.htparam.fdate. 
  IF transdate NE ? THEN bill-date = transdate. 
  ELSE
  DO:
    FIND FIRST htparam WHERE paramnr = 253 NO-LOCK NO-ERROR. 
    IF htparam.flogical AND bill-date LT TODAY THEN bill-date = bill-date + 1. 
  END.
  
  IF amount-foreign = ? THEN amount-foreign = 0.

  FIND FIRST bill WHERE RECID(bill) = r-recid NO-LOCK NO-ERROR. 
  /* Rulita 101224 | Fixing serverless issue 235 */
  IF AVAILABLE bill THEN                                  
  DO:
    IF bill.flag = 1 AND bil-flag = 0 THEN 
    DO: 
      msg-str = translateExtended ("The Bill was closed / guest checked out",lvCAREA,"") + CHR(10)
              + translateExtended ("Bill entry is no longer possible!",lvCAREA,""). 
      success-flag = NO.
      RETURN. 
    END. 
  
    /*MT 09/09/13 */
    IF artikel.artart = 9 AND artikel.artgrp = 0 THEN
    DO: 
        skip-it = YES.
        FIND FIRST res-line WHERE res-line.resnr = bill.resnr 
            AND res-line.reslinnr = bill.reslinnr NO-LOCK NO-ERROR. 
        FIND FIRST arrangement WHERE arrangement.arrangement = res-line.arrangement 
            NO-LOCK. 
        FIND FIRST buf-artikel WHERE buf-artikel.artnr = arrangement.argt-artikelnr 
            AND buf-artikel.departement = 0 NO-LOCK. 

        FIND FIRST buf-bill-line WHERE buf-bill-line.departement = 0
            AND buf-bill-line.artnr = buf-artikel.artnr
            AND buf-bill-line.bill-datum = bill-date
            AND buf-bill-line.zinr NE ""
            AND buf-bill-line.massnr = res-line.resnr
            AND buf-bill-line.billin-nr = res-line.reslinnr
            USE-INDEX dep-art-dat_ix NO-LOCK NO-ERROR.
        skip-it = AVAILABLE buf-bill-line.
        
        IF skip-it THEN
        DO:
            success-flag = NO.
            msg-str = translateExtended ("Not possible",lvCAREA,"") 
                    + CHR(10)
                    + translateExtended ("Room Charge Already Posted",lvCAREA,"") 
                    + " to bill no " + STRING(buf-bill-line.rechnr).
            /*MT
            RUN clear-bill-entry.
            */
            RETURN.
        END.
    END.

    DO TRANSACTION: 
      
      FIND CURRENT bill EXCLUSIVE-LOCK. 
      ASSIGN 
          curr-room    = bill.zinr
          gastnrmember = bill.gastnr
      .

      /*MT
      FIND FIRST artikel WHERE artikel.artnr = billart
          AND artikel.departement = deptno NO-LOCK.
      */

      IF invoice-type = "guest" THEN 
      DO:
        IF bill.flag = 0 THEN
          RUN update-masterbill(currZeit, OUTPUT master-flag). 
        IF master-flag THEN RETURN.
        FIND FIRST res-line WHERE res-line.resnr = bill.resnr 
          AND res-line.reslinnr = bill.reslinnr NO-LOCK NO-ERROR. 
        IF AVAILABLE res-line THEN gastnrmember = res-line.gastnrmember. 
      END.

      IF artikel.umsatzart = 1 
        THEN bill.logisumsatz = bill.logisumsatz + amount. 
      ELSE IF artikel.umsatzart = 2 
        THEN bill.argtumsatz = bill.argtumsatz + amount. 
      ELSE IF (artikel.umsatzart = 3 OR artikel.umsatzart = 5 
        OR artikel.umsatzart = 6) 
        THEN bill.f-b-umsatz = bill.f-b-umsatz + amount. 
      ELSE IF artikel.umsatzart = 4 
        THEN bill.sonst-umsatz = bill.sonst-umsatz + amount. 
      IF artikel.umsatzart GE 1 AND artikel.umsatzart LE 4 THEN 
        bill.gesamtumsatz = bill.gesamtumsatz + amount. 
  
      IF NOT artikel.autosaldo THEN bill.rgdruck = 0. 
  
      IF bill.datum LT bill-date OR bill.datum = ? THEN bill.datum = bill-date. 
      bill.saldo = bill.saldo + amount. 
      IF double-currency OR foreign-rate 
        THEN bill.mwst[99] = bill.mwst[99] + amount-foreign. 
      IF bill.rechnr = 0 THEN 
      DO: 
        FIND FIRST counters WHERE counters.counter-no = 3 EXCLUSIVE-LOCK. 
        counters.counter = counters.counter + 1. 
        bill.rechnr = counters.counter. 
        IF transdate NE ? THEN bill.datum = transdate. 
        FIND CURRENT counter NO-LOCK. 
      END. 
      ASSIGN billno = bill.rechnr. 
  
      create bill-line. 
      ASSIGN
        bill-line.rechnr       = bill.rechnr
        bill-line.massnr       = bill.resnr
        bill-line.billin-nr    = bill.reslinnr
        bill-line.zinr         = curr-room
        bill-line.artnr        = billart
        bill-line.anzahl       = qty
        bill-line.betrag       = amount 
        bill-line.fremdwbetrag = amount-foreign
        bill-line.bezeich      = DESCRIPTION
        bill-line.departement  = artikel.departement 
        bill-line.zeit         = TIME
        bill-line.userinit     = user-init 
        bill-line.bill-datum   = bill-date
      . 
      
      IF voucher-nr NE "" THEN bill-line.bezeich = bill-line.bezeich 
        + "/" + voucher-nr. 
      
      IF artikel.artart NE 2 AND artikel.artart NE 4 AND artikel.artart NE 6 
        AND artikel.artart NE 7 THEN bill-line.epreis = price. 
  
      IF artikel.artart = 9 THEN 
      DO:
        FIND FIRST arrangement WHERE arrangement.argt-artikelnr 
          = artikel.artnr NO-LOCK NO-ERROR.
        IF AVAILABLE arrangement AND AVAILABLE res-line THEN 
          bill-line.epreis = res-line.zipreis. 
      END.

      IF AVAILABLE res-line THEN 
      ASSIGN 
        bill-line.massnr      = res-line.resnr
        bill-line.billin-nr   = res-line.reslinnr 
        bill-line.arrangement = res-line.arrangement
      . 

      IF artikel.artart = 9 AND artikel.artgrp = 0 AND AVAILABLE res-line THEN 
      DO: 
        FIND FIRST arrangement WHERE 
          arrangement.arrangement = res-line.arrangement NO-LOCK NO-ERROR. 
        bill-line.bezeich = arrangement.argt-rgbez. 
      END. 

      FIND CURRENT bill-line NO-LOCK. 
  
      CREATE t-bill-line.
      BUFFER-COPY bill-line TO t-bill-line.
      ASSIGN 
          t-bill-line.artart   = artikel.artart
          t-bill-line.bl-recid = INTEGER(RECID(bill-line))
      .

      FIND FIRST umsatz WHERE umsatz.artnr = billart 
        AND umsatz.departement = artikel.departement 
        AND umsatz.datum = bill-date EXCLUSIVE-LOCK NO-ERROR. 
      IF NOT AVAILABLE umsatz THEN 
      DO: 
        CREATE umsatz.
        ASSIGN
          umsatz.artnr       = billart 
          umsatz.datum       = bill-date 
          umsatz.departement = artikel.departement
        . 
      END.
      ASSIGN
        umsatz.betrag = umsatz.betrag + amount
        umsatz.anzahl = umsatz.anzahl + qty
      . 
      FIND CURRENT umsatz NO-LOCK. 
  
      CREATE billjournal. 
      ASSIGN
        billjournal.rechnr       = bill.rechnr
        billjournal.zinr         = curr-room
        billjournal.artnr        = billart
        billjournal.anzahl       = qty
        billjournal.fremdwaehrng = amount-foreign 
        billjournal.betrag       = amount
        billjournal.bezeich      = DESCRIPTION
        billjournal.departement  = artikel.departement 
        billjournal.epreis       = price
        billjournal.zeit         = TIME
        billjournal.stornogrund  = cancel-str 
        billjournal.userinit     = user-init 
        billjournal.bill-datum   = bill-date
      . 
      
      IF voucher-nr NE "" THEN billjournal.bezeich = billjournal.bezeich 
        + "/" + voucher-nr. 
      FIND CURRENT billjournal NO-LOCK. 
  
      IF artikel.artart = 2 OR artikel.artart = 7 THEN 
      DO:
        IF invoice-type = "master" THEN
        DO:
          FIND FIRST resline WHERE resline.resnr = bill.resnr 
            AND (resline.resstatus = 6 OR resline.resstatus = 8) NO-LOCK NO-ERROR. 
          IF AVAILABLE resline THEN gastnrmember = resline.gastnrmember.
        END.
        RUN inv-ar(billart, "", bill.gastnr, gastnrmember, bill.rechnr, 
          amount, amount-foreign, bill-date, bill.name, user-init, voucher-nr, deptno). 
      END.
      ELSE IF artikel.artart = 9 THEN
      DO:     
        IF artikel.artgrp = 0 THEN RUN rev-bdown(currZeit).
        ELSE RUN rev-bdown1(currZeit).
      END.
      balance = bill.saldo. 
      IF double-currency OR foreign-rate THEN balance-foreign = bill.mwst[99]. 
      
      FIND CURRENT bill NO-LOCK. 

    END. 
  END. 
  /* End Rulita */
END. 
 
PROCEDURE rev-bdown:
DEFINE INPUT PARAMETER currZeit AS INTEGER.

DEFINE VARIABLE service         AS DECIMAL. 
DEFINE VARIABLE vat             AS DECIMAL. 
DEFINE VARIABLE service-foreign AS DECIMAL. 
DEFINE VARIABLE vat-foreign     AS DECIMAL. 
DEFINE VARIABLE rest-betrag     AS DECIMAL. 
DEFINE VARIABLE argt-betrag     AS DECIMAL. 
DEFINE VARIABLE frate           AS DECIMAL. 
DEFINE VARIABLE ex-rate         AS DECIMAL. 

DEFINE VARIABLE p-sign          AS INTEGER INITIAL 1 NO-UNDO. 
DEFINE VARIABLE qty1            AS INTEGER NO-UNDO. 

DEFINE VARIABLE rm-vat          AS LOGICAL. 
DEFINE VARIABLE rm-serv         AS LOGICAL. 

DEFINE BUFFER artikel1 FOR artikel. 
 
  FIND FIRST htparam WHERE htparam.paramnr = 127 NO-LOCK. 
  rm-vat = NOT htparam.flogical. 
  FIND FIRST htparam WHERE htparam.paramnr = 128 NO-LOCK. 
  rm-serv = NOT htparam.flogical. 
 
  FIND FIRST res-line WHERE res-line.resnr = bill.resnr 
    AND res-line.reslinnr = bill.parent-nr NO-LOCK NO-ERROR. 
  IF AVAILABLE res-line THEN
  DO:
    IF res-line.adrflag THEN frate = 1. 
    ELSE IF res-line.reserve-dec NE 0 THEN frate = res-line.reserve-dec. 
  END.
  ELSE frate = exchg-rate. 
 
  rest-betrag = amount. 
  IF amount LT 0 THEN p-sign = -1. 
 
  FOR EACH argt-line WHERE argt-line.argtnr = arrangement.argtnr 
    AND NOT argt-line.kind2 NO-LOCK:  /* kind2 = YES => fix cost e.g extrabed */ 
    RUN argt-betrag.p(RECID(res-line), RECID(argt-line), 
      OUTPUT argt-betrag, OUTPUT ex-rate). 
    argt-betrag = round(argt-betrag * ex-rate, price-decimal). 
    rest-betrag = rest-betrag - argt-betrag * p-sign. 

    IF argt-betrag NE 0 THEN 
    DO: 
      IF argt-line.betriebsnr = 0 THEN qty1 = res-line.erwachs * p-sign. 
      ELSE qty1 = argt-line.betriebsnr * p-sign. 
 
      FIND FIRST artikel1 WHERE artikel1.artnr = argt-line.argt-artnr 
        AND artikel1.departement = argt-line.departement NO-LOCK. 
      FIND FIRST umsatz WHERE umsatz.artnr = artikel1.artnr 
        AND umsatz.departement = artikel1.departement 
        AND umsatz.datum = bill-date EXCLUSIVE-LOCK NO-ERROR. 
      IF NOT AVAILABLE umsatz THEN 
      DO: 
        CREATE umsatz.
        ASSIGN
          umsatz.artnr = artikel1.artnr
          umsatz.datum = bill-date
          umsatz.departement = artikel1.departement
        . 
      END.
      ASSIGN
        umsatz.betrag = umsatz.betrag + argt-betrag * p-sign
        umsatz.anzahl = umsatz.anzahl + qty1
      . 
      FIND CURRENT umsatz NO-LOCK. 
      CREATE billjournal. 
      ASSIGN
        billjournal.rechnr = bill.rechnr
        billjournal.artnr = artikel1.artnr 
        billjournal.anzahl = qty1
        billjournal.fremdwaehrng = argt-line.betrag * p-sign
        billjournal.betrag = argt-betrag * p-sign
        billjournal.bezeich = artikel1.bezeich
        billjournal.zinr = curr-room
        billjournal.departement = artikel1.departement
        billjournal.epreis = 0
        billjournal.zeit = currZeit
        billjournal.stornogrund = cancel-str 
        billjournal.userinit = user-init
        billjournal.bill-datum = bill-date
      . 
      FIND CURRENT billjournal NO-LOCK. 
    END. 
  END. 
 
  FIND FIRST artikel1 WHERE artikel1.artnr = arrangement.artnr-logis 
    AND artikel1.departement = 0 NO-LOCK. 
  FIND FIRST umsatz WHERE umsatz.artnr = artikel1.artnr 
    AND umsatz.departement = artikel1.departement 
    AND umsatz.datum = bill-date EXCLUSIVE-LOCK NO-ERROR. 
  IF NOT AVAILABLE umsatz THEN 
  DO: 
    CREATE umsatz. 
    ASSIGN
      umsatz.artnr = artikel1.artnr
      umsatz.datum = bill-date
      umsatz.departement = artikel1.departement
    . 
  END.
  ASSIGN
    umsatz.betrag = umsatz.betrag + rest-betrag
    umsatz.anzahl = umsatz.anzahl + qty
  . 
  FIND CURRENT umsatz NO-LOCK. 
  
  CREATE billjournal. 
  ASSIGN
    billjournal.rechnr = bill.rechnr 
    billjournal.artnr = artikel1.artnr 
    billjournal.anzahl = qty
    billjournal.betrag = rest-betrag 
    billjournal.bezeich = artikel1.bezeich 
    billjournal.zinr = curr-room
    billjournal.departement = artikel1.departement 
    billjournal.epreis = 0
    billjournal.zeit = currZeit 
    billjournal.stornogrund = cancel-str 
    billjournal.userinit = user-init
    billjournal.bill-datum = bill-date
  . 
  IF double-currency THEN 
    billjournal.fremdwaehrng = round(rest-betrag / exchg-rate, 6). 
  FIND CURRENT billjournal NO-LOCK. 
 
  IF rm-serv AND artikel.service-code NE 0 THEN 
  DO: 
    FIND FIRST htparam WHERE htparam.paramnr = artikel.service-code NO-LOCK. 
    IF AVAILABLE htparam AND htparam.fdecimal NE 0 THEN 
    DO: 
      service = htparam.fdecimal. 
      FIND FIRST htparam WHERE htparam.paramnr = 133 NO-LOCK. 
      FIND FIRST artikel1 WHERE artikel1.artnr = htparam.finteger 
        AND artikel1.departement = 0 NO-LOCK. 
      ASSIGN
        service = service * price / 100
        service-foreign = round(service, 2) * qty
      . 
      IF double-currency THEN 
        service = round(service * exchg-rate, price-decimal) * qty. 
      ELSE service = round(service, price-decimal) * qty. 
 
      IF artikel1.umsatzart = 1 THEN
      ASSIGN
        bill.logisumsatz = bill.logisumsatz + service
        bill.argtumsatz = bill.argtumsatz + service
      . 
      ELSE IF artikel1.umsatzart = 2 
        THEN bill.argtumsatz = bill.argtumsatz + service. 
      ELSE IF (artikel1.umsatzart = 3 OR artikel1.umsatzart = 5 
        OR artikel1.umsatzart = 6) 
        THEN bill.f-b-umsatz = bill.f-b-umsatz + service. 
      ELSE IF artikel1.umsatzart = 4 
        THEN bill.sonst-umsatz = bill.sonst-umsatz + service. 
      IF artikel1.umsatzart GE 1 AND artikel1.umsatzart LE 4 THEN 
        bill.gesamtumsatz = bill.gesamtumsatz + service. 
 
      CREATE bill-line. 
      ASSIGN
        bill-line.rechnr = bill.rechnr
        bill-line.artnr = artikel1.artnr
        bill-line.bezeich = artikel1.bezeich
        bill-line.anzahl = qty
        bill-line.fremdwbetrag = service-foreign 
        bill-line.betrag = service
        bill-line.zinr = curr-room 
        bill-line.departement = artikel1.departement 
        bill-line.epreis = 0
        bill-line.zeit = currZeit + 1 
        bill-line.userinit = user-init 
        bill-line.bill-datum = bill-date
      .
      IF AVAILABLE res-line THEN bill-line.arrangement = res-line.arrangement. 
      FIND CURRENT bill-line NO-LOCK. 
 
      FIND FIRST umsatz WHERE umsatz.artnr = artikel1.artnr 
        AND umsatz.departement = artikel1.departement 
        AND umsatz.datum = bill-date EXCLUSIVE-LOCK NO-ERROR. 
      IF NOT AVAILABLE umsatz THEN 
      DO: 
        CREATE umsatz. 
        ASSIGN
          umsatz.artnr = artikel1.artnr
          umsatz.datum = bill-date
          umsatz.departement = artikel1.departement
        . 
      END.
      ASSIGN 
        umsatz.betrag = umsatz.betrag + service
        umsatz.anzahl = umsatz.anzahl + qty
      . 
      FIND CURRENT umsatz NO-LOCK. 
 
      CREATE billjournal. 
      ASSIGN
        billjournal.rechnr = bill.rechnr
        billjournal.artnr = artikel1.artnr 
        billjournal.anzahl = qty
        billjournal.fremdwaehrng = service-foreign
        billjournal.betrag = service
        billjournal.bezeich = artikel1.bezeich
        billjournal.zinr = curr-room
        billjournal.departement = artikel1.departement
        billjournal.epreis = 0
        billjournal.zeit = currZeit + 1
        billjournal.stornogrund = cancel-str 
        billjournal.userinit = user-init
        billjournal.bill-datum = bill-date
      . 
      FIND CURRENT billjournal NO-LOCK. 
    END. 
  END. 
 
  IF rm-vat AND artikel.mwst-code NE 0 THEN 
  DO: 
    FIND FIRST htparam WHERE htparam.paramnr = artikel.mwst-code NO-LOCK. 
    IF AVAILABLE htparam AND htparam.fdecimal NE 0 THEN 
    DO: 
      vat = htparam.fdecimal. 
      FIND FIRST htparam WHERE htparam.paramnr = 132 NO-LOCK. 
      FIND FIRST artikel1 WHERE artikel1.artnr = htparam.finteger 
        AND artikel1.departement = 0 NO-LOCK. 
      FIND FIRST htparam WHERE htparam.paramnr = 479 NO-LOCK. 
      IF htparam.flogical THEN 
        vat = vat * (price + service-foreign / qty) / 100. 
      ELSE vat = vat * price / 100. 
      vat-foreign = round(vat, 2) * qty. 
      IF double-currency THEN 
        vat = round(vat * exchg-rate, price-decimal) * qty. 
      ELSE vat = round(vat, price-decimal) * qty. 
 
      IF artikel1.umsatzart = 1 THEN
      ASSIGN 
        bill.logisumsatz = bill.logisumsatz + vat
        bill.argtumsatz = bill.argtumsatz + vat
      . 
      ELSE IF artikel1.umsatzart = 2 
        THEN bill.argtumsatz = bill.argtumsatz + vat. 
      ELSE IF (artikel1.umsatzart = 3 OR artikel1.umsatzart = 5 
        OR artikel1.umsatzart = 6) 
        THEN bill.f-b-umsatz = bill.f-b-umsatz + vat. 
      ELSE IF artikel1.umsatzart = 4 
        THEN bill.sonst-umsatz = bill.sonst-umsatz + vat. 
      IF artikel1.umsatzart GE 1 AND artikel1.umsatzart LE 4 THEN 
        bill.gesamtumsatz = bill.gesamtumsatz + vat. 
 
      CREATE bill-line. 
      ASSIGN
        bill-line.rechnr = bill.rechnr
        bill-line.artnr = artikel1.artnr 
        bill-line.bezeich = artikel1.bezeich 
        bill-line.anzahl = qty
        bill-line.fremdwbetrag = vat-foreign 
        bill-line.betrag = vat
        bill-line.zinr = curr-room 
        bill-line.departement = artikel1.departement 
        bill-line.epreis = 0
        bill-line.zeit = currZeit + 2 
        bill-line.userinit = user-init 
        bill-line.bill-datum = bill-date
      .
      IF AVAILABLE res-line THEN bill-line.arrangement = res-line.arrangement. 
      FIND CURRENT bill-line NO-LOCK. 
 
      FIND FIRST umsatz WHERE umsatz.artnr = artikel1.artnr 
        AND umsatz.departement = artikel1.departement 
        AND umsatz.datum = bill-date EXCLUSIVE-LOCK NO-ERROR. 
      IF NOT AVAILABLE umsatz THEN 
      DO: 
        CREATE umsatz.
        ASSIGN
          umsatz.artnr = artikel1.artnr
          umsatz.datum = bill-date
          umsatz.departement = artikel1.departement
        . 
      END.
      ASSIGN
        umsatz.betrag = umsatz.betrag + vat
        umsatz.anzahl = umsatz.anzahl + qty
      . 
      FIND CURRENT umsatz NO-LOCK. 
 
      CREATE billjournal. 
      ASSIGN
        billjournal.rechnr = bill.rechnr
        billjournal.artnr = artikel1.artnr 
        billjournal.anzahl = qty
        billjournal.fremdwaehrng = vat-foreign
        billjournal.betrag = vat
        billjournal.bezeich = artikel1.bezeich
        billjournal.zinr = curr-room
        billjournal.departement = artikel1.departement 
        billjournal.epreis = 0
        billjournal.zeit = currZeit + 2 
        billjournal.stornogrund = cancel-str 
        billjournal.userinit = user-init
        billjournal.bill-datum = bill-date
      .
      FIND CURRENT billjournal NO-LOCK. 
    END. 
  END. 
 
  bill.saldo = bill.saldo + vat + service. 
  IF price-decimal = 0 AND bill.saldo LE 0.4 AND bill.saldo GE -0.4 THEN 
    bill.saldo = 0. 
 
  IF double-currency OR foreign-rate THEN bill.mwst[99] = 
    bill.mwst[99] + vat-foreign + service-foreign. 
  balance = bill.saldo. 
  IF double-currency OR foreign-rate THEN balance-foreign = bill.mwst[99]. 
END. 
 
PROCEDURE rev-bdown1: 
DEFINE INPUT PARAMETER currZeit     AS INTEGER. 
DEFINE VARIABLE rest-betrag         AS DECIMAL. 
DEFINE VARIABLE argt-betrag         AS DECIMAL.
DEFINE VARIABLE p-qty               AS INTEGER.
DEFINE BUFFER artikel1              FOR artikel. 
  
  rest-betrag = amount. 

  IF amount GT 0 THEN 
  DO:    
      IF qty GT 0 THEN p-qty = qty.
      ELSE p-qty = - qty.
  END.
  ELSE IF amount LT 0 THEN
  DO:
      IF qty LT 0 THEN p-qty = qty.
      ELSE p-qty = - qty.
  END.

  FIND FIRST arrangement WHERE arrangement.argtnr = artikel.artgrp NO-LOCK. 
  FOR EACH argt-line WHERE argt-line.argtnr = arrangement.argtnr NO-LOCK: 
    IF argt-line.betrag NE 0 THEN 
    DO: 
      argt-betrag = argt-line.betrag * p-qty. 
      IF double-currency OR artikel.pricetab THEN 
        argt-betrag = round(argt-betrag * exchg-rate, price-decimal). 
    END. 
    ELSE 
    ASSIGN
      argt-betrag = amount * argt-line.vt-percnt / 100
      argt-betrag = round(argt-betrag, price-decimal)
    . 
    rest-betrag = rest-betrag - argt-betrag. 
    FIND FIRST artikel1 WHERE artikel1.artnr = argt-line.argt-artnr 
      AND artikel1.departement = argt-line.departement NO-LOCK. 
    FIND FIRST umsatz WHERE umsatz.artnr = artikel1.artnr 
      AND umsatz.departement = artikel1.departement 
      AND umsatz.datum = bill-date EXCLUSIVE-LOCK NO-ERROR. 
    IF NOT AVAILABLE umsatz THEN 
    DO: 
      CREATE umsatz. 
      ASSIGN
        umsatz.artnr       = artikel1.artnr
        umsatz.datum       = bill-date
        umsatz.departement = artikel1.departement
      . 
    END.
    ASSIGN
      umsatz.betrag = umsatz.betrag + argt-betrag
      umsatz.anzahl = umsatz.anzahl + qty
    . 
    FIND CURRENT umsatz NO-LOCK. 
    
    CREATE billjournal. 
    ASSIGN
      billjournal.rechnr       = bill.rechnr 
      billjournal.zinr         = curr-room
      billjournal.artnr        = artikel1.artnr 
      billjournal.anzahl       = qty
      billjournal.fremdwaehrng = argt-line.betrag
      billjournal.betrag       = argt-betrag
      billjournal.bezeich      = artikel1.bezeich 
      billjournal.departement  = artikel1.departement 
      billjournal.epreis       = 0
      billjournal.zeit         = currZeit
      billjournal.stornogrund  = cancel-str 
      billjournal.userinit     = user-init 
      billjournal.bill-datum   = bill-date
    . 
    FIND CURRENT billjournal NO-LOCK. 
  END. 
 
  IF rest-betrag NE 0 THEN
  DO:
    FIND FIRST artikel1 WHERE artikel1.artnr = arrangement.artnr-logis 
      AND artikel1.departement = arrangement.intervall NO-LOCK. 
    FIND FIRST umsatz WHERE umsatz.artnr = artikel1.artnr 
      AND umsatz.departement = artikel1.departement 
      AND umsatz.datum = bill-date EXCLUSIVE-LOCK NO-ERROR. 
    IF NOT AVAILABLE umsatz THEN 
    DO: 
      CREATE umsatz.
      ASSIGN
        umsatz.artnr       = artikel1.artnr 
        umsatz.datum       = bill-date
        umsatz.departement = artikel1.departement
      . 
    END.
    ASSIGN
      umsatz.betrag = umsatz.betrag + rest-betrag 
      umsatz.anzahl = umsatz.anzahl + qty
    . 
    FIND CURRENT umsatz NO-LOCK. 
  
    CREATE billjournal. 
    ASSIGN
      billjournal.rechnr      = bill.rechnr 
      billjournal.zinr        = curr-room
      billjournal.artnr       = artikel1.artnr 
      billjournal.anzahl      = qty
      billjournal.betrag      = rest-betrag
      billjournal.bezeich     = artikel1.bezeich 
      billjournal.departement = artikel1.departement 
      billjournal.epreis      = 0
      billjournal.zeit        = currZeit
      billjournal.stornogrund = cancel-str
      billjournal.userinit    = user-init 
      billjournal.bill-datum  = bill-date
    . 
    IF double-currency THEN 
      billjournal.fremdwaehrng = round(rest-betrag / exchg-rate, 6). 
    FIND CURRENT billjournal NO-LOCK. 
  END.
END. 
 
PROCEDURE update-masterbill:
DEFINE INPUT  PARAMETER currZeit    AS INTEGER.
DEFINE OUTPUT PARAMETER master-flag AS LOGICAL INITIAL NO.

DEFINE VARIABLE room                AS CHAR.
DEFINE VARIABLE transfer-case       AS INTEGER INITIAL 0.
DEFINE VARIABLE na-running          AS LOGICAL.
DEFINE VARIABLE transf-rm           AS CHAR.
DEFINE VARIABLE mess-str            AS CHAR.

DEFINE BUFFER mbill                 FOR bill.
DEFINE BUFFER resline               FOR res-line.
DEFINE BUFFER resline1              FOR res-line.

  FIND FIRST htparam WHERE htparam.paramnr = 110 NO-LOCK.   /* bill date */
  bill-date = htparam.fdate.
  FIND FIRST htparam WHERE paramnr = 253 NO-LOCK.
  na-running = htparam.flogical.
/* IF Night Audit is running THEN increase the billing date by 1.   */      
  IF na-running AND bill-date = fdate THEN bill-date = bill-date + 1.
/*  
  IF transdate NE ? THEN bill-date = transdate.
*/

  FIND FIRST resline WHERE resline.resnr = bill.resnr
      AND resline.reslinnr = bill.parent-nr NO-LOCK NO-ERROR.
  
  IF AVAILABLE resline AND resline.l-zuordnung[5] NE 0 THEN
  FIND FIRST master WHERE master.resnr = resline.l-zuordnung[5]
    AND master.active = YES AND master.flag = 0 NO-LOCK NO-ERROR.
  
  ELSE
  FIND FIRST master WHERE master.resnr = bill.resnr 
    AND master.active = YES AND master.flag = 0 NO-LOCK NO-ERROR.

  IF AVAILABLE master THEN
  DO:
    transfer-case = 1.
    IF (master.umsatzart[1] = YES AND artikel.artart = 8) 
      OR (master.umsatzart[2] = YES AND artikel.artart = 9 AND artikel.artgrp = 0) 
      OR (master.umsatzart[3] = YES AND artikel.umsatzart = 3) 
      OR (master.umsatzart[4] = YES AND artikel.umsatzart = 4) THEN
      master-flag = YES.
    IF NOT master-flag THEN
    DO:
      FIND FIRST mast-art WHERE mast-art.resnr = master.resnr
        AND mast-art.departement = artikel.departement
        AND mast-art.artnr = artikel.artnr NO-LOCK NO-ERROR.
      IF AVAILABLE mast-art THEN master-flag = YES.
    END.
  END.

  FIND FIRST resline WHERE resline.resnr = bill.resnr
    AND resline.reslinnr = bill.reslinnr NO-LOCK NO-ERROR.
  IF AVAILABLE resline AND resline.l-zuordnung[2] NE 0 THEN master-flag = NO.
  IF NOT master-flag THEN
  DO:
    transf-rm = ENTRY(1, resline.memozinr, ";").
    IF AVAILABLE resline AND transf-rm NE ""
      AND (transf-rm NE resline.zinr) THEN 
    DO:
      FIND FIRST resline1 WHERE resline1.zinr = transf-rm 
        AND resline1.resstatus = 6 NO-LOCK NO-ERROR.
      IF AVAILABLE resline1 THEN
      ASSIGN
        master-flag = YES
        transfer-case = 2
      .
    END.
  END.

  IF master-flag THEN 
  DO:
    IF transfer-case = 1 THEN 
    DO:
      FIND FIRST mbill WHERE mbill.resnr = master.resnr
      AND mbill.reslinnr = 0 EXCLUSIVE-LOCK. 
    END.
    ELSE 
    DO:
      FIND FIRST mbill WHERE mbill.resnr = resline1.resnr
      AND mbill.reslinnr = resline1.reslinnr
      AND mbill.billnr = 1 EXCLUSIVE-LOCK.
    END.
    IF artikel.umsatzart = 1 
        THEN mbill.logisumsatz = mbill.logisumsatz + amount.
    ELSE IF artikel.umsatzart = 2 
        THEN mbill.argtumsatz = mbill.argtumsatz + amount.
    ELSE IF artikel.umsatzart = 3 
        THEN mbill.f-b-umsatz = mbill.f-b-umsatz + amount.
    ELSE IF artikel.umsatzart = 4 
        THEN mbill.sonst-umsatz = mbill.sonst-umsatz + amount.
    IF artikel.umsatzart GE 1 AND artikel.umsatzart LE 4 THEN
        mbill.gesamtumsatz = mbill.gesamtumsatz + amount.

    ASSIGN
      mbill.rgdruck = 0
      mbill.saldo = mbill.saldo + amount 
      mbill.mwst[99] = mbill.mwst[99] + amount-foreign
      mbill.datum = bill-date
    .

    IF mbill.rechnr = 0 THEN
    DO:
      FIND FIRST counters WHERE counters.counter-no = 3 EXCLUSIVE-LOCK.
      counters.counter = counters.counter + 1.
      mbill.rechnr = counters.counter.
      FIND CURRENT counter NO-LOCK.
      FIND CURRENT master EXCLUSIVE-LOCK NO-ERROR.
      IF AVAILABLE master THEN
      DO:
        master.rechnr = mbill.rechnr.
        FIND CURRENT master NO-LOCK.
      END.
      IF transfer-case = 1 THEN master-str = "Master Bill".
      ELSE master-str = "Transfer Bill".
      master-rechnr = string(mbill.rechnr).
    END.

    FIND FIRST res-line WHERE res-line.resnr = bill.resnr
        AND res-line.reslinnr = bill.reslinnr NO-LOCK NO-ERROR.
    IF AVAILABLE res-line THEN gastnrmember = res-line.gastnrmember.
    ELSE gastnrmember = bill.gastnr.
    
    CREATE bill-line.
    ASSIGN
      bill-line.rechnr       = mbill.rechnr
      bill-line.artnr        = billart
      bill-line.bezeich      = DESCRIPTION
      bill-line.anzahl       = qty
      bill-line.fremdwbetrag = amount-foreign
      bill-line.betrag       = amount
      bill-line.zinr         = curr-room
      bill-line.departement  = artikel.departement
      bill-line.zeit         = currZeit
      bill-line.userinit     = user-init
      bill-line.bill-datum   = bill-date
    .
    IF artikel.artart NE 2 AND artikel.artart NE 4 AND artikel.artart NE 6
        AND artikel.artart NE 7 THEN bill-line.epreis = price.
    IF artikel.artart = 9 AND AVAILABLE res-line THEN
          bill-line.epreis = res-line.zipreis.

    IF AVAILABLE res-line THEN 
    ASSIGN
        bill-line.arrangement = res-line.arrangement
        bill-line.massnr = res-line.resnr
        bill-line.billin-nr = res-line.reslinnr
    .  
    
    IF artikel.artart = 9 AND artikel.artgrp = 0 AND AVAILABLE res-line THEN
    DO:
        FIND FIRST arrangement WHERE 
          arrangement.arrangement = res-line.arrangement NO-LOCK NO-ERROR.
        bill-line.bezeich = arrangement.argt-rgbez.
    END.
    FIND CURRENT bill-line NO-LOCK. 
      
    FIND FIRST umsatz WHERE umsatz.artnr = billart
        AND umsatz.departement = artikel.departement
        AND umsatz.datum = bill-date EXCLUSIVE-LOCK NO-ERROR.
    IF NOT AVAILABLE umsatz THEN
    DO:
      CREATE umsatz.
      ASSIGN
        umsatz.artnr = billart
        umsatz.datum = bill-date
        umsatz.departement = artikel.departement
      .
    END.
    ASSIGN  
      umsatz.betrag = umsatz.betrag + amount
      umsatz.anzahl = umsatz.anzahl + qty
    .
    FIND CURRENT umsatz NO-LOCK.
    
    CREATE billjournal.
    ASSIGN
      billjournal.rechnr        = mbill.rechnr
      billjournal.zinr          = curr-room
      billjournal.artnr         = billart
      billjournal.anzahl        = qty
      billjournal.fremdwaehrng  = amount-foreign
      billjournal.bezeich       = DESCRIPTION
      billjournal.departement   = artikel.departement
      billjournal.epreis        = price
      billjournal.zeit          = currZeit
      billjournal.stornogrund   = cancel-str
      billjournal.userinit      = user-init
      billjournal.bill-datum    = bill-date
    .

    IF AVAILABLE res-line THEN
    billjournal.comment = STRING(res-line.resnr) + ";" 
      + STRING(res-line.reslinnr).
    
    IF artikel.pricetab THEN billjournal.betrag = amount-foreign.
    ELSE billjournal.betrag = amount.
    
    cancel-str = "".
    FIND CURRENT billjournal NO-LOCK.
  
    IF artikel.artart = 2 OR artikel.artart = 7 THEN
      RUN inv-ar(billart, curr-room, mbill.gastnr, gastnrmember,
      mbill.rechnr, amount, amount-foreign, htparam.fdate, mbill.name, 
      user-init, "",deptno).                    

    IF artikel.artart = 9 AND artikel.artgrp = 0 THEN 
      RUN master-taxserv(RECID(mbill), currZeit).
    
    IF transfer-case = 1 THEN 
    msg-str = "&M"
            + translateExtended ("Transfered to Master Bill No.",lvCAREA,"") 
            + " " + string(mbill.rechnr).
    ELSE 
    msg-str = "&M"
            + translateExtended ("Transfered to Bill No.",lvCAREA,"") 
            + " " + string(mbill.rechnr) + " - " 
            + translateExtENDed ("RmNo",lvCAREA,"") + " " + mbill.zinr.
    FIND CURRENT mbill NO-LOCK.
  END.
END.

PROCEDURE master-taxserv:
DEFINE INPUT PARAMETER recid-mbill  AS INTEGER.
DEFINE INPUT PARAMETER currZeit     AS INTEGER.

DEFINE VARIABLE service             AS DECIMAL.
DEFINE VARIABLE vat                 AS DECIMAL.
DEFINE VARIABLE service-foreign     AS DECIMAL.
DEFINE VARIABLE vat-foreign         AS DECIMAL.
DEFINE VARIABLE argt-betrag0        AS DECIMAL.
DEFINE VARIABLE argt-betrag         AS DECIMAL.
DEFINE VARIABLE rest-betrag         AS DECIMAL.
DEFINE VARIABLE frate               AS DECIMAL.
DEFINE VARIABLE ex-rate             AS DECIMAL.

DEFINE VARIABLE p-sign              AS INTEGER INITIAL 1 NO-UNDO. 
DEFINE VARIABLE qty1                AS INTEGER NO-UNDO. 

DEFINE VARIABLE rm-vat              AS LOGICAL.
DEFINE VARIABLE rm-serv             AS LOGICAL.
DEFINE VARIABLE post-it             AS LOGICAL.

DEFINE BUFFER artikel1              FOR artikel.
DEFINE BUFFER mbill                 FOR bill.

  FIND FIRST htparam WHERE htparam.paramnr = 127 NO-LOCK.
  rm-vat = NOT htparam.flogical.
  FIND FIRST htparam WHERE htparam.paramnr = 128 NO-LOCK.
  rm-serv = NOT htparam.flogical.

  FIND FIRST res-line WHERE res-line.resnr = bill.resnr
    AND res-line.reslinnr = bill.parent-nr NO-LOCK NO-ERROR.
  IF res-line.adrflag THEN frate = 1.
  ELSE IF res-line.reserve-dec NE 0 THEN frate = res-line.reserve-dec.
  ELSE frate = exchg-rate.

  FIND FIRST mbill WHERE RECID(mbill) = recid-mbill EXCLUSIVE-LOCK.

  rest-betrag = amount.
  IF amount LT 0 THEN p-sign = -1. 

  FOR EACH argt-line WHERE argt-line.argtnr = arrangement.argtnr 
    AND NOT argt-line.kind2 NO-LOCK:  /* kind2 = yes => fix cost e.g extrabed */ 
     post-it = NO.
     RUN argt-betrag.p(RECID(res-line), RECID(argt-line), 
       OUTPUT argt-betrag0, OUTPUT ex-rate).
     argt-betrag = ROUND(argt-betrag0 * ex-rate, price-decimal).

     FIND FIRST artikel1 WHERE artikel1.artnr = argt-line.argt-artnr
         AND artikel1.departement = argt-line.departement NO-LOCK.
     IF argt-line.fakt-modus = 1 THEN post-it = YES.
     ELSE IF argt-line.fakt-modus = 2 THEN 
     /* checked-in , once */
     DO:
         FIND FIRST billjournal WHERE billjournal.rechnr = bill.rechnr
           AND billjournal.artnr = artikel1.artnr
           AND billjournal.betrag = argt-betrag
           AND billjournal.departement = artikel1.departement NO-LOCK NO-ERROR.
         IF NOT AVAILABLE billjournal THEN post-it = YES.
     END.
     ELSE IF argt-line.fakt-modus = 3 THEN 
     DO:
         IF (res-line.ankunft + 1) = bill-date THEN post-it = YES.
     END.
     ELSE IF argt-line.fakt-modus = 4 THEN   /* 1st day of month  */
     DO:
         IF day(bill-date) = 1 THEN post-it = YES.
     END.
     ELSE IF argt-line.fakt-modus = 5 THEN   /* last day of month */
     DO:
         IF DAY(bill-date + 1) = 1 THEN post-it = YES.
     END.
       
     IF post-it AND argt-betrag NE 0 THEN
     DO:
       IF argt-line.betriebsnr = 0 THEN qty1 = res-line.erwachs * p-sign. 
       ELSE qty1 = argt-line.betriebsnr * p-sign. 
       
       rest-betrag = rest-betrag - argt-betrag * p-sign.
       
       FIND FIRST artikel1 WHERE artikel1.artnr = argt-line.argt-artnr
         AND artikel1.departement = argt-line.departement NO-LOCK.
       FIND FIRST umsatz WHERE umsatz.artnr = artikel1.artnr
         AND umsatz.departement = artikel1.departement
         AND umsatz.datum = bill-date EXCLUSIVE-LOCK NO-ERROR.
       IF NOT AVAILABLE umsatz THEN
       DO:
         CREATE umsatz.
         umsatz.artnr = artikel1.artnr. 
         umsatz.datum = bill-date.
         umsatz.departement = artikel1.departement.
       END.
       umsatz.betrag = umsatz.betrag + argt-betrag * p-sign.
       umsatz.anzahl = umsatz.anzahl + qty1.
       FIND CURRENT umsatz NO-LOCK.    

       CREATE billjournal.
       billjournal.rechnr = bill.rechnr.
       billjournal.artnr = artikel1.artnr.  
       billjournal.anzahl = qty1.
       billjournal.fremdwaehrng = argt-betrag0  * p-sign.
       billjournal.betrag = argt-betrag  * p-sign.
       billjournal.bezeich = artikel1.bezeich.
       billjournal.zinr = res-line.zinr.
       billjournal.departement = artikel1.departement.
       billjournal.epreis = 0.
       billjournal.zeit = currZeit.
       billjournal.userinit = userinit.
       billjournal.bill-datum = bill-date.
       FIND CURRENT billjournal NO-LOCK.
     END.
  END.

  FIND FIRST artikel1 WHERE artikel1.artnr = arrangement.artnr-logis
    AND artikel1.departement = 0 NO-LOCK.
  FIND FIRST umsatz WHERE umsatz.artnr = artikel1.artnr
      AND umsatz.departement = artikel1.departement
      AND umsatz.datum = bill-date EXCLUSIVE-LOCK NO-ERROR.
  IF NOT AVAILABLE umsatz THEN
  DO:
    CREATE umsatz.
    umsatz.artnr = artikel1.artnr. 
    umsatz.datum = bill-date.
    umsatz.departement = artikel1.departement.
  END.
  umsatz.betrag = umsatz.betrag + rest-betrag.
  umsatz.anzahl = umsatz.anzahl + qty.
  FIND CURRENT umsatz NO-LOCK.    
  CREATE billjournal.
  billjournal.rechnr = mbill.rechnr.
  billjournal.artnr = artikel1.artnr.  
  billjournal.anzahl = qty. 
  billjournal.fremdwaehrng = ROUND(rest-betrag / exchg-rate , 2). 
  billjournal.betrag = rest-betrag.
  billjournal.bezeich = artikel1.bezeich.
  billjournal.zinr = curr-room.
  billjournal.departement = artikel1.departement.
  billjournal.epreis = 0.
  billjournal.zeit = currZeit.
  billjournal.stornogrund = cancel-str.
  billjournal.userinit = user-init.
  billjournal.bill-datum = bill-date.
  FIND CURRENT billjournal NO-LOCK.
    
  IF rm-serv AND artikel.service-code NE 0 THEN
  DO:
    FIND FIRST htparam WHERE htparam.paramnr = artikel.service-code NO-LOCK.
    IF available htparam AND htparam.fdecimal NE 0 THEN
    DO:
      service = htparam.fdecimal.
      FIND FIRST htparam WHERE htparam.paramnr = 133 NO-LOCK.
      FIND FIRST artikel1 WHERE artikel1.artnr = htparam.finteger 
        AND artikel1.departement = 0 NO-LOCK.
      service = service * price / 100.
      service-foreign = ROUND(service, 2) * qty. 
      IF double-currency THEN
        service = ROUND(service * exchg-rate, price-decimal) * qty. 
      ELSE service = ROUND(service, price-decimal) * qty. 

      IF artikel1.umsatzart = 1 
         THEN bill.logisumsatz = bill.logisumsatz + service.
      ELSE IF artikel1.umsatzart = 2 
        THEN bill.argtumsatz = bill.argtumsatz + service.
      ELSE IF artikel1.umsatzart = 3 
        THEN bill.f-b-umsatz = bill.f-b-umsatz + service.
      ELSE IF artikel1.umsatzart = 4 
        THEN bill.sonst-umsatz = bill.sonst-umsatz + service.
      IF artikel1.umsatzart GE 1 AND artikel1.umsatzart LE 4 THEN
        bill.gesamtumsatz = bill.gesamtumsatz + service.
      
      CREATE bill-line.
      bill-line.rechnr = mbill.rechnr.
      bill-line.artnr = artikel1.artnr.  
      bill-line.bezeich = artikel1.bezeich.
      bill-line.anzahl = qty.
      bill-line.fremdwbetrag = service-foreign.
      bill-line.betrag = service.
      bill-line.zinr = curr-room. 
      bill-line.departement = artikel1.departement.
      bill-line.epreis = 0.
      bill-line.zeit = currZeit + 1.
      bill-line.userinit = user-init.
      bill-line.arrangement = res-line.arrangement.
      bill-line.bill-datum = bill-date.
      FIND CURRENT bill-line NO-LOCK. 
      
      FIND FIRST umsatz WHERE umsatz.artnr = artikel1.artnr
        AND umsatz.departement = artikel1.departement
        AND umsatz.datum = bill-date EXCLUSIVE-LOCK NO-ERROR.
      IF not available umsatz THEN
      DO:
        CREATE umsatz.
        umsatz.artnr = artikel1.artnr. 
        umsatz.datum = bill-date.
        umsatz.departement = artikel1.departement.
      END.
      umsatz.betrag = umsatz.betrag + service.
      umsatz.anzahl = umsatz.anzahl + qty.
      FIND CURRENT umsatz NO-LOCK.
    
      CREATE billjournal.
      billjournal.rechnr = mbill.rechnr.
      billjournal.artnr = artikel1.artnr.  
      billjournal.anzahl = qty.
      billjournal.fremdwaehrng = service-foreign.
      billjournal.betrag = service.
      billjournal.bezeich = artikel1.bezeich.
      billjournal.zinr = curr-room.
      billjournal.departement = artikel1.departement.
      billjournal.epreis = 0.
      billjournal.zeit = currZeit + 1.
      billjournal.stornogrund = cancel-str.
      billjournal.userinit = user-init.
      billjournal.bill-datum = bill-date.
      FIND CURRENT billjournal NO-LOCK.
    END.  
  END.

  IF rm-vat AND artikel.mwst-code NE 0 THEN
  DO:
    FIND FIRST htparam WHERE htparam.paramnr = artikel.mwst-code NO-LOCK.
    IF available htparam AND htparam.fdecimal NE 0 THEN
    DO:
      vat = htparam.fdecimal.
      IF (service * qty ) < 0 THEN service = - service.
      FIND FIRST htparam WHERE htparam.paramnr = 132 NO-LOCK.
      FIND FIRST artikel1 WHERE artikel1.artnr = htparam.finteger 
        AND artikel1.departement = 0 NO-LOCK.
      FIND FIRST htparam WHERE htparam.paramnr = 479 NO-LOCK.
      IF htparam.flogical THEN 
        vat = vat * (price + service-foreign / qty) / 100.
      ELSE vat = vat * price / 100. 
      vat-foreign = ROUND(vat, 2) * qty. 
      IF double-currency THEN 
        vat = ROUND(vat * exchg-rate, price-decimal) * qty.
      ELSE vat = ROUND(vat, price-decimal) * qty. 
 
       IF artikel1.umsatzart = 1 
         THEN mbill.logisumsatz = mbill.logisumsatz + vat.
      ELSE IF artikel1.umsatzart = 2 
        THEN mbill.argtumsatz = mbill.argtumsatz + vat.
      ELSE IF artikel1.umsatzart = 3 
        THEN mbill.f-b-umsatz = mbill.f-b-umsatz + vat.
      ELSE IF artikel1.umsatzart = 4 
        THEN mbill.sonst-umsatz = mbill.sonst-umsatz + vat.
      IF artikel1.umsatzart GE 1 AND artikel1.umsatzart LE 4 THEN
        mbill.gesamtumsatz = mbill.gesamtumsatz + vat.
      
      CREATE bill-line.
      bill-line.rechnr = mbill.rechnr.
      bill-line.artnr = artikel1.artnr.  
      bill-line.bezeich = artikel1.bezeich.
      bill-line.anzahl = qty.
      bill-line.fremdwbetrag = vat-foreign.
      bill-line.betrag = vat.
      bill-line.zinr = curr-room.
      bill-line.departement = artikel1.departement.
      bill-line.epreis = 0.
      bill-line.zeit = currZeit + 2.
      bill-line.userinit = user-init.
      bill-line.arrangement = res-line.arrangement.
      bill-line.bill-datum = bill-date.
      FIND CURRENT bill-line NO-LOCK. 
      
      FIND FIRST umsatz WHERE umsatz.artnr = artikel1.artnr
        AND umsatz.departement = artikel1.departement
        AND umsatz.datum = bill-date EXCLUSIVE-LOCK NO-ERROR.
      IF NOT AVAILABLE umsatz THEN
      DO:
        CREATE umsatz.
        umsatz.artnr = artikel1.artnr. 
        umsatz.datum = bill-date.
        umsatz.departement = artikel1.departement.
      END.
      umsatz.betrag = umsatz.betrag + vat.
      umsatz.anzahl = umsatz.anzahl + qty.
      FIND CURRENT umsatz NO-LOCK.
    
      CREATE billjournal.
      billjournal.rechnr = mbill.rechnr.
      billjournal.artnr = artikel1.artnr.  
      billjournal.anzahl = qty.
      billjournal.fremdwaehrng = vat-foreign.
      billjournal.betrag = vat.
      billjournal.bezeich = artikel1.bezeich.
      billjournal.zinr = curr-room.
      billjournal.departement = artikel1.departement.
      billjournal.epreis = 0.
      billjournal.zeit = currZeit + 2.
      billjournal.stornogrund = cancel-str.
      billjournal.userinit = user-init.
      billjournal.bill-datum = bill-date.
      FIND CURRENT billjournal NO-LOCK.
    END.  
  END.

  mbill.saldo = mbill.saldo + vat + service. 
  mbill.mwst[99] = mbill.mwst[99] + vat-foreign + service-foreign.
  FIND CURRENT mbill NO-LOCK.
END.

PROCEDURE inv-ar:
  DEFINE INPUT PARAMETER curr-art       AS INTEGER.
  DEFINE INPUT PARAMETER zinr           LIKE zimmer.zinr.   /*MT 20/07/12 change zinr format */
  DEFINE INPUT PARAMETER gastnr         AS INTEGER.
  DEFINE INPUT PARAMETER gastnrmember   AS INTEGER.
  DEFINE INPUT PARAMETER rechnr         AS INTEGER.
  DEFINE INPUT PARAMETER saldo          AS DECIMAL.
  DEFINE INPUT PARAMETER saldo-foreign  AS DECIMAL.
  DEFINE INPUT PARAMETER bill-DATE      AS DATE.
  DEFINE INPUT PARAMETER billname       AS CHAR.
  DEFINE INPUT PARAMETER userinit       AS CHAR FORMAT "x(2)".
  DEFINE INPUT PARAMETER voucher-nr     AS CHAR.
  DEFINE INPUT PARAMETER dept-nr        AS INTEGER.

  DEFINE VARIABLE comment               AS CHAR INITIAL "".
  DEFINE VARIABLE verstat               AS INTEGER INITIAL 0.
  DEFINE VARIABLE fsaldo                AS DECIMAL INITIAL 0.
  DEFINE VARIABLE lsaldo                AS DECIMAL INITIAL 0.
  DEFINE VARIABLE FOReign-rate          AS LOGICAL.  
  DEFINE VARIABLE currency-nr           AS INTEGER INITIAL 0 NO-UNDO.
  DEFINE VARIABLE double-currency       AS LOGICAL.  

  DEFINE BUFFER debt                    FOR debitor.
  DEFINE BUFFER debt1                   FOR debitor.
  DEFINE BUFFER main-res                FOR reservation.
  DEFINE BUFFER resline                 FOR res-line.
  DEFINE BUFFER bill1                   FOR bill.
  DEFINE BUFFER bline                   FOR bill-line.
  DEFINE BUFFER guest1                  FOR guest.

  FIND FIRST htparam WHERE paramnr = 143 NO-LOCK.
  foreign-rate = htparam.flogical.

  FIND FIRST htparam WHERE paramnr = 240 NO-LOCK.
  double-currency = htparam.flogical.

  FIND FIRST bediener WHERE bediener.userinit = userinit NO-LOCK.
  
  FIND FIRST htparam WHERE paramnr = 997 NO-LOCK.
  IF NOT htparam.flogical THEN RETURN.

  FIND FIRST guest WHERE guest.gastnr = gastnr NO-LOCK.
  billname = STRING(guest.name + ", " + guest.vorname1 + " " 
    + guest.anrede1 + guest.anredefirma, "x(36)").
      
  FIND FIRST debt WHERE debt.artnr = curr-art
    AND debt.rechnr = rechnr AND debt.opart = 0 
    AND debt.rgdatum = bill-DATE AND debt.counter = 0 
    AND debt.saldo = saldo NO-LOCK NO-ERROR.

  IF AVAILABLE debt THEN
  DO:
    /*FIND CURRENT debt EXCLUSIVE-LOCK.
    DELETE debt.
    RETURN.*/

    FIND FIRST debt1 WHERE RECID(debt1) = RECID(debt) EXCLUSIVE-LOCK
        NO-ERROR.
    IF AVAILABLE debt1 THEN
    DO:
      DELETE debt1.
      RELEASE debt1.
      RETURN.
    END.
    ELSE
    DO:
        CREATE debt1.
        BUFFER-COPY debt TO debt1.
        ASSIGN 
            debt1.saldo       = - debt1.saldo
            debt1.bediener-nr = bediener.nr
            debt1.transzeit   = TIME
        .
        FIND CURRENT debt1 NO-LOCK.
        RELEASE debt1.
        RETURN.
    END.
  END.

  FIND FIRST bill1 WHERE bill1.rechnr = rechnr NO-LOCK NO-ERROR.

  IF AVAILABLE bill1 AND bill1.resnr NE 0 THEN
  DO:
    FIND FIRST resline WHERE resline.resnr = bill1.resnr
      AND resline.active-flag LE 2 AND resline.resstatus LE 8 
      AND resline.zipreis NE 0 NO-LOCK NO-ERROR.
    IF NOT AVAILABLE resline THEN
    FIND FIRST resline WHERE resline.resnr = bill1.resnr
      AND resline.active-flag LE 2 AND resline.resstatus LE 8 
      NO-LOCK NO-ERROR.
    IF AVAILABLE resline THEN currency-nr = resline.betriebsnr. 
    
    FIND FIRST main-res WHERE main-res.resnr = bill1.resnr NO-LOCK NO-ERROR.
    IF AVAILABLE main-res THEN comment = main-res.groupname.
    IF comment = "" AND gastnrmember NE gastnr THEN
    DO:
      FIND FIRST guest1 WHERE guest1.gastnr = gastnrmember NO-LOCK NO-ERROR.
      IF AVAILABLE guest1 THEN
      DO:
        comment = STRING(guest1.name + "," + guest1.vorname1,"x(20)").
        IF AVAILABLE resline THEN
          comment = comment + " " + STRING(resline.ankunft) + "-"
            + STRING(resline.abreise).
      END.
    END.

    IF bill1.reslinnr = 0 THEN verstat = 1. 

    IF AVAILABLE main-res AND main-res.insurance THEN
    DO:
      FIND FIRST resline WHERE resline.resnr = main-res.resnr
        AND resline.reserve-dec NE 0 AND resline.reserve-dec NE 1
        NO-LOCK NO-ERROR.
      IF AVAILABLE resline THEN saldo-foreign = saldo / resline.reserve-dec.
    END.
  END.
  ELSE IF AVAILABLE bill1 AND bill1.resnr = 0 THEN
    comment = bill1.bilname.

  CREATE debitor.
  ASSIGN
    debitor.artnr           = curr-art
    debitor.betrieb-gastmem = currency-nr
    debitor.zinr            = zinr
    debitor.gastnr          = gastnr
    debitor.gastnrmember    = gastnrmember
    debitor.rechnr          = rechnr
    debitor.saldo           = - saldo
    debitor.transzeit       = TIME
    debitor.rgdatum         = bill-DATE
    debitor.bediener-nr     = bediener.nr
    debitor.name            = billname
    debitor.vesrcod         = comment
    debitor.verstat         = verstat
    debitor.betriebsnr      = dept-nr
  .

  IF double-currency or foreign-rate THEN 
      debitor.vesrdep    = - saldo-foreign.

  IF voucher-nr NE "" THEN
  DO:
      IF comment NE "" THEN 
          ASSIGN debitor.vesrcod = voucher-nr + ";" + debitor.vesrcod.
      ELSE ASSIGN debitor.vesrcod = voucher-nr.
  END.

  RELEASE debitor.
  
END. 

