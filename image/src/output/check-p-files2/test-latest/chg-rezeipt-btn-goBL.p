
DEF INPUT PARAMETER rec-id AS INT.
DEF INPUT PARAMETER katnr AS INT.
DEF INPUT PARAMETER portion LIKE h-rezept.portion.
DEF INPUT PARAMETER h-bezeich AS CHAR.
DEF INPUT PARAMETER katbezeich AS CHAR.

FIND FIRST h-rezept WHERE RECID(h-rezept) = rec-id.
FIND CURRENT h-rezept EXCLUSIVE-LOCK. 
h-rezept.portion = portion.
h-rezept.datummod = TODAY.  /*FD September 18, 2020*/
IF katnr NE h-rezept.kategorie 
  OR STRING(h-bezeich, "x(24)") NE SUBSTR(h-rezept.bezeich, 1, 24) THEN 
DO: 
  h-rezept.kategorie = katnr. 
  h-rezept.bezeich  = STRING(h-bezeich, "x(24)") + katbezeich. 
END. 
FIND CURRENT h-rezept NO-LOCK.
