DEFINE INPUT PARAMETER tb1-char3 AS CHARACTER.
DEFINE OUTPUT PARAMETER adjust-combo AS CHARACTER.
DEFINE OUTPUT PARAMETER adjust-value AS DECIMAL FORMAT "->,>>>,>>9.99".

IF SUBSTR(ENTRY(3, tb1-char3, ";"),1,1) = "%" THEN
DO:
    adjust-combo = "Using Percentage(%)".
    adjust-value = DECIMAL(SUBSTR(ENTRY(3, tb1-char3, ";"),2)) / 100.
END.
ELSE
DO:
    adjust-combo = "Using Amount".
    adjust-value = DECIMAL(SUBSTR(ENTRY(3, tb1-char3, ";"),2)) / 100.
END.
