
DEF TEMP-TABLE t-bill LIKE bill.
DEF TEMP-TABLE t-res-line LIKE res-line
    FIELD guest-name AS CHAR            /*ragung penambahan guest name req Web*/
    .

DEF INPUT  PARAMETER bil-flag       AS INTEGER.
DEF INPUT  PARAMETER bil-recid      AS INT.
DEF INPUT  PARAMETER room           AS CHAR.
DEF INPUT  PARAMETER vipflag        AS LOGICAL.
DEF OUTPUT PARAMETER abreise        AS DATE.
DEF OUTPUT PARAMETER resname        AS CHAR.
DEF OUTPUT PARAMETER res-exrate     AS DECIMAL.
DEF OUTPUT PARAMETER zimmer-bezeich AS CHAR.
DEF OUTPUT PARAMETER kreditlimit    AS DECIMAL.
DEF OUTPUT PARAMETER master-str     AS CHAR.
DEF OUTPUT PARAMETER master-rechnr  AS CHAR.
DEF OUTPUT PARAMETER bill-anzahl    AS INT.
DEF OUTPUT PARAMETER queasy-char1   AS CHAR.
DEF OUTPUT PARAMETER disp-warning   AS LOGICAL INIT NO.
DEF OUTPUT PARAMETER flag-report    AS LOGICAL INIT NO.
DEF OUTPUT PARAMETER TABLE FOR t-res-line.
DEF OUTPUT PARAMETER TABLE FOR t-bill.

DEFINE BUFFER resbuff       FOR res-line.
DEFINE BUFFER guestmember   FOR guest. 
DEFINE BUFFER mbill FOR bill.
DEFINE BUFFER bill1 FOR bill. 

DEFINE VARIABLE vipnr1 AS INTEGER INITIAL 99999. 
DEFINE VARIABLE vipnr2 AS INTEGER INITIAL 99999. 
DEFINE VARIABLE vipnr3 AS INTEGER INITIAL 99999. 
DEFINE VARIABLE vipnr4 AS INTEGER INITIAL 99999. 
DEFINE VARIABLE vipnr5 AS INTEGER INITIAL 99999. 
DEFINE VARIABLE vipnr6 AS INTEGER INITIAL 99999. 
DEFINE VARIABLE vipnr7 AS INTEGER INITIAL 99999. 
DEFINE VARIABLE vipnr8 AS INTEGER INITIAL 99999. 
DEFINE VARIABLE vipnr9 AS INTEGER INITIAL 99999. 

DEFINE VARIABLE ci-date     AS DATE NO-UNDO.

DEFINE VARIABLE g-address   AS CHARACTER NO-UNDO.
DEFINE VARIABLE g-wonhort   AS CHARACTER NO-UNDO.
DEFINE VARIABLE g-plz       AS CHARACTER NO-UNDO.
DEFINE VARIABLE g-land      AS CHARACTER NO-UNDO.

FIND FIRST htparam WHERE paramnr = 87 NO-LOCK.
/* ci-date  = fdate. */       /* Rulita 181024 | Fixing for serverless */
ci-date  = htparam.fdate.

FIND FIRST bill WHERE RECID(bill) = bil-recid  NO-LOCK.   
FIND FIRST res-line WHERE res-line.resnr = bill.resnr 
    AND res-line.reslinnr = bill.reslinnr NO-LOCK NO-ERROR. 

IF AVAILABLE res-line THEN
DO:
    CREATE t-res-line.
    BUFFER-COPY res-line TO t-res-line.
    FIND FIRST guestmember WHERE guestmember.gastnr = res-line.gastnrmember NO-LOCK NO-ERROR.
    IF AVAILABLE guestmember THEN t-res-line.guest-name = guestmember.anrede1 + " " + guestmember.name + ", " + guestmember.vorname1.
END.
CREATE t-bill.
BUFFER-COPY bill TO t-bill.

