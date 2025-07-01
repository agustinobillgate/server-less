
/*MT 05/03/14 --> add history for vacant dirty status when c/o */

DEFINE INPUT PARAMETER pvILanguage  AS INTEGER NO-UNDO.
DEFINE INPUT PARAMETER case-type    AS INTEGER NO-UNDO.
DEFINE INPUT PARAMETER resnr        AS INTEGER NO-UNDO. 
DEFINE INPUT PARAMETER reslinnr     AS INTEGER NO-UNDO. 
DEFINE INPUT PARAMETER silenzio     AS LOGICAL NO-UNDO. 
DEFINE INPUT PARAMETER user-init    AS CHAR    NO-UNDO.

DEFINE OUTPUT PARAMETER co-ok       AS LOGICAL INITIAL YES.
DEFINE OUTPUT PARAMETER checked-out AS LOGICAL INITIAL NO. 
DEFINE OUTPUT PARAMETER flag-report AS LOGICAL INITIAL NO.
DEFINE OUTPUT PARAMETER msg-str     AS CHAR    INITIAL "".
/*
DEFINE VARIABLE pvILanguage  AS INTEGER INIT 1 NO-UNDO.
DEFINE VARIABLE case-type    AS INTEGER INIT 2 NO-UNDO.
DEFINE VARIABLE resnr        AS INTEGER INIT 16680 NO-UNDO. 
DEFINE VARIABLE reslinnr     AS INTEGER INIT 1 NO-UNDO. 
DEFINE VARIABLE silenzio     AS LOGICAL INIT NO NO-UNDO. 
DEFINE VARIABLE user-init    AS CHAR    INIT "01" NO-UNDO.
DEFINE VARIABLE co-ok       AS LOGICAL INITIAL YES.
DEFINE VARIABLE checked-out AS LOGICAL INITIAL NO. 
DEFINE VARIABLE flag-report AS LOGICAL INITIAL NO.
DEFINE VARIABLE msg-str     AS CHAR    INITIAL "".
*/

DEFINE VARIABLE co-date             AS DATE                 NO-UNDO.
DEFINE VARIABLE min-reslinnr        AS INTEGER INITIAL 0    NO-UNDO. 
DEFINE VARIABLE real-guest          AS LOGICAL INITIAL YES  NO-UNDO. 
DEFINE VARIABLE main-guest          AS LOGICAL              NO-UNDO.
DEFINE VARIABLE unbalanced-bill     AS LOGICAL              NO-UNDO. /*baca ke htparam*/
DEFINE VARIABLE priscilla-active    AS LOGICAL              NO-UNDO INITIAL YES.

DEFINE VARIABLE co-ankunft-int      AS INTEGER              NO-UNDO. /*Alder - Serverless - Issue 475*/
DEFINE VARIABLE abreise-date        AS DATE. /*NC - 21/02/24 #A06BFC*/

DEFINE BUFFER usr1    FOR bediener.

{SupertransBL.i} 
DEF VAR lvCAREA AS CHAR INITIAL "res-checkout". 

/*ITA 120615 --> for harris waterfront Request*/
FIND FIRST htparam WHERE htparam.paramnr = 974 NO-LOCK NO-ERROR.
unbalanced-bill = htparam.flogical.

/*ITA 130616*/
DEF VARIABLE bl-saldo  AS DECIMAL NO-UNDO.
DEFINE BUFFER tbuff FOR bill.
DEFINE BUFFER buf-rline FOR res-line.

FIND FIRST htparam WHERE paramnr = 87 NO-LOCK. 
co-date = htparam.fdate. 

FIND FIRST reservation WHERE reservation.resnr = resnr NO-LOCK NO-ERROR.
IF NOT AVAILABLE reservation THEN                                 /* Rulita 241124 | Fixing serverless issue 157 */
DO:
    msg-str = translateExtended ("No reservation found.",lvCAREA,"").
    RETURN.
END.

FIND FIRST res-line WHERE res-line.resnr = resnr 
    AND res-line.reslinnr = reslinnr NO-LOCK NO-ERROR. 
IF NOT AVAILABLE res-line THEN                                 /* Rulita 241124 | Fixing serverless issue 157 */
DO:
    msg-str = translateExtended ("No reservation member found.",lvCAREA,"").
    RETURN.
END.

IF case-type EQ 1 THEN RUN check-billstatus.
ELSE IF case-type EQ 2 THEN RUN guest-checkout.
/*NC- 15/10/19 #A06BFC*/
RUN update-queasy171.

/*FD Oct 13, 2022 => Ticket B1B3A0 - Create Reservation Log*/
FIND FIRST buf-rline WHERE buf-rline.resnr EQ resnr
    AND buf-rline.reslinnr EQ reslinnr NO-LOCK NO-ERROR.
