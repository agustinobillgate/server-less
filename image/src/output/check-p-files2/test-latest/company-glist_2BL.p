
/*gerald genstat, lodging, bfast, add-room, ex-bed, amount w/o arrangement*/

DEFINE TEMP-TABLE output-list 
  FIELD ankunft   LIKE res-line.ankunft 
  FIELD abreise   LIKE res-line.abreise COLUMN-LABEL "Departure" 
  FIELD zinr      LIKE res-line.zinr FORMAT " x(6)" COLUMN-LABEL "RmNo"     /*MT 25/07/12 */
  FIELD resnr     LIKE res-line.resnr 
  FIELD regno     LIKE bill.rechnr2 COLUMN-LABEL "RegNum" FORMAT ">>>>>9" 
  FIELD gname     AS CHAR FORMAT "x(32)" LABEL "Guest Name" 
  FIELD night     AS INTEGER FORMAT ">>>9" LABEL "Night" 
  FIELD zipreis   LIKE res-line.zipreis 
  FIELD amount    AS DECIMAL FORMAT ">,>>>,>>>,>>>,>>>,>>9.99" LABEL "Amount" 
  FIELD STR       AS CHAR FORMAT "x(1)" LABEL ""
  FIELD nr        AS INTEGER
  FIELD rmcat     AS CHAR
  FIELD verstat   LIKE reservation.verstat
  FIELD bill-no   LIKE bill.rechnr COLUMN-LABEL "Bill No" FORMAT ">>>>>9" 
  FIELD lodging   AS DECIMAL FORMAT ">>,>>>,>>>,>>>,>>9.99" COLUMN-LABEL "Lodging" 
  FIELD bfast     AS DECIMAL FORMAT ">,>>>,>>>,>>9.99" COLUMN-LABEL "Breakfast"
  FIELD lunch      AS DECIMAL FORMAT ">,>>>,>>>,>>9.99" COLUMN-LABEL "Lunch" 
  FIELD dinner     AS DECIMAL FORMAT ">,>>>,>>>,>>9.99" COLUMN-LABEL "Dinner"   
  FIELD ex-bed    AS DECIMAL FORMAT ">,>>>,>>>,>>9.99" COLUMN-LABEL "Extra Bed"  
  FIELD add-room  AS DECIMAL FORMAT ">,>>>,>>>,>>9.99" COLUMN-LABEL "Additional Room" 
  /* add pr-code by damen 15/02/23 267DE6*/
  FIELD pr-code   AS CHAR FORMAT "x(26)" COLUMN-LABEL "Promo Code". 

DEFINE INPUT PARAMETER sort-rmcat  AS LOGICAL NO-UNDO.
DEFINE INPUT PARAMETER fr-date     AS DATE NO-UNDO.
DEFINE INPUT PARAMETER to-date     AS DATE NO-UNDO.
DEFINE INPUT PARAMETER curr-gastnr AS INTEGER NO-UNDO.
DEFINE OUTPUT PARAMETER TABLE FOR output-list.

DEFINE VARIABLE curr-date AS DATE.
DEFINE VARIABLE datum     AS DATE.
DEFINE VARIABLE todate    AS DATE.
DEFINE VARIABLE zikatnr   AS INTEGER INIT 0.
DEFINE VARIABLE tot-nr    AS INTEGER INIT 0.
DEFINE VARIABLE tot-zipreis AS DECIMAL INIT 0.
DEFINE VARIABLE tot-amount  AS DECIMAL INIT 0.
DEFINE VARIABLE tot-night   AS INTEGER INIT 0.
DEFINE VARIABLE tot-lodging AS DECIMAL INIT 0.
DEFINE VARIABLE tot-bfast   AS DECIMAL INIT 0.
DEFINE VARIABLE tot-adroom  AS DECIMAL INIT 0.
DEFINE VARIABLE tot-exbed   AS DECIMAL INIT 0.
DEFINE VARIABLE gr-zipreis  AS DECIMAL INIT 0.
DEFINE VARIABLE gr-amount   AS DECIMAL INIT 0.
DEFINE VARIABLE gr-night    AS INTEGER INIT 0.
DEFINE VARIABLE gr-lodging AS DECIMAL INIT 0.
DEFINE VARIABLE gr-bfast   AS DECIMAL INIT 0.
DEFINE VARIABLE gr-adroom  AS DECIMAL INIT 0.
DEFINE VARIABLE gr-exbed   AS DECIMAL INIT 0.

/*gerald 060720*/
DEFINE VARIABLE ct        AS CHAR.
DEFINE VARIABLE take-it AS LOGICAL.
DEFINE VARIABLE contcode  AS CHAR.
DEFINE VARIABLE f-betrag AS DECIMAL.
DEFINE VARIABLE argt-betrag AS DECIMAL. 
DEFINE VARIABLE qty AS INTEGER. 
DEFINE VARIABLE bfast-art AS INTEGER. 
DEFINE VARIABLE lunch-art AS INTEGER. 
DEFINE VARIABLE dinner-art AS INTEGER. 
DEFINE VARIABLE lundin-art AS INTEGER. 
DEFINE VARIABLE fb-dept AS INTEGER. 
DEFINE VARIABLE exchg-rate          AS DECIMAL INITIAL 1. 
DEFINE VARIABLE frate               AS DECIMAL FORMAT ">,>>>,>>9.9999". 
DEFINE VARIABLE argt-rate   AS DECIMAL.
DEFINE VARIABLE add-it AS LOGICAL.
DEFINE VARIABLE delta AS INTEGER.
DEFINE VARIABLE start-date AS DATE.
DEFINE VARIABLE actflag1 AS INT.
DEFINE VARIABLE actflag2 AS INT.
DEFINE VARIABLE serv2         AS DECIMAL.
DEFINE VARIABLE vat2          AS DECIMAL.
DEFINE VARIABLE vat3          AS DECIMAL.
DEFINE VARIABLE vat4          AS DECIMAL.
DEFINE VARIABLE fact2         AS DECIMAL.

DEFINE BUFFER t-output FOR output-list.

DEFINE BUFFER tbill FOR bill.
DEFINE BUFFER rguest FOR guest. 
/* add pr-code by damen 15/02/23 267DE6*/
DEFINE VARIABLE find_code     AS CHARACTER.
DEFINE VARIABLE pr-code       AS CHARACTER.
DEFINE VARIABLE i             AS INTEGER.

FIND FIRST htparam WHERE paramnr = 125 NO-LOCK. 
bfast-art = htparam.finteger.               /* Rulita 211024 | Fixing for serverless */  
FIND FIRST htparam WHERE paramnr = 126 NO-LOCK. 
fb-dept = htparam.finteger.               /* Rulita 211024 | Fixing for serverless */  

FIND FIRST artikel WHERE artikel.zwkum = bfast-art 
AND artikel.departement = fb-dept NO-LOCK NO-ERROR. 
IF NOT AVAILABLE artikel AND bfast-art NE 0 THEN 
DO: 
/*MThide MESSAGE NO-PAUSE. 
MESSAGE translateExtended ("B'fast SubGrp not yed defined (Grp 7)",lvCAREA,"") 
  VIEW-AS ALERT-BOX INFORMATION.*/
RETURN. 
END. 

FIND FIRST htparam WHERE paramnr = 227 NO-LOCK. 
lunch-art = htparam.finteger.               /* Rulita 211024 | Fixing for serverless */  
FIND FIRST artikel WHERE artikel.zwkum = lunch-art 
AND artikel.departement = fb-dept NO-LOCK NO-ERROR. 
IF NOT AVAILABLE artikel AND lunch-art NE 0 THEN 
DO: 
/*MThide MESSAGE NO-PAUSE. 
MESSAGE translateExtended ("Lunch SubGrp not yed defined (Grp 7)",lvCAREA,"") 
  VIEW-AS ALERT-BOX INFORMATION.*/
RETURN. 
END. 

FIND FIRST htparam WHERE paramnr = 228 NO-LOCK. 
dinner-art = htparam.finteger.               /* Rulita 211024 | Fixing for serverless */  
FIND FIRST artikel WHERE artikel.zwkum = dinner-art 
AND artikel.departement = fb-dept NO-LOCK NO-ERROR. 
IF NOT AVAILABLE artikel AND dinner-art NE 0 THEN 
DO: 
/*MThide MESSAGE NO-PAUSE. 
MESSAGE translateExtended ("Dinner SubGrp not yed defined (Grp 7)",lvCAREA,"") 
  VIEW-AS ALERT-BOX INFORMATION.*/
