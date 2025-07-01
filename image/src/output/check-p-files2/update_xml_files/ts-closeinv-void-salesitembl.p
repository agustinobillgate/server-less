DEFINE TEMP-TABLE t-b-list LIKE h-bill-line 
    FIELD rec-id AS INTEGER.

DEFINE TEMP-TABLE ordered-item LIKE h-bill-line 
    FIELD rec-id    AS INTEGER
    FIELD tax       AS DECIMAL
    FIELD service   AS DECIMAL.

DEFINE TEMP-TABLE t-void-list LIKE h-bill-line 
    FIELD rec-id AS INTEGER.

DEFINE TEMP-TABLE t-h-artsales LIKE h-artikel
    FIELD rec-id AS INT.

DEFINE TEMP-TABLE b-list LIKE h-bill-line 
    FIELD rec-id AS INTEGER.

DEFINE TEMP-TABLE tmp-hartikel  LIKE h-artikel  
    FIELD rec-id AS INT.

DEFINE TEMP-TABLE tp-bediener  LIKE bediener. 

DEFINE TEMP-TABLE submenu-list 
    FIELD menurecid    AS INTEGER 
    FIELD zeit         AS INTEGER 
    FIELD nr           AS INTEGER 
    FIELD artnr        LIKE h-artikel.artnr 
    FIELD bezeich      LIKE h-artikel.bezeich 
    FIELD anzahl       AS INTEGER 
    FIELD zknr         AS INTEGER 
    FIELD request      AS CHAR.

DEFINE TEMP-TABLE t-h-bill  LIKE h-bill  
    FIELD rec-id AS INT.

DEFINE TEMP-TABLE t-kellner1   LIKE kellner. 

DEFINE TEMP-TABLE summary-bill
    FIELD subtotal      AS DECIMAL
    FIELD total-service AS DECIMAL
    FIELD total-tax     AS DECIMAL
    FIELD grand-total   AS DECIMAL
    .

DEFINE INPUT PARAMETER TABLE FOR t-b-list. /*ALL*/
DEFINE INPUT PARAMETER language-code    AS INTEGER.
DEFINE INPUT PARAMETER v-type           AS INTEGER. 
DEFINE INPUT PARAMETER bl-recid         AS INTEGER. /*Recid t-b-list selected*/
DEFINE INPUT PARAMETER rec-id           AS INTEGER. /*recid h-bill*/
DEFINE INPUT PARAMETER bill-no          AS INTEGER.
DEFINE INPUT PARAMETER curr-dept        AS INTEGER.
DEFINE INPUT PARAMETER tischnr          AS INTEGER.
DEFINE INPUT PARAMETER pax              AS INTEGER.
DEFINE INPUT PARAMETER price-decimal    AS INTEGER.
DEFINE INPUT PARAMETER curr-waiter      AS INTEGER.   
DEFINE INPUT PARAMETER kreditlimit      AS DECIMAL.
DEFINE INPUT PARAMETER exchg-rate       AS DECIMAL INITIAL 1.
DEFINE INPUT PARAMETER gname            AS CHARACTER.
DEFINE INPUT PARAMETER user-init        AS CHARACTER.
DEFINE INPUT PARAMETER cancel-str       AS CHARACTER.
DEFINE INPUT PARAMETER double-currency  AS LOGICAL. 
DEFINE INPUT PARAMETER foreign-rate     AS LOGICAL.
DEFINE INPUT-OUTPUT PARAMETER balance   AS DECIMAL.
DEFINE OUTPUT PARAMETER mess-result     AS CHARACTER.
DEFINE OUTPUT PARAMETER v-success       AS LOGICAL INITIAL NO.
DEFINE OUTPUT PARAMETER TABLE FOR t-void-list. /*ALL*/
DEFINE OUTPUT PARAMETER TABLE FOR summary-bill.

