DEF TEMP-TABLE t-guest   LIKE guest.

DEF INPUT  PARAMETER case-type AS INTEGER NO-UNDO.
DEF INPUT  PARAMETER TABLE FOR t-guest.
DEF OUTPUT PARAMETER success-flag AS LOGICAL INITIAL NO.

FIND FIRST t-guest.

CASE case-type:
  WHEN 1 THEN
  DO:
    FIND FIRST guest WHERE guest.gastnr = t-guest.gastnr 
      EXCLUSIVE-LOCK NO-ERROR NO-WAIT.
    IF AVAILABLE guest THEN
    DO:
      BUFFER-COPY t-guest TO guest.
      FIND CURRENT guest NO-LOCK.
      RELEASE guest.
      success-flag = YES.
    END.
  END.
  WHEN 2 THEN
  DO:
    CREATE guest.
    BUFFER-COPY t-guest TO guest.
    RELEASE guest.
    success-flag = YES.
  END.
  WHEN 3 THEN
  DO:
      FIND FIRST guest WHERE guest.gastnr = t-guest.gastnr 
          EXCLUSIVE-LOCK NO-ERROR NO-WAIT.
      IF AVAILABLE guest THEN
      DO:
          DELETE guest.
          RELEASE guest.
          success-flag = YES.
      END.
  END.
END CASE.

