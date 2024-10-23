DEF TEMP-TABLE hbill
    FIELD kellner-nr LIKE h-bill.kellner-nr.
DEF TEMP-TABLE t-kellner
    FIELD kellner-nr LIKE kellner.kellner-nr.
DEF TEMP-TABLE t-h-artikel LIKE h-artikel
    FIELD rec-id AS INTEGER.
DEF TEMP-TABLE t-submenu-list
    FIELD menurecid    AS INTEGER 
    FIELD zeit         AS INTEGER 
    FIELD nr           AS INTEGER 
    FIELD artnr        LIKE h-artikel.artnr 
    FIELD bezeich      LIKE h-artikel.bezeich 
    FIELD anzahl       AS INTEGER 
    FIELD zknr         AS INTEGER 
    FIELD request      AS CHAR. 
DEFINE TEMP-TABLE t-h-bill LIKE h-bill
    FIELD rec-id AS INT.
DEF TEMP-TABLE kellner1   LIKE kellner.
DEF TEMP-TABLE p-list
    FIELD rechnr       AS INTEGER 
    FIELD dept         AS INTEGER 
    FIELD billno       AS INTEGER 
    FIELD printed-line AS INTEGER 
    FIELD b-recid      AS INTEGER 
    FIELD last-amount  AS DECIMAL 
    FIELD last-famount AS DECIMAL.


DEFINE INPUT PARAMETER bill-no          AS INTEGER.
DEFINE INPUT PARAMETER dept-no          AS INTEGER.
DEFINE INPUT PARAMETER pay-type         AS INTEGER. /*pay-type=1*/
DEFINE INPUT PARAMETER tischnr          AS INTEGER.
DEFINE INPUT PARAMETER gname            AS CHARACTER.
DEFINE INPUT PARAMETER pax              AS INTEGER.
DEFINE INPUT PARAMETER payment          AS DECIMAL.
DEFINE INPUT PARAMETER resno            AS INTEGER.
DEFINE INPUT PARAMETER reslinno         AS INTEGER.
DEFINE INPUT PARAMETER curr-room        AS CHARACTER.
DEFINE INPUT PARAMETER user-init        AS CHARACTER.
DEFINE INPUT PARAMETER vhp-note         AS CHARACTER.
DEFINE OUTPUT PARAMETER rechnr          AS INTEGER.
DEFINE OUTPUT PARAMETER hbill-flag      AS INTEGER.
DEFINE OUTPUT PARAMETER result-msg      AS CHARACTER.
DEFINE OUTPUT PARAMETER vSuccess        AS LOGICAL INITIAL NO.

DEFINE VARIABLE language-code AS INTEGER NO-UNDO INIT 0.
DEFINE VARIABLE rec-id        AS INTEGER.
DEFINE VARIABLE balance       AS DECIMAL.
DEFINE VARIABLE gastnr        AS INTEGER.
DEFINE VARIABLE order-name    AS CHAR.
DEFINE VARIABLE order-phone   AS CHAR.
DEFINE VARIABLE order-email   AS CHAR.
DEFINE VARIABLE curr-gastnr   AS INTEGER.
DEFINE VARIABLE payment-param AS INTEGER.

IF NUM-ENTRIES(gname,"|") GE 2 THEN
DO:
    order-name  = ENTRY(1,gname,"|").
    order-phone = ENTRY(2,gname,"|").
    order-email = ENTRY(3,gname,"|").
END.
gname = order-name.

FIND FIRST h-bill WHERE h-bill.rechnr EQ bill-no AND h-bill.departement EQ dept-no NO-LOCK NO-ERROR.
IF AVAILABLE h-bill THEN
DO:
    rec-id  = RECID(h-bill).
    balance = h-bill.saldo.
END.


FIND FIRST queasy WHERE queasy.KEY EQ 270 
    AND queasy.number1 EQ 1 
    AND queasy.betriebsnr EQ 1
    AND queasy.number2 EQ 26 NO-LOCK NO-ERROR.
IF AVAILABLE queasy THEN
DO:
    payment-param = INT(queasy.char2).
END.
ELSE
DO:
    result-msg = "Artikel Number For Guest Ledger Not Available! Please Contact VHP Support!".
    RETURN.
