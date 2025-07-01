DEFINE TEMP-TABLE temp-rec
    FIELD prop-nr       AS INTEGER
    FIELD prop-nm       AS CHAR     FORMAT "x(30)"
    FIELD rec-date      AS DATE
    FIELD rec-time      AS INTEGER
    FIELD rec-by        AS CHAR
    FIELD rec-hour      AS INTEGER
    FIELD rec-meter     AS INTEGER.

DEF INPUT PARAMETER blframe AS INT.
DEF INPUT PARAMETER intRes AS INT.
DEF INPUT PARAMETER frd AS DATE.
DEF INPUT PARAMETER tod AS DATE.
DEF INPUT PARAMETER strName AS CHAR.
DEF OUTPUT PARAMETER TABLE FOR temp-rec.

DEF VAR sday   AS DATE NO-UNDO.
DEF VAR eday   AS DATE NO-UNDO.

FOR EACH temp-rec :
    DELETE temp-rec.
END.

IF blframe = 0 THEN
DO:
    sday = frd .
    eday = tod .

    DO WHILE sday <= eday :
        FIND FIRST eg-propMeter WHERE eg-propmeter.rec-date = sday  AND eg-propmeter.propertynr = intRes NO-LOCK NO-ERROR.
        IF AVAILABLE eg-propmeter THEN
        DO:
            CREATE temp-rec.
            ASSIGN temp-rec.prop-nr = intRes
                temp-rec.prop-nm    = strname
                temp-rec.rec-date   = eg-propmeter.rec-date       
                temp-rec.rec-hour   = eg-propMeter.val-hour   
                temp-rec.rec-meter  = eg-propmeter.val-meter.                
        END.
        ELSE
        DO:
            CREATE temp-rec.
            ASSIGN temp-rec.prop-nr = intRes
                temp-rec.prop-nm    = strname
                temp-rec.rec-date   = sday       
                temp-rec.rec-hour   = 0   
                temp-rec.rec-meter  = 0.
        END.
        sday = sday + 1.
    END.

END.
ELSE
DO:
    sday = frd .
    eday = tod .

    DO WHILE sday <= eday :
        FIND FIRST eg-propMeter WHERE eg-propmeter.rec-date = sday  AND eg-propmeter.propertynr = intRes NO-LOCK NO-ERROR.
        IF AVAILABLE eg-propmeter THEN
        DO:
            CREATE temp-rec.
            ASSIGN temp-rec.prop-nr = intRes
                temp-rec.prop-nm    = strname
                temp-rec.rec-date   = eg-propmeter.rec-date       
                temp-rec.rec-hour   = eg-propMeter.val-hour   
                temp-rec.rec-meter  = eg-propmeter.val-meter.                
        END.
        ELSE
        DO:
            CREATE temp-rec.
            ASSIGN temp-rec.prop-nr = intRes
                temp-rec.prop-nm    = strname
                temp-rec.rec-date   = sday       
                temp-rec.rec-hour   = 0   
                temp-rec.rec-meter  = 0.
        END.

        sday = sday + 1.
    END.
END.
