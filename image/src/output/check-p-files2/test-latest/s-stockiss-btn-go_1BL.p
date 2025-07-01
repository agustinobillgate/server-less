/*Only Used in vhpCloud*/
DEFINE TEMP-TABLE op-list LIKE l-op
    FIELD a-bezeich     LIKE l-artikel.bezeich
    FIELD vat-no        AS INTEGER
    FIELD vat-value     AS DECIMAL
    FIELD disc-amount   AS DECIMAL
    FIELD disc-amount2  AS DECIMAL
    FIELD tax-percent   AS DECIMAL
    FIELD discamt-flag  AS LOGICAL
    FIELD addvat-amount AS DECIMAL
.

DEF INPUT-OUTPUT PARAMETER TABLE FOR op-list.
DEF INPUT  PARAMETER f-endkum       AS INT.
DEF INPUT  PARAMETER b-endkum       AS INT.
DEF INPUT  PARAMETER m-endkum       AS INT.
DEF INPUT  PARAMETER lscheinnr      AS CHAR.
DEF INPUT  PARAMETER billdate       AS DATE.
DEF INPUT  PARAMETER curr-lager     AS INT.
DEF INPUT  PARAMETER jobnr          AS INT.
DEF INPUT  PARAMETER lief-nr        AS INT.
DEF INPUT  PARAMETER fb-closedate   AS DATE.
DEF INPUT  PARAMETER m-closedate    AS DATE.
DEF INPUT  PARAMETER user-init      AS CHAR.
DEF INPUT  PARAMETER t-amount       AS DECIMAL FORMAT "->,>>>,>>>,>>9.99".

DEF OUTPUT PARAMETER created        AS LOGICAL.
DEF OUTPUT PARAMETER s-artnr        AS INT.
DEF OUTPUT PARAMETER qty            AS DECIMAL.
DEF OUTPUT PARAMETER price          AS DECIMAL.
DEF OUTPUT PARAMETER cost-acct      LIKE gl-acct.fibukonto.
DEF OUTPUT PARAMETER err-code       AS INT INIT 0.

DEFINE VARIABLE gl-notfound AS LOGICAL.

DEFINE BUFFER queasy336 FOR queasy.

/*FDL Feb 29, 2024 => Ticket 65A160*/
FOR EACH op-list WHERE op-list.stornogrund NE ""
    AND op-list.stornogrund NE "00000000"
    AND op-list.stornogrund NE ?:

    FIND FIRST gl-acct WHERE gl-acct.fibukonto EQ op-list.stornogrund NO-LOCK NO-ERROR.
    IF NOT AVAILABLE gl-acct THEN
    DO:
        gl-notfound = YES.
        LEAVE.
    END.
END.
IF gl-notfound THEN 
DO:
    err-code = 2.
    RETURN.
END.

FIND FIRST bediener WHERE bediener.userinit = user-init.
DEFINE VARIABLE curr-pos AS INTEGER.

IF lief-nr NE 0 THEN
DO:
    FIND FIRST l-lieferant WHERE l-lieferant.lief-nr = lief-nr NO-LOCK NO-ERROR.
    IF NOT AVAILABLE l-lieferant THEN RETURN.
END.
/*  IF NOT created THEN 
DO: */
FIND FIRST l-op WHERE l-op.op-art = 1 AND l-op.loeschflag LE 1
  AND l-op.lscheinnr = lscheinnr NO-LOCK NO-ERROR.
IF AVAILABLE l-op THEN
DO:
  err-code = 1.
  RETURN NO-APPLY. 
END.
ELSE 
DO:
  FIND FIRST l-ophis WHERE l-ophis.op-art = 1
    AND l-ophis.lscheinnr = lscheinnr NO-LOCK NO-ERROR.

  IF AVAILABLE l-ophis THEN
  DO:
    err-code = 1.
    RETURN NO-APPLY. 
  END.
END.
/* END. */

/* create l-ophdr FOR receiving */ 
FIND FIRST l-ophdr WHERE l-ophdr.lscheinnr = lscheinnr 
AND l-ophdr.op-typ = "STI" NO-LOCK NO-ERROR. 
IF NOT AVAILABLE l-ophdr THEN 
DO: 
  create l-ophdr. 
  l-ophdr.datum =  billdate. 
  l-ophdr.lager-nr = curr-lager. 
  l-ophdr.lscheinnr = lscheinnr. 
  l-ophdr.op-typ = "STI". 
  FIND CURRENT l-ophdr NO-LOCK. 