DEFINE VARIABLE vCorrect            AS LOGICAL.
DEFINE VARIABLE cancel-flag         AS LOGICAL.
DEFINE VARIABLE answer              AS LOGICAL.
DEFINE VARIABLE zugriff             AS LOGICAL.
DEFINE VARIABLE fl-code             AS INT.
DEFINE VARIABLE fl-code1            AS INT.
DEFINE VARIABLE fl-code2            AS INT.
DEFINE VARIABLE fl-code3            AS INT.
DEFINE VARIABLE sales-art           AS INT.
DEFINE VARIABLE rec-id-h-art        AS INT.
DEFINE VARIABLE anz                 AS INT.
DEFINE VARIABLE total-qty           AS INTEGER.
DEFINE VARIABLE hoga-resnr          AS INTEGER.  
DEFINE VARIABLE hoga-reslinnr       AS INTEGER.
DEFINE VARIABLE qty                 AS INTEGER.
DEFINE VARIABLE f-disc              AS INTEGER.
DEFINE VARIABLE b-disc              AS INTEGER.
DEFINE VARIABLE o-disc              AS INTEGER.
DEFINE VARIABLE rechnr              AS INTEGER.
DEFINE VARIABLE bcol                AS INTEGER.
DEFINE VARIABLE add-second          AS INTEGER.
DEFINE VARIABLE ci-date             AS DATE.
DEFINE VARIABLE bill-date           AS DATE.
DEFINE VARIABLE description         AS CHARACTER.
DEFINE VARIABLE msg-str             AS CHARACTER.
DEFINE VARIABLE printed             AS CHARACTER.
DEFINE VARIABLE deptname            AS CHARACTER.
DEFINE VARIABLE price               AS DECIMAL.

DEFINE VARIABLE do-it               AS LOGICAL INITIAL YES. 
DEFINE VARIABLE s                   AS CHAR. 
DEFINE VARIABLE f-log               AS LOGICAL.
DEFINE VARIABLE p-88                AS LOGICAL.
DEFINE VARIABLE closed              AS LOGICAL.
DEFINE VARIABLE mwst-sales          AS DECIMAL.
DEFINE VARIABLE mwst-foreign-sales  AS DECIMAL.
DEFINE VARIABLE balance-sales       AS DECIMAL.
DEFINE VARIABLE balance-foreign-sales   AS DECIMAL.
DEFINE VARIABLE amount-foreign      AS DECIMAL.
DEFINE VARIABLE amount              AS DECIMAL.
DEFINE VARIABLE netto-betrag        AS DECIMAL.

/****************************** MAIN LOGIC ******************************/
FIND FIRST vhp.htparam WHERE paramnr = 557 no-lock. /*rest artnr food disc*/ 
f-disc = vhp.htparam.finteger. 
FIND FIRST vhp.htparam WHERE paramnr = 596 no-lock. /*rest artnr bev disc*/ 
b-disc = vhp.htparam.finteger.
FIND FIRST vhp.htparam WHERE paramnr = 556 no-lock. /*rest artnr food disc*/ 
o-disc = vhp.htparam.finteger. 

FOR EACH h-artikel WHERE h-artikel.departement EQ curr-dept
    AND h-artikel.artart EQ 0 NO-LOCK:
    CREATE t-h-artsales.
    BUFFER-COPY h-artikel TO t-h-artsales.
    ASSIGN t-h-artsales.rec-id = INTEGER(RECID(h-artikel)).
END.

FIND FIRST hoteldpt WHERE hoteldpt.num EQ curr-dept NO-LOCK NO-ERROR.
IF AVAILABLE hoteldpt THEN deptname = hoteldpt.depart.
/****************************** PROCESS ******************************/
FIND FIRST t-b-list.
IF NOT AVAILABLE t-b-list THEN
DO:
    mess-result = "01-No Data Available.".
    RETURN.
END.

FOR EACH t-b-list WHERE t-b-list.rec-id EQ bl-recid:
    CREATE b-list.
    BUFFER-COPY t-b-list TO b-list.
