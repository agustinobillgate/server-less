DEFINE TEMP-TABLE op-list LIKE l-op 
  FIELD bezeich  AS CHAR FORMAT "x(36)"             COLUMN-LABEL "Description" 
  FIELD username AS CHAR FORMAT "x(16)"             COLUMN-LABEL "Created by" 
  FIELD onhand   AS DECIMAL FORMAT "->,>>>,>>9.99"  COLUMN-LABEL "On-Hand"
  FIELD new-flag AS LOGICAL INIT YES
.

DEF INPUT-OUTPUT  PARAMETER curr-pos   AS INT.
DEF INPUT  PARAMETER TABLE FOR op-list.
DEF INPUT  PARAMETER transdate  AS DATE.
DEF INPUT  PARAMETER curr-lager AS INT.
DEF INPUT  PARAMETER deptNo     AS INT.
DEF INPUT  PARAMETER transfered AS LOGICAL.
DEF INPUT  PARAMETER to-stock   AS INT.
DEF INPUT  PARAMETER user-init  AS CHAR.
DEF INPUT  PARAMETER lscheinnr  AS CHAR.
DEF OUTPUT PARAMETER cost-acct  AS CHAR.
DEF OUTPUT PARAMETER price      AS DECIMAL FORMAT ">,>>>,>>>,>>9.99". 
DEF OUTPUT PARAMETER qty        AS DECIMAL FORMAT "->>>,>>9.999". 
DEF OUTPUT PARAMETER amount     AS DECIMAL FORMAT "->,>>>,>>>,>>9.99". 
DEF OUTPUT PARAMETER t-amount   AS DECIMAL FORMAT "->>,>>>,>>>,>>9.99". 
DEF OUTPUT PARAMETER s-artnr    AS INT.
DEF OUTPUT PARAMETER created    AS LOGICAL INITIAL NO.

DEFINE VARIABLE zeit        AS INTEGER.
MESSAGE curr-pos VIEW-AS ALERT-BOX INFO.
FIND FIRST bediener WHERE bediener.userinit = user-init NO-LOCK. 
ASSIGN
    curr-pos = curr-pos - 1  
    zeit     = TIME.

FOR EACH op-list WHERE op-list.anzahl NE 0 AND op-list.new-flag
    BY op-list.pos:     
    ASSIGN
      zeit      = zeit + 1
      /*ITA curr-pos  = curr-pos + 1 */
      curr-pos  = op-list.pos + 1 
      s-artnr   = op-list.artnr 
      qty       = op-list.anzahl 
      price     = op-list.warenwert / qty 
      cost-acct = op-list.stornogrund
    . 
    RUN create-l-op (zeit). 
END. 

PROCEDURE create-l-op: 
DEFINE INPUT PARAMETER zeit AS INTEGER. 
DEFINE VARIABLE anzahl AS DECIMAL FORMAT "->,>>>,>>9.999". 
DEFINE VARIABLE wert AS DECIMAL. 
 
DEFINE VARIABLE anz-oh AS DECIMAL. 
DEFINE VARIABLE val-oh AS DECIMAL. 
 
  ASSIGN
    anzahl   = qty 
    wert     = qty * price 
    amount   = wert
    t-amount = t-amount + wert
    created  = TRUE
  . 
 
/* Create l-op record */ 
  CREATE l-op. 
  ASSIGN
    l-op.datum          = transdate
    l-op.lager-nr       = curr-lager 
    l-op.artnr          = s-artnr
    l-op.zeit           = zeit
    l-op.anzahl         = anzahl 
    l-op.einzelpreis    = price 
    l-op.warenwert      = wert
    l-op.reorgflag      = deptNo
  . 
  IF transfered THEN l-op.op-art = 14. 
  ELSE l-op.op-art = 13. 

  ASSIGN
    l-op.herkunftflag = 1   
    l-op.lscheinnr    = lscheinnr
  . 

  IF NOT transfered THEN 
  ASSIGN 
    l-op.pos         = curr-pos 
    l-op.stornogrund = cost-acct
  . 
  ELSE l-op.pos = to-stock. 
  l-op.fuellflag = bediener.nr. 
  FIND CURRENT l-op NO-LOCK. 
  
END. 

