DEFINE TEMP-TABLE property LIKE eg-property.

DEF INPUT PARAMETER TABLE FOR property.
DEF INPUT PARAMETER nr AS INT.
DEF INPUT PARAMETER curr-date AS DATE.

DEFINE BUFFER queri FOR eg-property.
DEFINE BUFFER queri2 FOR eg-moveproperty.

FIND FIRST property.
FIND FIRST eg-property WHERE eg-property.nr = nr.

FIND CURRENT eg-property EXCLUSIVE-LOCK NO-ERROR.
IF AVAILABLE eg-property THEN
DO:
    IF eg-property.location NE property.location THEN
    DO:
        CREATE queri2.
            ASSIGN
             queri2.datum = curr-date
             queri2.property-nr = property.nr
             queri2.fr-location = eg-property.location
             queri2.to-location = property.location
             queri2.fr-room = eg-property.zinr
             queri2.to-room = property.zinr.
    END.
    ELSE 
    DO:
        IF eg-property.zinr NE "" THEN
        DO:
            IF eg-property.zinr NE property.zinr THEN
            DO:
                CREATE queri2.
                ASSIGN  queri2.datum = curr-date
                        queri2.property-nr = property.nr
                        queri2.fr-location = eg-property.location
                        queri2.to-location = property.location
                        queri2.fr-room = eg-property.zinr
                        queri2.to-room = property.zinr.
            END.
            
        END.
        ELSE
        DO:
            IF eg-property.zinr NE property.zinr THEN
            DO:
                CREATE queri2.
                ASSIGN  queri2.datum = curr-date
                        queri2.property-nr = property.nr
                        queri2.fr-location = eg-property.location
                        queri2.to-location = property.location
                        queri2.fr-room = eg-property.zinr
                        queri2.to-room = property.zinr.
            END.
        END.                  
    END.
END.

BUFFER-COPY property TO eg-property.
FIND CURRENT eg-property NO-LOCK.
