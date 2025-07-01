
DEF INPUT PARAMETER curr-lager AS INT.
DEF INPUT PARAMETER s-artnr AS INT.
DEF OUTPUT PARAMETER stock-oh AS DECIMAL INIT 0.
DEF OUTPUT PARAMETER description AS CHAR.
DEF OUTPUT PARAMETER price AS DECIMAL.
DEF OUTPUT PARAMETER l-artikel-artnr AS INT.

FIND FIRST l-artikel WHERE l-artikel.artnr = s-artnr NO-LOCK. 
FIND FIRST l-bestand WHERE l-bestand.lager-nr = curr-lager 
    AND l-bestand.artnr = s-artnr NO-LOCK NO-ERROR.
IF AVAILABLE l-bestand THEN
stock-oh = l-bestand.anz-anf-best + l-bestand.anz-eingang - l-bestand.anz-ausgang.
description = l-artikel.bezeich + " - " + l-artikel.masseinheit. 
price = l-artikel.vk-preis. 
l-artikel-artnr = l-artikel.artnr.
