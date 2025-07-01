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

DEFINE INPUT  PARAMETER pvILanguage     AS INTEGER  NO-UNDO.
DEFINE INPUT-OUTPUT PARAMETER tot-amt   AS DECIMAL.
DEFINE INPUT-OUTPUT PARAMETER tot-disc  AS DECIMAL.
DEFINE INPUT-OUTPUT PARAMETER tot-disc2 AS DECIMAL.
DEFINE INPUT-OUTPUT PARAMETER tot-vat   AS DECIMAL.
DEFINE INPUT-OUTPUT PARAMETER tot-val   AS DECIMAL.
DEFINE INPUT  PARAMETER qty             AS DECIMAL.
DEFINE INPUT  PARAMETER brutto          AS DECIMAL.
DEFINE INPUT  PARAMETER s-list-s-recid  AS INT.
DEFINE INPUT  PARAMETER f-endkum        AS INT.
DEFINE INPUT  PARAMETER b-endkum        AS INT.
DEFINE INPUT  PARAMETER m-endkum        AS INT.
DEFINE INPUT  PARAMETER fb-closedate    AS DATE.
DEFINE INPUT  PARAMETER m-closedate     AS DATE.
DEFINE INPUT  PARAMETER bediener-nr     AS INT.
DEFINE OUTPUT PARAMETER msg-str         AS CHAR.
DEFINE OUTPUT PARAMETER TABLE FOR s-list.

{SupertransBL.i} 
DEF VAR lvCAREA AS CHAR INITIAL "po-invoice".

RUN create-retinv.

PROCEDURE create-retinv:
DEFINE VARIABLE netto AS DECIMAL. 
DEFINE buffer l-op1 FOR l-op. 
  FIND FIRST l-op1 WHERE RECID(l-op1) = s-list-s-recid NO-LOCK. 
  FIND FIRST l-artikel WHERE l-artikel.artnr = l-op1.artnr NO-LOCK. 
  netto = brutto / (1 + l-op1.deci1[2] * 0.01). 
  create l-op. 
  ASSIGN 
    l-op.datum = l-op1.datum 
    l-op.lager-nr = l-op1.lager-nr 
    l-op.artnr = l-op1.artnr 
    l-op.lief-nr = l-op1.lief-nr 
    l-op.zeit = l-op1.zeit 
    l-op.anzahl = qty 
    l-op.einzelpreis = l-op1.einzelpreis 
    l-op.warenwert = netto 
    l-op.deci1[1] = l-op1.deci1[1] 
    l-op.deci1[2] = l-op1.deci1[2] 
    l-op.deci1[3] = l-op1.deci1[3] 
    l-op.deci1[4] = l-op.warenwert * l-op.deci1[3] * 0.01 
    l-op.op-art = 1 
    l-op.herkunftflag = l-op1.herkunftflag 
    l-op.docu-nr = l-op1.docu-nr 
    l-op.lscheinnr = l-op1.lscheinnr 
    l-op.pos = l-op1.pos 
    l-op.flag = l-op1.flag 
    l-op.fuellflag = bediener-nr 
    l-op.betriebsnr = l-op1.betriebsnr + 10. 
  FIND CURRENT l-op NO-LOCK. 
  
  create s-list. 
  ASSIGN 
    s-list.artnr = l-op.artnr 
    s-list.datum = l-op.datum 
    s-list.bezeich = l-artikel.bezeich 
    s-list.anzahl = l-op.anzahl 
    s-list.anz0 = l-op.anzahl 
    s-list.einzelpreis = l-op.deci1[1] 
    s-list.price0 = l-op.deci1[1] 
    s-list.brutto = brutto 
    s-list.warenwert = l-op.warenwert 
    s-list.val0 = l-op.warenwert 
    s-list.disc = l-op.deci1[2] 
    s-list.disc0 = l-op.deci1[2] 
    s-list.disc2 = l-op.rueckgabegrund / 100 
    s-list.disc20 = l-op.rueckgabegrund / 100 
    s-list.disc-amt = brutto * l-op.deci1[2] * 0.01 
    s-list.vat = l-op.deci1[3] 
    s-list.vat0 = l-op.deci1[3] 
    s-list.vat-amt = s-list.warenwert * s-list.vat * 0.01 
    s-list.betriebsnr = l-op.betriebsnr 
    s-list.s-recid = RECID(l-op). 
 
  IF l-op.flag THEN 
  DO: 
    FIND FIRST l-op1 WHERE l-op1.artnr = l-op.artnr 
      AND l-op1.datum = l-op.datum 
      AND l-op1.lscheinnr = l-op.lscheinnr 
      AND l-op1.op-art = 3 AND l-op1.flag 
      AND l-op1.lief-nr = l-op.lief-nr EXCLUSIVE-LOCK NO-ERROR. 
    IF AVAILABLE l-op1 THEN 
    DO: 
      l-op1.warenwert = l-op1.warenwert + l-op.warenwert. 
      FIND CURRENT l-op1 NO-LOCK. 
    END. 
  END. 
  ELSE RUN reorg-oh1. 
 
  ASSIGN
    tot-amt     = tot-amt + brutto
    tot-disc    = tot-disc + s-list.disc-amt 
    tot-disc2   = tot-disc2 + s-list.disc2-amt 
    tot-vat     = tot-vat + s-list.vat-amt
    tot-val     = tot-amt - tot-disc - tot-disc2 + tot-vat
  .
  
