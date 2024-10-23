DEFINE TEMP-TABLE t-bkqueasy1 LIKE bk-queasy.

DEFINE INPUT PARAMETER case-type AS INTEGER NO-UNDO.
DEFINE INPUT PARAMETER TABLE FOR t-bkqueasy1.

DEFINE OUTPUT PARAMETER success-flag AS LOGICAL NO-UNDO.


CASE case-type:
    WHEN 1 THEN DO: 
        FIND FIRST t-bkqueasy1 NO-LOCK NO-ERROR.
        IF AVAILABLE t-bkqueasy1 THEN DO:
            FIND FIRST bk-queasy WHERE bk-queasy.KEY = t-bkqueasy1.KEY
                AND bk-queasy.number1 = t-bkqueasy1.number1 NO-LOCK NO-ERROR.
            IF NOT AVAILABLE bk-queasy THEN DO:
                CREATE bk-queasy.
                BUFFER-COPY t-bkqueasy1 TO bk-queasy.
            END.
            ELSE DO:
                FIND CURRENT bk-queasy EXCLUSIVE-LOCK.
                BUFFER-COPY t-bkqueasy1 TO bk-queasy.
                FIND CURRENT bk-queasy NO-LOCK.
                RELEASE bk-queasy.
            END.
        END.
        ASSIGN success-flag = YES.
    END.    
END CASE.