END.

/* MESSAGE "check guest phone: " order-phone VIEW-AS ALERT-BOX INFO BUTTONS OK.  */
DEFINE BUFFER bguest FOR guest.
FIND FIRST guest WHERE guest.mobil-telefon EQ order-phone AND guest.karteityp EQ 0 EXCLUSIVE-LOCK NO-ERROR.
IF NOT AVAILABLE guest THEN
DO:
    FIND FIRST guest WHERE guest.telefon EQ order-phone AND guest.karteityp EQ 0 EXCLUSIVE-LOCK NO-ERROR.
    IF NOT AVAILABLE guest THEN 
    DO:
        FOR EACH bguest NO-LOCK BY bguest.gastnr DESC:
            curr-gastnr = bguest.gastnr.
            LEAVE.
        END.
        IF curr-gastnr EQ 0 THEN curr-gastnr = 1.
        ELSE curr-gastnr = curr-gastnr + 1.

        CREATE guest.
        guest.karteityp     = 0.
        guest.NAME          = order-name.
        guest.email-adr     = order-email.
        guest.telefon       = order-phone.
        guest.mobil-telefon = order-phone.
        guest.gastnr        = curr-gastnr.
        guest.zahlungsart   = payment-param.
        guest.point-gastnr  = payment-param.
        gastnr = curr-gastnr.
    END.
    ELSE 
    DO:
        gastnr = guest.gastnr.
        guest.NAME          = order-name.
        guest.email-adr     = order-email.
        guest.telefon       = order-phone.
        guest.mobil-telefon = order-phone.
        guest.zahlungsart   = payment-param.
        guest.point-gastnr  = payment-param.
    END.
END.
ELSE
DO:
    gastnr = guest.gastnr.
    guest.NAME          = order-name.
    guest.email-adr     = order-email.
    guest.telefon       = order-phone.
    guest.mobil-telefon = order-phone.
    guest.zahlungsart   = payment-param.
    guest.point-gastnr  = payment-param.
END.
RELEASE guest.

/* MESSAGE "gastnr: " curr-gastnr VIEW-AS ALERT-BOX INFO BUTTONS OK.  */