END.

RUN l-op-pos(OUTPUT curr-pos). 
curr-pos = curr-pos - 1. 
FOR EACH op-list: 
  ASSIGN
    created   = YES 
    curr-pos  = curr-pos + 1 
    s-artnr   = op-list.artnr 
    qty       = op-list.anzahl 
    price     = op-list.warenwert / qty 
    cost-acct = op-list.stornogrund
  . 
  RUN create-l-op.
END. 
IF lief-nr NE 0 THEN RUN create-ap. 

/* create l-ophdr FOR Outgoing */ 
FIND FIRST l-ophdr WHERE l-ophdr.lscheinnr = lscheinnr 
AND l-ophdr.op-typ = "STT" NO-LOCK NO-ERROR. 
IF NOT AVAILABLE l-ophdr THEN 
DO: 
  CREATE l-ophdr. 
  ASSIGN
    l-ophdr.datum     =  billdate 
    l-ophdr.lager-nr  = curr-lager 
    l-ophdr.lscheinnr = lscheinnr 
    l-ophdr.op-typ    = "STT"
    l-ophdr.fibukonto = cost-acct 
    l-ophdr.betriebsnr = jobnr
  . 
  FIND CURRENT l-ophdr NO-LOCK. 
END. 
RUN l-op-pos(OUTPUT curr-pos). 
curr-pos = curr-pos - 1. 
FOR EACH op-list: 
  ASSIGN
    curr-pos  = curr-pos + 1 
    s-artnr   = op-list.artnr 
    qty       = op-list.anzahl 
    price     = op-list.warenwert / qty
    cost-acct = op-list.stornogrund
  . 
  RUN create-l-op1(op-list.lager-nr). 
END. 

PROCEDURE l-op-pos: 
DEFINE OUTPUT PARAMETER pos AS INTEGER INITIAL 0. 
DEFINE buffer l-op1 FOR l-op. 
/* 
  FOR EACH l-op1 WHERE l-op1.lscheinnr = lscheinnr 
    AND l-op1.loeschflag GE 0 AND l-op1.pos GT 0 NO-LOCK: 
    IF l-op1.pos GT pos THEN pos = l-op1.pos. 
  END. 
*/ 
  pos =  1. 
END. 

/*ragung add validasi for close*/
FOR EACH queasy WHERE queasy.KEY = 331 
    AND (queasy.char2 EQ "Inv-Cek Reciving" 
         OR queasy.char2 EQ "Inv-Cek Reorg"
         OR queasy.char2 EQ "Inv-Cek Journal"):
    DELETE queasy.
END.
 

PROCEDURE create-l-op: 
DEF BUFFER buf-lieferant FOR l-lieferant.
DEFINE VARIABLE anzahl      AS DECIMAL FORMAT ">>>,>>9.999". 
DEFINE VARIABLE wert        AS DECIMAL. 
DEFINE VARIABLE tot-anz     AS DECIMAL. 
DEFINE VARIABLE tot-wert    AS DECIMAL. 
DEFINE VARIABLE avrg-price  AS DECIMAL INITIAL 0. 
 

  FIND FIRST l-artikel WHERE l-artikel.artnr = s-artnr NO-LOCK.
  ASSIGN
    anzahl = qty /*agung* l-artikel.lief-einheit ITA 010916*/
    wert   = qty * price
    wert   = ROUND(wert, 2).

  /* UPDATE supplier turnover */ 
  FIND FIRST buf-lieferant WHERE buf-lieferant.lief-nr = lief-nr NO-LOCK NO-ERROR. 
  IF AVAILABLE buf-lieferant THEN 
  DO: 
    FIND FIRST  l-liefumsatz WHERE l-liefumsatz.lief-nr = lief-nr 
    AND l-liefumsatz.datum = billdate EXCLUSIVE-LOCK NO-ERROR. 
    IF NOT AVAILABLE l-liefumsatz THEN 
    DO: 
      CREATE l-liefumsatz. 
      ASSIGN
        l-liefumsatz.datum  = billdate 
        l-liefumsatz.lief-nr = lief-nr
      . 
    END. 
    l-liefumsatz.gesamtumsatz = l-liefumsatz.gesamtumsatz + wert. 
    FIND CURRENT l-liefumsatz NO-LOCK. 
  END. 
 
