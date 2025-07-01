  
DEF INPUT  PARAMETER pvILanguage   AS INTEGER  NO-UNDO.  
DEF INPUT  PARAMETER recid1     AS INT.  
DEF INPUT  PARAMETER moved-room AS CHAR.  
DEF INPUT  PARAMETER ci-date    AS DATE.  
DEF INPUT  PARAMETER user-init  AS CHAR.  
DEF INPUT  PARAMETER moveReason AS CHAR.
DEF OUTPUT PARAMETER changed    AS LOGICAL INIT NO.  
DEF OUTPUT PARAMETER msg-str    AS CHAR.  
/*DEF VAR pvILanguage AS INT INIT 0.  
DEF VAR recid1 AS INT INIT 2187393.  
DEF VAR moved-room AS CHAR INIT "2107".  
DEF VAR ci-date AS DATE INIT 01/31/10.  
DEF VAR user-init AS CHAR INIT "01".  
DEF VAR changed AS LOGICAL.*/  
  
DEF VAR resnr         AS INTEGER                    NO-UNDO.   
DEF VAR reslinnr      AS INTEGER                    NO-UNDO.   
DEF VAR res-mode      AS CHAR                       NO-UNDO.   

/* SY 04 June 2016 */
DEF BUFFER bbuff FOR bill.
  
{SupertransBL.i}  
DEF VAR lvCAREA AS CHAR INITIAL "check-room-roomplan".   
  
FIND FIRST res-line WHERE RECID(res-line) = recid1 NO-LOCK NO-ERROR. 
IF AVAILABLE res-line  THEN
DO:
    RUN move-room.  
    changed = YES.  
END.
  
  
PROCEDURE move-room:   
DEF VARIABLE prev-zinr AS CHAR          NO-UNDO.   
DEF BUFFER resline FOR res-line.   
    
  resnr = res-line.resnr.   
  reslinnr = res-line.reslinnr.   
  IF res-line.resstatus = 6 OR res-line.resstatus = 13 THEN res-mode = "inhouse".   
  ELSE res-mode = "modify".   
   
  DO TRANSACTION:   
    IF res-mode = "inhouse" THEN  
    DO:  
      FIND FIRST zimmer WHERE zimmer.zinr = moved-room EXCLUSIVE-LOCK.  
      IF res-line.abreise = ci-date THEN zimmer.zistatus = 3.  
      ELSE zimmer.zistatus = 5.  
      FIND CURRENT zimmer NO-LOCK.  
    END.  
  
    FIND CURRENT res-line EXCLUSIVE-LOCK.   
    RUN min-resplan.   
    IF res-line.resstatus = 6 THEN   
    DO:   
      RUN rmchg-sharer(res-line.zinr, moved-room).   
      FIND FIRST htparam WHERE paramnr = 307 NO-LOCK NO-ERROR.   
      IF htparam.flogical THEN   
        RUN intevent-1.p(2, res-line.zinr, "Move out", res-line.resnr, res-line.reslinnr).  
      RUN update-billzinr.   
    END.   
    ELSE RUN rmchg-ressharer(res-line.zinr, moved-room).   
    prev-zinr = res-line.zinr.   
    RUN res-changes.   /* create log file IF any res-line changes */   
    RUN update-resline.   
    RUN add-resplan.   
       
    IF res-line.resstatus = 6 THEN   
    DO:   
      DEF VAR move-str AS CHAR NO-UNDO.
      FIND FIRST htparam WHERE paramnr = 307 NO-LOCK NO-ERROR.   
      IF htparam.flogical THEN   
      DO:
          ASSIGN move-str = "Move in|" + prev-zinr.
          RUN intevent-1.p(1, moved-room, move-str, 
             res-line.resnr, res-line.reslinnr).   
      END.
      /* FD Comment
      RUN create-historybl.p(res-line.resnr, res-line.reslinnr,   
          prev-zinr, "roomchg", user-init, ""). 
      */
      /*FD Sept 07, 2022 => 5BE61A - Given reason for change room with same the room type*/
      RUN create-historybl.p(res-line.resnr, res-line.reslinnr,   
          prev-zinr, "roomchg", user-init, moveReason). 

