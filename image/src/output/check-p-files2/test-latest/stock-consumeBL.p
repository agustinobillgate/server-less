DEFINE TEMP-TABLE consume-list
    FIELD artnr         LIKE l-verbrauch.artnr 
    FIELD datum         LIKE l-verbrauch.datum 
    FIELD anz-verbrau   LIKE l-verbrauch.anz-verbrau 
    FIELD wert-verbrau  LIKE l-verbrauch.wert-verbrau.

DEFINE INPUT PARAMETER s-artnr      AS INTEGER  NO-UNDO.
DEFINE INPUT PARAMETER from-date    AS DATE     NO-UNDO.
DEFINE INPUT PARAMETER to-date      AS DATE     NO-UNDO.
DEFINE OUTPUT PARAMETER qty         AS DECIMAL  NO-UNDO.
DEFINE OUTPUT PARAMETER val         AS DECIMAL  NO-UNDO.
DEFINE OUTPUT PARAMETER TABLE FOR consume-list.

IF from-date = ? THEN
DO:
    FOR EACH l-verbrauch WHERE l-verbrauch.artnr = s-artnr NO-LOCK: 
        /* Rulita 181024 | Fixing for serverless */
        /* qty = qty + anz-verbrau. 
        val = val + wert-verbrau. */
        qty = qty + l-verbrauch.anz-verbrau.                                
        val = val + l-verbrauch.wert-verbrau. 
    END. 

    FOR EACH l-verbrauch WHERE l-verbrauch.artnr = s-artnr NO-LOCK 
        BY l-verbrauch.datum.
        CREATE consume-list.
        BUFFER-COPY l-verbrauch TO consume-list.
    END.
END.
ELSE
DO:
    FOR EACH l-verbrauch WHERE l-verbrauch.artnr = s-artnr 
        AND l-verbrauch.datum GE from-date
        AND l-verbrauch.datum LE to-date NO-LOCK: 
        qty = qty + anz-verbrau. 
        val = val + wert-verbrau. 
    END. 
    FOR EACH l-verbrauch WHERE l-verbrauch.artnr = s-artnr 
        AND l-verbrauch.datum GE from-date
        AND l-verbrauch.datum LE to-date NO-LOCK BY l-verbrauch.datum:
        CREATE consume-list.
        BUFFER-COPY l-verbrauch TO consume-list.
    END.
END.
