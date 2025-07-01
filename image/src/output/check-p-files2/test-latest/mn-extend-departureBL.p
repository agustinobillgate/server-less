
DEFINE OUTPUT PARAMETER i       AS INTEGER NO-UNDO INIT 0.

DEF VAR ci-date AS DATE.
FIND FIRST htparam WHERE paramnr = 87 NO-LOCK.   /* ci-date */ 
ci-date = htparam.fdate.

RUN extend-departure.


PROCEDURE extend-departure: 
DEFINE VARIABLE i AS INTEGER INITIAL 0. 
DEFINE BUFFER rline  FOR res-line.
DEFINE BUFFER rline1 FOR res-line.
DEFINE BUFFER rline2 FOR res-line.

  /*MTmess-str = translateExtended ("Extended departure",lvCAREA,"") + " " + STRING(i). 
  DISP mess-str WITH FRAME frame1. */
  
  FOR EACH res-line WHERE active-flag = 1 AND resstatus = 12 NO-LOCK:
    FIND FIRST rline1 WHERE rline1.resnr = res-line.resnr
      AND rline1.zinr = res-line.zinr
      AND (rline1.resstatus = 6 OR rline1.resstatus = 13) NO-LOCK
      NO-ERROR.
    IF NOT AVAILABLE rline1 THEN
    DO:
      FIND FIRST bill WHERE bill.resnr = res-line.resnr
          AND bill.reslinnr = res-line.reslinnr NO-LOCK NO-ERROR.
      IF NOT AVAILABLE bill
          OR (AVAILABLE bill AND bill.saldo = 0) THEN
      DO TRANSACTION:
        FIND FIRST rline2 WHERE RECID(rline2) = RECID(res-line)
          EXCLUSIVE-LOCK.
        ASSIGN rline2.active-flag = 2.
        FIND CURRENT rline2 NO-LOCK.
        IF AVAILABLE bill AND bill.flag = 0 THEN
        DO:
            FIND CURRENT bill EXCLUSIVE-LOCK.
            ASSIGN bill.flag = 1.
            FIND CURRENT bill NO-LOCK.
        END.
      END.
    END.
  END.

  FIND FIRST res-line WHERE res-line.active-flag = 1 
    AND res-line.abreise LT ci-date NO-LOCK NO-ERROR. 
  DO WHILE AVAILABLE res-line: 
    DO TRANSACTION: 
      i = i + 1. 
      /*MTmess-str = translateExtended ("Extended departure",lvCAREA,"") + " " + STRING(i). 
      DISP mess-str WITH FRAME frame1. */
      FIND CURRENT res-line EXCLUSIVE-LOCK. 
      res-line.abreise  = ci-date. 
      FIND CURRENT res-line NO-LOCK. 
    END. 
    FIND NEXT res-line WHERE res-line.active-flag = 1 
      AND res-line.abreise LT ci-date NO-LOCK NO-ERROR. 
  END.
/* update res-line.zimmerfix */
  FIND FIRST res-line WHERE res-line.active-flag = 1 
    AND res-line.resstatus = 13 NO-LOCK NO-ERROR. 
  DO WHILE AVAILABLE res-line: 
    FIND FIRST rline WHERE rline.resnr = res-line.resnr
      AND rline.reslinnr NE res-line.reslinnr
      AND rline.zinr = res-line.zinr
      AND (rline.active-flag = 1 OR rline.resstatus = 8)
      AND rline.zimmerfix = NO NO-LOCK NO-ERROR.
    IF AVAILABLE rline AND res-line.zimmerfix = NO THEN
    DO TRANSACTION: 
      FIND FIRST rline WHERE RECID(rline) = RECID(res-line) EXCLUSIVE-LOCK.
      ASSIGN rline.zimmerfix = YES.
      FIND CURRENT rline NO-LOCK.
    END.
    ELSE IF NOT AVAILABLE rline AND res-line.zimmerfix = YES THEN
    DO TRANSACTION: 
      FIND FIRST rline WHERE RECID(rline) = RECID(res-line) EXCLUSIVE-LOCK.
      ASSIGN rline.zimmerfix = NO.
      FIND CURRENT rline NO-LOCK.
    END.
    FIND NEXT res-line WHERE res-line.active-flag = 1 
      AND res-line.resstatus = 13 NO-LOCK NO-ERROR. 
  END. 
  
  FIND FIRST res-line WHERE res-line.active-flag = 1 
    AND res-line.resstatus = 6 AND res-line.zimmerfix = YES NO-LOCK NO-ERROR. 
  DO WHILE AVAILABLE res-line: 
    FIND FIRST rline WHERE rline.resnr = res-line.resnr
      AND rline.reslinnr NE res-line.reslinnr
      AND rline.zinr = res-line.zinr
      AND (rline.active-flag = 1 OR rline.resstatus = 8)
      AND rline.zimmerfix = NO NO-LOCK NO-ERROR.
    IF NOT AVAILABLE rline THEN
    DO TRANSACTION: 
      FIND FIRST rline WHERE RECID(rline) = RECID(res-line) EXCLUSIVE-LOCK.
      ASSIGN rline.zimmerfix = NO.
      FIND CURRENT rline NO-LOCK.
    END.
    FIND NEXT res-line WHERE res-line.active-flag = 1 
      AND res-line.resstatus = 6 AND res-line.zimmerfix = YES NO-LOCK NO-ERROR. 
  END.
END. 
