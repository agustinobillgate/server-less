
DEFINE TEMP-TABLE t-bill LIKE bill.
DEFINE TEMP-TABLE spbill-list
    FIELD selected AS LOGICAL INITIAL YES 
    FIELD bl-recid AS INTEGER.

DEFINE TEMP-TABLE t-bill-line LIKE bill-line
    FIELD rec-id AS INT.

DEFINE TEMP-TABLE tp-bediener  LIKE bediener.

DEFINE INPUT PARAMETER pvILanguage      AS INTEGER NO-UNDO.
DEFINE INPUT PARAMETER bill-recid       AS INTEGER.
DEFINE INPUT PARAMETER user-init        AS CHAR.
DEFINE INPUT PARAMETER curr-rechnr      AS INTEGER.
DEFINE INPUT PARAMETER res-number       AS INTEGER.
DEFINE INPUT PARAMETER resllin-number   AS INTEGER.
DEFINE INPUT PARAMETER bill-flag        AS INTEGER.
DEFINE INPUT PARAMETER transdate        AS DATE.
DEFINE INPUT PARAMETER tbill-flag       AS INTEGER.
DEFINE INPUT PARAMETER change-date      AS LOGICAL.
DEFINE INPUT PARAMETER pay-depoamount   AS DECIMAL.
DEFINE INPUT PARAMETER amount-foreign   AS DECIMAL.
DEFINE INPUT PARAMETER curr-room        AS CHAR.
DEFINE INPUT PARAMETER exchg-rate       AS DECIMAL INITIAL 1.
DEFINE INPUT PARAMETER price-decimal    AS INTEGER.
DEFINE INPUT PARAMETER double-currency  AS LOGICAL.
DEFINE INPUT PARAMETER p-83             AS LOGICAL.
DEFINE INPUT PARAMETER kreditlimit      AS DECIMAL.
DEFINE INPUT PARAMETER foreign-rate     AS LOGICAL.
DEFINE INPUT PARAMETER bill-date        AS DATE.
DEFINE INPUT PARAMETER voucher-nr       AS CHARACTER.
DEFINE INPUT-OUTPUT PARAMETER cancel-str AS CHAR.

DEFINE OUTPUT PARAMETER error-desc      AS CHARACTER.
DEFINE OUTPUT PARAMETER balance         AS DECIMAL.
DEFINE OUTPUT PARAMETER balance-foreign AS DECIMAL.
DEFINE OUTPUT PARAMETER void-approve    AS LOGICAL INITIAL NO.
DEFINE OUTPUT PARAMETER flag3           AS INTEGER.
DEFINE OUTPUT PARAMETER tot-balance     AS DECIMAL.
DEFINE OUTPUT PARAMETER TABLE FOR t-bill.
DEFINE OUTPUT PARAMETER TABLE FOR t-bill-line.
DEFINE OUTPUT PARAMETER TABLE FOR spbill-list.

{SupertransBL.i} 
DEFINE VARIABLE lvCAREA AS CHAR INITIAL "fo-inv-paywith-deposit-webBL".

DEFINE VARIABLE depoart         AS INTEGER NO-UNDO.
DEFINE VARIABLE depobez         AS CHARACTER NO-UNDO.
DEFINE VARIABLE p-253           AS LOGICAL.
DEFINE VARIABLE zugriff         AS LOGICAL INITIAL YES.
DEFINE VARIABLE billdatum       AS DATE.
DEFINE VARIABLE r-recid         AS INT.
DEFINE VARIABLE na-running      AS LOGICAL. 
DEFINE VARIABLE gastnrmember    AS INTEGER.

FIND FIRST htparam WHERE htparam.paramnr EQ 1068 NO-LOCK NO-ERROR. 
IF AVAILABLE htparam THEN
DO:
    FIND FIRST artikel WHERE artikel.artnr EQ htparam.finteger AND artikel.departement EQ 0 NO-LOCK NO-ERROR.
    IF NOT AVAILABLE artikel OR artikel.artart NE 5 THEN
    DO:           
        error-desc = translateExtended ("Deposit article not defined.",lvCAREA,"").        
        RETURN. 
    END.
    ASSIGN 
        depoart = artikel.artnr
        depobez = artikel.bezeich
        .
END.

RUN htplogic.p(253, OUTPUT p-253).
IF p-253 THEN
DO: 
    error-desc = translateExtended ("Night Audit is running, posting not possible",lvCAREA,""). 
    RETURN.
END.

