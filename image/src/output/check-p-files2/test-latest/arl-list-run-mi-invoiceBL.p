/*FT 301013 add for print advance bill by lnl*/
/*Eko 4 Februari 2015 add for print advance bill by BIRT*/

DEFINE TEMP-TABLE s-list 
  FIELD nr      AS INTEGER 
  FIELD ankunft AS DATE 
  FIELD abreise AS DATE 
  FIELD bezeich AS CHAR 
  FIELD rmcat   AS CHAR 
  FIELD preis   AS DECIMAL
  FIELD lRate   AS DECIMAL INITIAL 0
  FIELD datum   AS DATE 
  FIELD qty     AS INTEGER 
  FIELD erwachs AS INTEGER 
  FIELD kind1   AS INTEGER 
  FIELD kind2   AS INTEGER. 
 
DEFINE TEMP-TABLE t-list 
  FIELD nr      AS INTEGER 
  FIELD ankunft AS DATE 
  FIELD abreise AS DATE 
  FIELD bezeich AS CHAR 
  FIELD rmcat   AS CHAR 
  FIELD preis   AS DECIMAL 
  FIELD lRate   AS DECIMAL
  FIELD tage    AS INTEGER 
  FIELD date1   AS DATE 
  FIELD date2   AS DATE 
  FIELD qty     AS INTEGER 
  FIELD betrag  AS DECIMAL 
  FIELD erwachs AS INTEGER 
  FIELD kind1   AS INTEGER 
  FIELD kind2   AS INTEGER. 

DEFINE TEMP-TABLE t-reservation LIKE reservation.
DEFINE TEMP-TABLE t-res-line LIKE res-line.
DEFINE TEMP-TABLE t-guest LIKE guest.

DEFINE buffer rline FOR res-line. 
DEFINE buffer mbill FOR bill. 
DEFINE buffer mainres FOR reservation.


DEF INPUT PARAMETER resnr               AS INTEGER.
DEF INPUT PARAMETER curr-resnr          AS INTEGER.
DEF INPUT PARAMETER arl-list-reslinnr   AS INTEGER.
DEF INPUT PARAMETER t-active-flag       AS INTEGER.
DEF INPUT PARAMETER printtype           AS INTEGER.
DEF OUTPUT PARAMETER err-flag           AS INTEGER INIT 0.
DEF OUTPUT PARAMETER avail-master       AS LOGICAL INIT NO.
DEF OUTPUT PARAMETER avail-bill         AS LOGICAL INIT NO.
DEF OUTPUT PARAMETER reslinnr           AS INTEGER INIT 1.
DEF OUTPUT PARAMETER master-rechnr  LIKE master.rechnr.
DEF OUTPUT PARAMETER bill-rechnr    LIKE bill.rechnr.
DEF OUTPUT PARAMETER mainres-gastnr LIKE mainres.gastnr.
DEF OUTPUT PARAMETER TABLE FOR t-reservation.
DEF OUTPUT PARAMETER TABLE FOR t-res-line.
DEF OUTPUT PARAMETER TABLE FOR t-guest.
DEF OUTPUT PARAMETER TABLE FOR t-list.

DEFINE VARIABLE new-contrate        AS LOGICAL INITIAL NO. 
DEFINE VARIABLE resline-exrate      AS DECIMAL NO-UNDO INIT 0.
DEFINE VARIABLE billdate            AS DATE. 
DEFINE VARIABLE bonus-array         AS LOGICAL EXTENT 999 INITIAL NO. 
DEFINE VARIABLE tot-amt             AS DECIMAL.

DEFINE STREAM s1.

FOR EACH t-reservation:
    DELETE t-reservation.
END.
FOR EACH t-res-line:
    DELETE t-res-line.
END.
FOR EACH t-guest:
    DELETE t-guest.
END.
FOR EACH s-list:
    DELETE s-list.
END.
FOR EACH t-list:
    DELETE t-list.
END.

FIND FIRST htparam WHERE htparam.paramnr = 550 NO-LOCK.
IF htparam.feldtyp = 4 THEN new-contrate = htparam.flogical.

FIND FIRST vhp.htparam WHERE vhp.htparam.paramnr = 110 NO-LOCK. 
billdate = vhp.htparam.fdate. 

/*FIND FIRST master WHERE master.resnr = resnr NO-LOCK NO-ERROR. 
IF NOT AVAILABLE master AND t-active-flag = 0 THEN 
DO:
    err-flag = 1.
    RETURN NO-APPLY.
END.*/


FIND FIRST mainres WHERE mainres.resnr = resnr NO-LOCK.
ASSIGN mainres-gastnr = mainres.gastnr.
FIND FIRST rline WHERE rline.resnr = resnr AND rline.active-flag LE 1 NO-LOCK. 
IF curr-resnr = resnr THEN reslinnr = arl-list-reslinnr.
ELSE reslinnr = rline.reslinnr. 

FIND FIRST master WHERE master.resnr = resnr NO-LOCK NO-ERROR. 
IF AVAILABLE master THEN 
DO:
    master-rechnr = master.rechnr.
    avail-master = YES.
END.
    
FIND FIRST bill WHERE bill.resnr = resnr AND bill.reslinnr = reslinnr NO-LOCK NO-ERROR.
IF AVAILABLE bill THEN 
DO:
    bill-rechnr = bill.rechnr.
    avail-bill = YES.
END.

FIND FIRST reservation WHERE reservation.resnr = resnr NO-LOCK NO-ERROR.
IF AVAILABLE reservation THEN
DO:
    CREATE t-reservation.
    BUFFER-COPY reservation TO t-reservation.
END.
FIND FIRST res-line WHERE res-line.resnr = resnr AND res-line.reslinnr = reslinnr NO-LOCK NO-ERROR.
IF AVAILABLE res-line THEN
DO: 
    CREATE t-res-line.
    BUFFER-COPY res-line TO t-res-line.
    FIND FIRST guest WHERE guest.gastnr = res-line.gastnr NO-LOCK NO-ERROR.
    IF AVAILABLE guest THEN
    DO:
        CREATE t-guest.
        BUFFER-COPY guest TO t-guest.
    END.
END.

IF printtype = 2 OR printtype = 3 THEN /* Eko add print type = 3 for print by BIRT*/
DO:
    IF avail-master THEN 
        RUN read-proforma-inv(resnr,master.rechnr). 
    ELSE 
    DO: 
        IF avail-bill THEN
          RUN read-proforma-inv1(resnr,reslinnr,bill.rechnr).
        ELSE RUN read-proforma-inv1(resnr,reslinnr,0).
    END.
END.


