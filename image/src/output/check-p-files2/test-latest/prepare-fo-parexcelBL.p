DEFINE TEMP-TABLE batch-list 
  FIELD briefnr AS INTEGER 
  FIELD fname   AS CHAR. 

DEFINE TEMP-TABLE htv-list 
  FIELD paramnr AS INTEGER 
  FIELD fchar   AS CHAR. 

DEFINE TEMP-TABLE htp-list 
  FIELD paramnr AS INTEGER 
  FIELD fchar   AS CHAR. 

DEFINE TEMP-TABLE brief-list 
  FIELD b-text AS CHAR. 

DEFINE INPUT PARAMETER briefnr      AS INTEGER. 
DEF OUTPUT PARAMETER serv-vat       AS LOGICAL.
DEF OUTPUT PARAMETER foreign-nr     AS INTEGER.
DEF OUTPUT PARAMETER start-date     AS DATE.
DEF OUTPUT PARAMETER price-decimal  AS INTEGER.
DEF OUTPUT PARAMETER no-decimal     AS LOGICAL.
DEF OUTPUT PARAMETER outfile-dir    AS CHAR.
DEF OUTPUT PARAMETER keycmd         AS CHAR.
DEF OUTPUT PARAMETER keyvar         AS CHAR.
DEF OUTPUT PARAMETER TABLE FOR batch-list.
DEF OUTPUT PARAMETER TABLE FOR htv-list.
DEF OUTPUT PARAMETER TABLE FOR htp-list.
DEF OUTPUT PARAMETER TABLE FOR brief-list.


FIND FIRST htparam WHERE htparam.paramnr = 479 NO-LOCK. 
serv-vat = htparam.flogical. 
 
FIND FIRST htparam WHERE htparam.paramnr = 144 NO-LOCK. 
IF htparam.fchar NE "" THEN 
DO: 
  FIND FIRST waehrung WHERE waehrung.wabkurz = htparam.fchar NO-LOCK NO-ERROR. 
  IF AVAILABLE waehrung THEN foreign-nr = waehrung.waehrungsnr. 
END. 
 
FIND FIRST htparam WHERE paramnr = 186 NO-LOCK. 
IF htparam.feldtyp = 3 AND htparam.fdate NE ? THEN start-date = htparam.fdate. 



FIND FIRST htparam WHERE htparam.paramnr = 491 NO-LOCK. 
price-decimal = htparam.finteger. 
no-decimal = (price-decimal = 0). 

RUN fill-list.

create batch-list. 
FIND FIRST brief WHERE brief.briefnr = briefnr NO-LOCK. 
batch-list.briefnr = briefnr. 
batch-list.fname = brief.fname. 


FIND FIRST htparam WHERE htparam.paramnr = 64 NO-LOCK.
outfile-dir = htparam.fchar.
IF outfile-dir NE "" AND SUBSTR(outfile-dir, LENGTH(outfile-dir), 1)
    NE "\" THEN outfile-dir = outfile-dir + "\".


