DEFINE INPUT PARAMETER userinit AS CHAR.
DEFINE INPUT PARAMETER rec-id AS INTEGER.

DEFINE VARIABLE curr-nr AS INTEGER.

DEFINE BUFFER bqueasy FOR queasy.

/*
FIND FIRST bediener WHERE bediener.userinit = userinit NO-LOCK. 

FIND FIRST queasy WHERE RECID(queasy) = rec-id NO-LOCK.

curr-nr = queasy.number3.

CREATE res-history. 
ASSIGN 
  res-history.nr = bediener.nr 
  res-history.datum = TODAY 
  res-history.zeit = TIME 
  res-history.aenderung = "Delete LostFound No" 
    + STRING(queasy.number3,">>>9") 
    + " Room " + queasy.char1.
  res-history.action = "HouseKeeping". 
FIND CURRENT res-history NO-LOCK. 
RELEASE res-history. 

FIND CURRENT queasy EXCLUSIVE-LOCK.
delete queasy. 

FOR EACH queasy WHERE queasy.KEY EQ 195 AND
  queasy.char1 = "LostAndFound;nr=" + STRING(curr-nr) EXCLUSIVE-LOCK:

  FIND FIRST guestbook WHERE guestbook.gastnr EQ queasy.number1 EXCLUSIVE-LOCK.
  IF AVAILABLE guestbook THEN
  DO:
    DELETE guestbook.
  END.

  DELETE queasy.
END.
*/

/*Alder - Serverless - Issue 785 - Start*/
FIND FIRST bediener WHERE bediener.userinit EQ userinit NO-LOCK NO-ERROR.
IF AVAILABLE bediener THEN
DO:
    FIND FIRST queasy WHERE RECID(queasy) EQ rec-id NO-LOCK NO-ERROR.
    IF AVAILABLE queasy THEN
    DO:
        ASSIGN curr-nr = queasy.number3.

        CREATE res-history.
        ASSIGN
            res-history.nr          = bediener.nr
            res-history.datum       = TODAY
            res-history.zeit        = TIME
            res-history.aenderung   = "Delete LostFound No"
                                    + STRING(queasy.number3, ">>>9")
                                    + " Room " + queasy.char1.
            res-history.action      = "HouseKeeping".
        FIND CURRENT res-history NO-LOCK.
        RELEASE res-history.

        FIND CURRENT queasy EXCLUSIVE-LOCK.
        DELETE queasy.
        RELEASE queasy.
    END.
END.

FOR EACH queasy WHERE queasy.KEY EQ 195 AND queasy.char1 EQ "LostAndFound;nr=" + STRING(curr-nr) NO-LOCK:
    FIND FIRST guestbook WHERE guestbook.gastnr EQ queasy.number1 NO-LOCK NO-ERROR.
    IF AVAILABLE guestbook THEN
    DO:
        FIND CURRENT guestbook EXCLUSIVE-LOCK.
        DELETE guestbook.
        RELEASE guestbook.
    END.

    FIND FIRST bqueasy WHERE RECID(bqueasy) EQ RECID(queasy) EXCLUSIVE-LOCK.
    DELETE bqueasy.
    RELEASE bqueasy.
END.
/*Alder - Serverless - Issue 785 - End*/