RETURN. 
END. 

FIND FIRST htparam WHERE paramnr = 229 NO-LOCK. 
lundin-art = htparam.finteger.               /* Rulita 211024 | Fixing for serverless */  
FIND FIRST artikel WHERE artikel.zwkum = lundin-art 
AND artikel.departement = fb-dept NO-LOCK NO-ERROR. 
IF NOT AVAILABLE artikel AND lundin-art NE 0 THEN 
DO: 
/*MThide MESSAGE NO-PAUSE. 
MESSAGE translateExtended ("HalfBoard SubGrp not yed defined (Grp 7)",lvCAREA,"") 
  VIEW-AS ALERT-BOX INFORMATION.*/
RETURN. 
END. 

RUN htpdate.p ( 87, OUTPUT curr-date ).

IF fr-date = curr-date AND to-date = curr-date THEN 
DO: 
  actflag1 = 1. 
  actflag2 = 1. 
END. 
ELSE 
DO: 
  actflag1 = 1. 
  actflag2 = 2. 
END. 

IF sort-rmcat = YES THEN DO: /*sorting rmcat*/
    IF fr-date GE curr-date THEN
    DO:
      /*FOR EACH res-line WHERE res-line.gastnr = curr-gastnr 
          AND res-line.ankunft GE fr-date AND res-line.ankunft LE to-date 
          AND res-line.resstatus NE 9 AND res-line.resstatus NE 10 
          AND res-line.resstatus NE 12 NO-LOCK BY res-line.zikatnr: */
        
      FOR EACH res-line WHERE res-line.gastnr = curr-gastnr 
          AND res-line.active-flag GE actflag1 
          AND res-line.active-flag LE actflag2 
          AND res-line.resstatus NE 9 AND res-line.resstatus NE 10 
          AND res-line.resstatus NE 12 
          AND res-line.ankunft LE fr-date 
          AND res-line.abreise GE to-date NO-LOCK BY res-line.zikatnr :

        FIND FIRST waehrung WHERE waehrung.waehrungsnr = res-line.betriebsnr 
            NO-LOCK NO-ERROR.

        exchg-rate = waehrung.ankauf / waehrung.einheit. 
        IF res-line.reserve-dec NE 0 THEN frate = reserve-dec. 
        ELSE frate = exchg-rate. 

        IF res-line.zikatnr NE zikatnr AND zikatnr NE 0 THEN 
        DO:
          CREATE output-list.
          ASSIGN 
              output-list.ankunft     = ? 
              output-list.abreise     = ? 
              output-list.zinr        = " " 
              output-list.gname       = "T O T A L"
              output-list.resnr       = 0 
              output-list.night       = tot-night
              output-list.zipreis     = tot-zipreis
              output-list.amount      = tot-amount
              output-list.lodging     = tot-lodging  
              output-list.bfast       = tot-bfast 
              output-list.add-room    = tot-adroom 
              output-list.ex-bed      = tot-exbed
              output-list.regno       = 0
              output-list.nr          = tot-nr
              tot-zipreis             = 0
              tot-night               = 0
              tot-amount              = 0
              output-list.bill-no     = 0.

          CREATE output-list.
          ASSIGN 
              output-list.ankunft     = ? 
              output-list.abreise     = ? 
              output-list.zinr        = " " 
              output-list.gname       = " " 
              output-list.resnr       = 0 
              output-list.night       = 0
              output-list.zipreis     = 0
              output-list.amount      = 0  
              output-list.lodging     = 0 
              output-list.bfast       = 0 
              output-list.add-room    = 0 
              output-list.ex-bed      = 0 
              output-list.amount      = 0
              output-list.regno       = 0
              output-list.bill-no     = 0
              output-list.nr          = tot-nr
              output-list.bill-no     = 0.
        END.

        CREATE output-list. 
        ASSIGN 
            output-list.ankunft = res-line.ankunft 
            output-list.abreise = res-line.abreise 
            output-list.zinr    = res-line.zinr 
            output-list.gname   = res-line.NAME 
            output-list.resnr   = res-line.resnr 
            /*output-list.night = res-line.abreise - res-line.ankunft */
            output-list.nr    = tot-nr.

        IF res-line.abreise = res-line.ankunft THEN
            output-list.night = 1.
        ELSE output-list.night = res-line.abreise - res-line.ankunft.

        FIND FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr NO-LOCK NO-ERROR.
        IF AVAILABLE zimkateg THEN output-list.rmcat = zimkateg.kurzbez.
        
        IF res-line.ankunft GE curr-date THEN 
        DO:
          output-list.zipreis = res-line.zipreis.
          output-list.amount  = res-line.zipreis * res-line.zimmeranz 
                  * (res-line.abreise - res-line.ankunft).
        END.
        ELSE
        DO:
          FOR EACH genstat WHERE genstat.datum = res-line.ankunft
            AND /*genstat.zinr = res-line.zinr*/ genstat.resnr = res-line.resnr NO-LOCK:
            output-list.zipreis = genstat.zipreis.
            output-list.amount  = genstat.zipreis * res-line.zimmeranz 
                  * (res-line.abreise - res-line.ankunft).
          END.
          IF output-list.zipreis = 0 AND res-line.gratis = 0 THEN
          DO:
            output-list.zipreis = res-line.zipreis.
            output-list.amount  = res-line.zipreis * res-line.zimmeranz 
                  * (res-line.abreise - res-line.ankunft).
          END.
        END.

        /*FIND FIRST reslin-queasy WHERE reslin-queasy.key = "arrangement" 
          AND reslin-queasy.resnr = res-line.resnr
          AND reslin-queasy.reslinnr = res-line.reslinnr NO-LOCK NO-ERROR.
        IF AVAILABLE reslin-queasy THEN
        DO:
          IF res-line.ankunft = res-line.abreise THEN
            todate = res-line.abreise.
          ELSE todate = res-line.abreise - 1.
          DO datum = res-line.ankunft  TO todate :
            FIND FIRST reslin-queasy WHERE reslin-queasy.key = "arrangement" 
              AND reslin-queasy.resnr = res-line.resnr
              AND reslin-queasy.reslinnr = res-line.reslinnr
              AND (reslin-queasy.date1 = datum OR reslin-queasy.date2 = datum)
                NO-LOCK NO-ERROR.
            IF AVAILABLE reslin-queasy THEN
              output-list.amount = output-list.amount + reslin-queasy.deci1.
          END.
          output-list.amount = output-list.amount * res-line.zimmeranz.
        END.
        ELSE IF NOT AVAILABLE reslin-queasy THEN
          output-list.amount = res-line.zipreis * res-line.zimmeranz * (res-line.abreise - res-line.ankunft) .*/
        
        /*gerald 060720*/
        IF output-list.zipreis NE 0 THEN
        DO:
          contcode = "".
          FIND FIRST rguest WHERE rguest.gastnr = res-line.gastnr NO-LOCK NO-ERROR. 
          IF res-line.reserve-int NE 0 THEN /* MarkNr -> contract rate exists */ 
          
          FIND FIRST guest-pr WHERE guest-pr.gastnr = rguest.gastnr NO-LOCK NO-ERROR. 
          IF AVAILABLE guest-pr THEN 
          DO: 
            contcode = guest-pr.CODE.
            ct = res-line.zimmer-wunsch.
            IF ct MATCHES("*$CODE$*") THEN
            DO:
              ct = SUBSTR(ct,INDEX(ct,"$CODE$") + 6).
              contcode = SUBSTR(ct, 1, INDEX(ct,";") - 1).
            END.
            /*IF new-contrate THEN 
            DO:   
               RUN ratecode-seek.p(res-line.resnr, 
                res-line.reslinnr, contcode, curr-date, OUTPUT prcode).
            END.
            ELSE
            DO:
              FIND FIRST pricecod WHERE pricecod.code = contcode 
                AND pricecod.marknr = res-line.reserve-int 
                AND pricecod.argtnr = arrangement.argtnr 
                AND pricecod.zikatnr = curr-zikatnr 
                AND curr-date GE pricecod.startperiode 
                AND curr-date LE pricecod.endperiode NO-LOCK NO-ERROR. 
              IF AVAILABLE pricecod THEN prcode = RECID(pricecod). 
            END.*/
          END.

          FIND FIRST arrangement WHERE arrangement.arrangement = res-line.arrangement NO-LOCK NO-ERROR. 
          
          FOR EACH argt-line WHERE argt-line.argtnr = arrangement.argtnr AND NOT argt-line.kind2 NO-LOCK: 
            FIND FIRST artikel WHERE artikel.artnr = argt-line.argt-artnr 
                AND artikel.departement = argt-line.departement NO-LOCK NO-ERROR.
            IF NOT AVAILABLE artikel THEN take-it = NO.
            ELSE RUN get-argtline-rate(contcode, RECID(argt-line), OUTPUT take-it, 
                 OUTPUT argt-betrag, OUTPUT qty). 

            IF artikel.zwkum = bfast-art AND 
              (artikel.umsatzart = 3 OR artikel.umsatzart GE 5) THEN 
            DO: 
              output-list.bfast = output-list.bfast + argt-betrag. 
              output-list.lodging = output-list.zipreis - argt-betrag. 
            END. 
            ELSE IF artikel.zwkum = lunch-art AND 
              (artikel.umsatzart = 3 OR artikel.umsatzart GE 5) THEN 
            DO: 
              output-list.lunch = output-list.lunch + argt-betrag. 
              output-list.lodging = output-list.zipreis - argt-betrag. 
            END. 
            ELSE IF artikel.zwkum = dinner-art AND 
              (artikel.umsatzart = 3 OR artikel.umsatzart GE 5) THEN 
            DO: 
              output-list.dinner = output-list.dinner + argt-betrag. 
              output-list.lodging = output-list.zipreis - argt-betrag. 
            END. 
            /*ELSE IF artikel.zwkum = lundin-art AND 
              (artikel.umsatzart = 3 OR artikel.umsatzart GE 5) THEN 
            DO: 
              output-list.lunch = output-list.lunch + argt-betrag. 
              output-list.lodging = output-list.zipreis - argt-betrag. 
            END. */
            ELSE 
            DO: 
              output-list.lodging = output-list.zipreis - argt-betrag. 
            END. 
            output-list.lodging = output-list.zipreis - output-list.bfast
                                  - output-list.lunch - output-list.dinner.
          END. 
        END.
        /*end gerald*/

        FOR EACH fixleist WHERE fixleist.resnr = res-line.resnr 
            AND fixleist.reslinnr = res-line.reslinnr NO-LOCK.
          IF AVAILABLE fixleist THEN
          DO:
            add-it = NO. 
            argt-rate = 0. 
            IF fixleist.sequenz = 1 THEN add-it = YES. 
            ELSE IF fixleist.sequenz = 2 OR fixleist.sequenz = 3 THEN 
            DO: 
                IF res-line.ankunft EQ datum THEN add-it = YES. 
            END. 
            ELSE IF fixleist.sequenz = 4 AND day(datum) = 1 THEN add-it = YES. 
            ELSE IF fixleist.sequenz = 5 
                AND day(datum + 1) = 1 THEN add-it = YES. 
            ELSE IF fixleist.sequenz = 6 THEN 
            DO: 
              IF lfakt = ? THEN delta = 0. 
              ELSE 
              DO: 
                delta = lfakt - res-line.ankunft. 
                IF delta LT 0 THEN delta = 0. 
              END. 
              start-date = res-line.ankunft + delta. 
              IF (res-line.abreise - start-date) LT fixleist.dekade 
                THEN start-date = res-line.ankunft. 
              IF datum LE (start-date + (fixleist.dekade - 1)) THEN add-it = YES. 
              IF datum LT start-date THEN add-it = no. /* may NOT post !! */ 
            END. 
            IF add-it THEN 
            DO: 
              FIND FIRST artikel WHERE artikel.artnr = fixleist.artnr 
                AND artikel.departement = fixleist.departement NO-LOCK. 
              argt-rate = fixleist.betrag * fixleist.number. 
            
              IF AVAILABLE artikel AND artikel.artnr = 110 AND argt-rate NE 0 THEN
              DO:
               output-list.ex-bed = argt-rate.
              END.
              ELSE IF AVAILABLE artikel AND artikel.artnr = 112 AND argt-rate NE 0 THEN
              DO:
              output-list.add-room = argt-rate.
              END.
          
            END.
          END.
        END.
        /*end geral*/
        

        FIND FIRST bill WHERE bill.resnr = res-line.resnr 
                AND bill.reslinnr = res-line.reslinnr NO-LOCK NO-ERROR. 
        IF AVAILABLE bill THEN 
        DO:
                output-list.regno   = bill.rechnr2.
                output-list.bill-no = bill.rechnr.
        END.
        
        /*
        FIND FIRST master WHERE master.resnr = output-list.resnr NO-LOCK NO-ERROR. 
        IF AVAILABLE master AND master.active THEN output-list.verstat = master.rechnr. */

        FIND FIRST tbill WHERE tbill.resnr = output-list.resnr
            AND tbill.reslinnr = 0 NO-LOCK NO-ERROR.
        IF AVAILABLE tbill THEN output-list.verstat = tbill.rechnr.

        ASSIGN zikatnr     = res-line.zikatnr
               tot-nr      = tot-nr + 1
               tot-zipreis = tot-zipreis + output-list.zipreis
               tot-amount  = tot-amount  + output-list.amount
               tot-night   = tot-night   + output-list.night
               tot-lodging = tot-lodging + output-list.lodging
               tot-bfast   = tot-bfast   + output-list.bfast
               tot-adroom  = tot-adroom  + output-list.add-room
               tot-exbed   = tot-exbed   + output-list.ex-bed.
      END.
    END.

    ELSE 
    DO:
      FOR EACH genstat WHERE genstat.datum GE fr-date AND genstat.datum LE to-date 
        AND genstat.gastnr = curr-gastnr NO-LOCK,
        FIRST res-line WHERE res-line.resnr = genstat.resnr AND res-line.reslinnr = genstat.res-int[1]
        AND res-line.l-zuordnung[3] = 0 NO-LOCK,
        FIRST guest WHERE guest.gastnr = genstat.gastnrmember NO-LOCK BY genstat.zikatnr :
        
        IF genstat.zikatnr NE zikatnr AND zikatnr NE 0 THEN 
        DO:
          CREATE output-list.
          ASSIGN 
              output-list.ankunft     = ? 
              output-list.abreise     = ? 
              output-list.zinr        = " " 
              output-list.gname       = "T O T A L"
              output-list.resnr       = 0 
              output-list.night       = tot-night
              output-list.zipreis     = tot-zipreis
              output-list.amount      = tot-amount
              output-list.lodging     = tot-lodging  
              output-list.bfast       = tot-bfast 
              output-list.add-room    = tot-adroom 
              output-list.ex-bed      = tot-exbed
              output-list.regno       = 0
              output-list.nr          = tot-nr
              tot-zipreis             = 0
              tot-night               = 0
              tot-amount              = 0
              output-list.bill-no     = 0.
  
          CREATE output-list.
          ASSIGN 
              output-list.ankunft     = ? 
              output-list.abreise     = ? 
              output-list.zinr        = " " 
              output-list.gname       = " " 
              output-list.resnr       = 0 
              output-list.night       = 0
              output-list.zipreis     = 0
              output-list.amount      = 0  
              output-list.lodging     = 0 
              output-list.bfast       = 0 
              output-list.add-room    = 0 
              output-list.ex-bed      = 0 
              output-list.amount      = 0
              output-list.regno       = 0
              output-list.bill-no     = 0
              output-list.nr          = tot-nr
              output-list.bill-no     = 0.
        END.

        CREATE output-list. 
        ASSIGN 
          output-list.ankunft = genstat.res-date[1] 
          output-list.abreise = genstat.res-date[2] 
          output-list.zinr    = genstat.zinr 
          output-list.gname   = guest.NAME
          output-list.resnr   = genstat.resnr 
          output-list.night   = genstat.res-date[2] - genstat.res-date[1]
          output-list.nr      = tot-nr.

        IF genstat.res-date[2] = genstat.res-date[1] THEN
        output-list.night = 1.
        ELSE output-list.night = genstat.res-date[2] - genstat.res-date[1].
        /* add pr-code by damen 15/02/23 267DE6*/
        IF res-line.zimmer-wunsch MATCHES "*PromotionCode*" THEN
            DO:
                DO i = 1 TO NUM-ENTRIES(res-line.zimmer-wunsch, ";"):
                find_code = ENTRY(i,res-line.zimmer-wunsch, ";").
                IF find_code MATCHES "*$PRCODE$*" THEN
                DO:
                  output-list.pr-code = trim(SUBSTRING(find_code, 7)).
                END. 
            END.
        END.
        FIND FIRST zimkateg WHERE zimkateg.zikatnr = genstat.zikatnr NO-LOCK NO-ERROR.
        IF AVAILABLE zimkateg THEN output-list.rmcat = zimkateg.kurzbez.

        IF res-line.ankunft GE curr-date THEN output-list.zipreis = res-line.zipreis.
        ELSE output-list.zipreis = genstat.zipreis.

        IF output-list.zipreis = 0 AND genstat.gratis = 0 THEN output-list.zipreis = genstat.zipreis.

        FIND FIRST reslin-queasy WHERE reslin-queasy.key = "arrangement" 
          AND reslin-queasy.resnr = res-line.resnr
          AND reslin-queasy.reslinnr = res-line.reslinnr NO-LOCK NO-ERROR.
        IF AVAILABLE reslin-queasy THEN
        DO:
          IF res-line.ankunft = res-line.abreise THEN
            todate = res-line.abreise.
          ELSE todate = res-line.abreise - 1.
          DO datum = res-line.ankunft  TO todate :
            FIND FIRST reslin-queasy WHERE reslin-queasy.key = "arrangement" 
              AND reslin-queasy.resnr = res-line.resnr
              AND reslin-queasy.reslinnr = res-line.reslinnr
              AND (reslin-queasy.date1 = datum OR reslin-queasy.date2 = datum)
                NO-LOCK NO-ERROR.
            IF AVAILABLE reslin-queasy THEN
              output-list.amount = output-list.amount + reslin-queasy.deci1.
          END.
          output-list.amount = output-list.amount * res-line.zimmeranz.
        END.
        ELSE IF NOT AVAILABLE reslin-queasy THEN
          output-list.amount = res-line.zipreis * res-line.zimmeranz * (res-line.abreise - res-line.ankunft) .

        FIND FIRST bill WHERE bill.resnr = genstat.resnr 
                AND bill.reslinnr = genstat.res-int[1] NO-LOCK NO-ERROR. 
        IF AVAILABLE bill THEN 
        DO:
                output-list.regno   = bill.rechnr2.
                output-list.bill-no = bill.rechnr.
        END.

        /*
        FIND FIRST master WHERE master.resnr = output-list.resnr NO-LOCK NO-ERROR. 
        IF AVAILABLE master AND master.active THEN output-list.verstat = master.rechnr. */

        FIND FIRST tbill WHERE tbill.resnr = output-list.resnr
            AND tbill.reslinnr = 0 NO-LOCK NO-ERROR.
        IF AVAILABLE tbill THEN output-list.verstat = tbill.rechnr.
        
        FIND FIRST arrangement WHERE arrangement.arrangement = genstat.argt NO-LOCK NO-ERROR.

        IF output-list.zipreis NE 0 THEN
        DO:
          FOR EACH argt-line WHERE argt-line.argtnr = arrangement.argtnr AND NOT argt-line.kind2
            AND argt-line.kind1,
            FIRST artikel WHERE artikel.artnr = argt-line.argt-artnr 
            AND artikel.departement = argt-line.departement NO-LOCK:

            DEFINE BUFFER argtline FOR argt-line.

            RUN get-genstat-argtline-rate(contcode, RECID(argt-line), OUTPUT take-it, 
                         OUTPUT f-betrag, OUTPUT argt-betrag, OUTPUT qty).

            IF artikel.zwkum = bfast-art AND 
                (artikel.umsatzart = 3 OR artikel.umsatzart GE 5) THEN 
            DO:
              ASSIGN 
                 /*output-list.bfast  = genstat.res-deci[2] * (1 + vat3 + serv2).*/
                  output-list.bfast  = output-list.bfast + argt-betrag.
            END.
            ELSE IF artikel.zwkum = lunch-art AND 
                (artikel.umsatzart = 3 OR artikel.umsatzart GE 5) THEN 
            DO:
              ASSIGN 
                 /*output-list.lunch  = genstat.res-deci[3] * (1 + vat3 + serv2).*/
                  output-list.lunch  = output-list.lunch + argt-betrag.
            END.
            ELSE IF artikel.zwkum = dinner-art AND 
                (artikel.umsatzart = 3 OR artikel.umsatzart GE 5) THEN 
            DO:
              ASSIGN 
                 /*output-list.dinner = genstat.res-deci[4] * (1 + vat3 + serv2).*/
                  output-list.dinner  = output-list.dinner + argt-betrag.
            END.
            ELSE IF artikel.zwkum = lundin-art AND 
                (artikel.umsatzart = 3 OR artikel.umsatzart GE 5) THEN 
            DO:
              ASSIGN 
                /*output-list.lunch = genstat.res-deci[3] * (1 + vat3 + serv2).*/
                  output-list.dinner  = output-list.dinner + argt-betrag.
            END.
          END.
        END.

        FOR EACH fixleist WHERE fixleist.resnr = res-line.resnr 
              AND fixleist.reslinnr = res-line.reslinnr NO-LOCK.
            IF AVAILABLE fixleist THEN
            DO:
              add-it = NO. 
              argt-rate = 0. 
              IF fixleist.sequenz = 1 THEN add-it = YES. 
              ELSE IF fixleist.sequenz = 2 OR fixleist.sequenz = 3 THEN 
              DO: 
                  IF res-line.ankunft EQ datum THEN add-it = YES. 
              END. 
              ELSE IF fixleist.sequenz = 4 AND day(datum) = 1 THEN add-it = YES. 
              ELSE IF fixleist.sequenz = 5 
                  AND day(datum + 1) = 1 THEN add-it = YES. 
              ELSE IF fixleist.sequenz = 6 THEN 
              DO: 
                IF lfakt = ? THEN delta = 0. 
                ELSE 
                DO: 
                  delta = lfakt - res-line.ankunft. 
                  IF delta LT 0 THEN delta = 0. 
                END. 
                start-date = res-line.ankunft + delta. 
                IF (res-line.abreise - start-date) LT fixleist.dekade 
                  THEN start-date = res-line.ankunft. 
                IF datum LE (start-date + (fixleist.dekade - 1)) THEN add-it = YES. 
                IF datum LT start-date THEN add-it = no. /* may NOT post !! */ 
              END. 
              IF add-it THEN 
              DO: 
                FIND FIRST artikel WHERE artikel.artnr = fixleist.artnr 
                  AND artikel.departement = fixleist.departement NO-LOCK. 
                argt-rate = fixleist.betrag * fixleist.number. 
              
                IF AVAILABLE artikel AND artikel.artnr = 110 AND argt-rate NE 0 THEN
                DO:
                 output-list.ex-bed = argt-rate.
                END.
                ELSE IF AVAILABLE artikel AND artikel.artnr = 112 AND argt-rate NE 0 THEN
                DO:
                 output-list.add-room = argt-rate.
                END.
              END.
            END.
          END.

          ASSIGN 
             output-list.lodging = output-list.lodging + genstat.logis
             zikatnr             = res-line.zikatnr
             tot-nr              = tot-nr + 1
             tot-zipreis         = tot-zipreis + output-list.zipreis
             tot-amount          = tot-amount  + output-list.amount
             tot-night           = tot-night   + output-list.night
             tot-lodging         = tot-lodging + output-list.lodging
             tot-bfast           = tot-bfast   + output-list.bfast
             tot-adroom          = tot-adroom  + output-list.add-room
             tot-exbed           = tot-exbed   + output-list.ex-bed.
      END.  
    END.
    
    CREATE output-list.
    ASSIGN                     
        output-list.ankunft     = ? 
        output-list.abreise     = ? 
        output-list.zinr        = " " 
        output-list.gname       = "T O T A L"
        output-list.resnr       = 0 
        output-list.night       = tot-night
        output-list.zipreis     = tot-zipreis
        output-list.amount      = tot-amount
        output-list.lodging     = tot-lodging  
        output-list.bfast       = tot-bfast 
        output-list.add-room    = tot-adroom 
        output-list.ex-bed      = tot-exbed
        output-list.regno       = 0
        output-list.nr          = tot-nr
        output-list.bill-no     = 0 .

   FOR EACH output-list:
       IF output-list.gname   = "T O T A L" THEN DO:
          ASSIGN gr-zipreis   = gr-zipreis + output-list.zipreis
                 gr-amount    = gr-amount  + output-list.amount
                 gr-night     = gr-night   + output-list.night
                 gr-lodging   = gr-lodging + output-list.lodging 
                 gr-bfast     = gr-bfast   + output-list.bfast   
                 gr-adroom    = gr-adroom  + output-list.add-room
                 gr-exbed     = gr-exbed   + output-list.ex-bed   .
      END.
   END.

   CREATE output-list.
   ASSIGN 
        output-list.ankunft     = ? 
        output-list.abreise     = ? 
        output-list.zinr        = " " 
        output-list.gname       = "GRAND TOTAL" 
        output-list.resnr       = 0 
        output-list.night       = gr-night
        output-list.zipreis     = gr-zipreis
        output-list.amount      = gr-amount
        output-list.lodging     = gr-lodging 
        output-list.bfast       = gr-bfast   
        output-list.add-room    = gr-adroom  
        output-list.ex-bed      = gr-exbed   
        output-list.regno       = 0
        output-list.nr          = tot-nr + 1
        output-list.bill-no     = 0.
