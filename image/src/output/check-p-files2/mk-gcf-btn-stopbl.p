
DEF INPUT PARAMETER gastnr AS INT.
DEF INPUT PARAMETER gcf-ok AS LOGICAL.
DEF INPUT PARAMETER karteityp AS INTEGER.
DEF INPUT-OUTPUT PARAMETER curr-gastnr AS INT.
DEF OUTPUT PARAMETER err-nr AS INT INIT 0.

IF gcf-ok = NO THEN 
DO: 
    IF karteityp = 0 THEN
        FIND FIRST guest WHERE guest.gastnr = curr-gastnr 
            AND guest.karteityp = karteityp EXCLUSIVE-LOCK. 
    ELSE
        FIND FIRST guest WHERE guest.gastnr = curr-gastnr 
            AND guest.karteityp GT 0 EXCLUSIVE-LOCK. 
    guest.gastnr = - guest.gastnr. 
    curr-gastnr = 0.
END. 
ELSE 
DO:
  IF karteityp GE 0 THEN
  DO:
    FIND FIRST guestseg WHERE guestseg.gastnr = gastnr NO-LOCK NO-ERROR. 
    IF NOT AVAILABLE guestseg THEN 
    DO: 
      err-nr = 1.
      RETURN NO-APPLY. 
    END.
  END.
END.
