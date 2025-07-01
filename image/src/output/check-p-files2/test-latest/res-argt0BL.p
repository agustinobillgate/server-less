
DEF TEMP-TABLE t-arrangement LIKE arrangement.
DEF TEMP-TABLE t-waehrung    LIKE waehrung.

DEF INPUT  PARAMETER pax         AS INTEGER.
DEF INPUT  PARAMETER nightstay   AS INTEGER.
DEF OUTPUT PARAMETER TABLE FOR t-arrangement.
DEF OUTPUT PARAMETER TABLE FOR t-waehrung.

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
    CREATE t-arrangement.
    BUFFER-COPY arrangement TO t-arrangement.
    FIND FIRST t-waehrung WHERE t-waehrung.waehrungsnr = waehrung.waehrungsnr
        NO-ERROR.
    IF NOT AVAILABLE t-waehrung THEN
    DO:
      CREATE t-waehrung.
      BUFFER-COPY waehrung TO t-waehrung.
  END.
END.