IF AVAILABLE buf-rline THEN
DO:
    CREATE reslin-queasy.
    ASSIGN
        reslin-queasy.key       = "ResChanges"
        reslin-queasy.resnr     = buf-rline.resnr 
        reslin-queasy.reslinnr  = buf-rline.reslinnr 
        reslin-queasy.date2     = TODAY 
        reslin-queasy.number2   = TIME
    .

    reslin-queasy.char3 = STRING(buf-rline.ankunft) + ";" 
                        + STRING(buf-rline.ankunft) + ";" 
                        + STRING(buf-rline.abreise) + ";" 
                        + STRING(buf-rline.abreise) + ";" 
                        + STRING(buf-rline.zimmeranz) + ";" 
                        + STRING(buf-rline.zimmeranz) + ";" 
                        + STRING(buf-rline.erwachs) + ";" 
                        + STRING(buf-rline.erwachs) + ";" 
                        + STRING(buf-rline.kind1) + ";" 
                        + STRING(buf-rline.kind1) + ";" 
                        + STRING(buf-rline.gratis) + ";" 
                        + STRING(buf-rline.gratis) + ";" 
                        + STRING(buf-rline.zikatnr) + ";" 
                        + STRING(buf-rline.zikatnr) + ";" 
                        + STRING(buf-rline.zinr) + ";" 
                        + STRING(buf-rline.zinr) + ";" 
                        + STRING(buf-rline.arrangement) + ";" 
                        + STRING(buf-rline.arrangement) + ";"
                        + STRING(buf-rline.zipreis) + ";" 
                        + STRING(buf-rline.zipreis) + ";"
                        + STRING(user-init) + ";" 
                        + STRING(user-init) + ";" 
                        + STRING(TODAY) + ";" 
                        + STRING(TODAY) + ";" 
                        + STRING(buf-rline.name) + ";" 
                        + STRING("CHECKED-OUT") + ";"
                        + STRING(" ") + ";" 
                        + STRING(" ") + ";"
                        .      

    FIND CURRENT reslin-queasy NO-LOCK.
    RELEASE reslin-queasy. 
END.

PROCEDURE check-billstatus: 
  DEFINE VARIABLE parent-nr AS INTEGER INITIAL 0. 
  DEFINE VARIABLE co-str    AS CHAR    NO-UNDO.

  DEFINE BUFFER bill1       FOR bill. 
  DEFINE BUFFER mbill       FOR bill.
  DEFINE BUFFER resline     FOR res-line.
  DEFINE BUFFER rline       FOR res-line.  
  DEFINE BUFFER rguest      FOR guest.

  IF unbalanced-bill = NO THEN DO:
      /*
      FIND FIRST bill1 WHERE bill1.resnr = resnr AND bill1.parent-nr = reslinnr 
        AND bill1.flag = 0 AND (bill1.saldo NE 0 OR bill1.rgdruck = 0) NO-LOCK NO-ERROR. 
      */
      /*FDL April 30, 2024 => Ticket EA165C - Match With inv-checkoutBL*/
      FIND FIRST bill1 WHERE bill1.resnr EQ resnr 
        AND bill1.reslinnr EQ reslinnr 
        AND bill1.flag EQ 0 NO-LOCK NO-ERROR.      
      
      IF AVAILABLE bill1 THEN 
      DO:
        parent-nr = bill1.parent-nr.
        FOR EACH bill1 WHERE bill1.resnr = resnr AND bill1.parent-nr = parent-nr
            AND bill1.flag = 0 /* AND bill1.zinr = zinr */ /*EXCLUSIVE-LOCK*/ NO-LOCK: /*FDL Change Exclusive-Lock to No-Lock*/
        /*FDL April 30, 2024 => TIcket EA165C - Match With inv-checkoutBL*/
            FIND FIRST bill-line WHERE bill-line.rechnr EQ bill1.rechnr NO-LOCK NO-ERROR.
            IF AVAILABLE bill-line AND co-ok AND (bill1.rgdruck EQ 0 OR bill1.saldo NE 0) THEN
            DO:
              co-ok = NO.
              IF bill1.saldo NE 0 THEN 
              ASSIGN
              msg-str = translateExtended ("RoomNo",lvCAREA,"") 
                      + " " + res-line.zinr + "  -  "  
                      + translateExtended ("BillNo",lvCAREA,"") 
                      + " " + STRING(bill1.rechnr) 
                      + " " + translateExtended ("not yet balanced",lvCAREA,"") + CHR(10)
                      + translateExtended ("Check-out not possible.",lvCAREA,"")
              . 
              ELSE
              ASSIGN
              msg-str = translateExtended ("RoomNo",lvCAREA,"") 
                      + " " + res-line.zinr + "  -  " 
                      + translateExtended ("BillNo",lvCAREA,"") 
                      + " " + STRING(bill1.rechnr) 
                      + " " + translateExtended ("not yet printed",lvCAREA,"") + CHR(10)
                      + translateExtended ("Check-out not possible.",lvCAREA,"") 
              . 
            END. 
        END.
      END.
      IF NOT co-ok THEN RETURN.
  END.

  /*FDL Nov 23, 2024: Ticket 2FD3E7 1C7B52 - Preventif cause it's anomali, happened sometime*/
  FIND FIRST htparam WHERE htparam.paramnr EQ 141 NO-LOCK NO-ERROR. 
  IF AVAILABLE htparam AND htparam.fchar NE "" THEN 
  DO:
      FIND FIRST resline WHERE resline.resnr EQ resnr
          AND resline.active-flag EQ 1
          AND resline.resstatus NE 12
          AND resline.reslinnr NE reslinnr NO-LOCK NO-ERROR.
      IF NOT AVAILABLE resline THEN
      DO:
          FIND FIRST mbill WHERE mbill.resnr EQ resnr 
              AND mbill.zinr EQ "" AND mbill.flag EQ 0 NO-LOCK NO-ERROR. 
          IF AVAILABLE mbill AND mbill.saldo GT 0 THEN 
          DO: 
              FIND FIRST rguest WHERE rguest.gastnr EQ mbill.gastnr NO-LOCK NO-ERROR. 
              IF AVAILABLE rguest AND rguest.zahlungsart EQ 0 THEN 
              DO:
                  ASSIGN                      
                      co-ok      = NO 
                      msg-str    = translateExtended ("RoomNo",lvCAREA,"") 
                        + " " + res-line.zinr + "  -  " 
                        + translateExtended ("Master Bill not yet settled.",lvCAREA,"") + CHR(10)
                        + translateExtended ("Check-out not possible.",lvCAREA,"") + CHR(10).
  
                  RETURN.
              END.
          END.
      END.
  END.
  
  FIND FIRST bediener WHERE bediener.userinit = user-init NO-LOCK.

  IF res-line.abreise GT co-date THEN 
  ASSIGN
    co-ok   = SUBSTR(bediener.permissions, 70, 1) GE "2"
    co-str  = translateExtended ("EARLY Check-out",lvCAREA,"")
  . 
  ELSE 
  ASSIGN
    co-ok   = YES
    co-str  = translateExtended ("Check-out",lvCAREA,"")
  . 

  IF NOT silenzio AND co-ok THEN
  DO:      
    msg-str = "&Q" + co-str + " " 
            + res-line.NAME + CHR(10)
            + translateExtended ("ROOM",lvCAREA,"") + " " 
            + res-line.zinr + " ?". 
    FIND FIRST reslin-queasy WHERE reslin-queasy.key = "flag" 
      AND reslin-queasy.resnr = resnr 
      AND reslin-queasy.reslinnr = reslinnr 
      AND reslin-queasy.betriebsnr = 0 NO-LOCK NO-ERROR. 
    IF AVAILABLE reslin-queasy AND 
      (reslin-queasy.logi1 = YES OR reslin-queasy.logi2 = YES 
      OR reslin-queasy.logi3 = YES) THEN ASSIGN flag-report = YES.
  END.
