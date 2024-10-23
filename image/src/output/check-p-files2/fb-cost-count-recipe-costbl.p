DEFINE WORKFILE s-rezlin 
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
  FIELD recipe-flag AS LOGICAL INITIAL NO. 

DEF INPUT  PARAMETER grid-list-artnrrezept AS INT.
DEF INPUT  PARAMETER price-type AS INT.
DEF INPUT-OUTPUT PARAMETER amount AS DECIMAL.

DEF VAR portion AS DECIMAL INITIAL 1 NO-UNDO.
DEFINE VARIABLE vk-preis AS DECIMAL.
DEFINE buffer h-recipe FOR h-rezept.

RELEASE h-rezept.
IF grid-list-artnrrezept NE 0 THEN
FIND FIRST h-rezept WHERE h-rezept.artnrrezept = grid-list-artnrrezept
  NO-LOCK NO-ERROR.
IF AVAILABLE h-rezept THEN portion = h-rezept.portion.

FOR EACH h-rezlin WHERE h-rezlin.artnrrezept = grid-list-artnrrezept NO-LOCK: 
    create s-rezlin. 
    s-rezlin.artnr = h-rezlin.artnrlager. 
    s-rezlin.menge = h-rezlin.menge / portion. 
    s-rezlin.lostfact = h-rezlin.lostfact. 
    IF h-rezlin.recipe-flag = NO THEN 
    DO: 
      FIND FIRST l-artikel WHERE l-artikel.artnr = h-rezlin.artnrlager NO-LOCK. 
      IF price-type = 0 OR l-artikel.ek-aktuell = 0 THEN 
        vk-preis = l-artikel.vk-preis. 
      ELSE vk-preis = l-artikel.ek-aktuell. 
      s-rezlin.bezeich = l-artikel.bezeich. 
      s-rezlin.masseinheit = STRING(l-artikel.masseinheit,"x(3)"). 
      s-rezlin.inhalt = l-artikel.inhalt. 
      s-rezlin.vk-preis = vk-preis. 
      s-rezlin.cost = h-rezlin.menge / l-artikel.inhalt * vk-preis / portion
        / (1 - h-rezlin.lostfact / 100). 
    END. 
    ELSE IF h-rezlin.recipe-flag = YES THEN 
    DO: 
      FIND FIRST h-recipe WHERE h-recipe.artnrrezept 
        = h-rezlin.artnrlager NO-LOCK. 
      s-rezlin.bezeich = h-recipe.bezeich. 
      s-rezlin.recipe-flag = YES. 
      s-rezlin.inhalt = 1. 
      cost = 0. 
      RUN cal-cost(h-rezlin.artnrlager, 1, INPUT-OUTPUT cost). 
      s-rezlin.cost = h-rezlin.menge * cost. 
    END. 
    amount = amount + s-rezlin.cost.
END.

PROCEDURE cal-cost: 
DEFINE INPUT PARAMETER p-artnr AS INTEGER. 
DEFINE INPUT PARAMETER menge AS DECIMAL. 
DEFINE INPUT-OUTPUT PARAMETER cost AS DECIMAL. 
DEFINE VARIABLE inh AS DECIMAL. 
DEFINE VARIABLE vk-preis AS DECIMAL. 
DEFINE buffer h-rezlin1 FOR h-rezlin. 

  FIND FIRST h-rezept WHERE h-rezept.artnrrezept = p-artnr NO-LOCK.  
  FOR EACH h-rezlin1 WHERE h-rezlin1.artnrrezept = p-artnr NO-LOCK: 
    inh = menge * h-rezlin1.menge. 
    IF h-rezlin1.recipe-flag = YES THEN RUN cal-cost(h-rezlin1.artnrlager, 
      inh, INPUT-OUTPUT cost). 
    ELSE 
    DO: 
      FIND FIRST l-artikel WHERE l-artikel.artnr = h-rezlin1.artnrlager NO-LOCK. 
      IF price-type = 0 OR l-artikel.ek-aktuell = 0 THEN 
        vk-preis = l-artikel.vk-preis. 
      ELSE vk-preis = l-artikel.ek-aktuell. 
      cost = cost + inh / l-artikel.inhalt * vk-preis / h-rezept.portion
        / (1 - h-rezlin1.lostfact / 100). 
    END. 
  END. 
END.
