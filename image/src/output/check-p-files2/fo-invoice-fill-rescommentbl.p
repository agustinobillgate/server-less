
DEF INPUT  PARAMETER bil-recid AS INT.
DEF INPUT  PARAMETER fill-co AS LOGICAL.
DEF OUTPUT PARAMETER rescomment AS CHAR.

DEFINE BUFFER usr              FOR bediener. 
DEFINE BUFFER resbuff          FOR res-line.
DEFINE BUFFER rbuff            FOR res-line.
DEFINE BUFFER guestmember      FOR guest. 

FIND FIRST bill WHERE RECID(bill) = bil-recid NO-LOCK.
FIND FIRST res-line WHERE res-line.resnr = bill.resnr 
    AND res-line.reslinnr = bill.reslinnr NO-LOCK NO-ERROR. 
FIND FIRST reservation WHERE reservation.resnr = bill.resnr NO-LOCK NO-ERROR. 
  
IF AVAILABLE res-line THEN 
FIND FIRST guestmember WHERE guestmember.gastnr = res-line.gastnrmember NO-LOCK.
 
FIND FIRST resbuff WHERE resbuff.resnr = bill.resnr 
    AND resbuff.reslinnr = bill.parent-nr NO-LOCK NO-ERROR. 

rescomment = "".

IF fill-co THEN 
DO: 
    FIND FIRST usr WHERE usr.userinit = bill.vesrcod NO-LOCK NO-ERROR. 
    IF AVAILABLE usr THEN 
        rescomment = rescomment + "C/O by: " + usr.username + chr(10). 
END. 

IF AVAILABLE resbuff AND 
      TRIM(ENTRY(1, resbuff.memozinr, ";")) NE "" THEN 
DO: 
    FIND FIRST rbuff WHERE rbuff.zinr = TRIM(ENTRY(1, resbuff.memozinr, ";"))
      AND rbuff.resstatus = 6 NO-LOCK NO-ERROR.
    IF AVAILABLE rbuff THEN
    rescomment = rescomment + "Transf " + 
      resbuff.zinr + " -> " + ENTRY(1, resbuff.memozinr, ";") 
      + " " + rbuff.NAME  + CHR(10). 
    ELSE
    rescomment = rescomment + "Transf " + 
      resbuff.zinr + " -> " + ENTRY(1, resbuff.memozinr, ";") + CHR(10). 
END. 

IF AVAILABLE resbuff AND resbuff.code NE "" THEN 
DO: 
    FIND FIRST queasy WHERE queasy.key = 9 
      AND queasy.number1 = INTEGER(res-line.code) NO-LOCK NO-ERROR. 
    IF AVAILABLE queasy THEN rescomment = rescomment + queasy.char1 + chr(10). 
END. 

IF bill.vesrdepot NE "" THEN
    rescomment = rescomment + bill.vesrdepot + CHR(10).

IF AVAILABLE res-line AND res-line.bemerk NE "" THEN 
    rescomment = rescomment + res-line.bemerk + chr(10).
IF AVAILABLE reservation AND reservation.bemerk NE "" THEN 
    rescomment = rescomment + reservation.bemerk + chr(10). 
IF AVAILABLE guestmember AND guestmember.bemerk NE "" THEN 
    rescomment = rescomment + guestmember.bemerk + chr(10). 


FIND FIRST waehrung WHERE waehrung.waehrungsnr = res-line.betriebsnr NO-LOCK 
      NO-ERROR. 
IF AVAILABLE resbuff THEN
rescomment = rescomment + "Arr " + STRING(resbuff.ankunft) 
    + " Dep " + STRING(resbuff.abreise) + " A " + STRING(resbuff.erwachs) 
    + " Ch " + STRING(resbuff.kind1) + " Ch " + STRING(resbuff.kind2) 
    + " Com " + STRING(resbuff.gratis) + CHR(10) 
    + "Argt " + resbuff.arrangement. 
IF AVAILABLE waehrung THEN 
      rescomment = rescomment + ">>Currency " + waehrung.wabkurz + CHR(10). 
ELSE rescomment = rescomment + CHR(10). 
