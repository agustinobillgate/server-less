DEFINE TEMP-TABLE op-list LIKE l-op
    FIELD a-bezeich LIKE l-artikel.bezeich.

DEF INPUT-OUTPUT PARAMETER curr-pos AS INT.
DEF INPUT-OUTPUT PARAMETER s-artnr AS INT.
DEF INPUT-OUTPUT PARAMETER price AS DECIMAL.
DEF INPUT-OUTPUT PARAMETER t-amount AS DECIMAL.
DEF INPUT-OUTPUT PARAMETER curr-lager AS INT.
DEF INPUT PARAMETER TABLE FOR op-list.
DEF INPUT PARAMETER pvILanguage      AS INT  NO-UNDO.
DEF INPUT PARAMETER l-out-stornogrund AS CHAR.
DEF INPUT PARAMETER lief-nr AS INT.
DEF INPUT PARAMETER billdate AS DATE.
DEF INPUT PARAMETER fb-closedate AS DATE.
DEF INPUT PARAMETER m-closedate AS DATE.
DEF INPUT PARAMETER m-endkum AS INT.
DEF INPUT PARAMETER f-endkum AS INT.
DEF INPUT PARAMETER b-endkum AS INT.
DEF INPUT PARAMETER avail-l-out AS LOGICAL.
DEF INPUT PARAMETER lscheinnr AS CHAR.
DEF INPUT PARAMETER rcv-type AS INT.
DEF INPUT PARAMETER qty AS DECIMAL.
DEF INPUT PARAMETER user-init AS CHAR.
DEF OUTPUT PARAMETER created AS LOGICAL INIT NO.
DEF OUTPUT PARAMETER msg-str AS CHAR.

{ supertransbl.i } 
DEF VAR lvCAREA AS CHAR INITIAL "s-stockins". 

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
    IF rcv-type = 2 AND avail-l-out THEN RUN create-l-op1.
    
    created = YES. 
END.
IF lief-nr NE 0 AND t-amount NE 0 THEN
    RUN s-stockins-create-apbl.p
        (lief-nr, lscheinnr, billdate, t-amount, user-init).

PROCEDURE create-l-op: 
DEFINE VARIABLE anzahl AS DECIMAL FORMAT ">>>,>>9.999". 
DEFINE VARIABLE wert AS DECIMAL. 
DEFINE VARIABLE tot-anz AS DECIMAL. 
DEFINE VARIABLE tot-wert AS DECIMAL. 
DEFINE VARIABLE avrg-price AS DECIMAL INITIAL 0. 
 
  anzahl = qty. 
  wert = qty * price. 
  wert = round(wert, 2). 
 
  DO transaction: 
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
          ASSIGN
            l-bestand.artnr        = s-artnr 
            l-bestand.anf-best-dat = billdate
          . 
        END.
        ASSIGN
          l-bestand.anz-eingang  = l-bestand.anz-eingang + anzahl 
          l-bestand.wert-eingang = l-bestand.wert-eingang + wert
        . 
        FIND CURRENT l-bestand NO-LOCK. 
        ASSIGN
          tot-anz  = l-bestand.anz-anf-best + l-bestand.anz-eingang 
            - l-bestand.anz-ausgang
          tot-wert = l-bestand.val-anf-best + l-bestand.wert-eingang 
            - l-bestand.wert-ausgang
        . 
        IF (tot-anz NE 0) AND (rcv-type NE 2) THEN 
        DO: 
          avrg-price = tot-wert / tot-anz. 
          FIND CURRENT l-artikel EXCLUSIVE-LOCK. 
          l-artikel.vk-preis = avrg-price. 
          FIND CURRENT l-artikel NO-LOCK. 
        END. 
      END. 
 
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
          l-liefumsatz.lief-nr = lief-nr
        . 
      END. 
      l-liefumsatz.gesamtumsatz = l-liefumsatz.gesamtumsatz + wert. 
      FIND CURRENT l-liefumsatz NO-LOCK. 
    END. 
 
/* Create l-op record */ 
    CREATE l-op. 
    BUFFER-COPY op-list TO l-op.
    ASSIGN l-op.pos     = curr-pos
           l-op.lief-nr = lief-nr
    .
    FIND CURRENT l-op NO-LOCK. 
 
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
          + translateExtended ("Incoming record for article ",lvCAREA,"") + STRING(s-artnr, "9999999")
          + " could not be created!!!" .
END. 


PROCEDURE create-l-op1: 
DEFINE VARIABLE anzahl AS DECIMAL FORMAT ">>>,>>9.999". 
DEFINE VARIABLE wert AS DECIMAL. 
DEFINE VARIABLE tot-anz AS DECIMAL. 
DEFINE VARIABLE tot-wert AS DECIMAL. 
DEFINE VARIABLE avrg-price AS DECIMAL INITIAL 0. 
DEFINE buffer l-art FOR l-artikel. 
  
  ASSIGN
    anzahl = qty 
    wert   = qty * price 
    wert   = ROUND(wert, 2)
  . 
 
/* Create l-op record  FOR outgoing */ 
  CREATE l-op. 
    BUFFER-COPY op-list TO l-op.
    ASSIGN l-op.pos         = op-list.lager-nr
           l-op.lief-nr     = lief-nr
           l-op.op-art      = 3 
           l-op.stornogrund = l-out-stornogrund
    .
    FIND CURRENT l-op NO-LOCK. 
 
  FIND FIRST l-art WHERE l-art.artnr = s-artnr NO-LOCK. 
  IF ((l-art.endkum = f-endkum OR l-art.endkum = b-endkum) 
    AND billdate LE fb-closedate) 
  OR (l-art.endkum GE m-endkum AND billdate LE m-closedate) THEN 
  DO: 
    FIND FIRST l-bestand WHERE l-bestand.lager-nr = op-list.lager-nr AND 
      l-bestand.artnr = s-artnr EXCLUSIVE-LOCK NO-ERROR. 
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
      AND l-pprice.counter = curr-anz USE-INDEX counter_ix NO-LOCK NO-ERROR. 
    IF AVAILABLE l-pprice AND l-pprice.einzelpreis = price 
      AND l-pprice.bestelldatum = /*l-order.bestelldatum*/ datum THEN RETURN. 
  END. 
*/  
  IF curr-anz GE max-anz THEN 
  DO: 
    FIND FIRST l-price1 WHERE l-price1.artnr = s-artnr 
      AND l-price1.counter = 1 USE-INDEX counter_ix EXCLUSIVE-LOCK NO-ERROR. 
    IF AVAILABLE l-price1 THEN 
    DO: 
      l-price1.docu-nr = lscheinnr. 
      l-price1.artnr = s-artnr. 
      l-price1.anzahl = qty. 
      l-price1.einzelpreis = price. 
      l-price1.warenwert = qty * price. 
      l-price1.bestelldatum = datum. 
      l-price1.lief-nr = lief-nr. 
      l-price1.counter = 0. 
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
    create l-pprice. 
    l-pprice.docu-nr = lscheinnr. 
    l-pprice.artnr = s-artnr. 
    l-pprice.anzahl = qty. 
    l-pprice.einzelpreis = price. 
    l-pprice.warenwert = qty * price. 
    l-pprice.bestelldatum = datum. 
    l-pprice.lief-nr = lief-nr. 
    l-pprice.counter = curr-anz + 1. 
    FIND CURRENT l-pprice NO-LOCK. 
    FIND CURRENT l-art EXCLUSIVE-LOCK. 
    l-art.lieferfrist = curr-anz + 1. 
    FIND CURRENT l-art NO-LOCK. 
  END. 
END. 

