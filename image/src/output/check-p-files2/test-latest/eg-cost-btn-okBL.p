
DEFINE TEMP-TABLE scost LIKE eg-cost
    FIELD strMonth AS CHAR FORMAT "x(12)".

DEF INPUT PARAMETER case-type AS INT.
DEF INPUT PARAMETER TABLE FOR scost.
DEF INPUT PARAMETER blframe AS INT.
DEF INPUT PARAMETER fdate1  AS DATE.
DEF INPUT PARAMETER tdate1  AS DATE.
DEF INPUT PARAMETER intres  AS INT.
DEF INPUT PARAMETER intres4 AS INT.

DEF INPUT PARAMETER fyear1  AS INT.
DEF INPUT PARAMETER rmonth  AS INT. 
DEF INPUT PARAMETER fusage  AS INTEGER.
DEF INPUT PARAMETER fprice  AS DECIMAL.
DEF INPUT PARAMETER fval    AS DECIMAL.

IF case-type = 1 THEN       /* btn-ok */
DO:
    IF blframe = 0 THEN
    DO:
        FOR EACH eg-cost WHERE eg-cost.datum >= fdate1 AND eg-cost.datum <= tdate1 AND eg-cost.resource-nr = intres :
            DELETE eg-cost.
        END.

        FOR EACH scost:
            CREATE eg-cost.
            ASSIGN eg-cost.datum       = scost.datum
                   eg-cost.resource-nr = scost.resource-nr
                   eg-cost.usage       = scost.usage
                   eg-cost.price       = scost.price
                   eg-cost.cost        = scost.usage * scost.price.
        END.
    END.
    ELSE
    DO:
        FOR EACH eg-cost WHERE eg-cost.datum >= fdate1 AND eg-cost.datum <= tdate1 AND eg-cost.resource-nr = intres4 :
            DELETE eg-cost.
        END.

        FOR EACH scost:
            CREATE eg-cost.
            ASSIGN eg-cost.datum       = scost.datum
                   eg-cost.resource-nr = scost.resource-nr
                   eg-cost.usage       = scost.usage
                   eg-cost.price       = scost.price
                   eg-cost.cost        = scost.usage * scost.price.
        END.
    END.
END.

IF case-type = 2 THEN       /* btn-ok1 */
DO:
    FIND FIRST eg-cost WHERE eg-cost.YEAR = fyear1 AND eg-cost.MONTH = rmonth
        AND eg-cost.resource-nr = intres4 NO-ERROR.
    IF AVAILABLE eg-cost THEN
    DO:

        ASSIGN eg-cost.YEAR = fyear1
               eg-cost.MONTH = rmonth
               eg-cost.resource-nr = intres4
               eg-cost.usage = fusage
               eg-cost.price = fprice
               eg-cost.cost  = fval. 
        /*MT
        HIDE MESSAGE NO-PAUSE.  
        MESSAGE translateExtended ("Cost has been Successfully added.",lvCAREA,"") 
            VIEW-AS ALERT-BOX INFORMATION.
        */
    END.
    ELSE
    DO:
        CREATE eg-cost.
        ASSIGN eg-cost.YEAR = fyear1
               eg-cost.MONTH = rmonth
               eg-cost.resource-nr = intres4
               eg-cost.usage = fusage
               eg-cost.price = fprice
               eg-cost.cost  = fval. 

        /*MT
        HIDE MESSAGE NO-PAUSE.  
        MESSAGE translateExtended ("Cost has been Successfully added.",lvCAREA,"") 
            VIEW-AS ALERT-BOX INFORMATION.
        */
    END.
END.
