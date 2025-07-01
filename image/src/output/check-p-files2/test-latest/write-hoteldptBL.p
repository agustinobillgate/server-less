DEF TEMP-TABLE t-hoteldpt LIKE hoteldpt.

DEF INPUT PARAMETER case-type AS INT.
DEF INPUT PARAMETER TABLE FOR t-hoteldpt.
DEF OUTPUT PARAMETER success-flag AS LOGICAL INIT NO.

FIND FIRST t-hoteldpt NO-ERROR.
IF NOT AVAILABLE t-hoteldpt THEN RETURN.

CASE case-type:
    WHEN 1 THEN
    DO:
        CREATE hoteldpt.
        BUFFER-COPY t-hoteldpt TO hoteldpt.
        RELEASE hoteldpt.
        ASSIGN success-flag = YES.
    END.
    WHEN 2 THEN
    DO:
        FIND FIRST hoteldpt WHERE hoteldpt.num = t-hoteldpt.num 
            EXCLUSIVE-LOCK NO-ERROR.
        IF AVAILABLE hoteldpt THEN
        DO:
            BUFFER-COPY t-hoteldpt TO hoteldpt.
            RELEASE hoteldpt.
            ASSIGN success-flag = YES.
        END.
    END.
END CASE.
