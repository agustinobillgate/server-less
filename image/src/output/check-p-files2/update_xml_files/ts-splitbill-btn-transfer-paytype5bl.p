  
DEF TEMP-TABLE t-h-bill-line LIKE h-bill-line  
    FIELD rec-id AS INT.  
  
DEF INPUT PARAMETER curr-select AS INT.  
DEF INPUT PARAMETER rec-id-h-bill AS INT.  
DEF INPUT PARAMETER p-artnr AS INT.  
DEF INPUT PARAMETER balance AS DECIMAL.  
DEF INPUT PARAMETER price-decimal AS INT.  
DEF INPUT PARAMETER transdate AS DATE.  
  
DEF INPUT PARAMETER dept AS INT.  
DEF INPUT PARAMETER change-str AS CHAR.  
DEF INPUT PARAMETER price AS DECIMAL.  
DEF INPUT PARAMETER add-zeit AS INT.  
DEF INPUT PARAMETER hoga-card AS CHAR.  
DEF INPUT PARAMETER cancel-str AS CHAR.  
DEF INPUT PARAMETER curr-waiter AS INTEGER.  
DEF INPUT PARAMETER amount-foreign AS DECIMAL.  
DEF INPUT PARAMETER curr-room AS CHAR.  
DEF INPUT PARAMETER user-init AS CHAR.  
DEF INPUT PARAMETER cc-comment AS CHAR.  
DEF INPUT PARAMETER guestnr AS INT.  
DEF INPUT PARAMETER tischnr AS INT.  
  
DEF OUTPUT PARAMETER billart AS INT.  
DEF OUTPUT PARAMETER qty AS INT.  
DEF OUTPUT PARAMETER description AS CHAR.  
DEF OUTPUT PARAMETER amount AS DECIMAL.  
DEF OUTPUT PARAMETER bill-date AS DATE.  
DEF OUTPUT PARAMETER fl-code AS INT INIT 0.  
DEF OUTPUT PARAMETER TABLE FOR t-h-bill-line.  
  
FIND FIRST h-bill WHERE RECID(h-bill) = rec-id-h-bill.  
  
RUN adjust-compliment-umsatz(curr-select).   
FIND FIRST vhp.h-artikel WHERE vhp.h-artikel.departement =   
  vhp.h-bill.departement   
  AND vhp.h-artikel.artnr = p-artnr NO-LOCK.   
billart = vhp.h-artikel.artnr.   
qty = 1.   
description = vhp.h-artikel.bezeich.   
amount = - balance.   
RUN ts-splitbill-update-billbl.p  
    (rec-id-h-bill, RECID(h-artikel), h-artikel.artart, vhp.h-artikel.artnrfront, dept, amount, transdate, billart, description, change-str, qty, tischnr,  
     price, add-zeit, curr-select, hoga-card, cancel-str, curr-waiter, amount-foreign,  
     curr-room, user-init, cc-comment, guestnr, OUTPUT bill-date).  
/*MTDISP balance  WITH FRAME frame1.*/  
IF ROUND(vhp.h-bill.saldo, price-decimal) = 0 THEN   
DO:   
  RUN del-queasy.   
  FIND CURRENT vhp.h-bill EXCLUSIVE-LOCK.   
  vhp.h-bill.flag = 1.   
  FIND CURRENT vhp.h-bill NO-LOCK.  
  fl-code = 1.  
  /*MTAPPLY "choose" TO btn-b IN FRAME frame1.*/  
END.   
ELSE   
DO:   
  /*MTbalance = 0.   
  DISP balance WITH FRAME frame1.   
  RUN build-rmenu.   
  RUN fill-rmenu.*/  
  fl-code = 2.  
