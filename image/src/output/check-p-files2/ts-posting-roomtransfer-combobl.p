DEFINE TEMP-TABLE t-h-bill LIKE h-bill  
    FIELD rec-id AS INT.

DEFINE TEMP-TABLE kellner1   LIKE kellner.

DEFINE TEMP-TABLE hbill
    FIELD kellner-nr LIKE h-bill.kellner-nr.

DEFINE TEMP-TABLE t-kellner
    FIELD kellner-nr LIKE kellner.kellner-nr.

DEFINE TEMP-TABLE t-h-artikel LIKE h-artikel
    FIELD rec-id AS INTEGER.

DEFINE TEMP-TABLE t-submenu-list
    FIELD menurecid    AS INTEGER 
    FIELD zeit         AS INTEGER 
    FIELD nr           AS INTEGER 
    FIELD artnr        LIKE h-artikel.artnr 
    FIELD bezeich      LIKE h-artikel.bezeich 
    FIELD anzahl       AS INTEGER 
    FIELD zknr         AS INTEGER 
    FIELD request      AS CHAR. 

DEFINE TEMP-TABLE p-list
    FIELD rechnr       AS INTEGER 
    FIELD dept         AS INTEGER 
    FIELD billno       AS INTEGER 
    FIELD printed-line AS INTEGER 
    FIELD b-recid      AS INTEGER 
    FIELD last-amount  AS DECIMAL 
    FIELD last-famount AS DECIMAL.

DEFINE INPUT PARAMETER language-code    AS INTEGER.
DEFINE INPUT PARAMETER vKey             AS CHARACTER.
DEFINE INPUT PARAMETER h-recid          AS INTEGER.
DEFINE INPUT PARAMETER bill-no          AS INTEGER.
DEFINE INPUT PARAMETER tischnr          AS INTEGER.
DEFINE INPUT PARAMETER pax              AS INTEGER.
DEFINE INPUT PARAMETER curr-dept        AS INTEGER.
DEFINE INPUT PARAMETER guestnr          AS INTEGER.   /*Param 155*/
DEFINE INPUT PARAMETER user-init        AS CHARACTER.
DEFINE INPUT PARAMETER pf-file1         AS CHARACTER. /*Param 339*/
DEFINE INPUT PARAMETER pf-file2         AS CHARACTER. /*Param 340*/
DEFINE INPUT PARAMETER curr-room        AS CHARACTER.
DEFINE INPUT PARAMETER kreditlimit      AS DECIMAL. /*Dari api /vhpOU/restInvOpenTable*/
DEFINE INPUT PARAMETER roomtf-code      AS CHARACTER.
DEFINE INPUT PARAMETER roomtf-resnr     AS INTEGER.
DEFINE INPUT PARAMETER roomtf-reslinnr  AS INTEGER.
DEFINE INPUT PARAMETER dept-mbar        AS INTEGER.
DEFINE INPUT PARAMETER dept-ldry        AS INTEGER.
DEFINE INPUT-OUTPUT PARAMETER bilrecid  AS INTEGER.
DEFINE OUTPUT PARAMETER mess-info       AS CHARACTER.
DEFINE OUTPUT PARAMETER mess-quest1     AS CHARACTER.
DEFINE OUTPUT PARAMETER mess-quest2     AS CHARACTER.
DEFINE OUTPUT PARAMETER vSuccess        AS LOGICAL INITIAL NO.
DEFINE OUTPUT PARAMETER vClosed         AS LOGICAL INITIAL NO.

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
DEFINE VARIABLE balance             AS DECIMAL.
DEFINE VARIABLE paid                AS DECIMAL.
DEFINE VARIABLE billart             AS INTEGER.
DEFINE VARIABLE qty                 AS INTEGER.
DEFINE VARIABLE price               AS DECIMAL.
DEFINE VARIABLE amount-foreign      AS DECIMAL.
DEFINE VARIABLE amount              AS DECIMAL.
DEFINE VARIABLE gname               AS CHARACTER.
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

DEFINE VARIABLE connect-param       AS CHAR    NO-UNDO.
DEFINE VARIABLE connect-paramSSL    AS CHAR   NO-UNDO.
DEFINE VARIABLE lreturn             AS LOGICAL NO-UNDO INIT NO.
DEFINE VARIABLE htl-name            AS CHARACTER.
DEFINE VARIABLE cc-comment          AS CHARACTER.
DEFINE VARIABLE success-flag        AS LOGICAL NO-UNDO INIT NO.
DEFINE VARIABLE var-testing         AS CHAR.
DEFINE VARIABLE rec-id-artikel      AS INT.
DEFINE VARIABLE service-code        AS INT.
DEFINE VARIABLE rechnr              AS INT.

