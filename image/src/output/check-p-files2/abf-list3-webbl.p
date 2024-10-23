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
DEFINE INPUT  PARAMETER incl-accom  AS LOGICAL. /*ragung*/
DEFINE INPUT  PARAMETER incl-guarantee AS LOGICAL. /*FDL June 03, 2024 => Ticket 597829*/
DEFINE INPUT  PARAMETER TABLE FOR zikat-list.   /*FD Jan 24, 20222 => Req Prime Plaza*/
DEFINE OUTPUT PARAMETER TABLE FOR abf-list.

/*{supertransBL.i} 
DEFINE VARIABLE lvCAREA AS CHARACTER INITIAL "abf-list". */


/************************  MAIN LOGIC   **************************/ 
/*FD August 29, 2022 => Artotel*/
DEFINE VARIABLE mxtime-dayuse   AS INTEGER.
DEFINE VARIABLE param-561       AS CHARACTER.


FIND FIRST htparam WHERE htparam.paramnr EQ 561 NO-LOCK NO-ERROR.
IF AVAILABLE htparam THEN param-561 = TRIM(htparam.fchar).
IF param-561 NE "" THEN
DO:
    mxtime-dayuse = INTEGER(SUBSTR(param-561, 1, 2)) * 3600 
        + INTEGER(SUBSTR(param-561, 4, 2)) * 60.
END.
/*End FD*/

