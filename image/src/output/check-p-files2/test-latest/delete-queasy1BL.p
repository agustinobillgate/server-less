
DEF INPUT PARAMETER case-type AS INTEGER.
DEF INPUT PARAMETER int1  AS INT.
DEF INPUT PARAMETER int2  AS INT.
DEF INPUT PARAMETER int3  AS INT.
DEF INPUT PARAMETER char1  AS CHAR.
DEF OUTPUT PARAMETER success-flag AS LOGICAL INITIAL NO NO-UNDO.

  
CASE case-type:
    WHEN 1 THEN
    DO:
        FIND FIRST queasy WHERE queasy.KEY = int1 
            AND queasy.number1 = int2
            AND queasy.number2 = int3
            AND queasy.char1 = char1 EXCLUSIVE-LOCK NO-ERROR.
        IF AVAILABLE queasy THEN
        DO:
            DELETE queasy.
            RELEASE queasy.
            ASSIGN success-flag = YES.
        END.
    END.
    WHEN 2 THEN
    DO:
        FIND FIRST queasy WHERE RECID(queasy) = int1 EXCLUSIVE-LOCK NO-ERROR.
        IF AVAILABLE queasy THEN
        DO:
            DELETE queasy.
            RELEASE queasy.
            ASSIGN success-flag = YES.
        END.
    END.
END CASE.
