  
DEF TEMP-TABLE t-h-bill-line LIKE h-bill-line  
    FIELD rec-id AS INT.  
  
DEF INPUT PARAMETER rec-id-h-bill AS INT.  
DEF INPUT PARAMETER curr-select AS INT.  
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
  
DEFINE buffer kellner1 FOR vhp.kellner.   
  
FIND FIRST h-bill WHERE RECID(h-bill) = rec-id-h-bill.  
  
RUN adjust-mealcoupon-umsatz(curr-select).   
FIND FIRST vhp.h-artikel WHERE vhp.h-artikel.departement =   
   vhp.h-bill.departement AND vhp.h-artikel.artnr = p-artnr NO-LOCK.   
billart = vhp.h-artikel.artnr.   
qty = 1.   
description = vhp.h-artikel.bezeich.   
amount = - balance.   
RUN ts-splitbill-update-billbl.p  
    (rec-id-h-bill, RECID(h-artikel), h-artikel.artart, vhp.h-artikel.artnrfront, dept, amount, transdate, billart, description, change-str, qty, tischnr,  
     price, add-zeit, curr-select, hoga-card, cancel-str, curr-waiter, amount-foreign,  
     curr-room, user-init, cc-comment, guestnr, OUTPUT bill-date).  
IF ROUND(vhp.h-bill.saldo, price-decimal) = 0 THEN   
DO:   
  RUN del-queasy.   
  FIND CURRENT vhp.h-bill EXCLUSIVE-LOCK.   
  vhp.h-bill.flag = 1.   
  FIND CURRENT vhp.h-bill NO-LOCK.  
  fl-code = 1.  
END.   
ELSE   
DO:   
  fl-code = 2.  
END.  
  
FOR EACH h-bill-line WHERE h-bill-line.departement = dept NO-LOCK:  
  CREATE t-h-bill-line.  
  BUFFER-COPY h-bill-line TO t-h-bill-line.  
  ASSIGN t-h-bill-line.rec-id = RECID(h-bill-line).  
END.  
   
  
  
PROCEDURE adjust-mealcoupon-umsatz:   
  DEFINE INPUT PARAMETER curr-select AS INTEGER.   
  DEFINE VARIABLE h-mwst AS DECIMAL.   
  DEFINE VARIABLE h-service AS DECIMAL.   
  DEFINE VARIABLE epreis AS DECIMAL.   
  DEFINE VARIABLE amount AS DECIMAL.   
  DEFINE buffer h-bline FOR vhp.h-bill-line.   
  DEFINE buffer h-art FOR vhp.h-artikel.   
   
  FIND FIRST vhp.kellner1 WHERE vhp.kellner1.kellner-nr = vhp.h-bill.kellner-nr   
    AND vhp.kellner1.departement = vhp.h-bill.departement NO-LOCK.   
  FIND FIRST kellne1 WHERE kellne1.kellner-nr = vhp.h-bill.kellner-nr   
    AND kellne1.departement = vhp.h-bill.departement NO-LOCK.   
   
  FOR EACH h-bline WHERE h-bline.rechnr = vhp.h-bill.rechnr   
    AND vhp.h-bill-line.waehrungsnr = curr-select,   
    FIRST h-art WHERE h-art.artnr = h-bline.artnr   
      AND h-art.departement = h-bline.departement   
      AND h-art.artart = 0 NO-LOCK:   
   
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
   
    FIND FIRST vhp.umsatz WHERE vhp.umsatz.artnr = vhp.kellner1.kumsatz-nr   
      AND vhp.umsatz.departement = h-bline.departement   
      AND vhp.umsatz.datum = h-bline.bill-datum EXCLUSIVE-LOCK NO-ERROR.   
    vhp.umsatz.betrag = vhp.umsatz.betrag - h-bline.betrag.   
    vhp.umsatz.anzahl = vhp.umsatz.anzahl - h-bline.anzahl.   
    FIND CURRENT vhp.umsatz NO-LOCK.   
   
    CREATE h-compli.   
    h-compli.datum = h-bline.bill-datum.   
    h-compli.departement = h-bline.departement.   
    h-compli.rechnr = h-bline.rechnr.   
    h-compli.artnr = h-bline.artnr.   
    h-compli.anzahl = h-bline.anzahl.   
    h-compli.epreis = h-bline.epreis.   
    h-compli.p-artnr = p-artnr.   
   
  END.   
END.   
  
PROCEDURE del-queasy:   
  FOR EACH vhp.queasy WHERE vhp.queasy.key = 4   
    AND vhp.queasy.number1 = (vhp.h-bill.departement + vhp.h-bill.rechnr * 100)   
    AND vhp.queasy.number2 GE 0 AND vhp.queasy.deci2 GE 0 EXCLUSIVE-LOCK:   
    DELETE vhp.queasy.   
  END.   
  RELEASE vhp.queasy.
END.   
  
