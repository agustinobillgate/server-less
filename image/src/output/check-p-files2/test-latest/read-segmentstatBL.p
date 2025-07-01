DEF TEMP-TABLE t-segmentstat LIKE segmentstat.

DEF INPUT PARAMETER case-type AS INT.
DEF INPUT PARAMETER int1      AS INT.
DEF INPUT PARAMETER int2      AS INT.
DEF INPUT PARAMETER int3      AS INT.
DEF INPUT PARAMETER int4      AS INT.
DEF INPUT PARAMETER int5      AS INT.
DEF INPUT PARAMETER date1     AS DATE.
DEF INPUT PARAMETER date2     AS DATE.
DEF INPUT PARAMETER deci1     AS DECIMAL.
DEF OUTPUT PARAMETER TABLE FOR t-segmentstat.

CASE case-type:
    WHEN 1 THEN
    DO:
        FOR EACH segmentstat WHERE
            segmentstat.segmentcode = int1
            AND segmentstat.datum GE date1 NO-LOCK BY segmentstat.datum:
            RUN assign-it.
        END.
    END.
END CASE.

PROCEDURE assign-it:
    CREATE t-segmentstat.
    BUFFER-COPY segmentstat TO t-segmentstat.
END.
