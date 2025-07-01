 
  
/* DELETE  GCF */ 
DEFINE INPUT PARAMETER userinit AS CHARACTER. 
DEFINE INPUT PARAMETER gastnr   AS INTEGER. 

DEFINE BUFFER guest1 FOR guest.
DEFINE BUFFER tqueasy FOR queasy.
/*IF 080419*/
DEFINE VARIABLE gastNo  AS CHARACTER NO-UNDO.
/*END IF*/

FIND FIRST guest WHERE guest.gastnr = gastnr NO-LOCK. 
DO TRANSACTION:
  FIND CURRENT guest EXCLUSIVE-LOCK. 

  FOR EACH guestseg WHERE guestseg.gastnr = guest.gastnr EXCLUSIVE-LOCK: 
    DELETE guestseg. 
  END. 
  FOR EACH history WHERE history.gastnr = guest.gastnr EXCLUSIVE-LOCK: 
    DELETE history. 
  END. 
  FOR EACH guest-pr WHERE guest-pr.gastnr = guest.gastnr EXCLUSIVE-LOCK: 
    DELETE guest-pr. 
  END. 
  FOR EACH gk-notes WHERE gk-notes.gastnr = guest.gastnr EXCLUSIVE-LOCK: 
    DELETE gk-notes. 
  END. 
  FOR EACH guestbud WHERE guestbud.gastnr = guest.gastnr EXCLUSIVE-LOCK: 
    DELETE guestbud. 
  END. 
  FOR EACH akt-kont WHERE akt-kont.gastnr = guest.gastnr EXCLUSIVE-LOCK: 
    DELETE akt-kont. 
  END.

  FOR EACH queasy WHERE queasy.KEY = 231 AND queasy.number1 = guest.gastnr EXCLUSIVE-LOCK:
    DELETE queasy.
  END.
  FOR EACH tqueasy WHERE tqueasy.KEY = 212 AND tqueasy.number3 = guest.gastnr EXCLUSIVE-LOCK:
    DELETE tqueasy.
  END.

/* Document Scanner License */
  FIND FIRST htparam WHERE htparam.paramnr = 472 NO-LOCK.
  IF htparam.flogical THEN RUN delete-guestbookbl.p(guest.gastnr). 
  
  DELETE guest.
  RELEASE guest.

  FIND FIRST bediener WHERE bediener.userinit = userinit NO-LOCK. 
  CREATE res-history. 
  ASSIGN 
      res-history.nr = bediener.nr 
      res-history.datum = TODAY 
      res-history.zeit = TIME 
      res-history.aenderung = "Delete GuestCard: GastNo " + STRING(gastnr)
      res-history.action = "GuestFile". 
  FIND CURRENT res-history NO-LOCK. 
  RELEASE res-history.
END.

