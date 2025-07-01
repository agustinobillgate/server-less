/*FT 050514 rapikan tampilan*/
DEFINE TEMP-TABLE complig-list 
  FIELD resnr           AS INTEGER
  FIELD reslinnr        AS INTEGER
  FIELD datum           AS DATE LABEL "Date" 
  FIELD zinr            LIKE zimmer.zinr LABEL "RmNo" 
  FIELD reserve-nm      AS CHAR FORMAT "x(32)" LABEL "Reserve Name"
  FIELD name            AS CHAR FORMAT "x(32)" LABEL "Guest Name" 
  FIELD zimmeranz       AS INTEGER FORMAT ">>>" LABEL "Qty" 
  FIELD pax             AS INTEGER FORMAT ">>>9" LABEL "Pax" 
  FIELD ankunft         AS DATE LABEL "Arrival" 
  FIELD abreise         AS DATE LABEL "Departure" 
  FIELD segm            AS CHAR FORMAT "x(13) " LABEL "Segment Code" 
  FIELD rstatus         AS CHAR FORMAT "x(8)"   LABEL "Status" 
  FIELD remark          AS CHAR FORMAT "x(80)"  LABEL "Remark" 
  FIELD rname           AS CHAR
  FIELD fsort           AS INTEGER
  FIELD fdatum          AS DATE
  
  FIELD vip             AS CHAR
  FIELD nat             AS CHAR
  FIELD rmtype          AS CHAR
  FIELD rm-rate         AS DECIMAL
  FIELD rate-code       AS CHAR
  FIELD argt            AS CHAR
  FIELD bill-detail     AS CHAR
  FIELD usr-id          AS CHAR
  FIELD gratis          AS INTEGER FORMAT "99". 

DEFINE INPUT PARAMETER pvILanguage      AS INTEGER              NO-UNDO.
DEFINE INPUT PARAMETER from-date        AS DATE.
DEFINE INPUT PARAMETER to-date          AS DATE.
DEFINE INPUT PARAMETER sorttype         AS INTEGER.
DEFINE INPUT PARAMETER bonus-flag       AS INTEGER.
DEFINE INPUT PARAMETER segmentcode      AS INTEGER.

DEFINE OUTPUT PARAMETER TABLE FOR complig-list.

DEFINE VARIABLE do-it AS LOGICAL NO-UNDO.
DEF VAR last-sort AS CHAR INITIAL "".
DEF VAR int-sort AS INTEGER .

DEFINE VARIABLE t-anz           AS INTEGER INITIAL 0. 
DEFINE VARIABLE t-pax           AS INTEGER INITIAL 0. 
DEFINE VARIABLE tot-anz         AS INTEGER INITIAL 0. 
DEFINE VARIABLE tot-pax         AS INTEGER INITIAL 0. 

DEFINE VARIABLE ci-date         AS DATE. 
DEFINE VARIABLE datum           AS DATE. 

DEFINE VARIABLE new-contrate AS LOGICAL INITIAL NO. 
DEFINE VARIABLE bonus-array  AS LOGICAL EXTENT 2500 INITIAL NO. 
DEFINE VARIABLE vip-nr       AS INTEGER EXTENT 10 NO-UNDO. 
DEFINE STREAM s1. 

DEFINE WORKFILE cl-list 
  FIELD segm AS INTEGER 
  FIELD bezeich AS CHAR FORMAT "x(16)" 
  FIELD zimmeranz AS INTEGER 
  FIELD pax AS INTEGER. 
 

 
{supertransBL.i} 
DEF VAR lvCAREA AS CHAR INITIAL "compli-glist". 


/*************************************************************************************************/

FIND FIRST htparam WHERE htparam.paramnr = 87 NO-LOCK. 
ci-date = htparam.fdate. 


FIND FIRST htparam WHERE paramnr = 700 NO-LOCK. 
vip-nr[1] = htparam.finteger. 
FIND FIRST htparam WHERE paramnr = 701 NO-LOCK. 
vip-nr[2] = htparam.finteger. 
FIND FIRST htparam WHERE paramnr =  702 NO-LOCK. 
vip-nr[3] = htparam.finteger. 
FIND FIRST htparam WHERE paramnr = 703 NO-LOCK. 
vip-nr[4] = htparam.finteger. 
FIND FIRST htparam WHERE paramnr = 704 NO-LOCK. 
vip-nr[5] = htparam.finteger. 
FIND FIRST htparam WHERE paramnr = 705 NO-LOCK. 
vip-nr[6] = htparam.finteger. 
FIND FIRST htparam WHERE paramnr = 706 NO-LOCK. 
vip-nr[7] = htparam.finteger. 
FIND FIRST htparam WHERE paramnr = 707 NO-LOCK. 
vip-nr[8] = htparam.finteger. 
FIND FIRST htparam WHERE paramnr = 708 NO-LOCK. 
vip-nr[9] = htparam.finteger. 
FIND FIRST htparam WHERE paramnr = 712 NO-LOCK. 
vip-nr[10] = htparam.finteger. 

