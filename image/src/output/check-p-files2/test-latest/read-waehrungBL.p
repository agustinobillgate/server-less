
DEF TEMP-TABLE t-waehrung          LIKE waehrung.

DEF INPUT  PARAMETER case-type    AS INTEGER NO-UNDO.
DEF INPUT  PARAMETER currencyNo   AS INTEGER NO-UNDO.
DEF INPUT  PARAMETER currBez      AS CHAR    NO-UNDO.
DEF OUTPUT PARAMETER TABLE FOR t-waehrung.

CASE case-type:
  WHEN 1 THEN 
  DO:
    FIND FIRST waehrung WHERE waehrung.waehrungsnr = currencyNo NO-LOCK NO-ERROR.
    IF AVAILABLE waehrung THEN
    DO:
      CREATE t-waehrung.
      BUFFER-COPY waehrung TO t-waehrung.
    END.
  END.
  WHEN 2 THEN 
  DO:    
    FIND FIRST waehrung WHERE waehrung.wabkurz = currBez NO-LOCK NO-ERROR.
    IF AVAILABLE waehrung THEN
    DO:
      CREATE t-waehrung.
      BUFFER-COPY waehrung TO t-waehrung.
    END.
  END.
  WHEN 3 THEN
  FOR EACH waehrung WHERE waehrung.betriebsnr = 0 NO-LOCK BY waehrung.bezeich:
    CREATE t-waehrung.
    BUFFER-COPY waehrung TO t-waehrung.
  END.
  WHEN 4 THEN 
  DO:    
    FIND FIRST waehrung WHERE waehrung.bezeich = currBez NO-LOCK NO-ERROR.
    IF AVAILABLE waehrung THEN
    DO:
      CREATE t-waehrung.
      BUFFER-COPY waehrung TO t-waehrung.
    END.
  END.
  WHEN 5 THEN
  DO:
      FOR EACH waehrung WHERE waehrung.waehrungsnr NE currencyNo AND 
          waehrung.betriebsnr = 0 NO-LOCK BY waehrung.bezeich:
          CREATE t-waehrung.
          BUFFER-COPY waehrung TO t-waehrung.
      END.
  END.
  WHEN 6 THEN
  DO:
      FOR EACH waehrung WHERE waehrung.betriebsnr = 0 AND 
          waehrung.ankauf GT 0 AND 
          waehrung.wabkurz NE currBez NO-LOCK BY waehrung.bezeich:
          CREATE t-waehrung.
          BUFFER-COPY waehrung TO t-waehrung.
      END.
  END.
  WHEN 7 THEN
  DO:
      FIND FIRST waehrung WHERE waehrung.waehrungsnr = currencyNo
          AND waehrung.ankauf NE 0 NO-LOCK NO-ERROR. 
      IF AVAILABLE waehrung THEN
      DO:
          CREATE t-waehrung.
          BUFFER-COPY waehrung TO t-waehrung.
      END.
  END.
  WHEN 8 THEN
  FOR EACH waehrung NO-LOCK :
    CREATE t-waehrung.
    BUFFER-COPY waehrung TO t-waehrung.
  END.
  WHEN 9 THEN
  DO:
      FIND FIRST waehrung WHERE waehrung.waehrungsnr NE currencyNo 
          AND waehrung.wabkurz = currBez NO-LOCK NO-ERROR. 
      IF AVAILABLE waehrung THEN
      DO:
          CREATE t-waehrung.
          BUFFER-COPY waehrung TO t-waehrung.
      END.
  END.
END CASE.
