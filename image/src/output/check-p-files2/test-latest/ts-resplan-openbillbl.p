DEFINE TEMP-TABLE hbill
    FIELD kellner-nr LIKE h-bill.kellner-nr.

DEFINE TEMP-TABLE t-kellner
    FIELD kellner-nr LIKE kellner.kellner-nr.

DEFINE TEMP-TABLE t-h-artikel LIKE h-artikel
    FIELD rec-id AS INTEGER.

DEFINE TEMP-TABLE menu-list
  FIELD rec-id      AS INTEGER
  FIELD DESCRIPTION AS CHARACTER
  FIELD qty         AS INTEGER
  FIELD price       AS DECIMAL
  FIELD special-request AS CHARACTER.

DEFINE TEMP-TABLE t-h-bill LIKE h-bill
    FIELD rec-id AS INT.

DEFINE TEMP-TABLE t-submenu-list
    FIELD menurecid    AS INTEGER 
    FIELD zeit         AS INTEGER 
    FIELD nr           AS INTEGER 
    FIELD artnr        LIKE h-artikel.artnr 
    FIELD bezeich      LIKE h-artikel.bezeich 
    FIELD anzahl       AS INTEGER 
    FIELD zknr         AS INTEGER 
    FIELD request      AS CHAR. 

DEF TEMP-TABLE kellner1   LIKE kellner. 

DEFINE INPUT PARAMETER pvILanguage  AS INTEGER NO-UNDO.
DEFINE INPUT PARAMETER s-recid      AS INTEGER.
DEFINE INPUT PARAMETER curr-dept    AS INTEGER.
DEFINE INPUT PARAMETER curr-date    AS DATE.
DEFINE INPUT PARAMETER recid-hbill  AS INTEGER.
DEFINE INPUT PARAMETER user-init    AS CHARACTER.
DEFINE INPUT PARAMETER pos-printer  AS INTEGER.
DEFINE INPUT PARAMETER curr-flag    AS CHARACTER.
DEFINE OUTPUT PARAMETER err-flag    AS LOGICAL INIT NO.
DEFINE OUTPUT PARAMETER result-msg  AS CHARACTER.

{SupertransBL.i} 
DEFINE VARIABLE lvCAREA AS CHAR INITIAL "ts-resplan". 

DEFINE VARIABLE exchg-rate          AS DECIMAL NO-UNDO INIT 1. 
DEFINE VARIABLE foreign-payment     AS DECIMAL NO-UNDO.
DEFINE VARIABLE local-payment       AS DECIMAL NO-UNDO.
DEFINE VARIABLE deposit-foreign     AS DECIMAL NO-UNDO.
DEFINE VARIABLE deposit-amount      AS DECIMAL NO-UNDO.
DEFINE VARIABLE price-decimal       AS INTEGER NO-UNDO.
DEFINE VARIABLE depoart             AS INTEGER NO-UNDO.
DEFINE VARIABLE h-depoart           AS INTEGER NO-UNDO.
DEFINE VARIABLE h-depoart-front     AS INTEGER NO-UNDO.
DEFINE VARIABLE h-depoart-type      AS INTEGER NO-UNDO.
DEFINE VARIABLE hart-recid          AS INTEGER NO-UNDO.
DEFINE VARIABLE h-depobez           AS CHARACTER NO-UNDO.
DEFINE VARIABLE gname               AS CHARACTER NO-UNDO.
DEFINE VARIABLE str1                AS CHARACTER NO-UNDO.
DEFINE VARIABLE table-no            AS INTEGER NO-UNDO.
DEFINE VARIABLE pax                 AS INTEGER NO-UNDO.
DEFINE VARIABLE gastno              AS INTEGER NO-UNDO.
DEFINE VARIABLE ns-billno           AS INTEGER NO-UNDO.
DEFINE VARIABLE ft-h                AS INTEGER NO-UNDO.
DEFINE VARIABLE ft-m                AS INTEGER NO-UNDO.
DEFINE VARIABLE from-time           AS INTEGER NO-UNDO.
DEFINE VARIABLE bill-date           AS DATE    NO-UNDO. 
DEFINE VARIABLE rsv-date            AS DATE    NO-UNDO.

