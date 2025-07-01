
DEF INPUT PARAMETER pvILanguage     AS INTEGER NO-UNDO.
DEF INPUT PARAMETER resnr           AS INTEGER.
DEF INPUT PARAMETER reslinnr        AS INTEGER.
DEF INPUT PARAMETER contcode        AS CHAR.
DEF OUTPUT PARAMETER msg-str        AS CHAR.
/*
DEF VAR pvILanguage AS INT INIT 1.
DEF VAR resnr AS INT INIT 16727.
DEF VAR reslinnr AS INT INIT 1.
DEF VAR contcode AS CHAR INIT "".
DEF VAR msg-str AS CHAR.*/

DEF BUFFER waehrung1 FOR waehrung.
DEF BUFFER resline FOR res-line.

{SupertransBL.i} 
DEF VAR lvCAREA AS CHAR INITIAL "res-rmrate". 

FIND FIRST res-line WHERE res-line.resnr = resnr AND res-line.reslinnr = reslinnr
    NO-LOCK.
FIND FIRST guest-pr WHERE guest-pr.gastnr = res-line.gastnr NO-LOCK NO-ERROR. 
/* SY 21/1/2013: do not run this procedure
RUN check-currency.
*/
PROCEDURE check-currency: 
DEF BUFFER rline FOR res-line.
  FIND FIRST reslin-queasy WHERE key = "arrangement" 
    AND reslin-queasy.resnr = resnr 
    AND reslin-queasy.reslinnr = reslinnr NO-LOCK NO-ERROR. 
  IF NOT AVAILABLE reslin-queasy THEN 
  DO: 
    IF NOT AVAILABLE guest-pr THEN RETURN. 
    FIND FIRST queasy WHERE queasy.key = 2 AND queasy.char1 = contcode 
      NO-LOCK NO-ERROR. 
    IF AVAILABLE queasy AND queasy.number1 NE 0 THEN 
    DO: 
      FIND FIRST waehrung1 WHERE waehrung1.waehrungsnr = queasy.number1 
        NO-LOCK NO-ERROR. 
      IF AVAILABLE waehrung1 AND waehrung1.waehrungsnr 
        NE res-line.betriebsnr THEN 
      DO:
        FIND FIRST rline WHERE RECID(rline) = RECID(res-line)
           EXCLUSIVE-LOCK NO-ERROR NO-WAIT.
        IF AVAILABLE rline THEN
        DO:
          UPDATE rline.betriebsnr = waehrung1.waehrungsnr. 
          FIND CURRENT rline NO-LOCK.
          msg-str = msg-str + CHR(2)
                + translateExtended ("No AdHoc Rates found; set back the currency code",lvCAREA,"")
                + CHR(10)
                + translateExtended ("to",lvCAREA,"") + " " + waehrung1.bezeich + " " + translateExtended ("as defined in the contract rates.",lvCAREA,"").
        END.
      END.
    END. 
  END. 
END.
