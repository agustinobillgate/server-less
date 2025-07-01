DEFINE TEMP-TABLE t-guestbook NO-UNDO LIKE guestbook
    FIELD recidguestbook AS INT
    INDEX ori_ix orig-infostr.

DEFINE INPUT PARAMETER userSession AS CHAR.
DEFINE OUTPUT PARAMETER scan-data AS CHAR.
DEFINE OUTPUT PARAMETER scan-image AS LONGCHAR.
DEFINE OUTPUT PARAMETER finish-flag AS LOGICAL INIT ?.
DEFINE OUTPUT PARAMETER success-flag AS LOGICAL INIT ?.

DEFINE VARIABLE pointer AS MEMPTR.
DEFINE VARIABLE guestnumber AS INT.
DEFINE VARIABLE recguestbook AS INT.

DEFINE VARIABLE logid  AS INT.
DEFINE VARIABLE logstr AS CHAR.

IF userSession EQ "" THEN userSession = "".
IF userSession EQ ?  THEN userSession = "".

logid = RANDOM(1,99999).
logstr = "LOGID=" + STRING(logid) + "|SESSION=" + userSession + "|START". 
MESSAGE logstr VIEW-AS ALERT-BOX INFO BUTTONS OK.

FIND LAST queasy WHERE 
    queasy.KEY EQ 999 AND
    queasy.char1 EQ userSession NO-LOCK NO-ERROR.
IF AVAILABLE queasy THEN
DO:
    FIND CURRENT queasy EXCLUSIVE-LOCK.
    
    logstr = "LOGID=" + STRING(logid) + "|SESSION=" + userSession + "|FOUND QUEASY". 
    MESSAGE logstr VIEW-AS ALERT-BOX INFO BUTTONS OK.

    finish-flag  = queasy.logi1.
    success-flag = queasy.logi2.
    scan-data    = queasy.char2.
    guestnumber  = queasy.number2.

    FOR EACH guestbook WHERE guestbook.gastnr EQ guestnumber NO-LOCK:
        CREATE t-guestbook.
        BUFFER-COPY guestbook TO t-guestbook.
        recidguestbook = RECID(guestbook).
    END.
    RELEASE guestbook.
    
    FIND FIRST t-guestbook WHERE t-guestbook.orig-infostr EQ userSession NO-ERROR.
    IF AVAILABLE t-guestbook THEN
    DO:
        logstr = "LOGID=" + STRING(logid) + "|SESSION=" + userSession + "|FOUND GUESTBOOK". 
        MESSAGE logstr VIEW-AS ALERT-BOX INFO BUTTONS OK.

        recguestbook = t-guestbook.recidguestbook.

        COPY-LOB t-guestbook.imagefile TO pointer.
        scan-image = BASE64-ENCODE(pointer).

        IF finish-flag THEN
        DO:
            DELETE t-guestbook.
        END.
        RELEASE t-guestbook.
    END.

    DEFINE BUFFER bguestbook FOR guestbook.
    IF finish-flag THEN
    DO:
        DELETE queasy.
        FIND FIRST bguestbook WHERE RECID(bguestbook) EQ recguestbook EXCLUSIVE-LOCK NO-ERROR.
        IF AVAILABLE bguestbook THEN
        DO:
            DELETE bguestbook.
        END.
    END.
    FIND CURRENT queasy NO-LOCK.
END.
logstr = "LOGID=" + STRING(logid) + "|SESSION=" + userSession + "|END|FINIS=" + STRING(finish-flag). 
MESSAGE logstr VIEW-AS ALERT-BOX INFO BUTTONS OK.

