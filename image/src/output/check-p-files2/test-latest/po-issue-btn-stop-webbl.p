
DEFINE TEMP-TABLE op-list LIKE l-op
    FIELD rec-id AS INTEGER.

DEF TEMP-TABLE t-l-order LIKE l-order
    FIELD rec-id AS INT
    FIELD a-bezeich AS CHARACTER
    FIELD jahrgang AS INTEGER
    FIELD alkoholgrad AS DECIMAL
    FIELD curr-disc AS INTEGER
    FIELD curr-disc2 AS INTEGER
    FIELD curr-vat AS INTEGER.

DEFINE INPUT PARAMETER user-init        AS CHAR    NO-UNDO.
DEFINE INPUT PARAMETER l-orderhdr-recid AS INTEGER NO-UNDO.
DEFINE INPUT PARAMETER f-endkum         AS INTEGER NO-UNDO.
DEFINE INPUT PARAMETER b-endkum         AS INTEGER NO-UNDO.
DEFINE INPUT PARAMETER m-endkum         AS INTEGER NO-UNDO.
DEFINE INPUT PARAMETER fb-closedate     AS DATE    NO-UNDO.
DEFINE INPUT PARAMETER m-closedate      AS DATE    NO-UNDO.
DEFINE INPUT PARAMETER lief-nr          AS INTEGER NO-UNDO.
DEFINE INPUT PARAMETER billdate         AS DATE    NO-UNDO.
DEFINE INPUT PARAMETER docu-nr          AS CHAR    NO-UNDO.
DEFINE INPUT PARAMETER lscheinnr        AS CHAR    NO-UNDO.
DEFINE INPUT PARAMETER curr-lager       AS INTEGER NO-UNDO.
DEFINE INPUT PARAMETER t-amount         AS DECIMAL NO-UNDO.
DEFINE INPUT PARAMETER jobnr            AS INTEGER NO-UNDO.
DEFINE INPUT PARAMETER curr-disc        AS INTEGER NO-UNDO.
DEFINE INPUT PARAMETER crterm           AS INTEGER NO-UNDO.
DEFINE INPUT PARAMETER TABLE FOR op-list.
DEFINE INPUT PARAMETER TABLE FOR t-l-order.
DEFINE OUTPUT PARAMETER fl-code         AS INTEGER NO-UNDO.

DEFINE VARIABLE gl-notfound AS LOGICAL.

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
    fl-code = 2.
    RETURN.
END.

FIND FIRST bediener WHERE bediener.userinit = user-init NO-LOCK NO-ERROR.

FOR EACH op-list:
    
    FIND FIRST t-l-order WHERE t-l-order.rec-id = op-list.rec-id NO-LOCK NO-ERROR.
    IF AVAILABLE t-l-order THEN DO:
        FIND FIRST l-order WHERE RECID(l-order) = t-l-order.rec-id NO-LOCK NO-ERROR.
        FIND FIRST l-art WHERE l-art.artnr = t-l-order.artnr NO-LOCK NO-ERROR.
        FIND FIRST l-orderhdr WHERE RECID(l-orderhdr) = l-orderhdr-recid NO-LOCK NO-ERROR.
        
        RUN create-l-op.
    END.
END.

IF lief-nr NE 0 THEN RUN create-ap.
RUN close-po.

