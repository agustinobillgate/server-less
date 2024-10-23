/*FT 130814 saat update resname guest name tidak ikut berubah*/
DEF INPUT PARAMETER pvILanguage   AS INTEGER NO-UNDO.  
DEF INPUT PARAMETER inp-resnr     AS INTEGER NO-UNDO.  
DEF INPUT PARAMETER resart        AS INTEGER NO-UNDO.  
DEF INPUT PARAMETER last-segm     AS INTEGER NO-UNDO.  
DEF INPUT PARAMETER curr-segm     AS INTEGER NO-UNDO.  
DEF INPUT PARAMETER gastnrherk    AS INTEGER NO-UNDO.  
DEF INPUT PARAMETER gastnrcom     AS INTEGER NO-UNDO.  
DEF INPUT PARAMETER gastnrpay     AS INTEGER NO-UNDO.  
DEF INPUT PARAMETER letterno      AS INTEGER NO-UNDO.  
DEF INPUT PARAMETER contact-nr    AS INTEGER NO-UNDO.  
DEF INPUT PARAMETER rechnerstart  AS INTEGER NO-UNDO.  
DEF INPUT PARAMETER rechnrend     AS INTEGER NO-UNDO.  
  
DEF INPUT PARAMETER res-mode      AS CHAR    NO-UNDO.  
DEF INPUT PARAMETER user-init     AS CHAR    NO-UNDO.  
DEF INPUT PARAMETER origin        AS CHAR    NO-UNDO.  
DEF INPUT PARAMETER groupname     AS CHAR    NO-UNDO.  
DEF INPUT PARAMETER comments      AS CHAR    NO-UNDO.  
DEF INPUT PARAMETER voucherno     AS CHAR    NO-UNDO.  
DEF INPUT PARAMETER bill-receiver AS CHAR    NO-UNDO.  
  
DEF INPUT PARAMETER depositgef    AS DECIMAL NO-UNDO.  
  
DEF INPUT PARAMETER limitdate     AS DATE    NO-UNDO.  
  
DEF INPUT PARAMETER fixed-rate    AS LOGICAL NO-UNDO.  
DEF INPUT PARAMETER init-rate     AS LOGICAL NO-UNDO.  
DEF INPUT PARAMETER master-active AS LOGICAL NO-UNDO.  
DEF INPUT PARAMETER umsatz1       AS LOGICAL NO-UNDO.  
DEF INPUT PARAMETER umsatz2       AS LOGICAL NO-UNDO.  
DEF INPUT PARAMETER umsatz3       AS LOGICAL NO-UNDO.  
DEF INPUT PARAMETER umsatz4       AS LOGICAL NO-UNDO.  
  
DEF INPUT PARAMETER init-time     AS INT.  
DEF INPUT PARAMETER init-date     AS DATE.  
  
DEF OUTPUT PARAMETER flag-ok      AS LOGICAL.  
DEF OUTPUT PARAMETER msg-str      AS CHAR    NO-UNDO INIT "".  
DEF OUTPUT PARAMETER error-number AS INTEGER NO-UNDO INIT 0.  
  
DEFINE VARIABLE segmstr           AS CHAR.  
DEF VAR a AS INT.  
DEF VAR b AS DATE.  

DEFINE BUFFER buff-bill FOR bill. /*FDL*/
  
{SupertransBL.i}   
DEF VAR lvCAREA AS CHAR INITIAL "mk-mainres".   
  
RUN check-timebl.p(3, inp-resnr, ?, "reservation", init-time, init-date,  
                   OUTPUT flag-ok, OUTPUT a, OUTPUT b).  
IF NOT flag-ok THEN RETURN NO-APPLY.  
  
RUN mk-mainres-go.  
  
