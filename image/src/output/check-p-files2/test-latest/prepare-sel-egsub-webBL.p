
DEFINE TEMP-TABLE duration
    FIELD dur-nr AS INTEGER
    FIELD dur-str AS CHAR FORMAT "x(100)".

DEF TEMP-TABLE q-list
    FIELD sub-code  AS CHAR
    FIELD bezeich   AS CHAR
    FIELD dur-str   AS CHAR
    FIELD dur-nr    AS INT
    FIELD days      AS CHAR
    FIELD hours     AS CHAR
    FIELD minutes   AS CHAR.

DEF INPUT  PARAMETER main-nr AS INT.
DEF INPUT  PARAMETER dept-nr AS INT.
DEF OUTPUT PARAMETER TABLE FOR q-list.

/*DEF VAR main-nr AS INT INIT 1.
DEF VAR dept-nr AS INT INIT 8.*/


IF main-nr = 0 AND dept-nr NE 0 THEN
    FOR EACH eg-subtask WHERE eg-subtask.dept-nr = dept-nr
        NO-LOCK BY eg-subtask.sub-code:
        RUN create-list.
    END.
ELSE IF main-nr = 0 AND dept-nr = 0 THEN
    FOR EACH eg-subtask NO-LOCK BY eg-subtask.sub-code:
        RUN create-list.
    END.
ELSE
    FOR EACH eg-subtask WHERE eg-subtask.dept-nr = dept-nr
        AND eg-subtask.main-nr = main-nr NO-LOCK BY eg-subtask.sub-code:
        RUN create-list.
    END.

PROCEDURE create-list:
    CREATE q-list.
    ASSIGN
        q-list.sub-code = eg-subtask.sub-code
        q-list.bezeich  = eg-subtask.bezeich
        q-list.dur-nr   = eg-subtask.dur-nr.
    IF eg-subtask.dur-nr NE 0 THEN
    DO:
        FIND FIRST eg-duration 
            WHERE eg-duration.duration-nr = eg-subtask.dur-nr NO-LOCK NO-ERROR.
        IF AVAILABLE eg-duration THEN
        DO:
            ASSIGN
                q-list.days = STRING(eg-duration.DAY)
                q-list.hour = STRING(eg-duration.hour)
                q-list.minutes = STRING(eg-duration.minute).
        END.                                         
    END.
    ELSE IF eg-subtask.reserve-char NE "" THEN
    DO:
        ASSIGN
        q-list.days     = ENTRY(1, eg-subtask.reserve-char, ";")
        q-list.hour     = ENTRY(2, eg-subtask.reserve-char, ";")
        q-list.minutes  = ENTRY(3, eg-subtask.reserve-char, ";").
    END.
END.


