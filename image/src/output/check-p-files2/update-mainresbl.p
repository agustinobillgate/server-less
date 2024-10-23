
DEF INPUT  PARAMETER pvILanguage AS INTEGER         NO-UNDO.
DEF INPUT  PARAMETER res-mode    AS CHAR            NO-UNDO.
DEF INPUT  PARAMETER user-init   AS CHAR            NO-UNDO.
DEF INPUT  PARAMETER mr-comment  AS CHAR            NO-UNDO.
DEF INPUT  PARAMETER letter      AS CHAR            NO-UNDO.
DEF INPUT  PARAMETER curr-segm   AS CHAR            NO-UNDO.
DEF INPUT  PARAMETER curr-source AS CHAR            NO-UNDO.
DEF INPUT  PARAMETER groupname   AS CHAR            NO-UNDO.
DEF INPUT  PARAMETER m-voucher   AS CHAR            NO-UNDO.
DEF INPUT  PARAMETER limitdate   AS DATE            NO-UNDO.
DEF INPUT  PARAMETER deposit     AS DECIMAL         NO-UNDO.
DEF INPUT  PARAMETER contact-nr  AS INTEGER         NO-UNDO.
DEF INPUT  PARAMETER cutoff-days AS INTEGER         NO-UNDO.
DEF INPUT  PARAMETER resNo       AS INTEGER         NO-UNDO.
DEF INPUT  PARAMETER gastNo      AS INTEGER         NO-UNDO.
DEF INPUT  PARAMETER l-grpnr     AS INTEGER         NO-UNDO.
DEF INPUT  PARAMETER fixrateFLag AS LOGICAL         NO-UNDO.
DEF OUTPUT PARAMETER msg-str     AS CHAR INIT ""    NO-UNDO.

{supertransBL.i} 
DEF VAR lvCAREA AS CHAR INITIAL "mk-resline". 

RUN update-mainres.

PROCEDURE update-mainres:
DEFINE VARIABLE ct     AS CHAR                  NO-UNDO. 
DEFINE VARIABLE answer AS LOGICAL INITIAL YES   NO-UNDO.
DEFINE BUFFER rline    FOR res-line. 
DEFINE BUFFER rgast    FOR guest.
    
/* must be here */  
  FIND FIRST reservation WHERE reservation.resnr = resNo EXCLUSIVE-LOCK.  
  FIND FIRST rgast WHERE rgast.gastnr = gastNo NO-LOCK.

  FIND FIRST master WHERE master.resnr = resNo NO-LOCK NO-ERROR. 
  IF AVAILABLE master AND master.active THEN reservation.verstat = 1. 
  ELSE reservation.verstat = 0. 
  IF res-mode = "new" THEN reservation.useridanlage = user-init. 
  ASSIGN reservation.bemerk = mr-comment.
 
  ct = letter.
  FIND FIRST brief WHERE brief.briefkateg = l-grpnr 
    AND brief.briefnr = INTEGER(SUBSTR(ct, 1, INDEX(ct," "))) NO-LOCK NO-ERROR. 
  IF AVAILABLE brief THEN reservation.briefnr = brief.briefnr. 
  ELSE reservation.briefnr = 0.

  ct = curr-segm.
  FIND FIRST segment WHERE segment.segmentcode =
      INTEGER(SUBSTR(ct, 1, INDEX(ct," "))) NO-LOCK NO-ERROR.
  IF AVAILABLE segment THEN reservation.segmentcode = segment.segmentcode.
  
  ct = curr-source.
  FIND FIRST sourccod WHERE sourccod.source-code =
      INTEGER(SUBSTR(ct, 1, INDEX(ct," "))) NO-LOCK NO-ERROR.
  IF AVAILABLE sourccod THEN reservation.resart = sourccod.source-code. 

  ASSIGN 
      reservation.groupname   = groupname 
      reservation.grpflag     = (groupname NE "") 
      reservation.limitdate   = limitdate 
      reservation.depositgef  = deposit 
      reservation.vesrdepot   = m-voucher 
      reservation.kontakt-nr  = contact-nr
      reservation.point-resnr = cutoff-days
  . 
  IF (reservation.insurance AND NOT fixrateFlag) 
    OR (NOT reservation.insurance AND fixrateFlag) THEN
  DO:
    ASSIGN reservation.insurance = fixrateFlag.
    RUN resline-reserve-dec. 
  END.

