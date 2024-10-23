
DEFINE INPUT PARAMETER curr-date AS DATE NO-UNDO. 
DEFINE INPUT PARAMETER foreign-flag AS LOGICAL.
DEF OUTPUT PARAMETER exrate-betrag AS DECIMAL INIT 0.
DEF OUTPUT PARAMETER frate AS DECIMAL INIT 0.

RUN find-exrate.
IF AVAILABLE exrate THEN frate = exrate.betrag. 

PROCEDURE find-exrate: 
DEFINE VARIABLE foreign-nr       AS INTEGER INITIAL 0 NO-UNDO. 

  IF foreign-flag THEN
  DO:
      FIND FIRST exrate WHERE exrate.artnr = 99999 
          AND exrate.datum = curr-date NO-LOCK NO-ERROR.
      IF AVAILABLE exrate THEN RETURN.
  END.

  FIND FIRST htparam WHERE htparam.paramnr = 144 NO-LOCK. 
  IF htparam.fchar NE "" THEN 
  DO: 
    FIND FIRST waehrung WHERE waehrung.wabkurz = htparam.fchar NO-LOCK NO-ERROR. 
    IF AVAILABLE waehrung THEN foreign-nr = waehrung.waehrungsnr. 
  END. 

  IF foreign-nr NE 0 THEN FIND FIRST exrate WHERE exrate.artnr = foreign-nr 
    AND exrate.datum = curr-date NO-LOCK NO-ERROR. 
  ELSE FIND FIRST exrate WHERE exrate.datum = curr-date NO-LOCK NO-ERROR. 

  IF AVAILABLE exrate THEN exrate-betrag = exrate.betrag. 
END. 
 
