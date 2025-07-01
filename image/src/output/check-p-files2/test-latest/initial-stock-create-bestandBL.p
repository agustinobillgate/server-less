DEFINE TEMP-TABLE best-list LIKE l-bestand
    FIELD rec-id AS INT.
DEFINE TEMP-TABLE t-best-list LIKE best-list. 

DEF INPUT PARAMETER s-artnr AS INT.
DEF INPUT PARAMETER m-endkum AS INT.
DEF INPUT PARAMETER m-date AS DATE.
DEF INPUT PARAMETER fb-date AS DATE.
DEF INPUT PARAMETER qty AS DECIMAL.
DEF INPUT PARAMETER amount AS DECIMAL.
DEF INPUT PARAMETER old-amount AS DECIMAL.
DEF INPUT PARAMETER curr-lager AS INT.

DEF INPUT-OUTPUT PARAMETER t-amount AS DECIMAL.
DEF OUTPUT PARAMETER TABLE FOR best-list.

DEFINE VARIABLE avrg-price AS DECIMAL. 

RUN create-bestand.

PROCEDURE create-bestand: 
DEFINE VARIABLE anzahl      AS DECIMAL. 
DEFINE VARIABLE wert        AS DECIMAL. 
DEFINE VARIABLE curr-pos    AS INTEGER. 
DEFINE VARIABLE init-date   AS DATE. 
DEFINE BUFFER l-art1        FOR l-artikel. 
DEFINE VARIABLE tot-anz     AS DECIMAL. 
 
  FIND FIRST l-art1 WHERE l-art1.artnr = s-artnr NO-LOCK. 
  IF l-art1.endkum GE m-endkum THEN init-date = m-date. 
  ELSE init-date = fb-date. 
 
  anzahl = qty. 
  wert   = amount. 
  t-amount = t-amount + wert - old-amount. 
 
/* UPDATE stock onhand  */ 
  FIND FIRST l-bestand WHERE l-bestand.lager-nr = 0 AND 
      l-bestand.artnr = s-artnr EXCLUSIVE-LOCK NO-ERROR. 
  IF NOT AVAILABLE l-bestand THEN 
  DO: 
    create l-bestand. 
    l-bestand.artnr = s-artnr. 
    l-bestand.anf-best-dat = init-date. 
  END. 
  l-bestand.anz-anf-best = l-bestand.anz-anf-best + anzahl. 
  l-bestand.val-anf-best = l-bestand.val-anf-best + wert. 
  FIND CURRENT l-bestand NO-LOCK. 
 
  tot-anz =  (l-bestand.anz-anf-best + l-bestand.anz-eingang 
   - l-bestand.anz-ausgang). 
  IF tot-anz NE 0 THEN 
  DO: 
    avrg-price = (l-bestand.val-anf-best + l-bestand.wert-eingang 
      - l-bestand.wert-ausgang) / tot-anz. 
    FIND FIRST l-artikel WHERE l-artikel.artnr = s-artnr EXCLUSIVE-LOCK. 
    l-artikel.vk-preis = avrg-price. 
    FIND CURRENT l-artikel NO-LOCK. 
  END. 
 
  FIND FIRST l-bestand WHERE l-bestand.lager-nr = curr-lager AND 
      l-bestand.artnr = s-artnr EXCLUSIVE-LOCK NO-ERROR. 
  IF NOT AVAILABLE l-bestand THEN 
  DO: 
    create l-bestand. 
    l-bestand.artnr = s-artnr. 
    l-bestand.lager-nr = curr-lager. 
    l-bestand.anf-best-dat = init-date. 
  END. 
  l-bestand.anz-anf-best = l-bestand.anz-anf-best + anzahl. 
  l-bestand.val-anf-best = l-bestand.val-anf-best + wert. 
  FIND CURRENT l-bestand NO-LOCK. 
 
  create best-list. 
  best-list.artnr = s-artnr. 
  best-list.anf-best-dat = init-date. 
  best-list.lager-nr = curr-lager. 
  best-list.anz-anf-best = anzahl. 
  best-list.val-anf-best = wert.
  best-list.rec-id = RECID(l-bestand).
END.