/* Create l-op record  FOR incoming */ 
  CREATE l-op. 
  BUFFER-COPY op-list TO l-op.
  ASSIGN l-op.pos     = curr-pos
         l-op.lief-nr = lief-nr
  .

  FIND FIRST queasy WHERE queasy.KEY = 304 AND queasy.char1 = l-op.lscheinnr 
          AND queasy.number1 = l-op.artnr NO-LOCK NO-ERROR.
  IF NOT AVAILABLE queasy THEN DO:
        CREATE queasy.
        ASSIGN queasy.KEY     = 304 
               queasy.char1   = l-op.lscheinnr 
               queasy.number1 = l-op.artnr
               queasy.number2 = op-list.vat-no
               queasy.deci1   = op-list.vat-value
         .   
        RELEASE queasy.
  END.

  /*FDL Jan 23, 2025: F26793*/
  FIND FIRST queasy336 WHERE queasy336.key EQ 336
      AND queasy336.number1 EQ INT(RECID(l-op))
      AND queasy336.char1 EQ l-op.lscheinnr
      AND queasy336.number2 EQ l-op.artnr        
      AND queasy336.char2 EQ STRING(l-op.einzelpreis)
      AND queasy336.date1 EQ l-op.datum NO-LOCK NO-ERROR.
  IF NOT AVAILABLE queasy336 THEN
  DO:
      CREATE queasy336.
      ASSIGN
          queasy336.key       = 336
          queasy336.char1     = l-op.lscheinnr
          queasy336.number1   = INT(RECID(l-op))
          queasy336.number2   = l-op.artnr
          queasy336.date1     = l-op.datum
          queasy336.deci1     = op-list.disc-amount 
          queasy336.deci2     = op-list.disc-amount2
          queasy336.deci3     = op-list.tax-percent 
          queasy336.logi1     = op-list.discamt-flag
          queasy336.logi2     = YES               /*Direct Issue*/
          queasy336.char2     = STRING(l-op.einzelpreis)
          queasy336.char3     = STRING(op-list.addvat-amount) /*FDL Feb 2025: 00B4A5*/
          queasy336.number3   = l-op.op-art
          queasy336.logi3     = NO               /*Without PO*/
          .
      RELEASE queasy336.
  END.

  FIND CURRENT l-op NO-LOCK. 
 
  RUN create-purchase-book(s-artnr, price, /*anzahl*/ qty, billdate, lief-nr). 
 
  IF (l-artikel.ek-aktuell NE price) AND price NE 0  THEN 
  DO: 
    FIND CURRENT l-artikel EXCLUSIVE-LOCK. 
    ASSIGN
      l-artikel.ek-letzter = l-artikel.ek-aktuell
      l-artikel.ek-aktuell = price
    . 
    FIND CURRENT l-artikel NO-LOCK. 
  END. 
END. 
 


PROCEDURE create-ap: 
DEFINE VARIABLE ap-license AS LOGICAL INITIAL NO. 
DEFINE VARIABLE ap-acct AS CHAR. 
DEFINE VARIABLE do-it AS LOGICAL INITIAL YES. 
 
  FIND FIRST htparam WHERE paramnr = 1016 NO-LOCK. 
  ap-license = htparam.flogical. 
  IF NOT ap-license THEN RETURN. 
 
  FIND FIRST htparam WHERE paramnr = 986 NO-LOCK. 
  ap-acct = htparam.fchar. 

  /*FIND FIRST gl-acct WHERE gl-acct.fibukonto = ap-acct NO-LOCK NO-ERROR. 
  IF AVAILABLE gl-acct THEN 
  DO: 
    IF l-lieferant.z-code NE "" THEN 
    DO: 
      FIND FIRST gl-acct WHERE gl-acct.fibukonto = l-lieferant.z-code 
        NO-LOCK NO-ERROR. 
      IF AVAILABLE gl-acct AND (l-lieferant.z-code NE ap-acct) THEN do-it = NO. 
    END. 
  END.*/

  FIND FIRST gl-acct WHERE gl-acct.fibukonto = ap-acct NO-LOCK NO-ERROR. 
  IF NOT AVAILABLE gl-acct THEN ASSIGN do-it = NO.
  
  IF NOT do-it THEN RETURN. 
 
  CREATE l-kredit. 
  ASSIGN
    l-kredit.name           = lscheinnr 
    l-kredit.lief-nr        = lief-nr
    l-kredit.lscheinnr      = lscheinnr 
    l-kredit.rgdatum        = billdate 
    l-kredit.datum          = ?
    l-kredit.saldo          = t-amount
    l-kredit.ziel           = 30
    l-kredit.netto          = t-amount 
    l-kredit.bediener-nr    = bediener.nr
  . 
  CREATE ap-journal.
  ASSIGN
    ap-journal.lief-nr      = lief-nr
    ap-journal.docu-nr      = lscheinnr 
    ap-journal.lscheinnr    = lscheinnr 
    ap-journal.rgdatum      = billdate 
    ap-journal.saldo        = t-amount 
    ap-journal.netto        = t-amount 
    ap-journal.userinit     = bediener.userinit 
    ap-journal.zeit         = TIME
  . 

