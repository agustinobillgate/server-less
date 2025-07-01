DEF TEMP-TABLE t-bediener
    FIELD username LIKE bediener.username
    FIELD nr       LIKE bediener.nr.

DEF INPUT  PARAMETER l-recid        AS INT.
DEF INPUT  PARAMETER rcvDate        AS DATE.

DEF OUTPUT PARAMETER rcv-type       AS INT.
DEF OUTPUT PARAMETER f-endkum       AS INT.
DEF OUTPUT PARAMETER b-endkum       AS INT.
DEF OUTPUT PARAMETER m-endkum       AS INT.
DEF OUTPUT PARAMETER lief-nr        AS INT.
DEF OUTPUT PARAMETER curr-lager     AS INT.
DEF OUTPUT PARAMETER billdate       AS DATE.
DEF OUTPUT PARAMETER fb-closedate   AS DATE.
DEF OUTPUT PARAMETER m-closedate    AS DATE.
DEF OUTPUT PARAMETER last-mdate     AS DATE.
DEF OUTPUT PARAMETER last-fbdate    AS DATE.
DEF OUTPUT PARAMETER lscheinnr      LIKE l-op.lscheinnr.
DEF OUTPUT PARAMETER lief-bezeich   AS CHAR INITIAL "Supplier Name".
DEF OUTPUT PARAMETER lager-bezeich  AS CHAR INITIAL "Store Name".
DEF OUTPUT PARAMETER err-code       AS INT INIT 0.
DEF OUTPUT PARAMETER fl-code1       AS INT INIT 0.
DEF OUTPUT PARAMETER fl-code2       AS INT INIT 0.
DEF OUTPUT PARAMETER l-rcv-lscheinnr LIKE l-op.lscheinnr.
DEF OUTPUT PARAMETER l-out-stornogrund AS CHAR.
DEF OUTPUT PARAMETER avail-l-out    AS LOGICAL INIT NO.
DEF OUTPUT PARAMETER TABLE FOR t-bediener.

DEFINE buffer l-rcv FOR l-op.
DEFINE buffer l-out FOR l-op.

FIND FIRST l-rcv WHERE RECID(l-rcv) = l-recid NO-LOCK. 
 
rcv-type = l-rcv.herkunftflag.    /* 2 = Direct Issue (IN) */ 

IF rcv-type = 2 THEN 
DO: 
  FIND FIRST l-out WHERE l-out.lief-nr = l-rcv.lief-nr 
    AND l-out.datum = l-rcv.datum 
    AND l-out.lager-nr = l-rcv.lager-nr 
    AND l-out.artnr = l-rcv.artnr 
    AND l-out.anzahl = l-rcv.anzahl 
    AND l-out.einzelpreis = l-rcv.einzelpreis 
    AND l-out.warenwert = l-rcv.warenwert 
    AND l-out.op-art = 3 
    AND l-out.herkunftflag = 2 
    AND l-out.docu-nr = l-rcv.docu-nr 
    AND l-out.lscheinnr = l-rcv.lscheinnr NO-LOCK NO-ERROR. 
  IF NOT AVAILABLE l-out THEN 
  DO:
    err-code = 1.
    RETURN. 
  END. 
  ELSE
  DO:
      l-out-stornogrund = l-out.stornogrund.
      avail-l-out = YES.
  END.
END.


FIND FIRST l-ophdr WHERE l-ophdr.lscheinnr = l-rcv.lscheinnr 
  AND l-ophdr.op-typ = "STI" AND l-ophdr.datum = l-rcv.datum 
  /* AND l-ophdr.lager-nr = l-rcv.lager-nr */ NO-LOCK NO-ERROR. 
IF NOT AVAILABLE l-ophdr THEN 
DO:
  err-code = 2.
  l-rcv-lscheinnr = l-rcv.lscheinnr.
  RETURN. 
END.


FIND FIRST htparam WHERE paramnr = 257 NO-LOCK. 
f-endkum = htparam.finteger.               /* Rulita 211024 | Fixing for serverless */  
FIND FIRST htparam WHERE paramnr = 258 NO-LOCK. 
b-endkum = htparam.finteger.               /* Rulita 211024 | Fixing for serverless */  
FIND FIRST htparam WHERE paramnr = 268 NO-LOCK. 
m-endkum = htparam.finteger.               /* Rulita 211024 | Fixing for serverless */  
 
ASSIGN billdate = rcvDate.

FIND FIRST htparam WHERE paramnr = 224 NO-LOCK. 
fb-closedate = htparam.fdate. 
FIND FIRST htparam WHERE paramnr = 221 NO-LOCK. 
m-closedate = htparam.fdate.


IF billdate = ? OR billdate GT today THEN billdate = today. 
ELSE 
DO: 
  IF m-closedate NE ? THEN last-mdate = DATE(month(m-closedate), 
    1, year(m-closedate)) - 1. 
  IF fb-closedate NE ? THEN last-fbdate = DATE(month(fb-closedate), 
    1, year(fb-closedate)) - 1. 
  IF (billdate LE last-mdate) OR (billdate LE last-fbdate) THEN 
  DO:
    fl-code1 = 1.
  END. 
  FIND FIRST htparam WHERE htparam.paramnr = 269 NO-LOCK. 
  IF htparam.fdate NE ? AND billdate LE htparam.fdate THEN 
  DO:
    fl-code2 = 1.
  END. 
END. 
 
ASSIGN
  lief-nr       = l-rcv.lief-nr 
  lscheinnr     = l-rcv.lscheinnr 
  billdate      = l-rcv.datum
  curr-lager    = l-rcv.lager-nr
. 
 
FIND FIRST l-lieferant WHERE l-lieferant.lief-nr = lief-nr NO-LOCK. 
FIND FIRST l-lager WHERE l-lager.lager-nr = curr-lager NO-LOCK. 

ASSIGN
  lief-bezeich  = l-lieferant.firma 
  lager-bezeich = l-lager.bezeich
.

FOR EACH bediener:
    CREATE t-bediener.
    ASSIGN
    t-bediener.username = bediener.username
    t-bediener.nr       = bediener.nr.
END.
