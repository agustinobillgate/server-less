DEF BUFFER ubuff FOR bediener.
DEF BUFFER bqueasy FOR queasy.

DEFINE TEMP-TABLE b1-list
    FIELD datum     LIKE res-history.datum
    FIELD action    LIKE res-history.action
    FIELD aenderung LIKE res-history.aenderung
    FIELD username  LIKE ubuff.username
    FIELD zeit      LIKE res-history.zeit.

/* */
DEF INPUT PARAMETER usrID     AS CHAR NO-UNDO.
DEF INPUT PARAMETER action    AS CHAR NO-UNDO.
DEF INPUT PARAMETER from-date AS DATE NO-UNDO.
DEF INPUT PARAMETER to-date   AS DATE NO-UNDO.
DEF INPUT PARAMETER idFlag    AS CHAR. /* Bily */
DEF OUTPUT PARAMETER TABLE FOR b1-list.

/* 
DEFINE VARIABLE usrID AS CHAR NO-UNDO.
DEFINE VARIABLE action AS CHAR NO-UNDO.
DEFINE VARIABLE from-date AS DATE NO-UNDO.
DEFINE VARIABLE to-date AS DATE NO-UNDO.
DEFINE VARIABLE idFlag AS CHAR.

usrID = ?.
action = ?.
from-date = 01/01/23.
to-date = 07/01/24.
idFlag = "".
*/

DEF VARIABLE counter AS INTEGER NO-UNDO INITIAL 0.

CREATE queasy.
ASSIGN queasy.KEY = 285
       queasy.char1 = "System Logfiles"
       queasy.number1 = 1
       queasy.char2 = idFlag.
RELEASE queasy.

RUN disp-it.

FIND FIRST b1-list NO-ERROR.
DO WHILE AVAILABLE b1-list:

    ASSIGN counter = counter + 1.

    CREATE queasy.
    ASSIGN queasy.KEY = 280
           queasy.char1 = "System Logfiles"
           queasy.char2 = idFlag
           queasy.char3 = STRING(b1-list.datum)          + "$" +
                          STRING(b1-list.action)         + "$" +
                          STRING(b1-list.aenderung)      + "$" +
                          STRING(b1-list.username)       + "$" +
                          STRING(b1-list.zeit, "HH:MM:SS").
            queasy.number1 = counter.
    FIND NEXT b1-list NO-ERROR.
END. 

FIND FIRST bqueasy WHERE bqueasy.KEY = 285
    AND bqueasy.char1 = "System Logfiles"
    AND bqueasy.char2 = idFlag NO-LOCK NO-ERROR.
IF AVAILABLE bqueasy THEN DO:
    FIND CURRENT bqueasy EXCLUSIVE-LOCK.
    ASSIGN bqueasy.number1 = 0.
    FIND CURRENT bqueasy NO-LOCK.
    RELEASE bqueasy.
END.

PROCEDURE disp-it:
  IF ((usrID NE ?) /*AND (usrID NE "")*/) AND (action = ?) THEN
  DO:
      FIND FIRST bediener WHERE bediener.userinit = TRIM(ENTRY(1, usrID, "-"))
          NO-LOCK.
      FOR EACH res-history WHERE res-history.datum GE from-date
          AND res-history.datum LE to-date 
          AND res-history.nr = bediener.nr NO-LOCK,
          FIRST ubuff WHERE ubuff.nr = res-history.nr NO-LOCK:
          /* BY res-history.datum BY res-history.action BY res-history.zeit: */
          RUN assign-it.
      END.
      RETURN.
  END.

  IF ((usrID = ?) /*AND (usrID = "")*/) AND (action NE ?) THEN
  DO:
      FOR EACH res-history WHERE res-history.datum GE from-date
          AND res-history.datum LE to-date 
          AND res-history.action = action NO-LOCK,
          FIRST ubuff WHERE ubuff.nr = res-history.nr NO-LOCK
          BY res-history.datum BY res-history.action BY res-history.zeit:
          RUN assign-it.
      END.
      RETURN.
  END.

  IF ((usrID NE ?) /*AND (usrID NE "")*/) AND (action NE ?) THEN
  DO:
      FIND FIRST bediener WHERE bediener.userinit = TRIM(ENTRY(1, usrID, "-"))
          NO-LOCK.
      FOR EACH res-history WHERE res-history.datum GE from-date
          AND res-history.datum LE to-date 
          AND res-history.nr = bediener.nr 
          AND res-history.action = action NO-LOCK,
          FIRST ubuff WHERE ubuff.nr = res-history.nr NO-LOCK
          BY res-history.datum BY res-history.action BY res-history.zeit:
          RUN assign-it.
      END.
      RETURN.
  END.

  FOR EACH res-history WHERE res-history.datum GE from-date
      AND res-history.datum LE to-date NO-LOCK
      BY res-history.datum BY res-history.action BY res-history.zeit:
      FIND FIRST ubuff WHERE ubuff.nr = res-history.nr NO-LOCK NO-ERROR.
      RUN assign-it.
  END.
END.

PROCEDURE assign-it:
    CREATE b1-list.
    ASSIGN
        b1-list.datum     = res-history.datum
        b1-list.action    = res-history.action
        b1-list.aenderung = res-history.aenderung
        b1-list.zeit      = res-history.zeit.
    IF AVAILABLE ubuff THEN b1-list.username  = ubuff.username.
END.




