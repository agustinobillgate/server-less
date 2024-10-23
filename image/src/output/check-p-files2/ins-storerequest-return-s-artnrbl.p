
DEF INPUT  PARAMETER s-artnr         AS INT.
DEF INPUT  PARAMETER curr-lager      AS INT.
DEF INPUT  PARAMETER avail-out-list  AS LOGICAL.
DEF INPUT  PARAMETER transdate       AS DATE.
DEF INPUT  PARAMETER closedate       AS DATE.
DEF INPUT  PARAMETER mat-closedate   AS DATE.
DEF INPUT  PARAMETER req-flag        AS LOGICAL.

DEF OUTPUT PARAMETER t-stock-oh      AS DECIMAL.
DEF OUTPUT PARAMETER t-price         AS DECIMAL.
DEF OUTPUT PARAMETER t-description   AS CHAR.
DEF OUTPUT PARAMETER err-flag        AS INT INIT 0.
DEF OUTPUT PARAMETER err-warning     AS LOGICAL INIT NO.

FIND FIRST l-artikel WHERE l-artikel.artnr = s-artnr NO-LOCK NO-ERROR. 
IF NOT AVAILABLE l-artikel THEN 
DO: 
  /*MT
  HIDE MESSAGE NO-PAUSE. 
  MESSAGE translateExtended ("Article not found",lvCAREA,"") VIEW-AS ALERT-BOX INFORMATION. 
  s-artnr = 0. 
  description = translateExtended ("Outgoing Stock Item",lvCAREA,""). 
  DISP s-artnr description WITH FRAME frame1. 
  APPLY "entry" TO s-artnr. 
  */
  err-flag = 1.
  RETURN NO-APPLY. 
END. 
IF l-artikel.betriebsnr = 0 THEN 
DO: 
  FIND FIRST l-bestand WHERE l-bestand.lager-nr = curr-lager 
    AND l-bestand.artnr = s-artnr NO-LOCK NO-ERROR. 
  IF NOT AVAILABLE l-bestand THEN 
  DO: 
    /*MT
    HIDE MESSAGE NO-PAUSE. 
    MESSAGE translateExtended ("Article not found in store ",lvCAREA,"") + CAPS(lager-bezeich) 
    VIEW-AS ALERT-BOX INFORMATION. 
    s-artnr = 0. 
    description = translateExtended ("Outgoing Stock Item",lvCAREA,""). 
    DISP s-artnr description WITH FRAME frame1. 
    APPLY "entry" TO s-artnr. 
    */
    err-flag = 2.
    RETURN NO-APPLY. 
  END. 
  ELSE 
  DO: 
    IF avail-out-list THEN 
    DO:
        err-flag = 3.
        RETURN NO-APPLY. 
    END.
    /*MT
    FIND FIRST out-list WHERE out-list.artnr = s-artnr NO-LOCK NO-ERROR. 
    IF AVAILABLE out-list THEN 
    DO: 
      HIDE MESSAGE NO-PAUSE. 
      MESSAGE translateExtended ("Article already selected, change the quantity instead.",lvCAREA,"") 
      VIEW-AS ALERT-BOX INFORMATION. 
      APPLY "entry" TO s-artnr. 
      RETURN NO-APPLY. 
    END. 
    */
    IF l-artikel.endkum LT 3 THEN 
    DO: 
      IF transdate GT closedate THEN 
      DO: 
        /*MT
        HIDE MESSAGE NO-PAUSE. 
        MESSAGE translateExtended ("F&B Closing Inventory not yet performed,",lvCAREA,"") 
        SKIP 
        translateExtended ("Outgoing not possible.",lvCAREA,"") 
        VIEW-AS ALERT-BOX INFORMATION. 
        s-artnr = 0. 
        description = translateExtended ("Outgoing Stock Item",lvCAREA,""). 
        DISP s-artnr description WITH FRAME frame1. 
        APPLY "entry" TO s-artnr. 
        */
        err-flag = 4.
        RETURN NO-APPLY. 
      END. 
    END. 
    IF l-artikel.endkum EQ 3 THEN 
    DO: 
      IF transdate GT mat-closedate THEN 
      DO: 
        /*MT
        HIDE MESSAGE NO-PAUSE. 
        MESSAGE translateExtended ("Material Closing Inventory not yet performed,",lvCAREA,"") 
        SKIP 
        translateExtended ("Outgoing not possible.",lvCAREA,"") 
        VIEW-AS ALERT-BOX INFORMATION. 
        s-artnr = 0. 
        description = translateExtended ("Outgoing Stock Item",lvCAREA,""). 
        DISP s-artnr description WITH FRAME frame1. 
        APPLY "entry" TO s-artnr. 
        */
        err-flag = 5.
        RETURN NO-APPLY. 
      END. 
    END. 
    IF req-flag THEN 
    DO: 
      FIND FIRST l-op WHERE l-op.artnr = s-artnr AND 
        l-op.datum = transdate AND (l-op.op-art = 13 OR l-op.op-art = 14) 
        AND SUBSTR(l-op.lscheinnr,4, (length(l-op.lscheinnr) - 3)) = 
      SUBSTR(lscheinnr,4, (length(lscheinnr) - 3)) NO-LOCK NO-ERROR. 
      IF AVAILABLE l-op THEN 
      DO: 
        /*MT
        HIDE MESSAGE NO-PAUSE. 
        MESSAGE translateExtended ("Article already posted in: ",lvCAREA,"") + l-op.lscheinnr 
        VIEW-AS ALERT-BOX WARNING. 
        */
        err-warning = YES.
      END. 
    END. 
    t-stock-oh = l-bestand.anz-anf-best + l-bestand.anz-eingang 
      - l-bestand.anz-ausgang. 
    t-description = l-artikel.bezeich + " - " + l-artikel.masseinheit. 
    t-price = l-artikel.vk-preis. 
    /*MT
    DISP description stock-oh WITH FRAME frame1. 
    IF show-price THEN DISP price WITH FRAME frame1. 
    ENABLE qty WITH FRAME frame1. 
    APPLY "entry" TO qty IN FRAME frame1. 
    */
    err-flag = 6.
    RETURN NO-APPLY. 
  END. 
END. 
ELSE 
DO: 
  t-description = l-artikel.bezeich + " - " + l-artikel.masseinheit. 
  t-price = 0. 
  t-stock-oh = 0. 
  /*MT
  DISP description stock-oh price WITH FRAME frame1. 
  ENABLE qty WITH FRAME frame1. 
  APPLY "entry" TO qty IN FRAME frame1. 
  */
  err-flag = 7.
  RETURN NO-APPLY. 
END. 
