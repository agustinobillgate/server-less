/* Delete OR cancel Reservation Line Records */ 
 
DEFINE INPUT PARAMETER pvILanguage  AS INTEGER NO-UNDO.
DEFINE INPUT  PARAMETER res-mode    AS CHAR.    /* "delete" OR "cancel" */ 
DEFINE INPUT  PARAMETER resnr       AS INTEGER. 
DEFINE INPUT  PARAMETER reslinnr    AS INTEGER. 
DEFINE INPUT  PARAMETER user-init   AS CHAR.
DEFINE INPUT  PARAMETER cancel-str  AS CHAR.
DEFINE OUTPUT PARAMETER del-mainres AS LOGICAL INITIAL NO. 
DEFINE OUTPUT PARAMETER msg-str     AS CHAR.

DEFINE VARIABLE ci-date             AS DATE NO-UNDO. 
DEFINE VARIABLE name1               AS CHAR NO-UNDO. 

DEFINE VARIABLE datum AS DATE.
DEFINE VARIABLE upto-date AS DATE.
DEFINE VARIABLE i           AS INT INIT 0.
DEFINE VARIABLE iftask      AS CHAR INIT "".
DEFINE VARIABLE origcode    AS CHAR INIT "".
DEFINE VARIABLE do-it       AS LOGICAL INIT NO.
DEFINE VARIABLE cat-flag    AS LOGICAL INIT NO.
DEFINE VARIABLE roomnr      AS INT INIT 0.

DEFINE VARIABLE priscilla-active    AS LOGICAL INIT YES NO-UNDO.

DEFINE BUFFER qsy   FOR queasy.
DEFINE BUFFER zbuff FOR zimkateg.
 
DEFINE BUFFER rline FOR res-line.

{ supertransbl.i }
DEF VAR lvCAREA AS CHAR INITIAL "del-resline". 
/**********  MAIN LOGIC  **********/ 
   
/*MASDOD 040723 trap log issue delete res-line*/
MESSAGE "TrapLog " + 
        " res-mode: " +  res-mode + 
        " resnr: " + string(resnr) +     
        " reslinnr: " + string(reslinnr) +
        " user-init: " + string(user-init) +
        " cancel-str: " + string(cancel-str) 
    VIEW-AS ALERT-BOX INFO BUTTONS OK.
 
FIND FIRST htparam WHERE paramnr = 87 NO-LOCK. 
ci-date = htparam.fdate. 
 

