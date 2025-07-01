
DEF INPUT PARAMETER departement AS INT.
DEF INPUT PARAMETER zknr AS INT.
DEF OUTPUT PARAMETER flag AS INT INIT 0.

FIND FIRST h-artikel WHERE h-artikel.departement = departement 
    AND h-artikel.zwkum = zknr NO-LOCK NO-ERROR. 
IF AVAILABLE h-artikel THEN 
DO: 
    flag = 1.
    /*MThide MESSAGE NO-PAUSE. 
    MESSAGE translateExtended ("Article exists, delete not possible.",lvCAREA,"") VIEW-AS ALERT-BOX.*/
END. 
ELSE 
DO: 
    FIND FIRST wgrpdep WHERE wgrpdep.departement = departement
        AND wgrpdep.zknr = zknr.
    DELETE wgrpdep.
    RELEASE wgrpdep.
END. 
