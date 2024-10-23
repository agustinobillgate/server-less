/*FT 230614 semua nilai ambil dr genstat*/
/*gerald 310820 genstat untuk arrangement dan summary*/
/*NAUFAL - rmrev-bdown-create-billbalance2bl for from-date to-date format*/
/*FD Jan 17, 2021 => New Method get data s-list just from billjournal*/

DEFINE TEMP-TABLE sum-list 
  FIELD bezeich    AS CHAR FORMAT "x(27)" INITIAL "In Local Currency" 
  FIELD pax        AS INTEGER 
  /* Add by Michael @ 27/09/2018 for Grand Mirage request - ticket no E0012E */
  FIELD adult      AS INTEGER INITIAL 0 COLUMN-LABEL "Adult"
  FIELD ch1        AS INTEGER INITIAL 0 COLUMN-LABEL "Ch1"
  FIELD ch2        AS INTEGER INITIAL 0 COLUMN-LABEL "Ch2"
  FIELD comch      AS INTEGER INITIAL 0 COLUMN-LABEL "ComCh"
  /* End of add */
  FIELD com        AS INTEGER FORMAT ">>9" 
  FIELD lodging    AS DECIMAL 
  FIELD bfast      AS DECIMAL 
  FIELD lunch      AS DECIMAL 
  FIELD dinner     AS DECIMAL 
  FIELD misc       AS DECIMAL 
  FIELD fixcost    AS DECIMAL 
  FIELD t-rev      AS DECIMAL. 

DEFINE TEMP-TABLE currency-list 
  FIELD code AS CHAR. 

DEFINE TEMP-TABLE cl-list 
  FIELD zipreis    AS DECIMAL FORMAT ">>>,>>>,>>>,>>9.99" COLUMN-LABEL "Room Rate"     
  FIELD localrate  AS DECIMAL FORMAT ">>,>>>,>>>,>>>,>>9" COLUMN-LABEL "Local Currency"
  FIELD lodging    AS DECIMAL FORMAT ">>>,>>>,>>>,>>9.99" COLUMN-LABEL "Lodging"       
  FIELD bfast      AS DECIMAL FORMAT ">>,>>>,>>>,>>9.99" COLUMN-LABEL "Breakfast"      
  FIELD lunch      AS DECIMAL FORMAT ">>,>>>,>>>,>>9.99" COLUMN-LABEL "Lunch"          
  FIELD dinner     AS DECIMAL FORMAT ">>,>>>,>>>,>>9.99" COLUMN-LABEL "Dinner"         
  FIELD misc       AS DECIMAL FORMAT "->,>>>,>>>,>>9.99" COLUMN-LABEL "Other Rev"      
  FIELD fixcost    AS DECIMAL FORMAT "->>>,>>>,>>9.99" COLUMN-LABEL "FixCost"          
  FIELD t-rev      AS DECIMAL FORMAT ">>>,>>>,>>>,>>9.99" COLUMN-LABEL "Total Rate"    
 
  FIELD c-zipreis    AS CHAR FORMAT "x(18)" LABEL "         Room Rate" 
  FIELD c-localrate  AS CHAR FORMAT "x(18)" LABEL "    Local Currency" 
  FIELD c-lodging    AS CHAR FORMAT "x(18)" LABEL "           Lodging" 
  FIELD c-bfast      AS CHAR FORMAT "x(17)" LABEL "        Breakfast" 
  FIELD c-lunch      AS CHAR FORMAT "x(17)" LABEL "            Lunch" 
  FIELD c-dinner     AS CHAR FORMAT "x(17)" LABEL "           Dinner" 
  FIELD c-misc       AS CHAR FORMAT "x(17)" LABEL "        Other Rev" 
  FIELD c-fixcost    AS CHAR FORMAT "x(15)" LABEL "        FixCost"   
  FIELD ct-rev       AS CHAR FORMAT "x(18)" LABEL "        Total Rate" 
 
  FIELD res-recid  AS INTEGER 
  FIELD sleeping   AS LOGICAL INITIAL YES 
  FIELD row-disp   AS INTEGER INITIAL 0 
  FIELD flag       AS CHAR 
  FIELD zinr       LIKE zimmer.zinr 
  FIELD rstatus    AS INTEGER 
  FIELD argt       AS CHAR FORMAT "x(5)" COLUMN-LABEL "Argt" 
  FIELD currency   AS CHAR FORMAT "x(4)" COLUMN-LABEL "Curr" 
  FIELD ratecode   AS CHAR FORMAT "x(4)" COLUMN-LABEL "RCode"
  FIELD pax        AS INTEGER FORMAT ">>,>>>"        COLUMN-LABEL "Pax" 
  FIELD com        AS INTEGER FORMAT ">>,>>>"        COLUMN-LABEL "Com" 
  FIELD ankunft    AS DATE                           COLUMN-LABEL "Arrival" 
  FIELD abreise    AS DATE                           COLUMN-LABEL "Depart" 
  FIELD rechnr     AS INTEGER FORMAT ">>>>>>>"       COLUMN-LABEL "BillNum" 
  FIELD name       LIKE res-line.name FORMAT "x(19)" COLUMN-LABEL "Guest Name" 
  FIELD ex-rate    AS CHAR FORMAT "x(9)"             COLUMN-LABEL "   ExRate"
  FIELD fix-rate   AS CHAR FORMAT "x(1)"             COLUMN-LABEL "F"
  /* Add by Michael @ 27/09/2018 for Grand Mirage request - ticket no E0012E */
  FIELD adult      AS INTEGER INITIAL 0 COLUMN-LABEL "Adult"
  FIELD ch1        AS INTEGER INITIAL 0 COLUMN-LABEL "Ch1"
  FIELD ch2        AS INTEGER INITIAL 0 COLUMN-LABEL "Ch2"
  FIELD comch      AS INTEGER INITIAL 0 COLUMN-LABEL "ComCh"
  /* End of add */
  /* Add by Michael @ 09/01/2019 for Atria request - ticket no 91A72A */
  FIELD age1       AS INTEGER INITIAL 0 COLUMN-LABEL "Age"
  FIELD age2       AS CHAR FORMAT "x(10)" COLUMN-LABEL "Age"
  /* End of add */
  /*MNaufal 170322 - for Ramada Solo request DFDC33*/
  FIELD rmtype     AS CHAR FORMAT "x(6)" COLUMN-LABEL "RmType"
  /*Ragung F46D14 penambahan kolom reservasi*/
  FIELD resnr      LIKE res-line.resnr COLUMN-LABEL "Resnr" 
  FIELD resname    LIKE res-line.resname    COLUMN-LABEL "Reserve Name" 
  FIELD segm-desc  AS CHARACTER
  FIELD nation     AS CHARACTER
  . 
 
DEFINE TEMP-TABLE s-list 
  FIELD artnr AS INTEGER 
  FIELD dept AS INTEGER 
  FIELD bezeich  AS CHAR FORMAT "x(24)" 
  FIELD curr AS CHAR FORMAT "x(4)" 
  FIELD anzahl AS INTEGER FORMAT ">>>>9" INITIAL 0 
  FIELD betrag AS DECIMAL FORMAT "->,>>>,>>>,>>9.99" INITIAL 0 
  FIELD l-betrag AS DECIMAL FORMAT "->,>>>,>>>,>>9.99" INITIAL 0 
  FIELD f-betrag AS DECIMAL FORMAT "->>>,>>9.99" INITIAL 0. 

DEFINE TEMP-TABLE argt-list
    FIELD argtnr    AS INTEGER
    FIELD argtcode  AS CHARACTER /*fd*/
    FIELD bezeich   AS CHAR
    FIELD room      AS INTEGER
    FIELD pax       AS INTEGER
    FIELD qty       AS INTEGER
    FIELD bfast     AS DECIMAL. /*fd*/

DEFINE TEMP-TABLE t-argt-line LIKE argt-line. /*FD*/

DEF INPUT PARAMETER exc-taxserv     AS LOGICAL NO-UNDO.
DEF INPUT PARAMETER pvILanguage     AS INTEGER  NO-UNDO.
DEF INPUT PARAMETER new-contrate    AS LOGICAL.
DEF INPUT PARAMETER foreign-rate    AS LOGICAL.
DEF INPUT PARAMETER price-decimal   AS INT.
DEF INPUT PARAMETER fdate           AS DATE.
DEF INPUT PARAMETER tdate           AS DATE.
DEF INPUT PARAMETER srttype         AS INTEGER. /* add sorttype by damen 07/03/23 485054 */
DEF OUTPUT PARAMETER TABLE FOR cl-list.
DEF OUTPUT PARAMETER TABLE FOR currency-list.
DEF OUTPUT PARAMETER TABLE FOR sum-list.
DEF OUTPUT PARAMETER TABLE FOR s-list.
DEF OUTPUT PARAMETER TABLE FOR argt-list.

DEFINE VARIABLE exchg-rate          AS DECIMAL INITIAL 1. 
DEFINE VARIABLE frate               AS DECIMAL FORMAT ">,>>>,>>9.9999". 
DEFINE VARIABLE post-it             AS LOGICAL. 
DEFINE VARIABLE total-rev           AS DECIMAL.

DEFINE BUFFER waehrung1 FOR waehrung. 
DEFINE BUFFER cc-list FOR cl-list. 

{SupertransBL.i} 
DEF VAR lvCAREA AS CHAR INITIAL "rmrev-bdown".

RUN create-billbalance1.

