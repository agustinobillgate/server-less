DEFINE TEMP-TABLE q1-list LIKE guest
    FIELD rec-id          AS INT
    FIELD aktcust-rec-id  AS INT
    FIELD userinit        LIKE akt-cust.userinit
    FIELD datum           LIKE akt-cust.datum
    FIELD c-init          LIKE akt-cust.c-init
    FIELD a-gastnr        LIKE akt-cust.gastnr.

DEF INPUT  PARAMETER lname    AS CHAR.
DEF INPUT  PARAMETER usr-init AS CHAR.
DEF OUTPUT PARAMETER err      AS INT INIT 0.
DEF OUTPUT PARAMETER TABLE FOR q1-list.

DEF BUFFER ubuff FOR bediener.

FIND FIRST ubuff WHERE ubuff.userinit = usr-init NO-LOCK NO-ERROR. 
IF NOT AVAILABLE ubuff THEN 
DO:
    err = 1.
    RETURN NO-APPLY.
END.

IF usr-init GE "" THEN 
DO:
    FOR EACH akt-cust WHERE akt-cust.userinit = usr-init NO-LOCK, 
        FIRST guest WHERE guest.gastnr = akt-cust.gastnr 
        AND guest.phonetik3 = akt-cust.userinit AND guest.NAME GE lname 
        AND guest.gastnr NE 0 NO-LOCK BY guest.name:
        FIND FIRST q1-list WHERE q1-list.gastnr = guest.gastnr
            NO-LOCK NO-ERROR.
        IF NOT AVAILABLE q1-list THEN
        DO:
            CREATE q1-list.
            BUFFER-COPY guest TO q1-list.
            ASSIGN 
                q1-list.rec-id          = RECID(guest)
                q1-list.aktcust-rec-id  = RECID(akt-cust)
                q1-list.userinit        = akt-cust.userinit
                q1-list.datum           = akt-cust.datum
                q1-list.c-init          = akt-cust.c-init
                q1-list.a-gastnr        = akt-cust.gastnr.
        END.
    END.
END.