END.
ELSE DO:
    IF fr-date GE curr-date THEN
    DO:
      /*FOR EACH res-line WHERE res-line.gastnr = curr-gastnr 
          AND res-line.ankunft GE fr-date AND res-line.ankunft LE to-date 
          AND res-line.resstatus NE 9 AND res-line.resstatus NE 10 
          AND res-line.resstatus NE 12 NO-LOCK BY res-line.ankunft:*/

        FOR EACH res-line WHERE res-line.gastnr = curr-gastnr 
            AND res-line.active-flag GE actflag1 
            AND res-line.active-flag LE actflag2 
            AND res-line.resstatus NE 9 AND res-line.resstatus NE 10 
            AND res-line.resstatus NE 12 
            AND res-line.ankunft LE fr-date 
            AND res-line.abreise GE to-date NO-LOCK BY res-line.ankunft :

        IF res-line.active-flag GE 1 THEN FIND FIRST bill WHERE 
              bill.resnr = res-line.resnr AND bill.reslinnr = res-line.reslinnr 
              NO-LOCK NO-ERROR. 
  
          CREATE output-list. 
          ASSIGN 
              output-list.ankunft = res-line.ankunft 
              output-list.abreise = res-line.abreise 
              output-list.zinr    = res-line.zinr 
              output-list.gname   = res-line.NAME 
              output-list.resnr   = res-line.resnr 
              output-list.night   = res-line.abreise - res-line.ankunft .
              
          IF res-line.abreise = res-line.ankunft THEN
              output-list.night = 1.
          ELSE output-list.night = res-line.abreise - res-line.ankunft .
          /* add pr-code by damen 15/02/23 267DE6*/
          IF res-line.zimmer-wunsch MATCHES "*PromotionCode*" THEN
              DO:
                  DO i = 1 TO NUM-ENTRIES(res-line.zimmer-wunsch, ";"):
                  find_code = ENTRY(i,res-line.zimmer-wunsch, ";").
                  IF find_code MATCHES "*$PRCODE$*" THEN
                  DO:
                      output-list.pr-code = trim(SUBSTRING(find_code, 7)).
                  END. 
              END.
          END.

          FIND FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr NO-LOCK NO-ERROR.
          IF AVAILABLE zimkateg THEN output-list.rmcat = zimkateg.kurzbez.
  
          IF res-line.ankunft GE curr-date THEN 
          DO: 
              output-list.zipreis = res-line.zipreis.
              output-list.amount  = res-line.zipreis * res-line.zimmeranz 
                  * (res-line.abreise - res-line.ankunft).
          END.
          ELSE
          DO:
            FOR EACH genstat WHERE genstat.datum = res-line.ankunft
              AND /*genstat.zinr = res-line.zinr*/ res-line.resnr = genstat.resnr NO-LOCK:
              output-list.zipreis = genstat.zipreis.
              output-list.amount  = genstat.zipreis * res-line.zimmeranz 
                  * (res-line.abreise - res-line.ankunft).
            END.
            IF output-list.zipreis = 0 AND res-line.gratis = 0 THEN
            DO:
                output-list.zipreis = res-line.zipreis.  
                output-list.amount  = res-line.zipreis * res-line.zimmeranz 
                  * (res-line.abreise - res-line.ankunft).
            END.
          END.
  
          /*gerald 060720*/
          IF output-list.zipreis NE 0 THEN
          DO:
              contcode = "".
              FIND FIRST rguest WHERE rguest.gastnr = res-line.gastnr NO-LOCK NO-ERROR. 
              IF res-line.reserve-int NE 0 THEN /* MarkNr -> contract rate exists */ 
              
              FIND FIRST guest-pr WHERE guest-pr.gastnr = rguest.gastnr NO-LOCK NO-ERROR. 
              IF AVAILABLE guest-pr THEN 
              DO: 
                contcode = guest-pr.CODE.
                ct = res-line.zimmer-wunsch.
                IF ct MATCHES("*$CODE$*") THEN
                DO:
                  ct = SUBSTR(ct,INDEX(ct,"$CODE$") + 6).
                  contcode = SUBSTR(ct, 1, INDEX(ct,";") - 1).
                END.
                /*IF new-contrate THEN 
                DO:   
                   RUN ratecode-seek.p(res-line.resnr, 
                    res-line.reslinnr, contcode, curr-date, OUTPUT prcode).
                END.
                ELSE
                DO:
                  FIND FIRST pricecod WHERE pricecod.code = contcode 
                    AND pricecod.marknr = res-line.reserve-int 
                    AND pricecod.argtnr = arrangement.argtnr 
                    AND pricecod.zikatnr = curr-zikatnr 
                    AND curr-date GE pricecod.startperiode 
                    AND curr-date LE pricecod.endperiode NO-LOCK NO-ERROR. 
                  IF AVAILABLE pricecod THEN prcode = RECID(pricecod). 
                END.*/
              END.
  
              FIND FIRST arrangement WHERE arrangement.arrangement = res-line.arrangement NO-LOCK NO-ERROR. 
              
              FOR EACH argt-line WHERE argt-line.argtnr = arrangement.argtnr AND NOT argt-line.kind2 NO-LOCK: 
                FIND FIRST artikel WHERE artikel.artnr = argt-line.argt-artnr 
                    AND artikel.departement = argt-line.departement NO-LOCK NO-ERROR.
                IF NOT AVAILABLE artikel THEN take-it = NO.
                ELSE RUN get-argtline-rate(contcode, RECID(argt-line), OUTPUT take-it, 
                     OUTPUT argt-betrag, OUTPUT qty). 
  
                IF artikel.zwkum = bfast-art AND 
                  (artikel.umsatzart = 3 OR artikel.umsatzart GE 5) THEN 
                DO: 
                  output-list.bfast = output-list.bfast + argt-betrag. 
                  output-list.lodging = output-list.zipreis - argt-betrag. 
                END. 
                ELSE IF artikel.zwkum = lunch-art AND 
                  (artikel.umsatzart = 3 OR artikel.umsatzart GE 5) THEN 
                DO: 
                  output-list.lunch = output-list.lunch + argt-betrag. 
                  output-list.lodging = output-list.zipreis - argt-betrag. 
                END. 
                ELSE IF artikel.zwkum = dinner-art AND 
                  (artikel.umsatzart = 3 OR artikel.umsatzart GE 5) THEN 
                DO: 
                  output-list.dinner = output-list.dinner + argt-betrag. 
                  output-list.lodging = output-list.zipreis - argt-betrag. 
                END. 
                ELSE 
                DO: 
                  output-list.lodging = output-list.zipreis - argt-betrag. 
                END. 
                output-list.lodging = output-list.zipreis - output-list.bfast - output-list.lunch
                                       - output-list.dinner.
              END. 
          END.
  
          FOR EACH fixleist WHERE fixleist.resnr = res-line.resnr 
              AND fixleist.reslinnr = res-line.reslinnr NO-LOCK.
            IF AVAILABLE fixleist THEN
            DO:
              add-it = NO. 
              argt-rate = 0. 
              IF fixleist.sequenz = 1 THEN add-it = YES. 
              ELSE IF fixleist.sequenz = 2 OR fixleist.sequenz = 3 THEN 
              DO: 
                  IF res-line.ankunft EQ datum THEN add-it = YES. 
              END. 
              ELSE IF fixleist.sequenz = 4 AND day(datum) = 1 THEN add-it = YES. 
              ELSE IF fixleist.sequenz = 5 
                  AND day(datum + 1) = 1 THEN add-it = YES. 
              ELSE IF fixleist.sequenz = 6 THEN 
              DO: 
                IF lfakt = ? THEN delta = 0. 
                ELSE 
                DO: 
                  delta = lfakt - res-line.ankunft. 
                  IF delta LT 0 THEN delta = 0. 
                END. 
                start-date = res-line.ankunft + delta. 
                IF (res-line.abreise - start-date) LT fixleist.dekade 
                  THEN start-date = res-line.ankunft. 
                IF datum LE (start-date + (fixleist.dekade - 1)) THEN add-it = YES. 
                IF datum LT start-date THEN add-it = no. /* may NOT post !! */ 
              END. 
              IF add-it THEN 
              DO: 
                FIND FIRST artikel WHERE artikel.artnr = fixleist.artnr 
                  AND artikel.departement = fixleist.departement NO-LOCK. 
                argt-rate = fixleist.betrag * fixleist.number. 
              
                IF AVAILABLE artikel AND artikel.artnr = 110 AND argt-rate NE 0 THEN
                DO:
                 output-list.ex-bed = argt-rate.
                END.
                ELSE IF AVAILABLE artikel AND artikel.artnr = 112 AND argt-rate NE 0 THEN
                DO:
                output-list.add-room = argt-rate.
                END.
            
              END.
            END.
          END.
          
          /*end geral*/
  
  
          /*FIND FIRST reslin-queasy WHERE reslin-queasy.key = "arrangement" 
            AND reslin-queasy.resnr = res-line.resnr
            AND reslin-queasy.reslinnr = res-line.reslinnr NO-LOCK NO-ERROR.
          IF AVAILABLE reslin-queasy THEN
          DO:
            IF res-line.ankunft = res-line.abreise THEN
              todate = res-line.abreise.
            ELSE todate = res-line.abreise - 1.
            DO datum = res-line.ankunft  TO todate :
              FIND FIRST reslin-queasy WHERE reslin-queasy.key = "arrangement" 
                AND reslin-queasy.resnr = res-line.resnr
                AND reslin-queasy.reslinnr = res-line.reslinnr
                AND (reslin-queasy.date1 = datum OR reslin-queasy.date2 = datum)
                  NO-LOCK NO-ERROR.
              IF AVAILABLE reslin-queasy THEN
                output-list.amount = output-list.amount + reslin-queasy.deci1.
            END.
            output-list.amount = output-list.amount * res-line.zimmeranz.
          END.
          ELSE IF NOT AVAILABLE reslin-queasy THEN
          DO:
            output-list.amount = res-line.zipreis * res-line.zimmeranz 
                  * (res-line.abreise - res-line.ankunft).
          END.*/

          FIND FIRST bill WHERE bill.resnr = res-line.resnr 
                  AND bill.reslinnr = res-line.reslinnr NO-LOCK NO-ERROR. 
          IF AVAILABLE bill THEN DO:
                  output-list.regno   = bill.rechnr2.
                  output-list.bill-no = bill.rechnr.
          END.
          
          /*
          FIND FIRST master WHERE master.resnr = output-list.resnr NO-LOCK NO-ERROR. 
          IF AVAILABLE master AND master.active THEN output-list.verstat = master.rechnr. */
  
          FIND FIRST tbill WHERE tbill.resnr = output-list.resnr
              AND tbill.reslinnr = 0 NO-LOCK NO-ERROR.
          IF AVAILABLE tbill THEN output-list.verstat = tbill.rechnr.
          
          ASSIGN zikatnr     = res-line.zikatnr
             tot-nr      = tot-nr + 1
             tot-zipreis = tot-zipreis + output-list.zipreis
             tot-amount  = tot-amount  + output-list.amount
             tot-night   = tot-night   + output-list.night
             tot-lodging = tot-lodging + output-list.lodging
             tot-bfast   = tot-bfast   + output-list.bfast
             tot-adroom  = tot-adroom  + output-list.add-room
             tot-exbed   = tot-exbed   + output-list.ex-bed.
      END.
    END.

    ELSE 
    DO:
      FOR EACH genstat WHERE genstat.datum GE fr-date
        AND genstat.datum LE to-date AND genstat.gastnr = curr-gastnr NO-LOCK,
        FIRST res-line WHERE res-line.resnr = genstat.resnr AND res-line.reslinnr = genstat.res-int[1]
        AND res-line.l-zuordnung[3] = 0 NO-LOCK,
        FIRST guest WHERE guest.gastnr = genstat.gastnrmember NO-LOCK BY genstat.res-date[1]: 
        CREATE output-list. 
          ASSIGN 
              output-list.ankunft = genstat.res-date[1] 
              output-list.abreise = genstat.res-date[2] 
              output-list.zinr    = genstat.zinr 
              output-list.gname   = guest.NAME
              output-list.resnr   = genstat.resnr 
              output-list.night   = genstat.res-date[2] - genstat.res-date[1].

        IF genstat.res-date[2] = genstat.res-date[1] THEN
          output-list.night = 1.
        ELSE output-list.night = genstat.res-date[2] - genstat.res-date[1].

        FIND FIRST zimkateg WHERE zimkateg.zikatnr = genstat.zikatnr NO-LOCK NO-ERROR.
        IF AVAILABLE zimkateg THEN output-list.rmcat = zimkateg.kurzbez.

        IF res-line.ankunft GE curr-date THEN output-list.zipreis = res-line.zipreis.
        ELSE output-list.zipreis = genstat.zipreis.
        
        IF output-list.zipreis = 0 AND genstat.gratis = 0 THEN output-list.zipreis = genstat.zipreis.

        /* add pr-code by damen 15/02/23 267DE6*/
        IF res-line.zimmer-wunsch MATCHES "*PromotionCode*" THEN
          DO:
              DO i = 1 TO NUM-ENTRIES(res-line.zimmer-wunsch, ";"):
              find_code = ENTRY(i,res-line.zimmer-wunsch, ";").
              IF find_code MATCHES "*$PRCODE$*" THEN
              DO:
                  output-list.pr-code = trim(SUBSTRING(find_code, 9)).
              END. 
          END.
        END.

        FIND FIRST reslin-queasy WHERE reslin-queasy.key = "arrangement" 
          AND reslin-queasy.resnr = res-line.resnr
          AND reslin-queasy.reslinnr = res-line.reslinnr NO-LOCK NO-ERROR.
        IF AVAILABLE reslin-queasy THEN
        DO:
          IF res-line.ankunft = res-line.abreise THEN
            todate = res-line.abreise.
          ELSE todate = res-line.abreise - 1.
          DO datum = res-line.ankunft  TO todate :
            FIND FIRST reslin-queasy WHERE reslin-queasy.key = "arrangement" 
              AND reslin-queasy.resnr = res-line.resnr
              AND reslin-queasy.reslinnr = res-line.reslinnr
              AND (reslin-queasy.date1 = datum OR reslin-queasy.date2 = datum)
                NO-LOCK NO-ERROR.
            IF AVAILABLE reslin-queasy THEN
              output-list.amount = output-list.amount + reslin-queasy.deci1.
          END.
          output-list.amount = output-list.amount * res-line.zimmeranz.
        END.
        ELSE IF NOT AVAILABLE reslin-queasy THEN
          output-list.amount = res-line.zipreis * res-line.zimmeranz * (res-line.abreise - res-line.ankunft) .

        FIND FIRST bill WHERE bill.resnr = genstat.resnr 
                AND bill.reslinnr = genstat.res-int[1] NO-LOCK NO-ERROR. 
        IF AVAILABLE bill THEN 
        DO:
                output-list.regno   = bill.rechnr2.
                output-list.bill-no = bill.rechnr.
        END.

        /*
        FIND FIRST master WHERE master.resnr = output-list.resnr NO-LOCK NO-ERROR. 
        IF AVAILABLE master AND master.active THEN output-list.verstat = master.rechnr. */

        FIND FIRST tbill WHERE tbill.resnr = output-list.resnr
            AND tbill.reslinnr = 0 NO-LOCK NO-ERROR.
        IF AVAILABLE tbill THEN output-list.verstat = tbill.rechnr.
        
        FIND FIRST arrangement WHERE arrangement.arrangement = genstat.argt NO-LOCK NO-ERROR.

        IF output-list.zipreis NE 0 THEN
        DO:
            DEF VAR a AS DECIMAL.
          FOR EACH argt-line WHERE argt-line.argtnr = arrangement.argtnr AND NOT argt-line.kind2
            AND argt-line.kind1,
            FIRST artikel WHERE artikel.artnr = argt-line.argt-artnr 
            AND artikel.departement = argt-line.departement NO-LOCK:

            RUN get-genstat-argtline-rate(contcode, RECID(argt-line), OUTPUT take-it, 
                         OUTPUT f-betrag, OUTPUT argt-betrag, OUTPUT qty).

            RUN calc-servtaxesbl.p (1, artikel.artnr, artikel.departement,
              curr-date, OUTPUT serv2, OUTPUT vat3, OUTPUT vat4,
              OUTPUT fact2).
            ASSIGN vat3 = vat3 + vat4.

            IF artikel.zwkum = bfast-art AND 
                (artikel.umsatzart = 3 OR artikel.umsatzart GE 5) THEN 
            DO:
              ASSIGN 
                 output-list.bfast  = genstat.res-deci[2] * (1 + vat3 + serv2).
                  /*output-list.bfast  = output-list.bfast + argt-betrag.*/
            END.
            ELSE IF artikel.zwkum = lunch-art AND 
                (artikel.umsatzart = 3 OR artikel.umsatzart GE 5) THEN 
            DO:
              ASSIGN 
                 output-list.lunch  = genstat.res-deci[3] * (1 + vat3 + serv2).
                 /* output-list.lunch  = output-list.lunch + argt-betrag.*/
            END.
            ELSE IF artikel.zwkum = dinner-art AND 
                (artikel.umsatzart = 3 OR artikel.umsatzart GE 5) THEN 
            DO:
              ASSIGN 
                 output-list.dinner = genstat.res-deci[4] * (1 + vat3 + serv2).
                  /*output-list.dinner  = output-list.dinner + argt-betrag.*/
            END.
            ELSE IF artikel.zwkum = lundin-art AND 
                (artikel.umsatzart = 3 OR artikel.umsatzart GE 5) THEN 
            DO:
              ASSIGN 
                output-list.lunch = genstat.res-deci[3] * (1 + vat3 + serv2).
                /*  output-list.dinner  = output-list.dinner + argt-betrag.  */
            END.
            ELSE 
            DO:
                a = a + argt-betrag.
            END.
          END.
        END.

        FOR EACH fixleist WHERE fixleist.resnr = genstat.resnr 
              AND fixleist.reslinnr = genstat.res-int[1] NO-LOCK.
            IF AVAILABLE fixleist THEN
            DO:
              add-it = NO. 
              argt-rate = 0. 
              IF fixleist.sequenz = 1 THEN add-it = YES. 
              ELSE IF fixleist.sequenz = 2 OR fixleist.sequenz = 3 THEN 
              DO: 
                  IF genstat.res-date[1] EQ datum THEN add-it = YES. 
              END. 
              ELSE IF fixleist.sequenz = 4 AND day(datum) = 1 THEN add-it = YES. 
              ELSE IF fixleist.sequenz = 5 
                  AND day(datum + 1) = 1 THEN add-it = YES. 
              ELSE IF fixleist.sequenz = 6 THEN 
              DO: 
                IF lfakt = ? THEN delta = 0. 
                ELSE 
                DO: 
                  delta = lfakt - genstat.res-date[1]. 
                  IF delta LT 0 THEN delta = 0. 
                END. 
                start-date = genstat.res-date[1] + delta. 
                IF (genstat.res-date[2] - start-date) LT fixleist.dekade 
                  THEN start-date = genstat.res-date[1]. 
                IF datum LE (start-date + (fixleist.dekade - 1)) THEN add-it = YES. 
                IF datum LT start-date THEN add-it = no. /* may NOT post !! */ 
              END. 
              IF add-it THEN 
              DO: 
                FIND FIRST artikel WHERE artikel.artnr = fixleist.artnr 
                  AND artikel.departement = fixleist.departement NO-LOCK. 
                argt-rate = fixleist.betrag * fixleist.number. 
              
                IF AVAILABLE artikel AND artikel.artnr = 110 AND argt-rate NE 0 THEN
                DO:
                 output-list.ex-bed = argt-rate.
                END.
                ELSE IF AVAILABLE artikel AND artikel.artnr = 112 AND argt-rate NE 0 THEN
                DO:
                 output-list.add-room = argt-rate.
                END.
              END.
            END.
          END.

          ASSIGN 
             output-list.lodging = output-list.lodging + genstat.logis
             zikatnr             = res-line.zikatnr
             tot-nr              = tot-nr + 1
             tot-zipreis         = tot-zipreis + output-list.zipreis
             tot-amount          = tot-amount  + output-list.amount
             tot-night           = tot-night   + output-list.night
             tot-lodging         = tot-lodging + output-list.lodging
             tot-bfast           = tot-bfast   + output-list.bfast
             tot-adroom          = tot-adroom  + output-list.add-room
             tot-exbed           = tot-exbed   + output-list.ex-bed.
      END.
    END.
    
    /*FIND FIRST resline WHERE resline.resnr = bill.resnr 
    AND resline.reslinnr = bill.reslinnr NO-LOCK.
    IF resline.l-zuordnung[5] NE 0 THEN
    DO:
        FIND FIRST mbill WHERE mbill.resnr = resline.l-zuordnung[5]
            AND mbill.reslinnr = 0 NO-LOCK NO-ERROR.
        IF AVAILABLE mbill THEN 
        DO:
            output-list.ACTIVE = master.active.
        END.*/
    
    CREATE output-list.
    ASSIGN                     
        output-list.ankunft     = ? 
        output-list.abreise     = ? 
        output-list.zinr        = " " 
        output-list.gname       = "T O T A L"
        output-list.resnr       = 0 
        output-list.night       = tot-night
        output-list.zipreis     = tot-zipreis
        output-list.amount      = tot-amount
        output-list.lodging     = tot-lodging  
        output-list.bfast       = tot-bfast 
        output-list.add-room    = tot-adroom 
        output-list.ex-bed      = tot-exbed
        output-list.regno       = 0
        output-list.nr          = tot-nr
        output-list.bill-no     = 0 .

   FOR EACH output-list:
     IF output-list.gname   = "T O T A L" THEN 
     DO:
       ASSIGN gr-zipreis   = gr-zipreis + output-list.zipreis
              gr-amount    = gr-amount  + output-list.amount
              gr-night     = gr-night   + output-list.night
              gr-lodging   = gr-lodging + output-list.lodging 
              gr-bfast     = gr-bfast   + output-list.bfast   
              gr-adroom    = gr-adroom  + output-list.add-room
              gr-exbed     = gr-exbed   + output-list.ex-bed   .
     END.
   END.

   CREATE output-list.
   ASSIGN 
        output-list.ankunft     = ? 
        output-list.abreise     = ? 
        output-list.zinr        = " " 
        output-list.gname       = "GRAND TOTAL" 
        output-list.resnr       = 0 
        output-list.night       = gr-night
        output-list.zipreis     = gr-zipreis
        output-list.amount      = gr-amount
        output-list.lodging     = gr-lodging 
        output-list.bfast       = gr-bfast   
        output-list.add-room    = gr-adroom  
        output-list.ex-bed      = gr-exbed   
        output-list.regno       = 0
        output-list.nr          = tot-nr + 1
        output-list.bill-no     = 0.