int-sort = 0.

FOR EACH complig-list: 
    DELETE complig-list. 
END. 

FOR EACH cl-list :
    DELETE cl-list.
END.

ASSIGN
tot-anz = 0 
tot-pax = 0
. 

DO datum = from-date TO to-date: 
    t-anz = 0. 
    t-pax = 0. 
    
    IF datum LT ci-date THEN
    DO:
        IF segmentcode NE 0 THEN DO:
            IF sorttype = 0 THEN
            FOR EACH genstat WHERE genstat.datum = datum AND 
                /*(genstat.gratis + genstat.erwachs) GT 0 NO-LOCK,*/
                genstat.zipreis = 0 AND 
                genstat.resstatus = 6 AND 
                genstat.res-logic[2] AND
                genstat.segmentcode = segmentcode NO-LOCK, 
                FIRST segment WHERE segment.segmentcode = genstat.segmentcode NO-LOCK,
                FIRST guest WHERE guest.gastnr = genstat.gastnr NO-LOCK BY guest.NAME
                BY genstat.zinr BY genstat.resstatus:
                IF bonus-flag = 0 THEN do-it = NOT genstat.res-logic[3].
                ELSE IF bonus-flag = 1 THEN do-it = YES.
                ELSE IF bonus-flag = 2 THEN do-it = genstat.res-logic[3].
                IF do-it THEN RUN create-list2.
            END.   
            ELSE IF sorttype = 1 THEN
            FOR EACH genstat WHERE genstat.datum = datum AND 
                /*(genstat.gratis + genstat.erwachs) GT 0 NO-LOCK,*/
                genstat.zipreis = 0 AND 
                genstat.resstatus = 6 AND
                genstat.res-logic[2] AND
                genstat.segmentcode = segmentcode NO-LOCK, 
                FIRST segment WHERE segment.segmentcode = genstat.segmentcode NO-LOCK,
                FIRST guest WHERE guest.gastnr = genstat.gastnrmember NO-LOCK BY guest.NAME:
                IF bonus-flag = 0 THEN do-it = NOT genstat.res-logic[3].
                ELSE IF bonus-flag = 1 THEN do-it = YES.
                ELSE IF bonus-flag = 2 THEN do-it = genstat.res-logic[3].
                IF do-it THEN RUN create-list2.
            END.    
            ELSE IF sorttype = 2 THEN
            FOR EACH genstat WHERE genstat.datum = datum AND 
                /*(genstat.gratis + genstat.erwachs) GT 0 NO-LOCK,*/
                genstat.zipreis = 0 AND 
                genstat.resstatus = 6 AND 
                genstat.res-logic[2] AND
                genstat.segmentcode = segmentcode NO-LOCK, 
                FIRST segment WHERE segment.segmentcode = genstat.segmentcode NO-LOCK,
                FIRST guest WHERE guest.gastnr = genstat.gastnr NO-LOCK,
                FIRST zimkateg WHERE zimkateg.zikatnr = genstat.zikatnr NO-LOCK BY genstat.zikatnr BY guest.NAME
                BY genstat.zinr BY genstat.resstatus:
                IF bonus-flag = 0 THEN do-it = NOT genstat.res-logic[3].
                ELSE IF bonus-flag = 1 THEN do-it = YES.
                ELSE IF bonus-flag = 2 THEN do-it = genstat.res-logic[3].
                IF do-it THEN RUN create-list2.
            END.   
        END.
        ELSE DO:
            IF sorttype = 0 THEN
            FOR EACH genstat WHERE genstat.datum = datum AND 
                /*(genstat.gratis + genstat.erwachs) GT 0 NO-LOCK,*/
                genstat.zipreis = 0 AND 
                genstat.resstatus = 6 AND 
                genstat.res-logic[2] NO-LOCK, 
                FIRST segment WHERE segment.segmentcode = genstat.segmentcode NO-LOCK,
                FIRST guest WHERE guest.gastnr = genstat.gastnr NO-LOCK BY guest.NAME
                BY genstat.zinr BY genstat.resstatus:
                IF bonus-flag = 0 THEN do-it = NOT genstat.res-logic[3].
                ELSE IF bonus-flag = 1 THEN do-it = YES.
                ELSE IF bonus-flag = 2 THEN do-it = genstat.res-logic[3].
                IF do-it THEN RUN create-list2.
            END.   
            ELSE IF sorttype = 1 THEN
            FOR EACH genstat WHERE genstat.datum = datum AND 
                /*(genstat.gratis + genstat.erwachs) GT 0 NO-LOCK,*/
                genstat.zipreis = 0 AND 
                genstat.resstatus = 6 AND
                genstat.res-logic[2] NO-LOCK, 
                FIRST segment WHERE segment.segmentcode = genstat.segmentcode NO-LOCK,
                FIRST guest WHERE guest.gastnr = genstat.gastnrmember NO-LOCK BY guest.NAME:
                IF bonus-flag = 0 THEN do-it = NOT genstat.res-logic[3].
                ELSE IF bonus-flag = 1 THEN do-it = YES.
                ELSE IF bonus-flag = 2 THEN do-it = genstat.res-logic[3].
                IF do-it THEN RUN create-list2.
            END. 
            ELSE IF sorttype = 2 THEN
            FOR EACH genstat WHERE genstat.datum = datum AND 
                /*(genstat.gratis + genstat.erwachs) GT 0 NO-LOCK,*/
                genstat.zipreis = 0 AND 
                genstat.resstatus = 6 AND 
                genstat.res-logic[2] NO-LOCK, 
                FIRST segment WHERE segment.segmentcode = genstat.segmentcode NO-LOCK,
                FIRST guest WHERE guest.gastnr = genstat.gastnr NO-LOCK,
                FIRST zimkateg WHERE zimkateg.zikatnr = genstat.zikatnr NO-LOCK BY genstat.zikatnr BY guest.NAME
                BY genstat.zinr BY genstat.resstatus:
                IF bonus-flag = 0 THEN do-it = NOT genstat.res-logic[3].
                ELSE IF bonus-flag = 1 THEN do-it = YES.
                ELSE IF bonus-flag = 2 THEN do-it = genstat.res-logic[3].
                IF do-it THEN RUN create-list2.
            END.   
        END.                            
    END.
    ELSE
    DO:
      IF segmentcode NE 0 THEN DO:
          IF sorttype = 0 THEN
          DO:
            FOR EACH res-line WHERE 
              res-line.active-flag LE 1
              AND (res-line.resstatus LE 2 OR res-line.resstatus = 5 
                   OR res-line.resstatus = 6) 
              AND res-line.ankunft LE datum AND res-line.abreise GT datum
              /* AND (res-line.gratis + res-line.erwachs) GT 0 */ NO-LOCK, 
              FIRST reservation WHERE reservation.resnr = res-line.resnr
                AND reservation.segmentcode = segmentcode NO-LOCK, 
              FIRST segment WHERE segment.segmentcode = reservation.segmentcode NO-LOCK,
              FIRST guest WHERE guest.gastnr = res-line.gastnr NO-LOCK BY guest.NAME: 
              RUN create-list1.          
            END. 
          END.
          ELSE
            FOR EACH res-line WHERE 
              res-line.active-flag LE 1
              AND (res-line.resstatus LE 2 OR res-line.resstatus = 5 
                   OR res-line.resstatus = 6) 
              AND res-line.ankunft LE datum AND res-line.abreise GT datum
              /* AND (res-line.gratis + res-line.erwachs) GT 0 */ NO-LOCK, 
              FIRST reservation WHERE reservation.resnr = res-line.resnr 
                AND reservation.segmentcode = segmentcode NO-LOCK, 
              FIRST segment WHERE segment.segmentcode = reservation.segmentcode NO-LOCK,
              FIRST guest WHERE guest.gastnr = res-line.gastnr NO-LOCK BY res-line.NAME: 
              RUN create-list1.
            END. 
      END.
      ELSE DO:
          IF sorttype = 0 THEN
          DO:
            FOR EACH res-line WHERE 
              res-line.active-flag LE 1
              AND (res-line.resstatus LE 2 OR res-line.resstatus = 5 
                   OR res-line.resstatus = 6) 
              AND res-line.ankunft LE datum AND res-line.abreise GT datum
              /* AND (res-line.gratis + res-line.erwachs) GT 0 */ NO-LOCK, 
              FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
              FIRST segment WHERE segment.segmentcode = reservation.segmentcode NO-LOCK,
              FIRST guest WHERE guest.gastnr = res-line.gastnr NO-LOCK BY guest.NAME: 
              RUN create-list1.          
            END. 
          END.
          ELSE
            FOR EACH res-line WHERE 
              res-line.active-flag LE 1
              AND (res-line.resstatus LE 2 OR res-line.resstatus = 5 
                   OR res-line.resstatus = 6) 
              AND res-line.ankunft LE datum AND res-line.abreise GT datum
              /* AND (res-line.gratis + res-line.erwachs) GT 0 */ NO-LOCK, 
              FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
              FIRST segment WHERE segment.segmentcode = reservation.segmentcode NO-LOCK,
              FIRST guest WHERE guest.gastnr = res-line.gastnr NO-LOCK BY res-line.NAME: 
              RUN create-list1.
            END. 
    
      END.  
    END.
    
    int-sort  = int-sort + 1.
    IF t-anz NE 0 AND t-pax NE 0 THEN   
    DO:
        CREATE  complig-list. 
        ASSIGN 
          complig-list.name = "T O T A L" 
          complig-list.zimmeranz = t-anz 
          complig-list.pax = t-pax
          complig-list.fdatum = datum
          complig-list.fsort = int-sort
          complig-list.zinr = "".  /*FT 050514*/ 
    END.
    
    
    /*int-sort  = int-sort + 1.
    create complig-list. 
    ASSIGN 
      complig-list.fdatum = datum
      complig-list.fsort = int-sort
      complig-list.zinr = "".  FT 050514*/ 
    
    int-sort  = int-sort + 1.
