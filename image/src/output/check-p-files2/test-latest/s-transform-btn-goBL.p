DEFINE TEMP-TABLE op-list LIKE l-op
    FIELD bezeich LIKE l-artikel.bezeich
    FIELD username LIKE bediener.username.

DEF INPUT PARAMETER TABLE FOR op-list.
DEF INPUT PARAMETER rec-id AS INT.
DEF INPUT PARAMETER curr-lager AS INT.
DEF INPUT PARAMETER curr-pos AS INT.
DEF INPUT PARAMETER transdate AS DATE.
DEF INPUT PARAMETER wip-acct AS CHAR.
DEF INPUT PARAMETER to-stock AS INT.
DEF INPUT PARAMETER s-artnr1 AS INT.
DEF INPUT PARAMETER qty1 AS DECIMAL.
DEF INPUT PARAMETER bediener-nr AS INT.
DEF OUTPUT PARAMETER t-amount AS DECIMAL.
DEF OUTPUT PARAMETER amount AS DECIMAL.
DEF OUTPUT PARAMETER s-artnr AS INT.
DEF OUTPUT PARAMETER qty AS DECIMAL.
DEF OUTPUT PARAMETER price AS DECIMAL.
    
DEF VAR zeit AS INT.
FIND FIRST l-ophdr WHERE RECID(l-ophdr) = rec-id.
DO transaction: 
    FIND CURRENT l-ophdr EXCLUSIVE-LOCK. 
    l-ophdr.datum =  transdate. 
    l-ophdr.lager-nr = curr-lager. 
    FIND CURRENT l-ophdr NO-LOCK. 
END. 
RUN l-op-pos(OUTPUT curr-pos). 
curr-pos = curr-pos - 1. 
 
zeit = time. 
t-amount = 0. 
FOR EACH op-list WHERE op-list.anzahl NE 0: 
    zeit = zeit + 1. 
    curr-pos = curr-pos + 1. 
    s-artnr = op-list.artnr. 
    qty = op-list.anzahl. 
    price = op-list.warenwert / qty. 
    curr-lager = op-list.lager-nr. 
    RUN create-l-op (zeit). 
END. 

RUN create-transin. 

PROCEDURE l-op-pos: 
DEFINE OUTPUT PARAMETER pos AS INTEGER INITIAL 0. 
DEFINE buffer l-op1 FOR l-op. 
  FOR EACH l-op1 WHERE l-op1.lscheinnr = lscheinnr 
    AND l-op1.loeschflag GE 0 AND l-op1.pos GT 0 NO-LOCK: 
    IF l-op1.pos GT pos THEN pos = l-op1.pos. 
  END. 
  pos = pos + 1. 
END. 

PROCEDURE create-l-op: 
DEFINE INPUT PARAMETER zeit AS INTEGER. 
DEFINE VARIABLE anzahl AS DECIMAL FORMAT "->,>>>,>>9.999". 
DEFINE VARIABLE wert AS DECIMAL. 
 
DEFINE VARIABLE anz-oh AS DECIMAL. 
DEFINE VARIABLE val-oh AS DECIMAL. 
 
  FIND FIRST l-bestand WHERE l-bestand.lager-nr = 0 AND 
    l-bestand.artnr = s-artnr NO-LOCK. 
  anz-oh = l-bestand.anz-anf-best + l-bestand.anz-eingang 
    - l-bestand.anz-ausgang. 
  val-oh = l-bestand.val-anf-best + l-bestand.wert-eingang 
    - l-bestand.wert-ausgang. 
  IF anz-oh NE 0 THEN 
  DO: 
    price = val-oh / anz-oh. 
    wert = qty * price. 
  END. 
 
  anzahl = qty. 
  wert = qty * price. 
  amount = wert. 
  t-amount = t-amount + wert. 
 
/* UPDATE stock onhand  */ 
  DO: 
    FIND CURRENT l-bestand EXCLUSIVE-LOCK. 
    l-bestand.anz-ausgang = l-bestand.anz-ausgang + anzahl. 
    l-bestand.wert-ausgang = l-bestand.wert-ausgang + wert. 
    FIND CURRENT l-bestand NO-LOCK. 
    RELEASE l-bestand.
 
    FIND FIRST l-bestand WHERE l-bestand.lager-nr = curr-lager AND 
      l-bestand.artnr = s-artnr EXCLUSIVE-LOCK. 
    l-bestand.anz-ausgang = l-bestand.anz-ausgang + anzahl. 
    l-bestand.wert-ausgang = l-bestand.wert-ausgang + wert. 
    FIND CURRENT l-bestand NO-LOCK. 
    RELEASE l-bestand.
  END. 
 
