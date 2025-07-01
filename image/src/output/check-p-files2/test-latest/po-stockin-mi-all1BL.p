DEF TEMP-TABLE t-l-order LIKE l-order
    FIELD rec-id        AS INT
    FIELD art-bezeich   AS CHAR
    FIELD jahrgang      LIKE l-artikel.jahrgang
    FIELD alkoholgrad   LIKE l-artikel.alkoholgrad
    .

DEFINE TEMP-TABLE s-list 
  FIELD artnr       AS INTEGER 
  FIELD qty         AS DECIMAL 
  FIELD s-qty       AS DECIMAL 
  FIELD wert        AS DECIMAL 
  FIELD op-recid    AS INTEGER 
  FIELD ss-artnr    AS INTEGER EXTENT 3 INITIAL 0 
  FIELD ss-in       AS INTEGER EXTENT 3 INITIAL 0 
  FIELD ss-out      AS INTEGER EXTENT 3 INITIAL 0. 

DEF INPUT PARAMETER user-init           AS CHAR.
DEF INPUT PARAMETER l-order-recid       AS INT.
DEF INPUT PARAMETER l-orderhdr-recid    AS INT.
DEF INPUT PARAMETER docu-nr             AS CHAR.
DEF INPUT PARAMETER exchg-rate          AS DECIMAL.
DEF INPUT PARAMETER price-decimal       AS INT.
DEF INPUT PARAMETER billdate            AS DATE.
DEF INPUT PARAMETER f-endkum            AS INT.
DEF INPUT PARAMETER b-endkum            AS INT.
DEF INPUT PARAMETER m-endkum            AS INT.
DEF INPUT PARAMETER fb-closedate        AS DATE.
DEF INPUT PARAMETER m-closedate         AS DATE.
DEF INPUT PARAMETER curr-lager          AS INT.
DEF INPUT PARAMETER lief-nr             AS INT.
DEF INPUT PARAMETER lscheinnr           LIKE l-op.lscheinnr.

DEF INPUT-OUTPUT PARAMETER t-amount AS DECIMAL.

DEF OUTPUT PARAMETER created AS LOGICAL.
DEF OUTPUT PARAMETER TABLE FOR s-list.
DEF OUTPUT PARAMETER TABLE FOR t-l-order.

DEFINE buffer l-od FOR l-order.
DEF VAR s-artnr AS INT.
DEF VAR qty AS DECIMAL.
DEF VAR s-qty AS INT.
DEF VAR price AS DECIMAL.
DEF VAR curr-disc AS INT.
DEF VAR curr-vat AS INT.
DEF VAR curr-disc2 AS INT.
DEF VAR curr-vat1 AS INT.
DEF VAR epreis AS DECIMAL.
DEF VAR amount AS DECIMAL.

FIND FIRST bediener WHERE bediener.userinit = user-init.
FIND FIRST l-order WHERE RECID(l-order) = l-order-recid.
FIND FIRST l-orderhdr WHERE RECID(l-orderhdr) = l-orderhdr-recid.

