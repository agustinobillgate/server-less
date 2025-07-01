DEFINE TEMP-TABLE journal-list  
    FIELD bill-date         AS DATE  
    FIELD table-no          AS INTEGER 
    FIELD bill-no           AS INTEGER
    FIELD order-no          AS INTEGER
    FIELD article-no        AS INTEGER   
    FIELD article-name      AS CHARACTER       
    FIELD qty               AS INTEGER
    FIELD amount            AS DECIMAL
    FIELD payment           AS DECIMAL
    FIELD dept-name         AS CHARACTER
    FIELD id                AS CHARACTER
    FIELD bill-time         AS CHARACTER 
    FIELD guest-name        AS CHARACTER    
    FIELD room-no           AS CHARACTER    
.  

DEFINE TEMP-TABLE t-list
    FIELD bill-date AS DATE
    FIELD dept-no   AS INTEGER
    FIELD rechnr    AS INTEGER
    .

DEFINE INPUT PARAMETER from-date    AS DATE.
DEFINE INPUT PARAMETER to-date      AS DATE.
DEFINE INPUT PARAMETER from-dept    AS INTEGER.
DEFINE INPUT PARAMETER to-dept      AS INTEGER.
DEFINE OUTPUT PARAMETER TABLE FOR journal-list.

DEFINE VARIABLE disc-art1 AS INTEGER.
DEFINE VARIABLE disc-art2 AS INTEGER.
DEFINE VARIABLE disc-art3 AS INTEGER.

FIND FIRST vhp.htparam WHERE paramnr = 557 NO-LOCK. 
disc-art1 = vhp.htparam.finteger. 
FIND FIRST vhp.htparam WHERE paramnr = 596 NO-LOCK. 
disc-art2 = vhp.htparam.finteger. 
FIND FIRST vhp.htparam WHERE paramnr = 556 NO-LOCK. 
disc-art3 = vhp.htparam.finteger.

RUN journal-list.

