DEFINE TEMP-TABLE output-list   
    FIELD counter   AS INT INIT 0
    FIELD str       AS CHAR
    FIELD pos       AS INT INIT 1.

DEFINE INPUT PARAMETER sorttype     AS INTEGER  NO-UNDO.
DEFINE INPUT PARAMETER s-artnr      AS INTEGER  NO-UNDO.
DEFINE OUTPUT PARAMETER TABLE FOR output-list.

DEFINE buffer l-price1 FOR l-pprice. 
DEFINE buffer l-supply FOR l-lieferant. 
DEFINE buffer l-art1 FOR l-artikel. 

DEFINE VARIABLE total-anzahl AS INTEGER FORMAT "9999".
DEFINE VARIABLE total-einzelpreis AS DECIMAL FORMAT "->>>,>>>,>>9.99".
DEFINE VARIABLE total-warenwert AS DECIMAL FORMAT "->>>,>>>,>>9.99".

DEFINE VARIABLE i   AS INT  INIT 0.
DEFINE VARIABLE long-digit AS LOGICAL. 
FIND FIRST htparam WHERE paramnr = 246 NO-LOCK. 
long-digit = htparam.flogical. 

DEFINE VARIABLE curr-remark AS CHARACTER.

IF sorttype = 1 THEN 
FOR EACH l-price1 WHERE l-price1.artnr = s-artnr NO-LOCK, 
  FIRST l-art1 WHERE l-art1.artnr = l-price1.artnr NO-LOCK, 
  FIRST l-supply WHERE l-supply.lief-nr = l-price1.lief-nr NO-LOCK 
  BY l-price1.bestelldatum descending BY l-price1.einzelpreis: 
  i = i + 1.
  CREATE output-list.
  output-list.counter = i.
  IF NOT long-digit THEN 
  DO:
      ASSIGN output-list.str = 
              STRING(l-price1.bestelldatum, "99/99/99") + " " +
              STRING(l-supply.firma, "x(24)") + " " + 
              STRING(l-price1.docu-nr, "x(16)") + " " + 
              STRING(l-art1.traubensort, "x(9)") + " " + 
              STRING(l-art1.lief-einheit, ">>>,>>9") + " " + 
              STRING(l-price1.anzahl) + " " + 
              STRING(l-price1.einzelpreis, "->>,>>>,>>9.99") + " " + 
              STRING(l-price1.warenwert, "->>,>>>,>>9.99")
              . 
        total-anzahl = total-anzahl + l-price1.anzahl.
        total-einzelpreis = total-einzelpreis + l-price1.einzelpreis.
        total-warenwert = total-warenwert + l-price1.warenwert.

        /*sis 220814*/
        FIND FIRST l-order WHERE l-order.docu-nr = l-price1.docu-nr
            AND l-order.lief-nr = l-price1.lief-nr 
            AND l-order.artnr = s-artnr NO-LOCK NO-ERROR.
        IF AVAILABLE l-order THEN 
        DO:
            curr-remark = REPLACE(l-order.besteller, CHR(10),  ";").
            output-list.str = output-list.str + " " + STRING(curr-remark, "x(32)").
        END.
        /*end sis*/
  END.
  ELSE
  DO: 
      ASSIGN output-list.str =
            STRING(l-price1.bestelldatum, "99/99/99") + " " +
            STRING(l-supply.firma, "x(24)") + " " + 
            STRING(l-price1.docu-nr, "x(16)") + " " + 
            STRING(l-art1.traubensort, "x(9)") + " " + 
            STRING(l-art1.lief-einheit, ">>>,>>9") + " " + 
            STRING(l-price1.anzahl) + " " +
            STRING(l-price1.einzelpreis, "->,>>>,>>>,>>9") + " " + 
            STRING(l-price1.warenwert, "->,>>>,>>>,>>9")
            . 
      total-anzahl = total-anzahl + l-price1.anzahl.
      total-einzelpreis = total-einzelpreis + l-price1.einzelpreis.
      total-warenwert = total-warenwert + l-price1.warenwert.
      /*sis 220814*/
      FIND FIRST l-order WHERE l-order.docu-nr = l-price1.docu-nr
            AND l-order.lief-nr = l-price1.lief-nr 
            AND l-order.artnr = s-artnr NO-LOCK NO-ERROR.
      IF AVAILABLE l-order THEN 
      DO:
          curr-remark = REPLACE(l-order.besteller, CHR(10),  ";").
          output-list.str = output-list.str + " " + STRING(curr-remark, "x(32)").
      END.
      /*end sis*/
  END.
