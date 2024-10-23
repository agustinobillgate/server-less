
DEF INPUT  PARAMETER pvILanguage            AS INTEGER NO-UNDO.
DEF INPUT  PARAMETER cancel-reason          AS CHAR.
DEF INPUT  PARAMETER str-list-l-recid       AS INT.
DEF INPUT  PARAMETER str-list-billdate      AS DATE.
DEF INPUT  PARAMETER str-list-qty           AS DECIMAL.
DEF INPUT  PARAMETER bediener-nr            AS INT.
DEF INPUT  PARAMETER bediener-username      AS CHAR.
DEF INPUT  PARAMETER userinit               AS CHAR.
DEF OUTPUT PARAMETER docu-nr                AS INT INIT 0 NO-UNDO.
DEF OUTPUT PARAMETER msg-str                AS CHAR INIT "" NO-UNDO.

{supertransBL.i} 
DEF VAR lvCAREA AS CHAR INITIAL "supply-inlist".
DEF VAR avrg-price      AS DECIMAL   NO-UNDO INIT ?.
DEF VAR direct-issue    AS LOGICAL   NO-UNDO. 
DEF VAR from-date       AS DATE      NO-UNDO.
DEF VAR start-date      AS DATE      NO-UNDO.
DEF VAR end-date        AS DATE      NO-UNDO.
/*ITA 300615*/
DEF VAR t-amount        AS DECIMAL   NO-UNDO INIT 0.

FIND FIRST l-op WHERE RECID(l-op) = str-list-l-recid.
FIND FIRST l-artikel WHERE l-artikel.artnr = l-op.artnr NO-LOCK.
ASSIGN  
  direct-issue     = l-op.flag 
  l-op.loeschflag  = 2 
  l-op.stornogrund = bediener-username + ": " + STRING(TODAY) 
      + "-" + STRING(TIME,"HH:MM:SS") + ";Reason:" + 
      cancel-reason. 
FIND CURRENT l-op NO-LOCK. 
ASSIGN
    from-date  = str-list-billdate
    start-date = DATE(MONTH(from-date), 1, YEAR(from-date)) 
    end-date   = start-date + 35
    end-date   = DATE(MONTH(end-date), 1, YEAR(end-date)) - 1
.

RUN update-it.
IF NOT direct-issue THEN
  RUN reorg-avrg-price(l-op.artnr, str-list-billdate).

PROCEDURE update-it: 
DEFINE VARIABLE f-endkum        AS INTEGER. 
DEFINE VARIABLE b-endkum        AS INTEGER. 
DEFINE VARIABLE m-endkum        AS INTEGER. 
DEFINE VARIABLE billdate        AS DATE. 
DEFINE VARIABLE fb-closedate    AS DATE. 
DEFINE VARIABLE m-closedate     AS DATE. 
DEFINE VARIABLE tot-anz         AS DECIMAL NO-UNDO INIT 0. 
DEFINE VARIABLE tot-wert        AS DECIMAL. 
DEFINE VARIABLE curr-pos        AS INTEGER. 
DEFINE VARIABLE answer          AS LOGICAL INITIAL YES NO-UNDO. 
DEFINE VARIABLE tot-vat         AS DECIMAL NO-UNDO.