/* Check MEalCoupon */   
      FIND FIRST resline WHERE resline.resnr = res-line.resnr   
        AND (resline.active-flag = 0 OR resline.active-flag = 1)   
        AND resline.resstatus NE 12   
        AND resline.zinr = prev-zinr NO-LOCK NO-ERROR.   
      IF NOT AVAILABLE resline THEN /* NO guest IN the previous stayed room */   
      DO:   
        FIND FIRST mealcoup WHERE mealcoup.zinr = prev-zinr   
          AND mealcoup.activeflag = YES USE-INDEX zinrflag_ix EXCLUSIVE-LOCK   
          NO-ERROR.   
        IF AVAILABLE mealcoup THEN   
        DO:   
          mealcoup.zinr = res-line.zinr.   
          FIND CURRENT mealcoup NO-LOCK.   
        END.   
      END.   
    END.   
   
    /*IF res-line.betrieb-gast GT 0 THEN   
    DO:   
      IF SESSION:PARAMETER MATCHES "*coder=*" THEN RUN add-keycard.   
      ELSE   
      DO:  
        msg-str = msg-str + CHR(2)  
                + translateExtended ("Replace the KeyCard / Qty =", lvCAREA, "":U)  
                + " " + STRING(res-line.betrieb-gast).  
      END.   
    END.  FT serverless*/
  END.   
    
END PROCEDURE.   
  
  
  
  
PROCEDURE min-resplan:  
  DEFINE VARIABLE curr-date AS DATE.  
  DEFINE VARIABLE beg-datum AS DATE.  
  DEFINE VARIABLE i AS INTEGER.  
  DEFINE BUFFER rline FOR res-line.  
  FIND FIRST rline WHERE rline.resnr = resnr   
      AND rline.reslinnr = reslinnr NO-LOCK NO-ERROR.  
  FIND FIRST zimmer WHERE zimmer.zinr = rline.zinr NO-LOCK NO-ERROR.  
  IF AVAILABLE zimmer AND (NOT zimmer.sleeping) THEN  
  DO:  
/* do not update */    
  END.  
  ELSE DO:  
    i = rline.resstatus.  
    FIND FIRST zimkateg WHERE zimkateg.zikatnr = rline.zikatnr NO-LOCK.  
    if res-mode = "inhouse" THEN beg-datum = today.  
    ELSE beg-datum = rline.ankunft.  
    curr-date = beg-datum.  
    do while curr-date GE beg-datum AND curr-date LT rline.abreise:  
      FIND FIRST resplan WHERE resplan.zikatnr = zimkateg.zikatnr  
        AND resplan.datum = curr-date NO-LOCK NO-ERROR.  
      if AVAILABLE resplan THEN   
      DO TRANSACTION:  
        FIND CURRENT resplan EXCLUSIVE-LOCK.  
        resplan.anzzim[i] = resplan.anzzim[i] - rline.zimmeranz.
        FIND CURRENT resplan NO-LOCK.
      END.  
      release resplan.  
      curr-date = curr-date + 1.  
    END.  
  END.  
