
DEF TEMP-TABLE temp-l-artikel1
    FIELD fibukonto    LIKE l-artikel.fibukonto
    FIELD bezeich      LIKE l-artikel.bezeich
    FIELD ek-aktuell   LIKE l-artikel.ek-aktuell
    FIELD artnr        LIKE l-artikel.artnr
    FIELD traubensort  LIKE l-artikel.traubensort
    FIELD lief-einheit LIKE l-artikel.lief-einheit
    FIELD masseinheit  LIKE l-artikel.masseinheit
    FIELD betriebsnr   LIKE l-artikel.betriebsnr
    FIELD alkoholgrad  LIKE l-artikel.alkoholgrad.


DEF INPUT  PARAMETER s-artnr AS INT.
DEF OUTPUT PARAMETER TABLE FOR temp-l-artikel1.

FIND FIRST l-artikel WHERE l-artikel.artnr = s-artnr NO-LOCK NO-ERROR.
IF AVAILABLE l-artikel THEN
DO:
    CREATE temp-l-artikel1.
    ASSIGN
    temp-l-artikel1.fibukonto    = l-artikel.fibukonto
    temp-l-artikel1.bezeich      = l-artikel.bezeich
    temp-l-artikel1.ek-aktuell   = l-artikel.ek-aktuell
    temp-l-artikel1.artnr        = l-artikel.artnr
    temp-l-artikel1.traubensort  = l-artikel.traubensort
    temp-l-artikel1.lief-einheit = l-artikel.lief-einheit
    temp-l-artikel1.masseinheit  = l-artikel.masseinheit
    temp-l-artikel1.betriebsnr   = l-artikel.betriebsnr
    temp-l-artikel1.alkoholgrad  = l-artikel.alkoholgrad.
END.
