DEFINE TEMP-TABLE t-bkqueasy LIKE bk-queasy.

DEFINE INPUT PARAMETER case-type AS INTEGER NO-UNDO.
DEFINE INPUT PARAMETER TABLE FOR t-bkqueasy.

DEFINE OUTPUT PARAMETER success-flag AS LOGICAL INITIAL NO NO-UNDO.

CASE case-type:
    WHEN 1 THEN DO:
        FIND FIRST t-bkqueasy NO-LOCK NO-ERROR.
        IF AVAILABLE t-bkqueasy THEN DO:            
            FIND FIRST bk-queasy WHERE bk-queasy.KEY = t-bkqueasy.KEY
                AND bk-queasy.number1 = t-bkqueasy.number1 NO-LOCK NO-ERROR.
            IF AVAILABLE bk-queasy THEN DO:
                FIND CURRENT bk-queasy EXCLUSIVE-LOCK.
                DELETE bk-queasy.
                RELEASE bk-queasy.
                ASSIGN success-flag = YES.
            END.
        END.
    END.
    WHEN 2 THEN DO:       
        FIND FIRST t-bkqueasy NO-LOCK NO-ERROR.
        IF AVAILABLE t-bkqueasy THEN DO:               
            FIND FIRST bk-queasy WHERE bk-queasy.KEY = t-bkqueasy.KEY
                AND bk-queasy.number1 = t-bkqueasy.number1 
                AND bk-queasy.number2 = t-bkqueasy.number2 NO-LOCK NO-ERROR.
            IF AVAILABLE bk-queasy THEN DO:                
                FIND CURRENT bk-queasy EXCLUSIVE-LOCK.
                DELETE bk-queasy.
                RELEASE bk-queasy.
                ASSIGN success-flag = YES.               
            END.
        END.
    END.
END CASE.