PROCEDURE read-proforma-inv: 
DEFINE INPUT PARAMETER resnr    AS INTEGER.
DEFINE INPUT PARAMETER rechnr   AS INTEGER.
DEFINE VARIABLE datum           AS DATE. 
DEFINE VARIABLE co-date         AS DATE. 
DEFINE VARIABLE add-it          AS LOGICAL. 
DEFINE VARIABLE ankunft         AS DATE. 
DEFINE VARIABLE abreise         AS DATE. 
DEFINE VARIABLE rm-rate         AS DECIMAL. 
DEFINE VARIABLE argt-rate       AS DECIMAL. 
DEFINE VARIABLE argt-defined    AS LOGICAL. 
DEFINE VARIABLE delta           AS INTEGER. 
DEFINE VARIABLE start-date      AS DATE. 
DEFINE VARIABLE fixed-rate      AS LOGICAL. 
DEFINE VARIABLE qty             AS INTEGER. 
DEFINE VARIABLE it-exist        AS LOGICAL INITIAL NO. 
DEFINE VARIABLE exrate1         AS DECIMAL INITIAL 1. 
DEFINE VARIABLE ex2             AS DECIMAL INITIAL 1. 
DEFINE VARIABLE pax             AS INTEGER NO-UNDO. 
DEFINE VARIABLE child1          AS INTEGER NO-UNDO. 
DEFINE VARIABLE bill-date       AS DATE NO-UNDO. 
DEFINE VARIABLE curr-zikatnr    AS INTEGER NO-UNDO. 
 
DEFINE VARIABLE ebdisc-flag     AS LOGICAL INITIAL NO   NO-UNDO.
DEFINE VARIABLE kbdisc-flag     AS LOGICAL INITIAL NO   NO-UNDO.
DEFINE VARIABLE rate-found      AS LOGICAL INITIAL NO   NO-UNDO.
DEFINE VARIABLE early-flag      AS LOGICAL              NO-UNDO.
DEFINE VARIABLE kback-flag      AS LOGICAL              NO-UNDO.

DEFINE VARIABLE count-heritage  AS INTEGER INITIAL 0    NO-UNDO.
DEFINE VARIABLE count-night     AS INTEGER              NO-UNDO.
DEFINE VARIABLE dept            AS INTEGER              NO-UNDO.
DEFINE VARIABLE loopi           AS INTEGER              NO-UNDO.
DEFINE VARIABLE curr-no         AS INTEGER INITIAL 1000 NO-UNDO.
DEFINE VARIABLE do-it           AS LOGICAL              NO-UNDO.


DEFINE BUFFER w1                FOR vhp.waehrung. 
DEFINE BUFFER resline           FOR vhp.res-line. 

DEF VAR i AS INT.
DEF VAR j AS INT.
DEF VAR qty1 AS INT.

 
  FOR EACH resline WHERE resline.resnr = resnr 
    AND resline.active-flag LT 2 AND resline.resstatus NE 12 
    AND resline.resstatus NE 9 AND resline.resstatus NE 10 
    AND resline.resstatus NE 99 NO-LOCK: 
 
    ebdisc-flag = resline.zimmer-wunsch MATCHES ("*ebdisc*").
    kbdisc-flag = resline.zimmer-wunsch MATCHES ("*kbdisc*").
    IF resline.l-zuordnung[1] NE 0 THEN curr-zikatnr = resline.l-zuordnung[1]. 
    ELSE curr-zikatnr = resline.zikatnr. 
 
    FIND FIRST zimkateg WHERE zimkateg.zikatnr = resline.zikatnr NO-LOCK. 
    FIND FIRST arrangement WHERE arrangement.arrangement 
      = resline.arrangement NO-LOCK. 
    ankunft = resline.ankunft. 
    abreise = resline.abreise. 
    fixed-rate = NO. 
    IF resline.was-status = 1 THEN fixed-rate = YES. 
    co-date = resline.abreise. 
    IF co-date GT resline.ankunft THEN co-date = co-date - 1. 
 
    RUN create-bonus. 
 
    DO datum = resline.ankunft TO co-date: 
      bill-date = datum. 
      argt-rate = 0. 
      rm-rate = resline.zipreis. 
      pax = resline.erwachs. 
/*    IF resline.erwachs GT 0 THEN */ 
  
      IF fixed-rate THEN 
      DO: 
        FIND FIRST reslin-queasy WHERE reslin-queasy.key = "arrangement" 
          AND reslin-queasy.resnr = resline.resnr 
          AND reslin-queasy.reslinnr = resline.reslinnr 
          AND datum GE vhp.reslin-queasy.date1 
          AND datum LE vhp.reslin-queasy.date2 NO-LOCK NO-ERROR. 
        IF AVAILABLE reslin-queasy THEN 
        DO: 
          rm-rate = reslin-queasy.deci1. 
          IF reslin-queasy.number3 NE 0 THEN pax = reslin-queasy.number3. 
        END. 
        /*RUN usr-prog1(datum, INPUT-OUTPUT rm-rate, OUTPUT it-exist).*/
      END. 
      ELSE 
      DO: 
        FIND FIRST vhp.guest WHERE vhp.guest.gastnr = resline.gastnr NO-LOCK. 
        FIND FIRST vhp.guest-pr WHERE vhp.guest-pr.gastnr = vhp.guest.gastnr 
          NO-LOCK NO-ERROR. 
        IF AVAILABLE vhp.guest-pr THEN 
        DO: 
          FIND FIRST vhp.queasy WHERE vhp.queasy.key = 18 AND vhp.queasy.number1 
            = resline.reserve-int NO-LOCK NO-ERROR. 
          IF AVAILABLE vhp.queasy AND vhp.queasy.logi3 THEN 
          bill-date = resline.ankunft. 
            
          IF new-contrate THEN 
          DO:
            IF resline-exrate NE 0 THEN
            RUN ratecode-rate.p(ebdisc-flag, kbdisc-flag, resline.resnr, 
              resline.reslinnr, vhp.guest-pr.CODE, ?, bill-date, resline.ankunft,
              resline.abreise, resline.reserve-int, vhp.arrangement.argtnr,
              curr-zikatnr, resline.erwachs, resline.kind1, resline.kind2,
              resline-exrate, resline.betriebsnr, OUTPUT rate-found,
              OUTPUT rm-rate, OUTPUT early-flag, OUTPUT kback-flag).
            ELSE
            RUN ratecode-rate.p(ebdisc-flag, kbdisc-flag, resline.resnr, 
              resline.reslinnr, vhp.guest-pr.CODE, ?, bill-date, resline.ankunft,
              resline.abreise, resline.reserve-int, vhp.arrangement.argtnr,
              curr-zikatnr, resline.erwachs, resline.kind1, resline.kind2,
              resline.reserve-dec, resline.betriebsnr, OUTPUT rate-found,
              OUTPUT rm-rate, OUTPUT early-flag, OUTPUT kback-flag).
          END.
          ELSE
          DO:
            RUN pricecod-rate.p(resline.resnr, resline.reslinnr,
              vhp.guest-pr.CODE, bill-date, resline.ankunft, resline.abreise, 
              resline.reserve-int, vhp.arrangement.argtnr, curr-zikatnr, 
              resline.erwachs, resline.kind1, resline.kind2,
              resline.reserve-dec, resline.betriebsnr, 
              OUTPUT rm-rate, OUTPUT rate-found).
            /*RUN usr-prog2(datum, INPUT-OUTPUT rm-rate, OUTPUT it-exist).*/
            IF it-exist THEN rate-found = YES.
            IF NOT it-exist AND bonus-array[datum - resline.ankunft + 1] = YES 
              THEN rm-rate = 0.  
          END. /* old contract rate */
        END.   /* availab;e vhp.guest-pr */  
      END.     /* IF contract rate */ 

      FIND FIRST s-list WHERE s-list.bezeich = vhp.arrangement.argt-rgbez 
        AND s-list.rmcat = vhp.zimkateg.kurzbez 
        AND s-list.preis = rm-rate 
        AND s-list.datum = datum 
        AND s-list.ankunft = resline.ankunft 
        AND s-list.abreise = resline.abreise 
        AND s-list.erwachs = pax 
        AND s-list.kind1 = resline.kind1 
        AND s-list.kind2 = resline.kind2 NO-ERROR. 
      IF NOT AVAILABLE s-list THEN 
      DO: 
        CREATE s-list. 
        s-list.bezeich = vhp.arrangement.argt-rgbez. 
        s-list.rmcat = vhp.zimkateg.kurzbez. 
        s-list.preis = rm-rate. 
        s-list.datum = datum. 
        s-list.ankunft = resline.ankunft. 
        s-list.abreise = resline.abreise. 
        s-list.erwachs = pax. 
        s-list.kind1 = resline.kind1. 
        s-list.kind2 = resline.kind2. 
      END. 
      s-list.qty = s-list.qty + resline.zimmeranz. 
 