END. 

PROCEDURE guest-checkout: 
  DEFINE VARIABLE ankunft       AS DATE. 
  DEFINE VARIABLE abreise       AS DATE. 
  DEFINE VARIABLE resstatus     AS INTEGER. 
  DEFINE VARIABLE res-recid     AS INTEGER. 
  DEFINE VARIABLE res-recid1    AS INTEGER. 
  DEFINE VARIABLE tot-umsatz    AS DECIMAL INITIAL 0. 
  DEFINE VARIABLE day-use       AS LOGICAL INITIAL NO. 
  DEFINE VARIABLE dummy-logi    AS LOGICAL. 
  DEFINE VARIABLE pax           AS INTEGER.
  DEFINE VARIABLE zinr          LIKE zimmer.zinr.
  DEFINE VARIABLE bill-date     AS DATE.

  DEFINE BUFFER bill1           FOR bill. 
  DEFINE BUFFER res-line1       FOR res-line. 
  DEFINE BUFFER res-line2       FOR res-line.
  DEFINE BUFFER rline           FOR res-line.
  DEFINE BUFFER resline         FOR res-line. 
  DEFINE BUFFER sharer          FOR res-line.
  DEFINE BUFFER rguest          FOR guest. 
  DEFINE BUFFER mbill           FOR bill.

  FIND FIRST htparam WHERE paramnr = 110 NO-LOCK. 
  bill-date = htparam.fdate. 

  ASSIGN
    zinr        = res-line.zinr
    pax         = res-line.erwachs 
    main-guest  = (res-line.resstatus = 6)
  . 
  
  IF main-guest AND (res-line.abreise GT co-date) AND NOT silenzio THEN
  DO:
    FIND FIRST sharer WHERE sharer.resnr = res-line.resnr
      AND sharer.zinr = res-line.zinr
      AND sharer.resstatus = 13 AND sharer.abreise GT co-date
      AND sharer.zipreis = 0 NO-LOCK NO-ERROR.
    IF AVAILABLE sharer THEN
    msg-str = "&W"
            + translateExtended ("Room sharer found with ZERO rate for room", lvCAREA,"")
            + " " + res-line.zinr + CHR(10)
            + translateExtended ("Change room sharer status and update the Rate.",lvCAREA,"") + CHR(10).
  END.

  IF co-date = res-line.ankunft THEN 
  DO: 
    IF res-line.l-zuordnung[3] = 1 THEN real-guest = NO.
    ELSE
    DO:
      FIND FIRST arrangement WHERE 
        arrangement.arrangement = res-line.arrangement NO-LOCK.
      FIND FIRST bill-line WHERE bill-line.departement = 0
        AND bill-line.artnr = arrangement.argt-artikelnr
        AND bill-line.bill-datum = bill-date
        AND bill-line.massnr = res-line.resnr
        AND bill-line.billin-nr = res-line.reslinnr
        USE-INDEX dep-art-dat_ix NO-LOCK NO-ERROR.
      real-guest = AVAILABLE bill-line.
    END.
  END.

  FIND FIRST htparam WHERE htparam.paramnr = 307 NO-LOCK.
  IF htparam.flogical THEN RUN intevent-1.p (2, res-line.zinr, 
    "My Checkout!", res-line.resnr, res-line.reslinnr).

  IF priscilla-active THEN
  DO:
      RUN intevent-1.p (2, res-line.zinr, "Priscilla", res-line.resnr, res-line.reslinnr).  
  END.
 