END.

IF v-type EQ 1 THEN
DO:    
    FIND FIRST b-list.
    FIND FIRST t-h-artsales WHERE t-h-artsales.artnr EQ b-list.artnr
        AND t-h-artsales.departement EQ b-list.departement
        AND b-list.anzahl GT 0 NO-LOCK NO-ERROR.
    IF AVAILABLE t-h-artsales AND balance NE 0 THEN
    DO:
        FIND FIRST t-b-list WHERE t-b-list.artnr EQ f-disc
            OR t-b-list.artnr EQ b-disc
            OR t-b-list.artnr EQ o-disc NO-LOCK NO-ERROR.
        IF AVAILABLE t-b-list THEN
        DO:
            mess-result = "02-Bill have discount article, deleteing not possible.".
            RETURN.
        END.
    END.
    ELSE
    DO:
        mess-result = "03-Balance not zero or article sales not available.".
        RETURN.
    END.
    v-success = YES.
END.
ELSE IF v-type EQ 2 THEN
DO:
    RUN ts-closeinv-cancel-orderbl.p (bl-recid, /*zugriff,*/
        OUTPUT fl-code, OUTPUT fl-code1, OUTPUT fl-code2,
        OUTPUT qty, OUTPUT answer, OUTPUT cancel-flag,
        OUTPUT sales-art, OUTPUT description, OUTPUT price,
        OUTPUT rec-id-h-art, OUTPUT anz, OUTPUT TABLE tmp-hartikel).  
    FIND FIRST tmp-hartikel NO-ERROR.

    IF fl-code EQ 1 THEN
    DO:
        mess-result = "04-Qty is zero. Cancel not possible.".
        RETURN.
    END.

    IF qty LT 0 AND tmp-hartikel.artart EQ 0 THEN 
    DO: 
        RUN htplogic.p(261, OUTPUT f-log).
        IF f-log THEN 
        DO: 
            RUN check-permission(user-init, 52, 2, OUTPUT zugriff, OUTPUT msg-str). 
            IF NOT zugriff THEN 
            DO:
                mess-result = "05-" + msg-str.
                RETURN.
            END.
        END. 
    END. 

    IF tmp-hartikel.artart NE 0 THEN do-it = NO. 
    IF qty = 0 OR sales-art = 0 THEN do-it = NO. 

    IF qty NE 0 THEN
    DO:
        IF price NE 0 THEN
        DO:
            RUN ts-closeinv-calculate-amountbl.p
                (1, tmp-hartikel.rec-id, double-currency, 
                INPUT-OUTPUT price, qty, exchg-rate, price-decimal, 
                ?, cancel-flag, foreign-rate, curr-dept,
                OUTPUT amount-foreign, OUTPUT amount,
                OUTPUT fl-code, OUTPUT fl-code1).
            
            netto-betrag = amount.

            IF fl-code1 EQ 1 THEN
            DO:                
                RUN check-permission(user-init, 52, 2, OUTPUT zugriff, OUTPUT msg-str).
                IF NOT zugriff THEN 
                DO:
                    mess-result = "05-" + msg-str.
                    RETURN.
                END.
            END.
            IF price NE 0 AND amount EQ 0 THEN
            DO:
                mess-result = "06-Amount is zero. Posting not possible.".
            END.

            IF tmp-hartikel.artart EQ 0 AND qty LT 0 THEN
            DO:
                IF cancel-str EQ "" THEN
                DO:
                    cancel-flag = NO. 
                    do-it = NO. 
                END.
            END.

            IF do-it THEN
            DO:
                IF NOT tmp-hartikel.autosaldo THEN printed = "". 

                IF tmp-hartikel.artart EQ 0 THEN 
                DO:                    
                    RUN check-permission(user-init, 19, 2, OUTPUT zugriff, OUTPUT msg-str).
                    IF NOT zugriff THEN
                    DO:
                        mess-result = "05-" + msg-str.
                        RETURN.
                    END.
                END.
                ELSE
                DO:                    
                    RUN check-permission(user-init, 20, 2, OUTPUT zugriff, OUTPUT msg-str).
                    IF NOT zugriff THEN
                    DO:
                        mess-result = "05-" + msg-str.
                        RETURN.
                    END.
                END.
                
                IF zugriff THEN
                DO:                                
                    DEF VAR rec-id-artikel AS INT.
                    DEF VAR service-code   AS INT.
                    IF NOT AVAILABLE tmp-hartikel THEN
                    DO:
                        rec-id-artikel = 0.
                        service-code = 0.
                    END.
                    ELSE
                    DO:
                        rec-id-artikel = tmp-hartikel.rec-id.
                        service-code = tmp-hartikel.service-code.
                    END. 
                    
                    RUN ts-closeinv-updatebill-cldbl.p
                        (language-code, rec-id, rec-id-artikel, deptname, ?,
                        tmp-hartikel.artart, NO, service-code, amount,
                        amount-foreign, price, double-currency, qty, exchg-rate, price-decimal, 0,
                        tischnr, curr-dept, curr-waiter, gname, pax, kreditlimit,
                        1, sales-art, description, "", "",
                        cancel-str, "", "", "", NO,
                        NO, tmp-hartikel.artnrfront, 0, 0, "",
                        NO, foreign-rate, "", user-init,
                        hoga-resnr, hoga-reslinnr, NO, 0, "",
                        INPUT TABLE submenu-list, OUTPUT bill-date,
                        OUTPUT cancel-flag, OUTPUT fl-code, OUTPUT mwst-sales,
                        OUTPUT mwst-foreign-sales, OUTPUT rechnr, OUTPUT balance-sales,
                        OUTPUT bcol, OUTPUT balance-foreign-sales, OUTPUT fl-code1,
                        OUTPUT fl-code2, OUTPUT fl-code3, OUTPUT p-88, OUTPUT closed,
                        OUTPUT TABLE t-h-bill, OUTPUT TABLE t-kellner1).
                    FIND FIRST t-h-bill NO-ERROR.
                    FIND FIRST t-kellner1 NO-ERROR.                    
                END.

                /*IF fl-code EQ 1 THEN
                DO:
                    mess-result = "07-Transaction not allowed: Posted item(s) with differrent billing date found.".
                    RETURN.
                END.*/
                IF fl-code EQ 2 THEN
                DO:
                    mess-result = "08-Occupied Table. Posting not possible.".
                    RETURN.
                END.
                    
                RUN ts-closeinv-calculate-amountbl.p
                    (2, tmp-hartikel.rec-id, double-currency, 
                    INPUT-OUTPUT price, qty, exchg-rate, price-decimal, 
                    ?, cancel-flag, foreign-rate, curr-dept,
                    OUTPUT amount-foreign, OUTPUT amount,
                    OUTPUT fl-code, OUTPUT fl-code1).

                RUN ts-closeinv-create-logfilebl.p(user-init,bl-recid).

                CREATE t-void-list.
                ASSIGN
                    add-second                 = add-second + 1  
                    t-void-list.rechnr         = t-h-bill.rechnr   
                    t-void-list.artnr          = sales-art   
                    t-void-list.bezeich        = DESCRIPTION   
                    t-void-list.anzahl         = qty   
                    t-void-list.nettobetrag    = netto-betrag  
                    t-void-list.fremdwbetrag   = amount-foreign   
                    t-void-list.betrag         = amount   
                    t-void-list.tischnr        = tischnr   
                    t-void-list.departement    = curr-dept   
                    t-void-list.epreis         = price   
                    t-void-list.zeit           = TIME + add-second   
                    t-void-list.bill-datum     = bill-date   
                    t-void-list.sysdate        = TODAY
                .

                balance = balance + amount.

                RUN recalculate-summarybill.
            END.
        END.
    END.
   
    v-success = YES.
