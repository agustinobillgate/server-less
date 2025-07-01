
DEF INPUT  PARAMETER rec-id       AS INTEGER.
DEF INPUT  PARAMETER user-init    AS CHAR.
DEF OUTPUT PARAMETER fl-error     AS INT INIT 0.

DEF VAR user-nr   AS INTEGER INITIAL 0 NO-UNDO.
DEF BUFFER ubuff FOR bediener.

FIND FIRST res-line WHERE RECID(res-line) = rec-id NO-LOCK NO-ERROR. /* Malik serverless 810 add if not available return  */
IF NOT AVAILABLE res-line THEN RETURN.
FIND FIRST outorder WHERE outorder.zinr = res-line.zinr 
    AND outorder.gespstart GE res-line.ankunft
    AND outorder.gespende LE res-line.ankunft NO-LOCK NO-ERROR.
IF NOT AVAILABLE outorder THEN
DO:
   fl-error = 1.
   RETURN NO-APPLY.
END.

DEF VAR oos-flag AS LOGICAL INITIAL NO NO-UNDO.
oos-flag = (outorder.betriebsnr = 3 OR outorder.betriebsnr = 4).
DO TRANSACTION:
    IF oos-flag AND (outorder.gespstart = outorder.gespende) THEN
    DO:
        FIND FIRST zinrstat WHERE zinrstat.zinr = "oos" 
           AND zinrstat.datum = outorder.gespende NO-ERROR. 
         IF NOT AVAILABLE zinrstat THEN 
         DO: 
           CREATE zinrstat. 
           ASSIGN 
             zinrstat.datum = outorder.gespende
             zinrstat.zinr = "oos". 
         END. 
         zinrstat.zimmeranz = zinrstat.zimmeranz + 1. 
     END. 
     FIND CURRENT outorder EXCLUSIVE-LOCK. 
     delete outorder. 
     RELEASE outorder.
     FIND FIRST ubuff WHERE ubuff.userinit = user-init NO-LOCK NO-ERROR.
     IF AVAILABLE ubuff THEN user-nr = ubuff.nr.
     FIND FIRST zimmer WHERE zimmer.zinr = res-line.zinr EXCLUSIVE-LOCK. 
     IF zimmer.zistatus = 6 THEN 
       ASSIGN
         zimmer.zistatus = 2
         zimmer.bediener-nr-stat = user-nr. 
     FIND CURRENT zimmer NO-LOCK. 
     fl-error = 2.
END.                       
