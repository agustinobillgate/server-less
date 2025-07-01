
DEFINE TEMP-TABLE b1-list
    FIELD argtnr        LIKE arrangement.argtnr
    FIELD wabkurz       LIKE waehrung.wabkurz
    FIELD arrangement   LIKE arrangement.arrangement
    FIELD argt-bez      LIKE arrangement.argt-bez.

DEF INPUT  PARAMETER pax         AS INTEGER.
DEF INPUT  PARAMETER nightstay   AS INTEGER.
DEF OUTPUT PARAMETER TABLE FOR b1-list.

IF pax = 0 AND nightstay = 0 THEN
FOR EACH arrangement WHERE arrangement.segmentcode = 0 
    AND NOT arrangement.weeksplit NO-LOCK, 
    FIRST waehrung WHERE waehrung.waehrungsnr = arrangement.betriebsnr NO-LOCK 
    BY arrangement.argtnr:
    RUN assign-it.
END.
ELSE
FOR EACH arrangement WHERE arrangement.segmentcode = 0 AND
    (arrangement.waeschewechsel = pax OR arrangement.waeschewechsel = 0) 
    AND (arrangement.handtuch = nightstay OR arrangement.handtuch = 0) 
    AND NOT arrangement.weeksplit NO-LOCK, 
    FIRST waehrung WHERE waehrung.waehrungsnr = arrangement.betriebsnr NO-LOCK 
    BY arrangement.argtnr:
    RUN assign-it.
END.

PROCEDURE assign-it:
    CREATE b1-list.
    ASSIGN
    b1-list.argtnr        = arrangement.argtnr
    b1-list.wabkurz       = waehrung.wabkurz
    b1-list.arrangement   = arrangement.arrangement
    b1-list.argt-bez      = arrangement.argt-bez.
END.
