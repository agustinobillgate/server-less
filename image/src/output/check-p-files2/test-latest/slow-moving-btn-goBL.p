DEFINE TEMP-TABLE s-list 
  FIELD artnr       AS INTEGER FORMAT "9999999" LABEL "ArtNo" 
  FIELD name        AS CHAR FORMAT "x(36)" LABEL "Name" 
  FIELD min-oh      AS DECIMAL FORMAT " >>>,>>9.99" LABEL "Min-Onhand" 
  FIELD curr-oh     AS DECIMAL FORMAT "->>>,>>9.99" LABEL "Curr-Onhand" 
  FIELD avrgprice   AS DECIMAL FORMAT ">>>,>>>,>>9.99" LABEL "Avrg-Price" INITIAL 0 
  FIELD ek-aktuell  AS DECIMAL FORMAT ">>>,>>>,>>9.99" LABEL "Actual-Price" INITIAL 0 
  FIELD datum       AS DATE LABEL "Last-Pchase". 

DEF INPUT  PARAMETER storeNo    AS INT.
DEF INPUT  PARAMETER main-grp   AS INT.
DEF INPUT  PARAMETER tage       AS INT.
DEF INPUT  PARAMETER show-price AS LOGICAL.
DEF OUTPUT PARAMETER TABLE FOR s-list.

IF storeNo = 0 THEN RUN create-list. 
ELSE RUN create-list1.

PROCEDURE create-list1: 
DEFINE VARIABLE n1 AS INTEGER. 
DEFINE VARIABLE n2 AS INTEGER. 
DEFINE VARIABLE curr-best AS DECIMAL FORMAT "->,>>9.999". 
DEFINE VARIABLE transdate AS DATE. 
  n1 = main-grp * 1000000. 
  n2 = (main-grp + 1) * 1000000 - 1. 
  FIND FIRST htparam WHERE paramnr = 110 NO-LOCK. 
  transdate = htparam.fdate. 
  
  FOR EACH s-list: 
    DELETE s-list. 
  END. 
  
  FOR EACH l-artikel WHERE l-artikel.artnr GE n1 AND l-artikel.artnr LE n2 
    NO-LOCK BY l-artikel.artnr: 
    curr-best = 0. 
    FIND FIRST l-bestand WHERE l-bestand.artnr = l-artikel.artnr 
    AND l-bestand.lager-nr = storeNo NO-LOCK NO-ERROR. 
    IF AVAILABLE l-bestand THEN curr-best = l-bestand.anz-anf-best 
      + l-bestand.anz-eingang - l-bestand.anz-ausgang. 
    IF curr-best GT 0 THEN 
    DO: 
      FIND FIRST l-op WHERE l-op.op-art = 3 AND l-op.loeschflag LE 1 
        AND l-op.artnr = l-artikel.artnr 
        AND l-op.lager-nr = storeNo NO-LOCK NO-ERROR. 
      IF NOT AVAILABLE l-op THEN
      FIND FIRST l-op WHERE l-op.op-art = 1 AND l-op.loeschflag LE 1 
        AND l-op.artnr = l-artikel.artnr 
        AND l-op.lager-nr = storeNo NO-LOCK NO-ERROR. 
      IF NOT AVAILABLE l-op THEN 
      DO: 
        FIND FIRST l-ophis WHERE l-ophis.artnr = l-artikel.artnr 
          AND l-ophis.op-art = 3 AND l-ophis.datum GE (transdate - tage) 
          AND l-ophis.lager-nr = storeNo NO-LOCK NO-ERROR. 
        IF NOT AVAILABLE l-ophis THEN 
        FIND FIRST l-ophis WHERE l-ophis.artnr = l-artikel.artnr 
          AND l-ophis.op-art = 1 AND l-ophis.datum GE (transdate - tage) 
          AND l-ophis.lager-nr = storeNo NO-LOCK NO-ERROR. 
        IF NOT AVAILABLE l-ophis THEN 
        DO: 
          /*MTASSIGN
            curr-dept = l-artikel.artnr
            curr-bezeich = l-artikel.bezeich. 
          DISP curr-dept curr-bezeich WITH FRAME frame2.*/
          
          CREATE s-list. 
          ASSIGN
            s-list.artnr = l-artikel.artnr
            s-list.name = l-artikel.bezeich 
            s-list.min-oh = l-artikel.min-best 
            s-list.curr-oh = curr-best
          . 
          IF show-price THEN 
          DO: 
            s-list.avrgprice = l-artikel.vk-preis. 
            s-list.ek-aktuell = l-artikel.ek-aktuell. 
          END. 
          IF l-artikel.lieferfrist GT 0 THEN 
          DO: 
            FIND FIRST l-pprice WHERE l-pprice.artnr = l-artikel.artnr 
              AND l-pprice.counter = l-artikel.lieferfrist USE-INDEX 
              counter_ix NO-LOCK NO-ERROR. 
            IF AVAILABLE l-pprice THEN s-list.datum = l-pprice.bestelldatum. 
          END. 
        END. 
      END. 
    END. 
  END. 
  /*MTHIDE FRAME frame2 NO-PAUSE.*/
