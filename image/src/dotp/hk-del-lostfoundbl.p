DEFINE INPUT PARAMETER userinit AS CHAR.
DEFINE INPUT PARAMETER rec-id AS INTEGER.

DEFINE VARIABLE curr-nr AS INTEGER.


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
