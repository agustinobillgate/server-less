DEFINE TEMP-TABLE setup-list
    FIELD setup-number AS INT
    FIELD setup-param AS CHAR
    FIELD setup-value AS CHAR
    .

DEFINE INPUT PARAMETER outlet-number AS INT.
DEFINE OUTPUT PARAMETER TABLE FOR setup-list.

FOR EACH queasy WHERE queasy.key EQ 222 
    AND queasy.number1 EQ 1 
    AND queasy.betriebsnr EQ outlet-number NO-LOCK BY queasy.number2:
    IF (queasy.number2 EQ 1  OR 
        queasy.number2 EQ 2  OR
        queasy.number2 EQ 3  OR
        queasy.number2 EQ 4  OR
        queasy.number2 EQ 18 OR
        queasy.number2 EQ 19) THEN
    DO:
        CREATE setup-list.
        ASSIGN 
            setup-list.setup-number = queasy.number2
            setup-list.setup-param  = queasy.char1
            setup-list.setup-value  = queasy.char2.
    END.
END.

