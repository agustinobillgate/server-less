DEFINE TEMP-TABLE s-rezlin 
  FIELD pos         AS INTEGER 
  FIELD artnr       LIKE l-artikel.artnr                 COLUMN-LABEL "     ArtNo" 
  FIELD bezeich     AS CHAR FORMAT "x(36)"               COLUMN-LABEL "Description" 
  FIELD s-unit      AS CHAR FORMAT "x(8)"                COLUMN-LABEL "R-Unit"
  FIELD masseinheit LIKE l-artikel.masseinheit           COLUMN-LABEL "Unit" 
  FIELD menge       LIKE h-rezlin.menge                  COLUMN-LABEL "Quantity" 
  FIELD cost        AS DECIMAL FORMAT ">>>,>>>,>>>,>>9.99" COLUMN-LABEL "Cost"            /*>,>>>,>>>,>>9.99 gerald 190620*/
  FIELD vk-preis    AS DECIMAL FORMAT ">>>,>>>,>>>,>>9.99" COLUMN-LABEL "Avrg Price"      /*>,>>>,>>>,>>9.99 gerald 190620*/
  FIELD inhalt      AS DECIMAL FORMAT ">>>,>>9.99"       COLUMN-LABEL "Content" 
  FIELD lostfact    LIKE h-rezlin.lostfact 
  FIELD recipe-flag AS LOGICAL INITIAL NO. 

DEF INPUT PARAMETER s-artnr     AS INT.
DEF INPUT PARAMETER qty         AS DECIMAL.
DEF INPUT PARAMETER recipetype  AS INT.
DEF INPUT PARAMETER price-type  AS INT.
DEF INPUT PARAMETER DESCRIPT    AS CHAR.
DEF INPUT PARAMETER inhalt      LIKE l-artikel.inhalt.
DEF INPUT PARAMETER lostfact LIKE h-rezlin.lostfact.
DEF INPUT PARAMETER vk-preis   LIKE l-artikel.vk-preis. 
DEF OUTPUT PARAMETER warn-flag  AS INT INIT 0.
DEF OUTPUT PARAMETER TABLE FOR s-rezlin.

DEFINE VARIABLE curr-pos AS INTEGER INITIAL 0. 

IF recipetype = 1 THEN FIND FIRST l-artikel WHERE l-artikel.artnr = s-artnr.
RUN create-rezlin.

PROCEDURE create-rezlin: 
DEFINE VARIABLE cost AS DECIMAL. 
  curr-pos = curr-pos + 1. 
  CREATE s-rezlin. 
  ASSIGN
    s-rezlin.pos = curr-pos
    s-rezlin.artnr = s-artnr
    s-rezlin.bezeich = DESCRIPT 
    s-rezlin.menge = qty
    s-rezlin.lostfact = lostfact
  . 
  IF recipetype = 1 THEN 
  DO: 
    IF price-type = 0 OR l-artikel.ek-aktuell = 0 THEN 
      vk-preis = l-artikel.vk-preis. 
    ELSE vk-preis = l-artikel.ek-aktuell. 
    ASSIGN
      s-rezlin.masseinheit = l-artikel.masseinheit
      s-rezlin.s-unit = ENTRY(2, l-artikel.herkunft, ";")
      s-rezlin.inhalt = l-artikel.inhalt
      s-rezlin.vk-preis = vk-preis
      s-rezlin.cost = qty / l-artikel.inhalt * vk-preis
    . 
    IF s-rezlin.s-unit = "" AND s-rezlin.inhalt = 1 THEN
       s-rezlin.s-unit = s-rezlin.masseinheit.

    IF lostfact NE 0 THEN s-rezlin.cost = s-rezlin.cost /  (1 - lostfact / 100). 
    IF s-rezlin.cost = 0 THEN 
    DO: 
      warn-flag = 1.
    END. 
  END. 
  ELSE IF recipetype = 2 THEN 
  DO: 
    ASSIGN
      s-rezlin.recipe-flag = YES
      s-rezlin.inhalt = inhalt
      s-rezlin.cost = qty * vk-preis
    . 
    IF s-rezlin.cost = 0 THEN 
    DO: 
      warn-flag = 2.
    END. 
  END. 
END. 