/**** additional fix cost ******/ 
      FOR EACH vhp.fixleist WHERE vhp.fixleist.resnr = resline.resnr 
        AND vhp.fixleist.reslinnr = resline.reslinnr NO-LOCK: 
        add-it = NO. 
        argt-rate = 0. 
        IF vhp.fixleist.sequenz = 1 THEN add-it = YES. 
        ELSE IF vhp.fixleist.sequenz = 2 OR vhp.fixleist.sequenz = 3 THEN 
        DO: 
          IF resline.ankunft EQ datum THEN add-it = YES. 
        END. 
        ELSE IF vhp.fixleist.sequenz = 4 AND day(datum) = 1 THEN add-it = YES. 
        ELSE IF vhp.fixleist.sequenz = 5 
          AND day(datum + 1) = 1 THEN add-it = YES. 
        ELSE IF vhp.fixleist.sequenz = 6 THEN 
        DO: 
          IF lfakt = ? THEN delta = 0. 
          ELSE 
          DO: 
            delta = lfakt - resline.ankunft. 
            IF delta LT 0 THEN delta = 0. 
          END. 
          start-date = resline.ankunft + delta. 
          IF (resline.abreise - start-date) LT vhp.fixleist.dekade 
            THEN start-date = resline.ankunft. 
          IF datum LE (start-date + (vhp.fixleist.dekade - 1)) THEN add-it = YES. 
          IF datum LT start-date THEN add-it = no. /* may NOT post !! */ 
        END. 
        IF add-it THEN 
        DO: 
          FIND FIRST vhp.artikel WHERE vhp.artikel.artnr = vhp.fixleist.artnr 
            AND vhp.artikel.departement = vhp.fixleist.departement NO-LOCK. 
          argt-rate = vhp.fixleist.betrag * vhp.fixleist.number. 
          IF NOT fixed-rate AND AVAILABLE vhp.guest-pr THEN 
          DO: 
          DEF VAR ct       AS CHAR.
          DEF VAR contcode AS CHAR.
            contcode = vhp.guest-pr.CODE.
            ct = resline.zimmer-wunsch.
            IF ct MATCHES("*$CODE$*") THEN
            DO:
              ct = SUBSTR(ct,INDEX(ct,"$CODE$") + 6).
              contcode = SUBSTR(ct, 1, INDEX(ct,";") - 1).
            END.
            FIND FIRST vhp.reslin-queasy WHERE vhp.reslin-queasy.key = "argt-line" 
              AND vhp.reslin-queasy.char1 = contcode 
              AND vhp.reslin-queasy.number1 = resline.reserve-int 
              AND vhp.reslin-queasy.number2 = vhp.arrangement.argtnr 
              AND vhp.reslin-queasy.reslinnr = resline.zikatnr 
              AND vhp.reslin-queasy.number3 = vhp.fixleist.artnr 
              AND vhp.reslin-queasy.resnr = vhp.fixleist.departement 
              AND bill-date GE vhp.reslin-queasy.date1 
              AND bill-date LE vhp.reslin-queasy.date2 NO-LOCK NO-ERROR. 
            IF AVAILABLE vhp.reslin-queasy THEN 
              argt-rate = vhp.reslin-queasy.deci1 * vhp.fixleist.number. 
          END. 
        END. 
        IF argt-rate NE 0 THEN 
        DO: 
          FIND FIRST s-list WHERE s-list.bezeich = vhp.artikel.bezeich 
            AND s-list.preis = (argt-rate / vhp.fixleist.number) 
            AND s-list.datum = datum 
            AND s-list.ankunft = resline.ankunft 
            AND s-list.abreise = resline.abreise 
            AND s-list.erwachs = pax 
            AND s-list.kind1 = resline.kind1 
            AND s-list.kind2 = resline.kind2 NO-ERROR. 
          IF NOT AVAILABLE s-list THEN 
          DO: 
            CREATE s-list. 
            s-list.nr = vhp.artikel.artnr. 
            s-list.bezeich = vhp.artikel.bezeich. 
            s-list.preis = argt-rate / vhp.fixleist.number. 
            s-list.datum = datum. 
            s-list.ankunft = resline.ankunft. 
            s-list.abreise = resline.abreise. 
            s-list.erwachs = pax. 
            s-list.kind1 = resline.kind1. 
            s-list.kind2 = resline.kind2. 
          END. 
          s-list.qty = s-list.qty + (vhp.fixleist.number * resline.zimmeranz). 
        END. /* argt-rate NE 0 */  
      END.   /* each vhp.fixleist */ 
    END.     /* datum */
  END.       /* for each resline */
  
  FOR EACH s-list BY s-list.ankunft BY s-list.datum BY s-list.bezeich 
    BY s-list.erwachs:  
    IF s-list.nr = 0 THEN 
    DO: 
      FIND FIRST t-list WHERE t-list.bezeich = s-list.bezeich 
        AND t-list.rmcat = s-list.rmcat 
        AND t-list.preis = s-list.preis 
        AND t-list.ankunft = s-list.ankunft 
        AND t-list.abreise = s-list.abreise 
        AND t-list.erwachs = s-list.erwachs 
        AND t-list.kind1 = s-list.kind1 
        AND t-list.kind2 = s-list.kind2 NO-ERROR. 
      IF NOT AVAILABLE t-list THEN 
      DO: 
        create t-list. 
        t-list.nr = s-list.nr. 
        t-list.bezeich = s-list.bezeich. 
        t-list.rmcat = s-list.rmcat. 
        t-list.preis = s-list.preis. 
        t-list.date1 = s-list.datum. 
        t-list.ankunft = s-list.ankunft. 
        t-list.abreise = s-list.abreise. 
        t-list.erwachs = s-list.erwachs. 
        t-list.kind1 = s-list.kind1. 
        t-list.kind2 = s-list.kind2.
      END. 
      IF s-list.qty GE t-list.qty THEN   /*FT 22/10/13*/
      t-list.tage = t-list.tage + 1.
      t-list.date2 = s-list.datum. 
      IF s-list.datum = t-list.date1 THEN t-list.qty = t-list.qty + s-list.qty.
      /*FT 22/10/13*/
      IF s-list.qty NE t-list.qty AND s-list.preis = t-list.preis THEN
      DO:
          qty1 = t-list.qty.
          CREATE t-list.
          ASSIGN
            t-list.nr = s-list.nr
            t-list.bezeich = s-list.bezeich 
            t-list.rmcat = s-list.rmcat 
            t-list.preis = s-list.preis 
            t-list.date1 = s-list.datum 
            t-list.ankunft = s-list.ankunft 
            t-list.abreise = s-list.abreise 
            t-list.erwachs = s-list.erwachs
            t-list.kind1 = s-list.kind1
            t-list.kind2 = s-list.kind2
            t-list.date1 = s-list.datum
            t-list.date2 = s-list.datum
            t-list.tage  = 1.
          IF s-list.qty GT qty1 THEN
            ASSIGN  
              j = s-list.qty - qty1
              t-list.qty = j.
          ELSE
            ASSIGN
              j = qty1 - s-list.qty
              t-list.qty = s-list.qty.
      END. /*endFT 22/10/13*/
    END. 
    ELSE 
    DO: 
      FIND FIRST t-list WHERE t-list.bezeich = s-list.bezeich 
        AND t-list.preis = s-list.preis 
        AND t-list.ankunft = s-list.ankunft 
        AND t-list.abreise = s-list.abreise 
        AND t-list.erwachs = s-list.erwachs 
        AND t-list.kind1 = s-list.kind1 
        AND t-list.kind2 = s-list.kind2 NO-ERROR. 
      IF NOT AVAILABLE t-list THEN 
      DO: 
        create t-list. 
        t-list.nr = s-list.nr. 
        t-list.bezeich = s-list.bezeich. 
        t-list.preis = s-list.preis. 
        t-list.date1 = s-list.datum. 
        t-list.ankunft = s-list.ankunft. 
        t-list.abreise = s-list.abreise. 
        t-list.erwachs = s-list.erwachs. 
        t-list.kind1 = s-list.kind1. 
        t-list.kind2 = s-list.kind2. 
      END. 
      t-list.tage = t-list.tage + 1. 
      t-list.date2 = s-list.datum. 
      IF s-list.datum = t-list.date1 THEN t-list.qty = t-list.qty + s-list.qty. 
    END.
    DELETE s-list. 
  END. 
  tot-amt = 0.
  FOR EACH t-list: 
    t-list.betrag = t-list.qty * t-list.tage * t-list.preis.
    tot-amt = tot-amt + t-list.betrag.
  END. 

  IF rechnr GT 0 THEN
  DO:
      FOR EACH bill-line WHERE bill-line.rechnr = bill.rechnr NO-LOCK,
          FIRST artikel WHERE artikel.artnr = bill-line.artnr
          AND artikel.departement = bill-line.departement NO-LOCK
          BY bill-line.bill-datum BY bill-line.zeit:
          do-it = YES.
          IF artikel.artart EQ 9 THEN
          DO:
              FIND FIRST arrangement WHERE arrangement.argt-artikelnr
                  = artikel.artnr NO-LOCK NO-ERROR.
              IF NOT AVAILABLE arrangement OR arrangement.segmentcode = 0 THEN
                  do-it = NO.
          END.
          IF do-it THEN DO:
            IF artikel.bezeich MATCHES "Heritage Fee*" THEN DO: 
                FIND FIRST t-list WHERE t-list.bezeich = bill-line.bezeich NO-ERROR.
                IF NOT AVAILABLE t-list THEN CREATE t-list. 

                ASSIGN 
                    count-heritage = count-heritage + 1
                    dept           = artikel.departement
                    t-list.preis   = bill-line.betrag
                    t-list.qty     = t-list.qty + 1
                    t-list.tage    = t-list.tage + 1
                    t-list.betrag  = t-list.betrag + bill-line.betrag.
            END.
            ELSE DO:
                CREATE t-list.
                ASSIGN 
                    t-list.preis   = 0
                    t-list.betrag  = bill-line.betrag.
            END.
           
            ASSIGN
              curr-no = curr-no + 1
              t-list.nr = curr-no 
              t-list.bezeich = bill-line.bezeich
              t-list.date1   = bill-line.bill-datum. 
          END.
      END.
  END.

  /*for penang*/
  FIND FIRST res-line WHERE res-line.resnr = resnr AND res-line.reslinnr = reslinnr NO-LOCK NO-ERROR.
  IF AVAILABLE res-line THEN ASSIGN count-night = res-line.abreise - res-line.ankunft.
  IF count-heritage LT count-night THEN DO:
      DO loopi = (count-heritage + 1) TO count-night:
          FIND FIRST artikel WHERE artikel.bezeich MATCHES "Heritage Fee*"
              AND artikel.departement = dept NO-LOCK NO-ERROR.
          IF AVAILABLE artikel THEN DO:
              FIND FIRST bill-line WHERE bill-line.rechnr = bill.rechnr 
                  AND bill-line.artnr = artikel.artnr NO-LOCK NO-ERROR.
              IF AVAILABLE bill-line THEN DO:
                  FIND FIRST t-list WHERE t-list.bezeich = bill-line.bezeich NO-LOCK NO-ERROR.
                  IF AVAILABLE t-list THEN DO:
                      FIND CURRENT t-list EXCLUSIVE-LOCK.
                      ASSIGN t-list.betrag = t-list.betrag + bill-line.betrag.
                      FIND CURRENT t-list NO-LOCK.
                  END.
                  ELSE IF NOT AVAILABLE t-list THEN DO:
                      CREATE t-list.
                      ASSIGN
                          curr-no        = curr-no + 1
                          t-list.nr      = curr-no 
                          t-list.bezeich = bill-line.bezeich
                          t-list.preis   = artikel.epreis
                          t-list.date1   = res-line.ankunft
                          t-list.betrag  = bill-line.betrag. 
                  END.
              END.
              ELSE DO:
                  FIND FIRST t-list WHERE t-list.bezeich = artikel.bezeich NO-LOCK NO-ERROR.
                  IF AVAILABLE t-list THEN DO:
                      FIND CURRENT t-list EXCLUSIVE-LOCK.
                      ASSIGN t-list.betrag  = t-list.betrag + artikel.epreis.
                      FIND CURRENT t-list NO-LOCK.
                  END.
                  ELSE IF NOT AVAILABLE t-list THEN DO:
                      CREATE t-list.
                      ASSIGN
                          curr-no        = curr-no + 1
                          t-list.nr      = curr-no 
                          t-list.bezeich = artikel.bezeich
                          t-list.preis   = artikel.epreis
                          t-list.date1   = res-line.ankunft
                          t-list.betrag  = artikel.epreis
                          t-list.betrag  = artikel.epreis. 
                  END.
              END.
          END.
      END.
      FOR EACH t-list WHERE t-list.bezeich MATCHES "Heritage Fee*":
          ASSIGN
              t-list.qty    = res-line.zimmeranz
              t-list.tage   = count-night
              t-list.betrag = t-list.betrag * t-list.qty.
      END.
  END. /*end*/
