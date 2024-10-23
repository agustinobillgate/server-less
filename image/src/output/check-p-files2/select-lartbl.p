DEF TEMP-TABLE t-l-artikel
    FIELD artnr         LIKE l-artikel.artnr
    FIELD bezeich       LIKE l-artikel.bezeich
    FIELD masseinheit   LIKE l-artikel.masseinheit
    FIELD ek-aktuell    LIKE l-artikel.ek-aktuell
    FIELD ek-letzter    LIKE l-artikel.ek-letzter.

DEFINE INPUT  PARAMETER lief-nr AS INTEGER.
DEFINE INPUT  PARAMETER t-zwkum AS INTEGER.
DEFINE OUTPUT PARAMETER TABLE FOR t-l-artikel.

IF lief-nr GT 0 THEN 
FOR EACH l-artikel WHERE 
    (l-artikel.lief-nr1 = lief-nr OR l-artikel.lief-nr2 = lief-nr 
    OR l-artikel.lief-nr3 = lief-nr) NO-LOCK BY l-artikel.bezeich:
    CREATE t-l-artikel.
    ASSIGN
    t-l-artikel.artnr         = l-artikel.artnr
    t-l-artikel.bezeich       = l-artikel.bezeich
    t-l-artikel.masseinheit   = l-artikel.masseinheit
    t-l-artikel.ek-aktuell    = l-artikel.ek-aktuell
    t-l-artikel.ek-letzter    = l-artikel.ek-letzter.
END.
ELSE 
DO:
    FOR EACH l-artikel WHERE 
        l-artikel.zwkum = t-zwkum NO-LOCK BY l-artikel.bezeich:
        CREATE t-l-artikel.
        ASSIGN
        t-l-artikel.artnr         = l-artikel.artnr
        t-l-artikel.bezeich       = l-artikel.bezeich
        t-l-artikel.masseinheit   = l-artikel.masseinheit
        t-l-artikel.ek-aktuell    = l-artikel.ek-aktuell
        t-l-artikel.ek-letzter    = l-artikel.ek-letzter.
    END.
END.