IF (res-mode = "cancel" OR res-mode = "delete") THEN 
DO TRANSACTION: 
  
  FIND FIRST res-line WHERE res-line.resnr = resnr AND 
      res-line.reslinnr = reslinnr NO-LOCK. 

  /*FDL Oct 13, 2022 => Ticket B1B3A0 - Create Reservation Log*/
  CREATE reslin-queasy.
  ASSIGN
      reslin-queasy.key       = "ResChanges"
      reslin-queasy.resnr     = res-line.resnr 
      reslin-queasy.reslinnr  = res-line.reslinnr 
      reslin-queasy.date2     = TODAY 
      reslin-queasy.number2   = TIME
  .

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
                      + STRING(user-init) + ";" 
                      + STRING(user-init) + ";" 
                      + STRING(TODAY) + ";" 
                      + STRING(TODAY) + ";" 
                      + STRING(res-line.name) + ";" 
                      + STRING(cancel-str) + ";" /*NC - 06/04/23 cancel can from CM tiket no 3B401D*/
                      + STRING(" ") + ";" 
                      + STRING(" ") + ";"
                      . 

  FIND CURRENT reslin-queasy NO-LOCK.
  RELEASE reslin-queasy. 

  /*FT update queasy availability booking engine*/
  DO i = 1 TO NUM-ENTRIES(res-line.zimmer-wunsch,";") - 1:
    iftask = ENTRY(i, res-line.zimmer-wunsch, ";").
    IF SUBSTR(iftask,1,10) = "$OrigCode$" THEN 
    DO:
      origcode  = SUBSTR(iftask,11).
      LEAVE.
    END.
  END. 

  FIND FIRST queasy WHERE queasy.KEY = 152 NO-LOCK NO-ERROR.
  IF AVAILABLE queasy THEN cat-flag = YES.

  FIND FIRST zbuff WHERE zbuff.zikatnr = res-line.zikatnr NO-LOCK NO-ERROR.
  IF AVAILABLE zbuff THEN
  DO:
    IF cat-flag THEN roomnr = zbuff.typ.
    ELSE roomnr = zbuff.zikatnr.
  END.

  IF res-line.ankunft = res-line.abreise THEN upto-date = res-line.abreise .
  ELSE upto-date = res-line.abreise  - 1. 
  DO datum = res-line.ankunft TO upto-date:
    FIND FIRST queasy WHERE queasy.KEY = 171 AND queasy.date1 = datum
        AND queasy.number1 = roomnr AND queasy.char1 = "" NO-LOCK NO-ERROR.
    IF AVAILABLE queasy AND queasy.logi1 = NO AND queasy.logi2 = NO THEN
    DO:
        /* FDL Comment => stack trace Mambruk Anyer Serang
        FIND FIRST qsy WHERE RECID(qsy) = RECID(queasy) EXCLUSIVE-LOCK NO-ERROR.
        IF AVAILABLE qsy THEN
        DO:
            qsy.logi2 = YES.
            FIND CURRENT qsy NO-LOCK.
            RELEASE qsy.
        END.
        */
        /*FDL April 18, 2024 => stack trace Mambruk Anyer Serang*/
        FIND CURRENT queasy EXCLUSIVE-LOCK.
        queasy.logi2 = YES.
        FIND CURRENT queasy NO-LOCK.
        RELEASE queasy.
    END. 
    
    IF origcode NE "" THEN
    DO:
        FIND FIRST queasy WHERE queasy.KEY = 171 AND queasy.date1 = datum
            AND queasy.number1 = roomnr AND queasy.char1 = origcode NO-LOCK NO-ERROR.
        IF AVAILABLE queasy AND queasy.logi1 = NO AND queasy.logi2 = NO THEN
        DO:
            /* FDL Comment => stack trace Mambruk Anyer Serang
            FIND FIRST qsy WHERE RECID(qsy) = RECID(queasy) EXCLUSIVE-LOCK NO-ERROR.
            IF AVAILABLE qsy THEN
            DO:
                qsy.logi2 = YES.
                FIND CURRENT qsy NO-LOCK.
                RELEASE qsy.
            END.
            */
            /*FDL April 18, 2024 => stack trace Mambruk Anyer Serang*/
            FIND CURRENT queasy EXCLUSIVE-LOCK.
            queasy.logi2 = YES.
            FIND CURRENT queasy NO-LOCK.
            RELEASE queasy.
        END.
    END.
  END.
  /*end FT*/
  
  name1 = res-line.NAME. 
  IF res-line.zinr NE "" THEN
  DO:
      FIND FIRST rline WHERE rline.active-flag = 0
        AND rline.memozinr MATCHES("*;*")
        AND ENTRY(2, rline.memozinr,";") = res-line.zinr
        AND NOT rline.ankunft GE res-line.abreise 
        AND NOT rline.abreise LE res-line.ankunft 
        AND rline.resnr NE res-line.resnr 
        AND rline.zinr NE res-line.zinr NO-LOCK NO-ERROR.
      IF NOT AVAILABLE rline THEN
      FIND FIRST rline WHERE rline.active-flag = 1
        AND rline.memozinr MATCHES("*;*")
        AND ENTRY(2, rline.memozinr,";") = res-line.zinr
        AND rline.resnr NE res-line.resnr 
        AND rline.zinr  NE res-line.zinr NO-LOCK NO-ERROR.
    IF AVAILABLE rline THEN
    DO:
      msg-str = msg-str + CHR(2) + "&W"
              + "Reservation found with Memo RmNo =" + " " + res-line.zinr.
    END.
  END.

  IF (res-mode = "cancel") AND (res-line.resstatus LE 2 OR res-line.resstatus = 5) 
    /* AND (res-line.zipreis GT 0) */ /* 16/02/2009 */ 
  THEN 
  DO: 
      FIND FIRST zinrstat WHERE zinrstat.zinr = "CancRes" 
        AND zinrstat.datum = ci-date EXCLUSIVE NO-ERROR. 
      IF NOT AVAILABLE zinrstat THEN 
      DO: 
        CREATE zinrstat. 
        ASSIGN 
          zinrstat.datum = ci-date 
          zinrstat.zinr = "CancRes". 
      END. 
      zinrstat.zimmeranz = zinrstat.zimmeranz + res-line.zimmeranz. 
        zinrstat.personen = zinrstat.personen 
            + res-line.zimmeranz * res-line.erwachs.
      FIND CURRENT zinrstat NO-LOCK.
  END. 
 
  IF (res-line.resstatus LE 2 OR res-line.resstatus = 5)
      AND res-line.zinr NE "" THEN
  DO:
      FIND FIRST outorder WHERE outorder.zinr = res-line.zinr
          AND outorder.betriebsnr = res-line.resnr NO-LOCK NO-ERROR.
      IF AVAILABLE outorder THEN
      DO:
          FIND CURRENT outorder EXCLUSIVE-LOCK NO-ERROR.
          DELETE outorder.
          RELEASE outorder.
      END.
  END.
  
  RUN release-zinr(res-line.zinr). 
  RUN min-resplan. 
  FIND CURRENT res-line EXCLUSIVE-LOCK. 
  IF res-mode = "delete" THEN 
  DO: 
      IF priscilla-active THEN
      DO:
          RUN intevent-1.p(15, res-line.zinr, "Priscilla", res-line.resnr, res-line.reslinnr). 
      END.

    /*FOR EACH rline WHERE rline.resnr = res-line.resnr
      AND rline.l-zuordnung[3] = 1
      AND rline.kontakt-nr = reslinnr EXCLUSIVE-LOCK:
      DELETE rline.
    END.

    FOR EACH reslin-queasy WHERE reslin-queasy.key = "arrangement" 
      AND reslin-queasy.resnr = resnr 
      AND reslin-queasy.reslinnr = reslinnr EXCLUSIVE-LOCK: 
      delete reslin-queasy. 
    END. 
    
    FOR EACH reslin-queasy WHERE key = "ResChanges" 
      AND reslin-queasy.resnr = resnr 
      AND reslin-queasy.reslinnr = reslinnr EXCLUSIVE-LOCK: 
      delete reslin-queasy. 
    END. 
    
    FOR EACH reslin-queasy WHERE key = "fargt-line" 
      AND reslin-queasy.resnr = resnr 
      AND reslin-queasy.reslinnr = reslinnr EXCLUSIVE-LOCK: 
      delete reslin-queasy. 
    END. 
    
    FOR EACH reslin-queasy WHERE reslin-queasy.key = "flag" 
      AND reslin-queasy.resnr = resnr 
      AND reslin-queasy.reslinnr = reslinnr:
      DELETE reslin-queasy. 
    END.

    FOR EACH messages WHERE messages.resnr = res-line.resnr 
      AND messages.reslinnr = res-line.reslinnr: 
      DELETE messages.
    END. 
    
    FOR EACH fixleist WHERE fixleist.resnr = resnr 
      AND fixleist.reslinnr = reslinnr EXCLUSIVE-LOCK: 
      delete fixleist. 
    END. 
    
    FIND FIRST gentable WHERE gentable.key = "reservation" 
      AND gentable.number1 = resnr 
      AND gentable.number2 = res-line.reslinnr EXCLUSIVE-LOCK NO-ERROR.
    IF AVAILABLE gentable THEN DELETE gentable.
        
    /*Begin Eko*/
    FIND FIRST reservation WHERE reservation.resnr = resnr EXCLUSIVE-LOCK NO-ERROR.
    IF AVAILABLE reservation THEN DO:
        reservation.vesrdepot2 = cancel-str.
    END.
    FIND CURRENT reservation NO-ERROR.
    /*End Eko*/

    DELETE res-line. FT delete = cancel*/

    ASSIGN 
      res-line.betrieb-gastpay  = res-line.resstatus
      res-line.resstatus        = 99 
      res-line.active-flag      = 2  
      res-line.cancelled        = ci-date
      res-line.cancelled-id     = user-init 
         + ";" + STRING(TODAY) + "-" + STRING(TIME,"HH:MM:SS") 
         + ";" + res-line.zinr
      res-line.zinr             = "" 
    . 
    FIND CURRENT res-line NO-LOCK. 
    
    FOR EACH rline WHERE rline.resnr = res-line.resnr
      AND rline.l-zuordnung[3] = 1
      AND rline.kontakt-nr = reslinnr EXCLUSIVE-LOCK:
      ASSIGN 
        rline.zinr             = "" 
        rline.betrieb-gastpay  = rline.resstatus
        rline.resstatus        = 99
        rline.active-flag      = 2 
        rline.cancelled        = ci-date 
        rline.cancelled-id     = user-init 
          + ";" + STRING(TODAY) + "-" + STRING(TIME,"HH:MM:SS").
      RELEASE rline.
    END.

    /*Begin Eko add cancel str*/
    FIND FIRST reservation WHERE reservation.resnr = resnr NO-LOCK NO-ERROR.
    IF AVAILABLE reservation THEN DO:
        FIND CURRENT reservation EXCLUSIVE-LOCK NO-ERROR.
        ASSIGN reservation.vesrdepot2 = cancel-str.
        FIND CURRENT reservation NO-ERROR.
    END.
    /*End Eko*/

  END. 
  ELSE 
  DO: 
    IF priscilla-active THEN
    DO:
      RUN intevent-1.p(14, res-line.zinr, "Priscilla", res-line.resnr, res-line.reslinnr). 
    END.

    ASSIGN 
      res-line.betrieb-gastpay  = res-line.resstatus
      res-line.resstatus        = 9 
      res-line.active-flag      = 2  
      res-line.cancelled        = ci-date
      res-line.cancelled-id     = user-init 
         + ";" + STRING(TODAY) + "-" + STRING(TIME,"HH:MM:SS") 
         + ";" + res-line.zinr
      res-line.zinr             = "" 
    . 
    FIND CURRENT res-line NO-LOCK. 
    
    FOR EACH rline WHERE rline.resnr = res-line.resnr
      AND rline.l-zuordnung[3] = 1
      AND rline.kontakt-nr = reslinnr EXCLUSIVE-LOCK:
      ASSIGN 
        rline.zinr             = "" 
        rline.betrieb-gastpay  = rline.resstatus
        rline.resstatus        = 9 
        rline.active-flag      = 2 
        rline.cancelled        = ci-date 
        rline.cancelled-id     = user-init 
          + ";" + STRING(TODAY) + "-" + STRING(TIME,"HH:MM:SS").
      RELEASE rline.
    END.

    /*Begin Eko add cancel str*/
    FIND FIRST reservation WHERE reservation.resnr = resnr NO-LOCK NO-ERROR.
    IF AVAILABLE reservation THEN DO:
        FIND CURRENT reservation EXCLUSIVE-LOCK NO-ERROR.
        reservation.vesrdepot2 = cancel-str.
        FIND CURRENT reservation NO-ERROR.
    END.
    /*End Eko*/
  END. 
  /*
  FIND FIRST res-line WHERE res-line.resnr = resnr /* AND 
    res-line.active-flag NE 2 */ NO-LOCK NO-ERROR. 
