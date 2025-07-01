
DEF INPUT  PARAMETER pvILanguage    AS INTEGER NO-UNDO.
DEF INPUT  PARAMETER nr AS INT.
DEF OUTPUT PARAMETER msg-str AS CHAR.

{SupertransBL.i}
DEF VAR lvCAREA AS CHAR INITIAL "gldepart-admin".

FIND FIRST gl-acct WHERE gl-acct.deptnr = nr NO-LOCK NO-ERROR.
IF AVAILABLE gl-acct THEN
DO: 
    msg-str = msg-str + CHR(2)
            + translateExtended ("Chart-of-account exists, deleting not possible.",lvCAREA,"").
    RETURN NO-APPLY.
END.
ELSE
DO:
    FIND FIRST gl-department WHERE gl-department.nr = nr EXCLUSIVE-LOCK NO-ERROR.
    IF AVAILABLE gl-department THEN delete gl-department.
    RELEASE gl-department.
END.
