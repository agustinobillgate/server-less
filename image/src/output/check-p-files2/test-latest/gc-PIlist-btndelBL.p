DEFINE INPUT PARAMETER docu-nr LIKE gc-pi.docu-nr.
DEFINE INPUT PARAMETER user-init LIKE bediener.userinit.



  DO TRANSACTION:
    FIND FIRST gc-pi WHERE gc-pi.docu-nr = docu-nr EXCLUSIVE-LOCK.
    ASSIGN 
      gc-pi.pi-status = 9
      gc-pi.cancelDate = TODAY
      gc-pi.cancelID = user-init
      gc-pi.cancelZeit = TIME
    .
    FIND CURRENT gc-pi NO-LOCK.
  END.
