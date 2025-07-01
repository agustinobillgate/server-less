DEF TEMP-TABLE temp-l-artikel
    FIELD fibukonto    LIKE l-artikel.fibukonto
    FIELD bezeich      LIKE l-artikel.bezeich
    FIELD ek-aktuell   LIKE l-artikel.ek-aktuell
    FIELD artnr        LIKE l-artikel.artnr
    FIELD traubensort  LIKE l-artikel.traubensort
    FIELD lief-einheit LIKE l-artikel.lief-einheit
    FIELD masseinheit  LIKE l-artikel.masseinheit
    FIELD betriebsnr   LIKE l-artikel.betriebsnr
    FIELD alkoholgrad  LIKE l-artikel.alkoholgrad.

DEF INPUT  PARAMETER icase AS INT.
DEF INPUT  PARAMETER a-artnr AS INT.
DEF INPUT  PARAMETER a-bezeich AS CHAR.
DEF OUTPUT PARAMETER TABLE FOR temp-l-artikel.

IF icase = 1 THEN
FOR EACH l-artikel WHERE l-artikel.artnr GE a-artnr NO-LOCK:
    RUN create-temp-l-artikel.
END.
ELSE IF icase = 2 THEN
FOR EACH l-artikel WHERE l-artikel.bezeich matches a-bezeich NO-LOCK:
    RUN create-temp-l-artikel.
END.
ELSE IF icase = 3 THEN
FOR EACH l-artikel WHERE l-artikel.bezeich GE a-bezeich NO-LOCK:
    RUN create-temp-l-artikel.
END.

PROCEDURE create-temp-l-artikel:
    CREATE temp-l-artikel.
    ASSIGN
        temp-l-artikel.fibukonto    = l-artikel.fibukonto
        temp-l-artikel.bezeich      = l-artikel.bezeich
        temp-l-artikel.ek-aktuell   = l-artikel.ek-aktuell
        temp-l-artikel.artnr        = l-artikel.artnr
        temp-l-artikel.traubensort  = l-artikel.traubensort
        temp-l-artikel.lief-einheit = l-artikel.lief-einheit
        temp-l-artikel.masseinheit  = l-artikel.masseinheit
        temp-l-artikel.betriebsnr   = l-artikel.betriebsnr
        temp-l-artikel.alkoholgrad  = l-artikel.alkoholgrad.
END.