/* moved to update-reslineBL 
  IF reservation.grpflag THEN 
  DO: 
    FIND FIRST rline WHERE rline.resnr = reservation.resnr 
      NO-LOCK NO-ERROR. 
    DO WHILE AVAILABLE rline: 
      FIND CURRENT rline EXCLUSIVE-LOCK. 
      rline.grpflag = YES. 
      FIND CURRENT rline NO-LOCK. 
      FIND NEXT rline WHERE rline.resnr = reservation.resnr 
        NO-LOCK NO-ERROR. 
    END. 
  END. 
*/
  
  IF AVAILABLE master THEN 
  DO: 
    FIND CURRENT master EXCLUSIVE-LOCK. 
    IF NOT master.active THEN 
    DO: 
      FIND FIRST bill WHERE bill.resnr = resNo AND bill.reslinnr = 0 
        NO-LOCK NO-ERROR. 
      IF AVAILABLE bill AND bill.saldo NE 0 THEN master.active = YES. 
    END.  
    FIND CURRENT master NO-LOCK. 
    IF master.active THEN reservation.verstat = 1. 
    ELSE reservation.verstat = 0. 
 
/* create master bill only IF resident guest exists !! ******/ 
    FIND FIRST rline WHERE rline.resnr = master.resnr 
      AND rline.active-flag = 1 NO-LOCK NO-ERROR. 
    IF AVAILABLE rline THEN 
    DO: 
      FIND FIRST bill WHERE bill.resnr = resNo AND bill.reslinnr = 0 
        EXCLUSIVE-LOCK NO-ERROR. 
      IF NOT AVAILABLE bill THEN 
      DO: 
        CREATE bill. 
        ASSIGN
          bill.resnr    = resNo 
          bill.reslinnr = 0 
          bill.rgdruck  = 1 
          bill.billtyp  = 2
        . 
        IF master.rechnr NE 0 THEN bill.rechnr = master.rechnr. 
        ELSE 
        DO: 
          FIND FIRST counters WHERE counters.counter-no = 3 EXCLUSIVE-LOCK. 
          counters.counter = counters.counter + 1. 
          bill.rechnr = counters.counter. 
          FIND CURRENT counter NO-LOCK. 
          FIND CURRENT master EXCLUSIVE-LOCK. 
          master.rechnr = bill.rechnr. 
          FIND CURRENT master NO-LOCK. 
        END. 
      END.
      ASSIGN
        bill.gastnr      = gastNo 
        bill.name        = rgast.NAME 
        bill.segmentcode = reservation.segmentcode
      . 
      FIND CURRENT bill NO-LOCK. 
    END. 
  END.   

  IF NOT AVAILABLE master AND (rgast.karteityp = 1 OR rgast.karteityp = 2) THEN 
  DO: 
    FIND FIRST htparam WHERE paramnr = 166 NO-LOCK. 
    IF htparam.flogical THEN 
      msg-str = "&Q" + translateExtended ("Master Bill does not exist, CREATE IT?",lvCAREA,""). 
  END. 

  FIND CURRENT reservation NO-LOCK.
END. 

PROCEDURE resline-reserve-dec: 
DEFINE VARIABLE exchg-rate AS DECIMAL INITIAL 0. 
DEFINE BUFFER rline FOR res-line.
  IF NOT reservation.insurance THEN 
  DO: 
    FOR EACH rline WHERE rline.resnr = reservation.resnr 
      AND (rline.resstatus = 6 OR rline.resstatus = 13) 
      AND rline.reserve-dec NE 0: 
      rline.reserve-dec = 0. 
    END. 
    RETURN. 
  END.  
  FIND FIRST htparam WHERE htparam.paramnr = 144 NO-LOCK. 
  FIND FIRST waehrung WHERE waehrung.wabkurz = htparam.fchar NO-LOCK NO-ERROR. 
  IF AVAILABLE waehrung THEN exchg-rate = waehrung.ankauf / waehrung.einheit. 
  IF exchg-rate NE 0 THEN 
  FOR EACH rline WHERE rline.resnr = reservation.resnr 
    AND (rline.resstatus = 6 OR rline.resstatus = 13) 
    AND rline.reserve-dec = 0: 
    rline.reserve-dec = exchg-rate. 
  END. 
END. 
