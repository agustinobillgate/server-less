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
    FIELD nation1       LIKE guest.nation1
    FIELD bezeich       LIKE segment.bezeich
    FIELD zipreis       LIKE res-line.zipreis
    FIELD CODE          LIKE ratecode.CODE
    FIELD id            LIKE reservation.useridanlage
    FIELD bezeichnung   LIKE zimkateg.bezeichnung
.

DEFINE INPUT  PARAMETER fdate       AS DATE.
DEFINE INPUT  PARAMETER tdate       AS DATE.
DEFINE INPUT  PARAMETER bfast-artnr AS INTEGER.
DEFINE INPUT  PARAMETER bfast-dept  AS INTEGER.
DEFINE OUTPUT PARAMETER TABLE FOR abf-list.

DEFINE VARIABLE datum   AS DATE.
DEFINE VARIABLE to-date AS DATE.

/*{supertransBL.i} 
DEFINE VARIABLE lvCAREA AS CHARACTER INITIAL "abf-list". */


/************************  MAIN LOGIC   ************************/
FIND FIRST htparam WHERE htparam.paramnr = 110 NO-LOCK.
ASSIGN
    datum   = htparam.fdate.
    /*to-date = tdate - 1.*/

IF fdate /*EQ*/ GT datum AND tdate EQ datum THEN 
DO:
      RUN disp-arlist.
END.
ELSE IF fdate LE datum AND tdate /*LE*/ EQ datum THEN 
DO:
      RUN disp-arlist1. /*genstat*/
END.




