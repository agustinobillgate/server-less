
DEFINE TEMP-TABLE t-bill LIKE bill.
DEFINE TEMP-TABLE t-res-line LIKE res-line
    FIELD guest-name AS CHAR            /*ragung penambahan guest name req Web*/
    .
DEFINE TEMP-TABLE spbill-list
    FIELD selected AS LOGICAL INITIAL YES 
    FIELD bl-recid AS INTEGER. 

DEF TEMP-TABLE t-bill-line LIKE bill-line
    FIELD rec-id AS INT
    FIELD serv   AS DECIMAL FORMAT "->,>>>,>>>,>>9" 
    FIELD vat    AS DECIMAL FORMAT "->,>>>,>>>,>>9" 
    FIELD netto  AS DECIMAL FORMAT "->,>>>,>>>,>>9" 
    FIELD art-type AS INTEGER
    .


DEFINE INPUT PARAMETER bil-flag         AS INTEGER.
DEFINE INPUT PARAMETER bil-recid        AS INTEGER.
DEFINE INPUT PARAMETER room             AS CHARACTER.
DEFINE INPUT PARAMETER vipflag          AS LOGICAL.
DEFINE INPUT PARAMETER fill-co          AS LOGICAL.
DEFINE INPUT PARAMETER double-currency  AS LOGICAL INITIAL NO.
DEFINE INPUT PARAMETER foreign-rate     AS LOGICAL. 

DEFINE OUTPUT PARAMETER abreise         AS DATE.
DEFINE OUTPUT PARAMETER resname         AS CHAR.
DEFINE OUTPUT PARAMETER res-exrate      AS DECIMAL.
DEFINE OUTPUT PARAMETER zimmer-bezeich  AS CHAR.
DEFINE OUTPUT PARAMETER kreditlimit     AS DECIMAL.
DEFINE OUTPUT PARAMETER master-str      AS CHAR.
DEFINE OUTPUT PARAMETER master-rechnr   AS CHAR.
DEFINE OUTPUT PARAMETER bill-anzahl     AS INT.
DEFINE OUTPUT PARAMETER queasy-char1    AS CHAR.
DEFINE OUTPUT PARAMETER disp-warning    AS LOGICAL INIT NO.
DEFINE OUTPUT PARAMETER flag-report     AS LOGICAL INIT NO.
DEFINE OUTPUT PARAMETER rescomment      AS CHARACTER.
DEFINE OUTPUT PARAMETER printed         AS CHARACTER.
DEFINE OUTPUT PARAMETER rechnr          AS INTEGER.
DEFINE OUTPUT PARAMETER rmrate          AS DECIMAL.
DEFINE OUTPUT PARAMETER balance         AS DECIMAL.
DEFINE OUTPUT PARAMETER balance-foreign AS DECIMAL.
DEFINE OUTPUT PARAMETER tot-balance     AS DECIMAL.
DEFINE OUTPUT PARAMETER guest-taxcode   AS CHAR.
DEFINE OUTPUT PARAMETER repeat-charge   AS LOGICAL.
DEFINE OUTPUT PARAMETER TABLE FOR t-res-line.
DEFINE OUTPUT PARAMETER TABLE FOR t-bill.
DEFINE OUTPUT PARAMETER TABLE FOR spbill-list.
DEFINE OUTPUT PARAMETER TABLE FOR t-bill-line.

/******************************************************************************/
/*ragung change to _1bl*/
RUN fo-invoice-open-bill-cld_2bl.p(bil-flag, bil-recid, room, vipflag, OUTPUT abreise,
         OUTPUT resname, OUTPUT res-exrate, OUTPUT zimmer-bezeich,
         OUTPUT kreditlimit, OUTPUT master-str, OUTPUT master-rechnr,
         OUTPUT bill-anzahl, OUTPUT queasy-char1, OUTPUT disp-warning,
         OUTPUT flag-report, OUTPUT guest-taxcode, OUTPUT repeat-charge,
         OUTPUT TABLE t-res-line, OUTPUT TABLE t-bill).

FIND FIRST t-bill NO-LOCK.
FIND FIRST t-res-line NO-LOCK NO-ERROR.

RUN fo-invoice-fill-rescommentbl.p(bil-recid, fill-co, OUTPUT rescomment).

IF t-bill.rgdruck = 0 THEN printed = "". 
ELSE printed = "*". 
rechnr = t-bill.rechnr. 
rmrate = 0.
IF AVAILABLE t-res-line THEN rmrate = t-res-line.zipreis.
balance = t-bill.saldo. 
IF double-currency OR foreign-rate THEN balance-foreign = t-bill.mwst[99].

IF bil-flag = 0 THEN
DO:
    tot-balance = 0.
    IF t-bill.parent-nr = 0 THEN tot-balance = t-bill.saldo. 
    ELSE RUN fo-invoice-disp-totbalancebl.p(bil-recid, OUTPUT tot-balance).
END.

FOR EACH spbill-list:
    DELETE spbill-list. 
END.

RUN disp-bill-line.

PROCEDURE disp-bill-line:
    RUN fo-invoice-disp-bill-line-cldbl.p(bil-recid, double-currency, 
        OUTPUT TABLE t-bill-line, OUTPUT TABLE spbill-list).
END PROCEDURE.