FIND FIRST resbuff WHERE resbuff.resnr = bill.resnr 
    AND resbuff.reslinnr = bill.parent-nr NO-LOCK NO-ERROR. 
IF AVAILABLE resbuff THEN abreise = resbuff.abreise. 
ELSE abreise = bill.datum.


IF AVAILABLE res-line AND bil-flag = 0 AND res-line.abreise = ci-date THEN
DO:
    FIND FIRST reslin-queasy WHERE reslin-queasy.key = "flag" 
      AND reslin-queasy.resnr = res-line.resnr 
      AND reslin-queasy.reslinnr = res-line.reslinnr 
      AND reslin-queasy.betriebsnr = 0 
      AND (reslin-queasy.logi1 = YES OR reslin-queasy.logi2 = YES 
      OR reslin-queasy.logi3 = YES) NO-LOCK NO-ERROR.
    IF AVAILABLE reslin-queasy THEN flag-report = YES.
        /*RUN flag-report.p(res-line.resnr, 
      res-line.reslinnr, NO, OUTPUT dummy-logi, YES). */
END.
FIND FIRST reservation WHERE reservation.resnr = bill.resnr NO-LOCK NO-ERROR. 

resname = "".
FIND FIRST guest WHERE guest.gastnr = bill.gastnr NO-LOCK. 

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

resname = guest.name + ", " + guest.vorname1 + guest.anredefirma 
    + " " + guest.anrede1 
    + chr(10) + g-address 
    + chr(10) + g-wonhort + " " + g-plz 
    + chr(10) + g-land. 

IF guest.kreditlimit NE 0 THEN kreditlimit = guest.kreditlimit. 
ELSE 
DO: 
    FIND FIRST htparam WHERE paramnr = 68 NO-LOCK. 
    IF htparam.fdecimal NE 0 THEN kreditlimit = htparam.fdecimal. 
    ELSE kreditlimit = htparam.finteger. 
END. 

FIND FIRST zimmer WHERE zimmer.zinr = bill.zinr NO-LOCK.
zimmer-bezeich = zimmer.bezeich.

res-exrate = 1. 
IF AVAILABLE res-line THEN 
DO: 
    IF res-line.reserve-dec NE 0 THEN res-exrate = res-line.reserve-dec. 
    ELSE 
    DO: 
      FIND FIRST waehrung WHERE waehrung.waehrungsnr = res-line.betriebsnr 
        NO-LOCK NO-ERROR. 
      IF AVAILABLE waehrung THEN res-exrate = waehrung.ankauf / waehrung.einheit. 
    END. 
END. 


FIND FIRST htparam WHERE paramnr = 700 NO-LOCK. 
IF htparam.finteger NE 0 THEN vipnr1 = htparam.finteger.               /* Rulita 211024 | Fixing for serverless */  
FIND FIRST htparam WHERE paramnr = 701 NO-LOCK. 
IF htparam.finteger NE 0 THEN vipnr2 = htparam.finteger.               /* Rulita 211024 | Fixing for serverless */  
FIND FIRST htparam WHERE paramnr = 702 NO-LOCK. 
IF htparam.finteger NE 0 THEN vipnr3 = htparam.finteger.               /* Rulita 211024 | Fixing for serverless */  
FIND FIRST htparam WHERE paramnr = 703 NO-LOCK. 
IF htparam.finteger NE 0 THEN vipnr4 = htparam.finteger.               /* Rulita 211024 | Fixing for serverless */  
FIND FIRST htparam WHERE paramnr = 704 NO-LOCK. 
IF htparam.finteger NE 0 THEN vipnr5 = htparam.finteger.               /* Rulita 211024 | Fixing for serverless */  
FIND FIRST htparam WHERE paramnr = 705 NO-LOCK. 
IF htparam.finteger NE 0 THEN vipnr6 = htparam.finteger.               /* Rulita 211024 | Fixing for serverless */  
FIND FIRST htparam WHERE paramnr = 706 NO-LOCK. 
IF htparam.finteger NE 0 THEN vipnr7 = htparam.finteger.               /* Rulita 211024 | Fixing for serverless */  
FIND FIRST htparam WHERE paramnr = 707 NO-LOCK. 
IF htparam.finteger NE 0 THEN vipnr8 = htparam.finteger.               /* Rulita 211024 | Fixing for serverless */  
FIND FIRST htparam WHERE paramnr = 708 NO-LOCK. 
IF htparam.finteger NE 0 THEN vipnr9 = htparam.finteger.               /* Rulita 211024 | Fixing for serverless */  

