DEF TEMP-TABLE t-gl-department LIKE gl-department.

DEF INPUT PARAMETER case-type AS INTEGER.
DEF INPUT PARAMETER int1 AS INT.
DEF INPUT PARAMETER int2 AS CHAR.
DEF INPUT PARAMETER char1 AS CHAR.
DEF OUTPUT PARAMETER TABLE FOR t-gl-department.

CASE case-type:
    WHEN 1 THEN
    DO:
        FIND FIRST gl-department WHERE gl-department.nr = int1 NO-LOCK NO-ERROR.
        IF AVAILABLE gl-department THEN RUN assign-it.
    END.
END CASE.

PROCEDURE assign-it:
    CREATE t-gl-department.
    BUFFER-COPY gl-department TO t-gl-department.
END.

