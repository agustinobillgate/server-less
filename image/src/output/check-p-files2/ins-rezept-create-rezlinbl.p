DEFINE TEMP-TABLE s-rezlin 
  FIELD new-created AS LOGICAL INITIAL NO 
  FIELD h-recid     AS INTEGER 
  FIELD pos         AS INTEGER 
  FIELD artnr       LIKE l-artikel.artnr                 COLUMN-LABEL "     ArtNo" 
  FIELD bezeich     AS CHAR FORMAT "x(36)"               COLUMN-LABEL "Description" 
  FIELD masseinheit LIKE l-artikel.masseinheit           COLUMN-LABEL "Unit" 
  FIELD inhalt      AS DECIMAL FORMAT ">>>,>>9.99"       COLUMN-LABEL "Content" 
  FIELD vk-preis    AS DECIMAL FORMAT ">>>,>>>,>>9.99"   COLUMN-LABEL "Avrg Price" 
  FIELD cost        AS DECIMAL FORMAT ">,>>>,>>>,>>9.99" COLUMN-LABEL "Cost" 
  FIELD menge       LIKE h-rezlin.menge                  COLUMN-LABEL "Quantity" 
  FIELD lostfact    LIKE h-rezlin.lostfact 
  FIELD recipe-flag AS LOGICAL INITIAL NO
  FIELD s-unit      AS CHAR FORMAT "x(8)"                   COLUMN-LABEL "R-Unit".

DEF INPUT PARAMETER artnr       AS INT.
DEF INPUT PARAMETER h-artnr     AS INT.
DEF INPUT PARAMETER s-artnr     AS INT.
DEF INPUT PARAMETER qty         AS DECIMAL.
DEF INPUT PARAMETER recipetype  AS INT.
DEF INPUT PARAMETER price-type  AS INT.
DEF INPUT PARAMETER inhalt      LIKE l-artikel.inhalt.
DEF INPUT PARAMETER descript    AS CHAR.
DEF INPUT PARAMETER lostfact    LIKE h-rezlin.lostfact.   

DEF OUTPUT PARAMETER warn-flag  AS INT INIT 0.
DEF OUTPUT PARAMETER vk-preis   LIKE l-artikel.vk-preis.
DEF OUTPUT PARAMETER TABLE FOR s-rezlin.

DEFINE VARIABLE curr-pos AS INTEGER INITIAL 0. 


RUN create-rezlin.

PROCEDURE create-rezlin: 
    
DEFINE VARIABLE cost AS DECIMAL. 
  curr-pos = curr-pos + 1. 
  create s-rezlin. 
  s-rezlin.pos = curr-pos. 
  s-rezlin.artnr = s-artnr. 
  s-rezlin.bezeich = descript. 
  s-rezlin.menge = qty. 
  s-rezlin.lostfact = lostfact. 
  s-rezlin.new-created = YES. 
  IF recipetype = 1 THEN 
  DO:
      FIND FIRST l-artikel WHERE l-artikel.artnr = artnr.
    IF price-type = 0 OR l-artikel.ek-aktuell = 0 THEN 
      vk-preis = l-artikel.vk-preis. 
    ELSE vk-preis = l-artikel.ek-aktuell. 
    s-rezlin.masseinheit = STRING(l-artikel.masseinheit,"x(3)"). 
    s-rezlin.inhalt = l-artikel.inhalt. 
    s-rezlin.vk-preis = vk-preis. 
    s-rezlin.cost = qty / l-artikel.inhalt * vk-preis 
      / (1 - s-rezlin.lostfact / 100). 

    IF NUM-ENTRIES(l-artikel.herkunft, ";") GT 1 THEN ASSIGN s-rezlin.s-unit = ENTRY(2, l-artikel.herkunft, ";" ).
    IF s-rezlin.s-unit = " " THEN ASSIGN s-rezlin.s-unit = l-artikel.masseinheit.
    IF s-rezlin.cost = 0 THEN 
    DO: 
      warn-flag = 1.
    END. 
  END. 
  ELSE IF recipetype = 2 THEN 
  DO: 
      /*Alder - Ticket A1CE77 - Start*/
      FIND FIRST l-artikel WHERE l-artikel.artnr EQ artnr.
      IF price-type EQ 0 OR l-artikel.ek-aktuell EQ 0 THEN
          vk-preis = l-artikel.vk-preis.
      ELSE 
          vk-preis = l-artikel.ek-aktuell. 
      /*Alder - Ticket A1CE77 - End*/
      s-rezlin.recipe-flag = YES. 
      s-rezlin.inhalt = inhalt. 
      s-rezlin.cost = qty * vk-preis. 
      IF s-rezlin.cost = 0 THEN 
      DO: 
        warn-flag = 2.
      END.
  END. 
 
  create h-rezlin. 
  h-rezlin.artnrrezept = h-artnr. 
  h-rezlin.artnrlager = s-rezlin.artnr. 
  h-rezlin.menge = s-rezlin.menge. 
  h-rezlin.lostfact = s-rezlin.lostfact. 
  h-rezlin.recipe-flag = s-rezlin.recipe-flag. 
  FIND CURRENT h-rezlin NO-LOCK. 
  s-rezlin.h-recid = RECID(h-rezlin).
END.
