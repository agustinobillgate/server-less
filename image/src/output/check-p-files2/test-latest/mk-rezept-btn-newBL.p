
DEF INPUT  PARAMETER case-type AS INT.
DEF INPUT  PARAMETER h-artnr   AS INT.
DEF OUTPUT PARAMETER katnr     AS INT.

IF case-type = 1 THEN   /*new-katnr*/
FOR EACH h-rezept NO-LOCK: 
    IF h-rezept.kategorie GT katnr THEN katnr = h-rezept.kategorie. 
END. 
ELSE IF case-type = 2 THEN  /*new-recipe*/
FOR EACH h-rezept NO-LOCK: 
    IF h-rezept.artnrrezept GT h-artnr THEN katnr = h-rezept.artnrrezept. 
END. 
