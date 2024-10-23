DEF TEMP-TABLE hbill
    FIELD kellner-nr LIKE h-bill.kellner-nr.

DEF TEMP-TABLE t-kellner
    FIELD kellner-nr LIKE kellner.kellner-nr.

DEF TEMP-TABLE t-h-artikel LIKE h-artikel
    FIELD rec-id AS INTEGER.

DEFINE TEMP-TABLE menu-list
    FIELD artnr           AS INTEGER
    FIELD DESCRIPTION     AS CHARACTER
    FIELD qty             AS INTEGER
    FIELD price           AS DECIMAL
    FIELD special-request AS CHARACTER.

DEF TEMP-TABLE t-h-bill LIKE h-bill
    FIELD rec-id AS INT.

DEF TEMP-TABLE t-submenu-list
    FIELD menurecid    AS INTEGER 
    FIELD zeit         AS INTEGER 
    FIELD nr           AS INTEGER 
    FIELD artnr        LIKE h-artikel.artnr 
    FIELD bezeich      LIKE h-artikel.bezeich 
    FIELD anzahl       AS INTEGER 
    FIELD zknr         AS INTEGER 
    FIELD request      AS CHAR. 

DEF TEMP-TABLE kellner1   LIKE kellner. 

DEFINE INPUT PARAMETER user-init    AS CHARACTER.
DEFINE INPUT PARAMETER tableNumber  AS INTEGER.
DEFINE INPUT PARAMETER outletNumber AS INTEGER.
DEFINE INPUT PARAMETER guestName    AS CHARACTER.
DEFINE INPUT PARAMETER pax          AS INTEGER.
DEFINE INPUT PARAMETER orderid      AS INTEGER.

DEFINE INPUT PARAMETER TABLE FOR menu-list.
DEFINE OUTPUT PARAMETER billNumber    AS INT.
DEFINE OUTPUT PARAMETER returnMessage AS CHAR.

DEFINE VARIABLE guestnr       AS INTEGER.
DEFINE VARIABLE tischnr       AS INTEGER.
DEFINE VARIABLE record-id     AS INTEGER.
DEFINE VARIABLE language-code AS INTEGER NO-UNDO.
DEFINE VARIABLE curr-room     AS CHARACTER.
DEFINE VARIABLE resnr         AS INTEGER.
DEFINE VARIABLE reslinnr      AS INTEGER.
DEFINE VARIABLE curr-dept     AS INTEGER.
DEFINE VARIABLE gName         AS CHARACTER.

DEFINE VARIABLE amount           LIKE bill-line.betrag.
DEFINE VARIABLE mealcoupon-cntrl AS LOGICAL.
DEFINE VARIABLE must-print       AS LOGICAL.
DEFINE VARIABLE zero-flag        AS LOGICAL.
DEFINE VARIABLE multi-cash       AS LOGICAL.
DEFINE VARIABLE cancel-exist     AS LOGICAL INIT NO.
DEFINE VARIABLE msg-str          AS CHAR.

DEFINE VARIABLE disc-art1        AS INT.
DEFINE VARIABLE disc-art2        AS INT.
DEFINE VARIABLE disc-art3        AS INT.
DEFINE VARIABLE mi-ordertaker    AS LOGICAL INIT YES.
DEFINE VARIABLE price-decimal    AS INT.
DEFINE VARIABLE curr-local       AS CHAR.
DEFINE VARIABLE curr-foreign     AS CHAR.
DEFINE VARIABLE double-currency  AS LOGICAL.
DEFINE VARIABLE foreign-rate     AS LOGICAL.
DEFINE VARIABLE exchg-rate       AS DECIMAL INIT 1.
DEFINE VARIABLE b-title          AS CHAR.
DEFINE VARIABLE deptname         AS CHAR.
DEFINE VARIABLE p-223            AS LOGICAL.
DEFINE VARIABLE curr-waiter      AS INT INIT 0.
DEFINE VARIABLE fl-code          AS INT INIT 0.
DEFINE VARIABLE pos1             AS INT.
DEFINE VARIABLE pos2             AS INT.
DEFINE VARIABLE cashless-flag    AS LOGICAL NO-UNDO.

DEFINE VARIABLE price            AS DECIMAL.   
DEFINE VARIABLE add-zeit         AS INTEGER INIT 0.

