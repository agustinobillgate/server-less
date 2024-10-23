DEF TEMP-TABLE t-zimmer   LIKE zimmer.

DEF INPUT PARAMETER TABLE FOR t-zimmer.
DEF OUTPUT PARAMETER success-flag AS LOGICAL INITIAL NO.

FIND FIRST t-zimmer   NO-ERROR.
IF AVAILABLE t-zimmer THEN
DO:
  FIND FIRST zimmer WHERE zimmer.zinr = t-zimmer.zinr EXCLUSIVE-LOCK NO-ERROR.
  IF AVAILABLE zimmer THEN
  DO:
      BUFFER-COPY t-zimmer TO zimmer.
      RELEASE zimmer.
      success-flag = YES.
  END.

END.