END. 
 
PROCEDURE read-proforma-inv1: 
DEFINE INPUT PARAMETER resnr    AS INTEGER.
DEFINE INPUT PARAMETER reslinnr AS INTEGER.
DEFINE INPUT PARAMETER rechnr   AS INTEGER.
DEFINE VARIABLE datum           AS DATE. 
DEFINE VARIABLE co-date         AS DATE. 
DEFINE VARIABLE add-it          AS LOGICAL. 
DEFINE VARIABLE ankunft         AS DATE. 
DEFINE VARIABLE abreise         AS DATE. 
DEFINE VARIABLE rm-rate         AS DECIMAL. 
DEFINE VARIABLE argt-rate       AS DECIMAL. 
DEFINE VARIABLE argt-defined    AS LOGICAL. 
DEFINE VARIABLE delta           AS INTEGER. 
DEFINE VARIABLE start-date      AS DATE. 
DEFINE VARIABLE fixed-rate      AS LOGICAL. 
DEFINE VARIABLE qty             AS INTEGER. 
DEFINE VARIABLE it-exist        AS LOGICAL INITIAL NO. 
DEFINE VARIABLE exrate1         AS DECIMAL INITIAL 1. 
DEFINE VARIABLE ex2             AS DECIMAL INITIAL 1. 
DEFINE VARIABLE pax             AS INTEGER NO-UNDO. 
DEFINE VARIABLE child1          AS INTEGER NO-UNDO. 
DEFINE VARIABLE bill-date       AS DATE NO-UNDO. 
DEFINE VARIABLE curr-zikatnr    AS INTEGER NO-UNDO. 

