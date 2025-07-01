DEF TEMP-TABLE t-h-artikel LIKE h-artikel
    FIELD rec-id AS INT.

DEF INPUT PARAMETER rec-id AS INT.
DEF INPUT PARAMETER guestnr AS INT.
DEF INPUT PARAMETER curr-dept AS INT.
DEF INPUT PARAMETER balance-foreign AS DECIMAL.
DEF INPUT PARAMETER balance AS DECIMAL.
DEF INPUT PARAMETER pay-type AS INT.
DEF INPUT PARAMETER transdate AS DATE.
DEF INPUT PARAMETER double-currency AS LOGICAL.
DEF INPUT PARAMETER exchg-rate AS DECIMAL.
DEF INPUT PARAMETER price-decimal AS INT.
DEF INPUT PARAMETER user-init AS CHAR.

DEFINE OUTPUT PARAMETER payment-exist AS LOGICAL INITIAL NO. 
DEFINE OUTPUT PARAMETER p-artnr AS INT.
DEFINE OUTPUT PARAMETER billart AS INT.
DEFINE OUTPUT PARAMETER qty AS INT.
DEFINE OUTPUT PARAMETER description AS CHAR.
DEFINE OUTPUT PARAMETER price AS DECIMAL.
DEFINE OUTPUT PARAMETER amount-foreign LIKE vhp.bill-line.betrag.
DEFINE OUTPUT PARAMETER amount LIKE vhp.bill-line.betrag.
DEFINE OUTPUT PARAMETER bill-date AS DATE.
DEFINE OUTPUT PARAMETER fl-code AS INT INIT 0.
DEFINE OUTPUT PARAMETER TABLE FOR t-h-artikel.

FIND FIRST h-bill WHERE RECID(h-bill) = rec-id.                 
IF h-bill.kellner-nr NE INT(user-init) THEN
    h-bill.kellner-nr = INT(user-init).
RUN check-payment.
/*FD Nov 02, 2022 => Ticket C8F1C7 => Still create h-compli if just return in procedure check-payment*/
IF payment-exist THEN RETURN. 

p-artnr = guestnr. 
RUN adjust-complito. 
FIND FIRST vhp.h-artikel WHERE vhp.h-artikel.departement = curr-dept 
AND vhp.h-artikel.artnr = p-artnr NO-LOCK. 
ASSIGN
    billart         = vhp.h-artikel.artnr
    qty             = vhp.h-bill.belegung
    description     = vhp.h-artikel.bezeich 
    price           = 0
    amount-foreign  = - balance-foreign 
    amount          = - balance
  . 
IF pay-type = 6 THEN RUN fill-mcoupon(curr-dept, p-artnr). 
RUN release-TBplan.

IF AVAILABLE h-artikel THEN
DO:
    CREATE t-h-artikel.
    BUFFER-COPY h-artikel TO t-h-artikel.
    ASSIGN t-h-artikel.rec-id = RECID(h-artikel).
END.


PROCEDURE check-payment: 
DEFINE buffer h-bline FOR vhp.h-bill-line. 
DEFINE buffer h-art FOR vhp.h-artikel. 
DEF VAR fdisc AS INTEGER NO-UNDO. 
DEF VAR bdisc AS INTEGER NO-UNDO. 
DEF VAR odisc AS INTEGER NO-UNDO. 
DEF VAR tot-disc AS DECIMAL INITIAL 0 NO-UNDO. 
 
  FIND FIRST h-bline WHERE h-bline.rechnr = vhp.h-bill.rechnr 
    AND h-bline.departement = vhp.h-bill.departement NO-LOCK NO-ERROR. 
  DO WHILE AVAILABLE h-bline: 
    IF h-bline.artnr = 0 THEN payment-exist = YES. 
    ELSE 
    DO: 
      FIND FIRST h-art WHERE h-art.artnr = h-bline.artnr AND 
        h-art.departement = h-bline.departement NO-LOCK. 
      IF h-art.artart NE 0 THEN payment-exist = YES. 
 
      IF (h-bline.artnr = fdisc OR h-bline.artnr = bdisc 
          OR h-bline.artnr = odisc) 
      THEN tot-disc = tot-disc + h-bline.betrag.       
    END. 
    FIND NEXT h-bline WHERE h-bline.rechnr = vhp.h-bill.rechnr 
        AND h-bline.departement = vhp.h-bill.departement NO-LOCK NO-ERROR. 
  END. 
  IF payment-exist THEN 
  DO: 
    fl-code = 1.
    RETURN. 
  END. 
 
  IF tot-disc NE 0 THEN 
  DO: 
    fl-code = 2.
    payment-exist = YES. 
  END. 
 