/******************** UPDATE room status */ 
  /*Original - Start*/
  /*FIND FIRST zimmer WHERE zimmer.zinr = zinr NO-LOCK. 
  /*MT 05/03/14 */
  FIND FIRST usr1 WHERE usr1.userinit = user-init NO-LOCK NO-ERROR. 
  CREATE res-history. 
  ASSIGN 
    res-history.nr = usr1.nr
    res-history.datum = TODAY 
    res-history.zeit = TIME 
    res-history.aenderung = "C/O "
       + "Room " + zimmer.zinr 
       + " Status Changed From " 
       + STRING(zimmer.zistatus) + " to Vacant Dirty" 
    res-history.action = "FO Cashier". 
  FIND CURRENT res-history NO-LOCK. 
  RELEASE res-history.*/
  /*Original - End*/

 /*Alder - Serverless - Issue 475 - Start*/
 FIND FIRST zimmer WHERE zimmer.zinr EQ zinr NO-LOCK NO-ERROR. 
 IF AVAILABLE zimmer THEN
 DO:
     FIND FIRST usr1 WHERE usr1.userinit EQ user-init NO-LOCK NO-ERROR. 
     IF AVAILABLE usr1 THEN
     DO:
         CREATE res-history. 
         ASSIGN 
             res-history.nr = usr1.nr
             res-history.datum = TODAY 
             res-history.zeit = TIME 
             res-history.aenderung = "C/O " + "Room " + zimmer.zinr + " Status Changed From " + STRING(zimmer.zistatus) + " to Vacant Dirty" 
             res-history.action = "FO Cashier". 
         FIND CURRENT res-history NO-LOCK. 
         RELEASE res-history. 
     END.
     FIND FIRST res-line1 WHERE RECID(res-line1) NE RECID(res-line) 
         AND res-line1.zinr = zinr 
         AND (res-line1.resstatus EQ 6 OR res-line1.resstatus EQ 13) 
         AND res-line1.l-zuordnung[3] = 0
         NO-LOCK NO-ERROR. 
     IF NOT AVAILABLE res-line1 THEN 
     DO:
         FIND FIRST outorder WHERE outorder.zinr = zimmer.zinr
             AND outorder.gespstart LE co-date AND outorder.gespende GE co-date
             AND outorder.betriebsnr LE 1 NO-LOCK NO-ERROR.
         FIND CURRENT zimmer EXCLUSIVE-LOCK. 
         IF NOT AVAILABLE outorder THEN
         DO:
             ASSIGN 
                 zimmer.zistatus = 2 
                 zimmer.bediener-nr-stat = 0.
         END.
         ELSE
         DO:
             ASSIGN 
                 zimmer.zistatus = 6 
                 zimmer.bediener-nr-stat = 0.
         END.
         FIND CURRENT zimmer NO-LOCK. 
     END.
 END.
 /*Alder - Serverless - Issue 475 - End*/

/********************* Check Day Use Guest */ 
  FOR EACH bill1 WHERE bill1.resnr = resnr AND bill1.parent-nr = reslinnr 
    AND bill1.flag = 0 AND bill1.zinr = res-line.zinr NO-LOCK: 
    tot-umsatz = tot-umsatz + bill1.gesamtumsatz. 
  END. 
  