END. 

/*int-sort  = int-sort + 1.
create complig-list. 
ASSIGN 
  complig-list.fsort = int-sort
  complig-list.zinr = "".  FT 050514*/ 

int-sort  = int-sort + 1.
CREATE complig-list. 
complig-list.name = translateExtended ("SUMMARY BY SEGMENTCODE",lvCAREA,""). 
complig-list.rname = "SUMMARY BY SEGMENTCODE". 
complig-list.fsort = int-sort.
complig-list.zinr = "".  /*FT 050514*/ 
FOR EACH cl-list: 
int-sort  = int-sort + 1.
CREATE complig-list. 
complig-list.name = cl-list.bezeich. 
complig-list.zimmeranz = cl-list.zimmeranz. 
complig-list.pax = cl-list.pax. 
tot-anz = tot-anz + cl-list.zimmeranz. 
tot-pax = tot-pax + cl-list.pax.
complig-list.fsort = int-sort.
complig-list.zinr = "".  /*FT 050514*/ 
END. 


int-sort  = int-sort + 1.
CREATE complig-list. 
complig-list.name = "TOTAL". 
complig-list.zimmeranz = tot-anz. 
complig-list.pax = tot-pax.
complig-list.fsort = int-sort. 
complig-list.zinr = "".  /*FT*/ 


