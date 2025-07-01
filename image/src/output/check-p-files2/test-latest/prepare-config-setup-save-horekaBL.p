DEFINE TEMP-TABLE tlist
    FIELD datum       AS DATE
    FIELD depart      AS INTEGER
    FIELD approved    AS LOGICAL
    FIELD send-horeka AS LOGICAL
    FIELD user-name   AS CHAR
.

DEFINE OUTPUT PARAMETER custID              AS CHAR    NO-UNDO.
DEFINE OUTPUT PARAMETER username            AS CHAR    NO-UNDO.
DEFINE OUTPUT PARAMETER password            AS CHAR    NO-UNDO.
DEFINE OUTPUT PARAMETER url-push            AS CHAR    NO-UNDO.
DEFINE OUTPUT PARAMETER url-notif           AS CHAR    NO-UNDO.
DEFINE OUTPUT PARAMETER storage             AS INTEGER NO-UNDO.
DEFINE OUTPUT PARAMETER push-dml            AS LOGICAL NO-UNDO.
DEFINE OUTPUT PARAMETER art-deposit         AS INTEGER NO-UNDO.
DEFINE OUTPUT PARAMETER api-key             AS CHAR    NO-UNDO.
DEFINE OUTPUT PARAMETER supplier            AS CHAR    NO-UNDO.
DEFINE OUTPUT PARAMETER coa-apdeposit       AS CHAR    NO-UNDO.
DEFINE OUTPUT PARAMETER coa-apclearence     AS CHAR    NO-UNDO.
DEFINE OUTPUT PARAMETER artikel-apclearence AS INTEGER NO-UNDO.
DEFINE OUTPUT PARAMETER usr-id              AS INTEGER NO-UNDO.
DEFINE OUTPUT PARAMETER TABLE FOR tlist.

DEFINE VARIABLE loopi AS INTEGER NO-UNDO.
DEFINE VARIABLE str   AS CHAR    NO-UNDO.


FIND FIRST queasy WHERE queasy.KEY = 253 NO-LOCK NO-ERROR.
IF AVAILABLE queasy THEN DO:
    DO loopi = 1 TO NUM-ENTRIES(queasy.char1,";"):
        str = ENTRY(loopi, queasy.char1, ";").
        IF SUBSTR(str,1,8) = "$CustID$" THEN ASSIGN custID = SUBSTR(str,9).
        ELSE IF SUBSTR(str,1,10)  = "$username$" THEN ASSIGN username = SUBSTR(str,11).
        ELSE IF SUBSTR(str,1,10)  = "$password$" THEN ASSIGN password = SUBSTR(str,11).
        ELSE IF SUBSTR(str,1,9)   = "$urlpush$" THEN ASSIGN url-push = SUBSTR(str,10).
        ELSE IF SUBSTR(str,1,10)  = "$urlnotif$" THEN ASSIGN url-notif = SUBSTR(str,11).
        ELSE IF SUBSTR(str,1,9)   = "$storage$" THEN ASSIGN storage = INTEGER(SUBSTR(str,10)).
        ELSE IF SUBSTR(str,1,9)   = "$pushdml$" THEN ASSIGN push-dml = LOGICAL(SUBSTR(str,10)).
        ELSE IF SUBSTR(str,1,12)  = "$artdeposit$" THEN ASSIGN art-deposit = INTEGER(SUBSTR(str,13)).
        ELSE IF SUBSTR(str,1,8)   = "$apikey$" THEN ASSIGN api-key = SUBSTR(str,9).
        ELSE IF SUBSTR(str,1,10)  = "$supplier$" THEN ASSIGN supplier = SUBSTR(str,11).
        ELSE IF SUBSTR(str,1,11)  = "$apdeposit$" THEN ASSIGN coa-apdeposit = SUBSTR(str,12).
        ELSE IF SUBSTR(str,1,13)  = "$apclearence$" THEN ASSIGN coa-apclearence = SUBSTR(str,14).
        ELSE IF SUBSTR(str,1,11)  = "$artikelap$" THEN ASSIGN artikel-apclearence = INTEGER(SUBSTR(str,12)).
        ELSE IF SUBSTR(str,1,8)  = "$userID$" THEN ASSIGN usr-id = INTEGER(SUBSTR(str,9)).
    END.
END.


FOR EACH queasy WHERE queasy.KEY = 254
    AND queasy.logi2  = YES AND queasy.logi3 = YES NO-LOCK:
    CREATE tlist.
    ASSIGN 
        tlist.datum         = queasy.date1
        tlist.depart        = queasy.number1
        tlist.approved      = queasy.logi1
        tlist.send-horeka   = queasy.logi2
        tlist.user-name     = queasy.char1
    .
END.