PROCEDURE fill-list: 
DEFINE VARIABLE i AS INTEGER.
DEFINE VARIABLE j AS INTEGER.
DEFINE VARIABLE n AS INTEGER.
DEFINE VARIABLE c AS CHAR.
DEFINE VARIABLE l AS INTEGER.
DEFINE VARIABLE continued AS LOGICAL INITIAL NO.
 
  FIND FIRST htparam WHERE paramnr = 600 NO-LOCK.
  keycmd = htparam.fchar.
  FIND FIRST htparam WHERE paramnr = 2030 NO-LOCK.
  keyvar = htparam.fchar.
 
  FOR EACH htparam WHERE paramgruppe = 8 AND htpara.fchar NE "" NO-LOCK 
    BY length(htparam.fchar) descending: 
    IF SUBSTR(htparam.fchar,1 ,1) = "." THEN 
    DO: 
      create htv-list.
      htv-list.paramnr = htparam.paramnr.
      htv-list.fchar = htparam.fchar.
    END.
    ELSE 
    DO: 
      create htp-list.
      htp-list.paramnr = htparam.paramnr.
      htp-list.fchar = keycmd + htparam.fchar.
    END. 
  END. 
 
  CREATE htv-list.
  ASSIGN
      htv-list.paramnr = 9199
      htv-list.fchar   = ".yesterday".

  CREATE htv-list.
  ASSIGN
      htv-list.paramnr = 9198
      htv-list.fchar   = ".lm-today".

  CREATE htv-list.
  ASSIGN
      htv-list.paramnr = 9197
      htv-list.fchar   = ".ny-budget".
  CREATE htv-list.
  ASSIGN
      htv-list.paramnr = 9196
      htv-list.fchar   = ".nmtd-budget".
  CREATE htv-list.
  ASSIGN
      htv-list.paramnr = 9195
      htv-list.fchar   = ".nytd-budget".

  CREATE htv-list.
  ASSIGN
      htv-list.paramnr = 9194
      htv-list.fchar   = ".today-serv".

  CREATE htv-list.
  ASSIGN
      htv-list.paramnr = 9193
      htv-list.fchar   = ".today-tax".

  CREATE htv-list.
  ASSIGN
      htv-list.paramnr = 9192
      htv-list.fchar   = ".mtd-serv".

  CREATE htv-list.
  ASSIGN
      htv-list.paramnr = 9191
      htv-list.fchar   = ".mtd-tax".

  CREATE htv-list.
  ASSIGN
      htv-list.paramnr = 9190
      htv-list.fchar   = ".ytd-serv".

  CREATE htv-list.
  ASSIGN
      htv-list.paramnr = 9189
      htv-list.fchar   = ".ytd-tax".

  CREATE htv-list.
  ASSIGN
      htv-list.paramnr = 9188
      htv-list.fchar   = ".lmtoday-serv".

  CREATE htv-list.
  ASSIGN
      htv-list.paramnr = 9187
      htv-list.fchar   = ".lmtoday-tax".

  CREATE htv-list.
  ASSIGN
      htv-list.paramnr = 9186
      htv-list.fchar   = ".pmtd-serv".

  CREATE htv-list.
  ASSIGN
      htv-list.paramnr = 9185
      htv-list.fchar   = ".pmtd-tax".
  
  CREATE htv-list.
  ASSIGN
      htv-list.paramnr = 9184
      htv-list.fchar   = ".lmtd-serv".

  CREATE htv-list.
  ASSIGN
      htv-list.paramnr = 9183
      htv-list.fchar   = ".lmtd-tax".

  CREATE htv-list.
  ASSIGN
      htv-list.paramnr = 9182
      htv-list.fchar   = ".lm-mtd".

  CREATE htp-list.
  ASSIGN
      htp-list.paramnr = 8092
      htp-list.fchar   = keycmd + "NatRev".
  CREATE htp-list.
  ASSIGN
      htp-list.paramnr = 8813
      htp-list.fchar   = keycmd + "NatRoom".
  CREATE htp-list.
  ASSIGN
      htp-list.paramnr = 8814
      htp-list.fchar   = keycmd + "NatPers".

  CREATE htp-list.
  ASSIGN
      htp-list.paramnr = 9981
      htp-list.fchar   = keycmd + "CompSaleRm".
  CREATE htp-list.
  ASSIGN
      htp-list.paramnr = 9982
      htp-list.fchar   = keycmd + "CompOccRm".
  CREATE htp-list.
  ASSIGN
      htp-list.paramnr = 9983
      htp-list.fchar   = keycmd + "CompCompliRm".
  CREATE htp-list.
  ASSIGN
      htp-list.paramnr = 9984
      htp-list.fchar   = keycmd + "CompRmRev".

  CREATE htp-list.
  ASSIGN
      htp-list.paramnr = 9985
      htp-list.fchar   = keycmd + "SgFbSales".

  CREATE htp-list.
  ASSIGN
      htp-list.paramnr = 9986
      htp-list.fchar   = keycmd + "SgFbQty".

  CREATE htp-list.
  ASSIGN
      htp-list.paramnr = 1995
      htp-list.fchar   = keycmd + "FP-Cover".

  CREATE htp-list.
  ASSIGN
      htp-list.paramnr = 1996
      htp-list.fchar   = keycmd + "BP-Cover".

  CREATE htp-list.
  ASSIGN
      htp-list.paramnr = 1997
      htp-list.fchar   = keycmd + "f-fbstat".

  CREATE htp-list.
  ASSIGN
      htp-list.paramnr = 1998
      htp-list.fchar   = keycmd + "b-fbstat".

  CREATE htp-list.
  ASSIGN
      htp-list.paramnr = 1999
      htp-list.fchar   = keycmd + "o-fbstat".

  CREATE htp-list.
  ASSIGN
      htp-list.paramnr = 9106
      htp-list.fchar   = keycmd + "WIG".

  /*******************************************/
  CREATE htp-list.
  ASSIGN
      htp-list.paramnr = 9092
      htp-list.fchar   = keycmd + "SourceRev".
  CREATE htp-list.
  ASSIGN
      htp-list.paramnr = 9813
      htp-list.fchar   = keycmd + "SourceRoom".
  CREATE htp-list.
  ASSIGN
      htp-list.paramnr = 9814
      htp-list.fchar   = keycmd + "SourcePers".
  CREATE htp-list.
  ASSIGN
      htp-list.paramnr = 7194
      htp-list.fchar   = keycmd + "Canc-night".

  CREATE htp-list.
  ASSIGN
      htp-list.paramnr = 9188
      htp-list.fchar   = keycmd + "Child-arr".

  CREATE htp-list.
  ASSIGN
      htp-list.paramnr = 9190
      htp-list.fchar   = keycmd + "Child-dep".

  CREATE htp-list.
  ASSIGN
      htp-list.paramnr = 1921
      htp-list.fchar   = keycmd + "F-Cover1".

  CREATE htp-list.
  ASSIGN
      htp-list.paramnr = 1922
      htp-list.fchar   = keycmd + "F-Cover2".

  CREATE htp-list.
  ASSIGN
      htp-list.paramnr = 1923
      htp-list.fchar   = keycmd + "F-Cover3".

  CREATE htp-list.
  ASSIGN
      htp-list.paramnr = 1924
      htp-list.fchar   = keycmd + "F-Cover4".

  CREATE htp-list.
  ASSIGN
      htp-list.paramnr = 1971
      htp-list.fchar   = keycmd + "B-Cover1".

  CREATE htp-list.
  ASSIGN
      htp-list.paramnr = 1972
      htp-list.fchar   = keycmd + "B-Cover2".

  CREATE htp-list.
  ASSIGN
      htp-list.paramnr = 1973
      htp-list.fchar   = keycmd + "B-Cover3".

  CREATE htp-list.
  ASSIGN
      htp-list.paramnr = 1974
      htp-list.fchar   = keycmd + "B-Cover4".

  CREATE htp-list.
  ASSIGN
      htp-list.paramnr = 1991
      htp-list.fchar   = keycmd + "P-Cover1".

  CREATE htp-list.
  ASSIGN
      htp-list.paramnr = 1992
      htp-list.fchar   = keycmd + "P-Cover2".

  CREATE htp-list.
  ASSIGN
      htp-list.paramnr = 1993
      htp-list.fchar   = keycmd + "P-Cover3".

  CREATE htp-list.
  ASSIGN
      htp-list.paramnr = 1994
      htp-list.fchar   = keycmd + "P-Cover4".

  CREATE htp-list.
  ASSIGN
      htp-list.paramnr = 9000
      htp-list.fchar   = keycmd + "LOS".

  DO n = 1 TO 31:
    CREATE htv-list. 
    ASSIGN
      htv-list.paramnr = 3000 + n
      htv-list.fchar   = ".D" + STRING(n,"99")
    . 
  END.

  FOR EACH briefzei WHERE briefzei.briefnr = briefnr 
    NO-LOCK BY briefzei.briefzeilnr: 
    j = 1. 
    DO i = 1 TO length(briefzei.texte): 
       IF asc(SUBSTR(briefzei.texte, i , 1)) EQ 10 THEN 
       DO: 
         n = i - j. 
         c = SUBSTR(briefzei.texte, j,  n). 
         l = length(c). 
         IF NOT continued THEN create brief-list. 
         brief-list.b-text = brief-list.b-text + c. 
         j = i + 1. 
       END. 
    END. 
    n = length(briefzei.texte) - j + 1. 
    c = SUBSTR(briefzei.texte, j,  n). 
    IF NOT continued THEN create brief-list. 
    b-text = b-text + c. 
  END. 
END. 
