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

DEFINE TEMP-TABLE t-kellner   LIKE kellner.

DEFINE INPUT PARAMETER pvILanguage          AS INTEGER NO-UNDO.
DEFINE INPUT PARAMETER rec-id               AS INTEGER. /*RECID Bill POS*/
DEFINE INPUT PARAMETER curr-dept            AS INTEGER.
DEFINE INPUT PARAMETER bilrecid             AS INTEGER. /*RECID Guest Bill from API rzinrbtnexit*/
DEFINE INPUT PARAMETER balance-foreign      AS DECIMAL.
DEFINE INPUT PARAMETER balance              AS DECIMAL.
DEFINE INPUT PARAMETER pay-type             AS INTEGER. /*Harcode=2*/
DEFINE INPUT PARAMETER transdate            AS DATE.    /*From payload API restInvUpdateBill1*/
DEFINE INPUT PARAMETER double-currency      AS LOGICAL. /*From output Prepare*/
DEFINE INPUT PARAMETER exchg-rate           AS DECIMAL. /*From output Prepare*/
DEFINE INPUT PARAMETER kellner1-kcredit-nr  AS INT.     /*From output Prepare*/
DEFINE INPUT PARAMETER foreign-rate         AS LOGICAL. /*From output Prepare*/
DEFINE INPUT PARAMETER user-init            AS CHAR.    
DEFINE INPUT PARAMETER price-decimal        AS INT.     /*From output Prepare*/
DEFINE INPUT PARAMETER rec-id-h-artikel     AS INT.     /*From API payload restInvUpdateBill1*/
DEFINE INPUT PARAMETER deptname             AS CHAR.    /*From API payload restInvUpdateBill1*/
DEFINE INPUT PARAMETER h-artart             AS INT.     /*From API payload restInvUpdateBill1*/
DEFINE INPUT PARAMETER cancel-order         AS LOGICAL. /*From API payload restInvUpdateBill1*/
DEFINE INPUT PARAMETER h-artikel-service-code  AS INT.     /*From API payload restInvUpdateBill1*/
DEFINE INPUT PARAMETER order-taker          AS INT.     /*From API payload restInvUpdateBill1*/
DEFINE INPUT PARAMETER tischnr              AS INT.     /*From API payload restInvUpdateBill1*/
DEFINE INPUT PARAMETER curr-waiter          AS INT.     /*From API payload restInvUpdateBill1*/
DEFINE INPUT PARAMETER pax                  AS INT.     /*From API payload restInvUpdateBill1*/
DEFINE INPUT PARAMETER kreditlimit          AS DECIMAL. /*From API payload restInvUpdateBill1*/
DEFINE INPUT PARAMETER add-zeit             AS INT.     /*From API payload restInvUpdateBill1*/
DEFINE INPUT PARAMETER print-to-kitchen     AS LOGICAL. /*From API payload restInvUpdateBill1*/
DEFINE INPUT PARAMETER from-acct            AS LOGICAL. /*From API payload restInvUpdateBill1*/
DEFINE INPUT PARAMETER h-artnrfront         AS INT.     /*From API payload restInvUpdateBill1*/
DEFINE INPUT PARAMETER guestnr              AS INT.     /*From API payload restInvUpdateBill1*/
DEFINE INPUT PARAMETER curedept-flag        AS LOGICAL. /*From API payload restInvUpdateBill1*/
DEFINE INPUT PARAMETER curr-room            AS CHAR.    /*From API payload restInvUpdateBill1*/
DEFINE INPUT PARAMETER hoga-resnr           AS INTEGER. /*From API payload restInvUpdateBill1*/
DEFINE INPUT PARAMETER hoga-reslinnr        AS INTEGER. /*From API payload restInvUpdateBill1*/
DEFINE INPUT PARAMETER incl-vat             AS LOGICAL. /*From API payload restInvUpdateBill1*/
DEFINE INPUT PARAMETER get-price            AS INTEGER. /*From API payload restInvUpdateBill1*/
DEFINE INPUT PARAMETER mc-str               AS CHAR.    /*From API payload restInvUpdateBill1*/
DEFINE INPUT PARAMETER disc-art1            AS INT.     /*From output Prepare*/
DEFINE INPUT PARAMETER disc-art2            AS INT.     /*From output Prepare*/
DEFINE INPUT PARAMETER disc-art3            AS INT.     /*From output Prepare*/
DEFINE INPUT PARAMETER TABLE FOR t-submenu-list.        /*From API payload restInvUpdateBill1*/
DEFINE OUTPUT PARAMETER bill-date           AS DATE.
DEFINE OUTPUT PARAMETER cancel-flag         AS LOGICAL.
DEFINE OUTPUT PARAMETER mwst                LIKE h-bill-line.betrag INIT 0.
DEFINE OUTPUT PARAMETER mwst-foreign        LIKE h-bill-line.betrag INIT 0.
DEFINE OUTPUT PARAMETER rechnr              AS INT.
DEFINE OUTPUT PARAMETER bcol                AS INT.
DEFINE OUTPUT PARAMETER p-88                AS LOGICAL.
DEFINE OUTPUT PARAMETER closed              AS LOGICAL.
DEFINE OUTPUT PARAMETER avail-bill          AS LOGICAL.
DEFINE OUTPUT PARAMETER billno-str          AS CHAR.
DEFINE OUTPUT PARAMETER cancel-str          AS CHAR.
DEFINE OUTPUT PARAMETER error-message       AS CHAR.
DEFINE OUTPUT PARAMETER TABLE FOR t-h-bill.
DEFINE OUTPUT PARAMETER TABLE FOR t-kellner.


