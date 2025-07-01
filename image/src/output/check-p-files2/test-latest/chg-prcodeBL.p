DEFINE TEMP-TABLE q1-list 
  FIELD char1   LIKE queasy.char1
  FIELD char2   LIKE queasy.char2
  FIELD logi2   LIKE queasy.logi2
  FIELD number3 LIKE queasy.number2
  FIELD SELECTED AS LOGICAL INITIAL NO.

DEFINE TEMP-TABLE q2-list 
  FIELD char1   LIKE queasy.char1
  FIELD char2   LIKE queasy.char2
  FIELD logi2   LIKE queasy.logi2
  FIELD number3 LIKE queasy.number2
  FIELD SELECTED AS LOGICAL INITIAL NO.


DEFINE INPUT PARAMETER gastnr AS INTEGER NO-UNDO.
DEFINE OUTPUT PARAMETER TABLE FOR q1-list.
DEFINE OUTPUT PARAMETER TABLE FOR q2-list.
/*DEFINE VARIABLE gastnr   AS INTEGER INIT 1366. */


/************************* MAIN LOGIC ***************************/

RUN check-resline.
RUN create-list.

/************************ PROCEDURE ************************/
PROCEDURE check-resline:
DEF BUFFER rline FOR res-line.
  FIND FIRST guest-pr WHERE guest-pr.gastnr = gastnr NO-LOCK NO-ERROR.
  IF NOT AVAILABLE guest-pr THEN RETURN.
  FIND FIRST res-line WHERE res-line.gastnr = gastnr AND active-flag LE 1
      NO-LOCK NO-ERROR.
  IF NOT AVAILABLE res-line THEN RETURN.
  FIND FIRST res-line WHERE res-line.gastnr = gastnr 
    AND res-line.active-flag LE 1 NO-LOCK NO-ERROR.
  DO WHILE AVAILABLE res-line:
    IF NOT res-line.zimmer-wunsch MATCHES("*$CODE$*") THEN
    DO TRANSACTION:
      FIND FIRST rline WHERE RECID(rline) = RECID(res-line) EXCLUSIVE-LOCK.
      rline.zimmer-wunsch = rline.zimmer-wunsch 
        + "$CODE$" + guest-pr.CODE + ";".
      FIND CURRENT rline NO-LOCK.
      RELEASE rline.
    END.
    FIND NEXT res-line WHERE res-line.gastnr = gastnr 
      AND res-line.active-flag LE 1 NO-LOCK NO-ERROR.    
  END.
END.

PROCEDURE create-list:
  FOR EACH guest-pr WHERE guest-pr.gastnr = gastnr NO-LOCK:
    FIND FIRST queasy WHERE queasy.KEY = 2 AND queasy.char1 = guest-pr.CODE
        NO-LOCK NO-ERROR.
    IF AVAILABLE queasy THEN 
    DO:
        CREATE q2-list.
        BUFFER-COPY queasy TO q2-list.
    END.
  END.

  FOR EACH queasy WHERE queasy.KEY = 2 NO-LOCK:
    CREATE q1-list.
    BUFFER-COPY queasy TO q1-list.
    
    FIND FIRST q2-list WHERE q2-list.char1 = q1-list.char1 NO-ERROR.
    IF AVAILABLE q2-list THEN ASSIGN q1-list.SELECTED = YES.
  END.
END.
