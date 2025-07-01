
DEFINE INPUT PARAMETER pvILanguage      AS INT  NO-UNDO.
DEFINE INPUT PARAMETER l-orderhdr-docu-nr AS CHAR.
DEFINE OUTPUT PARAMETER msg-str AS CHAR.
DEFINE OUTPUT PARAMETER msg-str1 AS CHAR.

{ supertransbl.i } 
DEF VAR lvCAREA AS CHAR INITIAL "po-list". 

RUN check-del.

PROCEDURE check-del:
/*MTDEFINE OUTPUT PARAMETER answer AS LOGICAL INITIAL NO.*/
DEFINE buffer l-order1 FOR l-order. 
/* 
  FIND FIRST l-order1 WHERE l-order1.docu-nr = l-orderhdr.docu-nr 
    AND l-order1.pos EQ 0 NO-LOCK. 
  IF l-order1.rechnungswert NE 0 THEN 
  DO: 
    HIDE MESSAGE NO-PAUSE. 
    MESSAGE translateExtended ("The purchase order is not balanced, closing not possible.",lvCAREA,"") 
    VIEW-AS ALERT-BOX INFORMATION. 
    RETURN. 
  END. 
*/ 
  FIND FIRST l-order1 WHERE l-order1.docu-nr = l-orderhdr-docu-nr 
    AND l-order1.pos GT 0 AND l-order1.loeschflag = 0 
    AND l-order1.geliefert NE 0 NO-LOCK NO-ERROR. 
  IF NOT AVAILABLE l-order1 THEN 
  DO: 
    msg-str =  msg-str + CHR(2) + "&Q"
            + translateExtended ("Are you sure you want to CLOSE the order document",lvCAREA,"")
            + " " + l-orderhdr-docu-nr + "?".
      /*MTVIEW-AS ALERT-BOX QUESTION BUTTONS YES-NO UPDATE answer.*/
  END. 
  ELSE 
  DO: 
    FIND FIRST l-order1 WHERE l-order1.docu-nr = l-orderhdr-docu-nr 
      AND l-order1.pos GT 0 AND l-order1.loeschflag = 0 
      AND (l-order1.geliefert NE l-order1.anzahl) NO-LOCK NO-ERROR. 
    IF AVAILABLE l-order1 THEN 
    DO: 
      msg-str1 =  msg-str1 + CHR(2) + "&W"
              + translateExtended ("The order items are not yet completely delivered.",lvCAREA,"").
      /*MTVIEW-AS ALERT-BOX WARNING.*/
    END. 
    msg-str =  msg-str + CHR(2) + "&Q"
            + translateExtended ("Are you sure you want to CLOSE the order document",lvCAREA,"") 
            + " " + l-orderhdr-docu-nr + "?".
      /*MTVIEW-AS ALERT-BOX QUESTION BUTTONS YES-NO UPDATE answer.*/
  END. 
END. 
