
DEF INPUT PARAMETER deptnr    AS INT.
DEF INPUT PARAMETER mainnr    AS INT.
DEF INPUT PARAMETER subtask   AS CHAR.
DEF INPUT PARAMETER user-init AS CHAR.
DEF INPUT PARAMETER bezeich   AS CHAR.
DEF INPUT PARAMETER days      AS CHAR.
DEF INPUT PARAMETER hours     AS CHAR.
DEF INPUT PARAMETER minutes   AS CHAR.
DEF OUTPUT PARAMETER fl-code  AS INT INIT 0.

FIND FIRST eg-subtask WHERE eg-subtask.main-nr = mainnr AND eg-subtask.bezeich = bezeich NO-LOCK NO-ERROR.
IF AVAILABLE eg-subtask THEN
DO:
    fl-code = 1.
    RETURN NO-APPLY.
END.
ELSE
DO:
    CREATE eg-subtask.
    ASSIGN
        eg-subtask.dept-nr      = deptnr
        eg-subtask.main-nr      = mainnr
        eg-subtask.reserve-char = days + ";" + hours + ";" + minutes
        eg-subtask.sub-code     = subtask
        eg-subtask.bezeich      = bezeich
        eg-subtask.create-DATE  = TODAY
        eg-subtask.create-TIME  = TIME
        eg-subtask.create-by    = user-init
        eg-subtask.sourceForm   = "1" .
END.
