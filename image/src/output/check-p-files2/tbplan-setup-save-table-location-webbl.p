
DEF TEMP-TABLE t-queasy LIKE queasy
    FIELD rec-id AS INT.

DEF INPUT PARAMETER case-type AS INTEGER.
DEF INPUT PARAMETER TABLE FOR t-queasy.
DEF OUTPUT PARAMETER success-flag AS LOGICAL INIT NO.

FIND FIRST t-queasy NO-ERROR.
IF NOT AVAILABLE t-queasy THEN RETURN NO-APPLY.

CASE case-type:
    WHEN 1 THEN
    DO:
        FIND FIRST queasy WHERE RECID(queasy) = t-queasy.rec-id EXCLUSIVE-LOCK NO-ERROR.
        IF AVAILABLE t-queasy THEN
        DO:
            BUFFER-COPY t-queasy TO queasy.
            RELEASE queasy.
            success-flag = YES.
        END.        
    END.
    WHEN 2 THEN
    DO:
        FIND FIRST t-queasy NO-LOCK NO-ERROR.
        DO WHILE AVAILABLE t-queasy:
            
            FIND FIRST queasy WHERE queasy.KEY EQ t-queasy.KEY
                AND queasy.number1 EQ t-queasy.number1
                AND queasy.number2 EQ t-queasy.number2
                AND (queasy.deci1 NE t-queasy.deci1 
                OR queasy.deci2 NE t-queasy.deci2)
                AND queasy.betriebsnr EQ 0 NO-LOCK NO-ERROR.
            IF AVAILABLE queasy THEN
            DO:
                FIND CURRENT queasy EXCLUSIVE-LOCK.
                ASSIGN
                    queasy.deci1 = t-queasy.deci1
                    queasy.deci2 = t-queasy.deci2
                .
                FIND CURRENT queasy NO-LOCK.
                RELEASE queasy.
                success-flag = YES.
            END.

            FIND NEXT t-queasy NO-LOCK NO-ERROR.
        END. 
    END.
END CASE.


