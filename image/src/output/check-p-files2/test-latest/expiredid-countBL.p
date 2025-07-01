DEFINE INPUT  PARAMETER AswaitTime  AS INTEGER NO-UNDO.
DEFINE OUTPUT PARAMETER expired-id  AS INTEGER NO-UNDO.
DEFINE OUTPUT PARAMETER user-name   AS LOGICAL NO-UNDO.

DEFINE VARIABLE server-time AS INTEGER NO-UNDO.
DEFINE VARIABLE server-date AS DATE    NO-UNDO.


FIND FIRST bediener WHERE bediener.username = "Wi-Guest" NO-LOCK NO-ERROR.
IF AVAILABLE bediener THEN DO:
    ASSIGN
        expired-id = 0
        user-name  = YES
    .
    FOR EACH res-line WHERE (res-line.resstatus = 6 OR res-line.resstatus = 13)
        AND res-line.cancelled-id = bediener.userinit
        AND res-line.betrieb-gast = 0 NO-LOCK,
      FIRST reservation WHERE reservation.resnr = res-line.resnr 
        AND reservation.depositbez = 0 NO-LOCK:
        
        ASSIGN 
            server-time = TIME - res-line.ankzeit
            server-date = TODAY
        .
        IF (server-time GT AswaitTime OR res-line.ankunft NE server-date) THEN
            expired-id = expired-id + 1.
    END.
END.
