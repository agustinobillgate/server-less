
DEF TEMP-TABLE t-gc-piacct LIKE gc-piacct.

DEF INPUT PARAMETER case-type AS INT.
DEF INPUT PARAMETER int1 AS INT.
DEF OUTPUT PARAMETER TABLE FOR t-gc-piacct.

CASE case-type:
    WHEN 1 THEN
    DO:
        FOR EACH gc-piacct WHERE gc-piacct.activeflag = int1 
            NO-LOCK BY gc-piacct.nr:
            CREATE t-gc-piacct.
            BUFFER-COPY gc-piacct TO t-gc-piacct.
        END.
    END.
END CASE.
