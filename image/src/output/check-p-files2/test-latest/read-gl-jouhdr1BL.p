DEF TEMP-TABLE t-gl-jouhdr LIKE gl-jouhdr.

DEF INPUT PARAMETER case-type AS INTEGER.
DEF INPUT PARAMETER int1 AS INTEGER.
DEF INPUT PARAMETER int2 AS INTEGER.
DEF INPUT PARAMETER char1 AS CHAR.
DEF INPUT PARAMETER date1 AS DATE.
DEF INPUT PARAMETER date2 AS DATE.
DEF OUTPUT PARAMETER TABLE FOR t-gl-jouhdr.

CASE case-type:
    WHEN 1 THEN
    DO:
        FIND FIRST gl-jouhdr WHERE gl-jouhdr.activeflag = int1
            AND gl-jouhdr.datum  LE  date2
            AND gl-jouhdr.datum  GE date1 NO-LOCK NO-ERROR.
        IF AVAILABLE gl-jouhdr THEN
        DO:
            CREATE t-gl-jouhdr.
            BUFFER-COPY gl-jouhdr TO t-gl-jouhdr.
        END.
    END.
    WHEN 2 THEN
    DO:
        FIND FIRST gl-jouhdr WHERE gl-jouhdr.datum GE date1 
            AND gl-jouhdr.datum LE date2 
            AND gl-jouhdr.activeflag = int1 NO-LOCK NO-ERROR.
        IF AVAILABLE gl-jouhdr THEN
        DO:
            CREATE t-gl-jouhdr.
            BUFFER-COPY gl-jouhdr TO t-gl-jouhdr.
        END.
    END.
END CASE.
