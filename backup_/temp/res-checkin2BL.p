 
/*  Program FOR Check-in a guest  */ 
 
DEFINE INPUT  PARAMETER pvILanguage   AS INTEGER NO-UNDO.
DEFINE INPUT  PARAMETER resnr         AS INTEGER. 
DEFINE INPUT  PARAMETER reslinnr      AS INTEGER. 
DEFINE INPUT  PARAMETER user-init     AS CHAR. 
DEFINE INPUT  PARAMETER silenzio      AS LOGICAL.
DEFINE OUTPUT PARAMETER new-resstatus AS INTEGER.
DEFINE OUTPUT PARAMETER checked-in    AS LOGICAL INIT NO.
DEFINE OUTPUT PARAMETER ask-deposit   AS LOGICAL INIT NO.
DEFINE OUTPUT PARAMETER ask-keycard   AS LOGICAL INIT NO.
DEFINE OUTPUT PARAMETER ask-mcard     AS LOGICAL INIT NO.
DEFINE OUTPUT PARAMETER msg-str       AS CHAR INIT "".
/* 
DEFINE VARIABLE gastnr AS INTEGER INITIAL 1079. 
DEFINE VARIABLE resnr AS INTEGER INITIAL 2977. 
DEFINE VARIABLE reslinnr AS INTEGER INITIAL 2. 
DEFINE VARIABLE silenzio AS LOGICAL INITIAL NO. 
DEFINE VARIABLE checked-in AS LOGICAL. 
*/ 
  
DEFINE VARIABLE dummy-b     AS LOGICAL. 
DEFINE VARIABLE answer      AS LOGICAL INITIAL YES. 
DEFINE BUFFER res-member    FOR res-line. 
DEFINE VARIABLE res-recid   AS INTEGER. 
DEFINE VARIABLE res-mode    AS CHAR INITIAL "inhouse". 
DEFINE VARIABLE resno       AS INTEGER. 
DEFINE VARIABLE resline     AS INTEGER. 

DEFINE VARIABLE exchg-rate      AS DECIMAL INITIAL 1. 
DEFINE VARIABLE price-decimal   AS INTEGER. 
DEFINE VARIABLE double-currency AS LOGICAL INITIAL NO. 
 
DEFINE VARIABLE err-status      AS INTEGER. 
DEFINE VARIABLE deposit         AS DECIMAL. 
DEFINE VARIABLE deposit-foreign AS DECIMAL INITIAL 0. 
DEFINE VARIABLE bill-date       AS DATE. 
DEFINE VARIABLE sys-id          AS CHAR. 
DEFINE VARIABLE it-is           AS LOGICAL. 
DEFINE VARIABLE inv-nr          AS INTEGER. 
DEFINE VARIABLE nat-bez         AS CHAR.

DEFINE VARIABLE curr-i          AS INTEGER NO-UNDO.
DEFINE VARIABLE curr-st         AS CHAR    NO-UNDO.
DEFINE VARIABLE curr-ct         AS CHAR    NO-UNDO INIT "".

DEFINE VARIABLE mc-flag AS logical. /* YES: read magnet card when check-in */ 
DEFINE VARIABLE mc-pos1 AS INTEGER. 
DEFINE VARIABLE mc-pos2 AS INTEGER. 

DEFINE VARIABLE priscilla-active AS LOGICAL NO-UNDO INITIAL YES.
 
DEF VAR casenum         AS INTEGER NO-UNDO.
DEF VAR rmNo            AS CHAR    NO-UNDO.
DEF VAR outstand        AS DECIMAL NO-UNDO. 
DEF VAR passwd-ok       AS LOGICAL INITIAL NO. 
/*IF 110319 - Add voucher number from billjournal into bill-line.bezeich requested by Safari Lodge*/
DEFINE VARIABLE strA    AS CHARACTER    NO-UNDO.
DEFINE VARIABLE strB    AS CHARACTER    NO-UNDO.    
DEFINE VARIABLE strC    AS CHARACTER    NO-UNDO.
/*END IF*/
DEFINE VARIABLE bill-no AS INTEGER NO-UNDO.

DEFINE BUFFER receiver      FOR guest. 
DEFINE BUFFER res-sharer    FOR res-line. 
DEFINE BUFFER res-line1     FOR res-line. 
DEFINE BUFFER rline         FOR res-line. 
DEFINE BUFFER b-receiver    FOR guest.
DEFINE BUFFER buff-bill     FOR bill. /*FDL*/
DEFINE BUFFER buf-resline   FOR res-line.   /*FDL Ticket 5DB055*/

