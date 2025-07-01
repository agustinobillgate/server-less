DEFINE TEMP-TABLE guest-deposit
    FIELD guest-number      AS INTEGER  
    FIELD guest-name        AS CHARACTER
    FIELD guest-type        AS CHARACTER
    FIELD deposit-amount    AS DECIMAL
    FIELD deposit-used      AS DECIMAL
    FIELD deposit-balance   AS DECIMAL    
    .

DEFINE TEMP-TABLE temp-guest-deposit
    FIELD guest-number      AS INTEGER  
    FIELD guest-name        AS CHARACTER
    FIELD guest-type        AS CHARACTER
    FIELD deposit-amount    AS DECIMAL
    FIELD deposit-used      AS DECIMAL
    FIELD deposit-balance   AS DECIMAL    
    .

DEFINE TEMP-TABLE payload-list
    FIELD v-mode       AS INTEGER
    FIELD user-init    AS CHARACTER
    FIELD guest-number AS INTEGER
    FIELD guest-name   AS CHARACTER
    .

DEFINE INPUT PARAMETER TABLE FOR payload-list. 
DEFINE INPUT PARAMETER pvILanguage      AS INTEGER NO-UNDO.
DEFINE OUTPUT PARAMETER error-desc      AS CHARACTER.
DEFINE OUTPUT PARAMETER TABLE FOR guest-deposit.

{SupertransBL.i} 
DEFINE VARIABLE lvCAREA AS CHAR INITIAL "guest-deposit". 

DEFINE VARIABLE depoart-guest       AS INTEGER NO-UNDO.
DEFINE VARIABLE depobez-guest       AS CHARACTER NO-UNDO.
DEFINE VARIABLE depoart-rsv         AS INTEGER NO-UNDO.
DEFINE VARIABLE depoart-bqt         AS INTEGER NO-UNDO.
DEFINE VARIABLE depoart-pos         AS INTEGER NO-UNDO.
DEFINE VARIABLE total-deposit       AS DECIMAL NO-UNDO.
DEFINE VARIABLE total-used          AS DECIMAL NO-UNDO.
DEFINE VARIABLE total-balance       AS DECIMAL NO-UNDO.

FIND FIRST payload-list.
IF NOT AVAILABLE payload-list THEN
DO:
    error-desc = translateExtended ("No data available.",lvCAREA,"").
    RETURN.
END.

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
        depoart-guest = artikel.artnr
        depobez-guest = artikel.bezeich
        .
END.

FIND FIRST htparam WHERE htparam.paramnr EQ 120 NO-LOCK NO-ERROR. 
IF AVAILABLE htparam THEN depoart-rsv = htparam.finteger.

FIND FIRST htparam WHERE htparam.paramnr EQ 117 NO-LOCK NO-ERROR. 
IF AVAILABLE htparam THEN depoart-bqt = htparam.finteger.

FIND FIRST htparam WHERE htparam.paramnr EQ 1361 NO-LOCK NO-ERROR. 
IF AVAILABLE htparam THEN depoart-pos = htparam.finteger.

