DEF TEMP-TABLE t-akthdr LIKE akthdr.

DEFINE INPUT PARAMETER case-type AS INTEGER NO-UNDO.
DEFINE INPUT PARAMETER TABLE FOR t-akthdr.
DEFINE OUTPUT PARAMETER success-flag AS LOGICAL INIT NO.

FIND FIRST t-akthdr NO-ERROR.
IF NOT AVAILABLE t-akthdr THEN
    RETURN NO-APPLY.

CASE case-type:
    WHEN 1 THEN
    DO: 
        CREATE akthdr.
        BUFFER-COPY t-akthdr TO akthdr.
        success-flag = YES.
        FIND CURRENT akthdr NO-LOCK.
    END.
    WHEN 2 THEN
    DO: 
        FIND FIRST akthdr WHERE akthdr.aktnr = t-akthdr.aktnr EXCLUSIVE-LOCK.
        IF AVAILABLE akthdr THEN
        DO: 
            BUFFER-COPY t-akthdr TO akthdr.
            success-flag = YES.
        END.
        FIND CURRENT akthdr NO-LOCK.
    END.
END CASE.



