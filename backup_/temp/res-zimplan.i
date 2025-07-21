
/*MT 20/07/12 -->change zinr format */

/* PROCEDUREs FOR updating Resplan AND Zimplan   */

PROCEDURE assign-zinr:
  DEFINE INPUT  PARAMETER resline-recid AS INTEGER.
  DEFINE INPUT  PARAMETER ankunft AS DATE.
  DEFINE INPUT  PARAMETER abreise AS DATE.
  DEFINE INPUT  PARAMETER zinr LIKE zimmer.zinr. /*MT 20/07/12 change zinr format */
  DEFINE INPUT  PARAMETER resstatus AS INTEGER.
  DEFINE INPUT  PARAMETER gastnrmember AS INTEGER.
  DEFINE INPUT  PARAMETER bemerk AS CHAR.
  DEFINE INPUT  PARAMETER name AS CHAR.
  DEFINE output PARAMETER room-blocked AS LOGICAL INITIAL NO.
  
  DEFINE VARIABLE sharer AS LOGICAL.
  DEFINE VARIABLE curr-datum AS DATE.
  DEFINE VARIABLE beg-datum AS DATE.
  DEFINE VARIABLE res-recid AS INTEGER.
  DEFINE BUFFER res-line1 FOR res-line.
  DEFINE BUFFER zimplan1  FOR zimplan.
  DEFINE BUFFER resline   FOR res-line.

  DEFINE BUFFER zbuff FOR zimplan.
    
  FIND FIRST htparam WHERE htparam.paramnr = 87 NO-LOCK.

  sharer = (resstatus = 11) OR (resstatus = 13).
  if zinr NE "" AND NOT sharer THEN
  DO:
    if res-mode = "inhouse" THEN beg-datum = htparam.fdate.
    ELSE beg-datum = ankunft.
    room-blocked = no.
    do curr-datum = beg-datum TO (abreise - 1): 
      FIND FIRST zimplan1 WHERE zimplan1.datum = curr-datum
          AND zimplan1.zinr = zinr NO-LOCK NO-ERROR.
      if (NOT AVAILABLE zimplan1) AND (NOT room-blocked) THEN 
      DO:
        CREATE zimplan.
        zimplan.datum = curr-datum.
        zimplan.zinr = zinr.
        zimplan.res-recid = resline-recid.
        zimplan.gastnrmember = gastnrmember.
        zimplan.bemerk = bemerk.
        zimplan.resstatus = resstatus.
        zimplan.name = name.
        FIND CURRENT zimplan NO-LOCK.
        RELEASE zimplan.
      END.
      ELSE 
      DO: 
/* it is possible that it is the zimplan of it's own res-line exists, 
   THEN room-blocked is false */       
        IF AVAILABLE zimplan1 AND (zimplan1.res-recid NE resline-recid) THEN
        DO:
          FIND FIRST resline WHERE RECID(resline) = zimplan1.res-recid 
            NO-LOCK NO-ERROR.
          IF AVAILABLE resline AND resline.zinr = zinr 
            AND resline.active-flag LT 2 
            AND resline.ankunft LE zimplan1.datum
            AND resline.abreise GT zimplan1.datum THEN
          DO:
            curr-datum = abreise.
            room-blocked = yes.
          END.
          ELSE
          DO: /* try to fix the room plan by deleting wrong zimplan records */
            FIND CURRENT zimplan1 EXCLUSIVE-LOCK.
            zimplan1.res-recid = resline-recid.
            zimplan1.gastnrmember = gastnrmember.
            zimplan1.bemerk = bemerk.
            zimplan1.resstatus = resstatus.
            zimplan1.name = name.
            FIND CURRENT zimplan1 NO-LOCK.
            RELEASE zimplan1.
          END.
        END.
      END.
    END.
    if room-blocked THEN
    DO:
      do curr-datum = beg-datum TO (abreise - 1): 
        FIND FIRST zimplan WHERE zimplan.datum = curr-datum
          AND zimplan.zinr = zinr 
          AND zimplan.res-recid = resline-recid NO-LOCK NO-ERROR.
        IF AVAILABLE zimplan THEN 
        DO:
          FIND FIRST zbuff WHERE RECID(zbuff) = RECID(zimplan) EXCLUSIVE-LOCK.
          DELETE zbuff.
          RELEASE zbuff.
        END.
      END.
/*
      HIDE MESSAGE NO-PAUSE.
      MESSAGE "RoomNo " + zinr 
        + " already blocked; room assignment not possible."
        VIEW-AS ALERT-BOX INFORMATION.
*/
    END.
    ELSE 
    DO:
      IF resstatus = 6 OR resstatus = 13 THEN
      DO:
        FIND FIRST zimmer WHERE zimmer.zinr = zinr EXCLUSIVE-LOCK.
        IF abreise GT htparam.fdate AND zimmer.zistatus = 0 
          THEN zimmer.zistatus = 5. /* occupied clean */
        ELSE IF abreise GT htparam.fdate AND zimmer.zistatus = 3 /* ED */
          THEN zimmer.zistatus = 4. /* occupied dirty */
        ELSE if abreise = htparam.fdate THEN
        DO:
          FIND FIRST res-line1 WHERE RECID(res-line1) NE resline-recid 
            AND res-line1.abreise = abreise 
            AND res-line1.zinr = zimmer.zinr AND
            (res-line1.resstatus = 6 OR res-line1.resstatus = 13) 
            NO-LOCK NO-ERROR.
          IF NOT AVAILABLE res-line1 THEN zimmer.zistatus = 3. /* ED */
        END.
