

DEF TEMP-TABLE t-waehrung
    FIELD wabkurz AS CHAR.

DEF INPUT  PARAMETER pricetab   AS LOGICAL.
DEF INPUT  PARAMETER rec-id     AS INT.
DEF INPUT  PARAMETER foreign-nr AS INT.
DEF INPUT  PARAMETER betriebsnr AS INT.
DEF INPUT  PARAMETER local-nr   AS INT.
DEF OUTPUT PARAMETER wabkurz    AS CHAR.
DEF OUTPUT PARAMETER TABLE FOR t-waehrung.

DEFINE buffer art1 FOR artikel. 
IF pricetab THEN 
DO: 
    FIND FIRST art1 WHERE RECID(art1) = rec-id NO-LOCK. 
    IF betriebsnr = 0 THEN 
    DO: 
      FIND CURRENT art1 EXCLUSIVE-LOCK. 
      art1.betriebsnr = foreign-nr. 
      FIND CURRENT art1 NO-LOCK. 
    END. 
/*  IF local-nr NE foreign-nr THEN */ 
    DO: 
      FIND FIRST waehrung WHERE waehrung.waehrungsnr = art1.betriebsnr NO-LOCK. 
      ASSIGN wabkurz = waehrung.wabkurz.
      FOR EACH waehrung WHERE waehrung.waehrungsnr NE art1.betriebsnr 
        AND waehrung.ankauf GT 0 NO-LOCK BY waehrung.wabkurz: 
        /*MTcurrency:add-last(waehrung.wabkurz) IN FRAME frame1. */
          CREATE t-waehrung.
          ASSIGN t-waehrung.wabkurz = waehrung.wabkurz.
      END. 
    END. 
END. 
ELSE 
DO: 
    IF betriebsnr NE 0 THEN 
    DO: 
      FIND FIRST art1 WHERE RECID(art1) = rec-id EXCLUSIVE-LOCK. 
      art1.betriebsnr = 0. 
      FIND CURRENT art1 NO-LOCK. 
    END. 
/*  IF local-nr NE foreign-nr THEN  */ 
    DO: 
      FIND FIRST waehrung WHERE waehrung.waehrungsnr = local-nr NO-LOCK. 
      ASSIGN wabkurz = waehrung.wabkurz.
      FOR EACH waehrung WHERE waehrung.waehrungsnr NE local-nr 
        AND waehrung.ankauf GT 0 NO-LOCK BY waehrung.wabkurz: 
        /*MTcurrency:add-last(waehrung.wabkurz) IN FRAME frame1. */
        CREATE t-waehrung.
        ASSIGN t-waehrung.wabkurz = waehrung.wabkurz.
      END. 
    END. 
END.
