
DEF INPUT  PARAMETER pvILanguage    AS INTEGER  NO-UNDO.
DEF INPUT PARAMETER t-h-rezept-artnrrezept AS INT.
DEF OUTPUT PARAMETER msg-str AS CHAR.

{SupertransBL.i} 
DEF VAR lvCAREA AS CHAR INITIAL "recipe-list".

DEFINE buffer h-recipe FOR h-rezept. 

FIND FIRST h-rezlin WHERE h-rezlin.artnrlager = t-h-rezept-artnrrezept NO-LOCK NO-ERROR. 
IF AVAILABLE h-rezlin THEN 
DO: 
    FIND FIRST h-recipe WHERE h-recipe.artnrrezept = h-rezlin.artnrrezept NO-LOCK.
    msg-str = msg-str + CHR(2)
            + translateExtended ("Deleting not possible, used by other recipe",lvCAREA,"")
            + CHR(10)
            + STRING(h-recipe.artnrrezept) + " - " + h-recipe.bezeich.
    RETURN NO-APPLY.
END. 

FIND FIRST h-artikel WHERE h-artikel.artnrrezept = t-h-rezept-artnrrezept NO-LOCK NO-ERROR. 
IF AVAILABLE h-artikel THEN 
DO: 
    msg-str = msg-str + CHR(2)
            + translateExtended ("Deleting not possible, used by F/B-Article",lvCAREA,"")
            + CHR(10)
            + STRING(h-artikel.artnr) + " - " + h-artikel.bezeich.
    RETURN NO-APPLY.
END.
