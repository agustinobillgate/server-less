DEFINE TEMP-TABLE s-list 
  FIELD resnr    LIKE res-line.resnr
  FIELD zinr     LIKE res-line.zinr
  FIELD name     LIKE res-line.name
  FIELD ankunft  LIKE res-line.ankunft
  FIELD abreise  LIKE res-line.abreise
  FIELD reslinnr AS INTEGER 
  FIELD assigned AS LOGICAL LABEL "Assign" 
  FIELD ass      AS LOGICAL. 

DEFINE TEMP-TABLE buf-s-list LIKE s-list.

DEFINE INPUT PARAMETER resnr     AS INTEGER. 
DEFINE OUTPUT PARAMETER TABLE FOR s-list.


RUN create-list.

FOR EACH buf-s-list,
  FIRST res-line WHERE res-line.resnr = buf-s-list.resnr 
  AND res-line.reslinnr = buf-s-list.reslinnr NO-LOCK
  BY res-line.resnr BY res-line.zinr BY res-line.name:
    CREATE s-list.
    ASSIGN
        s-list.resnr    = res-line.resnr
        s-list.zinr     = res-line.zinr
        s-list.name     = res-line.name
        s-list.ankunft  = res-line.ankunft
        s-list.abreise  = res-line.abreise
        s-list.reslinnr = buf-s-list.reslinnr
        s-list.assigned = buf-s-list.assigned
        s-list.ass      = buf-s-list.ass.
    . 
END.

 
PROCEDURE create-list: 
  FOR EACH res-line WHERE res-line.resnr = resnr 
    AND res-line.resstatus NE 12 AND res-line.active-flag LE 1 
    AND (res-line.l-zuordnung[5] = 0 OR res-line.l-zuordnung[5] = resnr) NO-LOCK: 
    CREATE buf-s-list. 
    ASSIGN
      buf-s-list.resnr    = res-line.resnr
      buf-s-list.reslinnr = res-line.reslinnr
      buf-s-list.assigned = NOT LOGICAL(res-line.l-zuordnung[2]) 
      buf-s-list.ass      = buf-s-list.assigned
    . 
  END. 
  FOR EACH res-line WHERE res-line.l-zuordnung[5] = resnr 
    AND res-line.resstatus NE 12 AND res-line.active-flag LE 1 
    AND res-line.resnr NE resnr NO-LOCK: 
    CREATE buf-s-list. 
    ASSIGN
      buf-s-list.resnr    = res-line.resnr
      buf-s-list.reslinnr = res-line.reslinnr
      buf-s-list.assigned = NOT LOGICAL(res-line.l-zuordnung[2]) 
      buf-s-list.ass      = buf-s-list.assigned
    . 
  END. 
END.