DEFINE BUFFER l-order1 FOR l-order. 
DEFINE BUFFER l-op1    FOR l-op. 
DEFINE BUFFER l-opbuff FOR l-op. 
 
  FIND FIRST htparam WHERE paramnr = 257 NO-LOCK. 
  f-endkum = htparam.finteger.               /* Rulita 211024 | Fixing for serverless */  
  FIND FIRST htparam WHERE paramnr = 258 NO-LOCK. 
  b-endkum = htparam.finteger.               /* Rulita 211024 | Fixing for serverless */  
  FIND FIRST htparam WHERE paramnr = 268 NO-LOCK. 
  m-endkum = htparam.finteger.               /* Rulita 211024 | Fixing for serverless */  
  FIND FIRST htparam WHERE paramnr = 224 NO-LOCK. 
  fb-closedate = htparam.fdate. 
  FIND FIRST htparam WHERE paramnr = 221 NO-LOCK. 
  m-closedate = htparam.fdate. 
   
  FIND FIRST l-kredit WHERE l-kredit.lief-nr = l-op.lief-nr 
    AND l-kredit.name = l-op.docu-nr 
    AND l-kredit.lscheinnr = l-op.lscheinnr 
    AND l-kredit.opart LE 2 AND l-kredit.zahlkonto = 0 NO-LOCK NO-ERROR. 
  IF NOT AVAILABLE l-kredit THEN 
  FIND FIRST l-kredit WHERE l-kredit.lief-nr = l-op.lief-nr 
    AND l-kredit.lscheinnr = l-op.lscheinnr 
    AND l-kredit.rgdatum = l-op.datum
    AND l-kredit.opart LE 2 AND l-kredit.zahlkonto = 0 NO-LOCK NO-ERROR. 
  IF AVAILABLE l-kredit THEN 
  DO: 
    ASSIGN tot-vat = 0.
    FIND FIRST queasy WHERE queasy.KEY = 304 AND queasy.char1 = l-op.lscheinnr 
          AND queasy.number1 = l-op.artnr NO-LOCK NO-ERROR.
    IF AVAILABLE queasy THEN ASSIGN tot-vat = (l-op.warenwert * (queasy.deci1 / 100)).

    IF tot-vat NE 0 THEN DO:
        FIND CURRENT l-kredit EXCLUSIVE-LOCK.
        IF l-kredit.saldo = (l-op.warenwert + tot-vat)  THEN DO:
            DELETE l-kredit. 
            RELEASE l-kredit.
        END.
        ELSE 
        DO: 
          l-kredit.saldo = l-kredit.saldo - (l-op.warenwert + tot-vat). 
          l-kredit.netto = l-kredit.netto - (l-op.warenwert + tot-vat). 
          FIND CURRENT l-kredit NO-LOCK.
          RELEASE l-kredit.
        END. 
        ASSIGN t-amount = t-amount - (l-op.warenwert + tot-vat).
    END.
    ELSE DO:
        FIND CURRENT l-kredit EXCLUSIVE-LOCK.
        IF l-kredit.saldo = l-op.warenwert THEN DO:
            DELETE l-kredit. 
            RELEASE l-kredit.
        END.
        ELSE 
        DO: 
          l-kredit.saldo = l-kredit.saldo - l-op.warenwert. 
          l-kredit.netto = l-kredit.netto - l-op.warenwert. 
          FIND CURRENT l-kredit NO-LOCK.
          RELEASE l-kredit.
        END. 
        ASSIGN t-amount = t-amount - l-op.warenwert.
    END.
    RUN update-ap. /*ITA 300615*/
  END. 
  
  IF (SUBSTR(l-op.docu-nr,1,1) = "P") THEN
  DO: 
    FIND FIRST l-order WHERE l-order.lief-nr = l-op.lief-nr 
      AND l-order.docu-nr = l-op.docu-nr 
      AND l-order.artnr = l-op.artnr 
      AND l-order.einzelpreis = l-op.einzelpreis 
/*    AND l-order.geliefert = (str-list.qty / l-order.txtnr) */
      EXCLUSIVE-LOCK NO-ERROR. 
    IF NOT AVAILABLE l-order THEN 
    DO: 
      IF str-list-qty > 0 THEN 
      FIND FIRST l-order WHERE l-order.lief-nr = l-op.lief-nr 
        AND l-order.docu-nr = l-op.docu-nr 
        AND l-order.artnr = l-op.artnr 
        AND l-order.einzelpreis = l-op.einzelpreis 
        AND l-order.geliefert > (str-list-qty / l-order.txtnr) 
        EXCLUSIVE-LOCK NO-ERROR. 
      ELSE 
      FIND FIRST l-order WHERE l-order.lief-nr = l-op.lief-nr 
        AND l-order.docu-nr = l-op.docu-nr 
        AND l-order.artnr = l-op.artnr 
        AND l-order.einzelpreis = l-op.einzelpreis
        AND l-order.geliefert > (str-list-qty / l-order.txtnr) 
        EXCLUSIVE-LOCK NO-ERROR. 
        
      /*ITA*/
      IF NOT AVAILABLE l-order THEN DO:
          FIND FIRST l-order WHERE l-order.lief-nr = l-op.lief-nr 
                AND l-order.docu-nr = l-op.docu-nr 
                AND l-order.artnr = l-op.artnr EXCLUSIVE-LOCK NO-ERROR. 
      END.  /*end*/
    END. 
    
    IF AVAILABLE l-order THEN 
    DO: 
      l-order.geliefert = l-order.geliefert - str-list-qty / l-order.txtnr. 
      l-order.rechnungswert = l-order.rechnungswert - l-op.warenwert. 
      FIND CURRENT l-order NO-LOCK. 
      FIND FIRST l-order1 WHERE l-order1.docu-nr = l-order.docu-nr 
        AND l-order1.pos = 0 EXCLUSIVE-LOCK. 
      l-order1.rechnungspreis = l-order1.rechnungspreis - l-op.warenwert. 
      l-order1.rechnungswert = l-order1.rechnungswert - l-op.warenwert. 
      FIND CURRENT l-order1 NO-LOCK. 
    END. 
  END. 
 
  IF NOT direct-issue THEN 
  DO: 
    IF ((l-artikel.endkum = f-endkum OR l-artikel.endkum = b-endkum) 
      AND (str-list-billdate LE fb-closedate)) 
    OR ((l-artikel.endkum GE m-endkum) AND (str-list-billdate LE m-closedate)) THEN 
    DO: 
