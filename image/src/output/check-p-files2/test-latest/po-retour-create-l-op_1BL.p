
DEF INPUT PARAMETER l-order-rec-id  AS INT.
DEF INPUT PARAMETER s-artnr         AS INT.
DEF INPUT PARAMETER docu-nr         AS CHAR.
DEF INPUT PARAMETER exchg-rate      AS DECIMAL.
DEF INPUT PARAMETER price-decimal   AS INT.
DEF INPUT PARAMETER lief-nr         AS INTEGER. 
DEF INPUT PARAMETER curr-lager      AS INT.
DEF INPUT PARAMETER lscheinnr       AS CHAR.
DEF INPUT PARAMETER f-endkum        AS INTEGER. 
DEF INPUT PARAMETER b-endkum        AS INTEGER. 
DEF INPUT PARAMETER m-endkum        AS INTEGER. 
DEF INPUT PARAMETER billdate        AS DATE.
DEF INPUT PARAMETER fb-closedate    AS DATE.
DEF INPUT PARAMETER m-closedate     AS DATE.
DEF INPUT PARAMETER reason LIKE l-order.stornogrund.
DEF INPUT PARAMETER user-init       AS CHAR.
DEF INPUT PARAMETER qty             AS DECIMAL.
DEF INPUT PARAMETER price           AS DECIMAL.
DEF INPUT PARAMETER amount          AS DECIMAL.
DEF INPUT PARAMETER s-qty           AS INTEGER FORMAT ">,>>9".
DEF INPUT-OUTPUT PARAMETER t-amount AS DECIMAL.
DEF OUTPUT PARAMETER epreis AS DECIMAL. 
DEF OUTPUT PARAMETER direct-issue AS LOGICAL.


DEF VAR ss-artnr    AS INTEGER EXTENT 3 NO-UNDO.
DEF VAR ss-in       AS INTEGER EXTENT 3 NO-UNDO.
DEF VAR ss-out      AS INTEGER EXTENT 3 NO-UNDO.
DEF VAR ss-content  AS INTEGER EXTENT 3 NO-UNDO.

FIND FIRST l-orderhdr WHERE l-orderhdr.docu-nr = docu-nr.
FIND FIRST bediener WHERE bediener.userinit = user-init.
FIND FIRST queasy WHERE queasy.KEY = 20 AND queasy.number1 = s-artnr 
    NO-LOCK NO-ERROR. 
IF AVAILABLE queasy THEN 
DO: 
  ss-artnr[1] = queasy.deci1. 
  ss-artnr[2] = queasy.deci2. 
  ss-artnr[3] = queasy.deci3. 
  ss-content[1] = INTEGER(SUBSTR(queasy.char3,1,3)). 
  ss-content[2] = INTEGER(SUBSTR(queasy.char3,5,3)). 
  ss-content[3] = INTEGER(SUBSTR(queasy.char3,9,3)). 

  IF ss-content[1] NE 0 THEN ss-in[1] = ROUND (qty / ss-content[1] - 0.6, 0) + 1. 
  IF ss-content[2] NE 0 THEN ss-in[2] = ROUND (qty / ss-content[2] - 0.6, 0) + 1. 
  IF ss-content[3] NE 0 THEN ss-in[3] = ROUND (qty / ss-content[3] - 0.6, 0) + 1. 
  ss-out[1] = ss-in[1]. 
  ss-out[2] = ss-in[2]. 
  ss-out[3] = ss-in[3].
END. 

FIND FIRST l-order WHERE RECID(l-order) = l-order-rec-id.
RUN create-l-op.
RUN reorg-inv.

