
DEFINE TEMP-TABLE art-bestand 
  FIELD nr       AS INTEGER FORMAT ">>>" LABEL " No" 
  FIELD zwkum    AS INTEGER 
  FIELD bezeich  AS CHARACTER FORMAT "x(28)" LABEL "Description" 
  FIELD prevval  AS DECIMAL FORMAT "->>>,>>>,>>>,>>9.99" LABEL "Opening Value" 
    INITIAL 0 
  FIELD adjust   AS DECIMAL FORMAT "->>>,>>>,>>9.99 " LABEL "InitOH Adjust" 
    INITIAL 0 
  FIELD inval    AS DECIMAL FORMAT "->>,>>>,>>>,>>9.99" LABEL "Incoming" 
    INITIAL 0 
  FIELD outval   AS DECIMAL FORMAT "->>,>>>,>>>,>>9.99" LABEL "Consumed" 
    INITIAL 0 
  FIELD actval   AS DECIMAL FORMAT "->>>,>>>,>>>,>>9.99" LABEL "Ending Value" 
    INITIAL 0
    
  FIELD inv-acct AS CHAR FORMAT "x(12)" LABEL "Inv Account"
  FIELD fibukonto AS CHAR FORMAT "x(20)"
  FIELD artnr LIKE l-artikel.artnr. 

DEFINE INPUT PARAMETER pvILanguage  AS INTEGER NO-UNDO.
DEFINE INPUT PARAMETER to-date      AS DATE.
DEFINE INPUT PARAMETER lager-no     AS INTEGER.
DEFINE INPUT PARAMETER from-main    AS INTEGER.
DEFINE INPUT PARAMETER to-main      AS INTEGER.
DEFINE INPUT PARAMETER sort-type    AS INTEGER. /* 1 by inv-acct 2 by desc */
DEFINE OUTPUT PARAMETER TABLE FOR art-bestand.

DEFINE VARIABLE long-digit AS LOGICAL. 
FIND FIRST htparam WHERE paramnr = 246 NO-LOCK. 
long-digit = htparam.flogical. 


DEFINE VARIABLE from-date AS DATE INITIAL today. 

{supertransBL.i} 
DEF VAR lvCAREA AS CHAR INITIAL "mat-reconsile".

/*************MAIN LOGIC************/
from-date = DATE(MONTH(to-date), 1 , YEAR(to-date)).
IF lager-no = 0 THEN RUN create-list.
ELSE RUN create-list1.


PROCEDURE create-list: 
DEFINE VARIABLE zwkum AS INTEGER. 
DEFINE VARIABLE prevval AS DECIMAL INITIAL 0. 
DEFINE VARIABLE inval AS DECIMAL INITIAL 0. 
DEFINE VARIABLE outval AS DECIMAL INITIAL 0. 
DEFINE VARIABLE actval AS DECIMAL INITIAL 0. 
DEFINE VARIABLE bezeich AS CHAR. 
DEFINE VARIABLE j AS INTEGER INITIAL 0. 
status default "Processing...". 
 
  FOR EACH art-bestand: 
    delete art-bestand. 
  END. 
 
  FOR EACH l-bestand WHERE l-bestand.lager-nr = 0 NO-LOCK, 
    FIRST l-artikel WHERE l-artikel.artnr = l-bestand.artnr 
    AND l-artikel.endkum GE from-main 
    AND l-artikel.endkum LE to-main NO-LOCK, 
    FIRST l-untergrup WHERE l-untergrup.zwkum = l-artikel.zwkum NO-LOCK 
    BY l-untergrup.fibukonto BY l-artikel.artnr: 
    FIND FIRST art-bestand WHERE art-bestand.zwkum EQ l-untergrup.zwkum 
      NO-ERROR. 
    IF NOT AVAILABLE art-bestand THEN 
    DO: 
      create art-bestand. 
      art-bestand.bezeich = l-untergrup.bezeich. 
      art-bestand.zwkum = l-untergrup.zwkum. 
      art-bestand.fibukonto = l-untergrup.fibukonto.
      art-bestand.artnr = l-artikel.artnr.
    END. 
    
    art-bestand.inv-acct = l-untergrup.fibukonto.
    art-bestand.prevval = art-bestand.prevval + l-bestand.val-anf-best. 
    prevval = prevval + l-bestand.val-anf-best. 
    art-bestand.actval  = art-bestand.actval + l-bestand.val-anf-best. 
 
    FOR EACH l-lager NO-LOCK: 
      FOR EACH l-op WHERE l-op.datum GE from-date AND l-op.datum LE to-date 
      AND l-op.artnr = l-artikel.artnr AND l-op.op-art LE 2 
      AND l-op.lager-nr = l-lager.lager-nr AND l-op.loeschflag LE 1 NO-LOCK 
      USE-INDEX artopart_ix:
      /* BLY - C38BE6 */
        IF l-op.op-art = 1 THEN 
        DO: 
          inval = inval + l-op.warenwert. 
          art-bestand.inval = art-bestand.inval + l-op.warenwert. 
          art-bestand.actval  = art-bestand.actval  + l-op.warenwert.
        END. 
        IF l-op.op-art = 2 AND l-op.herkunftflag = 3 THEN
        DO:
          inval = inval + l-op.anzahl * l-artikel.vk-preis. 
          art-bestand.inval   = art-bestand.inval + l-op.anzahl * l-artikel.vk-preis. 
          art-bestand.actval  = art-bestand.actval  + l-op.anzahl * l-artikel.vk-preis.
        END.  
      END. 
 
      FOR EACH l-op WHERE l-op.datum GE from-date AND l-op.datum LE to-date 
        AND l-op.artnr = l-artikel.artnr AND l-op.op-art LE 4 
        AND l-op.lager-nr EQ l-lager.lager-nr  AND l-op.loeschflag LE 1 
        NO-LOCK USE-INDEX artopart_ix,
