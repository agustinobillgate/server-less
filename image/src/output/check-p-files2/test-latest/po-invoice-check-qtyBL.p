
DEFINE INPUT  PARAMETER pvILanguage     AS INTEGER  NO-UNDO.
DEFINE INPUT  PARAMETER qty             AS DECIMAL NO-UNDO. 
DEFINE INPUT  PARAMETER s-list-s-recid  AS INT.
DEFINE INPUT  PARAMETER s-list-artnr    AS INT.
DEFINE OUTPUT PARAMETER msg-str         AS CHAR.
DEFINE OUTPUT PARAMETER may-chg         AS LOGICAL INITIAL YES. 

{SupertransBL.i} 
DEF VAR lvCAREA AS CHAR INITIAL "po-invoice".

RUN check-qty.

PROCEDURE check-qty:
DEFINE VARIABLE f-endkum AS INTEGER NO-UNDO. 
DEFINE VARIABLE b-endkum AS INTEGER NO-UNDO. 
DEFINE VARIABLE m-endkum AS INTEGER NO-UNDO. 
DEFINE VARIABLE billdate AS DATE NO-UNDO. 
DEFINE VARIABLE fb-closedate AS DATE NO-UNDO. 
DEFINE VARIABLE m-closedate AS DATE NO-UNDO. 
DEFINE VARIABLE qty1 AS DECIMAL NO-UNDO. 
DEFINE buffer l-art FOR l-artikel.
 
  FIND FIRST l-op WHERE RECID(l-op) = s-list-s-recid NO-LOCK. 
  IF l-op.flag THEN return.  /* indicates direct issue */ 
 
  FIND FIRST htparam WHERE paramnr = 257 NO-LOCK. 
  f-endkum = htparam.finteger.               /* Rulita 211024 | Fixing for serverless */  
  FIND FIRST htparam WHERE paramnr = 258 NO-LOCK. 
  b-endkum = htparam.finteger.               /* Rulita 211024 | Fixing for serverless */  
  FIND FIRST htparam WHERE paramnr = 268 NO-LOCK. 
  m-endkum = htparam.finteger.               /* Rulita 211024 | Fixing for serverless */  
  FIND FIRST htparam WHERE paramnr = 224 NO-LOCK. 
  fb-closedate = htparam.fdate. 
  FIND FIRST htparam WHERE paramnr = 221 NO-LOCK. 
  m-closedate = htparam.fdate. 
  FIND FIRST l-art WHERE l-art.artnr = s-list-artnr NO-LOCK. 
  IF ((l-art.endkum = f-endkum OR l-art.endkum = b-endkum) 
    AND l-op.datum GT fb-closedate) OR (l-art.endkum GE m-endkum 
    AND l-op.datum GT m-closedate) THEN RETURN. 
 
  FIND FIRST l-bestand WHERE l-bestand.artnr = l-op.artnr 
    AND l-bestand.lager-nr = l-op.lager-nr NO-LOCK NO-ERROR. 
  qty1 = l-bestand.anz-anf-best + l-bestand.anz-eingang - l-bestand.anz-ausgang 
    + qty - l-op.anzahl. 
  IF qty1 LT 0 THEN 
  DO:
    msg-str = msg-str + CHR(2)
            + translateExtended ("Onhand QTY in Store ",lvCAREA,"") + STRING(l-op.lager-nr,"99") 
            + " " + translateExtended ("would become negative",lvCAREA,"") + " = " + TRIM(STRING(qty1,"->>>,>>>,>>9.99")) 
            + CHR(10)
            + translateExtended ("The entered QTY is therefore not possible.",lvCAREA,"").
    may-chg = NO.
  END. 
END. 
