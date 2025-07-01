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
DEF INPUT PARAMETER cost-percent     AS DECIMAL NO-UNDO. /*bernatd 2024 FA7A78*/
DEF INPUT PARAMETER poten-sell-price AS DECIMAL NO-UNDO. /*bernatd 2024 FA7A78*/   

DEF OUTPUT PARAMETER warn-flag  AS INT INIT 0.
DEF OUTPUT PARAMETER vk-preis   LIKE l-artikel.vk-preis.
DEFINE VARIABLE inh AS DECIMAL.
DEF OUTPUT PARAMETER TABLE FOR s-rezlin.

DEFINE VARIABLE curr-pos AS INTEGER INITIAL 0. 
DEFINE VARIABLE recipe-cost AS DECIMAL.
DEFINE VARIABLE amount AS DECIMAL.
DEFINE VARIABLE portion LIKE h-rezept.portion.

IF lostfact EQ ? THEN lostfact = 0.00.
ELSE lostfact = lostfact.  /*bernatd-3AD18C-2025 */

DEFINE BUFFER h-rezlin1 FOR h-rezlin.
DEFINE BUFFER hrecipe  FOR h-rezept.

FIND FIRST h-rezept WHERE h-rezept.artnrrezept = h-artnr NO-LOCK.
IF AVAILABLE h-rezept THEN
DO:
  portion = h-rezept.portion. 
END.

RUN create-amount.
RUN create-rezlin.

