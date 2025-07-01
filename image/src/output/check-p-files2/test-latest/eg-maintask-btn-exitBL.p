
DEFINE TEMP-TABLE maintask LIKE queasy.

DEF INPUT PARAMETER TABLE FOR maintask.
DEF INPUT PARAMETER case-type AS INT.
DEF INPUT PARAMETER rec-id AS INT.
DEF OUTPUT PARAMETER fl-code AS INT INIT 0.

DEF BUFFER queasy1 FOR queasy.

FIND FIRST maintask.
IF case-type = 1 THEN
DO :
    CREATE queasy.  
    RUN fill-new-queasy.  
END.
ELSE IF case-type = 2 THEN
DO:
  FIND FIRST queasy WHERE RECID(queasy) = rec-id.
  FIND FIRST queasy1 WHERE queasy1.number1 = maintask.number1   
    and queasy1.deci2 = 0  
    and queasy1.key = 133 AND ROWID(queasy1) NE ROWID(queasy)
    NO-LOCK NO-ERROR.
  IF AVAILABLE queasy1 THEN
  DO:
      fl-code = 1.
      /*MTHIDE MESSAGE NO-PAUSE.  
      MESSAGE translateExtended ("Code number already exists, choose other one.",lvCAREA,"")  
          VIEW-AS ALERT-BOX INFORMATION. 
      maintask.number1 = s1.
      DISPLAY maintask.number1 WITH FRAME frame1.
      APPLY "entry" TO maintask.number1. */
  END.
  ELSE
  DO:
      FIND FIRST queasy1 WHERE queasy1.char1 = maintask.char1   
        and queasy1.deci2 = 0  
        and queasy1.key = 133 AND ROWID(queasy1) NE ROWID(queasy)
        NO-LOCK NO-ERROR.
      IF AVAILABLE queasy1 THEN
      DO:
          fl-code = 2.
          /*MTHIDE MESSAGE NO-PAUSE.  
          MESSAGE translateExtended ("Description already exists, choose other one.",lvCAREA,"")  
              VIEW-AS ALERT-BOX INFORMATION. 
          maintask.char1 = s2.
          DISPLAY maintask.char1 WITH FRAME frame1.
          APPLY "entry" TO maintask.char1.*/
      END.
      ELSE
      DO:
          FIND CURRENT queasy EXCLUSIVE-LOCK.  
          queasy.number1 = maintask.number1.
          queasy.number2 = maintask.number2.
          queasy.char1 = maintask.char1.  
          FIND CURRENT queasy NO-LOCK .
          fl-code = 3.
          /*MT
          RUN init-maintask.
          RUN mk-readonly(YES).
            
          ENABLE btn-addart btn-renart btn-delart btn-exit WITH FRAME frame1.  
          
          OPEN QUERY q1 FOR EACH queasy WHERE queasy.KEY = 133 NO-LOCK,
              FIRST tcategory WHERE tcategory.categ-nr = queasy.number2 NO-LOCK  BY queasy.number1.
          
          APPLY "entry" TO b1.
          curr-select = "".
          */
      END.
  END.
END.

PROCEDURE fill-new-queasy:  
  queasy.KEY = 133.  
  queasy.number1 = maintask.number1.  
  queasy.number2 = maintask.number2.
  queasy.char1 = maintask.char1.  
END.  