PROCEDURE create-l-op:
DEFINE VARIABLE anzahl AS DECIMAL. 
DEFINE VARIABLE wert AS DECIMAL. 
DEFINE VARIABLE tot-wert AS DECIMAL. 
DEFINE VARIABLE tot-anz AS DECIMAL. 
DEFINE BUFFER l-order1 FOR l-order. 
DEFINE VARIABLE curr-pos AS INTEGER. 
DEFINE BUFFER l-oph FOR l-ophdr. 
DEFINE BUFFER l-art FOR l-artikel.

 
  FIND CURRENT l-order EXCLUSIVE-LOCK. 
 
  DO WHILE s-qty GE l-order.txtnr: 
    s-qty = s-qty - l-order.txtnr. 
    qty = qty + 1. 
  END. 
  qty = - qty. 
  s-qty = - s-qty. 
 
  IF s-qty GE l-order.txtnr THEN s-qty = l-order.txtnr.
  anzahl = qty * l-order.txtnr + s-qty. 
 
  IF l-order.flag THEN 
  DO: 
    epreis = price / l-order.txtnr. 
    wert = qty * price + s-qty * epreis. 
  END. 
  ELSE 
  DO: 
    epreis = price. 
    wert = anzahl * epreis. 
  END. 
  wert = wert * exchg-rate. 
  wert = round(wert, price-decimal). 
 
  /*l-order.geliefert = l-order.geliefert + qty. */
  l-order.geliefert = l-order.geliefert + anzahl.
  
  /*IF s-qty NE 0 THEN 
  DO: 
    l-order.angebot-lief[1] = l-order.angebot-lief[1] 
      + l-order.txtnr + s-qty. 
    l-order.geliefert = l-order.geliefert - 1. 
  END. 

  DO WHILE l-order.angebot-lief[1] GE l-order.txtnr: 
    l-order.angebot-lief[1] = l-order.angebot-lief[1] - l-order.txtnr. 
    l-order.geliefert = l-order.geliefert + 1. 
  END. */

  l-order.rechnungswert = l-order.rechnungswert + wert. 
  l-order.lief-fax[2] = bediener.username. 
 
 
  amount = wert. 
  t-amount = t-amount + wert. 
  release l-order. 
 
  FIND FIRST l-order1 WHERE l-order1.docu-nr = l-orderhdr.docu-nr 
    AND l-order1.pos = 0 EXCLUSIVE-LOCK. 
  l-order1.rechnungspreis = l-order1.rechnungspreis + wert. 
  l-order1.rechnungswert = l-order1.rechnungswert + wert. 
  FIND CURRENT l-order1 NO-LOCK. 
 
/** check IF it was a direct issue **/ 
  direct-issue = NO. 
  FIND FIRST l-art WHERE l-art.artnr = s-artnr NO-LOCK NO-ERROR.
  FIND FIRST l-op WHERE l-op.artnr = l-art.artnr 
    AND l-op.op-art = 3 AND l-op.lief-nr = lief-nr 
    AND l-op.herkunftflag = 2 AND l-op.lager-nr = curr-lager 
    AND l-op.flag NO-LOCK NO-ERROR. 
  IF AVAILABLE l-op THEN 
  DO: 
    direct-issue = YES. 
    FIND CURRENT l-op EXCLUSIVE-LOCK. 
    l-op.anzahl = l-op.anzahl + anzahl. 
    l-op.warenwert = l-op.warenwert + wert. 
 
    /*FIND FIRST l-oph WHERE l-oph.lscheinnr = lscheinnr 
      AND l-oph.op-typ = "STT" NO-LOCK NO-ERROR. 
    IF AVAILABLE l-oph AND l-oph.betriebsnr NE 0 THEN 
    RUN create-lartjob.p(RECID(l-oph), l-op.artnr, anzahl, wert, 
      l-op.datum, NO). */
  END. 

  IF NOT direct-issue THEN 
  DO: 
    IF ((l-art.endkum = f-endkum OR l-art.endkum = b-endkum) 
      AND billdate LE fb-closedate) 
      OR (l-art.endkum GE m-endkum AND billdate LE m-closedate) THEN 
    DO: 
/* UPDATE stock onhand  */         
      FIND FIRST l-bestand WHERE l-bestand.lager-nr = 0 AND 
      l-bestand.artnr = l-art.artnr EXCLUSIVE-LOCK NO-ERROR. 
      l-bestand.anz-eingang = l-bestand.anz-eingang + anzahl. 
      l-bestand.wert-eingang = l-bestand.wert-eingang + wert. 
      tot-anz = l-bestand.anz-anf-best + l-bestand.anz-eingang 
          - l-bestand.anz-ausgang. 
      tot-wert = l-bestand.val-anf-best + l-bestand.wert-eingang 
          - l-bestand.wert-ausgang. 
      
      FIND CURRENT l-bestand NO-LOCK. 
 
      FIND FIRST l-bestand WHERE l-bestand.lager-nr = curr-lager AND 
        l-bestand.artnr = l-art.artnr EXCLUSIVE-LOCK NO-ERROR. 
      IF NOT AVAILABLE l-bestand THEN 
      DO: 
        create l-bestand. 
        l-bestand.anf-best-dat = billdate. 
        l-bestand.artnr = l-art.artnr. 
        l-bestand.lager-nr = curr-lager. 
      END. 
 
      l-bestand.anz-eingang = l-bestand.anz-eingang + anzahl. 
      l-bestand.wert-eingang = l-bestand.wert-eingang + wert. 
      FIND CURRENT l-bestand NO-LOCK. 
 
/* UPDATE average price */ 
      IF tot-anz NE 0 THEN 
      DO: 
        FIND CURRENT l-art EXCLUSIVE-LOCK. 
        l-art.vk-preis = tot-wert / tot-anz. 
        FIND CURRENT l-art NO-LOCK. 
      END. 
    END. 
  END. 
  ELSE IF direct-issue THEN 
  DO: 
