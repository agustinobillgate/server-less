
DEF INPUT PARAMETER ch AS CHAR.
DEF INPUT PARAMETER nr AS INT.
DEF INPUT PARAMETER username AS CHAR.
DEF INPUT PARAMETER permissions AS CHAR.
DEF INPUT PARAMETER rec-id AS INT.

  CREATE res-history. 
  ASSIGN 
    res-history.nr = nr 
    res-history.datum = TODAY 
    res-history.zeit = TIME
    res-history.action = "User Access"
    res-history.aenderung = "CHG Access Right of: " + username + " " 
    + permissions + "->" + ch
  .
  FIND CURRENT res-history NO-LOCK. 
  RELEASE res-history. 

  FIND FIRST bediener WHERE RECID(bediener) = rec-id EXCLUSIVE-LOCK. 
  bediener.permissions = ch. 
  FIND CURRENT bediener NO-LOCK. 

