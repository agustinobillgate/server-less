
DEF TEMP-TABLE t-l-artikel  
    FIELD artnr         LIKE l-artikel.artnr  
    FIELD bezeich       LIKE l-artikel.bezeich  
    FIELD ek-aktuell    LIKE l-artikel.ek-aktuell  
    FIELD t-description AS CHAR  
    FIELD lief-einheit  LIKE l-artikel.lief-einheit  
    FIELD betriebsnr    LIKE l-artikel.betriebsnr  
    FIELD vk-preis      LIKE l-artikel.vk-preis  
    FIELD alkoholgrad   LIKE l-artikel.alkoholgrad  
    FIELD rec-id        AS INT.  

DEF INPUT  PARAMETER icase AS INT.
DEF INPUT  PARAMETER a-artnr AS INT.
DEF INPUT  PARAMETER a-bezeich AS CHAR.
DEF OUTPUT PARAMETER TABLE FOR t-l-artikel.

IF icase = 1 THEN
FOR EACH l-artikel WHERE l-artikel.artnr GE a-artnr NO-LOCK :
    RUN create-t-l-artikel.
END.
ELSE IF icase = 2 THEN
FOR EACH l-artikel WHERE l-artikel.bezeich matches a-bezeich NO-LOCK :
    RUN create-t-l-artikel.
END.
ELSE IF icase = 3 THEN
FOR EACH l-artikel WHERE l-artikel.bezeich GE a-bezeich NO-LOCK :
    RUN create-t-l-artikel.
END.

PROCEDURE create-t-l-artikel:
    CREATE t-l-artikel.
    ASSIGN
        t-l-artikel.artnr         = l-artikel.artnr
        t-l-artikel.bezeich       = l-artikel.bezeich
        t-l-artikel.ek-aktuell    = l-artikel.ek-aktuell
        t-l-artikel.t-description = TRIM(l-artikel.bezeich) + " - " 
                                    + l-artikel.traubensort + " [" 
                                    + STRING(l-artikel.lief-einheit) + " "
                                    + l-artikel.masseinheit + "]"
        t-l-artikel.lief-einheit  = l-artikel.lief-einheit
        t-l-artikel.betriebsnr    = l-artikel.betriebsnr
        t-l-artikel.vk-preis      = l-artikel.vk-preis
        t-l-artikel.alkoholgrad   = l-artikel.alkoholgrad
        t-l-artikel.rec-id        = RECID(l-artikel).
END.