/* UPDATE average price  */ 
      FIND FIRST l-bestand WHERE l-bestand.artnr = l-op.artnr
          AND l-bestand.lager-nr = 0 NO-LOCK NO-ERROR.
      IF AVAILABLE l-bestand THEN
      ASSIGN
          tot-anz  = l-bestand.anz-anf-best
          tot-wert = l-bestand.val-anf-best
      .
      FOR EACH l-opbuff WHERE l-opbuff.artnr = l-op.artnr
          AND l-opbuff.op-art = 1
          AND l-opbuff.datum LE end-date
          AND l-opbuff.loeschflag LE 1 NO-LOCK:
          ASSIGN
              tot-anz  = tot-anz + l-opbuff.anzahl
              tot-wert = tot-wert + l-opbuff.warenwert
          .
      END.
      IF tot-anz NE 0 THEN avrg-price = tot-wert / tot-anz.
      ELSE 
      DO:  
        IF AVAILABLE l-bestand AND l-bestand.anz-anf-best NE 0 THEN 
            avrg-price = l-bestand.val-anf-best / l-bestand.anz-anf-best.
        ELSE avrg-price = l-artikel.vk-preis.
      END.

/* UPDATE average price */ 
      IF avrg-price NE l-artikel.vk-preis THEN 
      DO: 
        FIND CURRENT l-artikel EXCLUSIVE-LOCK. 
        l-artikel.vk-preis = avrg-price. 
        FIND CURRENT l-artikel NO-LOCK. 
      END. 
    END. 
  END. 
  ELSE IF direct-issue THEN 
  DO: 
/* UPDATE stock onhand  */ 
    FIND FIRST l-bestand WHERE l-bestand.lager-nr = 0 AND 
      l-bestand.artnr = l-artikel.artnr EXCLUSIVE-LOCK NO-ERROR. 
    IF AVAILABLE l-bestand THEN 
    DO:
      ASSIGN
        l-bestand.anz-eingang  = l-bestand.anz-eingang - str-list-qty 
        l-bestand.wert-eingang = l-bestand.wert-eingang - l-op.warenwert 
        l-bestand.anz-ausgang  = l-bestand.anz-ausgang - str-list-qty 
        l-bestand.wert-ausgang = l-bestand.wert-ausgang - l-op.warenwert
      . 
      FIND CURRENT l-bestand NO-LOCK. 
    END. 
    FIND FIRST l-bestand WHERE l-bestand.lager-nr = l-op.lager-nr AND 
      l-bestand.artnr = l-artikel.artnr EXCLUSIVE-LOCK NO-ERROR. 
    IF AVAILABLE l-bestand THEN 
    DO: 
      ASSIGN
        l-bestand.anz-eingang  = l-bestand.anz-eingang - str-list-qty 
        l-bestand.wert-eingang = l-bestand.wert-eingang - l-op.warenwert 
        l-bestand.anz-ausgang  = l-bestand.anz-ausgang - str-list-qty 
        l-bestand.wert-ausgang = l-bestand.wert-ausgang - l-op.warenwert
      . 
      FIND CURRENT l-bestand NO-LOCK. 
    END. 
    FIND FIRST l-op1 WHERE l-op1.artnr = l-op.artnr 
      AND l-op1.op-art = 3 AND l-op1.lief-nr = l-op.lief-nr 
      AND l-op1.lscheinnr = l-op.lscheinnr 
      AND l-op1.herkunftflag = 2 AND l-op1.lager-nr = l-op.lager-nr 
      EXCLUSIVE-LOCK NO-ERROR. 
    IF AVAILABLE l-op1 THEN 
    DO:
      ASSIGN
        l-op1.loeschflag = 2 
        l-op1.betriebsnr = bediener-nr
      .
      FIND CURRENT l-op1 NO-LOCK. 
    END. 

  END. 
  
