DEFINE TEMP-TABLE abf-list
    FIELD zinr          LIKE zimmer.zinr
    FIELD NAME          LIKE res-line.NAME
    FIELD segmentcode   LIKE segment.segmentcode
    FIELD ankunft       LIKE res-line.ankunft
    FIELD anztage       LIKE res-line.anztage
    FIELD abreise       LIKE res-line.abreise
    FIELD kurzbez       LIKE zimkateg.kurzbez
    FIELD arrangement   LIKE res-line.arrangement
    FIELD zimmeranz     LIKE res-line.zimmeranz
    FIELD erwachs       LIKE res-line.erwachs 
    FIELD kind1         LIKE res-line.kind1
    FIELD gratis        LIKE res-line.gratis
    FIELD resnr         LIKE res-line.resnr
    FIELD bemerk        LIKE res-line.bemerk
    FIELD gastnr        LIKE res-line.gastnr
    FIELD resstatus     AS INTEGER FORMAT ">9"
    FIELD resname       AS CHAR
    FIELD address       AS CHAR
    FIELD city          AS CHAR
    FIELD comments      AS CHAR
    FIELD datum         AS DATE
    FIELD nation1       LIKE guest.nation1
    FIELD bezeich       LIKE segment.bezeich
    FIELD zipreis       LIKE res-line.zipreis
    FIELD CODE          LIKE ratecode.CODE
    FIELD id            LIKE reservation.useridanlage
    FIELD bezeichnung   LIKE zimkateg.bezeichnung
    FIELD mobil-telefon LIKE guest.mobil-telefon    /*gerald 100221 phone*/
    FIELD bfast-consume AS INTEGER
    FIELD mcard-number  AS CHARACTER
    FIELD mcard-type    AS CHARACTER
    FIELD bfast-revenue AS DECIMAL
.

DEFINE TEMP-TABLE zikat-list 
    FIELD selected AS LOGICAL INITIAL NO 
    FIELD zikatnr  AS INTEGER 
    FIELD kurzbez  AS CHAR 
    FIELD bezeich  AS CHAR FORMAT "x(32)"
.

DEFINE INPUT  PARAMETER fdate       AS DATE.
DEFINE INPUT  PARAMETER bfast-artnr AS INTEGER.
DEFINE INPUT  PARAMETER bfast-dept  AS INTEGER.
DEFINE INPUT  PARAMETER show-bfast-rate AS LOGICAL. /*FDL Dec 05, 2024: Ticket 388744*/
DEFINE INPUT  PARAMETER TABLE FOR zikat-list.   /*FD Jan 24, 20222 => Req Prime Plaza*/
DEFINE OUTPUT PARAMETER TABLE FOR abf-list.

/*{supertransBL.i} 
DEFINE VARIABLE lvCAREA AS CHARACTER INITIAL "abf-list". */


/************************  MAIN LOGIC   **************************/ 
DEFINE VARIABLE diffCiDate      AS INTEGER NO-UNDO.
DEFINE VARIABLE p-87            AS DATE NO-UNDO.
DEFINE VARIABLE num-of-day      AS INTEGER NO-UNDO.
DEFINE VARIABLE exchg-rate      AS DECIMAL NO-UNDO INIT 1.

RUN disp-arlist1.

/************************  PROCEDURE   **************************/ 
PROCEDURE disp-arlist1: 
DEFINE VARIABLE do-it       AS LOGICAL  NO-UNDO.
DEFINE VARIABLE ROflag      AS LOGICAL  NO-UNDO.
DEFINE VARIABLE epreis      AS DECIMAL  NO-UNDO.
DEFINE VARIABLE qty         AS INTEGER  NO-UNDO.
DEFINE VARIABLE qty-argt    AS INTEGER  NO-UNDO.
DEFINE VARIABLE i           AS INTEGER  NO-UNDO.
DEFINE VARIABLE str         AS CHAR     NO-UNDO.
DEFINE VARIABLE contcode    AS CHAR     NO-UNDO.

