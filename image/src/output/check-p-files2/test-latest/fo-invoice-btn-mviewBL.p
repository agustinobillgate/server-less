
DEF INPUT  PARAMETER bil-recid      AS INT.
DEF OUTPUT PARAMETER mbill-resnr    AS INT INIT 0.
DEF OUTPUT PARAMETER mbill-rechnr   AS INT INIT 0.
DEF OUTPUT PARAMETER avail-mbill    AS LOGICAL INIT NO.

FIND FIRST bill WHERE RECID(bill) = bil-recid NO-LOCK NO-ERROR. /* Malik Serverless : NO-LOCK -> NO-LOCK NO-ERROR  */

DEFINE BUFFER resline FOR res-line.
DEFINE BUFFER mbill FOR bill. 

/* Malik Serverless */
IF AVAILABLE bill THEN
DO:
  FIND FIRST resline WHERE resline.resnr = bill.resnr 
    AND resline.reslinnr = bill.reslinnr NO-LOCK.
  IF resline.l-zuordnung[5] NE 0 THEN
  DO:
      FIND FIRST mbill WHERE mbill.resnr = resline.l-zuordnung[5]
          AND mbill.reslinnr = 0 NO-LOCK NO-ERROR.
      IF AVAILABLE mbill THEN 
      DO:
          avail-mbill = YES.
          mbill-resnr = mbill.resnr.
          mbill-rechnr = mbill.rechnr.
      END.
          
  END.
  ELSE
  DO:
    FIND FIRST master WHERE master.resnr = bill.resnr NO-LOCK NO-ERROR. 
    IF AVAILABLE master THEN 
    DO: 
      FIND FIRST mbill WHERE mbill.resnr = master.resnr AND mbill.reslinnr = 0 
        NO-LOCK NO-ERROR. 
      IF AVAILABLE mbill THEN 
      DO:
          avail-mbill = YES.
          mbill-resnr = mbill.resnr.
          mbill-rechnr = mbill.rechnr.
      END.
          
    END.
  END.
END.
ELSE
DO:
  RETURN.
END.
/* END Malik */


