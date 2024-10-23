
DEFINE TEMP-TABLE t-res-line
    FIELD resnr     LIKE res-line.resnr
    FIELD reslinnr  LIKE res-line.reslinnr
    FIELD name      LIKE res-line.name.

DEF INPUT PARAMETER resnr    AS INTEGER.
DEF INPUT PARAMETER reslinnr AS INTEGER.
DEF OUTPUT PARAMETER TABLE FOR t-res-line.

IF reslinnr NE ? THEN
DO:
    FIND FIRST res-line WHERE res-line.resnr = resnr 
        AND res-line.reslinnr = reslinnr NO-LOCK NO-ERROR.
    IF AVAILABLE res-line THEN
    DO :
        CREATE t-res-line.
        ASSIGN
            t-res-line.resnr = res-line.resnr
            t-res-line.reslinnr = res-line.reslinnr
            t-res-line.name = res-line.name.
    END.
END.
ELSE
DO:
    FIND FIRST res-line WHERE RECID(res-line) = resnr NO-LOCK NO-ERROR.
    IF AVAILABLE res-line THEN
    DO :
        CREATE t-res-line.
        ASSIGN
            t-res-line.resnr = res-line.resnr
            t-res-line.reslinnr = res-line.reslinnr
            t-res-line.name = res-line.name.
    END.
END.
