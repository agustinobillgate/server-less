
DEFINE TEMP-TABLE htv-list 
  FIELD paramnr AS INTEGER 
  FIELD fchar   AS CHAR
  INDEX idx1 fchar.

DEFINE TEMP-TABLE htp-list 
  FIELD paramnr AS INTEGER 
  FIELD fchar   AS CHAR
  INDEX idx1 paramnr
  INDEX idx2 fchar.

DEFINE TEMP-TABLE brief-list 
  FIELD b-text AS CHAR. 

DEF TEMP-TABLE t-parameters LIKE parameters.

DEFINE TEMP-TABLE t-brief LIKE brief.

DEF INPUT  PARAMETER pvILanguage    AS INTEGER  NO-UNDO.
DEF INPUT  PARAMETER briefnr        AS INTEGER.
DEF OUTPUT PARAMETER xls-dir        AS CHAR INIT "" NO-UNDO.
DEF OUTPUT PARAMETER msg-str        AS CHAR.
DEF OUTPUT PARAMETER serv-vat       AS LOGICAL.
DEF OUTPUT PARAMETER foreign-nr     AS INTEGER.
DEF OUTPUT PARAMETER start-date     AS DATE.
DEF OUTPUT PARAMETER price-decimal  AS INTEGER.
DEF OUTPUT PARAMETER no-decimal     AS LOGICAL.
DEF OUTPUT PARAMETER keycmd         AS CHAR.
DEF OUTPUT PARAMETER keyvar         AS CHAR.
DEF OUTPUT PARAMETER outfile-dir    AS CHAR.
DEF OUTPUT PARAMETER anz0           AS INT.
DEF OUTPUT PARAMETER TABLE FOR htv-list.
DEF OUTPUT PARAMETER TABLE FOR htp-list.
DEF OUTPUT PARAMETER TABLE FOR brief-list.
DEF OUTPUT PARAMETER TABLE FOR t-brief.
DEF OUTPUT PARAMETER TABLE FOR t-parameters.


{supertransBL.i} 
DEF VAR lvCAREA AS CHAR INITIAL "prepare-fo-parxls".

FOR EACH parameters WHERE progname = "FO-macro"
  AND parameters.SECTION = STRING(briefnr) NO-LOCK:
  CREATE t-parameters.
  BUFFER-COPY parameters TO t-parameters.
END.


FIND FIRST htparam WHERE htparam.paramnr = 418 NO-LOCK.
IF htparam.fchar EQ "" THEN 
DO: 
  msg-str = msg-str + CHR(2)
          + translateExtended ("Excel Output Directory not defined (Param 418 Grp 15)",lvCAREA,"").
  RETURN.
END. 
xls-dir = htparam.fchar.


FIND FIRST htparam WHERE htparam.paramnr = 479 NO-LOCK. 
serv-vat = htparam.flogical. 

FIND FIRST htparam WHERE htparam.paramnr = 144 NO-LOCK. 
IF htparam.fchar NE "" THEN 
DO: 
  FIND FIRST waehrung WHERE waehrung.wabkurz = htparam.fchar NO-LOCK NO-ERROR. 
  IF AVAILABLE waehrung THEN foreign-nr = waehrung.waehrungsnr. 
END. 

FIND FIRST htparam WHERE htparam.paramnr = 186 NO-LOCK. 
IF htparam.feldtyp = 3 AND htparam.fdate NE ? THEN start-date = htparam.fdate.


FIND FIRST htparam WHERE htparam.paramnr = 491 NO-LOCK. 
price-decimal = htparam.finteger. 
no-decimal = (price-decimal = 0). 

RUN fill-list.

FIND FIRST brief WHERE brief.briefnr = briefnr NO-LOCK.
CREATE t-brief.
BUFFER-COPY brief TO t-brief.

FIND FIRST htparam WHERE htparam.paramnr = 64 NO-LOCK.
outfile-dir = htparam.fchar.

