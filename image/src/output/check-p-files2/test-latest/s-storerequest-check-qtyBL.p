DEFINE TEMP-TABLE op-list LIKE l-op 
  FIELD bezeich  AS CHAR FORMAT "x(36)"             COLUMN-LABEL "Description" 
  FIELD username AS CHAR FORMAT "x(16)"             COLUMN-LABEL "Created by" 
  FIELD onhand   AS DECIMAL FORMAT "->,>>>,>>9.99"  COLUMN-LABEL "On-Hand"
  FIELD acct-bez AS CHAR
  FIELD masseinheit AS CHAR FORMAT "x(20)" 
.

DEF INPUT PARAMETER pvILanguage AS INTEGER  NO-UNDO.
DEF INPUT PARAMETER TABLE FOR op-list.
DEF OUTPUT PARAMETER its-ok AS LOGICAL INITIAL YES.
DEF OUTPUT PARAMETER msg-str AS CHAR.

{SupertransBL.i} 
DEF VAR lvCAREA AS CHAR INITIAL "s-storerequest".

RUN check-qty.

PROCEDURE check-qty: 
DEFINE VARIABLE curr-oh AS DECIMAL. 
  FOR EACH op-list: 
    ASSIGN curr-oh = 0.
    FIND FIRST l-bestand WHERE l-bestand.artnr = op-list.artnr 
      AND l-bestand.lager-nr = op-list.lager-nr NO-LOCK NO-ERROR.
    IF AVAILABLE l-bestand THEN curr-oh = l-bestand.anz-anf-best 
      + l-bestand.anz-eingang - l-bestand.anz-ausgang. 
    IF curr-oh LT op-list.anzahl THEN 
    DO: 
      FIND FIRST l-artikel WHERE l-artikel.artnr = op-list.artnr NO-LOCK. 
      msg-str = msg-str + CHR(2)
              + translateExtended ("Wrong quantity: ",lvCAREA,"") + STRING(l-artikel.artnr) + " - "
              + l-artikel.bezeich
              + CHR(10)
              + translateExtended ("Inputted quantity =",lvCAREA,"")
              + " " + STRING(op-list.anzahl)
              + translateExtended (" - Stock onhand =",lvCAREA,"") + " " + STRING(curr-oh)
              + CHR(10)
              + translateExtended ("POSTING NOT POSSIBLE",lvCAREA,"").
      its-ok = NO. 
      RETURN. 
    END. 
  END. 
END. 