IF curr-rechnr NE 0 THEN
DO:
    RUN read-billbl.p(2, curr-rechnr, res-number, resllin-number, bill-flag, OUTPUT TABLE t-bill).
    FIND FIRST t-bill NO-ERROR.
    IF AVAILABLE t-bill AND t-bill.flag EQ 1 THEN
    DO:
        RUN zugriff-test(user-init, 38, 2, OUTPUT zugriff, OUTPUT error-desc).
        IF NOT zugriff THEN
        DO:
            error-desc = translateExtended ("Not possible",lvCAREA,"") 
                    + CHR(10) +
                    translateExtended ("Selected Bill Already Closed",lvCAREA,""). 
            RETURN.
        END.        
    END.
END.

RUN htpdate.p (110, OUTPUT billdatum).
IF transdate NE ? THEN billdatum = transdate.
FIND FIRST res-line WHERE res-line.resnr EQ res-number 
    AND res-line.reslinnr EQ resllin-number NO-LOCK NO-ERROR.
IF AVAILABLE res-line AND tbill-flag EQ 1 AND change-date THEN
DO:
    IF billdatum GT res-line.abreise THEN
    DO:
        error-desc = translateExtended ("Posting Date Can not be later than Check-out Date",lvCAREA,"")
                + " " + STRING(res-line.abreise). 
        RETURN.
    END.
END.

RUN update-to-bill.

FIND FIRST t-bill NO-LOCK.
IF flag3 EQ 1 THEN
DO:    
    IF AVAILABLE t-bill THEN RUN disp-bill-line.
END.

IF bill-flag = 0 THEN 
DO: 
    tot-balance = 0. 
    IF t-bill.parent-nr EQ 0 THEN tot-balance = t-bill.saldo. 
    ELSE RUN fo-invoice-disp-totbalancebl.p(bill-recid, OUTPUT tot-balance).
END. 

/*******************************************************************************************
                                        PROCEDURE
*******************************************************************************************/
PROCEDURE update-to-bill:
    FIND FIRST bill WHERE RECID(bill) EQ bill-recid NO-LOCK.
    r-recid = RECID(bill).

    DO TRANSACTION:
        FIND FIRST bill WHERE RECID(bill) EQ r-recid EXCLUSIVE-LOCK. 
        IF bill.flag EQ 1 AND bill-flag EQ 0 THEN 
        DO: 
          error-desc = translateExtended ("The Bill was closed / guest checked out",lvCAREA,"") 
                  + CHR(10)
                  + "Bill entry is no longer possible!".
          FIND CURRENT bill NO-LOCK. 
          RELEASE bill.
          RETURN. 
        END. 
        ELSE
        DO:
            balance = balance + pay-depoamount. 
            balance-foreign = balance-foreign + amount-foreign.
            bill.saldo = bill.saldo + pay-depoamount. 

            IF price-decimal EQ 0 AND bill.saldo LE 0.4 AND bill.saldo GE -0.4 THEN bill.saldo = 0. 
            IF double-currency OR foreign-rate THEN bill.mwst[99] = bill.mwst[99] + amount-foreign. 

            IF bill.datum LT bill-date OR bill.datum = ? THEN bill.datum = bill-date.

            FIND FIRST htparam WHERE paramnr EQ 253 NO-LOCK. 
            na-running = htparam.flogical. 
            FIND FIRST vhp.htparam WHERE vhp.htparam.paramnr EQ 110 NO-LOCK. 
            bill-date = vhp.htparam.fdate. 
            IF transdate NE ? THEN bill-date = transdate. 
            ELSE
            DO:
                IF na-running AND bill-date LT TODAY THEN bill-date = bill-date + 1. 
            END.

            FIND FIRST res-line WHERE res-line.resnr EQ bill.resnr AND res-line.reslinnr EQ bill.reslinnr NO-LOCK NO-ERROR. 
            IF AVAILABLE res-line THEN gastnrmember = res-line.gastnrmember. 
            ELSE gastnrmember = bill.gastnr. 

            CREATE bill-line. 
            ASSIGN
                bill-line.rechnr = bill.rechnr
                bill-line.artnr = depoart
                bill-line.bezeich = depobez 
                bill-line.anzahl = 1
                bill-line.betrag = pay-depoamount 
                bill-line.fremdwbetrag = amount-foreign
                bill-line.zinr = curr-room 
                bill-line.departement = artikel.departement
                bill-line.bill-datum = bill-date
                bill-line.zeit = TIME
                bill-line.userinit = user-init 
                . 
            IF voucher-nr NE "" THEN bill-line.bezeich = bill-line.bezeich + "/" + voucher-nr. 

            IF AVAILABLE res-line THEN 
            DO:
                ASSIGN
                    bill-line.massnr = res-line.resnr
                    bill-line.billin-nr = res-line.reslinnr 
                    bill-line.arrangement = res-line.arrangement
                    . 
            END.
            FIND CURRENT bill-line NO-LOCK.

            FIND FIRST umsatz WHERE umsatz.artnr EQ depoart 
                AND umsatz.departement EQ artikel.departement 
                AND umsatz.datum EQ bill-date EXCLUSIVE-LOCK NO-ERROR. 
            IF NOT AVAILABLE umsatz THEN 
            DO: 
                CREATE umsatz. 
                ASSIGN
                  umsatz.artnr = depoart
                  umsatz.datum = bill-date 
                  umsatz.departement = artikel.departement
                . 
            END.
            ASSIGN
                umsatz.betrag = umsatz.betrag + pay-depoamount
                umsatz.anzahl = umsatz.anzahl + 1
                . 
            FIND CURRENT umsatz NO-LOCK. 
            
            CREATE billjournal. 
            ASSIGN
                billjournal.rechnr = bill.rechnr
                billjournal.artnr = depoart
                billjournal.anzahl = 1
                billjournal.fremdwaehrng = amount-foreign
                billjournal.betrag = pay-depoamount
                billjournal.bezeich = depobez 
                billjournal.zinr = curr-room
                billjournal.departement = artikel.departement
                billjournal.epreis = pay-depoamount
                billjournal.zeit = TIME 
                billjournal.stornogrund = cancel-str 
                billjournal.userinit = user-init
                billjournal.bill-datum = bill-date
                cancel-str   = ""                
                void-approve = NO
                . 
            
            IF AVAILABLE res-line THEN billjournal.comment = STRING(res-line.resnr) + ";" + STRING(res-line.reslinnr).            
            IF voucher-nr NE "" THEN billjournal.bezeich = billjournal.bezeich + "/" + voucher-nr. 

            FIND CURRENT billjournal NO-LOCK. 
        END.

        balance = bill.saldo. 
        IF double-currency OR foreign-rate THEN balance-foreign = bill.mwst[99]. 
        
        flag3 = 1.

        FIND CURRENT bill NO-LOCK NO-ERROR. 
        CREATE t-bill.
        BUFFER-COPY bill TO t-bill.
    END.
