 
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

DEFINE INPUT  PARAMETER to-date      AS DATE.
DEFINE INPUT  PARAMETER lager-no     AS INTEGER.
DEFINE INPUT  PARAMETER from-main    AS INTEGER.
DEFINE INPUT  PARAMETER to-main      AS INTEGER.
DEFINE INPUT  PARAMETER sort-type    AS INTEGER.
DEFINE OUTPUT PARAMETER TABLE FOR art-bestand.

DEFINE VARIABLE from-date AS DATE INITIAL today. 

 
/*************MAIN LOGIC************/
from-date = DATE(MONTH(to-date), 1 , YEAR(to-date)).
IF lager-no = 0 THEN RUN create-list.
ELSE RUN create-list1.

/****************PROCEDURE***************/
PROCEDURE create-list: 
DEFINE VARIABLE zwkum AS INTEGER. 
DEFINE VARIABLE prevval AS DECIMAL INITIAL 0. 
DEFINE VARIABLE inval AS DECIMAL INITIAL 0. 
DEFINE VARIABLE outval AS DECIMAL INITIAL 0. 
DEFINE VARIABLE actval AS DECIMAL INITIAL 0. 
DEFINE VARIABLE bezeich AS CHAR. 
DEFINE VARIABLE j AS INTEGER INITIAL 0. 

DEFINE VARIABLE other-fibu AS LOGICAL. 
DEFINE VARIABLE it-exist AS LOGICAL. 
DEFINE VARIABLE fibukonto AS CHAR. 
DEFINE VARIABLE cost-bezeich AS CHAR FORMAT "x(24)". 
DEFINE VARIABLE cost-acct AS CHAR.
DEFINE VARIABLE create-it AS LOGICAL. 
DEFINE buffer gl-acct1 FOR gl-acct. 


 DEFINE VARIABLE testa AS DECIMAL.

  FOR EACH art-bestand: 
    delete art-bestand. 
  END. 
  
  FOR EACH l-besthis WHERE l-besthis.lager-nr = 0 
      AND l-besthis.anf-best-dat = from-date
      NO-LOCK, 
      FIRST l-artikel WHERE l-artikel.artnr = l-besthis.artnr 
      AND l-artikel.endkum GE from-main 
      AND l-artikel.endkum LE to-main NO-LOCK, 
      FIRST l-untergrup WHERE l-untergrup.zwkum = l-artikel.zwkum NO-LOCK: 
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
      art-bestand.prevval = art-bestand.prevval + l-besthis.val-anf-best. 
      prevval = prevval + l-besthis.val-anf-best. 
      art-bestand.actval  = art-bestand.actval + l-besthis.val-anf-best. 
      
      ASSIGN testa = 0
             testa = l-besthis.val-anf-best.

     
      FOR EACH l-lager NO-LOCK: 
          FOR EACH l-ophis WHERE l-ophis.datum GE from-date 
              AND l-ophis.datum LE to-date 
              AND l-ophis.op-art LE 2 
              AND l-ophis.lager-nr = l-lager.lager-nr 
              AND l-ophis.artnr =  l-artikel.artnr
              AND NOT (l-ophis.fibukonto MATCHES "*CANCELLED*") /* Add by Michael @ 07/12/2018 for not include cancelled receiving */
              NO-LOCK:
              FIND FIRST art-bestand WHERE art-bestand.zwkum EQ l-untergrup.zwkum 
                  NO-ERROR. 
              inval = inval + l-ophis.warenwert. 
              art-bestand.inval = art-bestand.inval + l-ophis.warenwert. 
              art-bestand.actval  = art-bestand.actval  + l-ophis.warenwert. 

              testa = testa + l-ophis.warenwert.
              

          END. 

          FOR EACH l-ophis WHERE l-ophis.lager-nr = l-lager.lager-nr 
              AND l-ophis.datum GE from-date AND l-ophis.datum LE to-date 
              AND l-ophis.artnr GE 3000000 AND l-ophis.artnr LE 9999999 
              AND l-ophis.anzahl NE 0  AND l-ophis.op-art GE 3 
              AND l-ophis.op-art LE 4 
              AND l-ophis.artnr =  l-artikel.artnr 
              AND NOT (l-ophis.fibukonto MATCHES "*CANCELLED*") /* Add by Michael @ 07/12/2018 for not include cancelled receiving */NO-LOCK /*, 
              FIRST l-ophhis WHERE l-ophhis.op-typ = "STT" 
              AND l-ophhis.lscheinnr = l-ophis.lscheinnr 
              AND l-ophhis.fibukonto NE "" NO-LOCK , 
              FIRST gl-acct WHERE gl-acct.fibukonto = l-ophis.fibukonto */
              BY SUBSTR(l-ophis.lscheinnr,4,12) BY l-artikel.bezeich: 
              it-exist = YES. 
              other-fibu = NO. 
              /*IF l-ophis.fibukonto NE "" THEN 
              DO: 
                FIND FIRST gl-acct1 WHERE gl-acct1.fibukonto = l-ophis.fibukonto
                  NO-LOCK NO-ERROR. 
                IF AVAILABLE gl-acct1 THEN other-fibu = YES. 
              END. 
              IF other-fibu THEN 
              DO: 
                fibukonto = gl-acct1.fibukonto. 
                cost-bezeich = gl-acct1.bezeich. 
                IF cost-acct = "" THEN create-it = YES. 
                ELSE create-it = (cost-acct = fibukonto). 
              END. 
              ELSE 
              DO: 
                fibukonto = gl-acct.fibukonto. 
                cost-bezeich = gl-acct.bezeich. 
                IF cost-acct = "" THEN create-it = YES. 
                ELSE create-it = (cost-acct = fibukonto). 
              END. 

              IF create-it THEN 
              DO:*/
                  FIND FIRST art-bestand WHERE art-bestand.zwkum EQ l-untergrup.zwkum 
                  NO-ERROR. 
                  outval = outval + l-ophis.warenwert. 
                  art-bestand.outval = art-bestand.outval + l-ophis.warenwert. 
                  art-bestand.actval  = art-bestand.actval  - l-ophis.warenwert. 
                  testa = testa - l-ophis.warenwert.
                  
              /*END.*/
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
 