DEFINE BUFFER rline FOR res-line.
   
    FOR EACH abf-list:
        DELETE abf-list.
    END.
    
    FOR EACH genstat WHERE (genstat.resstatus NE 3 
        AND genstat.resstatus NE 4 AND genstat.resstatus NE 8 
        AND genstat.resstatus NE 9 AND genstat.resstatus NE 10
        AND genstat.resstatus NE 12) 
        /*AND genstat.res-date[1] LT fdate AND genstat.res-date[2] GE fdate,*/
        AND genstat.datum EQ fdate NO-LOCK,     
        FIRST res-line WHERE res-line.resnr EQ genstat.resnr        /*FDL April 26, 2024 => Ticket #6C17FB enhance from CB58AC*/
            AND res-line.reslinnr EQ genstat.res-int[1]
            /*AND genstat.datum GE (res-line.ankunft + 1)*/ NO-LOCK, /*FDL June 04, 2024 => Ticke 18FA49 Comment Ticket #6C17FB*/       
        FIRST zikat-list WHERE zikat-list.zikatnr EQ genstat.zikatnr
            AND zikat-list.SELECTED NO-LOCK BY genstat.zinr:

        ASSIGN
          do-it  = NO
          ROflag = YES
          qty    = 0
          epreis = 0
        .                

        IF (genstat.erwachs + genstat.kind1 + genstat.gratis + genstat.kind3) = 0 THEN .
        ELSE
        DO:
            FIND FIRST arrangement WHERE arrangement.arrangement = genstat.argt NO-LOCK NO-ERROR.
            IF AVAILABLE arrangement THEN /*FIX find failed on log appserver eko@12april2016*/
            DO:
                FOR EACH argt-line WHERE argt-line.argtnr = arrangement.argtnr NO-LOCK, 
                    FIRST artikel WHERE artikel.artnr = argt-line.argt-artnr 
                    AND artikel.departement = bfast-dept 
                    AND artikel.zwkum = bfast-artnr NO-LOCK BY argt-line.betrag DESCENDING :

                    ASSIGN
                      do-it  = YES
                      ROflag = NO
                      epreis = argt-line.betrag
                    .

                    IF argt-line.vt-percnt = 0 THEN 
                    DO: 
                        IF argt-line.betriebsnr = 0 THEN qty-argt = genstat.erwachs. 
                        ELSE qty-argt = argt-line.betriebsnr. 
                    END. 
                    ELSE IF argt-line.vt-percnt = 1 THEN qty-argt = genstat.kind1. 
                    ELSE IF argt-line.vt-percnt = 2 THEN qty-argt = genstat.kind2.

                    LEAVE.
                END.
            END.              
        END.
        
        IF do-it AND epreis = 0 THEN
        DO:
            contcode = "".
            RELEASE reslin-queasy.
            DO i = 1 TO NUM-ENTRIES(genstat.res-char[2],";") - 1:
                str = ENTRY(i, genstat.res-char[2], ";").
                IF SUBSTR(str,1,6) = "$CODE$" THEN 
                DO:    
                    contcode  = SUBSTR(str,7).
                    LEAVE.
                END.
            END.

            IF contcode NE "" THEN
            DO:
                FIND FIRST reslin-queasy WHERE reslin-queasy.key = "argt-line" 
                    AND reslin-queasy.char1    = /*guest-pr.CODE*/ contcode
                    AND reslin-queasy.number1  = genstat.res-int[2]
                    AND reslin-queasy.number2  = arrangement.argtnr
                    AND reslin-queasy.number3  = bfast-artnr 
                    AND reslin-queasy.resnr    = bfast-dept 
                    AND reslin-queasy.reslinnr = genstat.zikatnr
                    AND reslin-queasy.date1 LE fdate
                    AND reslin-queasy.date2 GE fdate 
                    AND reslin-queasy.deci1 GT 0 NO-LOCK NO-ERROR.
                IF NOT AVAILABLE reslin-queasy THEN
                DO:
                    FIND FIRST reslin-queasy WHERE reslin-queasy.key = "fargt-line" 
                        /*AND reslin-queasy.char1     = /*guest-pr.CODE*/ contcode*/
                        AND reslin-queasy.number1   = bfast-dept 
                        AND reslin-queasy.number2   = arrangement.argtnr
                        AND reslin-queasy.number3   = bfast-artnr 
                        AND reslin-queasy.resnr     = genstat.resnr  
                        AND reslin-queasy.reslinnr  = genstat.res-int[1]
                        AND reslin-queasy.date1 LE fdate
                        AND reslin-queasy.date2 GE fdate 
                        AND reslin-queasy.deci1 GT 0 NO-LOCK NO-ERROR.
                END.                
            END.
            
            ASSIGN
                do-it = AVAILABLE reslin-queasy
                ROflag = NOT do-it
            .

            IF do-it THEN epreis = reslin-queasy.deci1. /*FDL Dec 05, 2024: Ticket 388744*/
        END.
        
        IF NOT do-it THEN
        DO:
            DEF VAR dont-post AS LOGICAL NO-UNDO.

            FOR EACH fixleist WHERE fixleist.resnr = genstat.resnr 
                AND fixleist.reslinnr = genstat.res-int[1] 
                AND fixleist.artnr = bfast-artnr
                AND fixleist.departement = bfast-dept NO-LOCK:

                RUN check-fixleist-posted1(fixleist.artnr, fixleist.departement, 
                   fixleist.sequenz, fixleist.dekade, 
                   fixleist.lfakt, OUTPUT dont-post).

                IF NOT dont-post THEN
                DO:
                    ASSIGN
                        do-it = YES
                        qty = qty + fixleist.number
                    .
                END.                
            END.
        END.                

        IF do-it THEN
        DO:
            FIND FIRST guest WHERE guest.gastnr = genstat.gastnrmember NO-LOCK.
            FIND FIRST reservation WHERE reservation.resnr = genstat.resnr NO-LOCK. 
            /*FIND FIRST zimkateg WHERE zimkateg.zikatnr = genstat.zikatnr NO-LOCK.*/
            
            FIND FIRST segment WHERE segment.segmentcode = genstat.segmentcode NO-LOCK NO-ERROR.
            FIND FIRST ratecode WHERE ratecode.CODE = genstat.argt NO-LOCK NO-ERROR.
      

            CREATE abf-list.
            IF NOT ROflag THEN BUFFER-COPY genstat TO abf-list.
            ELSE 
            DO:    
                BUFFER-COPY genstat EXCEPT erwachs kind1 gratis datum TO abf-list.
                ASSIGN abf-list.erwachs = 0.
            END.
            ASSIGN
                abf-list.datum        = genstat.datum
                abf-list.segmentcode  = reservation.segmentcode 
                abf-list.kurzbez      = zikat-list.kurzbez
                abf-list.erwachs      = abf-list.erwachs + qty
                abf-list.gastnr       = genstat.gastnr
                abf-list.resname      = reservation.NAME
                abf-list.comments     = reservation.bemerk
                abf-list.bezeich      = segment.bezeich
                abf-list.zipreis      = genstat.zipreis
                abf-list.ankunft      = genstat.res-date[1]
                abf-list.abreise      = genstat.res-date[2]
                abf-list.arrangement  = genstat.argt   
                abf-list.id           = reservation.useridanlage
            . 
            
            IF abf-list.comments NE "" THEN abf-list.comments = abf-list.comments + CHR(10).
            
            /*FIND FIRST res-line WHERE res-line.resnr = genstat.resnr
                AND res-line.reslinnr = genstat.res-int[1] NO-LOCK NO-ERROR.
            IF AVAILABLE res-line THEN abf-list.bemerk = abf-list.comments + res-line.bemerk.*/
            FIND FIRST rline WHERE rline.resnr = genstat.resnr
                AND rline.reslinnr = genstat.res-int[1] NO-LOCK NO-ERROR.
            IF AVAILABLE rline THEN abf-list.bemerk = abf-list.comments + rline.bemerk.
            
            IF abf-list.comments NE "" THEN abf-list.comments = abf-list.comments + CHR(10).
            
            IF NOT ROflag THEN 
                abf-list.kind1 = abf-list.kind1 + genstat.kind3. /*FDL Feb 15, 2024 => Ticket CB58AC - Change kind1 ro kind3*/
            

            /*
            IF AVAILABLE zimkateg THEN
                abf-list.kurzbez     = zimkateg.kurzbez.
            */
            IF AVAILABLE ratecode THEN
                abf-list.CODE        = ratecode.CODE.
              
            IF AVAILABLE guest THEN
            DO:
                abf-list.address          = guest.adresse1.
                abf-list.city             = guest.wohnort + " " + guest.plz.
                abf-list.NAME             = guest.NAME. 
                abf-list.comments         = abf-list.comments + guest.bemerk.
                abf-list.nation1          = guest.nation1.
                abf-list.mobil-telefon    = guest.mobil-telefon. /*gerald 100221*/

                /*FDL Nov 28, 2024: Ticket F36670*/
                FIND FIRST mc-guest WHERE mc-guest.gastnr EQ guest.gastnr NO-LOCK NO-ERROR.
                IF AVAILABLE mc-guest THEN
                DO:
                    abf-list.mcard-number = mc-guest.cardnum.

                    FIND FIRST mc-type WHERE mc-type.nr EQ mc-guest.nr NO-LOCK NO-ERROR.
                    IF AVAILABLE mc-type THEN abf-list.mcard-type = mc-type.bezeich.
                END.
            END.   

            /*FDL Oct 23, 2024: Ticket 3955B4*/  
            diffCiDate = fdate - res-line.ankunft.
            IF diffCiDate GT 32 THEN num-of-day = diffCiDate - 32.
            ELSE num-of-day = diffCiDate.

            FIND FIRST mealcoup WHERE mealcoup.resnr EQ genstat.resnr 
                AND mealcoup.zinr EQ genstat.zinr 
                AND mealcoup.NAME EQ "Breakfast" NO-LOCK NO-ERROR.
            IF AVAILABLE mealcoup THEN abf-list.bfast-consume = mealcoup.verbrauch[num-of-day].
           /*END*/

            /*FDL Dec 05, 2024: Ticket 388744*/
            IF show-bfast-rate THEN
            DO:
                FIND FIRST artikel WHERE artikel.artnr EQ bfast-artnr
                    AND artikel.departement EQ bfast-dept                    
                    AND artikel.betriebsnr NE 0 
                    AND artikel.pricetab NO-LOCK NO-ERROR.
                IF AVAILABLE artikel THEN
                DO:
                    FIND FIRST waehrung WHERE waehrung.waehrungsnr EQ artikel.betriebsnr NO-LOCK NO-ERROR.
                    IF AVAILABLE waehrung THEN 
                    DO:
                        exchg-rate = waehrung.ankauf / waehrung.einheit.
                        abf-list.bfast-revenue = epreis * qty-argt * exchg-rate.
                    END.
                END.
                ELSE abf-list.bfast-revenue = epreis * qty-argt.                
            END.
            ELSE abf-list.bfast-revenue = 0.
        END.
    END.  
