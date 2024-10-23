
DEFINE TEMP-TABLE op-list LIKE l-op
    FIELD bezeich LIKE l-artikel.bezeich
    FIELD username LIKE bediener.username.

DEF INPUT PARAMETER TABLE FOR op-list.
DEF INPUT  PARAMETER pvILanguage    AS INTEGER NO-UNDO.
DEF OUTPUT PARAMETER its-ok AS LOGICAL INITIAL YES. 
DEF OUTPUT PARAMETER msg-str AS CHAR.

DEFINE VARIABLE curr-oh AS DECIMAL. 

{SupertransBL.i} 
DEF VAR lvCAREA AS CHAR INITIAL "s-transform".

FOR EACH op-list: 
    FIND FIRST l-bestand WHERE l-bestand.artnr = op-list.artnr 
      AND l-bestand.lager-nr = op-list.lager-nr NO-LOCK. 
    curr-oh = anz-anf-best + anz-eingang - anz-ausgang. 
    IF curr-oh LT op-list.anzahl THEN 
    DO: 
      FIND FIRST l-artikel WHERE l-artikel.artnr = op-list.artnr NO-LOCK. 
      msg-str = msg-str + CHR(2)
              + translateExtended ("Wrong quantity: ",lvCAREA,"") 
              + STRING(l-artikel.artnr) + " - " 
              + l-artikel.bezeich 
              + CHR(10)
              + translateExtended ("Inputted quantity =",lvCAREA,"") + " " 
              + STRING(op-list.anzahl) 
              + translateExtended (" - Stock onhand =",lvCAREA,"") + " " 
              + STRING(curr-oh) 
              + CHR(10)
              + translateExtended ("POSTING NOT POSSIBLE",lvCAREA,"") .
      its-ok = NO.
      RETURN. 
    END. 
END.