/*      zimmer.bediener-nr-stat = 0.   */
        FIND CURRENT zimmer NO-LOCK.

/*      delete queuing room if exists */
        FIND FIRST queasy WHERE queasy.KEY = 162
          AND queasy.char1 = zimmer.zinr NO-ERROR.
        IF AVAILABLE queasy THEN DELETE queasy. 

        RELEASE zimmer.
      END.
    END.
  END.
END.

PROCEDURE release-zinr:
DEFINE INPUT PARAMETER new-zinr LIKE zimmer.zinr. /*MT 20/07/12 change zinr format */
DEFINE VARIABLE res-recid1 AS INTEGER.
DEFINE VARIABLE beg-datum AS DATE.
DEFINE VARIABLE answer AS LOGICAL.
DEFINE VARIABLE parent-nr AS INTEGER.

DEFINE BUFFER res-line1 FOR res-line.
DEFINE BUFFER res-line2 FOR res-line.
DEFINE BUFFER rline     FOR res-line.
DEFINE BUFFER rline2    FOR res-line.
DEFINE BUFFER bbuff     FOR bill.

  FIND FIRST htparam WHERE htparam.paramnr = 87 NO-LOCK.

  FIND FIRST rline WHERE rline.resnr = resnr 
      AND rline.reslinnr = reslinnr NO-LOCK.
  if rline.zinr NE "" THEN
  DO: 
    beg-datum = rline.ankunft. 
    res-recid1 = 0.

    if res-mode = "delete" OR res-mode = "cancel" 
      AND rline.resstatus = 1 THEN 
    DO TRANSACTION:
      FIND FIRST res-line1 WHERE res-line1.resnr = resNr
        AND res-line1.zinr = rline.zinr AND res-line1.resstatus = 11
        NO-LOCK NO-ERROR.
      if AVAILABLE res-line1 THEN 
      DO:
        FIND CURRENT res-line1 EXCLUSIVE-LOCK.
        res-line1.resstatus = 1.
        FIND CURRENT res-line1 NO-LOCK.
        res-recid1 = RECID(res-line1).
      END.
    END.    
    if res-mode = "inhouse" THEN 
    DO:
      answer = yes.
      beg-datum = htparam.fdate.

      if rline.resstatus = 6 AND (rline.zinr NE new-zinr) THEN
      DO TRANSACTION:
        FIND FIRST res-line1 WHERE res-line1.resnr = resNr
          AND res-line1.zinr = rline.zinr AND res-line1.resstatus = 13 
          NO-LOCK NO-ERROR.
        if AVAILABLE res-line1 THEN 
/*        
        DO:
          HIDE MESSAGE NO-PAUSE.
          MESSAGE "Room-change FOR the RoomSharer too?"         
            VIEW-AS ALERT-BOX question buttons yes-no update answer.
        END.
        if answer = no THEN 
        DO:
          FIND CURRENT res-line1 EXCLUSIVE-LOCK.
          res-line1.resstatus = 6.
          FIND CURRENT res-line1 NO-LOCK.
          res-recid1 = RECID(res-line1).
        END.
        ELSE 
*/
        DO:       
          FOR EACH res-line2 WHERE res-line2.resnr = resnr
              AND res-line2.zinr = rline.zinr AND res-line2.resstatus = 13 
              NO-LOCK:
            FIND FIRST bill WHERE bill.resnr = resnr
              AND bill.reslinnr = res-line2.reslinnr AND bill.flag = 0 
              AND bill.zinr = res-line2.zinr EXCLUSIVE-LOCK.
            ASSIGN
                bill.zinr = new-zinr.
                parent-nr  = bill.parent-nr
            .
            FIND CURRENT bill NO-LOCK.
            FOR EACH bill WHERE bill.resnr = resnr 
              AND bill.parent-nr = parent-nr AND bill.flag = 0
              AND bill.zinr = res-line2.zinr NO-LOCK:
              FIND FIRST bbuff WHERE RECID(bbuff) = RECID(bill)
                  EXCLUSIVE-LOCK.
              bbuff.zinr = new-zinr.
              FIND CURRENT bbuff NO-LOCK.
              RELEASE bbuff.
            END.
            FIND FIRST rline2 WHERE RECID(rline2) = RECID(res-line2)
                EXCLUSIVE-LOCK.
            rline2.zinr = new-zinr.
            FIND CURRENT rline2 NO-LOCK.
            RELEASE rline2.
          END.
          FIND FIRST zimmer WHERE zimmer.zinr = rline.zinr EXCLUSIVE-LOCK.
          zimmer.zistatus = 2.
          FIND CURRENT zimmer NO-LOCK.
        END.
      END.
    END.
    DO:
      FOR EACH zimplan WHERE zimplan.zinr = rline.zinr 
          AND zimplan.datum GE beg-datum
          AND zimplan.datum LT rline.abreise EXCLUSIVE-LOCK:
        IF res-recid1 NE 0 THEN zimplan.res-recid = res-recid1.
        ELSE DELETE zimplan.
        RELEASE zimplan.
      END.
    END.
  END.
