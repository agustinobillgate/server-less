DEFINE TEMP-TABLE s-list 
  FIELD s-recid     AS INTEGER 
  FIELD datum       AS DATE LABEL "Date" 
  FIELD artnr       AS INTEGER FORMAT "9999999" LABEL "ArtNo" 
  FIELD bezeich     AS CHAR FORMAT "x(30)" LABEL "Description" 
  FIELD einzelpreis AS DECIMAL FORMAT ">,>>>,>>>,>>9.999" LABEL "Unit Price" 
  FIELD price0      AS DECIMAL INITIAL ? 
  FIELD anzahl      AS DECIMAL FORMAT "->>,>>9.999" LABEL "Qty" 
  FIELD anz0        AS DECIMAL FORMAT "->,>>>9.999" INITIAL ? 
  FIELD brutto      AS DECIMAL FORMAT "->>,>>>,>>9.99" LABEL "      Amount" 
  FIELD val0        AS DECIMAL 
  FIELD disc        AS DECIMAL FORMAT ">9.99" LABEL "Disc" 
  FIELD disc0       AS DECIMAL 
  FIELD disc2       AS DECIMAL FORMAT ">9.99" LABEL "Disc2" 
  FIELD disc20      AS DECIMAL 
  FIELD disc-amt    AS DECIMAL FORMAT "->,>>>,>>9.99" LABEL "Disc-Amount" 
  FIELD disc2-amt   AS DECIMAL FORMAT "->,>>>,>>9.99" LABEL "Disc2-Amount" 
  FIELD vat         AS DECIMAL FORMAT ">9.99" LABEL "VAT%" 
  FIELD warenwert   AS DECIMAL FORMAT "->>,>>>,>>9.99" LABEL "Net-Amount" 
  FIELD vat0        AS DECIMAL 
  FIELD vat-amt     AS DECIMAL FORMAT "->,>>>,>>9.99" LABEL "VAT-Amount" 
  FIELD betriebsnr  AS INTEGER. 

DEF INPUT PARAMETER pvILanguage      AS INT  NO-UNDO.
DEF INPUT PARAMETER lief-nr AS INT.
DEF INPUT PARAMETER lscheinnr AS CHAR. 
DEF OUTPUT PARAMETER f-endkum AS INT.
DEF OUTPUT PARAMETER b-endkum AS INT.
DEF OUTPUT PARAMETER m-endkum AS INT.
DEF OUTPUT PARAMETER fb-closedate AS DATE.
DEF OUTPUT PARAMETER m-closedate AS DATE.
DEF OUTPUT PARAMETER b1-tittle AS CHAR.
DEF OUTPUT PARAMETER tot-amt     AS DECIMAL.
DEF OUTPUT PARAMETER tot-disc    AS DECIMAL.
DEF OUTPUT PARAMETER tot-disc2   AS DECIMAL.
DEF OUTPUT PARAMETER tot-vat     AS DECIMAL.
DEF OUTPUT PARAMETER tot-val     AS DECIMAL.
DEF OUTPUT PARAMETER confirm-flag AS LOGICAL INITIAL YES. 
DEF OUTPUT PARAMETER price-decimal AS INT.
DEF OUTPUT PARAMETER long-digit AS LOGICAL.
DEF OUTPUT PARAMETER p-269 AS DATE.
DEF OUTPUT PARAMETER l-lieferant-firma AS CHAR.
DEF OUTPUT PARAMETER TABLE FOR s-list.

{ supertransbl.i } 
DEF VAR lvCAREA AS CHAR INITIAL "po-invoice". 

RUN htpdate.p(269, OUTPUT p-269).
RUN htpint.p(491, OUTPUT price-decimal).
RUN htplogic.p (246, OUTPUT long-digit).
FIND FIRST l-lieferant WHERE l-lieferant.lief-nr = lief-nr NO-LOCK. 
l-lieferant-firma = l-lieferant.firma.
FIND FIRST htparam WHERE htparam.paramnr = 257 NO-LOCK. 
f-endkum = htparam.finteger. 
FIND FIRST htparam WHERE htparam.paramnr = 258 NO-LOCK. 
b-endkum = htparam.finteger. 
FIND FIRST htparam WHERE htparam.paramnr = 268 NO-LOCK. 
m-endkum = htparam.finteger. 
FIND FIRST htparam WHERE paramnr = 224 NO-LOCK. 
fb-closedate = htparam.fdate. 
FIND FIRST htparam WHERE paramnr = 221 NO-LOCK. 
m-closedate = htparam.fdate. 

b1-tittle = translateExtended ("Stocks Incoming List -",lvCAREA,"") 
  + " " + l-lieferant.firma + " / " + lscheinnr.

RUN create-list. 

