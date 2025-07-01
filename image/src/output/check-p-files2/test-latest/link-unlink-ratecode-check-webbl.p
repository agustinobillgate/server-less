DEFINE INPUT PARAMETER case-type        AS INTEGER.
DEFINE INPUT PARAMETER inp-tb1char1     AS CHARACTER.
DEFINE INPUT PARAMETER adjust-combo     AS CHARACTER.
DEFINE INPUT PARAMETER adjust-value     AS DECIMAL.
DEFINE INPUT-OUTPUT PARAMETER inp-char3 AS CHARACTER.

CASE case-type:
    WHEN 1 THEN /*Link*/
    DO:
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