END. 
 
PROCEDURE add-resplan:
  DEFINE VARIABLE curr-date AS DATE.
  DEFINE VARIABLE beg-datum AS DATE.
  DEFINE VARIABLE end-datum AS DATE.
  DEFINE VARIABLE i AS INTEGER.
  DEFINE VARIABLE anz AS INTEGER.
  DEFINE BUFFER rline FOR res-line.

  DEFINE BUFFER rbuff FOR resplan.

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
          resplan.datum         = curr-date.
          resplan.zikatnr       = zimkateg.zikatnr.
          anz                   = resplan.anzzim[i] + rline.zimmeranz.
          resplan.anzzim[i]     = anz.
        END.
        anz = resplan.anzzim[i] + rline.zimmeranz.
        FIND FIRST rbuff WHERE RECID(rbuff) = RECID(resplan) EXCLUSIVE-LOCK.
        rbuff.anzzim[i] = anz.
        FIND CURRENT rbuff NO-LOCK.
        RELEASE rbuff.
      END.
    END.
  END.
END.

PROCEDURE min-resplan:
  DEFINE VARIABLE curr-date AS DATE.
  DEFINE VARIABLE beg-datum AS DATE.
  DEFINE VARIABLE i AS INTEGER.
  DEFINE BUFFER rline FOR res-line.
  DEFINE BUFFER rbuff FOR resplan.

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
    curr-date = beg-datum.
    do while curr-date GE beg-datum AND curr-date LT rline.abreise:
      FIND FIRST resplan WHERE resplan.zikatnr = zimkateg.zikatnr
        AND resplan.datum = curr-date NO-LOCK NO-ERROR.
      IF AVAILABLE resplan THEN 
      DO TRANSACTION:
        FIND FIRST rbuff WHERE RECID(rbuff) = RECID(resplan) EXCLUSIVE-LOCK.
        rbuff.anzzim[i] = rbuff.anzzim[i] - rline.zimmeranz.
        FIND CURRENT rbuff NO-LOCK.
        RELEASE rbuff.
      END.
      curr-date = curr-date + 1.
    END.
  END.
END.

PROCEDURE rmchg-sharer:
DEFINE INPUT PARAMETER act-zinr LIKE zimmer.zinr. /*MT 20/07/12 change zinr format */
DEFINE INPUT PARAMETER new-zinr LIKE zimmer.zinr. /*MT 20/07/12 change zinr format */
DEFINE VARIABLE res-recid1 AS INTEGER.
DEFINE BUFFER res-line1 FOR res-line.
DEFINE BUFFER res-line2 FOR res-line.
DEFINE VARIABLE beg-datum AS DATE.
DEFINE VARIABLE answer AS LOGICAL.
DEFINE VARIABLE parent-nr AS INTEGER.
DEFINE VARIABLE curr-datum AS DATE.
DEFINE VARIABLE end-datum AS DATE.

DEFINE BUFFER new-zkat FOR zimkateg.
DEFINE BUFFER bbuff    FOR bill.
DEFINE BUFFER rbuff    FOR resplan.

  FIND FIRST htparam WHERE htparam.paramnr = 87 NO-LOCK.
  beg-datum  = htparam.fdate.
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
                    FIND FIRST rbuff WHERE RECID(rbuff) = RECID(resplan) EXCLUSIVE-LOCK.
                    rbuff.anzzim[13] = rbuff.anzzim[13] - 1.
                    FIND CURRENT rbuff NO-LOCK.
                    RELEASE rbuff.
                 END.
                 FIND FIRST resplan WHERE resplan.zikatnr = new-zkat.zikatnr
                    AND resplan.datum = curr-datum NO-LOCK NO-ERROR.
                 IF NOT AVAILABLE resplan THEN
                 DO:
                    CREATE resplan.
                    resplan.datum = curr-datum.
                    resplan.zikatnr = new-zkat.zikatnr.
                    resplan.anzzim[13] = resplan.anzzim[13] + 1.
                 END.
                 ELSE DO:
                     FIND FIRST rbuff WHERE RECID(rbuff) = RECID(resplan) EXCLUSIVE-LOCK.
                     rbuff.anzzim[13] = rbuff.anzzim[13] + 1.
                     FIND CURRENT rbuff NO-LOCK.
                     RELEASE rbuff.
                 END.                 
              END.
           END.  
            
           FOR EACH bill WHERE bill.resnr = resnr 
              AND bill.parent-nr = res-line2.reslinnr AND bill.flag = 0
              AND bill.zinr = res-line2.zinr EXCLUSIVE-LOCK:
             bill.zinr = new-zinr.
             RELEASE bill.
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
