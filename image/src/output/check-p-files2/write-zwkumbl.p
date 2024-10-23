DEF TEMP-TABLE t-zwkum LIKE zwkum.

DEFINE INPUT  PARAMETER case-type   AS INT.
DEFINE INPUT  PARAMETER TABLE FOR t-zwkum.
DEFINE OUTPUT PARAMETER success-flag    AS LOGICAL INITIAL NO.


FIND FIRST t-zwkum NO-LOCK NO-ERROR.
IF NOT AVAILABLE t-zwkum THEN RETURN.

CASE case-type :
    WHEN 1 THEN
    DO:
        CREATE zwkum.
        BUFFER-COPY t-zwkum TO zwkum.
        RELEASE zwkum.
        success-flag = YES.
    END.
    WHEN 2 THEN
    DO:
        FIND FIRST zwkum WHERE zwkum.zknr = t-zwkum.zknr 
            AND zwkum.departement = t-zwkum.departement EXCLUSIVE-LOCK NO-ERROR.
        IF AVAILABLE zwkum THEN
        DO:
            BUFFER-COPY t-zwkum TO zwkum.
            RELEASE zwkum.
            success-flag = YES.
        END.
    END.
    WHEN 3 THEN
    DO:
        FIND FIRST zwkum WHERE zwkum.zknr = t-zwkum.zknr 
            AND zwkum.departement = t-zwkum.departement EXCLUSIVE-LOCK NO-ERROR.
        IF AVAILABLE zwkum THEN
        DO:
            DELETE zwkum.
            RELEASE zwkum.
            success-flag = YES.
        END.
    END.

END CASE.