DEFINE VARIABLE amount             LIKE bill-line.betrag.
DEFINE VARIABLE mealcoupon-cntrl   AS LOGICAL.
DEFINE VARIABLE must-print         AS LOGICAL.
DEFINE VARIABLE zero-flag          AS LOGICAL.
DEFINE VARIABLE multi-cash         AS LOGICAL.
DEFINE VARIABLE cancel-exist       AS LOGICAL INIT NO.
DEFINE VARIABLE msg-str            AS CHAR.
DEFINE VARIABLE disc-art1          AS INT.
DEFINE VARIABLE disc-art2          AS INT.
DEFINE VARIABLE disc-art3          AS INT.
DEFINE VARIABLE mi-ordertaker      AS LOGICAL INIT YES.
DEFINE VARIABLE curr-local         AS CHAR.
DEFINE VARIABLE curr-foreign       AS CHAR.
DEFINE VARIABLE double-currency    AS LOGICAL.
DEFINE VARIABLE foreign-rate       AS LOGICAL.
DEFINE VARIABLE b-title            AS CHAR.
DEFINE VARIABLE deptname           AS CHAR.
DEFINE VARIABLE p-223              AS LOGICAL.
DEFINE VARIABLE curr-waiter        AS INT INIT 0.
DEFINE VARIABLE fl-code            AS INT INIT 0.
DEFINE VARIABLE pos1               AS INT.
DEFINE VARIABLE pos2               AS INT.
DEFINE VARIABLE cashless-flag      AS LOGICAL NO-UNDO.
DEFINE VARIABLE price              AS DECIMAL.   
DEFINE VARIABLE add-zeit           AS INTEGER INIT 0.
DEFINE VARIABLE cancel-flag        AS LOGICAL.
DEFINE VARIABLE mwst               LIKE vhp.h-bill-line.betrag INIT 0.
DEFINE VARIABLE mwst-foreign       LIKE vhp.h-bill-line.betrag INIT 0.
DEFINE VARIABLE balance            AS DECIMAL.
DEFINE VARIABLE bcol               AS INT.
DEFINE VARIABLE balance-foreign    AS DECIMAL.
DEFINE VARIABLE fl-code1           AS INT INIT 0.
DEFINE VARIABLE fl-code2           AS INT INIT 0.
DEFINE VARIABLE fl-code3           AS INT INIT 0.
DEFINE VARIABLE p-88               AS LOGICAL.
DEFINE VARIABLE closed             AS LOGICAL.
DEFINE VARIABLE error-str          AS CHAR INITIAL "" NO-UNDO.
DEFINE VARIABLE usr                AS CHAR.
DEFINE VARIABLE outlet             AS CHAR.
DEFINE VARIABLE err                AS LOGICAL.  
DEFINE VARIABLE err1               AS LOGICAL.  
DEFINE VARIABLE fract              AS DECIMAL INITIAL 1 NO-UNDO.  
DEFINE VARIABLE service-code       AS INT.
DEFINE VARIABLE rechnr             AS INT.
DEFINE VARIABLE voucher-str        AS CHARACTER.
DEFINE VARIABLE voucher-depo       AS CHARACTER.
DEFINE VARIABLE rsvtable-text      AS CHARACTER.

RUN prepare-ts-restinvbl.p (pvILanguage, curr-dept, pos-printer, user-init, ?,
   OUTPUT mealcoupon-cntrl, OUTPUT must-print, OUTPUT zero-flag,
   OUTPUT multi-cash, OUTPUT cancel-exist, OUTPUT msg-str,
   OUTPUT disc-art1, OUTPUT disc-art2, OUTPUT disc-art3,
   OUTPUT mi-ordertaker, OUTPUT price-decimal, OUTPUT curr-local,
   OUTPUT curr-foreign, OUTPUT double-currency, OUTPUT foreign-rate,
   OUTPUT exchg-rate, OUTPUT b-title, OUTPUT deptname, OUTPUT p-223,
   OUTPUT curr-waiter, OUTPUT fl-code, OUTPUT pos1, OUTPUT pos2,
   OUTPUT cashless-flag, OUTPUT TABLE hbill, OUTPUT TABLE t-kellner).

IF msg-str NE "" THEN
DO:
    err-flag = YES.
    result-msg = msg-str.
    RETURN.
END.

FIND FIRST htparam WHERE htparam.paramnr EQ 1361 NO-LOCK NO-ERROR. 
IF AVAILABLE htparam THEN depoart = htparam.finteger.

FIND FIRST hoteldpt WHERE hoteldpt.num EQ curr-dept NO-LOCK NO-ERROR.
IF AVAILABLE hoteldpt THEN deptname = hoteldpt.depart.

/*Get Artikel Deposit Resto*/
FIND FIRST wgrpgen WHERE wgrpgen.bezeich MATCHES "*deposit*" NO-LOCK NO-ERROR.
IF AVAILABLE wgrpgen THEN
DO:
    FIND FIRST h-artikel WHERE h-artikel.endkum EQ wgrpgen.eknr
        AND h-artikel.activeflag NO-LOCK NO-ERROR.
    IF AVAILABLE h-artikel THEN
    DO:
        ASSIGN
            hart-recid      = RECID(h-artikel)
            h-depoart       = h-artikel.artnr
            h-depoart-type  = h-artikel.artart
            h-depobez       = h-artikel.bezeich
            h-depoart-front = h-artikel.artnrfront            
            service-code    = service-code
        .
    END.        
