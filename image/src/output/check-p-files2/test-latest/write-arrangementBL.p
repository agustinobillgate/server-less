
DEF TEMP-TABLE t-arrangement LIKE arrangement.

DEF INPUT PARAMETER case-type   AS INT.
DEF INPUT PARAMETER char1       AS CHAR.
DEF INPUT PARAMETER TABLE FOR t-arrangement.
DEF OUTPUT PARAMETER success-flag AS LOGICAL INIT NO.

FIND FIRST t-arrangement NO-ERROR.
IF NOT AVAILABLE t-arrangement THEN RETURN.

CASE case-type:
    WHEN 1 THEN
    DO:
        CREATE arrangement.
        BUFFER-COPY t-arrangement TO arrangement.
        IF char1 NE "" THEN
        DO:
            FIND FIRST waehrung WHERE waehrung.bezeich EQ char1 NO-LOCK.
            ASSIGN arrangement.betriebsnr = waehrung.waehrungsnr.
        END.
        RELEASE arrangement.
        ASSIGN success-flag = YES.
    END.
    WHEN 2 THEN
    DO:
        FIND FIRST arrangement WHERE arrangement.argtnr = t-arrangement.argtnr
            AND arrangement.arrangement = t-arrangement.arrangement
            EXCLUSIVE-LOCK NO-ERROR.
        IF AVAILABLE arrangement THEN
        DO:
           BUFFER-COPY t-arrangement TO arrangement.
           IF char1 NE "" THEN
           DO:
               FIND FIRST waehrung WHERE waehrung.bezeich EQ char1 NO-LOCK.
               ASSIGN arrangement.betriebsnr = waehrung.waehrungsnr.
           END.
           RELEASE arrangement.
           ASSIGN success-flag = YES.
        END.
    END.
END CASE.
