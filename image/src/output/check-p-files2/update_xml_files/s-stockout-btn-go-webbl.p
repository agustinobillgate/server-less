DEFINE TEMP-TABLE op-list LIKE l-op
  FIELD fibu AS CHAR
  FIELD a-bezeich LIKE l-artikel.bezeich
  FIELD a-lief-einheit LIKE l-artikel.lief-einheit
  FIELD a-traubensort LIKE l-artikel.traubensort.

DEFINE TEMP-TABLE stock-oh-tmp
  FIELD stock-oh  AS DECIMAL
  FIELD artnr     AS INTEGER.
  
DEFINE WORKFILE out-list 
  FIELD artnr AS INTEGER. 

DEF INPUT-OUTPUT PARAMETER TABLE FOR op-list.
DEF INPUT PARAMETER pvILanguage  AS INTEGER  NO-UNDO.
DEF INPUT PARAMETER out-type     AS INTEGER. 
DEF INPUT PARAMETER rec-id       AS INT.
DEF INPUT PARAMETER curr-lager   AS INT.
DEF INPUT PARAMETER jobnr        AS INT.
DEF INPUT PARAMETER cost-acct    AS CHAR.
DEF INPUT PARAMETER transdate    AS DATE.
DEF INPUT PARAMETER t-datum      AS DATE.
DEF INPUT PARAMETER transfered   AS LOGICAL.
DEF INPUT PARAMETER t-lschein    AS CHAR.
DEF INPUT PARAMETER to-stock     AS INT.
DEF INPUT PARAMETER lscheinnr    AS CHAR.
DEF INPUT PARAMETER bediener-nr  AS INT.

DEF INPUT-OUTPUT PARAMETER qty         AS DECIMAL.
DEF INPUT-OUTPUT PARAMETER t-amount    AS DECIMAL.

DEF OUTPUT PARAMETER s-artnr     AS INT.
DEF OUTPUT PARAMETER err-flag    AS INT INIT 0.
DEF OUTPUT PARAMETER price       AS DECIMAL.
DEF OUTPUT PARAMETER amount      AS DECIMAL.
DEF OUTPUT PARAMETER msg-str2    AS CHAR.
DEF OUTPUT PARAMETER msg-str3    AS CHAR.
DEF OUTPUT PARAMETER req-CREATEd AS LOGICAL INIT NO.

{SupertransBL.i} 
DEF VAR lvCAREA AS CHAR INITIAL "s-stockout".

DEFINE VARIABLE curr-pos    AS INT.
DEFINE VARIABLE zeit        AS INT.
DEFINE VARIABLE gl-notfound AS LOGICAL.

IF NOT transfered THEN
DO:
  /*FDL Feb 29, 2024 => Ticket 65A160*/
  IF cost-acct NE "" AND cost-acct NE "00000000" AND cost-acct NE ? THEN
  DO:
      FIND FIRST gl-acct WHERE gl-acct.fibukonto EQ cost-acct NO-LOCK NO-ERROR.
      IF NOT AVAILABLE gl-acct THEN
      DO:
          err-flag = 1.
          RETURN.
      END.
  END.

  FOR EACH op-list WHERE op-list.fibu NE ""
      AND op-list.fibu NE "00000000"
      AND op-list.fibu NE ?:

      FIND FIRST gl-acct WHERE gl-acct.fibukonto EQ op-list.fibu NO-LOCK NO-ERROR.
      IF NOT AVAILABLE gl-acct THEN
      DO:
          gl-notfound = YES.
          LEAVE.
      END.
  END.
  IF gl-notfound THEN 
  DO:
      err-flag = 1.
      RETURN.
  END.
END.

FIND FIRST l-ophdr WHERE RECID(l-ophdr) = rec-id.

DEF VAR its-ok AS LOGICAL.
/*MT 10/01/10 */
RUN check-min-oh.
RUN check-qty(OUTPUT its-ok). 
IF NOT its-ok THEN RETURN NO-APPLY. 
/*MT 10/01/10 */

DO TRANSACTION: 
    FIND CURRENT l-ophdr EXCLUSIVE-LOCK. 
    l-ophdr.datum =  transdate. 
    l-ophdr.lager-nr = curr-lager. 
    IF NOT transfered THEN 
    DO: 
      l-ophdr.fibukonto = cost-acct. 
      l-ophdr.betriebsnr = jobnr. 
    END. 
    FIND CURRENT l-ophdr NO-LOCK. 
END. 
RUN l-op-pos(OUTPUT curr-pos). 
curr-pos = curr-pos - 1. 
  