PROCEDURE create-list: 
  ASSIGN
    tot-amt     = 0 
    tot-vat     = 0 
    tot-disc    = 0 
    tot-disc2   = 0
  . 
  FOR EACH s-list: 
    DELETE s-list. 
  END. 
  FOR EACH l-op WHERE l-op.lief-nr = lief-nr AND l-op.lscheinnr = lscheinnr 
    AND l-op.op-art = 1 AND l-op.loeschflag LE 1 NO-LOCK, 
    FIRST l-artikel WHERE l-artikel.artnr = l-op.artnr 
    BY l-artikel.bezeich BY l-op.betriebsnr: 
/* Module Receiving: 
  Note: IF discount = 10% THEN curr-disc = 10.00 * 100 = 1000 !! 
        IF vat      = 11% THEN curr-vat  = 11.00 * 100 = 1100 !! 
        vat-amount is NOT included IN the l-op.warenwert      !! 
  l-op.deci1[1] = orig-preis. 
  l-op.deci1[2] = curr-disc / 100.   -> i.e. 10%  $$$ 
  IF curr-vat NE 0 THEN 
  DO: 
    l-op.deci1[3] = curr-vat / 100.  -> i.e. 11% 
    l-op.deci1[4] = epreis * l-op.deci1[3] * 0.01. 
  END. 
*/ 
    IF l-op.betriebsnr = 0 OR l-op.betriebsnr = 10 THEN confirm-flag = NO. 
    create s-list. 
    IF l-op.betriebsnr LE 1 THEN 
    DO: 
      ASSIGN 
        s-list.artnr = l-op.artnr 
        s-list.datum = l-op.datum 
        s-list.bezeich = l-artikel.bezeich 
        s-list.anzahl = l-op.anzahl 
        s-list.anz0 = l-op.anzahl 
        s-list.einzelpreis = l-op.deci1[1] 
        s-list.price0 = l-op.deci1[1] 
        s-list.disc = l-op.deci1[2] 
        s-list.disc0 = l-op.deci1[2] 
        s-list.disc2 = l-op.rueckgabegrund / 100 
        s-list.disc20 = l-op.rueckgabegrund / 100 
        s-list.brutto =  l-op.warenwert / (1 - s-list.disc * 0.01) 
          / (1 - s-list.disc2 * 0.01) /* / (1 + l-op.deci1[3] * 0.01) */ 
        s-list.warenwert = l-op.warenwert 
        s-list.val0 = l-op.warenwert 
        s-list.disc-amt = l-op.deci1[1] * l-op.anzahl * l-op.deci1[2] * 0.01 
        s-list.disc2-amt = l-op.deci1[1] * l-op.anzahl 
          * (1 - s-list.disc * 0.01) * s-list.disc2 * 0.01 
        s-list.vat = l-op.deci1[3] 
        s-list.vat0 = l-op.deci1[3] 
        s-list.vat-amt = s-list.warenwert * s-list.vat * 0.01 
        s-list.betriebsnr = l-op.betriebsnr 
        s-list.s-recid = RECID(l-op). 
      tot-amt = tot-amt + /* l-op.anzahl * l-op.deci1[1] */ s-list.brutto. 
      tot-disc = tot-disc + s-list.disc-amt. 
      tot-disc2 = tot-disc2 + s-list.disc2-amt. 
      tot-vat = tot-vat + s-list.vat-amt. 
    END. 
    ELSE 
    DO: 
      ASSIGN 
        s-list.artnr = l-op.artnr 
        s-list.datum = l-op.datum 
        s-list.bezeich = l-artikel.bezeich 
        s-list.anzahl = l-op.anzahl 
        s-list.einzelpreis = l-op.deci1[1] 
        s-list.price0 = l-op.deci1[1] 
        s-list.disc = l-op.deci1[2] 
        s-list.disc0 = l-op.deci1[2] 
        s-list.disc2 = l-op.rueckgabegrund / 100 
        s-list.disc20 = l-op.rueckgabegrund / 100 
        s-list.brutto = l-op.warenwert / ( 1 - s-list.disc * 0.01) 
          / (1 - s-list.disc2 * 0.01) 
        s-list.warenwert = l-op.warenwert 
        s-list.val0 = l-op.warenwert 
        s-list.disc-amt = s-list.brutto * l-op.deci1[2] * 0.01 
        s-list.disc2-amt = s-list.brutto * (1 - s-list.disc * 0.01) 
          * s-list.disc2 * 0.01 
        s-list.vat = l-op.deci1[3] 
        s-list.vat0 = l-op.deci1[3] 
        s-list.vat-amt = l-op.warenwert * l-op.deci[3] * 0.01 
        s-list.betriebsnr = l-op.betriebsnr 
        s-list.s-recid = RECID(l-op). 
      tot-amt = tot-amt + s-list.brutto. 
      tot-disc = tot-disc + s-list.disc-amt. 
      tot-disc2 = tot-disc2 + s-list.disc2-amt. 
      tot-vat = tot-vat + s-list.vat-amt. 
    END. 
  END. 
  tot-val = tot-amt - tot-disc - tot-disc2 + tot-vat. 
END. 

