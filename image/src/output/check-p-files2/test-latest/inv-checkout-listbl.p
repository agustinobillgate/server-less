 
/************************ Checking out the guest *******************************/ 

DEFINE INPUT PARAMETER pvILanguage  AS INTEGER NO-UNDO.
DEFINE INPUT PARAMETER case-type    AS INTEGER.
DEFINE INPUT PARAMETER resnr        AS INTEGER. 
DEFINE INPUT PARAMETER reslinnr     AS INTEGER. 
DEFINE INPUT PARAMETER user-init    AS CHAR. 
DEFINE INPUT PARAMETER reason-str   AS CHAR.
DEFINE INPUT PARAMETER silenzio     AS LOGICAL.

DEFINE OUTPUT PARAMETER error-code  AS INTEGER INITIAL 0. 
DEFINE OUTPUT PARAMETER checked-out AS LOGICAL INITIAL NO. 
DEFINE OUTPUT PARAMETER early-co    AS LOGICAL INITIAL NO.
DEFINE OUTPUT PARAMETER goto-master AS LOGICAL INITIAL NO. 
DEFINE OUTPUT PARAMETER flag-report AS LOGICAL INITIAL NO.
DEFINE OUTPUT PARAMETER msg-str     AS CHAR    INITIAL "".
DEFINE OUTPUT PARAMETER msg-int     AS INTEGER.

DEFINE VARIABLE min-reslinnr AS INTEGER INITIAL 0. 
DEFINE VARIABLE pax          AS INTEGER. 
DEFINE VARIABLE rechnr       AS INTEGER. 
DEFINE VARIABLE rm-nite      AS INTEGER NO-UNDO. 

DEFINE VARIABLE co-date     AS DATE. 
DEFINE VARIABLE bill-date   AS DATE. 

DEFINE VARIABLE abreise-date   AS DATE. /*NC - 21/02/24 #A06BFC*/
DEFINE VARIABLE zinr        LIKE zimmer.zinr.
DEFINE VARIABLE add-str     AS CHAR. 

DEFINE VARIABLE main-guest  AS LOGICAL NO-UNDO. 
DEFINE VARIABLE co-ok       AS LOGICAL. 
DEFINE VARIABLE zugriff     AS LOGICAL. 
DEFINE VARIABLE answer      AS LOGICAL INITIAL YES. 
DEFINE VARIABLE room-added  AS LOGICAL INITIAL NO. 
DEFINE VARIABLE do-it       AS LOGICAL NO-UNDO. 
DEFINE VARIABLE statusStr   AS CHAR NO-UNDO.
DEFINE VARIABLE unbalanced-bill AS LOGICAL NO-UNDO. /*baca ke htparam*/
DEFINE VARIABLE priscilla-active AS LOGICAL NO-UNDO INITIAL YES.

DEFINE BUFFER resline FOR res-line. 
DEFINE BUFFER mbill   FOR bill. 
DEFINE BUFFER rguest  FOR guest. 
DEFINE BUFFER rline   FOR res-line.
DEFINE BUFFER bline   FOR bediener.
DEFINE BUFFER buf-rline FOR res-line.

{SupertransBL.i} 
DEF VAR lvCAREA AS CHAR INITIAL "inv-checkout-listbl". 

FIND FIRST reservation WHERE reservation.resnr = resnr  NO-LOCK.  
FIND FIRST bediener WHERE bediener.userinit = user-init NO-LOCK.

FIND FIRST htparam WHERE paramnr = 87 NO-LOCK. 
co-date = htparam.fdate. 
FIND FIRST htparam WHERE paramnr = 110 NO-LOCK. 
bill-date = htparam.fdate. 

/*ITA 120615 --> for harris waterfront Request*/
FIND FIRST htparam WHERE htparam.paramnr = 974 NO-LOCK NO-ERROR.
unbalanced-bill = htparam.flogical.

/*ITA 130616*/
DEF VARIABLE bl-saldo  AS DECIMAL NO-UNDO.
DEFINE BUFFER tbuff FOR bill.

 
FIND FIRST res-line WHERE res-line.resnr = resnr 
  AND res-line.reslinnr = reslinnr NO-LOCK.

