DEFINE TEMP-TABLE g-list       LIKE mc-guest.

DEF INPUT PARAMETER TABLE FOR g-list.
DEF INPUT PARAMETER curr-mode AS CHAR.
DEF INPUT PARAMETER user-init AS CHAR.
DEF INPUT PARAMETER gastno    AS INTEGER.

FIND FIRST g-list.

IF curr-mode = "new" THEN
DO TRANSACTION:
    CREATE mc-guest.
    RUN fill-mc-guest.
    ASSIGN mc-guest.userinit = user-init.
    RUN create-mcfee.
END.

ELSE IF curr-mode = "chg" THEN
DO:
  DEF BUFFER tbuff FOR mc-types.
  DO TRANSACTION:
      FIND FIRST mc-guest WHERE mc-guest.gastnr = gastno NO-LOCK NO-ERROR.
      FIND FIRST mc-types WHERE mc-types.nr = g-list.nr NO-LOCK NO-ERROR.
      FIND FIRST tbuff WHERE tbuff.nr = mc-guest.nr NO-LOCK.
      IF g-list.cardnum NE mc-guest.cardnum THEN
      DO:
          CREATE mc-cardhis.
          ASSIGN
              mc-cardhis.gastnr   = gastno
              mc-cardhis.old-card = mc-guest.cardnum
              mc-cardhis.new-card = g-list.cardnum
              mc-cardhis.old-nr   = mc-guest.nr
              mc-cardhis.new-nr   = g-list.nr
              mc-cardhis.zeit     = TIME
              mc-cardhis.userinit = user-init
          .
      END.
      IF (g-list.fdate NE mc-guest.fdate) OR (g-list.tdate NE mc-guest.tdate) THEN
      DO:
        FIND FIRST mc-fee WHERE mc-fee.KEY = 1 AND mc-fee.gastnr = gastno
          AND mc-fee.von-datum = mc-guest.fdate 
          AND mc-fee.bis-datum = mc-guest.tdate EXCLUSIVE-LOCK NO-ERROR.
        IF AVAILABLE mc-fee THEN
        DO:
          ASSIGN
            mc-fee.von-datum = g-list.fdate
            mc-fee.bis-datum = g-list.tdate
          .
          FIND CURRENT mc-fee NO-LOCK.
        END.
      END.

      IF g-list.activeflag NE mc-guest.activeflag
          AND tbuff.bezeich = "THE ONE" THEN
      DO:
          FIND FIRST mc-aclub WHERE mc-aclub.KEY = mc-types.nr
              AND mc-aclub.cardnum = mc-guest.cardnum EXCLUSIVE-LOCK
              NO-ERROR.
          IF AVAILABLE mc-aclub THEN
          DO:
            ASSIGN
              mc-aclub.logi1 = NOT g-list.activeflag
              mc-aclub.date1 = TODAY
              mc-aclub.char1 = user-init
            .
          END.
      END.

      IF g-list.cardnum NE mc-guest.cardnum 
          AND tbuff.bezeich = "THE ONE" THEN
      DO:
      DEF BUFFER mcbuff FOR mc-aclub.  
        FOR EACH mc-aclub WHERE mc-aclub.KEY = mc-types.nr
          AND mc-aclub.cardnum = mc-guest.cardnum NO-LOCK:
          FIND FIRST mcbuff WHERE RECID(mcbuff) = RECID(mc-aclub)
              EXCLUSIVE-LOCK.
          mcbuff.cardnum = g-list.cardnum.
          FIND CURRENT mcbuff NO-LOCK.
        END.
      END.

      FIND CURRENT mc-guest EXCLUSIVE-LOCK.
      RUN fill-mc-guest.
      ASSIGN mc-guest.changed = user-init + " - " + STRING(TODAY)
          + " " + STRING(TIME,"HH:MM:SS").
      FIND CURRENT mc-guest NO-LOCK.
  END.
END.




PROCEDURE create-mcfee:
  FIND FIRST mc-types WHERE mc-types.nr = g-list.nr NO-LOCK.
  IF mc-types.joinfee = 0 THEN RETURN.
  CREATE mc-fee.
  ASSIGN
      mc-fee.KEY = 1
      mc-fee.nr = g-list.nr
      mc-fee.gastnr = gastno
      mc-fee.betrag = mc-types.joinfee
      mc-fee.von-datum = g-list.fdate
      mc-fee.bis-datum = g-list.tdate
  .
  FIND CURRENT mc-fee NO-LOCK.
END.

PROCEDURE fill-mc-guest:  
  BUFFER-COPY g-list TO mc-guest.
END.  