END.

PROCEDURE get-argtline-rate :
DEFINE INPUT PARAMETER contcode AS CHAR. 
DEFINE INPUT PARAMETER argt-recid AS INTEGER. 
DEFINE OUTPUT PARAMETER add-it AS LOGICAL INITIAL NO. 
DEFINE OUTPUT PARAMETER argt-betrag AS DECIMAL INITIAL 0. 
DEFINE OUTPUT PARAMETER qty AS INTEGER INITIAL 0. 

DEFINE VARIABLE curr-zikatnr AS INTEGER NO-UNDO. 
DEFINE BUFFER argtline FOR argt-line. 

    IF res-line.l-zuordnung[1] NE 0 THEN curr-zikatnr = res-line.l-zuordnung[1]. 
    ELSE curr-zikatnr = res-line.zikatnr. 

    FIND FIRST argtline WHERE RECID(argtline) = argt-recid NO-LOCK. 
      IF argt-line.vt-percnt = 0 THEN 
      DO: 
        IF argt-line.betriebsnr = 0 THEN qty = res-line.erwachs. 
        ELSE qty = argt-line.betriebsnr. 
      END. 
      ELSE IF argt-line.vt-percnt = 1 THEN qty = res-line.kind1. 
      ELSE IF argt-line.vt-percnt = 2 THEN qty = res-line.kind2. 
      IF qty GT 0 THEN 
      DO: 
        IF argtline.fakt-modus = 1 THEN add-it = YES. 
        ELSE IF argtline.fakt-modus = 2 THEN 
        DO: 
          IF res-line.ankunft EQ curr-date THEN add-it = YES. 
        END. 
        ELSE IF argtline.fakt-modus = 3 THEN 
        DO: 
          IF (res-line.ankunft + 1) EQ curr-date THEN add-it = YES. 
        END. 
        ELSE IF argtline.fakt-modus = 4 
          AND day(curr-date) = 1 THEN add-it = YES. 
        ELSE IF argtline.fakt-modus = 5 
          AND day(curr-date + 1) = 1 THEN add-it = YES. 
        ELSE IF argtline.fakt-modus = 6 THEN 
        DO: 
          IF (res-line.ankunft + (argtline.intervall - 1)) GE curr-date 
          THEN add-it = YES. 
        END. 
      END.

    IF add-it THEN 
    DO: 
      FIND FIRST reslin-queasy WHERE key = "fargt-line" 
          AND reslin-queasy.char1 = "" 
          AND reslin-queasy.resnr = res-line.resnr 
          AND reslin-queasy.reslinnr = res-line.reslinnr 
          AND reslin-queasy.number1 = argtline.departement 
          AND reslin-queasy.number2 =  argtline.argtnr 
          AND reslin-queasy.number3 = argtline.argt-artnr 
          AND curr-date GE reslin-queasy.date1 
          AND curr-date LE reslin-queasy.date2 
          USE-INDEX argt1_ix NO-LOCK NO-ERROR. 
      IF AVAILABLE reslin-queasy THEN 
      DO: 
        argt-betrag = reslin-queasy.deci1 * qty. 
        IF argt-betrag = 0 THEN add-it = NO. 
        RETURN. 
      END. 
  
      IF contcode NE "" THEN 
      DO: 
        FIND FIRST reslin-queasy WHERE reslin-queasy.key = "argt-line" 
          AND reslin-queasy.char1 = contcode 
          AND reslin-queasy.number1 = res-line.reserve-int 
          AND reslin-queasy.number2 = arrangement.argtnr 
          AND reslin-queasy.number3 = argtline.argt-artnr 
          AND reslin-queasy.resnr = argtline.departement 
          AND reslin-queasy.reslinnr = curr-zikatnr 
          AND curr-date GE reslin-queasy.date1 
          AND curr-date LE reslin-queasy.date2 NO-LOCK NO-ERROR. 
        IF AVAILABLE reslin-queasy THEN 
        DO: 
          argt-betrag = reslin-queasy.deci1 * qty. 
          IF argt-betrag = 0 THEN add-it = NO. 
          RETURN. 
        END. 
      END. 
      argt-betrag = argt-line.betrag. 
      FIND FIRST arrangement WHERE arrangement.argtnr = argt-line.argtnr 
        NO-LOCK NO-ERROR. 

      FIND FIRST waehrung WHERE waehrung.waehrungsnr = arrangement.betriebsnr 
      NO-LOCK NO-ERROR.
        
      IF res-line.betriebsnr NE arrangement.betriebsnr THEN 
        argt-betrag = argt-betrag * (waehrung.ankauf / waehrung.einheit) / frate. 
      argt-betrag = argt-betrag * qty. 
      IF argt-betrag = 0 THEN add-it = NO. 
    END.