ASSIGN
  zinr       = res-line.zinr
  pax        = res-line.erwachs 
  main-guest = (res-line.resstatus = 6)
. 
 
/*FDL Nov 23, 2024: Ticket 2FD3E7 - Preventif cause it's anomali, happened sometime*/
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
                    error-code = 3 
                    co-ok      = NO 
                    msg-str    = translateExtended ("RoomNo",lvCAREA,"") 
                      + " " + zinr + "  -  " 
                      + translateExtended ("Master Bill not yet settled.",lvCAREA,"") + CHR(10)
                      + translateExtended ("Check-out not possible.",lvCAREA,"") + CHR(10).

                RETURN.
            END.
        END.
    END.
END.

RUN check-billstatus(OUTPUT co-ok). 

IF NOT co-ok THEN RETURN.

IF case-type = 1 THEN 
DO: 
  FIND FIRST rline WHERE rline.active-flag = 1 
    AND rline.zinr = res-line.zinr
    AND rline.l-zuordnung[3] = 0
    AND RECID(rline) /*NE*/ EQ RECID(res-line) NO-LOCK NO-ERROR.
  IF /*NOT*/ AVAILABLE rline THEN
  DO:
    FIND FIRST outorder WHERE outorder.zinr = res-line.zinr
      AND outorder.gespstart LE co-date AND outorder.gespende GE co-date
      AND outorder.betriebsnr LE 1 NO-LOCK NO-ERROR.
    IF AVAILABLE outorder THEN
    DO:
        msg-int = 1.
        msg-str = translateExtended ("Out-Of-Order Record found for this room:",lvCAREA,"") 
            + " " + STRING(outorder.gespstart) + "-" + STRING(outorder.gespende) + CHR(10)
            + translateExtended ("The room status will immediately be changed to O-O-O after checking-out the guest.",lvCAREA,"")
            + CHR(10).    
    END.
    early-co = (res-line.abreise GT co-date).
    RUN check-co-time. 
    IF early-co THEN 
    DO:    
      IF SUBSTR(bediener.perm,70,1) GE "2" THEN
      DO:
          msg-int = 2.
          msg-str = translateExtended ("Early Check-out",lvCAREA,"") 
              + " " + res-line.NAME + CHR(10) 
              + translateExtended ("ROOM",lvCAREA,"") + " " 
              + res-line.zinr + " ?" + CHR(10).
      END.      
      ELSE
      DO:
        msg-str = translateExtended ("No Access Right for Early Checkout [70,2].",lvCAREA,"") + CHR(10).
        error-code = 4.
      END.
    END.
    ELSE  
    DO:
        msg-int = 3.
        msg-str = translateExtended ("Check-out",lvCAREA,"") 
            + " " + res-line.name + CHR(10)
            + translateExtended ("ROOM",lvCAREA,"") + " " 
            + res-line.zinr + " ?" + CHR(10).
    END.    
  END.
  RETURN.
END.

