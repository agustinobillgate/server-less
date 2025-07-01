DEF TEMP-TABLE t-gl-fstype LIKE gl-fstype.

DEF INPUT PARAMETER case-type AS INTEGER.
DEF INPUT PARAMETER int1 AS INT.
DEF INPUT PARAMETER char1 AS CHAR.
DEF INPUT PARAMETER char2 AS CHAR.
DEF OUTPUT PARAMETER TABLE FOR t-gl-fstype.

CASE case-type:
    WHEN 1 THEN
    DO:
        FIND FIRST gl-fstype WHERE gl-fstype.nr = int1 NO-LOCK NO-ERROR.
        IF AVAILABLE gl-fstype THEN RUN assign-it.
    END.
    WHEN 2 THEN
    DO:
        FOR EACH gl-fstype NO-LOCK BY gl-fstype.nr:
            RUN assign-it.
        END.
    END.
END CASE.

PROCEDURE assign-it:
    CREATE t-gl-fstype.
    BUFFER-COPY gl-fstype TO t-gl-fstype.
END.
