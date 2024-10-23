DEF INPUT PARAMETER s-artnr      AS INT.
DEF OUTPUT PARAMETER description AS CHAR.
DEF OUTPUT PARAMETER bezeich     AS CHAR.
DEF OUTPUT PARAMETER l-artikel-artnr AS INT.

FIND FIRST l-artikel WHERE l-artikel.artnr = s-artnr NO-LOCK. 
description = l-artikel.bezeich + " - " + l-artikel.masseinheit.
bezeich = l-artikel.bezeich.
l-artikel-artnr = l-artikel.artnr.
