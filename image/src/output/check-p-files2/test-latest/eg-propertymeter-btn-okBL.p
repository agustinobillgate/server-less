
DEFINE TEMP-TABLE temp-rec
    FIELD prop-nr       AS INTEGER
    FIELD prop-nm       AS CHAR     FORMAT "x(30)"
    FIELD rec-date      AS DATE
    FIELD rec-time      AS INTEGER
    FIELD rec-by        AS CHAR
    FIELD rec-hour      AS INTEGER
    FIELD rec-meter     AS INTEGER.

DEF INPUT PARAMETER TABLE FOR temp-rec.
DEF INPUT PARAMETER user-init AS CHAR.
DEF INPUT PARAMETER blframe AS INT.
DEF INPUT PARAMETER frd AS DATE.
DEF INPUT PARAMETER tod AS DATE.
DEF INPUT PARAMETER intres AS INT.

IF blframe = 0 THEN
DO:
    FOR EACH eg-propmeter WHERE eg-propmeter.rec-date >= frd AND eg-propmeter.rec-date <= tod 
        AND eg-propmeter.propertynr = intres :
        DELETE eg-propmeter.
    END.

    FOR EACH temp-rec:
        CREATE eg-propmeter.
        ASSIGN eg-propmeter.propertynr  = temp-rec.prop-nr
               eg-propmeter.rec-date    = temp-rec.rec-date
               /*eg-propmeter.rec-time    = */
               eg-propmeter.rec-by      = user-init
               eg-propmeter.val-meter   = temp-rec.rec-meter
               eg-propmeter.val-hour    = temp-rec.rec-hour
               eg-propmeter.create-date = TODAY
               eg-propmeter.create-time = TIME.
    END.
END.
ELSE
DO:
    FOR EACH eg-propmeter WHERE eg-propmeter.rec-date >= frd AND eg-propmeter.rec-date <= tod 
        AND eg-propmeter.propertynr = intres :
        DELETE eg-propmeter.
    END.

    FOR EACH temp-rec:
        CREATE eg-propmeter.
        ASSIGN eg-propmeter.propertynr  = temp-rec.prop-nr
               eg-propmeter.rec-date    = temp-rec.rec-date
               /*eg-propmeter.rec-time    = */
               eg-propmeter.rec-by      = user-init
               eg-propmeter.val-meter   = temp-rec.rec-meter
               eg-propmeter.val-hour    = temp-rec.rec-hour
               eg-propmeter.create-date = TODAY
               eg-propmeter.create-time = TIME.
    END.

END.