PROCEDURE mk-mainres-go:  
DEFINE VARIABLE last-segm       AS INTEGER NO-UNDO.   
DEFINE VARIABLE prev-gastnr     AS INTEGER NO-UNDO.   
DEFINE VARIABLE incorrect       AS LOGICAL NO-UNDO.   
DEFINE VARIABLE chg-member      AS LOGICAL INITIAL NO.   
DEFINE VARIABLE num-chg         AS INTEGER INITIAL 0.   
DEFINE VARIABLE contrate-found  AS LOGICAL INITIAL NO.   
DEFINE VARIABLE curr-name       AS CHAR.  
  
  RUN check-segm.   
  IF error-number GT 0 THEN RETURN.   
   
  IF resart = 0 THEN   
  DO:   
    msg-str = translateExtended ("Source of Booking not defined.",lvCAREA,"").   
    error-number = 2.   
    RETURN.   
  END.   
    
  FIND FIRST reservation WHERE reservation.resnr = inp-resnr EXCLUSIVE-LOCK  
      NO-ERROR.  
  IF NOT AVAILABLE reservation THEN  
  DO:  
    msg-str = translateExtended ("Reservation record is being used by other user.",lvCAREA,"").   
    error-number = 3.   
    RETURN.   
  END.  
  
  FIND FIRST bediener WHERE bediener.userinit = user-init NO-LOCK.  
  
  prev-gastnr = reservation.gastnr.   
  FIND FIRST master WHERE master.resnr = reservation.resnr NO-LOCK NO-ERROR.   
  IF AVAILABLE master AND master.active THEN reservation.verstat = 1.   
  ELSE reservation.verstat = 0.   
      
  IF res-mode = "new" THEN reservation.useridanlage = user-init.   
  ELSE IF res-mode = "modify" THEN   
  ASSIGN  
    reservation.useridmutat = user-init   
    reservation.mutdat      = TODAY  
  .   
      
  IF res-mode NE "new" AND   
    ((reservation.segmentcode NE curr-segm) OR   
     (reservation.bemerk NE comments)) THEN   
    RUN add-reslog(reservation.segmentcode, curr-segm).   
   
  ASSIGN   
      reservation.segmentcode = curr-segm   
      reservation.groupname = groupname   
      reservation.grpflag = (groupname NE "")   
      reservation.bemerk = comments   
      reservation.limitdate = limitdate   
      reservation.depositgef = depositgef   
      reservation.gastnrherk = gastnrherk   
      reservation.herkunft = origin   
      reservation.guestnrcom[1] = gastnrcom   
      reservation.briefnr = letterno   
      reservation.resart = resart   
      reservation.vesrdepot = voucherno   
      reservation.insurance = fixed-rate   
      reservation.kontakt-nr = contact-nr  
  .   
   
  FIND FIRST res-line WHERE res-line.resnr = reservation.resnr   
    AND res-line.active-flag LE 1 NO-LOCK NO-ERROR.   
  DO WHILE AVAILABLE res-line:   
    FIND CURRENT res-line EXCLUSIVE-LOCK NO-ERROR.  
    IF AVAILABLE res-line THEN  
    DO:  
      res-line.grpflag = reservation.grpflag.   
      FIND CURRENT res-line NO-LOCK.   
    END.  
    FIND NEXT res-line WHERE res-line.resnr = reservation.resnr   
      NO-LOCK NO-ERROR.   
  END.   
    
  FIND FIRST guest WHERE guest.gastnr = reservation.gastnr NO-LOCK.  
  IF NOT AVAILABLE master AND (guest.karteityp = 1 OR guest.karteityp = 2) THEN   
  DO:   
    FIND FIRST htparam WHERE paramnr = 166 NO-LOCK.   
    IF htparam.flogical THEN   
    msg-str = "&Q"  
      + translateExtended ("Master Bill does not exist, CREATE IT?",lvCAREA,"").  
  END.   
   
  IF AVAILABLE master THEN   
  DO:   
    FIND CURRENT master EXCLUSIVE-LOCK.   
    ASSIGN   
      master.ACTIVE         = master-active  
      master.rechnrstart    = rechnrstart   
      master.rechnrend      = rechnrend   
      master.umsatzart[1]   = umsatz1   
      master.umsatzart[2]   = umsatz2   
      master.umsatzart[3]   = umsatz3   
      master.umsatzart[4]   = umsatz4   
      master.gastnrpay      = gastnrpay   
      master.name           = bill-receiver  
    .   
   
    IF NOT master.active THEN   
    DO:   
      FIND FIRST bill WHERE bill.resnr = inp-resnr   
        AND bill.reslinnr = 0 NO-LOCK NO-ERROR.   
      IF AVAILABLE bill AND bill.saldo NE 0 THEN master.active = YES.   
    END.   
   
    FIND CURRENT master NO-LOCK.   
    IF master.active THEN reservation.verstat = 1.   
    ELSE reservation.verstat = 0.   
   
