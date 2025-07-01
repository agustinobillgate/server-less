
/*MT 20/07/12 --> change zinr format */ 
 
{supertrans.i} 
DEF VAR lvCAREA AS CHAR INITIAL "create-history".

/************* Create GCF history due TO checkout / room change ***************/ 
 
DEFINE INPUT PARAMETER resnr     AS INTEGER. 
DEFINE INPUT PARAMETER reslinnr  AS INTEGER. 
DEFINE INPUT PARAMETER old-zinr  LIKE zimmer.zinr.   /*MT 20/07/12 change zinr format */
DEFINE INPUT PARAMETER res-mode  AS char.     /* checkout OR roomchg */
DEFINE SHARED VARIABLE user-init AS CHAR. 
 
DEFINE BUFFER rline    FOR res-line.
DEFINE BUFFER bill1    FOR bill. 
DEFINE BUFFER history1 FOR history. 
DEFINE BUFFER rguest   FOR guest.

DEFINE VARIABLE parent-nr   AS INTEGER. 
DEFINE VARIABLE tot-umsatz  AS DECIMAL. 
DEFINE VARIABLE found       AS LOGICAL INITIAL NO. 
 
FIND FIRST bediener WHERE bediener.userinit = user-init NO-LOCK.

FIND FIRST res-line WHERE res-line.resnr = resnr 
  AND res-line.reslinnr = reslinnr NO-LOCK. 
FIND FIRST reservation WHERE reservation.resnr = resnr NO-LOCK. 
FIND FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr NO-LOCK. 
FIND FIRST guest WHERE guest.gastnr = res-line.gastnrmember NO-LOCK. 
 
FIND FIRST htparam WHERE paramnr = 87 NO-LOCK. 
 
