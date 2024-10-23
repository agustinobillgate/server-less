DEFINE TEMP-TABLE esign-list NO-UNDO
    FIELD sign-nr       AS INT FORMAT ">>>" LABEL "No"
    FIELD sign-name     AS CHARACTER FORMAT "x(35)" LABEL "Name"
    FIELD sign-img      AS BLOB 
    FIELD sign-use-for  AS CHARACTER FORMAT "x(15)" LABEL "Use For"
    FIELD sign-position AS CHARACTER FORMAT "x(23)" LABEL "Position"
    FIELD sign-userinit AS CHARACTER FORMAT "x(15)" LABEL "Username"
    FIELD sign-id       AS INTEGER FORMAT "->>>>>>>>>>"
    FIELD sign-select   AS LOGICAL
    FIELD sign-pass     AS CHAR 
    .

DEFINE TEMP-TABLE esign-print NO-UNDO
    FIELD sign-nr       AS INT FORMAT ">>>" LABEL "No"
    FIELD sign-name     AS CHARACTER FORMAT "x(35)" LABEL "Name"
    FIELD sign-img      AS BLOB 
    FIELD sign-date     AS CHAR FORMAT "x(20)"
    .

DEFINE INPUT PARAMETER case-type AS INT.
DEFINE INPUT PARAMETER user-init AS CHAR.
DEFINE INPUT PARAMETER docu-nr AS CHAR.
DEFINE OUTPUT PARAMETER found-flag AS LOGICAL.
DEFINE OUTPUT PARAMETER TABLE FOR esign-list.
DEFINE OUTPUT PARAMETER TABLE FOR esign-print.

IF case-type EQ 1 THEN
DO:
    FIND FIRST guestbook WHERE guestbook.gastnr GE -271100
        AND guestbook.gastnr LE -271080 
        AND guestbook.userinit EQ user-init NO-LOCK NO-ERROR.
    IF AVAILABLE guestbook THEN
    DO:
        found-flag = YES.
        CREATE esign-list.
        ASSIGN 
            esign-list.sign-nr       = INT(ENTRY(1,guestbook.infostr,"|"))
            esign-list.sign-name     = ENTRY(2,guestbook.infostr,"|")
            esign-list.sign-img      = guestbook.imagefile
            esign-list.sign-use-for  = ENTRY(3,guestbook.infostr,"|")
            esign-list.sign-position = ENTRY(4,guestbook.infostr,"|")
            esign-list.sign-userinit = guestbook.userinit
            esign-list.sign-id       = guestbook.gastnr
            esign-list.sign-pass     = guestbook.reserve-char[1]
            .
    END.
    ELSE found-flag = NO. 
END.
ELSE IF case-type EQ 2 THEN
DO:
    FOR EACH queasy WHERE queasy.KEY EQ 227 AND queasy.char1 EQ docu-nr NO-LOCK:
        FIND FIRST guestbook WHERE guestbook.gastnr EQ queasy.number2 NO-LOCK NO-ERROR.
        IF AVAILABLE guestbook THEN
        DO:
            CREATE esign-print.         
            ASSIGN esign-print.sign-nr   = queasy.number1
                   esign-print.sign-name = ENTRY(2,guestbook.infostr,"|")
                   esign-print.sign-img  = guestbook.imagefile
                   esign-print.sign-date = ENTRY(2,queasy.char3,"|").
        END.
    END.
END.

