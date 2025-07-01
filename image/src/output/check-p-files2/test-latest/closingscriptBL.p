
DEFINE TEMP-TABLE reslin-list LIKE res-line.

DEFINE TEMP-TABLE cl-list
      FIELD zinr LIKE zimmer.zinr
      FIELD zipreis    AS DECIMAL FORMAT "->>,>>>,>>>,>>9.99" COLUMN-LABEL "Room Rate" 
      FIELD localrate  AS DECIMAL FORMAT "->>,>>>,>>>,>>9" COLUMN-LABEL "Local Currency" 
      FIELD lodging    AS DECIMAL FORMAT "->>,>>>,>>>,>>9.99" COLUMN-LABEL "Lodging" 
      FIELD bfast      AS DECIMAL FORMAT "->,>>>,>>>,>>9.99" COLUMN-LABEL "Breakfast" 
      FIELD lunch      AS DECIMAL FORMAT "->,>>>,>>>,>>9.99" COLUMN-LABEL "Lunch" 
      FIELD dinner     AS DECIMAL FORMAT "->,>>>,>>>,>>9.99" COLUMN-LABEL "Dinner" 
      FIELD misc       AS DECIMAL FORMAT "->,>>>,>>>,>>9.99" COLUMN-LABEL "Other Rev" 
      FIELD fixcost    AS DECIMAL FORMAT "->>,>>>,>>9.99"  COLUMN-LABEL "FixCost" 
      FIELD t-rev      AS DECIMAL FORMAT ">>,>>>,>>>,>>9.99" LABEL "Total Rate" 
      FIELD res-recid  AS INTEGER 
      FIELD sleeping   AS LOGICAL INITIAL YES 
      FIELD row-disp   AS INTEGER INITIAL 0 
      FIELD flag       AS CHAR 
      FIELD rstatus    AS INTEGER 
      FIELD argt       AS CHAR FORMAT "x(5)" COLUMN-LABEL "Argt" 
      FIELD currency   AS CHAR FORMAT "x(4)" COLUMN-LABEL "Curr" 
      FIELD ratecode   AS CHAR FORMAT "x(4)" COLUMN-LABEL "RCode"
      FIELD pax        AS INTEGER FORMAT ">>>"           COLUMN-LABEL "Pax" 
      FIELD com        AS INTEGER FORMAT ">>>"           COLUMN-LABEL "Com" 
      FIELD ankunft    AS DATE                           COLUMN-LABEL "Arrival" 
      FIELD abreise    AS DATE                           COLUMN-LABEL "Depart" 
      FIELD rechnr     AS INTEGER FORMAT ">>>>>>>"       COLUMN-LABEL "BillNum" 
      FIELD name       LIKE res-line.name FORMAT "x(19)" COLUMN-LABEL "Guest Name" 
      FIELD ex-rate    AS CHAR FORMAT "x(9)"             COLUMN-LABEL "   ExRate"
      FIELD fix-rate   AS CHAR FORMAT "x(3)"             COLUMN-LABEL "FixedRate"
      FIELD fdate      AS DATE                           COLUMN-LABEL "Fdate"
      FIELD tdate      AS DATE                           COLUMN-LABEL "Tdate"
      FIELD datum      AS DATE                           COLUMN-LABEL "Datum"
      FIELD dt-rate    AS CHAR                           COLUMN-LABEL "DateRate".

DEFINE TEMP-TABLE output-list
    FIELD ci            AS CHAR FORMAT "x(10)"
    FIELD co            AS CHAR FORMAT "x(10)"
    FIELD guest         AS CHAR FORMAT "x(35)"
    FIELD rmcat         AS CHAR FORMAT "x(25)"
    FIELD card          AS CHAR FORMAT "x(22)"
    FIELD grpname       AS CHAR FORMAT "x(35)"
    FIELD res-status    AS CHAR FORMAT "x(15)"
    FIELD night         AS CHAR FORMAT "x(5)"
    FIELD adult         AS CHAR FORMAT "x(3)"
    FIELD child1        AS CHAR FORMAT "x(3)"
    FIELD child2        AS CHAR FORMAT "x(3)"
    FIELD com           AS CHAR FORMAT "x(4)"
    FIELD rmqty         AS CHAR FORMAT "x(3)"
    FIELD rmno          AS CHAR FORMAT "x(10)"
    FIELD memo-zinr     AS CHAR FORMAT "x(20)"
    FIELD voucher       AS CHAR FORMAT "x(20)"
    FIELD argt          AS CHAR FORMAT "x(15)"
    FIELD allot         AS CHAR FORMAT "x(20)"
    FIELD ratecode      AS CHAR FORMAT "x(10)"
    FIELD rmrate        AS CHAR FORMAT "x(16)"
    FIELD currency      AS CHAR FORMAT "x(10)"
    FIELD bill-reciv    AS CHAR FORMAT "x(35)"
    FIELD purpose       AS CHAR FORMAT "x(20)"
    FIELD bill-instruct AS CHAR FORMAT "x(20)"
    /*FIELD deposit       AS DECIMAL FORMAT ">,>>>,>>>,>>9.99"
    FIELD pay1          AS DECIMAL FORMAT ">,>>>,>>>,>>9.99"
    FIELD pay2          AS DECIMAL FORMAT ">,>>>,>>>,>>9.99"*/
    FIELD deposit       AS CHAR FORMAT "x(16)"
    FIELD pay1          AS CHAR FORMAT "x(16)"
    FIELD pay2          AS CHAR FORMAT "x(16)"
    FIELD contcode      AS CHAR FORMAT "x(15)"
    FIELD email-adr     AS CHAR FORMAT "x(32)"
    FIELD nat           AS CHAR FORMAT "x(20)"
    FIELD country       AS CHAR FORMAT "x(20)"
    FIELD restatus      AS INTEGER
    FIELD lzuordnung3   AS INTEGER.

DEFINE INPUT PARAMETER TABLE FOR reslin-list.
DEFINE INPUT PARAMETER pvILanguage    AS INTEGER  NO-UNDO.
DEFINE OUTPUT PARAMETER ausweis-nr2   AS CHAR     NO-UNDO.
DEFINE OUTPUT PARAMETER karteityp     AS INTEGER  NO-UNDO.
DEFINE OUTPUT PARAMETER msg-str       AS CHAR     NO-UNDO.
DEFINE OUTPUT PARAMETER msg-warning   AS CHAR     NO-UNDO.
DEFINE OUTPUT PARAMETER TABLE FOR cl-list.
DEFINE OUTPUT PARAMETER TABLE FOR output-list.


