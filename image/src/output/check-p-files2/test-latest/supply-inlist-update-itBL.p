/*FDL Stack Trace Lock Wait Timeout Le Eminance => Every Exclusive-Lock given release*/

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
DEFINE VARIABLE tot-receiving AS DECIMAL NO-UNDO.

DEFINE BUFFER blop FOR l-op.

FIND FIRST l-op WHERE RECID(l-op) EQ str-list-l-recid NO-LOCK NO-ERROR.
/*FIND FIRST l-artikel WHERE l-artikel.artnr EQ l-op.artnr NO-LOCK.*/ /*FDL Comment move above*/
FIND CURRENT l-op EXCLUSIVE-LOCK. 
ASSIGN  
  direct-issue     = l-op.flag 
  l-op.loeschflag  = 2 
  l-op.stornogrund = bediener-username + ": " + STRING(TODAY) 
      + "-" + STRING(TIME,"HH:MM:SS") + ";Reason:" + 
      cancel-reason. 
FIND CURRENT l-op NO-LOCK. 
FIND FIRST l-artikel WHERE l-artikel.artnr EQ l-op.artnr NO-LOCK.
ASSIGN
    from-date  = str-list-billdate
    start-date = DATE(MONTH(from-date), 1, YEAR(from-date)) 
    end-date   = start-date + 35
    end-date   = DATE(MONTH(end-date), 1, YEAR(end-date)) - 1
.

RUN update-it.
IF NOT direct-issue THEN
  RUN reorg-avrg-price(l-op.artnr, str-list-billdate).

RELEASE l-op.

/*ragung add validasi for close*/
FOR EACH queasy WHERE queasy.KEY = 328 
    AND (queasy.char2 EQ "Inv-Cek Reciving" 
         OR queasy.char2 EQ "Inv-Cek Reorg"
         OR queasy.char2 EQ "Inv-Cek Journal"):
    DELETE queasy.