END.  
  
  
PROCEDURE adjust-compliment-umsatz:   
  DEFINE INPUT PARAMETER curr-select AS INTEGER.   
  DEFINE VARIABLE h-mwst AS DECIMAL.   
  DEFINE VARIABLE h-service AS DECIMAL.   
  DEFINE VARIABLE epreis AS DECIMAL.   
  DEFINE VARIABLE amount AS DECIMAL.   
  DEFINE VARIABLE f-cost AS DECIMAL INITIAL 0.   
  DEFINE VARIABLE b-cost AS DECIMAL INITIAL 0.   
  DEFINE VARIABLE cost AS DECIMAL INITIAL 0.   
  DEFINE VARIABLE f-eknr AS INTEGER.   
  DEFINE VARIABLE b-eknr AS INTEGER.   
   
  DEFINE buffer h-bline FOR vhp.h-bill-line.   
  DEFINE buffer h-art FOR vhp.h-artikel.   
  DEFINE buffer fr-art FOR vhp.artikel.   
  DEFINE buffer kellner1 FOR vhp.kellner.   
  
   
  FIND FIRST vhp.htparam WHERE paramnr = 862 NO-LOCK.   
  f-eknr = htparam.finteger.               /* Rulita 211024 | Fixing for serverless */    
  FIND FIRST vhp.htparam WHERE paramnr = 892 NO-LOCK.   
  b-eknr = htparam.finteger.               /* Rulita 211024 | Fixing for serverless */    
   
  FIND FIRST vhp.kellner1 WHERE vhp.kellner1.kellner-nr = vhp.h-bill.kellner-nr   
    AND vhp.kellner1.departement = vhp.h-bill.departement NO-LOCK.   
  FIND FIRST vhp.kellne1 WHERE vhp.kellne1.kellner-nr = vhp.h-bill.kellner-nr   
    AND kellne1.departement = vhp.h-bill.departement NO-LOCK.   
   
  FIND FIRST h-bline WHERE h-bline.rechnr = vhp.h-bill.rechnr   
    AND vhp.h-bill-line.waehrungsnr = curr-select NO-LOCK NO-ERROR.   
  DO WHILE AVAILABLE h-bline:   
    FIND FIRST h-art WHERE h-art.artnr = h-bline.artnr   
      AND h-art.departement = h-bline.departement NO-LOCK.   
    IF h-art.artart = 0 THEN   
    DO:   
      h-service = 0.   
      h-mwst = 0.   
      amount = 0.   
      FIND FIRST vhp.h-umsatz WHERE vhp.h-umsatz.artnr = h-art.artnr   
        AND vhp.h-umsatz.departement = h-art.departement   
        AND vhp.h-umsatz.datum = h-bline.bill-datum EXCLUSIVE-LOCK.   
      vhp.h-umsatz.betrag = vhp.h-umsatz.betrag - h-bline.betrag.   
      vhp.h-umsatz.anzahl = vhp.h-umsatz.anzahl - h-bline.anzahl.   
      FIND CURRENT vhp.h-umsatz NO-LOCK.   
   
      FIND FIRST vhp.umsatz WHERE vhp.umsatz.artnr = h-art.artnrfront   
        AND vhp.umsatz.departement = h-art.departement   
        AND vhp.umsatz.datum = h-bline.bill-datum EXCLUSIVE-LOCK.   
      vhp.umsatz.betrag = vhp.umsatz.betrag - h-bline.betrag.   
      vhp.umsatz.anzahl = vhp.umsatz.anzahl - h-bline.anzahl.   
      FIND CURRENT vhp.umsatz NO-LOCK.   
/*   
      FIND FIRST vhp.umsatz WHERE vhp.umsatz.artnr = vhp.kellner1.kumsatz-nr   
        AND vhp.umsatz.departement = h-bline.departement   
        AND vhp.umsatz.datum = h-bline.bill-datum EXCLUSIVE-LOCK NO-ERROR.   
      vhp.umsatz.betrag = vhp.umsatz.betrag - h-bline.betrag.   
      vhp.umsatz.anzahl = vhp.umsatz.anzahl - h-bline.anzahl.   
      FIND CURRENT vhp.umsatz NO-LOCK.   
*/   
      FIND FIRST vhp.h-journal WHERE vhp.h-journal.bill-datum   
        = h-bline.bill-datum   
        AND vhp.h-journal.zeit = h-bline.zeit   
        AND vhp.h-journal.sysdate = h-bline.sysdate   
        AND vhp.h-journal.artnr = h-bline.artnr   
        AND vhp.h-journal.departement = h-bline.departement   
        EXCLUSIVE-LOCK USE-INDEX chrono_ix.   
      vhp.h-journal.betrag = h-bline.betrag.   
      FIND CURRENT vhp.h-journal NO-LOCK.   
   
      FIND CURRENT vhp.h-bill EXCLUSIVE-LOCK.   
      vhp.h-bill.gesamtumsatz = vhp.h-bill.gesamtumsatz - h-bline.betrag.   
      FIND CURRENT vhp.h-bill NO-LOCK.   
    END.   
   
    CREATE h-compli.   
    h-compli.datum = h-bline.bill-datum.   
    h-compli.departement = h-bline.departement.   
    h-compli.rechnr = h-bline.rechnr.   
    h-compli.artnr = h-bline.artnr.   
    h-compli.anzahl = h-bline.anzahl.   
    h-compli.epreis = h-bline.epreis.   
    h-compli.p-artnr = p-artnr.   
   
