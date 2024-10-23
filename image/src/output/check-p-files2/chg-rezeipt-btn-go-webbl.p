
DEF INPUT PARAMETER rec-id AS INT.
DEF INPUT PARAMETER katnr AS INT.
DEF INPUT PARAMETER portion LIKE h-rezept.portion.
DEF INPUT PARAMETER h-bezeich AS CHAR.
DEF INPUT PARAMETER katbezeich AS CHAR.
DEF INPUT PARAMETER user-init AS CHAR. /*FDL Sept 25, 2023 => Ticket 1E0427*/

DEFINE VARIABLE vLog AS LOGICAL.

FIND FIRST h-rezept WHERE RECID(h-rezept) = rec-id.
FIND CURRENT h-rezept EXCLUSIVE-LOCK. 

IF h-rezept.kategorie NE katnr
    OR h-rezept.portion NE portion 
    OR STRING(h-bezeich, "x(24)") NE SUBSTR(h-rezept.bezeich, 1, 24) THEN
DO:
    vLog = YES.
END.

IF vLog THEN
DO:
    FIND FIRST bediener WHERE bediener.userinit EQ user-init NO-LOCK NO-ERROR.
    CREATE res-history.
    ASSIGN
        res-history.nr          = bediener.nr
        res-history.datum       = TODAY
        res-history.zeit        = TIME
        res-history.action      = "Change Recipe"
        res-history.aenderung   = "Modify Recipe " + STRING(h-rezept.artnrrezept) 
                                + "(" + SUBSTR(h-rezept.bezeich, 1, 24) + ")" + " => "
        .

    IF h-rezept.kategorie NE katnr THEN
    DO:
        res-history.aenderung = res-history.aenderung + "CatNo " + STRING(h-rezept.kategorie)
            + " to " + STRING(katnr) + ";".
    END.
    ELSE IF h-rezept.portion NE portion THEN
    DO:
        res-history.aenderung = res-history.aenderung + "Portion " + STRING(h-rezept.portion)
            + " to " + STRING(portion) + ";".
    END.
    ELSE IF STRING(h-bezeich, "x(24)") NE SUBSTR(h-rezept.bezeich, 1, 24) THEN
    DO:
        res-history.aenderung = res-history.aenderung + "Description " + SUBSTR(h-rezept.bezeich, 1, 24)
            + " to " + STRING(h-bezeich, "x(24)") + ";".
    END.
END.

h-rezept.portion = portion.
h-rezept.datummod = TODAY.  /*FD September 18, 2020*/
IF katnr NE h-rezept.kategorie 
  OR STRING(h-bezeich, "x(24)") NE SUBSTR(h-rezept.bezeich, 1, 24) THEN 
DO: 
  h-rezept.kategorie = katnr. 
  h-rezept.bezeich  = STRING(h-bezeich, "x(24)") + katbezeich. 
END. 
FIND CURRENT h-rezept NO-LOCK.
