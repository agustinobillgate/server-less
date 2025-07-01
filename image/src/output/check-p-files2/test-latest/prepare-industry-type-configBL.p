
DEFINE TEMP-TABLE t-queasy LIKE queasy.
DEFINE TEMP-TABLE temp-list
    FIELD number1       AS INTEGER   FORMAT ">>>"
    FIELD number2       AS INTEGER   FORMAT ">>>"
    FIELD char1         AS CHARACTER FORMAT "x(50)"
    FIELD number3       AS INTEGER   FORMAT ">>>>>>>>>>"
    FIELD category      AS CHARACTER FORMAT "x(40)".

DEFINE OUTPUT PARAMETER TABLE FOR t-queasy.
DEFINE OUTPUT PARAMETER TABLE FOR temp-list.

DEFINE BUFFER b-queasy FOR queasy.

FOR EACH t-queasy:
    DELETE t-queasy.
END.

FOR EACH temp-list:
    DELETE temp-list.
END.

FOR EACH queasy WHERE queasy.KEY EQ 281 NO-LOCK:
    CREATE t-queasy.
    BUFFER-COPY queasy TO t-queasy.
END.

FOR EACH queasy WHERE queasy.KEY EQ 282 NO-LOCK:
    FIND FIRST b-queasy WHERE b-queasy.KEY EQ 281 AND b-queasy.number1 EQ queasy.number1 NO-LOCK NO-ERROR.
    IF AVAILABLE b-queasy THEN
    DO:
        CREATE temp-list.
        ASSIGN
            temp-list.number1 = queasy.number1
            temp-list.number2 = queasy.number2
            temp-list.char1   = queasy.char1
            temp-list.number3 = queasy.number3.
        IF queasy.number1 EQ b-queasy.number1 THEN
        DO:
            temp-list.category = b-queasy.char1.
        END.
    END.
END.

