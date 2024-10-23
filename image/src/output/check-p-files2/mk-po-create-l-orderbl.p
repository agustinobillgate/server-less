/*
DEF TEMP-TABLE t-l-order LIKE l-order
    FIELD rec-id AS INT
    FIELD a-bezeich LIKE l-artikel.bezeich
    FIELD lief-einheit LIKE l-artikel.lief-einheit.*/
    
DEF TEMP-TABLE t-l-order LIKE l-order
    FIELD rec-id        AS INT
    FIELD a-bezeich     AS CHARACTER FORMAT "x(36)"
    FIELD lief-einheit  AS DECIMAL FORMAT ">>>,>>9.999".

DEFINE TEMP-TABLE disc-list 
  FIELD l-recid     AS INTEGER 
  FIELD price0      AS DECIMAL FORMAT ">,>>>,>>>,>>9.999"   LABEL "Unit-Price" 
  FIELD brutto      AS DECIMAL FORMAT "->,>>>,>>>,>>9.999"  LABEL "Gross Amount" 
  FIELD disc        AS DECIMAL FORMAT ">9.99"               LABEL "Disc" 
  FIELD disc2       AS DECIMAL FORMAT ">9.99"               LABEL "Disc2" 
  FIELD vat         AS DECIMAL FORMAT ">9.99"               LABEL "VAT"
  FIELD disc-val    AS DECIMAL FORMAT ">,>>>,>>>,>>9.999"   LABEL "Disc Value" 
  FIELD disc2-val   AS DECIMAL FORMAT ">,>>>,>>>,>>9.999"   LABEL "Disc2 Value"
  FIELD vat-val     AS DECIMAL FORMAT ">,>>>,>>>,>>9.999"   LABEL "VAT-Value". 

DEF INPUT-OUTPUT PARAMETER pos          AS INT.
DEF INPUT PARAMETER rec-id-l-orderhdr   AS INT.
DEF INPUT PARAMETER rec-id-l-artikel    AS INT.
DEF INPUT PARAMETER s-artnr             AS INT.
DEF INPUT PARAMETER lief-nr             AS INT.
DEF INPUT PARAMETER docu-nr             AS CHAR.
DEF INPUT PARAMETER pr                  AS CHAR.
DEF INPUT PARAMETER remark              AS CHAR.
DEF INPUT PARAMETER price0              AS DECIMAL. 
DEF INPUT PARAMETER price1              AS DECIMAL. 
DEF INPUT PARAMETER price               AS DECIMAL.
DEF INPUT PARAMETER curr-disc           AS DECIMAL.
DEF INPUT PARAMETER curr-disc2          AS DECIMAL.
DEF INPUT PARAMETER curr-vat            AS DECIMAL. 
DEF INPUT PARAMETER qty                 AS DECIMAL.
DEF INPUT PARAMETER potype              AS INT.
DEF INPUT PARAMETER cost-acct           AS CHAR.
DEF INPUT PARAMETER new-bez             AS CHAR.
DEF INPUT PARAMETER dunit-price         AS LOGICAL.
DEF INPUT PARAMETER bediener-username   AS CHAR.
/*MT*/
DEF INPUT-OUTPUT PARAMETER t-amount           AS DECIMAL.

DEF OUTPUT PARAMETER put-disc           AS LOGICAL.
DEF OUTPUT PARAMETER amount             AS DECIMAL.
DEF OUTPUT PARAMETER fl-code            AS INT INIT 0.
DEF OUTPUT PARAMETER p-222              AS LOGICAL.
DEF OUTPUT PARAMETER TABLE FOR t-l-order.
DEF OUTPUT PARAMETER TABLE FOR disc-list.

/* SY 30/09/2014 */
DEF VARIABLE bemerkung       AS CHAR    NO-UNDO.
DEF VARIABLE globaldisc      AS DECIMAL NO-UNDO INIT 0.
DEF VARIABLE disc-value1     AS DECIMAL NO-UNDO INIT 0.
DEF VARIABLE disc-value2     AS DECIMAL NO-UNDO INIT 0.
DEF VARIABLE disc-vat        AS DECIMAL NO-UNDO INIT 0.

ASSIGN bemerkung = ENTRY(1, remark, CHR(2)).
IF NUM-ENTRIES (remark, CHR(2)) GT 1 THEN DO:  /*ITA 130616*/
    ASSIGN 
        globaldisc  = DECIMAL(ENTRY(2, remark, CHR(2))) / 100
        disc-value1 = DECIMAL(ENTRY(3, remark, CHR(2)))
        disc-value2 = DECIMAL(ENTRY(4, remark, CHR(2)))
        disc-vat    = DECIMAL(ENTRY(5, remark, CHR(2))).
END.

FIND FIRST l-artikel WHERE l-artikel.artnr = s-artnr NO-ERROR. 
IF NOT AVAILABLE l-artikel THEN RETURN. 

