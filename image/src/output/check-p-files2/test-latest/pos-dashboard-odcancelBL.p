DEFINE TEMP-TABLE cancellation-list  
    FIELD bill-date         AS DATE  
    FIELD table-no          AS INTEGER
    FIELD bill-no           AS INTEGER
    FIELD order-no          AS INTEGER
    FIELD article-no        AS INTEGER   
    FIELD article-name      AS CHARACTER   
    FIELD cancel-reason     AS CHARACTER
    FIELD qty               AS INTEGER
    FIELD amount            AS DECIMAL
    FIELD dept-name         AS CHARACTER
    FIELD cancel-time       AS CHARACTER
    FIELD cancel-id         AS CHARACTER    
.  

DEFINE INPUT PARAMETER from-date    AS DATE.
DEFINE INPUT PARAMETER to-date      AS DATE.
DEFINE INPUT PARAMETER from-dept    AS INTEGER.
DEFINE INPUT PARAMETER to-dept      AS INTEGER.
DEFINE OUTPUT PARAMETER TABLE FOR cancellation-list.

RUN create-cancellation.

PROCEDURE create-cancellation:
    DEFINE VARIABLE curr-date AS DATE NO-UNDO.
    DEFINE VARIABLE canceled-name AS CHARACTER NO-UNDO.

    FOR EACH cancellation-list:
        DELETE cancellation-list.
    END.

    FOR EACH hoteldpt WHERE hoteldpt.num GE from-dept 
        AND hoteldpt.num LE to-dept NO-LOCK BY hoteldpt.num: 

        FOR EACH queasy WHERE queasy.KEY = 225
            AND queasy.char1 EQ "orderbill-line"
            AND queasy.date1 GE from-date
            AND queasy.date1 LE to-date
            AND INT(ENTRY(1, queasy.char2, "|")) EQ hoteldpt.num
            AND NUM-ENTRIES(queasy.char3, "|") GT 8 NO-LOCK
            BY queasy.date1 BY queasy.number2 BY ENTRY(10, queasy.char3, "|"):

            FIND FIRST bediener WHERE bediener.userinit EQ ENTRY(11, queasy.char3, "|") NO-LOCK NO-ERROR.
            IF AVAILABLE bediener THEN
            DO:
                canceled-name = bediener.username.
            END.
    
            CREATE cancellation-list.
            ASSIGN
                cancellation-list.bill-date      = queasy.date1
                cancellation-list.table-no       = queasy.number2    
                cancellation-list.order-no       = queasy.number1
                cancellation-list.article-no     = INT(ENTRY(2, queasy.char3, "|"))
                cancellation-list.article-name   = ENTRY(3, queasy.char3, "|")
                cancellation-list.cancel-reason  = ENTRY(9, queasy.char3, "|")
                cancellation-list.qty            = INT(ENTRY(4, queasy.char3, "|"))                
                cancellation-list.dept-name      = hoteldpt.depart
                cancellation-list.cancel-time    = ENTRY(10, queasy.char3, "|")
                cancellation-list.cancel-id      = canceled-name
            .
    
        END.
    END.
END PROCEDURE.
