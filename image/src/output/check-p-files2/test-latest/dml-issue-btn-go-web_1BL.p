
DEFINE TEMP-TABLE op-list LIKE l-op
    FIELD bezeich LIKE l-artikel.bezeich
    FIELD username AS CHAR
    FIELD dml-code AS CHAR. 

DEF INPUT-OUTPUT PARAMETER TABLE FOR op-list.
DEF INPUT PARAMETER billdate    AS DATE.
DEF INPUT PARAMETER closedate   AS DATE.
DEF INPUT PARAMETER curr-lager  AS INT.
DEF INPUT PARAMETER curr-dept   AS INT.
DEF INPUT PARAMETER cost-acct   AS CHAR.
DEF INPUT PARAMETER lief-nr     AS INT.
DEF INPUT PARAMETER lscheinnr   AS CHAR.
DEF INPUT PARAMETER user-init   AS CHAR.
DEF INPUT PARAMETER t-amount    AS DECIMAL FORMAT "->>,>>>,>>>,>>9.99". 

DEF OUTPUT PARAMETER curr-pos   AS INT.
DEF OUTPUT PARAMETER s-artnr    AS INT.
DEF OUTPUT PARAMETER qty        AS DECIMAL.
DEF OUTPUT PARAMETER price      AS DECIMAL.
DEF OUTPUT PARAMETER created    AS LOGICAL.
DEF OUTPUT PARAMETER err-code   AS INT INITIAL 0.

DEFINE VARIABLE gl-notfound AS LOGICAL.
DEFINE VARIABLE dml-code    AS CHAR.

/*FDL Feb 29, 2024 => Ticket 65A160*/
IF cost-acct NE "" AND cost-acct NE "00000000" AND cost-acct NE ? THEN
DO:
    FIND FIRST gl-acct WHERE gl-acct.fibukonto EQ cost-acct NO-LOCK NO-ERROR.
    IF NOT AVAILABLE gl-acct THEN
    DO:
        err-code = 1.
        RETURN.
    END.
END.

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
    err-code = 1.
    RETURN.
END.

FIND FIRST bediener WHERE bediener.userinit = user-init.
/* create l-ophdr FOR receiving */ 
FIND FIRST l-ophdr WHERE l-ophdr.lscheinnr = lscheinnr 
AND l-ophdr.op-typ = "STI" NO-LOCK NO-ERROR. 
IF NOT AVAILABLE l-ophdr THEN 
DO: 
  create l-ophdr. 
  l-ophdr.datum =  billdate.
  l-ophdr.lager-nr = curr-lager. 
  l-ophdr.lscheinnr = lscheinnr. 
  /* l-ophdr.fibukonto = cost-acct.  */ /* wrong field to keep COA by Oscar (11 November 2024) - A17C35 */
  l-ophdr.op-typ = "STI". 
  FIND CURRENT l-ophdr NO-LOCK. 
END. 

RUN l-op-pos(OUTPUT curr-pos). 
curr-pos = curr-pos - 1. 
FOR EACH op-list: 
  created = YES. 
  curr-pos = curr-pos + 1. 
  s-artnr = op-list.artnr. 
  qty = op-list.anzahl. 
  price = op-list.warenwert / qty. 
  dml-code = op-list.dml-code.
  RUN create-l-op. 
END. 
IF lief-nr NE 0 AND t-amount NE 0 THEN RUN create-ap.

FIND FIRST l-ophdr WHERE l-ophdr.lscheinnr = lscheinnr 
AND l-ophdr.op-typ = "STT" NO-LOCK NO-ERROR. 
IF NOT AVAILABLE l-ophdr THEN 
DO: 
  create l-ophdr. 
  l-ophdr.datum =  billdate. 
  l-ophdr.lager-nr = curr-lager. 
  l-ophdr.lscheinnr = lscheinnr. 
  l-ophdr.op-typ = "STT". 
  l-ophdr.fibukonto = cost-acct.
  FIND CURRENT l-ophdr NO-LOCK. 