IF payload-list.v-mode EQ 1 THEN     /*ALL Guest Have Deposit*/
DO:
    FIND FIRST billjournal WHERE billjournal.billjou-ref NE 0
        AND billjournal.artnr NE 0
        AND billjournal.artnr NE depoart-guest
        AND billjournal.artnr NE depoart-rsv
        AND billjournal.artnr NE depoart-bqt
        AND billjournal.artnr NE depoart-pos        
        AND NUM-ENTRIES(billjournal.bezeich,"[") GT 1
        AND SUBSTR(ENTRY(2,billjournal.bezeich,"["),1,13) EQ "Guest Deposit" NO-LOCK NO-ERROR.
    IF AVAILABLE billjournal THEN
    DO:
        /* Get All Deposit Payment */
        FIND FIRST billjournal WHERE billjournal.billjou-ref NE 0
            AND billjournal.artnr NE 0
            AND billjournal.artnr NE depoart-guest
            AND billjournal.artnr NE depoart-rsv
            AND billjournal.artnr NE depoart-bqt
            AND billjournal.artnr NE depoart-pos        
            AND NUM-ENTRIES(billjournal.bezeich,"[") GT 1
            AND SUBSTR(ENTRY(2,billjournal.bezeich,"["),1,13) EQ "Guest Deposit" NO-LOCK NO-ERROR.                   
        DO WHILE AVAILABLE billjournal:

            FIND FIRST temp-guest-deposit WHERE temp-guest-deposit.guest-number EQ billjournal.billjou-ref NO-LOCK NO-ERROR.
            IF NOT AVAILABLE temp-guest-deposit THEN
            DO:
                CREATE temp-guest-deposit.
                temp-guest-deposit.guest-number = billjournal.billjou-ref.
                    
                FIND FIRST guest WHERE guest.gastnr EQ temp-guest-deposit.guest-number NO-LOCK NO-ERROR.
                IF AVAILABLE guest THEN
                DO:
                    temp-guest-deposit.guest-name = guest.name + ", " + guest.anredefirma.

                    IF guest.karteityp EQ 0 THEN temp-guest-deposit.guest-type = "Individual".
                    ELSE IF guest.karteityp EQ 1 THEN temp-guest-deposit.guest-type = "Company".
                    ELSE temp-guest-deposit.guest-type = "Travel Agent".
                END.
            END.

            ASSIGN                       
                temp-guest-deposit.deposit-amount   = temp-guest-deposit.deposit-amount + (- billjournal.betrag)
                temp-guest-deposit.deposit-balance  = temp-guest-deposit.deposit-balance + (- billjournal.betrag)          
                total-deposit                       = total-deposit + (- billjournal.betrag)
                total-balance                       = total-balance + (- billjournal.betrag)
                .   

            FIND NEXT billjournal WHERE billjournal.billjou-ref NE 0
                AND billjournal.artnr NE 0
                AND billjournal.artnr NE depoart-guest
                AND billjournal.artnr NE depoart-rsv
                AND billjournal.artnr NE depoart-bqt
                AND billjournal.artnr NE depoart-pos        
                AND NUM-ENTRIES(billjournal.bezeich,"[") GT 1
                AND SUBSTR(ENTRY(2,billjournal.bezeich,"["),1,13) EQ "Guest Deposit" NO-LOCK NO-ERROR.   
        END.        

        FOR EACH temp-guest-deposit BY temp-guest-deposit.guest-name:
            CREATE guest-deposit.
            BUFFER-COPY temp-guest-deposit TO guest-deposit.
        END.

        /* Get All Deposit Amount(-) From Bill */
        FIND FIRST guest-deposit NO-LOCK NO-ERROR.
        IF AVAILABLE guest-deposit THEN
        DO:
            FOR EACH guest-deposit,
                EACH bill WHERE bill.rechnr GT 0 AND bill.gastnr EQ guest-deposit.guest-number NO-LOCK,
                    EACH bill-line WHERE bill-line.rechnr EQ bill.rechnr
                    AND bill-line.artnr EQ depoart-guest NO-LOCK:
                
                    ASSIGN        
                        guest-deposit.deposit-used      = guest-deposit.deposit-used + bill-line.betrag
                        guest-deposit.deposit-balance   = guest-deposit.deposit-balance + bill-line.betrag
                        total-used                      = total-used + bill-line.betrag
                        total-balance                   = total-balance + bill-line.betrag
                        .                 
            END.
        END.        

        FIND FIRST guest-deposit NO-LOCK NO-ERROR.
        IF AVAILABLE guest-deposit THEN
        DO:
            CREATE guest-deposit.
            ASSIGN
                guest-deposit.guest-name        = "T O T A L"
                guest-deposit.deposit-amount    = total-deposit
                guest-deposit.deposit-used      = total-used
                guest-deposit.deposit-balance   = total-balance
                .

        END.
    END.
END.
ELSE    /*Selected Guest*/
DO:
    CREATE guest-deposit.
    guest-deposit.guest-number = payload-list.guest-number.
    guest-deposit.guest-name = payload-list.guest-name.

    FIND FIRST guest WHERE guest.gastnr EQ payload-list.guest-number NO-LOCK NO-ERROR.
    IF AVAILABLE guest THEN
    DO:
        IF guest.karteityp EQ 0 THEN guest-deposit.guest-type = "Individual".
        ELSE IF guest.karteityp EQ 1 THEN guest-deposit.guest-type = "Company".
        ELSE guest-deposit.guest-type = "Travel Agent".
    END.
    
    /* Get All Deposit Payment */
    FIND FIRST billjournal WHERE billjournal.billjou-ref EQ payload-list.guest-number
        AND billjournal.artnr NE 0
        AND billjournal.artnr NE depoart-guest
        AND billjournal.artnr NE depoart-rsv
        AND billjournal.artnr NE depoart-bqt
        AND billjournal.artnr NE depoart-pos        
        AND NUM-ENTRIES(billjournal.bezeich,"[") GT 1
        AND SUBSTR(ENTRY(2,billjournal.bezeich,"["),1,13) EQ "Guest Deposit" NO-LOCK NO-ERROR.
    DO WHILE AVAILABLE billjournal:
        
        ASSIGN        
            guest-deposit.deposit-amount   = guest-deposit.deposit-amount + (- billjournal.betrag)
            guest-deposit.deposit-balance  = guest-deposit.deposit-balance + (- billjournal.betrag)
            .    
            
        FIND NEXT billjournal WHERE billjournal.billjou-ref EQ payload-list.guest-number
            AND billjournal.artnr NE 0
            AND billjournal.artnr NE depoart-guest
            AND billjournal.artnr NE depoart-rsv
            AND billjournal.artnr NE depoart-bqt
            AND billjournal.artnr NE depoart-pos        
            AND NUM-ENTRIES(billjournal.bezeich,"[") GT 1
            AND SUBSTR(ENTRY(2,billjournal.bezeich,"["),1,13) EQ "Guest Deposit" NO-LOCK NO-ERROR.
    END.
    
    /* Get All Deposit Amount(-) From Bill */
    FOR EACH bill WHERE bill.rechnr GT 0 AND bill.gastnr EQ payload-list.guest-number NO-LOCK,
        EACH bill-line WHERE bill-line.rechnr EQ bill.rechnr
        AND bill-line.artnr EQ depoart-guest NO-LOCK:
    
        ASSIGN        
            guest-deposit.deposit-used      = guest-deposit.deposit-used + bill-line.betrag
            guest-deposit.deposit-balance   = guest-deposit.deposit-balance + bill-line.betrag
            . 
    END.
END.

