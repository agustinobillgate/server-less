DEFINE INPUT PARAMETER guestno         AS INTEGER NO-UNDO.
DEFINE OUTPUT PARAMETER imagedata      AS LONGCHAR NO-UNDO.
DEFINE OUTPUT PARAMETER result-message AS CHAR.

DEFINE VARIABLE pointer  AS MEMPTR NO-UNDO.

IF guestno EQ ? OR guestno EQ 0 THEN
DO:
    result-message = "3 - GuestNumber Can't be Null!".
    RETURN.
END.

FIND FIRST guest WHERE guest.gastnr = guestno NO-ERROR.
IF NOT AVAILABLE guest THEN
DO:
    result-message = "2 - Guest Not Found!".
    RETURN.
END.

FIND FIRST guestbook WHERE guestbook.gastnr = guest.gastnr EXCLUSIVE-LOCK NO-ERROR.
IF NOT AVAILABLE guestbook THEN
DO: 
    result-message = "1 - Image ID Card Not exist!".
    RETURN.
    .
END.
ELSE
DO:
    COPY-LOB guestbook.imagefile TO pointer.
    imagedata = BASE64-ENCODE(pointer).
    result-message = "0 - Image ID Card Already Exist!".
END.