DEFINE BUFFER waehrung1 FOR waehrung.
DEFINE BUFFER cc-list   FOR cl-list.
DEFINE BUFFER member1   FOR guest. 
DEFINE BUFFER rguest    FOR guest.
DEFINE BUFFER artikel1  FOR artikel. 
DEFINE BUFFER queasy1   FOR queasy.  
DEFINE BUFFER nation1   FOR nation.
DEFINE BUFFER bres      FOR res-line.

DEFINE VARIABLE exchg-rate          AS DECIMAL INITIAL 1. 
DEFINE VARIABLE frate               AS DECIMAL FORMAT ">,>>>,>>9.9999". 
DEFINE VARIABLE post-it             AS LOGICAL. 
DEFINE VARIABLE total-rev           AS DECIMAL. 
DEFINE VARIABLE new-contrate        AS LOGICAL INIT NO.
DEFINE VARIABLE foreign-rate        AS LOGICAL.
DEFINE VARIABLE price-decimal       AS INTEGER.
DEFINE VARIABLE fcost               AS DECIMAL. 
DEFINE VARIABLE tot-pax             AS INTEGER INITIAL 0. 
DEFINE VARIABLE tot-com             AS INTEGER INITIAL 0. 
DEFINE VARIABLE tot-rm              AS INTEGER INITIAL 0. 
DEFINE VARIABLE tot-rate            AS DECIMAL INITIAL 0. 
DEFINE VARIABLE tot-Lrate           AS DECIMAL INITIAL 0. 
DEFINE VARIABLE tot-lodging         AS DECIMAL INITIAL 0. 
DEFINE VARIABLE tot-bfast           AS DECIMAL INITIAL 0. 
DEFINE VARIABLE tot-lunch           AS DECIMAL INITIAL 0. 
DEFINE VARIABLE tot-dinner          AS DECIMAL INITIAL 0. 
DEFINE VARIABLE tot-misc            AS DECIMAL INITIAL 0. 
DEFINE VARIABLE tot-fix             AS DECIMAL INITIAL 0. 

DEFINE VARIABLE Ltot-rm             AS INTEGER INITIAL 0. 
DEFINE VARIABLE Ltot-pax            AS INTEGER INITIAL 0. 
DEFINE VARIABLE Ltot-rate           AS DECIMAL INITIAL 0. 
DEFINE VARIABLE Ltot-lodging        AS DECIMAL INITIAL 0. 
DEFINE VARIABLE Ltot-bfast          AS DECIMAL INITIAL 0. 
DEFINE VARIABLE Ltot-lunch          AS DECIMAL INITIAL 0. 
DEFINE VARIABLE Ltot-dinner         AS DECIMAL INITIAL 0. 
DEFINE VARIABLE Ltot-misc           AS DECIMAL INITIAL 0. 
DEFINE VARIABLE Ltot-fix            AS DECIMAL INITIAL 0. 

DEFINE VARIABLE curr-zinr           AS CHAR. 
DEFINE VARIABLE curr-resnr          AS INTEGER INITIAL 0. 

DEFINE VARIABLE bfast-art           AS INTEGER. 
DEFINE VARIABLE lunch-art           AS INTEGER. 
DEFINE VARIABLE dinner-art          AS INTEGER. 
DEFINE VARIABLE lundin-art          AS INTEGER. 
DEFINE VARIABLE fb-dept             AS INTEGER. 
DEFINE VARIABLE argt-betrag         AS DECIMAL. 
DEFINE VARIABLE take-it             AS LOGICAL. 
DEFINE VARIABLE prcode              AS INTEGER. 

DEFINE VARIABLE qty                 AS INTEGER. 
DEFINE VARIABLE r-qty               AS INTEGER INITIAL 0. 
DEFINE VARIABLE lodge-betrag        AS DECIMAL. 
DEFINE VARIABLE f-betrag            AS DECIMAL. 
DEFINE VARIABLE s                   AS CHAR.

DEFINE VARIABLE ct                  AS CHAR.
DEFINE VARIABLE contcode            AS CHAR.

DEFINE VARIABLE vat                 AS DECIMAL.
DEFINE VARIABLE service             AS DECIMAL.
DEFINE VARIABLE curr-zikatnr        AS INTEGER NO-UNDO. 

DEFINE VARIABLE co-date             AS DATE    NO-UNDO.
DEFINE VARIABLE datum               AS DATE    NO-UNDO.
DEFINE VARIABLE curr-date           AS DATE    NO-UNDO.
DEFINE VARIABLE i                   AS INTEGER NO-UNDO.
DEFINE VARIABLE str                 AS CHAR    NO-UNDO.
DEFINE VARIABLE segm_purcode        AS INTEGER NO-UNDO.  

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


{SupertransBL.i} 
DEF VAR lvCAREA AS CHAR INITIAL "rmrev-bdown".

DEFINE VARIABLE rstat-list AS CHAR EXTENT 13 FORMAT "x(9)" NO-UNDO.
rstat-list[1] = translateExtended ("Guaranted",lvCAREA,"").
rstat-list[2] = translateExtended ("6 PM",lvCAREA,"").
rstat-list[3] = translateExtended ("Tentative",lvCAREA,"").
rstat-list[4] = translateExtended ("WaitList",lvCAREA,"").
rstat-list[5] = translateExtended ("Verbal Confirm",lvCAREA,"").
rstat-list[6] = translateExtended ("Main Guest",lvCAREA,"").
rstat-list[7] = "".
rstat-list[8] = translateExtended ("Departed",lvCAREA,"").
rstat-list[9] = translateExtended ("Cancelled",lvCAREA,"").
rstat-list[10] = translateExtended ("NoShow",lvCAREA,"").
rstat-list[11] = translateExtended ("ResSharer",lvCAREA,"").
rstat-list[12] = "".
rstat-list[13] = translateExtended ("RmSharer",lvCAREA,"").


