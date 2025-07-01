DEFINE TEMP-TABLE temp-l-artikel
    FIELD artnr         LIKE l-artikel.artnr
    FIELD bezeich       LIKE l-artikel.bezeich
    FIELD betriebsnr    LIKE l-artikel.betriebsnr
    FIELD endkum        LIKE l-artikel.endkum
    FIELD masseinheit   LIKE l-artikel.masseinheit
    FIELD vk-preis      LIKE l-artikel.vk-preis
    FIELD inhalt        LIKE l-artikel.inhalt
    FIELD lief-einheit  LIKE l-artikel.lief-einheit
    FIELD traubensort   LIKE l-artikel.traubensort.

DEF INPUT  PARAMETER s-artnr         AS INT.
DEF INPUT  PARAMETER curr-lager      AS INT.
DEF OUTPUT PARAMETER t-stock-oh      AS DECIMAL.
DEF OUTPUT PARAMETER avail-l-bestand AS LOGICAL.
DEF OUTPUT PARAMETER TABLE FOR temp-l-artikel.

FIND FIRST l-artikel WHERE l-artikel.artnr = s-artnr NO-ERROR.
CREATE temp-l-artikel.
ASSIGN
    temp-l-artikel.artnr         = l-artikel.artnr
    temp-l-artikel.bezeich       = l-artikel.bezeich
    temp-l-artikel.betriebsnr    = l-artikel.betriebsnr
    temp-l-artikel.endkum        = l-artikel.endkum
    temp-l-artikel.masseinheit   = l-artikel.masseinheit
    temp-l-artikel.vk-preis      = l-artikel.vk-preis
    temp-l-artikel.inhalt        = l-artikel.inhalt
    temp-l-artikel.lief-einheit  = l-artikel.lief-einheit
    temp-l-artikel.traubensort   = l-artikel.traubensort.


RUN s-stockout-l-bestandbl.p
    (curr-lager, s-artnr, OUTPUT t-stock-oh, OUTPUT avail-l-bestand).
