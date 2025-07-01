DEFINE TEMP-TABLE t-eg-property LIKE eg-property.

DEFINE TEMP-TABLE rec-meter
    FIELD prop-nr       AS INTEGER
    FIELD rec-date      AS DATE
    FIELD rec-time      AS INTEGER
    FIELD rec-by        AS CHAR
    FIELD rec-hour      AS INTEGER
    FIELD rec-meter     AS INTEGER.


DEF INPUT PARAMETER user-init AS CHAR.
DEF OUTPUT PARAMETER GroupID AS INT.
DEF OUTPUT PARAMETER EngID AS INT.
DEF OUTPUT PARAMETER msg AS LOGICAL INIT NO.
DEF OUTPUT PARAMETER TABLE FOR rec-meter.
DEF OUTPUT PARAMETER TABLE FOR t-eg-property.

RUN define-group.
RUN define-engineering.

RUN create-rec-meter.

FOR EACH eg-property WHERE eg-property.nr NE 0:
    CREATE t-eg-property.
    BUFFER-COPY eg-property TO t-eg-property.
END.
PROCEDURE Define-Group:
    FIND FIRST bediener WHERE bediener.userinit = user-init NO-LOCK NO-ERROR.
    IF AVAILABLE bediener THEN
    DO:
        ASSIGN GroupID = bediener.user-group.
    END.
END.

PROCEDURE Define-engineering:

    FIND FIRST htparam WHERE htparam.paramnr = 1200 AND htparam.feldtyp = 1 NO-LOCK NO-ERROR.
    IF AVAILABLE htparam THEN
    DO:
        ASSIGN EngID = htparam.finteger.
    END.
    ELSE
    DO:
        ASSIGN EngID = 0.
        msg = YES.
    END.
END.

PROCEDURE create-rec-meter:
    FOR EACH rec-meter:
        DELETE rec-meter.
    END.

    FOR EACH eg-propMeter NO-LOCK:
        CREATE rec-meter.
        ASSIGN rec-meter.prop-nr    = eg-propMeter.propertynr
            rec-meter.rec-date      = eg-propMeter.rec-date
            rec-meter.rec-time      = eg-propMeter.rec-time
            rec-meter.rec-by        = eg-propMeter.rec-by
            rec-meter.rec-hour      = eg-propMeter.val-hour
            rec-meter.rec-meter     = eg-propMeter.val-meter.
    END.
END.

