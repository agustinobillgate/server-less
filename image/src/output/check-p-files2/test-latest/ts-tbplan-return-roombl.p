
DEF INPUT  PARAMETER pvILanguage    AS INTEGER NO-UNDO.
DEF INPUT-OUTPUT PARAMETER mc-pos1 AS INT.
DEF INPUT-OUTPUT PARAMETER mc-pos2 AS INT.
DEF INPUT-OUTPUT PARAMETER room    AS CHAR.
DEF INPUT-OUTPUT PARAMETER curr-room AS CHAR.

DEF OUTPUT PARAMETER resnr1 AS INT.
DEF OUTPUT PARAMETER reslinnr1 AS INT.
DEF OUTPUT PARAMETER gname AS CHAR.
DEF OUTPUT PARAMETER resrecid AS INT.
DEF OUTPUT PARAMETER fl-code AS INT INIT 0.
DEF OUTPUT PARAMETER remark AS CHAR.
DEF OUTPUT PARAMETER klimit AS DECIMAL.
DEF OUTPUT PARAMETER ksaldo AS DECIMAL.
DEF OUTPUT PARAMETER hoga-resnr AS INT.
DEF OUTPUT PARAMETER hoga-reslinnr AS INT.

DEF OUTPUT PARAMETER msg-str AS CHAR.

{supertransBL.i} 
DEF VAR lvCAREA AS CHAR INITIAL "TS-tbplan".

DEFINE buffer resline FOR vhp.res-line. 
IF length(room) GT 5 THEN 
DO: 
    IF mc-pos1 = 0 THEN mc-pos1 = 1. 
    IF mc-pos2 = 0 OR mc-pos2 LT mc-pos1 THEN 
      mc-pos2 = mc-pos1 + length(room) - 1. 
    mc-pos2 = mc-pos2 - mc-pos1 + 1. 
    room = SUBSTR(room, mc-pos1, mc-pos2).
    FIND FIRST vhp.res-line WHERE active-flag = 1 
      AND vhp.res-line.pin-code = room 
      AND vhp.res-line.resstatus NE 12 NO-LOCK NO-ERROR. 
    IF NOT AVAILABLE vhp.res-line THEN 
    DO: 
      FIND FIRST vhp.queasy WHERE vhp.queasy.key = 16 
        AND vhp.queasy.char1 = room NO-LOCK NO-ERROR. 
      IF AVAILABLE vhp.queasy THEN 
      FIND FIRST vhp.res-line WHERE vhp.res-line.active-flag = 1 
        AND vhp.res-line.resnr = vhp.queasy.number1 
        AND vhp.res-line.reslinnr = vhp.queasy.number2 NO-LOCK NO-ERROR. 
    END. 
    IF AVAILABLE vhp.res-line THEN 
    DO: 
      resrecid = RECID(vhp.res-line).
      RUN ts-table-check-creditlimitbl.p  
          (resrecid, OUTPUT klimit, OUTPUT ksaldo, OUTPUT remark).
      IF vhp.res-line.code NE "" THEN   
      DO:   
        FIND FIRST vhp.queasy WHERE vhp.queasy.key = 9   
          AND vhp.queasy.number1 = INTEGER(res-line.code) NO-LOCK NO-ERROR.   
        IF AVAILABLE vhp.queasy AND vhp.queasy.logi1 THEN   
        DO:   
          msg-str = msg-str + CHR(2) + "&W"  
                  + translateExtended ("CASH BASIS Billing Instruction: ",lvCAREA,"") + vhp.queasy.char1.  
        END.   
      END.
      resnr1 = vhp.res-line.resnr. 
      reslinnr1 = vhp.res-line.reslinnr. 
      
      hoga-resnr = vhp.res-line.resnr. 
      hoga-reslinnr = vhp.res-line.reslinnr. 
      
      room = vhp.res-line.zinr. 
      gname = vhp.res-line.name. 
      curr-room = room. 
      fl-code = 1.
      RETURN NO-APPLY. 
    END. 
END. 