PROCEDURE create-billbalance1: 
  DEFINE BUFFER member1 FOR guest. 
  DEFINE BUFFER rguest FOR guest. 
  DEFINE VARIABLE fcost AS DECIMAL. 
  DEFINE VARIABLE tot-pax AS INTEGER INITIAL 0. 
  DEFINE VARIABLE tot-com AS INTEGER INITIAL 0. 
  DEFINE VARIABLE tot-rm AS INTEGER INITIAL 0. 
  DEFINE VARIABLE tot-rate AS DECIMAL INITIAL 0. 
  DEFINE VARIABLE tot-Lrate AS DECIMAL INITIAL 0. 
  DEFINE VARIABLE tot-lodging AS DECIMAL INITIAL 0. 
  DEFINE VARIABLE tot-bfast AS DECIMAL INITIAL 0. 
  DEFINE VARIABLE tot-lunch AS DECIMAL INITIAL 0. 
  DEFINE VARIABLE tot-dinner AS DECIMAL INITIAL 0. 
  DEFINE VARIABLE tot-misc AS DECIMAL INITIAL 0. 
  DEFINE VARIABLE tot-fix AS DECIMAL INITIAL 0. 
  /* Add by Michael @ 27/09/2018 for Grand Mirage request - ticket no E0012E */
  DEFINE VARIABLE tot-adult AS INTEGER INITIAL 0. 
  DEFINE VARIABLE tot-ch1 AS INTEGER INITIAL 0. 
  DEFINE VARIABLE tot-ch2 AS INTEGER INITIAL 0. 
  DEFINE VARIABLE tot-comch AS INTEGER INITIAL 0. 
  /* End of add */
 
  DEFINE VARIABLE Ltot-rm AS INTEGER INITIAL 0. 
  DEFINE VARIABLE Ltot-pax AS INTEGER INITIAL 0. 
  DEFINE VARIABLE Ltot-rate AS DECIMAL INITIAL 0. 
  DEFINE VARIABLE Ltot-lodging AS DECIMAL INITIAL 0. 
  DEFINE VARIABLE Ltot-bfast AS DECIMAL INITIAL 0. 
  DEFINE VARIABLE Ltot-lunch AS DECIMAL INITIAL 0. 
  DEFINE VARIABLE Ltot-dinner AS DECIMAL INITIAL 0. 
  DEFINE VARIABLE Ltot-misc AS DECIMAL INITIAL 0. 
  DEFINE VARIABLE Ltot-fix AS DECIMAL INITIAL 0. 
 
  DEFINE VARIABLE curr-zinr AS CHAR. 
  DEFINE VARIABLE curr-resnr AS INTEGER INITIAL 0. 
 
  DEFINE VARIABLE bfast-art AS INTEGER. 
  DEFINE VARIABLE lunch-art AS INTEGER. 
  DEFINE VARIABLE dinner-art AS INTEGER. 
  DEFINE VARIABLE lundin-art AS INTEGER. 
  DEFINE VARIABLE fb-dept AS INTEGER. 
  DEFINE VARIABLE argt-betrag AS DECIMAL. 
  DEFINE VARIABLE take-it AS LOGICAL. 
  DEFINE VARIABLE prcode AS INTEGER. 
 
  DEFINE VARIABLE qty AS INTEGER. 
  DEFINE VARIABLE r-qty AS INTEGER INITIAL 0. 
  DEFINE VARIABLE lodge-betrag AS DECIMAL. 
  DEFINE VARIABLE f-betrag AS DECIMAL. 
  DEFINE VARIABLE s AS CHAR.
 
  DEFINE VARIABLE ct        AS CHAR.
  DEFINE VARIABLE contcode  AS CHAR.
  DEFINE VARIABLE vat           AS DECIMAL.
  DEFINE VARIABLE service       AS DECIMAL.
  DEFINE VARIABLE vat1          AS DECIMAL.
  DEFINE VARIABLE service1      AS DECIMAL.

  DEFINE VARIABLE serv1         AS DECIMAL.
  DEFINE VARIABLE serv2         AS DECIMAL.
  DEFINE VARIABLE vat2          AS DECIMAL.
  DEFINE VARIABLE vat3          AS DECIMAL.
  DEFINE VARIABLE vat4          AS DECIMAL.
  DEFINE VARIABLE fact          AS DECIMAL.
  DEFINE VARIABLE fact1         AS DECIMAL.
  DEFINE VARIABLE fact2         AS DECIMAL.
  DEFINE VARIABLE cr-code       AS CHAR.
  DEFINE VARIABLE loopi         AS INTEGER.
  DEFINE VARIABLE str1          AS CHAR.

  DEFINE VARIABLE curr-zikatnr AS INTEGER NO-UNDO. 
  DEFINE BUFFER artikel1 FOR artikel. 
 
  /*FD February 03, 2021*/
  DEFINE VARIABLE bill-rechnr AS INTEGER.
  DEFINE VARIABLE bill-master AS INTEGER.
  DEFINE VARIABLE serv-1 AS DECIMAL.
  DEFINE VARIABLE vat-1 AS DECIMAL.
  DEFINE VARIABLE vat-2 AS DECIMAL.
  DEFINE VARIABLE fact-1 AS DECIMAL.
  DEFINE VARIABLE serv-2 AS DECIMAL.
  DEFINE VARIABLE vat-3 AS DECIMAL. 
  DEFINE VARIABLE vat-4 AS DECIMAL. 
  DEFINE VARIABLE fact-2 AS DECIMAL.
  DEFINE VARIABLE bill-flag1 AS CHARACTER.  
  DEFINE VARIABLE bill-flag2 AS CHARACTER. 
  DEFINE VARIABLE deposit-art AS INTEGER. /*MNaufal D8F0B7 - add variable for exclude deposit article*/

  FIND FIRST htparam WHERE paramnr = 125 NO-LOCK. 
  bfast-art = htparam.finteger.               /* Rulita 211024 | Fixing for serverless */  
  FIND FIRST htparam WHERE paramnr = 126 NO-LOCK. 
  fb-dept = htparam.finteger.               /* Rulita 211024 | Fixing for serverless */  
  FIND FIRST htparam WHERE paramnr = 227 NO-LOCK. 
  lunch-art = htparam.finteger.               /* Rulita 211024 | Fixing for serverless */  
  FIND FIRST htparam WHERE paramnr = 228 NO-LOCK. 
  dinner-art = htparam.finteger.               /* Rulita 211024 | Fixing for serverless */ 
  FIND FIRST htparam WHERE paramnr = 229 NO-LOCK. 
  lundin-art = htparam.finteger.               /* Rulita 211024 | Fixing for serverless */  
  /*MNaufal D8F0B7 - add variable for exclude deposit article*/
  FIND FIRST htparam WHERE paramnr = 120 NO-LOCK.
  deposit-art = htparam.finteger.               /* Rulita 211024 | Fixing for serverless */ 

  FIND FIRST artikel WHERE artikel.zwkum = bfast-art 
    AND artikel.departement = fb-dept NO-LOCK NO-ERROR. 
  IF NOT AVAILABLE artikel AND bfast-art NE 0 THEN RETURN.
      
  FIND FIRST artikel WHERE artikel.zwkum = lunch-art 
    AND artikel.departement = fb-dept NO-LOCK NO-ERROR. 
  IF NOT AVAILABLE artikel AND lunch-art NE 0 THEN RETURN.
      
  FIND FIRST artikel WHERE artikel.zwkum = dinner-art 
    AND artikel.departement = fb-dept NO-LOCK NO-ERROR. 
  IF NOT AVAILABLE artikel AND dinner-art NE 0 THEN RETURN. 
      
  FIND FIRST artikel WHERE artikel.zwkum = lundin-art 
    AND artikel.departement = fb-dept NO-LOCK NO-ERROR. 
  IF NOT AVAILABLE artikel AND lundin-art NE 0 THEN RETURN. 
 
  FOR EACH s-list: 
    DELETE s-list. 
  END. 
  FOR EACH cl-list: 
    DELETE cl-list. 
  END. 
  FOR EACH currency-list: 
    DELETE currency-list. 
  END. 
   
  FOR EACH sum-list:
    DELETE sum-list.
  END.

  CREATE sum-list. 
 
  r-qty = 0. 
  lodge-betrag = 0. 

  /* add sorttype by damen 07/03/23 485054 */
  if srttype = 2 then
  DO:
    FOR EACH genstat WHERE genstat.zinr NE "" 
     AND genstat.datum GE fdate AND genstat.datum LE tdate 
     AND genstat.res-logic[2] NO-LOCK,
     FIRST res-line WHERE res-line.resnr = genstat.resnr
     AND res-line.reslinnr = genstat.res-int[1] 
     AND res-line.l-zuordnung[3] = 0 NO-LOCK, 
     FIRST zimmer WHERE zimmer.zinr = genstat.zinr NO-LOCK /*ft*/
     BY res-line.resname: 
    
      ASSIGN
          serv1    = 0
          vat1     = 0
          vat2     = 0
          fact1    = 0.

      FIND FIRST arrangement WHERE 
        arrangement.arrangement = genstat.argt NO-LOCK NO-ERROR. /*ft*/

      FIND FIRST artikel WHERE artikel.artnr = arrangement.argt-artikelnr 
          AND artikel.departement = 0 NO-LOCK NO-ERROR. 

      /*wen*/
      RUN calc-servtaxesbl.p (1, artikel.artnr, artikel.departement,
                genstat.datum, OUTPUT serv1, OUTPUT vat1, OUTPUT vat2,
                OUTPUT fact1).
    
      FIND FIRST waehrung1 WHERE waehrung1.waehrungsnr = res-line.betriebsnr NO-LOCK NO-ERROR.
      
      FIND FIRST exrate WHERE exrate.datum GE fdate AND exrate.datum LE tdate
          AND exrate.artnr = waehrung1.waehrungsnr NO-LOCK NO-ERROR.
      exchg-rate = exrate.betrag.

      IF res-line.reserve-dec NE 0 THEN frate = res-line.reserve-dec. 
      ELSE frate = exchg-rate. 
  
      IF genstat.zipreis NE 0 THEN r-qty = r-qty + 1. 
      FIND FIRST guest WHERE guest.gastnr = res-line.gastnrpay NO-LOCK NO-ERROR. 
      FIND FIRST member1 WHERE member1.gastnr = res-line.gastnrmember NO-LOCK NO-ERROR. 
      FIND FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK NO-ERROR. 
  
      IF res-line.l-zuordnung[1] NE 0 THEN curr-zikatnr = res-line.l-zuordnung[1]. 
      ELSE curr-zikatnr = res-line.zikatnr.     

      /*FD Jan 17, 2021 => get bill number*/
      /*Naufal - change to for each billjournal from find first billjournal. Fix discrepancy Lodging in summary*/
      FOR EACH billjournal WHERE billjournal.bill-datum EQ genstat.datum
          AND billjournal.zinr EQ genstat.zinr NO-LOCK:
          bill-flag1 = "".
          FIND FIRST bill WHERE bill.resnr EQ genstat.resnr 
              AND bill.reslinnr EQ 0 NO-LOCK NO-ERROR. 
          IF AVAILABLE bill THEN 
          DO:
              bill-master = bill.rechnr.  
              bill-flag1 = "Master Bill".
          END.
          IF bill-flag1 EQ "Master Bill" THEN LEAVE.
      END.

      FIND FIRST bill WHERE bill.resnr EQ genstat.resnr
          AND bill.reslinnr EQ genstat.res-int[1] NO-LOCK NO-ERROR.
      IF AVAILABLE bill THEN 
      DO:            
          bill-rechnr = bill.rechnr.
          bill-flag2 = "Guest Bill".
      END. 
      
      ASSIGN       
      sum-list.pax = sum-list.pax + genstat.erwachs + genstat.kind1 + genstat.kind2 
        sum-list.adult = sum-list.adult + genstat.erwachs    /*FD*/
        sum-list.com = sum-list.com + genstat.gratis + genstat.kind3. 
      
      CREATE cl-list. 
      ASSIGN
        cl-list.res-recid     = RECID(res-line)
        cl-list.zinr          = genstat.zinr
        cl-list.rstatus       = genstat.resstatus 
        cl-list.sleeping      = zimmer.sleeping
        cl-list.argt          = genstat.argt
        cl-list.name          = res-line.NAME + "-"      
        cl-list.com           = genstat.gratis
        cl-list.ankunft       = res-line.ankunft 
        cl-list.abreise       = res-line.abreise
        cl-list.resnr         = res-line.resnr        /*Add by Ragung*/ 
        cl-list.resname       = res-line.resname.     /*Add by Ragung*/

      IF NOT exc-taxserv THEN DO:
          ASSIGN
              cl-list.zipreis       = genstat.zipreis 
              cl-list.localrate     = genstat.rateLocal       
              cl-list.t-rev         = genstat.zipreis       
              cl-list.lodging       = genstat.logis * (1 + vat1 + vat2 + serv1)
              cl-list.fixcost       = genstat.res-deci[6] * (1 + vat1 + vat2 + serv1).
      END.
      ELSE DO: /*Naufal - Move from line 1102 for bugs fixing descripancy data tax & exc-tax*/
          ASSIGN
              cl-list.zipreis     = ROUND((genstat.zipreis / (1 + vat1 + vat2 + serv1)),price-decimal)
              cl-list.localrate   = ROUND((genstat.rateLocal / (1 + vat1 + vat2 + serv1)),price-decimal)
              cl-list.t-rev       = ROUND((genstat.zipreis / (1 + vat1 + vat2 + serv1)),price-decimal)
              cl-list.lodging     = ROUND(genstat.logis,price-decimal)
              cl-list.fixcost     = ROUND(genstat.res-deci[6],price-decimal).
      END.

      ASSIGN /*FD*/
        sum-list.lodging  = sum-list.lodging + cl-list.lodging
        sum-list.t-rev    = sum-list.t-rev + genstat.zipreis
        sum-list.fixcost  = sum-list.fixcost + cl-list.fixcost.

      /*FD Jan 17, 2021*/
      IF bill-flag1 EQ "Master Bill" THEN
      DO:
          FIND FIRST billjournal WHERE billjournal.rechnr EQ bill-master
              AND billjournal.bill-datum EQ genstat.datum NO-LOCK NO-ERROR.
          IF AVAILABLE billjournal THEN cl-list.rechnr = bill-master.
      END.

      IF bill-flag2 EQ "Guest Bill" THEN
      DO:
          FIND FIRST billjournal WHERE billjournal.rechnr EQ bill-rechnr
              AND billjournal.bill-datum EQ genstat.datum NO-LOCK NO-ERROR.
          IF AVAILABLE billjournal THEN cl-list.rechnr = bill-rechnr.
      END.
          
      IF genstat.gratis NE 0 THEN cl-list.rechnr = 0.
      /*End FD*/

      /*Add by Michael @ 27/09/2018 for Grand Mirage request - ticket no E0012E */
      ASSIGN
        cl-list.adult    = genstat.erwachs
        cl-list.ch1      = genstat.kind1 
        cl-list.ch2      = genstat.kind2
        cl-list.comch    = genstat.kind3
        .
      /* End of add */
      
      IF cl-list.zipreis EQ 0 AND cl-list.adult EQ 0 THEN ASSIGN cl-list.pax = cl-list.com + cl-list.comch.
      ELSE cl-list.pax = genstat.erwachs + genstat.kind1 + genstat.kind2 + cl-list.com + cl-list.comch.

      /*FDL June 27, 2023 => D32B07*/
      FIND FIRST segment WHERE segment.segmentcode EQ reservation.segmentcode NO-LOCK NO-ERROR.
      IF AVAILABLE segment THEN cl-list.segm-desc = segment.bezeich.

      IF member1.nation1 NE "" THEN cl-list.nation = member1.nation1.

      /*MNaufal 170322 - for Ramada Solo request DFDC33*/
      FIND FIRST zimkateg WHERE zimkateg.zikatnr EQ genstat.zikatnr NO-LOCK NO-ERROR.
      IF AVAILABLE zimkateg THEN ASSIGN cl-list.rmtype = zimkateg.kurzbez.

      IF AVAILABLE guest THEN
      ASSIGN
          cl-list.NAME     = cl-list.NAME + guest.NAME + ", " + guest.vorname1 + "-" + guest.adresse1
          cl-list.rechnr   = bill-rechnr /*NAUFAL - bill.rechnr */
          cl-list.currency = waehrung1.wabkurz.

      /*ITA 280218*/
      FIND FIRST argt-list WHERE argt-list.argtnr = arrangement.argtnr NO-LOCK NO-ERROR.
      IF NOT AVAILABLE argt-list THEN DO:
          CREATE argt-list.
          ASSIGN 
              argt-list.argtnr    = arrangement.argtnr
              argt-list.argtcode  = arrangement.arrangement
              argt-list.bezeich   = argt-bez
              argt-list.room      = 1
              argt-list.pax       = genstat.erwachs + genstat.kind1 + genstat.kind2 + cl-list.com + cl-list.comch.
      END.
      ELSE DO:
          ASSIGN
              argt-list.room    = argt-list.room + 1
              argt-list.pax     = argt-list.pax + (genstat.erwachs + genstat.gratis).
      END.

      /* Add by Michael @ 09/01/2019 for Atria request - ticket no 91A72A */
      IF guest.geburtdatum1 NE ? AND guest.geburtdatum2 NE ? THEN
          IF guest.geburtdatum1 < guest.geburtdatum2 THEN
              cl-list.age1 = YEAR(guest.geburtdatum2) - YEAR(guest.geburtdatum1).
      IF res-line.zimmer-wunsch MATCHES("*ChAge*") THEN
      DO:
          DO loopi = 1 TO NUM-ENTRIES(res-line.zimmer-wunsch, ";") - 1:
              str1 = ENTRY(loopi, res-line.zimmer-wunsch, ";").
              IF SUBSTR(str1,1,5) = "ChAge" THEN
                  /*cl-list.age2 = INT(SUBSTR(str1,6)).*/
                  cl-list.age2 = SUBSTR(str1,6).
          END.
      END.
      /* End of add */

      /*ITA 130216 bfast, lunch, dinner, misc*/
      ASSIGN
          serv2    = 0
          vat3     = 0
          vat4     = 0
          fact2    = 0.

      DO loopi = 1 TO NUM-ENTRIES(genstat.res-char[2], ";") - 1:
          str1 = ENTRY(loopi, genstat.res-char[2], ";").
          IF SUBSTR(str1,1,6) = "$CODE$" THEN DO:
              cr-code = SUBSTR(str1,7).
          END.
      END.
    
      IF genstat.zipreis NE 0 THEN
      DO:
          FOR EACH argt-line WHERE argt-line.argtnr = arrangement.argtnr 
              AND NOT argt-line.kind2 AND argt-line.kind1,
              FIRST artikel WHERE artikel.artnr = argt-line.argt-artnr 
                  AND artikel.departement = argt-line.departement NO-LOCK:
              
              DEFINE BUFFER argtline FOR argt-line. 
              
              RUN get-argtline-rate(contcode, RECID(argt-line), OUTPUT take-it, 
                                  OUTPUT f-betrag, OUTPUT argt-betrag, OUTPUT qty).  
              
              RUN calc-servtaxesbl.p (1, artikel.artnr, artikel.departement,
                    genstat.datum, OUTPUT serv2, OUTPUT vat3, OUTPUT vat4,
                    OUTPUT fact2).
              ASSIGN vat3 = vat3 + vat4.
              
              IF artikel.zwkum = bfast-art AND 
                  (artikel.umsatzart = 3 OR artikel.umsatzart GE 5) THEN 
              DO:
                  IF NOT exc-taxserv THEN
                  DO:
                      ASSIGN 
                          cl-list.bfast  = genstat.res-deci[2] * (1 + vat3 + serv2)
                          sum-list.bfast = sum-list.bfast + cl-list.bfast. 
                  END.
                  ELSE DO: /*MNaufal - Move from line 1106*/
                      ASSIGN 
                          cl-list.bfast  = ROUND(genstat.res-deci[2],price-decimal)
                          sum-list.bfast = ROUND(sum-list.bfast + cl-list.bfast,price-decimal). 
                  END.
              END.
              ELSE IF artikel.zwkum = lunch-art AND 
                  (artikel.umsatzart = 3 OR artikel.umsatzart GE 5) THEN 
              DO:
                  IF NOT exc-taxserv THEN
                  DO:
                      ASSIGN 
                          cl-list.lunch  = genstat.res-deci[3] * (1 + vat3 + serv2)
                          sum-list.lunch = sum-list.lunch + cl-list.lunch.
                  END.
                  ELSE DO: /*MNaufal - move from line 1106*/
                      ASSIGN
                          cl-list.lunch  = ROUND(genstat.res-deci[3],price-decimal)
                          sum-list.lunch = ROUND(sum-list.lunch + cl-list.lunch,price-decimal).
                  END.
              END.
              ELSE IF artikel.zwkum = dinner-art AND 
                  (artikel.umsatzart = 3 OR artikel.umsatzart GE 5) THEN 
              DO:
                  IF NOT exc-taxserv THEN
                  DO:
                      ASSIGN 
                          cl-list.dinner  = genstat.res-deci[4] * (1 + vat3 + serv2)
                          sum-list.dinner = sum-list.dinner + cl-list.dinner.
                  END.
                  ELSE DO: /*Naufal - Move from line 1106*/
                      ASSIGN 
                          cl-list.dinner  = ROUND(genstat.res-deci[4],price-decimal)
                          sum-list.dinner = ROUND(sum-list.dinner + cl-list.dinner,price-decimal).
                  END.             
              END.
              ELSE IF artikel.zwkum = lundin-art AND 
                  (artikel.umsatzart = 3 OR artikel.umsatzart GE 5) THEN 
              DO:
                  IF NOT exc-taxserv THEN
                  DO:
                      ASSIGN 
                          cl-list.lunch  = genstat.res-deci[3] * (1 + vat3 + serv2)
                          sum-list.lunch = sum-list.lunch + cl-list.lunch.
                  END.
                  ELSE DO: /*Naufal - Move from line 1106*/
                      ASSIGN 
                          cl-list.lunch  = ROUND(genstat.res-deci[3],price-decimal)
                          sum-list.lunch = ROUND(sum-list.lunch + cl-list.lunch,price-decimal).
                  END.             
              END.
              ELSE 
              DO:
                  IF argt-betrag NE 0 THEN
                  DO:
                      /*Naufal - move to line 550 for bugs fixing case aston madiun*/
                      /*ASSIGN 
                          /*FD Comment 30 Juny, 2021 => if data from argt-line not sequential(bfast, lunch, dinner),
                                                      then Other Rev will discrepancy value
                          cl-list.misc = genstat.rateLocal - (cl-list.lodging + cl-list.bfast + cl-list.lunch + cl-list.dinner).  
                          */            
                          /*FD Sept 20, 2021*/
                          cl-list.misc = genstat.res-deci[5] * (1 + vat3 + serv2)
                          sum-list.misc = sum-list.misc + cl-list.misc.*/
                  END.
                  /*
                  IF cl-list.misc LT 0 AND cl-list.misc GT -1 THEN DO: 
                      cl-list.misc = 0.00.
                  END.*/ /*Naufal - move to line 550 for bugs fixing case aston madiun*/
              END.
          END.
          /*Naufal - Move from line 534 for bugs fixing case aston madiun*/
          IF NOT exc-taxserv THEN
          DO:
              ASSIGN
                  cl-list.misc  = cl-list.localrate - (cl-list.lodging + cl-list.bfast + cl-list.lunch + cl-list.dinner)
                  sum-list.misc = sum-list.misc + cl-list.misc.
          END.
          ELSE DO:
              ASSIGN
                  cl-list.misc  = genstat.res-deci[5]
                  sum-list.misc = sum-list.misc + cl-list.misc.
          END.

          IF cl-list.misc LT 0 AND cl-list.misc GT -1 THEN DO: 
              cl-list.misc = 0.00.
          END.
      END.
    /*end*/ 
      FIND FIRST htparam WHERE htparam.paramnr = 127 NO-LOCK. 
      IF htparam.flogical AND NOT exc-taxserv THEN
          ASSIGN 
              cl-list.zipreis       = ROUND(cl-list.zipreis,price-decimal)
              cl-list.lodging       = ROUND(cl-list.lodging,price-decimal)
              cl-list.bfast         = ROUND(cl-list.bfast,price-decimal)
              cl-list.lunch         = ROUND(cl-list.lunch,price-decimal)
              cl-list.dinner        = ROUND(cl-list.dinner,price-decimal)
              cl-list.misc          = ROUND(cl-list.misc ,price-decimal)
              cl-list.fixcost       = ROUND(cl-list.fixcost,price-decimal)
              cl-list.localrate     = ROUND(cl-list.localrate,price-decimal)
              cl-list.t-rev         = ROUND(cl-list.t-rev,price-decimal).
      
      IF res-line.zimmer-wunsch MATCHES("*$CODE$*") THEN
      DO: 
          s = SUBSTR(res-line.zimmer-wunsch,(INDEX(res-line.zimmer-wunsch,"$CODE$") + 6)).
          cl-list.ratecode = TRIM(ENTRY(1, s, ";")).
      END.
      
      IF frate EQ 1 THEN cl-list.ex-rate = STRING(frate,"   >>9.99"). 
      ELSE IF frate LE 999 THEN cl-list.ex-rate = STRING(frate," >>9.9999"). 
      ELSE IF frate LE 99999 THEN cl-list.ex-rate = STRING(frate,">>,>>9.99"). 
      ELSE cl-list.ex-rate = STRING(frate,">,>>>,>>9"). 
      
      FIND FIRST reslin-queasy WHERE reslin-queasy.key = "arrangement" 
          AND reslin-queasy.resnr = res-line.resnr 
          AND reslin-queasy.reslinnr = res-line.reslinnr 
          AND tdate GE reslin-queasy.date1 
          AND fdate LE reslin-queasy.date2 NO-LOCK NO-ERROR. 
      IF AVAILABLE reslin-queasy THEN ASSIGN cl-list.fix-rate = "F".

      tot-rate = tot-rate + cl-list.zipreis. 
      tot-Lrate = tot-Lrate + cl-list.localrate. 
      IF NOT res-line.adrflag THEN tot-pax = tot-pax + cl-list.pax. 
      ELSE Ltot-pax = Ltot-pax + cl-list.pax. 
      tot-com = tot-com + cl-list.com. 
      /* Add by Michael @ 27/09/2018 for Grand Mirage request - ticket no E0012E */
      tot-adult = tot-adult + cl-list.adult.
      tot-ch1   = tot-ch1   + cl-list.ch1.
      tot-ch2   = tot-ch2   + cl-list.ch2.
      tot-comch = tot-comch + cl-list.comch.
      /* End of add */    
  
      /*FD August 12, 2021 => Validation if double arrangement line*/
      FOR EACH argt-line WHERE argt-line.argtnr = arrangement.argtnr 
          AND NOT argt-line.kind2 AND argt-line.kind1 
          BY argt-line.argtnr BY argt-line.argt-artnr:
                  
          FIND FIRST t-argt-line WHERE t-argt-line.argt-artnr EQ argt-line.argt-artnr
              AND t-argt-line.argtnr EQ arrangement.argtnr
              AND t-argt-line.departement EQ argt-line.departement NO-LOCK NO-ERROR.
          IF NOT AVAILABLE t-argt-line THEN
          DO:
              CREATE t-argt-line.
              BUFFER-COPY argt-line TO t-argt-line.
          END.
      END.

      /*FD February 03, 2021 => New Metode*/
      IF genstat.zipreis NE 0 THEN      
      DO:
          /*FD Jan 17, 2021 => New Method get data s-list just from billjournal*/
          IF bill-flag1 = "Master Bill" THEN
          DO:
              FOR EACH billjournal WHERE billjournal.rechnr EQ bill-master
                  AND billjournal.bill-datum EQ genstat.datum
                  AND billjournal.zinr EQ genstat.zinr
                  AND billjournal.betrag NE 0 /*Naufal 22/09/2022 - change validation from GT 0 to NE 0 for bug fix negative value should be included*/
                  AND billjournal.anzahl NE 0
                  AND NOT billjournal.kassarapport
                  AND billjournal.userinit EQ "$$" NO-LOCK,        
                  FIRST artikel WHERE artikel.artnr EQ billjournal.artnr 
                      AND artikel.departement EQ billjournal.departement
                      AND artikel.artart NE 9 
                  NO-LOCK BY billjournal.sysdate BY billjournal.bill-datum BY billjournal.zinr:                           
                      
                  IF billjournal.artnr NE deposit-art THEN
                  DO: /*MNaufal - add validation for bug fixing deposit articles shouldn't be displayed*/
                      FIND FIRST s-list WHERE s-list.artnr EQ billjournal.artnr 
                          AND s-list.dept EQ billjournal.departement 
                          AND s-list.curr EQ waehrung1.wabkurz NO-LOCK NO-ERROR. 
                      IF NOT AVAILABLE s-list THEN 
                      DO: 
                          CREATE s-list. 
                          ASSIGN 
                              s-list.artnr = billjournal.artnr 
                              s-list.dept = billjournal.departement 
                              s-list.bezeich = billjournal.bezeich 
                              s-list.curr = waehrung1.wabkurz.                     
                      END. 
                      
                      ASSIGN
                          s-list.f-betrag = s-list.f-betrag + billjournal.fremdwaehrng    /*Naufal 200922 - change from billjournal.betrag            */
                          s-list.l-betrag = s-list.l-betrag + billjournal.betrag          /*Naufal 200922 - change from billjournal.betrag * frate    */                 
                      . 
                  END.
              END.  

              bill-master = -1.
          END.
          
          IF bill-flag2 = "Guest Bill" THEN
          DO:
              FOR EACH billjournal WHERE billjournal.rechnr EQ bill-rechnr
                  AND billjournal.bill-datum EQ genstat.datum
                  AND billjournal.zinr EQ genstat.zinr
                  AND billjournal.betrag NE 0 /*Naufal 22/09/2022 - change validation from GT 0 to NE 0 for bug fix negative value should be included*/
                  AND billjournal.anzahl NE 0
                  AND NOT billjournal.kassarapport
                  AND billjournal.userinit EQ "$$" NO-LOCK ,        
                  FIRST artikel WHERE artikel.artnr EQ billjournal.artnr 
                      AND artikel.departement EQ billjournal.departement
                      AND artikel.artart NE 9 
                  NO-LOCK BY billjournal.sysdate BY billjournal.bill-datum BY billjournal.zinr:                           
                    
                  IF billjournal.artnr NE deposit-art THEN
                  DO: /*MNaufal - add validation for bug fixing deposit articles shouldn't be displayed*/
                      FIND FIRST s-list WHERE s-list.artnr EQ billjournal.artnr 
                          AND s-list.dept EQ billjournal.departement 
                          AND s-list.curr EQ waehrung1.wabkurz NO-LOCK NO-ERROR. 
                      IF NOT AVAILABLE s-list THEN 
                      DO: 
                          CREATE s-list. 
                          ASSIGN 
                              s-list.artnr = billjournal.artnr 
                              s-list.dept = billjournal.departement 
                              s-list.bezeich = billjournal.bezeich 
                              s-list.curr = waehrung1.wabkurz.                     
                      END. 
                      
                      ASSIGN
                          s-list.f-betrag = s-list.f-betrag + billjournal.fremdwaehrng    /*Naufal 200922 - change from billjournal.betrag            */
                          s-list.l-betrag = s-list.l-betrag + billjournal.betrag          /*Naufal 200922 - change from billjournal.betrag * frate    */                 
                      . 
                  END.
              END. 

              bill-rechnr = -1.
          END.

        /* FD Comment => move to new method above
        FOR EACH t-argt-line WHERE t-argt-line.argtnr = arrangement.argtnr 
          AND NOT t-argt-line.kind2 AND t-argt-line.kind1 NO-LOCK:
          /*FIRST*/ FOR EACH billjournal WHERE billjournal.artnr = t-argt-line.argt-artnr
            AND billjournal.departement = t-argt-line.departement           
            /*AND billjournal.rechnr = bill-rechnr*/
            AND billjournal.bill-datum = genstat.datum 
            AND billjournal.zinr = genstat.zinr NO-LOCK: /*FD Jan 05, 2022*/
            
            /*RUN calc-servtaxesbl.p (1, billjournal.artnr, billjournal.departement,
              billjournal.bill-datum, OUTPUT serv-1, OUTPUT vat-1, OUTPUT vat2,
              OUTPUT fact-1).*/

            FIND FIRST s-list WHERE s-list.artnr = billjournal.artnr 
              AND s-list.dept = billjournal.departement 
              AND s-list.curr = waehrung.wabkurz NO-LOCK NO-ERROR. 
            IF NOT AVAILABLE s-list THEN 
            DO: 
              CREATE s-list. 
              ASSIGN 
                s-list.artnr = billjournal.artnr 
                s-list.dept = billjournal.departement 
                s-list.bezeich = billjournal.bezeich 
                s-list.curr = waehrung.wabkurz.            
            END.     

            /*IF exc-taxserv THEN
            DO:              
              ASSIGN
                s-list.f-betrag = ROUND ((s-list.f-betrag + billjournal.betrag / (1 + vat-1 + vat-2 + serv-1)),price-decimal)
                s-list.l-betrag = ROUND ((s-list.l-betrag + billjournal.betrag * frate / (1 + vat-1 + vat-2 + serv-1)),price-decimal)
              .
            END.
            ELSE*/

            
            ASSIGN
              s-list.f-betrag = s-list.f-betrag + billjournal.betrag 
              s-list.l-betrag = s-list.l-betrag + billjournal.betrag * frate                 
            .                      
          END.
        END.
        */
      END.

      /* Comment FD - Wrong Lodging Value
      ASSIGN 
          cl-list.lodging = genstat.zipreis - (cl-list.bfast + cl-list.lunch + cl-list.dinner + cl-list.misc).
      */

      IF res-line.adrflag THEN Ltot-lodging = Ltot-lodging + cl-list.lodging. 
      ELSE tot-lodging = tot-lodging + cl-list.lodging. 
  
      lodge-betrag = cl-list.lodging /*FT 230614* frate*/ . 
      IF foreign-rate AND price-decimal = 0 AND NOT res-line.adrflag THEN 
      DO: 
        FIND FIRST htparam WHERE paramnr = 145 NO-LOCK. 
        IF htparam.finteger NE 0 THEN 
        DO: 
          DEFINE VARIABLE i AS INTEGER. 
          DEFINE VARIABLE n AS INTEGER. 
          n = 1. 
          DO i = 1 TO finteger: 
            n = n * 10. 
          END. 
          lodge-betrag = ROUND(lodge-betrag / n, 0) * n. 
        END. 
      END. 
  
      /* FD Comment => move to new method above
      FIND FIRST artikel1 WHERE artikel1.artnr = arrangement.artnr-logis 
        AND artikel1.departement = 0 NO-LOCK NO-ERROR. 
      IF AVAILABLE artikel1 THEN
      DO:
        FIND FIRST s-list WHERE s-list.artnr = artikel1.artnr 
          AND s-list.dept = artikel1.departement 
          AND s-list.curr = waehrung1.wabkurz NO-LOCK NO-ERROR. 
        IF NOT AVAILABLE s-list THEN 
        DO: 
          create s-list. 
          ASSIGN 
            s-list.artnr = artikel1.artnr 
            s-list.dept = artikel1.departement 
            s-list.bezeich = artikel1.bezeich 
            s-list.curr = waehrung1.wabkurz. 
        END.       
        
        /*FD February 03, 2021 => New Metode for exclude tax service
        IF exc-taxserv THEN
        DO:
          ASSIGN 
            s-list.f-betrag = ROUND((s-list.f-betrag + lodge-betrag / frate / (1 + vat1 + vat2 + serv1)),price-decimal)
            s-list.l-betrag = ROUND((s-list.l-betrag + lodge-betrag / (1 + vat1 + vat2 + serv1)),price-decimal)        
            s-list.anzahl = s-list.anzahl + 1. 
            sum-list.lodging = sum-list.lodging + lodge-betrag. 
            sum-list.t-rev = sum-list.t-rev + lodge-betrag
          . 
        END.
        ELSE*/
        DO:
          ASSIGN 
            s-list.f-betrag = s-list.f-betrag + lodge-betrag / frate 
            s-list.l-betrag = s-list.l-betrag + lodge-betrag 
            s-list.anzahl = s-list.anzahl + 1. 
            /*sum-list.lodging = sum-list.lodging + lodge-betrag. 
            sum-list.t-rev = sum-list.t-rev + lodge-betrag*/
          . 
        END.
        /*End FD*/
      END.
      */

      /* FD Comment => move to new method above
      /*FD February 03, 2021 => New Metode for exclude tax service*/
      FOR EACH fixleist WHERE fixleist.resnr = res-line.resnr 
        AND fixleist.reslinnr = res-line.reslinnr NO-LOCK: 
        RUN check-fixleist-posted(fixleist.artnr, fixleist.departement, 
          fixleist.sequenz, fixleist.dekade, 
          fixleist.lfakt, OUTPUT post-it). 
        /*IF NOT post-it THEN DISP fixleist.artnr fixleist.departement fixleist.sequenz fixleist.dekade fixleist.lfakt fixleist.betrag.*/
        IF post-it THEN 
        DO: 
          /*RUN calc-servtaxesbl.p (1, fixleist.artnr, fixleist.departement,
              genstat.datum, OUTPUT serv-2, OUTPUT vat-3, OUTPUT vat-4,
              OUTPUT fact-2).*/

          ASSIGN
            fcost = fixleist.betrag * fixleist.number
            /**/cl-list.t-rev = cl-list.t-rev + fcost
            sum-list.t-rev = sum-list.t-rev + fcost * frate
          . 

          IF res-line.adrflag THEN Ltot-rate = Ltot-rate + fcost. 
          ELSE tot-rate = tot-rate + fcost. 
          
          FIND FIRST artikel WHERE artikel.artnr = fixleist.artnr 
            AND artikel.departement = fixleist.departement NO-LOCK NO-ERROR.
        
          FIND FIRST s-list WHERE s-list.artnr = artikel.artnr 
            AND s-list.dept = artikel.departement 
            AND s-list.curr = waehrung1.wabkurz NO-LOCK NO-ERROR. 
          IF NOT AVAILABLE s-list THEN 
          DO: 
            CREATE s-list. 
            ASSIGN 
              s-list.artnr = artikel.artnr 
              s-list.dept = artikel.departement 
              s-list.bezeich = artikel.bezeich 
              s-list.curr = waehrung1.wabkurz. 
          END. 
        
          IF (artikel.zwkum = bfast-art AND artikel.departement = fb-dept) THEN
          DO:
            /*IF exc-taxserv THEN
            DO:
              ASSIGN 
                s-list.f-betrag = ROUND((s-list.f-betrag + fcost / (1 + vat-3 + vat-4 + serv-2)),price-decimal)
                s-list.l-betrag = ROUND((s-list.l-betrag + fcost * frate / (1 + vat-3 + vat-4 + serv-2)),price-decimal)             
                s-list.anzahl   = s-list.anzahl + fixleist.number
              .  
            END.
            ELSE*/
            DO:
              ASSIGN 
                s-list.f-betrag = s-list.f-betrag + fcost
                s-list.l-betrag = s-list.l-betrag + fcost * frate 
                s-list.anzahl   = s-list.anzahl + fixleist.number
                /* cl-list.bfast   = cl-list.bfast + fcost
                sum-list.bfast  = sum-list.bfast + fcost * frate*/
              .  
            END.                              
            IF res-line.adrflag THEN Ltot-bfast = Ltot-bfast + fcost * frate. 
            ELSE tot-bfast = tot-bfast + fcost. 
          END.
          ELSE IF (artikel.zwkum = lunch-art AND artikel.departement = fb-dept) THEN
          DO:
            /*IF exc-taxserv THEN
            DO:
              ASSIGN 
                s-list.f-betrag = ROUND((s-list.f-betrag + fcost / (1 + vat-3 + vat-4 + serv-2)),price-decimal)
                s-list.l-betrag = ROUND((s-list.l-betrag + fcost * frate / (1 + vat-3 + vat-4 + serv-2)),price-decimal)             
                s-list.anzahl   = s-list.anzahl + fixleist.number
              .  
            END.
            ELSE*/
            DO:
              ASSIGN 
                s-list.f-betrag = s-list.f-betrag + fcost
                s-list.l-betrag = s-list.l-betrag + fcost * frate 
                s-list.anzahl   = s-list.anzahl + fixleist.number
                /*cl-list.lunch   = cl-list.lunch + fcost
                sum-list.lunch  = sum-list.lunch + fcost * frate*/
              .  
            END. 
            IF res-line.adrflag THEN Ltot-lunch = Ltot-lunch + fcost * frate. 
            ELSE tot-lunch = tot-lunch + fcost. 
          END.
          ELSE IF (artikel.zwkum = dinner-art AND artikel.departement = fb-dept) THEN
          DO:
            /*IF exc-taxserv THEN
            DO:
              ASSIGN 
                s-list.f-betrag = ROUND((s-list.f-betrag + fcost / (1 + vat-3 + vat-4 + serv-2)),price-decimal)
                s-list.l-betrag = ROUND((s-list.l-betrag + fcost * frate / (1 + vat-3 + vat-4 + serv-2)),price-decimal)             
                s-list.anzahl   = s-list.anzahl + fixleist.number
              .  
            END.
            ELSE*/
            DO:
              ASSIGN 
                s-list.f-betrag = s-list.f-betrag + fcost
                s-list.l-betrag = s-list.l-betrag + fcost * frate 
                s-list.anzahl   = s-list.anzahl + fixleist.number
                /*cl-list.dinner  = cl-list.dinner + fcost
                sum-list.dinner = sum-list.dinner + fcost * frate*/
              .  
            END. 
            IF res-line.adrflag THEN Ltot-dinner = Ltot-dinner + fcost * frate. 
            ELSE tot-dinner = tot-dinner + fcost. 
          END.
          ELSE
          DO:
          /*IF exc-taxserv THEN
            DO:
              ASSIGN 
                s-list.f-betrag = ROUND((s-list.f-betrag + fcost / (1 + vat-3 + vat-4 + serv-2)),price-decimal)
                s-list.l-betrag = ROUND((s-list.l-betrag + fcost * frate / (1 + vat-3 + vat-4 + serv-2)),price-decimal)             
                s-list.anzahl   = s-list.anzahl + fixleist.number
              .  
            END.
            ELSE*/
            DO:
              ASSIGN 
                s-list.f-betrag = s-list.f-betrag + fcost
                s-list.l-betrag = s-list.l-betrag + fcost * frate 
                s-list.anzahl   = s-list.anzahl + fixleist.number
                /*cl-list.fixcost = cl-list.fixcost + fcost
                sum-list.fixcost = sum-list.fixcost + fcost * frate*/
              .  
            END. 
            IF res-line.adrflag THEN Ltot-fix = Ltot-fix + fcost. 
            ELSE tot-fix = tot-fix + fcost.  
          END.
        END. 
      END.
      /*End FD*/
      */

      IF curr-zinr NE res-line.zinr OR curr-resnr NE res-line.resnr THEN 
      DO: 
        IF res-line.adrflag THEN Ltot-rm = Ltot-rm + 1. 
        ELSE tot-rm = tot-rm + 1. 
      END. 
      curr-zinr = res-line.zinr. 
      curr-resnr = res-line.resnr. 
    END. 
  end.
  else
  DO:
    FOR EACH genstat WHERE genstat.zinr NE "" 
     AND genstat.datum GE fdate AND genstat.datum LE tdate 
     AND genstat.res-logic[2] NO-LOCK,
     FIRST res-line WHERE res-line.resnr = genstat.resnr
     AND res-line.reslinnr = genstat.res-int[1] 
     AND res-line.l-zuordnung[3] = 0 NO-LOCK, 
     FIRST zimmer WHERE zimmer.zinr = genstat.zinr NO-LOCK /*ft*/
     BY genstat.zinr BY genstat.resnr: 
    
      ASSIGN
          serv1    = 0
          vat1     = 0
          vat2     = 0
          fact1    = 0.

      FIND FIRST arrangement WHERE 
        arrangement.arrangement = genstat.argt NO-LOCK NO-ERROR. /*ft*/

      FIND FIRST artikel WHERE artikel.artnr = arrangement.argt-artikelnr 
          AND artikel.departement = 0 NO-LOCK NO-ERROR. 

      /*wen*/
      RUN calc-servtaxesbl.p (1, artikel.artnr, artikel.departement,
                genstat.datum, OUTPUT serv1, OUTPUT vat1, OUTPUT vat2,
                OUTPUT fact1).
    
      FIND FIRST waehrung1 WHERE waehrung1.waehrungsnr = res-line.betriebsnr NO-LOCK NO-ERROR.
      
      FIND FIRST exrate WHERE exrate.datum GE fdate AND exrate.datum LE tdate
          AND exrate.artnr = waehrung1.waehrungsnr NO-LOCK NO-ERROR.
      exchg-rate = exrate.betrag.

      IF res-line.reserve-dec NE 0 THEN frate = res-line.reserve-dec. 
      ELSE frate = exchg-rate. 
  
      IF genstat.zipreis NE 0 THEN r-qty = r-qty + 1. 
      FIND FIRST guest WHERE guest.gastnr = res-line.gastnrpay NO-LOCK NO-ERROR. 
      FIND FIRST member1 WHERE member1.gastnr = res-line.gastnrmember NO-LOCK NO-ERROR. 
      FIND FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK NO-ERROR. 
  
      IF res-line.l-zuordnung[1] NE 0 THEN curr-zikatnr = res-line.l-zuordnung[1]. 
      ELSE curr-zikatnr = res-line.zikatnr.     

      /*FD Jan 17, 2021 => get bill number*/
      /*Naufal - change to for each billjournal from find first billjournal. Fix discrepancy Lodging in summary*/
      FOR EACH billjournal WHERE billjournal.bill-datum EQ genstat.datum
          AND billjournal.zinr EQ genstat.zinr NO-LOCK:
          bill-flag1 = "".
          FIND FIRST bill WHERE bill.resnr EQ genstat.resnr 
              AND bill.reslinnr EQ 0 NO-LOCK NO-ERROR. 
          IF AVAILABLE bill THEN 
          DO:
              bill-master = bill.rechnr.  
              bill-flag1 = "Master Bill".
          END.
          IF bill-flag1 EQ "Master Bill" THEN LEAVE.
      END.

      FIND FIRST bill WHERE bill.resnr EQ genstat.resnr
          AND bill.reslinnr EQ genstat.res-int[1] NO-LOCK NO-ERROR.
      IF AVAILABLE bill THEN 
      DO:            
          bill-rechnr = bill.rechnr.
          bill-flag2 = "Guest Bill".
      END. 
      
      ASSIGN       
      sum-list.pax = sum-list.pax + genstat.erwachs + genstat.kind1 + genstat.kind2 
        sum-list.adult = sum-list.adult + genstat.erwachs    /*FD*/
        sum-list.com = sum-list.com + genstat.gratis + genstat.kind3. 
      
      CREATE cl-list. 
      ASSIGN
        cl-list.res-recid     = RECID(res-line)
        cl-list.zinr          = genstat.zinr
        cl-list.rstatus       = genstat.resstatus 
        cl-list.sleeping      = zimmer.sleeping
        cl-list.argt          = genstat.argt
        cl-list.name          = res-line.NAME + "-"      
        cl-list.com           = genstat.gratis
        cl-list.ankunft       = res-line.ankunft 
        cl-list.abreise       = res-line.abreise
        cl-list.resnr         = res-line.resnr        /*Add by Ragung*/ 
        cl-list.resname       = res-line.resname.     /*Add by Ragung*/

      IF NOT exc-taxserv THEN DO:
          ASSIGN
              cl-list.zipreis       = genstat.zipreis 
              cl-list.localrate     = genstat.rateLocal       
              cl-list.t-rev         = genstat.zipreis       
              cl-list.lodging       = genstat.logis * (1 + vat1 + vat2 + serv1)
              cl-list.fixcost       = genstat.res-deci[6] * (1 + vat1 + vat2 + serv1).
      END.
      ELSE DO: /*Naufal - Move from line 1102 for bugs fixing descripancy data tax & exc-tax*/
          ASSIGN
              cl-list.zipreis     = ROUND((genstat.zipreis / (1 + vat1 + vat2 + serv1)),price-decimal)
              cl-list.localrate   = ROUND((genstat.rateLocal / (1 + vat1 + vat2 + serv1)),price-decimal)
              cl-list.t-rev       = ROUND((genstat.zipreis / (1 + vat1 + vat2 + serv1)),price-decimal)
              cl-list.lodging     = ROUND(genstat.logis,price-decimal)
              cl-list.fixcost     = ROUND(genstat.res-deci[6],price-decimal).
      END.

      ASSIGN /*FD*/
        sum-list.lodging  = sum-list.lodging + cl-list.lodging
        sum-list.t-rev    = sum-list.t-rev + genstat.zipreis
        sum-list.fixcost  = sum-list.fixcost + cl-list.fixcost.

      /*FD Jan 17, 2021*/
      IF bill-flag1 EQ "Master Bill" THEN
      DO:
          FIND FIRST billjournal WHERE billjournal.rechnr EQ bill-master
              AND billjournal.bill-datum EQ genstat.datum NO-LOCK NO-ERROR.
          IF AVAILABLE billjournal THEN cl-list.rechnr = bill-master.
      END.

      IF bill-flag2 EQ "Guest Bill" THEN
      DO:
          FIND FIRST billjournal WHERE billjournal.rechnr EQ bill-rechnr
              AND billjournal.bill-datum EQ genstat.datum NO-LOCK NO-ERROR.
          IF AVAILABLE billjournal THEN cl-list.rechnr = bill-rechnr.
      END.
          
      IF genstat.gratis NE 0 THEN cl-list.rechnr = 0.
      /*End FD*/

      /*Add by Michael @ 27/09/2018 for Grand Mirage request - ticket no E0012E */
      ASSIGN
        cl-list.adult    = genstat.erwachs
        cl-list.ch1      = genstat.kind1 
        cl-list.ch2      = genstat.kind2
        cl-list.comch    = genstat.kind3
        .
      /* End of add */
      
      IF cl-list.zipreis EQ 0 AND cl-list.adult EQ 0 THEN ASSIGN cl-list.pax = cl-list.com + cl-list.comch.
      ELSE cl-list.pax = genstat.erwachs + genstat.kind1 + genstat.kind2 + cl-list.com + cl-list.comch.

      /*FDL June 27, 2023 => D32B07*/
      FIND FIRST segment WHERE segment.segmentcode EQ reservation.segmentcode NO-LOCK NO-ERROR.
      IF AVAILABLE segment THEN cl-list.segm-desc = segment.bezeich.

      IF member1.nation1 NE "" THEN cl-list.nation = member1.nation1.

      /*MNaufal 170322 - for Ramada Solo request DFDC33*/
      FIND FIRST zimkateg WHERE zimkateg.zikatnr EQ genstat.zikatnr NO-LOCK NO-ERROR.
      IF AVAILABLE zimkateg THEN ASSIGN cl-list.rmtype = zimkateg.kurzbez.

      IF AVAILABLE guest THEN
      ASSIGN
          cl-list.NAME     = cl-list.NAME + guest.NAME + ", " + guest.vorname1 + "-" + guest.adresse1
          cl-list.rechnr   = bill-rechnr /*NAUFAL - bill.rechnr */
          cl-list.currency = waehrung1.wabkurz.

      /*ITA 280218*/
      FIND FIRST argt-list WHERE argt-list.argtnr = arrangement.argtnr NO-LOCK NO-ERROR.
      IF NOT AVAILABLE argt-list THEN DO:
          CREATE argt-list.
          ASSIGN 
              argt-list.argtnr    = arrangement.argtnr
              argt-list.argtcode  = arrangement.arrangement
              argt-list.bezeich   = argt-bez
              argt-list.room      = 1
              argt-list.pax       = genstat.erwachs + genstat.kind1 + genstat.kind2 + cl-list.com + cl-list.comch.
      END.
      ELSE DO:
          ASSIGN
              argt-list.room    = argt-list.room + 1
              argt-list.pax     = argt-list.pax + (genstat.erwachs + genstat.gratis).
      END.

      /* Add by Michael @ 09/01/2019 for Atria request - ticket no 91A72A */
      IF guest.geburtdatum1 NE ? AND guest.geburtdatum2 NE ? THEN
          IF guest.geburtdatum1 < guest.geburtdatum2 THEN
              cl-list.age1 = YEAR(guest.geburtdatum2) - YEAR(guest.geburtdatum1).
      IF res-line.zimmer-wunsch MATCHES("*ChAge*") THEN
      DO:
          DO loopi = 1 TO NUM-ENTRIES(res-line.zimmer-wunsch, ";") - 1:
              str1 = ENTRY(loopi, res-line.zimmer-wunsch, ";").
              IF SUBSTR(str1,1,5) = "ChAge" THEN
                  /*cl-list.age2 = INT(SUBSTR(str1,6)).*/
                  cl-list.age2 = SUBSTR(str1,6).
          END.
      END.
      /* End of add */

      /*ITA 130216 bfast, lunch, dinner, misc*/
      ASSIGN
          serv2    = 0
          vat3     = 0
          vat4     = 0
          fact2    = 0.

      DO loopi = 1 TO NUM-ENTRIES(genstat.res-char[2], ";") - 1:
          str1 = ENTRY(loopi, genstat.res-char[2], ";").
          IF SUBSTR(str1,1,6) = "$CODE$" THEN DO:
              cr-code = SUBSTR(str1,7).
          END.
      END.
    
      IF genstat.zipreis NE 0 THEN
      DO:
          FOR EACH argt-line WHERE argt-line.argtnr = arrangement.argtnr 
              AND NOT argt-line.kind2 AND argt-line.kind1,
              FIRST artikel WHERE artikel.artnr = argt-line.argt-artnr 
                  AND artikel.departement = argt-line.departement NO-LOCK:
              
              DEFINE BUFFER argtline1 FOR argt-line. 
              
              RUN get-argtline-rate(contcode, RECID(argt-line), OUTPUT take-it, 
                                  OUTPUT f-betrag, OUTPUT argt-betrag, OUTPUT qty).  
              
              RUN calc-servtaxesbl.p (1, artikel.artnr, artikel.departement,
                    genstat.datum, OUTPUT serv2, OUTPUT vat3, OUTPUT vat4,
                    OUTPUT fact2).
              ASSIGN vat3 = vat3 + vat4.
              
              IF artikel.zwkum = bfast-art AND 
                  (artikel.umsatzart = 3 OR artikel.umsatzart GE 5) THEN 
              DO:
                  IF NOT exc-taxserv THEN
                  DO:
                      ASSIGN 
                          cl-list.bfast  = genstat.res-deci[2] * (1 + vat3 + serv2)
                          sum-list.bfast = sum-list.bfast + cl-list.bfast. 
                  END.
                  ELSE DO: /*MNaufal - Move from line 1106*/
                      ASSIGN 
                          cl-list.bfast  = ROUND(genstat.res-deci[2],price-decimal)
                          sum-list.bfast = ROUND(sum-list.bfast + cl-list.bfast,price-decimal). 
                  END.
              END.
              ELSE IF artikel.zwkum = lunch-art AND 
                  (artikel.umsatzart = 3 OR artikel.umsatzart GE 5) THEN 
              DO:
                  IF NOT exc-taxserv THEN
                  DO:
                      ASSIGN 
                          cl-list.lunch  = genstat.res-deci[3] * (1 + vat3 + serv2)
                          sum-list.lunch = sum-list.lunch + cl-list.lunch.
                  END.
                  ELSE DO: /*MNaufal - move from line 1106*/
                      ASSIGN
                          cl-list.lunch  = ROUND(genstat.res-deci[3],price-decimal)
                          sum-list.lunch = ROUND(sum-list.lunch + cl-list.lunch,price-decimal).
                  END.
              END.
              ELSE IF artikel.zwkum = dinner-art AND 
                  (artikel.umsatzart = 3 OR artikel.umsatzart GE 5) THEN 
              DO:
                  IF NOT exc-taxserv THEN
                  DO:
                      ASSIGN 
                          cl-list.dinner  = genstat.res-deci[4] * (1 + vat3 + serv2)
                          sum-list.dinner = sum-list.dinner + cl-list.dinner.
                  END.
                  ELSE DO: /*Naufal - Move from line 1106*/
                      ASSIGN 
                          cl-list.dinner  = ROUND(genstat.res-deci[4],price-decimal)
                          sum-list.dinner = ROUND(sum-list.dinner + cl-list.dinner,price-decimal).
                  END.             
              END.
              ELSE IF artikel.zwkum = lundin-art AND 
                  (artikel.umsatzart = 3 OR artikel.umsatzart GE 5) THEN 
              DO:
                  IF NOT exc-taxserv THEN
                  DO:
                      ASSIGN 
                          cl-list.lunch  = genstat.res-deci[3] * (1 + vat3 + serv2)
                          sum-list.lunch = sum-list.lunch + cl-list.lunch.
                  END.
                  ELSE DO: /*Naufal - Move from line 1106*/
                      ASSIGN 
                          cl-list.lunch  = ROUND(genstat.res-deci[3],price-decimal)
                          sum-list.lunch = ROUND(sum-list.lunch + cl-list.lunch,price-decimal).
                  END.             
              END.
              ELSE 
              DO:
                  IF argt-betrag NE 0 THEN
                  DO:
                      /*Naufal - move to line 550 for bugs fixing case aston madiun*/
                      /*ASSIGN 
                          /*FD Comment 30 Juny, 2021 => if data from argt-line not sequential(bfast, lunch, dinner),
                                                      then Other Rev will discrepancy value
                          cl-list.misc = genstat.rateLocal - (cl-list.lodging + cl-list.bfast + cl-list.lunch + cl-list.dinner).  
                          */            
                          /*FD Sept 20, 2021*/
                          cl-list.misc = genstat.res-deci[5] * (1 + vat3 + serv2)
                          sum-list.misc = sum-list.misc + cl-list.misc.*/
                  END.
                  /*
                  IF cl-list.misc LT 0 AND cl-list.misc GT -1 THEN DO: 
                      cl-list.misc = 0.00.
                  END.*/ /*Naufal - move to line 550 for bugs fixing case aston madiun*/
              END.
          END.
          /*Naufal - Move from line 534 for bugs fixing case aston madiun*/
          IF NOT exc-taxserv THEN
          DO:
              ASSIGN
                  cl-list.misc  = cl-list.localrate - (cl-list.lodging + cl-list.bfast + cl-list.lunch + cl-list.dinner)
                  sum-list.misc = sum-list.misc + cl-list.misc.
          END.
          ELSE DO:
              ASSIGN
                  cl-list.misc  = genstat.res-deci[5]
                  sum-list.misc = sum-list.misc + cl-list.misc.
          END.

          IF cl-list.misc LT 0 AND cl-list.misc GT -1 THEN DO: 
              cl-list.misc = 0.00.
          END.
      END.
     /*end*/ 
      FIND FIRST htparam WHERE htparam.paramnr = 127 NO-LOCK. 
      IF htparam.flogical AND NOT exc-taxserv THEN
          ASSIGN 
              cl-list.zipreis       = ROUND(cl-list.zipreis,price-decimal)
              cl-list.lodging       = ROUND(cl-list.lodging,price-decimal)
              cl-list.bfast         = ROUND(cl-list.bfast,price-decimal)
              cl-list.lunch         = ROUND(cl-list.lunch,price-decimal)
              cl-list.dinner        = ROUND(cl-list.dinner,price-decimal)
              cl-list.misc          = ROUND(cl-list.misc ,price-decimal)
              cl-list.fixcost       = ROUND(cl-list.fixcost,price-decimal)
              cl-list.localrate     = ROUND(cl-list.localrate,price-decimal)
              cl-list.t-rev         = ROUND(cl-list.t-rev,price-decimal).
      
      IF res-line.zimmer-wunsch MATCHES("*$CODE$*") THEN
      DO: 
          s = SUBSTR(res-line.zimmer-wunsch,(INDEX(res-line.zimmer-wunsch,"$CODE$") + 6)).
          cl-list.ratecode = TRIM(ENTRY(1, s, ";")).
      END.
      
      IF frate EQ 1 THEN cl-list.ex-rate = STRING(frate,"   >>9.99"). 
      ELSE IF frate LE 999 THEN cl-list.ex-rate = STRING(frate," >>9.9999"). 
      ELSE IF frate LE 99999 THEN cl-list.ex-rate = STRING(frate,">>,>>9.99"). 
      ELSE cl-list.ex-rate = STRING(frate,">,>>>,>>9"). 
      
      FIND FIRST reslin-queasy WHERE reslin-queasy.key = "arrangement" 
          AND reslin-queasy.resnr = res-line.resnr 
          AND reslin-queasy.reslinnr = res-line.reslinnr 
          AND tdate GE reslin-queasy.date1 
          AND fdate LE reslin-queasy.date2 NO-LOCK NO-ERROR. 
      IF AVAILABLE reslin-queasy THEN ASSIGN cl-list.fix-rate = "F".

      tot-rate = tot-rate + cl-list.zipreis. 
      tot-Lrate = tot-Lrate + cl-list.localrate. 
      IF NOT res-line.adrflag THEN tot-pax = tot-pax + cl-list.pax. 
      ELSE Ltot-pax = Ltot-pax + cl-list.pax. 
      tot-com = tot-com + cl-list.com. 
      /* Add by Michael @ 27/09/2018 for Grand Mirage request - ticket no E0012E */
      tot-adult = tot-adult + cl-list.adult.
      tot-ch1   = tot-ch1   + cl-list.ch1.
      tot-ch2   = tot-ch2   + cl-list.ch2.
      tot-comch = tot-comch + cl-list.comch.
      /* End of add */    
  
      /*FD August 12, 2021 => Validation if double arrangement line*/
      FOR EACH argt-line WHERE argt-line.argtnr = arrangement.argtnr 
          AND NOT argt-line.kind2 AND argt-line.kind1 
          BY argt-line.argtnr BY argt-line.argt-artnr:
                  
          FIND FIRST t-argt-line WHERE t-argt-line.argt-artnr EQ argt-line.argt-artnr
              AND t-argt-line.argtnr EQ arrangement.argtnr
              AND t-argt-line.departement EQ argt-line.departement NO-LOCK NO-ERROR.
          IF NOT AVAILABLE t-argt-line THEN
          DO:
              CREATE t-argt-line.
              BUFFER-COPY argt-line TO t-argt-line.
          END.
      END.

      /*FD February 03, 2021 => New Metode*/
      IF genstat.zipreis NE 0 THEN      
      DO:
          /*FD Jan 17, 2021 => New Method get data s-list just from billjournal*/
          IF bill-flag1 = "Master Bill" THEN
          DO:
              FOR EACH billjournal WHERE billjournal.rechnr EQ bill-master
                  AND billjournal.bill-datum EQ genstat.datum
                  AND billjournal.zinr EQ genstat.zinr
                  AND billjournal.betrag NE 0 /*Naufal 22/09/2022 - change validation from GT 0 to NE 0 for bug fix negative value should be included*/
                  AND billjournal.anzahl NE 0
                  AND NOT billjournal.kassarapport
                  AND billjournal.userinit EQ "$$" NO-LOCK,        
                  FIRST artikel WHERE artikel.artnr EQ billjournal.artnr 
                      AND artikel.departement EQ billjournal.departement
                      AND artikel.artart NE 9 
                  NO-LOCK BY billjournal.sysdate BY billjournal.bill-datum BY billjournal.zinr:                           
                      
                  IF billjournal.artnr NE deposit-art THEN
                  DO: /*MNaufal - add validation for bug fixing deposit articles shouldn't be displayed*/
                      FIND FIRST s-list WHERE s-list.artnr EQ billjournal.artnr 
                          AND s-list.dept EQ billjournal.departement 
                          AND s-list.curr EQ waehrung1.wabkurz NO-LOCK NO-ERROR. 
                      IF NOT AVAILABLE s-list THEN 
                      DO: 
                          CREATE s-list. 
                          ASSIGN 
                              s-list.artnr = billjournal.artnr 
                              s-list.dept = billjournal.departement 
                              s-list.bezeich = billjournal.bezeich 
                              s-list.curr = waehrung1.wabkurz.                     
                      END. 
                      
                      ASSIGN
                          s-list.f-betrag = s-list.f-betrag + billjournal.fremdwaehrng    /*Naufal 200922 - change from billjournal.betrag            */
                          s-list.l-betrag = s-list.l-betrag + billjournal.betrag          /*Naufal 200922 - change from billjournal.betrag * frate    */                 
                      . 
                  END.
              END.  

              bill-master = -1.
          END.
          
          IF bill-flag2 = "Guest Bill" THEN
          DO:
              FOR EACH billjournal WHERE billjournal.rechnr EQ bill-rechnr
                  AND billjournal.bill-datum EQ genstat.datum
                  AND billjournal.zinr EQ genstat.zinr
                  AND billjournal.betrag NE 0 /*Naufal 22/09/2022 - change validation from GT 0 to NE 0 for bug fix negative value should be included*/
                  AND billjournal.anzahl NE 0
                  AND NOT billjournal.kassarapport
                  AND billjournal.userinit EQ "$$" NO-LOCK ,        
                  FIRST artikel WHERE artikel.artnr EQ billjournal.artnr 
                      AND artikel.departement EQ billjournal.departement
                      AND artikel.artart NE 9 
                  NO-LOCK BY billjournal.sysdate BY billjournal.bill-datum BY billjournal.zinr:                           
                    
                  IF billjournal.artnr NE deposit-art THEN
                  DO: /*MNaufal - add validation for bug fixing deposit articles shouldn't be displayed*/
                      FIND FIRST s-list WHERE s-list.artnr EQ billjournal.artnr 
                          AND s-list.dept EQ billjournal.departement 
                          AND s-list.curr EQ waehrung1.wabkurz NO-LOCK NO-ERROR. 
                      IF NOT AVAILABLE s-list THEN 
                      DO: 
                          CREATE s-list. 
                          ASSIGN 
                              s-list.artnr = billjournal.artnr 
                              s-list.dept = billjournal.departement 
                              s-list.bezeich = billjournal.bezeich 
                              s-list.curr = waehrung1.wabkurz.                     
                      END. 
                      
                      ASSIGN
                          s-list.f-betrag = s-list.f-betrag + billjournal.fremdwaehrng    /*Naufal 200922 - change from billjournal.betrag            */
                          s-list.l-betrag = s-list.l-betrag + billjournal.betrag          /*Naufal 200922 - change from billjournal.betrag * frate    */                 
                      . 
                  END.
              END. 

              bill-rechnr = -1.
          END.

        /* FD Comment => move to new method above
        FOR EACH t-argt-line WHERE t-argt-line.argtnr = arrangement.argtnr 
          AND NOT t-argt-line.kind2 AND t-argt-line.kind1 NO-LOCK:
          /*FIRST*/ FOR EACH billjournal WHERE billjournal.artnr = t-argt-line.argt-artnr
            AND billjournal.departement = t-argt-line.departement           
            /*AND billjournal.rechnr = bill-rechnr*/
            AND billjournal.bill-datum = genstat.datum 
            AND billjournal.zinr = genstat.zinr NO-LOCK: /*FD Jan 05, 2022*/
            
            /*RUN calc-servtaxesbl.p (1, billjournal.artnr, billjournal.departement,
              billjournal.bill-datum, OUTPUT serv-1, OUTPUT vat-1, OUTPUT vat2,
              OUTPUT fact-1).*/

            FIND FIRST s-list WHERE s-list.artnr = billjournal.artnr 
              AND s-list.dept = billjournal.departement 
              AND s-list.curr = waehrung.wabkurz NO-LOCK NO-ERROR. 
            IF NOT AVAILABLE s-list THEN 
            DO: 
              CREATE s-list. 
              ASSIGN 
                s-list.artnr = billjournal.artnr 
                s-list.dept = billjournal.departement 
                s-list.bezeich = billjournal.bezeich 
                s-list.curr = waehrung.wabkurz.            
            END.     

            /*IF exc-taxserv THEN
            DO:              
              ASSIGN
                s-list.f-betrag = ROUND ((s-list.f-betrag + billjournal.betrag / (1 + vat-1 + vat-2 + serv-1)),price-decimal)
                s-list.l-betrag = ROUND ((s-list.l-betrag + billjournal.betrag * frate / (1 + vat-1 + vat-2 + serv-1)),price-decimal)
              .
            END.
            ELSE*/

            
            ASSIGN
              s-list.f-betrag = s-list.f-betrag + billjournal.betrag 
              s-list.l-betrag = s-list.l-betrag + billjournal.betrag * frate                 
            .                      
          END.
        END.
        */
      END.

      /* Comment FD - Wrong Lodging Value
      ASSIGN 
          cl-list.lodging = genstat.zipreis - (cl-list.bfast + cl-list.lunch + cl-list.dinner + cl-list.misc).
      */

      IF res-line.adrflag THEN Ltot-lodging = Ltot-lodging + cl-list.lodging. 
      ELSE tot-lodging = tot-lodging + cl-list.lodging. 
  
      lodge-betrag = cl-list.lodging /*FT 230614* frate*/ . 
      IF foreign-rate AND price-decimal = 0 AND NOT res-line.adrflag THEN 
      DO: 
        FIND FIRST htparam WHERE paramnr = 145 NO-LOCK. 
        IF htparam.finteger NE 0 THEN 
        DO: 
          DEFINE VARIABLE j AS INTEGER. 
          DEFINE VARIABLE m AS INTEGER. 
          m = 1. 
          DO j = 1 TO finteger: 
            m = m * 10. 
          END. 
          lodge-betrag = ROUND(lodge-betrag / n, 0) * n. 
        END. 
      END. 
  
      /* FD Comment => move to new method above
      FIND FIRST artikel1 WHERE artikel1.artnr = arrangement.artnr-logis 
        AND artikel1.departement = 0 NO-LOCK NO-ERROR. 
      IF AVAILABLE artikel1 THEN
      DO:
        FIND FIRST s-list WHERE s-list.artnr = artikel1.artnr 
          AND s-list.dept = artikel1.departement 
          AND s-list.curr = waehrung1.wabkurz NO-LOCK NO-ERROR. 
        IF NOT AVAILABLE s-list THEN 
        DO: 
          create s-list. 
          ASSIGN 
            s-list.artnr = artikel1.artnr 
            s-list.dept = artikel1.departement 
            s-list.bezeich = artikel1.bezeich 
            s-list.curr = waehrung1.wabkurz. 
        END.       
        
        /*FD February 03, 2021 => New Metode for exclude tax service
        IF exc-taxserv THEN
        DO:
          ASSIGN 
            s-list.f-betrag = ROUND((s-list.f-betrag + lodge-betrag / frate / (1 + vat1 + vat2 + serv1)),price-decimal)
            s-list.l-betrag = ROUND((s-list.l-betrag + lodge-betrag / (1 + vat1 + vat2 + serv1)),price-decimal)        
            s-list.anzahl = s-list.anzahl + 1. 
            sum-list.lodging = sum-list.lodging + lodge-betrag. 
            sum-list.t-rev = sum-list.t-rev + lodge-betrag
          . 
        END.
        ELSE*/
        DO:
          ASSIGN 
            s-list.f-betrag = s-list.f-betrag + lodge-betrag / frate 
            s-list.l-betrag = s-list.l-betrag + lodge-betrag 
            s-list.anzahl = s-list.anzahl + 1. 
            /*sum-list.lodging = sum-list.lodging + lodge-betrag. 
            sum-list.t-rev = sum-list.t-rev + lodge-betrag*/
          . 
        END.
        /*End FD*/
      END.
      */

      /* FD Comment => move to new method above
      /*FD February 03, 2021 => New Metode for exclude tax service*/
      FOR EACH fixleist WHERE fixleist.resnr = res-line.resnr 
        AND fixleist.reslinnr = res-line.reslinnr NO-LOCK: 
        RUN check-fixleist-posted(fixleist.artnr, fixleist.departement, 
          fixleist.sequenz, fixleist.dekade, 
          fixleist.lfakt, OUTPUT post-it). 
        /*IF NOT post-it THEN DISP fixleist.artnr fixleist.departement fixleist.sequenz fixleist.dekade fixleist.lfakt fixleist.betrag.*/
        IF post-it THEN 
        DO: 
          /*RUN calc-servtaxesbl.p (1, fixleist.artnr, fixleist.departement,
              genstat.datum, OUTPUT serv-2, OUTPUT vat-3, OUTPUT vat-4,
              OUTPUT fact-2).*/

          ASSIGN
            fcost = fixleist.betrag * fixleist.number
            /**/cl-list.t-rev = cl-list.t-rev + fcost
            sum-list.t-rev = sum-list.t-rev + fcost * frate
          . 

          IF res-line.adrflag THEN Ltot-rate = Ltot-rate + fcost. 
          ELSE tot-rate = tot-rate + fcost. 
          
          FIND FIRST artikel WHERE artikel.artnr = fixleist.artnr 
            AND artikel.departement = fixleist.departement NO-LOCK NO-ERROR.
        
          FIND FIRST s-list WHERE s-list.artnr = artikel.artnr 
            AND s-list.dept = artikel.departement 
            AND s-list.curr = waehrung1.wabkurz NO-LOCK NO-ERROR. 
          IF NOT AVAILABLE s-list THEN 
          DO: 
            CREATE s-list. 
            ASSIGN 
              s-list.artnr = artikel.artnr 
              s-list.dept = artikel.departement 
              s-list.bezeich = artikel.bezeich 
              s-list.curr = waehrung1.wabkurz. 
          END. 
        
          IF (artikel.zwkum = bfast-art AND artikel.departement = fb-dept) THEN
          DO:
            /*IF exc-taxserv THEN
            DO:
              ASSIGN 
                s-list.f-betrag = ROUND((s-list.f-betrag + fcost / (1 + vat-3 + vat-4 + serv-2)),price-decimal)
                s-list.l-betrag = ROUND((s-list.l-betrag + fcost * frate / (1 + vat-3 + vat-4 + serv-2)),price-decimal)             
                s-list.anzahl   = s-list.anzahl + fixleist.number
              .  
            END.
            ELSE*/
            DO:
              ASSIGN 
                s-list.f-betrag = s-list.f-betrag + fcost
                s-list.l-betrag = s-list.l-betrag + fcost * frate 
                s-list.anzahl   = s-list.anzahl + fixleist.number
                /* cl-list.bfast   = cl-list.bfast + fcost
                sum-list.bfast  = sum-list.bfast + fcost * frate*/
              .  
            END.                              
            IF res-line.adrflag THEN Ltot-bfast = Ltot-bfast + fcost * frate. 
            ELSE tot-bfast = tot-bfast + fcost. 
          END.
          ELSE IF (artikel.zwkum = lunch-art AND artikel.departement = fb-dept) THEN
          DO:
            /*IF exc-taxserv THEN
            DO:
              ASSIGN 
                s-list.f-betrag = ROUND((s-list.f-betrag + fcost / (1 + vat-3 + vat-4 + serv-2)),price-decimal)
                s-list.l-betrag = ROUND((s-list.l-betrag + fcost * frate / (1 + vat-3 + vat-4 + serv-2)),price-decimal)             
                s-list.anzahl   = s-list.anzahl + fixleist.number
              .  
            END.
            ELSE*/
            DO:
              ASSIGN 
                s-list.f-betrag = s-list.f-betrag + fcost
                s-list.l-betrag = s-list.l-betrag + fcost * frate 
                s-list.anzahl   = s-list.anzahl + fixleist.number
                /*cl-list.lunch   = cl-list.lunch + fcost
                sum-list.lunch  = sum-list.lunch + fcost * frate*/
              .  
            END. 
            IF res-line.adrflag THEN Ltot-lunch = Ltot-lunch + fcost * frate. 
            ELSE tot-lunch = tot-lunch + fcost. 
          END.
          ELSE IF (artikel.zwkum = dinner-art AND artikel.departement = fb-dept) THEN
          DO:
            /*IF exc-taxserv THEN
            DO:
              ASSIGN 
                s-list.f-betrag = ROUND((s-list.f-betrag + fcost / (1 + vat-3 + vat-4 + serv-2)),price-decimal)
                s-list.l-betrag = ROUND((s-list.l-betrag + fcost * frate / (1 + vat-3 + vat-4 + serv-2)),price-decimal)             
                s-list.anzahl   = s-list.anzahl + fixleist.number
              .  
            END.
            ELSE*/
            DO:
              ASSIGN 
                s-list.f-betrag = s-list.f-betrag + fcost
                s-list.l-betrag = s-list.l-betrag + fcost * frate 
                s-list.anzahl   = s-list.anzahl + fixleist.number
                /*cl-list.dinner  = cl-list.dinner + fcost
                sum-list.dinner = sum-list.dinner + fcost * frate*/
              .  
            END. 
            IF res-line.adrflag THEN Ltot-dinner = Ltot-dinner + fcost * frate. 
            ELSE tot-dinner = tot-dinner + fcost. 
          END.
          ELSE
          DO:
          /*IF exc-taxserv THEN
            DO:
              ASSIGN 
                s-list.f-betrag = ROUND((s-list.f-betrag + fcost / (1 + vat-3 + vat-4 + serv-2)),price-decimal)
                s-list.l-betrag = ROUND((s-list.l-betrag + fcost * frate / (1 + vat-3 + vat-4 + serv-2)),price-decimal)             
                s-list.anzahl   = s-list.anzahl + fixleist.number
              .  
            END.
            ELSE*/
            DO:
              ASSIGN 
                s-list.f-betrag = s-list.f-betrag + fcost
                s-list.l-betrag = s-list.l-betrag + fcost * frate 
                s-list.anzahl   = s-list.anzahl + fixleist.number
                /*cl-list.fixcost = cl-list.fixcost + fcost
                sum-list.fixcost = sum-list.fixcost + fcost * frate*/
              .  
            END. 
            IF res-line.adrflag THEN Ltot-fix = Ltot-fix + fcost. 
            ELSE tot-fix = tot-fix + fcost.  
          END.
        END. 
      END.
      /*End FD*/
      */

      IF curr-zinr NE res-line.zinr OR curr-resnr NE res-line.resnr THEN 
      DO: 
        IF res-line.adrflag THEN Ltot-rm = Ltot-rm + 1. 
        ELSE tot-rm = tot-rm + 1. 
      END. 
      curr-zinr = res-line.zinr. 
      curr-resnr = res-line.resnr. 
    END. 
  END.

  /* end by damen */

  create cl-list. 
  ASSIGN 
    cl-list.flag = "*"
    cl-list.zinr = ""
    cl-list.c-zipreis = "S U M M A R Y:".
 
  DEFINE VARIABLE curr-code     AS CHAR. 
  DEFINE VARIABLE curr-rate     AS DECIMAL. 
  DEFINE VARIABLE curr-local    AS DECIMAL. 
  DEFINE VARIABLE curr-bfast    AS DECIMAL. 
  DEFINE VARIABLE curr-lodge    AS DECIMAL. 
  DEFINE VARIABLE curr-lunch    AS DECIMAL. 
  DEFINE VARIABLE curr-dinner   AS DECIMAL. 
  DEFINE VARIABLE curr-misc     AS DECIMAL. 
  DEFINE VARIABLE curr-fcost    AS DECIMAL. 
  DEFINE VARIABLE curr-trev     AS DECIMAL. 
  DEFINE VARIABLE curr-pax      AS INTEGER. 
  DEFINE VARIABLE curr-com      AS INTEGER. 
  DEFINE VARIABLE curr-rm       AS INTEGER. 
  /* Add by Michael @ 27/09/2018 for Grand Mirage request - ticket no E0012E */
  DEFINE VARIABLE curr-adult    AS INTEGER. 
  DEFINE VARIABLE curr-ch1      AS INTEGER. 
  DEFINE VARIABLE curr-ch2      AS INTEGER. 
  DEFINE VARIABLE curr-comch    AS INTEGER. 
  /* End of add */
 
  curr-code = "". 
  curr-rate = 0. 
  curr-local = 0. 
  curr-lodge = 0. 
  curr-bfast = 0. 
  curr-lunch = 0. 
  curr-dinner = 0. 
  curr-misc = 0. 
  curr-fcost = 0. 
  curr-trev = 0. 
  curr-pax = 0. 
  curr-com = 0. 
  curr-rm = 0. 
  /* Add by Michael @ 27/09/2018 for Grand Mirage request - ticket no E0012E */
  curr-adult = 0. 
  curr-ch1   = 0. 
  curr-ch2   = 0. 
  curr-comch = 0. 
  /* End of add */
  FOR EACH cc-list WHERE cc-list.flag = "" BY cc-list.currency: 
    IF curr-code NE cc-list.currency THEN 
    DO: 
      IF curr-code NE "" THEN 
      DO: 
        cl-list.zipreis = curr-rate. 
        cl-list.localrate = curr-local. 
        cl-list.lodging = curr-lodge. 
        cl-list.bfast = curr-bfast. 
        cl-list.lunch = curr-lunch. 
        cl-list.dinner = curr-dinner. 
        cl-list.misc = curr-misc. 
        cl-list.fixcost = curr-fcost. 
        cl-list.t-rev = curr-trev. 
        cl-list.pax = curr-pax. 
        cl-list.com = curr-com. 
        cl-list.zinr = STRING(curr-rm, ">>>9"). 
        /* Add by Michael @ 27/09/2018 for Grand Mirage request - ticket no E0012E */
        cl-list.adult = curr-adult. 
        cl-list.ch1   = curr-ch1. 
        cl-list.ch2   = curr-ch2. 
        cl-list.comch = curr-comch. 
        /* End of add */
      END. 
      FIND FIRST waehrung WHERE waehrung.wabkurz = cc-list.currency NO-LOCK NO-ERROR. 
      IF (waehrung.ankauf / waehrung.einheit) NE 1 THEN 
      DO: 
        create currency-list. 
        currency-list.code = cc-list.currency. 
      END. 
      create cl-list. 
      cl-list.flag = "**". 
      cl-list.currency = cc-list.currency. 
      curr-code = cc-list.currency. 
      curr-rate = 0. 
      curr-local = 0. 
      curr-lodge = 0. 
      curr-bfast = 0. 
      curr-lunch = 0. 
      curr-dinner = 0. 
      curr-misc = 0. 
      curr-fcost = 0. 
      curr-trev = 0. 
      curr-pax = 0. 
      curr-com = 0. 
      curr-rm = 0. 
      /* Add by Michael @ 27/09/2018 for Grand Mirage request - ticket no E0012E */
      curr-adult = 0. 
      curr-ch1   = 0. 
      curr-ch2   = 0. 
      curr-comch = 0. 
      /* End of add */
    END. 
    curr-rate = curr-rate + cc-list.zipreis. 
    curr-local = curr-local + cc-list.localrate. 
    curr-lodge = curr-lodge + cc-list.lodging. 
    curr-bfast = curr-bfast + cc-list.bfast. 
    curr-lunch = curr-lunch + cc-list.lunch. 
    curr-dinner = curr-dinner + cc-list.dinner. 
    curr-misc = curr-misc + cc-list.misc. 
    curr-fcost = curr-fcost + cc-list.fixcost. 
    curr-trev = curr-trev + cc-list.t-rev. 
    curr-pax = curr-pax + cc-list.pax. 
    curr-com = curr-com + cc-list.com. 
    /* Add by Michael @ 27/09/2018 for Grand Mirage request - ticket no E0012E */
    curr-adult = curr-adult + cc-list.adult. 
    curr-ch1   = curr-ch1 + cc-list.ch1. 
    curr-ch2   = curr-ch2 + cc-list.ch2. 
    curr-comch = curr-comch + cc-list.comch. 
    /* End of add */
    IF cc-list.rstatus NE 13 THEN curr-rm = curr-rm + 1. 
  END. 
  cl-list.zipreis = curr-rate. 
  cl-list.localrate = curr-local. 
  cl-list.lodging = curr-lodge. 
  cl-list.bfast = curr-bfast. 
  cl-list.lunch = curr-lunch. 
  cl-list.dinner = curr-dinner. 
  cl-list.misc = curr-misc. 
  cl-list.fixcost = curr-fcost. 
  cl-list.t-rev = curr-trev. 
  cl-list.pax = curr-pax. 
  cl-list.com = curr-com. 
  cl-list.zinr = STRING(curr-rm,">>>9"). 
  /* Add by Michael @ 27/09/2018 for Grand Mirage request - ticket no E0012E */
  cl-list.adult = curr-adult. 
  cl-list.ch1   = curr-ch1. 
  cl-list.ch2   = curr-ch2. 
  cl-list.comch = curr-comch. 
  /* End of add */
 
  FOR EACH cl-list WHERE cl-list.flag NE "*":
      /* Naufal - Move to line 353 for bugs fixing descripancy data tax & exc-tax
    IF exc-taxserv THEN DO:
        ASSIGN
            cl-list.zipreis     = ROUND (( cl-list.zipreis / (1 + vat1 + vat2 + serv1)),price-decimal)
            cl-list.localrate   = ROUND ((cl-list.localrate / (1 + vat1 + vat2 + serv1)),price-decimal)
            cl-list.lodging     = ROUND ((cl-list.lodging / (1 + vat1 + vat2 + serv1)),price-decimal)
            cl-list.bfast       = ROUND ((cl-list.bfast  / (1 + vat1 + vat2 + serv1)),price-decimal)
            cl-list.lunch       = ROUND ((cl-list.lunch  / (1 + vat1 + vat2 + serv1)),price-decimal)
            cl-list.dinner      = ROUND ((cl-list.dinner  / (1 + vat1 + vat2 + serv1)),price-decimal)
            cl-list.misc        = ROUND ((cl-list.misc  / (1 + vat1 + vat2 + serv1)),price-decimal)
            cl-list.fixcost     = ROUND ((cl-list.fixcost  / (1 + vat1 + vat2 + serv1)),price-decimal)
            cl-list.t-rev       = ROUND ((cl-list.t-rev / (1 + vat1 + vat2 + serv1)),price-decimal).
			/*cl-list.zipreis     = ROUND (( cl-list.zipreis / (1 + vat1 + service1)),price-decimal)
            cl-list.localrate   = ROUND ((cl-list.localrate / (1 + vat1 + service1)),price-decimal)
            cl-list.lodging     = ROUND ((cl-list.lodging / (1 + vat1 + service1)),price-decimal)
            cl-list.bfast       = ROUND ((cl-list.bfast  / (1 + vat1 + service1)),price-decimal)
            cl-list.lunch       = ROUND ((cl-list.lunch  / (1 + vat1 + service1)),price-decimal)
            cl-list.dinner      = ROUND ((cl-list.dinner  / (1 + vat1 + service1)),price-decimal)
            cl-list.misc        = ROUND ((cl-list.misc  / (1 + vat1 + service1)),price-decimal)
            cl-list.fixcost     = ROUND ((cl-list.fixcost  / (1 + vat1 + service1)),price-decimal)
            cl-list.t-rev       = ROUND ((cl-list.t-rev / (1 + vat1 + service1)),price-decimal).*/
		
	END. */

    IF cl-list.lodging LT 0 THEN cl-list.c-lodging = STRING(cl-list.lodging,"->>,>>>,>>>,>>9.99"). 
    ELSE cl-list.c-lodging = STRING(cl-list.lodging,">>>,>>>,>>>,>>9.99"). 
    ASSIGN 
        cl-list.c-zipreis       = STRING(cl-list.zipreis,">>>,>>>,>>>,>>9.99")
        cl-list.c-localrate     = STRING(cl-list.localrate,">>>,>>>,>>>,>>9.99") 
        cl-list.c-bfast         = STRING(cl-list.bfast,"->,>>>,>>>,>>9.99") 
        cl-list.c-lunch         = STRING(cl-list.lunch,"->,>>>,>>>,>>9.99") 
        cl-list.c-dinner        = STRING(cl-list.dinner,"->,>>>,>>>,>>9.99") 
        cl-list.c-misc          = STRING(cl-list.misc,"->,>>>,>>>,>>9.99")
        cl-list.c-fixcost       = STRING(cl-list.fixcost,"->>>,>>>,>>9.99") 
        cl-list.ct-rev          = STRING(cl-list.t-rev,">>>,>>>,>>>,>>9.99"). 

    /*FD January 18, 2021 => Chanti SMG*/
    FIND FIRST argt-list WHERE argt-list.argtcode = cl-list.argt NO-LOCK NO-ERROR.
    IF AVAILABLE argt-list THEN
    DO:                
        argt-list.bfast = argt-list.bfast + cl-list.bfast.
    END.
  END. 
 
  /*FD April 05, 2021*/
  IF exc-taxserv THEN 
  DO:
    FOR EACH s-list:
         s-list.f-betrag = ROUND((s-list.f-betrag / (1 + vat1 + vat2 + serv1)),price-decimal).
         s-list.l-betrag = ROUND((s-list.l-betrag / (1 + vat1 + vat2 + serv1)),price-decimal).        
    END.

    FOR EACH sum-list:
        ASSIGN
            sum-list.lodging = ROUND((sum-list.lodging / (1 + vat1 + vat2 + serv1)),price-decimal)
            sum-list.bfast   = ROUND((sum-list.bfast   / (1 + vat1 + vat2 + serv1)),price-decimal)
            sum-list.lunch   = ROUND((sum-list.lunch   / (1 + vat1 + vat2 + serv1)),price-decimal)
            sum-list.dinner  = ROUND((sum-list.dinner  / (1 + vat1 + vat2 + serv1)),price-decimal)
            sum-list.misc    = ROUND((sum-list.misc    / (1 + vat1 + vat2 + serv1)),price-decimal)
            sum-list.fixcost = ROUND((sum-list.fixcost / (1 + vat1 + vat2 + serv1)),price-decimal)
            sum-list.t-rev   = ROUND((sum-list.t-rev   / (1 + vat1 + vat2 + serv1)),price-decimal)
        .
    END.
  END.
  total-rev = tot-rate.  
 