{SupertransBL.i}
DEF VAR lvCAREA AS CHAR INITIAL "TS-restinv-transfer-to-guestbill-web".

DEFINE VARIABLE billart-bfo         AS INT.
DEFINE VARIABLE billart             AS INT.
DEFINE VARIABLE qty                 AS INT.
DEFINE VARIABLE qty-bfo             AS INT.
DEFINE VARIABLE price               AS DECIMAL.
DEFINE VARIABLE amount-foreign      LIKE vhp.bill-line.betrag.
DEFINE VARIABLE amount              LIKE vhp.bill-line.betrag.
DEFINE VARIABLE gname               AS CHAR.
DEFINE VARIABLE description         AS CHAR.
DEFINE VARIABLE description-bfo     AS CHAR.
DEFINE VARIABLE transfer-zinr       AS CHAR.
DEFINE VARIABLE fl-code             AS INT INIT 0.
DEFINE VARIABLE fl-code1            AS INT INIT 0.
DEFINE VARIABLE fl-code2            AS INT INIT 0.
DEFINE VARIABLE fl-code3            AS INT INIT 0.
DEFINE VARIABLE flag-code           AS INT.


FIND FIRST bill WHERE RECID(bill) = bilrecid NO-LOCK NO-ERROR. 
IF NOT AVAILABLE bill THEN 
DO:
    error-message = "Record ID guest bill not found.".
    RETURN.
END.     
FIND FIRST h-bill WHERE RECID(h-bill) = rec-id NO-LOCK NO-ERROR.
IF NOT AVAILABLE h-bill THEN 
DO:
    error-message = "Record ID Outlet bill not found.".
    RETURN.
END.

IF curr-room        EQ ? THEN curr-room     = "".
IF user-init        EQ ? THEN user-init     = "".
IF mc-str           EQ ? THEN mc-str        = "".