END.  
  
  
PROCEDURE rmchg-sharer:  
DEFINE INPUT PARAMETER act-zinr LIKE res-line.zinr.		/*MT 25/07/12 */
DEFINE INPUT PARAMETER new-zinr LIKE res-line.zinr.		/*MT 25/07/12 */
DEFINE VARIABLE res-recid1 AS INTEGER.  
DEFINE BUFFER res-line1 FOR res-line.  
DEFINE BUFFER res-line2 FOR res-line.  
DEFINE VARIABLE beg-datum AS DATE.  
DEFINE VARIABLE answer AS LOGICAL.  
DEFINE VARIABLE parent-nr AS INTEGER.  
DEFINE VARIABLE curr-datum AS DATE.  
DEFINE VARIABLE end-datum AS DATE.  
DEFINE BUFFER new-zkat FOR zimkateg.  
  
  FIND FIRST htparam WHERE htparam.paramnr = 87 NO-LOCK NO-ERROR.  
  IF AVAILABLE htparam THEN beg-datum  = htparam.fdate.  
  end-datum = beg-datum.  
  res-recid1 = 0.  
  DO TRANSACTION:  
    FOR EACH messages WHERE messages.zinr = act-zinr AND messages.resnr =   
      res-line.resnr AND messages.reslinnr GE 1:  
      messages.zinr = new-zinr.  
    END.  
    FOR EACH res-line1 WHERE res-line1.resnr = resnr  
      AND res-line1.zinr = act-zinr AND res-line1.resstatus = 13   
      NO-LOCK:  
      if end-datum LE res-line1.abreise THEN   
      DO:  
        res-recid1 = RECID(res-line1).  
        end-datum = res-line1.abreise.  
      END.  
    END.   
  
    if res-line.resstatus = 6  /* this is the res-line from the main guest */  
       AND res-recid1 EQ 0 THEN /* there is no room sharers */  
    DO:  
      FIND FIRST zimmer WHERE zimmer.zinr = act-zinr EXCLUSIVE-LOCK.  
      zimmer.zistatus = 2.  
      FIND CURRENT zimmer NO-LOCK.  
    END.  
      
    if res-line.resstatus = 6  /* this is the res-line from the main guest */  
       AND res-recid1 NE 0 THEN /* there is a room sharer */  
    DO:  
      FIND FIRST res-line1 WHERE RECID(res-line1) = res-recid1 NO-LOCK.  
/*        
      answer = yes.  
      HIDE MESSAGE NO-PAUSE.  
      MESSAGE "Room-change FOR the RoomSharer too?"           
         VIEW-AS ALERT-BOX question buttons yes-no update answer.  
      if answer = no THEN   
      DO:  
        FIND CURRENT res-line1 EXCLUSIVE-LOCK.  
        res-line1.resstatus = 6.  
        FIND CURRENT res-line1 NO-LOCK.  
        res-recid1 = RECID(res-line1).  
        do curr-datum = beg-datum to (end-datum - 1):   
          FIND FIRST zimplan WHERE zimplan.datum = curr-datum  
               AND zimplan.zinr = act-zinr NO-LOCK NO-ERROR.  
          if not AVAILABLE zimplan THEN   
          DO:  
            CREATE zimplan.  
            zimplan.datum = curr-datum.  
            zimplan.zinr = act-zinr.  
            zimplan.res-recid = res-recid1.  
            zimplan.gastnrmember = res-line1.gastnrmember.  
            zimplan.bemerk = res-line1.bemerk.  
            zimplan.resstatus = res-line1.resstatus.  
            zimplan.name = res-line1.name.  
            FIND CURRENT zimplan NO-LOCK.  
          END.  
  
          FIND FIRST zimkateg WHERE zimkateg.zikatnr = res-line1.zikatnr   
              NO-LOCK.  
          FIND FIRST resplan WHERE resplan.zikatnr = zimkateg.zikatnr  
              AND resplan.datum = curr-datum NO-LOCK NO-ERROR.  
          if AVAILABLE resplan THEN   
          DO:  
            FIND CURRENT resplan share-lock.  
            resplan.anzzim[13] = resplan.anzzim[13] - 1.  
            resplan.anzzim[6] = resplan.anzzim[6] + 1.  
            release resplan.  
          END.  
        END.  
      END.  
      ELSE  /* answer = yes ==> move all room sharers to the new room */   
