DEF INPUT PARAMETER  inp-gastnr     AS INTEGER          NO-UNDO.
DEF OUTPUT PARAMETER error-code     AS INTEGER INIT 0   NO-UNDO.
DEF OUTPUT PARAMETER blacklist-code AS CHAR    INIT ""  NO-UNDO.
DEF OUTPUT PARAMETER block-rsv      AS LOGICAL INIT NO  NO-UNDO.
DEF OUTPUT PARAMETER pswd-str       AS CHAR    INIT ""  NO-UNDO.
DEF OUTPUT PARAMETER cr-limit       AS DECIMAL INIT 0   NO-UNDO.
DEF OUTPUT PARAMETER outstand       AS DECIMAL INIT 0   NO-UNDO. 

DEF VARIABLE ratecode-exist AS LOGICAL NO-UNDO INIT NO.
DEF VARIABLE bill-date      AS DATE NO-UNDO.
RUN htpdate.p(110, OUTPUT bill-date).

FIND FIRST guest WHERE guest.gastnr = inp-gastnr NO-LOCK.
ASSIGN cr-limit = guest.kreditlimit.

/* check guest total outstanding */
IF guest.karteityp GE 1 AND guest.zahlungsart > 0 THEN 
FOR EACH debitor WHERE debitor.gastnr = guest.gastnr 
  AND debitor.opart LE 1 NO-LOCK, 
  FIRST artikel WHERE artikel.artnr = debitor.artnr 
  AND artikel.departement = 0 
  AND (artikel.artart = 2 OR artikel.artart = 7) NO-LOCK: 
  outstand = outstand + debitor.saldo. 
END. 

/* check if the guest is under black list */ 
FOR EACH guestseg WHERE guestseg.gastnr = inp-gastnr NO-LOCK,
    FIRST segment WHERE segment.segmentcode = guestseg.segmentcode
    AND segment.betriebsnr = 4 NO-LOCK:  
    ASSIGN
      error-code     = 1
      blacklist-code = ENTRY(1, segment.bezeich, "$$0")
    .
    LEAVE.
END.

IF outstand GT guest.kreditlimit AND guest.kreditlimit GT 0 THEN 
    error-code = error-code + 2.

/* block reservation flag */
FIND FIRST htparam WHERE paramnr = 320 NO-LOCK. 
ASSIGN block-rsv = htparam.flogical.

/* pswd to allow rsv if black list or limit overdrawn */
FIND FIRST htparam WHERE paramnr = 141 NO-LOCK. 
ASSIGN pswd-str  = htparam.fchar. 