/* create master bill only IF resident guest exists !! ******/   
    FIND FIRST res-line WHERE res-line.resnr = master.resnr   
      AND res-line.active-flag = 1 NO-LOCK NO-ERROR.   
    IF AVAILABLE res-line THEN   
    DO:   
      FIND FIRST bill WHERE bill.resnr = inp-resnr   
        AND bill.reslinnr = 0 EXCLUSIVE-LOCK NO-ERROR.   
      IF NOT AVAILABLE bill THEN   
      DO:   
        CREATE bill.   
        ASSIGN  
          bill.resnr    = inp-resnr   
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
        bill.gastnr      = gastnrpay  
        bill.name        = bill-receiver   
        bill.segmentcode = curr-segm  
      .   
      FIND CURRENT bill NO-LOCK.   

      /*FDL Jan 10, 2024 => Ticket 1DBBEB => Validation Double Bill*/
      FIND FIRST buff-bill WHERE buff-bill.rechnr EQ bill.rechnr
          AND buff-bill.resnr EQ 0 AND buff-bill.reslinnr EQ 1
          AND buff-bill.billtyp NE 2 NO-LOCK NO-ERROR.
      IF AVAILABLE buff-bill THEN
      DO:
          /*FDL Debug*/
          MESSAGE 
              "MK-MAINRES-BTN-GOBL" SKIP
              "Origin Bill: " bill.rechnr SKIP
              "Double Bill Number: " STRING(buff-bill.rechnr)
              VIEW-AS ALERT-BOX INFO BUTTONS OK.

          FIND CURRENT buff-bill EXCLUSIVE-LOCK.
          DELETE buff-bill.
          RELEASE buff-bill.
      END.
    END.   
  END.   
   
  IF (reservation.insurance AND NOT init-rate)   
    OR (NOT reservation.insurance AND init-rate)   
    THEN RUN resline-reserve-dec.   
   
  IF reservation.gastnr NE gastnrherk THEN   
  DO:       
    curr-name = reservation.NAME.  
    FIND CURRENT reservation EXCLUSIVE-LOCK.   
    reservation.gastnr = gastnrherk.   
    FIND FIRST guest WHERE guest.gastnr = gastnrherk NO-LOCK.   
    reservation.name = guest.name + ", " + guest.vorname1 + guest.anredefirma.   
    FIND CURRENT reservation NO-LOCK.   
  
    CREATE res-history.   
    ASSIGN   
      res-history.nr        = bediener.nr   
      res-history.datum     = TODAY   
      res-history.zeit      = TIME  
      res-history.action    = "Reservation"  
      res-history.aenderung = "CHG Reservation Name " + curr-name   
        + " -> " + reservation.NAME  
    .  
    FIND CURRENT res-history NO-LOCK.  
  
    FIND FIRST master WHERE master.resnr = reservation.resnr   
      EXCLUSIVE-LOCK NO-ERROR.   
    IF AVAILABLE master THEN   
    DO:   
      master.gastnr = gastnrherk.   
      master.gastnrpay = gastnrherk.   
      master.name = reservation.name.   
      FIND CURRENT master NO-LOCK.   
      FIND FIRST bill WHERE bill.resnr = reservation.resnr   
        AND bill.reslinnr = 0 EXCLUSIVE-LOCK NO-ERROR.   
      IF AVAILABLE bill THEN   
      DO:   
        bill.gastnr = gastnrherk.   
        bill.name = guest.name.   
        FIND CURRENT bill NO-LOCK.   
      END.   
    END.   
    FOR EACH res-line WHERE res-line.resnr = reservation.resnr   
      AND res-line.reslinnr GE 1 EXCLUSIVE-LOCK:   
        
      res-line.gastnr = gastnrherk.   
        
      IF res-line.gastnrpay = prev-gastnr THEN   
      DO:   
        FOR EACH bill WHERE bill.resnr = res-line.resnr   
          AND bill.reslinnr = res-line.reslinnr   
          AND bill.zinr = res-line.zinr EXCLUSIVE-LOCK:   
          bill.gastnr = gastnrherk.   
          bill.name = guest.name.   
        END.   
        res-line.gastnrpay = gastnrherk.   
      END.   
        
      IF res-line.gastnrmember = prev-gastnr AND res-line.active-flag = 0 THEN   
      DO:  
        num-chg = num-chg + 1.   
        /*FT 130814 IF num-chg = 1 THEN  
          ASSIGN   
            res-line.gastnrmember = gastnrherk  
            res-line.name         = reservation.name. */
      END.   
      res-line.resname = reservation.NAME.  
    END.   
      
    FIND FIRST guest-pr WHERE guest-pr.gastnr = reservation.gastnr   
      NO-LOCK NO-ERROR.   
    IF NOT AVAILABLE guest-pr THEN  
      FIND FIRST guest-pr WHERE guest-pr.gastnr = gastnrherk NO-LOCK NO-ERROR.   
    IF AVAILABLE guest-pr THEN   
    msg-str = "&W"  
        + translateExtended ("Contract Rate exists",lvCAREA,"")   
        + CHR(10)   
        + translateExtended ("Manual Changes of the room rate(s) required.",lvCAREA,"").  
  END.   
