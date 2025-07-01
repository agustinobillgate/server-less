
DEF INPUT PARAMETER s-artnr     AS INT.
DEF INPUT PARAMETER qty         AS DECIMAL.
DEF INPUT PARAMETER old-qty     AS DECIMAL.
DEF INPUT PARAMETER amount      AS DECIMAL.
DEF INPUT PARAMETER old-amount  AS DECIMAL.
DEF INPUT PARAMETER curr-lager  AS INT.
DEF INPUT PARAMETER s-recid     AS INT.

DEF INPUT-OUTPUT PARAMETER t-amount AS DECIMAL.
DEF OUTPUT PARAMETER suc-flg  AS LOGICAL INIT NO.
DEF OUTPUT PARAMETER anzahl      AS DECIMAL. 
DEF OUTPUT PARAMETER wert        AS DECIMAL. 

DEFINE VARIABLE avrg-price AS DECIMAL. 

RUN modify-bestand.

PROCEDURE modify-bestand:
DEFINE VARIABLE curr-pos    AS INTEGER. 
DEFINE VARIABLE tot-anz     AS DECIMAL. 
 
  anzahl = qty. 
  wert   = amount. 
  t-amount = t-amount + wert - old-amount. 
 
/* UPDATE stock onhand  */ 
  FIND FIRST l-bestand WHERE l-bestand.lager-nr = 0 AND 
      l-bestand.artnr = s-artnr EXCLUSIVE-LOCK. 
  l-bestand.anz-anf-best = l-bestand.anz-anf-best + anzahl - old-qty. 
  l-bestand.val-anf-best = l-bestand.val-anf-best + wert - old-amount. 
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
  l-bestand.anz-anf-best = anzahl. 
  l-bestand.val-anf-best = wert. 
  FIND CURRENT l-bestand NO-LOCK.
  suc-flg = YES.
END.
