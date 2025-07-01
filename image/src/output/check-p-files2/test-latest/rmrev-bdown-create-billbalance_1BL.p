

DEFINE TEMP-TABLE sum-list 
  FIELD bezeich    AS CHAR FORMAT "x(27)" INITIAL "In Local Currency" 
  FIELD pax        AS INTEGER FORMAT ">>9" 
  /* Add by Michael @ 27/09/2018 for Grand Mirage request - ticket no E0012E */
  FIELD adult      AS INTEGER   FORMAT ">>9" 
  FIELD ch1        AS INTEGER   FORMAT ">>9" 
  FIELD ch2        AS INTEGER   FORMAT ">>9" 
  FIELD comch      AS INTEGER   FORMAT ">>9" 
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
 
  FIELD c-zipreis    AS CHAR FORMAT "x(18)" LABEL "        Room Rate" 
  FIELD c-localrate  AS CHAR FORMAT "x(18)" LABEL "   Local Currency" 
  FIELD c-lodging    AS CHAR FORMAT "x(18)" LABEL "          Lodging" 
  FIELD c-bfast      AS CHAR FORMAT "x(17)" LABEL "       Breakfast" 
  FIELD c-lunch      AS CHAR FORMAT "x(17)" LABEL "           Lunch" 
  FIELD c-dinner     AS CHAR FORMAT "x(17)" LABEL "          Dinner" 
  FIELD c-misc       AS CHAR FORMAT "x(17)" LABEL "       Other Rev" 
  FIELD c-fixcost    AS CHAR FORMAT "x(15)" LABEL "       FixCost"   
  FIELD ct-rev       AS CHAR FORMAT "x(18)" LABEL "       Total Rate" 
 
  FIELD res-recid  AS INTEGER 
  FIELD sleeping   AS LOGICAL INITIAL YES 
  FIELD row-disp   AS INTEGER INITIAL 0 
  FIELD flag       AS CHAR 
  FIELD zinr       LIKE zimmer.zinr 
  FIELD rstatus    AS INTEGER 
  FIELD argt       AS CHAR FORMAT "x(5)" COLUMN-LABEL "Argt" 
  FIELD currency   AS CHAR FORMAT "x(4)" COLUMN-LABEL "Curr" 
  FIELD ratecode   AS CHAR FORMAT "x(4)" COLUMN-LABEL "RCode"
  FIELD pax        AS INTEGER FORMAT ">>,>>>" INITIAL 0 COLUMN-LABEL "Pax" 
  FIELD com        AS INTEGER FORMAT ">>,>>>" INITIAL 0 COLUMN-LABEL "Com" 
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
  FIELD age1       AS INTEGER INITIAL 0     COLUMN-LABEL "Age"
  FIELD age2       AS CHAR FORMAT "x(10)"   COLUMN-LABEL "Age"
  /* End of add */
  /*MNaufal - 170322 - for Ramada Solo request DFDC33*/
  FIELD rmtype     AS CHAR FORMAT "x(6)"    COLUMN-LABEL "RmType"
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

DEF INPUT PARAMETER exc-taxserv   AS LOGICAL NO-UNDO.
DEF INPUT  PARAMETER pvILanguage    AS INTEGER  NO-UNDO.
DEF INPUT  PARAMETER new-contrate   AS LOGICAL.
DEF INPUT  PARAMETER foreign-rate   AS LOGICAL.
DEF INPUT  PARAMETER price-decimal  AS INT.
DEF INPUT  PARAMETER curr-date      AS DATE. 
DEF OUTPUT PARAMETER msg-str        AS CHAR.
DEF OUTPUT PARAMETER msg-warning    AS CHAR.
DEF OUTPUT PARAMETER TABLE FOR cl-list.
DEF OUTPUT PARAMETER TABLE FOR currency-list.
DEF OUTPUT PARAMETER TABLE FOR sum-list.
DEF OUTPUT PARAMETER TABLE FOR s-list.

DEFINE BUFFER waehrung1 FOR waehrung. 
DEFINE BUFFER cc-list FOR cl-list. 

