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

DEFINE TEMP-TABLE crd-list
    FIELD deptno AS INT
    FIELD uname  AS CHAR
    FIELD pass   AS CHAR
    FIELD tada-outlet-id AS INT.

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
    returnmessage = "You must enter a table number before proceeding".
    RETURN. 
END.

IF (curr-dept EQ 0 OR curr-dept EQ ?) THEN
DO:
    returnmessage = "Please enter an outlet number".
    RETURN. 
END.

FOR EACH queasy WHERE queasy.KEY EQ 270 AND queasy.number1 EQ 1 NO-LOCK BY queasy.betriebsnr BY queasy.number2:
    IF (queasy.number2 EQ 27 OR queasy.number2 EQ 28 OR queasy.number2 EQ 29 OR queasy.number2 EQ 30) THEN
    DO:
        IF NUM-ENTRIES(queasy.char2,";") GE 2 THEN
        DO:
            CREATE crd-list.
            ASSIGN 
                crd-list.deptno = INT(ENTRY(1,queasy.char2,";"))
                crd-list.uname  = ENTRY(2,queasy.char2,";")
                crd-list.pass   = ENTRY(3,queasy.char2,";")
                crd-list.tada-outlet-id = INT(ENTRY(4,queasy.char2,";")).
        END.
    END.

    /*IF queasy.number2 EQ 5 THEN tableno = INT(queasy.char2).*/
END.

FIND FIRST crd-list WHERE crd-list.deptno EQ curr-dept NO-ERROR.
IF AVAILABLE crd-list THEN deptno = crd-list.tada-outlet-id.

/*
FIND FIRST queasy WHERE queasy.KEY EQ 270 
    AND queasy.number1 EQ 1 
    AND queasy.betriebsnr EQ curr-dept
    AND queasy.number2 EQ 4 NO-LOCK NO-ERROR.
IF AVAILABLE queasy THEN deptNo = INT(queasy.char2).
*/
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
DEFINE VARIABLE strchar AS CHAR.
DEFINE VARIABLE tmp-menu-name AS CHAR.

/*CHECK DISCOUNT*/
DEFINE BUFFER mn-list   FOR menu-list.
DEFINE BUFFER orderhdr  FOR queasy.
DEFINE BUFFER orderline FOR queasy.

FOR EACH orderline WHERE orderline.KEY EQ 271 
    AND orderline.betriebsnr EQ 2 
    AND orderline.number2 EQ orderid
    AND orderline.logi1 EQ NO NO-LOCK.
    FIND FIRST mn-list WHERE mn-list.artnr EQ orderline.number1 NO-LOCK NO-ERROR.
    IF NOT AVAILABLE mn-list THEN
    DO:
        tmp-menu-name = ENTRY(2,orderline.char1,"|").
        IF tmp-menu-name MATCHES "*DISC*" THEN
        DO:
            CREATE menu-list.
            ASSIGN 
                menu-list.artnr           = orderline.number1 
                menu-list.DESCRIPTION     = tmp-menu-name
                menu-list.qty             = INT(ENTRY(1,orderline.char1,"|"))
                menu-list.price           = DEC(ENTRY(4,orderline.char1,"|"))
                menu-list.special-request = "". 
        END.
    END.
END.

/*CHECK MAPPING*/
FOR EACH menu-list:
    IF NOT menu-list.DESCRIPTION MATCHES "*DISC*" THEN
    DO:
        FIND FIRST queasy WHERE queasy.KEY EQ 270
            AND queasy.number1 EQ 2
            AND queasy.betriebsnr EQ curr-dept
            AND queasy.number2 EQ menu-list.artnr NO-LOCK NO-ERROR.
        IF NOT AVAILABLE queasy THEN
        DO:             
            returnmessage = "Posting is not possible because the article has not been mapped yet.".
            RETURN.       
        END.
    END.
END.

FOR EACH menu-list: 
    /*MESSAGE menu-list.DESCRIPTION
        VIEW-AS ALERT-BOX INFO BUTTONS OK.*/
    vhp-itemnumber = 0.
    IF NOT menu-list.DESCRIPTION MATCHES "*DISC*" THEN
    DO:
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
            returnmessage = "Posting is not possible because the article has not been mapped yet.".
            RETURN.       
        END.
    END.
    ELSE 
    DO:
        vhp-itemnumber = menu-list.artnr. 
        menu-list.price = - menu-list.price.
    END.
        
    add-zeit = add-zeit + 1.
    FIND FIRST h-artikel WHERE h-artikel.departement EQ curr-dept AND h-artikel.artnr EQ vhp-itemnumber NO-LOCK NO-ERROR.
    IF NOT AVAILABLE h-artikel THEN
    DO:
        returnmessage = "Posting is not possible because the article has not been mapped yet.".
        RETURN.    
    END.
    
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
                                    /*h-artikel.bezeich*/ menu-list.DESCRIPTION,
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
    DEFINE VARIABLE order-phone AS CHAR.
    DEFINE VARIABLE order-name  AS CHAR.
    DEFINE VARIABLE order-email AS CHAR.
    DEFINE VARIABLE curr-gastnr AS INT.

    FIND FIRST bediener WHERE bediener.userinit EQ TRIM(user-init) NO-LOCK NO-ERROR.
    returnmessage = "Post Menu Success".

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

        order-phone = ENTRY(6,strchar,"|").
        order-name  = ENTRY(3,strchar,"|").
        order-email = ENTRY(5,strchar,"|").
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

    /*create guestcard*/

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
            /*guest.zahlungsart   = payment-param.
            guest.point-gastnr  = payment-param.*/
            gastnr = curr-gastnr.
        END.
        ELSE 
        DO:
            guest.NAME          = order-name.
            guest.email-adr     = order-email.
            guest.telefon       = order-phone.
            guest.mobil-telefon = order-phone.
            /*guest.zahlungsart   = payment-param.
            guest.point-gastnr  = payment-param.*/
        END.
    END.
    ELSE
    DO:
        guest.NAME          = order-name.
        guest.email-adr     = order-email.
        guest.telefon       = order-phone.
        guest.mobil-telefon = order-phone.
        /*guest.zahlungsart   = payment-param.
        guest.point-gastnr  = payment-param.*/
    END.
    RELEASE guest.
END.

RUN add-kitchprbl.p (language-code, "", curr-dept, billNumber, bill-date, user-init, OUTPUT error-str).



