
DEF TEMP-TABLE t-artikel
    FIELD artnr         LIKE artikel.artnr
    FIELD departement   LIKE artikel.departement
    FIELD bezeich       LIKE artikel.bezeich.

DEF INPUT PARAMETER dept AS INT.
DEF OUTPUT PARAMETER TABLE FOR t-artikel.

FOR EACH artikel WHERE artikel.departement = dept 
    AND artikel.artart = 1 NO-LOCK:
    CREATE t-artikel.
    ASSIGN
    t-artikel.artnr         = artikel.artnr
    t-artikel.departement   = artikel.departement
    t-artikel.bezeich       = artikel.bezeich.
END.