DEFINE VARIABLE curr-no         AS INTEGER INITIAL 1000 NO-UNDO.
DEFINE VARIABLE do-it           AS LOGICAL              NO-UNDO.
DEFINE VARIABLE curr-date       AS DATE                 NO-UNDO.
DEFINE VARIABLE lRate           AS DECIMAL              NO-UNDO.

DEFINE VARIABLE ebdisc-flag     AS LOGICAL INITIAL NO   NO-UNDO.
DEFINE VARIABLE kbdisc-flag     AS LOGICAL INITIAL NO   NO-UNDO.
DEFINE VARIABLE rate-found      AS LOGICAL INITIAL NO   NO-UNDO.
DEFINE VARIABLE early-flag      AS LOGICAL              NO-UNDO.
DEFINE VARIABLE kback-flag      AS LOGICAL              NO-UNDO.
DEFINE VARIABLE count-heritage  AS INTEGER INITIAL 0    NO-UNDO.
DEFINE VARIABLE count-night     AS INTEGER              NO-UNDO.
DEFINE VARIABLE dept            AS INTEGER              NO-UNDO.
DEFINE VARIABLE loopi           AS INTEGER              NO-UNDO.

DEFINE BUFFER w1                FOR vhp.waehrung. 
DEFINE BUFFER resline           FOR vhp.res-line. 
  
  FOR EACH resline WHERE resline.resnr = resnr 
    AND resline.reslinnr = reslinnr NO-LOCK: 
    
    ebdisc-flag = resline.zimmer-wunsch MATCHES ("*ebdisc*").
    kbdisc-flag = resline.zimmer-wunsch MATCHES ("*kbdisc*").
    IF resline.l-zuordnung[1] NE 0 THEN curr-zikatnr = resline.l-zuordnung[1]. 
    ELSE curr-zikatnr = resline.zikatnr. 
 
    FIND FIRST vhp.zimkateg WHERE vhp.zimkateg.zikatnr = resline.zikatnr NO-LOCK. 
    FIND FIRST vhp.arrangement WHERE vhp.arrangement.arrangement 
      = resline.arrangement NO-LOCK. 
    ankunft = resline.ankunft. 
    abreise = resline.abreise. 
    fixed-rate = NO. 
    IF resline.was-status = 1 THEN fixed-rate = YES. 
    co-date = resline.abreise. 
    IF co-date GT resline.ankunft THEN co-date = co-date - 1. 
 
    RUN create-bonus. 
 
    DO datum = resline.ankunft TO co-date: 
      bill-date = datum. 
      argt-rate = 0. 
      rm-rate = resline.zipreis. 
      pax = resline.erwachs. 