*/  
      DO:         
        FOR EACH res-line2 WHERE res-line2.resnr = resnr  
             AND res-line2.zinr = act-zinr AND res-line2.resstatus = 13   
             AND res-line2.l-zuordnung[3] = 0 EXCLUSIVE-LOCK:  
           FIND FIRST zimmer WHERE zimmer.zinr = new-zinr NO-LOCK.  
           FIND FIRST new-zkat WHERE new-zkat.zikatnr = zimmer.zikatnr  
             NO-LOCK.  
           IF  new-zkat.zikatnr NE res-line2.zikatnr THEN   
           DO:        
              do curr-datum = beg-datum to (res-line2.abreise - 1):   
                 FIND FIRST resplan WHERE resplan.zikatnr = res-line2.zikatnr  
                 AND resplan.datum = curr-datum NO-LOCK NO-ERROR.  
                 if AVAILABLE resplan THEN   
                 DO:  
                    FIND CURRENT resplan EXCLUSIVE-LOCK.  
                    resplan.anzzim[13] = resplan.anzzim[13] - 1. 
                    FIND CURRENT resplan NO-LOCK.
                    release resplan.  
                 END.  
                 FIND FIRST resplan WHERE resplan.zikatnr = new-zkat.zikatnr  
                    AND resplan.datum = curr-datum EXCLUSIVE-LOCK NO-ERROR.  
                 if not AVAILABLE resplan THEN  
                 DO:  
                    CREATE resplan.  
                    resplan.datum = curr-datum.  
                    resplan.zikatnr = new-zkat.zikatnr.  
                 END.  
                 resplan.anzzim[13] = resplan.anzzim[13] + 1. 
                 FIND CURRENT resplan NO-LOCK.
                 RELEASE resplan.  
              END.  
           END.    
              
           /*
           FOR EACH bill WHERE bill.resnr = resnr   
              AND bill.parent-nr = res-line2.reslinnr AND bill.flag = 0  
              AND bill.zinr = res-line2.zinr EXCLUSIVE-LOCK:  
*/
           /* SY 04 June 2016 */
           FOR EACH bill WHERE bill.resnr = resnr   
              AND bill.parent-nr = res-line2.reslinnr NO-LOCK:  
             FIND FIRST bbuff WHERE RECID(bbuff) = RECID(bill)
                 EXCLUSIVE-LOCK.
             bbuff.zinr = new-zinr.
             FIND CURRENT bbuff NO-LOCK.
             RELEASE bbuff.  
           END.  

            
           ASSIGN  
             res-line2.zinr = new-zinr  
             res-line2.zikatnr = new-zkat.zikatnr  
             res-line2.setup   = zimmer.setup  
           .  
           RELEASE res-line2.  
        END.      
        FOR EACH res-line2 WHERE res-line2.resnr = resnr  
            AND res-line2.zinr = act-zinr AND res-line2.resstatus = 12   
            EXCLUSIVE-LOCK:  
          ASSIGN  
            res-line2.zinr    = new-zinr  
            res-line2.zikatnr = new-zkat.zikatnr  
            res-line2.setup   = zimmer.setup  
          .  
          RELEASE res-line2.  
        END.  
              
        FIND FIRST zimmer WHERE zimmer.zinr = act-zinr EXCLUSIVE-LOCK.  
        zimmer.zistatus = 2.  
        FIND CURRENT zimmer NO-LOCK.  
      END.  
    END.  
  END.  
END.   
  
  
  
PROCEDURE update-billzinr:   
DEFINE VARIABLE old-zinr  AS CHAR.   
DEFINE VARIABLE parent-nr AS INTEGER.   
DEFINE BUFFER resline     FOR res-line.   
  old-zinr = res-line.zinr.   
   
  /*
  FOR EACH bill WHERE bill.resnr = res-line.resnr   
    AND bill.parent-nr = res-line.reslinnr AND bill.flag = 0   
    AND bill.zinr = old-zinr EXCLUSIVE-LOCK:   
*/
  /* SY 04 June 2016 */
  FOR EACH bill WHERE bill.resnr = res-line.resnr   
    AND bill.parent-nr = res-line.reslinnr AND bill.flag = 0 NO-LOCK:
    FIND FIRST bbuff WHERE RECID(bbuff) = RECID(bill)
           EXCLUSIVE-LOCK.
    bbuff.zinr = moved-room.
    FIND CURRENT bbuff NO-LOCK.
    RELEASE bbuff.  
    FIND FIRST resline WHERE resline.resnr = bill.resnr   
      AND resline.reslinnr = bill.reslinnr NO-LOCK.   
    IF resline.resstatus = 12 /* i.e. res-line FOR additional bill */   
    THEN DO:   
      FIND CURRENT resline EXCLUSIVE-LOCK.   
      resline.zinr = moved-room.   
      FIND CURRENT resline NO-LOCK.   
    END.   
    RELEASE bill.   
  END.   
   
  IF res-line.active-flag = 1 THEN   
  /*  
  FOR EACH bill WHERE bill.resnr = res-line.resnr   
    AND bill.parent-nr = res-line.reslinnr AND bill.flag = 1   
    AND bill.zinr = old-zinr EXCLUSIVE-LOCK:   
*/
  /* SY 04 June 2016 */
  FOR EACH bill WHERE bill.resnr = res-line.resnr   
    AND bill.parent-nr = res-line.reslinnr AND bill.flag = 1 NO-LOCK:   
    FIND FIRST bbuff WHERE RECID(bbuff) = RECID(bill)
        EXCLUSIVE-LOCK.
    bbuff.zinr = moved-room.
    FIND CURRENT bbuff NO-LOCK.
    RELEASE bbuff.  
    FIND FIRST resline WHERE resline.resnr = bill.resnr   
      AND resline.reslinnr = bill.reslinnr NO-LOCK.   
    IF resline.resstatus = 12 /* i.e. res-line FOR additional bill */   
    THEN DO:   
      FIND CURRENT resline EXCLUSIVE-LOCK.   
      resline.zinr = moved-room.   
      FIND CURRENT resline NO-LOCK.   
    END.   
    RELEASE bill.   
  END.   