RUN guest-checkout. 
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
  DEFINE OUTPUT PARAMETER co-ok AS LOGICAL INITIAL YES. 
  DEFINE VARIABLE parent-nr AS INTEGER INITIAL 0. 
  DEFINE BUFFER bill1 FOR bill. 

  IF unbalanced-bill = NO THEN DO:
      FIND FIRST bill1 WHERE bill1.resnr = resnr AND bill1.reslinnr = reslinnr 
        AND bill1.flag = 0 AND bill1.zinr = zinr NO-LOCK NO-ERROR. 
      IF AVAILABLE bill1 THEN 
      DO: 
        parent-nr = bill1.parent-nr. 
        /* SY 07 June 2016 */
        FOR EACH bill1 WHERE bill1.resnr = resnr AND bill1.parent-nr = parent-nr 
            AND bill1.flag = 0 /* AND bill1.zinr = zinr */ /*EXCLUSIVE-LOCK*/ NO-LOCK: /*FDL Change Exclusive-Lock to No-Lock*/  
          FIND FIRST bill-line WHERE bill-line.rechnr = bill1.rechnr 
            NO-LOCK NO-ERROR. 
          IF AVAILABLE bill-line AND co-ok 
            AND (bill1.rgdruck EQ 0 OR bill1.saldo NE 0) THEN 
          DO: 
            co-ok = NO. 
            rechnr = bill1.rechnr. 
            IF bill1.saldo NE 0 THEN 
            ASSIGN
              error-code = 1
              msg-str    = translateExtended ("RoomNo",lvCAREA,"") 
                + " " + zinr + "  -  " 
                + translateExtended ("BillNo",lvCAREA,"") 
                + " " + STRING(rechnr) + " " 
                + translateExtended ("not yet balanced",lvCAREA,"") + CHR(10)
                + translateExtended ("Check-out not possible.",lvCAREA,"") + CHR(10)
             .
            ELSE 
            ASSIGN
              error-code = 2 
              msg-str    = translateExtended ("RoomNo",lvCAREA,"") 
                + " " + zinr + "  -  " 
                + translateExtended ("BillNo",lvCAREA,"") 
                + " "  + STRING(rechnr) + " " 
                + translateExtended ("not yet printed.",lvCAREA,"") + CHR(10)
                + translateExtended ("Check-out not possible.",lvCAREA,"") + CHR(10)
            . 
            RETURN. 
          END. 
        END. 
      END.
  END.

  FIND FIRST htparam WHERE paramnr = 141 NO-LOCK. 
  IF htparam.fchar NE "" THEN 
  DO:
    FIND FIRST resline WHERE resline.resnr = resnr
      AND resline.active-flag = 1
      AND resline.resstatus NE 12
      AND resline.reslinnr NE reslinnr NO-LOCK NO-ERROR.
    IF NOT AVAILABLE resline THEN
    DO:
      FIND FIRST mbill WHERE mbill.resnr = resnr 
        AND mbill.zinr = "" AND mbill.flag = 0 NO-LOCK NO-ERROR. 
      IF AVAILABLE mbill AND mbill.saldo GT 0 THEN 
      DO: 
        FIND FIRST rguest WHERE rguest.gastnr = mbill.gastnr NO-LOCK. 
        IF rguest.zahlungsart = 0 THEN 
        ASSIGN
          error-code = 3 
          co-ok      = NO 
          msg-str    = translateExtended ("RoomNo",lvCAREA,"") 
            + " " + zinr + "  -  " 
            + translateExtended ("Master Bill not yet settled.",lvCAREA,"") + CHR(10)
            + translateExtended ("Check-out not possible.",lvCAREA,"") + CHR(10).
      END.
    END.
  END. 
END. 
 
PROCEDURE check-co-time: 
DEFINE VARIABLE co-zeit AS INTEGER NO-UNDO. 
DEFINE VARIABLE co-datum AS DATE NO-UNDO. 
DEFINE VARIABLE zeit AS INTEGER NO-UNDO. 
  FIND FIRST htparam WHERE htparam.paramnr = 1076 NO-LOCK. 
  IF htparam.feldtyp EQ 4 AND htparam.flogical THEN 
  DO: 
    co-zeit = res-line.abreisezeit. 
    IF co-zeit = 0 THEN co-zeit = 12 * 3600. 
 
    co-datum = res-line.abreise. 
    zeit = TIME. 
    IF (co-datum = bill-date) AND (zeit GT co-zeit) THEN 
    DO:
        msg-int = 4.
        msg-str = translateExtended ("C/O Time",lvCAREA,"") + " " + STRING(co-zeit, "HH:MM:SS") 
            + " " + translateExtended ("exceeded. Current time is",lvCAREA,"") 
            + " " + STRING(zeit,"HH:MM:SS") + CHR(10) 
            + translateExtended ("Exceeded time =",lvCAREA,"") 
            + " " + STRING((zeit - co-zeit), "HH:MM:SS") + CHR(10).
    END.    
  END. 
END. 
 