END.

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
  DEFINE VARIABLE dml-no          AS INTEGER NO-UNDO.
  DEFINE VARIABLE dept-no         AS INTEGER NO-UNDO.

  DEFINE BUFFER l-order1 FOR l-order. 
  DEFINE BUFFER l-op1    FOR l-op. 
  DEFINE BUFFER l-opbuff FOR l-op. 
 
  FIND FIRST htparam WHERE paramnr EQ 257 NO-LOCK. 
  f-endkum = htparam.finteger.               /* Rulita 211024 | Fixing for serverless */  
  FIND FIRST htparam WHERE paramnr EQ 258 NO-LOCK. 
  b-endkum = htparam.finteger.               /* Rulita 211024 | Fixing for serverless */  
  FIND FIRST htparam WHERE paramnr EQ 268 NO-LOCK. 
  m-endkum = htparam.finteger.               /* Rulita 211024 | Fixing for serverless */  
  FIND FIRST htparam WHERE paramnr EQ 224 NO-LOCK. 
  fb-closedate = htparam.fdate. 
  FIND FIRST htparam WHERE paramnr EQ 221 NO-LOCK. 
  m-closedate = htparam.fdate. 
   
  FIND FIRST l-kredit WHERE l-kredit.lief-nr EQ l-op.lief-nr 
    AND l-kredit.name EQ l-op.docu-nr 
    AND l-kredit.lscheinnr EQ l-op.lscheinnr 
    AND l-kredit.opart LE 2 
    AND l-kredit.zahlkonto EQ 0 NO-LOCK NO-ERROR. 

  IF NOT AVAILABLE l-kredit THEN 
    FIND FIRST l-kredit WHERE l-kredit.lief-nr EQ l-op.lief-nr 
    AND l-kredit.lscheinnr EQ l-op.lscheinnr 
    AND l-kredit.rgdatum EQ l-op.datum
    AND l-kredit.opart LE 2 
    AND l-kredit.zahlkonto EQ 0 NO-LOCK NO-ERROR. 

  IF AVAILABLE l-kredit THEN 
  DO: 

    FIND CURRENT l-kredit EXCLUSIVE-LOCK.    
    DELETE l-kredit. 
    RELEASE l-kredit.

    FIND FIRST ap-journal WHERE ap-journal.lief-nr = l-op.lief-nr 
          AND ap-journal.docu-nr    = l-op.docu-nr 
          AND ap-journal.lscheinnr  = l-op.lscheinnr NO-LOCK NO-ERROR.
    IF AVAILABLE ap-journal THEN DO:
        FIND CURRENT ap-journal EXCLUSIVE-LOCK.
        DELETE ap-journal.
        RELEASE ap-journal.
    END.

    /*ASSIGN tot-vat = 0.
    FIND FIRST queasy WHERE queasy.KEY EQ 304 
      AND queasy.char1 EQ l-op.lscheinnr 
      AND queasy.number1 EQ l-op.artnr NO-LOCK NO-ERROR.

    IF AVAILABLE queasy THEN ASSIGN tot-vat = (l-op.warenwert * (queasy.deci1 / 100)).

    IF tot-vat NE 0 THEN DO:
        FIND CURRENT l-kredit EXCLUSIVE-LOCK.
        IF l-kredit.saldo EQ (l-op.warenwert + tot-vat) THEN 
        DO:
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
        IF l-kredit.saldo EQ l-op.warenwert THEN DO:
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
    RUN update-ap. /*ITA 300615*/*/
  END. 
  
  IF (SUBSTR(l-op.docu-nr,1,1) EQ "P") THEN
  DO: 
    FIND FIRST l-order WHERE l-order.lief-nr EQ l-op.lief-nr 
      AND l-order.docu-nr EQ l-op.docu-nr 
      AND l-order.artnr EQ l-op.artnr 
      AND l-order.einzelpreis EQ l-op.einzelpreis 
      /* AND l-order.geliefert = (str-list.qty / l-order.txtnr) */
      EXCLUSIVE-LOCK NO-ERROR. 

    IF NOT AVAILABLE l-order THEN 
    DO: 
      /* comment it because no difference by Oscar*/
      /* IF str-list-qty > 0 THEN 
        FIND FIRST l-order WHERE l-order.lief-nr = l-op.lief-nr 
          AND l-order.docu-nr = l-op.docu-nr 
          AND l-order.artnr = l-op.artnr 
          AND l-order.einzelpreis = l-op.einzelpreis 
          AND l-order.geliefert > (str-list.qty / l-order.txtnr)
          EXCLUSIVE-LOCK NO-ERROR. 
      ELSE 
        FIND FIRST l-order WHERE l-order.lief-nr = l-op.lief-nr 
          AND l-order.docu-nr = l-op.docu-nr 
          AND l-order.artnr = l-op.artnr 
          AND l-order.einzelpreis = l-op.einzelpreis
          AND l-order.geliefert > (str-list.qty / l-order.txtnr)
          EXCLUSIVE-LOCK NO-ERROR.  */
        
      FIND FIRST l-order WHERE l-order.lief-nr EQ l-op.lief-nr 
        AND l-order.docu-nr EQ l-op.docu-nr 
        AND l-order.artnr EQ l-op.artnr 
        AND l-order.einzelpreis EQ l-op.einzelpreis 
        AND l-order.geliefert GT str-list-qty /* Oscar (26/11/2024) - F0ADB1 - fix cancel receiving */
        EXCLUSIVE-LOCK NO-ERROR. 

      /*ITA*/
      IF NOT AVAILABLE l-order THEN 
      DO:
        FIND FIRST l-order WHERE l-order.lief-nr EQ l-op.lief-nr 
          AND l-order.docu-nr EQ l-op.docu-nr 
          AND l-order.artnr EQ l-op.artnr EXCLUSIVE-LOCK NO-ERROR. 
      END.  /*end*/
    END. 
    
    IF AVAILABLE l-order THEN 
    DO: 
      l-order.geliefert = l-order.geliefert - str-list-qty. /* Oscar (26/11/2024) - F0ADB1 - fix cancel receiving */
      l-order.rechnungswert = l-order.rechnungswert - l-op.warenwert. 

      FIND CURRENT l-order NO-LOCK. 
      FIND FIRST l-order1 WHERE l-order1.docu-nr EQ l-order.docu-nr 
        AND l-order1.pos EQ 0 EXCLUSIVE-LOCK. 

      l-order1.rechnungspreis = l-order1.rechnungspreis - l-op.warenwert. 
      l-order1.rechnungswert = l-order1.rechnungswert - l-op.warenwert. 
      FIND CURRENT l-order1 NO-LOCK. 
    END. 
  END. 
  /*  Oscar (29/11/2024) - F0ADB1 - deduct dml geliefert */
  ELSE IF SUBSTR(l-op.docu-nr,1,1) EQ "D" THEN
  DO:
    dml-no = INT(SUBSTRING(l-op.docu-nr, 11, 2)).
    dept-no = INT(SUBSTRING(l-op.docu-nr,2,2)).

    IF dml-no GT 1 THEN
    DO:
      FIND FIRST reslin-queasy WHERE reslin-queasy.KEY EQ "DML"
        AND INT(ENTRY(1,reslin-queasy.char1,";")) EQ l-op.artnr
        AND reslin-queasy.date1 EQ l-op.datum
        AND INT(ENTRY(2,reslin-queasy.char1,";")) EQ dept-no 
        AND reslin-queasy.number2 EQ dml-no EXCLUSIVE-LOCK NO-ERROR.
      IF AVAILABLE reslin-queasy THEN
      DO:
        ASSIGN reslin-queasy.deci3 = reslin-queasy.deci3 - str-list-qty.
        FIND CURRENT reslin-queasy NO-LOCK.
        RELEASE reslin-queasy.
      END.
    END.
    ELSE
    DO:
      FIND FIRST dml-artdep WHERE dml-artdep.artnr EQ l-op.artnr
        AND dml-artdep.datum EQ l-op.datum
        AND dml-artdep.departement EQ dept-no EXCLUSIVE-LOCK NO-ERROR.
      IF AVAILABLE dml-artdep THEN
      DO:
        ASSIGN dml-artdep.geliefert = dml-artdep.geliefert - str-list-qty.
        FIND CURRENT dml-artdep NO-LOCK.
        RELEASE dml-artdep.
      END.
      ELSE
      DO:
        FIND FIRST dml-art WHERE dml-art.artnr EQ l-op.artnr
          AND dml-art.datum EQ l-op.datum EXCLUSIVE-LOCK NO-ERROR.
        IF AVAILABLE dml-art THEN
        DO:
          ASSIGN dml-art.geliefert = dml-art.geliefert - str-list-qty.
          FIND CURRENT dml-art NO-LOCK.
          RELEASE dml-art.
        END.
      END.
    END.
  END.
 
  IF NOT direct-issue THEN 
  DO: 
    IF ((l-artikel.endkum EQ f-endkum
      OR l-artikel.endkum EQ b-endkum) 
      AND (str-list-billdate LE fb-closedate)) 
      OR ((l-artikel.endkum GE m-endkum) 
      AND (str-list-billdate LE m-closedate)) THEN 
    DO: 
      /* UPDATE average price  */ 
      FIND FIRST l-bestand WHERE l-bestand.artnr EQ l-op.artnr
        AND l-bestand.lager-nr EQ 0 NO-LOCK NO-ERROR.
      IF AVAILABLE l-bestand THEN
      ASSIGN
          tot-anz  = l-bestand.anz-anf-best
          tot-wert = l-bestand.val-anf-best
      .

      FOR EACH l-opbuff WHERE l-opbuff.artnr EQ l-op.artnr
        AND l-opbuff.op-art EQ 1
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

    /* Oscar (28/11/2024) - F0ADB1 - UPDATE stock onhand */
    FIND FIRST l-bestand WHERE l-bestand.lager-nr EQ 0 
        AND l-bestand.artnr EQ l-artikel.artnr EXCLUSIVE-LOCK NO-ERROR. 

    IF AVAILABLE l-bestand THEN 
    DO:
      ASSIGN
        l-bestand.anz-eingang  = l-bestand.anz-eingang - str-list-qty /* Oscar (26/11/2024) - F0ADB1 - fix cancel receiving */
        l-bestand.wert-eingang = l-bestand.wert-eingang - l-op.warenwert
      . 
      FIND CURRENT l-bestand NO-LOCK. 
      RELEASE l-bestand.
    END. 

    FIND FIRST l-bestand WHERE l-bestand.lager-nr EQ l-op.lager-nr 
      AND l-bestand.artnr EQ l-artikel.artnr EXCLUSIVE-LOCK NO-ERROR. 
    IF AVAILABLE l-bestand THEN 
    DO: 
      ASSIGN
        l-bestand.anz-eingang  = l-bestand.anz-eingang - str-list-qty /* Oscar (26/11/2024) - F0ADB1 - fix cancel receiving */
        l-bestand.wert-eingang = l-bestand.wert-eingang - l-op.warenwert 
      . 
      FIND CURRENT l-bestand NO-LOCK. 
      RELEASE l-bestand.
    END.
  END. 
  ELSE IF direct-issue THEN 
  DO: 
    /* Start - Oscar (29/11/2024) - F0ADB1 - add validation to prevent
    double deduct because delete in issuing report done first */
    FIND FIRST l-op1 WHERE l-op1.lscheinnr EQ l-op.lscheinnr
        AND l-op1.artnr EQ l-op.artnr
        AND l-op1.op-art EQ 3 
        AND l-op1.loeschflag NE 2
        AND l-op1.lief-nr EQ l-op.lief-nr
        AND l-op1.herkunftflag EQ 2 
        AND l-op1.lager-nr EQ l-op.lager-nr NO-LOCK NO-ERROR.
        
    IF AVAILABLE l-op1 THEN
    DO:
        /* UPDATE stock onhand  */ 
        FIND FIRST l-bestand WHERE l-bestand.lager-nr EQ 0 
            AND l-bestand.artnr EQ l-artikel.artnr EXCLUSIVE-LOCK NO-ERROR.
        
        IF AVAILABLE l-bestand THEN 
        DO:
            ASSIGN
              l-bestand.anz-eingang  = l-bestand.anz-eingang - l-op1.anzahl 
              l-bestand.wert-eingang = l-bestand.wert-eingang - l-op1.warenwert
        
              l-bestand.anz-ausgang  = l-bestand.anz-ausgang - l-op1.anzahl 
              l-bestand.wert-ausgang = l-bestand.wert-ausgang - l-op1.warenwert
            . 
            FIND CURRENT l-bestand NO-LOCK.
            RELEASE l-bestand.
        END. 
        
        FIND FIRST l-bestand WHERE l-bestand.lager-nr EQ l-op1.lager-nr 
            AND l-bestand.artnr EQ l-artikel.artnr EXCLUSIVE-LOCK NO-ERROR. 
        
        IF AVAILABLE l-bestand THEN 
        DO: 
            ASSIGN
              l-bestand.anz-eingang  = l-bestand.anz-eingang - l-op1.anzahl 
              l-bestand.wert-eingang = l-bestand.wert-eingang - l-op1.warenwert 
        
              l-bestand.anz-ausgang  = l-bestand.anz-ausgang - l-op1.anzahl 
              l-bestand.wert-ausgang = l-bestand.wert-ausgang - l-op1.warenwert
            . 
            FIND CURRENT l-bestand NO-LOCK. 
            RELEASE l-bestand.
        END.
        
        RELEASE l-op1.
    END.
    ELSE
    DO:
        /* UPDATE stock onhand  */ 
        FIND FIRST l-bestand WHERE l-bestand.lager-nr EQ 0 
            AND l-bestand.artnr EQ l-artikel.artnr EXCLUSIVE-LOCK NO-ERROR.

        IF AVAILABLE l-bestand THEN 
        DO:
            ASSIGN
              l-bestand.anz-eingang  = l-bestand.anz-eingang - l-op.anzahl 
              l-bestand.wert-eingang = l-bestand.wert-eingang - l-op.warenwert
            . 
            FIND CURRENT l-bestand NO-LOCK. 
            RELEASE l-bestand.
        END. 

        FIND FIRST l-bestand WHERE l-bestand.lager-nr EQ l-op.lager-nr 
            AND l-bestand.artnr EQ l-artikel.artnr EXCLUSIVE-LOCK NO-ERROR. 

        IF AVAILABLE l-bestand THEN 
        DO: 
            ASSIGN
              l-bestand.anz-eingang  = l-bestand.anz-eingang - l-op.anzahl 
              l-bestand.wert-eingang = l-bestand.wert-eingang - l-op.warenwert 
            . 
            FIND CURRENT l-bestand NO-LOCK. 
            RELEASE l-bestand.
        END.
    END.
    /* End - Oscar (29/11/2024) - F0ADB1 */
    
    FIND FIRST l-op1 WHERE l-op1.artnr EQ l-op.artnr 
      AND l-op1.op-art EQ 3 
      AND l-op1.lief-nr EQ l-op.lief-nr 
      AND l-op1.lscheinnr EQ l-op.lscheinnr 
      AND l-op1.herkunftflag EQ 2 
      AND l-op1.lager-nr EQ l-op.lager-nr 
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
  FIND FIRST  l-liefumsatz WHERE l-liefumsatz.lief-nr EQ l-op.lief-nr 
    AND l-liefumsatz.datum EQ str-list-billdate EXCLUSIVE-LOCK NO-ERROR. 
  IF AVAILABLE l-liefumsatz THEN 
    l-liefumsatz.gesamtumsatz = l-liefumsatz.gesamtumsatz - l-op.warenwert.
  FIND CURRENT l-liefumsatz NO-LOCK.
  RELEASE l-liefumsatz.

  FIND FIRST l-order WHERE l-order.docu-nr EQ l-op.docu-nr 
    AND l-order.lief-nr EQ l-op.lief-nr 
    AND l-order.pos EQ 0 
    AND l-order.loeschflag EQ 1 NO-LOCK NO-ERROR. 
  IF AVAILABLE l-order THEN 
  DO: 
      docu-nr = recid(l-op).
      msg-str = msg-str + CHR(2) + "&Q"
              + translateExtended ("Purchase Order closed; re-open it?",lvCAREA,"").
  END. 

  /* Start - Oscar (27/02/25) - B22CCA - Fix cancel incoming not delete purchase book */
  IF SUBSTR(l-op.docu-nr,1,1) EQ "D" OR SUBSTR(l-op.docu-nr,1,1) EQ "I" THEN
  DO:
    FIND FIRST l-pprice WHERE l-pprice.artnr EQ l-op.artnr 
      AND l-pprice.bestelldatum EQ l-op.datum 
      AND l-pprice.anzahl EQ l-op.anzahl 
      AND l-pprice.einzelpreis EQ l-op.einzelpreis 
      AND l-pprice.lief-nr EQ l-op.lief-nr 
      /* AND l-pprice.docu-nr EQ l-op.docu-nr */ AND l-pprice.docu-nr EQ l-op.lscheinnr NO-LOCK NO-ERROR. /* Oscar (27/02/25) - B22CCA - Fix cancel incoming not delete purchase book */
    IF AVAILABLE l-pprice THEN 
    DO: 
      FIND CURRENT l-pprice EXCLUSIVE-LOCK.
      DELETE l-pprice. 
      RELEASE l-pprice. 
    END.
  END.
  ELSE IF SUBSTR(l-op.docu-nr,1,1) EQ "P" THEN
  DO:
    FIND FIRST l-pprice WHERE l-pprice.artnr EQ l-op.artnr 
      AND l-pprice.bestelldatum EQ l-op.datum 
      AND l-pprice.anzahl EQ l-op.anzahl 
      AND l-pprice.einzelpreis EQ l-op.einzelpreis 
      AND l-pprice.lief-nr EQ l-op.lief-nr 
      AND l-pprice.docu-nr EQ l-op.docu-nr NO-LOCK NO-ERROR. /* Oscar (27/02/25) - B22CCA - Fix cancel incoming not delete purchase book */
    IF AVAILABLE l-pprice THEN 
    DO: 
      FIND CURRENT l-pprice EXCLUSIVE-LOCK.
      DELETE l-pprice. 
      RELEASE l-pprice. 
    END.
  END.
  /* End - Oscar (27/02/25) - B22CCA - Fix cancel incoming not delete purchase book */

  /*ITA 24/01/25 - Hitung ulang Nilai AP*/
  FOR EACH blop WHERE blop.lscheinnr EQ l-op.lscheinnr
       AND blop.lief-nr GT 0 AND blop.loeschflag LE 1
       AND blop.op-art = 1 NO-LOCK:

       ASSIGN tot-vat = 0.
       FIND FIRST queasy WHERE queasy.KEY EQ 304 
          AND queasy.char1 EQ blop.lscheinnr 
          AND queasy.number1 EQ blop.artnr NO-LOCK NO-ERROR.
       IF AVAILABLE queasy THEN ASSIGN tot-vat = (blop.warenwert * (queasy.deci1 / 100)).

       ASSIGN tot-receiving = tot-receiving + (blop.warenwert + tot-vat).       
   END.

   IF tot-receiving NE 0 THEN DO:

        FIND FIRST bediener WHERE bediener.userinit = userinit NO-LOCK NO-ERROR.

        CREATE l-kredit.
        ASSIGN
           l-kredit.NAME        = l-op.docu-nr
           l-kredit.lief-nr     = l-op.lief-nr
           l-kredit.lscheinnr   = l-op.lscheinnr
           l-kredit.rgdatum     = l-op.datum
           l-kredit.datum       = ?
           l-kredit.ziel        = 30
           l-kredit.saldo       = tot-receiving
           l-kredit.netto       = tot-receiving
           l-kredit.bediener-nr = bediener.nr
        .

        CREATE ap-journal.
        ASSIGN
           ap-journal.docu-nr   = l-op.docu-nr
           ap-journal.lscheinnr = l-op.lscheinnr
           ap-journal.lief-nr   = l-op.lief-nr
           ap-journal.rgdatum   = l-op.datum
           ap-journal.zeit      = l-op.zeit
           ap-journal.saldo     = tot-receiving
           ap-journal.netto     = tot-receiving
        .
        IF AVAILABLE bediener THEN ap-journal.userinit = userinit.

        RELEASE l-kredit.
        RELEASE ap-journal.
   END.
  /*ITA*/
  /* Oscar (29/11/2024) - F0ADB1 - comment to prevent dml-artdep.geliefert set to 0 if
  l-op datum, artnr same as dml-artdep available from receiving with PO and without PO*/
  /* IF l-op.loeschflag EQ 2 THEN 
  DO:  
    FIND FIRST dml-art WHERE dml-art.artnr EQ l-op.artnr 
      AND dml-art.datum EQ l-op.datum
      AND dml-art.anzahl GT 0 EXCLUSIVE-LOCK NO-ERROR.
    IF AVAILABLE dml-art THEN 
    DO:
      ASSIGN dml-art.geliefert = 0.
      FIND CURRENT dml-art NO-LOCK.
    END.
    ELSE IF NOT AVAILABLE dml-art THEN 
    DO:
      FIND FIRST dml-artdep WHERE dml-artdep.artnr EQ l-op.artnr 
        AND dml-artdep.datum EQ l-op.datum
        AND dml-artdep.anzahl GT 0 EXCLUSIVE-LOCK NO-ERROR.
      IF AVAILABLE dml-artdep THEN 
      DO:
          ASSIGN dml-artdep.geliefert = 0.
          FIND CURRENT dml-artdep NO-LOCK.
      END.
    END.
  END */
  /*end*/
  RELEASE l-order1.
  RELEASE l-op1.  
  RELEASE l-order.
  RELEASE l-artikel.
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
    AND l-bestand.artnr EQ curr-artnr
    AND l-bestand.lager-nr EQ l-op.lager-nr EXCLUSIVE-LOCK NO-ERROR.
  IF AVAILABLE l-bestand THEN
  ASSIGN
      l-bestand.anz-eingang  = 0
      l-bestand.anz-ausgang  = 0
      l-bestand.wert-eingang = 0
      l-bestand.wert-ausgang = 0
  .  

  FIND FIRST lbuff WHERE lbuff.anf-best-dat GE start-date 
    AND lbuff.anf-best-dat LE end-date 
    AND lbuff.artnr EQ curr-artnr
    AND lbuff.lager-nr EQ 0 EXCLUSIVE-LOCK NO-ERROR.
  IF AVAILABLE lbuff THEN
  ASSIGN
      lbuff.anz-eingang      = 0
      lbuff.anz-ausgang      = 0
      lbuff.wert-eingang     = 0
      lbuff.wert-ausgang     = 0
  .  

  /* fixing outgoing l-op price and amount */
  FOR EACH l-opbuff WHERE l-opbuff.artnr EQ curr-artnr
    AND l-opbuff.datum GE from-date 
    AND (l-opbuff.op-art GE 2 AND l-opbuff.op-art LE 14) 
    AND l-opbuff.loeschflag LE 1 EXCLUSIVE-LOCK:
      ASSIGN
          l-opbuff.einzelpreis = avrg-price
          l-opbuff.warenwert = avrg-price * l-opbuff.anzahl
      .
  END.
  RELEASE l-opbuff.
  
  /* fixing l-bestand receiving and outgoing amount */
  FOR EACH l-opbuff WHERE l-opbuff.artnr EQ curr-artnr
    AND l-opbuff.datum GE start-date
    AND l-opbuff.datum LE end-date
    AND (l-opbuff.op-art GE 1 AND l-opbuff.op-art LE 4) 
    AND l-opbuff.loeschflag LE 1 NO-LOCK: 
      IF l-opbuff.op-art LE 2 THEN
      DO:
        IF AVAILABLE lbuff THEN
        ASSIGN
          lbuff.anz-eingang  = lbuff.anz-eingang  + l-opbuff.anzahl
          lbuff.wert-eingang = lbuff.wert-eingang + l-opbuff.warenwert
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
          lbuff.anz-ausgang  = lbuff.anz-ausgang  + l-opbuff.anzahl
          lbuff.wert-ausgang = lbuff.wert-ausgang + l-opbuff.warenwert
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

  RELEASE l-bestand.
  RELEASE lbuff.
END.

/*ITA 300715*/
PROCEDURE update-ap:
  DEFINE VARIABLE flogic   AS LOGICAL NO-UNDO.
  DEFINE VARIABLE billdate AS DATE    NO-UNDO.

  FIND FIRST htparam WHERE paramnr EQ 1016 NO-LOCK NO-ERROR. /* ap license */ 
  ASSIGN flogic = htparam.flogical.

  FIND FIRST htparam WHERE paramnr EQ 474 NO-LOCK NO-ERROR. 
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
