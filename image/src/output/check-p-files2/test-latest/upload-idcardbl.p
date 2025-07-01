
DEFINE INPUT PARAMETER inp-resnr    AS INTEGER NO-UNDO.
DEFINE INPUT PARAMETER inp-reslinnr AS INTEGER NO-UNDO.
DEFINE INPUT PARAMETER guestno      AS INTEGER NO-UNDO.
DEFINE INPUT PARAMETER imagedata    AS LONGCHAR NO-UNDO.
DEFINE INPUT PARAMETER userinit     AS CHAR NO-UNDO.

DEFINE OUTPUT PARAMETER result-message AS CHAR.

DEFINE VARIABLE pointer  AS MEMPTR NO-UNDO.
DEFINE VARIABLE info-str AS CHAR NO-UNDO.

IF inp-resnr EQ ? OR inp-resnr EQ 0 THEN  
DO:
    result-message = "2 - ResNumber Can't be Null!".
    RETURN.
END.
IF inp-reslinnr EQ ? OR inp-reslinnr EQ 0 THEN
DO:
    result-message = "3 - ResLine Number Can't be Null!".
    RETURN.
END.
IF guestno EQ ? OR guestno EQ 0 THEN
DO:
    result-message = "4 - Guest Can't be Null!".
    RETURN.
END.
IF imagedata EQ ? OR imagedata EQ "" THEN
DO:
    result-message = "5 - Imagedata Can't be Null!".
    RETURN.
END.
IF userinit EQ ? OR userinit EQ "" THEN
DO:
    result-message = "6 - Userinit Can't be Null!".
    RETURN.
END.

info-str = "MC;RN" + STRING(inp-resnr) + ";RL" + STRING(inp-reslinnr) + ";GN" + STRING(guestno).
FIND FIRST guest WHERE guest.gastnr = guestno NO-ERROR.
IF NOT AVAILABLE guest THEN
DO:
    result-message = "1 - Guest Not Found!".
    RETURN.
END.

FIND FIRST guestbook WHERE guestbook.gastnr = guest.gastnr EXCLUSIVE-LOCK NO-ERROR.
IF NOT AVAILABLE guestbook THEN
DO: 
    CREATE guestbook.
    ASSIGN 
    guestbook.gastnr    = guest.gastnr
    guestbook.zeit      = TIME
    guestbook.userinit  = userinit
    .
END.
ELSE
DO:
    ASSIGN 
    guestbook.cid       = userinit
    guestbook.changed   = TODAY
    .
END.

ASSIGN guestbook.reserve-char[1] = STRING(TIME,"99999")
    + STRING(YEAR(TODAY))
    + STRING(MONTH(TODAY),"99") 
    + STRING(DAY(TODAY),"99")
        
    guestbook.infostr = info-str.

pointer = BASE64-DECODE(imagedata).
COPY-LOB pointer TO guestbook.imagefile.

FIND CURRENT guestbook.
RELEASE guestbook.
result-message = "0 - Save Image Success".





