DEFINE TEMP-TABLE del-list 
    FIELD int1  AS INT
    FIELD int2  AS INT
    FIELD date1 AS DATE.

DEF INPUT PARAMETER case-type AS INT.
DEF INPUT PARAMETER TABLE FOR del-list.
DEF OUTPUT PARAMETER success-flag AS LOGICAL INIT NO.

CASE case-type:
    WHEN 1 THEN
    DO:
        FOR EACH del-list NO-LOCK BY del-list.int1:
            FIND FIRST segmentstat WHERE segmentstat.segmentcode = del-list.int1
            AND segmentstat.datum = del-list.date1 EXCLUSIVE-LOCK NO-ERROR.
            IF AVAILABLE segmentstat THEN
            DO:
                delete segmentstat.
                success-flag = YES.
                RELEASE segmentstat.
            END.
        END.
    END.
END CASE.

