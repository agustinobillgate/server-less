DEFINE INPUT PARAMETER user-init  AS CHAR NO-UNDO.
DEFINE OUTPUT PARAMETER sales-name AS CHAR NO-UNDO.


FIND FIRST bediener WHERE bediener.userinit = user-init NO-LOCK NO-ERROR.
IF AVAILABLE bediener THEN sales-name = bediener.username.
