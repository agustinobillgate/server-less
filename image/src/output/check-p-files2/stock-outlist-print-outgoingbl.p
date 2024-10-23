DEF TEMP-TABLE print-list
    FIELD datum     LIKE l-op.datum
    FIELD lager-nr  LIKE l-op.lager-nr
    FIELD artnr     LIKE l-op.artnr
    FIELD bezeich   LIKE l-art.bezeich
    FIELD anzahl    LIKE l-op.anzahl
    FIELD gl-bezeich LIKE gl-acct.bezeich
    FIELD preis     AS DECIMAL
    FIELD wert      AS DECIMAL.

DEF INPUT PARAMETER s-op-recid AS INT.
DEF INPUT PARAMETER from-grp   AS INT.
DEF INPUT PARAMETER show-price AS LOGICAL.
DEF OUTPUT PARAMETER tot-amount AS DECIMAL INIT 0.
DEF OUTPUT PARAMETER l-op1-lscheinnr AS CHAR.
DEF OUTPUT PARAMETER TABLE FOR print-list.
DEFINE buffer l-op1 FOR l-op. 

DEF VAR preis     AS DECIMAL INIT 0.
DEF VAR wert      AS DECIMAL INIT 0.

FIND FIRST l-op1 WHERE RECID(l-op1) = s-op-recid NO-LOCK. 
FIND FIRST l-ophdr WHERE l-ophdr.op-typ = "STT" 
    AND l-ophdr.lscheinnr = l-op1.lscheinnr 
    AND l-ophdr.fibukonto NE "" NO-LOCK. 

l-op1-lscheinnr = l-op1.lscheinnr.


IF from-grp = 0 THEN 
FOR EACH l-op WHERE l-op.datum EQ l-op1.datum 
    AND l-op.op-art = 3 AND l-op.lscheinnr = l-op1.lscheinnr 
    AND l-op.loeschflag LE 1 NO-LOCK, 
    FIRST l-art WHERE l-art.artnr = l-op.artnr NO-LOCK BY l-art.bezeich: 
 
    IF show-price THEN 
    DO: 
      preis = l-op.einzelpreis. 
      wert = l-op.warenwert. 
    END. 
 
    IF l-op.stornogrund NE "" THEN 
    DO: 
      FIND FIRST gl-acct WHERE gl-acct.fibukonto = l-op.stornogrund 
        NO-LOCK NO-ERROR. 
    END. 
    IF l-op.stornogrund = "" OR NOT AVAILABLE gl-acct THEN 
      FIND FIRST gl-acct WHERE gl-acct.fibukonto = l-ophdr.fibukonto 
        NO-LOCK NO-ERROR.

    CREATE print-list.
    ASSIGN
    print-list.datum     = l-op.datum
    print-list.lager-nr  = l-op.lager-nr
    print-list.artnr     = l-op.artnr
    print-list.bezeich   = l-art.bezeich
    print-list.anzahl    = l-op.anzahl
    print-list.preis     = preis
    print-list.wert      = wert.
    IF AVAILABLE gl-acct THEN print-list.gl-bezeich = gl-acct.bezeich.
    
    tot-amount = tot-amount + wert. 
END. 
ELSE 
FOR EACH l-op WHERE l-op.datum EQ l-op1.datum 
    AND l-op.op-art = 3 AND l-op.lscheinnr = l-op1.lscheinnr 
    AND l-op.loeschflag LE 1 NO-LOCK, 
    FIRST l-art WHERE l-art.artnr = l-op.artnr 
    AND l-art.endkum = from-grp NO-LOCK BY l-art.bezeich: 
 
    IF show-price THEN 
    DO: 
      preis = l-op.einzelpreis. 
      wert = l-op.warenwert. 
    END. 
 
    IF l-op.stornogrund NE "" THEN 
    DO: 
      FIND FIRST gl-acct WHERE gl-acct.fibukonto = l-op.stornogrund 
        NO-LOCK NO-ERROR. 
    END. 
    IF l-op.stornogrund = "" OR NOT AVAILABLE gl-acct THEN 
      FIND FIRST gl-acct WHERE gl-acct.fibukonto = l-ophdr.fibukonto 
        NO-LOCK NO-ERROR. 

    CREATE print-list.
    ASSIGN
    print-list.datum     = l-op.datum
    print-list.lager-nr  = l-op.lager-nr
    print-list.artnr     = l-op.artnr
    print-list.bezeich   = l-art.bezeich
    print-list.anzahl    = l-op.anzahl
    print-list.preis     = preis
    print-list.wert      = wert.
    IF AVAILABLE gl-acct THEN print-list.gl-bezeich = gl-acct.bezeich.

    tot-amount = tot-amount + wert. 
END. 