/* UPDATE supplier turnover */ 
  FIND FIRST  l-liefumsatz WHERE l-liefumsatz.lief-nr = l-op.lief-nr 
    AND l-liefumsatz.datum = str-list-billdate EXCLUSIVE-LOCK NO-ERROR. 
  IF AVAILABLE l-liefumsatz THEN 
    l-liefumsatz.gesamtumsatz = l-liefumsatz.gesamtumsatz - l-op.warenwert.

  
  FIND FIRST l-order WHERE l-order.docu-nr = l-op.docu-nr 
      AND l-order.lief-nr = l-op.lief-nr 
      AND l-order.pos EQ 0 AND l-order.loeschflag = 1 NO-LOCK NO-ERROR. 
  IF AVAILABLE l-order THEN 
  DO: 
      docu-nr = recid(l-op).
      msg-str = msg-str + CHR(2) + "&Q"
              + translateExtended ("Purchase Order closed; re-open it?",lvCAREA,"").
  END. 
  
  FIND FIRST l-pprice WHERE l-pprice.artnr = l-op.artnr 
      AND l-pprice.bestelldatum = l-op.datum 
      AND l-pprice.anzahl = l-op.anzahl 
      AND l-pprice.einzelpreis = l-op.einzelpreis 
      AND l-pprice.lief-nr = l-op.lief-nr 
      AND l-pprice.docu-nr = l-op.docu-nr EXCLUSIVE-LOCK NO-ERROR. 
  IF AVAILABLE l-pprice THEN 
  DO: 
    DELETE l-pprice. 
    RELEASE l-pprice. 
  END.

  /*ITA*/
  IF l-op.loeschflag = 2 THEN DO:
      FIND FIRST dml-art WHERE dml-art.artnr = l-op.artnr AND dml-art.datum = l-op.datum
          AND dml-art.anzahl GT 0 EXCLUSIVE-LOCK NO-ERROR.
      IF AVAILABLE dml-art THEN DO:
          ASSIGN dml-art.geliefert = 0.
          FIND CURRENT dml-art NO-LOCK.
      END.
      ELSE IF NOT AVAILABLE dml-art THEN DO:
          FIND FIRST dml-artdep WHERE dml-artdep.artnr = l-op.artnr AND dml-artdep.datum = l-op.datum
          AND dml-artdep.anzahl GT 0 EXCLUSIVE-LOCK NO-ERROR.
          IF AVAILABLE dml-artdep THEN DO:
              ASSIGN dml-artdep.geliefert = 0.
              FIND CURRENT dml-artdep NO-LOCK.
          END.
      END.
  END.
  /*end*/
 
END.

PROCEDURE reorg-avrg-price:
DEF INPUT PARAMETER curr-artnr AS INTEGER NO-UNDO.
DEF INPUT PARAMETER from-date  AS DATE    NO-UNDO.

DEF VAR t-anz      AS DECIMAL   NO-UNDO.
DEF VAR t-wert     AS DECIMAL   NO-UNDO.

