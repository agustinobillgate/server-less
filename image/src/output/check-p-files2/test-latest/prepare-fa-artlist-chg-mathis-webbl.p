DEFINE TEMP-TABLE m-list LIKE mathis. 
/* DEFINE TEMP-TABLE fa-art LIKE fa-artikel. */

DEFINE TEMP-TABLE fa-art 
    LIKE fa-artikel 
    FIELD start-date AS DATE.

DEF INPUT  PARAMETER recid-mathis       AS INT.
DEF INPUT  PARAMETER recid-fa-artikel   AS INT.

DEF OUTPUT PARAMETER spec               AS CHAR.
DEF OUTPUT PARAMETER locate             AS CHAR.
DEF OUTPUT PARAMETER curr-location      AS CHAR.
DEF OUTPUT PARAMETER curr-gnr           AS INTEGER. 
DEF OUTPUT PARAMETER curr-subgrp        AS INTEGER. 
DEF OUTPUT PARAMETER curr-asset         AS CHAR. 
DEF OUTPUT PARAMETER fibukonto          AS CHAR.
DEF OUTPUT PARAMETER credit-fibu        AS CHAR.
DEF OUTPUT PARAMETER debit-fibu         AS CHAR.
DEF OUTPUT PARAMETER upgrade-part       AS LOGICAL INITIAL NO.
DEF OUTPUT PARAMETER grp-bez            AS CHAR.
DEF OUTPUT PARAMETER sgrp-bez           AS CHAR.
DEF OUTPUT PARAMETER rate               AS DECIMAL.
DEF OUTPUT PARAMETER rate-bez           AS CHAR.

DEF OUTPUT PARAMETER fa-grup-fibukonto    AS CHAR.
DEF OUTPUT PARAMETER fa-grup-credit-fibu  AS CHAR.
DEF OUTPUT PARAMETER fa-grup-debit-fibu   AS CHAR.
DEF OUTPUT PARAMETER TABLE FOR m-list.
DEF OUTPUT PARAMETER TABLE FOR fa-art.

create m-list. 
create fa-art. 

FIND FIRST mathis WHERE RECID(mathis) = recid-mathis.
FIND FIRST fa-artikel WHERE RECID(fa-artikel) = recid-fa-artikel.
FIND FIRST queasy WHERE queasy.key = 314 AND queasy.number1 = fa-artikel.nr NO-LOCK NO-ERROR. /* Malik */

m-list.datum = mathis.datum. 
m-list.name = mathis.name. 
m-list.supplier = mathis.supplier. 
m-list.model = mathis.model. 
m-list.mark = mathis.mark. 
m-list.asset = mathis.asset. 
m-list.price = mathis.price. 
m-list.remark = mathis.remark. 
spec = mathis.spec. 
locate = mathis.location. 
curr-location = locate. 
fa-art.lief-nr = fa-artikel.lief-nr. 
fa-art.gnr = fa-artikel.gnr. 
fa-art.subgrp = fa-artikel.subgrp. 

curr-gnr = fa-artikel.gnr. 
curr-subgrp = fa-artikel.subgrp. 
curr-asset = mathis.asset. 

IF AVAILABLE queasy THEN
DO:
  fa-art.start-date = queasy.date1. /* Malik */
END.

fa-art.katnr = fa-artikel.katnr. 
fa-art.anzahl = fa-artikel.anzahl. 
fa-art.warenwert = fa-artikel.warenwert. 
fa-art.depn-wert = fa-artikel.depn-wert. 
fa-art.book-wert = fa-artikel.book-wert. 
fa-art.anz-depn = fa-artikel.anz-depn. 
fa-art.next-depn = fa-artikel.next-depn. 
fa-art.first-depn = fa-artikel.first-depn. 
fa-art.last-depn = fa-artikel.last-depn. 
IF fa-artikel.fibukonto NE "" THEN fibukonto = fa-artikel.fibukonto. 
IF fa-artikel.credit-fibu NE "" THEN credit-fibu = fa-artikel.credit-fibu. 
IF fa-artikel.debit-fibu NE "" THEN debit-fibu = fa-artikel.debit-fibu. 
IF mathis.flag = 2 THEN
    upgrade-part = YES.
ELSE upgrade-part = NO.


FIND FIRST fa-grup WHERE fa-grup.flag = 1 AND fa-grup.gnr = fa-artikel.subgrp
    NO-LOCK NO-ERROR.
fa-grup-fibukonto = fa-grup.fibukonto.
fa-grup-credit-fibu = fa-grup.credit-fibu.
fa-grup-debit-fibu = fa-grup.debit-fibu.

FIND FIRST fa-kateg WHERE fa-kateg.katnr = fa-artikel.katnr 
  NO-LOCK. 
FIND FIRST fa-grup WHERE fa-grup.gnr = fa-artikel.gnr 
  AND fa-grup.flag = 0 NO-LOCK. 
grp-bez = fa-grup.bezeich. 

FIND FIRST fa-grup WHERE fa-grup.gnr = fa-artikel.subgrp 
  AND fa-grup.flag = 1 NO-LOCK NO-ERROR. 
IF AVAILABLE fa-grup THEN sgrp-bez = fa-grup.bezeich. 

rate = fa-kateg.rate. 
rate-bez = STRING(rate) + " %". 