zeit = TIME. 
FOR EACH op-list WHERE op-list.anzahl NE 0: 
    zeit = zeit + 1. 
    curr-pos = curr-pos + 1. 
    s-artnr = op-list.artnr. 
    qty = op-list.anzahl.
    price = op-list.warenwert / qty. 
    curr-lager = op-list.lager-nr. 
    cost-acct = op-list.fibu.
    RUN create-l-op (zeit). 
END. 
  
FOR EACH out-list: 
    DELETE out-list. 
END. 
 
IF t-lschein NE "" THEN
DO:
    RUN update-request-records.
    /*MTAPPLY "choose" TO btn-stop.
    RETURN NO-APPLY.*/
END.

FOR EACH op-list: 
    DELETE op-list. 
END. 

PROCEDURE create-l-op: 
  DEFINE INPUT PARAMETER zeit AS INTEGER. 
  DEFINE VARIABLE anzahl AS DECIMAL FORMAT "->,>>>,>>9.999". 
  DEFINE VARIABLE wert AS DECIMAL. 
  
  DEFINE VARIABLE anz-oh   AS DECIMAL. 
  DEFINE VARIABLE val-oh   AS DECIMAL. 
  DEFINE VARIABLE stock-oh AS DECIMAL.

 
  FIND FIRST l-bestand WHERE l-bestand.lager-nr = 0 
    AND l-bestand.artnr = s-artnr NO-LOCK. 

  anz-oh = l-bestand.anz-anf-best + l-bestand.anz-eingang - l-bestand.anz-ausgang. 
  val-oh = l-bestand.val-anf-best + l-bestand.wert-eingang - l-bestand.wert-ausgang. 

  IF anz-oh NE 0 THEN 
  DO: 
    price = val-oh / anz-oh. 
    wert = qty * price. 
  END. 
 
  anzahl = qty. 
  wert = qty * price. 
  amount = wert. 
  t-amount = t-amount + wert. 
 
  /* UPDATE stock onhand  */ 
  IF NOT transfered THEN 
  DO: 
    FIND CURRENT l-bestand EXCLUSIVE-LOCK. 
    l-bestand.anz-ausgang = l-bestand.anz-ausgang + anzahl. 
    l-bestand.wert-ausgang = l-bestand.wert-ausgang + wert. 
    FIND CURRENT l-bestand NO-LOCK. 
  END. 

  /* Oscar (02/04/25) - ACE54F - retrieve to-stock to sync between 
  inter store transfer report and edit storage in store requisition */
  RUN get-to-stock (op-list.lscheinnr, op-list.artnr, OUTPUT to-stock).

  FIND FIRST l-bestand WHERE l-bestand.artnr = op-list.artnr 
      AND l-bestand.lager-nr = op-list.lager-nr NO-LOCK. 

  /* Oscar (13/04/25) - ACE54F - adjust for user story 1  */
  IF AVAILABLE l-bestand THEN
  DO:
      CREATE stock-oh-tmp.
      ASSIGN 
          stock-oh-tmp.stock-oh  = l-bestand.anz-anf-best + l-bestand.anz-eingang - l-bestand.anz-ausgang
          stock-oh-tmp.artnr     = l-bestand.artnr
      .
      stock-oh = l-bestand.anz-anf-best + l-bestand.anz-eingang - l-bestand.anz-ausgang.
  END.
 
  /* Oscar (13/04/25) - ACE54F - adjust for user story 1  */
  IF stock-oh GT 0 THEN
  DO:
    FIND FIRST l-bestand WHERE l-bestand.lager-nr = curr-lager 
      AND l-bestand.artnr = s-artnr EXCLUSIVE-LOCK. 
    l-bestand.anz-ausgang = l-bestand.anz-ausgang + anzahl. 
    l-bestand.wert-ausgang = l-bestand.wert-ausgang + wert. 
    FIND CURRENT l-bestand NO-LOCK. 
  
    IF transfered THEN 
    DO: 
      FIND FIRST l-bestand WHERE l-bestand.lager-nr = to-stock 
        AND l-bestand.artnr = s-artnr EXCLUSIVE-LOCK NO-ERROR. 
      IF NOT AVAILABLE l-bestand THEN 
      DO: 
        CREATE l-bestand. 
        l-bestand.anf-best-dat = transdate. 
        l-bestand.artnr = s-artnr. 
        l-bestand.lager-nr = to-stock. 
      END. 
      l-bestand.anz-eingang = l-bestand.anz-eingang + anzahl. 
      l-bestand.wert-eingang = l-bestand.wert-eingang + wert. 
      FIND CURRENT l-bestand NO-LOCK. 
    END. 
  
    /* CREATE l-op record */ 
    CREATE l-op. 
    l-op.datum = transdate. 
    l-op.lager-nr = curr-lager. 
    l-op.artnr = s-artnr. 
    l-op.zeit = /*FTzeit*/ op-list.zeit. 
    l-op.anzahl = anzahl. 
    l-op.einzelpreis = price. 
    l-op.warenwert = wert.

    IF NOT transfered THEN l-op.op-art = 3. 
    ELSE l-op.op-art = 4. 

    l-op.herkunftflag = 1.    /* 4 = inventory !!! */ 
    l-op.lscheinnr = lscheinnr. 

    IF NOT transfered THEN 
    DO: 
      l-op.pos = curr-pos. 

      IF op-list.fibu NE "" THEN l-op.stornogrund = op-list.fibu.
      ELSE l-op.stornogrund = cost-acct. 
    END. 
    ELSE l-op.pos = to-stock. 

    l-op.fuellflag = bediener-nr. 

    FIND CURRENT l-op NO-LOCK. 
  
    /**
    IF NOT transfered AND jobnr NE 0 THEN 
      RUN create-lartjob.p(RECID(l-ophdr), s-artnr, anzahl, wert, transdate, YES). 
    */
  
    IF transfered THEN 
    DO: 
      CREATE l-op. 
      l-op.datum = transdate. 
      l-op.lager-nr = to-stock. 
      l-op.artnr = s-artnr. 
      l-op.zeit = /*FTzeit*/ op-list.zeit. 
      l-op.anzahl = anzahl. 
      l-op.einzelpreis = price. 
      l-op.warenwert = wert. 
      l-op.op-art = 2. 
      l-op.herkunftflag = 1.    /* 4 = inventory !!! */ 
      l-op.lscheinnr = lscheinnr. 
      l-op.pos = curr-lager. 
      l-op.fuellflag = bediener-nr. 

      FIND CURRENT l-op NO-LOCK. 
    END. 
  
    /* UPDATE consumption */ 
    IF NOT transfered THEN 
    DO: 
    FIND FIRST l-verbrauch WHERE l-verbrauch.artnr = s-artnr 
      AND l-verbrauch.datum = transdate EXCLUSIVE-LOCK NO-ERROR. 
    IF NOT AVAILABLE l-verbrauch THEN 
    DO: 
      CREATE l-verbrauch. 
      l-verbrauch.artnr = s-artnr. 
      l-verbrauch.datum = transdate. 
    END. 
    l-verbrauch.anz-verbrau = l-verbrauch.anz-verbrau + anzahl. 
    l-verbrauch.wert-verbrau = l-verbrauch.wert-verbrau + wert. 
    FIND CURRENT l-verbrauch NO-LOCK. 
    END. 
  END.
