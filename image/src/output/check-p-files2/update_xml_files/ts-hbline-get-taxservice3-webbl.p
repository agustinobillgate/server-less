DEFINE TEMP-TABLE menu-list   
    FIELD request AS CHAR   
    FIELD krecid  AS INTEGER INITIAL 0   
    FIELD posted  AS LOGICAL INITIAL NO   
    FIELD nr      AS INTEGER FORMAT ">>>" LABEL "No"   
    FIELD artnr   LIKE h-artikel.artnr   
    FIELD bezeich LIKE h-artikel.bezeich   
    FIELD anzahl  LIKE h-bill-line.anzahl INITIAL 1   
    FIELD price   AS DECIMAL   
    FIELD betrag  AS DECIMAL   
    FIELD voucher AS CHAR.   

DEFINE TEMP-TABLE t-amount-list 
    FIELD nr            AS INTEGER
    FIELD anzahl        AS INTEGER
    FIELD menu-recid    AS INTEGER
    FIELD amount        AS DECIMAL
    FIELD orig-amount   AS DECIMAL
    FIELD unit-price    AS DECIMAL
    FIELD artnr         AS INTEGER
    .

DEFINE TEMP-TABLE t-out-list 
    FIELD amount        AS DECIMAL
    FIELD orig-amount   AS DECIMAL
    FIELD amt-balance   AS DECIMAL
    .

DEFINE INPUT PARAMETER vMode        AS INTEGER.
DEFINE INPUT PARAMETER hbill-recid  AS INTEGER.
DEFINE INPUT PARAMETER menu-nr      AS INTEGER.
DEFINE INPUT PARAMETER dept         AS INTEGER.
DEFINE INPUT PARAMETER artnr        AS INTEGER.
DEFINE INPUT PARAMETER price        AS DECIMAL.
DEFINE INPUT PARAMETER anzahl       AS INTEGER.
DEFINE INPUT PARAMETER incl-vat     AS LOGICAL.
DEFINE INPUT-OUTPUT PARAMETER balance AS DECIMAL.
DEFINE INPUT-OUTPUT PARAMETER TABLE FOR t-amount-list.
DEFINE OUTPUT PARAMETER amount      AS DECIMAL.
DEFINE OUTPUT PARAMETER TABLE FOR t-out-list.

DEFINE VARIABLE fact-scvat AS DECIMAL NO-UNDO.
DEFINE VARIABLE curr-nr AS INTEGER NO-UNDO.
DEFINE VARIABLE curr-balance AS DECIMAL NO-UNDO.
DEFINE VARIABLE price-decimal       AS INTEGER. 

FIND FIRST h-bill WHERE RECID(h-bill) EQ hbill-recid NO-LOCK NO-ERROR.
IF AVAILABLE h-bill THEN curr-balance = h-bill.saldo.

FIND FIRST vhp.htparam WHERE vhp.htparam.paramnr = 491 NO-LOCK. 
price-decimal = vhp.htparam.finteger.   /* non-digit OR digit version */ 

IF vMode EQ 1 THEN
DO:
    RUN ts-hbline-get-taxservicebl.p(artnr, dept, OUTPUT fact-scvat).
    CREATE t-out-list.
    IF NOT incl-vat THEN
    DO:              
        FIND FIRST t-amount-list WHERE t-amount-list.nr EQ menu-nr NO-LOCK NO-ERROR.
        IF NOT AVAILABLE t-amount-list THEN
        DO:
            CREATE t-amount-list.
            ASSIGN
                t-amount-list.nr = menu-nr    
                t-amount-list.artnr = artnr
                t-amount-list.anzahl = anzahl
                t-amount-list.unit-price = price
                t-amount-list.amount = (price * fact-scvat) * anzahl
                t-amount-list.orig-amount = price * anzahl
                t-amount-list.amount = ROUND(t-amount-list.amount, price-decimal) /* Dzikri 67CBDE - Rounding problem */
                amount = amount + t-amount-list.amount
                .
        END.     
        ELSE
        DO:
            IF t-amount-list.anzahl NE anzahl THEN
            DO:
                ASSIGN
                    t-amount-list.anzahl = anzahl
                    t-amount-list.amount = (price * fact-scvat) * anzahl
                    t-amount-list.orig-amount = price * anzahl
                    t-amount-list.amount = ROUND(t-amount-list.amount, price-decimal) /* Dzikri 67CBDE - Rounding problem */
                    .
            END.
        END.

        amount = 0.
        FOR EACH t-amount-list:
            amount = amount + t-amount-list.amount.
            t-out-list.orig-amount = t-out-list.orig-amount + t-amount-list.orig-amount.
        END.
        t-out-list.amount = amount.
        amount = amount + balance.
        t-out-list.amt-balance = amount.
    END.  
    ELSE
    DO:     
        FIND FIRST t-amount-list WHERE t-amount-list.nr EQ menu-nr NO-LOCK NO-ERROR.
        IF NOT AVAILABLE t-amount-list THEN
        DO:
            CREATE t-amount-list.
            ASSIGN
                t-amount-list.nr = menu-nr   
                t-amount-list.artnr = artnr
                t-amount-list.anzahl = anzahl
                t-amount-list.unit-price = price
                t-amount-list.amount = price * anzahl
                t-amount-list.amount = ROUND(t-amount-list.amount, price-decimal) /* Dzikri 67CBDE - Rounding problem */
                t-amount-list.orig-amount = (price * anzahl) / fact-scvat
                amount = amount + t-amount-list.amount
                .  
        END.    
        ELSE
        DO:
            IF t-amount-list.anzahl NE anzahl THEN
            DO:
                ASSIGN
                    t-amount-list.anzahl = anzahl
                    /*t-amount-list.amount = (price * fact-scvat) * anzahl.*/
                    t-amount-list.amount = price * anzahl
                    t-amount-list.orig-amount = (price * anzahl) / fact-scvat
                    t-amount-list.amount = ROUND(t-amount-list.amount, price-decimal) /* Dzikri 67CBDE - Rounding problem */
                    .
            END.            
        END.

        amount = 0.
        FOR EACH t-amount-list:
            amount = amount + t-amount-list.amount.
            t-out-list.orig-amount = t-out-list.orig-amount + t-amount-list.orig-amount.
        END.
        t-out-list.amount = amount.
        amount = amount + balance.
        t-out-list.amt-balance = amount.        
    END.
END.
ELSE
DO:
    CREATE t-out-list.
    FIND FIRST t-amount-list WHERE t-amount-list.nr EQ menu-nr NO-LOCK NO-ERROR.
    IF AVAILABLE t-amount-list THEN
    DO:
        /*amount = amount - t-amount-list.amount.*/
        DELETE t-amount-list.
    END.

    amount = 0.
    FOR EACH t-amount-list:
        amount = amount + t-amount-list.amount.
        t-out-list.orig-amount = t-out-list.orig-amount + t-amount-list.orig-amount.
    END.    
    t-out-list.amount = amount.
    amount = amount + balance.
    t-out-list.amt-balance = amount.
    
    curr-nr = 0.
    FOR EACH t-amount-list WHERE t-amount-list.nr GT 0 BY t-amount-list.nr:  
        curr-nr = curr-nr + 1.  
        t-amount-list.nr = curr-nr.  
    END. 
END.

