DEFINE TEMP-TABLE s-list 
  FIELD artnr       AS INTEGER 
  FIELD qty         AS DECIMAL 
  FIELD s-qty       AS DECIMAL 
  FIELD wert        AS DECIMAL 
  FIELD op-recid1   AS INTEGER 
  FIELD op-recid2   AS INTEGER. 

DEFINE TEMP-TABLE t-l-order LIKE l-order
    FIELD rec-id AS INT
    FIELD a-bezeich LIKE l-artikel.bezeich
    FIELD jahrgang LIKE l-artikel.jahrgang
    FIELD alkoholgrad LIKE l-artikel.alkoholgrad.

DEF INPUT PARAMETER amount              AS DECIMAL. 
DEF INPUT PARAMETER user-init           AS CHAR.
DEF INPUT PARAMETER recid-l-order       AS INT.
DEF INPUT PARAMETER recid-l-orderhdr    AS INT.
DEF INPUT PARAMETER l-art-artnr         AS INT.
DEF INPUT PARAMETER price               AS DECIMAL.
DEF INPUT PARAMETER billdate            AS DATE.
DEF INPUT PARAMETER lief-nr             AS INT.
DEF INPUT PARAMETER docu-nr             AS CHAR.
DEF INPUT PARAMETER curr-disc           AS INT.
DEF INPUT PARAMETER curr-disc2          AS INT.
DEF INPUT PARAMETER curr-vat            AS INT.
DEF INPUT PARAMETER curr-vat1           AS INT.
DEF INPUT PARAMETER curr-lager          AS INT.
DEF INPUT PARAMETER cost-acct           AS CHAR.
DEF INPUT PARAMETER lscheinnr           LIKE l-op.lscheinnr.
DEF INPUT PARAMETER jobnr               AS INT.
DEF INPUT PARAMETER f-endkum            AS INT.
DEF INPUT PARAMETER b-endkum            AS INT.
DEF INPUT PARAMETER m-endkum            AS INT.
DEF INPUT PARAMETER fb-closedate        AS DATE.
DEF INPUT PARAMETER m-closedate         AS DATE.
DEF INPUT PARAMETER s-artnr             AS INT.

DEF INPUT-OUTPUT PARAMETER t-amount     AS DECIMAL.
DEF INPUT-OUTPUT PARAMETER qty          AS DECIMAL.
DEF INPUT-OUTPUT PARAMETER s-qty        AS INT.

DEF OUTPUT PARAMETER epreis             AS DECIMAL.
DEF OUTPUT PARAMETER orig-preis         AS DECIMAL.
DEF OUTPUT PARAMETER TABLE FOR s-list.
DEF OUTPUT PARAMETER TABLE FOR t-l-order.

FIND FIRST l-order WHERE RECID(l-order) = recid-l-order.
FIND FIRST bediener WHERE bediener.userinit = user-init NO-LOCK. 
FIND FIRST l-orderhdr WHERE RECID(l-orderhdr) = recid-l-orderhdr.
FIND FIRST l-art WHERE l-art.artnr = l-art-artnr.

RUN create-l-op.

FOR EACH l-order WHERE /*l-order.docu-nr = docu-nr
    AND*/ l-order.pos GT 0 AND l-order.loeschflag = 0:
    CREATE t-l-order.
    BUFFER-COPY l-order TO t-l-order.
    ASSIGN t-l-order.rec-id = RECID(l-order).

    FIND FIRST l-artikel WHERE l-artikel.artnr = l-order.artnr NO-LOCK.
    ASSIGN 
        t-l-order.a-bezeich = l-artikel.bezeich
        t-l-order.jahrgang = l-artikel.jahrgang
        t-l-order.alkoholgrad = l-artikel.alkoholgrad.
END.

PROCEDURE create-l-op:
DEFINE VARIABLE anzahl AS DECIMAL FORMAT ">>>,>>9.999". 
DEFINE VARIABLE wert AS DECIMAL. 
DEFINE VARIABLE tot-wert AS DECIMAL. 
DEFINE VARIABLE tot-anz AS DECIMAL. 
DEFINE buffer l-order1 FOR l-order. 
DEFINE VARIABLE curr-pos AS INTEGER. 
 
  FIND CURRENT l-order EXCLUSIVE-LOCK. 
 
  DO WHILE s-qty GE l-order.txtnr: 
    s-qty = s-qty - l-order.txtnr. 
    qty = qty + 1. 
  END. 
 
  anzahl = qty * l-order.txtnr + s-qty. 
  IF l-order.flag THEN epreis = price / l-order.txtnr. 
  ELSE epreis = price. 
  
  wert = amount.
