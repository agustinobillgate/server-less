DEFINE INPUT PARAMETER case-type    AS INTEGER.
DEFINE INPUT PARAMETER int1         AS INTEGER.
DEFINE INPUT PARAMETER char1        AS CHAR.
DEFINE INPUT PARAMETER char2        AS CHAR.
DEFINE OUTPUT PARAMETER success-flag    AS LOGICAL  NO-UNDO INITIAL NO.


CASE case-type :
    WHEN 1 THEN
    DO:
        FIND FIRST telephone WHERE telephone.telephone = char1
            AND telephone.NAME EQ char2
            EXCLUSIVE-LOCK. 
        IF AVAILABLE telephone THEN
        DO:
            DELETE telephone.
            RELEASE telephone.
            ASSIGN success-flag = YES.
        END.                 
    END.
END CASE.