/******** Sharer without guest bill */
  FIND FIRST bill1 WHERE bill1.resnr = resnr AND bill1.parent-nr = reslinnr 
    AND bill1.zinr = res-line.zinr NO-LOCK NO-ERROR. 
  IF NOT AVAILABLE bill1 THEN
  DO:
    FIND FIRST res-line1 WHERE RECID(res-line1) = RECID(res-line)
      EXCLUSIVE-LOCK.
    ASSIGN 
        res-line1.resstatus   = 8
        res-line1.abreise     = co-date
        res-line1.abreisezeit = TIME 
        res-line1.changed     = co-date 
        res-line1.changed-id  = user-init 
        res-line1.active-flag = 2 
    . 
    FIND FIRST guest WHERE guest.gastnr = res-line1.gastnrmember 
      EXCLUSIVE-LOCK. 
    ASSIGN 
      guest.date1 = res-line1.ankunft 
      guest.date2 = res-line1.abreise 
      guest.zimmeranz = guest.zimmeranz + 1 
      guest.resflag = 0 
    . 
    
    FIND FIRST rline WHERE rline.resstatus = 8 AND rline.abreise = co-date
      AND rline.gastnrmember = guest.gastnr
      AND ((rline.resnr NE res-line.resnr) OR (rline.reslinnr NE res-line.reslinnr))
      NO-LOCK NO-ERROR.
    IF NOT AVAILABLE rline THEN
      ASSIGN guest.aufenthalte = guest.aufenthalte + 1.
    
    FIND CURRENT res-line1 NO-LOCK.
    FIND CURRENT guest NO-LOCK.
  END.

/****************** create history */ 
  IF real-guest THEN 
    RUN create-historybl.p(resnr, reslinnr, res-line.zinr, "checkout",
        user-init, "").

  FOR EACH resline WHERE resline.resnr = resnr
    AND resline.l-zuordnung[3] = 1
    AND resline.kontakt-nr = reslinnr
    AND resline.active-flag LE 1:
    IF real-guest THEN
    ASSIGN
        resline.active-flag = 2
        resline.resstatus   = 8
        resline.abreise     = co-date 
        resline.abreisezeit = TIME 
        resline.changed     = co-date 
        resline.changed-id  = user-init 
    .
  END.

/*********************** UPDATE Bills etc */ 
  
  /* close all related active guest bills */
  FOR EACH bill1 WHERE bill1.resnr = resnr 
    AND bill1.parent-nr = reslinnr 
    AND bill1.flag = 0  EXCLUSIVE-LOCK: 
    ASSIGN
      bill1.vesrcod = user-init
      bill1.flag = 1 
      bill1.datum = co-date.

    /*ITA 130616 --> fix bill-saldo = penambahan betrag semua bill-line*/
    ASSIGN bl-saldo = 0.
    FOR EACH bill-line WHERE bill-line.rechnr = bill1.rechnr NO-LOCK:
          ASSIGN bl-saldo = bl-saldo + bill-line.betrag.
    END.

    IF bl-saldo NE bill1.saldo THEN DO:
        FIND FIRST tbuff WHERE RECID(tbuff) = RECID(bill1) EXCLUSIVE-LOCK.
        tbuff.saldo = bl-saldo.
        FIND CURRENT tbuff NO-LOCK.
        RELEASE tbuff.
    END.
  END.

  /* all related bills */
  FOR EACH bill1 WHERE bill1.resnr = resnr 
    AND bill1.parent-nr = reslinnr 
    AND bill1.zinr = zinr EXCLUSIVE-LOCK: 
    
/****************** UPDATE res-line */ 

    /*Alder - Serverless - Issue 718 - Start*/
    FIND FIRST res-line WHERE res-line.resnr = bill1.resnr 
        AND res-line.reslinnr = bill1.reslinnr 
        AND res-line.zinr = bill1.zinr NO-LOCK NO-ERROR.
    IF AVAILABLE res-line THEN
    DO:
        FIND CURRENT res-line EXCLUSIVE-LOCK.
        res-recid = RECID(res-line). 
        resstatus = res-line.resstatus. 
        ankunft = res-line.ankunft. 
        abreise = res-line.abreise. 
        IF res-line.resstatus NE 12 THEN res-line.resstatus = 8. 
        res-line.abreise = co-date. 
        /*    res-line.anztage = res-line.abreise - res-line.ankunft.   */
        abreise-date = res-line.abreise. /*NC - 21/02/24 #A06BFC*/
     
        ASSIGN 
          res-line.abreisezeit = TIME 
          res-line.changed = co-date 
          res-line.changed-id = user-init 
          res-line.active-flag = 2. 
     
        FIND FIRST res-line2 WHERE res-line2.resnr = res-line.resnr 
            AND res-line2.active-flag LT 2 NO-LOCK NO-ERROR. 
        IF NOT AVAILABLE res-line2 THEN  /* all guests checked-out */ 
        DO: 
            FIND CURRENT reservation EXCLUSIVE-LOCK. 
            reservation.activeflag = 1. 
            FIND CURRENT reservation NO-LOCK.
        END. 
        FIND CURRENT res-line NO-LOCK.
        RELEASE res-line.
    END.
    /*Alder - Serverless - Issue 718 - End*/
 
