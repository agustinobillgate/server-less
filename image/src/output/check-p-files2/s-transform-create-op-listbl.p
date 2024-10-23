DEFINE WORKFILE out-list 
  FIELD artnr AS INTEGER. 
DEFINE TEMP-TABLE op-list LIKE l-op
    FIELD bezeich LIKE l-artikel.bezeich
    FIELD username LIKE bediener.username.
DEFINE TEMP-TABLE t-op-list LIKE op-list.

DEF INPUT PARAMETER TABLE FOR op-list.
DEF INPUT PARAMETER qty         AS DECIMAL.
DEF INPUT PARAMETER price       AS DECIMAL.
DEF INPUT PARAMETER curr-lager  AS INT.
DEF INPUT PARAMETER transdate   AS DATE.
DEF INPUT PARAMETER s-artnr     AS INT.
DEF INPUT PARAMETER bediener-nr AS INT.
DEF INPUT PARAMETER lscheinnr   LIKE l-op.lscheinnr.

DEF INPUT-OUTPUT PARAMETER t-amount   AS DECIMAL.

DEF OUTPUT PARAMETER amount     AS DECIMAL.
DEF OUTPUT PARAMETER err-code   AS INT INIT 0.
DEF OUTPUT PARAMETER TABLE FOR t-op-list.
DEFINE buffer sys-user FOR bediener. 

RUN create-op-list.
FOR EACH op-list,
    FIRST l-art WHERE l-art.artnr = op-list.artnr, 
    FIRST sys-user WHERE sys-user.nr = op-list.fuellflag 
    NO-LOCK BY op-list.pos descending:
    CREATE t-op-list.
    BUFFER-COPY op-list TO t-op-list.
    ASSIGN 
        t-op-list.bezeich = l-art.bezeich
        t-op-list.username = sys-user.username.
END.

PROCEDURE create-op-list: 
DEFINE VARIABLE anzahl AS DECIMAL FORMAT "->,>>>,>>9.999". 
DEFINE VARIABLE wert AS DECIMAL. 
DEFINE VARIABLE oh-ok AS LOGICAL INITIAL YES. 
  anzahl = qty. 
  wert = qty * price. 
  amount = wert. 
  t-amount = t-amount + wert. 
 
  IF curr-lager = 0 THEN 
  DO: 
    err-code = 1.
    RETURN. 
  END. 
 
  create op-list. 
  op-list.datum = transdate. 
  op-list.lager-nr = curr-lager. 
  op-list.artnr = s-artnr. 
  op-list.zeit = time. 
  op-list.anzahl = anzahl. 
  op-list.einzelpreis = price. 
  op-list.warenwert = wert. 
  op-list.op-art = 4. 
  op-list.herkunftflag = 3.    /* 1 = regular, 4 = inventory !!! */ 
  op-list.lscheinnr = lscheinnr. 
  op-list.fuellflag = bediener-nr. 
  op-list.pos = 1.
END. 
