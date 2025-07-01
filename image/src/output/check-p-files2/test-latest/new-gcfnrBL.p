DEF OUTPUT PARAMETER curr-gastnr AS INTEGER NO-UNDO.

  ASSIGN curr-gastnr = 0.
  FIND FIRST guest WHERE guest.gastnr < 0 NO-ERROR. 
  IF AVAILABLE guest THEN 
  DO: 
    curr-gastnr = - guest.gastnr. 
    DELETE guest. 
    FIND FIRST guest WHERE guest.gastnr = curr-gastnr NO-LOCK NO-ERROR.
    IF AVAILABLE guest THEN curr-gastnr = 0.
  END. 
  IF curr-gastnr = 0 THEN
  DO: 
    FIND LAST guest NO-LOCK NO-ERROR. 
    IF AVAILABLE guest THEN curr-gastnr = guest.gastnr + 1. 
    ELSE curr-gastnr = 1. 
  END. 
