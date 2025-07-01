
DEF TEMP-TABLE book-engine-list LIKE queasy.

DEF INPUT  PARAMETER TABLE FOR book-engine-list.
DEF INPUT  PARAMETER icase AS INT.

FIND FIRST book-engine-list.
IF icase = 1 THEN
DO:
    CREATE queasy.
    ASSIGN
        queasy.KEY     = 159
        queasy.number1 = book-engine-list.number1
        queasy.char1   = book-engine-list.char1
        queasy.number2 = book-engine-list.number2.
END.
ELSE
DO:
    FIND FIRST queasy WHERE queasy.KEY = 159 AND 
        queasy.number1 = book-engine-list.number1 NO-LOCK NO-ERROR.
    IF AVAILABLE queasy THEN
    DO:
        BUFFER-COPY book-engine-list TO queasy.
    END.
END.
