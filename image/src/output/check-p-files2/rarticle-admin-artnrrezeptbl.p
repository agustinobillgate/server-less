
DEF INPUT PARAMETER h-artnrrezept AS INT.
DEF INPUT PARAMETER artnr         AS INT.
DEF OUTPUT PARAMETER flag         AS INT INIT 0.

FIND FIRST h-rezept WHERE h-rezept.artnrrezept = h-artnrrezept NO-LOCK NO-ERROR. 
IF NOT AVAILABLE h-rezept AND artnr NE 0 THEN flag = 1.
