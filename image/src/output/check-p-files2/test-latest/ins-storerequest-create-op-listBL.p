DEFINE TEMP-TABLE op-list LIKE l-op 
  FIELD bezeich  AS CHAR FORMAT "x(36)"             COLUMN-LABEL "Description" 
  FIELD username AS CHAR FORMAT "x(16)"             COLUMN-LABEL "Created by" 
  FIELD onhand   AS DECIMAL FORMAT "->,>>>,>>9.99"  COLUMN-LABEL "On-Hand"
  FIELD new-flag AS LOGICAL INIT YES
.

DEFINE TEMP-TABLE op-list1 LIKE op-list. 

DEFINE TEMP-TABLE out-list 
  FIELD artnr AS INTEGER. 

DEFINE BUFFER sys-user FOR bediener. 

DEF INPUT-OUTPUT PARAMETER TABLE FOR out-list.
DEF INPUT-OUTPUT PARAMETER TABLE FOR op-list.
DEF INPUT-OUTPUT PARAMETER amount   AS DECIMAL.
DEF INPUT-OUTPUT PARAMETER t-amount AS DECIMAL.

DEF INPUT  PARAMETER pvILanguage    AS INTEGER NO-UNDO.
DEF INPUT  PARAMETER user-init      AS CHAR.
DEF INPUT  PARAMETER s-artnr        AS INT.
DEF INPUT  PARAMETER qty            AS DECIMAL.
DEF INPUT  PARAMETER transfered     AS LOGICAL.
DEF INPUT  PARAMETER cost-acct      AS CHAR.
DEF INPUT  PARAMETER curr-lager     AS INT.
DEF INPUT  PARAMETER price          AS DECIMAL.
DEF INPUT  PARAMETER transdate      AS DATE.
DEF INPUT  PARAMETER lscheinnr      AS CHAR.

DEF OUTPUT PARAMETER err-flag2      AS INT INIT 0.
DEF OUTPUT PARAMETER err-flag1      AS INT INIT 0.
DEF OUTPUT PARAMETER err-flag       AS INT INIT 0.
DEF OUTPUT PARAMETER oh-ok          AS LOGICAL INIT YES.

DEF OUTPUT PARAMETER msg-str2       AS CHAR.

{supertransBL.i} 
DEF VAR lvCAREA AS CHAR INITIAL "ins-storerequest". 

DEFINE VARIABLE anzahl AS DECIMAL FORMAT "->,>>>,>>9.999". 
DEFINE VARIABLE wert AS DECIMAL. 

FIND FIRST bediener WHERE bediener.userinit = user-init NO-LOCK. 
FIND FIRST l-artikel WHERE l-artikel.artnr = s-artnr NO-LOCK NO-ERROR.
IF l-artikel.betriebsnr GT 0 THEN /* = recipe */
DO: 
    FOR EACH op-list1: 
      DELETE op-list1. 
    END. 
    RUN create-op-list1(l-artikel.betriebsnr, qty, INPUT-OUTPUT oh-ok). 
    IF oh-ok THEN 
    DO: 
      FOR EACH op-list1: 
        CREATE op-list. 
        BUFFER-COPY op-list1 TO op-list.
        IF NOT transfered THEN op-list.stornogrund = cost-acct. 
      END. 
      err-flag1 = 1.
      /*
      IF NOT transfered THEN ENABLE btn-print WITH FRAME frame1. 
      RUN disp-l-op. 
      amount = 0. 
      DISP amount WITH FRAME frame1. 
      ENABLE btn-del btn-go WITH FRAME frame1.
      */
    END.
    err-flag = 1.
    RETURN. 
END. 

anzahl = qty. 
wert = qty * price. 
amount = wert. 
t-amount = t-amount + wert. 

IF curr-lager = 0 THEN 
DO: 
    /*
    HIDE MESSAGE NO-PAUSE. 
    MESSAGE translateExtended ("Store number incorrect",lvCAREA,"") VIEW-AS ALERT-BOX INFORMATION. 
    */
    RETURN. 
END. 

CREATE op-list. 
ASSIGN
    op-list.datum        = transdate
    op-list.lager-nr     = curr-lager 
    op-list.artnr        = s-artnr
    op-list.zeit         = TIME
    op-list.anzahl       = anzahl 
    op-list.einzelpreis  = price 
    op-list.warenwert    = wert 
    op-list.herkunftflag = 1    /* 4 = inventory !!! */ 
    op-list.lscheinnr    = lscheinnr
    op-list.fuellflag    = bediener.nr 
    op-list.pos          = 1
  . 
IF transfered THEN op-list.op-art = 14. 
ELSE op-list.op-art = 13. 
IF NOT transfered THEN op-list.stornogrund = cost-acct. 
  
FIND FIRST l-art WHERE l-art.artnr = op-list.artnr NO-LOCK. 
FIND FIRST sys-user WHERE sys-user.nr = op-list.fuellflag NO-LOCK.
FIND FIRST l-bestand WHERE l-bestand.artnr = op-list.artnr
    AND l-bestand.lager-nr = curr-lager NO-LOCK NO-ERROR.
ASSIGN
    op-list.bezeich  = l-art.bezeich
    op-list.username = sys-user.username
.
IF AVAILABLE l-bestand THEN op-list.onhand = l-bestand.anz-anf-best
    + l-bestand.anz-eingang - l-bestand.anz-ausgang.


CREATE out-list. 
out-list.artnr = l-artikel.artnr. 


PROCEDURE create-op-list1: 
DEFINE INPUT PARAMETER p-artnr      AS INTEGER. 
DEFINE INPUT PARAMETER menge        AS DECIMAL. 
DEFINE INPUT-OUTPUT PARAMETER oh-ok AS LOGICAL. 
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
          err-flag2 = 1.
          msg-str2 = translateExtended ("Article ",lvCAREA,"") 
                   + STRING(l-art.artnr,"9999999") + " - " 
                   + l-art.bezeich + " not found, posting not possible.".
          oh-ok = NO.
          RETURN. 
        END. 
        stock-oh = l-bestand.anz-anf-best + l-bestand.anz-eingang - l-bestand.anz-ausgang. 
        inh = inh / l-art.inhalt. 
        IF inh GT stock-oh THEN 
        DO: 
          err-flag2 = 2.
          msg-str2 = translateExtended ("Quantity over stock-onhand: ",lvCAREA,"") 
                   + STRING(l-art.artnr,"9999999") 
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
          op-list1.fuellflag    = bediener.nr 
          op-list1.pos          = 1
        . 
        FIND FIRST l-art WHERE l-art.artnr = op-list1.artnr NO-LOCK. 
        FIND FIRST sys-user WHERE sys-user.nr = op-list1.fuellflag NO-LOCK.
        FIND FIRST l-bestand WHERE l-bestand.artnr = op-list.artnr
          AND l-bestand.lager-nr = curr-lager NO-LOCK NO-ERROR.
        ASSIGN
          op-list1.bezeich  = l-art.bezeich
          op-list1.username = sys-user.username
        .
        IF AVAILABLE l-bestand THEN op-list1.onhand = l-bestand.anz-anf-best
          + l-bestand.anz-eingang - l-bestand.anz-ausgang.
        
      END.
  END.
END. 

