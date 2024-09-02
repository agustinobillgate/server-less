DEF TEMP-TABLE t-telephone LIKE telephone.

DEFINE INPUT PARAMETER case-type AS INTEGER.
DEFINE INPUT PARAMETER int1      AS INTEGER.
DEFINE INPUT PARAMETER TABLE FOR t-telephone.
DEFINE OUTPUT PARAMETER success-flag AS LOGICAL.

FIND FIRST t-telephone NO-ERROR.
IF NOT AVAILABLE t-telephone THEN
    RETURN.

CASE case-type:
    WHEN 1 THEN
    DO:
        FIND FIRST telephone WHERE RECID(telephone) = int1 EXCLUSIVE-LOCK NO-ERROR.
        IF AVAILABLE telephone THEN
        DO:
            BUFFER-COPY t-telephone TO telephone.
            FIND CURRENT telephone NO-LOCK.
            success-flag = YES.
        END.
    END.
    WHEN 2 THEN
    DO:
        CREATE telephone.
        BUFFER-COPY t-telephone TO telephone.
        success-flag = YES.
    END.
END CASE.