DEF BUFFER lbuff       FOR l-bestand.
DEFINE BUFFER l-opbuff FOR l-op. 

    FIND FIRST l-bestand WHERE l-bestand.anf-best-dat GE start-date 
      AND l-bestand.anf-best-dat LE end-date 
      AND l-bestand.artnr = curr-artnr
      AND l-bestand.lager-nr = l-op.lager-nr NO-ERROR.
    IF AVAILABLE l-bestand THEN
    ASSIGN
        l-bestand.anz-eingang  = 0
        l-bestand.anz-ausgang  = 0
        l-bestand.wert-eingang = 0
        l-bestand.wert-ausgang = 0
    .

    FIND FIRST lbuff WHERE lbuff.anf-best-dat GE start-date 
      AND lbuff.anf-best-dat LE end-date 
      AND lbuff.artnr = curr-artnr
      AND lbuff.lager-nr = 0 NO-ERROR.

    IF AVAILABLE lbuff THEN
    ASSIGN
        lbuff.anz-eingang      = 0
        lbuff.anz-ausgang      = 0
        lbuff.wert-eingang     = 0
        lbuff.wert-ausgang     = 0
    .

    /* fixing outgoing l-op price and amount */
    FOR EACH l-opbuff WHERE l-opbuff.artnr = curr-artnr
        AND l-opbuff.datum GE from-date 
        AND (l-opbuff.op-art GE 2 AND l-opbuff.op-art LE 14) 
        AND l-opbuff.loeschflag LE 1:
        ASSIGN
            l-opbuff.einzelpreis = avrg-price
            l-opbuff.warenwert = avrg-price * l-opbuff.anzahl
        .
    END.
    
    /* fixing l-bestand receiving and outgoing amount */
    FOR EACH l-opbuff WHERE l-opbuff.artnr = curr-artnr
        AND l-opbuff.datum GE start-date
        AND l-opbuff.datum LE end-date
        AND (l-opbuff.op-art GE 1 AND l-opbuff.op-art LE 4) 
        AND l-opbuff.loeschflag LE 1: 
        IF l-opbuff.op-art LE 2 THEN
        DO:
          IF AVAILABLE lbuff THEN
          ASSIGN
            lbuff.anz-eingang      = lbuff.anz-eingang  + l-opbuff.anzahl
            lbuff.wert-eingang     = lbuff.wert-eingang + l-opbuff.warenwert
          .

          IF AVAILABLE l-bestand THEN
          IF l-opbuff.lager-nr = l-bestand.lager-nr THEN
          ASSIGN
            l-bestand.anz-eingang  = l-bestand.anz-eingang  + l-opbuff.anzahl
            l-bestand.wert-eingang = l-bestand.wert-eingang + l-opbuff.warenwert
          .
        END.
        ELSE
        DO:
          IF AVAILABLE lbuff THEN
          ASSIGN
              lbuff.anz-ausgang      = lbuff.anz-ausgang  + l-opbuff.anzahl
              lbuff.wert-ausgang     = lbuff.wert-ausgang + l-opbuff.warenwert
          .

          IF AVAILABLE l-bestand THEN
          IF l-opbuff.lager-nr = l-bestand.lager-nr THEN
          ASSIGN
              l-bestand.anz-ausgang  = l-bestand.anz-ausgang  + l-opbuff.anzahl
              l-bestand.wert-ausgang = l-bestand.wert-ausgang + l-opbuff.warenwert
          .
        END.
    END.
    FIND CURRENT lbuff NO-LOCK NO-ERROR.
    FIND CURRENT l-bestand NO-LOCK NO-ERROR.
END.

/*ITA 300715*/
PROCEDURE update-ap:
    DEFINE VARIABLE flogic   AS LOGICAL NO-UNDO.
    DEFINE VARIABLE billdate AS DATE    NO-UNDO.

    FIND FIRST htparam WHERE paramnr = 1016 NO-LOCK NO-ERROR. /* ap license */ 
    ASSIGN flogic = htparam.flogical.

    FIND FIRST htparam WHERE paramnr = 474 NO-LOCK NO-ERROR. 
    ASSIGN billdate = htparam.fdate. 

    IF flogic THEN DO:
      CREATE  ap-journal. 
      ASSIGN  ap-journal.lief-nr    = l-op.lief-nr 
              ap-journal.docu-nr    = l-op.docu-nr 
              ap-journal.lscheinnr  = l-op.lscheinnr 
              ap-journal.rgdatum    = /*billdate*/ l-op.datum
              ap-journal.saldo      = t-amount 
              ap-journal.netto      = t-amount 
              ap-journal.userinit   = userinit 
              ap-journal.zeit       = TIME 
              ap-journal.bemerk     = "Cancel Receiving Inventory". 
    END.
END.
/*end*/
