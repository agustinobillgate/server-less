


DEF INPUT  PARAMETER case-type  AS INTEGER NO-UNDO.
DEF INPUT  PARAMETER int1       AS INTEGER NO-UNDO.
DEF INPUT  PARAMETER char1      AS CHAR    NO-UNDO.
DEF OUTPUT PARAMETER success-flag AS LOGICAL INIT NO.

CASE case-type:
    WHEN 1 THEN
    DO:
        FIND FIRST nation WHERE nation.nationnr = int1
            AND nation.kurzbez EQ char1 EXCLUSIVE-LOCK NO-ERROR.
        IF AVAILABLE nation THEN
        DO:
            DELETE nation.
            RELEASE nation.
            success-flag = YES.
        END.
    END.
    WHEN 2 THEN
    DO:
        FIND FIRST nation WHERE RECID(nation) = int1 EXCLUSIVE-LOCK NO-ERROR.
        IF AVAILABLE nation THEN
        DO:
            DELETE nation.
            RELEASE nation.
            success-flag = YES.
        END.
    END.
END CASE.
