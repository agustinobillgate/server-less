DEFINE TEMP-TABLE t-l-artikel LIKE l-artikel.
DEFINE TEMP-TABLE t-h-rezept LIKE h-rezept.

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

DEF INPUT PARAMETER fr-artnr    AS INT.
DEF INPUT PARAMETER to-artnr    AS INT.
DEF INPUT PARAMETER h-artnr     AS INT.

DEF OUTPUT PARAMETER katnr      AS INT.
DEF OUTPUT PARAMETER katbezeich AS CHAR.
DEF OUTPUT PARAMETER h-bezeich  AS CHAR.
DEF OUTPUT PARAMETER portion    LIKE h-rezept.portion.
DEF OUTPUT PARAMETER price-type AS INT.
DEF OUTPUT PARAMETER amount     AS DECIMAL.
DEF OUTPUT PARAMETER cost-percent     AS DECIMAL. /*bernatd FA7A78*/
DEF OUTPUT PARAMETER poten-sell-price AS DECIMAL. /*bernatd FA7A78*/
DEF OUTPUT PARAMETER TABLE FOR t-l-artikel.
DEF OUTPUT PARAMETER TABLE FOR t-h-rezept.
DEF OUTPUT PARAMETER TABLE FOR s-rezlin.

DEFINE VARIABLE curr-pos AS INTEGER INITIAL 0.

FIND FIRST h-rezept WHERE h-rezept.artnrrezept = h-artnr NO-LOCK. 
katnr = h-rezept.kategorie. 
katbezeich = SUBSTR(h-rezept.bezeich, 25, 24). 
h-bezeich = SUBSTR(h-rezept.bezeich, 1, 24). 
portion = h-rezept.portion. 
amount = 0. 
 
FIND FIRST htparam WHERE paramnr = 1024 NO-LOCK. 
price-type = htparam.finteger. 
 
RUN create-list. 

FOR EACH l-artikel WHERE l-artikel.artnr GE fr-artnr
    AND l-artikel.artnr LE to-artnr NO-LOCK:
    CREATE t-l-artikel.
    BUFFER-COPY l-artikel TO t-l-artikel.
END.

FOR EACH h-rezept:
    CREATE t-h-rezept.
    BUFFER-COPY h-rezept TO t-h-rezept.
END.


PROCEDURE create-list: 
DEFINE VARIABLE cost AS DECIMAL. 
DEFINE buffer h-recipe FOR h-rezept. 
DEFINE VARIABLE vk-preis AS DECIMAL. 
  FOR EACH h-rezlin WHERE h-rezlin.artnrrezept = h-artnr NO-LOCK: 
    curr-pos = curr-pos + 1. 
    create s-rezlin. 
    s-rezlin.pos = curr-pos. 
    s-rezlin.artnr = h-rezlin.artnrlager. 
    s-rezlin.menge = h-rezlin.menge. 
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
      s-rezlin.cost = h-rezlin.menge / l-artikel.inhalt * vk-preis 
        / (1 - h-rezlin.lostfact / 100). 

      IF NUM-ENTRIES(l-artikel.herkunft, ";") GT 1 THEN ASSIGN s-rezlin.s-unit = ENTRY(2, l-artikel.herkunft, ";" ).
      IF s-rezlin.s-unit = " " THEN ASSIGN s-rezlin.s-unit = l-artikel.masseinheit.
    END. 
    ELSE IF h-rezlin.recipe-flag = YES THEN 
    DO: 
      FIND FIRST h-recipe WHERE h-recipe.artnrrezept = h-rezlin.artnrlager NO-LOCK. 
      s-rezlin.bezeich     = h-recipe.bezeich. 
      s-rezlin.recipe-flag = YES. 
      s-rezlin.inhalt = h-recipe.portion. 
      cost = 0. 
      RUN cal-cost(h-rezlin.artnrlager, 1, INPUT-OUTPUT cost). 
      s-rezlin.cost = h-rezlin.menge * cost. 
    END. 
    amount = amount + s-rezlin.cost.


    /*start bernatd FA7A78*/
    FIND FIRST queasy WHERE queasy.KEY EQ 252 AND queasy.number1 EQ h-rezlin.artnrrezept NO-LOCK NO-ERROR.
    IF AVAILABLE queasy THEN
    DO:
        ASSIGN
        cost-percent     = queasy.deci1
        poten-sell-price = queasy.deci2.
    END.
    /*end bernatd*/

  END. 
END. 


PROCEDURE cal-cost:   
DEFINE INPUT PARAMETER p-artnr AS INTEGER.   
DEFINE INPUT PARAMETER menge AS DECIMAL.   
DEFINE INPUT-OUTPUT PARAMETER cost AS DECIMAL.   
DEFINE VARIABLE inh AS DECIMAL.   
DEFINE VARIABLE vk-preis AS DECIMAL.   
DEFINE BUFFER h-rezlin1 FOR h-rezlin.
DEFINE BUFFER hrecipe  FOR h-rezept.

  FOR EACH h-rezlin1 WHERE h-rezlin1.artnrrezept = p-artnr NO-LOCK:   
    FIND FIRST hrecipe WHERE hrecipe.artnrrezept = h-rezlin1.artnrrezept NO-LOCK NO-ERROR.
     
    IF hrecipe.portion GT 1 THEN
           ASSIGN inh = menge * h-rezlin1.menge / hrecipe.portion.
    ELSE inh = menge * h-rezlin1.menge /* SY 25022016 / h-recipe.portion */.

    IF h-rezlin1.recipe-flag = YES THEN RUN cal-cost(h-rezlin1.artnrlager,   
      inh, INPUT-OUTPUT cost).   
    ELSE   
    DO:   
      FIND FIRST l-artikel WHERE l-artikel.artnr = h-rezlin1.artnrlager NO-LOCK.   
      IF price-type = 0 OR l-artikel.ek-aktuell = 0 THEN   
        vk-preis = l-artikel.vk-preis.   
      ELSE vk-preis = l-artikel.ek-aktuell.   
      cost = cost + inh / l-artikel.inhalt * vk-preis   
        / (1 - h-rezlin1.lostfact / 100).   
    END.   
  END.   
END.   
