
DEFINE INPUT PARAMETER p-artnr AS INTEGER. 
DEFINE INPUT PARAMETER menge AS DECIMAL. 
DEFINE INPUT-OUTPUT PARAMETER cost AS DECIMAL. 
DEFINE INPUT PARAMETER price-type AS INT.


DEFINE BUFFER hrecipe  FOR h-rezept.

RUN cal-cost.

/*
PROCEDURE cal-cost: 
DEFINE VARIABLE inh AS DECIMAL. 
DEFINE VARIABLE vk-preis AS DECIMAL. 
  FOR EACH h-rezlin WHERE h-rezlin.artnrrezept = p-artnr NO-LOCK: 
    IF NOT h-rezlin.recipe-flag THEN 
      inh = menge * h-rezlin.menge / (1 - h-rezlin.lostfact / 100). 
    ELSE inh = menge * h-rezlin.menge. 
    IF h-rezlin.recipe-flag = YES THEN DO:
        RUN cal-cost2(h-rezlin.artnrlager, inh, INPUT-OUTPUT cost).         
    END.
    ELSE 
    DO: 
      FIND FIRST l-artikel WHERE l-artikel.artnr = h-rezlin.artnrlager NO-LOCK. 
      IF price-type = 0 OR l-artikel.ek-aktuell = 0 THEN 
        vk-preis = l-artikel.vk-preis. 
      ELSE vk-preis = l-artikel.ek-aktuell. 
      cost = cost + inh / l-artikel.inhalt * vk-preis. 
    END.     
  END. 
END.

PROCEDURE cal-cost2: 
DEFINE INPUT PARAMETER p-artnr AS INTEGER. 
DEFINE INPUT PARAMETER menge AS DECIMAL. 
DEFINE INPUT-OUTPUT PARAMETER cost AS DECIMAL. 
DEFINE VARIABLE inh AS DECIMAL. 
DEFINE VARIABLE vk-preis AS DECIMAL. 

  FOR EACH h-rezlin WHERE h-rezlin.artnrrezept = p-artnr NO-LOCK:     
    IF NOT h-rezlin.recipe-flag THEN 
      inh = menge * h-rezlin.menge / (1 - h-rezlin.lostfact / 100). 
    ELSE inh = menge * h-rezlin.menge. 
    IF h-rezlin.recipe-flag = YES THEN RUN cal-cost3(h-rezlin.artnrlager, 
      inh, INPUT-OUTPUT cost). 
    ELSE 
    DO: 
      FIND FIRST l-artikel WHERE l-artikel.artnr = h-rezlin.artnrlager NO-LOCK. 
      IF price-type = 0 OR l-artikel.ek-aktuell = 0 THEN 
        vk-preis = l-artikel.vk-preis. 
      ELSE vk-preis = l-artikel.ek-aktuell. 
      cost = cost + inh / l-artikel.inhalt * vk-preis.       
    END. 
  END. 
END. 

PROCEDURE cal-cost3: 
DEFINE INPUT PARAMETER p-artnr AS INTEGER. 
DEFINE INPUT PARAMETER menge AS DECIMAL. 
DEFINE INPUT-OUTPUT PARAMETER cost AS DECIMAL. 
DEFINE VARIABLE inh AS DECIMAL. 
DEFINE VARIABLE vk-preis AS DECIMAL. 
  FOR EACH h-rezlin WHERE h-rezlin.artnrrezept = p-artnr NO-LOCK: 
    IF NOT h-rezlin.recipe-flag THEN 
      inh = menge * h-rezlin.menge / (1 - h-rezlin.lostfact / 100). 
    ELSE inh = menge * h-rezlin.menge. 
    IF h-rezlin.recipe-flag = YES THEN RUN cal-cost3(h-rezlin.artnrlager, 
      inh, INPUT-OUTPUT cost). 
    ELSE 
    DO: 
      FIND FIRST l-artikel WHERE l-artikel.artnr = h-rezlin.artnrlager NO-LOCK. 
      IF price-type = 0 OR l-artikel.ek-aktuell = 0 THEN 
        vk-preis = l-artikel.vk-preis. 
      ELSE vk-preis = l-artikel.ek-aktuell. 
      cost = cost + inh / l-artikel.inhalt * vk-preis. 
    END. 
  END. 
END.  */