END. 


PROCEDURE release-TBplan:
    FIND FIRST vhp.queasy WHERE vhp.queasy.KEY = 31 
      AND vhp.queasy.number1 = vhp.h-bill.departement
      AND vhp.queasy.number2 = vhp.h-bill.tischnr NO-LOCK NO-ERROR.
    IF AVAILABLE vhp.queasy THEN
    DO TRANSACTION:
      FIND CURRENT vhp.queasy EXCLUSIVE-LOCK.
      ASSIGN vhp.queasy.number3 = 0
             vhp.queasy.date1 = ?.
      FIND CURRENT vhp.queasy NO-LOCK.
      RELEASE vhp.queasy.
    END.
END.


PROCEDURE fill-mcoupon: 
  DEF INPUT PARAMETER dept  AS INTEGER.
  DEF INPUT PARAMETER artNo AS INTEGER.
 
  DO TRANSACTION: 
    
    FIND FIRST vhp.htparam WHERE vhp.htparam.paramnr = 110 NO-LOCK. 
    /* vhp.bill DATE */ 
    bill-date = vhp.htparam.fdate. 
    IF transdate NE ? THEN bill-date = transdate. 
    ELSE 
    DO: 
      FIND FIRST vhp.htparam WHERE vhp.htparam.paramnr = 253 NO-LOCK. /* NA running */ 
      IF vhp.htparam.flogical AND bill-date LT TODAY THEN bill-date = bill-date + 1. 
    END. 
 
    FIND FIRST vhp.h-umsatz WHERE vhp.h-umsatz.artnr = artNo 
      AND vhp.h-umsatz.departement = - dept AND 
      vhp.h-umsatz.betriebsnr = dept 
      AND vhp.h-umsatz.datum = bill-date EXCLUSIVE-LOCK NO-ERROR. 
    IF NOT AVAILABLE vhp.h-umsatz THEN 
    DO: 
      CREATE vhp.h-umsatz. 
      ASSIGN
        vhp.h-umsatz.artnr       = artNo
        vhp.h-umsatz.departement = - dept 
        vhp.h-umsatz.betriebsnr  = dept 
        vhp.h-umsatz.datum = bill-date
      . 
    END. 
    vhp.h-umsatz.anzahl = vhp.h-umsatz.anzahl + vhp.h-bill.belegung.  
    FIND CURRENT vhp.h-umsatz NO-LOCK. 
    RELEASE vhp.h-umsatz. 
  END. 
END. 



