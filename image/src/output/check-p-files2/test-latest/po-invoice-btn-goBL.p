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

DEFINE INPUT PARAMETER pvILanguage  AS INT  NO-UNDO.
DEF INPUT-OUTPUT PARAMETER TABLE FOR s-list.
DEF INPUT PARAMETER f-endkum        AS INT.
DEF INPUT PARAMETER b-endkum        AS INT.
DEF INPUT PARAMETER m-endkum        AS INT.
DEF INPUT PARAMETER fb-closedate    AS DATE.
DEF INPUT PARAMETER m-closedate     AS DATE.
DEF INPUT PARAMETER lscheinnr       AS CHAR.

DEF OUTPUT PARAMETER tot-amt      AS DECIMAL.
DEF OUTPUT PARAMETER tot-disc     AS DECIMAL.
DEF OUTPUT PARAMETER tot-disc2    AS DECIMAL.
DEF OUTPUT PARAMETER tot-vat      AS DECIMAL.
DEF OUTPUT PARAMETER tot-val      AS DECIMAL.
DEF OUTPUT PARAMETER confirm-flag AS LOGICAL INITIAL YES. 
DEF OUTPUT PARAMETER msg-str AS CHAR.
DEF OUTPUT PARAMETER msg-str2 AS CHAR.

{ supertransbl.i } 
DEF VAR lvCAREA AS CHAR INITIAL "po-invoice". 

RUN do-adjustment. 
RUN create-list.

PROCEDURE do-adjustment: 
DEFINE BUFFER l-op1 FOR l-op. 
  tot-amt = 0. 
  tot-vat = 0. 
  tot-disc = 0. 
  tot-disc2 = 0. 
  FOR EACH s-list BY s-list.bezeich BY s-list.betriebsnr: 
    IF (s-list.anzahl NE s-list.anz0) 
      OR (s-list.einzelpreis NE s-list.price0) 
      OR (s-list.disc NE s-list.disc0) 
      OR (s-list.disc2 NE s-list.disc20) 
      OR (s-list.vat NE s-list.vat0) THEN 
    DO: 
      
      FIND FIRST l-op WHERE RECID(l-op) = s-list.s-recid EXCLUSIVE-LOCK. 
      ASSIGN 
          l-op.anzahl = s-list.anzahl 
          l-op.deci1[1] = s-list.einzelpreis 
          l-op.deci1[2] = s-list.disc 
          l-op.deci1[3] = s-list.vat 
          l-op.rueckgabegrund = s-list.disc2 * 100 
          l-op.einzelpreis = s-list.einzelpreis * (1 - s-list.disc * 0.01) 
            * (1 - s-list.disc2 * 0.01) 
          l-op.warenwert = s-list.warenwert 
          l-op.deci1[4] = l-op.warenwert * l-op.deci1[3] * 0.01. 
      FIND CURRENT l-op NO-LOCK. 
 
      IF l-op.flag /* direct issue */ THEN 
      DO: 
        FIND FIRST l-op1 WHERE l-op1.artnr = l-op.artnr 
            AND l-op1.datum = l-op.datum 
            AND l-op1.lscheinnr = l-op.lscheinnr 
            AND l-op1.op-art = 3 AND l-op1.flag 
            AND l-op1.lief-nr = l-op.lief-nr EXCLUSIVE-LOCK NO-ERROR. 
        IF AVAILABLE l-op1 THEN 
        DO: 
          IF l-op.betriebsnr LE 1 THEN l-op1.warenwert = l-op.warenwert. 
          ELSE l-op1.warenwert = l-op1.warenwert + l-op.warenwert. 
          FIND CURRENT l-op1 NO-LOCK. 
        END. 
      END. 
      RUN reorg-oh(l-op.flag). 
    END.
  END.
  FOR EACH s-list:
    ASSIGN
      s-list.anz0 = s-list.anzahl
      s-list.price0 = s-list.einzelpreis 
      s-list.disc0 = s-list.disc
      s-list.disc20 = s-list.disc2 
      s-list.vat0 = s-list.vat
      s-list.val0 = s-list.warenwert
    .
  END.
END. 


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

    /*ITA 180516 cek purchase book*/
    FIND FIRST l-pprice WHERE l-pprice.artnr = l-op.artnr
      AND l-pprice.bestelldatum = l-op.datum 
      AND l-pprice.lief-nr = l-op.lief-nr 
      AND l-pprice.docu-nr = l-op.docu-nr NO-LOCK NO-ERROR.
    IF AVAILABLE l-pprice THEN DO:
        FIND CURRENT l-pprice EXCLUSIVE-LOCK.
        ASSIGN 
            l-pprice.anzahl      = l-op.anzahl
            l-pprice.einzelpreis = l-op.einzelpreis
            l-pprice.warenwert   = l-op.warenwert.
        FIND CURRENT l-pprice NO-LOCK.
        RELEASE l-pprice.
    END.

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


