
DEF INPUT  PARAMETER case-type   AS INT.
DEF INPUT  PARAMETER nonr        AS INT.
DEF INPUT  PARAMETER location2   AS INT.
DEF INPUT  PARAMETER zinr        AS CHAR.
DEF OUTPUT PARAMETER msg         AS LOGICAL INIT NO.

DEF BUFFER queri2 FOR eg-moveproperty.

IF case-type = 1 THEN
DO:
    FIND FIRST eg-property WHERE eg-property.nr = nonr NO-ERROR.
    IF AVAILABLE eg-property THEN
    DO:
        IF eg-property.location NE location2 THEN /*FT serverless*/
        DO:
            CREATE queri2.
            ASSIGN queri2.datum = TODAY
                       queri2.property-nr = eg-property.nr
                       queri2.fr-location = eg-property.location
                       queri2.to-location = location2
                       queri2.fr-room     = eg-property.zinr
                       queri2.to-room     = zinr.
        END.
        ELSE 
        DO:
            CREATE queri2.
            ASSIGN queri2.datum = TODAY
                queri2.property-nr = eg-property.nr
                queri2.fr-location = eg-property.location
                queri2.to-location = location2
                queri2.fr-room     = eg-property.zinr
                queri2.to-room     = zinr.
        END.
        ASSIGN eg-property.location = location2
               eg-property.zinr     = zinr .

        FOR each eg-request where eg-request.propertynr = eg-property.nr and eg-request.reqstatus < 3 :
            assign eg-request.reserve-int = location2
                    eg-request.zinr       = zinr.
        end.

        FOR each eg-maintain where eg-maintain.propertynr = eg-property.nr and eg-maintain.type = 1 :
            assign eg-maintain.location =location2
                    eg-maintain.zinr    = zinr.
        end.

        msg = YES.
    END.
END.
ELSE IF case-type = 2 THEN
DO:
    FIND FIRST eg-property WHERE eg-property.nr = nonr NO-ERROR.
    IF AVAILABLE eg-property THEN
    DO:
        IF eg-property.location NE location2 THEN
            DO:
                CREATE queri2.
                ASSIGN queri2.datum = TODAY
                       queri2.property-nr = eg-property.nr
                       queri2.fr-location = eg-property.location
                       queri2.to-location = location2
                       queri2.fr-room     = eg-property.zinr
                       queri2.to-room     = zinr.
            END.
            ELSE 
            DO:
                CREATE queri2.
                ASSIGN queri2.datum = TODAY
                       queri2.property-nr = eg-property.nr
                       queri2.fr-location = eg-property.location
                       queri2.to-location = location2
                       queri2.fr-room     = eg-property.zinr
                       queri2.to-room     = zinr.
            END.

        ASSIGN 
            eg-property.location = location2
            eg-property.zinr     = zinr .

        for each eg-request where eg-request.propertynr = eg-property.nr and eg-request.reqstatus < 3 :
            assign eg-request.reserve-int = location2
                   eg-request.zinr        = zinr.
        end.
                
        for each eg-maintain where eg-maintain.propertynr = eg-property.nr and eg-maintain.type = 1 :
            assign eg-maintain.location = location2
                   eg-maintain.zinr     = zinr.
        end.

        msg = YES.
    END.
END.
