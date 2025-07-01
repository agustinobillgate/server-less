DEF TEMP-TABLE t-nation       LIKE nation.

DEF INPUT  PARAMETER case-type  AS INTEGER NO-UNDO.
DEF INPUT  PARAMETER int1       AS INTEGER NO-UNDO.
DEF INPUT  PARAMETER int2       AS INTEGER NO-UNDO.
DEF INPUT  PARAMETER int3       AS INTEGER NO-UNDO.
DEF INPUT  PARAMETER char1      AS CHAR    NO-UNDO.
DEF INPUT  PARAMETER char2      AS CHAR    NO-UNDO.
DEF INPUT  PARAMETER logic1     AS LOGICAL NO-UNDO.
DEF OUTPUT PARAMETER TABLE FOR t-nation.

CASE case-type:
    WHEN 1 THEN
    DO:
        FIND FIRST nation WHERE nation.untergruppe = int1 
            AND nation.natcode = int2 NO-LOCK NO-ERROR.
        IF AVAILABLE nation THEN
        DO:
            CREATE t-nation.
            BUFFER-COPY nation TO t-nation.
        END.
    END.
    WHEN 2 THEN
    DO:
        FOR EACH nation WHERE nation.natcode = int1 NO-LOCK :
            CREATE t-nation.
            BUFFER-COPY nation TO t-nation.
        END.
    END.
    WHEN 3 THEN
    DO:
        FIND FIRST nation WHERE nation.kurzbez = char1
          AND nation.natcode = int1 NO-LOCK NO-ERROR. 
        IF AVAILABLE nation THEN
        DO:
            CREATE t-nation.
            BUFFER-COPY nation TO t-nation.
        END.
    END.
END CASE.
