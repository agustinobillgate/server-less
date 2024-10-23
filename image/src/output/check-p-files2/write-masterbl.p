DEF TEMP-TABLE t-master LIKE master.

DEF INPUT  PARAMETER TABLE FOR t-master.
DEF OUTPUT PARAMETER success-flag AS LOGICAL INITIAL NO NO-UNDO.

FIND FIRST t-master NO-ERROR.

FIND FIRST master WHERE master.resnr = t-master.resnr EXCLUSIVE-LOCK NO-ERROR.
IF NOT AVAILABLE master THEN CREATE master.
DO:
    BUFFER-COPY t-master TO master.
    RELEASE master.
    ASSIGN success-flag = YES.
END.