END. 
 
PROCEDURE create-list: 
DEFINE VARIABLE n1 AS INTEGER. 
DEFINE VARIABLE n2 AS INTEGER. 
DEFINE VARIABLE curr-best AS DECIMAL FORMAT "->,>>9.999". 
DEFINE VARIABLE transdate AS DATE. 
  n1 = main-grp * 1000000. 
  n2 = (main-grp + 1) * 1000000 - 1. 
  FIND FIRST htparam WHERE paramnr = 110 NO-LOCK. 
  transdate = htparam.fdate. 
  
  FOR EACH s-list: 
    DELETE s-list. 
  END. 
  
  FOR EACH l-artikel WHERE l-artikel.artnr GE n1 AND l-artikel.artnr LE n2 
    NO-LOCK BY l-artikel.artnr: 
    curr-best = 0. 
    FIND FIRST l-bestand WHERE l-bestand.artnr = l-artikel.artnr 
    AND l-bestand.lager-nr = 0 NO-LOCK NO-ERROR. 
    IF AVAILABLE l-bestand THEN curr-best = l-bestand.anz-anf-best 
      + l-bestand.anz-eingang - l-bestand.anz-ausgang. 
    IF curr-best GT 0 THEN 
    DO: 
      FIND FIRST l-op WHERE l-op.op-art = 3 AND l-op.loeschflag LE 1 
        AND l-op.artnr = l-artikel.artnr NO-LOCK NO-ERROR. 
      IF NOT AVAILABLE l-op THEN
      FIND FIRST l-op WHERE l-op.op-art = 1 AND l-op.loeschflag LE 1 
        AND l-op.artnr = l-artikel.artnr NO-LOCK NO-ERROR. 
      IF NOT AVAILABLE l-op THEN 
      DO: 
        FIND FIRST l-ophis WHERE l-ophis.artnr = l-artikel.artnr 
          AND l-ophis.op-art = 3 AND l-ophis.datum GE (transdate - tage) 
          NO-LOCK NO-ERROR. 
        IF NOT AVAILABLE l-ophis THEN 
        FIND FIRST l-ophis WHERE l-ophis.artnr = l-artikel.artnr 
          AND l-ophis.op-art = 1 AND l-ophis.datum GE (transdate - tage) 
          NO-LOCK NO-ERROR. 
        IF NOT AVAILABLE l-ophis THEN 
        DO: 
          /*MTASSIGN
            curr-dept = l-artikel.artnr
            curr-bezeich = l-artikel.bezeich. 
          DISP curr-dept curr-bezeich WITH FRAME frame2.*/
          
          CREATE s-list. 
          ASSIGN
            s-list.artnr = l-artikel.artnr
            s-list.name = l-artikel.bezeich 
            s-list.min-oh = l-artikel.min-best 
            s-list.curr-oh = curr-best
          . 
          IF show-price THEN 
          DO: 
            s-list.avrgprice = l-artikel.vk-preis. 
            s-list.ek-aktuell = l-artikel.ek-aktuell. 
          END. 
          IF l-artikel.lieferfrist GT 0 THEN 
          DO: 
            FIND FIRST l-pprice WHERE l-pprice.artnr = l-artikel.artnr 
              AND l-pprice.counter = l-artikel.lieferfrist USE-INDEX 
              counter_ix NO-LOCK NO-ERROR. 
            IF AVAILABLE l-pprice THEN s-list.datum = l-pprice.bestelldatum. 
          END. 
        END. 
      END. 
    END. 
  END. 
  /*MTHIDE FRAME frame2 NO-PAUSE.*/
END. 