END.   
   
PROCEDURE check-segm:   
DEFINE VARIABLE i       AS INTEGER NO-UNDO.   
DEFINE VARIABLE b-list  AS INTEGER NO-UNDO.   
    
  FIND FIRST segment WHERE segment.segmentcode = curr-segm   
    NO-LOCK NO-ERROR.   
  IF NOT AVAILABLE segment THEN   
  DO:   
    msg-str = translateExtended ("No such segmentcode.",lvCAREA,"").   
    error-number = 1.  
    RETURN.   
  END.   
   
  IF segment.betriebsnr = 3 THEN   
  DO:   
    MESSAGE translateExtended ("VIP Segment Code is not for reservation.",lvCAREA,"").  
    error-number = 1.  
    RETURN.   
  END.   
  
  IF segment.betriebsnr = 4 THEN   
  DO:   
    MESSAGE translateExtended ("Black-List Segment Code is not for reservation.",lvCAREA,"").   
    error-number = 1.  
    RETURN.   
  END.   
   
  IF segment.betriebsnr GE 1 AND segment.betriebsnr LE 2 THEN   
  DO:   
    FIND FIRST res-line WHERE res-line.resnr = inp-resnr   
      AND res-line.active-flag LE 1 AND res-line.zipreis GT 0   
      NO-LOCK NO-ERROR.   
    IF AVAILABLE res-line THEN   
    DO:   
      msg-str = translateExtended ("The selected COMPLIMENT segment is not valid:",lvCAREA,"")   
              + CHR(10)  
              + translateExtended ("Reservation record found with non-zero RmRate =",lvCAREA,"")   
              + " " + STRING(res-line.zipreis).  
      error-number = 1.  
      RETURN.   
    END.   
  END.   
  segmstr = ENTRY(1, segment.bezeich, "$$0").   
END.   
  
PROCEDURE add-reslog:   
DEFINE INPUT PARAMETER old-segm AS INTEGER.   
DEFINE INPUT PARAMETER new-segm AS INTEGER.   
  
DEFINE VARIABLE cdate AS DATE INITIAL TODAY.   
DEFINE VARIABLE heute AS DATE NO-UNDO.   
DEFINE VARIABLE zeit  AS INTEGER NO-UNDO.   
  
