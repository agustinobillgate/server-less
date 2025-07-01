
DEF TEMP-TABLE t-queasy1 LIKE queasy
    FIELD rec-id AS INT.

DEF INPUT PARAMETER curr-mode AS CHAR.
DEF INPUT PARAMETER location AS INT.
DEF INPUT PARAMETER floor AS INT.
DEF INPUT PARAMETER from-room AS CHAR.
DEF OUTPUT PARAMETER TABLE FOR t-queasy1.

IF curr-mode = "add" THEN 
DO: 
  CREATE queasy. 
  ASSIGN 
    queasy.key = 25 
    queasy.number1 = location 
    queasy.number2 = floor 
    queasy.char1 = from-room. 
  FIND CURRENT queasy NO-LOCK.
  CREATE t-queasy1.
  BUFFER-COPY queasy TO t-queasy1.
  ASSIGN t-queasy1.rec-id = RECID(queasy).
  /*MTRUN save-room-location(curr-n). 
  RUN disable-room(curr-n). 
  RUN assign-color(curr-n, 14, 0). 
  ENABLE btn-add btn-move btn-rem WITH FRAME frame1. 
  DISABLE btn-go WITH FRAME frame1. 
  curr-mode = "". 
  APPLY "entry" TO location. */
END. 
 
ELSE IF curr-mode = "move" THEN 
DO: 
  FIND FIRST queasy WHERE queasy.key = 25 AND 
    queasy.number1 = location AND queasy.number2 = floor AND 
    queasy.char1 = from-room NO-LOCK.
  FIND CURRENT queasy NO-LOCK.
  CREATE t-queasy1.
  BUFFER-COPY queasy TO t-queasy1.
  ASSIGN t-queasy1.rec-id = RECID(queasy).
  /*MTRUN save-room-location(curr-i). 
  RUN disable-room(curr-i). 
  RUN assign-color(curr-i, 14, 0). 
  ENABLE btn-add btn-move btn-rem WITH FRAME frame1. 
  DISABLE btn-go WITH FRAME frame1. 
  curr-mode = "". 
  APPLY "entry" TO location. */
END. 
/*MTELSE 
DO: 
  APPLY "entry" TO location. 
END. */
