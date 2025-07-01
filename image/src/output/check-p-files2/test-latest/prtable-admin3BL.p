    
    
DEF INPUT PARAMETER nr AS INT.
DEF OUTPUT PARAMETER enable-it AS LOGICAL INITIAL YES NO-UNDO.

DEFINE buffer prtable1 FOR prtable.

FIND FIRST prtable1 WHERE prtable1.nr = nr AND prtable1.prcode NE "" 
    NO-LOCK NO-ERROR.
DO WHILE AVAILABLE prtable1 AND enable-it: 
  FIND FIRST guest-pr WHERE guest-pr.code = prtable1.prcode NO-LOCK NO-ERROR. 
  IF AVAILABLE guest-pr THEN 
  DO: 
    FIND FIRST res-line WHERE res-line.gastnr = guest-pr.gastnr 
      AND res-line.active-flag LE 1 
      AND res-line.reserve-int = prtable1.marknr NO-LOCK NO-ERROR. 
    DO WHILE AVAILABLE res-line AND enable-it: 
      FIND FIRST reslin-queasy WHERE reslin-queasy.key = "arrangement" 
        AND reslin-queasy.resnr = res-line.resnr 
        AND reslin-queasy.reslinnr = res-line.reslinnr NO-LOCK NO-ERROR. 
      IF NOT AVAILABLE reslin-queasy THEN enable-it = NO. 
      FIND NEXT res-line WHERE res-line.gastnr = guest-pr.gastnr 
        AND res-line.active-flag LE 1 
        AND res-line.reserve-int = prtable1.marknr NO-LOCK NO-ERROR. 
    END. 
  END. 
  FIND NEXT prtable1 WHERE prtable1.nr = nr AND prtable1.prcode NE ""
      NO-LOCK NO-ERROR. 
END.
