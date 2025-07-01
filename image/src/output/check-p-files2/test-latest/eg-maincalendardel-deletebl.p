
DEF INPUT PARAMETER smaintain-maintainnr AS INT.
DEF OUTPUT PARAMETER msgInt AS INT INIT 0.

DEFINE BUFFER buf-maintain FOR eg-maintain.

FIND FIRST buf-maintain WHERE buf-maintain.maintainnr = smaintain-maintainnr 
    AND buf-maintain.delete-flag = YES EXCLUSIVE-LOCK NO-ERROR.
IF AVAILABLE buf-maintain THEN
DO:
    DELETE buf-maintain.
    RELEASE buf-maintain.
    ASSIGN msgInt = 1.
END.