*/
  FIND FIRST res-line WHERE res-line.resnr = resnr AND 
    res-line.resstatus NE 9 AND res-line.resstatus NE 99 
    NO-LOCK NO-ERROR. 

  IF NOT AVAILABLE res-line THEN 
  DO: 
    del-mainres = YES. 
    FIND FIRST reservation WHERE reservation.resnr = resnr EXCLUSIVE-LOCK. 
    /*FT delete = cancel IF res-mode = "cancel" THEN */
    DO: 
      reservation.activeflag = 1. 
      IF cancel-str NE "" THEN 
        ASSIGN reservation.vesrdepot2 = cancel-str. 
      FIND CURRENT reservation NO-LOCK. 
      FIND FIRST guest WHERE guest.gastnr = reservation.gastnr EXCLUSIVE-LOCK. 
      guest.stornos = guest.stornos + 1. 
      FIND CURRENT guest NO-LOCK. 
    END. 
    /*FTdelete=cancel ELSE IF res-mode = "delete" THEN 
    DO: 
      FIND FIRST reslin-queasy WHERE reslin-queasy.key = "rate-prog" 
        AND reslin-queasy.number1 = resnr 
        AND reslin-queasy.number2 = 0 AND reslin-queasy.char1 = "" 
        AND reslin-queasy.reslinnr = 1 USE-INDEX argt_ix 
        EXCLUSIVE-LOCK NO-ERROR. 
      IF AVAILABLE reslin-queasy THEN delete reslin-queasy. 
      delete reservation. 
    END.*/ 
 