PROCEDURE create-l-op:
    DEFINE VARIABLE anzahl AS DECIMAL FORMAT ">>>,>>9.999". 
    DEFINE VARIABLE wert AS DECIMAL. 
    DEFINE VARIABLE tot-wert AS DECIMAL. 
    DEFINE VARIABLE tot-anz AS DECIMAL. 
    DEFINE buffer l-order1 FOR l-order. 
    DEFINE VARIABLE curr-pos AS INTEGER. 

    FIND CURRENT l-order EXCLUSIVE-LOCK. 
    MESSAGE l-order.geliefert op-list.anzahl VIEW-AS ALERT-BOX.
    
    ASSIGN 
        l-order.geliefert       = l-order.geliefert + op-list.anzahl
        /*l-order.angebot-lief[1] = t-l-order.angebot-lief[1]*/
        l-order.lief-fax[2]     = bediener.username
        l-order.rechnungspreis  = t-l-order.rechnungspreis 
        l-order.rechnungswert   = l-order.rechnungswert + t-l-order.rechnungswert
        l-order.lieferdatum-eff = t-l-order.lieferdatum-eff 
        l-order.stornogrund = op-list.stornogrund. 
    FIND CURRENT l-order NO-LOCK.

    FIND FIRST l-order1 WHERE l-order1.docu-nr = l-orderhdr.docu-nr 
        AND l-order1.pos = 0 EXCLUSIVE-LOCK NO-ERROR.
    IF AVAILABLE l-order1 THEN
    DO:
        ASSIGN
          l-order1.rechnungspreis = l-order1.rechnungspreis + op-list.einzelpreis
          l-order1.rechnungswert  = l-order1.rechnungswert + op-list.einzelpreis. 
        FIND CURRENT l-order1 NO-LOCK.
    END.

  IF l-art.ek-aktuell NE op-list.einzelpreis THEN 
  DO: 
    FIND CURRENT l-art EXCLUSIVE-LOCK. 
    l-art.ek-letzter = l-art.ek-aktuell. 
    l-art.ek-aktuell = op-list.einzelpreis. 
    FIND CURRENT l-art NO-LOCK. 
  END. 

  /* UPDATE supplier turnover */ 
  FIND FIRST  l-liefumsatz WHERE l-liefumsatz.lief-nr = op-list.lief-nr 
    AND l-liefumsatz.datum = billdate EXCLUSIVE-LOCK NO-ERROR. 
  IF NOT AVAILABLE l-liefumsatz THEN 
  DO: 
    CREATE l-liefumsatz. 
    ASSIGN
        l-liefumsatz.datum   = billdate 
        l-liefumsatz.lief-nr = lief-nr. 
  END. 
  l-liefumsatz.gesamtumsatz = l-liefumsatz.gesamtumsatz + op-list.einzelpreis. 

  CREATE l-op.
  BUFFER-COPY op-list TO l-op.
  RUN l-op-pos(OUTPUT curr-pos). 
  ASSIGN
     l-op.pos       = curr-pos
     l-op.fuellflag = bediener.nr
     l-op.flag      = yes. 
  FIND CURRENT l-op NO-LOCK. 

  RUN create-purchase-book. 

  /* Create l-op record  FOR outgoing */ 
  CREATE l-op. 
  ASSIGN
      l-op.datum        = op-list.datum 
      l-op.lager-nr     = op-list.lager-nr
      l-op.artnr        = op-list.artnr 
      l-op.lief-nr      = op-list.lief-nr 
      l-op.zeit         = TIME  
      l-op.anzahl       = op-list.anzahl 
      l-op.einzelpreis  = op-list.einzelpreis 
      l-op.warenwert    = op-list.warenwert 
      l-op.op-art       = 3 
      l-op.herkunftflag = 2    /* 4 = inventory !!! */ 
      l-op.docu-nr      = op-list.docu-nr
      l-op.lscheinnr    = op-list.lscheinnr 
      l-op.pos          = curr-pos 
      l-op.fuellflag    = bediener.nr
      l-op.flag         = YES   /* flag indicates direct issue **/ 
      l-op.stornogrund  = op-list.stornogrund. 
  FIND CURRENT l-op NO-LOCK. 

  /* create l-ophdr FOR incoming */ 
  FIND FIRST l-ophdr WHERE l-ophdr.lscheinnr = op-list.lscheinnr 
    AND l-ophdr.op-typ = "STI" NO-LOCK NO-ERROR. 
  IF NOT AVAILABLE l-ophdr THEN 
  DO: 
    CREATE l-ophdr. 
    ASSIGN
        l-ophdr.datum     = op-list.datum
        l-ophdr.lager-nr  = op-list.lager-nr
        l-ophdr.docu-nr   = op-list.docu-nr 
        l-ophdr.lscheinnr = op-list.lscheinnr
        l-ophdr.op-typ    = "STI". 
    FIND CURRENT l-ophdr NO-LOCK. 
  END. 
 