/*************************************************************************************************/
PROCEDURE create-list2:
    DEFINE VARIABLE loopi AS INTEGER NO-UNDO.
    DEFINE BUFFER gbuff FOR guest.
    DEFINE BUFFER buf-guest FOR guest.

    DEFINE VARIABLE s AS CHAR NO-UNDO.

    CREATE complig-list.
    ASSIGN 
        complig-list.datum      = genstat.datum
        complig-list.zinr       = genstat.zinr
        complig-list.pax        = genstat.erwachs + genstat.gratis
        complig-list.ankunft    = genstat.res-date[1]
        complig-list.abreise    = genstat.res-date[2]
        complig-list.segm       = segment.bezeich
        complig-list.gratis     = genstat.gratis
        t-pax = t-pax + genstat.erwachs + genstat.gratis
        complig-list.fsort = int-sort
        complig-list.resnr = genstat.resnr.

    /*ITA 25Sept 2017*/
    ASSIGN complig-list.rm-rate = genstat.zipreis
           complig-list.argt    = genstat.argt.

    IF genstat.res-char[2] MATCHES("*$CODE$*") THEN
    DO:
          s = SUBSTR(genstat.res-char[2],(INDEX(genstat.res-char[2],"$CODE$") + 6)).
          complig-list.rate-code = TRIM(ENTRY(1, s, ";")).
    END.
    ELSE complig-list.rate-code = "UNKNOWN".

    FIND FIRST reservation WHERE reservation.resnr = genstat.resnr NO-LOCK NO-ERROR.
    IF AVAILABLE reservation THEN complig-list.usr-id = reservation.useridanlage.
        
    /* Malik Serverless 483, change query guest to buf-guest 
    FIND FIRST guest WHERE guest.gastnr = genstat.gastnrmember NO-LOCK NO-ERROR.
    IF AVAILABLE guest THEN 
    DO:
        FIND FIRST guestseg WHERE guestseg.gastnr = guest.gastnr AND 
          (guestseg.segmentcode = vip-nr[1] OR 
           guestseg.segmentcode = vip-nr[2] OR 
           guestseg.segmentcode = vip-nr[3] OR 
           guestseg.segmentcode = vip-nr[4] OR 
           guestseg.segmentcode = vip-nr[5] OR 
           guestseg.segmentcode = vip-nr[6] OR 
           guestseg.segmentcode = vip-nr[7] OR 
           guestseg.segmentcode = vip-nr[8] OR 
           guestseg.segmentcode = vip-nr[9] OR 
           guestseg.segmentcode = vip-nr[10]) NO-LOCK NO-ERROR.
        IF AVAILABLE guestseg THEN
        DO:
          FIND FIRST segment WHERE segment.segmentcode = guestseg.segmentcode NO-LOCK NO-ERROR.
          IF AVAILABLE segment THEN ASSIGN complig-list.vip = segment.bezeich.
        END.
        ASSIGN complig-list.nat = guest.nation1.  
    END.*/
    FIND FIRST buf-guest WHERE buf-guest.gastnr = genstat.gastnrmember NO-LOCK NO-ERROR.
    IF AVAILABLE buf-guest THEN 
    DO:
        FIND FIRST guestseg WHERE guestseg.gastnr = buf-guest.gastnr AND 
          (guestseg.segmentcode = vip-nr[1] OR 
           guestseg.segmentcode = vip-nr[2] OR 
           guestseg.segmentcode = vip-nr[3] OR 
           guestseg.segmentcode = vip-nr[4] OR 
           guestseg.segmentcode = vip-nr[5] OR 
           guestseg.segmentcode = vip-nr[6] OR 
           guestseg.segmentcode = vip-nr[7] OR 
           guestseg.segmentcode = vip-nr[8] OR 
           guestseg.segmentcode = vip-nr[9] OR 
           guestseg.segmentcode = vip-nr[10]) NO-LOCK NO-ERROR.
        IF AVAILABLE guestseg THEN
        DO:
          FIND FIRST segment WHERE segment.segmentcode = guestseg.segmentcode NO-LOCK NO-ERROR.
          IF AVAILABLE segment THEN ASSIGN complig-list.vip = segment.bezeich.
        END.
        ASSIGN complig-list.nat = buf-guest.nation1. 
    END.

    FIND FIRST zimkateg WHERE zimkateg.zikatnr = genstat.zikatnr NO-LOCK NO-ERROR.
    IF AVAILABLE zimkateg THEN ASSIGN complig-list.rmtype = zimkateg.kurzbez.

    /*end*/

    IF genstat.resstatus = 6 THEN ASSIGN complig-list.zimmeranz = 1
         t-anz = t-anz + 1.

    IF genstat.resstatus EQ 6 THEN 
        complig-list.rstatus = translateExtended ("In-House", lvCAREA,""). 
    ELSE IF genstat.resstatus EQ 13 THEN 
        complig-list.rstatus = translateExtended ("Rm Sharer", lvCAREA,""). 
    ELSE complig-list.rstatus = translateExtended ("Departed", lvCAREA,""). 

    /*ITA 270617 add reservasi remark*/
    FIND FIRST res-line WHERE res-line.resnr = genstat.resnr
        AND res-line.reslinnr = genstat.res-int[1] NO-LOCK NO-ERROR.
    IF AVAILABLE res-line THEN DO:
        DO loopi = 1 TO LENGTH(res-line.bemerk): 
            IF SUBSTR(res-line.bemerk,loopi,1) NE CHR(10) THEN 
                complig-list.remark = complig-list.remark + SUBSTR(res-line.bemerk,loopi,1). 
            ELSE complig-list.remark = complig-list.remark + " ". 
        END. 
    END.

    FIND FIRST gbuff WHERE gbuff.gastnr = genstat.gastnrmember NO-LOCK NO-ERROR.
    IF AVAILABLE gbuff THEN
        complig-list.NAME = gbuff.NAME + ", " + gbuff.vorname1 + gbuff.anredefirma
            + " " + gbuff.anrede1.

    FIND FIRST reservation WHERE reservation.resnr = genstat.resnr NO-LOCK NO-ERROR.
    IF AVAILABLE reservation THEN complig-list.reserve-nm = reservation.NAME.
    /*
    IF sorttype = 0 THEN
    DO:
        FIND FIRST gbuff WHERE gbuff.gastnr = genstat.gastnrmember NO-LOCK NO-ERROR.
        IF AVAILABLE gbuff THEN
            complig-list.NAME = gbuff.NAME + ", " + gbuff.vorname1 + gbuff.anredefirma
                + " " + gbuff.anrede1
            .
        complig-list.reserve-nm = guest.NAME + ", " + guest.vorname1 + guest.anredefirma
            + " " + guest.anrede1.
    END.
    ELSE
    DO:
        FIND FIRST gbuff WHERE gbuff.gastnr = genstat.gastnr NO-LOCK NO-ERROR.
        IF AVAILABLE gbuff THEN
        complig-list.reserve-NM = gbuff.NAME + ", " + gbuff.vorname1 + gbuff.anredefirma
            + " " + gbuff.anrede1
        .
        complig-list.NAME = guest.NAME + ", " + guest.vorname1 + guest.anredefirma
            + " " + guest.anrede1.
    END.
    */
    FIND FIRST cl-list WHERE cl-list.segm = genstat.segmentcode 
      NO-ERROR. 
    IF NOT AVAILABLE cl-list THEN 
    DO: 
      CREATE cl-list. 
      cl-list.segm = genstat.segmentcode. 
      cl-list.bezeich = ENTRY(1, segment.bezeich, "$$0"). 
    END. 
    IF genstat.resstatus = 6 THEN cl-list.zimmeranz = cl-list.zimmeranz + 1.
    cl-list.pax = cl-list.pax + genstat.erwachs + genstat.gratis.
