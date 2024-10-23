DEFINE TEMP-TABLE op-list LIKE l-op 
  FIELD bezeich  AS CHAR FORMAT "x(36)"             COLUMN-LABEL "Description" 
  FIELD username AS CHAR FORMAT "x(16)"             COLUMN-LABEL "Created by" 
  FIELD onhand   AS DECIMAL FORMAT "->,>>>,>>9.99"  COLUMN-LABEL "On-Hand"
  FIELD new-flag AS LOGICAL INIT YES
.

DEF TEMP-TABLE t-l-lager LIKE l-lager.

DEFINE BUFFER sys-user FOR bediener. 

DEF INPUT  PARAMETER user-init      AS CHAR.
DEF INPUT  PARAMETER t-datum        AS DATE.
DEF INPUT  PARAMETER t-lschein      AS CHAR.
DEF OUTPUT PARAMETER deptname       AS CHAR.
DEF OUTPUT PARAMETER curr-lager     AS INT.
DEF OUTPUT PARAMETER deptNo         AS INTEGER.
DEF OUTPUT PARAMETER show-price     AS LOGICAL.
DEF OUTPUT PARAMETER req-flag       AS LOGICAL.
DEF OUTPUT PARAMETER p-220          AS INT.
DEF OUTPUT PARAMETER out-type       AS INTEGER INIT 1.
DEF OUTPUT PARAMETER transfered     AS LOGICAL INITIAL NO.
DEF OUTPUT PARAMETER to-stock       AS INTEGER.
DEF OUTPUT PARAMETER lager-bezeich  AS CHAR.
DEF OUTPUT PARAMETER lager-bez1     AS CHAR.
DEF OUTPUT PARAMETER curr-pos       AS INTEGER.
DEF OUTPUT PARAMETER t-amount       AS DECIMAL.
DEF OUTPUT PARAMETER lscheinnr      LIKE l-op.lscheinnr.
DEF OUTPUT PARAMETER TABLE FOR op-list.
/*DEF OUTPUT PARAMETER TABLE FOR t-l-lager.*/

FIND FIRST bediener WHERE bediener.userinit = user-init NO-LOCK. 
FIND FIRST htparam WHERE htparam.paramnr = 43 NO-LOCK. 
show-price = htparam.flogical. 
IF SUBSTR(bediener.permissions, 22, 1) NE "0" THEN show-price = YES. 

FIND FIRST htparam WHERE paramnr = 475 NO-LOCK. 
req-flag = NOT htparam.flogical. 
 
FIND FIRST htparam WHERE paramnr = 220 NO-LOCK. 
p-220 = htparam.finteger.

/*
FOR EACH l-lager NO-LOCK:
    CREATE t-l-lager.
    BUFFER-COPY l-lager TO t-l-lager.
END.
*/

RUN read-data.


PROCEDURE read-data:
  ASSIGN lscheinnr = t-lschein.
  FIND FIRST l-op WHERE l-op.datum = t-datum 
    AND l-op.lscheinnr = t-lschein AND l-op.pos GT 0 NO-LOCK.
  ASSIGN 
    curr-lager = l-op.lager
    deptNo     = l-op.reorgflag
  .
  FIND FIRST parameters WHERE parameters.progname = "CostCenter" 
    AND parameters.section = "Name" AND INTEGER(parameters.varname) = deptNo 
    NO-LOCK NO-ERROR. 
  IF AVAILABLE parameters THEN deptname = parameters.vstring. 
  IF l-op.op-art = 14 THEN 
  ASSIGN
    transfered = YES
    out-type   = 1
    to-stock   = l-op.pos
  .
  ELSE out-type = 2.

  FIND FIRST l-lager WHERE l-lager.lager-nr = curr-lager NO-LOCK.
  lager-bezeich = l-lager.bezeich.
  IF to-stock NE 0 THEN
  DO:
    FIND FIRST l-lager WHERE l-lager.lager-nr = to-stock NO-LOCK.
    lager-bez1 = l-lager.bezeich.
  END.

  FOR EACH l-op WHERE l-op.datum = t-datum 
      AND l-op.lscheinnr = t-lschein AND l-op.pos GT 0 
      AND l-op.loeschflag LE 1 NO-LOCK BY l-op.pos:
      CREATE op-list.
      BUFFER-COPY l-op TO op-list.
      FIND FIRST l-artikel WHERE l-artikel.artnr = l-op.artnr NO-LOCK.
      FIND FIRST sys-user WHERE sys-user.nr = l-op.fuellflag NO-LOCK.
      FIND FIRST l-bestand WHERE l-bestand.artnr = l-op.artnr
        AND l-bestand.lager-nr = curr-lager NO-LOCK NO-ERROR.
      ASSIGN
        op-list.bezeich  = l-artikel.bezeich
        op-list.username = sys-user.username
        op-list.new-flag = NO
        curr-pos         = l-op.pos
        t-amount         = t-amount + l-op.warenwert. 

      .
      IF AVAILABLE l-bestand THEN op-list.onhand = l-bestand.anz-anf-best
        + l-bestand.anz-eingang - l-bestand.anz-ausgang.
  END.
END.