DEFINE BUFFER segment1 FOR segment.   
   
  FIND FIRST res-line WHERE res-line.resnr = inp-resnr   
    AND res-line.active-flag = 1   
    AND res-line.resstatus = 6 NO-LOCK NO-ERROR.   
  IF NOT AVAILABLE res-line THEN   
  DO:   
    IF (reservation.bemerk EQ comments) THEN RETURN.   
    FIND FIRST res-line WHERE res-line.resnr = inp-resnr   
      AND res-line.active-flag = 0   
      AND (res-line.resstatus LE 2 OR res-line.resstatus = 5) NO-LOCK NO-ERROR.   
    IF NOT AVAILABLE res-line THEN RETURN.   
  END.   
   
  ASSIGN  
    heute = TODAY   
    zeit  = TIME  
  .   
   
  IF reservation.mutdat NE ? THEN cdate = reservation.mutdat.   
  FIND FIRST segment1 WHERE segment1.segmentcode = reservation.segmentcode NO-LOCK. 
  IF AVAILABLE segment1 THEN DO:
    CREATE reslin-queasy.   
    ASSIGN  
      reslin-queasy.key      = "ResChanges"  
      reslin-queasy.resnr    = res-line.resnr   
      reslin-queasy.reslinnr = res-line.reslinnr   
      reslin-queasy.date2    = heute  
      reslin-queasy.number2  = zeit  
    .     
    IF reservation.segmentcode NE curr-segm THEN   
      reslin-queasy.char3 = STRING(res-line.ankunft) + ";"   
                        + STRING(res-line.ankunft) + ";"   
                        + STRING(res-line.abreise) + ";"   
                        + STRING(res-line.abreise) + ";"   
                        + STRING(res-line.zimmeranz) + ";"   
                        + STRING(res-line.zimmeranz) + ";"   
                        + STRING(res-line.erwachs) + ";"   
                        + STRING(res-line.erwachs) + ";"   
                        + STRING(res-line.kind1) + ";"   
                        + STRING(res-line.kind1) + ";"   
                        + STRING(res-line.gratis) + ";"   
                        + STRING(res-line.gratis) + ";"   
                        + STRING(res-line.zikatnr) + ";"   
                        + STRING(res-line.zikatnr) + ";"   
                        + STRING(res-line.zinr) + ";"   
                        + STRING("SEGM") + ";"   
                        + STRING(res-line.arrangement) + ";"   
                        + STRING(res-line.arrangement) + ";"   
                        + STRING(res-line.zipreis) + ";"   
                        + STRING(res-line.zipreis) + ";"   
                        + STRING(reservation.useridanlage) + ";"   
                        + STRING(user-init) + ";"   
                        + STRING(cdate) + ";"   
                        + STRING(heute) + ";"   
                        + STRING(segment1.bezeich) + ";"   
                        + STRING(segmstr) + ";"   
                        + STRING(" ") + ";"   
                        + STRING(" ") + ";".   
    ELSE   
    reslin-queasy.char3 = STRING(res-line.ankunft) + ";"   
                        + STRING(res-line.ankunft) + ";"   
                        + STRING(res-line.abreise) + ";"   
                        + STRING(res-line.abreise) + ";"   
                        + STRING(res-line.zimmeranz) + ";"   
                        + STRING(res-line.zimmeranz) + ";"   
                        + STRING(res-line.erwachs) + ";"   
                        + STRING(res-line.erwachs) + ";"   
                        + STRING(res-line.kind1) + ";"   
                        + STRING(res-line.kind1) + ";"   
                        + STRING(res-line.gratis) + ";"   
                        + STRING(res-line.gratis) + ";"   
                        + STRING(res-line.zikatnr) + ";"   
                        + STRING(res-line.zikatnr) + ";"   
                        + STRING(res-line.zinr) + ";"   
                        + STRING(res-line.zinr) + ";"   
                        + STRING(res-line.arrangement) + ";"   
                        + STRING(res-line.arrangement) + ";"   
                        + STRING(res-line.zipreis) + ";"   
                        + STRING(res-line.zipreis) + ";"   
                        + STRING(reservation.useridanlage) + ";"   
                        + STRING(user-init) + ";"   
                        + STRING(cdate) + ";"   
                        + STRING(heute) + ";"   
                        + STRING(segment1.bezeich) + ";"   
                        + STRING(segment1.bezeich) + ";"   
                        + STRING(" ") + ";"   
                        + STRING(" ") + ";".   
   
    FIND CURRENT reslin-queasy NO-LOCK.  
    RELEASE reslin-queasy.   
  END.

  IF reservation.bemerk NE comments THEN   
  DO:   
    CREATE res-history.   
    ASSIGN   
      res-history.nr        = bediener.nr   
      res-history.resnr     = res-line.resnr   
      res-history.reslinnr  = res-line.reslinnr   
      res-history.datum     = heute   
      res-history.zeit      = zeit   
      res-history.action    = "MainRes Remark"   
      res-history.aenderung = reservation.bemerk   
        + "*** Changed to: " + comments  
    .  
    FIND CURRENT res-history NO-LOCK.  
    RELEASE res-history.   
  END.   
   
END.   
  
