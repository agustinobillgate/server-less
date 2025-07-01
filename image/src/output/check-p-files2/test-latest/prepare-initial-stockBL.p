DEF TEMP-TABLE temp-l-artikel
    FIELD artnr       LIKE l-artikel.artnr
    FIELD bezeich     LIKE l-artikel.bezeich
    FIELD ek-aktuell  LIKE l-artikel.ek-aktuell
    FIELD masseinheit LIKE l-artikel.masseinheit
    FIELD inhalt      LIKE l-artikel.inhalt.

DEF TEMP-TABLE t-l-lager LIKE l-lager.

DEF OUTPUT PARAMETER m-endkum AS INT.
DEF OUTPUT PARAMETER fb-date AS DATE.
DEF OUTPUT PARAMETER m-date AS DATE.
DEF OUTPUT PARAMETER TABLE FOR t-l-lager.
DEF OUTPUT PARAMETER TABLE FOR temp-l-artikel.

FIND FIRST htparam WHERE paramnr = 268 NO-LOCK. 
m-endkum = htparam.finteger.         /* Rulita 211024 | Fixing for serverless */
 
FIND FIRST htparam WHERE paramnr = 224 NO-LOCK. 
fb-date = htparam.fdate.         /* Rulita 211024 | Fixing for serverless */
fb-date = DATE(month(fb-date), 1, year(fb-date)). 
 
FIND FIRST htparam WHERE paramnr = 221 NO-LOCK. 
m-date = htparam.fdate.         /* Rulita 211024 | Fixing for serverless */
m-date = DATE(month(m-date), 1, year(m-date)). 

FOR EACH l-artikel:
    CREATE temp-l-artikel.
    ASSIGN
    temp-l-artikel.artnr       = l-artikel.artnr
    temp-l-artikel.bezeich     = l-artikel.bezeich
    temp-l-artikel.ek-aktuell  = l-artikel.ek-aktuell
    temp-l-artikel.masseinheit = l-artikel.masseinheit
    temp-l-artikel.inhalt      = l-artikel.inhalt.
END.

FOR EACH l-lager:
    CREATE t-l-lager.
    BUFFER-COPY l-lager TO t-l-lager.
END.