/* try TO delete the master bill, IF it exists */ 
    FIND FIRST bill WHERE bill.resnr = resnr AND bill.reslinnr = 0 
      AND bill.zinr = "" NO-LOCK NO-ERROR. 
    IF AVAILABLE bill THEN DO: 
        FIND CURRENT bill EXCLUSIVE-LOCK NO-ERROR.
        DELETE bill.
        RELEASE bill.
    END.
    FIND FIRST master WHERE master.resnr = resnr AND master.flag = 0 NO-LOCK NO-ERROR. 
    IF AVAILABLE master THEN DO:
        FIND CURRENT master EXCLUSIVE-LOCK NO-ERROR.
        DELETE master. 
        RELEASE master.
    END.
    FOR EACH mast-art WHERE mast-art.resnr = resnr AND mast-art.reslinnr EQ 1: 
      DELETE mast-art. 
    END. 
  END. 
  IF res-mode = "delete" THEN 
  DO:       
    FIND FIRST bediener WHERE bediener.userinit = user-init NO-LOCK. 
    CREATE res-history. 
    ASSIGN 
      res-history.nr = bediener.nr 
      res-history.datum = ci-date 
      res-history.zeit = TIME 
      res-history.aenderung = "Delete ResLine: ResNo " + STRING(resnr) + " No " 
        + STRING(reslinnr) + " - " + name1 
      res-history.action = "Reservation"
    . 
    FIND CURRENT res-history NO-LOCK. 
    RELEASE res-history. 
  END.   