/*    IF resline.erwachs GT 0 THEN */ 
      IF fixed-rate THEN 
      DO: 
        FIND FIRST vhp.reslin-queasy WHERE vhp.reslin-queasy.key = "arrangement" 
          AND vhp.reslin-queasy.resnr = resline.resnr 
          AND vhp.reslin-queasy.reslinnr = resline.reslinnr 
          AND datum GE vhp.reslin-queasy.date1 
          AND datum LE vhp.reslin-queasy.date2 NO-LOCK NO-ERROR. 
        IF AVAILABLE vhp.reslin-queasy THEN 
        DO: 
          rm-rate = vhp.reslin-queasy.deci1. 
          IF vhp.reslin-queasy.number3 NE 0 THEN pax = vhp.reslin-queasy.number3. 
        END. 
        /*RUN usr-prog1(datum, INPUT-OUTPUT rm-rate, OUTPUT it-exist). */
      END. 
      ELSE 
      DO: 
        FIND FIRST vhp.guest WHERE vhp.guest.gastnr = resline.gastnr NO-LOCK. 
        FIND FIRST vhp.guest-pr WHERE vhp.guest-pr.gastnr = vhp.guest.gastnr 
          NO-LOCK NO-ERROR. 
        IF AVAILABLE vhp.guest-pr THEN 
        DO: 
          FIND FIRST vhp.queasy WHERE vhp.queasy.key = 18 AND vhp.queasy.number1 
            = resline.reserve-int NO-LOCK NO-ERROR. 
          IF AVAILABLE vhp.queasy AND vhp.queasy.logi3 THEN 
          bill-date = resline.ankunft. 
            
          IF new-contrate THEN 
          DO:
            IF resline-exrate NE 0 THEN
            RUN ratecode-rate.p(ebdisc-flag, kbdisc-flag, resline.resnr, 
              resline.reslinnr, vhp.guest-pr.CODE, ?, bill-date, resline.ankunft,
              resline.abreise, resline.reserve-int, vhp.arrangement.argtnr,
              curr-zikatnr, resline.erwachs, resline.kind1, resline.kind2,
              resline-exrate, resline.betriebsnr, OUTPUT rate-found,
              OUTPUT rm-rate, OUTPUT early-flag, OUTPUT kback-flag).
            ELSE
            RUN ratecode-rate.p(ebdisc-flag, kbdisc-flag, resline.resnr, 
              resline.reslinnr, vhp.guest-pr.CODE, ?, bill-date, resline.ankunft,
              resline.abreise, resline.reserve-int, vhp.arrangement.argtnr,
              curr-zikatnr, resline.erwachs, resline.kind1, resline.kind2,
              resline.reserve-dec, resline.betriebsnr, OUTPUT rate-found,
              OUTPUT rm-rate, OUTPUT early-flag, OUTPUT kback-flag).
          END.
          ELSE
          DO:
            RUN pricecod-rate.p(resline.resnr, resline.reslinnr,
              vhp.guest-pr.CODE, bill-date, resline.ankunft, resline.abreise, 
              resline.reserve-int, vhp.arrangement.argtnr, curr-zikatnr, 
              resline.erwachs, resline.kind1, resline.kind2,
              resline.reserve-dec, resline.betriebsnr, 
              OUTPUT rm-rate, OUTPUT rate-found).
            /*RUN usr-prog2(datum, INPUT-OUTPUT rm-rate, OUTPUT it-exist).*/
            IF it-exist THEN rate-found = YES.
            IF NOT it-exist AND bonus-array[datum - resline.ankunft + 1] = YES 
              THEN rm-rate = 0.  
          END. /* old contract rate */
        END.   /* availab;e vhp.guest-pr */  
      END.     /* IF contract rate */ 
 
      lRate = rm-rate.
      IF datum LT billdate THEN
      DO:
          FIND FIRST genstat WHERE genstat.resnr = resnr
              AND genstat.res-int[1] = reslinnr
              AND genstat.datum = datum NO-LOCK NO-ERROR.
          IF AVAILABLE genstat THEN rm-rate = genstat.rateLocal.
          ELSE
          DO:
              FIND FIRST exrate WHERE exrate.artnr = resline.betriebsnr
                  AND exrate.datum = datum NO-LOCK NO-ERROR.
              IF AVAILABLE exrate THEN lRate = rm-rate * exrate.betrag.
          END.
      END.
      ELSE
      DO:
          FIND FIRST waehrung WHERE waehrung.waehrungsnr = resline.betriebsnr
              NO-LOCK NO-ERROR.
          IF AVAILABLE waehrung THEN 
            lRate = rm-rate * waehrung.ankauf / waehrung.einheit.
      END.

      FIND FIRST s-list WHERE s-list.bezeich = vhp.arrangement.argt-rgbez 
        AND s-list.rmcat = vhp.zimkateg.kurzbez 
        AND s-list.preis = rm-rate 
        AND s-list.lRate = lRate
        AND s-list.datum = datum 
        AND s-list.ankunft = resline.ankunft 
        AND s-list.abreise = resline.abreise 
        AND s-list.erwachs = pax 
        AND s-list.kind1 = resline.kind1 
        AND s-list.kind2 = resline.kind2 NO-ERROR. 
      IF NOT AVAILABLE s-list THEN 
      DO: 
        CREATE s-list. 
        ASSIGN
          s-list.bezeich = vhp.arrangement.argt-rgbez
          s-list.rmcat = vhp.zimkateg.kurzbez
          s-list.preis = rm-rate
          s-list.lRate = lRate
          s-list.datum = datum 
          s-list.ankunft = resline.ankunft
          s-list.abreise = resline.abreise 
          s-list.erwachs = pax
          s-list.kind1 = resline.kind1 
          s-list.kind2 = resline.kind2
        . 
      END. 
      s-list.qty = s-list.qty + resline.zimmeranz. 