PROCEDURE adjust-complito: 
  DEFINE VARIABLE h-mwst AS DECIMAL. 
  DEFINE VARIABLE h-service AS DECIMAL. 
  DEFINE VARIABLE h-mwst-foreign AS DECIMAL. 
  DEFINE VARIABLE h-service-foreign AS DECIMAL. 
  DEFINE VARIABLE epreis AS DECIMAL. 
  DEFINE VARIABLE amount AS DECIMAL. 
  DEFINE VARIABLE amount-foreign AS DECIMAL. 
  DEFINE VARIABLE cost AS DECIMAL. 
  DEFINE VARIABLE f-cost AS DECIMAL INITIAL 0. 
  DEFINE VARIABLE b-cost AS DECIMAL INITIAL 0. 
 
  DEFINE VARIABLE f-eknr AS INTEGER. 
  DEFINE VARIABLE b-eknr AS INTEGER. 
 
  DEFINE VARIABLE f-disc AS INTEGER NO-UNDO. 
  DEFINE VARIABLE b-disc AS INTEGER NO-UNDO. 
  DEFINE VARIABLE o-disc AS INTEGER NO-UNDO. 
 
  DEFINE buffer h-bline FOR vhp.h-bill-line. 
  DEFINE buffer h-art FOR vhp.h-artikel. 
  DEFINE buffer fr-art FOR vhp.artikel. 
  DEFINE buffer kellner1 FOR vhp.kellner. 
  DEFINE buffer kellne1 FOR vhp.kellner. 
 
  FIND FIRST vhp.htparam WHERE paramnr = 862 NO-LOCK. 
  f-eknr = htparam.finteger.               /* Rulita 211024 | Fixing for serverless */  
  FIND FIRST vhp.htparam WHERE paramnr = 892 NO-LOCK. 
  b-eknr = htparam.finteger.               /* Rulita 211024 | Fixing for serverless */  
 
  FIND FIRST vhp.htparam WHERE paramnr = 557 no-lock. /*rest artnr 4 disc*/ 
  f-disc = vhp.htparam.finteger. 
  FIND FIRST vhp.htparam WHERE paramnr = 596 no-lock. /*rest artnr 4 disc*/ 
  b-disc = vhp.htparam.finteger. 
  FIND FIRST vhp.htparam WHERE paramnr = 556 no-lock. /*rest artnr 4 disc*/ 
  o-disc = vhp.htparam.finteger. 
 
  FIND FIRST kellner1 WHERE kellner1.kellner-nr = vhp.h-bill.kellner-nr 
    AND kellner1.departement = curr-dept NO-LOCK NO-ERROR. 
  FIND FIRST kellne1 WHERE kellne1.kellner-nr = vhp.h-bill.kellner-nr 
    AND kellne1.departement = curr-dept NO-LOCK NO-ERROR. 
 
  FIND FIRST h-bline WHERE h-bline.rechnr = vhp.h-bill.rechnr 
    AND h-bline.departement = curr-dept NO-LOCK NO-ERROR. 
  DO WHILE AVAILABLE h-bline: 
    FIND FIRST h-art WHERE h-art.artnr = h-bline.artnr 
      AND h-art.departement = h-bline.departement NO-LOCK NO-ERROR. 
    IF AVAILABLE h-art AND h-art.artart = 0 THEN 
    DO TRANSACTION: 
      h-service = 0. 
      h-mwst = 0. 
      h-service-foreign = 0. 
      h-mwst-foreign = 0. 
      amount = 0. 
      amount-foreign = 0. 

      FIND FIRST vhp.artikel WHERE vhp.artikel.artnr = h-art.artnrfront 
        AND vhp.artikel.departement = h-art.departement NO-LOCK. 
      IF vhp.artikel.artart = 9 AND vhp.artikel.artgrp NE 0 THEN 
      RUN adjust-revbdown(h-bline.bill-datum, - h-bline.betrag, 
        - h-bline.anzahl). 

      FIND FIRST vhp.h-umsatz WHERE vhp.h-umsatz.artnr = h-art.artnr 
        AND vhp.h-umsatz.departement = h-art.departement 
        AND vhp.h-umsatz.datum = h-bline.bill-datum EXCLUSIVE-LOCK NO-ERROR. 
      IF AVAILABLE vhp.h-umsatz AND pay-type = 5 THEN 
      DO: 
        vhp.h-umsatz.betrag = vhp.h-umsatz.betrag - h-bline.betrag. 
        vhp.h-umsatz.anzahl = vhp.h-umsatz.anzahl - h-bline.anzahl. 
        FIND CURRENT vhp.h-umsatz NO-LOCK. 
      END. 
 
      FIND FIRST vhp.umsatz WHERE vhp.umsatz.artnr = h-art.artnrfront 
        AND vhp.umsatz.departement = h-art.departement 
        AND vhp.umsatz.datum = h-bline.bill-datum EXCLUSIVE-LOCK NO-ERROR. 
      IF AVAILABLE vhp.umsatz THEN 
      DO: 
        vhp.umsatz.betrag = vhp.umsatz.betrag - h-bline.betrag. 
        vhp.umsatz.anzahl = vhp.umsatz.anzahl - h-bline.anzahl. 
        FIND CURRENT vhp.umsatz NO-LOCK. 
      END. 