/************************  PROCEDURE   **************************/ 
PROCEDURE disp-arlist: 
DEFINE VARIABLE do-it       AS LOGICAL  NO-UNDO.
DEFINE VARIABLE ROflag      AS LOGICAL  NO-UNDO.
DEFINE VARIABLE epreis      AS DECIMAL  NO-UNDO.
DEFINE VARIABLE qty         AS INTEGER  NO-UNDO.
DEFINE VARIABLE i           AS INTEGER  NO-UNDO.
DEFINE VARIABLE str         AS CHAR     NO-UNDO.
DEFINE VARIABLE contcode    AS CHAR     NO-UNDO.
  
 
  FOR EACH abf-list:
      DELETE abf-list.
  END.

  FOR EACH res-line WHERE /*res-line.ankunft LE fdate AND res-line.abreise EQ tdate*/ res-line.ankunft LT fdate AND res-line.abreise GE fdate  AND (res-line.resstatus NE 3 
    AND res-line.resstatus NE 4 AND res-line.resstatus NE 8 
    AND res-line.resstatus NE 9 AND res-line.resstatus NE 10
    AND res-line.resstatus NE 12) AND res-line.active-flag LE 1
    /*AND res-line.ankunft /*LT*/ GE fdate AND res-line.abreise /*GE*/ GT tdate*/
    AND res-line.l-zuordnung[3] = 0 
    NO-LOCK BY res-line.zinr:
    ASSIGN
      do-it  = NO
      ROflag = YES
      qty    = 0
    .
    IF (res-line.erwachs + res-line.kind1 + res-line.gratis + res-line.l-zuordnung[4]) = 0 THEN .
    ELSE
    DO:
      FIND FIRST arrangement WHERE arrangement.arrangement = res-line.arrangement 
        NO-LOCK NO-ERROR.
        IF AVAILABLE arrangement THEN /*FIX find failed on log appserver eko@12april2016*/
          FOR EACH argt-line WHERE argt-line.argtnr = arrangement.argtnr NO-LOCK, 
            FIRST artikel WHERE artikel.artnr = argt-line.argt-artnr 
            AND artikel.departement = bfast-dept 
            AND artikel.zwkum = bfast-artnr NO-LOCK BY argt-line.betrag DESCENDING :
            ASSIGN
              do-it  = YES
              ROflag = NO
              epreis = argt-line.betrag
            .
            LEAVE.
      END.
    END.

    IF do-it AND epreis = 0 THEN
    DO:
        contcode = "".
        RELEASE reslin-queasy.
        DO i = 1 TO NUM-ENTRIES(res-line.zimmer-wunsch,";") - 1:
            str = ENTRY(i, res-line.zimmer-wunsch, ";").
            IF SUBSTR(str,1,6) = "$CODE$" THEN 
            DO:    
              contcode  = SUBSTR(str,7).
              LEAVE.
            END.
        END.
        IF contcode NE "" THEN
        FIND FIRST reslin-queasy WHERE reslin-queasy.key = "argt-line" 
            AND reslin-queasy.char1    = guest-pr.CODE 
            AND reslin-queasy.number1  = res-line.reserve-int
            AND reslin-queasy.number2  = arrangement.argtnr
            AND reslin-queasy.number3  = bfast-artnr 
            AND reslin-queasy.resnr    = bfast-dept 
            AND reslin-queasy.reslinnr = res-line.zikatnr
            AND reslin-queasy.date1 LE fdate
            AND reslin-queasy.date2 GE fdate 
            AND reslin-queasy.deci1 GT 0 NO-LOCK NO-ERROR.
        IF NOT AVAILABLE reslin-queasy THEN
        FIND FIRST reslin-queasy WHERE reslin-queasy.key = "fargt-line" 
            AND reslin-queasy.char1   = guest-pr.CODE 
            AND reslin-queasy.number1 = res-line.reserve-int
            AND reslin-queasy.number2 = arrangement.argtnr
            AND reslin-queasy.number3 = bfast-artnr 
            AND reslin-queasy.resnr   = bfast-dept 
            AND reslin-queasy.date1 LE fdate
            AND reslin-queasy.date2 GE fdate 
            AND reslin-queasy.deci1 GT 0 NO-LOCK NO-ERROR.
        ASSIGN
            do-it = AVAILABLE reslin-queasy
            ROflag = NOT do-it
        .
    END.

    IF NOT do-it THEN
    DO:
    DEF VAR dont-post AS LOGICAL NO-UNDO.
        FOR EACH fixleist WHERE fixleist.resnr = res-line.resnr 
          AND fixleist.reslinnr = res-line.reslinnr 
          AND fixleist.artnr = bfast-artnr
          AND fixleist.departement = bfast-dept NO-LOCK:
          RUN check-fixleist-posted(fixleist.artnr, fixleist.departement, 
             fixleist.sequenz, fixleist.dekade, 
             fixleist.lfakt, OUTPUT dont-post).
          IF NOT dont-post THEN
          ASSIGN
              do-it = YES
              qty = qty + fixleist.number
          .
        END.
    END.

    IF do-it THEN
    DO:
      FIND FIRST guest WHERE guest.gastnr = res-line.resnr NO-LOCK NO-ERROR.
      FIND FIRST reservation WHERE reservation.resnr = res-line.resnr
          NO-LOCK NO-ERROR.
      FIND FIRST segment WHERE segment.segmentcode = res-line.argt-typ NO-LOCK NO-ERROR.
      FIND FIRST ratecode WHERE ratecode.CODE = res-line.arrangement NO-LOCK NO-ERROR.
      CREATE abf-list.
      IF NOT ROflag THEN BUFFER-COPY res-line TO abf-list.
      ELSE 
      DO:    
          BUFFER-COPY res-line EXCEPT erwachs kind1 gratis TO abf-list.
          ASSIGN abf-list.erwachs = 0.
      END.
      ASSIGN
          abf-list.segmentcode = reservation.segmentcode
          
          abf-list.erwachs     = abf-list.erwachs + qty
          abf-list.gastnr      = res-line.gastnr
          abf-list.resname     = reservation.NAME
          abf-list.comments    = reservation.bemerk
          
          abf-list.bezeich     = segment.bezeich
          abf-list.zipreis     = res-line.zipreis
          
          abf-list.id          = reservation.useridanlage
      . 
     
      IF abf-list.comments NE "" THEN abf-list.comments = abf-list.comments + CHR(10).
      abf-list.comments = abf-list.comments + res-line.bemerk.
      IF NOT ROflag THEN 
          abf-list.kind1 = abf-list.kind1 + res-line.l-zuordnung[4].
      IF AVAILABLE zimkateg THEN
        abf-list.kurzbez     = zimkateg.kurzbez.
      IF AVAILABLE ratecode THEN
          abf-list.CODE        = ratecode.CODE.
      IF AVAILABLE guest THEN
      DO:
          abf-list.nation1     = guest.nation1.
          abf-list.address     = guest.adresse1.
          abf-list.city        = guest.wohnort + " " + guest.plz .
      END.
    END.
  END.  