DEFINE VARIABLE bill-date        AS DATE.
DEFINE VARIABLE cancel-flag      AS LOGICAL.
DEFINE VARIABLE mwst             LIKE vhp.h-bill-line.betrag INIT 0.
DEFINE VARIABLE mwst-foreign     LIKE vhp.h-bill-line.betrag INIT 0.
DEFINE VARIABLE balance          AS DECIMAL.
DEFINE VARIABLE bcol             AS INT.
DEFINE VARIABLE balance-foreign  AS DECIMAL.
DEFINE VARIABLE fl-code1         AS INT INIT 0.
DEFINE VARIABLE fl-code2         AS INT INIT 0.
DEFINE VARIABLE fl-code3         AS INT INIT 0.
DEFINE VARIABLE p-88             AS LOGICAL.
DEFINE VARIABLE closed           AS LOGICAL.
DEFINE VARIABLE doit             AS LOGICAL INIT NO.
                                 
DEFINE VARIABLE error-str        AS CHAR INITIAL "" NO-UNDO.
DEFINE VARIABLE active-flag      AS INTEGER INIT 1 NO-UNDO.
DEFINE VARIABLE deptNo           AS INTEGER.
/*
MESSAGE
    "language-code: " + string(language-code) skip
    "record-id    : " + string(record-id    ) skip
    "tischnr      : " + string(tischnr      ) skip
    "curr-dept    : " + string(curr-dept    ) skip
    "user-init    : " + string(user-init    ) skip
    "gname        : " + string(gname        ) skip
    "pax          : " + string(pax          ) skip
    "guestnr      : " + string(guestnr      ) skip
    "curr-room    : " + string(curr-room    ) skip
    "resnr        : " + string(resnr        ) skip
    "reslinnr     : " + string(reslinnr     )
    VIEW-AS ALERT-BOX INFO BUTTONS OK.
*/
returnmessage = "".

tischnr   = tableNumber.
curr-dept = outletNumber.
gName     = guestName.

IF (tischnr EQ 0 OR tischnr EQ ? ) THEN
DO:
    returnmessage = "1 - Table Number cannot be empty!".
    RETURN. 
END.

IF (curr-dept EQ 0 OR curr-dept EQ ?) THEN
DO:
    returnmessage = "2 - Outlet Number cannot be empty!".
    RETURN. 
END.

FIND FIRST queasy WHERE queasy.KEY EQ 270 
    AND queasy.number1 EQ 1 
    AND queasy.betriebsnr EQ curr-dept
    AND queasy.number2 EQ 4 NO-LOCK NO-ERROR.
IF AVAILABLE queasy THEN deptNo = INT(queasy.char2).

RUN prepare-tada-post-menubl.p (language-code, curr-dept, /*curr-printer*/ 0 , user-init, ?,
   OUTPUT mealcoupon-cntrl, OUTPUT must-print, OUTPUT zero-flag,
   OUTPUT multi-cash, OUTPUT cancel-exist, OUTPUT msg-str,
   OUTPUT disc-art1, OUTPUT disc-art2, OUTPUT disc-art3,
   OUTPUT mi-ordertaker, OUTPUT price-decimal, OUTPUT curr-local,
   OUTPUT curr-foreign, OUTPUT double-currency, OUTPUT foreign-rate,
   OUTPUT exchg-rate, OUTPUT b-title, OUTPUT deptname, OUTPUT p-223,
   OUTPUT curr-waiter, OUTPUT fl-code, OUTPUT pos1, OUTPUT pos2,
   OUTPUT cashless-flag, OUTPUT TABLE hbill, OUTPUT TABLE t-kellner).

FIND FIRST t-kellner NO-LOCK NO-ERROR.
FIND FIRST h-bill WHERE h-bill.departement EQ curr-dept 
    AND h-bill.flag EQ 0 
    AND h-bill.tischnr EQ tischnr NO-LOCK NO-ERROR.
IF AVAILABLE h-bill THEN
DO:
     record-id = RECID(h-bill).
END.
ELSE record-id = 0.

DEFINE VARIABLE err       AS LOGICAL.  
DEFINE VARIABLE err1      AS LOGICAL.  
DEFINE VARIABLE fract     AS DECIMAL INITIAL 1 NO-UNDO. 
DEFINE VARIABLE vhp-itemnumber AS INTEGER.

