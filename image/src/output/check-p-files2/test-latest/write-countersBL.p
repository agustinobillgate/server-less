DEF TEMP-TABLE t-counters LIKE counters.

DEFINE INPUT PARAMETER case-type AS INTEGER NO-UNDO.
DEFINE INPUT PARAMETER counter-no AS INTEGER.
DEFINE INPUT PARAMETER TABLE FOR t-counters.
DEFINE OUTPUT PARAMETER success-flag AS LOGICAL INIT NO.

FIND FIRST t-counters NO-ERROR.
IF NOT AVAILABLE t-counters THEN RETURN.

CASE case-type:
    WHEN 1 THEN
    DO:
        FIND FIRST counters WHERE counters.counter-no = counter-no 
            EXCLUSIVE-LOCK NO-ERROR. 
        IF NOT AVAILABLE counters THEN 
        DO:
            CREATE counters.
            BUFFER-COPY t-counters TO counters.
            /*FIND CURRENT counters NO-LOCK. */
            success-flag = YES.
        END.
        ASSIGN counters.counter = counters.counter + 1.
        FIND CURRENT counters NO-LOCK.
        success-flag = YES.
    END.
END CASE.