END.

/*Get data reservation table*/
FIND FIRST queasy WHERE RECID(queasy) EQ s-recid NO-LOCK NO-ERROR.
IF AVAILABLE queasy THEN
DO:
    ASSIGN
        ns-billno   = INTEGER(queasy.deci2)
        gname       = ENTRY(1, queasy.char2, "&&")
        gastno      = INTEGER(ENTRY(3, queasy.char2, "&&")) 
        ft-h        = INTEGER(SUBSTR(queasy.char1, 1, 2))
        ft-m        = INTEGER(SUBSTR(queasy.char1, 3, 2))
        rsv-date    = queasy.date1
        deposit-amount = queasy.deci1
        table-no    = queasy.number2
        pax         = queasy.number3
    .   
END.

/*Get Voucher Deposit*/
FIND FIRST bill WHERE bill.rechnr EQ ns-billno AND bill.gastnr EQ gastno 
    AND bill.resnr EQ 0 AND bill.reslinnr EQ 1 
    AND bill.billtyp EQ curr-dept AND bill.flag EQ 1 NO-LOCK NO-ERROR.
IF AVAILABLE bill THEN
DO:
    FIND FIRST bill-line WHERE bill-line.rechnr EQ bill.rechnr
        AND bill-line.artnr EQ depoart NO-LOCK NO-ERROR.
    IF AVAILABLE bill-line THEN
    DO:
        str1 = ENTRY(1, bill-line.bezeich, "[").
        voucher-depo = TRIM(ENTRY(2, str1, "/")).
    END.
END.

FIND FIRST htparam WHERE htparam.paramnr EQ 144 NO-LOCK. 
FIND FIRST waehrung WHERE waehrung.wabkurz EQ htparam.fchar NO-LOCK NO-ERROR. 
IF AVAILABLE waehrung THEN exchg-rate = waehrung.ankauf / waehrung.einheit.

ASSIGN
    deposit-foreign = deposit-amount / exchg-rate
    foreign-payment = - deposit-amount / exchg-rate
    local-payment   = - deposit-amount
.

add-zeit = add-zeit + 1.
RUN ts-restinv-update-bill_1bl.p (pvILanguage, recid-hbill, hart-recid, deptname, ?,
    h-depoart-type, NO, service-code, local-payment,
    foreign-payment, local-payment, double-currency, 1, exchg-rate, price-decimal, user-init,
    table-no, curr-dept, curr-waiter, gname, pax, 0,
    add-zeit, h-depoart, h-depobez, "", voucher-depo,
    "", "", voucher-str, "", YES,
    NO, h-depoart-front, 0, gastno, "",
    NO, foreign-rate, "", user-init,
    0, 0, NO, 0, "",
    INPUT TABLE t-submenu-list, OUTPUT bill-date,
    OUTPUT cancel-flag, OUTPUT fl-code, OUTPUT mwst,
    OUTPUT mwst-foreign, OUTPUT rechnr, OUTPUT balance,
    OUTPUT bcol, OUTPUT balance-foreign, OUTPUT fl-code1,
    OUTPUT fl-code2, OUTPUT fl-code3, OUTPUT p-88, OUTPUT closed,
    OUTPUT TABLE t-h-bill, OUTPUT TABLE kellner1).

FIND FIRST kellner1 NO-ERROR.
IF fl-code EQ 1 THEN
DO:
    err-flag = YES.
    result-msg = translateExtended ("Transaction not allowed: Posted item(s) with differrent billing date found.",lvCAREA,"").
    RETURN.
END.
ELSE IF fl-code EQ 2 THEN
DO:
    err-flag = YES.
    result-msg = translateExtended ("Table has occupied with another guest.",lvCAREA,"").
    RETURN.
END.

FIND FIRST t-h-bill NO-LOCK NO-ERROR.
IF AVAILABLE t-h-bill THEN
DO:
    IF curr-flag NE "" THEN rsvtable-text = "Delete RSV Table".
    ELSE rsvtable-text = "".

    CREATE queasy.
    ASSIGN
        queasy.KEY      = 251
        queasy.char1    = rsvtable-text
        queasy.number1  = t-h-bill.rec-id
        queasy.number2  = s-recid
        .
    FIND CURRENT queasy NO-LOCK.
END.
