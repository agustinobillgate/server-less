DEFINE INPUT-OUTPUT PARAMETER curr-tisch    AS INT.
DEFINE INPUT-OUTPUT PARAMETER mc-pos1       AS INT.
DEFINE INPUT-OUTPUT PARAMETER mc-pos2       AS INT.
DEFINE INPUT-OUTPUT PARAMETER curr-room     AS CHAR.
DEFINE INPUT-OUTPUT PARAMETER room          AS CHAR.
DEFINE INPUT-OUTPUT PARAMETER pax           AS INT.
DEFINE INPUT-OUTPUT PARAMETER gname         AS CHAR.

DEFINE INPUT PARAMETER pvILanguage      AS INTEGER NO-UNDO.
DEFINE INPUT PARAMETER tischnr          AS INT.
DEFINE INPUT PARAMETER dept             AS INT.
DEFINE INPUT PARAMETER curr-waiter      AS INT.
DEFINE INPUT PARAMETER curr-cursor      AS CHAR.

DEFINE INPUT  PARAMETER resrecid        AS INT.
DEFINE INPUT  PARAMETER hostnr          AS INT.

DEFINE OUTPUT PARAMETER klimit          AS DECIMAL.
DEFINE OUTPUT PARAMETER ksaldo          LIKE vhp.bill.saldo.
DEFINE OUTPUT PARAMETER remark          AS CHAR.

DEFINE OUTPUT PARAMETER table-ok        AS LOGICAL INITIAL YES. 
DEFINE OUTPUT PARAMETER person          AS INTEGER. 
DEFINE OUTPUT PARAMETER rmno            AS CHAR. 
DEFINE OUTPUT PARAMETER bname           AS CHAR. 

DEFINE OUTPUT PARAMETER resnr1          AS INT.
DEFINE OUTPUT PARAMETER reslinnr1       AS INT.
DEFINE OUTPUT PARAMETER hoga-resnr      AS INT.
DEFINE OUTPUT PARAMETER hoga-reslinnr   AS INT.
DEFINE OUTPUT PARAMETER msg-str         AS CHAR.

DEFINE OUTPUT PARAMETER curr-gname      AS CHAR.
DEFINE OUTPUT PARAMETER err-code        AS INT INIT 0.
DEFINE OUTPUT PARAMETER msg-str2        AS CHAR.

DEFINE VARIABLE check-flag AS LOGICAL INIT NO.

DEFINE BUFFER buff-hbill FOR h-bill.

{supertransBL.i} 
DEF VAR lvCAREA AS CHAR INITIAL "TS-table".
FIND FIRST vhp.kellner WHERE kellner.kellner-nr = curr-waiter 
    AND kellner.departement = dept NO-LOCK . 
FIND FIRST vhp.tisch WHERE vhp.tisch.tischnr = tischnr 
    AND vhp.tisch.departement = dept NO-LOCK NO-ERROR. 

check-flag = NO.
RUN check-table.

IF NOT table-ok THEN 
DO: 
    tischnr = 0. 
    pax = 0. 
    room = "". 
    gname = "". 
    /*MTDISP tischnr pax room gname WITH FRAME frame1. 
    APPLY "entry" TO tischnr.*/
    err-code = 1.
    RETURN NO-APPLY. 
END. 

/*FDL - Helpdesk Ticket 0D2316 - Comment curr-cursor = "tischnr"*/
IF table-ok /*AND curr-cursor = "tischnr"*/ THEN 
DO: 
    IF curr-cursor = "tischnr" OR curr-cursor = "pax" THEN
    DO:
        pax = person. 
        room = rmno. 
        gname = bname. 
    END.
END. 

IF table-ok AND curr-cursor = "pax" AND person NE 0 THEN /*FT 111115*/
    pax = person.  

IF curr-room NE room THEN 
DO: 
    RUN return-room. 
END. 
 
FIND FIRST vhp.h-bill WHERE vhp.h-bill.tischnr = tischnr 
    AND vhp.h-bill.departement = dept AND vhp.h-bill.flag = 0 NO-LOCK NO-ERROR. 
IF AVAILABLE vhp.h-bill THEN 
DO TRANSACTION : 
    FIND CURRENT vhp.h-bill EXCLUSIVE-LOCK. 
    ASSIGN
        vhp.h-bill.service[2] = hostnr
        vhp.h-bill.belegung = pax
        vhp.h-bill.bilname = gname. 
    IF check-flag THEN
        ASSIGN
            vhp.h-bill.resnr = resnr1 
            vhp.h-bill.reslinnr = reslinnr1. 
    FIND CURRENT vhp.h-bill NO-LOCK. 
END. 