DEFINE VARIABLE exchg-rate          AS DECIMAL INITIAL 1. 
DEFINE VARIABLE frate               AS DECIMAL FORMAT ">,>>>,>>9.9999". 
DEFINE VARIABLE post-it             AS LOGICAL. 
DEFINE VARIABLE total-rev           AS DECIMAL. 
DEFINE VARIABLE rm-rate             AS DECIMAL.

{SupertransBL.i} 
DEF VAR lvCAREA AS CHAR INITIAL "rmrev-bdown".

CREATE sum-list.
RUN create-billbalance.

PROCEDURE create-billbalance: 
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

  DEFINE VARIABLE vat                     AS DECIMAL.
  DEFINE VARIABLE service                 AS DECIMAL.

  /*add*/
  DEFINE VARIABLE serv                    AS DECIMAL.
  DEFINE VARIABLE vat2                    AS DECIMAL.
  DEFINE VARIABLE fact                    AS DECIMAL.
  DEFINE VARIABLE curr-zikatnr AS INTEGER NO-UNDO. 
  DEFINE BUFFER artikel1 FOR artikel. 
 
  FIND FIRST htparam WHERE paramnr = 125 NO-LOCK. 
  bfast-art = htparam.finteger.               /* Rulita 211024 | Fixing for serverless */  
  FIND FIRST htparam WHERE paramnr = 126 NO-LOCK. 
  fb-dept = htparam.finteger.               /* Rulita 211024 | Fixing for serverless */  
 
  FIND FIRST artikel WHERE artikel.zwkum = bfast-art 
    AND artikel.departement = fb-dept /*GE 1*/ NO-LOCK NO-ERROR. 
  IF NOT AVAILABLE artikel AND bfast-art NE 0 THEN 
  DO: 
    msg-str = translateExtended ("B'fast SubGrp not yed defined (Grp 7)",lvCAREA,"").
    RETURN. 
  END. 
 
  FIND FIRST htparam WHERE paramnr = 227 NO-LOCK. 
  lunch-art = htparam.finteger.               /* Rulita 211024 | Fixing for serverless */  
  FIND FIRST artikel WHERE artikel.zwkum = lunch-art 
    AND artikel.departement = fb-dept /*GE 1*/ NO-LOCK NO-ERROR. 
  IF NOT AVAILABLE artikel AND lunch-art NE 0 THEN 
  DO: 
    msg-str = translateExtended ("Lunch SubGrp not yed defined (Grp 7)",lvCAREA,"").
    RETURN. 
  END. 
 
  FIND FIRST htparam WHERE paramnr = 228 NO-LOCK. 
  dinner-art = htparam.finteger.               /* Rulita 211024 | Fixing for serverless */  
  FIND FIRST artikel WHERE artikel.zwkum = dinner-art 
    AND artikel.departement = fb-dept /*GE 1*/ NO-LOCK NO-ERROR. 
  IF NOT AVAILABLE artikel AND dinner-art NE 0 THEN 
  DO: 
    msg-str = translateExtended ("Dinner SubGrp not yed defined (Grp 7)",lvCAREA,"").
    RETURN. 
  END. 
 
  FIND FIRST htparam WHERE paramnr = 229 NO-LOCK. 
  lundin-art = htparam.finteger.               /* Rulita 211024 | Fixing for serverless */  
  FIND FIRST artikel WHERE artikel.zwkum = lundin-art 
    AND artikel.departement = fb-dept /*GE 1*/ NO-LOCK NO-ERROR. 
  IF NOT AVAILABLE artikel AND lundin-art NE 0 THEN 
  DO: 
    msg-str = translateExtended ("HalfBoard SubGrp not yed defined (Grp 7)",lvCAREA,"").
    RETURN. 
  END. 
 
  FOR EACH s-list: 
    DELETE s-list. 
  END. 
  FOR EACH cl-list: 
    DELETE cl-list. 
  END. 
  FOR EACH currency-list: 
    DELETE currency-list. 
  END. 
 
  IF AVAILABLE sum-list THEN DELETE sum-list. 
  CREATE sum-list. 
 
  r-qty = 0. 
  lodge-betrag = 0. 
  FOR EACH res-line 
    /*WHERE (res-line.active-flag = 1 AND resstatus NE 12 )*/ 
    WHERE (res-line.active-flag = 1 AND res-line.resstatus EQ 6) 
    AND res-line.l-zuordnung[3] = 0 NO-LOCK, 
    FIRST zimmer WHERE zimmer.zinr = res-line.zinr 
    BY res-line.zinr BY res-line.resnr: 
 
    FIND FIRST arrangement WHERE 
      arrangement.arrangement = res-line.arrangement NO-LOCK NO-ERROR. 

    FIND FIRST artikel WHERE artikel.artnr = arrangement.argt-artikelnr 
    AND artikel.departement = 0 NO-LOCK NO-ERROR. 
    ASSIGN 
        serv = 0
        vat  = 0
        vat2 = 0
        fact = 0.
        /*wen*/
    RUN calc-servtaxesbl.p (1, artikel.artnr, artikel.departement,
              curr-date, OUTPUT service, OUTPUT vat, OUTPUT vat2,
              OUTPUT fact).
    /*ASSIGN
	
      service = 0 
      vat = 0.

    RUN calc-servvat.p(artikel.departement, artikel.artnr, res-line.ankunft,
                       artikel.service-code, artikel.mwst-code,
                       OUTPUT service, OUTPUT vat).
	*/
	
 
 
    FIND FIRST waehrung1 WHERE waehrung1.waehrungsnr = res-line.betriebsnr 
	  NO-LOCK NO-ERROR.
      
	  
    exchg-rate = waehrung1.ankauf / waehrung1.einheit. 
    IF res-line.reserve-dec NE 0 THEN frate = reserve-dec. 
    ELSE frate = exchg-rate. 
 
    IF res-line.zipreis NE 0 THEN r-qty = r-qty + 1. 
    FIND FIRST guest WHERE guest.gastnr = res-line.gastnrpay NO-LOCK. 
    FIND FIRST member1 WHERE member1.gastnr = res-line.gastnrmember NO-LOCK. 
    FIND FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK. 
 
    IF res-line.l-zuordnung[1] NE 0 THEN curr-zikatnr = res-line.l-zuordnung[1]. 
    ELSE curr-zikatnr = res-line.zikatnr. 
 
    FIND FIRST bill WHERE bill.resnr = res-line.resnr 
      AND bill.reslinnr = res-line.reslinnr AND bill.zinr = res-line.zinr 
      NO-LOCK NO-ERROR. 
    IF NOT AVAILABLE bill THEN 
	DO:
      FIND FIRST bill WHERE bill.resnr = res-line.resnr 
      AND bill.reslinnr = res-line.reslinnr NO-LOCK NO-ERROR. 
		IF NOT AVAILABLE bill THEN 
		DO: 
		
			msg-warning = "&W" + translateExtended ("Bill not found: RmNo ",lvCAREA,"") + res-line.zinr + " - " + res-line.name.
		END. 
		
	END.
	
    ASSIGN 
      sum-list.pax = sum-list.pax + 
        res-line.erwachs + res-line.kind1 + res-line.kind2 
      sum-list.adult = sum-list.adult + res-line.erwachs    /*FD*/
      sum-list.com = sum-list.com + res-line.gratis. 
