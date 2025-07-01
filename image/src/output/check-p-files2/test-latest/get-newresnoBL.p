DEF OUTPUT PARAMETER resNo  AS INTEGER  NO-UNDO.
DEF VAR progName            AS CHAR     NO-UNDO.

RUN htpchar.p (736, OUTPUT progName).
IF progName NE "" THEN RUN VALUE(progName) (OUTPUT resNo).
ELSE
DO: /* search the biggest resNo within reservation */
  FIND FIRST reservation NO-LOCK NO-ERROR. 
  IF NOT AVAILABLE reservation THEN resNo = 1. 
  ELSE resNo = reservation.resnr + 1. 
END.
    
/* search the biggest resNo within res-line */
FOR EACH res-line NO-LOCK BY res-line.resnr DESCENDING:
  IF resNo LE res-line.resnr THEN resNo = res-line.resnr + 1.
  LEAVE.
END.