END. 


PROCEDURE l-op-pos: 
  DEFINE OUTPUT PARAMETER pos AS INTEGER INITIAL 0. 
  DEFINE buffer l-op1 FOR l-op. 
  FOR EACH l-op1 WHERE l-op1.lscheinnr = lscheinnr 
    AND l-op1.loeschflag GE 0 AND l-op1.pos GT 0 NO-LOCK: 
      IF l-op1.pos GT pos THEN pos = l-op1.pos. 
  END. 
  pos = pos + 1. 
END. 
 
PROCEDURE check-min-oh:
  DEF VAR curr-oh    AS DECIMAL NO-UNDO INIT 0.
  DEF BUFFER bbuff   FOR l-bestand.

  FOR EACH op-list:
    FIND FIRST l-artikel WHERE l-artikel.artnr = op-list.artnr NO-LOCK.
    IF l-artikel.min-bestand NE 0 THEN
    DO:
      FOR EACH l-bestand WHERE l-bestand.artnr = l-artikel.artnr
        AND l-bestand.lager-nr > 0 NO-LOCK:
          curr-oh = l-bestand.anz-anf-best + l-bestand.anz-eingang - l-bestand.anz-ausgang.

          IF curr-oh LT l-artikel.min-best THEN
          DO:
            msg-str2 = msg-str2 + "&W" + translateExtended ("One (or more) stock item(s) under Minimum Onhand Level!",lvCAREA,"")
                     + CHR(10)
                     + STRING(l-artikel.artnr) + " " + l-artikel.bezeich
                     + CHR(10)
                     + translateExtended ("Current Onhand:",lvCAREA,"") 
                     + " " + STRING(curr-oh) 
                     + " <> " + translateExtended ("Minimum Onhand:",lvCAREA,"")
                     + " " + STRING(l-artikel.min-best).
            LEAVE.
          END.
      END.
    END.
  END.