RUN disp-arlist.
/************************  PROCEDURE   **************************/ 
PROCEDURE disp-arlist: 
DEFINE VARIABLE do-it       AS LOGICAL  NO-UNDO.
DEFINE VARIABLE ROflag      AS LOGICAL  NO-UNDO.
DEFINE VARIABLE epreis      AS DECIMAL  NO-UNDO.
DEFINE VARIABLE qty         AS INTEGER  NO-UNDO.
DEFINE VARIABLE i           AS INTEGER  NO-UNDO.
DEFINE VARIABLE str         AS CHAR     NO-UNDO.
DEFINE VARIABLE contcode    AS CHAR     NO-UNDO.
DEFINE VARIABLE c           AS INTEGER.
DEFINE VARIABLE b           AS INTEGER.
DEFINE VARIABLE resline-remark AS CHARACTER NO-UNDO.
DEFINE VARIABLE rsv-remark AS CHARACTER NO-UNDO.
  
    FOR EACH abf-list:
        DELETE abf-list.
    END.

    FOR EACH res-line WHERE (res-line.resstatus NE 3 AND res-line.resstatus NE 2 
        AND res-line.resstatus NE 4 AND res-line.resstatus NE 8 
        AND res-line.resstatus NE 9 AND res-line.resstatus NE 10
        AND res-line.resstatus NE 12 AND res-line.resstatus NE 99) 
        AND res-line.active-flag LE /*EQ*/ 1
        AND ((res-line.ankunft /*LT*/ LE fdate AND res-line.abreise GE fdate) 
            OR (res-line.ankunft EQ fdate AND res-line.abreise EQ fdate 
            AND res-line.ankzeit LE mxtime-dayuse))
        AND res-line.l-zuordnung[3] LE 1 NO-LOCK,/*ragung res-line.l-zuordnung[3] EQ 0 */
        FIRST zikat-list WHERE zikat-list.zikatnr EQ res-line.zikatnr
            AND zikat-list.SELECTED NO-LOCK BY res-line.zinr:
        
        ASSIGN
            do-it  = NO
            ROflag = YES
            qty    = 0
        .

        /*FDL June 03, 2024 => Ticket 597829*/
        IF NOT incl-guarantee AND res-line.active-flag EQ 0 AND res-line.resstatus EQ 1 THEN NEXT.        

        IF incl-accom AND res-line.l-zuordnung[3] EQ 1 THEN DO:
            ASSIGN do-it = NO.
            FIND FIRST arrangement WHERE arrangement.arrangement = res-line.arrangement NO-LOCK NO-ERROR.
            IF AVAILABLE arrangement THEN DO:
                FOR EACH argt-line WHERE argt-line.argtnr = arrangement.argtnr NO-LOCK, 
                    FIRST artikel WHERE artikel.artnr = argt-line.argt-artnr 
                    AND artikel.departement = bfast-dept 
                    AND artikel.zwkum = bfast-artnr NO-LOCK BY argt-line.betrag DESCENDING :
                    ASSIGN
                        do-it  = YES
                        ROflag = NO
                        epreis = argt-line.betrag.  
                    LEAVE.
                END.
            END.      
        END.

        IF incl-accom AND res-line.l-zuordnung[3] EQ 0 THEN DO:
            ASSIGN do-it = NO.
            FIND FIRST arrangement WHERE arrangement.arrangement = res-line.arrangement NO-LOCK NO-ERROR.
            IF AVAILABLE arrangement THEN DO:
                FOR EACH argt-line WHERE argt-line.argtnr = arrangement.argtnr NO-LOCK, 
                    FIRST artikel WHERE artikel.artnr = argt-line.argt-artnr 
                    AND artikel.departement = bfast-dept 
                    AND artikel.zwkum = bfast-artnr NO-LOCK BY argt-line.betrag DESCENDING :
                    ASSIGN
                        do-it  = YES
                        ROflag = NO
                        epreis = argt-line.betrag.  
                    LEAVE.
                END.
            END.      
        END.
            
        IF res-line.l-zuordnung[3] = 0 THEN DO:
            IF (res-line.erwachs + res-line.kind1 + res-line.gratis + res-line.l-zuordnung[4]) = 0 THEN .
            ELSE
            DO:
               FIND FIRST arrangement WHERE arrangement.arrangement = res-line.arrangement NO-LOCK NO-ERROR.
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
                        LEAVE.
                    END.
                END.              
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
            DO:
                FIND FIRST reslin-queasy WHERE reslin-queasy.key = "argt-line" 
                    AND reslin-queasy.char1    = /*guest-pr.CODE*/ contcode
                    AND reslin-queasy.number1  = res-line.reserve-int
                    AND reslin-queasy.number2  = arrangement.argtnr
                    AND reslin-queasy.number3  = bfast-artnr 
                    AND reslin-queasy.resnr    = bfast-dept 
                    AND reslin-queasy.reslinnr = res-line.zikatnr
                    AND reslin-queasy.date1 LE fdate
                    AND reslin-queasy.date2 GE fdate 
                    AND reslin-queasy.deci1 GT 0 NO-LOCK NO-ERROR.
                IF NOT AVAILABLE reslin-queasy THEN
                DO:
                    FIND FIRST reslin-queasy WHERE reslin-queasy.key = "fargt-line" 
                        /*AND reslin-queasy.char1     = /*guest-pr.CODE*/ contcode */
                        AND reslin-queasy.number1   = bfast-dept
                        AND reslin-queasy.number2   = arrangement.argtnr
                        AND reslin-queasy.number3   = bfast-artnr 
                        AND reslin-queasy.resnr     = res-line.resnr 
                        AND reslin-queasy.reslinnr  = res-line.reslinnr
                        AND reslin-queasy.date1 LE fdate
                        AND reslin-queasy.date2 GE fdate 
                        AND reslin-queasy.deci1 GT 0 NO-LOCK NO-ERROR.            
                END.
            END.        
        
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
            FIND FIRST guest WHERE guest.gastnr = res-line.gastnrmember NO-LOCK.
            FIND FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK.
            /*FIND FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr NO-LOCK.*/      
            
            /*FIND FIRST segment WHERE segment.segmentcode = res-line.argt-typ NO-LOCK NO-ERROR.*/
            /*FDL april 16, 2024 => Ticket #98B8C0*/
            FIND FIRST segment WHERE segment.segmentcode = reservation.segmentcode NO-LOCK NO-ERROR. 
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
                abf-list.kurzbez     = zikat-list.kurzbez
                abf-list.erwachs     = abf-list.erwachs + qty
                abf-list.gastnr      = res-line.gastnr
                abf-list.resname     = reservation.NAME          
                /*abf-list.comments    = reservation.bemerk*/                  
                abf-list.zipreis     = res-line.zipreis 
                abf-list.id          = reservation.useridanlage.                        
            
            /*FDL april 16, 2024 => Ticket #98B8C0*/
            IF AVAILABLE segment THEN abf-list.bezeich = segment.bezeich.

            rsv-remark = reservation.bemerk.
            rsv-remark = REPLACE(rsv-remark,CHR(10),"").
            rsv-remark = REPLACE(rsv-remark,CHR(13),"").
            rsv-remark = REPLACE(rsv-remark,"~n","").
            rsv-remark = REPLACE(rsv-remark,"\n","").
            rsv-remark = REPLACE(rsv-remark,"~r","").
            rsv-remark = REPLACE(rsv-remark,"~r~n","").
            rsv-remark = REPLACE(rsv-remark,"&nbsp;"," ").
            rsv-remark = REPLACE(rsv-remark,"</p>","</p></p>").
            rsv-remark = REPLACE(rsv-remark,"</p>",CHR(13)).
            rsv-remark = REPLACE(rsv-remark,"<BR>",CHR(13)).
            rsv-remark = REPLACE(rsv-remark,"<li>","").
            rsv-remark = REPLACE(rsv-remark,"</li>",CHR(13)).
            rsv-remark = REPLACE(rsv-remark,"<div>","").
            rsv-remark = REPLACE(rsv-remark,"</div>",CHR(13)).
            rsv-remark = REPLACE(rsv-remark,CHR(10) + CHR(13),"").
        
            IF LENGTH(rsv-remark) LT 3 THEN rsv-remark = REPLACE(rsv-remark,CHR(32),"").
            IF LENGTH(rsv-remark) LT 3 THEN rsv-remark = "".
            IF rsv-remark EQ ? THEN rsv-remark = "".

            abf-list.comments = rsv-remark.
            rsv-remark = "".
            
            resline-remark = res-line.bemerk.
            resline-remark = REPLACE(resline-remark,CHR(10),"").
            resline-remark = REPLACE(resline-remark,CHR(13),"").
            resline-remark = REPLACE(resline-remark,"~n","").
            resline-remark = REPLACE(resline-remark,"\n","").
            resline-remark = REPLACE(resline-remark,"~r","").
            resline-remark = REPLACE(resline-remark,"~r~n","").
            resline-remark = REPLACE(resline-remark,"&nbsp;"," ").
            resline-remark = REPLACE(resline-remark,"</p>","</p></p>").
            resline-remark = REPLACE(resline-remark,"</p>",CHR(13)).
            resline-remark = REPLACE(resline-remark,"<BR>",CHR(13)).
            resline-remark = REPLACE(resline-remark,"<li>","").
            resline-remark = REPLACE(resline-remark,"</li>",CHR(13)).
            resline-remark = REPLACE(resline-remark,"<div>","").
            resline-remark = REPLACE(resline-remark,"</div>",CHR(13)).
            resline-remark = REPLACE(resline-remark,CHR(10) + CHR(13),"").

            IF LENGTH(resline-remark) LT 3 THEN resline-remark = REPLACE(resline-remark,CHR(32),"").
            IF LENGTH(resline-remark) LT 3 THEN resline-remark = "".
            IF resline-remark EQ ? THEN resline-remark = "".

            abf-list.bemerk = resline-remark.
                        
            IF abf-list.comments NE "" THEN abf-list.comments = abf-list.comments + CHR(10).
            abf-list.comments = abf-list.comments + /*res-line.bemerk*/ resline-remark.
            resline-remark = "".
            /*END*/

            IF NOT ROflag THEN abf-list.kind1 = abf-list.kind1 + res-line.l-zuordnung[4].
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
                abf-list.nation1          = guest.nation1.
                abf-list.mobil-telefon    = guest.mobil-telefon. /*gerald 100221*/
            END.
            /*ragung*/
            IF res-line.resstatus EQ 11 AND res-line.l-zuordnung[3] EQ 0 THEN ASSIGN abf-list.NAME =  abf-list.NAME + " *".
            IF res-line.resstatus EQ 11 AND res-line.l-zuordnung[3] EQ 1 THEN ASSIGN abf-list.NAME =  abf-list.NAME + " **".
            IF res-line.resstatus EQ 13 AND res-line.l-zuordnung[3] EQ 0 THEN ASSIGN abf-list.NAME =  abf-list.NAME + " *".
            IF res-line.resstatus EQ 13 AND res-line.l-zuordnung[3] EQ 1 THEN ASSIGN abf-list.NAME =  abf-list.NAME + " **".
            /*end*/
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

