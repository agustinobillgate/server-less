DEFINE OUTPUT PARAMETER strKtext AS CHARACTER.

strKtext = "".
DEFINE VARIABLE i AS INTEGER.
DO i = 1 TO 12:
    FIND FIRST queasy WHERE queasy.KEY = 148 AND queasy.char3 NE "" 
    AND queasy.number1 EQ i NO-LOCK NO-ERROR.
    IF AVAILABLE queasy THEN 
        strKtext = strKtext + "[" + STRING(i) + "] " + queasy.char3 + CHR(2).
    ELSE DO:
        IF i = 1 THEN strKtext = strKtext + "[1] Banquet Instructions" + CHR(2). 
        IF i = 2 THEN strKtext = strKtext + "[2] F/O Instructions" + CHR(2). 
        IF i = 3 THEN strKtext = strKtext + "[3] Kitchen Instructions" + CHR(2). 
        IF i = 4 THEN strKtext = strKtext + "[4] House-Keeping Instructions" + CHR(2).        
        IF i = 5 THEN strKtext = strKtext + "[5] Steward Instructions" + CHR(2). 
        IF i = 6 THEN strKtext = strKtext + "[6] Engineering Instructions" + CHR(2). 
        IF i = 7 THEN strKtext = strKtext + "[7] Restaurant Instructions" + CHR(2).   
        IF i = 8 THEN strKtext = strKtext + "[8] Security Instructions" + CHR(2).    
        IF i = 9 THEN strKtext = strKtext + "[9] Bar Instructions" + CHR(2).           
        IF i = 10 THEN strKtext = strKtext + "[10] MCM Instructions" + CHR(2).          
        IF i = 11 THEN strKtext = strKtext + "[11] Sales & Marketing" + CHR(2). 
        IF i = 12 THEN strKtext = strKtext + "[12] Order Taken By" + CHR(2). 
    END.
END.