FIND FIRST reslin-list NO-ERROR.
IF AVAILABLE reslin-list THEN DO:
    CREATE output-list.
    ASSIGN 
            output-list.night       = STRING(reslin-list.anztage)
            output-list.adult       = STRING(reslin-list.erwachs)
            output-list.child1      = STRING(reslin-list.kind1)
            output-list.child2      = STRING(reslin-list.kind2)
            output-list.com         = STRING(reslin-list.gratis)
            output-list.rmqty       = STRING(reslin-list.zimmeranz)
            output-list.ci          = STRING(reslin-list.ankunft, "99/99/9999")
            output-list.co          = STRING(reslin-list.abreise, "99/99/9999")
            output-list.rmno        = reslin-list.zinr
            output-list.argt        = reslin-list.arrangement.

     IF reslin-list.zipreis NE 0 THEN 
          ASSIGN output-list.rmrate = STRING(reslin-list.zipreis, ">,>>>,>>>,>>9.99").
     ELSE ASSIGN output-list.rmrate = "0.00".

     FIND FIRST guest WHERE guest.gastnr = reslin-list.gastnrmember NO-LOCK NO-ERROR.
     IF AVAILABLE guest THEN DO:
         ASSIGN output-list.guest     = guest.name + ", " + guest.vorname1 + guest.anredefirma 
                                        + " " + guest.anrede1
                output-list.email-adr = guest.email-adr
                ausweis-nr2           = guest.ausweis-nr2
                karteityp             = guest.karteityp.
     END.

     FIND FIRST nation WHERE nation.kurzbez = guest.nation1 NO-LOCK NO-ERROR.
     IF AVAILABLE nation THEN DO: 
         IF nation.bezeich MATCHES "*;*" THEN 
             ASSIGN output-list.nat = ENTRY(1,nation.bezeich, ";").
         ELSE ASSIGN output-list.nat = nation.bezeich.
     END.

     FIND FIRST nation1 WHERE nation1.kurzbez = guest.land NO-LOCK NO-ERROR.
     IF AVAILABLE nation1 THEN DO:
         IF nation1.bezeich MATCHES "*;*" THEN
             ASSIGN output-list.country = ENTRY(1, nation1.bezeich, ";").
         ELSE ASSIGN output-list.country = nation1.bezeich.
     END.
               
     FIND FIRST reservation WHERE reservation.resnr = reslin-list.resnr NO-LOCK NO-ERROR.
     IF AVAILABLE reservation THEN DO:
         ASSIGN output-list.grpname = reservation.groupname.

         IF reservation.depositgef NE 0  THEN
                output-list.deposit = STRING(reservation.depositgef, ">,>>>,>>>,>>9.99").

         IF reservation.depositbez NE 0 THEN 
               ASSIGN output-list.pay1 = STRING(reservation.depositbez,">,>>>,>>>,>>9.99") .
         /*ELSE ASSIGN output-list.pay1  = 0.00.*/
    
         IF reservation.depositbez2 NE 0 THEN
             ASSIGN output-list.pay2 = STRING(reservation.depositbez2, ">,>>>,>>>,>>9.99").
         /*ELSE ASSIGN output-list.pay2 = 0.00. */
     END.

     FIND FIRST res-line WHERE res-line.resnr = reslin-list.resnr 
         AND res-line.reslinnr = reslin-list.reslinnr
         NO-LOCK NO-ERROR.
     IF AVAILABLE res-line THEN DO:
         ASSIGN output-list.res-status  = rstat-list[reslin-list.resstatus]
                output-list.restat      = res-line.resstatus
                output-list.lzuordnung3 = res-line.l-zuordnung[3].

         IF res-line.memozinr MATCHES("*;*") THEN
            ASSIGN output-list.memo-zinr   = ENTRY(2, res-line.memozinr,";").
         ELSE ASSIGN output-list.memo-zinr = res-line.memozinr.

         FIND FIRST guest WHERE guest.gastnr = res-line.gastnrpay NO-LOCK NO-ERROR.
         IF AVAILABLE guest THEN 
             ASSIGN output-list.bill-reciv  = guest.name + ", " + guest.vorname1 + guest.anredefirma 
                                              + " " + guest.anrede1.

          DO i = 1 TO NUM-ENTRIES(reslin-list.zimmer-wunsch,";") - 1:
              str = ENTRY(i, reslin-list.zimmer-wunsch, ";").
              IF SUBSTR(str,1,8) = "SEGM_PUR" THEN 
                  ASSIGN segm_purcode = INTEGER(SUBSTR(str,9)).
              ELSE IF SUBSTR(str,1,6) = "$CODE$" THEN 
                  ASSIGN output-list.contcode  = SUBSTR(str,7).
          END.

          FIND FIRST queasy1 WHERE queasy1.KEY = 143 AND queasy1.number1 = segm_purcode NO-LOCK NO-ERROR.
          IF AVAILABLE queasy1 THEN ASSIGN output-list.purpose = queasy1.char3.
          
          FIND FIRST queasy WHERE queasy.key = 9 
                    AND queasy.number1 = INTEGER(reslin-list.code) NO-LOCK NO-ERROR.
          IF AVAILABLE queasy THEN ASSIGN output-list.bill-instruct = queasy.char1.
     END.

     IF reslin-list.kontignr GT 0 THEN 
        FIND FIRST kontline WHERE kontline.kontignr = reslin-list.kontignr 
          AND kontline.kontstatus = 1 NO-LOCK NO-ERROR. 
     ELSE 
        FIND FIRST kontline WHERE kontline.kontignr = - reslin-list.kontignr 
          AND kontline.betriebsnr = 1 AND kontline.kontstatus = 1 NO-LOCK NO-ERROR. 
     IF AVAILABLE kontline THEN 
         ASSIGN output-list.allot = kontline.kontcode.
    
     IF output-list.contcode NE "" THEN DO:
        FIND FIRST queasy WHERE queasy.KEY = 2 AND queasy.char1 = output-list.contcode NO-LOCK NO-ERROR.
        IF AVAILABLE queasy THEN ASSIGN output-list.ratecode = queasy.char1.
     END.
     
     FIND FIRST waehrung1 WHERE waehrung1.waehrungsnr = reslin-list.betriebsnr NO-LOCK NO-ERROR.
     IF AVAILABLE waehrung1 THEN ASSIGN output-list.currency = waehrung1.wabkurz.

     FIND FIRST zimkateg WHERE zimkateg.zikatnr = reslin-list.zikatnr NO-LOCK NO-ERROR.
     IF AVAILABLE zimkateg THEN ASSIGN output-list.rmcat = zimkateg.bezeichnung.

     /*find rmsharer and accompany*/
     IF res-line.kontakt-nr NE 0 AND res-line.resstatus LE 6 THEN
     FOR EACH bres WHERE bres.resnr EQ reslin-list.resnr 
         AND bres.reslinnr NE reslin-list.reslinnr 
         AND bres.kontakt-nr EQ reslin-list.reslinnr
         AND bres.resstatus NE 9 
         AND bres.resstatus NE 10 AND bres.resstatus NE 12 NO-LOCK
         BY  bres.l-zuordnung[3]  BY bres.resstatus  BY bres.NAME:
         FIND FIRST guest WHERE guest.gastnr = bres.gastnrmember NO-LOCK NO-ERROR.
         IF AVAILABLE guest THEN
         DO:
             CREATE output-list.
             ASSIGN output-list.guest       = guest.name + ", " + guest.vorname1 + guest.anredefirma 
                                            + " " + guest.anrede1
                    output-list.restat      = bres.resstatus
                    output-list.lzuordnung3 = bres.l-zuordnung[3]
             .
         END.
     END.
     ELSE IF res-line.kontakt-nr NE 0 AND res-line.resstatus GT 6 THEN
     DO:
       FIND FIRST bres WHERE bres.resnr EQ res-line.resnr 
         AND bres.reslinnr EQ res-line.kontakt-nr 
         AND bres.resstatus NE 9 
         AND bres.resstatus NE 10 AND bres.resstatus NE 12 NO-LOCK
         NO-ERROR.
       IF AVAILABLE bres THEN
       DO:
         FIND FIRST guest WHERE guest.gastnr = bres.gastnrmember NO-LOCK NO-ERROR.
         IF AVAILABLE guest THEN
         DO:
             CREATE output-list.
             ASSIGN output-list.guest       = guest.name + ", " + guest.vorname1 + guest.anredefirma 
                                            + " " + guest.anrede1
                    output-list.restat      = bres.resstatus
                    output-list.lzuordnung3 = bres.l-zuordnung[3]
             .
         END.
       END.
     END.