/*MT 03/05/13 */
        FIRST l-ophdr WHERE l-ophdr.lscheinnr = l-op.lscheinnr 
        AND l-ophdr.op-typ = "STT" AND l-ophdr.fibukonto NE "" NO-LOCK, 
        FIRST gl-acct WHERE gl-acct.fibukonto = l-op.stornogrund 
        NO-LOCK: 
/*MT*/  
        IF l-op.op-art = 3 THEN 
        DO: 
            outval = outval + l-op.warenwert. 
            art-bestand.outval = art-bestand.outval + l-op.warenwert. 
            art-bestand.actval  = art-bestand.actval  - l-op.warenwert.
        END. 
        IF l-op.op-art = 4 AND l-op.herkunftflag = 3 THEN
        DO: 
            outval = outval + l-op.anzahl * l-artikel.vk-preis. 
            art-bestand.outval = art-bestand.outval 
             + l-op.anzahl * l-artikel.vk-preis. 
            art-bestand.actval  = art-bestand.outval 
             - l-op.anzahl * l-artikel.vk-preis.
        END.
      END. 
    END.
    /* END BLY - C38BE6 */
  END. 
  
  j = 0.
  IF sort-type = 1 THEN
  FOR EACH art-bestand BY art-bestand.fibukonto BY art-bestand.artnr:
      j = j + 1. 
      art-bestand.nr = j.
  END.
  ELSE
  FOR EACH art-bestand BY art-bestand.bezeich BY art-bestand.artnr:
      j = j + 1. 
      art-bestand.nr = j.
  END.

  actval = prevval + inval - outval. 
  create art-bestand. 
  art-bestand.bezeich = "                   T O T A L". 
  art-bestand.prevval = prevval. 
  art-bestand.inval = inval. 
  art-bestand.outval = outval. 
  art-bestand.actval = actval.
  art-bestand.nr = 999.
END. 

PROCEDURE create-list1: 
DEFINE VARIABLE zwkum AS INTEGER. 
DEFINE VARIABLE prevval AS DECIMAL INITIAL 0. 
DEFINE VARIABLE inval AS DECIMAL INITIAL 0. 
DEFINE VARIABLE outval AS DECIMAL INITIAL 0. 
DEFINE VARIABLE actval AS DECIMAL INITIAL 0. 
DEFINE VARIABLE bezeich AS CHAR. 
DEFINE VARIABLE j AS INTEGER INITIAL 0. 
DEFINE VARIABLE qty AS DECIMAL. 
DEFINE VARIABLE qty0 AS DECIMAL. 
DEFINE VARIABLE val0 AS DECIMAL. 
 
DEFINE buffer l-oh FOR l-bestand. 
 
