DEF TEMP-TABLE t-l-artikel
    FIELD rec-id        AS INT
    FIELD artnr         LIKE l-artikel.artnr
    FIELD bezeich       LIKE l-artikel.bezeich
    FIELD ek-aktuell    LIKE l-artikel.ek-aktuell
    FIELD ek-letzter    LIKE l-artikel.ek-letzter
    FIELD traubensort   LIKE l-artikel.traubensort
    FIELD lief-einheit  LIKE l-artikel.lief-einheit
    FIELD lief-nr1      LIKE l-artikel.lief-nr1
    FIELD lief-nr2      LIKE l-artikel.lief-nr2
    FIELD lief-nr3      LIKE l-artikel.lief-nr3
    FIELD jahrgang      LIKE l-artikel.jahrgang
    FIELD alkoholgrad   LIKE l-artikel.alkoholgrad.

DEF INPUT PARAMETER s-artnr AS INT.
DEF OUTPUT PARAMETER TABLE FOR t-l-artikel.

FIND FIRST l-artikel WHERE artnr = s-artnr.
CREATE t-l-artikel.
ASSIGN
    t-l-artikel.rec-id        = RECID(l-artikel)
    t-l-artikel.artnr         = l-artikel.artnr
    t-l-artikel.bezeich       = l-artikel.bezeich
    t-l-artikel.ek-aktuell    = l-artikel.ek-aktuell
    t-l-artikel.ek-letzter    = l-artikel.ek-letzter
    t-l-artikel.traubensort   = l-artikel.traubensort
    t-l-artikel.lief-einheit  = l-artikel.lief-einheit
    t-l-artikel.lief-nr1      = l-artikel.lief-nr1
    t-l-artikel.lief-nr2      = l-artikel.lief-nr2
    t-l-artikel.lief-nr3      = l-artikel.lief-nr3
    t-l-artikel.jahrgang      = l-artikel.jahrgang
    t-l-artikel.alkoholgrad   = l-artikel.alkoholgrad.