/* 
      sum-list.lodging = sum-list.lodging + res-line.zipreis * frate 
      sum-list.t-rev = sum-list.t-rev + res-line.zipreis * frate. 
*/ 
    CREATE cl-list. 
    ASSIGN
      cl-list.res-recid = RECID(res-line)
      cl-list.zinr = res-line.zinr
      cl-list.rstatus = res-line.resstatus 
      cl-list.sleeping = zimmer.sleeping
      cl-list.argt = res-line.arrangement 
      cl-list.name = res-line.NAME   
      /*cl-list.pax = res-line.erwachs + res-line.kind1 + res-line.kind2
      cl-list.com = res-line.gratis + res-line.l-zuordnung[4]*/
      cl-list.com = res-line.gratis
      cl-list.ankunft = res-line.ankunft 
      cl-list.abreise = res-line.abreise 
      cl-list.zipreis = res-line.zipreis 
      cl-list.localrate = res-line.zipreis * frate 
      
      cl-list.t-rev   = res-line.zipreis 
	.
	
    /*IF cl-list.zipreis EQ 0 THEN ASSIGN cl-list.pax = cl-list.com + cl-list.comch.
    ELSE cl-list.pax = res-line.erwachs + res-line.kind1 + res-line.kind2.*/

    /* Add by Michael @ 27/09/2018 for Grand Mirage request - ticket no E0012E */
    ASSIGN
    cl-list.adult    = res-line.erwachs
    cl-list.ch1      = res-line.kind1 
    cl-list.ch2      = res-line.kind2
    cl-list.comch    = res-line.l-zuordnung[4]
    .
    /* End of add */

    IF cl-list.zipreis EQ 0 THEN ASSIGN cl-list.pax = res-line.gratis + cl-list.comch.
    ELSE cl-list.pax = res-line.erwachs + res-line.kind1 + res-line.kind2 + res-line.gratis + cl-list.comch.

    IF AVAILABLE guest THEN
    ASSIGN
        cl-list.NAME     = cl-list.NAME + guest.NAME + ", " + guest.vorname1 + "-" + guest.adresse1
        cl-list.rechnr   = bill.rechnr
        cl-list.currency = waehrung1.wabkurz
        .
    /*disini*/
      
    /* Add by Michael @ 09/01/2019 for Atria request - ticket no 91A72A */
    DEFINE VARIABLE loopi AS INTEGER NO-UNDO.
    IF guest.geburtdatum1 NE ? AND guest.geburtdatum2 NE ? THEN
        IF guest.geburtdatum1 < guest.geburtdatum2 THEN
            ASSIGN cl-list.age1 = YEAR(guest.geburtdatum2) - YEAR(guest.geburtdatum1).
    IF res-line.zimmer-wunsch MATCHES("*ChAge*") THEN
    DO:
        DO loopi = 1 TO NUM-ENTRIES(res-line.zimmer-wunsch, ";") - 1:
            s = ENTRY(loopi, res-line.zimmer-wunsch, ";").
            IF SUBSTR(s,1,5) = "ChAge" THEN
                /*ASSIGN cl-list.age2 = INT(SUBSTR(s,6)).*/
                ASSIGN cl-list.age2 = SUBSTR(s,6).
        END.
    END.
    /* End of add */

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
      AND curr-date GE reslin-queasy.date1 
      AND curr-date LE reslin-queasy.date2 NO-LOCK NO-ERROR. 
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
 
    cl-list.lodging = cl-list.zipreis. 
    IF cl-list.lodging NE 0 THEN 
    DO: 
      prcode = 0. 
      contcode = "".
      FIND FIRST rguest WHERE rguest.gastnr = res-line.gastnr NO-LOCK NO-ERROR. 

      IF res-line.reserve-int NE 0 THEN /* MarkNr -> contract rate exists */ 
        FIND FIRST guest-pr WHERE guest-pr.gastnr = rguest.gastnr 
          NO-LOCK NO-ERROR. 
      IF AVAILABLE guest-pr THEN 
      DO: 
        contcode = guest-pr.CODE.
        ct = res-line.zimmer-wunsch.
        IF ct MATCHES("*$CODE$*") THEN
        DO:
          ct = SUBSTR(ct,INDEX(ct,"$CODE$") + 6).
          contcode = SUBSTR(ct, 1, INDEX(ct,";") - 1).
        END.
        IF new-contrate THEN 
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
        END.
      END.
 
      ASSIGN rm-rate = res-line.zipreis.
      FOR EACH argt-line WHERE argt-line.argtnr = arrangement.argtnr 
        AND NOT argt-line.kind2 NO-LOCK: 
        FIND FIRST artikel WHERE artikel.artnr = argt-line.argt-artnr 
          AND artikel.departement = argt-line.departement NO-LOCK NO-ERROR.
        IF NOT AVAILABLE artikel THEN take-it = NO.
        ELSE RUN get-argtline-rate(contcode, RECID(argt-line), OUTPUT take-it, 
          OUTPUT f-betrag, OUTPUT argt-betrag, OUTPUT qty). 
        IF take-it THEN 
        DO: 
          FIND FIRST s-list WHERE s-list.artnr = argt-line.argt-artnr 
            AND s-list.dept = argt-line.departement 
            AND s-list.curr = waehrung.wabkurz NO-ERROR. 
          IF NOT AVAILABLE s-list THEN 
          DO: 
            create s-list. 
            ASSIGN 
              s-list.artnr = argt-line.argt-artnr 
              s-list.dept = argt-line.departement 
              s-list.bezeich = artikel.bezeich 
              s-list.curr = waehrung.wabkurz. 
          END. 
          ASSIGN 
            s-list.f-betrag = s-list.f-betrag + f-betrag 
            s-list.l-betrag = s-list.l-betrag + argt-betrag * frate 
            s-list.anzahl = s-list.anzahl + qty. 
          sum-list.t-rev = sum-list.t-rev + argt-betrag * frate. 
 
          IF artikel.zwkum = bfast-art AND 
            (artikel.umsatzart = 3 OR artikel.umsatzart GE 5) THEN 
          DO: 
            sum-list.bfast = sum-list.bfast + argt-betrag * frate. 
            cl-list.bfast = cl-list.bfast + argt-betrag. 
            IF res-line.adrflag THEN Ltot-bfast = Ltot-bfast + argt-betrag. 
            ELSE tot-bfast = tot-bfast + argt-betrag. 
            cl-list.lodging = cl-list.lodging - argt-betrag. 
          END. 
          ELSE IF artikel.zwkum = lunch-art AND 
            (artikel.umsatzart = 3 OR artikel.umsatzart GE 5) THEN 
          DO: 
            sum-list.lunch = sum-list.lunch + argt-betrag * frate. 
            cl-list.lunch = cl-list.lunch + argt-betrag. 
            IF res-line.adrflag THEN Ltot-lunch = Ltot-lunch + argt-betrag. 
            ELSE tot-lunch = tot-lunch + argt-betrag. 
            cl-list.lodging = cl-list.lodging - argt-betrag. 
          END. 
          ELSE IF artikel.zwkum = dinner-art AND 
            (artikel.umsatzart = 3 OR artikel.umsatzart GE 5) THEN 
          DO: 
            sum-list.dinner = sum-list.dinner + argt-betrag * frate. 
            cl-list.dinner = cl-list.dinner + argt-betrag. 
            IF res-line.adrflag THEN Ltot-dinner = Ltot-dinner + argt-betrag. 
            ELSE tot-dinner = tot-dinner + argt-betrag. 
            cl-list.lodging = cl-list.lodging - argt-betrag. 
          END. 
          ELSE IF artikel.zwkum = lundin-art AND 
            (artikel.umsatzart = 3 OR artikel.umsatzart GE 5) THEN 
          DO: 
            sum-list.lunch = sum-list.lunch + argt-betrag * frate. 
            cl-list.lunch = cl-list.lunch + argt-betrag. 
            IF res-line.adrflag THEN Ltot-lunch = Ltot-lunch + argt-betrag. 
            ELSE tot-lunch = tot-lunch + argt-betrag. 
            cl-list.lodging = cl-list.lodging - argt-betrag. 
          END. 
          ELSE 
          DO: 
            sum-list.misc = sum-list.misc + argt-betrag * frate. 
            cl-list.misc = cl-list.misc + argt-betrag. 
            IF res-line.adrflag THEN Ltot-misc = Ltot-misc + argt-betrag. 
            ELSE tot-misc = tot-misc + argt-betrag. 
            cl-list.lodging = cl-list.lodging - argt-betrag. 
          END. 
        END. 
      END. 
    END. 

    IF res-line.adrflag THEN Ltot-lodging = Ltot-lodging + cl-list.lodging. 
    ELSE tot-lodging = tot-lodging + cl-list.lodging. 
 
    lodge-betrag = cl-list.lodging * frate. 
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
 
    FIND FIRST artikel1 WHERE artikel1.artnr = arrangement.artnr-logis 
      AND artikel1.departement = 0 NO-LOCK NO-ERROR. 
    FIND FIRST s-list WHERE s-list.artnr = artikel1.artnr 
      AND s-list.dept = artikel1.departement 
      AND s-list.curr = waehrung1.wabkurz NO-ERROR. 
    IF NOT AVAILABLE s-list THEN 
    DO: 
      create s-list. 
      ASSIGN 
        s-list.artnr = artikel1.artnr 
        s-list.dept = artikel1.departement 
        s-list.bezeich = artikel1.bezeich 
        s-list.curr = waehrung1.wabkurz. 
    END. 
    ASSIGN 
      s-list.f-betrag = s-list.f-betrag + lodge-betrag / frate 
      s-list.l-betrag = s-list.l-betrag + lodge-betrag 
      s-list.anzahl = s-list.anzahl + 1. 
      sum-list.lodging = sum-list.lodging + lodge-betrag. 
      sum-list.t-rev = sum-list.t-rev + lodge-betrag. 
 
    FOR EACH fixleist WHERE fixleist.resnr = res-line.resnr 
      AND fixleist.reslinnr = res-line.reslinnr NO-LOCK: 
      RUN check-fixleist-posted(fixleist.artnr, fixleist.departement, 
        fixleist.sequenz, fixleist.dekade, 
        fixleist.lfakt, OUTPUT post-it). 
      IF post-it THEN 
      DO: 
        ASSIGN
          fcost = fixleist.betrag * fixleist.number
          cl-list.t-rev = cl-list.t-rev + fcost
          sum-list.t-rev = sum-list.t-rev + fcost * frate
        . 
        IF res-line.adrflag THEN Ltot-rate = Ltot-rate + fcost. 
        ELSE tot-rate = tot-rate + fcost. 
        
        FIND FIRST artikel WHERE artikel.artnr = fixleist.artnr 
          AND artikel.departement = fixleist.departement NO-LOCK.
       
        FIND FIRST s-list WHERE s-list.artnr = artikel.artnr 
          AND s-list.dept = artikel.departement 
          AND s-list.curr = waehrung1.wabkurz NO-ERROR. 
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
          ASSIGN 
            s-list.f-betrag = s-list.f-betrag + fcost
            s-list.l-betrag = s-list.l-betrag + fcost * frate 
            s-list.anzahl   = s-list.anzahl + fixleist.number 
            cl-list.bfast   = cl-list.bfast + fcost
            sum-list.bfast  = sum-list.bfast + fcost * frate
          .
            IF res-line.adrflag THEN Ltot-bfast = Ltot-bfast + fcost * frate. 
            ELSE tot-bfast = tot-bfast + fcost. 
          END.
          ELSE IF (artikel.zwkum = lunch-art AND artikel.departement = fb-dept) THEN
          DO:
            ASSIGN 
              s-list.f-betrag = s-list.f-betrag + fcost
              s-list.l-betrag = s-list.l-betrag + fcost * frate 
              s-list.anzahl   = s-list.anzahl + fixleist.number 
              cl-list.lunch   = cl-list.lunch + fcost
              sum-list.lunch  = sum-list.lunch + fcost * frate
          .
          IF res-line.adrflag THEN Ltot-lunch = Ltot-lunch + fcost * frate. 
          ELSE tot-lunch = tot-lunch + fcost. 
        END.
        ELSE IF (artikel.zwkum = dinner-art AND artikel.departement = fb-dept) THEN
        DO:
          ASSIGN 
            s-list.f-betrag = s-list.f-betrag + fcost
            s-list.l-betrag = s-list.l-betrag + fcost * frate 
            s-list.anzahl   = s-list.anzahl + fixleist.number 
            cl-list.dinner  = cl-list.dinner + fcost
            sum-list.dinner = sum-list.dinner + fcost * frate
          .
          IF res-line.adrflag THEN Ltot-dinner = Ltot-dinner + fcost * frate. 
          ELSE tot-dinner = tot-dinner + fcost. 
        END.
        ELSE
        DO:
          ASSIGN 
            s-list.f-betrag = s-list.f-betrag + fcost 
            s-list.l-betrag = s-list.l-betrag + fcost * frate 
            s-list.anzahl = s-list.anzahl + fixleist.number
            cl-list.fixcost = cl-list.fixcost + fcost
            sum-list.fixcost = sum-list.fixcost + fcost * frate
          .
          IF res-line.adrflag THEN Ltot-fix = Ltot-fix + fcost. 
          ELSE tot-fix = tot-fix + fcost.  
        END. 
      END. 
    END.
    IF curr-zinr NE res-line.zinr OR curr-resnr NE res-line.resnr THEN 
    DO: 
      IF res-line.adrflag THEN Ltot-rm = Ltot-rm + 1. 
      ELSE tot-rm = tot-rm + 1. 
    END. 
    curr-zinr = res-line.zinr. 
    curr-resnr = res-line.resnr. 
  END. 
 
  /*FD January 28, 2020 For Summary Amount / Local Amount Excl Tax Service*/
  IF exc-taxserv THEN
  DO:
      FOR EACH s-list:      
            ASSIGN
              s-list.f-betrag = ROUND ((s-list.f-betrag / (1 + vat + service)),price-decimal)
              s-list.l-betrag = ROUND ((s-list.l-betrag / (1 + vat + service)),price-decimal)
            .      
      END.
    
      FOR EACH sum-list:
          ASSIGN
              sum-list.lodging = ROUND((sum-list.lodging / (1 + vat + service)),price-decimal)
              sum-list.bfast   = ROUND((sum-list.bfast   / (1 + vat + service)),price-decimal)
              sum-list.lunch   = ROUND((sum-list.lunch   / (1 + vat + service)),price-decimal)
              sum-list.dinner  = ROUND((sum-list.dinner  / (1 + vat + service)),price-decimal)
              sum-list.misc    = ROUND((sum-list.misc    / (1 + vat + service)),price-decimal)
              sum-list.fixcost = ROUND((sum-list.fixcost / (1 + vat + service)),price-decimal)
              sum-list.t-rev   = ROUND((sum-list.t-rev   / (1 + vat + service)),price-decimal)
          .
      END.
  END.
  /*End FD*/

  CREATE cl-list. 
  cl-list.flag = "*". 
  cl-list.zinr = " ".
  /*MTcl-list.c-zipreis = translateExtended ("S U M M A R Y:",lvCAREA,"").*/
 
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
      curr-rm  = 0. 
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
    curr-ch1   = curr-ch1   + cc-list.ch1. 
    curr-ch2   = curr-ch2   + cc-list.ch2. 
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
    IF exc-taxserv THEN
      ASSIGN
        cl-list.zipreis = ROUND ((cl-list.zipreis / (1 + vat + service)),price-decimal)
        cl-list.localrate = ROUND ((cl-list.localrate / (1 + vat + service)),price-decimal)
        cl-list.lodging = ROUND ((cl-list.lodging / (1 + vat + service)),price-decimal)
        cl-list.bfast = ROUND ((cl-list.bfast / (1 + vat + service)),price-decimal)
        cl-list.lunch = ROUND ((cl-list.lunch / (1 + vat + service)),price-decimal)
        cl-list.dinner = ROUND ((cl-list.dinner / (1 + vat + service)),price-decimal)
        cl-list.misc = ROUND ((cl-list.misc / (1 + vat + service)),price-decimal)
        cl-list.fixcost = ROUND ((cl-list.fixcost / (1 + vat + service)),price-decimal)
        cl-list.t-rev = ROUND ((cl-list.t-rev / (1 + vat + service)),price-decimal).
    cl-list.c-zipreis = STRING(cl-list.zipreis,">>>,>>>,>>>,>>9.99"). 
    cl-list.c-localrate = STRING(cl-list.localrate,">>>,>>>,>>>,>>9.99"). 
    IF cl-list.lodging LT 0 THEN 
      cl-list.c-lodging = STRING(cl-list.lodging,"->>,>>>,>>>,>>9.99"). 
    ELSE cl-list.c-lodging = STRING(cl-list.lodging,">>>,>>>,>>>,>>9.99"). 
    cl-list.c-bfast = STRING(cl-list.bfast,">>,>>>,>>>,>>9.99"). 
    cl-list.c-lunch = STRING(cl-list.lunch,">>,>>>,>>>,>>9.99"). 
    cl-list.c-dinner = STRING(cl-list.dinner,">>,>>>,>>>,>>9.99"). 
    cl-list.c-misc = STRING(cl-list.misc,">>,>>>,>>>,>>9.99"). 
    cl-list.c-fixcost = STRING(cl-list.fixcost,"->>>,>>>,>>9.99"). 
    cl-list.ct-rev = STRING(cl-list.t-rev,">>>,>>>,>>>,>>9.99").
  END. 
 
