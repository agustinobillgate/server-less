DEFINE TEMP-TABLE rec-meter
    FIELD prop-nr       AS INTEGER
    FIELD rec-date      AS DATE
    FIELD rec-time      AS INTEGER
    FIELD rec-by        AS CHAR
    FIELD rec-hour      AS INTEGER
    FIELD rec-meter     AS INTEGER.

DEF OUTPUT PARAMETER TABLE FOR rec-meter.

RUN create-rec-meter.

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