/* create l-ophdr  FOR outgoing */ 
  FIND FIRST l-ophdr WHERE l-ophdr.lscheinnr = op-list.lscheinnr  
    AND l-ophdr.op-typ = "STT" NO-LOCK NO-ERROR. 
  IF NOT AVAILABLE l-ophdr THEN 
  DO: 
    CREATE l-ophdr. 
    ASSIGN
        l-ophdr.datum       = op-list.datum 
        l-ophdr.lager-nr    = op-list.lager-nr
        l-ophdr.docu-nr     = op-list.docu-nr 
        l-ophdr.lscheinnr   = op-list.lscheinnr
        l-ophdr.op-typ      = "STT" 
        l-ophdr.fibukonto   = op-list.stornogrund
        l-ophdr.betriebsnr  = jobnr. 
    FIND CURRENT l-ophdr NO-LOCK. 
  END. 

  IF ((l-art.endkum = f-endkum OR l-art.endkum = b-endkum) 
    AND billdate LE fb-closedate) 
  OR (l-art.endkum GE m-endkum AND billdate LE m-closedate) THEN 
  DO: 
    FIND FIRST l-bestand WHERE l-bestand.lager-nr = op-list.lager-nr AND 
      l-bestand.artnr = l-art.artnr EXCLUSIVE-LOCK NO-ERROR. 
    IF NOT AVAILABLE l-bestand THEN 
    DO: 
      CREATE l-bestand. 
      ASSIGN
          l-bestand.lager-nr        = op-list.lager-nr
          l-bestand.artnr           = l-art.artnr 
          l-bestand.anf-best-dat    = billdate. 
    END. 
    ASSIGN
        l-bestand.anz-eingang   = l-bestand.anz-eingang + op-list.anzahl
        l-bestand.wert-eingang  = l-bestand.wert-eingang + op-list.warenwert
        l-bestand.anz-ausgang   = l-bestand.anz-ausgang + op-list.anzahl 
        l-bestand.wert-ausgang  = l-bestand.wert-ausgang + op-list.warenwert. 
    FIND CURRENT l-bestand NO-LOCK. 
 
    FIND FIRST l-bestand WHERE l-bestand.lager-nr = 0 AND 
      l-bestand.artnr = l-art.artnr EXCLUSIVE-LOCK NO-ERROR. 
    IF NOT AVAILABLE l-bestand THEN 
    DO: 
      CREATE l-bestand. 
      ASSIGN
          l-bestand.lager-nr        = 0
          l-bestand.artnr           = l-art.artnr 
          l-bestand.anf-best-dat    = billdate. 
    END. 
    ASSIGN
        l-bestand.anz-eingang   = l-bestand.anz-eingang + op-list.anzahl 
        l-bestand.wert-eingang  = l-bestand.wert-eingang + op-list.warenwert
        l-bestand.anz-ausgang   = l-bestand.anz-ausgang + op-list.anzahl 
        l-bestand.wert-ausgang  = l-bestand.wert-ausgang + op-list.warenwert. 
    FIND CURRENT l-bestand NO-LOCK. 
  END. 

END.


PROCEDURE l-op-pos: 
DEFINE OUTPUT PARAMETER pos AS INTEGER INITIAL 0. 
DEFINE buffer l-op1 FOR l-op. 
  pos = 1. 
END. 

PROCEDURE create-purchase-book: 
DEFINE VARIABLE max-anz AS INTEGER. 
DEFINE VARIABLE curr-anz AS INTEGER. 
DEFINE VARIABLE created AS LOGICAL INITIAL NO. 
DEFINE VARIABLE i AS INTEGER. 
DEFINE BUFFER l-price1 FOR l-pprice. 

  FIND FIRST htparam WHERE paramnr = 225 no-lock.  /* max stored p-price */ 
  max-anz = htparam.finteger.               /* Rulita 211024 | Fixing for serverless */  
  IF max-anz = 0 THEN max-anz = 1. 
  curr-anz = l-art.lieferfrist. 

  IF curr-anz GE max-anz THEN 
  DO: 
    FIND FIRST l-price1 WHERE l-price1.artnr = l-op.artnr 
      AND l-price1.counter = 1 USE-INDEX counter_ix EXCLUSIVE-LOCK NO-ERROR. 
    IF AVAILABLE l-price1 THEN 
    DO: 
      ASSIGN
          l-price1.docu-nr      = l-op.docu-nr
          l-price1.artnr        = l-op.artnr 
          l-price1.anzahl       = l-op.anzahl 
          l-price1.einzelpreis  = l-op.einzelpreis
          l-price1.warenwert    = l-op.warenwert 
          l-price1.bestelldatum = l-op.datum 
          l-price1.lief-nr      = l-op.lief-nr
          l-price1.counter      = 0. 
          created = YES. 
    END. 
    DO i = 2 TO curr-anz: 
      FIND FIRST l-pprice WHERE l-pprice.artnr = l-op.artnr 
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
        l-pprice.docu-nr        = l-op.docu-nr 
        l-pprice.artnr          = l-op.artnr 
        l-pprice.anzahl         = l-op.anzahl 
        l-pprice.einzelpreis    = l-op.einzelpreis
        l-pprice.warenwert      = l-op.warenwert
        l-pprice.bestelldatum   = l-op.datum 
        l-pprice.lief-nr        = l-op.lief-nr
        l-pprice.counter        = curr-anz + 1 
        l-pprice.betriebsnr     = curr-disc. 
    FIND CURRENT l-pprice NO-LOCK. 
    FIND CURRENT l-art EXCLUSIVE-LOCK. 
    l-art.lieferfrist = curr-anz + 1. 
    FIND CURRENT l-art NO-LOCK. 
  END. 