DEFINE BUFFER bbill FOR bill.
DEFINE VARIABLE loopi   AS INTEGER NO-UNDO.
 
{SupertransBL.i} 
DEF VAR lvCAREA AS CHAR INITIAL "res-checkin". 

FIND FIRST htparam WHERE paramnr = 110 NO-LOCK. 
bill-date = htparam.fdate. 

FIND FIRST htparam WHERE paramnr = 336 NO-LOCK. 
IF htparam.feldtyp = 4 THEN 
DO: 
  mc-flag = htparam.flogical. 
  FIND FIRST htparam WHERE paramnr = 337 NO-LOCK. 
  mc-pos1 = htparam.finteger. 
  FIND FIRST htparam WHERE paramnr = 338 NO-LOCK. 
  mc-pos2 = htparam.finteger. 
END. 
 
/*FDL Ticket 5DB055*/
FIND FIRST buf-resline WHERE buf-resline.resnr EQ resnr 
    AND buf-resline.reslinnr EQ reslinnr
    AND (buf-resline.resstatus EQ 6 OR buf-resline.resstatus EQ 13) NO-LOCK NO-ERROR.
IF AVAILABLE buf-resline THEN
DO:
    msg-str = translateExtended ("Guest already checkin by another user.",lvCAREA,"").
    RETURN.
END.

FIND FIRST res-line WHERE res-line.resnr = resnr 
  AND res-line.reslinnr = reslinnr NO-LOCK NO-ERROR. 

