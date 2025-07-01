
DEF INPUT PARAMETER smaintain-maintainnr AS INT.
DEF OUTPUT PARAMETER flag AS INT INIT 0.

FIND FIRST eg-maintain WHERE eg-maintain.maintainnr = smaintain-maintainnr NO-ERROR.
IF AVAILABLE eg-maintain THEN
DO:
    ASSIGN 
        eg-maintain.delete-flag = NO
        eg-maintain.cancel-date = ?
        flag = 1.
END.