DO TRANSACTION:
    /*ts-biltransferbl*/
    IF AVAILABLE bill THEN
    DO:
        FIND CURRENT h-bill EXCLUSIVE-LOCK NO-WAIT NO-ERROR.
        IF AVAILABLE h-bill THEN
        DO:
            ASSIGN
                h-bill.resnr = bill.resnr
                h-bill.reslinnr = bill.reslinnr.
            FIND CURRENT h-bill NO-LOCK.
        END.
    END.
    /*ts-biltransferbl*/
    
    /*ts-restinv-btn-transfer-paytypegt1bl*/ 
    qty = 1. 
    price = 0. 
    amount-foreign = - balance-foreign. 
    amount = - balance. 
    gname = "". 
    
    IF bill.rechnr EQ 0 THEN 
    DO: 
        FIND FIRST vhp.counters WHERE vhp.counters.counter-no EQ 3 EXCLUSIVE-LOCK. 
        counters.counter = counters.counter + 1. 
        FIND CURRENT counter NO-LOCK. 
        FIND CURRENT bill EXCLUSIVE-LOCK. 
        bill.rechnr = counters.counter. 
        FIND CURRENT bill NO-LOCK. 
    END. 
    
    IF pay-type EQ 2 THEN     /* room transfer */ 
    DO: 
        description = "RmNo " + bill.zinr + " *" + STRING(bill.rechnr). 
        transfer-zinr = bill.zinr. 
        FIND FIRST res-line WHERE res-line.resnr EQ bill.resnr 
            AND res-line.reslinnr EQ bill.reslinnr NO-LOCK NO-ERROR. 
        IF AVAILABLE res-line AND AVAILABLE h-bill THEN 
        DO: 
            gname = vhp.res-line.name. 
            FIND CURRENT h-bill EXCLUSIVE-LOCK. 
            h-bill.bilname = gname. 
            FIND CURRENT h-bill NO-LOCK. 
        END.     
    END. 
    /*ts-restinv-btn-transfer-paytypegt1bl*/
    
    FIND FIRST kellner WHERE kellner.kellner-nr EQ h-bill.kellner-nr 
        AND kellner.departement EQ curr-dept NO-LOCK NO-ERROR.
    IF AVAILABLE kellner THEN
    DO:
        CREATE t-kellner.
        BUFFER-COPY kellner TO t-kellner.
    END.
    FIND FIRST t-kellner NO-ERROR.

    /*Update to Guest Bill*/
    RUN ts-restinv-update-bill1bl.p (rec-id, transdate, double-currency, exchg-rate,
            t-kellner.kcredit-nr, bilrecid, foreign-rate, user-init, gname,
            hoga-resnr, hoga-reslinnr, price-decimal,
            INPUT-OUTPUT amount, INPUT-OUTPUT amount-foreign,
            OUTPUT bill-date, OUTPUT billart-bfo, OUTPUT qty-bfo, OUTPUT description-bfo, OUTPUT cancel-str, OUTPUT TABLE t-h-bill).

    /*Update to Bill POS*/
    FIND CURRENT h-bill EXCLUSIVE-LOCK. 
    h-bill.flag = 0. 
    FIND CURRENT h-bill NO-LOCK.

    RUN ts-restinv-update-bill_1bl.p
            (pvILanguage, rec-id, rec-id-h-artikel, deptname, transdate,
            h-artart, cancel-order, h-artikel-service-code, amount,
            amount-foreign, price, double-currency, qty, exchg-rate, price-decimal, order-taker,
            tischnr, curr-dept, curr-waiter, gname, pax, kreditlimit,
            add-zeit, billart, description, "", "",
            "", "", "", "", print-to-kitchen,
            from-acct, h-artnrfront, pay-type, guestnr, transfer-zinr,
            curedept-flag, foreign-rate, curr-room, user-init,
            hoga-resnr, hoga-reslinnr, incl-vat, get-price, mc-str, /*tambah disini ITA*/
            INPUT TABLE t-submenu-list, OUTPUT bill-date,
            OUTPUT cancel-flag, OUTPUT fl-code, OUTPUT mwst,
            OUTPUT mwst-foreign, OUTPUT rechnr, OUTPUT balance,
            OUTPUT bcol, OUTPUT balance-foreign, OUTPUT fl-code1,
            OUTPUT fl-code2, OUTPUT fl-code3, OUTPUT p-88, OUTPUT closed,
            OUTPUT TABLE t-h-bill, OUTPUT TABLE t-kellner).
    FIND FIRST t-h-bill NO-ERROR.
    FIND FIRST t-kellner NO-ERROR.

    /*IF fl-code EQ 1 THEN error-message = translateExtended("Transaction not allowed: Posted item(s) with differrent billing date found.",lvCAREA,"").*/
    IF fl-code2 EQ 1 THEN billno-str = translateExtended ("BillNo:",lvCAREA,"") + " " + STRING(rechnr).            

    IF AVAILABLE h-bill THEN
    DO:
        FIND CURRENT h-bill EXCLUSIVE-LOCK. 
        h-bill.rgdruck = 1. 
        FIND CURRENT h-bill NO-LOCK.
    END.

    RUN ts-restinv-btn-transfer-paytypegt1-2bl.p
        (rec-id, YES, transdate, curr-dept,
        disc-art1, disc-art2, disc-art3, /*t-kellner.kellner-nr*/ curr-waiter,
        OUTPUT bill-date, OUTPUT flag-code, OUTPUT TABLE t-h-bill). /* Bernatd chg t-kellner.kellner-nr -> curr-waiter 683B73 2024 */

    FIND FIRST t-h-bill NO-ERROR.
    avail-bill = AVAILABLE t-h-bill.
END.
