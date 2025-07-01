
DEF BUFFER ubuff FOR bediener.
DEFINE TEMP-TABLE b1-list
    FIELD datum     LIKE res-history.datum
    FIELD action    LIKE res-history.action
    FIELD aenderung LIKE res-history.aenderung
    FIELD username  LIKE ubuff.username
    FIELD zeit      LIKE res-history.zeit.

DEF INPUT PARAMETER usrID       AS CHAR NO-UNDO.
DEF INPUT PARAMETER action      AS CHAR NO-UNDO.
DEF INPUT PARAMETER from-date   AS DATE NO-UNDO.
DEF INPUT PARAMETER to-date     AS DATE NO-UNDO.
DEF OUTPUT PARAMETER TABLE FOR b1-list.

RUN disp-it.

PROCEDURE disp-it:
  IF ((usrID NE ?) /*AND (usrID NE "")*/) AND (action = ?) THEN
  DO:
      FIND FIRST bediener WHERE bediener.userinit = TRIM(ENTRY(1, usrID, "-"))
          NO-LOCK.
      FOR EACH res-history WHERE res-history.datum GE from-date
          AND res-history.datum LE to-date 
          AND res-history.nr = bediener.nr NO-LOCK,
          FIRST ubuff WHERE ubuff.nr = res-history.nr NO-LOCK
          BY res-history.datum BY res-history.action BY res-history.zeit:
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
