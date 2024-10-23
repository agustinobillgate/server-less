  
 
/*  Program FOR Check-in a guest  */ 
 
DEFINE INPUT  PARAMETER pvILanguage     AS INTEGER NO-UNDO.
DEFINE INPUT  PARAMETER resnr           AS INTEGER. 
DEFINE INPUT  PARAMETER reslinnr        AS INTEGER. 
DEFINE INPUT  PARAMETER silenzio        AS LOGICAL. 
DEFINE OUTPUT PARAMETER can-checkin     AS LOGICAL INITIAL NO. 
DEFINE OUTPUT PARAMETER msg-str         AS CHAR INIT "".
DEFINE OUTPUT PARAMETER msg-str1        AS CHAR INIT "".
DEFINE OUTPUT PARAMETER msg-str2        AS CHAR INIT "".
DEFINE OUTPUT PARAMETER msg-str3        AS CHAR INIT "".
DEFINE OUTPUT PARAMETER msg-str4        AS CHAR INIT "".
DEFINE OUTPUT PARAMETER err-number1     AS INT INIT 0.
DEFINE OUTPUT PARAMETER err-number2     AS INT INIT 0.
DEFINE OUTPUT PARAMETER err-number3     AS INT INIT 0.
DEFINE OUTPUT PARAMETER err-number4     AS INT INIT 0.
DEFINE OUTPUT PARAMETER fill-gcfemail   AS LOGICAL INIT NO.
DEFINE OUTPUT PARAMETER gast-gastnr     AS INTEGER.
DEFINE OUTPUT PARAMETER q-143           AS LOGICAL INIT NO.
DEFINE OUTPUT PARAMETER flag-report     AS LOGICAL INIT NO.
DEFINE OUTPUT PARAMETER warn-flag       AS LOGICAL NO-UNDO INIT NO.
/* 
DEFINE VARIABLE resnr AS INTEGER INITIAL 2977. 
DEFINE VARIABLE reslinnr AS INTEGER INITIAL 2. 
DEFINE VARIABLE silenzio AS LOGICAL INITIAL NO. 
DEFINE VARIABLE checked-in AS LOGICAL. 
*/ 

DEFINE BUFFER res-member    FOR res-line. 
DEFINE BUFFER res-sharer    FOR res-line. 
DEFINE BUFFER res-line1     FOR res-line. 
DEFINE BUFFER gast          FOR guest. 
 
{SupertransBL.i} 
DEF VAR lvCAREA AS CHAR INITIAL "res-checkin". 

FIND FIRST res-line WHERE res-line.resnr = resnr 
  AND res-line.reslinnr = reslinnr NO-LOCK. 
 
IF res-line.active-flag = 1 THEN 
DO: 
  msg-str = translateExtended ("Guest already checked-in.",lvCAREA,"").
  RETURN. 
END. 
 
IF res-line.zimmeranz GT 1 THEN 
DO: 
  msg-str = translateExtended ("Wrong room quantity.",lvCAREA,"").
  RETURN. 
END. 
 
FIND FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK. 

IF (reservation.depositgef - reservation.depositbez - 
    reservation.depositbez2) GT 0 THEN 
DO: 
  msg-str = translateExtended ("Deposit not yet settled, check-in not possible",lvCAREA,"").
  RETURN. 
END. 

FIND FIRST gast WHERE gast.gastnr = res-line.gastnrmember NO-LOCK.

IF gast.karteityp NE 0 THEN
DO:
  msg-str = translateExtended ("Guest Type must be individual guest.",lvCAREA,"").
  RETURN.
END.

FIND FIRST res-line1 WHERE res-line1.resstatus = 6 
  AND res-line1.zinr = res-line.zinr 
  AND RECID(res-line1) NE RECID(res-line) NO-LOCK NO-ERROR. 
IF NOT AVAILABLE res-line1 THEN
FIND FIRST res-line1 WHERE res-line1.resstatus = 13 
  AND res-line1.zinr = res-line.zinr 
  AND res-line1.l-zuordnung[3] = 0
  AND RECID(res-line1) NE RECID(res-line) NO-LOCK NO-ERROR. 
IF AVAILABLE res-line1 THEN 
DO: 
  IF res-line1.resstatus = 6 THEN
  DO:
    IF (res-line.resstatus LE 2) OR (res-line.resstatus = 5) 
      OR (res-line.resstatus = 11 AND (res-line.resnr NE res-line1.resnr)) THEN 
    DO: 
      msg-str = translateExtended ("Room",lvCAREA,"") + " " 
        + res-line1.zinr + " " 
        + translateExtended ("occupied by : ",lvCAREA,"") 
        + res-line1.NAME + CHR(10)
        + translateExtended ("Check-out date:",lvCAREA,"") 
        + " " + STRING(res-line1.abreise).
      RETURN.
    END.
  END. 
  ELSE IF res-line1.resstatus = 13 THEN
  DO:
    IF res-line.resnr NE res-line1.resnr THEN 
    DO:
      msg-str = translateExtended ("Room",lvCAREA,"") + " " 
        + res-line1.zinr + " " 
        + translateExtended ("occupied by : ",lvCAREA,"") 
        + res-line1.NAME + CHR(10)
        + translateExtended ("Check-out date:",lvCAREA,"") 
        + " " + STRING(res-line1.abreise).
     RETURN.
    END.
  END.
  IF res-line.resstatus = 11 AND res-line1.resstatus = 6
    AND res-line1.abreise LT res-line.abreise THEN 
  DO: 
    msg-str = translateExtended ("Room",lvCAREA,"") + " " + res-line1.zinr 
        + ": " + translateExtended ("Main guest will checkout earlier than room sharer",lvCAREA,"")
        + CHR(10)
        + "==> " + translateExtended ("Check-in of sharing guest not possible",lvCAREA,""). 
    RETURN. 
  END. 