END.

RUN cal-revenue.


PROCEDURE cal-revenue:

  FOR EACH cl-list: 
      DELETE cl-list. 
  END. 
  
  FIND FIRST htparam WHERE paramnr = 125 NO-LOCK NO-ERROR. 
  ASSIGN bfast-art = htparam.finteger. 
  
  FIND FIRST htparam WHERE paramnr = 126 NO-LOCK NO-ERROR. 
  ASSIGN fb-dept = htparam.finteger. 

  FIND FIRST htparam WHERE paramnr = 87 NO-LOCK NO-ERROR.
  ASSIGN curr-date = htparam.fdate.

  FIND FIRST htparam WHERE paramnr = 240 NO-LOCK NO-ERROR.  /* double currency */ 
  ASSIGN foreign-rate = htparam.flogical. 
  IF NOT foreign-rate THEN 
  DO: 
      FIND FIRST htparam WHERE htparam.paramnr = 143 NO-LOCK. /* rate IN foreign */ 
      ASSIGN foreign-rate = htparam.flogical. 
  END. 

  FIND FIRST htparam WHERE htparam.paramnr = 491 NO-LOCK. 
  ASSIGN price-decimal = htparam.finteger. 

  FIND FIRST htparam WHERE htparam.paramnr = 550 NO-LOCK.
  IF htparam.feldtyp = 4 THEN ASSIGN new-contrate = htparam.flogical.
 
  FIND FIRST artikel WHERE artikel.zwkum = bfast-art 
    AND artikel.departement = fb-dept /*GE 1*/ NO-LOCK NO-ERROR. 
  IF NOT AVAILABLE artikel AND bfast-art NE 0 THEN 
  DO: 
    msg-str = translateExtended ("B'fast SubGrp not yed defined (Grp 7)",lvCAREA,"").
    RETURN. 
  END. 
 
  FIND FIRST htparam WHERE paramnr = 227 NO-LOCK. 
  ASSIGN lunch-art = htparam.finteger. 

  FIND FIRST artikel WHERE artikel.zwkum = lunch-art 
    AND artikel.departement = fb-dept /*GE 1*/ NO-LOCK NO-ERROR. 
  IF NOT AVAILABLE artikel AND lunch-art NE 0 THEN 
  DO: 
    msg-str = translateExtended ("Lunch SubGrp not yed defined (Grp 7)",lvCAREA,"").
    RETURN. 
  END. 
 
  FIND FIRST htparam WHERE paramnr = 228 NO-LOCK. 
  ASSIGN dinner-art = htparam.finteger. 

  FIND FIRST artikel WHERE artikel.zwkum = dinner-art 
    AND artikel.departement = fb-dept /*GE 1*/ NO-LOCK NO-ERROR. 
  IF NOT AVAILABLE artikel AND dinner-art NE 0 THEN 
  DO: 
    msg-str = translateExtended ("Dinner SubGrp not yed defined (Grp 7)",lvCAREA,"").
    RETURN. 
  END. 
 
  FIND FIRST htparam WHERE paramnr = 229 NO-LOCK. 
  ASSIGN lundin-art = htparam.finteger. 

  FIND FIRST artikel WHERE artikel.zwkum = lundin-art 
    AND artikel.departement = fb-dept /*GE 1*/ NO-LOCK NO-ERROR. 
  IF NOT AVAILABLE artikel AND lundin-art NE 0 THEN 
  DO: 
    msg-str = translateExtended ("HalfBoard SubGrp not yed defined (Grp 7)",lvCAREA,"").
    RETURN. 
  END. 
 
  r-qty = 0. 
  lodge-betrag = 0. 

  FIND FIRST reslin-list NO-LOCK NO-ERROR.
  IF AVAILABLE reslin-list THEN DO:
      FIND FIRST zimmer WHERE zimmer.zinr = reslin-list.zinr NO-LOCK NO-ERROR.
      FIND FIRST arrangement WHERE arrangement.arrangement = reslin-list.arrangement
           NO-LOCK NO-ERROR.
        
      IF reslin-list.abreise GT reslin-list.ankunft THEN co-date = reslin-list.abreise - 1. 
      ELSE co-date = reslin-list.abreise. 
       
      DO datum = reslin-list.ankunft TO co-date:
          IF datum LT curr-date THEN RUN read-genstat.
          ELSE RUN read-resline.
      END.
  END.
END.