END.   
  
  
PROCEDURE rmchg-ressharer:   
DEFINE INPUT PARAMETER act-zinr LIKE zimmer.zinr.
DEFINE INPUT PARAMETER new-zinr LIKE zimmer.zinr.
DEFINE BUFFER new-zkat FOR zimkateg.   
DEFINE BUFFER res-line2 FOR res-line.   
DEFINE BUFFER rline2    FOR res-line.   
DEFINE VARIABLE curr-datum AS DATE.   
   
  FIND FIRST zimmer WHERE zimmer.zinr = moved-room NO-LOCK.   
  FOR EACH rline2 WHERE rline2.resnr = resnr   
    AND rline2.zinr NE ""   
    AND rline2.zinr = act-zinr AND rline2.resstatus = 11 NO-LOCK:   
    FIND FIRST res-line2 WHERE RECID(res-line2) = RECID(rline2) EXCLUSIVE-LOCK.   
    IF zimmer.zikatnr NE res-line2.zikatnr THEN   
    DO curr-datum = res-line2.ankunft TO (res-line2.abreise - 1):   
      FIND FIRST resplan WHERE resplan.zikatnr = res-line2.zikatnr   
        AND resplan.datum = curr-datum NO-LOCK NO-ERROR.   
      IF AVAILABLE resplan THEN   
      DO:   
        FIND CURRENT resplan EXCLUSIVE-LOCK.   
        resplan.anzzim[11] = resplan.anzzim[11] - 1.   
        FIND CURRENT resplan NO-LOCK.   
        RELEASE resplan.   
      END.   
      FIND FIRST resplan WHERE resplan.zikatnr = zimmer.zikatnr   
        AND resplan.datum = curr-datum EXCLUSIVE-LOCK NO-ERROR.   
      IF NOT AVAILABLE resplan THEN   
      DO:   
        CREATE resplan.   
        resplan.datum = curr-datum.   
        resplan.zikatnr = zimmer.zikatnr.   
      END.   
      resplan.anzzim[11] = resplan.anzzim[11] + 1.   
      FIND CURRENT resplan NO-LOCK.   
      RELEASE resplan.   
    END.   
    res-line2.zinr = new-zinr.   
    res-line2.zikatnr = zimmer.zikatnr.   
    FIND CURRENT res-line2 NO-LOCK.   
    RELEASE res-line2.   
  END.   
