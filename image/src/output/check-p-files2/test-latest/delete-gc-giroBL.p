

DEF INPUT  PARAMETER case-type   AS INTEGER.
DEF INPUT  PARAMETER int1        AS INTEGER.
DEF OUTPUT PARAMETER successFlag AS LOGICAL INIT NO.

CASE case-type:
    WHEN 1 THEN
    DO:
        FIND FIRST gc-giro WHERE RECID(gc-giro) = int1 EXCLUSIVE-LOCK.
        IF AVAILABLE gc-giro THEN 
        DO:    
            DELETE gc-giro.
            successFlag = YES.
        END.
    END.
END CASE.
