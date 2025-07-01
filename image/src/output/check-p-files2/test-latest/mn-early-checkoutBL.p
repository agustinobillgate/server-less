
DEFINE OUTPUT PARAMETER i       AS INTEGER INIT 0 NO-UNDO.

DEF VAR ci-date AS DATE.
FIND FIRST htparam WHERE paramnr = 87 NO-LOCK.   /* ci-date */ 
ci-date = htparam.fdate.

RUN early-checkout.

PROCEDURE early-checkout: 
DEFINE VARIABLE i AS INTEGER INITIAL 0. 
DEFINE VARIABLE ci-datum AS DATE NO-UNDO. 
  ci-datum = ci-date - 1. 
  /*MTmess-str = translateExtended ("Early Checkout",lvCAREA,"") + " " + STRING(i). 
  DISP mess-str WITH FRAME frame1. */
  FIND FIRST res-line WHERE res-line.active-flag = 2 AND res-line.resstatus = 8 
    AND res-line.abreise = ci-datum 
    AND res-line.zipreis GT 0 AND res-line.erwachs GT 0 
    AND (res-line.ankunft + res-line.anztage) GT ci-datum NO-LOCK NO-ERROR. 
  DO WHILE AVAILABLE res-line: 
    DO TRANSACTION: 
      i = i + 1. 
      /*MTmess-str = translateExtended ("Early Checkout",lvCAREA,"") + " " + STRING(i). 
      DISP mess-str WITH FRAME frame1. */
      FIND FIRST zinrstat WHERE zinrstat.zinr = "Early-CO" 
        AND zinrstat.datum = ci-datum NO-ERROR. 
      IF NOT AVAILABLE zinrstat THEN 
      DO: 
        CREATE zinrstat. 
        ASSIGN 
          zinrstat.datum = ci-datum 
          zinrstat.zinr = "Early-CO". 
      END. 
      zinrstat.zimmeranz = zinrstat.zimmeranz + res-line.zimmeranz. 
      zinrstat.personen = zinrstat.personen + res-line.erwachs. 
    END. 
    FIND NEXT res-line WHERE res-line.active-flag = 2 AND res-line.resstatus = 8 
      AND res-line.abreise = ci-datum 
      AND res-line.zipreis GT 0 AND res-line.erwachs GT 0 
      AND (res-line.ankunft + res-line.anztage) GT ci-datum NO-LOCK NO-ERROR. 
  END. 
  /*MTPAUSE 0. */
END. 