END. 

PROCEDURE create-ap: 
DEFINE VARIABLE ap-license AS LOGICAL INITIAL NO. 
DEFINE VARIABLE ap-acct AS CHAR. 
DEFINE VARIABLE do-it AS LOGICAL INITIAL YES. 
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

  FIND FIRST htparam WHERE paramnr = 1016. 
  ap-license = htparam.flogical. 
  
  IF ap-license AND do-it THEN 
  DO: 
    CREATE l-kredit. 
    ASSIGN 
    l-kredit.name        = docu-nr 
    l-kredit.lief-nr     = lief-nr 
    l-kredit.lscheinnr   = lscheinnr 
    l-kredit.rgdatum     = billdate 
    l-kredit.saldo       = t-amount 
    l-kredit.ziel        = crterm 
    l-kredit.netto       = t-amount 
    l-kredit.bediener-nr = bediener.nr. 
 
    create ap-journal. 
    ASSIGN 
    ap-journal.lief-nr      = lief-nr 
    ap-journal.docu-nr      = docu-nr 
    ap-journal.lscheinnr    = lscheinnr 
    ap-journal.rgdatum      = billdate 
    ap-journal.saldo        = t-amount 
    ap-journal.netto        = t-amount 
    ap-journal.userinit     = bediener.userinit 
    ap-journal.zeit         = TIME. 
  END. 
END. 

PROCEDURE close-po:  /* A/P is still OPEN / NOT yet paid   */ 
DEFINE buffer l-od FOR l-order. 
DEFINE VARIABLE closed AS LOGICAL INIT YES.
 
  /*FIND FIRST l-od WHERE l-od.docu-nr = docu-nr AND 
    l-od.pos GT 0 AND (l-od.anzahl GT l-od.geliefert) AND 
    l-od.loeschflag = 0 NO-LOCK NO-ERROR. 
  IF AVAILABLE l-od THEN RETURN. */

  FOR EACH l-od WHERE l-od.docu-nr = docu-nr AND l-od.artnr GT 0 AND 
    l-od.pos GT 0 AND l-od.loeschflag = 0 NO-LOCK,
    FIRST l-artikel WHERE l-artikel.artnr = l-od.artnr NO-LOCK:
    IF (l-od.anzahl * l-artikel.lief-einheit) GT l-od.geliefert THEN
    DO:
       closed = NO.
       LEAVE.
    END.
  END.

  IF NOT closed THEN RETURN.
 
  FIND FIRST l-od WHERE l-od.docu-nr = docu-nr AND 
    l-od.pos EQ 0 EXCLUSIVE-LOCK. 
  l-od.loeschflag = 1. 
  l-od.lieferdatum-eff = billdate. 
  l-od.lief-fax[3] = bediener.username. 
  FIND CURRENT l-od NO-LOCK. 
 
  FOR EACH l-od WHERE l-od.docu-nr = docu-nr AND 
     l-od.pos GT 0 AND l-od.loeschflag = 0 EXCLUSIVE-LOCK: 
    l-od.loeschflag = 1. 
    l-od.lieferdatum = billdate. 
    release l-od. 
  END.
  fl-code = 1.
END. 