/*
  wert = anzahl * epreis. 
  wert = wert * exchg-rate. 
  wert = round(wert, price-decimal). 
*/

  l-order.geliefert = l-order.geliefert + qty. 
  l-order.angebot-lief[1] = l-order.angebot-lief[1] + s-qty. 
  l-order.lief-fax[2] = bediener.username. 
  DO WHILE l-order.angebot-lief[1] GE l-order.txtnr: 
    l-order.angebot-lief[1] = l-order.angebot-lief[1] - l-order.txtnr. 
    l-order.geliefert = l-order.geliefert + 1. 
  END. 
 
  l-order.rechnungspreis = price. 
  l-order.rechnungswert = l-order.rechnungswert + wert. 
  l-order.lieferdatum-eff = billdate. 
  l-order.lief-fax[2] = bediener.username. 
 
  amount = wert. 
  t-amount = t-amount + wert. 
  FIND CURRENT l-order NO-LOCK. 
 
  FIND FIRST l-order1 WHERE l-order1.docu-nr = l-orderhdr.docu-nr 
    AND l-order1.pos = 0 EXCLUSIVE-LOCK. 
  l-order1.rechnungspreis = l-order1.rechnungspreis + wert. 
  l-order1.rechnungswert = l-order1.rechnungswert + wert. 
  FIND CURRENT l-order1 NO-LOCK. 
 
  IF l-art.ek-aktuell NE epreis THEN 
  DO: 
    FIND CURRENT l-art EXCLUSIVE-LOCK. 
    l-art.ek-letzter = l-art.ek-aktuell. 
    l-art.ek-aktuell = epreis. 
    FIND CURRENT l-art NO-LOCK. 
  END. 
 
 
/* UPDATE supplier turnover */ 
  FIND FIRST  l-liefumsatz WHERE l-liefumsatz.lief-nr = lief-nr 
    AND l-liefumsatz.datum = billdate EXCLUSIVE-LOCK NO-ERROR. 
  IF NOT AVAILABLE l-liefumsatz THEN 
  DO: 
    create l-liefumsatz. 
    l-liefumsatz.datum = billdate. 
    l-liefumsatz.lief-nr = lief-nr. 
  END. 
  l-liefumsatz.gesamtumsatz = l-liefumsatz.gesamtumsatz + wert. 
 
  orig-preis = epreis / (1 - curr-disc / 10000) / (1 - curr-disc2 / 10000) 
    / (1 + curr-vat / 10000). 
 
/* Create l-op record */ 
  CREATE l-op. 
  l-op.datum = billdate. 
  l-op.lager-nr = curr-lager. 
  l-op.artnr = l-art.artnr. 
  l-op.lief-nr = lief-nr. 
  l-op.zeit = time. 
  l-op.anzahl = anzahl. 
  l-op.einzelpreis = epreis. 
  l-op.warenwert = wert. 
  l-op.deci1[1] = orig-preis. 
  l-op.deci1[2] = curr-disc / 100. 
  l-op.rueckgabegrund = curr-disc2. 
  IF curr-vat NE 0 THEN 
  DO: 
    l-op.deci1[3] = curr-vat / 100. 
    l-op.deci1[4] = price * l-op.deci1[3] / 100. 
  END. 
  ELSE 
  DO: 
    l-op.deci1[3] = curr-vat1 / 100. 
    l-op.deci1[4] = price * l-op.deci1[3] / 100. 
  END. 
  l-op.op-art = 1. 
  l-op.herkunftflag = 2.    /* 4 = inventory !!! */ 
  l-op.docu-nr = docu-nr. 
  l-op.lscheinnr = lscheinnr. 
  RUN l-op-pos(OUTPUT curr-pos). 
  l-op.pos = curr-pos. 
  l-op.fuellflag = bediener.nr. 
  l-op.flag = yes.   /* flag indicates direct issue **/ 
  l-op.stornogrund = cost-acct. 
  FIND CURRENT l-op NO-LOCK. 
 
  create s-list. 
  s-list.op-recid1 = RECID(l-op). 
  s-list.artnr = l-op.artnr. 
  s-list.qty = qty. 
  s-list.s-qty = s-qty. 
  s-list.wert = wert. 
 
  RUN create-purchase-book. 
 
/* Create l-op record  FOR outgoing */ 
  create l-op. 
  l-op.datum = billdate. 
  l-op.lager-nr = curr-lager. 
  l-op.artnr = l-art.artnr. 
  l-op.lief-nr = lief-nr. 
  l-op.zeit = time. 
  l-op.anzahl = anzahl. 
  l-op.einzelpreis = epreis. 
  l-op.warenwert = wert. 
  l-op.op-art = 3. 
  l-op.herkunftflag = 2.    /* 4 = inventory !!! */ 
  l-op.docu-nr = docu-nr. 
  l-op.lscheinnr = lscheinnr. 
  l-op.pos = curr-pos. 
  l-op.fuellflag = bediener.nr. 
  l-op.flag = yes.   /* flag indicates direct issue **/ 
  l-op.stornogrund = cost-acct. 
  FIND CURRENT l-op NO-LOCK. 
 
  s-list.op-recid2 = RECID(l-op). 
  /*MTENABLE btn-del WITH FRAME frame1. */
 
