
DEF INPUT  PARAMETER pvILanguage AS INTEGER         NO-UNDO.
DEF INPUT  PARAMETER gastNo      AS INTEGER         NO-UNDO.
DEF OUTPUT PARAMETER msg-str     AS CHAR INITIAL "" NO-UNDO.

RUN get-vipnr.
RUN check-black-VIP-list.

DEFINE VARIABLE vipnr1              AS INTEGER INITIAL 999999999 NO-UNDO. 
DEFINE VARIABLE vipnr2              AS INTEGER INITIAL 999999999 NO-UNDO. 
DEFINE VARIABLE vipnr3              AS INTEGER INITIAL 999999999 NO-UNDO. 
DEFINE VARIABLE vipnr4              AS INTEGER INITIAL 999999999 NO-UNDO. 
DEFINE VARIABLE vipnr5              AS INTEGER INITIAL 999999999 NO-UNDO. 
DEFINE VARIABLE vipnr6              AS INTEGER INITIAL 999999999 NO-UNDO. 
DEFINE VARIABLE vipnr7              AS INTEGER INITIAL 999999999 NO-UNDO. 
DEFINE VARIABLE vipnr8              AS INTEGER INITIAL 999999999 NO-UNDO. 
DEFINE VARIABLE vipnr9              AS INTEGER INITIAL 999999999 NO-UNDO. 

{supertransBL.i} 
DEF VAR lvCAREA AS CHAR INITIAL "black-vip-list". 

PROCEDURE get-vipnr: 
  FIND FIRST htparam WHERE paramnr = 700 NO-LOCK. 
  IF finteger NE 0 THEN vipnr1 = htparam.finteger.               /* Rulita 211024 | Fixing for serverless */  
  FIND FIRST htparam WHERE paramnr = 701 NO-LOCK. 
  IF finteger NE 0 THEN vipnr2 = htparam.finteger.               /* Rulita 211024 | Fixing for serverless */  
  FIND FIRST htparam WHERE paramnr = 702 NO-LOCK. 
  IF finteger NE 0 THEN vipnr3 = htparam.finteger.               /* Rulita 211024 | Fixing for serverless */  
  FIND FIRST htparam WHERE paramnr = 703 NO-LOCK. 
  IF finteger NE 0 THEN vipnr4 = htparam.finteger.               /* Rulita 211024 | Fixing for serverless */  
  FIND FIRST htparam WHERE paramnr = 704 NO-LOCK. 
  IF finteger NE 0 THEN vipnr5 = htparam.finteger.               /* Rulita 211024 | Fixing for serverless */  
  FIND FIRST htparam WHERE paramnr = 705 NO-LOCK. 
  IF finteger NE 0 THEN vipnr6 = htparam.finteger.               /* Rulita 211024 | Fixing for serverless */  
  FIND FIRST htparam WHERE paramnr = 706 NO-LOCK. 
  IF finteger NE 0 THEN vipnr7 = htparam.finteger.               /* Rulita 211024 | Fixing for serverless */  
  FIND FIRST htparam WHERE paramnr = 707 NO-LOCK. 
  IF finteger NE 0 THEN vipnr8 = htparam.finteger.               /* Rulita 211024 | Fixing for serverless */  
  FIND FIRST htparam WHERE paramnr = 708 NO-LOCK. 
  IF finteger NE 0 THEN vipnr9 = htparam.finteger.               /* Rulita 211024 | Fixing for serverless */  
END. 

PROCEDURE check-black-VIP-list:
DEF VARIABLE integerFlag AS INTEGER NO-UNDO.
  RUN htpint.p (709, OUTPUT integerFlag).
  IF integerFlag NE 0 THEN 
  DO: 
    FIND FIRST guestseg WHERE guestseg.gastnr = gastNo 
      AND guestseg.segmentcode = integerFlag NO-LOCK NO-ERROR. 
    IF AVAILABLE guestseg THEN 
    DO: 
      FIND FIRST segment WHERE segment.segmentcode = integerFlag NO-LOCK. 
      msg-str = "&W" + translateExtended( "ATTENTION: ", lvCAREA, "":U) + CHR(10)
        + translateExtended ("SegmentCode:", lvCAREA, "":U) + " "
        + segment.bezeich + CHR(2).
    END. 
  END. 
  FIND FIRST guestseg WHERE guestseg.gastnr = gastNo 
    AND (guestseg.segmentcode = vipnr1 OR 
    guestseg.segmentcode = vipnr2 OR 
    guestseg.segmentcode = vipnr3 OR 
    guestseg.segmentcode = vipnr4 OR 
    guestseg.segmentcode = vipnr5 OR 
    guestseg.segmentcode = vipnr6 OR 
    guestseg.segmentcode = vipnr7 OR 
    guestseg.segmentcode = vipnr8 OR 
    guestseg.segmentcode = vipnr9) NO-LOCK NO-ERROR. 
  IF AVAILABLE guestseg THEN 
  DO: 
    FIND FIRST segment WHERE segment.segmentcode = guestseg.segmentcode NO-LOCK. 
    msg-str = msg-str + translateExtended( "VIP Guest: ", lvCAREA, "":U) + CHR(10)
      + translateExtended ("SegmentCode:", lvCAREA, "":U) + " " 
      + segment.bezeich.
  END. 
END. 