/* 
      FIND FIRST vhp.umsatz WHERE vhp.umsatz.artnr = kellner1.kumsatz-nr 
        AND vhp.umsatz.departement = h-bline.departement 
        AND vhp.umsatz.datum = h-bline.bill-datum EXCLUSIVE-LOCK NO-ERROR. 
      IF AVAILABLE vhp.umsatz THEN 
      DO: 
        vhp.umsatz.betrag = vhp.umsatz.betrag - h-bline.betrag. 
        vhp.umsatz.anzahl = vhp.umsatz.anzahl - h-bline.anzahl. 
        FIND CURRENT vhp.umsatz NO-LOCK. 
      END. 
*/ 
/* 04 Dec 2008: seems to be no longer relevant
      IF vhp.h-bline.artnr NE f-disc AND vhp.h-bline.artnr NE b-disc 
        AND vhp.h-bline.artnr NE o-disc THEN 
      DO: 
        FIND FIRST vhp.h-journal EXCLUSIVE-LOCK WHERE 
          vhp.h-journal.bill-datum      = h-bline.bill-datum 
          AND vhp.h-journal.zeit        = h-bline.zeit 
          AND vhp.h-journal.sysdate     = h-bline.sysdate 
          AND vhp.h-journal.artnr       = h-bline.artnr 
          AND vhp.h-journal.departement = h-bline.departement 
          AND vhp.h-journal.anzahl      = h-bline.anzahl
          USE-INDEX chrono_ix NO-ERROR. 
        IF AVAILABLE vhp.h-journal THEN 
        DO:
          ASSIGN
            vhp.h-journal.fremdwaehrng = h-bline.fremdwbetrag
            vhp.h-journal.betrag       = h-bline.betrag
          . 
          FIND CURRENT vhp.h-journal NO-LOCK. 
        END. 
      END. 
*/ 
      FIND CURRENT vhp.h-bill EXCLUSIVE-LOCK. 
      vhp.h-bill.gesamtumsatz = vhp.h-bill.gesamtumsatz - h-bline.betrag. 
      vhp.h-bill.mwst[99] = vhp.h-bill.mwst[99] 
        - (h-service-foreign + h-mwst-foreign) * h-bline.anzahl. 
      vhp.h-bill.saldo = vhp.h-bill.saldo 
        - (h-service + h-mwst) * h-bline.anzahl. 
      FIND CURRENT vhp.h-bill NO-LOCK. 
    END. 
 
    balance-foreign = vhp.h-bill.mwst[99]. 
    balance = vhp.h-bill.saldo. 
 
    IF pay-type = 5 THEN 
    DO TRANSACTION: 
      create vhp.h-compli. 
      vhp.h-compli.datum = h-bline.bill-datum. 
      vhp.h-compli.departement = h-bline.departement. 
      vhp.h-compli.rechnr = h-bline.rechnr. 
      vhp.h-compli.artnr = h-bline.artnr. 
      vhp.h-compli.anzahl = h-bline.anzahl. 
      vhp.h-compli.epreis = h-bline.epreis. 
      vhp.h-compli.p-artnr = p-artnr. 
      FIND CURRENT vhp.h-compli NO-LOCK. 
    END. 
 
    FIND NEXT h-bline WHERE h-bline.rechnr = vhp.h-bill.rechnr 
      AND h-bline.departement = curr-dept NO-LOCK NO-ERROR. 
  END. 
END. 

