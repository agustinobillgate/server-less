DEFINE TEMP-TABLE staff LIKE eg-staff.

DEF INPUT PARAMETER TABLE FOR staff.
DEF INPUT PARAMETER case-type AS INT.
DEF INPUT PARAMETER rec-id AS INT.
DEF OUTPUT PARAMETER fl-code AS INT INIT 0.

DEFINE BUFFER queri FOR eg-staff. 

FIND FIRST staff.
IF case-type = 1 THEN
DO :
    CREATE eg-staff.
    BUFFER-COPY staff TO eg-staff.
END.
ELSE IF case-type = 2 THEN
DO:
    FIND FIRST eg-staff WHERE RECID(eg-staff) = rec-id.
    FIND FIRST queri WHERE queri.Nr = staff.Nr AND rowid(queri) NE rowid(eg-staff) NO-LOCK NO-ERROR.
    IF AVAILABLE queri THEN
    DO:
        fl-code = 1.
        RETURN NO-APPLY.
    END.
    ELSE
    DO:
        FIND FIRST queri WHERE queri.NAME = staff.NAME AND rowid(queri) NE rowid(eg-staff) NO-LOCK NO-ERROR.
        IF AVAILABLE queri THEN
        DO:
            fl-code = 2.
            RETURN NO-APPLY.
        END.
        ELSE
        DO:
            FIND CURRENT eg-staff EXCLUSIVE-LOCK NO-ERROR.
            BUFFER-COPY staff TO eg-staff.
            FIND CURRENT eg-staff NO-LOCK.
            fl-code = 3.
        END.
    END.
END.
