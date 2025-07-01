 
 
DEF INPUT PARAMETER pvILanguage     AS INTEGER              NO-UNDO.
DEF INPUT PARAMETER resnr           AS INTEGER. 
DEF INPUT PARAMETER reslinnr        AS INTEGER. 
DEF INPUT PARAMETER gastnr          AS INTEGER. 
DEF INPUT PARAMETER datum           AS DATE. 
DEF INPUT PARAMETER marknr          AS INTEGER. 
DEF INPUT PARAMETER zikatnr         AS INTEGER. 
DEF INPUT PARAMETER argt            AS CHAR. 
DEF INPUT PARAMETER qty             AS INTEGER. 
DEF INPUT PARAMETER rate            AS DECIMAL. 

DEF OUTPUT PARAMETER still-error    AS LOGICAL INITIAL NO. 
DEF OUTPUT PARAMETER comp-room      AS INTEGER INITIAL 0    NO-UNDO. 
DEF OUTPUT PARAMETER max-room       AS INTEGER INITIAL 0    NO-UNDO. 
DEF OUTPUT PARAMETER pswd-str       AS CHAR    INITIAL ""   NO-UNDO.
DEF OUTPUT PARAMETER msg-str        AS CHAR INITIAL ""      NO-UNDO.

DEF VAR s-recid                     AS INTEGER NO-UNDO.
DEF VAR book-room                   AS INTEGER NO-UNDO. 
 
DEF VAR pay-rm                      AS INTEGER INITIAL 0    NO-UNDO. 
DEF VAR curr-rm                     AS INTEGER              NO-UNDO. 
DEF VAR max-comp                    AS INTEGER INITIAL 0    NO-UNDO. 
DEF VAR com-rm                      AS INTEGER INITIAL 0    NO-UNDO. 
DEF VAR passwd-ok                   AS LOGICAL INITIAL NO   NO-UNDO. 
DEF VAR new-contrate                AS LOGICAL INITIAL NO. 
 
DEF VAR ct                          AS CHAR    NO-UNDO.
DEF VAR contcode                    AS CHAR    NO-UNDO.

DEF BUFFER resline FOR res-line. 
 
{supertransBL.i} 
DEF VAR lvCAREA AS CHAR INITIAL "check-compliment". 

FIND FIRST arrangement WHERE arrangement.arrangement = argt 
  NO-LOCK NO-ERROR. 
IF NOT AVAILABLE arrangement THEN RETURN. 
 
FIND FIRST guest-pr WHERE guest-pr.gastnr = gastnr NO-LOCK NO-ERROR. 
IF NOT AVAILABLE guest-pr THEN RETURN. 

contcode = guest-pr.CODE.
FIND FIRST res-line WHERE res-line.resnr = resnr
    AND res-line.reslinnr = reslinnr NO-LOCK.
ct = res-line.zimmer-wunsch.
IF ct MATCHES("*$CODE$*") THEN
DO:
  ct = SUBSTR(ct,INDEX(ct,"$CODE$") + 6).
  contcode = SUBSTR(ct, 1, INDEX(ct,";") - 1).
END.

FIND FIRST reslin-queasy WHERE reslin-queasy.key = "arrangement" 
  AND reslin-queasy.resnr = resnr AND reslin-queasy.reslinnr = reslinnr 
  AND datum GE reslin-queasy.date1 AND datum LE reslin-queasy.date2 
  NO-LOCK NO-ERROR. 
IF AVAILABLE reslin-queasy THEN RETURN. 
 
IF rate = 0 THEN com-rm = qty. /* in case of option INSERT */
ELSE pay-rm = qty.  
FOR EACH resline WHERE resline.resnr = resnr 
  AND resline.active-flag LE 1 AND resline.resstatus LE 6 
  AND resline.reslinnr NE reslinnr NO-LOCK: 
  IF resline.zipreis = 0 THEN com-rm = com-rm + resline.zimmeranz. 
  ELSE pay-rm = pay-rm + resline.zimmeranz. 
END.  
IF com-rm = 0 THEN RETURN. 

FIND FIRST htparam WHERE htparam.paramnr = 550 NO-LOCK.
IF htparam.feldtyp = 4 THEN new-contrate = htparam.flogical.

IF new-contrate THEN
DO:
  RUN ratecode-seek.p(resnr, reslinnr, contcode, datum, OUTPUT s-recid).
  IF s-recid = 0 THEN RETURN.
  FIND FIRST ratecode WHERE RECID(ratecode) = s-recid NO-LOCK NO-ERROR.
  IF NOT AVAILABLE ratecode THEN RETURN.
  IF NUM-ENTRIES(ratecode.char1[4], ";") LT 3 THEN RETURN.  
  book-room = INTEGER(ENTRY(1, ratecode.char1[4], ";")). 
  comp-room = INTEGER(ENTRY(2, ratecode.char1[4], ";")). 
  max-room  = INTEGER(ENTRY(3, ratecode.char1[4], ";")). 
END.
ELSE
DO:
  FIND FIRST pricecod WHERE pricecod.code = contcode 
    AND pricecod.marknr = marknr AND pricecod.argtnr = arrangement.argtnr 
    AND pricecod.zikatnr = zikatnr AND datum GE pricecod.startperiode 
    AND datum LE pricecod.endperiode NO-LOCK NO-ERROR. 
  IF NOT AVAILABLE pricecod THEN RETURN. 
  IF NUM-ENTRIES(pricecod.bezeichnung, ";") LT 3 THEN RETURN.  
  book-room = INTEGER(ENTRY(1, pricecod.bezeichnung, ";")). 
  comp-room = INTEGER(ENTRY(2, pricecod.bezeichnung, ";")). 
  max-room  = INTEGER(ENTRY(3, pricecod.bezeichnung, ";")). 
END.

curr-rm = pay-rm. 
IF curr-rm GT max-room THEN curr-rm = max-room. 
max-comp = ROUND(curr-rm / book-room - 0.5, 0) * comp-room. 
IF max-comp LT 0 THEN max-comp = 0. 
 
IF com-rm LE max-comp THEN RETURN. 
 
msg-str = translateExtended ("Wrong total number of compliment rooms:",lvCAREA,"") 
  + CHR(10)
  + translateExtended ("Max allowed =",lvCAREA,"") + " " + STRING(max-comp) 
  + CHR(10) 
  + translateExtended ("Actual compliment rooms =",lvCAREA,"") + " " 
  + STRING(com-rm) + CHR(2). 
 
RUN htpchar.p (141, OUTPUT pswd-str).
still-error = (pswd-str = "").
