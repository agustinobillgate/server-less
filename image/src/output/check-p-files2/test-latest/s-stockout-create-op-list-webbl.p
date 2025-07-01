DEF TEMP-TABLE t-l-bestand LIKE l-bestand.
DEF TEMP-TABLE t-h-rezlin LIKE h-rezlin.

DEFINE TEMP-TABLE temp-l-artikel
    FIELD artnr         AS INTEGER
    FIELD bezeich       AS CHARACTER
    FIELD betriebsnr    AS INTEGER
    FIELD endkum        AS INTEGER
    FIELD masseinheit   AS CHARACTER
    FIELD vk-preis      AS DECIMAL
    FIELD inhalt        AS DECIMAL
    FIELD lief-einheit  AS DECIMAL
    FIELD traubensort   AS CHARACTER
.
     
DEFINE TEMP-TABLE op-list LIKE l-op
    FIELD fibu          AS CHAR
    FIELD a-bezeich     AS CHARACTER
    FIELD a-lief-einheit AS DECIMAL
    FIELD a-traubensort AS CHARACTER
.

DEFINE TEMP-TABLE op-list1 LIKE l-op
    FIELD a-lief-einheit AS DECIMAL
    FIELD a-traubensort AS CHARACTER
.

DEFINE INPUT PARAMETER s-artnr AS INTEGER.
DEFINE INPUT PARAMETER curr-lager AS INTEGER.
DEFINE INPUT PARAMETER lscheinnr AS CHARACTER.
DEFINE INPUT PARAMETER transdate AS DATE.
DEFINE INPUT PARAMETER qty AS DECIMAL. 
DEFINE INPUT PARAMETER cost-acct AS CHARACTER.
DEFINE INPUT PARAMETER a-bez AS CHARACTER.
DEFINE INPUT PARAMETER transfered AS LOGICAL.
DEFINE INPUT PARAMETER tp-bediener-nr AS INTEGER.
DEFINE OUTPUT PARAMETER msg-str AS CHARACTER.
DEFINE OUTPUT PARAMETER TABLE FOR op-list.

DEFINE VARIABLE amount AS DECIMAL.
DEFINE VARIABLE t-amount AS DECIMAL.
DEFINE VARIABLE price AS DECIMAL.
DEFINE VARIABLE DESCRIPTION AS CHARACTER.

FIND FIRST l-artikel WHERE l-artikel.artnr = s-artnr NO-LOCK NO-ERROR.
IF AVAILABLE l-artikel THEN
DO:
    ASSIGN
        DESCRIPTION = l-artikel.bezeich + " - " + l-artikel.masseinheit
        price = l-artikel.vk-preis.
    RUN create-op-list.
END.
    

PROCEDURE create-op-list:
DEFINE VARIABLE anzahl AS DECIMAL FORMAT "->,>>>,>>9.999". 
DEFINE VARIABLE wert AS DECIMAL. 
DEFINE VARIABLE oh-ok AS LOGICAL INITIAL YES. 
 
  IF l-artikel.betriebsnr GT 0 THEN
  DO: 
    FOR EACH op-list1:
      DELETE op-list1.
    END.

    RUN s-stockout-h-rezlinbl.p (l-artikel.betriebsnr, curr-lager,
                   OUTPUT TABLE t-l-bestand, OUTPUT TABLE t-h-rezlin).
    RUN create-op-list1(l-artikel.betriebsnr, qty, INPUT-OUTPUT oh-ok).
    IF oh-ok THEN 
    DO: 
      FOR EACH op-list1:
          CREATE op-list.
          op-list.datum = op-list1.datum.
          op-list.lager-nr = op-list1.lager-nr.
          op-list.artnr = op-list1.artnr.
          op-list.zeit = op-list1.zeit.
          op-list.anzahl = op-list1.anzahl.
          op-list.einzelpreis = op-list1.einzelpreis.
          op-list.warenwert = op-list1.warenwert.
          op-list.op-art = op-list1.op-art.
          op-list.herkunftflag = op-list1.herkunftflag.
          op-list.lscheinnr = op-list1.lscheinnr.
          op-list.fuellflag = op-list1.fuellflag.
          op-list.pos = op-list1.pos.
          op-list.a-lief-einheit = op-list1.a-lief-einheit.
          op-list.a-traubensort = op-list1.a-traubensort.

          ASSIGN
                op-list.fibu = cost-acct
                op-list.stornogrund = a-bez.
          /*IF NOT transfered THEN 
              ASSIGN
                op-list.fibu = cost-acct
                op-list.stornogrund = a-bez.*/
      END.
    END.
    RETURN.
  END.
 
  anzahl = qty. 
  wert = qty * price. 
  amount = wert. 
  t-amount = t-amount + wert. 
 
  IF curr-lager = 0 THEN 
  DO: 
    RETURN. 
  END. 
 
  CREATE op-list. 
  ASSIGN
    op-list.datum = transdate
    op-list.lager-nr = curr-lager
    op-list.artnr = s-artnr 
    op-list.zeit = TIME 
    op-list.anzahl = anzahl 
    op-list.einzelpreis = price
    op-list.warenwert = wert 
    op-list.herkunftflag = 1    /* 4 = inventory !!! */ 
    op-list.lscheinnr = lscheinnr 
    op-list.fuellflag = tp-bediener-nr
    op-list.pos = 1 
    op-list.a-bezeich = DESCRIPTION
    op-list.fibu = cost-acct
    op-list.stornogrund = a-bez.

  IF transfered THEN op-list.op-art = 4. 
  ELSE op-list.op-art = 3. 
  
  IF NOT transfered THEN op-list.fibu = cost-acct.