/* Malik Serverless */
IF NOT AVAILABLE res-line THEN RETURN.
ELSE
DO:
  DO TRANSACTION:
    
      IF res-line.resstatus NE 11 THEN
      FOR EACH res-sharer WHERE res-sharer.resnr = resnr
        AND res-sharer.kontakt-nr = reslinnr
        AND res-sharer.l-zuordnung[3] = 1:
        ASSIGN
          res-sharer.zinr        = res-line.zinr
          res-sharer.zikatnr     = res-line.zikatnr
          res-sharer.setup       = res-line.setup
        .
      END.

    /******************** CHECKIN ROOM SHARER(s) WITHOUT BILL **********/
      FIND FIRST res-sharer WHERE res-sharer.resnr = resnr
        AND res-sharer.kontakt-nr = reslinnr
        AND res-sharer.l-zuordnung[3] = 1 NO-LOCK NO-ERROR.
      DO WHILE AVAILABLE res-sharer:
        FIND CURRENT res-sharer EXCLUSIVE-LOCK.
        ASSIGN
          res-sharer.active-flag  = 1
          res-sharer.resstatus    = 13
          res-sharer.ziwechseldat = TODAY
          res-sharer.ankzeit      = TIME
          res-sharer.cancelled-id = user-init
        .
        FIND CURRENT res-sharer NO-LOCK.
        FIND NEXT res-sharer WHERE res-sharer.resnr = resnr
          AND res-sharer.kontakt-nr = reslinnr
          AND res-sharer.l-zuordnung[3] = 1 NO-LOCK NO-ERROR.
      END.
      
      FIND FIRST res-line WHERE res-line.resnr = resnr 
        AND res-line.reslinnr = reslinnr  NO-LOCK. 
      IF res-line.resstatus NE 11 THEN 
      DO:    
          RUN release-zinr(res-line.zinr). 
      END.
      RUN min-resplan. 
  
      FIND FIRST outorder WHERE outorder.zinr = res-line.zinr 
        AND outorder.betriebsnr = res-line.resnr NO-LOCK NO-ERROR. 
      IF AVAILABLE outorder THEN  /* off-market record will be deleted */ 
      DO: 
        FIND CURRENT outorder EXCLUSIVE-LOCK. 
        DELETE outorder.
        RELEASE outorder.
        IF NOT silenzio THEN 
          msg-str = translateExtended ("Off-Market record found and has been removed.",lvCAREA,"") + CHR(10). 
      END. 
  
      FIND FIRST res-line WHERE res-line.resnr = resnr 
        AND res-line.reslinnr = reslinnr EXCLUSIVE-LOCK. 
      IF res-line.resstatus EQ 11 THEN new-resstatus = 13. 
      ELSE new-resstatus = 6. 
      IF res-line.zipreis GT 0 THEN res-line.l-zuordnung[3] = 0.
      ASSIGN
        res-line.resstatus    = new-resstatus
        res-line.active-flag  = 1
        res-line.zimmerfix    = (res-line.resstatus = 13)
        res-line.ziwechseldat = TODAY
        res-line.ankzeit      = TIME 
        res-line.cancelled-id = user-init
    . 
    
      DO curr-i = 1 TO NUM-ENTRIES(res-line.zimmer-wunsch,";") - 1:
        curr-st = ENTRY(curr-i, res-line.zimmer-wunsch, ";").
        IF SUBSTR(curr-st,1,7) = "abreise" THEN .
        ELSE curr-ct = curr-ct + curr-st + ";".
      END.
      ASSIGN res-line.zimmer-wunsch = curr-ct + "abreise"
            + STRING(YEAR(res-line.abreise)) 
            + STRING(MONTH(res-line.abreise),"99")
            + STRING(DAY(res-line.abreise),"99") + ";".

      IF res-line.reserve-dec EQ 0 THEN 
      DO: 
        FIND FIRST reservation WHERE reservation.resnr = res-line.resnr 
          NO-LOCK. 
        IF reservation.insurance THEN 
        DO: 
          IF res-line.betriebsnr NE 0 THEN FIND FIRST waehrung WHERE 
            waehrung.waehrungsnr = res-line.betriebsnr NO-LOCK NO-ERROR. 
          ELSE 
          DO: 
            FIND FIRST htparam WHERE htparam.paramnr = 144 NO-LOCK. 
            FIND FIRST waehrung WHERE waehrung.wabkurz = 
              htparam.fchar NO-LOCK NO-ERROR. 
          END. 
          IF AVAILABLE waehrung THEN 
            res-line.reserve-dec = waehrung.ankauf / waehrung.einheit. 
        END. 
      END. 
  
      FIND CURRENT res-line NO-LOCK. 
  
      IF res-line.resstatus = 6 THEN 
        RUN assign-zinr(RECID(res-line), res-line.ankunft, 
          res-line.abreise, res-line.zinr, res-line.resstatus, 
          res-line.gastnrmember, res-line.bemerk, res-line.name, 
          OUTPUT dummy-b). 
      RUN add-resplan. 
  
      FIND FIRST guest WHERE guest.gastnr = res-line.gastnrmember EXCLUSIVE-LOCK. 
      guest.resflag = 2. 
      FIND CURRENT guest NO-LOCK. 
  
    /* CURRENT status (11/09/99): master bill will be created upon check-in */ 
      IF res-line.resstatus = 6 OR res-line.resstatus = 13 THEN 
      DO: 
        FIND FIRST master WHERE master.resnr = res-line.resnr 
          /* AND master.gastnr = res-line.gastnr */ AND master.flag = 0 
          AND master.ACTIVE = YES NO-LOCK NO-ERROR. 
        IF AVAILABLE master AND master.rechnr NE 0 THEN 
        DO: 
          FIND FIRST bill WHERE bill.rechnr = master.rechnr 
            AND bill.resnr = master.resnr AND bill.reslinnr = 0
            NO-LOCK NO-ERROR. 
          IF NOT AVAILABLE bill THEN 
          DO: 
            casenum = 1.
            FIND FIRST bill WHERE bill.rechnr = master.rechnr 
              NO-LOCK NO-ERROR. 
            IF AVAILABLE bill THEN casenum = 2.
            FIND FIRST b-receiver WHERE b-receiver.gastnr = master.gastnr 
              NO-LOCK. 
            IF casenum = 1 THEN
            DO:
              CREATE bill.
              ASSIGN
                bill.resnr    = master.resnr 
                bill.reslinnr = 0
                bill.rgdruck  = 1 
                bill.billtyp  = 2 
                bill.rechnr   = master.rechnr 
                bill.gastnr   = master.gastnrpay
                bill.datum    = bill-date
                bill.name     = b-receiver.name
              . 
              bill-no = bill.rechnr.

              FIND CURRENT bill NO-LOCK. 
            END.
            ELSE IF casenum = 2 THEN
            DO:
              FIND FIRST counters WHERE counters.counter-no = 3 EXCLUSIVE-LOCK. 
              counters.counter = counters.counter + 1. 
              FIND CURRENT counter NO-LOCK. 
              FIND CURRENT master EXCLUSIVE-LOCK. 
              CREATE bill.
              ASSIGN
                bill.resnr    = master.resnr 
                bill.reslinnr = 0
                bill.rgdruck  = 1 
                bill.billtyp  = 2 
                bill.rechnr   = counters.counter
                bill.gastnr   = master.gastnrpay
                bill.datum    = bill-date
                bill.name     = b-receiver.name
                master.rechnr = bill.rechnr
              . 
              bill-no = bill.rechnr.

              FIND CURRENT bill NO-LOCK. 
              FIND CURRENT master NO-LOCK.
            END.
          END.
          ELSE IF AVAILABLE bill THEN DO: /*ITA 13/12/24 -> Jika reservasi dicheckinkan setelah cancel checkin*/
              FIND CURRENT bill EXCLUSIVE-LOCK.
              ASSIGN bill.flag = 0.
              FIND CURRENT bill NO-LOCK.
          END.
        END. 
        ELSE IF AVAILABLE master AND master.rechnr EQ 0 THEN 
        DO: 
          CREATE bill.
          ASSIGN
            bill.resnr    = master.resnr
            bill.reslinnr = 0
            bill.rgdruck  = 1 
            bill.billtyp  = 2
            bill.datum    = bill-date
          .
          
          FIND FIRST counters WHERE counters.counter-no = 3 EXCLUSIVE-LOCK
            NO-ERROR.
          IF NOT AVAILABLE counters THEN 
          DO: 
            CREATE counters. 
            ASSIGN 
              counters.counter-no = 3 
              counters.counter-bez = "Counter for Bill No" 
            . 
          END. 
          counters.counter = counters.counter + 1. 
          bill.rechnr = counters.counter.         
          FIND CURRENT counter NO-LOCK. 
          FIND CURRENT master EXCLUSIVE-LOCK. 
          master.rechnr = bill.rechnr. 
          FIND CURRENT master NO-LOCK. 
          bill.gastnr = master.gastnrpay. 
          FIND FIRST b-receiver WHERE b-receiver.gastnr = master.gastnr NO-LOCK. 
          bill.name = b-receiver.name. 
          FIND CURRENT bill NO-LOCK. 

          bill-no = bill.rechnr.
        END. 
        /*FDL Jan 10, 2024 => Ticket 1DBBEB => Validation Double Bill*/
        IF bill-no NE 0 THEN /*FDL 8518D4*/
        DO:
          FIND FIRST buff-bill WHERE buff-bill.rechnr EQ bill-no
              AND buff-bill.resnr EQ 0 AND buff-bill.reslinnr EQ 1
              AND buff-bill.billtyp NE 2 NO-LOCK NO-ERROR.
          IF AVAILABLE buff-bill THEN
          DO:
              /*FDL Debug*/
              MESSAGE 
                  "RES-CHECKIN2BL" SKIP
                  "Origin Bill: " bill-no SKIP
                  "Double Bill Number: " STRING(buff-bill.rechnr)
                  VIEW-AS ALERT-BOX INFO BUTTONS OK.
          
              FIND CURRENT buff-bill EXCLUSIVE-LOCK.
              DELETE buff-bill.
              RELEASE buff-bill.
          END.
        END.      
      END. 
  
      FIND FIRST bediener WHERE bediener.userinit = user-init NO-LOCK. 
      FIND FIRST receiver WHERE receiver.gastnr = res-line.gastnrpay NO-LOCK. 
      FIND FIRST reservation WHERE reservation.resnr = res-line.resnr 
        AND reservation.gastnr = res-line.gastnr NO-LOCK. 
  
      FIND FIRST bill WHERE bill.resnr = res-line.resnr 
          AND bill.reslinnr = res-line.reslinnr AND bill.flag = 0 
          AND bill.zinr = res-line.zinr EXCLUSIVE-LOCK NO-ERROR. 
      IF (NOT AVAILABLE bill) AND (res-line.l-zuordnung[3] = 0) THEN 
      DO: 
        CREATE bill. 
        ASSIGN 
          bill.flag        = 0 
          bill.billnr      = 1 
          bill.rgdruck     = 1 
          bill.zinr        = res-line.zinr 
          bill.gastnr      = res-line.gastnrpay 
          bill.resnr       = res-line.resnr 
          bill.reslinnr    = res-line.reslinnr 
          bill.parent-nr   = res-line.reslinnr 
          bill.name        = receiver.NAME 
          bill.kontakt-nr  = bediener.nr 
          bill.segmentcode = reservation.segmentcode
          bill.datum       = bill-date
        .
      END. 
  
      FIND FIRST htparam WHERE htparam.paramnr = 932 NO-LOCK.
      IF htparam.feldtyp = 4 AND htparam.flogical = YES
        AND AVAILABLE bill AND bill.rechnr = 0 THEN
      DO:
        FIND FIRST counters WHERE counters.counter-no = 3 EXCLUSIVE-LOCK
            NO-ERROR. 
        IF NOT AVAILABLE counters THEN 
        DO: 
          CREATE counters. 
          ASSIGN 
            counters.counter-no = 3
            counters.counter-bez = "Counter for Bill No" 
          . 
        END. 
        counters.counter = counters.counter + 1. 
        bill.rechnr = counters.counter. 
        FIND CURRENT counter NO-LOCK. 

        /*ITA 16/10/24*/
          FIND FIRST queasy WHERE queasy.KEY = 301 AND
              queasy.number1 = res-line.resnr AND queasy.logi1 = YES NO-LOCK NO-ERROR.
          IF AVAILABLE queasy THEN DO:
            DO loopi = 1 TO 4:
                  CREATE bbill. 
                  ASSIGN 
                    bbill.flag        = 0 
                    bbill.billnr      = loopi + 1
                    bbill.rgdruck     = 1 
                    bbill.zinr        = res-line.zinr 
                    bbill.gastnr      = res-line.gastnrpay 
                    bbill.resnr       = res-line.resnr 
                    bbill.reslinnr    = res-line.reslinnr 
                    bbill.parent-nr   = res-line.reslinnr 
                    bbill.name        = receiver.NAME 
                    bbill.kontakt-nr  = bediener.nr 
                    bbill.segmentcode = reservation.segmentcode
                    bbill.datum       = bill-date
                    /*bbill.rechnr      = bill.rechnr*/
                  .
                  FIND FIRST counters WHERE counters.counter-no = 3 EXCLUSIVE-LOCK
                      NO-ERROR. 
                  IF NOT AVAILABLE counters THEN 
                  DO: 
                    CREATE counters. 
                    ASSIGN 
                      counters.counter-no = 3
                      counters.counter-bez = "Counter for Bill No" 
                    . 
                  END. 
                  counters.counter = counters.counter + 1. 
                  bbill.rechnr = counters.counter. 
                  FIND CURRENT counter NO-LOCK. 
            END.
          END.
          /*end*/
      END.

      FIND FIRST htparam WHERE htparam.paramnr = 799 NO-LOCK. 
      IF htparam.flogical AND htparam.feldtyp = 4 THEN 
      DO: 
        FIND FIRST counters WHERE counters.counter-no = 29 
            EXCLUSIVE-LOCK NO-ERROR. 
        IF NOT AVAILABLE counters THEN 
        DO: 
          CREATE counters. 
          ASSIGN 
            counters.counter-no = 29 
            counters.counter-bez = "Counter for Registration No" 
          . 
        END. 
        counters.counter = counters.counter + 1. 
        FIND CURRENT counter NO-LOCK. 
        IF AVAILABLE bill THEN bill.rechnr2 = counters.counter. 
        RELEASE counter. 
      END. 
  
      FIND CURRENT reservation NO-LOCK.
      IF reservation.depositbez NE 0 AND reservation.bestat-datum EQ ? 
        AND AVAILABLE bill THEN 
      DO: 
        DEF BUFFER art1 FOR artikel. 
        FIND FIRST htparam WHERE htparam.paramnr = 120 NO-LOCK. 
        FIND FIRST artikel WHERE artikel.artnr = htparam.finteger 
          AND artikel.departement = 0 NO-LOCK NO-ERROR. 
        IF NOT AVAILABLE artikel THEN 
        DO:    
          IF NOT silenzio THEN 
            msg-str = msg-str + CHR(2) 
              + translateExtended ("Deposit article not defined, deposit transfer",lvCAREA,"") + CHR(10)
              + translateExtended ("to the guest bill not possible!",lvCAREA,"") + CHR(10).
        END.
        ELSE 
        DO: 
          answer = YES.
          FIND FIRST htparam WHERE htparam.paramnr = 946 NO-LOCK.
          IF htparam.paramgr = 6 AND htparam.flogical
            AND NOT silenzio THEN
          DO:
            FIND FIRST res-member WHERE res-member.resnr = resnr
              AND res-member.reslinnr NE reslinnr
              AND res-member.active-flag = 0 
              AND res-member.l-zuordnung[3] = 0 NO-LOCK NO-ERROR.
            IF AVAILABLE res-member 
              AND htparam.paramgr = 6 AND htparam.flogical
              AND NOT silenzio THEN
            ASSIGN
              answer      = NO
              ask-deposit = YES
              msg-str = msg-str + CHR(2) + "&Q"
                + translateExtended ("Transfer deposit amount to the bill NOW?",lvCAREA,"") + CHR(10).
          END.
          IF answer THEN
          DO:
            FIND CURRENT reservation EXCLUSIVE-LOCK. 
            reservation.bestat-dat = bill-date. 
            RUN calculate-deposit-amount. 
            FIND FIRST htparam WHERE htparam.paramnr = 104 NO-LOCK. 
            sys-id = htparam.fchar. 
  
            RUN check-masterbill(OUTPUT it-is). 
            IF it-is THEN 
            DO:    
                RUN update-mastbill(OUTPUT inv-nr). 
            END.
            ELSE 
            DO: 
              FIND FIRST counters WHERE counters.counter-no = 3 EXCLUSIVE-LOCK
                NO-ERROR. 
              IF NOT AVAILABLE counters THEN 
              DO: 
                CREATE counters. 
                ASSIGN 
                  counters.counter-no = 3
                  counters.counter-bez = "Counter for Bill No" 
                . 
              END. 
              counters.counter = counters.counter + 1. 
        
              ASSIGN
                bill.rechnr = counters.counter
                bill.saldo  = bill.saldo + deposit /* deposit value is negative */ 
                bill.mwst[99] = bill.mwst[99] + deposit-foreign
                bill.rgdruck = 0
              . 
              FIND CURRENT counter NO-LOCK. 
              inv-nr = bill.rechnr. 
            END. 
      
            FIND FIRST art1 WHERE art1.artnr = reservation.zahlkonto 
              AND art1.departement = 0 NO-LOCK NO-ERROR. 
  
            /*IF 110319 - Add voucher number from billjournal into bill-line.bezeich requested by Safari Lodge*/
            FOR EACH billjournal NO-LOCK:
              IF NUM-ENTRIES(billjournal.bezeich, "#") GT 1 THEN 
              DO:
                  strA = ENTRY(2, billjournal.bezeich, "#").
                  IF NUM-ENTRIES(strA, CHR(32)) GT 0 THEN 
                  DO:
                      strB = ENTRY(1, strA, CHR(32)).
                      IF strB EQ STRING(res-line.resnr) THEN 
                      DO:
                          strC = ENTRY(2, strA, "]").
                      END.
                  END.
              END.
            END.
            /*END IF*/         
            
            CREATE bill-line. 
            ASSIGN
              bill-line.rechnr = inv-nr
              bill-line.artnr = artikel.artnr
              bill-line.bezeich = artikel.bezeich /*IF 110319*/ + "/" + strC /*END IF*/
              bill-line.anzahl = 1
              bill-line.betrag = deposit 
              bill-line.fremdwbetrag = deposit-foreign
              bill-line.zeit = TIME
              bill-line.userinit = sys-id 
              bill-line.zinr = res-line.zinr
              bill-line.massnr = res-line.resnr
              bill-line.billin-nr = res-line.reslinnr 
              bill-line.arrangement = res-line.arrangement 
              bill-line.bill-datum = bill-date
            . 
      
            IF AVAILABLE art1 THEN 
              bill-line.bezeich = bill-line.bezeich + " [" + art1.bezeich + "]". 
  
            FIND CURRENT bill-line NO-LOCK. 
  
            CREATE billjournal. 
            ASSIGN
              billjournal.rechnr = inv-nr
              billjournal.artnr = artikel.artnr 
              billjournal.anzahl = 1
              billjournal.fremdwaehrng = deposit-foreign
              billjournal.betrag = deposit
              billjournal.bezeich = artikel.bezeich + " " + STRING(reservation.resnr) 
              billjournal.zinr = res-line.zinr
              billjournal.epreis = 0
              billjournal.zinr = res-line.zinr
              billjournal.zeit = TIME 
              billjournal.userinit = sys-id
              billjournal.bill-datum = bill-date
            . 
  
            IF AVAILABLE art1 THEN 
              billjournal.bezeich = billjournal.bezeich + " [" + art1.bezeich + "]". 
  
            FIND CURRENT billjournal NO-LOCK. 
  
            FIND FIRST umsatz WHERE umsatz.artnr = artikel.artnr 
              AND umsatz.departement = 0 
              AND umsatz.datum = bill-date EXCLUSIVE-LOCK  NO-ERROR. 
            IF NOT AVAILABLE umsatz THEN 
            DO: 
              CREATE umsatz. 
              umsatz.artnr = artikel.artnr. 
              umsatz.datum = bill-date. 
            END. 
            umsatz.anzahl = umsatz.anzahl + 1. 
            umsatz.betrag = umsatz.betrag + deposit. 
            FIND CURRENT umsatz NO-LOCK. 
          END.
        END.
      END. 
      IF AVAILABLE bill THEN FIND CURRENT bill NO-LOCK. 
  
      IF (res-line.ankunft = res-line.abreise) AND (res-line.zipreis GT 0) THEN 
      DO: 
        RUN post-dayuse.p(res-line.resnr, res-line.reslinnr). 
      END. 
  
    /*** Switch ON extension line ****/ 
      FIND FIRST htparam WHERE paramnr = 307 NO-LOCK. 
      IF htparam.flogical THEN 
      DO:
          RUN intevent-1.p( 1, res-line.zinr, "My Checkin!", res-line.resnr, res-line.reslinnr).
      END.
      ELSE
      DO:
          /*FD June 28, 2022 => Activation Digital First if param 307 = No*/
          FIND FIRST queasy WHERE queasy.KEY EQ 246 AND queasy.logi1 NO-LOCK NO-ERROR.
          IF AVAILABLE queasy THEN
          DO:
              RUN intevent-1.p( 1, res-line.zinr, "My Checkin!", res-line.resnr, res-line.reslinnr).
          END.
      END.      

      IF priscilla-active THEN
      DO:
          RUN intevent-1.p( 1, res-line.zinr, "Priscilla", res-line.resnr, res-line.reslinnr). 
      END.

      RUN check-messages. 
  
      checked-in = YES. 
      IF res-line.resstatus = 6 THEN 
      DO:    
        RUN mk-mcoupon.p(res-line.resnr, res-line.zinr). 
      END.
      IF NOT silenzio THEN 
      DO: 
        FIND FIRST res-sharer WHERE res-sharer.resnr = res-line.resnr 
          AND res-sharer.reslinnr NE res-line.reslinnr 
          AND res-sharer.resstatus = 11 
          AND res-sharer.zinr = res-line.zinr NO-LOCK NO-ERROR. 
        IF AVAILABLE res-sharer THEN 
          msg-str = msg-str + CHR(2)
            + translateExtended ("NOTE: Room sharer",lvCAREA, "") + " " + res-sharer.name + " " 
            + translateExtended ("not yet checked-in.",lvCAREA, "") + CHR(10).
  
        RUN generate-keycard. 
  
        IF mc-flag AND NOT silenzio THEN ask-mcard = YES.
  
        msg-str = msg-str + CHR(2) + "&M"
            + translateExtended ("Guest checked-in.",lvCAREA,"") + CHR(10). 
  
        IF NOT silenzio THEN 
        DO:    
          RUN check-midnite-checkin. 
        END.
  
      END.  

      CREATE res-history. 
      ASSIGN 
          res-history.nr          = bediener.nr 
          res-history.resnr       = res-line.resnr
          res-history.reslinnr    = res-line.reslinnr
          res-history.datum       = TODAY 
          res-history.zeit        = TIME 
          res-history.aenderung   = "CheckIn Room " + res-line.zinr 
                                  + " ResNo " + STRING(res-line.resnr)
          res-history.action      = "Checkin". 
      FIND CURRENT res-history NO-LOCK. 
      RELEASE res-history. 

      /*FD Oct 13, 2022 => Ticket B1B3A0 - Create Reservation Log*/    
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
                          + STRING("CHECKED-IN") + ";"
                          + STRING(" ") + ";" 
                          + STRING(" ") + ";"
                          .      
      FIND CURRENT reslin-queasy NO-LOCK.
      RELEASE reslin-queasy. 

      RELEASE res-line. 
  END. 