/****************************************************************************************/
DEFINE VARIABLE hServer             AS HANDLE NO-UNDO.
CREATE SERVER hServer.

IF vKey EQ "checkRoomTfCombo" THEN
DO:
    FIND FIRST h-bill WHERE RECID(h-bill) EQ h-recid NO-LOCK NO-ERROR.
    IF AVAILABLE h-bill THEN
    DO:
        balance-foreign = h-bill.mwst[99].
        balance = h-bill.saldo.

        CREATE t-h-bill.
        BUFFER-COPY h-bill TO t-h-bill.
    END.
    FIND FIRST t-h-bill NO-ERROR.

    /*Connect to Other DB*/
    connect-param = "-H " + ENTRY(1, pf-file2, ":") + " -S "
        + ENTRY(2, pf-file2, ":") 
        + " -DirectConnect -sessionModel Session-free".
    connect-paramSSL = connect-param + " -ssl -nohostverify".

    lreturn = hServer:CONNECT(connect-paramSSL, ?, ?, ?) NO-ERROR.
    IF NOT lreturn THEN lreturn = hServer:CONNECT(connect-param, ?, ?, ?) NO-ERROR.

    IF lreturn THEN RUN read-hotelnamebl.p ON hServer ("A120", OUTPUT htl-name).

    IF roomtf-code NE "" AND (curr-dept EQ dept-mbar OR curr-dept EQ dept-ldry) THEN fl-code = 1.
    ELSE IF roomtf-code NE "" AND curr-dept NE dept-mbar AND curr-dept NE dept-ldry THEN fl-code = 2.

    RUN ts-rzinr-btn-exitbl.p  
        ON hServer(language-code, fl-code, roomtf-code, roomtf-resnr,  
        roomtf-reslinnr, balance, OUTPUT bilrecid,  
        OUTPUT msg-str, OUTPUT msg-str1, OUTPUT msg-str2).
    
    IF msg-str NE "" THEN
    DO:
        IF fl-code EQ 1 THEN
        DO:
            mess-quest1 = SUBSTR(msg-str,4).
        END.
        ELSE IF fl-code EQ 2 THEN
        DO:
            mess-info = SUBSTR(msg-str,2).
            RETURN.
        END.
    END.
    IF msg-str1 NE "" THEN
    DO:
        mess-quest2 = SUBSTR(msg-str1,4).
    END.
    IF msg-str2 NE "" THEN
    DO:
        mess-info = msg-str2.
        RETURN.
    END.

    /*Disconnect Other DB*/
    hServer:DISCONNECT() NO-ERROR.
    DELETE OBJECT hServer NO-ERROR.

    vSuccess = YES.
