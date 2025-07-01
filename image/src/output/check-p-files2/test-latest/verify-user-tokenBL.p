/* 
SY: 20/11/2019
Purpore: 
- To check if user token is valid 
- Update / create new master key and new user token if expired
Output Parameter
- new-user-token if user-token is correct but expired
- i-result: 0 = user token is correct and up-to-date
            1 = user token is correct and expired
            2 = user token is incorrect. The related program has to be
            terminated / back to Login Screen.
            9 = black list (not implemented yet)
Remark:
- The master key will be expired after 30 minutes and the new master
  key will be generated and saved in guest-queasy
- Upto 4 expired master keys will be kept in guest-queasy 

*/
/**/
DEFINE INPUT PARAMETER user-init         AS CHAR    NO-UNDO.
DEFINE INPUT PARAMETER license-nr        AS CHAR    NO-UNDO.
DEFINE INPUT PARAMETER user-token        AS CHAR    NO-UNDO. 
DEFINE OUTPUT PARAMETER new-user-token   AS CHAR    NO-UNDO.
DEFINE OUTPUT PARAMETER i-result         AS INTEGER NO-UNDO INIT 0.
DEFINE OUTPUT PARAMETER errMess          AS CHAR    NO-UNDO.

/*
DEFINE VARIABLE user-init        AS CHAR    NO-UNDO INIT "01".
DEFINE VARIABLE user-code        AS CHAR    NO-UNDO INIT "system@1016".
DEFINE VARIABLE license-nr       AS CHAR    NO-UNDO INIT 2216.
DEFINE VARIABLE user-token       AS CHAR    NO-UNDO.
DEFINE VARIABLE new-user-token   AS CHAR    NO-UNDO.
DEFINE VARIABLE i-result         AS INTEGER NO-UNDO INIT 0.
DEFINE VARIABLE errMess          AS CHAR    NO-UNDO.
       
user-token = "eyJhbGciOiJIUzI1NiIsInR5cGUiOiJKV1QifQeyJsb2dnZWRJbkFzIjoiYWRtaW4iLCJnZW5lcmF0ZWQiOiIyMDIwLTAxLTA4VDE3OjA5OjMxLjU4MyswNzowMCIsImV4cGlyZWQiOiIyMDIwLTAxLTA4VDE4OjA5OjMxLjU4MyswNzowMCJ9c67ca74a371710b9f39d4d0719969c32261494d0".
*/
DEFINE VARIABLE headerString  AS CHARACTER.
DEFINE VARIABLE payloadString AS CHARACTER.

DEFINE VARIABLE tokenString   AS CHARACTER.
DEFINE VARIABLE calcToken     AS CHARACTER.
DEFINE VARIABLE i             AS INTEGER.
DEFINE VARIABLE secret        AS CHARACTER NO-UNDO.

DEFINE VARIABLE master-key    AS CHAR    NO-UNDO.
DEFINE VARIABLE system-token  AS CHAR    NO-UNDO.
DEFINE VARIABLE l-match       AS LOGICAL NO-UNDO.
DEFINE VARIABLE curr-i        AS INTEGER NO-UNDO INIT 0.
DEFINE VARIABLE max-counter   AS INTEGER NO-UNDO INIT 0.
DEFINE VARIABLE tot-counter   AS INTEGER NO-UNDO INIT 0.

DEFINE VARIABLE last-date     AS DATE    NO-UNDO.
DEFINE VARIABLE last-time     AS INTEGER NO-UNDO.
DEFINE VARIABLE delta-time    AS INTEGER NO-UNDO.

DEFINE BUFFER gqbuff  FOR guest-queasy.
DEFINE BUFFER gqbuff1 FOR guest-queasy.

DEFINE VARIABLE username    AS CHARACTER.
DEFINE VARIABLE tokenlen    AS INT.

new-user-token = user-token.

tokenlen       = LENGTH(user-token) - 39.
tokenString    = SUBSTRING(user-token,tokenlen,40).

FIND FIRST bediener WHERE bediener.userinit EQ user-init NO-LOCK NO-ERROR.
username = bediener.username.

DEF VAR secret-str AS CHAR.

/*MESSAGE "in masdod 1"
    VIEW-AS ALERT-BOX INFO BUTTONS OK.*/
FOR EACH guest-queasy WHERE guest-queasy.KEY = "userToken" AND guest-queasy.char1 EQ user-init NO-LOCK BY guest-queasy.number3 DESCENDING:
    ASSIGN 
        tot-counter = tot-counter + 1
        curr-i      = guest-queasy.number3
        master-key  = ENTRY(1,guest-queasy.char3,"|")
    .
    IF max-counter = 0 THEN 
    ASSIGN    
        last-date    = guest-queasy.date1
        last-time    = guest-queasy.number1
        max-counter  = guest-queasy.number3
    .

    /*MESSAGE "in masdod 2"
    VIEW-AS ALERT-BOX INFO BUTTONS OK.*/
    IF NOT l-match THEN
    DO:
        /*secret = LC(username) + license-nr + master-key.*/
        secret = master-key.
        /*MESSAGE "in masdod " secret
    VIEW-AS ALERT-BOX INFO BUTTONS OK.*/
        DO i = 1 TO LENGTH(secret):
            secret-str = secret-str + "#" + SUBSTRING(secret,i,1).
        END.
    
        secret-str = secret-str + "#".
    
        calcToken = HEX-ENCODE(SHA1-DIGEST(secret-str)).
    
        MESSAGE "tokenString " tokenString SKIP
                "calcToken " calcToken
            VIEW-AS ALERT-BOX INFO BUTTONS OK.
    
        ASSIGN l-match = (tokenString EQ calcToken).

        IF l-match THEN LEAVE.
    END.