END.


PROCEDURE disp-arlist1: 
DEFINE VARIABLE do-it       AS LOGICAL  NO-UNDO.
DEFINE VARIABLE ROflag      AS LOGICAL  NO-UNDO.
DEFINE VARIABLE epreis      AS DECIMAL  NO-UNDO.
DEFINE VARIABLE qty         AS INTEGER  NO-UNDO.
DEFINE VARIABLE i           AS INTEGER  NO-UNDO.
DEFINE VARIABLE str         AS CHAR     NO-UNDO.
DEFINE VARIABLE contcode    AS CHAR     NO-UNDO.
  
 
  FOR EACH abf-list:
      DELETE abf-list.
  END.
 
  FOR EACH genstat WHERE (genstat.resstatus NE 3 
    AND genstat.resstatus NE 4 AND genstat.resstatus NE 8 
    AND genstat.resstatus NE 9 AND genstat.resstatus NE 10
    AND genstat.resstatus NE 12) /*AND genstat.active-flag LE 1*/
    AND genstat.datum GE fdate AND genstat.datum LE tdate 
    /*AND genstat.l-zuordnung[3] = 0 */
    NO-LOCK BY genstat.zinr:
    ASSIGN
      do-it  = NO
      ROflag = YES
      qty    = 0
    .
    IF (genstat.erwachs + genstat.kind1 + genstat.gratis + genstat.kind3) = 0 THEN .
    ELSE
    DO:
      FIND FIRST arrangement WHERE arrangement.arrangement = genstat.argt 
        NO-LOCK NO-ERROR.
        IF AVAILABLE arrangement THEN /*FIX find failed on log appserver eko@12april2016*/
          FOR EACH argt-line WHERE argt-line.argtnr = arrangement.argtnr NO-LOCK, 
            FIRST artikel WHERE artikel.artnr = argt-line.argt-artnr 
            AND artikel.departement = bfast-dept 
            AND artikel.zwkum = bfast-artnr NO-LOCK BY argt-line.betrag DESCENDING :
            ASSIGN
              do-it  = YES
              ROflag = NO
              epreis = argt-line.betrag
            .
            LEAVE.
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
        FIND FIRST reslin-queasy WHERE reslin-queasy.key = "argt-line" 
            AND reslin-queasy.char1    = guest-pr.CODE 
            AND reslin-queasy.number1  = genstat.res-int[2]
            AND reslin-queasy.number2  = arrangement.argtnr
            AND reslin-queasy.number3  = bfast-artnr 
            AND reslin-queasy.resnr    = bfast-dept 
            AND reslin-queasy.reslinnr = genstat.zikatnr
            AND reslin-queasy.date1 LE fdate
            AND reslin-queasy.date2 GE fdate 
            AND reslin-queasy.deci1 GT 0 NO-LOCK NO-ERROR.
        IF NOT AVAILABLE reslin-queasy THEN
        FIND FIRST reslin-queasy WHERE reslin-queasy.key = "fargt-line" 
            AND reslin-queasy.char1   = guest-pr.CODE 
            AND reslin-queasy.number1 = genstat.res-int[2] 
            AND reslin-queasy.number2 = arrangement.argtnr
            AND reslin-queasy.number3 = bfast-artnr 
            AND reslin-queasy.resnr   = bfast-dept 
            AND reslin-queasy.date1 LE fdate
            AND reslin-queasy.date2 GE fdate 
            AND reslin-queasy.deci1 GT 0 NO-LOCK NO-ERROR.
        ASSIGN
            do-it = AVAILABLE reslin-queasy
            ROflag = NOT do-it
        .
    END.

    IF NOT do-it THEN
    DO:
    DEF VAR dont-post AS LOGICAL NO-UNDO.
        FOR EACH fixleist WHERE fixleist.resnr = genstat.resnr 
          /*AND fixleist.reslinnr = genstat.reslinnr */
          AND fixleist.artnr = bfast-artnr
          AND fixleist.departement = bfast-dept NO-LOCK:
          RUN check-fixleist-posted1(fixleist.artnr, fixleist.departement, 
             fixleist.sequenz, fixleist.dekade, 
             fixleist.lfakt, OUTPUT dont-post).
          IF NOT dont-post THEN
          ASSIGN
              do-it = YES
              qty = qty + fixleist.number
          .
        END.
    END.

    IF do-it THEN
    DO:
      FIND FIRST guest WHERE guest.gastnr = genstat.gastnrmember NO-LOCK NO-ERROR.
      FIND FIRST reservation WHERE reservation.resnr = genstat.resnr NO-LOCK NO-ERROR.
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
          abf-list.segmentcode = reservation.segmentcode
          
          abf-list.erwachs     = abf-list.erwachs + qty
          abf-list.gastnr      = genstat.gastnr
          abf-list.resname     = reservation.NAME
          abf-list.comments    = reservation.bemerk
          abf-list.bezeich     = segment.bezeich
          abf-list.zipreis     = genstat.zipreis
          abf-list.ankunft     = genstat.res-date[1]
          abf-list.abreise     = genstat.res-date[2]
          
          abf-list.id          = reservation.useridanlage
      . 

      /*IF abf-list.NAME = "" THEN
          abf-list.NAME =  reservation.NAME.*/
      IF abf-list.comments NE "" THEN abf-list.comments = abf-list.comments + CHR(10).
      
      IF NOT ROflag THEN 
          abf-list.kind1 = abf-list.kind1 + genstat.kind1.
      IF AVAILABLE zimkateg THEN
        abf-list.kurzbez     = zimkateg.kurzbez.
      IF AVAILABLE ratecode THEN
          abf-list.CODE        = ratecode.CODE.
      IF AVAILABLE guest THEN
          abf-list.address     = guest.adresse1.
          abf-list.city        = guest.wohnort + " " + guest.plz.
          abf-list.nation1     = guest.nation1.
          abf-list.NAME        = guest.NAME. 
          abf-list.comments    = abf-list.comments + guest.bemerk.
    END.
  END.  
END.

PROCEDURE check-fixleist-posted:
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
    FIND FIRST invoice WHERE invoice.resnr = res-line.resnr 
      AND invoice.reslinnr = 0 NO-LOCK. 
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
    FIND FIRST invoice WHERE invoice.zinr = res-line.zinr 
    AND invoice.resnr = res-line.resnr AND invoice.reslinnr = res-line.reslinnr 
    AND invoice.billtyp = 0 AND invoice.billnr = 1 AND invoice.flag = 0 
    NO-LOCK. 
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
        IF res-line.ankunft NE fdate THEN dont-post = YES. 
     END. 
     ELSE IF fakt-modus = 3 THEN 
     DO: 
       IF (res-line.ankunft + 1) NE fdate THEN dont-post = YES. 
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
         delta = lfakt - res-line.ankunft. 
         IF delta LT 0 THEN delta = 0. 
       END. 
       start-date = res-line.ankunft + delta. 
       IF (res-line.abreise - start-date) LT intervall 
         THEN start-date = res-line.ankunft. 
       IF fdate GT (start-date + (intervall - 1)) 
       THEN dont-post = YES. 
       IF fdate LT start-date THEN dont-post = yes. /* may NOT post !! */ 
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

