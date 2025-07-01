DEFINE TEMP-TABLE s-list 
    FIELD name          AS CHAR
    FIELD nat           AS CHAR
    FIELD ankunft       AS DATE
    FIELD abreise       AS DATE
    FIELD sharerflag    AS LOGICAL
    FIELD accompflag    AS LOGICAL
    FIELD added         AS LOGICAL
    FIELD gastnr        AS INTEGER
    . 

DEFINE INPUT PARAMETER TABLE FOR s-list.
DEFINE INPUT PARAMETER user-init AS CHAR    NO-UNDO.
DEFINE INPUT PARAMETER lname  AS CHAR       NO-UNDO.
DEFINE INPUT PARAMETER fname  AS CHAR       NO-UNDO.
DEFINE INPUT PARAMETER ftitle AS CHAR       NO-UNDO.
DEFINE INPUT PARAMETER mresnr AS INTEGER    NO-UNDO. 
DEFINE INPUT PARAMETER mreslinnr AS INTEGER NO-UNDO. 

DEFINE OUTPUT PARAMETER sh-created AS LOGICAL.
/*
DEF VAR user-init AS CHAR INIT "01".
DEF VAR name AS CHAR INIT "".
DEF VAR fname AS CHAR INIT "".
DEF VAR ftitle AS CHAR INIT "".
DEF VAR mresnr AS INT INIT 16695.
DEF VAR mreslinnr AS INT INIT 1.
DEF VAR sh-created AS LOGICAL.
*/

DEFINE VARIABLE vipnr1 AS INTEGER INITIAL 999999999. 
DEFINE VARIABLE vipnr2 AS INTEGER INITIAL 999999999. 
DEFINE VARIABLE vipnr3 AS INTEGER INITIAL 999999999. 
DEFINE VARIABLE vipnr4 AS INTEGER INITIAL 999999999. 
DEFINE VARIABLE vipnr5 AS INTEGER INITIAL 999999999. 
DEFINE VARIABLE vipnr6 AS INTEGER INITIAL 999999999. 
DEFINE VARIABLE vipnr7 AS INTEGER INITIAL 999999999. 
DEFINE VARIABLE vipnr8 AS INTEGER INITIAL 999999999. 
DEFINE VARIABLE vipnr9 AS INTEGER INITIAL 999999999. 

DEFINE VARIABLE room-qty AS INTEGER NO-UNDO.
DEFINE VARIABLE priscilla-active AS LOGICAL NO-UNDO INITIAL YES.

DEFINE BUFFER resline FOR res-line.

FIND FIRST res-line WHERE res-line.resnr = mresnr 
    AND res-line.reslinnr = mreslinnr 
    AND res-line.active-flag LE 1 NO-LOCK.
FIND FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK. 
ASSIGN room-qty = res-line.zimmeranz.

RUN create-rmsharer.

PROCEDURE create-rmsharer: 
DEFINE VARIABLE gcf-found AS LOGICAL INITIAL NO. 
DEFINE VARIABLE created AS LOGICAL INITIAL NO NO-UNDO. 
  FOR EACH s-list: 
    IF room-qty GT 1 OR 
        SUBSTR(s-list.name,1,11) NE "Room Sharer" THEN 
    DO: 
      RUN check-name(s-list.name).
      FIND FIRST guest WHERE guest.gastnr = s-list.gastnr 
          NO-LOCK NO-ERROR.
      gcf-found = (AVAILABLE guest). 
      IF AVAILABLE guest AND s-list.nat NE guest.nation1 
        AND s-list.nat NE "" THEN 
      DO: 
        FIND CURRENT guest EXCLUSIVE-LOCK. 
        ASSIGN
            guest.nation1 = s-list.nat
            guest.land    = s-list.nat 
            guest.char2   = user-init
        . 
        FIND CURRENT guest NO-LOCK. 
      END. 
      IF NOT AVAILABLE guest THEN RUN create-gcf. 
      RUN create-resline. 
      created = YES. 
    END. 
  END. 
  IF created THEN 
  DO: 
    FIND CURRENT res-line EXCLUSIVE-LOCK. 
    res-line.kontakt-nr = res-line.reslinnr. 
    FIND CURRENT res-line NO-LOCK. 
  END. 
END. 