END. 
ELSE IF sorttype = 2 THEN 
FOR EACH l-price1 WHERE l-price1.artnr = s-artnr NO-LOCK, 
  FIRST l-art1 WHERE l-art1.artnr = l-price1.artnr NO-LOCK, 
  FIRST l-supply WHERE l-supply.lief-nr = l-price1.lief-nr NO-LOCK 
  BY l-supply.firma BY l-price1.bestelldatum descending: 
  i = i + 1.
  CREATE output-list.
  output-list.counter = i.
  IF NOT long-digit THEN 
  DO:
  ASSIGN output-list.str =
            STRING(l-price1.bestelldatum, "99/99/99") + " " +
            STRING(l-supply.firma, "x(24)") + " " + 
            STRING(l-price1.docu-nr, "x(16)") + " " + 
            STRING(l-art1.traubensort, "x(9)") + " " + 
            STRING(l-art1.lief-einheit, ">>>,>>9") + " " + 
            STRING(l-price1.anzahl) + " " +
            STRING(l-price1.einzelpreis, "->>,>>>,>>9.99") + " " + 
            STRING(l-price1.warenwert, "->>,>>>,>>9.99"). 

          total-anzahl = total-anzahl + l-price1.anzahl.
          total-einzelpreis = total-einzelpreis + l-price1.einzelpreis.
          total-warenwert = total-warenwert + l-price1.warenwert.
          /*sis 220814*/
          FIND FIRST l-order WHERE l-order.docu-nr = l-price1.docu-nr
            AND l-order.lief-nr = l-price1.lief-nr 
            AND l-order.artnr = s-artnr NO-LOCK NO-ERROR.
          IF AVAILABLE l-order THEN 
          DO:
              curr-remark = REPLACE(l-order.besteller, CHR(10),  ";").
              output-list.str = output-list.str + " " + STRING(curr-remark, "x(32)").
          END.
          /*end sis*/
  END.
  ELSE 
  DO:
  ASSIGN output-list.str =
            STRING(l-price1.bestelldatum, "99/99/99") + " " +
            STRING(l-supply.firma, "x(24)") + " " + 
            STRING(l-price1.docu-nr, "x(16)") + " " + 
            STRING(l-art1.traubensort, "x(9)") + " " + 
            STRING(l-art1.lief-einheit, ">>>,>>9") + " " + 
            STRING(l-price1.anzahl) + " " +
            STRING(l-price1.einzelpreis, "->,>>>,>>>,>>9") + " " + 
            STRING(l-price1.warenwert, "->,>>>,>>>,>>9").       
          
          total-anzahl = total-anzahl + l-price1.anzahl.
          total-einzelpreis = total-einzelpreis + l-price1.einzelpreis.
          total-warenwert = total-warenwert + l-price1.warenwert.
          /*sis 220814*/
          FIND FIRST l-order WHERE l-order.docu-nr = l-price1.docu-nr
            AND l-order.lief-nr = l-price1.lief-nr 
            AND l-order.artnr = s-artnr NO-LOCK NO-ERROR.
          IF AVAILABLE l-order THEN 
          DO:
              curr-remark = REPLACE(l-order.besteller, CHR(10),  ";").
              output-list.str = output-list.str + " " + STRING(curr-remark, "x(32)").
          END.
          /*end sis*/
  END.
END. 
ELSE IF sorttype = 3 THEN 
FOR EACH l-price1 WHERE l-price1.artnr = s-artnr NO-LOCK, 
  FIRST l-art1 WHERE l-art1.artnr = l-price1.artnr NO-LOCK, 
  FIRST l-supply WHERE l-supply.lief-nr = l-price1.lief-nr NO-LOCK 
  BY l-price1.einzelpreis BY l-price1.bestelldatum: 
  i = i + 1.
  CREATE output-list.
  output-list.counter = i.
  IF NOT long-digit THEN 
  DO:
      ASSIGN output-list.str =
                STRING(l-price1.bestelldatum, "99/99/99") + " " +
                STRING(l-supply.firma, "x(24)") + " " + 
                STRING(l-price1.docu-nr, "x(16)") + " " + 
                STRING(l-art1.traubensort, "x(9)") + " " + 
                STRING(l-art1.lief-einheit, ">>>,>>9") + " " + 
                STRING(l-price1.anzahl) + " " +
                STRING(l-price1.einzelpreis, "->>,>>>,>>9.99") + " " + 
                STRING(l-price1.warenwert, "->>,>>>,>>9.99"). 

          total-anzahl = total-anzahl + l-price1.anzahl.
          total-einzelpreis = total-einzelpreis + l-price1.einzelpreis.
          total-warenwert = total-warenwert + l-price1.warenwert.
          /*sis 220814*/
          FIND FIRST l-order WHERE l-order.docu-nr = l-price1.docu-nr
            AND l-order.lief-nr = l-price1.lief-nr 
            AND l-order.artnr = s-artnr NO-LOCK NO-ERROR.
          IF AVAILABLE l-order THEN 
          DO:
              curr-remark = REPLACE(l-order.besteller, CHR(10),  ";").
              output-list.str = output-list.str + " " + STRING(curr-remark, "x(32)").
          END.
          /*end sis*/
  END.
  ELSE 
  DO:
      ASSIGN output-list.str = 
                STRING(l-price1.bestelldatum, "99/99/99") + " " +
                STRING(l-supply.firma, "x(24)") + " " + 
                STRING(l-price1.docu-nr, "x(16)") + " " + 
                STRING(l-art1.traubensort, "x(9)") + " " + 
                STRING(l-art1.lief-einheit, ">>>,>>9") + " " + 
                STRING(l-price1.anzahl) + " " +
                STRING(l-price1.einzelpreis, "->,>>>,>>>,>>9") + " " + 
                STRING(l-price1.warenwert, "->,>>>,>>>,>>9"). 

      total-anzahl = total-anzahl + l-price1.anzahl.
      total-einzelpreis = total-einzelpreis + l-price1.einzelpreis.
      total-warenwert = total-warenwert + l-price1.warenwert.
      /*sis 220814*/
      FIND FIRST l-order WHERE l-order.docu-nr = l-price1.docu-nr
            AND l-order.lief-nr = l-price1.lief-nr 
            AND l-order.artnr = s-artnr NO-LOCK NO-ERROR.
      IF AVAILABLE l-order THEN 
      DO:
          curr-remark = REPLACE(l-order.besteller, CHR(10),  ";").
          output-list.str = output-list.str + " " + STRING(curr-remark, "x(32)").
      END.
      /*end sis*/
  END.
END.

CREATE output-list.
    output-list.str = '~n' + "T o t a l"
        + STRING(" ", "x(60)")
        + STRING(total-anzahl, "9999")
        + STRING(total-einzelpreis, "->>,>>>,>>9.99")
        + STRING(" ", "x(1)")
        + STRING(total-warenwert, "->>,>>>,>>9.99").

    ASSIGN output-list.counter = i.