PROCEDURE guest-checkout: 
  DEFINE BUFFER bill1           FOR bill. 
  DEFINE BUFFER rline           FOR res-line.
  DEFINE BUFFER res-line1       FOR res-line. 
  DEFINE BUFFER res-line2       FOR res-line. 
  DEFINE BUFFER sharer          FOR res-line.
  DEFINE VARIABLE ankunft       AS DATE. 
  DEFINE VARIABLE abreise       AS DATE. 
  DEFINE VARIABLE resstatus     AS INTEGER. 
  DEFINE VARIABLE res-recid     AS INTEGER. 
  DEFINE VARIABLE res-recid1    AS INTEGER. 
  DEFINE VARIABLE tot-umsatz    AS DECIMAL INITIAL 0. 
  DEFINE VARIABLE day-use       AS LOGICAL INITIAL NO. 
  DEFINE VARIABLE real-guest    AS LOGICAL INITIAL YES. 
  DEFINE VARIABLE sales-lic     AS LOGICAL. 
  DEFINE VARIABLE dummy-logi    AS LOGICAL. 
  DEFINE VARIABLE sharer-co     AS LOGICAL.
  DEFINE VARIABLE avail-bill-line AS INTEGER.
  
  FIND FIRST reslin-queasy WHERE reslin-queasy.key = "flag" 
    AND reslin-queasy.resnr = resnr 
    AND reslin-queasy.reslinnr = reslinnr 
    AND reslin-queasy.betriebsnr = 0 NO-LOCK NO-ERROR. 
  IF AVAILABLE reslin-queasy AND 
    (reslin-queasy.logi1 = YES OR reslin-queasy.logi2 = YES 
    OR reslin-queasy.logi3 = YES) THEN ASSIGN flag-report = YES.
  
  FIND FIRST htparam WHERE paramnr = 1002 no-lock. /* license Sales */ 
  sales-lic = htparam.flogical. 
 
  IF res-line.betrieb-gast GT 0 THEN 
  DO:
      msg-int = 5.
      msg-str = translateExtended ("Number of created KeyCard(s) =",lvCAREA,"") 
        + " " + STRING(res-line.betrieb-gast) + CHR(10). 
  END.
    
 
/******************** UPDATE room status */ 
  FIND FIRST zimmer WHERE zimmer.zinr = zinr NO-LOCK. 
  FIND FIRST res-line1 WHERE RECID(res-line1) NE RECID(res-line) 
    AND res-line1.zinr = zinr 
    AND (res-line1.resstatus EQ 6 OR res-line1.resstatus EQ 13) 
    AND res-line1.l-zuordnung[3] = 0
    NO-LOCK NO-ERROR. 
  IF NOT AVAILABLE res-line1 THEN 
  DO TRANSACTION: 
    FIND FIRST outorder WHERE outorder.zinr = zimmer.zinr
        AND outorder.gespstart LE co-date AND outorder.gespende GE co-date
        AND outorder.betriebsnr LE 1 NO-LOCK NO-ERROR.
    FIND CURRENT zimmer EXCLUSIVE-LOCK. 
    IF AVAILABLE outorder THEN
    ASSIGN           
      zimmer.zistatus = 6 
      zimmer.bediener-nr-stat = 0 
    . 
    ELSE
    ASSIGN           
      zimmer.zistatus = 2 
      zimmer.bediener-nr-stat = 0 
    . 
    FIND CURRENT zimmer NO-LOCK. 
    RELEASE zimmer.
  END. 
 
/********************* Check Day Use Guest */ 
  FOR EACH bill1 WHERE bill1.resnr = resnr AND bill1.parent-nr = reslinnr 
    AND bill1.flag = 0 AND bill1.zinr = zinr NO-LOCK: 
    tot-umsatz = tot-umsatz + bill1.gesamtumsatz. 
  END. 
 
  IF (co-date - res-line.ankunft) = 0 AND tot-umsatz = 0 THEN 
    real-guest = NO.
 
DO TRANSACTION: 
 
/******************** CHECKOUT ROOM SHARER(s) WITHOUT BILL **********/
  FOR EACH sharer WHERE sharer.resnr = resnr
    AND sharer.kontakt-nr = reslinnr
    AND sharer.l-zuordnung[3] = 1 
    AND sharer.active-flag LE 1:
    IF real-guest THEN
      RUN create-historybl.p(sharer.resnr, sharer.reslinnr, sharer.zinr, "checkout",
          user-init, ""). 
    ASSIGN
      sharer.active-flag = 2
      sharer.resstatus   = 8
      sharer.abreise     = co-date 
      sharer.abreisezeit = TIME 
      sharer.changed     = co-date 
      sharer.changed-id  = user-init 
    .
  END.