END.

PROCEDURE check-qty: 
  DEFINE OUTPUT PARAMETER its-ok AS LOGICAL INITIAL YES. 
  DEFINE VARIABLE curr-oh AS DECIMAL. 

  FOR EACH op-list: 
    FIND FIRST l-bestand WHERE l-bestand.artnr = op-list.artnr 
      AND l-bestand.lager-nr = op-list.lager-nr NO-LOCK. 

    curr-oh = l-bestand.anz-anf-best + l-bestand.anz-eingang - l-bestand.anz-ausgang. 
    /* Oscar (13/04/25) - ACE54F - adjust for user story 1  */
    IF curr-oh LT op-list.anzahl AND curr-oh GT 0 THEN 
    DO: 
      FIND FIRST l-artikel WHERE l-artikel.artnr = op-list.artnr NO-LOCK. 
      msg-str3 = msg-str3 + translateExtended ("Wrong quantity: ",lvCAREA,"") + STRING(l-artikel.artnr) + " - " 
               + l-artikel.bezeich 
               + CHR(10)
               + translateExtended ("Inputted quantity =",lvCAREA,"") 
               + " " + STRING(op-list.anzahl) 
               + translateExtended (" - Stock onhand =",lvCAREA,"") 
               + " " + STRING(curr-oh) 
               + CHR(10)
               + translateExtended ("POSTING NOT POSSIBLE",lvCAREA,"").
      its-ok = NO. 
      RETURN. 
    END. 
  END. 
END. 


PROCEDURE update-request-records:
  DEF BUFFER lbuff FOR l-op.
  DEF VAR op-num AS INTEGER INITIAL 13 NO-UNDO.  /*outgoing*/

  IF out-type = 1 THEN op-num = 14.            /* transfer */
  ASSIGN req-CREATEd = YES.

  FIND FIRST l-op WHERE l-op.datum = t-datum
    AND l-op.op-art = op-num
    AND l-op.lscheinnr = t-lschein NO-LOCK NO-ERROR.

  DO WHILE AVAILABLE l-op:
    DO TRANSACTION:
      /*FIND FIRST op-list WHERE op-list.betriebsnr = INTEGER(RECID(l-op)) NO-ERROR.*/
      FIND FIRST op-list WHERE op-list.artnr = l-op.artnr NO-ERROR.    /*can't do outgoing qty*/ /*Gerald 121120 AA6ABF*/
      FIND FIRST lbuff WHERE RECID(lbuff) = RECID(l-op) EXCLUSIVE-LOCK.

      ASSIGN lbuff.herkunftflag = 2.
      IF AVAILABLE op-list THEN 
      DO:
          /* Oscar (13/04/25) - ACE54F - adjust for user story 1  */
          FIND FIRST stock-oh-tmp WHERE stock-oh-tmp.artnr EQ op-list.artnr NO-LOCK NO-ERROR.
          IF AVAILABLE stock-oh-tmp THEN
          DO:
              IF stock-oh-tmp.stock-oh GT 0 THEN
                  lbuff.deci1[1] = op-list.anzahl.
          END.

          /* Oscar (09/01/25) - 88AA99 - fix coa is not saved on modify in store requisition */
          IF op-list.fibu NE "" THEN lbuff.stornogrund = op-list.fibu.
          ELSE lbuff.stornogrund = cost-acct.
      END.
      FIND CURRENT lbuff NO-LOCK.
      RELEASE lbuff.
    END.

    FIND NEXT l-op WHERE l-op.datum = t-datum
      AND l-op.op-art = op-num
      AND l-op.lscheinnr = t-lschein NO-LOCK NO-ERROR.
  END.
END.

/* Oscar (02/04/25) - ACE54F - retrieve to-stock to sync between 
  inter store transfer report and edit storage in store requisition */
PROCEDURE get-to-stock:
  DEFINE INPUT PARAMETER lscheinnr AS CHARACTER.
  DEFINE INPUT PARAMETER artnr     AS INTEGER.

  DEFINE OUTPUT PARAMETER to-stock AS INTEGER.

  DEFINE BUFFER buffer-l-op FOR l-op. 

  FIND FIRST buffer-l-op WHERE buffer-l-op.lscheinnr EQ lscheinnr
    AND buffer-l-op.artnr EQ artnr NO-LOCK NO-ERROR.
  IF AVAILABLE buffer-l-op THEN
  DO:
    to-stock = buffer-l-op.pos.
  END.
  ELSE
  DO:
    to-stock = 0.
  END.
END.