FIND FIRST l-orderhdr WHERE RECID(l-orderhdr) = rec-id-l-orderhdr.
FIND FIRST l-artikel WHERE RECID(l-artikel) = rec-id-l-artikel.

RUN create-l-order. 

FOR EACH l-order WHERE l-order.docu-nr = docu-nr 
    AND l-order.pos GT 0 NO-LOCK:
    CREATE t-l-order.
    BUFFER-COPY l-order TO t-l-order.
    ASSIGN t-l-order.rec-id = RECID(l-order).

    FIND FIRST l-artikel WHERE l-artikel.artnr = l-order.artnr NO-LOCK.
    ASSIGN t-l-order.a-bezeich    = l-artikel.bezeich
           t-l-order.lief-einheit = l-artikel.lief-einheit.
END.


PROCEDURE create-l-order: 
DEFINE buffer l-od FOR l-order. 
DEFINE VARIABLE bruto AS DECIMAL.

  IF pos = 0 THEN 
  DO: 
    create l-od. 
    ASSIGN 
      l-od.docu-nr = docu-nr 
      l-od.pos = 0 
      l-od.bestelldatum = l-orderhdr.bestelldatum 
      l-od.lief-nr = lief-nr 
      l-od.op-art = 2 
      l-od.lief-fax[1] = pr 
      l-od.betriebsnr = 2. 
    FIND FIRST htparam WHERE paramnr = 222 NO-LOCK.
    p-222 = htparam.flogical.
    fl-code = 1.
  END. 

  DO: 
    pos = pos + 1. 
    CREATE l-order. 
    ASSIGN 
    l-order.docu-nr = docu-nr 
    l-order.artnr = s-artnr 
    l-order.pos = pos 
    l-order.bestelldatum = l-orderhdr.bestelldatum 
    l-order.besteller = bemerkung
    l-order.lief-nr = lief-nr 
    l-order.op-art = 2 
    l-order.lief-fax[1] = bediener-username 
    l-order.lief-fax[3] = l-artikel.traubensort
    l-order.betriebsnr = 2. 
    CREATE disc-list. 
    ASSIGN 
      disc-list.l-recid = RECID(l-order) 
      disc-list.price0 = price0 
      disc-list.disc = curr-disc 
      disc-list.disc2 = curr-disc2 
      disc-list.vat = curr-vat. 
  END. 
  l-order.anzahl = qty. 
  l-order.einzelpreis = price. 
 
  IF potype = 2 THEN l-order.stornogrund = STRING(cost-acct, "x(12)"). 
  ELSE l-order.stornogrund = STRING(" ", "x(12)"). 
  l-order.stornogrund = l-order.stornogrund + new-bez. 
 
  IF l-artikel.lief-einheit NE 0 THEN 
  DO: 
    IF dunit-price THEN 
    DO: 
      l-order.warenwert = qty * price. 
      disc-list.brutto = disc-list.price0 * qty. 
      bruto = price1 * qty. 
    END. 
    ELSE 
    DO: 
      l-order.warenwert = qty * price * l-artikel.lief-einheit. 
      disc-list.brutto = disc-list.price0 * qty *  l-artikel.lief-einheit. 
      bruto = price1 * qty *  l-artikel.lief-einheit. 
    END. 
    l-order.txtnr = l-artikel.lief-einheit. 
  END. 
  ELSE 
  DO: 
    l-order.warenwert = qty * price. 
    l-order.txtnr = 1. 
    disc-list.brutto = disc-list.price0 * l-order.anzahl.
    bruto = price1 * l-order.anzahl. 
  END. 
  l-order.flag = dunit-price. 
 
/*  IF curr-disc NE 0 OR curr-vat NE 0 THEN */ 
  DO: 
    l-order.quality = STRING(curr-disc, "99.99 ") + STRING(curr-vat, "99.99") 
      + STRING(curr-disc2, " 99.99") + STRING(disc-value1, " >,>>>,>>>,>>9.999") 
      + STRING(disc-value2, " >,>>>,>>>,>>9.999")
      + STRING(disc-vat, " >,>>>,>>>,>>9.999").  /*ITA 130616*/
    l-order.quality = l-order.quality. 
    put-disc = NO. 
  END. 
  
  amount                = l-order.warenwert. 
  t-amount              = t-amount + l-order.warenwert. 
  disc-list.disc-val    = (curr-disc / 100) * disc-list.brutto.
  disc-list.disc2-val   = (curr-disc2 / 100) * bruto.
  disc-list.vat-val     = (curr-vat / 100) * amount.
  RELEASE l-order.

  FIND FIRST l-od WHERE 
      l-od.docu-nr = docu-nr AND
      l-od.pos     = 0       AND
      l-od.lief-nr = lief-nr AND
      l-od.op-art = 2.
  ASSIGN l-od.warenwert = globaldisc.
  FIND CURRENT l-od NO-LOCK.

END. 