END.
ELSE IF vKey EQ "postRoomTfCombo" THEN
DO:
    RUN prepare-ts-restinv_1bl.p(language-code, curr-dept, 1, user-init, ?,
            OUTPUT mealcoupon-cntrl, OUTPUT must-print, OUTPUT zero-flag,
            OUTPUT multi-cash, OUTPUT cancel-exist, OUTPUT msg-str,
            OUTPUT disc-art1, OUTPUT disc-art2, OUTPUT disc-art3,
            OUTPUT mi-ordertaker, OUTPUT price-decimal, OUTPUT curr-local,
            OUTPUT curr-foreign, OUTPUT double-currency, OUTPUT foreign-rate,
            OUTPUT exchg-rate, OUTPUT b-title, OUTPUT deptname, OUTPUT p-223,
            OUTPUT curr-waiter, OUTPUT fl-code, OUTPUT pos1, OUTPUT pos2,
            OUTPUT cashless-flag, OUTPUT c-param870, OUTPUT activate-deposit,
            OUTPUT TABLE hbill, OUTPUT TABLE t-kellner).
    
    FIND FIRST hbill NO-ERROR.
    FIND FIRST t-kellner NO-ERROR.
    
    IF msg-str NE "" THEN
    DO:
        mess-info = SUBSTR(msg-str,2).
        RETURN.
    END.
    
    FIND FIRST h-bill WHERE RECID(h-bill) EQ h-recid NO-LOCK NO-ERROR.
    IF AVAILABLE h-bill THEN
    DO:
        balance-foreign = h-bill.mwst[99].
        balance = h-bill.saldo.
    
        CREATE t-h-bill.
        BUFFER-COPY h-bill TO t-h-bill.
    END.
    FIND FIRST t-h-bill NO-ERROR.
    
    /*Connect to Other DB*/
    connect-param = "-H " + ENTRY(1, pf-file2, ":") + " -S "
        + ENTRY(2, pf-file2, ":") 
        + " -DirectConnect -sessionModel Session-free".
    connect-paramSSL = connect-param + " -ssl -nohostverify".
    
    lreturn = hServer:CONNECT(connect-paramSSL, ?, ?, ?) NO-ERROR.
    IF NOT lreturn THEN lreturn = hServer:CONNECT(connect-param, ?, ?, ?) NO-ERROR.
    
    IF lreturn THEN RUN read-hotelnamebl.p ON hServer ("A120", OUTPUT htl-name).
    
    RUN combo-transfer-bill_1bl.p ON hServer (language-code, 1, curr-dept, deptname, 
        bill-no, ?, double-currency, exchg-rate, bilrecid, 
        foreign-rate, user-init, balance, balance-foreign,
        OUTPUT cc-comment, OUTPUT success-flag, OUTPUT msg-str, OUTPUT gname).
    
    /*Disconnect Other DB*/
    hServer:DISCONNECT() NO-ERROR.
    DELETE OBJECT hServer NO-ERROR.
    
    IF msg-str NE "" THEN
    DO:
        mess-info = msg-str.
        RETURN.
    END.
    
    IF success-flag THEN
    DO:
        paid = - balance.
    
        /* city ledger */
        RUN ts-restinv-btn-transfer-paytype1bl.p
            (language-code, t-h-bill.rec-id, guestnr, curr-dept,
            paid, exchg-rate, price-decimal, balance, ?,
            disc-art1, disc-art2, disc-art3, t-kellner.kellner-nr,
            OUTPUT billart, OUTPUT qty,
            OUTPUT description, OUTPUT price, OUTPUT amount-foreign,
            OUTPUT amount, OUTPUT bill-date, OUTPUT fl-code,
            OUTPUT fl-code1, OUTPUT msg-str, OUTPUT var-testing,
            OUTPUT TABLE t-h-artikel).
        FIND FIRST t-h-artikel NO-ERROR.
    
        IF msg-str NE "" THEN
        DO:
            mess-info = msg-str.
            RETURN.
        END.
        IF fl-code EQ 1 THEN
        DO:
            fl-code = 0.
            IF NOT AVAILABLE t-h-artikel THEN
            DO:
                rec-id-artikel = 0.
                service-code = 0.
            END.
            ELSE
            DO:
                rec-id-artikel = t-h-artikel.rec-id.
                service-code = t-h-artikel.service-code.
            END.
    
            RUN ts-restinv-update-bill_1bl.p
                (language-code, h-recid, rec-id-artikel, deptname, ?,
                t-h-artikel.artart, NO, service-code, amount,
                amount-foreign, price, double-currency, qty, exchg-rate, price-decimal, 0,
                tischnr, curr-dept, user-init, gname, pax, kreditlimit,
                1, billart, description, "", cc-comment,
                "", "", "", "", YES,
                NO, t-h-artikel.artnrfront, 1, guestnr, "",
                NO, foreign-rate, curr-room, user-init,
                0, 0, NO, 0, "", 
                INPUT TABLE t-submenu-list, OUTPUT bill-date,
                OUTPUT cancel-flag, OUTPUT fl-code, OUTPUT mwst,
                OUTPUT mwst-foreign, OUTPUT rechnr, OUTPUT balance,
                OUTPUT bcol, OUTPUT balance-foreign, OUTPUT fl-code1,
                OUTPUT fl-code2, OUTPUT fl-code3, OUTPUT p-88, OUTPUT vClosed,
                OUTPUT TABLE t-h-bill, OUTPUT TABLE kellner1).
    
            FIND FIRST t-h-bill NO-ERROR.
            FIND FIRST kellner1 NO-ERROR.
    
            IF fl-code EQ 1 THEN
            DO:
                mess-info = "Transaction not allowed: Posted item(s) with differrent billing date found.".
                RETURN.
            END.
            ELSE IF fl-code EQ 2 THEN RETURN.
    
            IF t-h-artikel.artart EQ 2 AND vClosed THEN
            DO:
                RUN ts-restsale-update-h-billbl.p(t-h-bill.rec-id).
                RUN ts-restinv-del-queasybl.p(INPUT-OUTPUT TABLE p-list, t-h-bill.rec-id, NO).
            END.
        END.
        ELSE IF fl-code EQ 2 THEN
        DO:
            mess-info = "NOT DEFINED: F/O Article" + " " + STRING(billart)
                + CHR(10) + "C/L Posting not possible.".
            RETURN.
        END.
        ELSE IF fl-code EQ 3 THEN
        DO:
            mess-info = "F/O Article not available.".
            RETURN.
        END.
    END.
    vSuccess = YES.
END.