END.

/******************************************************************************************/
PROCEDURE check-permission:
DEFINE INPUT PARAMETER user-init   AS CHAR.   
DEFINE INPUT PARAMETER array-nr    AS INTEGER.   
DEFINE INPUT PARAMETER expected-nr AS INTEGER.   
DEFINE OUTPUT PARAMETER zugriff    AS LOGICAL INITIAL YES.   
DEFINE OUTPUT PARAMETER msg-str    AS CHARACTER.

DEFINE VARIABLE mail-exist      AS LOGICAL NO-UNDO.  
DEFINE VARIABLE logical-flag    AS LOGICAL NO-UNDO.  
DEFINE VARIABLE n               AS INTEGER.   
DEFINE VARIABLE perm            AS INTEGER EXTENT 120 FORMAT "9" . /* Malik 4CD2E2 */   
DEFINE VARIABLE s1              AS CHAR FORMAT "x(2)".   
DEFINE VARIABLE s2              AS CHAR FORMAT "x(1)".   
DEFINE VARIABLE mn-date         AS DATE.   
DEFINE VARIABLE anz             AS INTEGER.

    IF user-init = "" THEN  
    DO:   
        zugriff = NO.   
        msg-str = "User not defined.".
        RETURN.
    END.   
    ELSE   
    DO:  
        FOR EACH tp-bediener:
            DELETE tp-bediener.
        END.

        FIND FIRST bediener WHERE bediener.userinit EQ user-init NO-LOCK NO-ERROR.
        IF AVAILABLE bediener THEN
        DO:
            CREATE tp-bediener.
            BUFFER-COPY bediener TO tp-bediener.
        END.
        ELSE
        DO:
            zugriff = NO.  
            msg-str = "User not found.".
            RETURN.
        END.
            
        DO  n = 1 TO LENGTH(tp-bediener.permissions):   
            perm[n] = INTEGER(SUBSTR(tp-bediener.permissions, n, 1)).   
        END.   
        IF perm[array-nr] LT expected-nr THEN   
        DO:   
            zugriff = NO.   
            s1 = STRING(array-nr, "999").   
            s2 = STRING(expected-nr).
            msg-str = "Sorry, No Access Right, Access Code = " + s1 + s2. 
        END.   
    END.   
