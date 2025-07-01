DEFINE TEMP-TABLE op-list LIKE l-op
    FIELD bezeich LIKE l-artikel.bezeich
    FIELD username LIKE bediener.username.
DEFINE TEMP-TABLE t-op-list LIKE op-list.

DEFINE INPUT  PARAMETER pvILanguage  AS INTEGER NO-UNDO.
DEF INPUT-OUTPUT PARAMETER TABLE FOR op-list.
DEF INPUT PARAMETER curr-dept AS INT.
DEF INPUT PARAMETER billdate AS DATE.
DEF INPUT PARAMETER curr-lager AS INT.
DEF INPUT PARAMETER lscheinnr AS CHAR.
DEF INPUT PARAMETER lief-nr AS INT.
DEF INPUT PARAMETER f-endkum AS INT.
DEF INPUT PARAMETER b-endkum AS INT.
DEF INPUT PARAMETER m-endkum AS INT.
DEF INPUT PARAMETER fb-closedate AS DATE.
DEF INPUT PARAMETER m-closedate AS DATE.
DEF INPUT PARAMETER user-init AS CHAR.

DEF INPUT-OUTPUT PARAMETER t-amount AS DECIMAL.

DEF OUTPUT PARAMETER s-artnr AS INT.
DEF OUTPUT PARAMETER qty AS DECIMAL.
DEF OUTPUT PARAMETER price AS DECIMAL.
DEF OUTPUT PARAMETER err-code AS INT INIT 0.
DEF OUTPUT PARAMETER msg-str AS CHAR.

DEFINE VARIABLE curr-pos AS INTEGER. 
DEFINE VARIABLE created AS LOGICAL. 

{ supertransbl.i }
DEF VAR lvCAREA AS CHAR INITIAL "dml-stockin". 
DEFINE buffer sys-user FOR bediener.
DEFINE buffer l-art    FOR l-artikel.

FIND FIRST bediener WHERE bediener.userinit = user-init.
/* create l-ophdr  */ 
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
 
t-amount = 0. 
FOR EACH op-list:
    ASSIGN
      op-list.docu-nr = lscheinnr
      op-list.lscheinnr = lscheinnr
      curr-pos = curr-pos + 1
      s-artnr = op-list.artnr 
      qty = op-list.anzahl
      price = op-list.warenwert / qty
      t-amount = t-amount + op-list.warenwert 
      curr-lager = op-list.lager-nr
    . 
    FIND FIRST l-artikel WHERE l-artikel.artnr = s-artnr NO-LOCK. 
    RUN create-l-op. 
    created = YES. 
END. 

IF lief-nr NE 0 AND t-amount NE 0 THEN RUN create-ap.
FOR EACH op-list,
    FIRST l-art WHERE l-art.artnr = op-list.artnr, 
    FIRST sys-user WHERE sys-user.nr = op-list.fuellflag 
    NO-LOCK BY op-list.pos:
    CREATE t-op-list.
    BUFFER-COPY op-list TO t-op-list.
    ASSIGN
        t-op-list.bezeich = l-artikel.bezeich
        t-op-list.username = bediener.username.
END.
FOR EACH op-list:
    DELETE op-list.
END.
FOR EACH t-op-list:
    CREATE op-list.
    BUFFER-COPY t-op-list TO op-list.
END.

PROCEDURE l-op-pos: 
DEFINE OUTPUT PARAMETER pos AS INTEGER INITIAL 0. 
DEFINE buffer l-op1 FOR l-op. 
  ASSIGN pos =  1. 
END. 
 

PROCEDURE create-l-op: 
DEFINE VARIABLE anzahl AS DECIMAL. 
DEFINE VARIABLE wert AS DECIMAL. 
DEFINE VARIABLE tot-anz AS DECIMAL. 
DEFINE VARIABLE tot-wert AS DECIMAL. 
DEFINE VARIABLE avrg-price AS DECIMAL INITIAL 0. 
 