END. 

PROCEDURE get-argtline-rate: 
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
 
  FIND FIRST argtline WHERE RECID(argtline) = argt-recid NO-LOCK NO-ERROR. 
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
      IF (res-line.ankunft EQ genstat.datum) THEN add-it = YES. 
    END. 
    ELSE IF argtline.fakt-modus = 3 THEN 
    DO: 
      IF (res-line.ankunft + 1) EQ genstat.datum THEN add-it = YES. 
    END. 
    ELSE IF argtline.fakt-modus = 4 
      AND (DAY(genstat.datum) EQ 1) THEN add-it = YES. 
    ELSE IF argtline.fakt-modus = 5 
      AND (DAY(genstat.datum + 1) EQ 1) THEN add-it = YES. 
    ELSE IF argtline.fakt-modus = 6 THEN 
    DO: 
      IF (res-line.ankunft + (argtline.intervall - 1)) GE genstat.datum 
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
        AND tdate GE reslin-queasy.date1 
        AND fdate LE reslin-queasy.date2 
        USE-INDEX argt1_ix NO-LOCK NO-ERROR. 
    IF AVAILABLE reslin-queasy THEN 
    DO: 
      /*argt-betrag = reslin-queasy.deci1 * qty. */
      /*FDL May 24, 2023 => Ticket 803CE8*/
      IF reslin-queasy.char2 NE ""
          AND reslin-queasy.char2 NE "0" THEN argt-betrag = (res-line.zipreis * INT(reslin-queasy.char2) / 100) * qty.
      ELSE argt-betrag = reslin-queasy.deci1 * qty.

      f-betrag = argt-betrag. 
      FIND FIRST waehrung WHERE RECID(waehrung) = RECID(waehrung1) NO-LOCK NO-ERROR. 
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
        AND tdate GE reslin-queasy.date1 
        AND fdate LE reslin-queasy.date2 NO-LOCK NO-ERROR. 
      IF AVAILABLE reslin-queasy THEN 
      DO: 
        argt-betrag = reslin-queasy.deci1 * qty. 
        f-betrag = argt-betrag. 
        FIND FIRST waehrung WHERE RECID(waehrung) = RECID(waehrung1) NO-LOCK NO-ERROR. 
        IF argt-betrag = 0 THEN add-it = NO. 
        RETURN. 
      END. 
    END. 
    argt-betrag = argt-line.betrag. 
    FIND FIRST arrangement WHERE arrangement.argtnr = argt-line.argtnr 
      NO-LOCK NO-ERROR. 

	FIND FIRST waehrung WHERE waehrung.waehrungsnr = arrangement.betriebsnr 
      NO-LOCK NO-ERROR. 
	  
    f-betrag = argt-betrag * qty. 
    IF res-line.betriebsnr NE arrangement.betriebsnr THEN
      argt-betrag = argt-betrag * (waehrung.ankauf / waehrung.einheit) / frate. 
    argt-betrag = argt-betrag * qty. 
    IF argt-betrag = 0 THEN add-it = NO. 

  END.
