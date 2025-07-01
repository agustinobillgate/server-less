DEFINE TEMP-TABLE q1-list LIKE guest
    FIELD rec-id            AS INT
    FIELD aktcust-rec-id    AS INT
    FIELD userinit          LIKE akt-cust.userinit
    FIELD datum             LIKE akt-cust.datum
    FIELD c-init            LIKE akt-cust.c-init
    FIELD a-gastnr          LIKE akt-cust.gastnr.

DEF INPUT  PARAMETER pvILanguage    AS INTEGER NO-UNDO.
DEF INPUT  PARAMETER gastnr         AS INTEGER.
DEF INPUT  PARAMETER lname          AS CHAR.
DEF INPUT  PARAMETER usr-init       AS CHAR.
DEF INPUT  PARAMETER user-init      AS CHAR.
DEF OUTPUT PARAMETER msg-str        AS CHAR.
DEF OUTPUT PARAMETER TABLE FOR q1-list.

{SupertransBL.i} 
DEF VAR lvCAREA AS CHAR INITIAL "comp-stataccor".

RUN create-list.

PROCEDURE create-list:
DEFINE buffer akt-cust1 FOR akt-cust. 
DEFINE buffer usr FOR bediener. 
DEFINE buffer guest1 FOR guest. 
DEFINE VARIABLE answer AS LOGICAL. 
  answer = YES. 
  FIND FIRST akt-cust1 WHERE akt-cust1.gastnr = gastnr NO-LOCK NO-ERROR. 
  IF AVAILABLE akt-cust1 THEN 
  DO: 
    FIND FIRST guest1 WHERE guest1.gastnr = gastnr NO-LOCK. 
    FIND FIRST usr WHERE usr.userinit = akt-cust1.userinit NO-LOCK. 
    msg-str = caps(guest1.name) 
        + translateExtended( " - has been selected by", lvCAREA, "":U) 
      + CHR(10) +
      usr.userinit + " - " + usr.username 
      + CHR(10) +
      translateExtended( "Double-entry not allowed.", lvCAREA, "":U) 
      .    
  END. 
  ELSE 
  DO TRANSACTION: 
    FIND FIRST guest1 WHERE guest1.gastnr = gastnr EXCLUSIVE-LOCK. 
    guest1.phonetik3 = usr-init. 
    CREATE akt-cust. 
    ASSIGN 
      akt-cust.gastnr = gastnr 
      akt-cust.c-init = user-init 
      akt-cust.userinit = usr-init. 
    FIND CURRENT akt-cust NO-LOCK. 
    FIND CURRENT guest1 NO-LOCK. 

    FOR EACH akt-cust WHERE akt-cust.userinit = usr-init NO-LOCK, 
        FIRST guest WHERE guest.gastnr = akt-cust.gastnr 
        AND guest.phonetik3 = akt-cust.userinit AND guest.NAME GE lname 
        AND guest.gastnr GT 0 NO-LOCK BY guest.name:
        CREATE q1-list.
        BUFFER-COPY guest TO q1-list.
        ASSIGN 
            q1-list.rec-id            = RECID(guest)
            q1-list.aktcust-rec-id    = RECID(akt-cust)
            q1-list.userinit      = akt-cust.userinit
            q1-list.datum         = akt-cust.datum
            q1-list.c-init        = akt-cust.c-init
            q1-list.a-gastnr      = akt-cust.gastnr.
    END.

  END. 
END. 
