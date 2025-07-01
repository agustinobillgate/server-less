DEFINE TEMP-TABLE op-list LIKE l-op
    FIELD fibu AS CHAR
    FIELD a-bezeich LIKE l-artikel.bezeich
    FIELD a-lief-einheit LIKE l-artikel.lief-einheit
    FIELD a-traubensort LIKE l-artikel.traubensort.

DEFINE INPUT PARAMETER TABLE FOR op-list.
DEFINE INPUT PARAMETER pvILanguage  AS INTEGER  NO-UNDO.
DEFINE OUTPUT PARAMETER msg-str     AS CHAR.
DEFINE OUTPUT PARAMETER its-ok      AS LOGICAL INITIAL YES. 

{SupertransBL.i} 
DEF VAR lvCAREA AS CHAR INITIAL "s-stockout".

RUN check-qty.

PROCEDURE check-qty:
DEFINE VARIABLE curr-oh     AS DECIMAL. 
DEFINE VARIABLE out-oh      AS DECIMAL.
DEFINE VARIABLE curr-artnr  AS INTEGER.
DEFINE VARIABLE count-artnr AS INTEGER.

  FOR EACH op-list BY op-list.artnr: 
    FIND FIRST l-bestand WHERE l-bestand.artnr = op-list.artnr 
      AND l-bestand.lager-nr = op-list.lager-nr NO-LOCK.

    IF curr-artnr = 0 OR (curr-artnr NE op-list.artnr) THEN 
            ASSIGN curr-oh    = l-bestand.anz-anf-best + l-bestand.anz-eingang - l-bestand.anz-ausgang
                   count-artnr = 0. 

    ASSIGN count-artnr = count-artnr + 1.
    /* Oscar (13/04/25) - ACE54F - adjust for user story 1  */
    IF curr-oh LT op-list.anzahl AND curr-oh GT 0 THEN 
    DO: 
      FIND FIRST l-artikel WHERE l-artikel.artnr = op-list.artnr NO-LOCK.
      IF count-artnr = 1 THEN
          msg-str = msg-str + CHR(2)
                  + translateExtended ("Wrong quantity: ",lvCAREA,"") + STRING(l-artikel.artnr) + " - "
                  + l-artikel.bezeich
                  + CHR(10)
                  + translateExtended ("Inputted quantity =",lvCAREA,"")
                  + " " + STRING(op-list.anzahl)
                  + translateExtended (" - Stock onhand =",lvCAREA,"") + " " + STRING(curr-oh)
                  + CHR(10)
                  + translateExtended ("POSTING NOT POSSIBLE",lvCAREA,"").
      ELSE 
          msg-str = msg-str + CHR(2)
              + translateExtended ("The same article has been found : ",lvCAREA,"") + STRING(l-artikel.artnr) + " - "
              + l-artikel.bezeich
              + CHR(10)
              + translateExtended ("Inputted quantity =",lvCAREA,"")
              + " " + STRING(op-list.anzahl)
              + translateExtended (" - Stock onhand =",lvCAREA,"") + " " + STRING(curr-oh)
              + CHR(10)
              + translateExtended ("POSTING NOT POSSIBLE",lvCAREA,"").

      /*MT*/
      its-ok = NO. 
      RETURN. 
    END.

    ASSIGN out-oh     = op-list.anzahl
           curr-oh    = curr-oh - out-oh
           curr-artnr = op-list.artnr.
  END. 
END. 
