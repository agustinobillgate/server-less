DEFINE TEMP-TABLE output-list LIKE queasy.

DEFINE INPUT PARAMETER department AS INT.
DEFINE INPUT PARAMETER queasy-number AS INT.

DEFINE OUTPUT PARAMETER mess-result AS CHAR.
DEFINE OUTPUT PARAMETER TABLE FOR output-list.

FIND FIRST queasy WHERE queasy.KEY EQ 222 
    AND queasy.number1 EQ 1 
    AND queasy.betriebsnr EQ department 
    AND queasy.number2 EQ queasy-number NO-LOCK NO-ERROR.
IF AVAILABLE queasy THEN
DO:
    mess-result = "0-Queasy Found!".
    CREATE output-list.
    BUFFER-COPY queasy TO output-list.
END.
ELSE
DO :
    mess-result = "0-Queasy Not Found!".
END.