/* Create l-op record */ 
  create l-op. 
  ASSIGN 
  l-op.datum = transdate 
  l-op.lager-nr = curr-lager 
  l-op.artnr = s-artnr 
  l-op.zeit = zeit 
  l-op.anzahl = anzahl 
  l-op.einzelpreis = price 
  l-op.warenwert = wert 
  l-op.op-art = 4 
  l-op.herkunftflag = 3    /* 4 = inventory !!! */ 
  l-op.lscheinnr = lscheinnr 
  l-op.stornogrund = wip-acct 
  l-op.pos = 1 
  l-op.fuellflag = bediener-nr.
  FIND CURRENT l-op NO-LOCK. 
 
/* UPDATE consumption */ 
  DO: 
   FIND FIRST l-verbrauch WHERE l-verbrauch.artnr = s-artnr 
     AND l-verbrauch.datum = transdate EXCLUSIVE-LOCK NO-ERROR. 
   IF NOT AVAILABLE l-verbrauch THEN 
   DO: 
     create l-verbrauch. 
     l-verbrauch.artnr = s-artnr. 
     l-verbrauch.datum = transdate. 
   END. 
   l-verbrauch.anz-verbrau = l-verbrauch.anz-verbrau + anzahl. 
   l-verbrauch.wert-verbrau = l-verbrauch.wert-verbrau + wert. 
   FIND CURRENT l-verbrauch NO-LOCK. 
  END. 
END. 

PROCEDURE create-transin: 
DEFINE VARIABLE tot-anz AS DECIMAL INITIAL 0. 
DEFINE VARIABLE tot-val AS DECIMAL. 
  create l-op. 
  ASSIGN 
    l-op.datum = transdate 
    l-op.lager-nr = to-stock 
    l-op.artnr = s-artnr1 
    l-op.zeit = time 
    l-op.anzahl = qty1 
    l-op.einzelpreis = (t-amount / qty1) 
    l-op.warenwert = t-amount 
    l-op.op-art = 2 
    l-op.herkunftflag = 3 
    l-op.lscheinnr = lscheinnr 
    l-op.pos = 1 
    l-op.stornogrund = wip-acct 
    l-op.fuellflag = bediener-nr.
  FIND CURRENT l-op NO-LOCK. 
 
  FIND FIRST l-bestand WHERE l-bestand.lager-nr = 0 AND 
    l-bestand.artnr = s-artnr1 EXCLUSIVE-LOCK NO-ERROR. 
  IF NOT AVAILABLE l-bestand THEN 
  DO: 
    create l-bestand. 
    l-bestand.artnr = s-artnr1. 
    l-bestand.anf-best-dat = transdate. 
  END. 
  l-bestand.anz-eingang = l-bestand.anz-eingang + qty1. 
  l-bestand.wert-eingang = l-bestand.wert-eingang + t-amount. 
  FIND CURRENT l-bestand NO-LOCK. 
 
  tot-anz = l-bestand.anz-anf-best + l-bestand.anz-eingang 
    - l-bestand.anz-ausgang. 
  tot-val = l-bestand.val-anf-best + l-bestand.wert-eingang 
    - l-bestand.wert-ausgang. 
 
  FIND FIRST l-bestand WHERE l-bestand.lager-nr = to-stock AND 
    l-bestand.artnr = s-artnr1 EXCLUSIVE-LOCK NO-ERROR. 
  IF NOT AVAILABLE l-bestand THEN 
  DO: 
    create l-bestand. 
    l-bestand.artnr = s-artnr1. 
    l-bestand.lager-nr = to-stock. 
    l-bestand.anf-best-dat = transdate. 
  END. 
  l-bestand.anz-eingang = l-bestand.anz-eingang + qty1. 
  l-bestand.wert-eingang = l-bestand.wert-eingang + t-amount. 
  FIND CURRENT l-bestand NO-LOCK. 
 
  IF tot-anz NE 0 THEN 
  DO: 
    FIND FIRST l-artikel WHERE l-artikel.artnr = s-artnr1 EXCLUSIVE-LOCK. 
    l-artikel.vk-preis = tot-val / tot-anz. 
    FIND CURRENT l-artikel NO-LOCK.
  END. 
END. 