END.
/* END Malik */
 
PROCEDURE generate-keycard: 
  FIND FIRST htparam WHERE paramnr = 1111 no-lock.  /* License FOR KeyCard */ 
  ask-keycard = htparam.flogical.  
END. 
 
PROCEDURE check-masterbill: 
DEFINE OUTPUT PARAMETER master-flag AS LOGICAL INITIAL NO. 
  FIND FIRST master WHERE master.resnr = res-line.resnr 
    AND master.active = YES AND master.flag = 0 NO-LOCK NO-ERROR. 
  IF AVAILABLE master THEN master-flag = YES. 
END. 
 
PROCEDURE update-mastbill: 
DEFINE OUTPUT PARAMETER inv-nr AS INTEGER. 
DEFINE BUFFER mbill FOR bill. 
 
  FIND FIRST mbill WHERE mbill.resnr = res-line.resnr 
    AND mbill.reslinnr = 0 EXCLUSIVE-LOCK. 
 
  mbill.gesamtumsatz = mbill.gesamtumsatz + deposit. 
  mbill.rgdruck = 0. 
  mbill.datum = bill-date. 
  mbill.saldo = mbill.saldo + deposit. 
  mbill.mwst[99] = mbill.mwst[99] + deposit-foreign. 
  IF mbill.rechnr = 0 THEN 
  DO: 
    FIND FIRST counters WHERE counters.counter-no = 3 EXCLUSIVE-LOCK
      NO-ERROR. 
    IF NOT AVAILABLE counters THEN 
    DO: 
      CREATE counters. 
      ASSIGN 
        counters.counter-no = 3 
        counters.counter-bez = "Counter for Bill No" 
      . 
    END. 
    counters.counter = counters.counter + 1. 
    mbill.rechnr = counters.counter. 
    FIND CURRENT counter NO-LOCK. 
    FIND CURRENT master EXCLUSIVE-LOCK. 
    master.rechnr = mbill.rechnr. 
    FIND CURRENT master NO-LOCK. 
  END. 
  inv-nr = mbill.rechnr. 
  FIND CURRENT mbill NO-LOCK. 