END. 

/**************** PROCEDURES  ****************/ 
 
/*{ res-zimplan.i } */
PROCEDURE release-zinr:
DEFINE INPUT PARAMETER new-zinr LIKE zimmer.zinr.
DEFINE VARIABLE res-recid1 AS INTEGER.
DEFINE BUFFER res-line1 FOR res-line.
DEFINE BUFFER res-line2 FOR res-line.
DEFINE BUFFER rline FOR res-line.
DEFINE VARIABLE beg-datum AS DATE.
DEFINE VARIABLE answer AS LOGICAL.
DEFINE VARIABLE parent-nr AS INTEGER.

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
      FIND FIRST res-line1 WHERE res-line1.resnr = resnr
        AND res-line1.zinr = rline.zinr AND res-line1.resstatus = 11
        NO-LOCK NO-ERROR.
      IF AVAILABLE res-line1 THEN 
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

      IF rline.resstatus = 6 AND (rline.zinr NE new-zinr) THEN
      DO TRANSACTION:
        FIND FIRST res-line1 WHERE res-line1.resnr = resnr
          AND res-line1.zinr = rline.zinr AND res-line1.resstatus = 13 
          NO-LOCK NO-ERROR.
        IF AVAILABLE res-line1 THEN 
        DO:       
          FOR EACH res-line2 WHERE res-line2.resnr = resnr
              AND res-line2.zinr = rline.zinr AND res-line2.resstatus = 13 
              EXCLUSIVE-LOCK:
            FIND FIRST bill WHERE bill.resnr = resnr
              AND bill.reslinnr = res-line2.reslinnr AND bill.flag = 0 
              AND bill.zinr = res-line2.zinr EXCLUSIVE-LOCK.
            bill.zinr = new-zinr.
            parent-nr = bill.parent-nr.
            FIND CURRENT bill NO-LOCK.
            FOR EACH bill WHERE bill.resnr = resnr 
              AND bill.parent-nr = parent-nr AND bill.flag = 0
              AND bill.zinr = res-line2.zinr EXCLUSIVE-LOCK:
              bill.zinr = new-zinr.
              RELEASE bill.
            END.
            res-line2.zinr = new-zinr.
            RELEASE res-line2.
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

PROCEDURE min-resplan:
  DEFINE VARIABLE curr-date AS DATE.
  DEFINE VARIABLE beg-datum AS DATE.
  DEFINE VARIABLE i AS INTEGER.
  DEFINE BUFFER rline FOR res-line.
  FIND FIRST rline WHERE rline.resnr = resnr 
      AND rline.reslinnr = reslinnr NO-LOCK.
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
      RELEASE resplan.
      curr-date = curr-date + 1.
    END.
  END.
END.