/******************************/
  FIND FIRST vhp.res-line WHERE vhp.res-line.active-flag = 1 
    AND vhp.res-line.zinr = room AND vhp.res-line.resstatus NE 12 
    NO-LOCK NO-ERROR. 
  IF AVAILABLE vhp.res-line THEN 
  DO: 
    IF (room NE curr-room) THEN 
    DO:         
      resrecid = RECID(vhp.res-line). 
      FIND FIRST vhp.resline WHERE vhp.resline.active-flag = 1 
        AND vhp.resline.zinr = room AND vhp.resline.resstatus NE 12 
        AND RECID(vhp.resline) NE resrecid NO-LOCK NO-ERROR. 
      IF NOT AVAILABLE resline THEN gname = vhp.res-line.name. 
      ELSE
      DO:
          fl-code = 2.
          RETURN NO-APPLY.
      END.

      IF room = "" OR resrecid = 0 THEN .
      ELSE
      DO:
          FIND FIRST vhp.res-line WHERE RECID(res-line) = resrecid NO-LOCK.
          RUN ts-table-check-creditlimitbl.p  
              (resrecid, OUTPUT klimit, OUTPUT ksaldo, OUTPUT remark).
          IF vhp.res-line.code NE "" THEN   
          DO:   
            FIND FIRST vhp.queasy WHERE vhp.queasy.key = 9   
              AND vhp.queasy.number1 = INTEGER(res-line.code) NO-LOCK NO-ERROR.   
            IF AVAILABLE vhp.queasy AND vhp.queasy.logi1 THEN   
            DO:   
              msg-str = msg-str + CHR(2) + "&W"  
                      + translateExtended ("CASH BASIS Billing Instruction: ",lvCAREA,"") + vhp.queasy.char1.  
            END.   
          END.
          resnr1 = vhp.res-line.resnr. 
          reslinnr1 = vhp.res-line.reslinnr. 
          gname = vhp.res-line.name. 
          fl-code = 1.
      END.
    END. 
    ELSE 
    DO:
      fl-code = 3.
      RETURN NO-APPLY. 
    END. 
  END. 
  ELSE 
  DO: 
    fl-code = 4.
    RETURN NO-APPLY. 
  END. 




PROCEDURE check-creditlimit:
DEFINE VARIABLE answer AS LOGICAL INITIAL YES. 

    FIND FIRST vhp.htparam WHERE paramnr = 68 no-lock.  /* credit limit */ 
    FIND FIRST vhp.guest WHERE vhp.guest.gastnr 
      = vhp.res-line.gastnrpay NO-LOCK. 

    FIND FIRST vhp.mc-guest WHERE mc-guest.gastnr = vhp.guest.gastnr
        AND vhp.mc-guest.activeflag = YES NO-LOCK NO-ERROR.
    IF AVAILABLE vhp.mc-guest THEN
    ASSIGN remark = translateExtended ("Membership No:",lvCAREA,"") 
        + " " + vhp.mc-guest.cardnum + CHR(10).

    IF vhp.guest.kreditlimit NE 0 THEN klimit = vhp.guest.kreditlimit. 
    ELSE 
    DO: 
      IF vhp.htparam.fdecimal NE 0 THEN klimit = vhp.htparam.fdecimal. 
      ELSE klimit = vhp.htparam.finteger. 
    END.    

    ksaldo = 0. 
    FIND FIRST vhp.bill WHERE vhp.bill.resnr = vhp.res-line.resnr 
      AND vhp.bill.reslinnr = vhp.res-line.reslinnr AND vhp.bill.flag = 0 
      AND vhp.bill.zinr = vhp.res-line.zinr NO-LOCK NO-ERROR. 
    IF AVAILABLE vhp.bill THEN ksaldo = vhp.bill.saldo. 

    remark = remark + STRING(vhp.res-line.ankunft) + " - " 
      + STRING(vhp.res-line.abreise) + CHR(10) 
      + "A " + STRING(vhp.res-line.erwachs + vhp.res-line.gratis) 
      + "  Ch " + STRING(vhp.res-line.kind1) 
      + " - " + vhp.res-line.arrangement + CHR(10) 
      + vhp.res-line.bemerk. 
END. 
