DEF INPUT PARAMETER wi-flag         AS LOGICAL NO-UNDO.
DEF INPUT PARAMETER gastno          AS INTEGER NO-UNDO.
DEF INPUT-OUTPUT PARAMETER resNo    AS INTEGER NO-UNDO.

DEFINE VARIABLE segm-ok AS LOGICAL INITIAL YES. 

IF wi-flag THEN
DO:
  RUN check-walkin-segm.
  IF NOT segm-ok THEN RETURN.
END.

FIND FIRST guest WHERE guest.gastnr = gastno NO-LOCK.

IF resNo = 0 THEN 
DO:    
  RUN get-NewResNo(OUTPUT resNo).
  CREATE reservation. 
  ASSIGN 
    reservation.resnr = resNo
    reservation.name  = guest.name
  . 
  FIND CURRENT reservation NO-LOCK. 
  RELEASE reservation. 
END.

PROCEDURE check-walkin-segm: 
DEFINE VARIABLE wi-segm           AS LOGICAL INITIAL NO. 
DEFINE VARIABLE main-exist        AS LOGICAL. 
DEFINE VARIABLE segmstr           AS CHAR. 
DEFINE VARIABLE curr-segm         AS INTEGER INITIAL 0. 
  
  FIND FIRST htparam WHERE paramnr = 48 NO-LOCK. 
  IF htparam.finteger NE 0 THEN 
  DO: 
    FIND FIRST segment WHERE segment.segmentcode = htparam.finteger 
      NO-LOCK NO-ERROR. 
    wi-segm = AVAILABLE segment. 
  END. 
  
  IF NOT wi-segm THEN 
  DO: 
    segm-ok = NO. 
    RETURN. 
  END. 
  
  curr-segm = segment.segmentcode. 
  FIND FIRST guest WHERE guest.gastnr = gastno NO-LOCK. 
  FIND FIRST guestseg WHERE guestseg.gastnr = guest.gastnr 
    AND guestseg.segmentcode = curr-segm NO-LOCK NO-ERROR. 
  IF NOT AVAILABLE guestseg THEN 
  DO: 
    FIND FIRST guestseg WHERE guestseg.gastnr = guest.gastnr 
      AND guestseg.reihenfolge = 1 NO-LOCK NO-ERROR. 
    main-exist = AVAILABLE guestseg. 
    create guestseg. 
    guestseg.gastnr = guest.gastnr. 
    guestseg.segmentcode = curr-segm. 
    IF NOT main-exist THEN guestseg.reihenfolge = 1. 
  END. 
END. 

PROCEDURE get-NewResNo:
DEF OUTPUT PARAMETER resNo AS INTEGER.
  FIND FIRST htparam WHERE htparam.paramnr = 736 NO-LOCK.
  IF htparam.fchar NE "" THEN RUN VALUE(htparam.fchar) (OUTPUT resNo).
  ELSE
  DO:
    FIND FIRST reservation NO-LOCK NO-ERROR. 
    IF NOT AVAILABLE reservation THEN resNo = 1. 
    ELSE resNo = reservation.resnr + 1. 
  END.
  FOR EACH res-line NO-LOCK BY res-line.resnr DESCENDING:
    IF resNo LE res-line.resnr THEN resNo = res-line.resnr + 1.
    LEAVE.
  END.
END.