/****************** UPDATE gcf */ 
    IF tot-umsatz NE 0 THEN 
    DO: 
      FIND FIRST guest WHERE guest.gastnr = bill1.gastnr EXCLUSIVE-LOCK. 
      guest.logisumsatz = guest.logisumsatz + bill1.logisumsatz. 
      guest.argtumsatz = guest.argtumsatz + bill1.argtumsatz. 
      guest.f-b-umsatz = guest.f-b-umsatz + bill1.f-b-umsatz. 
      guest.sonst-umsatz = guest.sonst-umsatz + bill1.sonst-umsatz. 
      guest.gesamtumsatz = guest.gesamtumsatz + bill1.gesamtumsatz. 
      RELEASE guest. 
 
      DO: 
        FIND FIRST guestat WHERE guestat.gastnr = res-line.gastnr 
          AND guestat.monat = month(bill-date) 
          AND guestat.jahr = year(bill-date) 
          AND guestat.betriebsnr = 0 EXCLUSIVE-LOCK NO-ERROR. 
        IF NOT AVAILABLE guestat THEN 
        DO: 
          create guestat. 
          ASSIGN 
            guestat.gastnr = res-line.gastnr 
            guestat.monat = month(bill-date) 
            guestat.jahr = year(bill-date) 
          . 
        END. 
        ASSIGN 
          guestat.logisumsatz = guestat.logisumsatz + bill1.logisumsatz 
          guestat.argtumsatz = guestat.argtumsatz + bill1.argtumsatz 
          guestat.f-b-umsatz = guestat.f-b-umsatz + bill1.f-b-umsatz 
          guestat.sonst-umsatz = guestat.sonst-umsatz + bill1.sonst-umsatz 
          guestat.gesamtumsatz = guestat.gesamtumsatz + bill1.gesamtumsatz 
        . 
 
        FIND CURRENT guestat NO-LOCK. 
 
        FIND FIRST akt-cust WHERE akt-cust.gastnr = res-line.gastnr 
          NO-LOCK NO-ERROR. 
        IF AVAILABLE akt-cust THEN 
        DO: 
          FIND FIRST bediener WHERE bediener.userinit = akt-cust.userinit 
            NO-LOCK NO-ERROR. 
        END. 
        IF NOT AVAILABLE akt-cust OR NOT AVAILABLE bediener THEN 
        DO: 
          FIND FIRST rguest WHERE rguest.gastnr = res-line.gastnr NO-LOCK. 
          IF rguest.phonetik3 NE "" THEN 
          DO: 
            FIND FIRST bediener WHERE bediener.userinit = rguest.phonetik3 
              NO-LOCK NO-ERROR. 
          END. 
        END. 
        IF AVAILABLE bediener THEN 
        DO: 
          FIND FIRST salestat WHERE salestat.bediener-nr = bediener.nr 
            AND salestat.jahr = year(bill-date) 
            AND salestat.monat = month(bill-date) EXCLUSIVE-LOCK NO-ERROR. 
          IF NOT AVAILABLE salestat THEN 
          DO: 
            create salestat. 
            ASSIGN 
              salestat.bediener-nr = bediener.nr 
              salestat.jahr = year(bill-date) 
              salestat.monat = month(bill-date) 
            . 
          END. 
          ASSIGN 
            salestat.logisumsatz = salestat.logisumsatz + bill1.logisumsatz 
            salestat.argtumsatz = salestat.argtumsatz + bill1.argtumsatz 
            salestat.f-b-umsatz = salestat.f-b-umsatz + bill1.f-b-umsatz 
            salestat.sonst-umsatz = salestat.sonst-umsatz + bill1.sonst-umsatz 
            salestat.gesamtumsatz = salestat.gesamtumsatz + bill1.gesamtumsatz 
          . 
          IF res-line.resstatus NE 12 THEN 
          DO: 
            /*Alder - Serverless - Issue 475 - Start*/
            ASSIGN co-ankunft-int = co-date - ankunft.
            /*salestat.room-nights = salestat.room-nights + (co-date - ankunft). 
            IF (co-date - ankunft) = 0 THEN salestat.room-nights = salestat.room-nights + 1. */
            salestat.room-nights = salestat.room-nights + co-ankunft-int. 
            IF co-ankunft-int = 0 THEN salestat.room-nights = salestat.room-nights + 1. 
            /*Alder - Serverless - Issue 475 - End*/
          END. 
          FIND CURRENT salestat NO-LOCK. 
        END. 
      END. 
    END. 
    IF real-guest AND res-line.resstatus NE 12 THEN 
    DO: 
      FIND FIRST guest WHERE guest.gastnr = res-line.gastnrmember 
        EXCLUSIVE-LOCK. 
      ASSIGN 
        guest.date1 = res-line.ankunft 
        guest.date2 = res-line.abreise 
        guest.zimmeranz = guest.zimmeranz + 1 
        guest.aufenthalte = guest.aufenthalte + 1 
        guest.resflag = 0 
      . 
      FIND CURRENT guest NO-LOCK. 

      IF res-line.gastnrmember NE res-line.gastnr THEN 
      DO: 
        RUN get-min-reslinnr. 
        FIND FIRST guest WHERE guest.gastnr = res-line.gastnr EXCLUSIVE-LOCK. 
        guest.zimmeranz = guest.zimmeranz + 1.
        IF min-reslinnr = 1 THEN
        DO:
          guest.aufenthalte = guest.aufenthalte + 1.
        END.
        FIND CURRENT guest NO-LOCK.
      END.
      FIND CURRENT res-line NO-LOCK.
    END.
    ELSE
    DO:
      res-line.cancelled = co-date. 
      FIND CURRENT res-line NO-LOCK.
      RELEASE res-line.
    END. 
 