PROCEDURE check-name: 
  DEFINE INPUT PARAMETER inp-name AS CHAR. 
  DEFINE VARIABLE i AS INTEGER. 
  DEFINE VARIABLE n AS INTEGER INITIAL 1. 
  DEFINE VARIABLE m AS INTEGER. 
  DEFINE VARIABLE len AS INTEGER. 

  IF room-qty GT 1 THEN
  DO:
      FIND FIRST guest WHERE guest.gastnr = s-list.gastnr NO-LOCK.
      ASSIGN
          lname  = guest.NAME
          fname  = guest.vorname1
          ftitle = guest.anrede1
      .
      RETURN.
  END.

  ASSIGN
      lname  = "" 
      fname  = "" 
      ftitle = ""
  .   
  DO i = 1 TO NUM-ENTRIES(inp-name, ","):
      CASE i:
          WHEN 1 THEN lname  = TRIM(ENTRY(1, inp-name, ",")).
          WHEN 2 THEN fname  = TRIM(ENTRY(2, inp-name, ",")).
          WHEN 3 THEN ftitle = TRIM(ENTRY(3, inp-name, ",")).
      END CASE.
  END.
END. 

PROCEDURE create-gcf: 
DEFINE VARIABLE curr-gastnr AS INTEGER NO-UNDO.   
  
  FIND LAST guest NO-LOCK NO-ERROR. 
  IF AVAILABLE guest THEN curr-gastnr = guest.gastnr + 1. 
  ELSE curr-gastnr = 1. 
   
  CREATE guest. 
  ASSIGN 
    guest.gastnr    = curr-gastnr 
    guest.karteityp = 0
    guest.nation1   = s-list.nat 
    guest.land      = s-list.nat
    guest.name      = lname 
    guest.vorname1  = fname 
    guest.anrede1   = ftitle 
    guest.char1     = user-init
  . 
  FIND CURRENT guest NO-LOCK. 
 
  CREATE guestseg. 
  ASSIGN 
    guestseg.gastnr = guest.gastnr 
    guestseg.reihenfolge = 1 
    guestseg.segmentcode = reservation.segmentcode. 
  FIND CURRENT guestseg NO-LOCK.
  RELEASE guestseg. 

END. 

PROCEDURE create-resline: 
DEFINE VARIABLE reslinnr AS INTEGER INITIAL 0. 
  FOR EACH resline WHERE resline.resnr = res-line.resnr 
      NO-LOCK BY resline.reslinnr DESCENDING: 
      reslinnr = resline.reslinnr + 1. 
      LEAVE.
  END. 
  CREATE resline. 
  ASSIGN 
    resline.resnr          = res-line.resnr 
    resline.reslinnr       = reslinnr 
    resline.name           = s-list.name 
    resline.gastnr         = res-line.gastnr 
    resline.gastnrpay      = guest.gastnr 
    resline.gastnrmember   = guest.gastnr 
    resline.ankunft        = s-list.ankunft 
    resline.abreise        = s-list.abreise 
    resline.l-zuordnung[3] = INTEGER(NOT s-list.sharerflag)
    resline.anztage        = resline.abreise - resline.ankunft 
    resline.erwachs        = 0 
    resline.zimmeranz      = room-qty 
    resline.zikatnr        = res-line.zikatnr 
    resline.zinr           = res-line.zinr 
    resline.arrangement    = res-line.arrangement 
    resline.grpflag        = res-line.grpflag 
    resline.kontignr       = 0 
    resline.reserve-int    = res-line.reserve-int 
    resline.setup          = res-line.setup 
    resline.adrflag        = res-line.adrflag 
    resline.was-status     = res-line.was-status 
    resline.kontakt-nr     = res-line.reslinnr 
    resline.betriebsnr     = res-line.betriebsnr 
    resline.reserve-char   = STRING(today) + STRING(time,"HH:MM") + user-init
    resline.resstatus      = 11
  .
  IF NOT s-list.sharerflag THEN 
  DO:    
    IF res-line.active-flag = 1 THEN 
    ASSIGN 
        resline.resstatus   = 13
        resline.active-flag = 1
        resline.ankzeit = TIME
    .
  END.

  IF priscilla-active THEN
  DO:
      RUN intevent-1.p(11, resline.zinr, "Priscilla", resline.resnr, resline.reslinnr). 
  END.

  RUN store-vip. 
  FIND CURRENT resline NO-LOCK. 
  sh-created = YES. 
END. 


PROCEDURE store-vip: 
  IF guest.karteityp NE 0 THEN RETURN. 
  FIND FIRST guestseg WHERE guestseg.gastnr = guest.gastnr 
    AND (guestseg.segmentcode = vipnr1 OR 
     guestseg.segmentcode = vipnr2 OR 
     guestseg.segmentcode = vipnr3 OR 
     guestseg.segmentcode = vipnr4 OR 
     guestseg.segmentcode = vipnr5 OR 
     guestseg.segmentcode = vipnr6 OR 
     guestseg.segmentcode = vipnr7 OR 
     guestseg.segmentcode = vipnr8 OR 
     guestseg.segmentcode = vipnr9) NO-LOCK NO-ERROR. 
  IF AVAILABLE guestseg THEN resline.betrieb-gastmem = guestseg.segmentcode. 
END. 