/* create l-ophdr FOR incoming */ 
  FIND FIRST l-ophdr WHERE l-ophdr.lscheinnr = lscheinnr 
    AND l-ophdr.op-typ = "STI" NO-LOCK NO-ERROR. 
  IF NOT AVAILABLE l-ophdr THEN 
  DO: 
    create l-ophdr. 
    l-ophdr.datum = billdate. 
    l-ophdr.lager-nr = curr-lager. 
    l-ophdr.docu-nr = docu-nr. 
    l-ophdr.lscheinnr = lscheinnr. 
    l-ophdr.op-typ = "STI". 
    FIND CURRENT l-ophdr NO-LOCK. 
  END. 
 
/* create l-ophdr  FOR outgoing */ 
  FIND FIRST l-ophdr WHERE l-ophdr.lscheinnr = lscheinnr 
    AND l-ophdr.op-typ = "STT" NO-LOCK NO-ERROR. 
  IF NOT AVAILABLE l-ophdr THEN 
  DO: 
    create l-ophdr. 
    l-ophdr.datum = billdate. 
    l-ophdr.lager-nr = curr-lager. 
    l-ophdr.docu-nr = docu-nr. 
    l-ophdr.lscheinnr = lscheinnr. 
    l-ophdr.op-typ = "STT". 
    l-ophdr.fibukonto = cost-acct. 
    l-ophdr.betriebsnr = jobnr. 
    FIND CURRENT l-ophdr NO-LOCK. 
  END. 
 
  /**
  IF jobnr NE 0 THEN 
    RUN create-lartjob.p(RECID(l-ophdr), l-art.artnr, anzahl, 
      wert, billdate, YES). 
  **/
/* %%% 
  FIND FIRST l-bestand WHERE l-bestand.lager-nr = curr-lager AND 
    l-bestand.artnr = s-artnr NO-LOCK NO-ERROR. 
  IF NOT AVAILABLE l-bestand THEN 
  DO: 
    create l-bestand. 
    l-bestand.lager-nr = curr-lager. 
    l-bestand.artnr = s-artnr. 
    l-bestand.anf-best-dat = billdate. 
    FIND CURRENT l-bestand NO-LOCK. 
  END. 
 
  FIND FIRST l-bestand WHERE l-bestand.lager-nr = 0 AND 
    l-bestand.artnr = s-artnr NO-LOCK NO-ERROR. 
  IF NOT AVAILABLE l-bestand THEN 
  DO: 
    create l-bestand. 
    l-bestand.artnr = s-artnr. 
    l-bestand.anf-best-dat = billdate. 
    FIND CURRENT l-bestand NO-LOCK. 
  END. 
*/ 
 
  IF ((l-art.endkum = f-endkum OR l-art.endkum = b-endkum) 
    AND billdate LE fb-closedate) 
  OR (l-art.endkum GE m-endkum AND billdate LE m-closedate) THEN 
  DO: 
    FIND FIRST l-bestand WHERE l-bestand.lager-nr = curr-lager AND 
      l-bestand.artnr = s-artnr EXCLUSIVE-LOCK NO-ERROR. 
    IF NOT AVAILABLE l-bestand THEN 
    DO: 
      create l-bestand. 
      l-bestand.lager-nr = curr-lager. 
      l-bestand.artnr = s-artnr. 
      l-bestand.anf-best-dat = billdate. 
    END. 
    l-bestand.anz-eingang = l-bestand.anz-eingang + anzahl. 
    l-bestand.wert-eingang = l-bestand.wert-eingang + wert. 
    l-bestand.anz-ausgang = l-bestand.anz-ausgang + anzahl. 
    l-bestand.wert-ausgang = l-bestand.wert-ausgang + wert. 
    FIND CURRENT l-bestand NO-LOCK. 
 
    FIND FIRST l-bestand WHERE l-bestand.lager-nr = 0 AND 
      l-bestand.artnr = s-artnr EXCLUSIVE-LOCK NO-ERROR. 
    IF NOT AVAILABLE l-bestand THEN 
    DO: 
      create l-bestand. 
      l-bestand.lager-nr = 0. 
      l-bestand.artnr = s-artnr. 
      l-bestand.anf-best-dat = billdate. 
    END. 
    l-bestand.anz-eingang = l-bestand.anz-eingang + anzahl. 
    l-bestand.wert-eingang = l-bestand.wert-eingang + wert. 
    l-bestand.anz-ausgang = l-bestand.anz-ausgang + anzahl. 
    l-bestand.wert-ausgang = l-bestand.wert-ausgang + wert. 
    FIND CURRENT l-bestand NO-LOCK. 
  END. 
 
  /*MTOPEN QUERY q1 FOR EACH l-order WHERE l-order.docu-nr = docu-nr 
    AND l-order.pos GT 0 AND l-order.loeschflag = 0, 
    FIRST l-art WHERE l-art.artnr = l-order.artnr 
    NO-LOCK BY flag-list[1 + INTEGER(l-order.geliefert EQ 0)] 
    BY l-order.pos descending.*/
