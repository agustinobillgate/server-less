DEFINE TEMP-TABLE op-list LIKE l-op
    FIELD fibu AS CHAR
    FIELD a-bezeich LIKE l-artikel.bezeich
    FIELD a-lief-einheit LIKE l-artikel.lief-einheit
    FIELD a-traubensort LIKE l-artikel.traubensort.
DEF TEMP-TABLE t-l-ophdr     LIKE l-ophdr
    FIELD rec-id AS INT.
DEFINE WORKFILE out-list 
  FIELD artnr AS INTEGER. 

DEF INPUT PARAMETER rec-id AS INT.
DEF INPUT PARAMETER out-type AS INT.
DEF INPUT PARAMETER t-lschein AS CHAR.
DEF INPUT PARAMETER t-datum AS DATE.
DEF INPUT PARAMETER user-init AS CHAR.

DEF INPUT-OUTPUT PARAMETER t-amount AS DECIMAL.

DEF OUTPUT PARAMETER lscheinnr AS CHAR.
DEF OUTPUT PARAMETER cost-acct AS CHAR.
DEF OUTPUT PARAMETER lager-bezeich AS CHAR.
DEF OUTPUT PARAMETER lager-bez1 AS CHAR.
DEF OUTPUT PARAMETER curr-lager AS INT.
DEF OUTPUT PARAMETER to-stock AS INT.
DEF OUTPUT PARAMETER to-stock-ro AS LOGICAL INIT NO.
DEF OUTPUT PARAMETER TABLE FOR t-l-ophdr.
DEF OUTPUT PARAMETER TABLE FOR op-list.

FIND FIRST bediener WHERE bediener.userinit = user-init.
FIND FIRST l-ophdr WHERE RECID(l-ophdr) = rec-id.
RUN read-request-records.

PROCEDURE read-request-records:
DEF VAR op-num AS INTEGER INITIAL 13 NO-UNDO.  /*outgoing*/
  IF out-type = 1 THEN op-num = 14.            /* transfer */
  lscheinnr = t-lschein.
  FOR EACH l-op WHERE l-op.datum = t-datum
      AND l-op.op-art = op-num
      AND l-op.lscheinnr = t-lschein 
      AND l-op.loeschflag LE 1 NO-LOCK BY l-op.artnr:
      FIND FIRST l-artikel WHERE l-artikel.artnr = l-op.artnr NO-LOCK.
      FIND FIRST gl-acct WHERE gl-acct.fibukonto = l-op.stornogrund
          NO-LOCK NO-ERROR.
      IF NOT AVAILABLE gl-acct THEN
          FIND FIRST gl-acct WHERE gl-acct.bezeich = l-op.stornogrund
          NO-LOCK NO-ERROR.
      CREATE op-list.
      ASSIGN
        curr-lager            = l-op.lager-nr
        to-stock              = l-op.pos
        op-list.lager-nr      = l-op.lager-nr
        op-list.artnr         = l-op.artnr
        op-list.zeit          = TIME
        op-list.anzahl        = l-op.anzahl
        op-list.einzelpreis   = l-artikel.vk-preis 
        op-list.warenwert     = l-artikel.vk-preis * l-op.anzahl 
        op-list.op-art        = l-op.op-art - 10 /* = 3 or 4 */
        op-list.herkunftflag  = 1 
        op-list.lscheinnr     = l-op.lscheinnr
        op-list.fuellflag     = bediener.nr
        op-list.pos           = 1 
        op-list.stornogrund   = l-op.stornogrund
        op-list.betriebsnr    = RECID(l-op)
        op-list.a-bezeich     = l-artikel.bezeich.
        t-amount              = t-amount + op-list.warenwert.
      . 
      IF out-type = 2 THEN
      DO:
          IF AVAILABLE gl-acct THEN cost-acct = gl-acct.fibukonto.
          ELSE cost-acct = l-op.stornogrund.
      END.

      IF AVAILABLE gl-acct THEN
          ASSIGN
            op-list.stornogrund = gl-acct.bezeich
            op-list.fibu = gl-acct.fibukonto
            .
  END.
  IF out-type = 2 THEN to-stock = 0.

  CREATE out-list. 
  out-list.artnr = l-artikel.artnr. 

  FIND FIRST l-lager WHERE l-lager.lager-nr = curr-lager NO-LOCK NO-ERROR. 
  IF AVAILABLE l-lager THEN lager-bezeich = l-lager.bezeich. 
  
  IF out-type = 1 THEN
  DO:
    FIND FIRST l-lager WHERE l-lager.lager-nr = to-stock NO-LOCK NO-ERROR. 
    IF AVAILABLE l-lager THEN lager-bez1 = l-lager.bezeich.
    to-stock-ro = YES.
    /*MTASSIGN to-stock:READ-ONLY IN FRAME frame1 = YES.*/
  END.

  DO TRANSACTION: 
    FIND CURRENT l-ophdr EXCLUSIVE-LOCK.
    ASSIGN
      l-ophdr.docu-nr   = t-lschein
      l-ophdr.lscheinnr = t-lschein 
      l-ophdr.op-typ    = "STT"
    . 
    FIND CURRENT l-ophdr NO-LOCK.
    CREATE t-l-ophdr.
    BUFFER-COPY l-ophdr TO t-l-ophdr.
    ASSIGN t-l-ophdr.rec-id = RECID(l-ophdr).
  END.
END.