/**** additional fix cost ******/ 
      FOR EACH vhp.fixleist WHERE vhp.fixleist.resnr = resline.resnr 
        AND vhp.fixleist.reslinnr = resline.reslinnr NO-LOCK: 
        add-it = NO. 
        argt-rate = 0. 
        IF vhp.fixleist.sequenz = 1 THEN add-it = YES. 
        ELSE IF vhp.fixleist.sequenz = 2 OR vhp.fixleist.sequenz = 3 THEN 
        DO: 
          IF resline.ankunft EQ datum THEN add-it = YES. 
        END. 
        ELSE IF vhp.fixleist.sequenz = 4 AND day(datum) = 1 THEN add-it = YES. 
        ELSE IF vhp.fixleist.sequenz = 5 
          AND day(datum + 1) = 1 THEN add-it = YES. 
        ELSE IF vhp.fixleist.sequenz = 6 THEN 
        DO: 
          IF lfakt = ? THEN delta = 0. 
          ELSE 
          DO: 
            delta = lfakt - resline.ankunft. 
            IF delta LT 0 THEN delta = 0. 
          END. 
          start-date = resline.ankunft + delta. 
          IF (resline.abreise - start-date) LT vhp.fixleist.dekade 
            THEN start-date = resline.ankunft. 
          IF datum LE (start-date + (vhp.fixleist.dekade - 1)) THEN add-it = YES. 
          IF datum LT start-date THEN add-it = no. /* may NOT post !! */ 
        END. 
        IF add-it THEN 
        DO: 
          FIND FIRST vhp.artikel WHERE vhp.artikel.artnr = vhp.fixleist.artnr 
            AND vhp.artikel.departement = vhp.fixleist.departement NO-LOCK. 
          argt-rate = vhp.fixleist.betrag * vhp.fixleist.number. 
          IF NOT fixed-rate AND AVAILABLE vhp.guest-pr THEN 
          DO: 
          DEF VAR ct       AS CHAR.
          DEF VAR contcode AS CHAR.
            contcode = vhp.guest-pr.CODE.
            ct = resline.zimmer-wunsch.
            IF ct MATCHES("*$CODE$*") THEN
            DO:
              ct = SUBSTR(ct,INDEX(ct,"$CODE$") + 6).
              contcode = SUBSTR(ct, 1, INDEX(ct,";") - 1).
            END.
            FIND FIRST vhp.reslin-queasy WHERE vhp.reslin-queasy.key = "argt-line" 
              AND vhp.reslin-queasy.char1 = contcode 
              AND vhp.reslin-queasy.number1 = resline.reserve-int 
              AND vhp.reslin-queasy.number2 = vhp.arrangement.argtnr 
              AND vhp.reslin-queasy.reslinnr = resline.zikatnr 
              AND vhp.reslin-queasy.number3 = vhp.fixleist.artnr 
              AND vhp.reslin-queasy.resnr = vhp.fixleist.departement 
              AND bill-date GE vhp.reslin-queasy.date1 
              AND bill-date LE vhp.reslin-queasy.date2 NO-LOCK NO-ERROR. 
            IF AVAILABLE vhp.reslin-queasy THEN 
              argt-rate = vhp.reslin-queasy.deci1 * vhp.fixleist.number. 
          END. 
        END. 
        
        IF argt-rate NE 0 THEN 
        DO: 
          FIND FIRST s-list WHERE s-list.bezeich = vhp.artikel.bezeich 
            AND s-list.preis = (argt-rate / vhp.fixleist.number) 
            AND s-list.datum = datum 
            AND s-list.ankunft = resline.ankunft 
            AND s-list.abreise = resline.abreise 
            AND s-list.erwachs = pax 
            AND s-list.kind1 = resline.kind1 
            AND s-list.kind2 = resline.kind2 NO-ERROR. 
          IF NOT AVAILABLE s-list THEN 
          DO: 
            CREATE s-list. 
            ASSIGN
                s-list.nr       = vhp.artikel.artnr
                s-list.bezeich  = vhp.artikel.bezeich 
                s-list.preis    = argt-rate / vhp.fixleist.number
                s-list.lRate    = argt-rate / vhp.fixleist.number
                s-list.datum    = datum
                s-list.ankunft  = resline.ankunft
                s-list.abreise  = resline.abreise 
                s-list.erwachs  = pax
                s-list.kind1    = resline.kind1
                s-list.kind2    = resline.kind2. 
          END. 
          s-list.qty = s-list.qty + (vhp.fixleist.number * resline.zimmeranz). 
        END. /* argt-rate NE 0 */  
      END.   /* each vhp.fixleist */ 
    END.     /* datum */
  END.       /* for each resline */
  
  FOR EACH s-list BY s-list.ankunft BY s-list.datum BY s-list.bezeich 
    BY s-list.erwachs:       
    IF s-list.nr = 0 THEN 
    DO: 
      FIND FIRST t-list WHERE t-list.bezeich = s-list.bezeich 
        AND t-list.rmcat = s-list.rmcat 
        AND t-list.preis = s-list.preis 
        AND t-list.lRate = s-list.lRate
        AND t-list.ankunft = s-list.ankunft 
        AND t-list.abreise = s-list.abreise 
        AND t-list.erwachs = s-list.erwachs 
        AND t-list.kind1 = s-list.kind1 
        AND t-list.kind2 = s-list.kind2 NO-ERROR. 
      IF NOT AVAILABLE t-list THEN 
      DO: 
        create t-list. 
        ASSIGN
          t-list.nr = s-list.nr
          t-list.bezeich = s-list.bezeich
          t-list.rmcat = s-list.rmcat
          t-list.preis = s-list.preis
          t-list.lRate = s-list.lRate
          t-list.date1 = s-list.datum 
          t-list.ankunft = s-list.ankunft 
          t-list.abreise = s-list.abreise 
          t-list.erwachs = s-list.erwachs 
          t-list.kind1 = s-list.kind1 
          t-list.kind2 = s-list.kind2
        . 
      END. 
      ASSIGN
        t-list.tage = t-list.tage + 1
        t-list.date2 = s-list.datum
      . 
      IF s-list.datum = t-list.date1 THEN t-list.qty = t-list.qty + s-list.qty. 
    END. 
    ELSE 
    DO: 
      FIND FIRST t-list WHERE t-list.bezeich = s-list.bezeich 
        AND t-list.preis = s-list.preis
        AND t-list.lRate = s-list.lRate
        AND t-list.ankunft = s-list.ankunft 
        AND t-list.abreise = s-list.abreise 
        AND t-list.erwachs = s-list.erwachs 
        AND t-list.kind1 = s-list.kind1 
        AND t-list.kind2 = s-list.kind2 NO-ERROR. 
      IF NOT AVAILABLE t-list THEN 
      DO: 
        CREATE t-list.
        ASSIGN
          t-list.nr = s-list.nr
          t-list.bezeich = s-list.bezeich
          t-list.preis = s-list.preis
          t-list.lRate = s-list.lRate
          t-list.date1 = s-list.datum 
          t-list.ankunft = s-list.ankunft
          t-list.abreise = s-list.abreise 
          t-list.erwachs = s-list.erwachs 
          t-list.kind1 = s-list.kind1
          t-list.kind2 = s-list.kind2
        . 
      END.
      ASSIGN
        t-list.tage = t-list.tage + 1
        t-list.date2 = s-list.datum
      . 
      IF s-list.datum = t-list.date1 THEN t-list.qty = t-list.qty + s-list.qty. 
    END. 
    DELETE s-list. 
  END. 

  FOR EACH t-list: 
    t-list.betrag = t-list.qty * t-list.tage * t-list.lRate. 
  END.
    
  IF rechnr GT 0 THEN
  DO:
      FOR EACH bill-line WHERE bill-line.rechnr = bill.rechnr NO-LOCK,
          FIRST artikel WHERE artikel.artnr = bill-line.artnr
          AND artikel.departement = bill-line.departement NO-LOCK
          BY bill-line.bill-datum BY bill-line.zeit:
          do-it = YES.
          IF artikel.artart EQ 9 THEN
          DO:
              FIND FIRST arrangement WHERE arrangement.argt-artikelnr
                  = artikel.artnr NO-LOCK NO-ERROR.
              IF NOT AVAILABLE arrangement OR arrangement.segmentcode = 0 THEN
                  do-it = NO.
          END.
          IF do-it THEN DO: 

            IF artikel.bezeich MATCHES "Heritage Fee*" THEN DO: 
                FIND FIRST t-list WHERE t-list.bezeich = bill-line.bezeich NO-ERROR.
                IF NOT AVAILABLE t-list THEN CREATE t-list. 

                ASSIGN 
                    count-heritage = count-heritage + 1
                    dept           = artikel.departement
                    t-list.preis   = bill-line.betrag
                    t-list.qty     = t-list.qty + 1
                    t-list.tage    = t-list.tage + 1
                    t-list.betrag  = t-list.betrag + bill-line.betrag.
            END.
            ELSE DO:
                CREATE t-list.
                ASSIGN 
                    t-list.preis   = 0
                    t-list.betrag  = bill-line.betrag.
            END.
           
            ASSIGN
              curr-no = curr-no + 1
              t-list.nr = curr-no 
              t-list.bezeich = bill-line.bezeich
              t-list.date1   = bill-line.bill-datum. 
          END.
      END.
  END.

  /*for penang*/
  FIND FIRST res-line WHERE res-line.resnr = resnr AND res-line.reslinnr = reslinnr NO-LOCK NO-ERROR.
  IF AVAILABLE res-line THEN ASSIGN count-night = res-line.abreise - res-line.ankunft.
  IF count-heritage LT count-night THEN DO:
      DO loopi = (count-heritage + 1) TO count-night:
          FIND FIRST artikel WHERE artikel.bezeich MATCHES "Heritage Fee*"
              AND artikel.departement = dept NO-LOCK NO-ERROR.
          IF AVAILABLE artikel THEN DO:
              FIND FIRST bill-line WHERE bill-line.rechnr = bill.rechnr 
                  AND bill-line.artnr = artikel.artnr NO-LOCK NO-ERROR.
              IF AVAILABLE bill-line THEN DO:
                  FIND FIRST t-list WHERE t-list.bezeich = bill-line.bezeich NO-LOCK NO-ERROR.
                  IF AVAILABLE t-list THEN DO:
                      FIND CURRENT t-list EXCLUSIVE-LOCK.
                      ASSIGN
                          t-list.betrag  = t-list.betrag + bill-line.betrag.
                      FIND CURRENT t-list NO-LOCK.
                  END.
                  ELSE IF NOT AVAILABLE t-list THEN DO:
                      CREATE t-list.
                      ASSIGN
                          curr-no        = curr-no + 1
                          t-list.nr      = curr-no 
                          t-list.bezeich = bill-line.bezeich
                          t-list.preis   = artikel.epreis
                          t-list.date1   = res-line.ankunft
                          t-list.betrag  = bill-line.betrag. 
                  END.
              END.
              ELSE DO:
                  FIND FIRST t-list WHERE t-list.bezeich = artikel.bezeich NO-LOCK NO-ERROR.
                  IF AVAILABLE t-list THEN DO:
                      FIND CURRENT t-list EXCLUSIVE-LOCK.
                      ASSIGN t-list.betrag  = t-list.betrag + artikel.epreis.
                      FIND CURRENT t-list NO-LOCK.
                  END.
                  ELSE IF NOT AVAILABLE t-list THEN DO:
                      CREATE t-list.
                      ASSIGN
                          curr-no        = curr-no + 1
                          t-list.nr      = curr-no 
                          t-list.bezeich = artikel.bezeich
                          t-list.preis   = artikel.epreis
                          t-list.date1   = res-line.ankunft
                          t-list.betrag  = artikel.epreis. 
                  END.
              END.
          END.
      END.
      FOR EACH t-list WHERE t-list.bezeich MATCHES "Heritage Fee*":
          ASSIGN
              t-list.qty     = res-line.zimmeranz
              t-list.tage    = count-night
              t-list.betrag  = t-list.betrag * t-list.qty.
      END.
  END. /*end*/