END. 


PROCEDURE l-op-pos: 
DEFINE OUTPUT PARAMETER pos AS INTEGER INITIAL 0. 
DEFINE buffer l-op1 FOR l-op. 
/*  FOR EACH l-op1 WHERE l-op1.lscheinnr = lscheinnr 
    AND l-op1.loeschflag GE 0 AND l-op1.pos GT 0 NO-LOCK: 
    IF l-op1.pos GT pos THEN pos = l-op1.pos. 
  END. 
  pos = pos + 1. 
*/ 
  pos = 1. 
END. 


PROCEDURE create-purchase-book: 
DEFINE VARIABLE max-anz AS INTEGER. 
DEFINE VARIABLE curr-anz AS INTEGER. 
DEFINE VARIABLE created AS LOGICAL INITIAL NO. 
DEFINE VARIABLE i AS INTEGER. 
DEFINE buffer l-price1 FOR l-pprice. 
  FIND FIRST htparam WHERE paramnr = 225 no-lock.  /* max stored p-price */ 
  max-anz = htparam.finteger.               /* Rulita 211024 | Fixing for serverless */  
  IF max-anz = 0 THEN max-anz = 1. 
  curr-anz = l-art.lieferfrist. 
/*  
  IF curr-anz GT 0 THEN 
  DO: 
    FIND FIRST l-pprice WHERE l-pprice.artnr = l-op.artnr 
      AND l-pprice.bestelldatum = l-op.datum 
      AND l-pprice.einzelpreis = l-op.einzelpreis 
      AND l-pprice.lief-nr = l-op.lief-nr NO-LOCK NO-ERROR. 
    IF AVAILABLE l-pprice THEN RETURN. 
  END. 
*/
  IF curr-anz GE max-anz THEN 
  DO: 
    FIND FIRST l-price1 WHERE l-price1.artnr = l-op.artnr 
      AND l-price1.counter = 1 USE-INDEX counter_ix EXCLUSIVE-LOCK NO-ERROR. 
    IF AVAILABLE l-price1 THEN 
    DO: 
      l-price1.docu-nr = docu-nr. 
      l-price1.artnr = l-op.artnr. 
      l-price1.anzahl = l-op.anzahl. 
      l-price1.einzelpreis = l-op.einzelpreis. 
      l-price1.warenwert = l-op.warenwert. 
      l-price1.bestelldatum = l-op.datum. 
      l-price1.lief-nr = l-op.lief-nr. 
      l-price1.counter = 0. 
      created = YES. 
    END. 
    DO i = 2 TO curr-anz: 
      FIND FIRST l-pprice WHERE l-pprice.artnr = l-op.artnr 
        AND l-pprice.counter = i USE-INDEX counter_ix NO-LOCK NO-ERROR. 
      IF AVAILABLE l-pprice THEN 
      DO: 
        FIND CURRENT l-pprice EXCLUSIVE-LOCK. 
        l-pprice.counter = l-pprice.counter - 1. 
        FIND CURRENT l-pprice NO-LOCK. 
      END. 
    END. 
    IF created THEN 
    DO: 
      l-price1.counter = curr-anz. 
      FIND CURRENT l-price1 NO-LOCK. 
    END. 
  END. 
  IF NOT created THEN 
  DO: 
    create l-pprice. 
    l-pprice.docu-nr = docu-nr. 
    l-pprice.artnr = l-op.artnr. 
    l-pprice.anzahl = l-op.anzahl. 
    l-pprice.einzelpreis = l-op.einzelpreis. 
    l-pprice.warenwert = l-op.warenwert. 
    l-pprice.bestelldatum = l-op.datum. 
    l-pprice.lief-nr = l-op.lief-nr. 
    l-pprice.counter = curr-anz + 1. 
    l-pprice.betriebsnr = curr-disc. 
    FIND CURRENT l-pprice NO-LOCK. 
    FIND CURRENT l-art EXCLUSIVE-LOCK. 
    l-art.lieferfrist = curr-anz + 1. 
    FIND CURRENT l-art NO-LOCK. 
  END. 
END. 
