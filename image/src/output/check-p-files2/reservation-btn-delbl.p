DEF INPUT PARAMETER pvILanguage  AS INTEGER NO-UNDO.
DEF INPUT PARAMETER curr-select  AS CHAR    NO-UNDO.
DEF INPUT PARAMETER resno        AS INTEGER NO-UNDO.
DEF INPUT PARAMETER reslinno     AS INTEGER NO-UNDO.

DEF OUTPUT PARAMETER msg-str     AS CHAR     NO-UNDO INIT "".
DEF OUTPUT PARAMETER delete-str  AS CHAR     NO-UNDO INIT "".
DEF OUTPUT PARAMETER error-flag  AS LOGICAL  NO-UNDO INIT YES.
DEF OUTPUT PARAMETER pswd-str    AS CHAR     NO-UNDO INIT "".
DEF OUTPUT PARAMETER max-comp    AS INTEGER  NO-UNDO INIT 0.
DEF OUTPUT PARAMETER com-rm      AS INTEGER  NO-UNDO INIT 0.
DEF OUTPUT PARAMETER queasy-flag AS LOGICAL NO-UNDO INIT NO.

DEFINE VARIABLE deposit    AS LOGICAL NO-UNDO INIT NO.
DEFINE VARIABLE may-delete AS LOGICAL NO-UNDO INIT YES.

{SupertransBL.i} 
DEF VAR lvCAREA AS CHAR INITIAL "reservation". 
 
FIND FIRST reservation WHERE reservation.resnr = resno 
    NO-LOCK NO-ERROR.
FIND FIRST res-line WHERE res-line.resnr = resno
  AND res-line.reslinnr = reslinno NO-LOCK NO-ERROR.

IF curr-select = "res-line" THEN RUN delete-resline.
ELSE RUN delete-mainres.

PROCEDURE delete-resline:

    IF (res-line.active-flag = 1 OR res-line.resstatus = 6 
        OR res-line.resstatus = 13) AND res-line.l-zuordnung[3] = 0 THEN   /* Inhouse Guest */ 
    DO: 
      msg-str = translateExtended( "Deleting of Inhouse-Guests is not possible.", lvCAREA, "":U).
      RETURN. 
    END. 

    FIND FIRST htparam WHERE paramnr = 437 NO-LOCK.
    IF htparam.flogical = NO AND res-line.betrieb-gast > 0
        AND res-line.l-zuordnung[3] = 0 THEN 
    DO: 
      msg-str = translateExtended ("KeyCard has been generated. Cancellation no longer possible.",lvCAREA,"").
      RETURN. 
    END.

    RUN check-deposit. 
    IF may-delete = NO AND res-line.l-zuordnung[3] = 0 THEN 
    DO: 
      msg-str = translateExtended( "ATTENTION: Deposit Payment exists for this reservartion.",lvCAREA, "":U).
      RETURN.
    END. 

    IF res-line.resstatus NE 11 AND res-line.resstatus NE 13 THEN 
    DO: 
      RUN check-compliment(res-line.resnr, res-line.reslinnr, res-line.gastnr, 
        res-line.ankunft, res-line.reserve-int, res-line.zikatnr, res-line.arrangement, 
        0, res-line.zipreis, OUTPUT error-flag).
      IF error-flag THEN RETURN.
    END. 

    FIND FIRST queasy WHERE queasy.KEY = 32 AND queasy.char3 NE ""
      NO-LOCK NO-ERROR.
    IF AVAILABLE reservation THEN delete-str = reservation.vesrdepot2.
    ASSIGN
      error-flag  = NO
      queasy-flag = AVAILABLE queasy
      msg-str = "&Q"
            + translateExtended( "Do you really want to DELETE the reservation:",lvCAREA, "":U) 
            + CHR(10) 
            + res-line.name + " - " + res-line.zinr 
            + CHR(10)
            + translateExtended( "Arrival :", lvCAREA, "":U) + " "
            + STRING(res-line.ankunft) + " " 
            + translateExtended( "Departure:", lvCAREA, "":U) + " "
            + STRING(res-line.abreise) + " ?".
END.
    
