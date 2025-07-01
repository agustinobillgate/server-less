DEFINE TEMP-TABLE maingrp-list LIKE queasy.

DEFINE INPUT PARAMETER case-type AS INTEGER.
DEFINE INPUT PARAMETER TABLE FOR maingrp-list.
DEFINE OUTPUT PARAMETER success-flag AS LOGICAL INITIAL NO.

FIND FIRST maingrp-list NO-ERROR.
IF NOT AVAILABLE maingrp-list THEN RETURN.

CASE case-type:
    WHEN 1 THEN
    DO:
        CREATE queasy.
        BUFFER-COPY maingrp-list TO queasy.
        RELEASE queasy.
        success-flag = YES.
    END.
    WHEN 2 THEN
    DO:
        FIND FIRST queasy WHERE queasy.KEY EQ 228 
            AND queasy.number1 EQ maingrp-list.number1 NO-LOCK NO-ERROR.
        IF AVAILABLE queasy THEN
        DO:
            FIND CURRENT queasy EXCLUSIVE-LOCK.
            queasy.char1 = maingrp-list.char1.
            queasy.char2 = maingrp-list.char2.
            queasy.number2 = maingrp-list.number2.
            FIND CURRENT queasy NO-LOCK.
            RELEASE queasy.
            success-flag = YES.
        END.
    END.
END CASE.