/******************** UPDATE zimplan */ 
    res-recid1 = 0. 
    FOR EACH zimplan WHERE zimplan.datum GE co-date AND 
        zimplan.datum LT abreise AND zimplan.zinr = zinr 
        AND zimplan.res-recid = res-recid EXCLUSIVE-LOCK: 
      IF res-recid1 NE 0 THEN 
      DO:
        IF zimplan.datum LT res-line1.abreise 
          THEN zimplan.res-recid = res-recid1. 
        ELSE DELETE zimplan.  
      END.
    END. 
 
/******************** UPDATE resplan */ 
    IF resstatus NE 12 THEN 
    DO: 
      FOR EACH resplan WHERE resplan.datum GE co-date 
        AND resplan.datum LT abreise 
        AND resplan.zikatnr = zimmer.zikatnr EXCLUSIVE-LOCK: 
        resplan.anzzim[resstatus] = resplan.anzzim[resstatus] - 1.
        RELEASE resplan.
      END. 
    END. 
 
/****************** Check MEalCoupon ***************/ 
    FIND FIRST resline WHERE resline.resnr = resnr 
      AND (resline.active-flag = 0 OR resline.active-flag = 1) 
      AND resline.resstatus NE 12 NO-LOCK NO-ERROR. 
    IF NOT AVAILABLE resline THEN /* all guests c/o */ 
    DO: 
      FIND FIRST mealcoup WHERE mealcoup.zinr = zinr 
        AND mealcoup.activeflag = YES USE-INDEX zinrflag_ix 
        NO-LOCK NO-ERROR. 
      IF AVAILABLE mealcoup THEN 
      DO:
        FIND CURRENT mealcoup EXCLUSIVE-LOCK.
        mealcoup.activeflag = NO. 
        mealcoup.abreise = today. 
        FIND CURRENT mealcoup NO-LOCK. 
        RELEASE mealcoup.
      END. 
    END. 
 
/****************** Delete Additonal Magnet Cards ***************/ 
    FOR EACH queasy WHERE queasy.key = 16 AND queasy.number1 = resnr 
      AND queasy.number2 = reslinnr EXCLUSIVE-LOCK: 
      DELETE queasy. 
      RELEASE queasy.
    END. 
   
  END. /* for each bill */
 
/****************** Check Master Bill ***/ 
  FIND FIRST res-line1 WHERE (res-line1.resnr = resnr) AND 
    (res-line1.reslinnr NE reslinnr) AND 
    (res-line1.resstatus EQ 6 OR res-line1.resstatus EQ 13) NO-LOCK NO-ERROR. 
  IF NOT AVAILABLE res-line1 THEN 
  DO: 
    FIND FIRST master WHERE master.resnr = resnr NO-LOCK NO-ERROR. 
    IF AVAILABLE master THEN 
    DO: 
      FIND CURRENT master EXCLUSIVE-LOCK.
      master.active = NO. 
      FIND CURRENT master NO-LOCK. 
      RELEASE master.

      FIND FIRST bill1 WHERE bill1.resnr = resnr AND bill1.reslinnr = 0 NO-LOCK. 
      IF bill1.rechnr NE 0 THEN 
      DO: 
        FIND FIRST guest WHERE guest.gastnr = bill1.gastnr NO-LOCK NO-ERROR.
        IF AVAILABLE guest THEN
        DO:
            FIND CURRENT guest EXCLUSIVE-LOCK. 
            ASSIGN 
              guest.logisumsatz = guest.logisumsatz + bill1.logisumsatz 
              guest.argtumsatz = guest.argtumsatz + bill1.argtumsatz 
              guest.f-b-umsatz = guest.f-b-umsatz + bill1.f-b-umsatz 
              guest.sonst-umsatz = guest.sonst-umsatz + bill1.sonst-umsatz 
              guest.gesamtumsatz = guest.gesamtumsatz + bill1.gesamtumsatz 
            . 
            FIND CURRENT guest NO-LOCK.
            RELEASE guest. 
        END.
      END. 
    END. 
    FOR EACH queasy WHERE queasy.KEY = 24 AND queasy.char1 = zinr EXCLUSIVE-LOCK: 
        DELETE queasy. 
        RELEASE queasy.
    END. 
  END. 
 
  FIND FIRST reslin-queasy WHERE reslin-queasy.key = "flag" 
    AND reslin-queasy.resnr = resnr 
    AND reslin-queasy.reslinnr = reslinnr 
    AND reslin-queasy.betriebsnr = 0 EXCLUSIVE-LOCK NO-ERROR. 
  IF AVAILABLE reslin-queasy THEN DELETE reslin-queasy. 
 
  checked-out = YES. 
  