END. 
 


PROCEDURE create-purchase-book: 
DEFINE INPUT PARAMETER s-artnr AS INTEGER. 
DEFINE INPUT PARAMETER price AS DECIMAL. 
DEFINE INPUT PARAMETER qty AS DECIMAL. 
DEFINE INPUT PARAMETER datum AS DATE. 
DEFINE INPUT PARAMETER lief-nr AS INTEGER. 
DEFINE VARIABLE max-anz AS INTEGER. 
DEFINE VARIABLE curr-anz AS INTEGER. 
DEFINE VARIABLE created AS LOGICAL INITIAL NO. 
DEFINE VARIABLE i AS INTEGER. 
DEFINE buffer l-art FOR l-artikel. 
DEFINE buffer l-price1 FOR l-pprice. 
  FIND FIRST htparam WHERE paramnr = 225 no-lock.  /* max stored p-price */ 
  max-anz = htparam.finteger. 
  IF max-anz = 0 THEN max-anz = 1. 
  FIND FIRST l-art WHERE l-art.artnr = s-artnr NO-LOCK. 
  curr-anz = l-art.lieferfrist. 
/*
  IF curr-anz GT 0 THEN 
  DO: 
    FIND FIRST l-pprice WHERE l-pprice.artnr = s-artnr 
      AND l-pprice.bestelldatum = datum 
      AND l-pprice.einzelpreis = price 
      AND l-pprice.lief-nr = lief-nr NO-LOCK NO-ERROR. 
    IF AVAILABLE l-pprice THEN RETURN. 
  END. 
*/  
  IF curr-anz GE max-anz THEN 
  DO: 
    FIND FIRST l-price1 WHERE l-price1.artnr = s-artnr 
      AND l-price1.counter = 1 USE-INDEX counter_ix EXCLUSIVE-LOCK NO-ERROR. 
    IF AVAILABLE l-price1 THEN 
    ASSIGN 
      l-price1.docu-nr      = lscheinnr 
      l-price1.artnr        = s-artnr
      l-price1.anzahl       = qty
      l-price1.einzelpreis  = price 
      l-price1.warenwert    = qty * price 
      l-price1.bestelldatum = datum
      l-price1.lief-nr      = lief-nr 
      l-price1.counter      = 0 
      created               = YES
    . 
    DO i = 2 TO curr-anz: 
      FIND FIRST l-pprice WHERE l-pprice.artnr = s-artnr 
        AND l-pprice.counter = i USE-INDEX counter_ix NO-LOCK NO-ERROR. 
      IF AVAILABLE l-pprice THEN 
      DO: 
        FIND CURRENT l-pprice EXCLUSIVE-LOCK. 
        l-pprice.counter = l-pprice.counter - 1. 
        FIND CURRENT l-pprice NO-LOCK. 
      END. 
    END. 
    IF created THEN 
    DO: 
      l-price1.counter = curr-anz. 
      FIND CURRENT l-price1 NO-LOCK. 
    END. 
  END. 
  IF NOT created THEN 
  DO: 
    CREATE l-pprice. 
    ASSIGN
      l-pprice.docu-nr      = lscheinnr 
      l-pprice.artnr        = s-artnr
      l-pprice.anzahl       = qty
      l-pprice.einzelpreis  = price 
      l-pprice.warenwert    = qty * price 
      l-pprice.bestelldatum = datum
      l-pprice.lief-nr      = lief-nr 
      l-pprice.counter      = curr-anz + 1
    . 
    FIND CURRENT l-pprice NO-LOCK. 
    FIND CURRENT l-art EXCLUSIVE-LOCK. 
    l-art.lieferfrist = curr-anz + 1. 
    FIND CURRENT l-art NO-LOCK. 
  END. 