PROCEDURE reorg-oh: 
DEF INPUT PARAMETER direct-issue AS LOGICAL.
DEFINE VARIABLE oh-anz AS DECIMAL. 
DEFINE VARIABLE oh-wert AS DECIMAL. 
DEFINE buffer l-art FOR l-artikel. 

  FIND FIRST htparam WHERE htparam.paramnr = 1016 NO-LOCK.
  IF htparam.flogical THEN
  DO:
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
      l-kredit.saldo = l-kredit.saldo - s-list.val0 + s-list.warenwert. 
      l-kredit.netto = l-kredit.netto - s-list.val0 + s-list.warenwert. 
      FIND CURRENT l-kredit NO-LOCK. 
    END.
    ELSE
    DO:
      msg-str = msg-str + CHR(2) + "&W"
              + translateExtended ("A/P record not found!",lvCAREA,"").
    END.
  END.
 
  /* UPDATE supplier turnover */ 
  FIND FIRST  l-liefumsatz WHERE l-liefumsatz.lief-nr = l-op.lief-nr 
    AND l-liefumsatz.datum = s-list.datum EXCLUSIVE-LOCK NO-ERROR. 
  IF AVAILABLE l-liefumsatz THEN 
  DO: 
    l-liefumsatz.gesamtumsatz 
      = l-liefumsatz.gesamtumsatz - s-list.val0 + s-list.warenwert. 
    FIND CURRENT l-liefumsatz NO-LOCK. 
  END. 
  
  IF direct-issue THEN RETURN.

  IF (s-list.anzahl EQ s-list.anz0) AND (s-list.einzelpreis EQ s-list.price0) 
    AND (s-list.disc EQ s-list.disc0) AND (s-list.disc2 EQ s-list.disc20) 
    AND (s-list.val0 EQ s-list.warenwert)  THEN RETURN. 
  FIND FIRST l-art WHERE l-art.artnr = s-list.artnr NO-LOCK. 
  IF (l-art.endkum = f-endkum OR l-art.endkum = b-endkum) 
    AND s-list.datum GT fb-closedate THEN RETURN. 
  ELSE IF l-art.endkum GE m-endkum AND s-list.datum GT m-closedate THEN RETURN. 
 
  FIND FIRST l-bestand WHERE l-bestand.lager-nr EQ 0 AND 
    l-bestand.artnr = l-op.artnr EXCLUSIVE-LOCK NO-ERROR. 
  IF AVAILABLE l-bestand THEN 
  DO: 
    l-bestand.anz-eingang = l-bestand.anz-eingang 
      - s-list.anz0 + s-list.anzahl. 
    l-bestand.wert-eingang = l-bestand.wert-eingang 
      - s-list.val0 + s-list.warenwert. 
    oh-anz = l-bestand.anz-anf-best + l-bestand.anz-eingang 
      - l-bestand.anz-ausgang. 
    IF oh-anz NE 0 THEN 
    DO: 
      oh-wert = l-bestand.val-anf-best + l-bestand.wert-eingang 
      - l-bestand.wert-ausgang. 
      FIND CURRENT l-art EXCLUSIVE-LOCK. 
      l-art.vk-preis = oh-wert / oh-anz. 
        FIND CURRENT l-art NO-LOCK. 
    END. 
  END. 
  FIND FIRST l-bestand WHERE l-bestand.lager-nr EQ l-op.lager-nr AND 
    l-bestand.artnr = l-op.artnr EXCLUSIVE-LOCK NO-ERROR. 
  IF AVAILABLE l-bestand THEN 
  DO: 
    l-bestand.anz-eingang = l-bestand.anz-eingang 
      - s-list.anz0 + s-list.anzahl. 
    l-bestand.wert-eingang = l-bestand.wert-eingang 
      - s-list.val0 + s-list.warenwert. 
    FIND CURRENT l-bestand NO-LOCK. 
    oh-anz = l-bestand.anz-anf-best + l-bestand.anz-eingang 
      - l-bestand.anz-ausgang. 
    IF oh-anz < 0 THEN 
    DO: 
      msg-str2 = msg-str2 + CHR(2) + "&W"
               + translateExtended ("Onhand becomes negative",lvCAREA,"") + " " 
               + STRING(l-art.artnr) + ": " 
               + STRING(oh-anz).
    END. 
  END. 
END. 
