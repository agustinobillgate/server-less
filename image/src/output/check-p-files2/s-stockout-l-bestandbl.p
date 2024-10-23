
DEF INPUT PARAMETER curr-lager AS INT.
DEF INPUT PARAMETER s-artnr AS INT.
DEF OUTPUT PARAMETER stock-oh AS DECIMAL.
DEF OUTPUT PARAMETER avail-l-bestand AS LOGICAL INIT NO.

FIND FIRST l-bestand WHERE l-bestand.lager-nr = curr-lager
    AND l-bestand.artnr = s-artnr NO-LOCK NO-ERROR. 
IF AVAILABLE l-bestand THEN 
DO:
    avail-l-bestand = YES.
    stock-oh = l-bestand.anz-anf-best + l-bestand.anz-eingang 
          - l-bestand.anz-ausgang. 
END.