/* 
  create cl-list. 
  cl-list.flag = "*". 
  cl-list.name = "". 
  cl-list.zinr = STRING(tot-rm, ">>>9"). 
  cl-list.pax = tot-pax. 
  cl-list.com = tot-com. 
  cl-list.zipreis = tot-rate. 
  cl-list.localrate = tot-Lrate. 
  cl-list.lodging = tot-lodging. 
  cl-list.bfast = tot-bfast. 
  cl-list.lunch = tot-lunch. 
  cl-list.dinner = tot-dinner. 
  cl-list.misc = tot-misc. 
  cl-list.fixcost = tot-fix. 
  cl-list.t-rev = tot-rate. 
*/ 
/*  July 1st, 2002: Whiterose, should we remove it? 
  IF Ltot-rate NE 0 THEN 
  DO: 
    create cl-list. 
    cl-list.zinr = STRING(Ltot-rm, ">>>9"). 
    cl-list.pax = Ltot-pax. 
    cl-list.argt = "LOCAL". 
    cl-list.zipreis = Ltot-rate. 
    cl-list.lodging = Ltot-lodging. 
    cl-list.bfast = Ltot-bfast. 
    cl-list.lunch = Ltot-lunch. 
    cl-list.dinner = Ltot-dinner. 
    cl-list.misc = Ltot-misc. 
    cl-list.fixcost = Ltot-fix. 
    cl-list.t-rev = Ltot-rate. 
  END. 
*/ 
  total-rev = tot-rate. 
 
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
 
  IF fakt-modus = 1 THEN post-it = YES. 
  ELSE IF fakt-modus = 2 THEN 
  DO: 
    IF res-line.ankunft = curr-date THEN post-it = YES. 
  END. 
  ELSE IF fakt-modus = 3 THEN 
  DO: 
    IF (res-line.ankunft + 1) = curr-date THEN post-it = YES. 
  END. 
  ELSE IF fakt-modus = 4 THEN   /* 1st day OF month  */ 
  DO: 
    IF day(curr-date) EQ 1 THEN post-it = YES. 
  END. 
  ELSE IF fakt-modus = 5 THEN   /* LAST day OF month */ 
  DO: 
    IF day(curr-date + 1) EQ 1 THEN post-it = YES. 
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
    IF curr-date LE (start-date + (intervall - 1)) 
    THEN post-it = YES. 
    IF curr-date LT start-date THEN post-it = no. /* may NOT post !! */ 
  END. 
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
      f-betrag = argt-betrag. 
      FIND FIRST waehrung WHERE RECID(waehrung) = RECID(waehrung1) NO-LOCK. 
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
        f-betrag = argt-betrag. 
        FIND FIRST waehrung WHERE RECID(waehrung) = RECID(waehrung1) NO-LOCK. 
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

    /*ITA 21/04/1988*/
    IF argt-betrag GT 0 THEN argt-betrag = argt-betrag * qty. 
    ELSE argt-betrag = (rm-rate * (- argt-betrag / 100)) * qty.
    /*argt-betrag = argt-betrag * qty. */
    IF argt-betrag = 0 THEN add-it = NO. 

  END.
END. 