/*** Calculate fb-cost, - outlet cost, + (compliment) dept cost ***/   
    f-cost = 0.   
    b-cost = 0.   
    FIND FIRST fr-art WHERE fr-art.departement = h-art.departement   
      AND fr-art.artnr = h-art.artnrfront NO-LOCK.   
    IF h-art.artnrlager NE 0 THEN   /* stock article */   
    DO:   
      FIND FIRST vhp.l-artikel WHERE vhp.l-artikel.artnr = h-art.artnrlager   
        NO-LOCK NO-ERROR.   
      IF AVAILABLE vhp.l-artikel THEN   
      DO:   
        IF fr-art.endkum = f-eknr THEN   
          f-cost = vhp.l-artikel.vk-preis * h-bline.anzahl.   
        ELSE IF fr-art.endkum = b-eknr THEN   
          b-cost = vhp.l-artikel.vk-preis * h-bline.anzahl.   
      END.   
    END.   
    ELSE IF h-art.artnrrezept NE 0 THEN   
    DO:   
      cost = 0.   
      FIND FIRST vhp.h-rezept WHERE   
        vhp.h-rezept.artnrrezept = h-art.artnrrezept NO-LOCK NO-ERROR.   
      IF AVAILABLE vhp.h-rezept THEN   
      DO:   
        RUN cal-cost(h-rezept.artnrrezept, 1, INPUT-OUTPUT cost).   
        IF fr-art.endkum = f-eknr THEN f-cost = cost * h-bline.anzahl.   
        ELSE IF fr-art.endkum = b-eknr THEN b-cost = cost * h-bline.anzahl.   
      END.   
    END.   
    ELSE   
    DO:   
      IF fr-art.endkum = f-eknr THEN f-cost = h-art.prozent * h-bline.anzahl.   
      ELSE IF fr-art.endkum = b-eknr THEN   
        b-cost = h-art.prozent * h-bline.anzahl.   
    END.   
    IF f-cost NE 0 OR b-cost NE 0 THEN   
    DO:   
      FIND FIRST vhp.htparam WHERE vhp.htparam.paramnr = 110 NO-LOCK.   
      bill-date = vhp.htparam.fdate.   
      IF transdate NE ? THEN bill-date = transdate.   
      ELSE  
      DO:  
        FIND FIRST vhp.htparam WHERE vhp.htparam.paramnr = 253 NO-LOCK. /* NA running */   
        IF vhp.htparam.flogical AND bill-date LT TODAY THEN bill-date = bill-date + 1.   
      END.  
  
      /* 1. minus outlet cost */   
      FIND FIRST gl-acct WHERE gl-acct.fibukonto = fr-art.bezeich1   
        NO-LOCK NO-ERROR.   
      IF AVAILABLE gl-acct THEN   
      DO:   
        FIND FIRST gl-cost WHERE gl-cost.fibukonto = gl-acct.fibukonto   
          AND gl-cost.datum = bill-date EXCLUSIVE-LOCK NO-ERROR.   
        IF NOT AVAILABLE gl-cost THEN   
        DO:   
          CREATE gl-cost.   
          gl-cost.fibukonto = gl-acct.fibukonto.   
          gl-cost.datum = bill-date.   
        END.   
        gl-cost.f-betrag = gl-cost.f-betrag - f-cost.   
        gl-cost.b-betrag = gl-cost.b-betrag - b-cost.   
        gl-cost.betrag = gl-cost.betrag - f-cost - b-cost.   
        FIND CURRENT gl-cost NO-LOCK.   
      END.   
/* 2. plus dept cost */   
      FIND FIRST vhp.h-artikel WHERE vhp.h-artikel.departement = dept   
        AND vhp.h-artikel.artnr = p-artnr NO-LOCK.   
      FIND FIRST fr-art WHERE fr-art.artnr = vhp.h-artikel.artnrfront   
        AND fr-art.departement = 0 no-lock.   /* f/o compliment article */   
      FIND FIRST gl-acct WHERE gl-acct.fibukonto = fr-art.fibukonto   
        NO-LOCK NO-ERROR.   
      IF AVAILABLE gl-acct THEN   
      DO:   
        FIND FIRST gl-cost WHERE gl-cost.fibukonto = gl-acct.fibukonto   
          AND gl-cost.datum = bill-date EXCLUSIVE-LOCK NO-ERROR.   
        IF NOT AVAILABLE gl-cost THEN   
        DO:   
          CREATE gl-cost.   
          gl-cost.fibukonto = gl-acct.fibukonto.   
          gl-cost.datum = bill-date.   
        END.   
        gl-cost.f-betrag = gl-cost.f-betrag + f-cost.   
        gl-cost.b-betrag = gl-cost.b-betrag + b-cost.   
        gl-cost.betrag = gl-cost.betrag + f-cost + b-cost.   
        FIND CURRENT gl-cost NO-LOCK.   
      END.   
    END.   
   
    FIND NEXT h-bline WHERE h-bline.rechnr = vhp.h-bill.rechnr   
      AND vhp.h-bill-line.waehrungsnr = curr-select NO-LOCK NO-ERROR.   
  END.   
END.   
  
FOR EACH h-bill-line WHERE h-bill-line.departement = dept NO-LOCK:  
  CREATE t-h-bill-line.  
  BUFFER-COPY h-bill-line TO t-h-bill-line.  
  ASSIGN t-h-bill-line.rec-id = RECID(h-bill-line).  
END.  
  
  
PROCEDURE del-queasy:   
  FOR EACH vhp.queasy WHERE vhp.queasy.key = 4   
    AND vhp.queasy.number1 = (vhp.h-bill.departement + vhp.h-bill.rechnr * 100)   
    AND vhp.queasy.number2 GE 0 AND vhp.queasy.deci2 GE 0 EXCLUSIVE-LOCK:   
    DELETE vhp.queasy.   
  END.   
  RELEASE vhp.queasy.
END.   
  
