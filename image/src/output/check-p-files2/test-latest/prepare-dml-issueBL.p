DEFINE TEMP-TABLE t-l-artikel   LIKE l-artikel.
DEFINE TEMP-TABLE t-l-lager LIKE l-lager.
DEFINE TEMP-TABLE t-hoteldpt LIKE hoteldpt.

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

DEF INPUT  PARAMETER curr-dept AS INT.

DEF OUTPUT PARAMETER mat-grp        AS INT.
DEF OUTPUT PARAMETER price-decimal  AS INT.
DEF OUTPUT PARAMETER billdate       AS DATE.
DEF OUTPUT PARAMETER closedate      AS DATE.
DEF OUTPUT PARAMETER over-proz      AS DECIMAL INIT 0.
DEF OUTPUT PARAMETER err-code       AS INT INIT 0.
DEF OUTPUT PARAMETER p-232          AS LOGICAL.
DEF OUTPUT PARAMETER TABLE FOR t-l-lager.
DEF OUTPUT PARAMETER TABLE FOR t-hoteldpt.
DEF OUTPUT PARAMETER TABLE FOR dml-list.
DEF OUTPUT PARAMETER TABLE FOR t-l-artikel.

RUN htplogic.p (232, OUTPUT p-232).
FIND FIRST htparam WHERE htparam.paramnr = 268 NO-LOCK. 
mat-grp = htparam.finteger. 
 
FIND FIRST htparam WHERE htparam.paramnr = 491. 
price-decimal = htparam.finteger.   /* non-digit OR digit version */ 
 
FIND FIRST htparam WHERE paramnr = 474 NO-LOCK. 
billdate = htparam.fdate. 
FIND FIRST htparam WHERE paramnr = 224 NO-LOCK. 
closedate = htparam.fdate. 
 
FIND FIRST htparam WHERE htparam.paramnr = 269 NO-LOCK. 
IF htparam.fdate NE ? AND billdate LE htparam.fdate THEN 
DO: 
    err-code = 1.
    RETURN.
END. 

FIND FIRST htparam WHERE paramnr = 403 NO-LOCK. 
over-proz = htparam.fdecimal / 100. 

FOR EACH l-lager:
    CREATE t-l-lager.
    BUFFER-COPY l-lager TO t-l-lager.
END.

FOR EACH hoteldpt:
    CREATE t-hoteldpt.
    BUFFER-COPY hoteldpt TO t-hoteldpt.
END.

RUN dml-issue-create-dml-listbl.p
    (curr-dept, billdate, OUTPUT TABLE dml-list, OUTPUT TABLE t-l-artikel).