FOR EACH l-od WHERE l-od.docu-nr = docu-nr 
    AND l-od.pos GT 0 AND l-od.loeschflag = 0 NO-LOCK: 
    FIND FIRST l-art WHERE l-art.artnr = l-od.artnr NO-LOCK. 
    FIND FIRST l-order WHERE RECID(l-order) = RECID(l-od) NO-LOCK. 
    s-artnr = l-od.artnr. 
    IF l-od.angebot-lief[1] EQ 0 THEN 
    DO: 
      qty = l-od.anzahl - l-od.geliefert. 
      s-qty = 0. 
    END. 
    ELSE DO: 
      qty = l-od.anzahl - l-od.geliefert - 1. 
      s-qty = l-od.txtnr - l-od.angebot-lief[1]. 
    END. 
    IF qty NE 0 OR s-qty NE 0 THEN 
    DO: 
      price = l-od.einzelpreis. 
      curr-disc = INTEGER(SUBSTR(l-od.quality,1,2)) * 100 
        + INTEGER(SUBSTR(l-od.quality,4,2)). 
      curr-vat = INTEGER(SUBSTR(l-od.quality,7,2)) * 100 
        + INTEGER(SUBSTR(l-od.quality,10,2)). 
      curr-disc2 = 0. 
      IF length(l-od.quality) GE 17 THEN 
      curr-disc2 = INTEGER(SUBSTR(l-od.quality,13,2)) * 100 
        + INTEGER(SUBSTR(l-od.quality,16,2)). 
      curr-vat1 = l-art.alkoholgrad * 100. 
      IF l-od.flag THEN epreis = price / l-od.txt. 
      ELSE epreis = price. 
      amount = qty * price + s-qty * epreis. 
      amount = amount * exchg-rate. 
      amount = round(amount, price-decimal). 
      RUN create-l-op (INPUT amount, NO). 
      created = YES. 
    END. 
END. 

FOR EACH l-order WHERE l-order.docu-nr = docu-nr 
    AND l-order.pos GT 0 AND l-order.loeschflag = 0:
    CREATE t-l-order.
    BUFFER-COPY l-order TO t-l-order.
    ASSIGN t-l-order.rec-id = RECID(l-order).

    FIND FIRST l-artikel WHERE l-artikel.artnr = l-order.artnr NO-LOCK.
    ASSIGN 
        t-l-order.art-bezeich   = l-artikel.bezeich
        t-l-order.jahrgang      = l-artikel.jahrgang
        t-l-order.alkoholgrad   = l-artikel.alkoholgrad
        .
END.


PROCEDURE create-l-op: 
DEFINE INPUT PARAMETER wert AS DECIMAL. 
DEFINE INPUT PARAMETER disp-flag AS LOGICAL. 
DEFINE VARIABLE anzahl AS DECIMAL FORMAT ">>>,>>9.999". 
DEFINE VARIABLE tot-wert AS DECIMAL. 
DEFINE VARIABLE tot-anz AS DECIMAL. 
DEFINE buffer l-order1 FOR l-order. 
DEFINE VARIABLE curr-pos AS INTEGER. 
DEFINE VARIABLE orig-preis AS DECIMAL. 
 
  DO TRANSACTION:
    anzahl = qty * l-order.txtnr + s-qty. 
    IF l-order.flag THEN epreis = price / l-order.txt. 
    ELSE epreis = price. 
 
    FIND CURRENT l-order EXCLUSIVE-LOCK. 
    ASSIGN
      l-order.geliefert = l-order.geliefert + qty
      l-order.angebot-lief[1] = l-order.angebot-lief[1] + s-qty
      l-order.lief-fax[2] = bediener.username
    . 
   MESSAGE "in"
       VIEW-AS ALERT-BOX INFO.
    DO WHILE l-order.angebot-lief[1] GE l-order.txtnr: 
      ASSIGN
        l-order.angebot-lief[1] = l-order.angebot-lief[1] - l-order.txtnr
        l-order.geliefert = l-order.geliefert + 1
      . 
    END. 

    MESSAGE "in1"
       VIEW-AS ALERT-BOX INFO.
 
    ASSIGN
      l-order.rechnungspreis  = price
      l-order.rechnungswert   = l-order.rechnungswert + wert 
      l-order.lieferdatum-eff = billdate
      l-order.lief-fax[2]     = bediener.username
      amount                  = wert. 
      t-amount                = t-amount + wert
    . 
    FIND CURRENT l-order NO-LOCK. 
 
    FIND FIRST l-order1 WHERE l-order1.docu-nr = l-orderhdr.docu-nr 
      AND l-order1.pos = 0 EXCLUSIVE-LOCK. 
    
    ASSIGN
      l-order1.rechnungspreis = l-order1.rechnungspreis + wert
      l-order1.rechnungswert = l-order1.rechnungswert + wert
    . 
    
    FIND CURRENT l-order1 NO-LOCK. 
 
    IF l-art.ek-aktuell NE epreis THEN 
    DO: 
      FIND CURRENT l-art EXCLUSIVE-LOCK. 
      ASSIGN
        l-art.ek-letzter = l-art.ek-aktuell
        l-art.ek-aktuell = epreis
      . 
      FIND CURRENT l-art NO-LOCK. 
    END. 
 
    IF ((l-art.endkum = f-endkum OR l-art.endkum = b-endkum) 
      AND billdate LE fb-closedate) 
    OR (l-art.endkum GE m-endkum AND billdate LE m-closedate) THEN 
    DO: 
