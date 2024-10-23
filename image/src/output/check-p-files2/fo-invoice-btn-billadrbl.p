
DEFINE INPUT  PARAMETER gastpay        AS INT.
DEFINE INPUT  PARAMETER bil-recid      AS INT.
DEFINE INPUT  PARAMETER user-init      AS CHAR NO-UNDO.  /*sis 161214*/
DEFINE OUTPUT PARAMETER art-no         AS INT  NO-UNDO INIT 0.
DEFINE OUTPUT PARAMETER resname        AS CHAR.
DEFINE OUTPUT PARAMETER rescomment     AS CHAR NO-UNDO.
DEFINE OUTPUT PARAMETER r-gastnrpay    AS INT.
DEFINE OUTPUT PARAMETER bill-gastnr    AS INT.
DEFINE OUTPUT PARAMETER bill-name      AS CHAR.

DEFINE VARIABLE g-address   AS CHARACTER NO-UNDO.
DEFINE VARIABLE g-wonhort   AS CHARACTER NO-UNDO.
DEFINE VARIABLE g-plz       AS CHARACTER NO-UNDO.
DEFINE VARIABLE g-land      AS CHARACTER NO-UNDO.

/*sis 161214*/
DEFINE VARIABLE curr-gastnr AS INTEGER NO-UNDO.
DEFINE BUFFER gbuff FOR guest.

FIND FIRST bediener WHERE bediener.userinit = user-init NO-LOCK.
/*end sis*/

FIND FIRST bill WHERE RECID(bill) = bil-recid EXCLUSIVE-LOCK.
FIND FIRST guest WHERE guest.gastnr = gastpay NO-LOCK. 

/*FD Oct 06, 2022 => Ticket 559E7C - Bill Address Empty Cause Value=?*/
ASSIGN
    g-address   = guest.adresse1
    g-wonhort   = guest.wohnort
    g-plz       = guest.plz
    g-land      = guest.land
    .
IF g-address EQ ? THEN g-address = "".
IF g-wonhort EQ ? THEN g-wonhort = "".
IF g-plz EQ ? THEN g-plz = "".
IF g-land EQ ? THEN g-land = "".

ASSIGN    
    curr-gastnr = bill.gastnr
    art-no      = guest.zahlungsart
    bill.gastnr = guest.gastnr 
    bill.name   = guest.NAME 
    bill-gastnr = bill.gastnr
    bill-name   = bill.NAME    
    r-gastnrpay = guest.gastnr
    resname     = guest.name + ", " + guest.vorname1 + guest.anredefirma 
                + " " + guest.anrede1 
                + chr(10) + g-address 
                + chr(10) + g-wonhort + " " + g-plz 
                + chr(10) + g-land
    .

IF bill.resnr GT 0 AND bill.reslinnr GT 0 THEN
DO:
    FIND FIRST res-line WHERE res-line.resnr = bill.resnr 
      AND res-line.reslinnr = bill.reslinnr EXCLUSIVE-LOCK NO-ERROR. 
    IF AVAILABLE res-line THEN
    DO:
      res-line.gastnrpay = guest.gastnr.
      FIND CURRENT res-line NO-LOCK.
  END.
END.

RUN fill-rescomment(NO). 

IF curr-gastnr NE gastpay THEN
DO:
    FIND FIRST gbuff WHERE gbuff.gastnr = curr-gastnr NO-LOCK. 
    CREATE res-history. 
    ASSIGN 
        res-history.nr          = bediener.nr 
        res-history.betriebsnr  = bediener.nr 
        res-history.resnr       = bill.resnr 
        res-history.reslinnr    = bill.reslinnr 
        res-history.datum       = TODAY 
        res-history.zeit        = TIME 
        res-history.action      = "Bill Receiver Changed" 
        res-history.aenderung = gbuff.NAME + CHR(10) + CHR(10)
            + "*** Changed to:" + CHR(10) + CHR(10) 
            + guest.NAME + CHR(10) + CHR(10) 
            + "*** Bill No: " + STRING(bill.rechnr). 
    FIND CURRENT res-history NO-LOCK.
    RELEASE res-history. 
END.

PROCEDURE fill-rescomment: 
DEFINE INPUT PARAMETER fill-co AS LOGICAL. 
DEFINE BUFFER guestmember   FOR guest. 
DEFINE BUFFER usr           FOR bediener. 
DEFINE BUFFER resbuff       FOR res-line.
DEFINE BUFFER rbuff         FOR res-line.

  FIND FIRST reservation WHERE reservation.resnr = bill.resnr NO-LOCK NO-ERROR. 
  
  IF AVAILABLE res-line THEN 
  FIND FIRST guestmember WHERE guestmember.gastnr = res-line.gastnrmember NO-LOCK. 
 
  IF bill.reslinnr GT 0 THEN
  FIND FIRST resbuff WHERE resbuff.resnr = bill.resnr 
    AND resbuff.reslinnr = bill.parent-nr NO-LOCK NO-ERROR. 

  ASSIGN rescomment = "". 
 
  IF fill-co THEN 
  DO: 
    FIND FIRST usr WHERE usr.userinit = bill.vesrcod NO-LOCK NO-ERROR. 
    IF AVAILABLE usr THEN 
        rescomment = rescomment + "C/O by: " + usr.username + CHR(10). 
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
    IF AVAILABLE queasy THEN rescomment = rescomment + queasy.char1 + CHR(10). 
  END. 
 
  IF AVAILABLE res-line AND res-line.bemerk NE "" THEN 
    rescomment = rescomment + res-line.bemerk. 
  IF AVAILABLE reservation AND reservation.bemerk NE "" THEN 
    rescomment = rescomment + reservation.bemerk + CHR(10). 
  IF AVAILABLE guestmember AND guestmember.bemerk NE "" THEN 
    rescomment = rescomment + guestmember.bemerk + CHR(10). 
 
  IF AVAILABLE res-line THEN
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
 
END. 


