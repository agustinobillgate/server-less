
DEF INPUT  PARAMETER s-artnr        AS INT.
DEF INPUT  PARAMETER curr-lager     AS INT.
DEF OUTPUT PARAMETER description    AS CHAR.
DEF OUTPUT PARAMETER stock-oh       AS DECIMAL.
DEF OUTPUT PARAMETER price          AS DECIMAL.

FIND FIRST l-artikel WHERE l-artikel.artnr = s-artnr NO-LOCK. 
FIND FIRST l-bestand WHERE l-bestand.lager-nr = curr-lager 
    AND l-bestand.artnr = s-artnr NO-LOCK NO-ERROR. 
description = l-artikel.bezeich + " - " + l-artikel.masseinheit. 
IF AVAILABLE l-bestand THEN 
    stock-oh = l-bestand.anz-anf-best + l-bestand.anz-eingang 
             - l-bestand.anz-ausgang. 
ELSE stock-oh = 0. 

price = l-artikel.vk-preis. 