/* UPDATE stock onhand  */ 
      FIND FIRST l-bestand WHERE l-bestand.lager-nr = 0 AND 
        l-bestand.artnr = l-art.artnr EXCLUSIVE-LOCK NO-ERROR. 
      IF NOT AVAILABLE l-bestand THEN 
      DO: 
        CREATE l-bestand. 
        ASSIGN
          l-bestand.anf-best-dat = billdate
          l-bestand.artnr = l-art.artnr
        . 
      END. 
      ASSIGN
        l-bestand.anz-eingang  = l-bestand.anz-eingang + anzahl
        l-bestand.wert-eingang = l-bestand.wert-eingang + wert 
        tot-anz  = l-bestand.anz-anf-best + l-bestand.anz-eingang 
                - l-bestand.anz-ausgang 
        tot-wert = l-bestand.val-anf-best + l-bestand.wert-eingang 
                - l-bestand.wert-ausgang. 
      FIND CURRENT l-bestand NO-LOCK. 
 
      FIND FIRST l-bestand WHERE l-bestand.lager-nr = curr-lager AND 
        l-bestand.artnr = l-art.artnr EXCLUSIVE-LOCK NO-ERROR. 
       IF NOT AVAILABLE l-bestand THEN 
      DO: 
        CREATE l-bestand. 
        ASSIGN
          l-bestand.anf-best-dat = billdate
          l-bestand.artnr = l-art.artnr
          l-bestand.lager-nr = curr-lager
        . 
      END.
      ASSIGN
        l-bestand.anz-eingang = l-bestand.anz-eingang + anzahl
        l-bestand.wert-eingang = l-bestand.wert-eingang + wert
      . 
      FIND CURRENT l-bestand NO-LOCK. 
 
/* UPDATE average price */ 
      FIND CURRENT l-art EXCLUSIVE-LOCK. 
      IF tot-anz NE 0 THEN l-art.vk-preis = tot-wert / tot-anz. 
      FIND CURRENT l-art NO-LOCK. 
    END. 
 
/* UPDATE supplier turnover */ 
    FIND FIRST  l-liefumsatz WHERE l-liefumsatz.lief-nr = lief-nr 
      AND l-liefumsatz.datum = billdate EXCLUSIVE-LOCK NO-ERROR. 
    IF NOT AVAILABLE l-liefumsatz THEN 
    DO: 
      CREATE l-liefumsatz. 
      ASSIGN
        l-liefumsatz.datum = billdate
        l-liefumsatz.lief-nr = lief-nr
      . 
    END. 
    ASSIGN
      l-liefumsatz.gesamtumsatz = l-liefumsatz.gesamtumsatz + wert
      orig-preis = epreis / (1 - curr-disc / 10000) / (1 - curr-disc2 / 10000) 
        / (1 + curr-vat / 10000)
    . 
    FIND CURRENT l-liefumsatz NO-LOCK.