FOR EACH zimmer NO-LOCK: 
    anz0 = anz0 + 1. 
END.

PROCEDURE fill-list: 
DEFINE VARIABLE i           AS INTEGER. 
DEFINE VARIABLE j           AS INTEGER. 
DEFINE VARIABLE n           AS INTEGER. 
DEFINE VARIABLE l           AS INTEGER. 
DEFINE VARIABLE continued   AS LOGICAL INITIAL NO. 
DEFINE VARIABLE c           AS CHAR. 
DEFINE VARIABLE ct          AS CHAR.
 
  FIND FIRST htparam WHERE paramnr = 600 NO-LOCK. 
  keycmd = htparam.fchar. 
  FIND FIRST htparam WHERE paramnr = 2030 NO-LOCK. 
  keyvar = htparam.fchar. 
 
  FOR EACH htparam WHERE paramgruppe = 8 AND htparam.fchar NE "" NO-LOCK 
    BY LENGTH(htparam.fchar) descending: 
    IF SUBSTR(htparam.fchar,1 ,1) = "." THEN 
    DO: 
      CREATE htv-list. 
      htv-list.paramnr = htparam.paramnr. 
      htv-list.fchar = htparam.fchar. 
    END. 
    ELSE 
    DO: 
      CREATE htp-list. 
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
      htv-list.paramnr = 9200
      htv-list.fchar   = ".lytd-serv".

  CREATE htv-list.
  ASSIGN
      htv-list.paramnr = 9201
      htv-list.fchar   = ".lytd-tax".

  CREATE htv-list.
  ASSIGN
      htv-list.paramnr = 9202
      htv-list.fchar   = ".lytoday-serv".

  CREATE htv-list.
  ASSIGN
      htv-list.paramnr = 9203
      htv-list.fchar   = ".lytoday-tax".

  /*gerald awal - akhir bulan E9DE63*/
  CREATE htv-list.
  ASSIGN 
      htv-list.paramnr = 9204
      htv-list.fchar   = ".month-budget".

  /*gerald awal - akhir tahun E9DE63*/
  CREATE htv-list.
  ASSIGN 
      htv-list.paramnr = 9205
      htv-list.fchar   = ".year-budget".

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
      htp-list.paramnr = 2001
      htp-list.fchar   = keycmd + "PI-Cover1".

  CREATE htp-list.
  ASSIGN
      htp-list.paramnr = 2002
      htp-list.fchar   = keycmd + "PI-Cover2".

  CREATE htp-list.
  ASSIGN
      htp-list.paramnr = 2003
      htp-list.fchar   = keycmd + "PI-Cover3".

  CREATE htp-list.
  ASSIGN
      htp-list.paramnr = 2004
      htp-list.fchar   = keycmd + "PI-Cover4".

  CREATE htp-list.
  ASSIGN
      htp-list.paramnr = 2005
      htp-list.fchar   = keycmd + "PN-Cover1".

  CREATE htp-list.
  ASSIGN
      htp-list.paramnr = 2006
      htp-list.fchar   = keycmd + "PN-Cover2".

  CREATE htp-list.
  ASSIGN
      htp-list.paramnr = 2007
      htp-list.fchar   = keycmd + "PN-Cover3".

  CREATE htp-list.
  ASSIGN
      htp-list.paramnr = 2008
      htp-list.fchar   = keycmd + "PN-Cover4".

 CREATE htp-list.
 ASSIGN
     htp-list.paramnr = 2009
     htp-list.fchar   = keycmd + "PH-Cover1".

 CREATE htp-list.
 ASSIGN
     htp-list.paramnr = 2010
     htp-list.fchar   = keycmd + "PH-Cover2".

 CREATE htp-list.
 ASSIGN
     htp-list.paramnr = 2011
     htp-list.fchar   = keycmd + "PH-Cover3".

 CREATE htp-list.
 ASSIGN
     htp-list.paramnr = 2012
     htp-list.fchar   = keycmd + "PH-Cover4".

 CREATE htp-list.
 ASSIGN
     htp-list.paramnr = 2013
     htp-list.fchar   = keycmd + "PW-Cover1".

 CREATE htp-list.
 ASSIGN
     htp-list.paramnr = 2014
     htp-list.fchar   = keycmd + "PW-Cover2".

 CREATE htp-list.
 ASSIGN
     htp-list.paramnr = 2015
     htp-list.fchar   = keycmd + "PW-Cover3".

 CREATE htp-list.
 ASSIGN
     htp-list.paramnr = 2016
     htp-list.fchar   = keycmd + "PW-Cover4".

  /*Gerald Pax food by shift 4079F5*/
  CREATE htp-list.
  ASSIGN
      htp-list.paramnr = 2020
      htp-list.fchar   = keycmd + "FP-Cover1".

  CREATE htp-list.
  ASSIGN
      htp-list.paramnr = 2021
      htp-list.fchar   = keycmd + "FP-Cover2".

  CREATE htp-list.
  ASSIGN
      htp-list.paramnr = 2022
      htp-list.fchar   = keycmd + "FP-Cover3".

  CREATE htp-list.
  ASSIGN
      htp-list.paramnr = 2023
      htp-list.fchar   = keycmd + "FP-Cover4".
  /*end geral */

  /*Gerald Pax bev by shift 4079F5*/
  CREATE htp-list.
  ASSIGN
      htp-list.paramnr = 2024
      htp-list.fchar   = keycmd + "BP-Cover1".

  CREATE htp-list.
  ASSIGN
      htp-list.paramnr = 2025
      htp-list.fchar   = keycmd + "BP-Cover2".

  CREATE htp-list.
  ASSIGN
      htp-list.paramnr = 2026
      htp-list.fchar   = keycmd + "BP-Cover3".

  CREATE htp-list.
  ASSIGN
      htp-list.paramnr = 2027
      htp-list.fchar   = keycmd + "BP-Cover4".
  /*end geral*/

  /*geral G-total daily sales 0ADD87*/
  CREATE htp-list.
  ASSIGN
      htp-list.paramnr = 2028
      htp-list.fchar   = keycmd + "G-Cover".

  /*geral tot-bill & pax table daily sales 72AF1A*/
  CREATE htp-list.
  ASSIGN htp-list.paramnr = 2029
         htp-list.fchar   = keycmd + "TOT-BILL".

  CREATE htp-list.
  ASSIGN htp-list.paramnr = 2031
         htp-list.fchar   = keycmd + "PAX-TABLE".
  /*end gerald*/

  /*gerald Pax Compliment Inhouse , Pax Outsider, Compliment Outsider, Revenue Inhouse & Revenue Outsider E122F2*/
  CREATE htp-list.
  ASSIGN htp-list.paramnr = 2032
         htp-list.fchar   = keycmd + "PC-Cover1".

  CREATE htp-list.
  ASSIGN htp-list.paramnr = 2033
         htp-list.fchar   = keycmd + "PC-Cover2".

  CREATE htp-list.
  ASSIGN htp-list.paramnr = 2034
         htp-list.fchar   = keycmd + "PC-Cover3".

  CREATE htp-list.
  ASSIGN htp-list.paramnr = 2035
         htp-list.fchar   = keycmd + "PC-Cover4".

  CREATE htp-list.
  ASSIGN htp-list.paramnr = 2036
         htp-list.fchar   = keycmd + "PO-Cover1".

  CREATE htp-list.
  ASSIGN htp-list.paramnr = 2037
         htp-list.fchar   = keycmd + "PO-Cover2".

  CREATE htp-list.
  ASSIGN htp-list.paramnr = 2038
         htp-list.fchar   = keycmd + "PO-Cover3".

  CREATE htp-list.
  ASSIGN htp-list.paramnr = 2039
         htp-list.fchar   = keycmd + "PO-Cover4".

  CREATE htp-list.
  ASSIGN htp-list.paramnr = 2040
         htp-list.fchar   = keycmd + "PCO-Cover1".

  CREATE htp-list.
  ASSIGN htp-list.paramnr = 2041
         htp-list.fchar   = keycmd + "PCO-Cover2".

  CREATE htp-list.
  ASSIGN htp-list.paramnr = 2042
         htp-list.fchar   = keycmd + "PCO-Cover3".

  CREATE htp-list.
  ASSIGN htp-list.paramnr = 2043
         htp-list.fchar   = keycmd + "PCO-Cover4".

  CREATE htp-list.
  ASSIGN htp-list.paramnr = 2044
         htp-list.fchar   = keycmd + "Rev-Inhouse1".

  CREATE htp-list.
  ASSIGN htp-list.paramnr = 2045
         htp-list.fchar   = keycmd + "Rev-Inhouse2".
  
  CREATE htp-list.
  ASSIGN htp-list.paramnr = 2046
         htp-list.fchar   = keycmd + "Rev-Inhouse3".
  
  CREATE htp-list.
  ASSIGN htp-list.paramnr = 2047
         htp-list.fchar   = keycmd + "Rev-Inhouse4".

  CREATE htp-list.
  ASSIGN htp-list.paramnr = 2048
         htp-list.fchar   = keycmd + "Rev-Outsider1".

  CREATE htp-list.
  ASSIGN htp-list.paramnr = 2049
         htp-list.fchar   = keycmd + "Rev-Outsider2".

  CREATE htp-list.
  ASSIGN htp-list.paramnr = 2050
         htp-list.fchar   = keycmd + "Rev-Outsider3".

  CREATE htp-list.
  ASSIGN htp-list.paramnr = 2051
         htp-list.fchar   = keycmd + "Rev-Outsider4".
  /*end geral*/

  /*MG QTY-FOOD QTY-BEV E78F9A*/
  CREATE htp-list.
  ASSIGN htp-list.paramnr = 2052
         htp-list.fchar   = keycmd + "RF-QTY".
  CREATE htp-list.
  ASSIGN htp-list.paramnr = 2053
         htp-list.fchar   = keycmd + "RB-QTY".
  CREATE htp-list.
  ASSIGN htp-list.paramnr = 2054
         htp-list.fchar   = keycmd + "GF-QTY".
  CREATE htp-list.
  ASSIGN htp-list.paramnr = 2055
         htp-list.fchar   = keycmd + "GB-QTY".
  /*end*/

  /*MG Daily FB Flash : DirectPurchase, TransferSideStore, Cost, Compliment 61236D*/
  CREATE htp-list.
  ASSIGN htp-list.paramnr = 2056
         htp-list.fchar   = keycmd + "FB-Direct".
  CREATE htp-list.
  ASSIGN htp-list.paramnr = 2057
         htp-list.fchar   = keycmd + "FB-Transfer".
  CREATE htp-list.
  ASSIGN htp-list.paramnr = 2058
         htp-list.fchar   = keycmd + "FB-Cost-Alloc".
  CREATE htp-list.
  ASSIGN htp-list.paramnr = 2059
         htp-list.fchar   = keycmd + "FB-Compliment".
  /*end*/

  /*MG C8D69F : CANCEL CHECK IN BY ARRIVAL (ANKUNFT)*/
  CREATE htp-list.
  ASSIGN htp-list.paramnr = 2060
         htp-list.fchar   = keycmd + "Cancel-CI".

  /*MG BED81E : WALK IN GUEST BY ARRIVAL (ANKUNFT)*/
  CREATE htp-list.
  ASSIGN htp-list.paramnr = 2061
         htp-list.fchar   = keycmd + "WIG-CI".

  CREATE htp-list.
  ASSIGN
      htp-list.paramnr = 9106
      htp-list.fchar   = keycmd + "WIG".

  CREATE htp-list.
  ASSIGN
      htp-list.paramnr = 7194
      htp-list.fchar   = keycmd + "Canc-night".

  CREATE htp-list.
  ASSIGN
      htp-list.paramnr = 7195
      htp-list.fchar   = keycmd + "canc-cidate".

  CREATE htp-list.
  ASSIGN
      htp-list.paramnr = 7196
      htp-list.fchar   = keycmd + "canc-cidate-nite".

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
      htp-list.paramnr = 9180
      htp-list.fchar   = keycmd + "statRoom".

  CREATE htp-list.
  ASSIGN
      htp-list.paramnr = 8180
      htp-list.fchar   = keycmd + "rComp".

  CREATE htp-list.
  ASSIGN
      htp-list.paramnr = 9000
      htp-list.fchar   = keycmd + "LOS".

  CREATE htp-list.
  ASSIGN
      htp-list.paramnr = 9001
      htp-list.fchar   = keycmd + "CountryRev".

  CREATE htp-list.
  ASSIGN
      htp-list.paramnr = 9002
      htp-list.fchar   = keycmd + "CountryRoom".

  CREATE htp-list.
  ASSIGN
      htp-list.paramnr = 9003
      htp-list.fchar   = keycmd + "RcRev".

  CREATE htp-list.
  ASSIGN
      htp-list.paramnr = 9004
      htp-list.fchar   = keycmd + "RcRoom".


  CREATE htp-list.
  ASSIGN
      htp-list.paramnr = 9005
      htp-list.fchar   = keycmd + "RcSegRev".

  CREATE htp-list.
  ASSIGN
      htp-list.paramnr = 9006
      htp-list.fchar   = keycmd + "RcSegRoom".

  /*ITA 180917*/
  CREATE htp-list.
  ASSIGN
      htp-list.paramnr = 9007
      htp-list.fchar   = keycmd + "SEGMREV-OTH".
  /*end*/

  CREATE htp-list.
  ASSIGN
      htp-list.paramnr = 9008
      htp-list.fchar   = keycmd + "comp-bonus".

  CREATE htp-list.
  ASSIGN
      htp-list.paramnr = 9051
      htp-list.fchar   = keycmd + "sameday-res".

  CREATE htp-list.
  ASSIGN
      htp-list.paramnr = 9052
      htp-list.fchar   = keycmd + "grp-arr".

  CREATE htp-list.
  ASSIGN
      htp-list.paramnr = 9053
      htp-list.fchar   = keycmd + "grp-dep".

  CREATE htp-list.
  ASSIGN
      htp-list.paramnr = 9054
      htp-list.fchar   = keycmd + "grp-room".

  CREATE htp-list.
  ASSIGN
      htp-list.paramnr = 9055
      htp-list.fchar   = keycmd + "indv-room".

  DO n = 1 TO 31:
    CREATE htv-list. 
    ASSIGN
      htv-list.paramnr = 3000 + n
      htv-list.fchar   = ".D" + STRING(n,"99")
    . 
  END.

  /*begin*/
  CREATE htp-list.
  ASSIGN
      htp-list.paramnr = 9009
      htp-list.fchar   = keycmd + "rmrev".

  CREATE htp-list.
  ASSIGN
      htp-list.paramnr = 9010
      htp-list.fchar   = keycmd + "rmnight".

  CREATE htp-list.
  ASSIGN
      htp-list.paramnr = 9011
      htp-list.fchar   = keycmd + "lyrmrev".

  CREATE htp-list.
  ASSIGN
      htp-list.paramnr = 9012
      htp-list.fchar   = keycmd + "lyrmnight".

  CREATE htp-list.
  ASSIGN
      htp-list.paramnr = 9013
      htp-list.fchar   = keycmd + "rmrev-sob".

  CREATE htp-list.
  ASSIGN
      htp-list.paramnr = 9014
      htp-list.fchar   = keycmd + "rmnight-sob".

  CREATE htp-list.
  ASSIGN
      htp-list.paramnr = 9015
      htp-list.fchar   = keycmd + "lyrmrev-sob".

  CREATE htp-list.
  ASSIGN
      htp-list.paramnr = 9016
      htp-list.fchar   = keycmd + "lyrmnight-sob".

  CREATE htp-list.
  ASSIGN
      htp-list.paramnr = 9017
      htp-list.fchar   = keycmd + "rmrev-segm".

  CREATE htp-list.
  ASSIGN
      htp-list.paramnr = 9018
      htp-list.fchar   = keycmd + "rmnight-segm".

  CREATE htp-list.
  ASSIGN
      htp-list.paramnr = 9019
      htp-list.fchar   = keycmd + "lyrmrev-segm".

  CREATE htp-list.
  ASSIGN
      htp-list.paramnr = 9020
      htp-list.fchar   = keycmd + "lyrmnight-segm".

  CREATE htp-list.
  ASSIGN
      htp-list.paramnr = 9021
      htp-list.fchar   = keycmd + "rmrev-compt".

  CREATE htp-list.
  ASSIGN
      htp-list.paramnr = 9022
      htp-list.fchar   = keycmd + "rmocc-compt".

  CREATE htp-list.
  ASSIGN
      htp-list.paramnr = 9023
      htp-list.fchar   = keycmd + "revbud-segm".

  CREATE htp-list.
  ASSIGN
      htp-list.paramnr = 9024
      htp-list.fchar   = keycmd + "nightbud-segm".

  CREATE htp-list.
  ASSIGN
      htp-list.paramnr = 9025
      htp-list.fchar   = keycmd + "lyrevbud-segm".

  CREATE htp-list.
  ASSIGN
      htp-list.paramnr = 9026
      htp-list.fchar   = keycmd + "lynightbud-segm".

  /*geral ambil nilai awal - akhir tahun to-date E9DE63*/
  CREATE htp-list.
  ASSIGN
      htp-list.paramnr = 829
      htp-list.fchar   = keycmd + "INCL-BUDGET-ALL".

  DO n = 1 TO 12:
    CREATE htv-list. 
    ASSIGN
      htv-list.paramnr = 4000 + n
      htv-list.fchar   = ".M" + STRING(n,"99")
    . 
  END.

  /*end.*/

