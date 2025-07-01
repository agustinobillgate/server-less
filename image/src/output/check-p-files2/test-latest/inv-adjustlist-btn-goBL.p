DEFINE TEMP-TABLE c-list 
  FIELD artnr       LIKE l-artikel.artnr 
  FIELD bezeich     AS CHAR FORMAT "x(36)" COLUMN-LABEL "Description" 
  FIELD munit       AS CHAR FORMAT "x(3)" COLUMN-LABEL "Unit" 
  FIELD inhalt      AS DECIMAL FORMAT ">>>9.99" COLUMN-LABEL "Content" 
  FIELD zwkum       AS INTEGER 
  FIELD endkum      AS INTEGER 
  FIELD qty         AS DECIMAL  FORMAT "->>>,>>9.999" LABEL "   Curr-Qty" 
  FIELD qty1        AS DECIMAL FORMAT "->>>,>>9.999" LABEL " Actual-Qty" 
  FIELD amount      AS DECIMAL  FORMAT "->>,>>>,>>>,>>9.99" LABEL " Amount"
  FIELD avrg-amount AS DECIMAL  FORMAT "->>,>>>,>>>,>>9.99" LABEL "Average Amount"
  FIELD fibukonto   LIKE gl-acct.fibukonto INITIAL "0000000000" 
/* DO NOT change the INITIAL value 0000000000, used BY hcost-anal.p */ 
  FIELD cost-center AS CHAR FORMAT "x(50)" LABEL "Cost Allocation"
  FIELD variance    AS DECIMAL  FORMAT "->>>,>>9.999" LABEL "Variance Qty"
.

DEFINE INPUT PARAMETER sorttype AS INT.
DEFINE INPUT PARAMETER curr-lager AS INT.
DEFINE INPUT PARAMETER from-grp AS INT.
DEFINE INPUT PARAMETER transdate AS DATE.
DEFINE OUTPUT PARAMETER tot-amount AS DECIMAL.
DEFINE OUTPUT PARAMETER tot-avrg-amount AS DECIMAL.
DEFINE OUTPUT PARAMETER TABLE FOR c-list.

RUN journal-list1.

