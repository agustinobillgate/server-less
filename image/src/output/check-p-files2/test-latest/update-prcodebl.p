DEFINE TEMP-TABLE q2-list 
  FIELD char1   LIKE queasy.char1
  FIELD char2   LIKE queasy.char2
  FIELD logi2   LIKE queasy.logi2
  FIELD number3 LIKE queasy.number2
  FIELD SELECTED AS LOGICAL INITIAL NO.

DEF INPUT PARAMETER gastnr AS INTEGER NO-UNDO.
DEF INPUT PARAMETER TABLE FOR q2-list.

DEF VARIABLE new-contrate        AS LOGICAL INIT NO NO-UNDO. 
DEF BUFFER   g-pr                FOR guest-pr. 
DEF BUFFER qsy FOR queasy.

DEF VARIABLE new-flag AS LOGICAL INIT NO.

FIND FIRST htparam WHERE htparam.paramnr = 550 NO-LOCK.
IF htparam.feldtyp = 4 THEN new-contrate = htparam.flogical.

FOR EACH guest-pr WHERE guest-pr.gastnr = gastnr NO-LOCK:
    DISP guest-pr.
    MESSAGE guest-pr.CODE
        VIEW-AS ALERT-BOX INFO BUTTONS OK.

  FIND FIRST q2-list WHERE q2-list.char1 = guest-pr.CODE NO-LOCK NO-ERROR.
  IF NOT AVAILABLE q2-list THEN
  DO:
    FIND FIRST g-pr WHERE g-pr.code = guest-pr.CODE 
      AND g-pr.gastnr NE guest-pr.gastnr NO-LOCK NO-ERROR. 
    IF NOT AVAILABLE g-pr THEN 
    DO: 
      IF new-contrate THEN
      FOR EACH ratecode WHERE ratecode.code = guest-pr.CODE: 
        DELETE ratecode. 
      END.
      ELSE
      FOR EACH pricecod WHERE pricecod.code = guest-pr.CODE: 
        DELETE pricecod. 
      END. 
    END.


    FIND FIRST queasy WHERE queasy.KEY = 159 AND queasy.number2 = gastnr NO-LOCK NO-ERROR.
    IF AVAILABLE queasy THEN
    DO:
        FIND FIRST qsy WHERE qsy.KEY = 161 AND ENTRY(1,qsy.char1,";") = guest-pr.CODE
            NO-LOCK NO-ERROR.
        DO WHILE AVAILABLE qsy:
            FIND CURRENT qsy EXCLUSIVE-LOCK.
            DELETE qsy.
            RELEASE qsy.
            FIND NEXT qsy WHERE qsy.KEY = 161 AND ENTRY(1,qsy.char1,";") = guest-pr.CODE
                NO-LOCK NO-ERROR.
        END.

        FIND FIRST qsy WHERE qsy.KEY = 170 AND qsy.char1 = guest-pr.CODE
            NO-LOCK NO-ERROR.
        DO WHILE AVAILABLE qsy:
            FIND CURRENT qsy EXCLUSIVE-LOCK.
            DELETE qsy.
            RELEASE qsy.
            FIND NEXT qsy WHERE qsy.KEY = 170 AND qsy.char1 = guest-pr.CODE
                NO-LOCK NO-ERROR.
        END.

        FIND FIRST qsy WHERE qsy.KEY = 171 AND qsy.char1 = guest-pr.CODE
            NO-LOCK NO-ERROR.
        DO WHILE AVAILABLE qsy:
            FIND CURRENT qsy EXCLUSIVE-LOCK.
            DELETE qsy.
            RELEASE qsy.
            FIND NEXT qsy WHERE qsy.KEY = 171 AND qsy.char1 = guest-pr.CODE
                NO-LOCK NO-ERROR.
        END.
    END.                         

    FIND FIRST g-pr WHERE RECID(g-pr) = RECID(guest-pr) EXCLUSIVE-LOCK.
    DELETE g-pr.
    RELEASE g-pr.
  END.
END.
    
FOR EACH q2-list:
  FIND FIRST guest-pr WHERE guest-pr.gastnr = gastnr
    AND guest-pr.CODE = q2-list.char1 NO-LOCK NO-ERROR.
  IF NOT AVAILABLE guest-pr THEN
  DO:
    new-flag = YES.
    CREATE guest-pr.
    ASSIGN
      guest-pr.gastnr = gastnr
      guest-pr.CODE   = q2-list.char1
    .
  END.
END.


FIND FIRST queasy WHERE queasy.KEY = 159 AND queasy.number2 = gastnr NO-LOCK NO-ERROR.
IF AVAILABLE queasy AND new-flag THEN
    RUN update-bookengine-configbl.p (9,queasy.number1,YES,"").