END. 
 
PROCEDURE calculate-deposit-amount: 
DEFINE VARIABLE deposit-exrate AS DECIMAL INITIAL 1  NO-UNDO. 
    
  FIND FIRST htparam WHERE htparam.paramnr = 120 NO-LOCK. 
  FIND FIRST artikel WHERE artikel.artnr = htparam.finteger 
    AND artikel.departement = 0 NO-LOCK. 
  
  IF NOT artikel.pricetab THEN
    ASSIGN deposit = - reservation.depositbez - reservation.depositbez2. 
  ELSE
  DO:
    deposit-exrate = 1.
    FIND FIRST waehrung WHERE waehrung.waehrungsnr = artikel.betriebsnr
      NO-LOCK NO-ERROR.
    IF reservation.zahldatum = bill-date THEN
    DO:
      IF AVAILABLE waehrung THEN 
        deposit-exrate = waehrung.ankauf / waehrung.einheit.
    END.
    ELSE
    DO:
      FIND FIRST exrate WHERE exrate.artnr = artikel.betriebsnr
        AND exrate.datum = reservation.zahldatum NO-LOCK NO-ERROR.
      IF AVAILABLE exrate THEN deposit-exrate = exrate.betrag.
      ELSE IF AVAILABLE waehrung THEN
        deposit-exrate = waehrung.ankauf / waehrung.einheit.
    END.
    deposit = - reservation.depositbez * deposit-exrate.
    IF reservation.depositbez2 NE 0 THEN
    DO:
      deposit-exrate = 1.
      IF reservation.zahldatum = bill-date THEN
      DO:
        IF AVAILABLE waehrung THEN 
          deposit-exrate = waehrung.ankauf / waehrung.einheit.
      END.
      ELSE
      DO:
        FIND FIRST exrate WHERE exrate.artnr = artikel.betriebsnr
          AND exrate.datum = reservation.zahldatum2 NO-LOCK NO-ERROR.
        IF AVAILABLE exrate THEN deposit-exrate = exrate.betrag.
        ELSE IF AVAILABLE waehrung THEN 
          deposit-exrate = waehrung.ankauf / waehrung.einheit.
      END.
    END.
    deposit = deposit - reservation.depositbez2 * deposit-exrate.
  END.
    
  FIND FIRST htparam WHERE htparam.paramnr = 144 NO-LOCK. 
  FIND FIRST waehrung WHERE waehrung.wabkurz = htparam.fchar NO-LOCK NO-ERROR. 
  IF AVAILABLE waehrung THEN exchg-rate = waehrung.ankauf / waehrung.einheit. 
  ASSIGN deposit-foreign = ROUND(deposit / exchg-rate, 2). 

END. 
 
PROCEDURE check-messages: 
  FIND FIRST messages WHERE /* messages.gastnr = gastnr AND */ 
    messages.resnr = resnr AND messages.reslinnr = reslinnr 
    NO-LOCK NO-ERROR. 
  IF AVAILABLE messages THEN 
  DO: 
  /** switch ON MESSAGE lamp ***/ 
    RUN intevent-1.p( 4, res-line.zinr, "Message Lamp on!",
       res-line.resnr, res-line.reslinnr). 
    IF NOT silenzio THEN 
      msg-str = msg-str + CHR(2) 
        + translateExtended ("Message(s) exist for this guest.",lvCAREA,"") + CHR(10).
  END. 
END. 
 
PROCEDURE check-midnite-checkin: 
  IF TIME GT 6 * 3600 THEN RETURN. 
  FIND FIRST htparam WHERE htparam.paramnr = 87 NO-LOCK. 
  IF htparam.fdate = TODAY AND NOT silenzio THEN 
   msg-str = msg-str + CHR(2) 
     + translateExtended ("EARLY CHECKED-IN GUEST! POST DAY-USE FEE IF NEEDED.",lvCAREA,"") + CHR(10). 
END. 
 
/* { res-zimplan.i } */

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

 