PROCEDURE adjust-revbdown: 
DEFINE INPUT PARAMETER bill-date AS DATE. 
DEFINE INPUT PARAMETER amount AS DECIMAL. 
DEFINE INPUT PARAMETER qty AS INTEGER. 
DEFINE BUFFER artikel1 FOR vhp.artikel. 
DEFINE VARIABLE rest-betrag AS DECIMAL. 
DEFINE VARIABLE argt-betrag AS DECIMAL. 
 
  rest-betrag = amount. 
  FIND FIRST vhp.arrangement WHERE vhp.arrangement.argtnr 
    = vhp.artikel.artgrp NO-LOCK. 
  FOR EACH vhp.argt-line WHERE vhp.argt-line.argtnr 
    = vhp.arrangement.argtnr NO-LOCK: 
    IF vhp.argt-line.betrag NE 0 THEN 
    DO: 
      argt-betrag = vhp.argt-line.betrag * qty. 
      IF double-currency OR vhp.artikel.pricetab THEN 
        argt-betrag = ROUND(argt-betrag * exchg-rate, price-decimal). 
    END. 
    ELSE 
    DO: 
      argt-betrag = amount * vhp.argt-line.vt-percnt / 100. 
      argt-betrag = ROUND(argt-betrag, price-decimal). 
    END. 
    rest-betrag = rest-betrag - argt-betrag. 
    FIND FIRST artikel1 WHERE artikel1.artnr = vhp.argt-line.argt-artnr 
      AND artikel1.departement = vhp.argt-line.departement NO-LOCK. 
    FIND FIRST vhp.umsatz WHERE vhp.umsatz.artnr = artikel1.artnr 
      AND vhp.umsatz.departement = artikel1.departement 
      AND vhp.umsatz.datum = bill-date EXCLUSIVE-LOCK NO-ERROR. 
    IF NOT AVAILABLE vhp.umsatz THEN 
    DO: 
      CREATE vhp.umsatz. 
      vhp.umsatz.artnr = artikel1.artnr. 
      vhp.umsatz.datum = bill-date. 
      vhp.umsatz.departement = artikel1.departement. 
    END. 
    vhp.umsatz.betrag = vhp.umsatz.betrag + argt-betrag. 
    vhp.umsatz.anzahl = vhp.umsatz.anzahl + qty. 
    FIND CURRENT vhp.umsatz NO-LOCK. 
    
    CREATE vhp.billjournal. 
    ASSIGN
      vhp.billjournal.rechnr = h-bill.rechnr
      vhp.billjournal.artnr = artikel1.artnr
      vhp.billjournal.anzahl = qty
      vhp.billjournal.fremdwaehrng = vhp.argt-line.betrag
      vhp.billjournal.betrag = argt-betrag
      vhp.billjournal.bezeich = artikel1.bezeich
        + "<" + STRING(vhp.h-bill.departement,"99") + ">"
      vhp.billjournal.departement = artikel1.departement
      vhp.billjournal.epreis = 0
      vhp.billjournal.zeit = TIME 
      vhp.billjournal.userinit = user-init
      vhp.billjournal.bill-datum = bill-date 
    .
    FIND CURRENT vhp.billjournal NO-LOCK. 
  END. 
 
  FIND FIRST artikel1 WHERE artikel1.artnr = vhp.arrangement.artnr-logis 
    AND artikel1.departement = vhp.arrangement.intervall NO-LOCK. 
  FIND FIRST vhp.umsatz WHERE vhp.umsatz.artnr = artikel1.artnr 
    AND vhp.umsatz.departement = artikel1.departement 
    AND vhp.umsatz.datum = bill-date EXCLUSIVE-LOCK NO-ERROR. 
  IF NOT AVAILABLE vhp.umsatz THEN 
  DO: 
    CREATE vhp.umsatz. 
    vhp.umsatz.artnr = artikel1.artnr. 
    vhp.umsatz.datum = bill-date. 
    vhp.umsatz.departement = artikel1.departement. 
  END. 
  vhp.umsatz.betrag = vhp.umsatz.betrag + rest-betrag. 
  vhp.umsatz.anzahl = vhp.umsatz.anzahl + qty. 
  FIND CURRENT vhp.umsatz NO-LOCK. 
  
  CREATE vhp.billjournal. 
  ASSIGN
    vhp.billjournal.rechnr = vhp.h-bill.rechnr
    vhp.billjournal.artnr = artikel1.artnr
    vhp.billjournal.anzahl = qty
    vhp.billjournal.betrag = rest-betrag
    vhp.billjournal.bezeich = artikel1.bezeich 
      + "<" + STRING(vhp.h-bill.departement,"99") + ">"
    vhp.billjournal.departement = artikel1.departement 
    vhp.billjournal.epreis = 0
    vhp.billjournal.zeit = TIME 
    vhp.billjournal.userinit = user-init 
    vhp.billjournal.bill-datum = bill-date
  . 
  FIND CURRENT vhp.billjournal NO-LOCK. 
END. 