/* Create l-op record */ 
    CREATE l-op. 
    ASSIGN
      l-op.datum          = billdate
      l-op.lager-nr       = curr-lager 
      l-op.artnr          = l-art.artnr 
      l-op.lief-nr        = lief-nr
      l-op.zeit           = TIME
      l-op.anzahl         = anzahl 
      l-op.einzelpreis    = epreis 
      l-op.warenwert      = wert
      l-op.deci1[1]       = orig-preis 
      l-op.deci1[2]       = curr-disc / 100 
      l-op.rueckgabegrund = curr-disc2
    . 

    IF curr-vat NE 0 THEN 
    ASSIGN 
      l-op.deci1[3] = curr-vat / 100
      l-op.deci1[4] = epreis * l-op.deci1[3] / 100
    . 
    ELSE 
    ASSIGN 
      l-op.deci1[3] = curr-vat1 / 100
      l-op.deci1[4] = epreis * l-op.deci1[3] / 100
    . 
    ASSIGN  
      l-op.op-art       = 1
      l-op.herkunftflag = 1    /* 4 = inventory !!! */ 
      l-op.docu-nr      = docu-nr 
      l-op.lscheinnr    = lscheinnr
    . 
  
    RUN l-op-pos(OUTPUT curr-pos). 
    ASSIGN
      l-op.pos = curr-pos
      l-op.fuellflag = bediener.nr
    . 
    FIND CURRENT l-op NO-LOCK. 
 
    CREATE s-list. 
    ASSIGN
      s-list.op-recid = RECID(l-op)
      s-list.artnr    = l-op.artnr 
      s-list.qty      = qty
      s-list.s-qty    = s-qty 
      s-list.wert     = wert
    . 
 
    FIND FIRST queasy WHERE queasy.KEY = 20 AND queasy.number1 = l-op.artnr 
      NO-LOCK NO-ERROR. 
 
    IF AVAILABLE queasy THEN 
    ASSIGN 
      s-list.ss-artnr[1] = ss-artnr[1]
      s-list.ss-artnr[2] = ss-artnr[2] 
      s-list.ss-artnr[3] = ss-artnr[3] 
      s-list.ss-in[1]    = ss-in[1]
      s-list.ss-in[2]    = ss-in[2] 
      s-list.ss-in[3]    = ss-in[3] 
      s-list.ss-out[1]   = ss-out[1]
      s-list.ss-out[2]   = ss-out[2] 
      s-list.ss-out[3]   = ss-out[3]
    . 
 
    /*MTENABLE btn-del WITH FRAME frame1.*/
    RUN create-purchase-book. 
 
/* create l-ophdr  */ 
    FIND FIRST l-ophdr WHERE l-ophdr.lscheinnr = lscheinnr 
      AND l-ophdr.op-typ = "STI" AND l-ophdr.lager-nr = curr-lager 
      AND l-ophdr.datum = billdate NO-LOCK NO-ERROR. 
    IF NOT AVAILABLE l-ophdr THEN 
    DO: 
      CREATE l-ophdr. 
      ASSIGN
        l-ophdr.datum = billdate
        l-ophdr.lager-nr = curr-lager 
        l-ophdr.docu-nr = docu-nr
        l-ophdr.lscheinnr = lscheinnr 
        l-ophdr.op-typ = "STI"
      . 
      FIND CURRENT l-ophdr NO-LOCK. 
    END.

  END.  /* DO TRANSACTION */

  /*MT
  IF disp-flag AND show-price THEN 
    OPEN QUERY q1 FOR EACH l-order WHERE l-order.docu-nr = docu-nr 
      AND l-order.pos GT 0 AND l-order.loeschflag = 0, 
      FIRST l-art WHERE l-art.artnr = l-order.artnr 
      NO-LOCK BY flag-list[1 + INTEGER(l-order.geliefert EQ 0)] 
      BY l-order.pos DESCENDING. 
  ELSE IF disp-flag AND NOT show-price THEN 
    OPEN QUERY q11 FOR EACH l-order WHERE l-order.docu-nr = docu-nr 
      AND l-order.pos GT 0 AND l-order.loeschflag = 0, 
      FIRST l-art WHERE l-art.artnr = l-order.artnr 
      NO-LOCK BY flag-list[1 + INTEGER(l-order.geliefert EQ 0)] 
      BY l-order.pos DESCENDING. 
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