/*** Switch off extension line ****/ 
  FIND FIRST htparam WHERE paramnr = 307 NO-LOCK. 
  IF flogical THEN RUN intevent-1.p( 2, zinr, "My Checkout!", res-line.resnr, res-line.reslinnr). 
 
  RUN intevent-1.p( 2, zinr, "bridge", res-line.resnr, res-line.reslinnr). 

  IF priscilla-active THEN
  DO:
      RUN intevent-1.p( 2, zinr, "Priscilla", res-line.resnr, res-line.reslinnr).   
  END.
/*********************** UPDATE Bills etc */ 

  FOR EACH bill1 WHERE bill1.resnr = resnr 
    AND bill1.parent-nr = reslinnr 
    AND bill1.flag = 0  
    /* SY 04 June 2016 AND bill1.zinr = zinr */ EXCLUSIVE-LOCK: 
    
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


    ASSIGN
      bill1.vesrcod = user-init
      bill1.flag = 1 
      bill1.datum = co-date. 
  END.

  FOR EACH bill1 WHERE bill1.resnr = resnr 
      AND bill1.parent-nr = reslinnr 
      AND bill1.zinr = zinr EXCLUSIVE-LOCK: 
 
/****************** create history */ 
    IF real-guest AND resstatus NE 12 THEN 
    DO:
      RUN create-historybl.p(resnr, reslinnr, zinr, "checkout", 
          user-init, ""). 
    END. 

/****************** UPDATE res-line */ 
    FIND FIRST res-line WHERE res-line.resnr = bill1.resnr 
      AND res-line.reslinnr = bill1.reslinnr 
      AND res-line.zinr = bill1.zinr EXCLUSIVE-LOCK. 
    res-recid = RECID(res-line). 
    resstatus = res-line.resstatus. 
    ankunft = res-line.ankunft. 
    abreise = res-line.abreise. 
    IF res-line.resstatus NE 12 THEN res-line.resstatus = 8. 
    res-line.abreise = co-date. 
    abreise-date = res-line.abreise. /*NC - 21/02/24 #A06BFC*/
    
    ASSIGN 
      res-line.abreisezeit = TIME 
      res-line.changed = co-date 
      res-line.changed-id = user-init 
      res-line.active-flag = 2 
    . 
    
    IF res-line.erwachs GT 0 THEN ASSIGN avail-bill-line = bill1.rechnr.

    IF reason-str NE "" AND reason-str NE ? THEN res-line.zimmer-wunsch =
        res-line.zimmer-wunsch + "earlyCO," + reason-str + ";".

    FIND FIRST res-line2 WHERE res-line2.resnr = res-line.resnr 
      AND res-line2.active-flag LT 2 NO-LOCK NO-ERROR. 
    IF NOT AVAILABLE res-line2 THEN  /* all guests checked-out */ 
    DO: 
      FIND CURRENT reservation EXCLUSIVE-LOCK. 
      reservation.activeflag = 1. 
      FIND CURRENT reservation NO-LOCK. 
    END. 
 