PROCEDURE read-genstat:
    FIND FIRST genstat WHERE genstat.zinr NE "" AND genstat.datum = datum 
        AND genstat.res-logic[2] EQ YES 
        AND genstat.resnr = reslin-list.resnr
        AND genstat.res-int[1] = reslin-list.reslinnr  NO-LOCK NO-ERROR.
    IF AVAILABLE genstat THEN DO:

        FIND FIRST artikel WHERE artikel.artnr = arrangement.argt-artikelnr 
            AND artikel.departement = 0 NO-LOCK. 
        ASSIGN
          service = 0 
          vat     = 0
          serv1   = 0
          vat1    = 0
          vat2    = 0
          fact1   = 0.
        
        RUN calc-servtaxesbl.p (1, artikel.artnr, artikel.departement,
                                curr-date, OUTPUT serv1, OUTPUT vat1, OUTPUT vat2,
                                OUTPUT fact1).
        /*RUN calc-servvat.p(artikel.departement, artikel.artnr, genstat.datum,
                           artikel.service-code, artikel.mwst-code,
                           OUTPUT service, OUTPUT vat).*/
        FIND FIRST waehrung1 WHERE waehrung1.waehrungsnr = reslin-list.betriebsnr 
          NO-LOCK. 
        IF AVAILABLE waehrung1 THEN DO:
            FIND FIRST exrate WHERE exrate.datum = curr-date
                AND exrate.artnr = waehrung1.waehrungsnr NO-LOCK NO-ERROR.
            IF AVAILABLE exrate THEN ASSIGN exchg-rate = exrate.betrag. 
        END.
        
        IF reslin-list.reserve-dec NE 0 THEN frate = reslin-list.reserve-dec. 
        ELSE frate = exchg-rate. 
     
        IF genstat.zipreis NE 0 THEN r-qty = r-qty + 1. 
        FIND FIRST guest WHERE guest.gastnr = reslin-list.gastnrpay NO-LOCK NO-ERROR. 
        FIND FIRST member1 WHERE member1.gastnr = reslin-list.gastnrmember NO-LOCK NO-ERROR. 
        FIND FIRST reservation WHERE reservation.resnr = reslin-list.resnr NO-LOCK NO-ERROR. 
     
        IF reslin-list.l-zuordnung[1] NE 0 THEN curr-zikatnr = reslin-list.l-zuordnung[1]. 
        ELSE curr-zikatnr = reslin-list.zikatnr. 
     
        FIND FIRST bill WHERE bill.resnr = reslin-list.resnr 
          AND bill.reslinnr = reslin-list.reslinnr AND bill.zinr = reslin-list.zinr 
          NO-LOCK NO-ERROR. 
        IF NOT AVAILABLE bill THEN 
          FIND FIRST bill WHERE bill.resnr = reslin-list.resnr 
          AND bill.reslinnr = reslin-list.reslinnr NO-LOCK NO-ERROR. 
        IF NOT AVAILABLE bill THEN 
        DO: 
          msg-str = translateExtended ("Bill not found: RmNo ",lvCAREA,"") + reslin-list.zinr + " - " + reslin-list.name .
        END. 

        CREATE cl-list. 
        ASSIGN
          cl-list.res-recid         = RECID(reslin-list)
          cl-list.zinr              = genstat.zinr
          cl-list.rstatus           = genstat.resstatus 
          cl-list.sleeping          = zimmer.sleeping
          cl-list.argt              = genstat.argt
          cl-list.name              = reslin-list.NAME
          cl-list.pax               = genstat.erwachs + genstat.kind1 + genstat.kind2
          cl-list.com               = genstat.gratis + genstat.kind3
          cl-list.ankunft           = reslin-list.ankunft 
          cl-list.abreise           = reslin-list.abreise 
          cl-list.zipreis           = genstat.zipreis 
          cl-list.localrate         = genstat.rateLocal 
          cl-list.rechnr            = bill.rechnr
          cl-list.t-rev             = genstat.zipreis 
          cl-list.currency          = waehrung1.wabkurz
          cl-list.lodging           = genstat.logis
    
          cl-list.bfast             = genstat.res-deci[2] * (1 + vat1 + vat2 + serv1)
          cl-list.lunch             = genstat.res-deci[3] * (1 + vat1 + vat2 + serv1)
          cl-list.dinner            = genstat.res-deci[4] * (1 + vat1 + vat2 + serv1)
          cl-list.misc              = genstat.res-deci[5] * (1 + vat1 + vat2 + serv1)
          cl-list.fixcost           = genstat.res-deci[6] * (1 + vat1 + vat2 + serv1)
          cl-list.datum             = datum.
         
          FIND FIRST htparam WHERE htparam.paramnr = 127 NO-LOCK NO-ERROR. 
          IF htparam.flogical THEN
              cl-list.lodging = ROUND ((cl-list.lodging * (1 + vat1 + vat2 + serv1)),price-decimal).
              /*cl-list.lodging = ROUND ((cl-list.lodging * (1 + vat + service)),price-decimal).*/
          IF reslin-list.zimmer-wunsch MATCHES("*$CODE$*") THEN
          DO:
               s = SUBSTR(reslin-list.zimmer-wunsch,(INDEX(reslin-list.zimmer-wunsch,"$CODE$") + 6)).
               cl-list.ratecode = TRIM(ENTRY(1, s, ";")).
          END.
            
          IF frate EQ 1 THEN cl-list.ex-rate = STRING(frate,"   >>9.99"). 
          ELSE IF frate LE 999 THEN cl-list.ex-rate = STRING(frate," >>9.9999"). 
          ELSE IF frate LE 99999 THEN cl-list.ex-rate = STRING(frate,">>,>>9.99"). 
          ELSE cl-list.ex-rate = STRING(frate,">,>>>,>>9"). 

          FIND FIRST reslin-queasy WHERE reslin-queasy.key = "arrangement" 
              AND reslin-queasy.resnr = reslin-list.resnr 
              AND reslin-queasy.reslinnr = reslin-list.reslinnr 
              AND datum GE reslin-queasy.date1 
              AND datum LE reslin-queasy.date2 NO-LOCK NO-ERROR. 
          IF AVAILABLE reslin-queasy THEN DO:
              ASSIGN cl-list.fix-rate = "YES"
                     cl-list.fdate    = reslin-queasy.date1
                     cl-list.tdate    = reslin-queasy.date2.
          END.
          ELSE  ASSIGN cl-list.fix-rate = "NO".
          
          IF cl-list.fdate NE ? THEN
            ASSIGN cl-list.dt-rate = STRING(cl-list.fdate, "99/99/99") + " - " + STRING(cl-list.tdate, "99/99/99").

          ASSIGN 
              tot-rate = tot-rate + cl-list.zipreis
              tot-Lrate = tot-Lrate + cl-list.localrate. 
          IF NOT reslin-list.adrflag THEN tot-pax = tot-pax + cl-list.pax. 
          ELSE Ltot-pax = Ltot-pax + cl-list.pax. 
          ASSIGN tot-com = tot-com + cl-list.com. 

          IF reslin-list.adrflag THEN Ltot-lodging = Ltot-lodging + cl-list.lodging. 
          ELSE tot-lodging = tot-lodging + cl-list.lodging. 
         
          ASSIGN lodge-betrag = cl-list.lodging . 
          IF foreign-rate AND price-decimal = 0 AND NOT reslin-list.adrflag THEN 
          DO: 
              FIND FIRST htparam WHERE paramnr = 145 NO-LOCK NO-ERROR. 
              IF htparam.finteger NE 0 THEN 
              DO: 
                DEFINE VARIABLE i AS INTEGER. 
                DEFINE VARIABLE n AS INTEGER. 
                n = 1. 
                DO i = 1 TO htparam.finteger: 
                  n = n * 10. 
                END. 
                lodge-betrag = ROUND(lodge-betrag / n, 0) * n. 
              END. 
          END.
          IF curr-zinr NE reslin-list.zinr OR curr-resnr NE reslin-list.resnr THEN 
          DO: 
            IF reslin-list.adrflag THEN Ltot-rm = Ltot-rm + 1. 
            ELSE tot-rm = tot-rm + 1. 
          END. 
          ASSIGN 
              curr-zinr = reslin-list.zinr. 
               curr-resnr = reslin-list.resnr. 
    END.
