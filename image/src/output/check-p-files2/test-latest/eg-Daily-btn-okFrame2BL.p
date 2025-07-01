
DEFINE TEMP-TABLE scost LIKE eg-cost.

DEF INPUT PARAMETER TABLE FOR scost.
DEF INPUT PARAMETER blframe AS INT.
DEF INPUT PARAMETER a1      AS DATE.
DEF INPUT PARAMETER b1      AS DATE.
DEF INPUT PARAMETER intres  AS INT.

IF blframe = 0 THEN
DO:
    FOR EACH eg-cost WHERE eg-cost.datum >= a1 AND eg-cost.datum <= b1 AND eg-cost.resource-nr = intres :
        DELETE eg-cost.
    END.

    FOR EACH scost:
        CREATE eg-cost.
        ASSIGN eg-cost.datum       = scost.datum
               eg-cost.resource-nr = scost.resource-nr
               eg-cost.usage       = scost.usage
               eg-cost.price       = scost.price
               eg-cost.cost        = scost.usage * scost.price
               eg-cost.YEAR        = YEAR(TODAY).
    END.
END.
ELSE
DO:
    FOR EACH eg-cost WHERE eg-cost.datum >= a1 AND eg-cost.datum <= b1 AND eg-cost.resource-nr = intres :
        DELETE eg-cost.
    END.

    FOR EACH scost:
        CREATE eg-cost.
        ASSIGN eg-cost.datum       = scost.datum
               eg-cost.resource-nr = scost.resource-nr
               eg-cost.usage       = scost.usage
               eg-cost.price       = scost.price
               eg-cost.cost        = scost.usage * scost.price
               eg-cost.YEAR        = YEAR(TODAY).
    END.
END.