PROCEDURE journal-list1: 
  FOR EACH c-list: 
    delete c-list. 
  END. 
  /*IF sorttype LE 2 THEN 
  FOR EACH l-op WHERE l-op.lager-nr = curr-lager AND l-op.op-art = 3 
      AND l-op.datum LE transdate 
      AND (SUBSTR(l-op.lscheinnr,1,3) = "INV" OR SUBSTR(l-op.lscheinnr,1,3) = "SRD") 
      AND l-op.loeschflag LE 1 NO-LOCK, 
    FIRST l-artikel WHERE l-artikel.artnr = l-op.artnr 
    AND l-artikel.endkum = from-grp NO-LOCK,
    FIRST l-untergrup WHERE l-untergrup.zwkum = l-artikel.zwkum
    BY l-artikel.bezeich BY l-op.datum BY l-op.lscheinnr: 

    FIND FIRST c-list WHERE c-list.artnr = 0 
      AND c-list.endkum = l-artikel.endkum
      AND c-list.zwkum = l-artikel.zwkum NO-ERROR.
    IF NOT AVAILABLE c-list THEN
    DO:
      CREATE c-list.
      ASSIGN c-list.artnr     = 0
             c-list.fibukonto = ""
             c-list.endkum    = l-artikel.endkum
             c-list.zwkum     = l-artikel.zwkum
             c-list.bezeich   = l-untergrup.bezeich.
    END.
    
    CREATE c-list. 
    ASSIGN 
      c-list.artnr = l-artikel.artnr 
      c-list.bezeich = l-artikel.bezeich 
      c-list.munit = l-artikel.masseinheit 
      c-list.inhalt = l-artikel.inhalt 
      c-list.zwkum = l-artikel.zwkum 
      c-list.endkum = l-artikel.endkum 
      c-list.qty = l-op.deci1[1] 
      c-list.qty1 = l-op.deci1[1] - l-op.anzahl 
      c-list.fibukonto = l-op.stornogrund 
      c-list.amount = l-op.warenwert
      c-list.avrg-amount = l-op.warenwert / l-op.anzahl
    . 
    tot-amount = tot-amount + l-op.warenwert.
    tot-avrg-amount = tot-avrg-amount + (l-op.warenwert / l-op.anzahl).
    FIND FIRST gl-acct WHERE gl-acct.fibukonto = c-list.fibukonto 
        NO-LOCK NO-ERROR. 
    IF AVAILABLE gl-acct THEN c-list.cost-center = gl-acct.bezeich. 
  END.*/ 
  IF sorttype EQ 1 THEN 
  FOR EACH l-op WHERE l-op.lager-nr = curr-lager AND l-op.op-art = 3 
      AND l-op.datum LE transdate 
      AND (SUBSTR(l-op.lscheinnr,1,3) = "INV" OR SUBSTR(l-op.lscheinnr,1,3) = "SRD") 
      AND l-op.loeschflag LE 1 NO-LOCK, 
    FIRST l-artikel WHERE l-artikel.artnr = l-op.artnr 
    AND l-artikel.endkum = from-grp NO-LOCK,
    FIRST l-untergrup WHERE l-untergrup.zwkum = l-artikel.zwkum
    BY l-artikel.artnr BY l-op.datum BY l-op.lscheinnr: 

    FIND FIRST c-list WHERE c-list.artnr = 0 
      AND c-list.endkum = l-artikel.endkum
      AND c-list.zwkum = l-artikel.zwkum NO-ERROR.
    IF NOT AVAILABLE c-list THEN
    DO:
      CREATE c-list.
      ASSIGN c-list.artnr     = 0
             c-list.fibukonto = ""
             c-list.endkum    = l-artikel.endkum
             c-list.zwkum     = l-artikel.zwkum
             c-list.bezeich   = l-untergrup.bezeich.
    END.
    
    CREATE c-list. 
    ASSIGN 
      c-list.artnr = l-artikel.artnr 
      c-list.bezeich = l-artikel.bezeich 
      c-list.munit = l-artikel.masseinheit 
      c-list.inhalt = l-artikel.inhalt 
      c-list.zwkum = l-artikel.zwkum 
      c-list.endkum = l-artikel.endkum 
      c-list.qty = l-op.deci1[1] 
      c-list.qty1 = l-op.deci1[1] - l-op.anzahl 
      c-list.fibukonto = l-op.stornogrund 
      c-list.amount = l-op.warenwert
      c-list.avrg-amount = l-op.warenwert / l-op.anzahl
      c-list.variance = c-list.qty - c-list.qty1            /*FD March 07, 2022*/
    . 
    tot-amount = tot-amount + l-op.warenwert.
    tot-avrg-amount = tot-avrg-amount + (l-op.warenwert / l-op.anzahl).
    FIND FIRST gl-acct WHERE gl-acct.fibukonto = c-list.fibukonto 
        NO-LOCK NO-ERROR. 
    IF AVAILABLE gl-acct THEN c-list.cost-center = gl-acct.bezeich. 
  END. 
  ELSE IF sorttype EQ 2 THEN 
  FOR EACH l-op WHERE l-op.lager-nr = curr-lager AND l-op.op-art = 3 
      AND l-op.datum LE transdate 
      AND (SUBSTR(l-op.lscheinnr,1,3) = "INV" OR SUBSTR(l-op.lscheinnr,1,3) = "SRD") 
      AND l-op.loeschflag LE 1 NO-LOCK, 
    FIRST l-artikel WHERE l-artikel.artnr = l-op.artnr 
    AND l-artikel.endkum = from-grp NO-LOCK,
    FIRST l-untergrup WHERE l-untergrup.zwkum = l-artikel.zwkum
    BY l-artikel.bezeich BY l-op.datum BY l-op.lscheinnr: 

    FIND FIRST c-list WHERE c-list.artnr = 0 
      AND c-list.endkum = l-artikel.endkum
      AND c-list.zwkum = l-artikel.zwkum NO-ERROR.
    IF NOT AVAILABLE c-list THEN
    DO:
      CREATE c-list.
      ASSIGN c-list.artnr     = 0
             c-list.fibukonto = ""
             c-list.endkum    = l-artikel.endkum
             c-list.zwkum     = l-artikel.zwkum
             c-list.bezeich   = l-untergrup.bezeich.
    END.
    
    CREATE c-list. 
    ASSIGN 
      c-list.artnr = l-artikel.artnr 
      c-list.bezeich = l-artikel.bezeich 
      c-list.munit = l-artikel.masseinheit 
      c-list.inhalt = l-artikel.inhalt 
      c-list.zwkum = l-artikel.zwkum 
      c-list.endkum = l-artikel.endkum 
      c-list.qty = l-op.deci1[1] 
      c-list.qty1 = l-op.deci1[1] - l-op.anzahl 
      c-list.fibukonto = l-op.stornogrund 
      c-list.amount = l-op.warenwert
      c-list.avrg-amount = l-op.warenwert / l-op.anzahl
      c-list.variance = c-list.qty - c-list.qty1            /*FD March 07, 2022*/
    . 

    tot-amount = tot-amount + l-op.warenwert.
    tot-avrg-amount = tot-avrg-amount + (l-op.warenwert / l-op.anzahl).
    FIND FIRST gl-acct WHERE gl-acct.fibukonto = c-list.fibukonto 
        NO-LOCK NO-ERROR. 
    IF AVAILABLE gl-acct THEN c-list.cost-center = gl-acct.bezeich. 
  END. 
  ELSE IF sorttype = 3 THEN 
  FOR EACH l-op WHERE l-op.lager-nr = curr-lager AND l-op.op-art = 3 
      AND l-op.datum LE transdate 
      AND (SUBSTR(l-op.lscheinnr,1,3) = "INV" OR SUBSTR(l-op.lscheinnr,1,3) = "SRD") 
      AND l-op.loeschflag LE 1 NO-LOCK, 
    FIRST l-artikel WHERE l-artikel.artnr = l-op.artnr 
    AND l-artikel.endkum = from-grp NO-LOCK,
    FIRST l-untergrup WHERE l-untergrup.zwkum = l-artikel.zwkum
    BY l-artikel.zwkum BY l-artikel.bezeich BY l-op.datum BY l-op.lscheinnr: 

    FIND FIRST c-list WHERE c-list.artnr = 0 
      AND c-list.endkum = l-artikel.endkum
      AND c-list.zwkum = l-artikel.zwkum NO-ERROR.
    IF NOT AVAILABLE c-list THEN
    DO:
      CREATE c-list.
      ASSIGN c-list.artnr     = 0
             c-list.fibukonto = ""
             c-list.endkum    = l-artikel.endkum
             c-list.zwkum     = l-artikel.zwkum
             c-list.bezeich   = l-untergrup.bezeich.
    END.

    create c-list. 
    ASSIGN 
      c-list.artnr = l-artikel.artnr 
      c-list.bezeich = l-artikel.bezeich 
      c-list.munit = l-artikel.masseinheit 
      c-list.inhalt = l-artikel.inhalt 
      c-list.zwkum = l-artikel.zwkum 
      c-list.endkum = l-artikel.endkum 
      c-list.qty = l-op.deci1[1] 
      c-list.qty1 = l-op.deci1[1] - l-op.anzahl 
      c-list.fibukonto = l-op.stornogrund 
      c-list.amount = l-op.warenwert
      c-list.avrg-amount = l-op.warenwert / l-op.anzahl
      c-list.variance = c-list.qty - c-list.qty1            /*FD March 07, 2022*/
    . 
    tot-amount = tot-amount + l-op.warenwert.
    tot-avrg-amount = tot-avrg-amount + (l-op.warenwert / l-op.anzahl).
    FIND FIRST gl-acct WHERE gl-acct.fibukonto = c-list.fibukonto 
        NO-LOCK NO-ERROR. 
    IF AVAILABLE gl-acct THEN c-list.cost-center = gl-acct.bezeich. 
  END.               
END. 