status default "Processing...". 

  FOR EACH art-bestand: 
    delete art-bestand. 
  END. 
 
  FOR EACH l-bestand WHERE l-bestand.lager-nr = lager-no NO-LOCK, 
    FIRST l-artikel WHERE l-artikel.artnr = l-bestand.artnr 
    AND l-artikel.endkum GE from-main 
    AND l-artikel.endkum LE to-main NO-LOCK, 
    FIRST l-untergrup WHERE l-untergrup.zwkum = l-artikel.zwkum NO-LOCK 
    BY l-untergrup.fibukonto BY l-artikel.artnr: 
 
    FIND FIRST art-bestand WHERE art-bestand.zwkum EQ l-untergrup.zwkum 
      NO-ERROR. 
    IF NOT AVAILABLE art-bestand THEN 
    DO: 
      create art-bestand. 
      art-bestand.bezeich = l-untergrup.bezeich. 
      art-bestand.zwkum = l-untergrup.zwkum. 
      art-bestand.fibukonto = l-untergrup.fibukonto.
      art-bestand.artnr = l-artikel.artnr.
    END. 
    
    art-bestand.inv-acct = l-untergrup.fibukonto.
    FIND FIRST l-oh WHERE l-oh.lager-nr = 0 AND l-oh.artnr = l-bestand.artnr 
      NO-LOCK. 
    qty = l-bestand.anz-anf-best + l-bestand.anz-eingang - l-bestand.anz-ausgang. 
    qty0 = l-oh.anz-anf-best + l-oh.anz-eingang - l-oh.anz-ausgang. 
    val0 = l-oh.val-anf-best + l-oh.wert-eingang - l-oh.wert-ausgang. 
    IF qty0 NE 0 THEN 
      art-bestand.actval  = art-bestand.actval + (qty / qty0) * val0. 
 
    art-bestand.prevval = art-bestand.prevval + l-bestand.val-anf-best. 
    prevval = prevval + l-bestand.val-anf-best. 
 
 
    FOR EACH l-op WHERE l-op.datum GE from-date AND l-op.datum LE to-date 
      AND l-op.artnr = l-artikel.artnr AND l-op.op-art LE 2 
      AND l-op.lager-nr = lager-no AND l-op.loeschflag LE 1 NO-LOCK 
      USE-INDEX artopart_ix: 
      IF l-op.op-art = 1 THEN 
      DO: 
        inval = inval + l-op.warenwert. 
        art-bestand.inval = art-bestand.inval + l-op.warenwert. 
      END. 
      ELSE 
      DO: 
        inval = inval + l-op.anzahl * l-artikel.vk-preis. 
        art-bestand.inval = art-bestand.inval 
          + l-op.anzahl * l-artikel.vk-preis. 
      END. 
    END. 
 
    FOR EACH l-op WHERE l-op.datum GE from-date AND l-op.datum LE to-date 
      AND l-op.artnr = l-artikel.artnr AND l-op.op-art GE 3 
      AND l-op.op-art LE 4 AND l-op.lager-nr EQ lager-no 
      AND l-op.loeschflag LE 1 NO-LOCK USE-INDEX artopart_ix: 
      IF l-op.op-art = 3 THEN 
      DO: 
        outval = outval + l-op.warenwert. 
        art-bestand.outval = art-bestand.outval + l-op.warenwert. 
      END. 
      ELSE 
      DO: 
        outval = outval + l-op.anzahl * l-artikel.vk-preis. 
        art-bestand.outval = art-bestand.outval 
          + l-op.anzahl * l-artikel.vk-preis. 
      END. 
    END. 
  END. 
  
  j = 0.
  IF sort-type = 1 THEN
  FOR EACH art-bestand BY art-bestand.fibukonto BY art-bestand.artnr:
      j = j + 1. 
      art-bestand.nr = j.
  END.
  ELSE
  FOR EACH art-bestand BY art-bestand.bezeich BY art-bestand.artnr:
      j = j + 1. 
      art-bestand.nr = j.
  END.

  actval = 0. 
  FOR EACH art-bestand: 
    IF art-bestand.prevval = 0 AND art-bestand.inval = 0 
      AND art-bestand.outval = 0 THEN delete art-bestand. 
    ELSE 
    DO: 
      art-bestand.adjust = art-bestand.actval - (art-bestand.prevval 
        + art-bestand.inval - art-bestand.outval).

      actval = actval + art-bestand.actval. 
    END. 
  END. 
 
  create art-bestand. 
  art-bestand.bezeich = "                   T O T A L". 
  art-bestand.prevval = prevval. 
  art-bestand.inval = inval. 
  art-bestand.outval = outval. 
  art-bestand.actval = actval. 
  art-bestand.adjust = (prevval + inval - outval) - actval.
  art-bestand.nr = 999.
END. 

