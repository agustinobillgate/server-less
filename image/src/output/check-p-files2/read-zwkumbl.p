DEF TEMP-TABLE t-zwkum LIKE zwkum.

DEFINE INPUT  PARAMETER case-type   AS INT.
DEFINE INPUT  PARAMETER int1        AS INT.
DEFINE INPUT  PARAMETER int2        AS INT.
DEFINE INPUT  PARAMETER int3        AS INT.
DEFINE INPUT  PARAMETER char1       AS CHAR.
DEFINE INPUT  PARAMETER char2       AS CHAR.
DEFINE INPUT  PARAMETER log1        AS LOGICAL.
DEFINE INPUT  PARAMETER log2        AS LOGICAL.
DEFINE OUTPUT PARAMETER TABLE FOR t-zwkum.

CASE case-type:
    WHEN 1 THEN
    DO:
        FIND FIRST zwkum WHERE zwkum.zknr = int1
            AND zwkum.departement = int2 NO-LOCK NO-ERROR.
        IF AVAILABLE zwkum THEN RUN assign-it.
    END.
    WHEN 2 THEN
    DO:
        FOR EACH zwkum WHERE zwkum.departement = int1 NO-LOCK:
            RUN assign-it.
        END.
    END.
    WHEN 3 THEN
    DO:
        FIND FIRST zwkum WHERE zwkum.zknr NE int1
            AND zwkum.departement = int2 
            AND zwkum.bezeich = char1 NO-LOCK NO-ERROR.
        IF AVAILABLE zwkum THEN RUN assign-it.
    END.
END CASE.

PROCEDURE assign-it:
    CREATE t-zwkum.
    BUFFER-COPY  zwkum TO t-zwkum.
END.
