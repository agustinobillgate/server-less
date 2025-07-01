DEFINE INPUT PARAMETER bqt-resnr    AS INTEGER.
DEFINE INPUT PARAMETER bqt-reslinnr AS INTEGER.
DEFINE INPUT PARAMETER user-init    AS CHAR.
DEFINE OUTPUT PARAMETER msg-str     AS CHAR.

DEFINE VARIABLE cancel-str AS CHARACTER.

FIND FIRST bk-veran WHERE bk-veran.veran-nr = bqt-resnr USE-INDEX vernr-ix NO-LOCK. /* Malik Serverless 592 add NO-LOCK NO-ERROR and IF AVAILABLE */
IF AVAILABLE bk-veran THEN
DO:
  IF (bk-veran.deposit-payment[1] + bk-veran.deposit-payment[2] 
    + bk-veran.deposit-payment[3] + bk-veran.deposit-payment[4] 
    + bk-veran.deposit-payment[5] + bk-veran.deposit-payment[6] 
    + bk-veran.deposit-payment[7] + bk-veran.deposit-payment[8] 
    + bk-veran.deposit-payment[9]) GT 0 THEN 
  DO: 
      FIND FIRST bk-reser WHERE bk-reser.veran-nr = bk-veran.veran-nr AND bk-reser.veran-resnr NE bqt-reslinnr
      AND bk-reser.resstatus = 1 NO-LOCK NO-ERROR. 
      IF NOT AVAILABLE bk-reser THEN 
      DO: 
          HIDE MESSAGE NO-PAUSE. 
          msg-str = "Deposit exists, cancel reservation not possible.". 
          RETURN. 
      END. 
  END. 
  IF bk-veran.rechnr > 0 THEN 
  DO: 
      FIND FIRST bk-reser WHERE bk-reser.veran-nr = bk-veran.veran-nr AND bk-reser.veran-resnr NE bqt-reslinnr
      AND bk-reser.resstatus = 1 NO-LOCK NO-ERROR. 
      IF NOT AVAILABLE bk-reser THEN 
      DO: 
          msg-str = "Bill exists, cancel reservation not possible.". 
          RETURN. 
      END. 
  END. 

  FIND FIRST bk-reser WHERE bk-reser.veran-nr = bqt-resnr AND bk-reser.veran-seite = bqt-reslinnr NO-LOCK. 
  FIND FIRST guest WHERE guest.gastnr = bk-veran.gastnr NO-LOCK. 
  FIND FIRST bk-raum WHERE bk-raum.raum = bk-reser.raum NO-LOCK. 
  /*
  MESSAGE translateExtended ("Do you really want to delete reservation of",lvCAREA,"") 
    SKIP 
    guest.name + " - " + translateExtended ("Room:",lvCAREA,"") + " " + bk-raum.bezeich SKIP 
    translateExtended ("Date:",lvCAREA,"") + " " + STRING(bk-reser.datum) + " - " + STRING(bk-reser.bis-datum) 
    + "  " + translateExtended ("Time:",lvCAREA,"") + " " + STRING(bk-reser.von-zeit,"99:99") 
    + " - " + STRING(bk-reser.bis-zeit,"99:99") + "?" 
    VIEW-AS ALERT-BOX QUESTION BUTTONS YES-NO UPDATE answer. 
  IF answer THEN 
  DO: 
      
  cancel-str = "". 
  RUN cancel-res.p(OUTPUT cancel-str). 
  IF cancel-str EQ "" THEN RETURN. */
  FIND FIRST b-storno WHERE b-storno.bankettnr = bk-reser.veran-nr AND b-storno.breslinnr = bk-reser.veran-resnr EXCLUSIVE-LOCK NO-ERROR. 
  IF NOT AVAILABLE b-storno THEN CREATE b-storno. 
  ASSIGN 
    b-storno.bankettnr = bk-reser.veran-nr 
    b-storno.breslinnr = bk-reser.veran-resnr 
    b-storno.gastnr = bk-veran.gastnr 
    b-storno.betrieb-gast = bk-veran.gastnrver 
    b-storno.datum = bk-reser.datum 
    b-storno.grund[18] = cancel-str + " D*" 
      + STRING(TODAY,"99/99/99") + " " + STRING(TIME,"hh:mm:ss") 
      + " " + bk-reser.raum. 
    b-storno.usercode = user-init 
  . 
  RUN ba-cancreslinebl.p(bk-reser.veran-nr, bk-reser.veran-resnr). 