/*
FIND FIRST queasy WHERE queasy.KEY EQ 270 
    AND queasy.number1 EQ 1 
    AND queasy.betriebsnr EQ 1
    AND queasy.number2 EQ 25 NO-LOCK NO-ERROR.
IF AVAILABLE queasy THEN
DO:
    gastnr = INT(queasy.char2).
END.
ELSE
DO:
    MESSAGE "Parameter Dummy Guest Number For Payment FB Not Available!" SKIP
            "Please Contact VHP Support!"
        VIEW-AS ALERT-BOX INFO BUTTONS OK.
    RETURN.
END.
*/
DEFINE VARIABLE saldo               AS DECIMAL.
DEFINE VARIABLE disc-art1           AS INT.
DEFINE VARIABLE disc-art2           AS INT.
DEFINE VARIABLE disc-art3           AS INT.
DEFINE VARIABLE mi-ordertaker       AS LOGICAL INIT YES.
DEFINE VARIABLE price-decimal       AS INT.
DEFINE VARIABLE curr-local          AS CHAR.
DEFINE VARIABLE curr-foreign        AS CHAR.
DEFINE VARIABLE foreign-rate        AS LOGICAL.
DEFINE VARIABLE exchg-rate          AS DECIMAL INIT 1.
DEFINE VARIABLE b-title             AS CHAR.
DEFINE VARIABLE deptname            AS CHAR.
DEFINE VARIABLE p-223               AS LOGICAL.
DEFINE VARIABLE curr-waiter         AS INT INIT 0.
DEFINE VARIABLE fl-code             AS INT INIT 0.
DEFINE VARIABLE pos1                AS INT.
DEFINE VARIABLE pos2                AS INT.
DEFINE VARIABLE cashless-flag       AS LOGICAL NO-UNDO.
DEFINE VARIABLE c-param870          AS CHARACTER. 
DEFINE VARIABLE add-zeit            AS INTEGER INIT 0.
DEFINE VARIABLE activate-deposit    AS LOGICAL. 
DEFINE VARIABLE bill-date           AS DATE.
DEFINE VARIABLE p-88                AS LOGICAL NO-UNDO INIT NO.
DEFINE VARIABLE amt                 AS DECIMAL.
DEFINE VARIABLE amt-foreign         AS DECIMAL.
DEFINE VARIABLE msg-str             AS CHARACTER.  
DEFINE VARIABLE msg-str1            AS CHARACTER.  
DEFINE VARIABLE msg-str2            AS CHARACTER.
DEFINE VARIABLE balance-foreign     AS DECIMAL.
DEFINE VARIABLE billart             AS INTEGER.
DEFINE VARIABLE qty                 AS INTEGER.
DEFINE VARIABLE price               AS DECIMAL.
DEFINE VARIABLE amount-foreign      AS DECIMAL.
DEFINE VARIABLE amount              AS DECIMAL.
DEFINE VARIABLE description         AS CHARACTER.
DEFINE VARIABLE transfer-zinr       AS CHARACTER.
DEFINE VARIABLE cancel-flag         AS LOGICAL.
DEFINE VARIABLE mwst                LIKE vhp.h-bill-line.betrag INIT 0.
DEFINE VARIABLE mwst-foreign        LIKE vhp.h-bill-line.betrag INIT 0.
DEFINE VARIABLE bcol                AS INT.
DEFINE VARIABLE fl-code1            AS INT INIT 0.
DEFINE VARIABLE fl-code2            AS INT INIT 0.
DEFINE VARIABLE fl-code3            AS INT INIT 0.
DEFINE VARIABLE closed              AS LOGICAL.
DEFINE VARIABLE mealcoupon-cntrl    AS LOGICAL.
DEFINE VARIABLE must-print          AS LOGICAL.
DEFINE VARIABLE zero-flag           AS LOGICAL.
DEFINE VARIABLE multi-cash          AS LOGICAL.
DEFINE VARIABLE cancel-exist        AS LOGICAL INIT NO.
DEFINE VARIABLE double-currency     AS LOGICAL.
DEFINE VARIABLE dept-name           AS CHARACTER.
DEFINE VARIABLE cancel-str          AS CHARACTER.
DEFINE VARIABLE flag-code           AS INTEGER.
DEFINE VARIABLE var-testing         AS CHAR.
DEFINE VARIABLE rec-id-h-artikel    AS INT.
DEFINE VARIABLE service-code        AS INT.
DEFINE VARIABLE h-artart            AS INT.
DEFINE VARIABLE h-artnrfront        AS INT.

IF curr-room EQ ? THEN
DO:
    curr-room = "".
END.
IF gname EQ ? THEN
DO:
    gname = "".
END.

/* MESSAGE "tada-post-payment-getsaldobl.p" VIEW-AS ALERT-BOX INFO BUTTONS OK.  */
RUN tada-post-payment-getsaldobl.p(bill-no, dept-no, OUTPUT saldo).
IF balance NE saldo THEN
DO:
    result-msg = "There is a new article posted, balance to be different."
        + CHR(10) + "Please check the bill.".
    RETURN.
END.

/* MESSAGE "tada-post-payment-preparebl.p" VIEW-AS ALERT-BOX INFO BUTTONS OK.  */
RUN tada-post-payment-preparebl.p(language-code, dept-no, 1, user-init, ?,
        OUTPUT mealcoupon-cntrl, OUTPUT must-print, OUTPUT zero-flag,
        OUTPUT multi-cash, OUTPUT cancel-exist, OUTPUT msg-str,
        OUTPUT disc-art1, OUTPUT disc-art2, OUTPUT disc-art3,
        OUTPUT mi-ordertaker, OUTPUT price-decimal, OUTPUT curr-local,
        OUTPUT curr-foreign, OUTPUT double-currency, OUTPUT foreign-rate,
        OUTPUT exchg-rate, OUTPUT b-title, OUTPUT deptname, OUTPUT p-223,
        OUTPUT curr-waiter, OUTPUT fl-code, OUTPUT pos1, OUTPUT pos2,
        OUTPUT cashless-flag, OUTPUT c-param870, OUTPUT activate-deposit,
        OUTPUT TABLE hbill, OUTPUT TABLE t-kellner).
