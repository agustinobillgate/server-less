
DEF INPUT PARAMETER s-artnr AS INT.
DEF INPUT PARAMETER curr-lager AS INT.
DEF OUTPUT PARAMETER stock-oh AS DECIMAL.
DEF OUTPUT PARAMETER description AS CHAR.

FIND FIRST l-art WHERE l-art.artnr = s-artnr NO-LOCK. 
DO: 
    FIND FIRST l-bestand WHERE l-bestand.lager-nr = curr-lager
      AND l-bestand.artnr = s-artnr NO-LOCK NO-ERROR. 
    IF AVAILABLE l-bestand THEN 
      stock-oh = l-bestand.anz-anf-best + l-bestand.anz-eingang 
        - l-bestand.anz-ausgang. 
    ELSE stock-oh = 0. 
    ASSIGN
      description = TRIM(l-art.bezeich) + " - " 
                  + STRING(l-art.masseinheit,"x(3)"). 
END. 