DEFINE BUFFER d-art  FOR dml-art. 
DEFINE BUFFER d-art1 FOR dml-artdep. 
 
  ASSIGN
    anzahl = qty 
    wert   = qty * price 
    wert   = ROUND(wert, 2)
  . 
 
  DO TRANSACTION: 
    IF ((l-artikel.endkum = f-endkum OR l-artikel.endkum = b-endkum) 
      AND billdate LE fb-closedate) 
    OR (l-artikel.endkum GE m-endkum AND billdate LE m-closedate) THEN 
    DO: 
/* UPDATE stock onhand  */ 
      DO: 
        FIND FIRST l-bestand WHERE l-bestand.lager-nr = 0 AND 
          l-bestand.artnr = s-artnr EXCLUSIVE-LOCK NO-ERROR. 
        IF NOT AVAILABLE l-bestand THEN 
        DO: 
          CREATE l-bestand. 
          l-bestand.artnr = s-artnr. 
          l-bestand.anf-best-dat = billdate. 
        END. 
        l-bestand.anz-eingang = l-bestand.anz-eingang + anzahl. 
        l-bestand.wert-eingang = l-bestand.wert-eingang + wert. 
        FIND CURRENT l-bestand NO-LOCK. 
        tot-anz = l-bestand.anz-anf-best + l-bestand.anz-eingang 
          - l-bestand.anz-ausgang. 
        tot-wert = l-bestand.val-anf-best + l-bestand.wert-eingang 
          - l-bestand.wert-ausgang. 
 
        IF tot-anz NE 0 THEN 
        DO: 
          avrg-price = tot-wert / tot-anz. 
          FIND CURRENT l-artikel EXCLUSIVE-LOCK. 
          l-artikel.vk-preis = avrg-price. 
          FIND CURRENT l-artikel NO-LOCK. 
        END. 
      END. 
 
      FIND FIRST l-bestand WHERE l-bestand.lager-nr = curr-lager AND 
        l-bestand.artnr = s-artnr EXCLUSIVE-LOCK NO-ERROR. 
      IF NOT AVAILABLE l-bestand THEN 
      DO: 
        CREATE l-bestand. 
        ASSIGN
            l-bestand.lager-nr     = curr-lager 
            l-bestand.artnr        = s-artnr
            l-bestand.anf-best-dat = billdate
        . 
      END. 
      ASSIGN
        l-bestand.anz-eingang  = l-bestand.anz-eingang + anzahl
        l-bestand.wert-eingang = l-bestand.wert-eingang + wert
      . 
      FIND CURRENT l-bestand NO-LOCK. 
    END. 
 
/* UPDATE supplier turnover */ 
    FIND FIRST l-lieferant WHERE l-lieferant.lief-nr = lief-nr NO-LOCK NO-ERROR. 
    IF AVAILABLE l-lieferant THEN 
    DO: 
      FIND FIRST  l-liefumsatz WHERE l-liefumsatz.lief-nr = lief-nr 
      AND l-liefumsatz.datum = billdate EXCLUSIVE-LOCK NO-ERROR. 
      IF NOT AVAILABLE l-liefumsatz THEN 
      DO: 
        CREATE l-liefumsatz. 
        ASSIGN
          l-liefumsatz.datum   = billdate
          l-liefumsatz.lief-nr = lief-nr. 
      END. 
      l-liefumsatz.gesamtumsatz = l-liefumsatz.gesamtumsatz + wert. 
      FIND CURRENT l-liefumsatz NO-LOCK. 
    END. 
 