DEFINE buffer l-oh FOR l-besthis.

  FOR EACH art-bestand: 
    delete art-bestand. 
  END. 
 
  FOR EACH l-besthis WHERE l-besthis.lager-nr = lager-no 
      AND l-besthis.anf-best-dat = from-date
      NO-LOCK, 
      FIRST l-artikel WHERE l-artikel.artnr = l-besthis.artnr 
      AND l-artikel.endkum GE from-main 
      AND l-artikel.endkum LE to-main NO-LOCK, 
      FIRST l-untergrup WHERE l-untergrup.zwkum = l-artikel.zwkum NO-LOCK:

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
      FIND FIRST l-oh WHERE l-oh.lager-nr = 0 AND l-oh.artnr = l-besthis.artnr
          /**/AND l-oh.anf-best-dat = from-date NO-LOCK. 
      qty = l-besthis.anz-anf-best + l-besthis.anz-eingang - l-besthis.anz-ausgang. 
      qty0 = l-oh.anz-anf-best + l-oh.anz-eingang - l-oh.anz-ausgang. 
      val0 = l-oh.val-anf-best + l-oh.wert-eingang - l-oh.wert-ausgang. 
      IF qty0 NE 0 THEN 
        art-bestand.actval  = art-bestand.actval + (qty / qty0) * val0. 

      art-bestand.prevval = art-bestand.prevval + l-besthis.val-anf-best. 
      prevval = prevval + l-besthis.val-anf-best. 


      FOR EACH l-ophis WHERE l-ophis.datum GE from-date 
          AND l-ophis.datum LE to-date 
          AND l-ophis.artnr = l-artikel.artnr AND l-ophis.op-art LE 2 
          AND l-ophis.lager-nr = lager-no 
          AND NOT (l-ophis.fibukonto MATCHES "*CANCELLED*") /* Add by Michael @ 07/12/2018 for not include cancelled receiving */ NO-LOCK :
          IF l-ophis.op-art = 1 THEN 
          DO: 
            inval = inval + l-ophis.warenwert. 
            art-bestand.inval = art-bestand.inval + l-ophis.warenwert. 
          END. 
          ELSE 
          DO: 
            inval = inval + l-ophis.anzahl * l-artikel.vk-preis. 
            art-bestand.inval = art-bestand.inval 
              + l-ophis.anzahl * l-artikel.vk-preis. 
          END. 
      END. 

      FOR EACH l-ophis WHERE l-ophis.datum GE from-date 
          AND l-ophis.datum LE to-date 
          AND l-ophis.artnr = l-artikel.artnr AND l-ophis.op-art GE 3 
          AND l-ophis.op-art LE 4 AND l-ophis.lager-nr EQ lager-no 
          AND NOT (l-ophis.fibukonto MATCHES "*CANCELLED*") /* Add by Michael @ 07/12/2018 for not include cancelled receiving */
          NO-LOCK :
          IF l-ophis.op-art = 3 THEN 
          DO: 
            outval = outval + l-ophis.warenwert. 
            art-bestand.outval = art-bestand.outval + l-ophis.warenwert. 
          END. 
          ELSE 
          DO: 
            outval = outval + l-ophis.anzahl * l-artikel.vk-preis. 
            art-bestand.outval = art-bestand.outval 
              + l-ophis.anzahl * l-artikel.vk-preis. 
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
      /*FD Comment Oct 06, 2020 => Can be minus value at column InitOH Adjust
      art-bestand.adjust = art-bestand.actval - (art-bestand.prevval 
        + art-bestand.inval - art-bestand.outval). 
      */
       art-bestand.adjust = (art-bestand.prevval + art-bestand.inval - art-bestand.outval) 
          - art-bestand.actval.
      actval = actval + art-bestand.actval. 
    END. 
  END. 
 
  create art-bestand. 
  art-bestand.bezeich = "                   T O T A L". 
  art-bestand.prevval = prevval. 
  art-bestand.inval = inval. 
  art-bestand.outval = outval. 
  art-bestand.actval = actval. 
  /*art-bestand.adjust = actval - (prevval + inval - outval).*/
  art-bestand.adjust = (prevval + inval - outval) - actval.
  art-bestand.nr = 999.
END. 
