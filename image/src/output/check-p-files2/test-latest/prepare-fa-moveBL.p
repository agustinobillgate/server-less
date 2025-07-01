
DEF TEMP-TABLE t-fa-lager LIKE fa-lager.

DEF INPUT  PARAMETER artnr              AS INT.
DEF OUTPUT PARAMETER mathis-name        AS CHAR.
DEF OUTPUT PARAMETER fa-artikel-anzahl  AS INT.
DEF OUTPUT PARAMETER mathis-location    AS CHAR.
DEF OUTPUT PARAMETER TABLE FOR t-fa-lager.

FIND FIRST mathis WHERE mathis.nr = artnr NO-LOCK.
FIND FIRST fa-artikel WHERE fa-artikel.nr = artnr NO-LOCK.

ASSIGN
mathis-name = mathis.NAME
fa-artikel-anzahl = fa-artikel.anzahl
mathis-location = mathis.location.

FOR EACH fa-lager NO-LOCK:
    CREATE t-fa-lager.
    BUFFER-COPY fa-lager TO t-fa-lager.
END.