END.

PROCEDURE check-fixleist-posted1:
DEFINE INPUT PARAMETER artnr        AS INTEGER. 
DEFINE INPUT PARAMETER dept         AS INTEGER. 
DEFINE INPUT PARAMETER fakt-modus   AS INTEGER. 
DEFINE INPUT PARAMETER intervall    AS INTEGER. 
DEFINE INPUT PARAMETER lfakt        AS DATE. 
DEFINE OUTPUT PARAMETER dont-post   AS LOGICAL INITIAL NO. 
DEFINE VARIABLE master-flag         AS LOGICAL INITIAL NO. 
DEFINE VARIABLE delta               AS INTEGER. 
DEFINE VARIABLE start-date          AS DATE. 
DEFINE BUFFER invoice FOR bill. 
 
  FIND FIRST master WHERE master.resnr = res-line.resnr 
    AND master.active = YES AND master.flag = 0 NO-LOCK NO-ERROR. 
  IF AVAILABLE master AND master.umsatzart[2] = YES THEN master-flag = YES. 
  
  IF master-flag THEN 
  DO: 
    FIND FIRST invoice WHERE invoice.resnr = genstat.resnr 
      AND invoice.reslinnr = 0 NO-LOCK NO-ERROR. 
/* 
    FIND FIRST bill-line WHERE bill-line.artnr = artnr 
      AND bill-line.departement = dept 
      AND bill-line.zinr = res-line.zinr AND bill-line.rechnr = invoice.rechnr 
      AND bill-line.bill-datum = fdate 
      NO-LOCK NO-ERROR. 
    IF AVAILABLE bill-line THEN dont-post = YES. 
*/ 
  END. 
  ELSE 
  DO: 
  /* check personal account */ 
    FIND FIRST invoice WHERE invoice.zinr = genstat.zinr 
    AND invoice.resnr = genstat.resnr AND invoice.reslinnr = genstat.res-int[1] 
    AND invoice.billtyp = 0 AND invoice.billnr = 1 AND invoice.flag = 0 
    NO-LOCK NO-ERROR. 