/*start bernatd 9DB4FF 2024*/
PROCEDURE create-amount: 
  DEFINE VARIABLE cost AS DECIMAL. 
  DEFINE VARIABLE cost2 AS DECIMAL. 
  DEFINE buffer h-recipe FOR h-rezept. 
  DEFINE VARIABLE vk-preis AS DECIMAL. 
    FOR EACH h-rezlin WHERE h-rezlin.artnrrezept = h-artnr NO-LOCK: 
      curr-pos = curr-pos + 1. 

      IF h-rezlin.recipe-flag = NO THEN 
      DO: 
        FIND FIRST l-artikel WHERE l-artikel.artnr = h-rezlin.artnrlager NO-LOCK. 
        
        IF price-type = 0 OR l-artikel.ek-aktuell = 0 THEN 
          vk-preis = l-artikel.vk-preis. 
        ELSE vk-preis = l-artikel.ek-aktuell. 
        cost2 = h-rezlin.menge / l-artikel.inhalt * vk-preis 
          / (1 - h-rezlin.lostfact / 100). 
      END. 
      ELSE IF h-rezlin.recipe-flag = YES THEN 
      DO: 
        RUN cal-cost(h-rezlin1.artnrlager,inh, INPUT-OUTPUT cost).
        cost2 = cost2 + cost.  
      END. 
      amount = amount + cost2.
    END. 
  END. 
  /*end bernatd*/

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
    FIND FIRST l-artikel WHERE l-artikel.artnr = artnr NO-LOCK NO-ERROR. 
    IF price-type = 0 OR l-artikel.ek-aktuell = 0 THEN 
      vk-preis = l-artikel.vk-preis. 
    ELSE vk-preis = l-artikel.ek-aktuell. 
    s-rezlin.masseinheit = STRING(l-artikel.masseinheit,"x(3)"). 
    s-rezlin.inhalt = l-artikel.inhalt. 
    s-rezlin.vk-preis = vk-preis. 
    s-rezlin.cost = qty / l-artikel.inhalt * vk-preis 
      / (1 - s-rezlin.lostfact / 100). 

    amount = amount + s-rezlin.cost.

    IF NUM-ENTRIES(l-artikel.herkunft, ";") GT 1 THEN ASSIGN s-rezlin.s-unit = ENTRY(2, l-artikel.herkunft, ";" ).
    IF s-rezlin.s-unit = " " THEN ASSIGN s-rezlin.s-unit = l-artikel.masseinheit.
    IF s-rezlin.cost = 0 THEN 
    DO: 
      warn-flag = 1.
    END. 
    poten-sell-price = 100 / cost-percent * amount / portion. 

    /*start bernatd FA7A78*/
    FIND FIRST queasy WHERE queasy.KEY EQ 252 AND queasy.number1 EQ h-artnr EXCLUSIVE-LOCK NO-ERROR.
    IF AVAILABLE queasy THEN
    DO:
        ASSIGN
            queasy.deci1 = cost-percent
            queasy.deci2 = poten-sell-price.

        FIND CURRENT queasy NO-LOCK.
        RELEASE queasy.
    END.
    ELSE
    DO:
        CREATE queasy.
        ASSIGN
            queasy.KEY     = 252
            queasy.number1 = h-artnr
            queasy.date1   = TODAY
            queasy.deci1   = cost-percent
            queasy.deci2   = poten-sell-price.

        FIND CURRENT queasy NO-LOCK.
    END.
    /*end bernatd FA7A78*/
  
    
  END. 
  /*modified by bernatd 9DB4FF*/
  ELSE IF recipetype = 2 THEN  
  DO: 
      FIND FIRST h-rezept WHERE h-rezept.artnrrezept EQ artnr NO-LOCK NO-ERROR.
      IF AVAILABLE h-rezept THEN
        DO: 
          FOR EACH h-rezlin1 WHERE h-rezlin1.artnrrezept = artnr NO-LOCK:   
            FIND FIRST hrecipe WHERE hrecipe.artnrrezept = h-rezlin1.artnrrezept NO-LOCK NO-ERROR.
            IF hrecipe.portion GT 1 THEN
                   ASSIGN inh = qty * h-rezlin1.menge / hrecipe.portion.
            ELSE inh = qty * h-rezlin1.menge. 

            IF h-rezlin1.recipe-flag = YES THEN 
            DO:
              RUN cal-cost(h-rezlin1.artnrlager,inh, INPUT-OUTPUT cost).
            END. 
            ELSE DO:
              FIND FIRST l-artikel WHERE l-artikel.artnr = h-rezlin1.artnrlager NO-LOCK.   
              IF price-type = 0 OR l-artikel.ek-aktuell = 0 THEN   
              vk-preis = l-artikel.vk-preis.   
              ELSE vk-preis = l-artikel.ek-aktuell.   
              cost = cost + inh / l-artikel.inhalt * vk-preis / (1 - h-rezlin1.lostfact / 100). 
            END.
            
          END.   
        s-rezlin.recipe-flag = YES. 
        s-rezlin.inhalt = inhalt.
        s-rezlin.cost = cost. 
        IF s-rezlin.cost = 0 THEN 
        DO: 
          warn-flag = 2.
        END.

        amount = amount + s-rezlin.cost.
        poten-sell-price = 100 / cost-percent * amount / portion. 

        FIND FIRST queasy WHERE queasy.KEY EQ 252 AND queasy.number1 EQ h-artnr EXCLUSIVE-LOCK NO-ERROR.
        IF AVAILABLE queasy THEN
        DO:
            ASSIGN
                queasy.deci1 = cost-percent
                queasy.deci2 = poten-sell-price.

            FIND CURRENT queasy NO-LOCK.
            RELEASE queasy.
        END.
        ELSE
        DO:
            CREATE queasy.
            ASSIGN
                queasy.KEY     = 252
                queasy.number1 = h-artnr
                queasy.date1   = TODAY
                queasy.deci1   = cost-percent
                queasy.deci2   = poten-sell-price.

            FIND CURRENT queasy NO-LOCK.
        END.
      END. 
  END. /*end modified*/
 
  create h-rezlin. 
  h-rezlin.artnrrezept = h-artnr. 
  h-rezlin.artnrlager = s-rezlin.artnr. 
  h-rezlin.menge = s-rezlin.menge. 
  h-rezlin.lostfact = s-rezlin.lostfact. 
  h-rezlin.recipe-flag = s-rezlin.recipe-flag. 
  FIND CURRENT h-rezlin NO-LOCK. 
  s-rezlin.h-recid = RECID(h-rezlin).
END.

/*add by bernatd 9DB4FF*/
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
      ELSE inh = menge * h-rezlin1.menge.
  
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
  /*end bernatd*/