END.

PROCEDURE create-list1:
    DEF VAR fixed-rate AS LOGICAL.
    DEF VAR rate-found AS LOGICAL.
    DEF VAR ebdisc-flag AS LOGICAL. 
    DEF VAR kbdisc-flag AS LOGICAL. 
    DEF VARIABLE early-flag         AS LOGICAL NO-UNDO.
    DEF VARIABLE kback-flag         AS LOGICAL NO-UNDO.
    DEF VARIABLE rate               AS DECIMAL NO-UNDO.
    DEF VARIABLE do-it              AS LOGICAL NO-UNDO.
    DEF VARIABLE it-exist           AS LOGICAL NO-UNDO.
    DEFINE VARIABLE pax             AS INTEGER NO-UNDO.
    DEFINE VARIABLE curr-zikatnr    AS INTEGER NO-UNDO.
    DEF VARIABLE i                  AS INTEGER NO-UNDO. 
    DEF VARIABLE curr-i             AS INTEGER INITIAL 0    NO-UNDO.
    DEF VARIABLE rm-rate            AS DECIMAL NO-UNDO.
    DEFINE VARIABLE datum-ankunft   AS INTEGER NO-UNDO. /*Alder - Serverless - Issue 483*/

    DEFINE VARIABLE loopi AS INTEGER NO-UNDO.
    DEFINE VARIABLE str   AS CHAR    NO-UNDO.
    DEFINE BUFFER buf-guest FOR guest.

      ASSIGN
        fixed-rate = NO
        rate-found = NO
        ebdisc-flag = res-line.zimmer-wunsch MATCHES ("*ebdisc*")
        kbdisc-flag = res-line.zimmer-wunsch MATCHES ("*kbdisc*")
      .
      IF res-line.l-zuordnung[1] NE 0 THEN curr-zikatnr = res-line.l-zuordnung[1]. 
      ELSE curr-zikatnr = res-line.zikatnr. 

      FIND FIRST guest-pr WHERE guest-pr.gastnr = res-line.gastnr 
          NO-LOCK NO-ERROR. 

      /*Alder - Serverless - Issue 483 - Start*/
      ASSIGN datum-ankunft = datum - res-line.ankunft.
      FIND FIRST arrangement WHERE arrangement.arrangement EQ res-line.arrangement NO-LOCK NO-ERROR.
      IF AVAILABLE arrangement THEN
      DO:
          RUN check-bonus.
          curr-i  = datum-ankunft + 1.
          rm-rate = res-line.zipreis.
      END.
      
      FIND FIRST reslin-queasy WHERE reslin-queasy.key EQ "arrangement" 
          AND reslin-queasy.resnr EQ res-line.resnr 
          AND reslin-queasy.reslinnr EQ res-line.reslinnr 
          /*AND datum GE reslin-queasy.date1*/
          /*AND datum LE reslin-queasy.date2*/
          AND reslin-queasy.date1 LE datum
          AND reslin-queasy.date2 GE datum
          NO-LOCK NO-ERROR. 
      
      IF AVAILABLE reslin-queasy THEN 
      DO: 
        fixed-rate = YES. 
        rm-rate = reslin-queasy.deci1. 
        IF reslin-queasy.number3 NE 0 THEN pax = reslin-queasy.number3. 
        IF reslin-queasy.char1 NE "" THEN 
        DO:
          FIND FIRST arrangement WHERE arrangement.arrangement EQ reslin-queasy.char1 NO-LOCK NO-ERROR.
          IF AVAILABLE arrangement THEN
          DO:
              RUN check-bonus.
            /*RUN usr-prog1(datum, INPUT-OUTPUT rm-rate, OUTPUT it-exist). */
          END.
        END.
      END.
      /*Alder - Serverless - Issue 483 - End*/
      ELSE 
      DO: 
         
        /*RUN usr-prog1(datum, INPUT-OUTPUT rm-rate, OUTPUT it-exist). */
        IF NOT it-exist THEN 
        DO: 
          IF AVAILABLE guest-pr THEN 
          DO: 
            FIND FIRST queasy WHERE queasy.key = 18 AND queasy.number1 
                = res-line.reserve-int NO-LOCK NO-ERROR. 

            IF new-contrate THEN
            DO:
              RUN ratecode-rate.p(ebdisc-flag, kbdisc-flag, res-line.resnr, 
                res-line.reslinnr,
                guest-pr.CODE, ?, datum, res-line.ankunft,
                res-line.abreise, res-line.reserve-int, arrangement.argtnr,
                curr-zikatnr, res-line.erwachs, res-line.kind1, res-line.kind2,
                res-line.reserve-dec, res-line.betriebsnr, OUTPUT rate-found,
                OUTPUT rate, OUTPUT early-flag, OUTPUT kback-flag).
              IF rate-found THEN rm-rate = rate.
            END.
            ELSE
            DO:
              RUN pricecod-rate.p(res-line.resnr, res-line.reslinnr,
                guest-pr.CODE, datum, res-line.ankunft, res-line.abreise, 
                res-line.reserve-int, arrangement.argtnr, curr-zikatnr, 
                res-line.erwachs, res-line.kind1, res-line.kind2,
                res-line.reserve-dec, res-line.betriebsnr, 
                OUTPUT rate, OUTPUT rate-found).
              /*RUN usr-prog2(datum, INPUT-OUTPUT rate, OUTPUT it-exist).*/
              IF it-exist THEN rate-found = YES.
              IF rate-found THEN rm-rate = rate.
              IF NOT it-exist AND bonus-array[curr-i] = YES THEN rm-rate = 0.  
            END.  /* old contract rate  */
          END.    /* available guest-pr */

          
          IF NOT rate-found THEN
          DO:  
            IF bonus-array[curr-i] = YES THEN rm-rate = 0.  
          END.   /* publish rate   */  
        END.     /* not exist      */ 
      END.       /* not fixed rate */
       
      IF bonus-flag = 0 THEN do-it = (rm-rate = 0) AND (res-line.gratis GT 0).
      ELSE IF bonus-flag = 1 THEN do-it = (rm-rate = 0).
      ELSE IF bonus-flag = 2 THEN
        do-it = (rm-rate = 0) AND (res-line.erwachs GT 0).
      IF do-it THEN 
      DO:         
            
        CREATE complig-list. 
        ASSIGN 
          complig-list.resnr = res-line.resnr
          complig-list.reslinnr = res-line.reslinnr
          complig-list.datum = datum 
          complig-list.zinr = res-line.zinr 
          complig-list.name = res-line.name 
          complig-list.pax = res-line.erwachs + res-line.gratis 
          complig-list.ankunft = res-line.ankunft 
          complig-list.abreise = res-line.abreise 
          complig-list.segm = ENTRY(1, segment.bezeich, "$$0") 
          complig-list.fsort = int-sort
          complig-list.gratis = res-line.gratis.

        /*ITA 25Sept 2017*/
        ASSIGN complig-list.rm-rate = res-line.zipreis
               complig-list.argt    = res-line.arrangement .
    
        DO loopi = 1 TO NUM-ENTRIES(res-line.zimmer-wunsch,";") - 1:
            str = ENTRY(loopi, res-line.zimmer-wunsch, ";").
            IF SUBSTR(str,1,6) = "$CODE$" THEN 
            DO:
              complig-list.rate-code  = SUBSTR(str,7).
              LEAVE.
            END.
        END.
    
        FIND FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK NO-ERROR.
        IF AVAILABLE reservation THEN
        DO:
          complig-list.usr-id = reservation.useridanlage.
          complig-list.reserve-nm = reservation.NAME.
        END.
            
        /* Malik Serverless 483 change query from guest to buf-guest        
        FIND FIRST guest WHERE guest.gastnr = res-line.gastnrmember NO-LOCK NO-ERROR.
        IF AVAILABLE guest THEN 
        DO:
            FIND FIRST guestseg WHERE guestseg.gastnr = guest.gastnr AND 
              (guestseg.segmentcode = vip-nr[1] OR 
               guestseg.segmentcode = vip-nr[2] OR 
               guestseg.segmentcode = vip-nr[3] OR 
               guestseg.segmentcode = vip-nr[4] OR 
               guestseg.segmentcode = vip-nr[5] OR 
               guestseg.segmentcode = vip-nr[6] OR 
               guestseg.segmentcode = vip-nr[7] OR 
               guestseg.segmentcode = vip-nr[8] OR 
               guestseg.segmentcode = vip-nr[9] OR 
               guestseg.segmentcode = vip-nr[10]) NO-LOCK NO-ERROR.
            IF AVAILABLE guestseg THEN
            DO:
              FIND FIRST segment WHERE segment.segmentcode = guestseg.segmentcode NO-LOCK NO-ERROR.
              IF AVAILABLE segment THEN ASSIGN complig-list.vip = segment.bezeich.
            END.
            ASSIGN complig-list.nat = guest.nation1.  
        END.*/
        FIND FIRST buf-guest WHERE buf-guest.gastnr = res-line.gastnrmember NO-LOCK NO-ERROR.
        IF AVAILABLE buf-guest THEN 
        DO:
            FIND FIRST guestseg WHERE guestseg.gastnr = buf-guest.gastnr AND 
              (guestseg.segmentcode = vip-nr[1] OR 
               guestseg.segmentcode = vip-nr[2] OR 
               guestseg.segmentcode = vip-nr[3] OR 
               guestseg.segmentcode = vip-nr[4] OR 
               guestseg.segmentcode = vip-nr[5] OR 
               guestseg.segmentcode = vip-nr[6] OR 
               guestseg.segmentcode = vip-nr[7] OR 
               guestseg.segmentcode = vip-nr[8] OR 
               guestseg.segmentcode = vip-nr[9] OR 
               guestseg.segmentcode = vip-nr[10]) NO-LOCK NO-ERROR.
            IF AVAILABLE guestseg THEN
            DO:
              FIND FIRST segment WHERE segment.segmentcode = guestseg.segmentcode NO-LOCK NO-ERROR.
              IF AVAILABLE segment THEN ASSIGN complig-list.vip = segment.bezeich.
            END.
            ASSIGN complig-list.nat = buf-guest.nation1.  
        END.
    
       FIND FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr NO-LOCK NO-ERROR.
       IF AVAILABLE zimkateg THEN ASSIGN complig-list.rmtype = zimkateg.kurzbez.
       /*end*/

        IF res-line.resstatus NE 11 AND res-line.resstatus NE 13 THEN 
            complig-list.zimmeranz = res-line.zimmeranz. 
          
        /* Malik Serverless 483 comment useless code 
        FIND FIRST guest WHERE guest.gastnr = res-line.gastnr USE-INDEX gastnr_index
              NO-LOCK NO-ERROR.*/
        /*IF AVAILABLE guest THEN complig-list.reserve-nm = guest.NAME + ", " + guest.vorname1
            + guest.anredefirma + " " + guest.anrede1.*/
        DO i = 1 TO LENGTH(res-line.bemerk): 
            IF SUBSTR(res-line.bemerk,i,1) NE CHR(10) THEN 
                complig-list.remark = complig-list.remark + SUBSTR(res-line.bemerk,i,1). 
            ELSE complig-list.remark = complig-list.remark + " ". 
        END. 
        IF res-line.active-flag = 1 THEN complig-list.rstatus = "In-House". 
        ELSE IF res-line.active-flag = 0 THEN complig-list.rstatus = "Arival". 
        ELSE complig-list.rstatus = "Departed". 
        FIND FIRST cl-list WHERE cl-list.segm = reservation.segmentcode 
          NO-ERROR. 
        IF NOT AVAILABLE cl-list THEN 
        DO: 
          CREATE cl-list. 
          cl-list.segm = reservation.segmentcode. 
          cl-list.bezeich = ENTRY(1, segment.bezeich, "$$0"). 
        END. 
        IF (res-line.abreise GT datum) 
          OR ((res-line.abreise = datum) AND (res-line.active-flag = 1)) THEN 
        DO: 
          cl-list.zimmeranz = cl-list.zimmeranz + 1. 
          cl-list.pax = cl-list.pax + res-line.erwachs + res-line.gratis. 
          t-anz = t-anz + 1. 
          t-pax = t-pax + res-line.erwachs + res-line.gratis. 
        END. 
      END.
