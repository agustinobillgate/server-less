
DEF INPUT  PARAMETER subtask AS CHAR.
DEF OUTPUT PARAMETER fl-code AS INT INIT 0.

FIND FIRST eg-subtask WHERE eg-subtask.sub-code = subtask /*AND
    eg-subtask.reserve-int = "" */ NO-LOCK NO-ERROR.
IF AVAILABLE eg-subtask THEN
    fl-code = 1.