PROCEDURE delete-mainres:
  
  IF NOT AVAILABLE reservation THEN RETURN.

  FIND FIRST res-line WHERE res-line.resnr = reservation.resnr 
    AND (res-line.resstatus EQ 6 OR res-line.resstatus EQ 13) 
    NO-LOCK NO-ERROR. 
  IF AVAILABLE res-line THEN 
  DO: 
    msg-str = translateExtended( "Deleting not possible, In-House guest exists.", lvCAREA, "":U). 
    RETURN. 
  END. 

  FIND FIRST res-line WHERE res-line.resnr = reservation.resnr 
    AND res-line.active-flag = 0 AND res-line.betrieb-gast > 0 
    NO-LOCK NO-ERROR. 
  IF AVAILABLE res-line THEN 
  DO: 
    msg-str = translateExtended ("KeyCard has been generated for",lvCAREA,"") 
        + " " + res-line.NAME 
        + " - " + translateExtended ("RmNo",lvCAREA,"") + " " + res-line.zinr 
        + CHR(10)
        + translateExtended ("Deleting for all members no longer possible.",lvCAREA,""). 
    RETURN. 
  END. 

  RUN check-deposit. 
  IF deposit THEN 
  DO: 
    msg-str = translateExtended( "ATTENTION: Deposit Payment exists for this reservartion.",lvCAREA, "":U).
    RETURN.
  END. 
    
  FIND FIRST guest WHERE guest.gastnr = reservation.gastnr NO-LOCK. 
  FIND FIRST queasy WHERE queasy.KEY = 32 AND queasy.char3 NE ""
    NO-LOCK NO-ERROR.
      
  ASSIGN
    error-flag  = NO
    queasy-flag = AVAILABLE queasy
    delete-str  = reservation.vesrdepot2.
    msg-str = "&Q"
            + translateExtended( "Do you really want to DELETE the main reservation of", lvCAREA, "":U) 
            + CHR(10)
            + guest.name + ", " + guest.vorname1 + guest.anredefirma 
            + " " + guest.anrede1 
            + CHR(10) 
            + translateExtended( "including it's all reservation members ?", lvCAREA, "":U).
  .
END.

PROCEDURE check-deposit: 
DEFINE VARIABLE anzahl     AS INTEGER NO-UNDO INIT 0. 
DEFINE BUFFER reservation1 FOR reservation. 
DEFINE BUFFER resline1     FOR res-line. 

  FIND FIRST reservation1 WHERE reservation1.resnr = resno NO-LOCK. 
  IF (reservation1.depositbez + reservation1.depositbez2) NE 0 
    THEN deposit = YES. /* deposit payment found */
  IF deposit AND reservation1.bestat-dat = ? /* guest mot checked-in yet */ THEN 
  DO: 
    FIND FIRST resline1 WHERE resline1.resnr = resno 
          AND resline1.active-flag = 1 NO-LOCK NO-ERROR. 
    IF AVAILABLE resline1 THEN RETURN. 
    FIND FIRST resline1 WHERE resline1.resnr = resno 
          AND resline1.active-flag = 2 AND resline1.resstatus = 8 
           NO-LOCK NO-ERROR. 
    IF AVAILABLE resline1 THEN RETURN. 
 
    FOR EACH resline1 WHERE resline1.resnr = resno 
        AND resline1.active-flag = 0 NO-LOCK: 
      anzahl = anzahl + 1. 
    END. 
  END. 
  IF anzahl EQ 1 THEN may-delete = NO. 
END. 

PROCEDURE check-compliment:
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
 
DEF VAR s-recid                     AS INTEGER NO-UNDO.
DEF VAR book-room                   AS INTEGER NO-UNDO. 
DEF VAR comp-room                   AS INTEGER NO-UNDO. 
DEF VAR max-room                    AS INTEGER NO-UNDO. 
 
DEF VAR pay-rm                      AS INTEGER INITIAL 0 NO-UNDO. 
DEF VAR curr-rm                     AS INTEGER NO-UNDO. 
DEF VAR passwd-ok                   AS LOGICAL INITIAL NO NO-UNDO. 
DEF VAR new-contrate                AS LOGICAL INITIAL NO. 
 
DEF VAR ct                          AS CHAR    NO-UNDO.
DEF VAR contcode                    AS CHAR    NO-UNDO.

DEF BUFFER resline FOR res-line. 
 
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
    
    RUN ratecode-seek.p(resnr, reslinnr, contcode, datum, OUTPUT s-recid).
    IF s-recid = 0 THEN RETURN.
    FIND FIRST ratecode WHERE RECID(ratecode) = s-recid NO-LOCK.
    IF NUM-ENTRIES(ratecode.char1[4], ";") LT 3 THEN RETURN.  
    ASSIGN  
      book-room = INTEGER(ENTRY(1, ratecode.char1[4], ";"))
      comp-room = INTEGER(ENTRY(2, ratecode.char1[4], ";")) 
      max-room  = INTEGER(ENTRY(3, ratecode.char1[4], ";"))
    . 
    
    curr-rm = pay-rm. 
    IF curr-rm GT max-room THEN curr-rm = max-room. 
    max-comp = ROUND(curr-rm / book-room - 0.5, 0) * comp-room. 
    IF max-comp LT 0 THEN max-comp = 0. 
     
    IF com-rm LE max-comp THEN RETURN. 
     
    msg-str = translateExtended ("Wrong total number of compliment rooms:",lvCAREA,"") 
            + CHR(10)
            + CHR(10)
            + translateExtended ("Max allowed =",lvCAREA,"") + " " + STRING(max-comp) 
            + CHR(10)
            + translateExtended ("Actual compliment rooms =",lvCAREA,"") 
            + " " + STRING(com-rm).
     
    FIND FIRST htparam WHERE htparam.paramnr = 141 NO-LOCK. 
    IF htparam.fchar = "" THEN still-error = YES. 
    ELSE
    ASSIGN
      still-error = NO
      pswd-str   = htparam.fchar
    . 
END.
