DEF TEMP-TABLE t-wgrpdep LIKE wgrpdep.

DEFINE INPUT  PARAMETER case-type     AS INTEGER NO-UNDO.
DEFINE INPUT  PARAMETER TABLE         FOR t-wgrpdep.
DEFINE OUTPUT PARAMETER success-flag  AS LOGICAL NO-UNDO INIT NO.

DEFINE VARIABLE curr-counter          AS INTEGER NO-UNDO INIT 1.

FIND FIRST t-wgrpdep NO-ERROR.
IF NOT AVAILABLE t-wgrpdep THEN RETURN.

CASE case-type :
    WHEN 1 THEN
    DO:
        IF t-wgrpdep.zknr = 0 THEN
        DO:
            FOR EACH wgrpdep WHERE 
                wgrpdep.departement = t-wgrpdep.departement 
                NO-LOCK BY wgrpdep.zknr DESC:
                curr-counter = wgrpdep.zknr + 1.
                LEAVE.
            END.
            ASSIGN t-wgrpdep.zknr = curr-counter.
        END.
        CREATE wgrpdep.
        BUFFER-COPY t-wgrpdep TO wgrpdep.
        RELEASE wgrpdep.
        success-flag = YES.
    END.
    WHEN 2 THEN
    DO:
        FIND FIRST wgrpdep WHERE wgrpdep.zknr = t-wgrpdep.zknr 
            AND wgrpdep.departement = t-wgrpdep.departement 
            EXCLUSIVE-LOCK NO-ERROR.
        IF AVAILABLE wgrpdep THEN
        DO:
            BUFFER-COPY t-wgrpdep TO wgrpdep.
            FIND CURRENT wgrpdep NO-LOCK.
            RELEASE wgrpdep.
            success-flag = YES.
        END.
    END.
    WHEN 3 THEN
    DO:
        FIND FIRST wgrpdep WHERE wgrpdep.zknr = t-wgrpdep.zknr 
            AND wgrpdep.departement = t-wgrpdep.departement 
            EXCLUSIVE-LOCK NO-ERROR.
        IF AVAILABLE wgrpdep THEN
        DO:
            DELETE wgrpdep.
            RELEASE wgrpdep.
            success-flag = YES.
        END.
    END.

END CASE.