PROCEDURE check-table: 
DEFINE VARIABLE billno AS INTEGER. 
DEFINE buffer h-bill1 FOR vhp.h-bill. 
  /*IF curr-tisch = tischnr THEN RETURN.*/
  check-flag = YES.
  FIND FIRST vhp.h-bill1 WHERE vhp.h-bill1.tischnr = tischnr AND 
    vhp.h-bill1.departement = dept AND vhp.h-bill1.flag = 0 NO-LOCK NO-ERROR. 
  IF NOT vhp.kellner.masterkey THEN 
  DO: 
    IF AVAILABLE vhp.h-bill1 AND vhp.h-bill1.kellner-nr NE curr-waiter 
      THEN table-ok = NO. 
    ELSE IF vhp.tisch.kellner-nr NE 0 AND vhp.tisch.kellner-nr NE curr-waiter 
      THEN table-ok = NO. 
    IF NOT table-ok THEN 
    DO:
      msg-str = msg-str + CHR(2)
              + translateExtended ("This table belongs to other waiter.",lvCAREA,"").
      err-code = 2.
      RETURN. 
    END. 
  END. 
  IF AVAILABLE vhp.h-bill1 THEN 
  DO: 
    person = vhp.h-bill1.belegung. 
    bname = vhp.h-bill1.bilname. 

      FIND FIRST vhp.res-line WHERE vhp.res-line.resnr = vhp.h-bill1.resnr 
        AND vhp.res-line.reslinnr = vhp.h-bill1.reslinnr NO-LOCK NO-ERROR. 
      IF AVAILABLE vhp.res-line THEN 
      DO: 
        RUN ts-table-check-creditlimitbl.p
            (RECID(res-line), OUTPUT klimit, OUTPUT ksaldo, OUTPUT remark).
        IF vhp.res-line.code NE "" THEN   
        DO:   
          FIND FIRST vhp.queasy WHERE vhp.queasy.key = 9   
            AND vhp.queasy.number1 = INTEGER(res-line.code) NO-LOCK NO-ERROR.   
          IF AVAILABLE vhp.queasy AND vhp.queasy.logi1 THEN   
          DO:   
            msg-str2 = msg-str2 + CHR(2) + "&W"  
                    + translateExtended ("CASH BASIS Billing Instruction: ",lvCAREA,"") + vhp.queasy.char1.  
          END.   
        END.
        ASSIGN
          rmno = vhp.res-line.zinr
          resnr1 = vhp.h-bill1.resnr
          reslinnr1 = vhp.h-bill1.reslinnr
          hoga-resnr = vhp.h-bill1.resnr /*FT*/
          hoga-reslinnr = vhp.h-bill1.resnr. 
      END. 
      bname = vhp.h-bill1.bilname. 
  END. 
  ELSE 
  DO: 
    person = vhp.tisch.normalbeleg. 
    rmno = "". 
    gname = "". 
    hoga-resnr = 0. 
    hoga-reslinnr = 0. 
  END. 
  curr-tisch = tischnr. 
END.



PROCEDURE return-room: 
DEFINE buffer resline FOR vhp.res-line. 
  FIND FIRST vhp.htparam WHERE vhp.htparam.paramnr = 253 NO-LOCK. 
  IF tischnr = 0 /* OR vhp.htparam.flogical */ THEN 
  DO: 
    room = "". 
    err-code = 3.
    RETURN NO-APPLY. 
  END. 
  ELSE 
  DO: 
    FIND FIRST vhp.h-bill WHERE vhp.h-bill.tischnr = tischnr 
      AND vhp.h-bill.departement = dept NO-LOCK NO-ERROR. 
    curr-gname = gname. 
    
    IF room = "" THEN 
    DO: 
      resnr1 = 0. 
      reslinnr1 = 0. 
      hostnr = 0. 
      err-code = 4.
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
          /*AND vhp.res-line.resstatus NE 12*/ /*FDL Comment*/
          AND vhp.res-line.resstatus EQ 6 /*FDL Dec 21, 2022 => Releate Ticket 40A11E - Just main guest*/
          NO-LOCK NO-ERROR. 
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
              (RECID(res-line), OUTPUT klimit, OUTPUT ksaldo, OUTPUT remark).
          IF vhp.res-line.code NE "" THEN   
          DO:   
            FIND FIRST vhp.queasy WHERE vhp.queasy.key = 9   
              AND vhp.queasy.number1 = INTEGER(res-line.code) NO-LOCK NO-ERROR.   
            IF AVAILABLE vhp.queasy AND vhp.queasy.logi1 THEN   
            DO:   
              msg-str2 = msg-str2 + CHR(2) + "&W"  
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
          err-code = 5.
          RETURN NO-APPLY. 
        END. 
      END. 
      FIND FIRST vhp.res-line WHERE vhp.res-line.active-flag = 1 
        AND vhp.res-line.zinr = room 
        /*AND vhp.res-line.resstatus NE 12 */ /*FDL Comment*/
        AND vhp.res-line.resstatus EQ 6 /*FDL Dec 21, 2022 => Releate Ticket 40A11E - Just main guest*/
        NO-LOCK NO-ERROR. 
      IF AVAILABLE vhp.res-line THEN 
      DO: 
        IF (room NE curr-room) THEN 
        DO: 
          resrecid = RECID(vhp.res-line). 
          FIND FIRST vhp.resline WHERE vhp.resline.active-flag = 1 
            AND vhp.resline.zinr = room 
            /*AND vhp.resline.resstatus NE 12*/ /*FDL Comment*/
            AND vhp.res-line.resstatus EQ 6 /*FDL Dec 21, 2022 => Releate Ticket 40A11E - Just main guest*/
            AND RECID(vhp.resline) NE resrecid NO-LOCK NO-ERROR. 
          IF NOT AVAILABLE resline THEN gname = vhp.res-line.name. 
          IF room = "" OR resrecid = 0 THEN 
          DO: 
            room = curr-room. 
            err-code = 6.
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
                msg-str2 = msg-str2 + CHR(2) + "&W"  
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
            err-code = 7.
            RETURN NO-APPLY. 
          END. 
        END. 
        ELSE 
        DO: 
          ASSIGN 
              resnr1        = vhp.res-line.resnr
              reslinnr1     = vhp.res-line.reslinnr
              hoga-resnr    = vhp.res-line.resnr
              hoga-reslinnr = vhp.res-line.reslinnr
              gname         = vhp.res-line.name. 
          err-code = 8.
          RETURN NO-APPLY. 
        END. 
      END. 
      ELSE 
      DO: 
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
        err-code = 9.
        RETURN NO-APPLY. 
      END. 
    END. 
  END. 
END. 