/* UPDATE stock onhand  */ 
    FIND FIRST l-bestand WHERE l-bestand.lager-nr = 0 AND 
      l-bestand.artnr = l-art.artnr EXCLUSIVE-LOCK NO-ERROR. 
    IF AVAILABLE l-bestand THEN 
    DO: 
      l-bestand.anz-eingang = l-bestand.anz-eingang + anzahl. 
      l-bestand.wert-eingang = l-bestand.wert-eingang + wert. 
      l-bestand.anz-ausgang = l-bestand.anz-ausgang + anzahl. 
      l-bestand.wert-ausgang = l-bestand.wert-ausgang + wert. 
      FIND CURRENT l-bestand NO-LOCK. 
    END. 
    FIND FIRST l-bestand WHERE l-bestand.lager-nr = curr-lager AND 
      l-bestand.artnr = l-art.artnr EXCLUSIVE-LOCK NO-ERROR. 
    IF AVAILABLE l-bestand THEN 
    DO: 
      l-bestand.anz-eingang = l-bestand.anz-eingang + anzahl. 
      l-bestand.wert-eingang = l-bestand.wert-eingang + wert. 
      l-bestand.anz-ausgang = l-bestand.anz-ausgang + anzahl. 
      l-bestand.wert-ausgang = l-bestand.wert-ausgang + wert.       
      FIND CURRENT l-bestand NO-LOCK. 
    END. 
  END. 
 
/* UPDATE supplier turnover */ 
  FIND FIRST  l-liefumsatz WHERE l-liefumsatz.lief-nr = lief-nr 
    AND l-liefumsatz.datum = billdate 
    EXCLUSIVE-LOCK NO-ERROR. 
  IF NOT AVAILABLE l-liefumsatz THEN 
  DO: 
    create l-liefumsatz. 
    l-liefumsatz.datum = billdate. 
    l-liefumsatz.lief-nr = lief-nr. 
  END. 
  l-liefumsatz.gesamtumsatz = l-liefumsatz.gesamtumsatz + wert. 
 
/* Create l-op record */ 
  create l-op. 
  l-op.datum = billdate. 
  l-op.lager-nr = curr-lager. 
  l-op.artnr = l-art.artnr. 
  l-op.lief-nr = lief-nr. 
  l-op.zeit = time. 
  l-op.anzahl = anzahl. 
  l-op.einzelpreis = epreis. 
  l-op.warenwert = wert. 
  l-op.op-art = 1. 
  l-op.herkunftflag = 1.    /* 4 = inventory !!! */ 
  l-op.docu-nr = docu-nr. 
  l-op.lscheinnr = lscheinnr. 
  RUN l-op-pos(OUTPUT curr-pos). 
  l-op.pos = curr-pos. 
  l-op.fuellflag = bediener.nr. 
  l-op.stornogrund = reason. 
  FIND CURRENT l-op NO-LOCK. 
 
  RUN create-container. 
 
/* create l-ophdr  */ 
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
 
  /*MT
  IF show-price THEN 
  DO:
    IF delflag = 0 THEN
    OPEN QUERY q1 FOR EACH t-l-order WHERE t-l-order.loeschflag = delflag,
      FIRST l-art WHERE l-art.artnr = t-l-order.artnr 
      NO-LOCK BY flag-list[1 + INTEGER(t-l-order.geliefert EQ 0)] 
      BY t-l-order.pos descending. 
    ELSE
    OPEN QUERY q1 FOR EACH t-l-order WHERE t-l-order.loeschflag GE delflag,
      FIRST l-art WHERE l-art.artnr = t-l-order.artnr 
      NO-LOCK BY flag-list[1 + INTEGER(t-l-order.geliefert EQ 0)] 
      BY t-l-order.pos descending. 
  END.
  ELSE 
  DO:
    IF delflag = 0 THEN
    OPEN QUERY q2 FOR EACH t-l-order WHERE t-l-order.loeschflag = delflag,
      FIRST l-art WHERE l-art.artnr = t-l-order.artnr 
      NO-LOCK BY flag-list[1 + INTEGER(t-l-order.geliefert EQ 0)] 
      BY t-l-order.pos descending. 
    ELSE
    OPEN QUERY q2 FOR EACH t-l-order WHERE t-l-order.loeschflag GE delflag,
      FIRST l-art WHERE l-art.artnr = t-l-order.artnr 
      NO-LOCK BY flag-list[1 + INTEGER(t-l-order.geliefert EQ 0)] 
      BY t-l-order.pos descending. 
  END.
  */
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


