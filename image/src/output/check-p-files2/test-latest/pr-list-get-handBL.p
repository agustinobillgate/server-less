DEFINE INPUT PARAMETER artnr AS INTEGER.
DEFINE OUTPUT PARAMETER soh AS DECIMAL.

FIND FIRST l-bestand WHERE l-bestand.artnr = artnr NO-LOCK NO-ERROR.
IF AVAILABLE l-bestand THEN
DO:
    ASSIGN soh = l-bestand.anz-anf-best + l-bestand.anz-eingang - l-bestand.anz-ausgang.
END.
    

