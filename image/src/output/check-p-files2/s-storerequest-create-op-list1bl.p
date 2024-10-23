DEFINE TEMP-TABLE op-list LIKE l-op 
  FIELD bezeich  AS CHAR FORMAT "x(36)"             COLUMN-LABEL "Description" 
  FIELD username AS CHAR FORMAT "x(16)"             COLUMN-LABEL "Created by" 
  FIELD onhand   AS DECIMAL FORMAT "->,>>>,>>9.99"  COLUMN-LABEL "On-Hand"
  FIELD acct-bez AS CHAR
.

DEFINE TEMP-TABLE op-list1 LIKE op-list. 

DEFINE INPUT PARAMETER pvILanguage  AS INTEGER  NO-UNDO.
DEFINE INPUT PARAMETER p-artnr      AS INTEGER.
DEFINE INPUT PARAMETER menge        AS DECIMAL.
DEFINE INPUT-OUTPUT PARAMETER oh-ok AS LOGICAL. 

DEFINE INPUT PARAMETER curr-lager   AS INT.
DEFINE INPUT PARAMETER transdate    AS DATE.
DEFINE INPUT PARAMETER lscheinnr    AS CHAR.
DEFINE INPUT PARAMETER bediener-nr  AS INT.

DEFINE OUTPUT PARAMETER msg-str     AS CHAR.
DEFINE OUTPUT PARAMETER TABLE FOR op-list1.

{SupertransBL.i} 
DEF VAR lvCAREA AS CHAR INITIAL "s-storerequest".

DEFINE VARIABLE amount      AS DECIMAL FORMAT "->,>>>,>>>,>>9.99". 
DEFINE VARIABLE t-amount    AS DECIMAL FORMAT "->>,>>>,>>>,>>9.99". 

DEFINE BUFFER sys-user FOR bediener. 

RUN create-op-list1.

PROCEDURE create-op-list1: 
DEFINE VARIABLE stock-oh AS DECIMAL. 
DEFINE VARIABLE inh      AS DECIMAL FORMAT "->,>>>,>>9.999". 
DEFINE BUFFER l-art      FOR l-artikel. 
 
  FOR EACH h-rezlin WHERE h-rezlin.artnrrezept = p-artnr NO-LOCK:
    inh = menge * h-rezlin.menge.
    IF h-rezlin.recipe-flag = YES THEN 
      RUN create-op-list1(h-rezlin.artnrlager, inh).
    ELSE
    DO:
      FIND FIRST l-art WHERE l-art.artnr = h-rezlin.artnrlager NO-LOCK. 
      FIND FIRST l-bestand WHERE l-bestand.lager-nr = curr-lager 
        AND l-bestand.artnr = h-rezlin.artnrlager NO-LOCK NO-ERROR. 
      IF NOT AVAILABLE l-bestand THEN 
      DO: 
        msg-str = msg-str + CHR(2)
                + translateExtended ("Article ",lvCAREA,"") + STRING(l-art.artnr,"9999999") + " - " 
                + l-art.bezeich + " not found, posting not possible.".
        oh-ok = NO. 
        RETURN. 
      END. 
      stock-oh = l-bestand.anz-anf-best + l-bestand.anz-eingang 
          - l-bestand.anz-ausgang. 
      inh = inh / l-art.inhalt. 
      IF inh GT stock-oh THEN 
      DO: 
        msg-str = msg-str + CHR(2)
                + translateExtended ("Quantity over stock-onhand: ",lvCAREA,"") + STRING(l-art.artnr,"9999999") 
                + " - " + l-art.bezeich 
                + CHR(10)
                + "  (" + STRING(inh) + " > " + STRING(stock-oh) 
                + translateExtended ("), posting not possible.",lvCAREA,"").
        oh-ok = NO. 
        RETURN. 
      END. 
      amount = inh * l-art.vk-preis / (1 - h-rezlin.lostfact / 100). 
      t-amount = t-amount + amount. 
      CREATE op-list1. 
      ASSIGN
        op-list1.datum        = transdate
        op-list1.lager-nr     = curr-lager 
        op-list1.artnr        = l-art.artnr 
        op-list1.zeit         = TIME
        op-list1.anzahl       = inh 
        op-list1.einzelpreis  = l-art.vk-preis 
        op-list1.warenwert    = amount
        op-list1.op-art       = 13
        op-list1.herkunftflag = 1 
        op-list1.lscheinnr    = lscheinnr 
        op-list1.fuellflag    = bediener-nr 
        op-list1.pos          = 1
      . 
      FIND FIRST l-art WHERE l-art.artnr = op-list1.artnr NO-LOCK.
      FIND FIRST sys-user WHERE sys-user.nr = op-list1.fuellflag NO-LOCK.
      FIND FIRST l-bestand WHERE l-bestand.artnr = op-list1.artnr
        AND l-bestand.lager-nr = curr-lager NO-LOCK NO-ERROR.
      ASSIGN
        op-list1.bezeich  = l-art.bezeich
        op-list1.username = sys-user.username
      .
      FIND FIRST gl-acct WHERE gl-acct.fibukonto = op-list1.stornogrund NO-LOCK
          NO-ERROR.
      IF AVAILABLE gl-acct THEN 
          op-list1.acct-bez = gl-acct.bezeich.

      IF AVAILABLE l-bestand THEN op-list1.onhand = l-bestand.anz-anf-best
        + l-bestand.anz-eingang - l-bestand.anz-ausgang.
      END.
    END.
END.