END PROCEDURE.

PROCEDURE recalculate-summarybill:    
    DEFINE VARIABLE t-serv%         AS DECIMAL INITIAL 0.  
    DEFINE VARIABLE t-mwst%         AS DECIMAL INITIAL 0.  
    DEFINE VARIABLE t-fact          AS DECIMAL INITIAL 1.
    DEFINE VARIABLE t-service       AS DECIMAL.
    DEFINE VARIABLE t-mwst1         AS DECIMAL INITIAL 0. 
    DEFINE VARIABLE t-mwst          AS DECIMAL INITIAL 0. 
    DEFINE VARIABLE h-service       AS DECIMAL.  
    DEFINE VARIABLE h-mwst          AS DECIMAL.  
    DEFINE VARIABLE h-mwst2         AS DECIMAL.
    DEFINE VARIABLE t-h-service     AS DECIMAL.  
    DEFINE VARIABLE t-h-mwst        AS DECIMAL.  
    DEFINE VARIABLE t-h-mwst2       AS DECIMAL.
    DEFINE VARIABLE incl-service    AS LOGICAL.  
    DEFINE VARIABLE incl-mwst       AS LOGICAL.
    DEFINE VARIABLE gst-logic       AS LOGICAL INITIAL NO.
    DEFINE VARIABLE serv-disc       AS LOGICAL INITIAL YES.
    DEFINE VARIABLE vat-disc        AS LOGICAL INITIAL YES.
    DEFINE VARIABLE f-discArt       AS INTEGER INITIAL -1 NO-UNDO. 
    DEFINE VARIABLE amount          AS DECIMAL. 
    DEFINE VARIABLE f-dec           AS DECIMAL.  

    DEFINE VARIABLE serv-code       AS INTEGER. 
    DEFINE VARIABLE vat-code        AS INTEGER. 
    DEFINE VARIABLE servtax-use-foart AS LOGICAL. 
    DEFINE VARIABLE serv-vat        AS LOGICAL NO-UNDO. 
    DEFINE VARIABLE tax-vat         AS LOGICAL NO-UNDO. 
    DEFINE VARIABLE ct              AS CHAR    NO-UNDO.
    DEFINE VARIABLE l-deci          AS INTEGER NO-UNDO INIT 2.
    DEFINE VARIABLE fact-scvat      AS DECIMAL NO-UNDO INIT 1.
    DEFINE VARIABLE service         AS DECIMAL.
    DEFINE VARIABLE vat             AS DECIMAL.
    DEFINE VARIABLE vat2            AS DECIMAL.
    DEFINE VARIABLE mwst            AS DECIMAL.
    DEFINE VARIABLE mwst1           AS DECIMAL.
    
    DEFINE VARIABLE sub-tot   AS DECIMAL.
    DEFINE VARIABLE tot-serv  AS DECIMAL.
    DEFINE VARIABLE tot-tax   AS DECIMAL.
    DEFINE VARIABLE grand-tot AS DECIMAL.
    
    DEFINE VARIABLE netto-bet    AS DECIMAL. /*FD*/
    DEFINE VARIABLE compli-flag  AS LOGICAL. /*FD*/
    
    DEFINE BUFFER buff-hart FOR h-artikel.

    /****************************************************************************************/
    FIND FIRST hoteldpt WHERE hoteldpt.num EQ curr-dept NO-LOCK NO-ERROR.
    IF AVAILABLE hoteldpt THEN servtax-use-foart = hoteldpt.defult.
    
    FIND FIRST htparam WHERE htparam.paramnr = 468 NO-LOCK NO-ERROR.
    IF AVAILABLE htparam THEN serv-disc = htparam.flogic.
    
    FIND FIRST htparam WHERE htparam.paramnr = 469 NO-LOCK NO-ERROR.
    IF AVAILABLE htparam THEN vat-disc = htparam.flogic.
    
    FIND FIRST vhp.htparam WHERE paramnr = 135 NO-LOCK. 
    incl-service = vhp.htparam.flogical. 
     
    FIND FIRST vhp.htparam WHERE paramnr = 134 NO-LOCK. 
    incl-mwst = vhp.htparam.flogical. 
    
    RUN htplogic.p(479, OUTPUT serv-vat).
    RUN htplogic.p(483, OUTPUT tax-vat).

    FOR EACH t-b-list:
        CREATE ordered-item.
        BUFFER-COPY t-b-list TO ordered-item.
    END.

    FOR EACH ordered-item WHERE ordered-item.rec-id EQ bl-recid:
        t-h-service = 0.
        t-h-mwst = 0.
        t-h-mwst2 = 0.
        h-service = 0.
        h-mwst = 0.
        service = 0.
        mwst = 0.

        FIND FIRST h-artikel WHERE h-artikel.departement EQ ordered-item.departement 
            AND h-artikel.artnr EQ ordered-item.artnr 
            AND h-artikel.artart EQ 0 NO-LOCK NO-ERROR.
        IF AVAILABLE h-artikel THEN
        DO:
            netto-bet = netto-bet + (ordered-item.epreis * ordered-item.anzahl).
    
            IF NOT servtax-use-foart THEN
            DO:
                ASSIGN
                    serv-code = h-artikel.service-code
                    vat-code = h-artikel.mwst-code
                .
            END.
            ELSE
            DO:
                FIND FIRST artikel WHERE artikel.artnr EQ h-artikel.artnrfront
                    AND artikel.departement EQ h-artikel.departement NO-LOCK NO-ERROR.
                IF AVAILABLE artikel THEN
                DO:
                    ASSIGN
                        serv-code = artikel.service-code
                        vat-code = artikel.mwst-code
                    .
                END.
            END.
        END.

        IF AVAILABLE h-artikel THEN
        DO:
            IF ordered-item.artnr NE f-disc THEN
            DO:
                IF serv-code NE 0 AND NOT incl-service THEN
                DO:
                    FIND FIRST htparam WHERE htparam.paramnr EQ serv-code NO-LOCK NO-ERROR.                        
                    IF AVAILABLE htparam AND htparam.fdecimal NE 0 THEN 
                    DO:
                        IF NUM-ENTRIES(htparam.fchar, CHR(2)) GE 2 THEN
                            ASSIGN t-h-service = DECIMAL(ENTRY(2, htparam.fchar, CHR(2))) / 10000.
                        ELSE t-h-service = htparam.fdecimal.
                    END.
                END.

                IF vat-code NE 0 AND NOT incl-mwst THEN
                DO:
                    FIND FIRST htparam WHERE htparam.paramnr EQ vat-code NO-LOCK NO-ERROR. 
                    IF AVAILABLE htparam AND htparam.fdecimal NE 0 THEN 
                    DO: 
                        IF NUM-ENTRIES(htparam.fchar, CHR(2)) GE 2 THEN
                            ASSIGN t-h-mwst = DECIMAL(ENTRY(2, htparam.fchar, CHR(2))) / 10000.
                        ELSE t-h-mwst = htparam.fdecimal.
    
                        IF serv-vat AND NOT tax-vat THEN 
                            t-h-mwst = t-h-mwst + t-h-mwst * t-h-service / 100.
                        ELSE IF serv-vat AND tax-vat THEN 
                            t-h-mwst = t-h-mwst + t-h-mwst * (t-h-service + t-h-mwst2) / 100.
                        ELSE IF NOT serv-vat AND tax-vat THEN 
                            t-h-mwst = t-h-mwst + t-h-mwst * t-h-mwst2 / 100.
    
                        ASSIGN 
                            ct     = REPLACE(STRING(t-h-mwst), ".", ",")
                            l-deci = LENGTH(ENTRY(2, ct, ",")) NO-ERROR
                        .
                        IF l-deci LE 2     THEN t-h-mwst = ROUND(t-h-mwst, 2).
                        ELSE IF l-deci = 3 THEN t-h-mwst = ROUND(t-h-mwst, 3).
                        ELSE t-h-mwst = ROUND(t-h-mwst, 4).
                    END.
                END.

                IF t-h-service NE 0 OR t-h-mwst NE 0 THEN
                DO:
                    ASSIGN
                        t-h-service = t-h-service / 100
                        t-h-mwst = t-h-mwst / 100
                        t-h-mwst2 = t-h-mwst2 / 100
                    .
       
                    fact-scvat = 1 + t-h-service + t-h-mwst + t-h-mwst2. 
                    h-service = ordered-item.betrag / fact-scvat * t-h-service.
                    h-service = ROUND(h-service, 2).
                    h-mwst = ordered-item.betrag / fact-scvat * t-h-mwst.
                    h-mwst = ROUND(h-mwst, 2).
    
                    IF NOT incl-service THEN service = service + h-service.
                    
                    IF NOT incl-mwst THEN 
                    DO:
                        mwst   = mwst   + h-mwst.
                        mwst1  = mwst1  + h-mwst.
                    END.  
                END. 
            END.
            ELSE
            DO:
                IF serv-code NE 0 AND NOT incl-service AND serv-disc THEN
                DO:
                    FIND FIRST htparam WHERE htparam.paramnr EQ serv-code NO-LOCK NO-ERROR.                        
                    IF AVAILABLE htparam AND htparam.fdecimal NE 0 THEN 
                    DO:
                        IF NUM-ENTRIES(htparam.fchar, CHR(2)) GE 2 THEN
                            ASSIGN t-h-service = DECIMAL(ENTRY(2, htparam.fchar, CHR(2))) / 10000.
                        ELSE t-h-service = htparam.fdecimal.
                    END.
                END.

                IF vat-code NE 0 AND NOT incl-mwst AND vat-disc THEN
                DO:
                    FIND FIRST htparam WHERE htparam.paramnr EQ vat-code NO-LOCK NO-ERROR. 
                    IF AVAILABLE htparam AND htparam.fdecimal NE 0 THEN 
                    DO: 
                        IF NUM-ENTRIES(htparam.fchar, CHR(2)) GE 2 THEN
                            ASSIGN t-h-mwst = DECIMAL(ENTRY(2, htparam.fchar, CHR(2))) / 10000.
                        ELSE t-h-mwst = htparam.fdecimal.
    
                        IF serv-vat AND NOT tax-vat THEN 
                            t-h-mwst = t-h-mwst + t-h-mwst * t-h-service / 100.
                        ELSE IF serv-vat AND tax-vat THEN 
                            t-h-mwst = t-h-mwst + t-h-mwst * (t-h-service + t-h-mwst2) / 100.
                        ELSE IF NOT serv-vat AND tax-vat THEN 
                            t-h-mwst = t-h-mwst + t-h-mwst * t-h-mwst2 / 100.
    
                        ASSIGN 
                            ct     = REPLACE(STRING(t-h-mwst), ".", ",")
                            l-deci = LENGTH(ENTRY(2, ct, ",")) NO-ERROR
                        .
                        IF l-deci LE 2     THEN t-h-mwst = ROUND(t-h-mwst, 2).
                        ELSE IF l-deci = 3 THEN t-h-mwst = ROUND(t-h-mwst, 3).
                        ELSE t-h-mwst = ROUND(t-h-mwst, 4).
                    END.
                END.

                IF ordered-item.epreis NE ordered-item.betrag THEN
                DO:
                    IF t-h-service NE 0 OR t-h-mwst NE 0 THEN
                    DO:
                        ASSIGN
                            t-h-service = t-h-service / 100
                            t-h-mwst = t-h-mwst / 100
                            t-h-mwst2 = t-h-mwst2 / 100
                        .
           
                        fact-scvat = 1 + t-h-service + t-h-mwst + t-h-mwst2. 
                        h-service = ordered-item.betrag / fact-scvat * t-h-service.
                        h-service = ROUND(h-service, 2).
                        h-mwst = ordered-item.betrag / fact-scvat * t-h-mwst.
                        h-mwst = ROUND(h-mwst, 2).
        
                        IF NOT incl-service THEN service = service + h-service.
                        
                        IF NOT incl-mwst THEN 
                        DO:
                            mwst   = mwst   + h-mwst.
                            mwst1  = mwst1  + h-mwst.
                        END.  
                    END.
                END. 
            END.

            ordered-item.service = service.
            ordered-item.tax     = mwst.
        END.
    END.

    FOR EACH ordered-item,
        FIRST buff-hart WHERE buff-hart.artnr EQ ordered-item.artnr 
        AND buff-hart.departement EQ ordered-item.departement NO-LOCK:
    
        sub-tot   = netto-bet.
        tot-serv  = tot-serv + ordered-item.service.
        tot-tax   = tot-tax + ordered-item.tax.
    
        IF buff-hart.artart EQ 11 OR buff-hart.artart EQ 12 THEN compli-flag = YES.
    END.
    IF compli-flag THEN
    DO:
        tot-serv = 0.
        tot-tax = 0.
    END.
    
    grand-tot = sub-tot + tot-serv + tot-tax.

    CREATE summary-bill.
    ASSIGN 
        summary-bill.subtotal       = sub-tot
        summary-bill.total-service  = tot-serv
        summary-bill.total-tax      = tot-tax
        summary-bill.grand-total    = grand-tot
        .
END PROCEDURE.