/****************** UPDATE gcf */ 
    IF tot-umsatz NE 0 THEN 
    DO: 
      FIND FIRST guest WHERE guest.gastnr = res-line.gastnrpay EXCLUSIVE-LOCK. 
      ASSIGN 
        guest.logisumsatz = guest.logisumsatz + bill1.logisumsatz 
        guest.argtumsatz = guest.argtumsatz + bill1.argtumsatz 
        guest.f-b-umsatz = guest.f-b-umsatz + bill1.f-b-umsatz 
        guest.sonst-umsatz = guest.sonst-umsatz + bill1.sonst-umsatz 
        guest.gesamtumsatz = guest.gesamtumsatz + bill1.gesamtumsatz 
      . 
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
            salestat.room-nights = salestat.room-nights + (co-date - ankunft). 
            IF (co-date - ankunft) = 0 THEN 
              salestat.room-nights = salestat.room-nights + 1. 
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
        guest.resflag = 0 
      . 

      FIND FIRST rline WHERE rline.resstatus = 8 AND rline.abreise = co-date
        AND rline.gastnrmember = guest.gastnr
        AND ((rline.resnr NE res-line.resnr) OR (rline.reslinnr NE res-line.reslinnr))
        NO-LOCK NO-ERROR.
      IF NOT AVAILABLE rline THEN
        ASSIGN guest.aufenthalte = guest.aufenthalte + 1.
      
      FIND CURRENT guest NO-LOCK. 
      IF res-line.gastnrmember NE res-line.gastnr THEN 
      DO: 
        RUN get-min-reslinnr. 
        FIND FIRST guest WHERE guest.gastnr = res-line.gastnr EXCLUSIVE-LOCK. 
        guest.zimmeranz = guest.zimmeranz + 1. 
        IF min-reslinnr = 1 THEN 
        DO: 
          ASSIGN guest.aufenthalte = guest.aufenthalte + 1. 
        END. 
        FIND CURRENT guest NO-LOCK. 
      END. 

      FIND FIRST bline WHERE bline.userinit = user-init NO-LOCK NO-ERROR.
      CREATE res-history. 
      ASSIGN 
          res-history.nr          = bline.nr 
          res-history.resnr       = res-line.resnr
          res-history.reslinnr    = res-line.reslinnr
          res-history.datum       = TODAY 
          res-history.zeit        = TIME 
          res-history.aenderung   = "CheckOut Room " + res-line.zinr 
                                  + " ResNo " + STRING(res-line.resnr)
          res-history.action      = "CheckOut".
      FIND CURRENT res-history NO-LOCK. 
      RELEASE res-history.

      FIND CURRENT res-line NO-LOCK.
      RELEASE res-line. 
    END. 
    ELSE 
    DO: 
      res-line.cancelled = co-date. 
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
        AND mealcoup.activeflag = YES USE-INDEX zinrflag_ix EXCLUSIVE-LOCK NO-ERROR. 
      IF AVAILABLE mealcoup THEN 
      DO: 
        mealcoup.activeflag = NO. 
        mealcoup.abreise = today. 
        FIND CURRENT mealcoup NO-LOCK. 
      END. 
    END. 
 
/****************** Delete Additonal Magnet Cards ***************/ 
    FOR EACH queasy WHERE queasy.key = 16 AND queasy.number1 = resnr 
      AND queasy.number2 = reslinnr: 
      DELETE queasy. 
    END. 

    /************************online tax vanguard (pengiriman realtime)*****************/
    IF avail-bill-line NE 0 THEN DO:
        CREATE INTERFACE.
        ASSIGN
            INTERFACE.KEY         = 38
            INTERFACE.action      = YES
            INTERFACE.nebenstelle = ""
            INTERFACE.parameters = "close-bill"
            INTERFACE.intfield    = bill1.rechnr
            INTERFACE.decfield    = bill1.billtyp
            INTERFACE.int-time    = TIME
            INTERFACE.intdate     = TODAY
            INTERFACE.resnr       = bill1.resnr
            INTERFACE.reslinnr    = bill1.reslinnr
          .
        FIND CURRENT INTERFACE NO-LOCK.
        RELEASE INTERFACE.
    END.
  END.

/****************** Check Master Bill ***/ 
  FIND FIRST res-line1 WHERE (res-line1.resnr = resnr) AND 
    (res-line1.reslinnr NE reslinnr) AND 
    (res-line1.resstatus EQ 6 OR res-line1.resstatus EQ 13) NO-LOCK NO-ERROR. 
  IF NOT AVAILABLE res-line1 THEN 
  DO: 
    FIND FIRST master WHERE master.resnr = resnr EXCLUSIVE-LOCK NO-ERROR. 
    IF AVAILABLE master THEN 
    DO: 
      master.active = NO. 
      FIND CURRENT master NO-LOCK. 
      FIND FIRST bill1 WHERE bill1.resnr = resnr AND bill1.reslinnr = 0 NO-LOCK 
        NO-ERROR. 
      IF AVAILABLE bill1 AND bill1.rechnr NE 0 THEN 
      DO: 
        FIND FIRST guest WHERE guest.gastnr = bill1.gastnr EXCLUSIVE-LOCK. 
        ASSIGN 
          guest.logisumsatz = guest.logisumsatz + bill1.logisumsatz 
          guest.argtumsatz = guest.argtumsatz + bill1.argtumsatz 
          guest.f-b-umsatz = guest.f-b-umsatz + bill1.f-b-umsatz 
          guest.sonst-umsatz = guest.sonst-umsatz + bill1.sonst-umsatz 
          guest.gesamtumsatz = guest.gesamtumsatz + bill1.gesamtumsatz 
        . 
        RELEASE guest. 
      END. 
    END. 
    FOR EACH queasy WHERE queasy.KEY = 24 AND queasy.char1 = zinr: 
        DELETE queasy. 
    END. 
  END. 
 
