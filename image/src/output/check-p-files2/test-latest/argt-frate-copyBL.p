
DEF INPUT PARAMETER s-recid     AS INTEGER NO-UNDO.
DEF OUTPUT PARAMETER done       AS LOGICAL NO-UNDO INIT NO.

DEF BUFFER r-queasy FOR reslin-queasy.
DEF BUFFER rline FOR res-line.

  FIND FIRST reslin-queasy WHERE 
      INTEGER(RECID(reslin-queasy)) = s-recid NO-LOCK NO-ERROR.
  IF NOT AVAILABLE reslin-queasy THEN RETURN.

  DO TRANSACTION:
    FOR EACH rline WHERE rline.resnr = reslin-queasy.resnr
      AND rline.active-flag LE 1
      AND rline.resstatus NE 12
      AND rline.reslinnr NE reslin-queasy.reslinnr
      AND rline.zipreis GT 0 NO-LOCK:
      FIND FIRST r-queasy WHERE
        r-queasy.key        = "fargt-line"          AND
        r-queasy.number1    = reslin-queasy.number1 AND
        r-queasy.number2    = reslin-queasy.number2 AND
        r-queasy.number3    = reslin-queasy.number3 AND
        r-queasy.resnr      = rline.resnr           AND
        r-queasy.reslinnr   = rline.reslinnr        NO-ERROR.
      IF NOT AVAILABLE r-queasy THEN 
      DO:    
          CREATE r-queasy.
          ASSIGN r-queasy.reslinnr = rline.reslinnr.
      END.
      BUFFER-COPY reslin-queasy EXCEPT reslin-queasy.reslinnr 
          TO r-queasy.
      FIND CURRENT r-queasy NO-LOCK.
    END.
  END.
  ASSIGN done = YES.