END.   
  
  
PROCEDURE update-resline:   
DEF BUFFER qsy   FOR queasy.   
DEF BUFFER rline FOR res-line.  
  
  IF res-line.active-flag = 1 THEN   
  DO:   
      FIND FIRST queasy WHERE queasy.KEY = 24 AND queasy.char1   
         = res-line.zinr NO-LOCK NO-ERROR.   
      DO WHILE AVAILABLE queasy:   
          FIND FIRST qsy WHERE RECID(qsy) = RECID(queasy) EXCLUSIVE-LOCK.   
          qsy.char1 = moved-room.   
          FIND CURRENT qsy NO-LOCK.   
          FIND NEXT queasy WHERE queasy.KEY = 24 AND queasy.char1   
             = res-line.zinr NO-LOCK NO-ERROR.   
      END.   
  END.   
   
  FIND FIRST zimmer WHERE zimmer.zinr = moved-room NO-LOCK.   
  ASSIGN   
    res-line.zikatnr      = zimmer.zikatnr   
    res-line.zinr         = zimmer.zinr   
    res-line.setup        = zimmer.setup   
    res-line.reserve-char = STRING(TODAY) + STRING(TIME,"HH:MM") + user-init   
    res-line.changed      = ci-date   
    res-line.changed-id   = user-init  
  .   
  FIND CURRENT res-line NO-LOCK.   
   
  FIND FIRST rline WHERE rline.resnr = res-line.resnr   
      AND rline.kontakt-nr = res-line.reslinnr  
      AND rline.l-zuordnung[3] = 1 NO-LOCK NO-ERROR.  
  DO WHILE AVAILABLE rline:  
      FIND CURRENT rline EXCLUSIVE-LOCK.  
      ASSIGN rline.zinr = moved-room.  
      FIND NEXT rline WHERE rline.resnr = res-line.resnr   
          AND rline.kontakt-nr = res-line.reslinnr  
          AND rline.l-zuordnung[3] = 1 NO-LOCK NO-ERROR.  
  END.  
  
END.   
  
  
PROCEDURE add-resplan:  
  DEFINE VARIABLE curr-date AS DATE.  
  DEFINE VARIABLE beg-datum AS DATE.  
  DEFINE VARIABLE end-datum AS DATE.  
  DEFINE VARIABLE i AS INTEGER.  
  DEFINE VARIABLE anz AS INTEGER.  
  DEFINE BUFFER rline FOR res-line.  
  
  FIND FIRST rline WHERE rline.resnr = resnr   
      AND rline.reslinnr = reslinnr NO-LOCK.  
  FIND FIRST zimmer WHERE zimmer.zinr = rline.zinr NO-LOCK NO-ERROR.  
  if AVAILABLE zimmer AND (not zimmer.sleeping) THEN  
  DO:  
/* do not update */    
  END.  
  ELSE DO:  
    i = rline.resstatus.  
    FIND FIRST zimkateg WHERE zimkateg.zikatnr = rline.zikatnr NO-LOCK.  
    if res-mode = "inhouse" THEN beg-datum = today.  
    ELSE beg-datum = rline.ankunft.  
    end-datum = rline.abreise - 1.  
    curr-date = beg-datum.  
    do curr-date = beg-datum to end-datum:  
      FIND FIRST resplan WHERE resplan.zikatnr = zimkateg.zikatnr  
          AND resplan.datum = curr-date NO-LOCK NO-ERROR.  
      DO TRANSACTION:  
        if not AVAILABLE resplan THEN  
        DO:  
          CREATE resplan.  
          resplan.datum = curr-date.  
          resplan.zikatnr = zimkateg.zikatnr.  
        END.  
        anz = resplan.anzzim[i] + rline.zimmeranz.  
        FIND CURRENT resplan EXCLUSIVE-LOCK.  
        resplan.anzzim[i] = anz.  
        FIND CURRENT resplan NO-LOCK.  
        RELEASE resplan.  
      END.  
    END.  
  END.  