END. 

PROCEDURE reorg-oh1: 
DEFINE VARIABLE oh-anz AS DECIMAL. 
DEFINE VARIABLE oh-wert AS DECIMAL. 
DEFINE buffer l-art FOR l-artikel. 
  FIND FIRST l-art WHERE l-art.artnr = l-op.artnr NO-LOCK. 
  IF (l-art.endkum = f-endkum OR l-art.endkum = b-endkum) 
    AND l-op.datum GT fb-closedate THEN RETURN. 
  ELSE IF l-art.endkum GE m-endkum AND l-op.datum GT m-closedate THEN RETURN. 
 
  FIND FIRST l-bestand WHERE l-bestand.lager-nr EQ 0 AND 
    l-bestand.artnr = l-op.artnr EXCLUSIVE-LOCK NO-ERROR. 
  IF AVAILABLE l-bestand THEN 
  DO: 
    l-bestand.wert-eingang = l-bestand.wert-eingang + l-op.warenwert. 
    oh-anz = l-bestand.anz-anf-best + l-bestand.anz-eingang 
      - l-bestand.anz-ausgang. 
    oh-wert = l-bestand.val-anf-best + l-bestand.wert-eingang 
      - l-bestand.wert-ausgang. 
    FIND CURRENT l-art EXCLUSIVE-LOCK. 
    l-art.vk-preis = oh-wert / oh-anz. 
    FIND CURRENT l-art NO-LOCK. 
  END. 
  FIND FIRST l-bestand WHERE l-bestand.lager-nr EQ l-op.lager-nr AND 
    l-bestand.artnr = l-op.artnr EXCLUSIVE-LOCK NO-ERROR. 
  IF AVAILABLE l-bestand THEN 
  DO: 
    l-bestand.wert-eingang = l-bestand.wert-eingang + l-op.warenwert. 
    oh-anz = l-bestand.anz-anf-best + l-bestand.anz-eingang 
      - l-bestand.anz-ausgang. 
    IF oh-anz < 0 THEN 
    DO: 
      msg-str = msg-str + CHR(2) + "&W"
              + translateExtended ("Onhand becomes negative",lvCAREA,"") + " " + STRING(l-art.artnr) + ": "
              + STRING(oh-anz).
    END. 
  END. 
 
  FIND FIRST l-kredit WHERE l-kredit.lief-nr = l-op.lief-nr 
    AND l-kredit.name = l-op.docu-nr 
    AND l-kredit.lscheinnr = l-op.lscheinnr 
    AND l-kredit.opart = 0 AND l-kredit.zahlkonto = 0 EXCLUSIVE-LOCK NO-ERROR. 
  IF AVAILABLE l-kredit THEN 
  DO: 
    l-kredit.saldo = l-kredit.saldo + l-op.warenwert. 
    l-kredit.netto = l-kredit.netto + l-op.warenwert. 
    FIND CURRENT l-kredit NO-LOCK. 
  END. 
 
/* UPDATE supplier turnover */ 
  FIND FIRST  l-liefumsatz WHERE l-liefumsatz.lief-nr = l-op.lief-nr 
    AND l-liefumsatz.datum = l-op.datum EXCLUSIVE-LOCK NO-ERROR. 
  IF AVAILABLE l-liefumsatz THEN 
  DO: 
    l-liefumsatz.gesamtumsatz 
      = l-liefumsatz.gesamtumsatz + l-op.warenwert. 
    FIND CURRENT l-liefumsatz NO-LOCK. 
  END. 
END. 
