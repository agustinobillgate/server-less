
DEFINE TEMP-TABLE q1-list LIKE guest
    FIELD rec-id            AS INT
    FIELD aktcust-rec-id    AS INT
    FIELD userinit          LIKE akt-cust.userinit
    FIELD datum             LIKE akt-cust.datum
    FIELD c-init            LIKE akt-cust.c-init
    FIELD a-gastnr          LIKE akt-cust.gastnr.

DEF INPUT  PARAMETER user-init  AS CHAR.
DEF INPUT  PARAMETER lname      AS CHAR.
DEF OUTPUT PARAMETER ext-char   AS CHAR.
DEF OUTPUT PARAMETER usr-name   AS CHAR.
DEF OUTPUT PARAMETER usr-init   AS CHAR.
DEF OUTPUT PARAMETER old-init   AS CHAR.
DEF OUTPUT PARAMETER tot-gcf    AS INT.
DEF OUTPUT PARAMETER TABLE FOR q1-list.

FIND FIRST htparam WHERE paramnr = 148 no-lock.  /* Extended CHAR FOR GCF Prog */ 
ext-char = htparam.fchar. 

FIND FIRST bediener WHERE bediener.userinit = user-init NO-LOCK. 
usr-name = bediener.username. 
usr-init = user-init. 
old-init = usr-init. 

tot-gcf = 0.
IF usr-init NE "" THEN 
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

    tot-gcf = tot-gcf + 1.
END.
