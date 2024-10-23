
DEF INPUT-OUTPUT PARAMETER room     AS CHAR.
DEF INPUT-OUTPUT PARAMETER mc-pos1  AS INT.
DEF INPUT-OUTPUT PARAMETER mc-pos2  AS INT.
DEF INPUT-OUTPUT PARAMETER gname    AS CHAR.

DEF INPUT PARAMETER tischnr         AS INT.
DEF INPUT PARAMETER dept            AS INT.
DEF INPUT PARAMETER pvILanguage     AS INTEGER NO-UNDO.  

DEF OUTPUT PARAMETER klimit         AS DECIMAL.
DEF OUTPUT PARAMETER ksaldo         LIKE vhp.bill.saldo.
DEF OUTPUT PARAMETER remark         AS CHAR.
DEF OUTPUT PARAMETER msg-flag       AS INT INIT 0.
DEF OUTPUT PARAMETER curr-gname     AS CHAR.
DEF OUTPUT PARAMETER resnr1         AS INT.
DEF OUTPUT PARAMETER reslinnr1      AS INT.
DEF OUTPUT PARAMETER hostnr         AS INT.
DEF OUTPUT PARAMETER hoga-resnr     AS INT.
DEF OUTPUT PARAMETER hoga-reslinnr  AS INT.
DEF OUTPUT PARAMETER curr-room      AS CHAR.
DEF OUTPUT PARAMETER resrecid       AS INT.
DEF OUTPUT PARAMETER msg-str        AS CHAR.

DEF OUTPUT PARAMETER err-code       AS INT INIT 0.

DEFINE buffer resline FOR vhp.res-line. 

{SupertransBL.i}   
DEF VAR lvCAREA AS CHAR INITIAL "TS-table".  

FIND FIRST vhp.h-bill WHERE vhp.h-bill.tischnr = tischnr
  AND vhp.h-bill.departement = dept NO-LOCK NO-ERROR. 
curr-gname = gname. 

IF room = "" THEN 
DO: 
  resnr1 = 0. 
  reslinnr1 = 0. 
  hostnr = 0.
  err-code = 1.
  RETURN NO-APPLY. 
END. 
ELSE 
DO: 
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
      curr-gname = gname.
      err-code = 2.
      RETURN NO-APPLY. 
    END. 
  END. 
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
      ELSE RUN TS-pguest.p(INPUT-OUTPUT room, 
        INPUT-OUTPUT gname, INPUT-OUTPUT resrecid). 
      IF room = "" OR resrecid = 0 THEN 
      DO: 
        room = curr-room. 
        err-code = 3.
        RETURN NO-APPLY. 
      END. 
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
        hoga-resnr = vhp.res-line.resnr. 
        hoga-reslinnr = vhp.res-line.reslinnr. 
        gname = vhp.res-line.name. 
        curr-room = room. 
        curr-gname = gname.
        err-code = 4.
        RETURN NO-APPLY. 
      END. 
    END. 
    ELSE 
    DO:
      err-code = 5.
      RETURN NO-APPLY. 
    END. 
  END. 
  ELSE 
  DO: 
    msg-flag = 1.
    room = "". 
    IF AVAILABLE vhp.h-bill AND vhp.h-bill.resnr GT 0 THEN 
    DO: 
      FIND FIRST vhp.res-line WHERE vhp.res-line.resnr = vhp.h-bill.resnr 
        AND vhp.res-line.reslinnr = vhp.h-bill.reslinnr NO-LOCK NO-ERROR. 
      IF AVAILABLE vhp.res-line THEN room = vhp.res-line.zinr. 
    END. 
    ELSE 
    DO: 
      FIND FIRST vhp.zimmer WHERE vhp.zimmer.zinr = curr-room 
        NO-LOCK NO-ERROR. 
      IF AVAILABLE vhp.zimmer THEN room = curr-room. 
    END.
    err-code = 6.
    RETURN NO-APPLY. 
  END. 
END.
