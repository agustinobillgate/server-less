DEF TEMP-TABLE t-guest-pr LIKE guest-pr.

DEF INPUT  PARAMETER case-type AS INTEGER NO-UNDO.
DEF INPUT  PARAMETER guestNo   AS INTEGER NO-UNDO.
DEF INPUT  PARAMETER rateCode  AS CHAR    NO-UNDO.
DEF OUTPUT PARAMETER TABLE FOR t-guest-pr.

CASE case-type:
  WHEN 1 THEN 
  DO:
    FIND FIRST guest-pr WHERE guest-pr.gastnr = guestNo NO-LOCK NO-ERROR.
    IF AVAILABLE guest-pr THEN
    DO:
      CREATE t-guest-pr.
      BUFFER-COPY guest-pr TO t-guest-pr.
    END.
  END.
  WHEN 2 THEN
  DO:
    FIND FIRST guest-pr WHERE guest-pr.CODE = rateCode NO-LOCK NO-ERROR.
    IF AVAILABLE guest-pr THEN
    DO:
      CREATE t-guest-pr.
      BUFFER-COPY guest-pr TO t-guest-pr.
    END.
  END.
  WHEN 3 THEN
  FOR EACH guest-pr WHERE guest-pr.gastnr = guestNo NO-LOCK BY guest-pr.CODE:
    CREATE t-guest-pr.
    BUFFER-COPY guest-pr TO t-guest-pr.
  END.
  WHEN 4 THEN
  DO:
      FIND FIRST guest-pr WHERE guest-pr.gastnr = guestNo
          AND guest-pr.CODE = rateCode NO-LOCK NO-ERROR.
      IF AVAILABLE guest-pr THEN
      DO:
        CREATE t-guest-pr.
        BUFFER-COPY guest-pr TO t-guest-pr.
      END.
  END.
  WHEN 5 THEN
  FOR EACH guest-pr WHERE guest-pr.gastnr = guestNo 
      AND guest-pr.CODE NE rateCode NO-LOCK BY guest-pr.CODE:
      CREATE t-guest-pr.
      BUFFER-COPY guest-pr TO t-guest-pr.
  END.
  WHEN 6 THEN
  DO:
      FOR EACH guest-pr WHERE guest-pr.CODE = rateCode NO-LOCK :
          CREATE t-guest-pr.
          BUFFER-COPY guest-pr TO t-guest-pr.
      END.
  END.
END CASE.
