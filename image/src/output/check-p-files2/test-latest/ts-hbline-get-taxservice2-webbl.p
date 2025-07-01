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
    .


DEFINE INPUT PARAMETER vMode        AS INTEGER.
DEFINE INPUT PARAMETER hbill-recid  AS INTEGER.
DEFINE INPUT PARAMETER menu-nr      AS INTEGER.
DEFINE INPUT PARAMETER dept         AS INTEGER.
DEFINE INPUT PARAMETER artnr        AS INTEGER.
DEFINE INPUT PARAMETER price        AS DECIMAL.
DEFINE INPUT PARAMETER anzahl       AS INTEGER.
DEFINE INPUT PARAMETER incl-vat     AS LOGICAL.
DEFINE OUTPUT PARAMETER amount      AS DECIMAL.
DEFINE INPUT-OUTPUT PARAMETER balance AS DECIMAL.
DEFINE INPUT-OUTPUT PARAMETER TABLE FOR t-amount-list.

DEFINE VARIABLE fact-scvat AS DECIMAL NO-UNDO.
DEFINE VARIABLE curr-nr AS INTEGER NO-UNDO.
DEFINE VARIABLE curr-balance AS DECIMAL NO-UNDO.

FIND FIRST h-bill WHERE RECID(h-bill) EQ hbill-recid NO-LOCK NO-ERROR.
IF AVAILABLE h-bill THEN curr-balance = h-bill.saldo.

IF vMode EQ 1 THEN
DO:
    IF NOT incl-vat THEN
    DO:      
        RUN ts-hbline-get-taxservicebl.p(artnr, dept, OUTPUT fact-scvat).
        FIND FIRST t-amount-list WHERE t-amount-list.nr EQ menu-nr NO-LOCK NO-ERROR.
        IF NOT AVAILABLE t-amount-list THEN
        DO:
            CREATE t-amount-list.
            ASSIGN
                t-amount-list.nr = menu-nr                
                t-amount-list.anzahl = anzahl
                t-amount-list.amount = (price * fact-scvat) * anzahl.
                amount = amount + t-amount-list.amount
                .
        END.     
        ELSE
        DO:
            IF t-amount-list.anzahl NE anzahl THEN
            DO:
                ASSIGN
                    t-amount-list.anzahl = anzahl
                    t-amount-list.amount = (price * fact-scvat) * anzahl.                    
                    .
            END.
        END.

        amount = 0.
        FOR EACH t-amount-list:
            amount = amount + t-amount-list.amount.
        END.
        amount = amount + balance.
    END.  
    ELSE
    DO:     
        FIND FIRST t-amount-list WHERE t-amount-list.nr EQ menu-nr NO-LOCK NO-ERROR.
        IF NOT AVAILABLE t-amount-list THEN
        DO:
            CREATE t-amount-list.
            ASSIGN
                t-amount-list.nr = menu-nr   
                t-amount-list.anzahl = anzahl
                t-amount-list.amount = price * anzahl.
                amount = amount + t-amount-list.amount
                .  
        END.    
        ELSE
        DO:
            IF t-amount-list.anzahl NE anzahl THEN
            DO:
                ASSIGN
                    t-amount-list.anzahl = anzahl
                    t-amount-list.amount = (price * fact-scvat) * anzahl.                    
                    .
            END.            
        END.

        amount = 0.
        FOR EACH t-amount-list:
            amount = amount + t-amount-list.amount.
        END.
        amount = amount + balance.
    END.
END.
ELSE
DO:
    FIND FIRST t-amount-list WHERE t-amount-list.nr EQ menu-nr NO-LOCK NO-ERROR.
    IF AVAILABLE t-amount-list THEN
    DO:
        /*amount = amount - t-amount-list.amount.*/
        DELETE t-amount-list.
    END.

    amount = 0.
    FOR EACH t-amount-list:
        amount = amount + t-amount-list.amount.
    END.
    amount = amount + balance.

    /*
    curr-nr = 0.
    FOR EACH t-amount-list WHERE t-amount-list.nr GT 0 BY t-amount-list.nr:  
        curr-nr = curr-nr + 1.  
        t-amount-list.nr = curr-nr.  
    END. 
    */
END.