IF res-mode = "checkout" THEN 
DO: 
  CREATE history. 

  FIND FIRST rguest WHERE rguest.gastnr = res-line.gastnr NO-LOCK.
  ASSIGN history.bemerk = history.bemerk + "RSV:" + rguest.NAME + CHR(10).

  IF res-line.l-zuordnung[3] = 0 AND res-line.resstatus = 6 THEN
  DO:
    FOR EACH rline WHERE rline.resnr = res-line.resnr
      AND rline.l-zuordnung[3] = 1
      AND rline.kontakt-nr = res-line.reslinnr NO-LOCK:
      ASSIGN history.bemerk = history.bemerk + "AG:" + rline.NAME + CHR(10).
      FIND FIRST rguest WHERE rguest.gastnr = rline.gastnrmember 
        NO-LOCK.
      IF rguest.date1 NE rline.ankunft OR rguest.date2 NE rline.abreise THEN
      DO:
        FIND CURRENT rguest EXCLUSIVE-LOCK.
        ASSIGN
          rguest.date1       = rline.ankunft 
          rguest.date2       = rline.abreise 
          /*rguest.zimmeranz   = rguest.zimmeranz + 1 
          rguest.aufenthalte = rguest.aufenthalte + 1 */
          rguest.resflag     = 0 
        . 
        FIND CURRENT rguest NO-LOCK.
      END.
    END.
    FOR EACH rline WHERE rline.resnr = res-line.resnr
      AND rline.reslinnr NE res-line.reslinnr
      AND rline.zinr = res-line.zinr AND rline.l-zuordnung[3] = 0
      AND (rline.resstatus = 13 OR rline.resstatus = 8) NO-LOCK:
      ASSIGN history.bemerk = history.bemerk + "SH:" + rline.NAME + CHR(10).
    END.
  END.
  ELSE IF res-line.l-zuordnung[3] = 0 AND res-line.resstatus = 13 THEN
  DO:
    FIND FIRST rline WHERE rline.resnr = res-line.resnr
      AND rline.reslinnr NE res-line.reslinnr
      AND rline.zinr = res-line.zinr AND rline.l-zuordnung[3] = 0
      AND (rline.resstatus = 6 OR rline.resstatus = 8) NO-LOCK NO-ERROR.
    IF AVAILABLE rline THEN 
    ASSIGN history.bemerk = history.bemerk + "MG:" + rline.NAME + CHR(10).
  END.
  ELSE IF res-line.l-zuordnung[3] = 1 THEN
  DO:
    FIND FIRST rline WHERE rline.resnr = res-line.resnr
      AND rline.reslinnr = res-line.kontakt-nr NO-LOCK NO-ERROR.
    IF AVAILABLE rline THEN
    ASSIGN history.bemerk = history.bemerk + "MG:" + rline.NAME + CHR(10).
  END.

  IF reservation.kontakt-nr NE 0 THEN
  DO:
    FIND FIRST akt-kont WHERE akt-kont.gastnr = reservation.gastnr 
      AND akt-kont.kontakt-nr = reservation.kontakt-nr NO-LOCK NO-ERROR. 
    IF AVAILABLE akt-kont THEN 
    ASSIGN history.bemerk = history.bemerk + "CT:" + akt-kont.NAME 
      + ", " + akt-kont.vorname + CHR(10).
  END.
  
  ASSIGN
    history.gastnr      = res-line.gastnrmember
    history.ankunft     = res-line.ankunft
    history.abreise     = htparam.fdate
    history.zimmeranz   = res-line.zimmeranz 
    history.zikateg     = zimkateg.kurzbez
    history.zinr        = res-line.zinr
    history.erwachs     = res-line.erwachs 
    history.gratis      = res-line.gratis
    history.zipreis     = res-line.zipreis 
    history.arrangement = res-line.arrangement
    history.guestnrcom  = res-line.reserve-int
    history.gastinfo    = res-line.name + " - "  
                          + guest.adresse1 + ", " + guest.wohnort 
    history.abreisezeit = STRING(time, "HH:MM") 
    history.segmentcode = reservation.segmentcode 
    history.zi-wechsel  = NO
    history.resnr       = res-line.resnr 
    history.reslinnr    = res-line.reslinnr 
    history.betriebsnr  = INTEGER(res-line.pseudofix)
  . 
  IF res-line.bemerk NE "" THEN 
      history.bemerk = history.bemerk + "RL:" + res-line.bemerk    + CHR(10). 
  IF reservation.bemerk NE "" THEN 
      history.bemerk = history.bemerk + "R:"  + reservation.bemerk + CHR(10).

  FIND FIRST bill1 WHERE bill1.resnr = res-line.resnr AND bill1.reslinnr = 0 
    NO-LOCK NO-ERROR. 
  IF AVAILABLE bill1 THEN history.bemerk = history.bemerk 
    + "M:" + STRING(bill1.rechnr) + CHR(10). 

  found = NO.
  FOR EACH bill1 WHERE bill1.resnr = res-line.resnr AND bill1.parent-nr 
    = res-line.reslinnr AND bill1.zinr = res-line.zinr 
    AND bill1.rechnr GT 0 NO-LOCK:
    IF NOT found THEN history.bemerk = history.bemerk + "B:".
    ELSE history.bemerk = history.bemerk + "/".
    history.bemerk =  history.bemerk + STRING(bill1.rechnr). 
    found = YES.
  END.
  IF found THEN history.bemerk = history.bemerk + CHR(10).
  history.bemerk = history.bemerk + "C/O: " + user-init + CHR(10). 
 
  IF res-line.gastnr NE res-line.gastnrmember THEN 
  DO: 
    FIND FIRST history1 WHERE history1.resnr = res-line.resnr 
      AND history1.reslinnr = 999 EXCLUSIVE-LOCK NO-ERROR. 
    IF NOT AVAILABLE history1 THEN 
    DO: 
      CREATE history1. 
      IF AVAILABLE akt-kont THEN 
        ASSIGN history1.bemerk = history1.bemerk + "CT:" + akt-kont.NAME 
        + ", " + akt-kont.vorname + CHR(10).
      ASSIGN
        history1.gastnr = res-line.gastnr
        history1.resnr = res-line.resnr
        history1.reslinnr = 999
        history1.ankunft = res-line.ankunft 
        history1.abreise = res-line.abreise 
        history1.arrangement = res-line.arrangement 
        history1.gastinfo = res-line.resname
        history1.segmentcode = reservation.segmentcode 
      .
      IF reservation.bemerk NE "" THEN history1.bemerk 
        =  history1.bemerk + "R:" + reservation.bemerk + CHR(10).

      FIND FIRST bill1 WHERE bill1.resnr = res-line.resnr AND bill1.reslinnr = 0 
        NO-LOCK NO-ERROR. 
      IF AVAILABLE bill1 THEN history1.bemerk 
        = history1.bemerk + "M:" + STRING(bill1.rechnr) + CHR(10). 
      
      FIND FIRST bill1 WHERE bill1.resnr = resnr AND bill1.reslinnr = 0 
        AND bill1.flag = 0 NO-LOCK NO-ERROR. 
      IF AVAILABLE bill1 THEN 
      DO: 
        history1.logisumsatz  = bill1.logisumsatz. 
        history1.argtumsatz   = bill1.argtumsatz. 
        history1.f-b-umsatz   = bill1.f-b-umsatz. 
        history1.sonst-umsatz = bill1.sonst-umsatz. 
        history1.gesamtumsatz = bill1.gesamtumsatz. 
      END. 
    END. 
    history1.zimmeranz = history1.zimmeranz + res-line.zimmeranz. 
    IF history1.zipreis = 0 AND res-line.zipreis NE 0 THEN 
    DO: 
      ASSIGN 
        history1.zikateg = zimkateg.kurzbez 
        history1.zipreis = res-line.zipreis 
        history1.abreisezeit = STRING(time, "HH:MM"). 
    END. 
  END. 
 
  FOR EACH bill1 WHERE bill1.resnr = resnr AND bill1.parent-nr = reslinnr 
        AND bill1.flag = 1 AND bill1.zinr = res-line.zinr NO-LOCK: 
    tot-umsatz = tot-umsatz + bill1.gesamtumsatz. 
  END. 
 
  IF tot-umsatz NE 0 THEN 
  DO: 
    FOR EACH bill1 WHERE bill1.resnr = resnr 
      AND bill1.parent-nr = reslinnr 
      AND bill1.flag = 1 AND bill1.zinr = res-line.zinr NO-LOCK: 
      history.logisumsatz = history.logisumsatz + bill1.logisumsatz. 
      history.argtumsatz = history.argtumsatz + bill1.argtumsatz. 
      history.f-b-umsatz = history.f-b-umsatz + bill1.f-b-umsatz. 
      history.sonst-umsatz = history.sonst-umsatz + bill1.sonst-umsatz. 
      history.gesamtumsatz = history.gesamtumsatz + bill1.gesamtumsatz. 
      IF AVAILABLE history1 AND history1.gastnr = bill1.gastnr THEN 
      DO: 
        history1.logisumsatz = history1.logisumsatz + bill1.logisumsatz. 
        history1.argtumsatz = history1.argtumsatz + bill1.argtumsatz. 
        history1.f-b-umsatz = history1.f-b-umsatz + bill1.f-b-umsatz. 
        history1.sonst-umsatz = history1.sonst-umsatz + bill1.sonst-umsatz. 
        history1.gesamtumsatz = history1.gesamtumsatz + bill1.gesamtumsatz. 
      END. 
      FIND FIRST bill-line WHERE bill-line.rechnr = bill1.rechnr NO-LOCK 
         NO-ERROR. 
      found = NO.
      DO WHILE AVAILABLE bill-line AND NOT found: 
         FIND FIRST artikel WHERE artikel.artnr = bill-line.artnr 
           AND artikel.departement = bill-line.departement 
           AND (artart = 2 OR artart = 4 OR artart = 6 OR artart = 7) 
           NO-LOCK NO-ERROR. 
        IF AVAILABLE artikel THEN 
        DO: 
          found = YES. 
          history.zahlungsart = artikel.artnr. 
        END. 
        FIND NEXT bill-line WHERE bill-line.rechnr = bill1.rechnr NO-LOCK 
            NO-ERROR. 
      END. 
    END. 
  END. 
  IF AVAILABLE history1 THEN FIND CURRENT history1 NO-LOCK. 
