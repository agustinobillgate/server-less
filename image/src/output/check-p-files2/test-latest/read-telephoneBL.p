DEF TEMP-TABLE t-telephone LIKE telephone.

DEF INPUT  PARAMETER case-type  AS INTEGER      NO-UNDO.
DEF INPUT  PARAMETER int1       AS INTEGER      NO-UNDO.
DEF INPUT  PARAMETER int2       AS INTEGER      NO-UNDO.
DEF INPUT  PARAMETER char1      AS CHARACTER    NO-UNDO.
DEF INPUT  PARAMETER char2      AS CHARACTER    NO-UNDO.
DEF INPUT  PARAMETER char3      AS CHARACTER    NO-UNDO.
DEF INPUT  PARAMETER char4      AS CHARACTER    NO-UNDO.
DEF OUTPUT PARAMETER TABLE FOR t-telephone.

CASE case-type:
    WHEN 1 THEN
    DO:
        FIND FIRST telephone WHERE RECID(telephone) = int1 NO-LOCK NO-ERROR.
        IF AVAILABLE telephone THEN
        DO:
            CREATE t-telephone.
            BUFFER-COPY telephone TO t-telephone.
        END.
    END.

    WHEN 99 THEN
    DO:
        FIND FIRST telephone WHERE RECID(telephone) = int1 EXCLUSIVE-LOCK.
        IF AVAILABLE telephone THEN
        DO:
            CREATE t-telephone.
            BUFFER-COPY telephone TO t-telephone.
        END.
    END.
END CASE.