END. 
RUN l-op-pos(OUTPUT curr-pos). 
curr-pos = curr-pos - 1. 
FOR EACH op-list: 
  curr-pos = curr-pos + 1. 
  s-artnr = op-list.artnr. 
  qty = op-list.anzahl. 
  price = op-list.warenwert / qty. 
  RUN create-l-op1. 
END.

/*ragung add validasi for close*/
FOR EACH queasy WHERE queasy.KEY = 331 
  AND (queasy.char2 EQ "Inv-Cek Reciving" 
       OR queasy.char2 EQ "Inv-Cek Reorg"
       OR queasy.char2 EQ "Inv-Cek Journal"):
  DELETE queasy.
END.


PROCEDURE l-op-pos: 
  DEFINE OUTPUT PARAMETER pos AS INTEGER INITIAL 0. 
  DEFINE buffer l-op1 FOR l-op. 
  ASSIGN pos = 1. 
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
 
  FIND FIRST l-artikel WHERE l-artikel.artnr = s-artnr NO-LOCK. 
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
 
  /* Create l-op record FOR incoming */ 
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
    l-op.herkunftflag = 2    /* 2 = Direct Issue (IN) */ 
    l-op.docu-nr      = dml-code /* Oscar (29/12/24) - F0ADB1 - fix cancel incoming on qty dml not going back to dml */
    l-op.lscheinnr    = lscheinnr 
    l-op.pos          = curr-pos 
    l-op.fuellflag    = bediener.nr
    l-op.flag         = YES
    l-op.stornogrund  = cost-acct /* fix wrong field to keep COA by Oscar (28 Oktober 2024) - A17C35 */
  . 
  FIND CURRENT l-op NO-LOCK. 
 
  /*
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
  END. */

  /*FDL Jan 03,2025: F3344B - Add validation NUM-ENTRIES*/
  IF curr-dept = 0 THEN 
  DO: 
      FIND FIRST d-art WHERE d-art.artnr = s-artnr AND d-art.datum = billdate
          /*AND ENTRY(2, d-art.chginit, ";") = dml-code*/
          AND NUM-ENTRIES(d-art.chginit,";") GT 1 NO-LOCK NO-ERROR.
      IF AVAILABLE d-art THEN DO:
          IF ENTRY(2, d-art.chginit, ";") NE "" AND ENTRY(2, d-art.chginit, ";") EQ dml-code THEN
          DO:
              FIND CURRENT d-art EXCLUSIVE-LOCK.
              d-art.geliefert = d-art.geliefert + anzahl. 
              FIND CURRENT d-art NO-LOCK. 
          END.          
      END.
      ELSE 
      DO:
          FIND FIRST d-art WHERE d-art.artnr = s-artnr AND d-art.datum = billdate NO-LOCK NO-ERROR.
          IF AVAILABLE d-art THEN 
          DO:
              FIND CURRENT d-art EXCLUSIVE-LOCK.
              d-art.geliefert = d-art.geliefert + anzahl. 
              FIND CURRENT d-art NO-LOCK. 
          END.
      END.
  END. 
  ELSE IF curr-dept > 0 THEN 
  DO: 
    FIND FIRST d-art1 WHERE d-art1.artnr = s-artnr AND d-art1.datum = billdate 
        AND d-art1.departement = curr-dept
        /*AND ENTRY(2, d-art1.chginit, ";") = dml-code*/
        AND NUM-ENTRIES(d-art.chginit,";") GT 1 NO-LOCK NO-ERROR.
    IF AVAILABLE d-art1 THEN DO:
        IF ENTRY(2, d-art.chginit, ";") NE "" AND ENTRY(2, d-art.chginit, ";") EQ dml-code THEN
        DO:
            FIND CURRENT d-art1 EXCLUSIVE-LOCK.
            d-art1.geliefert = d-art1.geliefert + anzahl. 
            FIND CURRENT d-art1 NO-LOCK. 
        END.        
    END.
    ELSE 
    DO:
        FIND FIRST reslin-queasy WHERE reslin-queasy.KEY EQ "DML"
            AND reslin-queasy.date1 EQ billdate
            AND INTEGER(ENTRY(1, reslin-queasy.char1, ";")) = s-artnr
            AND INTEGER(ENTRY(2, reslin-queasy.char1, ";")) = curr-dept
            /*AND ENTRY(2, reslin-queasy.char3, ";") = dml-code*/
            AND NUM-ENTRIES(reslin-queasy.char3,";") GT 1 NO-LOCK NO-ERROR.
        IF AVAILABLE reslin-queasy THEN 
        DO:
            IF ENTRY(2, reslin-queasy.char3, ";") NE "" AND ENTRY(2, reslin-queasy.char3, ";") EQ dml-code THEN
            DO:
                FIND CURRENT reslin-queasy EXCLUSIVE-LOCK.
                ASSIGN reslin-queasy.deci3 = reslin-queasy.deci3 + anzahl.
                FIND CURRENT reslin-queasy NO-LOCK.
            END.            
        END.
        ELSE DO:
            FIND FIRST d-art1 WHERE d-art1.artnr = s-artnr AND d-art1.datum = billdate 
                AND d-art1.departement = curr-dept NO-LOCK NO-ERROR.
            IF AVAILABLE d-art1 THEN DO:
                FIND CURRENT d-art1 EXCLUSIVE-LOCK.
                d-art1.geliefert = d-art1.geliefert + anzahl. 
                FIND CURRENT d-art1 NO-LOCK. 
            END.
        END.
    END.
  END. 
 
  RUN create-purchase-book(s-artnr, price, anzahl, billdate, lief-nr). 

  IF (l-artikel.ek-aktuell NE price) AND price NE 0  THEN 
  DO: 
    FIND CURRENT l-artikel EXCLUSIVE-LOCK. 
    l-artikel.ek-letzter = l-artikel.ek-aktuell. 
    l-artikel.ek-aktuell = price. 
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