END. 

PROCEDURE get-genstat-argt-betrag:
DEF INPUT        PARAMETER frate       AS DECIMAL.
DEF INPUT-OUTPUT PARAMETER argt-betrag AS DECIMAL.
DEF VARIABLE tokcounter AS INTEGER  NO-UNDO.
DEF VARIABLE mesToken   AS CHAR     NO-UNDO.
DEF VARIABLE curr-artnr AS INTEGER  NO-UNDO.
DEF VARIABLE curr-dept  AS INTEGER  NO-UNDO.
DEF VARIABLE a-betrag   AS DECIMAL  NO-UNDO.
DEF VARIABLE x-betrag   AS DECIMAL  NO-UNDO.
  
IF genstat.res-char[4] = "" THEN RETURN.
  DO tokcounter = 1 TO NUM-ENTRIES(genstat.res-char[4], ";"):
    mesToken = TRIM(ENTRY(tokcounter, genstat.res-char[4], ";")).
    IF mesToken NE "" THEN
    DO:
      ASSIGN
        curr-artnr = INTEGER(ENTRY(1, mesToken, ","))
        curr-dept  = INTEGER(ENTRY(2, mesToken, ","))
        a-betrag   = DECIMAL(ENTRY(3, mesToken, ",")) * 0.01
        x-betrag   = DECIMAL(ENTRY(4, mesToken, ",")) * 0.01
      .
      IF curr-artnr = argt-line.argt-artnr 
        AND curr-dept = argt-line.departement THEN
      DO:
        ASSIGN argt-betrag = a-betrag * x-betrag / frate.
        RETURN.
      END.
    END.
  END.