PROCEDURE cal-cost: 
DEFINE VARIABLE inh AS DECIMAL. 
DEFINE VARIABLE vk-preis AS DECIMAL. 

  FOR EACH h-rezlin WHERE h-rezlin.artnrrezept = p-artnr NO-LOCK: 
    IF NOT h-rezlin.recipe-flag THEN 
      inh = menge * h-rezlin.menge / (1 - h-rezlin.lostfact / 100). 
    ELSE DO: 
        FIND FIRST hrecipe WHERE hrecipe.artnrrezept = h-rezlin.artnrlager NO-LOCK NO-ERROR.
        IF hrecipe.portion GT 1 THEN
               ASSIGN inh = menge * h-rezlin.menge / hrecipe.portion.
        ELSE inh = menge * h-rezlin.menge /* SY 25022016 / h-recipe.portion */. 
    END.
    IF h-rezlin.recipe-flag = YES THEN DO:
        RUN cal-cost2(h-rezlin.artnrlager, inh, INPUT-OUTPUT cost).         
    END.
    ELSE 
    DO: 
      FIND FIRST l-artikel WHERE l-artikel.artnr = h-rezlin.artnrlager NO-LOCK. 
      IF price-type = 0 OR l-artikel.ek-aktuell = 0 THEN 
        vk-preis = l-artikel.vk-preis. 
      ELSE vk-preis = l-artikel.ek-aktuell. 
      cost = cost + inh / l-artikel.inhalt * vk-preis. 
    END.     
  END. 
END. 

PROCEDURE cal-cost2: 
DEFINE INPUT PARAMETER p-artnr AS INTEGER. 
DEFINE INPUT PARAMETER menge AS DECIMAL. 
DEFINE INPUT-OUTPUT PARAMETER cost AS DECIMAL. 
DEFINE VARIABLE inh AS DECIMAL. 
DEFINE VARIABLE vk-preis AS DECIMAL. 

  FOR EACH h-rezlin WHERE h-rezlin.artnrrezept = p-artnr NO-LOCK:     
    IF NOT h-rezlin.recipe-flag THEN 
      inh = menge * h-rezlin.menge / (1 - h-rezlin.lostfact / 100). 
    ELSE DO: 
        FIND FIRST hrecipe WHERE hrecipe.artnrrezept = h-rezlin.artnrlager NO-LOCK NO-ERROR.
        IF hrecipe.portion GT 1 THEN
               ASSIGN inh = menge * h-rezlin.menge / hrecipe.portion.
        ELSE inh = menge * h-rezlin.menge /* SY 25022016 / h-recipe.portion */. 
    END.
    IF h-rezlin.recipe-flag = YES THEN 
        RUN cal-cost3(h-rezlin.artnrlager, inh, INPUT-OUTPUT cost). 
    ELSE 
    DO: 
      FIND FIRST l-artikel WHERE l-artikel.artnr = h-rezlin.artnrlager NO-LOCK. 
      IF price-type = 0 OR l-artikel.ek-aktuell = 0 THEN 
        vk-preis = l-artikel.vk-preis. 
      ELSE vk-preis = l-artikel.ek-aktuell. 
      cost = cost + inh / l-artikel.inhalt * vk-preis.       
    END. 
  END. 
END. 

PROCEDURE cal-cost3: 
DEFINE INPUT PARAMETER p-artnr AS INTEGER. 
DEFINE INPUT PARAMETER menge AS DECIMAL. 
DEFINE INPUT-OUTPUT PARAMETER cost AS DECIMAL. 
DEFINE VARIABLE inh AS DECIMAL. 
DEFINE VARIABLE vk-preis AS DECIMAL. 
  FOR EACH h-rezlin WHERE h-rezlin.artnrrezept = p-artnr NO-LOCK: 
    IF NOT h-rezlin.recipe-flag THEN 
      inh = menge * h-rezlin.menge / (1 - h-rezlin.lostfact / 100). 
    ELSE DO: 
        FIND FIRST hrecipe WHERE hrecipe.artnrrezept = h-rezlin.artnrlager NO-LOCK NO-ERROR.
        IF hrecipe.portion GT 1 THEN
               ASSIGN inh = menge * h-rezlin.menge / hrecipe.portion.
        ELSE inh = menge * h-rezlin.menge /* SY 25022016 / h-recipe.portion */. 
    END.
    IF h-rezlin.recipe-flag = YES THEN 
        RUN cal-cost3(h-rezlin.artnrlager, inh, INPUT-OUTPUT cost). 
    ELSE 
    DO: 
      FIND FIRST l-artikel WHERE l-artikel.artnr = h-rezlin.artnrlager NO-LOCK. 
      IF price-type = 0 OR l-artikel.ek-aktuell = 0 THEN 
        vk-preis = l-artikel.vk-preis. 
      ELSE vk-preis = l-artikel.ek-aktuell. 
      cost = cost + inh / l-artikel.inhalt * vk-preis. 
    END. 
  END. 
END. 