PROCEDURE create-l-op1: 
  DEFINE VARIABLE anzahl AS DECIMAL. 
  DEFINE VARIABLE wert AS DECIMAL. 
  DEFINE VARIABLE tot-anz AS DECIMAL. 
  DEFINE VARIABLE tot-wert AS DECIMAL. 
  DEFINE VARIABLE avrg-price AS DECIMAL INITIAL 0. 
  
  ASSIGN
    anzahl = qty 
    wert   = qty * price 
    wert   = ROUND(wert, 2)
  . 
 
  /* Create l-op record  FOR outgoing */ 
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
    l-op.op-art       = 3
    l-op.herkunftflag = 2    /* 2 Direct Issue (out) */ 
    l-op.docu-nr      = dml-code /* Oscar (29/12/24) - F0ADB1 - fix cancel incoming on qty dml not going back to dml */
    l-op.lscheinnr    = lscheinnr 
    l-op.pos          = curr-pos 
    l-op.fuellflag    = bediener.nr 
    l-op.flag         = YES   /* flag indicates direct issue **/ 
    l-op.stornogrund  = cost-acct
  . 
  FIND CURRENT l-op NO-LOCK. 
 
  IF billdate LE closedate THEN 
  DO: 
    FIND FIRST l-bestand WHERE l-bestand.lager-nr = curr-lager AND 
      l-bestand.artnr = s-artnr EXCLUSIVE-LOCK NO-ERROR. 
    IF NOT AVAILABLE l-bestand THEN 
    DO: 
      CREATE l-bestand. 
      ASSIGN
        l-bestand.artnr        = s-artnr
        l-bestand.lager-nr     = curr-lager 
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
