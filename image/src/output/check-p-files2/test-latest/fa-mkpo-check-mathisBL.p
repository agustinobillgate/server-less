
DEF TEMP-TABLE t-mathis LIKE mathis.
DEF INPUT  PARAMETER art-nr       AS INT.
DEF OUTPUT PARAMETER avail-mathis AS LOGICAL INIT YES.
DEF INPUT-OUTPUT PARAMETER TABLE FOR t-mathis.

FIND FIRST mathis WHERE mathis.nr = art-nr NO-LOCK NO-ERROR. 
IF NOT AVAILABLE mathis THEN avail-mathis = NO.

FOR EACH mathis WHERE mathis.nr = art-nr NO-LOCK:
    CREATE t-mathis.
    BUFFER-COPY mathis TO t-mathis.
END.
