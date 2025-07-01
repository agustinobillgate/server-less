DEFINE TEMP-TABLE waehrung-his
    FIELD waehrungsnr                AS INTEGER
    FIELD wabkurz                    AS CHARACTER
    FIELD bezeich                    AS CHARACTER
    FIELD betrag                     AS DECIMAL
    FIELD datum                      AS DATE
.

DEFINE INPUT PARAMETER currencyNo AS INTEGER.
DEFINE INPUT PARAMETER from-date  AS DATE.
DEFINE INPUT PARAMETER to-date    AS DATE.
DEFINE OUTPUT PARAMETER avg-rate  AS DECIMAL.
DEFINE OUTPUT PARAMETER TABLE FOR waehrung-his.

DEFINE VARIABLE days       AS INTEGER NO-UNDO INIT 0.
DEFINE VARIABLE tot-betrag AS DECIMAL NO-UNDO INIT 0.

FIND FIRST waehrung WHERE waehrung.waehrungsnr EQ currencyNo NO-LOCK NO-ERROR.
IF AVAILABLE waehrung THEN
DO:
    FOR EACH exrate WHERE exrate.artnr EQ waehrung.waehrungsnr
        AND exrate.datum GE from-date
        AND exrate.datum LE to-date NO-LOCK BY exrate.datum BY exrate.betrag:
        FIND FIRST waehrung-his WHERE waehrung-his.betrag EQ exrate.betrag NO-LOCK NO-ERROR.
        IF NOT AVAILABLE waehrung-his THEN
        DO:
            CREATE waehrung-his.
            ASSIGN      
                days = days + 1
                tot-betrag = tot-betrag + exrate.betrag
                waehrung-his.waehrungsnr = waehrung.waehrungsnr             
                waehrung-his.wabkurz     = waehrung.wabkurz                 
                waehrung-his.bezeich     = waehrung.bezeich                 
                waehrung-his.betrag      = exrate.betrag                    
                waehrung-his.datum       = exrate.datum                     
            . 
        END.
    END.
END.

ASSIGN avg-rate = tot-betrag / days.
