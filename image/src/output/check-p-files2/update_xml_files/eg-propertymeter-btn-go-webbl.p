DEFINE TEMP-TABLE t-eg-property LIKE eg-property.

DEFINE TEMP-TABLE rec-meter
    FIELD prop-nr       AS INTEGER
    FIELD rec-date      AS DATE
    FIELD rec-time      AS INTEGER
    FIELD rec-by        AS CHAR
    FIELD rec-hour      AS INTEGER
    FIELD rec-meter     AS INTEGER
.

DEFINE TEMP-TABLE input-list
    FIELD last-propnr   AS INTEGER INIT 0
    FIELD location      AS INTEGER
    FIELD task          AS INTEGER
    FIELD zinr          AS CHARACTER
.

DEFINE TEMP-TABLE output-list
    FIELD last-propnr   AS INTEGER INIT 0
    FIELD all-data      AS LOGICAL INIT NO
.


DEF INPUT PARAMETER TABLE FOR input-list.
/* 
DEF INPUT PARAMETER user-init AS CHAR.
DEF OUTPUT PARAMETER GroupID AS INT.
DEF OUTPUT PARAMETER EngID AS INT.
DEF OUTPUT PARAMETER msg AS LOGICAL.
*/
DEF OUTPUT PARAMETER TABLE FOR rec-meter.
DEF OUTPUT PARAMETER TABLE FOR t-eg-property.
DEF OUTPUT PARAMETER TABLE FOR output-list.

DEFINE VARIABLE counter AS INTEGER.
counter = 0.

FIND FIRST input-list NO-LOCK NO-ERROR.
IF NOT AVAILABLE input-list THEN
DO:
    RETURN.
END.
ELSE
DO:
    CREATE output-list.
END.

IF input-list.location NE 0 AND TRIM(input-list.zinr) EQ "" AND input-list.task NE 0 THEN
DO:
    FOR EACH eg-property WHERE eg-property.nr GT input-list.last-propnr
        AND eg-property.location EQ input-list.location 
        AND eg-property.maintask EQ input-list.task NO-LOCK BY eg-property.nr:
        counter = counter + 1.
        CREATE t-eg-property.
        BUFFER-COPY eg-property TO t-eg-property.
        RUN create-rec-meter(eg-property.nr).
        IF counter EQ 300 THEN
        DO:
            output-list.last-propnr = eg-property.nr.
            LEAVE.
        END.
    END.
END.
ELSE IF input-list.location NE 0 AND TRIM(input-list.zinr) EQ "" AND input-list.task EQ 0 THEN
DO:
    FOR EACH eg-property WHERE eg-property.nr GT input-list.last-propnr
        AND eg-property.location EQ input-list.location NO-LOCK BY eg-property.nr:
        counter = counter + 1.
        CREATE t-eg-property.
        BUFFER-COPY eg-property TO t-eg-property.
        RUN create-rec-meter(eg-property.nr).
        IF counter EQ 300 THEN
        DO:
            output-list.last-propnr = eg-property.nr.
            LEAVE.
        END.
    END.
END.
ELSE IF input-list.location EQ 0 AND TRIM(input-list.zinr) NE "" AND input-list.task NE 0 THEN
DO:
    FOR EACH eg-property WHERE eg-property.nr GT input-list.last-propnr
        AND eg-property.zinr EQ input-list.zinr
        AND eg-property.maintask EQ input-list.task NO-LOCK BY eg-property.nr:
        counter = counter + 1.
        CREATE t-eg-property.
        BUFFER-COPY eg-property TO t-eg-property.
        RUN create-rec-meter(eg-property.nr).
        IF counter EQ 300 THEN
        DO:
            output-list.last-propnr = eg-property.nr.
            LEAVE.
        END.
    END.
END.
ELSE IF input-list.location EQ 0 AND TRIM(input-list.zinr) NE "" AND input-list.task EQ 0 THEN
DO:
    FOR EACH eg-property WHERE eg-property.nr GT input-list.last-propnr
        AND eg-property.zinr EQ input-list.zinr NO-LOCK BY eg-property.nr:
        counter = counter + 1.
        CREATE t-eg-property.
        BUFFER-COPY eg-property TO t-eg-property.
        RUN create-rec-meter(eg-property.nr).
        IF counter EQ 300 THEN
        DO:
            output-list.last-propnr = eg-property.nr.
            LEAVE.
        END.
    END.
END.
ELSE IF input-list.location EQ 0 AND TRIM(input-list.zinr) EQ "" AND input-list.task NE 0 THEN
DO:
    FOR EACH eg-property WHERE eg-property.nr GT input-list.last-propnr
        AND eg-property.location NE 999
        AND eg-property.maintask EQ input-list.task NO-LOCK BY eg-property.nr:
        counter = counter + 1.
        CREATE t-eg-property.
        BUFFER-COPY eg-property TO t-eg-property.
        RUN create-rec-meter(eg-property.nr).
        IF counter EQ 300 THEN
        DO:
            output-list.last-propnr = eg-property.nr.
            LEAVE.
        END.
    END.
END.
ELSE
DO:
    FOR EACH eg-property WHERE eg-property.nr GT input-list.last-propnr
        AND eg-property.location NE 999 NO-LOCK BY eg-property.nr:
        counter = counter + 1.
        CREATE t-eg-property.
        BUFFER-COPY eg-property TO t-eg-property.
        RUN create-rec-meter(eg-property.nr).
        IF counter EQ 300 THEN
        DO:
            output-list.last-propnr = eg-property.nr.
            LEAVE.
        END.
    END.
END.

IF counter LT 300 THEN output-list.all-data = YES.

PROCEDURE create-rec-meter:
    DEFINE INPUT PARAMETER propnr AS INT.

    FOR EACH eg-propMeter WHERE eg-propMeter.propertynr EQ propnr NO-LOCK:
        CREATE rec-meter.
        ASSIGN rec-meter.prop-nr    = eg-propMeter.propertynr
            rec-meter.rec-date      = eg-propMeter.rec-date
            rec-meter.rec-time      = eg-propMeter.rec-time
            rec-meter.rec-by        = eg-propMeter.rec-by
            rec-meter.rec-hour      = eg-propMeter.val-hour
            rec-meter.rec-meter     = eg-propMeter.val-meter.
    END.
END.

