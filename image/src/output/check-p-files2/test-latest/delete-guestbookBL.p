DEF INPUT PARAMETER gastno AS INTEGER NO-UNDO.

FIND FIRST vhp.guestbook WHERE vhp.guestbook.gastnr = gastno NO-ERROR.
IF AVAILABLE vhp.guestbook THEN
DO:
  DELETE vhp.guestbook.
  RELEASE vhp.guestbook.
END.