END.

IF res-line.zinr NE "" THEN
DO:
    FIND FIRST zimmer WHERE zimmer.zinr = res-line.zinr NO-LOCK. 
    IF zimmer.zistatus EQ 1  THEN 
    DO:
      msg-str = translateExtended ("Room ",lvCAREA,"") + zimmer.zinr 
          + " " + translateExtended ("Status: Clean not Checked",lvCAREA,"") + CHR(10)
          + translateExtended ("Check-in not possible - Contact House Keeping.",lvCAREA,"").
      RETURN. 
    END. 

    ELSE IF zimmer.zistatus = 2 THEN 
    DO: 
      msg-str = translateExtended ("Room",lvCAREA,"") + " " + zimmer.zinr 
        + " " + translateExtended ("Status: Vacant Dirty",lvCAREA,"") + CHR(10)
        + translateExtended ("Check-in not possible.",lvCAREA,"").
      RETURN. 
    END. 

    ELSE IF zimmer.zistatus = 6 THEN 
    DO: 
      msg-str = translateExtended ("Room",lvCAREA,"") 
        + " " + zimmer.zinr + " " 
        + translateExtended ("Status = Out-Of-Order.",lvCAREA,"") + CHR(10)
        + translateExtended ("Checkin not possible.",lvCAREA,"").
      RETURN. 
    END. 

    IF res-line.resstatus = 11 THEN 
    DO: 
        FIND FIRST res-member WHERE res-member.resnr = res-line.resnr 
          AND res-member.resstatus LE 6 
          AND res-member.zinr = res-line.zinr NO-LOCK NO-ERROR. 
        IF NOT AVAILABLE res-member THEN 
        DO: 
          msg-str = translateExtended ("Room",lvCAREA,"") 
            + " " + zimmer.zinr + ": " 
            + translateExtended ("No main guest found.",lvCAREA,"").
          RETURN. 
        END. 
        ELSE IF res-member.resstatus NE 6 THEN 
        DO: 
          warn-flag = YES.
          msg-str = "&W"
              + translateExtended ("Room",lvCAREA,"") 
              + " " + zimmer.zinr + CHR(10)
              + translateExtended ("The main guest",lvCAREA,"") 
              + " " + res-member.name 
              + " " + translateExtended ("not yet checked-in.",lvCAREA,""). 
        END. 
    END.
END.

FIND FIRST reslin-queasy WHERE reslin-queasy.key = "flag" 
  AND reslin-queasy.resnr = res-line.resnr 
  AND reslin-queasy.reslinnr = res-line.reslinnr 
  AND reslin-queasy.betriebsnr = 0 NO-LOCK NO-ERROR. 
flag-report = AVAILABLE reslin-queasy.

FIND FIRST nation WHERE nation.kurzbez = gast.land NO-LOCK NO-ERROR. 
IF NOT AVAILABLE nation THEN
DO:
  msg-str1 = translateExtended ("Guest COUNTRY not defined:",lvCAREA,"") 
    + " " + gast.land.
  err-number1 = 1.
END.

FIND FIRST nation WHERE nation.kurzbez = gast.nation1 NO-LOCK NO-ERROR. 
IF NOT AVAILABLE nation THEN
DO:
  msg-str2 = translateExtended ("Guest NATIONALITY not defined:",lvCAREA,"") 
    + " " + gast.nation1.
  err-number2 = 1.
END.


gast-gastnr   = gast.gastnr.

IF gast.email-adr = "" THEN /*Email mandatory*/
DO:
  FIND FIRST htparam WHERE htparam.paramnr = 249 NO-LOCK.
  IF htparam.paramgr = 6 AND htparam.flogical THEN
  DO:
      ASSIGN 
          fill-gcfemail = YES.
  END.
END.

IF TRIM(gast.telefon) = "" AND TRIM(gast.mobil-telefon) = "" THEN /*Phone Mandatory*/
DO:
  FIND FIRST htparam WHERE htparam.paramnr = 279 NO-LOCK.
  IF htparam.paramgr = 6 AND htparam.flogical THEN
  DO:
      ASSIGN 
          msg-str = msg-str + CHR(3) + "YES".
  END.
END.

IF NOT res-line.zimmer-wunsch MATCHES ("*SEGM_PUR*") THEN
DO:
  msg-str3 = translateExtended ("Purpose of Stay not assigned.",lvCAREA,"").
  FIND FIRST queasy WHERE queasy.KEY = 143 NO-LOCK NO-ERROR.
  IF AVAILABLE queasy THEN q-143 = YES.
  err-number3 = 1.
END.

IF res-line.zinr EQ "" THEN 
DO: 
  msg-str4 = translateExtended ("Room number not assigned.",lvCAREA,"").
  err-number4 = 1.
END.

can-checkin = (err-number1 = 0 AND err-number2 = 0 
           AND err-number3 = 0 AND err-number4 = 0).
