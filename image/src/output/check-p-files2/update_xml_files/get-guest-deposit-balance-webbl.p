DEFINE TEMP-TABLE gdeposit-list
    FIELD gdeposit-balance  AS DECIMAL
    FIELD guest-deposit-num AS INTEGER
    FIELD guest-type        AS CHARACTER
    .

DEFINE INPUT PARAMETER guest-number         AS INTEGER.
DEFINE OUTPUT PARAMETER TABLE FOR gdeposit-list.

DEFINE VARIABLE depoart-guest       AS INTEGER NO-UNDO.
DEFINE VARIABLE depobez-guest       AS CHARACTER NO-UNDO.
DEFINE VARIABLE depoart-rsv         AS INTEGER NO-UNDO.
DEFINE VARIABLE depoart-bqt         AS INTEGER NO-UNDO.
DEFINE VARIABLE depoart-pos         AS INTEGER NO-UNDO.
DEFINE VARIABLE depo-balance        AS DECIMAL NO-UNDO.

CREATE gdeposit-list.

FIND FIRST htparam WHERE htparam.paramnr EQ 1068 NO-LOCK NO-ERROR. 
IF AVAILABLE htparam THEN
DO:
    gdeposit-list.guest-deposit-num = htparam.finteger.
    FIND FIRST artikel WHERE artikel.artnr EQ htparam.finteger AND artikel.departement EQ 0 NO-LOCK NO-ERROR.
    IF AVAILABLE artikel AND artikel.artart EQ 5 THEN
    DO:
        ASSIGN 
            depoart-guest = artikel.artnr
            depobez-guest = artikel.bezeich
            .    
    END.    
END. 

FIND FIRST guest WHERE guest.gastnr EQ guest-number NO-LOCK NO-ERROR.
IF AVAILABLE guest THEN 
DO:
    IF guest.karteityp EQ 0 THEN gdeposit-list.guest-type = "Individual".
    ELSE IF guest.karteityp EQ 1 THEN gdeposit-list.guest-type = "Company".
    ELSE gdeposit-list.guest-type = "Travel Agent".
END.

IF gdeposit-list.guest-deposit-num NE 0 AND gdeposit-list.guest-type NE "Individual" THEN
DO:
    FIND FIRST htparam WHERE htparam.paramnr EQ 120 NO-LOCK NO-ERROR. 
    IF AVAILABLE htparam THEN depoart-rsv = htparam.finteger.

    FIND FIRST htparam WHERE htparam.paramnr EQ 117 NO-LOCK NO-ERROR. 
    IF AVAILABLE htparam THEN depoart-bqt = htparam.finteger.

    FIND FIRST htparam WHERE htparam.paramnr EQ 1361 NO-LOCK NO-ERROR. 
    IF AVAILABLE htparam THEN depoart-pos = htparam.finteger.

    FIND FIRST billjournal WHERE billjournal.billjou-ref EQ guest-number
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
        FIND FIRST billjournal WHERE billjournal.billjou-ref EQ guest-number
            AND billjournal.artnr NE 0
            AND billjournal.artnr NE depoart-guest
            AND billjournal.artnr NE depoart-rsv
            AND billjournal.artnr NE depoart-bqt
            AND billjournal.artnr NE depoart-pos        
            AND NUM-ENTRIES(billjournal.bezeich,"[") GT 1
            AND SUBSTR(ENTRY(2,billjournal.bezeich,"["),1,13) EQ "Guest Deposit" NO-LOCK NO-ERROR.
        DO WHILE AVAILABLE billjournal:
        
            depo-balance = depo-balance + (- billjournal.betrag).
            
            FIND NEXT billjournal WHERE billjournal.billjou-ref EQ guest-number
                AND billjournal.artnr NE 0            
                AND billjournal.artnr NE depoart-guest
                AND billjournal.artnr NE depoart-rsv
                AND billjournal.artnr NE depoart-bqt
                AND billjournal.artnr NE depoart-pos
                AND NUM-ENTRIES(billjournal.bezeich,"[") GT 1
                AND SUBSTR(ENTRY(2,billjournal.bezeich,"["),1,13) EQ "Guest Deposit" NO-LOCK NO-ERROR.
        END.
    
        /* Get All Deposit Amount(-) From Bill */
        FOR EACH bill WHERE bill.rechnr GT 0 AND bill.gastnr EQ guest-number NO-LOCK,
            EACH bill-line WHERE bill-line.rechnr EQ bill.rechnr
            AND bill-line.artnr EQ depoart-guest NO-LOCK:
            
            depo-balance = depo-balance + bill-line.betrag.   
        END.    
    
        gdeposit-list.gdeposit-balance = depo-balance.
    END.    
END.