/* Move to UI !!! */
  FIND FIRST htparam WHERE htparam.paramnr = 1002 NO-LOCK. /* Lic Sales Mktg */
  IF htparam.flogical THEN
  DO:
    FIND FIRST htparam WHERE htparam.paramnr = 1099 NO-LOCK.
    IF htparam.paramgr = 27 AND htparam.flogical THEN
    DO:
      FIND FIRST guest WHERE guest.gastnr = res-line.gastnrmember NO-LOCK.
      IF guest.email-adr NE "" THEN
      DO:
      END.
    END.
  END.

  msg-str = msg-str + CHR(2) + "&M"
          + translateExtended ("Guest checked-out.",lvCAREA,"") + CHR(10).

  /* check IF master bill exists AND NO other guest inhouse */ 
  FIND FIRST mbill WHERE mbill.resnr = resnr 
    AND mbill.zinr = "" NO-LOCK NO-ERROR. 
  IF NOT AVAILABLE mbill THEN RETURN. 
    
  FIND FIRST resline WHERE resline.resnr = resnr 
    AND resline.active-flag LE 1 NO-LOCK NO-ERROR. 
  IF NOT AVAILABLE resline THEN 
  msg-str = msg-str + CHR(2)
          + translateExtended ("All guests checked-out, close the master bill SOONEST",lvCAREA,"") + CHR(10)
          + translateExtended ("BillNo : ",lvCAREA,"") + STRING(mbill.rechnr) 
          + " - " + translateExtended ("ResNo : ",lvCAREA,"") 
          + STRING(mbill.resnr) + CHR(10). 
END. 

PROCEDURE get-min-reslinnr: 
DEFINE BUFFER resline FOR res-line. 
  FOR EACH resline WHERE resline.resnr = resnr AND 
    resline.active-flag = 1 AND resline.resstatus NE 12 NO-LOCK:  
    min-reslinnr = min-reslinnr + 1.
  END. 
END. 

/*NC - 21/02/24 #A06BFC*/
PROCEDURE update-queasy171:
  DEFINE BUFFER zbuff 			FOR zimkateg.  
  DEFINE BUFFER qsy   			FOR queasy.

  DEFINE VARIABLE i           AS INT INIT 0.
  DEFINE VARIABLE upto-date AS DATE.
  DEFINE VARIABLE iftask      AS CHAR INIT "".
  DEFINE VARIABLE origcode    AS CHAR INIT "".
  DEFINE VARIABLE cat-flag    AS LOGICAL INIT NO.
  DEFINE VARIABLE roomnr      AS INT INIT 0.
  DEFINE VARIABLE datum AS DATE. 
  
  FIND FIRST res-line WHERE res-line.resnr = resnr 
    AND res-line.reslinnr = reslinnr NO-LOCK NO-ERROR. 
  IF AVAILABLE res-line THEN
  DO:	
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

      /*Alder - Serverless - Issue 718 - Start*/
	  IF res-line.ankunft = co-date THEN
      DO:
          upto-date = co-date.
      END.
	  ELSE
      DO:
          IF abreise-date NE ? THEN
          DO:
              upto-date = abreise-date - 1.
          END.
          ELSE
          DO:
              upto-date = co-date.
          END.
      END.
      /*Alder - Serverless - Issue 718 - End*/

	  DO datum = co-date TO upto-date:
	  
			FIND FIRST queasy WHERE queasy.KEY = 171 AND queasy.date1 = datum
				AND queasy.number1 = roomnr AND queasy.char1 = "" NO-LOCK NO-ERROR.
			IF AVAILABLE queasy AND queasy.logi1 = NO AND queasy.logi2 = NO THEN
			DO:
				FIND FIRST qsy WHERE RECID(qsy) = RECID(queasy) EXCLUSIVE-LOCK NO-ERROR.
				IF AVAILABLE qsy THEN
				DO:
					qsy.logi2 = YES.
					FIND CURRENT qsy NO-LOCK.
					RELEASE qsy.
				END.
			END. 
			
			IF origcode NE "" THEN
			DO:
				FIND FIRST queasy WHERE queasy.KEY = 171 AND queasy.date1 = datum
					AND queasy.number1 = roomnr AND queasy.char1 = origcode NO-LOCK NO-ERROR.
				IF AVAILABLE queasy AND queasy.logi1 = NO AND queasy.logi2 = NO THEN
				DO:
					FIND FIRST qsy WHERE RECID(qsy) = RECID(queasy) EXCLUSIVE-LOCK NO-ERROR.
					IF AVAILABLE qsy THEN
					DO:
						qsy.logi2 = YES.
						FIND CURRENT qsy NO-LOCK.
						RELEASE qsy.
					END.
				END.
			END.
	  END.
  END.
END.