END.



IF NOT l-match THEN
DO:
    i-result = 2.
    errMess  = "Invalid Token".
    RETURN.
END.

IF curr-i LT max-counter THEN i-result = 1. /* userToken needs to be updated */
ELSE
DO: /* curr-i = max-counter */
    delta-time = TIME + (TODAY - last-date) * 86400 - last-time.
    IF delta-time LE 1800 THEN RETURN. /* userToken's age LE 30 minutes */
    ELSE i-result = 1. /* userToken needs to be updated */
END.

MESSAGE "i-result " i-result
    VIEW-AS ALERT-BOX INFO BUTTONS OK.

IF i-result = 1 THEN /* update userToken and master key */
DO:
    IF tot-counter GE 4 THEN /* The system only stores maximum 4 master keys */
    DO:
        FIND FIRST gqbuff WHERE gqbuff.KEY = "userToken" AND gqbuff.char1 EQ user-init AND gqbuff.number3 LE 1 NO-LOCK NO-ERROR.
        DO WHILE AVAILABLE gqbuff:
            DO TRANSACTION:
                FIND FIRST gqbuff1 WHERE RECID(gqbuff1) EQ RECID(gqbuff) EXCLUSIVE-LOCK.
                DELETE gqbuff1.
                RELEASE gqbuff1.
            END.
            FIND NEXT gqbuff WHERE gqbuff.KEY = "userToken" AND gqbuff.char1 EQ user-init AND gqbuff.number3 LE 1 NO-LOCK NO-ERROR.
        END.
        
        FIND FIRST guest-queasy WHERE guest-queasy.KEY = "userToken" AND guest-queasy.char1 EQ user-init NO-LOCK NO-ERROR.
        IF AVAILABLE guest-queasy THEN
        DO:
            FIND FIRST gqbuff WHERE gqbuff.KEY = "userToken" AND gqbuff.char1 EQ user-init AND gqbuff.number3 EQ 1 NO-LOCK NO-ERROR.
            DO WHILE NOT AVAILABLE gqbuff:
                max-counter = max-counter - 1.
                FOR EACH guest-queasy WHERE guest-queasy.KEY EQ "userToken" AND guest-queasy.char1 EQ user-init NO-LOCK:
                    DO TRANSACTION:
                        FIND FIRST gqbuff1 WHERE RECID(gqbuff1) = RECID(guest-queasy) EXCLUSIVE-LOCK.
                        gqbuff1.number3 = gqbuff1.number3 - 1.
                        FIND CURRENT gqbuff1 NO-LOCK.
                    END.
                END.
                FIND NEXT gqbuff WHERE gqbuff.KEY = "userToken" AND gqbuff.char1 EQ user-init AND gqbuff.number3 EQ 1 NO-LOCK NO-ERROR.
            END.
        END.
        ELSE max-counter = 0.
    END.
    
    RUN update-master-key(OUTPUT master-key). 
    DO TRANSACTION:
        CREATE guest-queasy.
        ASSIGN
            guest-queasy.KEY     = "userToken"
            guest-queasy.date1   = TODAY
            guest-queasy.number1 = TIME
            guest-queasy.number3 = max-counter + 1
            guest-queasy.char3   = master-key
            guest-queasy.char1   = user-init
        .
        FIND CURRENT guest-queasy NO-LOCK.
    END.
    RUN get-user-tokenbl.p (user-init, "", license-nr, master-key, OUTPUT new-user-token).
END.

PROCEDURE update-master-key:
    DEFINE OUTPUT PARAMETER new-key AS CHAR.
    DEF VAR user-pswd AS CHAR.
    RUN decode-string1(bediener.usercode, OUTPUT user-pswd). 

    new-key = license-Nr + CAPS(bediener.username) + CAPS(user-pswd) + "|" + STRING(TODAY) + STRING(TIME).

END.

PROCEDURE decode-string1: 
DEFINE INPUT PARAMETER in-str   AS CHAR     NO-UNDO. 
DEFINE OUTPUT PARAMETER out-str AS CHAR     NO-UNDO INITIAL "". 
DEFINE VARIABLE s               AS CHAR     NO-UNDO. 
DEFINE VARIABLE j               AS INTEGER  NO-UNDO. 
DEFINE VARIABLE len             AS INTEGER  NO-UNDO. 
    ASSIGN
        s   = in-str 
        j   = ASC(SUBSTR(s, 1, 1)) - 71 
        len = LENGTH(in-str) - 1 
        s   = SUBSTR(in-str, 2, len)
    .
    DO len = 1 TO LENGTH(s): 
      out-str = out-str + chr(ASC(SUBSTR(s,len,1)) - j). 
    END. 
    out-str = SUBSTR(out-str, 5, (LENGTH(out-str) - 4)). 
END. 