PROCEDURE create-container: 
DEF VAR i AS INTEGER. 
DEF VAR curr-pos AS INTEGER. 
DEF VAR do-it AS LOGICAL. 
DEF VAR tot-anz AS DECIMAL. 
DEF VAR tot-wert AS DECIMAL. 
DEF VAR anzahl AS DECIMAL. 
DEF VAR wert AS DECIMAL. 
DEF BUFFER l-art FOR l-artikel. 
 
  FIND FIRST queasy WHERE queasy.KEY = 20 AND queasy.number1 = l-op.artnr 
      NO-LOCK NO-ERROR. 
  IF NOT AVAILABLE queasy THEN RETURN. 
 
  DO i = 1 TO 3: 
      do-it = NO. 
      IF ss-artnr[i] NE 0 THEN 
      DO: 
        FIND FIRST l-art WHERE l-art.artnr = ss-artnr[i] NO-LOCK NO-ERROR. 
        do-it = AVAILABLE l-art AND (ss-in[i] - ss-out[i]) NE 0. 
      END. 
      IF do-it THEN 
      DO: 
        anzahl = - (ss-in[i] - ss-out[i]). 
        wert = l-art.ek-aktuell * anzahl. 
        t-amount = t-amount + wert. 
 
        IF ((l-art.endkum = f-endkum OR l-art.endkum = b-endkum) 
          AND billdate LE fb-closedate) 
        OR (l-art.endkum GE m-endkum AND billdate LE m-closedate) THEN 
        DO: 
    /* UPDATE stock onhand  */ 
          FIND FIRST l-bestand WHERE l-bestand.lager-nr = 0 AND 
            l-bestand.artnr = l-art.artnr EXCLUSIVE-LOCK NO-ERROR. 
          IF NOT AVAILABLE l-bestand THEN 
          DO: 
            create l-bestand. 
            l-bestand.anf-best-dat = billdate. 
            l-bestand.artnr = l-art.artnr. 
          END. 
          l-bestand.anz-eingang = l-bestand.anz-eingang + anzahl. 
          l-bestand.wert-eingang = l-bestand.wert-eingang + wert. 
          tot-anz = l-bestand.anz-anf-best + l-bestand.anz-eingang 
              - l-bestand.anz-ausgang. 
          tot-wert = l-bestand.val-anf-best + l-bestand.wert-eingang 
              - l-bestand.wert-ausgang. 
          FIND CURRENT l-bestand NO-LOCK. 
 
          FIND FIRST l-bestand WHERE l-bestand.lager-nr = curr-lager AND 
            l-bestand.artnr = l-art.artnr EXCLUSIVE-LOCK NO-ERROR. 
          IF NOT AVAILABLE l-bestand THEN 
          DO: 
            create l-bestand. 
            l-bestand.anf-best-dat = billdate. 
            l-bestand.artnr = l-art.artnr. 
            l-bestand.lager-nr = curr-lager. 
          END. 
          l-bestand.anz-eingang = l-bestand.anz-eingang + anzahl. 
          l-bestand.wert-eingang = l-bestand.wert-eingang + wert. 
          FIND CURRENT l-bestand NO-LOCK. 
 
    /* UPDATE average price */ 
          FIND CURRENT l-art EXCLUSIVE-LOCK. 
          IF tot-anz NE 0 THEN l-art.vk-preis = tot-wert / tot-anz. 
          FIND CURRENT l-art NO-LOCK. 
        END. 
 
    /* Create l-op record */ 
        create l-op. 
        l-op.datum = billdate. 
        l-op.lager-nr = curr-lager. 
        l-op.artnr = l-art.artnr. 
        l-op.lief-nr = lief-nr. 
        l-op.zeit = time. 
        l-op.anzahl = anzahl. 
        l-op.einzelpreis = l-art.ek-aktuell. 
        l-op.warenwert = wert. 
        l-op.deci1[1] = l-art.ek-aktuell. 
        l-op.op-art = 1. 
        l-op.herkunftflag = 1.    /* 4 = inventory !!! */ 
        l-op.docu-nr = docu-nr. 
        l-op.lscheinnr = lscheinnr. 
        RUN l-op-pos(OUTPUT curr-pos). 
        l-op.pos = curr-pos. 
        l-op.fuellflag = bediener.nr. 
        FIND CURRENT l-op NO-LOCK. 
      END. 
  END. 
END. 

PROCEDURE reorg-inv:
    DEFINE VARIABLE inv-type AS INTEGER NO-UNDO.

    DO inv-type = 1 TO 3:
        RUN reorg-monhand-init-onhandbl.p(inv-type).
        RUN reorg-monhand-update-eingang_1bl.p(inv-type, user-init).
        RUN reorg-monhand-update-ausgangbl.p(inv-type).
        RUN reorg-monhand-update-averagebl.p(inv-type).
    END.

END.