END.  /* TRANSACTION */ 
 
  DO:
      checked-out = YES. 
      msg-int = 6.
      msg-str = translateExtended ("Guest checked-out.",lvCAREA,"") + CHR(10).
  END.

/* check IF master bill exists AND NO other guest inhouse */ 
  
  FIND FIRST res-line WHERE res-line.resnr = resnr
      AND res-line.reslinnr = reslinnr NO-LOCK.
  
  /*MT*/
  IF NOT silenzio THEN
  DO:
    FIND FIRST resline WHERE resline.resnr = resnr
      AND resline.active-flag EQ 1
      AND resline.zinr = res-line.zinr
      AND resline.l-zuordnung[3] = 0
      AND resline.abreise = co-date NO-LOCK NO-ERROR.
    IF AVAILABLE resline THEN
    DO:
      IF resline.resstatus = 6 THEN
        statusStr = translateExtended ("Status: Main Guest; RmRate =",lvCAREA,"").
      ELSE 
      DO:
          statusStr = translateExtended ("Status: Room Sharer; RmRate =",lvCAREA,"").
          msg-int = 7.
          msg-str = translateExtended ("Other Expected Departure Guest FOUND in the same room:",lvCAREA,"") 
                  + CHR(10)
                  + resline.NAME + " " + STRING(resline.ankunft)
                  + " - " + STRING(resline.abreise)
                  + CHR(10)
                  + statusStr + " " + STRING(resline.zipreis).
      END.          
    END.
  END.

  FIND FIRST mbill WHERE mbill.resnr = resnr 
    AND mbill.zinr = "" NO-LOCK NO-ERROR. 
  IF NOT AVAILABLE mbill AND res-line.l-zuordnung[5] NE 0
    AND res-line.l-zuordnung[2] = 0 THEN
    FIND FIRST mbill WHERE mbill.resnr = res-line.l-zuordnung[5] 
    AND mbill.zinr = "" AND mbill.flag = 0 NO-LOCK NO-ERROR. 
  IF AVAILABLE mbill THEN
  DO:
    FIND FIRST resline WHERE resline.resnr = mbill.resnr 
      AND resline.active-flag LE 1 NO-LOCK NO-ERROR.
    IF NOT AVAILABLE resline THEN
    DO:
      IF res-line.l-zuordnung[5] = 0 THEN goto-master = YES.
      ELSE
      DO:
        FIND FIRST resline WHERE resline.resnr NE mbill.resnr
          AND resline.active-flag EQ 1 
          AND resline.l-zuordnung[2] = 0       
          AND resline.l-zuordnung[5] = mbill.resnr NO-LOCK NO-ERROR.
        goto-master = NOT AVAILABLE resline.
      END.
    END.
  END.
  
  IF goto-master THEN
  DO:
      msg-int = 8.
      msg-str = translateExtended ("All guests are checked-out, close the master bill NOW?",lvCAREA,"") + CHR(10) 
        + translateExtended ("BillNo :",lvCAREA,"") 
        + " " + STRING(mbill.rechnr) + " " 
        + translateExtended ("- ResNo :",lvCAREA,"") 
        + " " + STRING(mbill.resnr) + CHR(10).
  END. 
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

	  IF res-line.ankunft = co-date THEN upto-date = co-date .
	  ELSE upto-date = abreise-date - 1. 

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
