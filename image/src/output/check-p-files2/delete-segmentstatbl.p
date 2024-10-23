
DEF INPUT PARAMETER case-type AS INT.
DEF INPUT PARAMETER int1      AS INT.
DEF INPUT PARAMETER int2      AS INT.
DEF INPUT PARAMETER date1     AS DATE.
DEF OUTPUT PARAMETER success-flag AS LOGICAL INIT NO.

CASE case-type:
    WHEN 1 THEN
    DO:
        FIND FIRST segmentstat WHERE segmentstat.segmentcode = int1
            AND segmentstat.datum = date1 EXCLUSIVE-LOCK NO-ERROR.
        IF AVAILABLE segmentstat THEN
        DO:
            delete segmentstat.
            success-flag = YES.
            RELEASE segmentstat.
        END.
        /*
        IF segmentstat.budzimmeranz EQ 0 AND segmentstat.betriebsnr EQ 0 THEN
        DO:
            delete segmentstat.
            success-flag = YES.
        END.
        ELSE
        DO:
          segmentstat.budzimmeranz = 0.
          segmentstat.budpersanz = 0.
          segmentstat.budlogis = 0.
          success-flag = YES.
          FIND CURRENT segmentstat NO-LOCK.
        END.
        */
    END.
END CASE.