RUN check-vip(bill.gastnr).
IF NOT vipflag AND AVAILABLE guestmember THEN RUN check-vip(guestmember.gastnr).

master-str = "". 
master-rechnr = "". 
FIND FIRST master WHERE master.resnr = bill.resnr NO-LOCK NO-ERROR. 
IF AVAILABLE master /* AND master.active */ THEN 
DO: 
    FIND FIRST mbill WHERE mbill.resnr = bill.resnr AND 
      mbill.reslinnr = 0 AND mbill.zinr = "" NO-LOCK NO-ERROR. 
    IF NOT AVAILABLE mbill THEN 
    DO: 
      FIND FIRST counters WHERE counters.counter-no = 3 EXCLUSIVE-LOCK. 
      counters.counter = counters.counter + 1. 
      FIND CURRENT counter NO-LOCK. 
      create mbill. 
      mbill.rechnr = counters.counter. 
      FIND CURRENT mbill NO-LOCK. 
      FIND CURRENT master EXCLUSIVE-LOCK. 
      master.rechnr = mbill.rechnr. 
      FIND CURRENT master NO-LOCK. 
    END. 
    IF AVAILABLE mbill THEN 
    DO: 
      master-str = "Master Bill". 
      master-rechnr = STRING(mbill.rechnr) + " - " + mbill.NAME. 
    END. 
END. 
DO: 
    bill-anzahl = 0. 
    IF bill.flag = 0 THEN 
    FOR EACH bill1 WHERE bill1.resnr = bill.resnr 
        AND bill1.parent-nr = bill.parent-nr 
        AND bill1.parent-nr NE 0 
        AND bill1.flag = 0 AND bill1.zinr = bill.zinr NO-LOCK: 
      bill-anzahl = bill-anzahl + 1. 
    END.
END. 

IF AVAILABLE res-line AND res-line.code NE "" AND bill.flag = 0 THEN 
DO: 
    FIND FIRST queasy WHERE queasy.key = 9 
      AND queasy.number1 = INTEGER(res-line.code) NO-LOCK NO-ERROR. 
    IF AVAILABLE queasy AND queasy.logi1 THEN 
    DO: 
        disp-warning = YES.
        queasy-char1 = queasy.char1.
    END. 
END.

PROCEDURE check-vip: 
DEFINE INPUT PARAMETER gastnr AS INTEGER. 
  FIND FIRST guestseg WHERE guestseg.gastnr = gastnr NO-LOCK NO-ERROR. 
  DO WHILE AVAILABLE guestseg AND NOT vipflag: 
    IF (guestseg.segmentcode = vipnr1 OR 
      guestseg.segmentcode = vipnr2 OR 
      guestseg.segmentcode = vipnr3 OR 
      guestseg.segmentcode = vipnr4 OR 
      guestseg.segmentcode = vipnr5 OR 
      guestseg.segmentcode = vipnr6 OR 
      guestseg.segmentcode = vipnr7 OR 
      guestseg.segmentcode = vipnr8 OR 
      guestseg.segmentcode = vipnr9) THEN vipflag = YES. 
    FIND NEXT guestseg WHERE guestseg.gastnr = gastnr NO-LOCK NO-ERROR. 
  END.
END. 