END. 
 
ELSE IF res-mode = "roomchg" THEN 
DO: 
DEF VAR ziwechsel-str AS CHAR NO-UNDO.
  /*RUN ziwechsel-str.p(OUTPUT ziwechsel-str).*/

  CREATE history.
  ASSIGN
    history.gastnr = res-line.gastnrmember
    history.ankunft = res-line.ankunft
    history.abreise = res-line.abreise 
    history.zimmeranz = res-line.zimmeranz 
    history.zikateg = zimkateg.kurzbez
    history.zinr = old-zinr
    history.erwachs = res-line.erwachs
    history.gratis = res-line.gratis
    history.zipreis = res-line.zipreis 
    history.arrangement = res-line.arrangement
    history.abreisezeit = STRING(time, "HH:MM")
    history.gastinfo = res-line.name + " - " 
      + guest.adresse1 + ", " + guest.wohnort
    history.segmentcode = reservation.segmentcode 
    history.zi-wechsel = YES
    history.resnr = res-line.resnr 
    history.reslinnr = res-line.reslinnr
    history.betriebsnr = INTEGER(res-line.pseudofix)
  .
  history.bemerk = STRING(htparam.fdate) 
    + translateExtended (": Moved to",lvCAREA,"") + " " + res-line.zinr
    + CHR(10) + ziwechsel-str.

  CREATE res-history. 
  ASSIGN 
    res-history.nr = bediener.nr 
    res-history.datum = TODAY 
    res-history.zeit = TIME 
    res-history.aenderung = old-zinr + " -> " + res-line.zinr
    + CHR(10) + ziwechsel-str
    res-history.action = "RoomChange". 
  FIND CURRENT res-history NO-LOCK. 
  RELEASE res-history. 

END. 

ELSE IF res-mode = "HK-preference" THEN 
DO: 
  CREATE history.
  ASSIGN
    history.gastnr = res-line.gastnrmember
    history.ankunft = res-line.ankunft
    history.abreise = res-line.abreise 
    history.zimmeranz = res-line.zimmeranz 
    history.zikateg = zimkateg.kurzbez
    history.zinr = TRIM(ENTRY(1, old-zinr, ";"))
    history.erwachs = res-line.erwachs
    history.gratis = res-line.gratis
    history.zipreis = res-line.zipreis 
    history.arrangement = res-line.arrangement
    history.abreisezeit = STRING(time, "HH:MM")
    history.gastinfo = res-line.name + " - " 
      + guest.adresse1 + ", " + guest.wohnort
    history.segmentcode = reservation.segmentcode 
    history.zi-wechsel = NO
    history.resnr = res-line.resnr 
    history.reslinnr = res-line.reslinnr
    history.betriebsnr = INTEGER(res-line.pseudofix)
  .
  ASSIGN history.bemerk = translateExtended ("HK-Preference",lvCAREA,"")
       + ":=" + TRIM(ENTRY(2, old-zinr, ";")).
  FIND CURRENT history NO-LOCK.
END. 