FOR EACH menu-list:   
    vhp-itemnumber = 0.
    FIND FIRST queasy WHERE queasy.KEY EQ 270
        AND queasy.number1 EQ 2
        AND queasy.betriebsnr EQ curr-dept
        AND queasy.number2 EQ menu-list.artnr NO-LOCK NO-ERROR.
    IF AVAILABLE queasy THEN
    DO:
        vhp-itemnumber = queasy.number3.
    END.
    ELSE
    DO:                
        returnmessage = "1 - Article not mapping yet, posting not possible!".
        RETURN.       
    END.

    add-zeit = add-zeit + 1.
    FIND FIRST h-artikel WHERE h-artikel.departement EQ curr-dept
        AND h-artikel.artnr EQ vhp-itemnumber NO-LOCK NO-ERROR.
    
    IF record-id EQ 0 THEN
    DO:
        FIND FIRST t-h-bill NO-LOCK NO-ERROR.
        IF AVAILABLE t-h-bill THEN
        DO:
            record-id = t-h-bill.rec-id.
        END.
    END.
    
    IF h-artikel.epreis1 NE 0 THEN
    DO:
        RUN ts-hbline-get-pricebl.p (h-artikel.artnr, curr-dept, OUTPUT err, 
                                     OUTPUT err1, OUTPUT price, OUTPUT fract).  
    END.
    ELSE
    DO:
        price = menu-list.price.
    END.
    
    amount = price * menu-list.qty.

    RUN tada-update-billbl.p (language-code, 
                                    record-id, 
                                    RECID(h-artikel),
                                    "",
                                    ?,
                                    h-artikel.artart,
                                    NO, 
                                    h-artikel.service-code, 
                                    amount,
                                    0, 
                                    price, 
                                    double-currency, 
                                    menu-list.qty,
                                    exchg-rate, 
                                    price-decimal,
                                    user-init,
                                    tischnr, 
                                    curr-dept,
                                    user-init,
                                    gname,
                                    pax,
                                    0,
                                    add-zeit, 
                                    h-artikel.artnr,
                                    h-artikel.bezeich,
                                    "",
                                    "",
                                    "", 
                                    menu-list.special-request, 
                                    "", 
                                    "", 
                                    YES,
                                    NO, 
                                    h-artikel.artnrfront, 
                                    0, 
                                    guestnr, 
                                    "",
                                    NO, 
                                    foreign-rate, 
                                    curr-room,
                                    user-init,
                                    resnr, 
                                    reslinnr,
                                    INPUT TABLE t-submenu-list, 
                                    OUTPUT bill-date,
                                    OUTPUT cancel-flag,
                                    OUTPUT fl-code, 
                                    OUTPUT mwst,
                                    OUTPUT mwst-foreign,
                                    OUTPUT billNumber,
                                    OUTPUT balance,
                                    OUTPUT bcol, 
                                    OUTPUT balance-foreign, 
                                    OUTPUT fl-code1,
                                    OUTPUT fl-code2, 
                                    OUTPUT fl-code3, 
                                    OUTPUT p-88, 
                                    OUTPUT closed,
                                    OUTPUT TABLE t-h-bill, 
                                    OUTPUT TABLE kellner1).
    
    FIND FIRST t-h-bill NO-LOCK NO-ERROR.
    IF AVAILABLE t-h-bill THEN
    DO:
        billNumber = t-h-bill.rechnr.
    END.
    doit = YES.
END.

IF doit = YES THEN
DO:
    FIND FIRST bediener WHERE bediener.userinit EQ TRIM(user-init) NO-LOCK NO-ERROR.
    returnmessage = "0 - Post Menu Success".
    
    DEFINE BUFFER orderhdr  FOR queasy.
    DEFINE BUFFER orderline FOR queasy.
    DEFINE VARIABLE strchar AS CHAR.

    FIND FIRST orderhdr WHERE orderhdr.KEY EQ 271 
        AND orderhdr.betriebsnr EQ 1 
        AND orderhdr.number1 EQ deptNo
        AND orderhdr.number2 EQ orderid NO-LOCK NO-ERROR.
    IF AVAILABLE orderhdr THEN
    DO:
        strchar = orderhdr.char2. 
        FIND CURRENT orderhdr EXCLUSIVE-LOCK.
        ASSIGN 
            orderhdr.logi1   = YES
            orderhdr.number3 = billNumber
            orderhdr.char2   = ENTRY(1,strchar,"|") + "|" + STRING(tableNumber) + "|" + ENTRY(3,strchar,"|") + "|" + ENTRY(4,strchar,"|") + "|" + ENTRY(5,strchar,"|") + "|" + ENTRY(6,strchar,"|")
            .
        FIND CURRENT orderhdr NO-LOCK.
        RELEASE orderhdr.
    END.

    FOR EACH menu-list:
        FIND FIRST orderline WHERE orderline.KEY EQ 271 
            AND orderline.betriebsnr EQ 2 
            AND orderline.number2 EQ orderid 
            AND orderline.number1 EQ menu-list.artnr NO-LOCK NO-ERROR.
        IF AVAILABLE orderline THEN
        DO:
            FIND CURRENT orderline EXCLUSIVE-LOCK.
            ASSIGN 
                orderline.logi1   = YES
                orderline.number3 = billNumber
                .
            FIND CURRENT orderline NO-LOCK.
            RELEASE orderline.
        END.
    END.

END.

RUN add-kitchprbl.p (language-code, "", curr-dept, billNumber, bill-date, user-init, OUTPUT error-str).