/*
  FOR EACH briefzei WHERE briefzei.briefnr = briefnr 
      NO-LOCK BY briefzei.briefzeilnr: 
      ct = briefzei.texte.
      DO i = 1 TO NUM-ENTRIES(ct, CHR(10)):
          c = TRIM(ENTRY(i, ct, CHR(10))).
          IF (LENGTH(c) GT 0) AND SUBSTR(c,1,1) NE "#" THEN
          DO:
              CREATE brief-list.
              ASSIGN brief-list.b-text = c.
          END.
      END.
  END.
*/
 
  FOR EACH briefzei WHERE briefzei.briefnr = briefnr 
    NO-LOCK BY briefzei.briefzeilnr: 
    j = 1. 
    DO i = 1 TO LENGTH(briefzei.texte): 
       IF ASC(SUBSTR(briefzei.texte, i , 1)) EQ 10 THEN 
       DO: 
         n = i - j. 
         c = SUBSTR(briefzei.texte, j,  n). 
         l = LENGTH(c). 
         IF NOT continued THEN CREATE brief-list.
         brief-list.b-text = brief-list.b-text + c. 
         j = i + 1.
       END. 
    END. 
    n = LENGTH(briefzei.texte) - j + 1. 
    c = SUBSTR(briefzei.texte, j,  n). 
    IF NOT continued THEN CREATE brief-list. 
    b-text = b-text + c.
  END.
END. 