END PROCEDURE.

PROCEDURE zugriff-test:
DEFINE INPUT PARAMETER user-init   AS CHAR FORMAT "x(2)".   
DEFINE INPUT PARAMETER array-nr    AS INTEGER.   
DEFINE INPUT PARAMETER expected-nr AS INTEGER.   
DEFINE OUTPUT PARAMETER zugriff    AS LOGICAL INITIAL YES.   
DEFINE OUTPUT PARAMETER msgStr     AS CHARACTER.

DEFINE VARIABLE n               AS INTEGER.  
DEFINE VARIABLE perm            AS INTEGER EXTENT 120 FORMAT "9".   
DEFINE VARIABLE s1              AS CHAR FORMAT "x(2)".   
DEFINE VARIABLE s2              AS CHAR FORMAT "x(1)".

    IF user-init EQ "" THEN
    DO:
        zugriff = NO.
        msgStr = translateExtended ("User not defined.",lvCAREA,"").
        RETURN.
    END.
    ELSE
    DO:
        FIND FIRST bediener WHERE bediener.userinit EQ user-init NO-LOCK NO-ERROR.
        IF AVAILABLE bediener THEN
        DO:
            CREATE tp-bediener.
            BUFFER-COPY bediener TO tp-bediener.
        END.
        ELSE
        DO:
            zugriff = NO.  
            msgStr = translateExtended ("User not defined.",lvCAREA,"").
            RETURN.
        END.
    END.

    DO n = 1 TO LENGTH(tp-bediener.permissions):   
        perm[n] = INTEGER(SUBSTR(tp-bediener.permissions, n, 1)).   
    END.   
    IF perm[array-nr] LT expected-nr THEN   
    DO:   
        zugriff = NO.   
        s1 = STRING(array-nr, "999").   
        s2 = STRING(expected-nr).
        msgStr = translateExtended ("Sorry, No Access Right, Access Code =",lvCAREA,"") + " "
            + s1 + s2. 
        RETURN.
    END.
END PROCEDURE.

PROCEDURE disp-bill-line:
    RUN fo-invoice-disp-bill-linebl.p(bill-recid, double-currency, 
        OUTPUT TABLE t-bill-line, OUTPUT TABLE spbill-list).
END PROCEDURE.
