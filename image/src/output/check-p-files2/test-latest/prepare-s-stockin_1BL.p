DEF TEMP-TABLE t-l-lager LIKE l-lager.
DEF TEMP-TABLE temp-bediener LIKE bediener.

DEF OUTPUT PARAMETER f-endkum       AS INT.
DEF OUTPUT PARAMETER b-endkum       AS INT.
DEF OUTPUT PARAMETER m-endkum       AS INT.
DEF OUTPUT PARAMETER billdate       AS DATE.
DEF OUTPUT PARAMETER fb-closedate   AS DATE.
DEF OUTPUT PARAMETER m-closedate    AS DATE.
DEF OUTPUT PARAMETER last-mdate     AS DATE.
DEF OUTPUT PARAMETER last-fbdate    AS DATE.
DEF OUTPUT PARAMETER fl-code1       AS INT INIT 0.
DEF OUTPUT PARAMETER fl-code2       AS INT INIT 0.
DEF OUTPUT PARAMETER ci-date        AS DATE. /*gerald 030820*/
DEF OUTPUT PARAMETER TABLE FOR t-l-lager.
DEF OUTPUT PARAMETER TABLE FOR temp-bediener.

FIND FIRST htparam WHERE paramnr = 257 NO-LOCK. 
f-endkum = htparam.finteger.               /* Rulita 211024 | Fixing for serverless */  
FIND FIRST htparam WHERE paramnr = 258 NO-LOCK. 
b-endkum = htparam.finteger.               /* Rulita 211024 | Fixing for serverless */  
FIND FIRST htparam WHERE paramnr = 268 NO-LOCK. 
m-endkum = htparam.finteger.               /* Rulita 211024 | Fixing for serverless */  
 
FIND FIRST htparam WHERE paramnr = 474 NO-LOCK. 
billdate = htparam.fdate. 
FIND FIRST htparam WHERE paramnr = 224 NO-LOCK. 
fb-closedate = htparam.fdate. 
FIND FIRST htparam WHERE paramnr = 221 NO-LOCK. 
m-closedate = htparam.fdate. 

FIND FIRST htparam WHERE htparam.paramnr = 87 NO-LOCK NO-ERROR.
ci-date = htparam.fdate.
 
IF billdate = ? OR billdate GT today THEN billdate = today. 
ELSE 
DO: 
  IF m-closedate NE ? THEN last-mdate = DATE(month(m-closedate), 
    1, year(m-closedate)) - 1. 
  IF fb-closedate NE ? THEN last-fbdate = DATE(month(fb-closedate), 
    1, year(fb-closedate)) - 1. 
  IF (billdate LE last-mdate) OR (billdate LE last-fbdate) THEN 
  DO:
    fl-code1 = 1.
  END. 
  FIND FIRST htparam WHERE htparam.paramnr = 269 NO-LOCK. 
  IF htparam.fdate NE ? AND billdate LE htparam.fdate THEN 
  DO:
    fl-code2 = 1.
    RETURN.
  END. 
END. 


FOR EACH l-lager:
    CREATE t-l-lager.
    BUFFER-COPY l-lager TO t-l-lager.
END.

FOR EACH bediener:
    CREATE temp-bediener.
    BUFFER-COPY bediener TO temp-bediener.
END.
