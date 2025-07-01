

DEFINE INPUT PARAMETER p-artnr AS INTEGER. 
DEFINE INPUT PARAMETER menge AS DECIMAL. 
DEFINE INPUT-OUTPUT PARAMETER cost AS DECIMAL. 

DEF INPUT PARAMETER price-type AS INT.

RUN cal-cost(p-artnr, menge, INPUT-OUTPUT cost).

PROCEDURE cal-cost:

DEFINE INPUT PARAMETER p-artnr AS INTEGER. 
DEFINE INPUT PARAMETER menge   AS DECIMAL.
DEFINE INPUT-OUTPUT PARAMETER cost AS DECIMAL. 

DEFINE VARIABLE inh AS DECIMAL. 
DEFINE VARIABLE i   AS INTEGER NO-UNDO. 
DEFINE BUFFER h-recipe FOR h-rezept. 
DEFINE BUFFER hrecipe  FOR h-rezept.
  
  FIND FIRST h-recipe WHERE h-recipe.artnrrezept = p-artnr NO-LOCK. 
  FOR EACH h-rezlin WHERE h-rezlin.artnrrezept = p-artnr NO-LOCK: 
    /*inh = menge * h-rezlin.menge /* / h-recipe.portion */ . */

    IF h-rezlin.recipe-flag = YES THEN DO:
        /*ITA 101116*/
        FIND FIRST hrecipe WHERE hrecipe.artnrrezept = h-rezlin.artnrlager NO-LOCK NO-ERROR.
        IF hrecipe.portion GT 1 THEN
               ASSIGN inh = menge * h-rezlin.menge / hrecipe.portion.
        ELSE inh = menge * h-rezlin.menge /* SY 25022016 / h-recipe.portion */.
        RUN cal-cost(h-rezlin.artnrlager, inh, INPUT-OUTPUT cost). 
    END.
    ELSE 
    DO:
      inh = menge * h-rezlin.menge /* SY 25022016 / h-recipe.portion */.
      FIND FIRST l-artikel WHERE l-artikel.artnr = h-rezlin.artnrlager NO-LOCK.
      IF price-type = 0 OR l-artikel.ek-aktuell = 0 THEN 
      cost = cost + inh / l-artikel.inhalt * l-artikel.vk-preis 
        / (1 - h-rezlin.lostfact / 100).
      ELSE cost = cost + inh / l-artikel.inhalt * l-artikel.ek-aktuell 
        / (1 - h-rezlin.lostfact / 100).
    END.
  END.
END.
