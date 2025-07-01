DEFINE TEMP-TABLE dml-list 
  FIELD bezeich     AS CHAR FORMAT "x(36)" COLUMN-LABEL "Description"
  FIELD anzahl      LIKE dml-art.anzahl
  FIELD geliefert   LIKE dml-art.geliefert
  FIELD einzelpreis LIKE dml-art.einzelpreis FORMAT ">,>>>,>>>,>>9.99"
  FIELD artnr       LIKE l-artikel.artnr COLUMN-LABEL "ArtNo"
  FIELD departement LIKE dml-artdep.departement
  FIELD lief-nr     AS INTEGER
  FIELD supplier    AS CHAR FORMAT "x(24)" COLUMN-LABEL "Supplier"
.

DEF TEMP-TABLE t-hoteldpt LIKE hoteldpt.
DEF TEMP-TABLE t-l-lager  LIKE l-lager.
DEF TEMP-TABLE t-bediener LIKE bediener.

DEF INPUT PARAMETER curr-dept AS INT.

DEF OUTPUT PARAMETER price-decimal AS INT.
DEF OUTPUT PARAMETER f-endkum AS INT.
DEF OUTPUT PARAMETER b-endkum AS INT.
DEF OUTPUT PARAMETER m-endkum AS INT.
DEF OUTPUT PARAMETER billdate AS DATE.
DEF OUTPUT PARAMETER fb-closedate AS DATE.
DEF OUTPUT PARAMETER m-closedate AS DATE.
DEF OUTPUT PARAMETER over-proz AS DECIMAL.
DEF OUTPUT PARAMETER flag-error AS LOGICAL INIT NO.
DEF OUTPUT PARAMETER p-232 AS LOGICAL.
DEF OUTPUT PARAMETER TABLE FOR dml-list.
DEF OUTPUT PARAMETER TABLE FOR t-hoteldpt.
DEF OUTPUT PARAMETER TABLE FOR t-l-lager.
DEF OUTPUT PARAMETER TABLE FOR t-bediener.

RUN htplogic.p (232, OUTPUT p-232).
FIND FIRST htparam WHERE htparam.paramnr = 491. 
price-decimal = htparam.finteger.   /* non-digit OR digit version */ 
 
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
 
FIND FIRST htparam WHERE paramnr = 403 NO-LOCK. 
over-proz = htparam.fdecimal / 100. 

FIND FIRST htparam WHERE htparam.paramnr = 269 NO-LOCK. 
IF htparam.fdate NE ? AND billdate LE htparam.fdate THEN 
DO: 
    flag-error = YES.
    RETURN.
END. 

RUN dml-stockin-create-dml-listbl.p
    (curr-dept, billdate, OUTPUT TABLE dml-list).

FOR EACH hoteldpt:
    CREATE t-hoteldpt.
    BUFFER-COPY hoteldpt TO t-hoteldpt.
END.

FOR EACH l-lager:
    CREATE t-l-lager.
    BUFFER-COPY l-lager TO t-l-lager.
END.

FOR EACH bediener:
    CREATE t-bediener.
    BUFFER-COPY bediener TO t-bediener.
END.
