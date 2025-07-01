DEF TEMP-TABLE t-counters LIKE counters.

DEFINE INPUT PARAMETER case-type AS INTEGER NO-UNDO.
DEFINE INPUT PARAMETER counterNo AS INTEGER.
DEFINE OUTPUT PARAMETER TABLE FOR t-counters.

CASE case-type:
    WHEN 1 THEN
    DO:
        FIND FIRST counters WHERE counters.counter-no = counterNo 
            NO-LOCK NO-ERROR. 
        IF AVAILABLE counters THEN 
        DO:
            CREATE t-counters.
            BUFFER-COPY counters TO t-counters.
        END.
    END.
    WHEN 2 THEN
    DO:
        FIND FIRST counters WHERE counters.counter-no = counterNo 
            EXCLUSIVE-LOCK. 
        ASSIGN counters.counter = counters.counter + 1.
        FIND CURRENT counters NO-LOCK.
        CREATE t-counters.
        BUFFER-COPY counters TO t-counters.
    END.
END CASE.
