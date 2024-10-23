DEFINE INPUT PARAMETER case-type    AS INTEGER.
DEFINE INPUT PARAMETER int1         AS INTEGER.
DEFINE OUTPUT PARAMETER success-flag    AS LOGICAL  NO-UNDO INITIAL NO.


CASE case-type :
    WHEN 1 THEN
    DO:
        FIND FIRST master WHERE master.resnr = int1 EXCLUSIVE-LOCK. 
        IF AVAILABLE master THEN
        DO:
            DELETE master.
            RELEASE master.
        END.                 
    END.
    WHEN 2 THEN
    DO:
        FIND FIRST master WHERE master.resnr = int1 EXCLUSIVE-LOCK. 
        IF AVAILABLE master THEN
        DO:
            DELETE master.
            RELEASE master.
        END.                 
        FOR EACH mast-art WHERE mast-art.resnr = int1 EXCLUSIVE-LOCK: 
            DELETE mast-art.
            RELEASE mast-art.
        END.                 
    END.
END CASE.

