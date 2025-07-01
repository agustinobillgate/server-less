
DEF BUFFER sub FOR eg-subtask.

DEF INPUT PARAMETER curr-select AS CHAR.
DEF INPUT PARAMETER subtask-sub-code AS CHAR.
DEF output PARAMETER avail-sub AS LOGICAL INIT NO.

IF curr-select = "chg" THEN
    FIND FIRST sub WHERE sub.sub-code = subtask-sub-code AND 
    ROWID(sub) NE ROWID(eg-subtask) NO-LOCK NO-ERROR.
ELSE IF curr-select = "add" THEN
    FIND FIRST sub WHERE sub.sub-code = subtask-sub-code
    /*AND sub.reserve-int = "" */ NO-LOCK NO-ERROR.
IF AVAILABLE sub THEN avail-sub = YES.
