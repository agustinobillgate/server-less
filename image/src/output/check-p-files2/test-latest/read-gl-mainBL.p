DEF TEMP-TABLE t-gl-main LIKE gl-main.

DEF INPUT PARAMETER case-type AS INTEGER.
DEF INPUT PARAMETER int1 AS INTEGER.
DEF INPUT PARAMETER int2 AS INTEGER.
DEF INPUT PARAMETER char1 AS CHAR.
DEF INPUT PARAMETER char2 AS CHAR.
DEF OUTPUT PARAMETER TABLE FOR t-gl-main.

CASE case-type:
    WHEN 1 THEN
    DO:
        FIND FIRST gl-main NO-LOCK NO-ERROR.
        IF AVAILABLE gl-main THEN
        DO:
            CREATE t-gl-main.
            BUFFER-COPY gl-main TO t-gl-main.
        END.
    END.
    WHEN 2 THEN
    DO:
        FIND FIRST gl-main WHERE gl-main.code = int1 NO-LOCK NO-ERROR. 
        IF AVAILABLE gl-main THEN
        DO:
            CREATE t-gl-main.
            BUFFER-COPY gl-main TO t-gl-main.
        END.
    END.
    WHEN 3 THEN
    DO:
        FIND FIRST gl-main WHERE gl-main.nr = int1 NO-LOCK NO-ERROR. 
        IF AVAILABLE gl-main THEN
        DO:
            CREATE t-gl-main.
            BUFFER-COPY gl-main TO t-gl-main.
        END.
    END.
    WHEN 4 THEN
    DO:
        FOR EACH gl-main NO-LOCK:
            CREATE t-gl-main.
            BUFFER-COPY gl-main TO t-gl-main.
        END.
    END.
    WHEN 5 THEN
    DO:
        FIND FIRST gl-main WHERE gl-main.bezeich = char1
            AND gl-main.nr NE int1 NO-LOCK NO-ERROR.
        IF AVAILABLE gl-main THEN
        DO:
            CREATE t-gl-main.
            BUFFER-COPY gl-main TO t-gl-main.
        END.
    END.
    WHEN 6 THEN
    DO:
        FIND FIRST gl-main WHERE gl-main.code = int1
            AND gl-main.nr NE int2 NO-LOCK NO-ERROR. 
        IF AVAILABLE gl-main THEN
        DO:
            CREATE t-gl-main.
            BUFFER-COPY gl-main TO t-gl-main.
        END.
    END.
END CASE.