IF msg-str NE "" THEN
DO:
    result-msg = SUBSTR(msg-str,2).
    RETURN.
END.
FIND FIRST t-kellner NO-ERROR.
/*
MESSAGE "tada-post-paymentcityledgerbl: " gastnr
    VIEW-AS ALERT-BOX INFO BUTTONS OK.
*/
/* MESSAGE "tada-post-payment-btn-transferbl.p" VIEW-AS ALERT-BOX INFO BUTTONS OK.  */
RUN tada-post-payment-btn-transferbl.p
    (language-code, rec-id, gastnr, dept-no,
    payment, exchg-rate, price-decimal, balance, ?,
    disc-art1, disc-art2, disc-art3, t-kellner.kellner-nr,
    OUTPUT billart, OUTPUT qty,
    OUTPUT description, OUTPUT price, OUTPUT amount-foreign,
    OUTPUT amount, OUTPUT bill-date, OUTPUT fl-code,
    OUTPUT fl-code1, OUTPUT msg-str, OUTPUT var-testing,
    OUTPUT TABLE t-h-artikel).
FIND FIRST t-h-artikel.

DESCRIPTION = DESCRIPTION + "/" + vhp-note.

IF msg-str NE "" THEN
DO:
    result-msg = msg-str.
    RETURN.
END.
IF fl-code1 EQ 1 THEN
DO:
    result-msg = "Payment with Voucher is not support".
    RETURN.
END.
IF fl-code EQ 2 THEN
DO:
    result-msg = "NOT DEFINED: F/O Article" + " " + STRING(billart) + CHR(10) + "C/L Posting not possible.".
    RETURN.
END.
ELSE IF fl-code EQ 3 THEN
DO:
    RETURN.
END.
ELSE IF fl-code EQ 1 THEN
DO:
    IF AVAILABLE t-h-artikel THEN
    DO:
        ASSIGN
            rec-id-h-artikel    = t-h-artikel.rec-id
            service-code        = t-h-artikel.service-code
            h-artart            = t-h-artikel.artart
            h-artnrfront        = t-h-artikel.artnrfront
            .
    END.
    add-zeit = 1.
/*     MESSAGE STRING(fl-code) + " tada-post-payment-updatebillbl.p" VIEW-AS ALERT-BOX INFO BUTTONS OK.  */
    RUN tada-post-payment-updatebillbl.p (language-code, rec-id, rec-id-h-artikel, deptname, ?,
        h-artart, NO, service-code, payment,
        amount-foreign, price, double-currency, qty,
        exchg-rate, price-decimal, user-init,
        tischnr, dept-no, user-init, gname, pax, 0,
        add-zeit, billart, description, "", "",
        "", "", "", "", YES,
        NO, h-artnrfront, pay-type, gastnr, "",
        NO, foreign-rate, curr-room, user-init,
        resno, reslinno,
        INPUT TABLE t-submenu-list, OUTPUT bill-date,
        OUTPUT cancel-flag, OUTPUT fl-code, OUTPUT mwst,
        OUTPUT mwst-foreign, OUTPUT rechnr, OUTPUT balance,
        OUTPUT bcol, OUTPUT balance-foreign, OUTPUT fl-code1,
        OUTPUT fl-code2, OUTPUT fl-code3, OUTPUT p-88, OUTPUT closed,
        OUTPUT TABLE t-h-bill, OUTPUT TABLE kellner1). 
    FIND FIRST t-h-bill NO-ERROR.
    FIND FIRST kellner1 NO-ERROR.
    IF AVAILABLE t-h-bill THEN
    DO:        
        rechnr = t-h-bill.rechnr.
        hbill-flag = t-h-bill.flag.  
    END.
    IF hbill-flag EQ 1 THEN RUN tada-post-payment-restsale-updatehbillbl.p(t-h-bill.rec-id).
    RUN tada-post-payment-delqueasybl.p(INPUT-OUTPUT TABLE p-list, t-h-bill.rec-id, NO).    
    vSuccess = YES.
END.
