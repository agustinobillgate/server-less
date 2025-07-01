
DEF INPUT  PARAMETER pvILanguage    AS INTEGER NO-UNDO.
DEF INPUT PARAMETER number1 AS INT.
DEF INPUT PARAMETER logi1   AS LOGICAL.
DEF OUTPUT PARAMETER success-flag AS LOGICAL INIT NO.
DEF OUTPUT PARAMETER msg-str AS CHAR.

{SupertransBL.i}
DEF VAR lvCAREA AS CHAR INITIAL "bill-instruct".

FIND FIRST res-line WHERE res-line.active-flag LE 1 
  AND INTEGER(res-line.code) EQ number1 NO-LOCK NO-ERROR. 
IF AVAILABLE res-line THEN 
DO: 
  msg-str = msg-str + CHR(2)
          + translateExtended ("Reservation exists for this code, deleting not possible.",lvCAREA,"").
  RETURN NO-APPLY. 
END. 
ELSE 
DO: 
    FIND FIRST queasy WHERE queasy.KEY = 9 
        AND queasy.number1 = number1 
        AND queasy.logi1 = logi1 EXCLUSIVE-LOCK.
    IF AVAILABLE queasy THEN
    DO:
        delete queasy.
        success-flag = YES.
    END.
    /*MTb1:delete-current-row(). 
    answer = NO. 
    RUN init-region-list. */
END.