/* 
    FIND FIRST bill-line WHERE bill-line.artnr = artnr 
      AND bill-line.departement = dept 
      AND bill-line.zinr = res-line.zinr AND bill-line.rechnr = invoice.rechnr 
      AND bill-line.bill-datum = fdate NO-LOCK NO-ERROR. 
    IF AVAILABLE bill-line THEN dont-post = YES. 
*/ 
  END. 
 
  IF NOT dont-post THEN 
  DO: 
     IF fakt-modus = 2 THEN 
     DO: 
/* deactivated on Sept 14, 2007
        FIND FIRST bill-line WHERE bill-line.artnr = artnr 
          AND bill-line.departement = dept 
          AND bill-line.zinr = res-line.zinr 
          AND bill-line.rechnr = invoice.rechnr 
          NO-LOCK NO-ERROR. 
        IF AVAILABLE bill-line THEN dont-post = YES. 
*/
        IF genstat.datum /*res-line.ankunft*/ NE fdate THEN dont-post = YES. 
     END. 
     ELSE IF fakt-modus = 3 THEN 
     DO: 
       IF (genstat.datum /*res-line.ankunft*/ + 1) NE fdate THEN dont-post = YES.
     END. 
     ELSE IF fakt-modus = 4 THEN   /* 1st day OF month  */ 
     DO: 
        IF DAY(fdate) NE 1 THEN dont-post= YES. 
     END. 
     ELSE IF fakt-modus = 5 THEN   /* LAST day OF month */ 
     DO: 
        IF day(fdate + 1) NE 1 THEN dont-post = YES. 
     END. 
     ELSE IF fakt-modus = 6 THEN 
     DO: 
       IF lfakt = ? THEN delta = 0. 
       ELSE 
       DO: 
         delta = lfakt - genstat.datum /*res-line.ankunft*/. 
         IF delta LT 0 THEN delta = 0. 
       END. 
       start-date = genstat.datum /*res-line.ankunft*/ + delta. 
       IF (/*res-line.abreise*/ genstat.datum - start-date) LT intervall 
         THEN start-date = genstat.datum /*res-line.ankunft*/. 
       IF fdate GT (start-date + (intervall - 1)) 
       THEN dont-post = YES. 
       IF fdate LT start-date THEN dont-post = yes. /* may NOT post !! */ 
    END. 
  END. 
END. 
