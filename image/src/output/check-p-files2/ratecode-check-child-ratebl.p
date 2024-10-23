
DEFINE INPUT PARAMETER case-type AS INTEGER NO-UNDO.
DEFINE INPUT PARAMETER inpChar1  AS CHARACTER NO-UNDO.

DEFINE OUTPUT PARAMETER child-rate AS LOGICAL NO-UNDO INITIAL NO.

CASE case-type:
    WHEN 1 THEN
    DO:
        FIND FIRST queasy WHERE queasy.KEY = 2 NO-LOCK NO-ERROR.
        DO WHILE AVAILABLE queasy:   
            IF queasy.char3 NE "" THEN
            DO:
                IF ENTRY(2, queasy.char3, ";") = inpChar1 THEN
                DO:
                    ASSIGN child-rate = YES.
                    LEAVE.
                END.
            END.            
            FIND NEXT queasy WHERE queasy.KEY = 2 NO-LOCK NO-ERROR.
        END.
    END.
END CASE.