END.

PROCEDURE check-bonus: 
DEFINE VARIABLE i AS INTEGER. 
DEFINE VARIABLE j AS INTEGER INITIAL 1. 
DEFINE VARIABLE k AS INTEGER. 
DEFINE VARIABLE n AS INTEGER INITIAL 0. 
DEFINE VARIABLE stay AS INTEGER. 
DEFINE VARIABLE pay AS INTEGER. 
DEFINE VARIABLE num-bonus AS INTEGER INITIAL 0. 
 
  DO i = 1 TO 99:
    bonus-array[i] = NO.
  END.

  j = 1. 
  DO i = 1 TO 4: 
    stay = INTEGER(SUBSTR(arrangement.options, j, 2)). 
    pay  = INTEGER(SUBSTR(arrangement.options, j + 2, 2)). 
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
/*
PROCEDURE usr-prog1: 
DEFINE INPUT PARAMETER bill-date AS DATE. 
DEFINE INPUT-OUTPUT PARAMETER roomrate AS DECIMAL. 
DEFINE OUTPUT PARAMETER it-exist AS LOGICAL INITIAL NO. 
DEFINE VARIABLE prog-str AS CHAR INITIAL "". 
DEFINE VARIABLE i AS INTEGER. 
  FIND FIRST reslin-queasy WHERE reslin-queasy.key = "rate-prog" 
    AND reslin-queasy.number1 = resnr 
    AND reslin-queasy.number2 = 0 AND reslin-queasy.char1 = "" 
    AND reslin-queasy.reslinnr = 1 USE-INDEX argt_ix NO-LOCK NO-ERROR. 
  IF AVAILABLE reslin-queasy THEN prog-str = reslin-queasy.char3. 
  IF prog-str NE "" THEN 
  DO: 
    OUTPUT STREAM s1 TO ".\_rate.p". 
    DO i = 1 TO LENGTH(prog-str): 
      PUT STREAM s1 SUBSTR(prog-str, i, 1) FORMAT "x(1)". 
    END. 
    OUTPUT STREAM s1 CLOSE. 
    COMPILE value(".\_rate.p"). 
    DOS SILENT "del .\_rate.p". 
    IF NOT COMPILER:ERROR THEN 
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
  FIND FIRST queasy WHERE queasy.key = 2 
    AND queasy.char1 = guest-pr.code NO-LOCK NO-ERROR. 
  IF AVAILABLE queasy THEN prog-str = queasy.char3. 
  IF prog-str NE "" THEN 
  DO: 
    OUTPUT STREAM s1 TO ".\_rate.p". 
    DO i = 1 TO LENGTH(prog-str): 
      PUT STREAM s1 SUBSTR(prog-str, i, 1) FORMAT "x(1)". 
    END. 
    OUTPUT STREAM s1 CLOSE. 
    COMPILE value(".\_rate.p"). 
    DOS SILENT "del .\_rate.p". 
    IF NOT COMPILER:ERROR THEN 
    DO: 
      RUN value(".\_rate.p") (0, res-line.resnr, res-line.reslinnr, 
      bill-date, roomrate, NO, OUTPUT roomrate). 
      it-exist = YES. 
    END. 
  END. 
END. 
*/
