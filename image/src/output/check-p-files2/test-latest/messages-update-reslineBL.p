DEF INPUT PARAMETER resnr       AS INTEGER NO-UNDO.
DEF INPUT PARAMETER reslinnr    AS INTEGER NO-UNDO.

FIND FIRST res-line WHERE res-line.resnr = resnr
    AND res-line.reslinnr = reslinnr NO-LOCK.

RUN update-resline.

PROCEDURE update-resline: 
  FIND FIRST messages WHERE messages.resnr = resnr 
    AND messages.reslinnr = reslinnr 
    AND messages.betriebsnr = 0 NO-LOCK NO-ERROR. 
  IF AVAILABLE messages THEN 
  DO: 
    IF res-line.wabkurz = "" THEN 
    DO TRANSACTION: 
      FIND CURRENT res-line EXCLUSIVE-LOCK. 
      res-line.wabkurz = "M". 
      FIND CURRENT res-line NO-LOCK. 
  /** switch ON MESSAGE lamp ***/ 
     IF res-line.active-flag = 1 THEN 
       RUN intevent-1.p( 4, res-line.zinr, "Message Lamp on!", res-line.resnr, res-line.reslinnr). 
    END. 
  END. 
  ELSE 
  DO: 
    IF res-line.wabkurz = "M" THEN 
    DO TRANSACTION: 
      FIND CURRENT res-line EXCLUSIVE-LOCK. 
      res-line.wabkurz = "". 
      FIND CURRENT res-line NO-LOCK. 
  /** switch off MESSAGE lamp ***/ 
      IF res-line.active-flag = 1 THEN 
        RUN intevent-1.p( 5, res-line.zinr, "Message Lamp off!", res-line.resnr, res-line.reslinnr). 
    END. 
  END. 
END. 
