DEFINE INPUT PARAMETER case-type        AS INTEGER.
DEFINE INPUT PARAMETER inp-tb1char1     AS CHARACTER.
DEFINE INPUT PARAMETER adjust-combo     AS CHARACTER.
DEFINE INPUT PARAMETER adjust-value     AS DECIMAL.
DEFINE INPUT PARAMETER rate-code        AS CHARACTER.
DEFINE INPUT-OUTPUT PARAMETER inp-char3 AS CHARACTER.
DEFINE OUTPUT PARAMETER result-message  AS CHARACTER.

DEFINE VARIABLE found-child AS LOGICAL NO-UNDO.
DEFINE VARIABLE child-code AS CHARACTER NO-UNDO.

CASE case-type:
    WHEN 1 THEN /*Link*/
    DO:
        /*FDL Oct 11, 2024: Ticket EA982C - Check rate code is already be parent or not*/
        FOR EACH queasy WHERE queasy.KEY EQ 2
            AND NUM-ENTRIES(queasy.char3, ";") GT 2
            AND ENTRY(2, queasy.char3, ";") EQ rate-code NO-LOCK:
            
            child-code = queasy.char1.
            found-child = YES.
            LEAVE.            
        END.
        IF found-child THEN
        DO:
            result-message = "Ratecode has become the parent of child: " + child-code
                            + CHR(10) + "Link ratecode not possible.".
            RETURN.
        END.

        IF inp-char3 = "" THEN inp-char3 = ";" + inp-tb1char1 + ";".
        ELSE
        DO:             
            IF SUBSTR(inp-char3, LENGTH(inp-char3)) NE ";" THEN
                inp-char3 = inp-char3 + ";".
            inp-char3 = inp-char3 + inp-tb1char1 + ";".
        END.
        
        IF adjust-combo = "Using Percentage(%)" THEN 
          inp-char3 = inp-char3 + "%" + STRING(adjust-value * 100) + ";".
        ELSE
          inp-char3 = inp-char3 + "A" + STRING(adjust-value * 100) + ";".
    END.
    WHEN 2 THEN /*Unlink*/
    DO:
        inp-char3 = ENTRY(1, inp-char3, ";") + ";" + ENTRY(2, inp-char3, ";") + ";".
        IF adjust-combo = "Using Percentage(%)" THEN 
          inp-char3 = inp-char3 + "%" + STRING(adjust-value * 100) + ";".
        ELSE
          inp-char3 = inp-char3 + "A" + STRING(adjust-value * 100) + ";".
    END.
END CASE.
