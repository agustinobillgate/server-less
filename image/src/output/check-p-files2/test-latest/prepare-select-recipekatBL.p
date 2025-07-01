
DEFINE TEMP-TABLE recipe 
  FIELD katno   AS INTEGER FORMAT ">>9" 
  FIELD bezeich AS CHAR FORMAT "x(24)". 

DEF OUTPUT PARAMETER TABLE FOR recipe.

FOR EACH h-rezept NO-LOCK BY h-rezept.kategorie: 
  FIND FIRST recipe WHERE recipe.katno = h-rezept.kategorie NO-LOCK NO-ERROR. 
  IF NOT AVAILABLE recipe THEN 
  DO: 
    create recipe. 
    recipe.katno   = h-rezept.kategorie.

    IF NUM-ENTRIES(h-rezept.bezeich, ";") GT 1 THEN
        recipe.bezeich = ENTRY(2, h-rezept.bezeich, ";").
    ELSE recipe.bezeich = SUBSTR(h-rezept.bezeich, 25, 24). 
  END. 
END. 