END.

PROCEDURE read-resline:
   ASSIGN
      service = 0 
      vat     = 0
      serv1   = 0
      vat1    = 0
      vat2    = 0
      fact1   = 0.

   FIND FIRST artikel WHERE artikel.artnr = arrangement.argt-artikelnr AND artikel.departement = 0 
       NO-LOCK NO-ERROR. 
   IF AVAILABLE artikel THEN DO:
       /*RUN calc-servvat.p(artikel.departement, artikel.artnr, reslin-list.ankunft,
                          artikel.service-code, artikel.mwst-code, OUTPUT service, OUTPUT vat).*/
       RUN calc-servtaxesbl.p (1, artikel.artnr, artikel.departement,
                               curr-date, OUTPUT serv1, OUTPUT vat1, OUTPUT vat2,
                               OUTPUT fact1).
   END.

   FIND FIRST waehrung1 WHERE waehrung1.waehrungsnr = reslin-list.betriebsnr NO-LOCK NO-ERROR. 
   IF AVAILABLE waehrung1 THEN ASSIGN exchg-rate = waehrung1.ankauf / waehrung1.einheit. 
   IF reslin-list.reserve-dec NE 0 THEN frate = reslin-list.reserve-dec. 
   ELSE frate = exchg-rate. 

   IF reslin-list.zipreis NE 0 THEN r-qty = r-qty + 1. 
   FIND FIRST guest WHERE guest.gastnr = reslin-list.gastnrpay NO-LOCK NO-ERROR. 
   FIND FIRST member1 WHERE member1.gastnr = reslin-list.gastnrmember NO-LOCK NO-ERROR. 
   FIND FIRST reservation WHERE reservation.resnr = reslin-list.resnr NO-LOCK NO-ERROR.

   IF reslin-list.l-zuordnung[1] NE 0 THEN curr-zikatnr = reslin-list.l-zuordnung[1]. 
   ELSE curr-zikatnr = reslin-list.zikatnr. 
    
   FIND FIRST bill WHERE bill.resnr = reslin-list.resnr 
      AND bill.reslinnr = reslin-list.reslinnr AND bill.zinr = reslin-list.zinr NO-LOCK NO-ERROR. 

   IF NOT AVAILABLE bill THEN 
      FIND FIRST bill WHERE bill.resnr = reslin-list.resnr 
        AND bill.reslinnr = reslin-list.reslinnr NO-LOCK NO-ERROR. 
   IF NOT AVAILABLE bill THEN 
   DO: 
      msg-warning = "&W" + translateExtended ("Bill not found: RmNo ",lvCAREA,"") + reslin-list.zinr + " - " + reslin-list.name.
   END. 

   CREATE cl-list. 
   ASSIGN
      cl-list.res-recid     = RECID(reslin-list)
      cl-list.zinr          = reslin-list.zinr
      cl-list.rstatus       = reslin-list.resstatus 
      cl-list.argt          = reslin-list.arrangement 
      cl-list.name          = reslin-list.name
      cl-list.pax           = reslin-list.erwachs + reslin-list.kind1 + reslin-list.kind2
      cl-list.com           = reslin-list.gratis + reslin-list.l-zuordnung[4]
      cl-list.ankunft       = reslin-list.ankunft 
      cl-list.abreise       = reslin-list.abreise 
      cl-list.currency      = waehrung1.wabkurz
      cl-list.datum         = datum.

   IF AVAILABLE bill THEN ASSIGN cl-list.rechnr  = bill.rechnr.
   IF AVAILABLE zimmer THEN ASSIGN cl-list.sleeping = zimmer.sleeping.
    
   IF frate EQ 1 THEN cl-list.ex-rate = STRING(frate,"   >>9.99"). 
   ELSE IF frate LE 999 THEN cl-list.ex-rate = STRING(frate," >>9.9999"). 
   ELSE IF frate LE 99999 THEN cl-list.ex-rate = STRING(frate,">>,>>9.99"). 
   ELSE cl-list.ex-rate = STRING(frate,">,>>>,>>9"). 

   FIND FIRST reslin-queasy WHERE reslin-queasy.key = "arrangement" 
      AND reslin-queasy.resnr = reslin-list.resnr 
      AND reslin-queasy.reslinnr = reslin-list.reslinnr 
      AND datum GE reslin-queasy.date1 
      AND datum LE reslin-queasy.date2 NO-LOCK NO-ERROR. 
   IF AVAILABLE reslin-queasy THEN DO:
       ASSIGN cl-list.fix-rate  = "YES"
              cl-list.zipreis   = reslin-queasy.deci1
              cl-list.localrate = reslin-queasy.deci1 * frate 
              cl-list.t-rev     = reslin-queasy.deci1 
              cl-list.fdate     = reslin-queasy.date1
              cl-list.tdate     = reslin-queasy.date2.
   END.
   ELSE DO:
       ASSIGN cl-list.fix-rate  = "NO"
              cl-list.zipreis   = reslin-list.zipreis
              cl-list.localrate = reslin-list.zipreis * frate 
              cl-list.t-rev     = reslin-list.zipreis.
   END.


   IF cl-list.fdate NE ? THEN
     ASSIGN cl-list.dt-rate = STRING(cl-list.fdate, "99/99/99") + "-" + STRING(cl-list.tdate, "99/99/99").

   ASSIGN 
       tot-rate  = tot-rate + cl-list.zipreis
       tot-Lrate = tot-Lrate + cl-list.localrate. 
   IF NOT reslin-list.adrflag THEN tot-pax = tot-pax + cl-list.pax. 
   ELSE Ltot-pax = Ltot-pax + cl-list.pax. 
   ASSIGN tot-com = tot-com + cl-list.com. 

   cl-list.lodging = cl-list.zipreis. 
   IF cl-list.lodging NE 0 THEN 
   DO: 
      prcode = 0. 
      contcode = "".
      FIND FIRST rguest WHERE rguest.gastnr = reslin-list.gastnr NO-LOCK. 
      IF reslin-list.reserve-int NE 0 THEN /* MarkNr -> contract rate exists */ 
        FIND FIRST guest-pr WHERE guest-pr.gastnr = rguest.gastnr 
          NO-LOCK NO-ERROR. 
      IF AVAILABLE guest-pr THEN 
      DO: 
        contcode = guest-pr.CODE.
        ct = reslin-list.zimmer-wunsch.
        IF ct MATCHES("*$CODE$*") THEN
        DO:
          ct = SUBSTR(ct,INDEX(ct,"$CODE$") + 6).
          contcode = SUBSTR(ct, 1, INDEX(ct,";") - 1).
        END.
        IF new-contrate THEN 
        DO:   
           RUN ratecode-seek.p(reslin-list.resnr, 
                               reslin-list.reslinnr, contcode, curr-date, OUTPUT prcode).
        END.
        ELSE
        DO:
          FIND FIRST pricecod WHERE pricecod.code = contcode 
            AND pricecod.marknr = reslin-list.reserve-int 
            AND pricecod.argtnr = arrangement.argtnr 
            AND pricecod.zikatnr = curr-zikatnr 
            AND curr-date GE pricecod.startperiode 
            AND curr-date LE pricecod.endperiode NO-LOCK NO-ERROR. 
          IF AVAILABLE pricecod THEN prcode = RECID(pricecod). 
        END.
      END.
 
      FOR EACH argt-line WHERE argt-line.argtnr = arrangement.argtnr 
        AND NOT argt-line.kind2 NO-LOCK: 
        FIND FIRST artikel WHERE artikel.artnr = argt-line.argt-artnr 
          AND artikel.departement = argt-line.departement NO-LOCK NO-ERROR.
        IF NOT AVAILABLE artikel THEN take-it = NO.
        ELSE 
          RUN get-argtline-rate(contcode, RECID(argt-line), OUTPUT take-it, 
                                OUTPUT f-betrag, OUTPUT argt-betrag, OUTPUT qty). 
        IF take-it THEN 
        DO: 
          
          IF artikel.zwkum = bfast-art AND 
            (artikel.umsatzart = 3 OR artikel.umsatzart GE 5) THEN 
          DO: 
            ASSIGN cl-list.bfast = cl-list.bfast + argt-betrag. 
            IF reslin-list.adrflag THEN Ltot-bfast = Ltot-bfast + argt-betrag. 
            ELSE tot-bfast = tot-bfast + argt-betrag. 
            ASSIGN cl-list.lodging = cl-list.lodging - argt-betrag. 
          END. 
          ELSE IF artikel.zwkum = lunch-art AND 
            (artikel.umsatzart = 3 OR artikel.umsatzart GE 5) THEN 
          DO: 
            ASSIGN cl-list.lunch = cl-list.lunch + argt-betrag. 
            IF reslin-list.adrflag THEN Ltot-lunch = Ltot-lunch + argt-betrag. 
            ELSE tot-lunch = tot-lunch + argt-betrag. 
            ASSIGN cl-list.lodging = cl-list.lodging - argt-betrag. 
          END. 
          ELSE IF artikel.zwkum = dinner-art AND 
            (artikel.umsatzart = 3 OR artikel.umsatzart GE 5) THEN 
          DO: 
            ASSIGN cl-list.dinner = cl-list.dinner + argt-betrag. 
            IF reslin-list.adrflag THEN Ltot-dinner = Ltot-dinner + argt-betrag. 
            ELSE tot-dinner = tot-dinner + argt-betrag. 
            ASSIGN cl-list.lodging = cl-list.lodging - argt-betrag. 
          END. 
          ELSE IF artikel.zwkum = lundin-art AND 
            (artikel.umsatzart = 3 OR artikel.umsatzart GE 5) THEN 
          DO: 
            ASSIGN cl-list.lunch = cl-list.lunch + argt-betrag. 
            IF reslin-list.adrflag THEN Ltot-lunch = Ltot-lunch + argt-betrag. 
            ELSE tot-lunch = tot-lunch + argt-betrag. 
            ASSIGN cl-list.lodging = cl-list.lodging - argt-betrag. 
          END. 
          ELSE 
          DO: 
            ASSIGN cl-list.misc = cl-list.misc + argt-betrag. 
            IF reslin-list.adrflag THEN Ltot-misc = Ltot-misc + argt-betrag. 
            ELSE tot-misc = tot-misc + argt-betrag. 
            ASSIGN cl-list.lodging = cl-list.lodging - argt-betrag. 
          END. 
        END. 
      END. 
   END. 

   IF reslin-list.adrflag THEN Ltot-lodging = Ltot-lodging + cl-list.lodging. 
   ELSE tot-lodging = tot-lodging + cl-list.lodging. 
 
   ASSIGN lodge-betrag = cl-list.lodging * frate. 
   IF foreign-rate AND price-decimal = 0 AND NOT reslin-list.adrflag THEN 
   DO: 
      FIND FIRST htparam WHERE paramnr = 145 NO-LOCK NO-ERROR. 
      IF htparam.finteger NE 0 THEN 
      DO: 
        DEFINE VARIABLE i AS INTEGER. 
        DEFINE VARIABLE n AS INTEGER. 
        n = 1. 
        DO i = 1 TO htparam.finteger: 
          n = n * 10. 
        END. 
        lodge-betrag = ROUND(lodge-betrag / n, 0) * n. 
      END. 
   END. 
 
   FIND FIRST artikel1 WHERE artikel1.artnr = arrangement.artnr-logis 
      AND artikel1.departement = 0 NO-LOCK NO-ERROR. 

   FOR EACH fixleist WHERE fixleist.resnr = reslin-list.resnr 
      AND fixleist.reslinnr = reslin-list.reslinnr NO-LOCK:

      RUN check-fixleist-posted(fixleist.artnr, fixleist.departement, 
                                fixleist.sequenz, fixleist.dekade, 
                                fixleist.lfakt, OUTPUT post-it). 
      IF post-it THEN 
      DO: 
        ASSIGN
          fcost = fixleist.betrag * fixleist.number
          cl-list.t-rev = cl-list.t-rev + fcost.

        IF reslin-list.adrflag THEN Ltot-rate = Ltot-rate + fcost. 
        ELSE tot-rate = tot-rate + fcost. 
        
        FIND FIRST artikel WHERE artikel.artnr = fixleist.artnr 
          AND artikel.departement = fixleist.departement NO-LOCK NO-ERROR.
       
        IF (artikel.zwkum = bfast-art AND artikel.departement = fb-dept) THEN
        DO:
          ASSIGN 
            cl-list.bfast   = cl-list.bfast + fcost.

            IF reslin-list.adrflag THEN Ltot-bfast = Ltot-bfast + fcost * frate. 
            ELSE tot-bfast = tot-bfast + fcost. 
          END.
          ELSE IF (artikel.zwkum = lunch-art AND artikel.departement = fb-dept) THEN
          DO:
            ASSIGN 
              cl-list.lunch   = cl-list.lunch + fcost.

          IF reslin-list.adrflag THEN Ltot-lunch = Ltot-lunch + fcost * frate. 
          ELSE tot-lunch = tot-lunch + fcost. 
        END.
        ELSE IF (artikel.zwkum = dinner-art AND artikel.departement = fb-dept) THEN
        DO:
          ASSIGN 
            cl-list.dinner  = cl-list.dinner + fcost.

          IF reslin-list.adrflag THEN Ltot-dinner = Ltot-dinner + fcost * frate. 
          ELSE tot-dinner = tot-dinner + fcost. 
        END.
        ELSE
        DO:
          ASSIGN 
            cl-list.fixcost = cl-list.fixcost + fcost.

          IF reslin-list.adrflag THEN Ltot-fix = Ltot-fix + fcost. 
          ELSE tot-fix = tot-fix + fcost.  
        END. 
      END. 
    END.
    IF curr-zinr NE reslin-list.zinr OR curr-resnr NE reslin-list.resnr THEN 
    DO: 
      IF reslin-list.adrflag THEN Ltot-rm = Ltot-rm + 1. 
      ELSE tot-rm = tot-rm + 1. 
    END. 
    ASSIGN 
        curr-zinr  = reslin-list.zinr
        curr-resnr = reslin-list.resnr.
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
    IF reslin-list.ankunft = curr-date THEN post-it = YES. 
  END. 
  ELSE IF fakt-modus = 3 THEN 
  DO: 
    IF (reslin-list.ankunft + 1) = curr-date THEN post-it = YES. 
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
      delta = lfakt - reslin-list.ankunft. 
      IF delta LT 0 THEN delta = 0. 
    END. 
    start-date = reslin-list.ankunft + delta. 
    IF (reslin-list.abreise - start-date) LT intervall 
      THEN start-date = reslin-list.ankunft. 
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
 
  IF reslin-list.l-zuordnung[1] NE 0 THEN curr-zikatnr = reslin-list.l-zuordnung[1]. 
  ELSE curr-zikatnr = reslin-list.zikatnr. 
 
  FIND FIRST argtline WHERE RECID(argtline) = argt-recid NO-LOCK. 
  IF argt-line.vt-percnt = 0 THEN 
  DO: 
    IF argt-line.betriebsnr = 0 THEN qty = reslin-list.erwachs. 
    ELSE qty = argt-line.betriebsnr. 
  END. 
  ELSE IF argt-line.vt-percnt = 1 THEN qty = reslin-list.kind1. 
  ELSE IF argt-line.vt-percnt = 2 THEN qty = reslin-list.kind2. 
  IF qty GT 0 THEN 
  DO: 
    IF argtline.fakt-modus = 1 THEN add-it = YES. 
    ELSE IF argtline.fakt-modus = 2 THEN 
    DO: 
      IF reslin-list.ankunft EQ curr-date THEN add-it = YES. 
    END. 
    ELSE IF argtline.fakt-modus = 3 THEN 
    DO: 
      IF (reslin-list.ankunft + 1) EQ curr-date THEN add-it = YES. 
    END. 
    ELSE IF argtline.fakt-modus = 4 
      AND day(curr-date) = 1 THEN add-it = YES. 
    ELSE IF argtline.fakt-modus = 5 
      AND day(curr-date + 1) = 1 THEN add-it = YES. 
    ELSE IF argtline.fakt-modus = 6 THEN 
    DO: 
      IF (reslin-list.ankunft + (argtline.intervall - 1)) GE curr-date 
      THEN add-it = YES. 
    END. 
  END. 
 
  IF add-it THEN 
  DO: 
    FIND FIRST reslin-queasy WHERE key = "fargt-line" 
        AND reslin-queasy.char1 = "" 
        AND reslin-queasy.resnr = reslin-list.resnr 
        AND reslin-queasy.reslinnr = reslin-list.reslinnr 
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
        AND reslin-queasy.number1 = reslin-list.reserve-int 
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
      NO-LOCK. 
    FIND FIRST waehrung WHERE waehrung.waehrungsnr = arrangement.betriebsnr 
      NO-LOCK. 
    f-betrag = argt-betrag * qty. 
    IF reslin-list.betriebsnr NE arrangement.betriebsnr THEN 
      argt-betrag = argt-betrag * (waehrung.ankauf / waehrung.einheit) / frate. 
    argt-betrag = argt-betrag * qty. 
    IF argt-betrag = 0 THEN add-it = NO. 
  END.
END. 