/* Create l-op record */ 
    CREATE l-op. 
    ASSIGN
      l-op.lief-nr      = lief-nr
      l-op.datum        = billdate 
      l-op.lager-nr     = curr-lager 
      l-op.artnr        = s-artnr
      l-op.zeit         = TIME
      l-op.anzahl       = anzahl 
      l-op.einzelpreis  = price 
      l-op.warenwert    = wert 
      l-op.op-art       = 1
      l-op.herkunftflag = 1    /* 4 = inventory !!! */ 
      l-op.docu-nr      = lscheinnr 
      l-op.lscheinnr    = lscheinnr 
      l-op.pos          = curr-pos 
      l-op.fuellflag    = bediener.nr
    . 
    FIND CURRENT l-op NO-LOCK. 
 
    IF curr-dept = 0 THEN 
    DO: 
      FIND FIRST d-art WHERE d-art.artnr = s-artnr AND d-art.datum = billdate 
        EXCLUSIVE-LOCK. 
    d-art.geliefert = d-art.geliefert + anzahl. 
    FIND CURRENT d-art NO-LOCK. 
    END. 
    ELSE IF curr-dept > 0 THEN 
    DO: 
      FIND FIRST d-art1 WHERE d-art1.artnr = s-artnr AND d-art1.datum = billdate 
        AND d-art1.departement = curr-dept EXCLUSIVE-LOCK. 
      d-art1.geliefert = d-art1.geliefert + anzahl. 
      FIND CURRENT d-art1 NO-LOCK. 
    END. 
 
    RUN create-purchase-book(s-artnr, price, anzahl, billdate, lief-nr). 
 
    IF (l-artikel.ek-aktuell NE price) AND price NE 0  THEN 
    DO: 
      FIND CURRENT l-artikel EXCLUSIVE-LOCK. 
      ASSIGN
        l-artikel.ek-letzter = l-artikel.ek-aktuell 
        l-artikel.ek-aktuell = price
      . 
      FIND CURRENT l-artikel NO-LOCK. 
    END. 
    RETURN. 
  END.
  msg-str = msg-str + CHR(2)
          + translateExtended ("Incoming record can not be ctreated : ", lvCAREA, "":U)
          + STRING(s-artnr, "9999999").
END. 


PROCEDURE create-ap: 
DEFINE VARIABLE ap-license AS LOGICAL INITIAL NO. 
DEFINE VARIABLE ap-acct AS CHAR. 
DEFINE VARIABLE do-it AS LOGICAL INITIAL YES. 
DEFINE buffer l-op1 FOR l-op. 
 
  FIND FIRST htparam WHERE paramnr = 1016 NO-LOCK. 
  ap-license = htparam.flogical. 
  IF NOT ap-license THEN RETURN. 
 
  FIND FIRST l-op1 WHERE l-op1.lscheinnr = lscheinnr 
    AND l-op1.loeschflag = 0 AND l-op1.pos GE 1 NO-LOCK NO-ERROR. 
  IF NOT AVAILABLE l-op1 THEN 
  DO:
    err-code = 1.
    RETURN. 
  END. 
 
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
    l-kredit.name        = lscheinnr 
    l-kredit.lief-nr     = lief-nr
    l-kredit.lscheinnr   = lscheinnr 
    l-kredit.rgdatum     = billdate 
    l-kredit.datum       = ?
    l-kredit.saldo       = t-amount 
    l-kredit.ziel        = 30
    l-kredit.netto       = t-amount 
    l-kredit.bediener-nr = bediener.nr
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
  
  IF curr-anz GE max-anz THEN 
  DO: 
    FIND FIRST l-price1 WHERE l-price1.artnr = s-artnr 
      AND l-price1.counter = 1 USE-INDEX counter_ix EXCLUSIVE-LOCK NO-ERROR. 
    IF AVAILABLE l-price1 THEN 
    DO: 
      ASSIGN
        l-price1.docu-nr        = lscheinnr 
        l-price1.artnr          = s-artnr
        l-price1.anzahl         = qty
        l-price1.einzelpreis    = price 
        l-price1.warenwert      = qty * price 
        l-price1.bestelldatum   = datum
        l-price1.lief-nr        = lief-nr 
        l-price1.counter        = 0
      . 
      created = YES. 
    END. 
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
