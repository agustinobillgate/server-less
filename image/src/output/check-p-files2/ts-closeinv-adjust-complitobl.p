
DEFINE TEMP-TABLE t-h-bill  LIKE h-bill
    FIELD rec-id AS INT.

DEF INPUT  PARAMETER rec-h-bill       AS INT.
DEF INPUT  PARAMETER p-sign           AS INTEGER. 
DEF INPUT  PARAMETER p-artnr          AS INTEGER. 
DEF INPUT  PARAMETER h-artart         AS INTEGER.
DEF INPUT  PARAMETER curr-dept        AS INT.
DEF INPUT  PARAMETER pay-type         AS INT.
DEF INPUT  PARAMETER double-currency  AS LOGICAL.
DEF INPUT  PARAMETER exchg-rate       AS DECIMAL.
DEF INPUT  PARAMETER price-decimal    AS INT.
DEF INPUT  PARAMETER user-init        AS CHAR.

DEF OUTPUT PARAMETER balance-foreign  AS DECIMAL.
DEF OUTPUT PARAMETER balance          AS DECIMAL.
DEF OUTPUT PARAMETER TABLE FOR t-h-bill.

FIND FIRST h-bill WHERE RECID(h-bill) = rec-h-bill.
RUN adjust-complito.
FIND FIRST h-bill WHERE RECID(h-bill) = rec-h-bill.
CREATE t-h-bill.
BUFFER-COPY h-bill TO t-h-bill.
ASSIGN t-h-bill.rec-id = RECID(h-bill).

