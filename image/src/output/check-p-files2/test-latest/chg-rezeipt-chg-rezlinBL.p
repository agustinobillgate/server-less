
DEF INPUT  PARAMETER s-rezlin-h-recid AS INT.
DEF INPUT  PARAMETER h-rezept-recid AS INT.
DEF INPUT  PARAMETER qty AS DECIMAL.
DEF INPUT  PARAMETER lostfact LIKE h-rezlin.lostfact.
DEF OUTPUT PARAMETER artnrlager LIKE h-rezlin.artnrlager.

FIND FIRST h-rezept WHERE RECID(h-rezept) = h-rezept-recid NO-LOCK.
FIND FIRST h-rezlin WHERE RECID(h-rezlin) = s-rezlin-h-recid NO-LOCK.
DO TRANSACTION:
    FIND CURRENT h-rezlin EXCLUSIVE-LOCK.
    ASSIGN
        h-rezlin.menge = qty
        h-rezlin.lostfact = lostfact.
    FIND CURRENT h-rezlin NO-LOCK. 

    FIND CURRENT h-rezept EXCLUSIVE-LOCK.
    h-rezept.datummod = today.
    FIND CURRENT h-rezept NO-LOCK.
END.

artnrlager = h-rezlin.artnrlager.