END.

PROCEDURE create-op-list1: 
DEFINE INPUT PARAMETER p-artnr      AS INTEGER. 
DEFINE INPUT PARAMETER menge        AS DECIMAL. 
DEFINE INPUT-OUTPUT PARAMETER oh-ok AS LOGICAL. 
DEFINE VARIABLE stock-oh    AS DECIMAL. 
DEFINE VARIABLE inh         AS DECIMAL FORMAT "->,>>>,>>9.999". 
DEFINE BUFFER l-art FOR temp-l-artikel.
    
  FOR EACH temp-l-artikel:
      DELETE temp-l-artikel.
  END.
  
  RUN s-stockout-create-op-list1bl.p (p-artnr, OUTPUT TABLE temp-l-artikel).

  FOR EACH t-h-rezlin:
    inh = menge * t-h-rezlin.menge. 
    IF t-h-rezlin.recipe-flag = YES THEN
    DO:
        RUN create-op-list1(t-h-rezlin.artnrlager, inh,
          INPUT-OUTPUT oh-ok). 
        IF NOT oh-ok THEN RETURN.
    END.
    ELSE 
    DO: 
      FIND FIRST l-art WHERE l-art.artnr = t-h-rezlin.artnrlager NO-LOCK. 
      FIND FIRST t-l-bestand WHERE t-l-bestand.lager-nr = curr-lager 
        AND t-l-bestand.artnr = t-h-rezlin.artnrlager NO-ERROR. 
      IF NOT AVAILABLE t-l-bestand THEN 
      DO: 
        msg-str = "Article " + STRING(l-art.artnr,"9999999") + " - " + 
          l-art.bezeich + " not found, posting not possible.". 
        oh-ok = NO. 
        RETURN. 
      END. 
      stock-oh = t-l-bestand.anz-anf-best + t-l-bestand.anz-eingang 
          - t-l-bestand.anz-ausgang. 
      inh = inh / l-art.inhalt.
      IF inh GT stock-oh THEN 
      DO: 
        msg-str = "Quantity over stock-onhand: " + STRING(l-art.artnr,"9999999") 
          + " - " + l-art.bezeich + " " + STRING(inh) + " > " + STRING(stock-oh) 
          + ", posting not possible.". 
        oh-ok = NO. 
        RETURN. 
      END. 
      amount = inh * l-art.vk-preis / (1 - t-h-rezlin.lostfact / 100). 
      t-amount = t-amount + amount. 
      CREATE op-list1. 
      ASSIGN
        op-list1.datum = transdate
        op-list1.lager-nr = curr-lager
        op-list1.artnr = l-art.artnr
        op-list1.zeit = TIME
        op-list1.anzahl = inh 
        op-list1.einzelpreis = l-art.vk-preis
        op-list1.warenwert = amount 
        op-list1.op-art = 3 
        op-list1.herkunftflag = 1    /* 4 = inventory !!! */ 
        op-list1.lscheinnr = lscheinnr
        op-list1.fuellflag = tp-bediener-nr
        op-list1.pos = 1
        op-list1.a-lief-einheit = l-art.lief-einheit
        op-list1.a-traubensort = l-art.traubensort.
    END. 
  END. 
END. 
