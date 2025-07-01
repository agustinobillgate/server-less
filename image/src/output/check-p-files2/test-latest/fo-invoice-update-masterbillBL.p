
DEFINE INPUT  PARAMETER pvILanguage     AS INTEGER  NO-UNDO.
DEFINE INPUT  PARAMETER bil-recid       AS INTEGER.
DEFINE INPUT  PARAMETER curr-department AS INTEGER.
DEFINE INPUT  PARAMETER currZeit        AS INTEGER.
DEFINE INPUT  PARAMETER amount          AS DECIMAL.
DEFINE INPUT  PARAMETER amount-foreign  AS DECIMAL.
DEFINE INPUT  PARAMETER billart         AS INT.
DEFINE INPUT  PARAMETER description     AS CHAR.
DEFINE INPUT  PARAMETER qty             AS INT.
DEFINE INPUT  PARAMETER curr-room       AS CHAR.
DEFINE INPUT  PARAMETER user-init       AS CHAR.
DEFINE INPUT  PARAMETER artnr           AS INTEGER.
DEFINE INPUT  PARAMETER price           AS DECIMAL.
DEFINE INPUT  PARAMETER cancel-str      AS CHAR.
DEFINE INPUT  PARAMETER exchg-rate      AS DECIMAL.
DEFINE INPUT  PARAMETER price-decimal   AS INTEGER.
DEFINE INPUT  PARAMETER double-currency AS LOGICAL.
DEFINE OUTPUT PARAMETER ex-rate         AS DECIMAL.
DEFINE OUTPUT PARAMETER mess-str        AS CHAR.
DEFINE OUTPUT PARAMETER master-str      AS CHAR.
DEFINE OUTPUT PARAMETER master-rechnr   AS CHAR.
DEFINE INPUT-OUTPUT PARAMETER master-flag     AS LOGICAL INITIAL NO.

DEF VAR bill-date AS DATE.
DEF VAR na-running AS LOGICAL.
DEFINE VARIABLE gastnrmember    AS INTEGER. 

{SupertransBL.i} 
DEF VAR lvCAREA AS CHAR INITIAL "fo-invoice".

FIND FIRST bill WHERE RECID(bill) = bil-recid NO-LOCK.
FIND FIRST artikel WHERE artikel.artnr = artnr 
    AND artikel.departement = curr-department NO-LOCK.
IF AVAILABLE artikel THEN
    RUN update-masterbill(currZeit, OUTPUT master-flag).

{ inv-ar.i } 
{ update-masterbl.i } 
{ master-taxserv.i } 
