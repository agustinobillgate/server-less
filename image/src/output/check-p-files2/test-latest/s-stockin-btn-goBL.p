DEFINE TEMP-TABLE op-list LIKE l-op
    FIELD a-bezeich LIKE l-artikel.bezeich.

DEF INPUT-OUTPUT PARAMETER s-artnr  AS INT NO-UNDO.
DEF INPUT-OUTPUT PARAMETER qty      AS DECIMAL NO-UNDO.
DEF INPUT  PARAMETER TABLE FOR op-list.
DEF INPUT  PARAMETER f-endkum       AS INT.
DEF INPUT  PARAMETER b-endkum       AS INT.
DEF INPUT  PARAMETER m-endkum       AS INT.
DEF INPUT  PARAMETER lief-nr        AS INT.
DEF INPUT  PARAMETER lscheinnr      AS CHAR.
DEF INPUT  PARAMETER billdate       AS DATE.
DEF INPUT  PARAMETER curr-lager     AS INT.
DEF INPUT  PARAMETER fb-closedate   AS DATE.
DEF INPUT  PARAMETER m-closedate    AS DATE.
DEF INPUT  PARAMETER bediener-nr    AS INT.
DEF INPUT  PARAMETER bediener-userinit AS CHAR.

DEF OUTPUT PARAMETER err-flag       AS INT INIT 0.
DEF OUTPUT PARAMETER err-flag2      AS INT INIT 0.
DEF OUTPUT PARAMETER price          AS DECIMAL.
DEF OUTPUT PARAMETER created        AS LOGICAL.
DEF OUTPUT PARAMETER printer-nr     AS INT.

DEFINE VARIABLE curr-pos AS INTEGER.
DEFINE VARIABLE t-amount AS DECIMAL FORMAT "->,>>>,>>>,>>9.99".
DEFINE VARIABLE pos      AS INTEGER INITIAL 0. 

/*   IF NOT created THEN */ 
DO:
  FIND FIRST l-op WHERE l-op.op-art = 1 AND l-op.loeschflag LE 1
    AND l-op.lscheinnr = lscheinnr NO-LOCK NO-ERROR.
  IF AVAILABLE l-op THEN
  DO:
    err-flag = 1.
    RETURN NO-APPLY. 
  END.
END.

  /* create l-ophdr  */ 
FIND FIRST l-ophdr WHERE l-ophdr.lscheinnr = lscheinnr 
    AND l-ophdr.op-typ = "STI" AND l-ophdr.datum = billdate 
    AND l-ophdr.lager-nr = curr-lager NO-LOCK NO-ERROR. 
IF NOT AVAILABLE l-ophdr THEN 
DO: 
    create l-ophdr. 
    l-ophdr.datum =  billdate. 
    l-ophdr.lager-nr = curr-lager. 
    l-ophdr.lscheinnr = lscheinnr. 
    l-ophdr.op-typ = "STI". 
    FIND CURRENT l-ophdr NO-LOCK. 
END.

/*****************************************************/
RUN l-op-pos(OUTPUT curr-pos). 
curr-pos = curr-pos - 1.
 
t-amount = 0.
FOR EACH op-list:
    ASSIGN
      op-list.docu-nr   = lscheinnr
      op-list.lscheinnr = lscheinnr
      curr-pos = curr-pos + 1
      s-artnr = op-list.artnr
      qty = op-list.anzahl
      price = op-list.warenwert / qty
      t-amount = t-amount + op-list.warenwert
    .
    
    RUN create-l-op.
    created = YES.
    /*
    IF (endkum = f-endkum OR endkum = b-endkum)
      AND billdate LE fb-closedate THEN created = YES.
    IF endkum GE m-endkum AND billdate LE m-closedate THEN created = YES.
    */
END.

IF lief-nr NE 0 AND t-amount NE 0 THEN 
DO:
    RUN create-ap.
END.
    

RUN htpint.p (220, OUTPUT printer-nr).


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


PROCEDURE create-l-op: 
DEFINE VARIABLE anzahl AS DECIMAL FORMAT ">>>,>>9.999". 
DEFINE VARIABLE wert AS DECIMAL. 
DEFINE VARIABLE tot-anz AS DECIMAL. 
DEFINE VARIABLE tot-wert AS DECIMAL. 
DEFINE VARIABLE avrg-price AS DECIMAL INITIAL 0. 
 
   
  FIND FIRST l-artikel WHERE l-artikel.artnr = s-artnr NO-LOCK NO-ERROR.
  ASSIGN 
      anzahl = qty /*agung * l-artikel.lief-einheit ITA 010916*/
      wert = qty * price
      wert = round(wert, 2).
  
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
          create l-bestand. 
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
        l-bestand.anz-eingang = l-bestand.anz-eingang + anzahl
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
        create l-liefumsatz. 
        l-liefumsatz.datum = billdate. 
        l-liefumsatz.lief-nr = lief-nr. 
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
      l-artikel.ek-letzter = l-artikel.ek-aktuell. 
      l-artikel.ek-aktuell = price. 
      FIND CURRENT l-artikel NO-LOCK. 
    END. 
    RETURN. 
  END. 
  err-flag2 = 1.
END. 


PROCEDURE create-ap: 
DEFINE VARIABLE ap-license AS LOGICAL INITIAL NO. 
DEFINE VARIABLE ap-acct AS CHAR. 
DEFINE VARIABLE do-it AS LOGICAL INITIAL YES. 
DEFINE buffer l-op1 FOR l-op. 
  
  FIND FIRST l-op1 WHERE l-op1.lscheinnr = lscheinnr 
    AND l-op1.loeschflag = 0 AND l-op1.pos GE 1 NO-LOCK NO-ERROR. 
  IF NOT AVAILABLE l-op1 THEN 
  DO:
    err-flag = 2.
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
  
  FIND FIRST htparam WHERE paramnr = 1016 NO-LOCK. 
  ap-license = htparam.flogical. 
  IF ap-license AND do-it THEN 
  DO: 
    create l-kredit. 
    l-kredit.name = lscheinnr. 
    l-kredit.lief-nr = lief-nr. 
    l-kredit.lscheinnr = lscheinnr. 
    l-kredit.rgdatum = billdate. 
    l-kredit.datum = ?. 
    l-kredit.saldo = t-amount. 
    l-kredit.ziel = 30. 
    l-kredit.netto = t-amount. 
    l-kredit.bediener-nr = bediener-nr. 
 
    create ap-journal. 
    ap-journal.lief-nr = lief-nr. 
    ap-journal.docu-nr = lscheinnr. 
    ap-journal.lscheinnr = lscheinnr. 
    ap-journal.rgdatum = billdate. 
    ap-journal.saldo = t-amount. 
    ap-journal.netto = t-amount. 
    ap-journal.userinit = bediener-userinit. 
    ap-journal.zeit = time. 
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
DEFINE BUFFER l-art FOR l-artikel. 
DEFINE BUFFER l-price1 FOR l-pprice. 
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

