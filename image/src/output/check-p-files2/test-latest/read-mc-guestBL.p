
DEF TEMP-TABLE t-mc-guest LIKE mc-guest.

DEF INPUT  PARAMETER case-type  AS INTEGER NO-UNDO.
DEF INPUT  PARAMETER guestNo    AS INTEGER NO-UNDO.
DEF INPUT  PARAMETER cardNum    AS CHAR    NO-UNDO.
DEF OUTPUT PARAMETER TABLE FOR t-mc-guest.

CASE case-type:
  WHEN 1 THEN
  DO:
    FIND FIRST mc-guest WHERE mc-guest.gastnr = guestNo 
      AND mc-guest.activeflag = YES NO-LOCK NO-ERROR.
    IF AVAILABLE mc-guest THEN
    DO:
      CREATE t-mc-guest.
      BUFFER-COPY mc-guest TO t-mc-guest.
    END.
  END.
  WHEN 2 THEN
  DO:
    FIND FIRST mc-guest WHERE mc-guest.cardnum = cardNum NO-LOCK NO-ERROR.
    IF AVAILABLE mc-guest THEN
    DO:
      CREATE t-mc-guest.
      BUFFER-COPY mc-guest TO t-mc-guest.
    END.
  END.
  WHEN 3 THEN
  DO:
    FIND FIRST mc-guest WHERE mc-guest.cardnum = cardNum 
      AND mc-guest.gastnr NE guestNo NO-LOCK NO-ERROR.
    IF AVAILABLE mc-guest THEN
    DO:
      CREATE t-mc-guest.
      BUFFER-COPY mc-guest TO t-mc-guest.
    END.
  END.
  WHEN 4 THEN
  DO:
    FIND FIRST mc-guest WHERE mc-guest.gastnr = guestNo NO-LOCK NO-ERROR.
    IF AVAILABLE mc-guest THEN
    DO:
      CREATE t-mc-guest.
      BUFFER-COPY mc-guest TO t-mc-guest.
    END.
  END.
  WHEN 5 THEN
  DO:
    FIND FIRST mc-guest WHERE mc-guest.cardnum = cardNum 
        AND mc-guest.activeflag = YES NO-LOCK NO-ERROR.
    IF AVAILABLE mc-guest THEN
    DO:
      CREATE t-mc-guest.
      BUFFER-COPY mc-guest TO t-mc-guest.
    END.
  END.
END.