PROCEDURE journal-list:
    DEFINE VARIABLE qty AS INTEGER FORMAT "->>>,>>9" INITIAL 0. 
    DEFINE VARIABLE sub-tot AS DECIMAL FORMAT "->,>>>,>>>,>>9.99" INITIAL 0. 
    DEFINE VARIABLE tot AS DECIMAL FORMAT "->,>>>,>>>,>>9.99" INITIAL 0. 
    DEFINE VARIABLE sub-tot1 AS DECIMAL FORMAT "->,>>>,>>>,>>9.99" INITIAL 0. 
    DEFINE VARIABLE tot1 AS DECIMAL FORMAT "->,>>>,>>>,>>9.99" INITIAL 0. 
    DEFINE VARIABLE curr-date AS DATE. 
    DEFINE VARIABLE last-dept AS INTEGER INITIAL -1. 
    DEFINE VARIABLE it-exist AS LOGICAL.  
    DEFINE VARIABLE curr-guest AS CHARACTER.    
    DEFINE VARIABLE curr-room  AS CHARACTER. 
    DEFINE VARIABLE validate-rechnr AS INTEGER.
    DEFINE VARIABLE mess-str AS CHARACTER. 
    DEFINE VARIABLE i-str AS INT.
    DEFINE VARIABLE mess-token AS CHAR.
    DEFINE VARIABLE mess-keyword AS CHAR.
    DEFINE VARIABLE mess-value AS CHAR.
    DEFINE VARIABLE dept-i AS INT.
    
    FOR EACH journal-list:
        DELETE journal-list.
    END.

    FOR EACH queasy WHERE queasy.KEY EQ 225
        AND queasy.char1 EQ "orderbill"
        AND NUM-ENTRIES(queasy.char2, "|") GT 7
        AND ENTRY(8, queasy.char2, "|") MATCHES "*BL=*" NO-LOCK:

        mess-str = queasy.char2.
        DO i-str = 1 TO NUM-ENTRIES(mess-str, "|"):
            mess-token   = ENTRY(i-str,mess-str,"|").
            mess-keyword = ENTRY(1,mess-token,"=").
            mess-value   = ENTRY(2,mess-token,"=").
            IF mess-keyword EQ "BL" THEN validate-rechnr = INT(mess-value).
            IF validate-rechnr NE 0 THEN LEAVE.
        END.

        IF validate-rechnr NE 0 THEN
        DO:
            FIND FIRST t-list WHERE t-list.rechnr EQ validate-rechnr
                AND t-list.bill-date EQ queasy.date1
                AND t-list.dept-no EQ queasy.number1 NO-LOCK NO-ERROR.
            IF NOT AVAILABLE t-list THEN
            DO:
                CREATE t-list.
                ASSIGN
                    t-list.bill-date     = queasy.date1
                    t-list.dept-no       = queasy.number1
                    t-list.rechnr        = validate-rechnr
                    .
            END.
            validate-rechnr = 0.
        END.
    END.
        
    FOR EACH hoteldpt WHERE hoteldpt.num GE from-dept AND hoteldpt.num LE to-dept NO-LOCK BY hoteldpt.num: 
        sub-tot = 0. 
        sub-tot1 = 0. 
        it-exist = NO. 
        qty = 0.
        
        FOR EACH h-journal WHERE h-journal.bill-datum GE from-date 
            AND h-journal.bill-datum LE to-date 
            AND h-journal.departement EQ hoteldpt.num NO-LOCK,
            FIRST t-list WHERE t-list.rechnr EQ h-journal.rechnr
            AND t-list.dept-no EQ h-journal.departement
            NO-LOCK BY h-journal.rechnr BY h-journal.sysdate BY h-journal.zeit: 

            FIND FIRST h-artikel WHERE h-artikel.artnr EQ h-journal.artnr 
                AND h-artikel.departement EQ h-journal.departement NO-LOCK NO-ERROR. 
            
            it-exist = YES. 
            
            curr-guest = "".
            curr-room  = "".
            FIND FIRST h-bill WHERE h-bill.rechnr = h-journal.rechnr 
                AND h-bill.departement = h-journal.departement NO-LOCK NO-ERROR.
            IF AVAILABLE h-bill THEN
            DO:
                IF h-bill.resnr GT 0 AND h-bill.reslinnr GT 0 THEN
                DO:
                    FIND FIRST res-line WHERE res-line.resnr = h-bill.resnr AND res-line.reslinnr = h-bill.reslinnr NO-LOCK NO-ERROR.
                    IF AVAILABLE res-line THEN
                    DO:
                        ASSIGN
                            curr-guest = res-line.NAME
                            curr-room  = res-line.zinr.
                    END.                            
                END.
                ELSE IF h-bill.resnr GT 0 THEN
                DO:
                    FIND FIRST guest WHERE guest.gastnr = h-bill.resnr NO-LOCK NO-ERROR.
                    IF AVAILABLE guest THEN
                    ASSIGN
                        curr-guest = guest.NAME + "," + guest.vorname1
                        curr-room  = "".
                END.
                ELSE IF h-bill.resnr = 0 THEN 
                DO:
                    ASSIGN
                        curr-guest = h-bill.bilname
                        curr-room  = "".
                END.
            END.

            IF (h-journal.artnr EQ disc-art1 OR h-journal.artnr EQ disc-art2
                OR h-journal.artnr EQ disc-art3) AND h-journal.betrag EQ 0 THEN .
            ELSE
            DO:
                CREATE journal-list. 
                ASSIGN
                    journal-list.guest-name     = curr-guest
                    journal-list.bill-date      = h-journal.bill-datum
                    journal-list.table-no       = h-journal.tischnr
                    journal-list.bill-no        = h-journal.rechnr
                    journal-list.article-no     = h-journal.artnr
                    journal-list.article-name   = h-journal.bezeich
                    journal-list.dept-name      = hoteldpt.depart
                    journal-list.qty            = h-journal.anzahl
                .
                                            
                IF AVAILABLE h-artikel AND h-artikel.artart = 0 THEN 
                DO:                        
                    journal-list.amount = h-journal.betrag.
                    journal-list.payment = 0.

                    sub-tot = sub-tot + h-journal.betrag. 
                    tot     = tot + h-journal.betrag. 
                END. 
                ELSE IF h-journal.artnr = 0 AND SUBSTR(h-journal.bezeich, 1, 9) = "To Table " THEN 
                DO: 
                    journal-list.amount = h-journal.betrag.
                    journal-list.payment = 0.

                    sub-tot = sub-tot + h-journal.betrag. 
                    tot     = tot + h-journal.betrag. 
                END. 
                ELSE IF h-journal.artnr = 0 AND SUBSTR(h-journal.bezeich, 1, 11) = "From Table " THEN 
                DO: 
                    journal-list.amount = h-journal.betrag.
                    journal-list.payment = 0.

                    sub-tot = sub-tot + h-journal.betrag. 
                    tot     = tot + h-journal.betrag. 
                END. 
                ELSE 
                DO: 
                    journal-list.amount = 0.
                    journal-list.payment = h-journal.betrag.

                    sub-tot1 = sub-tot1 + h-journal.betrag. 
                    tot1     = tot1 + h-journal.betrag. 
                END. 
        
                journal-list.id = STRING(h-journal.kellner-nr, "9999").
                journal-list.bill-time = STRING(h-journal.zeit, "HH:MM:SS").
                journal-list.room-no = curr-room.

                qty = qty + h-journal.anzahl.
            END.
        END.                      
        IF it-exist THEN 
        DO: 
            CREATE journal-list. 
            ASSIGN
                journal-list.article-name   = "T O T A L"
                journal-list.qty            = qty
                journal-list.amount         = sub-tot
                journal-list.payment        = sub-tot1
            .                   
        END.    
    END.
END PROCEDURE.
