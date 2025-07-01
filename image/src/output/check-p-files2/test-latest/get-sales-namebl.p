DEFINE INPUT PARAMETER nr           AS INTEGER.
DEFINE OUTPUT PARAMETER username    AS CHARACTER.

FIND FIRST bediener WHERE bediener.nr EQ nr NO-LOCK NO-ERROR.
IF AVAILABLE bediener THEN 
DO:
    username    = bediener.username.
END.
