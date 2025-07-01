
DEF INPUT  PARAMETER pvILanguage  AS INTEGER NO-UNDO.
DEF INPUT  PARAMETER nr           AS INT.
DEF OUTPUT PARAMETER msg-str      AS CHAR.
DEF OUTPUT PARAMETER success-flag AS LOGICAL INIT NO.

{SupertransBL.i}
DEF VAR lvCAREA AS CHAR INITIAL "glmain-admin".

FIND FIRST gl-acct WHERE gl-acct.main-nr = nr NO-LOCK NO-ERROR. 
IF AVAILABLE gl-acct  THEN 
DO:
 msg-str = msg-str + CHR(2)
         + translateExtended ("Chart-of-account under this main code exists, deleting not possible.",lvCAREA,"").
END.
ELSE
DO:
    FIND FIRST gl-main WHERE gl-main.nr = nr EXCLUSIVE-LOCK NO-ERROR.
    IF AVAILABLE gl-main THEN
    DO:
        DELETE gl-main.
        RELEASE gl-main.
        ASSIGN success-flag = YES.
    END.
END.
