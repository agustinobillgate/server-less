
DEFINE TEMP-TABLE disc-list 
  FIELD l-recid     AS INTEGER 
  FIELD price0      AS DECIMAL FORMAT ">,>>>,>>>,>>9.999" LABEL "Unit-Price" 
  FIELD brutto      AS DECIMAL FORMAT "->,>>>,>>>,>>9.999" LABEL "Gross Amount" 
  FIELD disc        AS DECIMAL FORMAT ">9.99" LABEL "Disc" 
  FIELD disc2       AS DECIMAL FORMAT ">9.99" LABEL "Disc2" 
  FIELD vat         AS DECIMAL FORMAT ">9.99" LABEL "VAT"
  FIELD new-created AS LOGICAL INITIAL NO. 

DEF TEMP-TABLE t-l-order LIKE l-order
    FIELD rec-id AS INT.

DEF INPUT-OUTPUT PARAMETER pos AS INT.
DEF INPUT-OUTPUT PARAMETER t-amount AS DECIMAL.
DEF INPUT PARAMETER docu-nr AS CHAR.
DEF INPUT PARAMETER s-artnr AS INT.
DEF INPUT PARAMETER dunit-price AS LOGICAL.
DEF INPUT PARAMETER price AS DECIMAL.
DEF INPUT PARAMETER curr-disc AS DECIMAL.
DEF INPUT PARAMETER curr-disc2 AS DECIMAL.
DEF INPUT PARAMETER curr-vat AS DECIMAL.
DEF INPUT PARAMETER qty AS DECIMAL.
DEF INPUT PARAMETER potype AS INT.
DEF INPUT PARAMETER cost-acct AS CHAR.
DEF INPUT PARAMETER new-bez AS CHAR.
DEF INPUT PARAMETER t-l-artikel-lief-einheit AS DEC.
DEF INPUT PARAMETER bemerkung AS CHAR.
DEF INPUT PARAMETER lief-nr AS INT.
DEF INPUT PARAMETER t-l-artikel-traubensort AS CHAR.
DEF INPUT PARAMETER l-orderhdr-bestelldatum LIKE l-orderhdr.bestelldatum.
DEF INPUT PARAMETER billdate AS DATE.
DEF INPUT PARAMETER bediener-username AS CHAR.

DEF OUTPUT PARAMETER amount AS DECIMAL.
DEF OUTPUT PARAMETER TABLE FOR disc-list.
DEF OUTPUT PARAMETER TABLE FOR t-l-order.

RUN create-l-order.

PROCEDURE create-l-order: 
DEFINE VARIABLE price0 AS DECIMAL. 
  price0 = price. 
  price = price * (1 - curr-disc / 100). 
  price = price * (1 - curr-disc2 / 100). 
  price = price * (1 + curr-vat / 100). 
 
  pos = pos + 1. 
  DO: 
    create l-order. 
    l-order.docu-nr = docu-nr. 
    l-order.artnr = s-artnr. 
    l-order.anzahl = qty. 
    l-order.einzelpreis = price. 
 
    IF potype = 2 THEN l-order.stornogrund = STRING(cost-acct, "x(12)"). 
    ELSE l-order.stornogrund = STRING(" ", "x(12)"). 
    l-order.stornogrund = l-order.stornogrund + new-bez. 
 
    IF t-l-artikel-lief-einheit NE 0 THEN 
    DO: 
      IF dunit-price THEN l-order.warenwert = qty * price. 
      ELSE l-order.warenwert = qty * price * t-l-artikel-lief-einheit. 
      l-order.txtnr = t-l-artikel-lief-einheit. 
    END. 
    ELSE 
    DO: 
      l-order.warenwert = qty * price. 
      l-order.txtnr = 1. 
    END. 
    
    ASSIGN
      l-order.pos = pos
      l-order.bestelldatum = l-orderhdr-bestelldatum
      l-order.besteller = bemerkung
      l-order.lief-nr = lief-nr 
      l-order.op-art = 2
      l-order.flag = dunit-price
      l-order.lief-fax[3] = t-l-artikel-traubensort 
      l-order.bestelldatum = billdate
      l-order.lief-fax[1] = bediener-username
    . 
 
/*  IF curr-disc NE 0 OR curr-vat NE 0 OR curr-disc2 NE 0 THEN */ 
    l-order.quality = STRING(curr-disc, "99.99 ") + STRING(curr-vat, "99.99") 
      + STRING(curr-disc, " 99.99"). 
 
    create disc-list. 
    ASSIGN 
      disc-list.new-created = YES
      disc-list.l-recid = RECID(l-order)
      disc-list.disc = curr-disc 
      disc-list.disc2 = curr-disc2 
      disc-list.vat = curr-vat 
      disc-list.price0 =  l-order.einzelpreis / (1 - disc-list.disc * 0.01) 
        / (1 - disc-list.disc2 * 0.01) / (1 + disc-list.vat * 0.01). 
      disc-list.brutto = disc-list.price0 * l-order.anzahl. 
 
    amount = l-order.warenwert. 
    t-amount = t-amount + l-order.warenwert. 
    release l-order. 
  END. 
  /*MTRUN disp-it.*/
  FOR EACH l-order WHERE l-order.docu-nr = docu-nr 
      AND l-order.pos GT 0 AND l-order.loeschflag = 0 NO-LOCK:
      CREATE t-l-order.
      BUFFER-COPY l-order TO t-l-order.
      ASSIGN t-l-order.rec-id = RECID(l-order).
  END.
END. 