END.  
  
  
PROCEDURE res-changes:   
DEFINE VARIABLE do-it AS LOGICAL INITIAL NO.   
DEFINE BUFFER guest1 FOR guest.   
DEFINE VARIABLE cid AS CHAR FORMAT "x(2)" INITIAL "  ".   
DEFINE VARIABLE cdate AS CHAR FORMAT "x(8)" INITIAL "        ".   
   
  IF TRIM(res-line.changed-id) NE "" THEN   
  DO:   
    cid = res-line.changed-id.   
    cdate = STRING(res-line.changed).   
  END.   
  ELSE IF LENGTH(res-line.reserve-char) GE 14 THEN    /* created BY */   
  cid = SUBSTR(res-line.reserve-char,14).   
   
  CREATE reslin-queasy.   
  ASSIGN   
    reslin-queasy.key = "ResChanges"   
    reslin-queasy.resnr = resnr   
    reslin-queasy.reslinnr = reslinnr   
    reslin-queasy.char3 = STRING(res-line.ankunft)              + ";" 
                        + STRING(res-line.ankunft)              + ";" 
                        + STRING(res-line.abreise)              + ";" 
                        + STRING(res-line.abreise)              + ";" 
                        + STRING(res-line.zimmeranz, ">>9")     + ";" 
                        + STRING(res-line.zimmeranz, ">>9")     + ";" 
                        + STRING(res-line.erwachs, ">9")        + ";" 
                        + STRING(res-line.erwachs, ">9")        + ";" 
                        + STRING(res-line.kind1, ">9")          + ";" 
                        + STRING(res-line.kind1, ">9")          + ";" 
                        + STRING(res-line.gratis, ">9")         + ";" 
                        + STRING(res-line.gratis, ">9")         + ";" 
                        + STRING(res-line.zikatnr, ">>9")       + ";" 
                        + STRING(zimmer.zikatnr, ">>9")         + ";" 
                        + STRING(res-line.zinr, "x(6)")         + ";" 
                        + STRING(moved-room, "x(6)")            + ";" 
                        + STRING(res-line.arrangement, "x(5)")  + ";" 
                        + STRING(res-line.arrangement, "x(5)")  + ";".
   
  IF res-line.zipreis LE 9999999 THEN   
    reslin-queasy.char3 = reslin-queasy.char3   
                        + STRING(res-line.zipreis, ">,>>>,>>9.99") + ";" 
                        + STRING(res-line.zipreis, ">,>>>,>>9.99") + ";" .
  ELSE reslin-queasy.char3 = reslin-queasy.char3   
                        + STRING(res-line.zipreis, ">>>>,>>>,>>9") + ";" 
                        + STRING(res-line.zipreis, ">>>>,>>>,>>9") + ";" .
   
  reslin-queasy.char3 = reslin-queasy.char3   
                        + STRING(cid, "x(2)")                   + ";" 
                        + STRING(user-init, "x(2)")             + ";" 
                        + STRING(cdate, "x(8)")                 + ";" 
                        + STRING(TODAY)                         + ";" 
                        + STRING(res-line.name, "x(16)")        + ";" 
                        + STRING(res-line.NAME, "x(16)")        + ";" .
  IF res-line.was-status = 0 THEN   
    reslin-queasy.char3 = reslin-queasy.char3 + STRING(" NO", "x(3)") + ";" .
  ELSE reslin-queasy.char3 = reslin-queasy.char3 + STRING("YES", "x(3)") + ";" .
   
  reslin-queasy.char3 = reslin-queasy.char3 + STRING("   ", "x(3)") + ";" .
  reslin-queasy.date2 = TODAY.   
  reslin-queasy.number2 = TIME.   
   
  RELEASE reslin-queasy.   
   
END.   
  
  
  
PROCEDURE add-keycard:   
DEFINE VARIABLE maxkey AS INTEGER INITIAL 2 NO-UNDO.   
DEFINE VARIABLE errcode AS INTEGER.   
DEFINE VARIABLE i AS INTEGER.   
DEFINE VARIABLE anz0 AS INTEGER.   
DEFINE VARIABLE answer AS LOGICAL INITIAL YES.   
   
  FIND FIRST htparam WHERE paramnr = 926 NO-LOCK.   
  anz0 = htparam.finteger.   
  FIND FIRST htparam WHERE paramnr = 927 NO-LOCK.   
  IF htparam.finteger NE 0 THEN maxkey = htparam.finteger.   
   
  msg-str = msg-str + CHR(2)  
          + translateExtended ("The Keycard has been created (Qty =",lvCAREA,"")  
          + " " + STRING(res-line.betrieb-gast) + ") "  
          + translateExtended ("and can be replaced now.",lvCAREA,"").  
   
  /*MTDO i = 1 TO res-line.betrieb-gast:   
    IF i = 1 AND res-line.resstatus NE 11 AND res-line.resstatus NE 13 THEN   
      RUN keycard.w(res-line.resnr, res-line.reslinnr, "", OUTPUT errcode).   
    ELSE  RUN keycard.w(res-line.resnr, res-line.reslinnr, "cardtype=2",   
      OUTPUT errcode).   
  END.*/  
END.   