END. 



PROCEDURE create-l-op1:
DEFINE INPUT PARAM curr-lager   AS INTEGER.
DEFINE VARIABLE anzahl          AS DECIMAL FORMAT ">>>,>>9.999". 
DEFINE VARIABLE wert            AS DECIMAL. 
DEFINE VARIABLE tot-anz         AS DECIMAL. 
DEFINE VARIABLE tot-wert        AS DECIMAL. 
DEFINE VARIABLE avrg-price      AS DECIMAL INITIAL 0. 
DEFINE BUFFER l-art FOR l-artikel. 
  
  FIND FIRST l-art WHERE l-art.artnr = s-artnr NO-LOCK. 
  ASSIGN
    anzahl = qty /*agung* l-art.lief-einheit ITA 010916*/
    wert   = qty * price 
    wert   = ROUND(wert, 2). 
 
/* Create l-op record  FOR outgoing */ 
  CREATE l-op.
  ASSIGN
    l-op.lief-nr        = lief-nr
    l-op.datum          = billdate 
    l-op.lager-nr       = curr-lager 
    l-op.artnr          = s-artnr
    l-op.zeit           = TIME
    l-op.anzahl         = anzahl 
    l-op.einzelpreis    = price 
    l-op.warenwert      = wert 
    l-op.op-art         = 3 
    l-op.herkunftflag   = 2    /* 2 Direct Issue (out) */ 
    l-op.docu-nr        = lscheinnr
    l-op.lscheinnr      = lscheinnr 
    l-op.pos            = curr-pos 
    l-op.fuellflag      = bediener.nr 
    l-op.flag           = YES   /* flag indicates direct issue **/ 
    l-op.stornogrund    = cost-acct
  . 
  FIND CURRENT l-op NO-LOCK. 
 
  IF jobnr NE 0 THEN 
    RUN create-lartjob.p(RECID(l-ophdr), s-artnr, anzahl, wert, billdate, YES).  
 
  IF ((l-art.endkum = f-endkum OR l-art.endkum = b-endkum) 
    AND billdate LE fb-closedate) 
  OR (l-art.endkum GE m-endkum AND billdate LE m-closedate) THEN 
  DO: 
    FIND FIRST l-bestand WHERE l-bestand.lager-nr = op-list.lager-nr 
      AND l-bestand.artnr = s-artnr EXCLUSIVE-LOCK NO-ERROR. 
    IF NOT AVAILABLE l-bestand THEN 
    DO: 
      CREATE l-bestand.
      ASSIGN
        l-bestand.lager-nr     = op-list.lager-nr
        l-bestand.artnr        = s-artnr 
        l-bestand.anf-best-dat = billdate
      . 
    END. 
    ASSIGN
      l-bestand.anz-eingang  = l-bestand.anz-eingang + anzahl
      l-bestand.wert-eingang = l-bestand.wert-eingang + wert 
      l-bestand.anz-ausgang  = l-bestand.anz-ausgang + anzahl 
      l-bestand.wert-ausgang = l-bestand.wert-ausgang + wert
    . 
    FIND CURRENT l-bestand NO-LOCK. 
 
    FIND FIRST l-bestand WHERE l-bestand.lager-nr = 0 AND 
      l-bestand.artnr = s-artnr EXCLUSIVE-LOCK NO-ERROR. 
    IF NOT AVAILABLE l-bestand THEN 
    DO: 
      CREATE l-bestand. 
      ASSIGN
        l-bestand.lager-nr     = 0 
        l-bestand.artnr        = s-artnr 
        l-bestand.anf-best-dat = billdate
      . 
    END.
    ASSIGN
      l-bestand.anz-eingang  = l-bestand.anz-eingang + anzahl 
      l-bestand.wert-eingang = l-bestand.wert-eingang + wert 
      l-bestand.anz-ausgang  = l-bestand.anz-ausgang + anzahl 
      l-bestand.wert-ausgang = l-bestand.wert-ausgang + wert
    . 
    FIND CURRENT l-bestand NO-LOCK. 
  END. 
END. 
 