END.

PROCEDURE get-genstat-argtline-rate :
DEFINE INPUT PARAMETER contcode AS CHAR. 
DEFINE INPUT PARAMETER argt-recid AS INTEGER. 
DEFINE OUTPUT PARAMETER add-it AS LOGICAL INITIAL NO.
DEFINE OUTPUT PARAMETER f-betrag AS DECIMAL.
DEFINE OUTPUT PARAMETER argt-betrag AS DECIMAL INITIAL 0. 
DEFINE OUTPUT PARAMETER qty AS INTEGER INITIAL 0. 

DEFINE VARIABLE curr-zikatnr AS INTEGER NO-UNDO. 
DEFINE BUFFER argtline FOR argt-line. 

    IF res-line.l-zuordnung[1] NE 0 THEN curr-zikatnr = res-line.l-zuordnung[1]. 
    ELSE curr-zikatnr = res-line.zikatnr. 

    FIND FIRST argtline WHERE RECID(argtline) = argt-recid NO-LOCK. 
      IF argt-line.vt-percnt = 0 THEN 
      DO: 
        IF argt-line.betriebsnr = 0 THEN qty = genstat.erwachs. 
        ELSE qty = argt-line.betriebsnr. 
      END. 
      ELSE IF argt-line.vt-percnt = 1 THEN qty = genstat.kind1. 
      ELSE IF argt-line.vt-percnt = 2 THEN qty = genstat.kind2. 
      IF qty GT 0 THEN 
      DO: 
        IF argtline.fakt-modus = 1 THEN add-it = YES. 
        ELSE IF argtline.fakt-modus = 2 THEN 
        DO: 
          IF res-line.ankunft EQ curr-date THEN add-it = YES. 
        END. 
        ELSE IF argtline.fakt-modus = 3 THEN 
        DO: 
          IF (res-line.ankunft + 1) EQ curr-date THEN add-it = YES. 
        END. 
        ELSE IF argtline.fakt-modus = 4 
          AND day(curr-date) = 1 THEN add-it = YES. 
        ELSE IF argtline.fakt-modus = 5 
          AND day(curr-date + 1) = 1 THEN add-it = YES. 
        ELSE IF argtline.fakt-modus = 6 THEN 
        DO: 
          IF (res-line.ankunft + (argtline.intervall - 1)) GE curr-date 
          THEN add-it = YES. 
        END. 
      END.

    IF add-it THEN 
    DO: 
      FIND FIRST reslin-queasy WHERE key = "fargt-line" 
          AND reslin-queasy.char1 = "" 
          AND reslin-queasy.resnr = res-line.resnr 
          AND reslin-queasy.reslinnr = res-line.reslinnr 
          AND reslin-queasy.number1 = argtline.departement 
          AND reslin-queasy.number2 =  argtline.argtnr 
          AND reslin-queasy.number3 = argtline.argt-artnr 
          AND curr-date GE reslin-queasy.date1 
          AND curr-date LE reslin-queasy.date2 
          USE-INDEX argt1_ix NO-LOCK NO-ERROR. 
      IF AVAILABLE reslin-queasy THEN 
      DO: 
        argt-betrag = reslin-queasy.deci1 * qty. 
        IF argt-betrag = 0 THEN add-it = NO. 
        RETURN. 
      END. 
  
      IF contcode NE "" THEN 
      DO: 
        FIND FIRST reslin-queasy WHERE reslin-queasy.key = "argt-line" 
          AND reslin-queasy.char1 = contcode 
          AND reslin-queasy.number1 = res-line.reserve-int 
          AND reslin-queasy.number2 = arrangement.argtnr 
          AND reslin-queasy.number3 = argtline.argt-artnr 
          AND reslin-queasy.resnr = argtline.departement 
          AND reslin-queasy.reslinnr = curr-zikatnr 
          AND curr-date GE reslin-queasy.date1 
          AND curr-date LE reslin-queasy.date2 NO-LOCK NO-ERROR. 
        IF AVAILABLE reslin-queasy THEN 
        DO: 
          argt-betrag = reslin-queasy.deci1 * qty. 
          IF argt-betrag = 0 THEN add-it = NO. 
          RETURN. 
        END. 
      END. 
      argt-betrag = argt-line.betrag. 
      FIND FIRST arrangement WHERE arrangement.argtnr = argt-line.argtnr 
        NO-LOCK NO-ERROR. 

      FIND FIRST waehrung WHERE waehrung.waehrungsnr = arrangement.betriebsnr 
      NO-LOCK NO-ERROR.
        
      IF res-line.betriebsnr NE arrangement.betriebsnr THEN 
        argt-betrag = argt-betrag * (waehrung.ankauf / waehrung.einheit) / frate. 
      argt-betrag = argt-betrag * qty. 
      IF argt-betrag = 0 THEN add-it = NO. 
    END.
END.