PROCEDURE adjust-complito: 

  DEFINE VARIABLE rest-betrag       AS DECIMAL.
  DEFINE VARIABLE argt-betrag       AS DECIMAL.
  
  DEFINE VARIABLE h-mwst            AS DECIMAL. 
  DEFINE VARIABLE h-service         AS DECIMAL. 
  DEFINE VARIABLE h-mwst-foreign    AS DECIMAL. 
  DEFINE VARIABLE h-service-foreign AS DECIMAL. 
  DEFINE VARIABLE epreis            AS DECIMAL. 
  DEFINE VARIABLE amount            AS DECIMAL. 
  DEFINE VARIABLE amount-foreign    AS DECIMAL. 
  DEFINE VARIABLE cost              AS DECIMAL. 
  DEFINE VARIABLE f-cost            AS DECIMAL INITIAL 0. 
  DEFINE VARIABLE b-cost            AS DECIMAL INITIAL 0. 
 
  DEFINE VARIABLE f-eknr AS INTEGER. 
  DEFINE VARIABLE b-eknr AS INTEGER. 
  DEFINE VARIABLE f-disc AS INTEGER NO-UNDO. 
  DEFINE VARIABLE b-disc AS INTEGER NO-UNDO. 
  DEFINE VARIABLE o-disc AS INTEGER NO-UNDO. 
 
  DEFINE BUFFER artikel1 FOR vhp.artikel.
  DEFINE BUFFER h-bline  FOR vhp.h-bill-line. 
  DEFINE BUFFER h-art    FOR vhp.h-artikel. 
  DEFINE BUFFER fr-art   FOR vhp.artikel. 
  DEFINE BUFFER kellner1 FOR vhp.kellner. 
  DEFINE BUFFER kellne1  FOR vhp.kellner. 
 
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
/* 
  FIND FIRST kellner1 WHERE kellner1.kellner-nr = vhp.h-bill.kellner-nr 
    AND kellner1.departement = curr-dept NO-LOCK. 
  FIND FIRST kellne1 WHERE kellne1.kellner-nr = vhp.h-bill.kellner-nr 
    AND kellne1.departement = curr-dept NO-LOCK. 
*/ 
  FIND FIRST h-bline WHERE h-bline.rechnr = vhp.h-bill.rechnr 
    AND h-bline.departement = curr-dept NO-LOCK NO-ERROR. 
  DO WHILE AVAILABLE h-bline: 
    FIND FIRST h-art WHERE h-art.artnr = h-bline.artnr 
      AND h-art.departement = h-bline.departement NO-LOCK NO-ERROR. 
    IF AVAILABLE h-art AND h-art.artart = 0 THEN 
    DO: 
      h-service = 0. 
      h-mwst = 0. 
      h-service-foreign = 0. 
      h-mwst-foreign = 0. 
      amount = 0. 
      amount-foreign = 0. 
 
      FIND FIRST vhp.h-umsatz WHERE vhp.h-umsatz.artnr = h-art.artnr 
        AND vhp.h-umsatz.departement = h-art.departement 
        AND vhp.h-umsatz.datum = h-bline.bill-datum EXCLUSIVE-LOCK NO-ERROR. 
      IF AVAILABLE vhp.h-umsatz AND pay-type = 5 THEN 
      DO: 
        vhp.h-umsatz.betrag = vhp.h-umsatz.betrag - p-sign * h-bline.betrag. 
        vhp.h-umsatz.anzahl = vhp.h-umsatz.anzahl - p-sign * h-bline.anzahl. 
        FIND CURRENT vhp.h-umsatz NO-LOCK. 
      END. 

      FIND FIRST vhp.umsatz WHERE vhp.umsatz.artnr = h-art.artnrfront 
        AND vhp.umsatz.departement = h-art.departement 
        AND vhp.umsatz.datum = h-bline.bill-datum EXCLUSIVE-LOCK NO-ERROR. 
      IF AVAILABLE vhp.umsatz THEN 
      DO: 
        vhp.umsatz.betrag = vhp.umsatz.betrag - p-sign * h-bline.betrag. 
        vhp.umsatz.anzahl = vhp.umsatz.anzahl - p-sign * h-bline.anzahl. 
        FIND CURRENT vhp.umsatz NO-LOCK. 
      END.
      FIND FIRST vhp.artikel WHERE vhp.artikel.artnr = vhp.umsatz.artnr
        AND vhp.artikel.departement = vhp.umsatz.departement NO-LOCK.
      IF vhp.artikel.artart = 9 THEN
      DO:
        ASSIGN
          amount = p-sign * h-bline.betrag
          rest-betrag = amount
        .
        FIND FIRST vhp.arrangement WHERE vhp.arrangement.argtnr 
          = vhp.artikel.artgrp NO-LOCK. 
        FOR EACH vhp.argt-line WHERE vhp.argt-line.argtnr 
          = vhp.arrangement.argtnr NO-LOCK: 
          IF vhp.argt-line.betrag NE 0 THEN 
          DO: 
            argt-betrag = p-sign * vhp.argt-line.betrag * h-bline.anzahl. 
            IF double-currency OR vhp.artikel.pricetab THEN 
              argt-betrag = ROUND(argt-betrag * exchg-rate, price-decimal). 
          END. 
          ELSE 
          ASSIGN
             argt-betrag = amount * vhp.argt-line.vt-percnt / 100
             argt-betrag = ROUND(argt-betrag, price-decimal)
          .
          rest-betrag = rest-betrag - argt-betrag.
          
          FIND FIRST artikel1 WHERE artikel1.artnr = vhp.argt-line.argt-artnr 
            AND artikel1.departement = vhp.argt-line.departement NO-LOCK. 
          FIND FIRST vhp.umsatz WHERE vhp.umsatz.artnr = artikel1.artnr 
            AND vhp.umsatz.departement = artikel1.departement 
            AND vhp.umsatz.datum = h-bline.bill-datum EXCLUSIVE-LOCK NO-ERROR. 
          IF NOT AVAILABLE vhp.umsatz THEN 
          DO: 
            CREATE vhp.umsatz. 
            ASSIGN
              vhp.umsatz.artnr = artikel1.artnr 
              vhp.umsatz.datum = h-bline.bill-datum
              vhp.umsatz.departement = artikel1.departement
            . 
          END. 
          ASSIGN
            vhp.umsatz.betrag = vhp.umsatz.betrag - argt-betrag
            vhp.umsatz.anzahl = vhp.umsatz.anzahl - p-sign * h-bline.anzahl
          . 
          FIND CURRENT vhp.umsatz NO-LOCK. 

          CREATE vhp.billjournal. 
          ASSIGN
            vhp.billjournal.rechnr = h-bline.rechnr
            vhp.billjournal.artnr = artikel1.artnr 
            vhp.billjournal.anzahl = - p-sign * h-bline.anzahl
            vhp.billjournal.betrag = - argt-betrag 
            vhp.billjournal.bezeich = artikel1.bezeich 
              + "<" + STRING(h-bline.departement,"99") + ">"
            vhp.billjournal.departement = artikel1.departement
            vhp.billjournal.epreis = 0 
            vhp.billjournal.zeit = TIME
            vhp.billjournal.userinit = user-init
            vhp.billjournal.bill-datum = h-bline.bill-datum
          .
          FIND CURRENT vhp.billjournal NO-LOCK. 
        END. 

        FIND FIRST artikel1 WHERE artikel1.artnr = vhp.arrangement.artnr-logis
          AND artikel1.departement = vhp.arrangement.intervall NO-LOCK. 
        FIND FIRST vhp.umsatz WHERE vhp.umsatz.artnr = artikel1.artnr 
          AND vhp.umsatz.departement = artikel1.departement 
          AND vhp.umsatz.datum = h-bline.bill-datum EXCLUSIVE-LOCK NO-ERROR. 
        IF NOT AVAILABLE vhp.umsatz THEN 
        DO: 
          CREATE vhp.umsatz. 
          ASSIGN
            vhp.umsatz.artnr = artikel1.artnr 
            vhp.umsatz.datum = h-bline.bill-datum
            vhp.umsatz.departement = artikel1.departement
          . 
        END. 
        ASSIGN
          vhp.umsatz.betrag = vhp.umsatz.betrag - rest-betrag
          vhp.umsatz.anzahl = vhp.umsatz.anzahl - p-sign * h-bline.anzahl
        . 
        FIND CURRENT vhp.umsatz NO-LOCK. 

        CREATE vhp.billjournal. 
        ASSIGN
            vhp.billjournal.rechnr = h-bline.rechnr
            vhp.billjournal.artnr = artikel1.artnr 
            vhp.billjournal.anzahl = - p-sign * h-bline.anzahl
            vhp.billjournal.betrag = - rest-betrag 
            vhp.billjournal.bezeich = artikel1.bezeich 
              + "<" + STRING(h-bline.departement,"99") + ">"
            vhp.billjournal.departement = artikel1.departement
            vhp.billjournal.epreis = 0 
            vhp.billjournal.zeit = TIME 
            vhp.billjournal.userinit = user-init
            vhp.billjournal.bill-datum = h-bline.bill-datum
        .
        FIND CURRENT vhp.billjournal NO-LOCK. 
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
      IF vhp.h-bline.artnr NE f-disc AND vhp.h-bline.artnr NE b-disc 
        AND vhp.h-bline.artnr NE o-disc THEN 
      DO: 
        FIND FIRST vhp.h-journal WHERE vhp.h-journal.bill-datum 
          = h-bline.bill-datum 
          AND vhp.h-journal.zeit = h-bline.zeit 
          AND vhp.h-journal.sysdate = h-bline.sysdate 
          AND vhp.h-journal.artnr = h-bline.artnr 
          AND vhp.h-journal.departement = h-bline.departement 
          EXCLUSIVE-LOCK USE-INDEX chrono_ix. 
        vhp.h-journal.fremdwaehrng = h-bline.fremdwbetrag. 
        vhp.h-journal.betrag = h-bline.betrag. 
        FIND CURRENT vhp.h-journal NO-LOCK. 
      END. 
 
      FIND CURRENT vhp.h-bill EXCLUSIVE-LOCK. 
      vhp.h-bill.gesamtumsatz = vhp.h-bill.gesamtumsatz 
        - p-sign * h-bline.betrag. 
      vhp.h-bill.mwst[99] = vhp.h-bill.mwst[99] 
        - p-sign * (h-service-foreign + h-mwst-foreign) * h-bline.anzahl. 
      vhp.h-bill.saldo = vhp.h-bill.saldo 
        - p-sign * (h-service + h-mwst) * h-bline.anzahl. 
      FIND CURRENT vhp.h-bill NO-LOCK. 
 
      balance-foreign = vhp.h-bill.mwst[99]. 
      balance = vhp.h-bill.saldo. 
 
      IF h-artart = 11 THEN 
      DO: 
        CREATE vhp.h-compli. 
        vhp.h-compli.datum = h-bline.bill-datum. 
        vhp.h-compli.departement = h-bline.departement. 
        vhp.h-compli.rechnr = h-bline.rechnr. 
        vhp.h-compli.artnr = h-bline.artnr. 
        vhp.h-compli.anzahl = p-sign * h-bline.anzahl. 
        vhp.h-compli.epreis = h-bline.epreis. 
        vhp.h-compli.p-artnr = p-artnr. 
        FIND CURRENT vhp.h-compli NO-LOCK. 
      END. 
    END. 
    FIND NEXT h-bline WHERE h-bline.rechnr = vhp.h-bill.rechnr 
      AND h-bline.departement = curr-dept NO-LOCK NO-ERROR. 
  END. 
END. 

