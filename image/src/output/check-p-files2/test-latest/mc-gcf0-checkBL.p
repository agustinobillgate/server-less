
DEFINE TEMP-TABLE g-list       LIKE mc-guest.  
DEF BUFFER bbuff FOR bediener.
DEF BUFFER gbuff FOR mc-guest.
DEF BUFFER gast FOR guest.
DEF BUFFER tbuff FOR mc-types.
    
DEF INPUT  PARAMETER pvILanguage AS INTEGER          NO-UNDO.
DEF INPUT  PARAMETER gastno      AS INTEGER.
DEF INPUT  PARAMETER curr-mode   AS CHAR.
DEF INPUT  PARAMETER sales-id    AS CHAR.
DEF INPUT  PARAMETER nr          AS INTEGER.
DEF INPUT  PARAMETER cardnum     AS CHAR.
DEF OUTPUT PARAMETER err-code    AS INTEGER INIT 0.
DEF OUTPUT PARAMETER msg-str     AS CHAR.


{SupertransBL.i} 
DEF VAR lvCAREA AS CHAR INITIAL "mc-gcf". 

DEF VARIABLE gname AS CHAR INITIAL "".

FIND FIRST mc-guest WHERE mc-guest.gastnr = gastno NO-LOCK NO-ERROR.

IF sales-id NE "" THEN
DO:
    FIND FIRST bbuff WHERE bbuff.userinit = sales-id NO-LOCK NO-ERROR.
    IF NOT AVAILABLE bbuff THEN
    DO:
      msg-str = msg-str + CHR(2)
              + translateExtended ("No such Sales User Initial.",lvCAREA,"").
      err-code = 1.
      /*MTAPPLY "entry" TO g-list.sales-id.*/
      RETURN NO-APPLY.
    END.
END.

FIND FIRST mc-types WHERE mc-types.nr = nr NO-LOCK NO-ERROR.
IF NOT AVAILABLE mc-types THEN
DO:
  msg-str = msg-str + CHR(2)
          + translateExtended ("No such membership card type number.",lvCAREA,"").
  err-code = 2.
  /*MTAPPLY "entry" TO g-list.nr.*/
  RETURN NO-APPLY.
END.

IF curr-mode = "new" THEN
DO:
  FIND FIRST gbuff WHERE gbuff.cardnum = cardnum NO-LOCK NO-ERROR.
  IF AVAILABLE gbuff THEN
  DO:
    FIND FIRST gast WHERE gast.gastnr = gbuff.gastnr NO-LOCK NO-ERROR.
    IF AVAILABLE gast THEN gname = gast.NAME + " " + gast.vorname1
      + ", " + gast.anrede1.
    msg-str = msg-str + CHR(2)
            + translateExtended ("Card number already exist and owned by",lvCAREA,"")
            + " - " + gname.
    err-code = 3.
    /*MTAPPLY "entry" TO g-list.cardnum.*/
    RETURN NO-APPLY.
  END.
END.
ELSE IF curr-mode = "chg" THEN
DO:
  FIND FIRST gbuff WHERE gbuff.cardnum = cardnum 
    AND RECID(gbuff) NE RECID(mc-guest) NO-LOCK NO-ERROR.
  IF AVAILABLE gbuff THEN
  DO:
    FIND FIRST gast WHERE gast.gastnr = gbuff.gastnr NO-LOCK NO-ERROR.
    IF AVAILABLE gast THEN gname = gast.NAME + " " + gast.vorname1
      + ", " + gast.anrede1.
    msg-str = msg-str + CHR(2)
            + translateExtended ("Card number already exist and owned by",lvCAREA,"")
            + " - " + gname.
    err-code = 3.
    /*MTAPPLY "entry" TO g-list.cardnum.*/
    RETURN NO-APPLY.
  END.
  
  FIND FIRST tbuff WHERE tbuff.nr = mc-guest.nr NO-LOCK.

  IF nr NE mc-guest.nr AND tbuff.bezeich = "THE ONE" THEN
  DO:
      FIND FIRST mc-aclub WHERE mc-aclub.KEY = tbuff.nr
          AND mc-aclub.cardnum = mc-guest.cardnum NO-LOCK NO-ERROR.
      IF AVAILABLE mc-aclub THEN
      DO:
          msg-str = msg-str + CHR(2)
                  + translateExtended ("THE ONE Point transaction exists, TYPE changes no longer allowed.",lvCAREA,"").
          err-code = 4.
          /*MTAPPLY "entry" TO g-list.nr.*/
          RETURN NO-APPLY.
      END.
  END.

END.

/*MT
IF curr-mode = "new" THEN
DO TRANSACTION:
  g-list.created-date = ci-date.
  HIDE MESSAGE NO-PAUSE.
  MESSAGE translateExtended ("Confirm to create the membership card NOW?",lvCAREA,"")
    VIEW-AS ALERT-BOX QUESTION BUTTONS YES-NO UPDATE answer.
  IF NOT answer THEN 
  DO: 
    APPLY "entry" TO g-list.nr.
    RETURN NO-APPLY.
  END.
  CREATE mc-guest.
  RUN fill-mc-guest.
  ASSIGN mc-guest.userinit = user-init.
  RUN create-mcfee.
  HIDE btn-addname btn-ask1 btn-ask2.
  ENABLE btn-chgname WITH FRAME frame1.
  DISP bezeich WITH FRAME frame1.
  RUN assign-read-only(YES).
  curr-mode = "".
  APPLY "entry" TO g-list.nr.
  RETURN NO-APPLY.
END.
ELSE IF curr-mode = "chg" THEN
DO TRANSACTION:
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
    FOR mc-aclub WHERE mc-aclub.KEY = mc-types.nr
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
  HIDE btn-ask1 btn-ask2.
  ENABLE btn-chgname WITH FRAME frame1.
  DISP bezeich WITH FRAME frame1.
  RUN assign-read-only(YES).
  curr-mode = "".
  APPLY "entry" TO g-list.nr.
  RETURN NO-APPLY.
END.*/
