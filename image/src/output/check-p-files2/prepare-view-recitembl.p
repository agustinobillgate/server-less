
DEFINE TEMP-TABLE h-list 
  FIELD STR         AS CHAR 
  FIELD portion     AS INTEGER FORMAT ">,>>>"            LABEL "Portion" 
  FIELD artnr       AS INTEGER FORMAT "9999999"          COLUMN-LABEL "  ArtNo" 
  FIELD bezeich     AS CHAR FORMAT "x(36)"               COLUMN-LABEL "Description" 
  FIELD lostfact    LIKE h-rezlin.lostfact 
  FIELD menge       AS DECIMAL FORMAT ">>>,>>9.999"      COLUMN-LABEL "Quantity" 
  FIELD cost        AS DECIMAL FORMAT ">,>>>,>>>,>>9.99" COLUMN-LABEL "Cost" 
  FIELD r-artnr     AS INTEGER FORMAT ">>>,>>>"          COLUMN-LABEL "RecipeNo" 
  FIELD r-flag      AS LOGICAL FORMAT "Yes/ "            COLUMN-LABEL "Recipe-Flag" INITIAL NO
  FIELD costportion AS DECIMAL FORMAT ">,>>>,>>>,>>9.99" COLUMN-LABEL "Cost/Portion". 

DEF INPUT PARAMETER artnr AS INT.
DEF INPUT PARAMETER curr-i AS INT.

DEF OUTPUT PARAMETER t-str AS CHAR.
DEF OUTPUT PARAMETER o-portion LIKE h-rezept.portion.
DEF OUTPUT PARAMETER price-type AS INT.
DEF OUTPUT PARAMETER amount AS DECIMAL.
DEF OUTPUT PARAMETER amount1 AS DECIMAL.
DEF OUTPUT PARAMETER TABLE FOR h-list.

DEFINE VARIABLE curr-artnr AS INTEGER.  /*FD May 10, 2021*/

FIND FIRST h-rezept WHERE h-rezept.artnrrezept = artnr NO-LOCK. 
t-str = "Recipe Items - " + STRING(artnr) + " " 
      + TRIM(SUBSTR(h-rezept.bezeich, 1, 24)) 
      + " (Portion " + STRING(h-rezept.portion) + ")".
o-portion = h-rezept.portion.

FIND FIRST htparam WHERE paramnr = 1024 NO-LOCK. 
price-type = htparam.finteger. 

amount = 0. 
RUN create-list(artnr, curr-i). 
amount1 = amount / o-portion.

PROCEDURE create-list: 
DEFINE INPUT PARAMETER p-artnr AS INTEGER. 
DEFINE INPUT PARAMETER menge AS DECIMAL. 
DEFINE VARIABLE c-artnr AS INTEGER. 
DEFINE VARIABLE cost AS DECIMAL. 
DEFINE buffer h-recipe FOR h-rezept. 
DEFINE buffer hrecipe FOR h-rezept. 
DEFINE BUFFER t-h-rezlin FOR h-rezlin.
DEF VAR i AS INTEGER NO-UNDO. 
 
  FOR EACH h-rezlin WHERE h-rezlin.artnrrezept = p-artnr NO-LOCK:     
    IF h-rezlin.recipe-flag = YES THEN 
    DO: 
/* 
      DO i = 1 TO curr-i: 
        IF r-list.recipe-nr[i] = h-rezlin.artnrlager THEN 
        DO: 
             HIDE MESSAGE NO-PAUSE. 
            MESSAGE translateExtended ("Wrong recursive definition in Recipe :",lvCAREA,"") 
                + STRING(p-artnr) 
                VIEW-AS ALERT-BOX INFORMATION. 
            RETURN. 
        END. 
      END. 
      curr-i = curr-i + 1. 
      r-list.recipe-nr[curr-i] = h-rezlin.artnrlager. 
*/ 
      curr-artnr = p-artnr.
      create h-list. 
      h-list.r-artnr = p-artnr. 
      FIND FIRST h-recipe WHERE h-recipe.artnrrezept = h-rezlin.artnrlager 
        NO-LOCK. 
      h-list.artnr = h-recipe.artnrrezept. 
      h-list.bezeich = h-recipe.bezeich. 
      h-list.menge = h-rezlin.menge.       
      h-list.portion = h-recipe.portion. 
      h-list.r-flag = YES. 
      h-list.str = STRING(h-list.artnr, ">>>>>>9") 
                 + STRING(h-list.bezeich, "x(24)") 
                 + STRING(" ", "x(12)") 
                 + STRING(h-list.menge, ">>>,>>9.999"). 

      RUN create-list(h-rezlin.artnrlager, 
          menge * h-rezlin.menge / h-recipe.portion).
    END. 
    ELSE 
    DO: 
      CREATE h-list. 
      FIND FIRST h-recipe WHERE h-recipe.artnrrezept = p-artnr NO-LOCK. 
      FIND FIRST l-artikel WHERE l-artikel.artnr = h-rezlin.artnrlager NO-LOCK. 
      FIND FIRST t-h-rezlin WHERE t-h-rezlin.artnrrezept = curr-artnr
        AND t-h-rezlin.artnrlager = p-artnr NO-LOCK NO-ERROR. /*FD May 10, 2021*/
      IF price-type = 0 OR l-artikel.ek-aktuell = 0 THEN 
      cost = (menge * h-rezlin.menge / l-artikel.inhalt * l-artikel.vk-preis) 
       / ( 1 - h-rezlin.lostfact / 100). 
      ELSE 
      cost = (menge * h-rezlin.menge / l-artikel.inhalt * l-artikel.ek-aktuell) 
       / ( 1 - h-rezlin.lostfact / 100). 
      amount = amount + cost.
      h-list.r-artnr = p-artnr. 
      h-list.artnr = l-artikel.artnr. 
      h-list.bezeich = l-artikel.bezeich. 
      h-list.lostfact = h-rezlin.lostfact. 
      h-list.menge = h-rezlin.menge * menge.  
      h-list.cost = cost.
      IF AVAILABLE t-h-rezlin AND t-h-rezlin.recipe-flag = YES THEN
      DO:
          h-list.costportion = cost / /* t-h-rezlin.menge */ o-portion.
      END.      
      ELSE 
      DO:
          h-list.costportion = cost / /* h-recipe.portion */ o-portion.         
      END.
        
      h-list.str = STRING(h-list.artnr, "9999999") 
                 + STRING(h-list.bezeich, "x(31)") 
                 + STRING(h-list.lostfact, "99.99") 
                 + STRING(h-list.menge, ">>>,>>9.999") 
                 + STRING(h-list.cost, ">,>>>,>>>,>>9.99")
                 + STRING(h-list.costportion, ">,>>>,>>>,>>9.99"). 
    END. 
  END. 
/*  create h-list. */ 
END. 
