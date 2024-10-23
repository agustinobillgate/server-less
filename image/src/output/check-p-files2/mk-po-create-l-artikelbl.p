/*DEF TEMP-TABLE t-l-artikel
    FIELD rec-id        AS INT
    FIELD artnr         LIKE l-artikel.artnr
    FIELD bezeich       LIKE l-artikel.bezeich
    FIELD betriebsnr    LIKE l-artikel.betriebsnr
    FIELD ek-aktuell    LIKE l-artikel.ek-aktuell
    FIELD ek-letzter    LIKE l-artikel.ek-letzter
    FIELD traubensort   LIKE l-artikel.traubensort
    FIELD lief-einheit  LIKE l-artikel.lief-einheit
    FIELD lief-nr1      LIKE l-artikel.lief-nr1
    FIELD lief-nr2      LIKE l-artikel.lief-nr2
    FIELD lief-nr3      LIKE l-artikel.lief-nr3
    FIELD jahrgang      LIKE l-artikel.jahrgang
    FIELD alkoholgrad   LIKE l-artikel.alkoholgrad.*/
    
DEF TEMP-TABLE t-l-artikel
    FIELD rec-id        AS INT
    FIELD artnr         AS INTEGER      FORMAT "9999999"
    FIELD bezeich       AS CHARACTER    FORMAT "x(36)"
    FIELD betriebsnr    AS INTEGER      FORMAT ">>>>9"
    FIELD ek-aktuell    AS DECIMAL      FORMAT "->>,>>9.999"
    FIELD ek-letzter    AS DECIMAL      FORMAT "->>,>>9.999"
    FIELD traubensort   AS CHARACTER    FORMAT "x(24)"
    FIELD lief-einheit  AS DECIMAL      FORMAT ">>>,>>9.999"
    FIELD lief-nr1      AS INTEGER      FORMAT ">,>>>,>>9"
    FIELD lief-nr2      AS INTEGER      FORMAT ">,>>>,>>9"
    FIELD lief-nr3      AS INTEGER      FORMAT ">,>>>,>>9"
    FIELD jahrgang      AS INTEGER      FORMAT ">>>9"
    FIELD alkoholgrad   AS DECIMAL      FORMAT ">9.99".

DEF INPUT PARAMETER s-artnr AS INT.
DEF OUTPUT PARAMETER TABLE FOR t-l-artikel.

FIND FIRST l-artikel WHERE l-artikel.artnr = s-artnr NO-LOCK NO-ERROR.
IF NOT AVAILABLE l-artikel THEN RETURN.

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