END.

/* Malik Serverless 592 Comment 
IF (bk-veran.deposit-payment[1] + bk-veran.deposit-payment[2] 
   + bk-veran.deposit-payment[3] + bk-veran.deposit-payment[4] 
   + bk-veran.deposit-payment[5] + bk-veran.deposit-payment[6] 
   + bk-veran.deposit-payment[7] + bk-veran.deposit-payment[8] 
   + bk-veran.deposit-payment[9]) GT 0 THEN 
DO: 
    FIND FIRST bk-reser WHERE bk-reser.veran-nr = bk-veran.veran-nr AND bk-reser.veran-resnr NE bqt-reslinnr
    AND bk-reser.resstatus = 1 NO-LOCK NO-ERROR. 
    IF NOT AVAILABLE bk-reser THEN 
    DO: 
        HIDE MESSAGE NO-PAUSE. 
        msg-str = "Deposit exists, cancel reservation not possible.". 
        RETURN. 
    END. 
END. 
IF bk-veran.rechnr > 0 THEN 
DO: 
    FIND FIRST bk-reser WHERE bk-reser.veran-nr = bk-veran.veran-nr AND bk-reser.veran-resnr NE bqt-reslinnr
    AND bk-reser.resstatus = 1 NO-LOCK NO-ERROR. 
    IF NOT AVAILABLE bk-reser THEN 
    DO: 
        msg-str = "Bill exists, cancel reservation not possible.". 
        RETURN. 
    END. 
END. 

FIND FIRST bk-reser WHERE bk-reser.veran-nr = bqt-resnr AND bk-reser.veran-seite = bqt-reslinnr NO-LOCK. 
FIND FIRST guest WHERE guest.gastnr = bk-veran.gastnr NO-LOCK. 
FIND FIRST bk-raum WHERE bk-raum.raum = bk-reser.raum NO-LOCK. 
/*
MESSAGE translateExtended ("Do you really want to delete reservation of",lvCAREA,"") 
  SKIP 
  guest.name + " - " + translateExtended ("Room:",lvCAREA,"") + " " + bk-raum.bezeich SKIP 
  translateExtended ("Date:",lvCAREA,"") + " " + STRING(bk-reser.datum) + " - " + STRING(bk-reser.bis-datum) 
  + "  " + translateExtended ("Time:",lvCAREA,"") + " " + STRING(bk-reser.von-zeit,"99:99") 
  + " - " + STRING(bk-reser.bis-zeit,"99:99") + "?" 
  VIEW-AS ALERT-BOX QUESTION BUTTONS YES-NO UPDATE answer. 
IF answer THEN 
DO: 
    
cancel-str = "". 
RUN cancel-res.p(OUTPUT cancel-str). 
IF cancel-str EQ "" THEN RETURN. */
FIND FIRST b-storno WHERE b-storno.bankettnr = bk-reser.veran-nr AND b-storno.breslinnr = bk-reser.veran-resnr EXCLUSIVE-LOCK NO-ERROR. 
IF NOT AVAILABLE b-storno THEN CREATE b-storno. 
ASSIGN 
  b-storno.bankettnr = bk-reser.veran-nr 
  b-storno.breslinnr = bk-reser.veran-resnr 
  b-storno.gastnr = bk-veran.gastnr 
  b-storno.betrieb-gast = bk-veran.gastnrver 
  b-storno.datum = bk-reser.datum 
  b-storno.grund[18] = cancel-str + " D*" 
    + STRING(TODAY,"99/99/99") + " " + STRING(TIME,"hh:mm:ss") 
    + " " + bk-reser.raum. 
  b-storno.usercode = user-init 
. 
RUN ba-cancreslinebl.p(bk-reser.veran-nr, bk-reser.veran-resnr). */