END.


PROCEDURE check-fixleist-posted: 
DEFINE INPUT PARAMETER artnr AS INTEGER. 
DEFINE INPUT PARAMETER dept AS INTEGER. 
DEFINE INPUT PARAMETER fakt-modus AS INTEGER. 
DEFINE INPUT PARAMETER intervall AS INTEGER. 
DEFINE INPUT PARAMETER lfakt AS DATE. 
DEFINE OUTPUT PARAMETER post-it AS LOGICAL INITIAL NO. 
DEFINE VARIABLE delta AS INTEGER. 
DEFINE VARIABLE start-date AS DATE. 
 
/*MESSAGE post-it fixleist.artnr fixleist.departement fixleist.sequenz fixleist.dekade fixleist.lfakt fixleist.betrag VIEW-AS ALERT-BOX INFO.*/
  IF fakt-modus = 1 THEN post-it = YES. 
  ELSE IF fakt-modus = 2 THEN 
  DO: 
    IF (res-line.ankunft EQ genstat.datum) THEN post-it = YES. 
  END. 
  ELSE IF fakt-modus = 3 THEN 
  DO: 
    IF ((res-line.ankunft + 1) EQ genstat.datum) THEN post-it = YES. 
  END. 
  ELSE IF fakt-modus = 4 THEN   /* 1st day OF month  */ 
  DO: 
    IF (DAY(genstat.datum) EQ 1) THEN post-it = YES. 
  END. 
  ELSE IF fakt-modus = 5 THEN   /* LAST day OF month */ 
  DO: 
    IF (DAY(genstat.datum + 1) EQ 1) THEN post-it = YES. 
  END. 
  ELSE IF fakt-modus = 6 THEN 
  DO: 
    IF lfakt = ? THEN delta = 0. 
    ELSE 
    DO: 
      delta = lfakt - res-line.ankunft. 
      IF delta LT 0 THEN delta = 0. 
    END. 
    start-date = res-line.ankunft + delta. 
    IF (res-line.abreise - start-date) LT intervall 
      THEN start-date = res-line.ankunft. 
    IF tdate LE (start-date + (intervall - 1)) 
    THEN post-it = YES. 
    IF tdate LT start-date THEN post-it = no. /* may NOT post !! */ 
  END. 
END. 