END. 
/*
PROCEDURE usr-prog1: 
DEFINE INPUT PARAMETER bill-date AS DATE. 
DEFINE INPUT-OUTPUT PARAMETER roomrate AS DECIMAL. 
DEFINE OUTPUT PARAMETER it-exist AS LOGICAL INITIAL NO. 
DEFINE VARIABLE prog-str AS CHAR INITIAL "". 
DEFINE VARIABLE i AS INTEGER. 
  FIND FIRST vhp.reslin-queasy WHERE vhp.reslin-queasy.key = "rate-prog" 
    AND vhp.reslin-queasy.number1 = resnr 
    AND vhp.reslin-queasy.number2 = 0 AND vhp.reslin-queasy.char1 = "" 
    AND vhp.reslin-queasy.reslinnr = 1 USE-INDEX argt_ix NO-LOCK NO-ERROR. 
  IF AVAILABLE vhp.reslin-queasy THEN prog-str = vhp.reslin-queasy.char3. 
  IF prog-str NE "" THEN 
  DO: 
    OUTPUT STREAM s1 TO ".\_rate.p". 
    DO i = 1 TO length(prog-str): 
      PUT STREAM s1 SUBSTR(prog-str, i, 1) FORMAT "x(1)". 
    END. 
    OUTPUT STREAM s1 CLOSE. 
    compile value(".\_rate.p"). 
    dos silent "del .\_rate.p". 
    IF NOT compiler:ERROR THEN 
    DO: 
      RUN value(".\_rate.p") (0, resnr, reslinnr, 
      bill-date, roomrate, NO, OUTPUT roomrate). 
      it-exist = YES. 
    END. 
  END. 
END. 
 
PROCEDURE usr-prog2: 
DEFINE INPUT PARAMETER bill-date AS DATE. 
DEFINE INPUT-OUTPUT PARAMETER roomrate AS DECIMAL. 
DEFINE OUTPUT PARAMETER it-exist AS LOGICAL INITIAL NO. 
DEFINE VARIABLE prog-str AS CHAR INITIAL "". 
DEFINE VARIABLE i AS INTEGER. 
  FIND FIRST vhp.queasy WHERE vhp.queasy.key = 2 
    AND vhp.queasy.char1 = vhp.guest-pr.code NO-LOCK NO-ERROR. 
  IF AVAILABLE vhp.queasy THEN prog-str = vhp.queasy.char3. 
  IF prog-str NE "" THEN 
  DO: 
    OUTPUT STREAM s1 TO ".\_rate.p". 
    DO i = 1 TO length(prog-str): 
      PUT STREAM s1 SUBSTR(prog-str, i, 1) FORMAT "x(1)". 
    END. 
    OUTPUT STREAM s1 CLOSE. 
    compile value(".\_rate.p"). 
    dos silent "del .\_rate.p". 
    IF NOT compiler:ERROR THEN 
    DO: 
      RUN value(".\_rate.p") (0, resnr, reslinnr, 
      bill-date, roomrate, NO, OUTPUT roomrate). 
      it-exist = YES. 
    END. 
  END. 
END. 
*/
PROCEDURE create-bonus: 
DEFINE VARIABLE i AS INTEGER. 
DEFINE VARIABLE j AS INTEGER INITIAL 1. 
DEFINE VARIABLE k AS INTEGER. 
DEFINE VARIABLE n AS INTEGER INITIAL 0. 
DEFINE VARIABLE stay AS INTEGER. 
DEFINE VARIABLE pay AS INTEGER. 
DEFINE VARIABLE num-bonus AS INTEGER INITIAL 0. 
 
  DO i = 1 TO 999: 
      bonus-array[i] = NO. 
  END. 
  j = 1. 
  DO i = 1 TO 4: 
    stay = INTEGER(SUBSTR(vhp.arrangement.options, j, 2)). 
    pay  = INTEGER(SUBSTR(vhp.arrangement.options, j + 2, 2)). 
    IF (stay - pay) GT 0 THEN 
    DO: 
      n = num-bonus + pay  + 1. 
      DO k = n TO stay: 
        bonus-array[k] = YES. 
      END. 
      num-bonus = stay - pay. 
    END. 
     j = j + 4. 
  END. 
END. 
