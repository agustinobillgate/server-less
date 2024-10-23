DEFINE INPUT PARAMETER gastno AS INTEGER NO-UNDO.
FIND FIRST vhpgb.guestbook WHERE vhpgb.guestbook.gastnr = gastno EXCLUSIVE-LOCK
    NO-ERROR.
IF AVAILABLE vhpgb.guestbook THEN
DO:
    DELETE vhpgb.guestbook.
    RELEASE guestbook.
END.
