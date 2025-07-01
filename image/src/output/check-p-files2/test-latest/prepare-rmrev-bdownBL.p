

DEF OUTPUT PARAMETER new-contrate AS LOGICAL INIT NO.
DEF OUTPUT PARAMETER curr-date AS DATE.
DEF OUTPUT PARAMETER bill-date AS DATE.
DEF OUTPUT PARAMETER price-decimal AS INT.
DEF OUTPUT PARAMETER long-digit AS LOGICAL.
DEF OUTPUT PARAMETER foreign-rate AS LOGICAL.
DEF OUTPUT PARAMETER curr-local AS CHAR.
DEF OUTPUT PARAMETER curr-foreign AS CHAR.
DEF OUTPUT PARAMETER exchg-rate AS DECIMAL INIT 1.
DEF OUTPUT PARAMETER LnL-filepath AS CHAR INIT "\vhp\LnL\" NO-UNDO.
DEF OUTPUT PARAMETER LnL-prog AS CHAR INITIAL "rmrev-bdown.lst".

FIND FIRST htparam WHERE htparam.paramnr = 417 NO-LOCK. 
IF htparam.fchar NE "" THEN 
DO: 
    LnL-filepath = htparam.fchar. 
    IF SUBSTR(LnL-filepath, LENGTH(LnL-filepath), 1) NE "\" THEN 
        LnL-filepath = LnL-filepath + "\". 
    LnL-filepath = LnL-filepath + LnL-prog. 
END. 
 

FIND FIRST htparam WHERE htparam.paramnr = 550 NO-LOCK.
IF htparam.feldtyp = 4 THEN new-contrate = htparam.flogical.

FIND FIRST htparam WHERE paramnr = 110 no-lock.  /* Invoicing DATE */ 
ASSIGN
  curr-date = htparam.fdate
  bill-date = curr-date
.

FIND FIRST htparam WHERE htparam.paramnr = 491. 
price-decimal = htparam.finteger. 
 
FIND FIRST htparam WHERE htparam.paramnr = 246. 
long-digit = htparam.flogical. 
 
FIND FIRST htparam WHERE paramnr = 240 no-lock.  /* double currency */ 
foreign-rate = htparam.flogical. 
IF NOT foreign-rate THEN 
DO: 
  FIND FIRST htparam WHERE htparam.paramnr = 143 no-lock. /* rate IN foreign */ 
  foreign-rate = htparam.flogical. 
END. 
 
IF foreign-rate THEN 
DO: 
  FIND FIRST htparam WHERE paramnr = 152 NO-LOCK. 
  curr-local = fchar. 
  FIND FIRST htparam WHERE paramnr = 144 NO-LOCK. 
  curr-foreign = fchar. 
  FIND FIRST htparam WHERE htparam.paramnr = 144 NO-LOCK. 
  FIND FIRST waehrung WHERE waehrung.wabkurz = htparam.fchar NO-LOCK NO-ERROR. 
  IF AVAILABLE waehrung THEN exchg-rate = waehrung.ankauf / waehrung.einheit. 
  ELSE exchg-rate = 1. 
END. 

RUN update-resline.

PROCEDURE update-resline: 
DEFINE VARIABLE found      AS LOGICAL. 
DEFINE VARIABLE local-nr   AS INTEGER. 
DEFINE VARIABLE foreign-nr AS INTEGER.
DEFINE VARIABLE ct         AS CHAR.
DEFINE VARIABLE contcode   AS CHAR.
DEFINE BUFFER rline        FOR res-line. 
 
  FIND FIRST res-line WHERE res-line.active-flag = 1 
    AND (resstatus = 6 OR resstatus = 13) AND res-line.betriebsnr = 0 
    NO-LOCK NO-ERROR. 
  IF NOT AVAILABLE res-line THEN RETURN. 
 
  FIND FIRST htparam WHERE htparam.paramnr = 152 NO-LOCK. 
  FIND FIRST waehrung WHERE waehrung.wabkurz = htparam.fchar NO-LOCK. 
  local-nr = waehrung.waehrungsnr. 
  FIND FIRST htparam WHERE htparam.paramnr = 144 NO-LOCK. 
  FIND FIRST waehrung WHERE waehrung.wabkurz = htparam.fchar NO-LOCK NO-ERROR. 
  IF AVAILABLE waehrung THEN foreign-nr = waehrung.waehrungsnr. 
  
  FOR EACH res-line WHERE res-line.active-flag = 1 
    AND (resstatus = 6 OR resstatus = 13) AND res-line.betriebsnr = 0 NO-LOCK: 
    found = NO. 
    FIND FIRST rline WHERE rline.resnr = res-line.resnr 
      AND rline.reslinnr = res-line.reslinnr EXCLUSIVE-LOCK. 
    IF NOT res-line.adrflag THEN 
    DO: 
      FIND FIRST guest-pr WHERE guest-pr.gastnr = res-line.gastnr NO-LOCK 
        NO-ERROR. 
      IF AVAILABLE guest-pr THEN 
      DO:
        contcode = guest-pr.CODE.
        ct = res-line.zimmer-wunsch.
        IF ct MATCHES("*$CODE$*") THEN
        DO:
          ct = SUBSTR(ct,INDEX(ct,"$CODE$") + 6).
          contcode = SUBSTR(ct, 1, INDEX(ct,";") - 1).
        END.

        IF res-line.reserve-int NE 0 THEN  /* market segment */ 
        DO: 
          FIND FIRST queasy WHERE queasy.key = 18 AND queasy.number1 = 
            res-line.reserve-int NO-LOCK NO-ERROR. 
          IF NOT AVAILABLE queasy OR (AVAILABLE queasy AND queasy.char3 = "") 
            THEN FIND FIRST queasy WHERE queasy.key = 2 AND queasy.char1 
            = contcode NO-LOCK NO-ERROR. 
        END. 
        ELSE FIND FIRST queasy WHERE queasy.key = 2 AND queasy.char1 
          = contcode NO-LOCK NO-ERROR. 
        IF AVAILABLE queasy THEN 
        DO: 
          IF queasy.key = 18 THEN FIND FIRST waehrung WHERE waehrung.wabkurz 
            = queasy.char3 NO-LOCK NO-ERROR. 
          ELSE FIND FIRST waehrung WHERE waehrung.waehrungsnr = queasy.number1 
            NO-LOCK NO-ERROR. 
          IF AVAILABLE waehrung THEN 
          DO: 
            found = YES. 
            rline.betriebsnr = waehrung.waehrungsnr. 
          END. 
        END. 
      END. 
    END. 
    IF NOT found THEN 
    DO: 
      IF res-line.adrflag = YES OR NOT foreign-rate THEN 
        rline.betriebsnr = local-nr. 
      ELSE rline.betriebsnr = foreign-nr. 
    END. 
    FIND CURRENT rline NO-LOCK. 
  END. 
END. 

