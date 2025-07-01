DEFINE WORKFILE setup-list 
  FIELD nr          AS INTEGER 
  FIELD CHAR        AS CHAR FORMAT "x(1)". 

DEFINE WORKFILE str-list 
  FIELD flag        AS INTEGER INITIAL 0 
  FIELD rflag       AS LOGICAL INITIAL YES 
  
  FIELD line1       AS CHAR FORMAT "x(80)" 
  FIELD line2       AS CHAR FORMAT "x(124)"
  FIELD line3       AS CHAR FORMAT "x(124)" /*SIS 31/01/13 */
  FIELD company     AS CHAR FORMAT "x(32)".

DEFINE TEMP-TABLE cl-list 
  FIELD flag        AS INTEGER 
  FIELD karteityp   AS INTEGER 
  FIELD nr          AS INTEGER FORMAT ">>9" 
  FIELD vip         AS CHAR FORMAT "x(5)" 
  FIELD resnr       AS INTEGER FORMAT ">>>>>9" 
  FIELD name        AS CHAR FORMAT "x(24)" 
  FIELD groupname   AS CHAR FORMAT "x(24)" 
  FIELD rmno        LIKE zimmer.zinr		/*MT 25/07/12 */
  FIELD qty         AS INTEGER FORMAT ">>9" 
  FIELD arrive      AS DATE 
  FIELD depart      AS DATE 
  FIELD rmcat       AS CHAR FORMAT "x(6)" 
  FIELD ratecode    AS CHAR FORMAT "x(18)"  /* "x(6)" Gerald 270720*/
  FIELD zipreis     AS DECIMAL 
  FIELD kurzbez     AS CHAR 
  FIELD bezeich     AS CHAR 
  FIELD a           AS INTEGER FORMAT "9" 
  FIELD c           AS INTEGER FORMAT "9" 
  FIELD co          AS INTEGER FORMAT ">9" 
  FIELD pax         AS CHAR FORMAT "x(6)" 
  FIELD nat         AS CHAR FORMAT "x(3)" 
  FIELD nation      AS CHAR 
  FIELD argt        AS CHAR FORMAT "x(6)" 
  FIELD company     AS CHAR FORMAT "x(18)" 
  FIELD flight      AS CHAR FORMAT "x(6)" 
  FIELD etd         AS CHAR FORMAT "99:99" 
  FIELD paym        AS INTEGER FORMAT ">>9" 
  FIELD segm        AS CHAR FORMAT "x(12)"
  FIELD telefon     AS CHAR FORMAT "x(24)" /*SIS 31/01/13 */
  FIELD mobil-tel   AS CHAR FORMAT "x(24)" /*SIS 31/01/13 */
  FIELD created     AS DATE FORMAT "99/99/99"
  FIELD createID    AS CHAR FORMAT "x(4)"
  FIELD bemerk      AS CHAR FORMAT "x(16)"
  FIELD bemerk01    AS CHAR FORMAT "x(255)" /*DO add remark 1000 char*/
  FIELD bemerk02    AS CHAR FORMAT "x(255)" /*DO add remark 1000 char*/
  FIELD bemerk03    AS CHAR FORMAT "x(255)" /*DO add remark 1000 char*/
  FIELD bemerk04    AS CHAR FORMAT "x(255)" /*DO add remark 1000 char*/
  FIELD bemerk05    AS CHAR FORMAT "x(255)" /*naufal Add Remarks 1000 Char*/
  FIELD bemerk06    AS CHAR FORMAT "x(255)" /*naufal Add Remarks 1000 Char*/
  FIELD bemerk07    AS CHAR FORMAT "x(255)" /*naufal Add Remarks 1000 Char*/
  FIELD bemerk08    AS CHAR FORMAT "x(255)" /*naufal Add Remarks 1000 Char*/
  FIELD bemerk1     AS CHAR FORMAT "x(32)" /*IT 200612 add incl-rsvcomment*/
  FIELD ci-time     AS CHAR
  FIELD curr        AS CHAR FORMAT "x(4)"
  FIELD spreq       AS CHAR FORMAT "x(20)"
  FIELD tot-bfast   AS INTEGER
  FIELD local-reg   AS CHARACTER
  FIELD rsv-comment AS CHARACTER /*FDL August 28, 2023 => Req Kayu Manis Group*/    
  FIELD other-comment AS CHARACTER /*FDL August 28, 2023 => Req Kayu Manis Group*/
  FIELD g-comment   AS CHARACTER /*FDL August 28, 2023 => Req Kayu Manis Group*/
  FIELD zinr-bez    AS CHAR     /*Gerald 7E2311*/
  FIELD flag-guest  AS INTEGER  /*Gerald 7E2311*/
  FIELD etage       AS INTEGER /*FDL April 24, 2023 => 7958BA*/
  FIELD birthdate   AS DATE /*MCH Dec 20, 2024 => 5BB5DC Req Royal Santrian*/
.


DEFINE TEMP-TABLE s-list 
  FIELD rmcat       AS CHAR FORMAT "x(6)" 
  FIELD bezeich     AS CHAR FORMAT "x(24)" 
  FIELD nat         AS CHAR FORMAT "x(24)" 
  FIELD anz         AS INTEGER FORMAT ">>9" 
  FIELD adult       AS INTEGER FORMAT ">>9" 
  FIELD proz        AS DECIMAL FORMAT ">>9.99" 
  FIELD child       AS INTEGER FORMAT ">>9"
  FIELD rmqty       AS INTEGER  FORMAT ">>9".   /*FD Jan 06, 2019*/

DEFINE TEMP-TABLE zinr-list
    FIELD resnr     AS INTEGER
    FIELD reslinnr  AS INTEGER
    FIELD zinr      AS CHAR.

DEFINE TEMP-TABLE t-buff-queasy LIKE queasy.

DEF INPUT PARAMETER sorttype        AS INT.
DEF INPUT PARAMETER datum           AS DATE.
DEF INPUT PARAMETER curr-date       AS DATE.
DEF INPUT PARAMETER curr-gastnr     AS INT.
DEF INPUT PARAMETER froom           LIKE zimmer.zinr.
DEF INPUT PARAMETER troom           LIKE zimmer.zinr.
DEF INPUT PARAMETER exc-depart      AS LOGICAL.
DEF INPUT PARAMETER incl-gcomment   AS LOGICAL.
DEF INPUT PARAMETER incl-rsvcomment AS LOGICAL.
DEF INPUT PARAMETER prog-name       AS CHAR.
DEF INPUT PARAMETER disp-accompany  AS LOGICAL.
DEF INPUT PARAMETER disp-exclinact  AS LOGICAL.
DEF INPUT PARAMETER split-rsv-print AS LOGICAL. /*FDL August 28, 2023 => Req Kayu Manis Group*/
DEF INPUT PARAMETER exc-compli      AS LOGICAL. /*bernatd 9D155B 2025*/
DEF OUTPUT PARAMETER tot-payrm      AS INTEGER INITIAL 0. 
DEF OUTPUT PARAMETER tot-rm         AS INTEGER INITIAL 0. 
DEF OUTPUT PARAMETER tot-a          AS INTEGER INITIAL 0. 
DEF OUTPUT PARAMETER tot-c          AS INTEGER INITIAL 0. 
DEF OUTPUT PARAMETER tot-co         AS INTEGER INITIAL 0. 
DEF OUTPUT PARAMETER tot-avail      AS INTEGER INITIAL 0.
DEF OUTPUT PARAMETER tot-rmqty      AS INTEGER INITIAL 0.   /*FD Jan 06, 2019*/
DEF OUTPUT PARAMETER inactive       AS INTEGER INITIAL 0. 
DEF OUTPUT PARAMETER TABLE FOR cl-list.
DEF OUTPUT PARAMETER TABLE FOR s-list.
DEF OUTPUT PARAMETER TABLE FOR t-buff-queasy.

DEFINE VARIABLE vipnr1 AS INTEGER INITIAL 999999999. 
DEFINE VARIABLE vipnr2 AS INTEGER INITIAL 999999999. 
DEFINE VARIABLE vipnr3 AS INTEGER INITIAL 999999999. 
DEFINE VARIABLE vipnr4 AS INTEGER INITIAL 999999999. 
DEFINE VARIABLE vipnr5 AS INTEGER INITIAL 999999999. 
DEFINE VARIABLE vipnr6 AS INTEGER INITIAL 999999999. 
DEFINE VARIABLE vipnr7 AS INTEGER INITIAL 999999999. 
DEFINE VARIABLE vipnr8 AS INTEGER INITIAL 999999999. 
DEFINE VARIABLE vipnr9 AS INTEGER INITIAL 999999999. 

FIND FIRST htparam WHERE paramnr = 700 NO-LOCK. 
IF finteger NE 0 THEN vipnr1 = htparam.finteger.               /* Rulita 211024 | Fixing for serverless */  
FIND FIRST htparam WHERE paramnr = 701 NO-LOCK. 
IF finteger NE 0 THEN vipnr2 = htparam.finteger.               /* Rulita 211024 | Fixing for serverless */  
FIND FIRST htparam WHERE paramnr = 702 NO-LOCK. 
IF finteger NE 0 THEN vipnr3 = htparam.finteger.               /* Rulita 211024 | Fixing for serverless */  
FIND FIRST htparam WHERE paramnr = 703 NO-LOCK. 
IF finteger NE 0 THEN vipnr4 = htparam.finteger.               /* Rulita 211024 | Fixing for serverless */  
FIND FIRST htparam WHERE paramnr = 704 NO-LOCK. 
IF finteger NE 0 THEN vipnr5 = htparam.finteger.               /* Rulita 211024 | Fixing for serverless */  
FIND FIRST htparam WHERE paramnr = 705 NO-LOCK. 
IF finteger NE 0 THEN vipnr6 = htparam.finteger.               /* Rulita 211024 | Fixing for serverless */  
FIND FIRST htparam WHERE paramnr = 706 NO-LOCK. 
IF finteger NE 0 THEN vipnr7 = htparam.finteger.               /* Rulita 211024 | Fixing for serverless */  
FIND FIRST htparam WHERE paramnr = 707 NO-LOCK. 
IF finteger NE 0 THEN vipnr8 = htparam.finteger.               /* Rulita 211024 | Fixing for serverless */  
FIND FIRST htparam WHERE paramnr = 708 NO-LOCK. 
IF finteger NE 0 THEN vipnr9 = htparam.finteger.               /* Rulita 211024 | Fixing for serverless */  

DEFINE VARIABLE tot-room AS INT.
DEFINE VARIABLE all-room AS INT.

DEFINE VARIABLE all-remark AS LONGCHAR.
/*DEFINE VARIABLE exc-compli AS LOGICAL INITIAL TRUE.*/

/***********************************************************/
RUN bed-setup.
IF sorttype = 1 THEN 
DO:
  IF disp-exclinact THEN /*FD April 06, 2021*/
  DO:
    IF datum GE curr-date THEN RUN create-inhouse2.
    ELSE RUN create-genstat-inhouse2.
  END.
  ELSE
  DO:
    IF datum GE curr-date THEN RUN create-inhouse.
    ELSE RUN create-genstat-inhouse.
  END.  
END.
ELSE 
DO:    
  IF disp-exclinact THEN /*FD April 06, 2021*/
  DO:
    IF datum GE curr-date THEN RUN create-inhouse3.
    ELSE RUN create-genstat-inhouse3.
  END.
  ELSE
  DO:
    IF datum GE curr-date THEN RUN create-inhouse1. 
    ELSE RUN create-genstat-inhouse1.
  END.
END.
RUN create-buf-queasy.

IF datum LT curr-date THEN
DO:
    FOR EACH zkstat WHERE zkstat.datum = datum NO-LOCK:
        tot-room = tot-room + zkstat.anz100.
    END.
    FIND FIRST zinrstat WHERE zinrstat.zinr = "tot-rm" AND zinrstat.datum = datum NO-LOCK NO-ERROR.
    IF AVAILABLE zinrstat THEN all-room = zinrstat.zimmeranz.
    inactive = all-room - tot-room.
END.
/***********************************************************/

PROCEDURE bed-setup: 
  create setup-list. 
  setup-list.nr = 1. 
  setup-list.char = " ". 
  FOR EACH paramtext WHERE paramtext.txtnr GE 9201 
    AND paramtext.txtnr LE 9299 NO-LOCK: 
    create setup-list. 
    setup-list.nr = paramtext.txtnr - 9199. 
    setup-list.char = SUBSTR(paramtext.notes,1,1). 
  END. 
END.

PROCEDURE create-inhouse:
DEFINE VARIABLE i           AS INTEGER.
DEFINE VARIABLE j           AS INTEGER.
DEFINE VARIABLE vip-flag    AS CHAR. 
DEFINE VARIABLE nr          AS INTEGER INITIAL 0. 
DEFINE VARIABLE str         AS CHAR.
DEFINE VARIABLE actflag1    AS INTEGER. 
DEFINE VARIABLE actflag2    AS INTEGER. 
DEFINE VARIABLE do-it       AS LOGICAL.
DEFINE buffer gmember       FOR guest. 
DEFINE BUFFER gbuff         FOR guest.
DEFINE BUFFER rbuff         FOR reservation.

 
  FOR EACH zinr-list:
      DELETE zinr-list.
  END.

  IF datum = curr-date THEN 
  DO: 
    actflag1 = 1. 
    actflag2 = 1. 
  END. 
  ELSE 
  DO: 
    actflag1 = 1. 
    actflag2 = 2. 
  END. 
 
  tot-payrm = 0. 
  tot-rm = 0. 
  tot-a = 0. 
  tot-c = 0. 
  tot-co = 0. 
  inactive = 0. 
 
  FOR EACH s-list: 
   delete s-list. 
  END. 
 
  FOR EACH cl-list: 
    delete cl-list. 
  END. 
 
  FOR EACH str-list: 
    delete str-list. 
  END. 
 
  tot-avail = 0. 
  FOR EACH zimmer WHERE zimmer.sleeping = YES NO-LOCK: 
    tot-avail = tot-avail + 1. 
  END. 
  
  FOR EACH res-line WHERE res-line.active-flag GE actflag1 
    AND res-line.active-flag LE actflag2 
    AND res-line.resstatus NE 9 AND res-line.resstatus NE 10 
    AND res-line.resstatus NE 12 AND res-line.ankunft LE datum 
    AND res-line.abreise GE datum 
    AND res-line.zinr GE froom AND res-line.zinr LE troom NO-LOCK, 
    FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr NO-LOCK, 
    FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
    FIRST guest WHERE guest.gastnr = reservation.gastnr NO-LOCK, 
    FIRST gmember WHERE gmember.gastnr = res-line.gastnrmember NO-LOCK    

    BY res-line.zinr BY res-line.erwachs DESCENDING BY res-line.name: 
    IF exc-depart AND res-line.abreise = datum THEN .
    ELSE
    DO:
        FIND FIRST setup-list WHERE setup-list.nr = res-line.setup + 1. 
        FIND FIRST zimmer WHERE zimmer.zinr = res-line.zinr NO-LOCK NO-ERROR.
     
        nr = nr + 1. 
        vip-flag = "". 
        FIND FIRST guestseg WHERE guestseg.gastnr = gmember.gastnr 
          AND (guestseg.segmentcode = vipnr1 OR 
          guestseg.segmentcode = vipnr2 OR 
          guestseg.segmentcode = vipnr3 OR 
          guestseg.segmentcode = vipnr4 OR 
          guestseg.segmentcode = vipnr5 OR 
          guestseg.segmentcode = vipnr6 OR 
          guestseg.segmentcode = vipnr7 OR 
          guestseg.segmentcode = vipnr8 OR 
          guestseg.segmentcode = vipnr9) NO-LOCK NO-ERROR. 
        IF AVAILABLE guestseg THEN 
        DO: 
          FIND FIRST segment WHERE segment.segmentcode = guestseg.segmentcode
              NO-LOCK.
            ASSIGN vip-flag = segment.bezeich. 
        END.
             
        CREATE cl-list. 
        ASSIGN 
          cl-list.nr        = nr 
    /* 
          cl-list.groupname = reservation.groupname 
    */ 
          cl-list.rmcat     = zimkateg.kurzbez + setup-list.char 
          cl-list.kurzbez   = zimkateg.kurzbez 
          cl-list.bezeich   = zimkateg.bezeich 
          cl-list.nat       = gmember.nation1 
          cl-list.resnr     = res-line.resnr 
          cl-list.vip       = vip-flag 
          cl-list.name      = res-line.name 
          cl-list.rmno      = res-line.zinr 
          cl-list.zipreis   = res-line.zipreis
          cl-list.arrive    = res-line.ankunft 
          cl-list.depart    = res-line.abreise 
          cl-list.qty       = res-line.zimmeranz 
          cl-list.a         = res-line.erwachs 
          cl-list.c         = res-line.kind1 + res-line.kind2 
          cl-list.co        = res-line.gratis 
          cl-list.argt      = res-line.arrangement 
          cl-list.flight    = SUBSTR(res-line.flight-nr, 12, 6) 
          cl-list.etd       = SUBSTR(res-line.flight-nr, 18, 5) 
          cl-list.ci-time   = STRING(res-line.ankzeit, "HH:MM")
    /*    cl-list.paym      = INTEGER(res-line.code).  */ 
          cl-list.paym      = reservation.segmentcode
          cl-list.created   = reservation.resdat
          cl-list.createID  = reservation.useridanlage
          cl-list.etage     = zimmer.etage  
          cl-list.zinr-bez  = zimmer.bezeich
          cl-list.birthdate = gmember.geburtdatum1
          cl-list.telefon   = gmember.telefon /*add by bernatd 70F06C*/
          cl-list.mobil-tel = gmember.mobil-telefon /*add by bernatd 70F06C*/
          .

        IF res-line.resstatus NE 11 AND res-line.resstatus NE 13 THEN ASSIGN cl-list.flag-guest = 1.
        ELSE ASSIGN cl-list.flag-guest = 2.

        /*DODY 01/07/16 penambahan membership number dan type of membership */
        FIND FIRST mc-guest WHERE mc-guest.gastnr = gmember.gastnr NO-LOCK NO-ERROR.
        IF AVAILABLE mc-guest THEN /*FT serverless*/
        DO:
            cl-list.telefon   = gmember.telefon + ";" + mc-guest.cardnum.      /*SIS 31/01/13 */
            FIND FIRST mc-types WHERE mc-types.nr = mc-guest.nr NO-LOCK NO-ERROR.
            IF AVAILABLE mc-types THEN 
             cl-list.mobil-tel = gmember.mobil-telefon + ";" + mc-types.bezeich. /*SIS 31/01/13 */
            ELSE
             cl-list.mobil-tel = gmember.mobil-telefon. 
        END.                                            
        ELSE
         cl-list.telefon   = gmember.telefon.
        
                

        /*FD 15 April, 2021*/
        FIND FIRST nation WHERE nation.kurzbez EQ gmember.nation2 NO-LOCK NO-ERROR.
        IF AVAILABLE nation THEN cl-list.local-reg = nation.bezeich.

        /*/* new Jun 30 09 by LN*/
        FIND FIRST waehrung WHERE waehrung.waehrungsnr = res-line.betriebsnr 
            NO-LOCK NO-ERROR.
        IF AVAILABLE waehrung THEN
            cl-list.curr = waehrung.wabkurz.*/

        /*dody 23/09/16 penambahan email*/
        FIND FIRST waehrung WHERE waehrung.waehrungsnr = res-line.betriebsnr 
            NO-LOCK NO-ERROR.
        IF AVAILABLE waehrung THEN
            cl-list.curr = waehrung.wabkurz + ";" + gmember.email-adr.
        /*end dody*/
        
        /*ITA 130717 --> Add Request Patra*/
        FIND FIRST reslin-queasy WHERE reslin-queasy.KEY = "specialRequest"
             AND reslin-queasy.resnr = res-line.resnr 
             AND reslin-queasy.reslinnr = res-line.reslinnr NO-LOCK NO-ERROR.
        IF AVAILABLE reslin-queasy THEN
             ASSIGN cl-list.spreq = reslin-queasy.char3 + "," + cl-list.spreq.
        /*end*/
        
        /*FD Juny 14, 2021 => Get ratecode per date*/
        FIND FIRST reslin-queasy WHERE reslin-queasy.key EQ "arrangement" 
          AND reslin-queasy.resnr EQ res-line.resnr 
          AND reslin-queasy.reslinnr EQ res-line.reslinnr 
          AND datum GE reslin-queasy.date1 
          AND datum LE reslin-queasy.date2 NO-LOCK NO-ERROR. 
        IF AVAILABLE reslin-queasy THEN 
        DO:
          IF reslin-queasy.char2 NE "" THEN cl-list.ratecode = reslin-queasy.char2.
          ELSE
          DO:
            DO i = 1 TO NUM-ENTRIES(res-line.zimmer-wunsch,";") - 1:
              str = ENTRY(i, res-line.zimmer-wunsch, ";").
              IF SUBSTR(str,1,6) EQ "$CODE$" THEN 
              DO:
                cl-list.ratecode = SUBSTR(str,7).
                LEAVE.
              END.
            END.
          END.
        END.
        /*End FD*/

        /*ITA 021117*/
        FIND FIRST mealcoup WHERE mealcoup.NAME = "Breakfast" 
            AND mealcoup.resnr = res-line.resnr
            AND mealcoup.zinr = res-line.zinr  NO-LOCK NO-ERROR.
        IF AVAILABLE mealcoup THEN DO:
            ASSIGN cl-list.tot-bfast = mealcoup.verbrauch[1] + mealcoup.verbrauch[2] + mealcoup.verbrauch[3] + mealcoup.verbrauch[4] + mealcoup.verbrauch[5]
                                      + mealcoup.verbrauch[6] + mealcoup.verbrauch[7] + mealcoup.verbrauch[8] + mealcoup.verbrauch[9] + mealcoup.verbrauch[10]
                                      + mealcoup.verbrauch[11] + mealcoup.verbrauch[12] + mealcoup.verbrauch[13] + mealcoup.verbrauch[14] + mealcoup.verbrauch[15]
                                      + mealcoup.verbrauch[16] + mealcoup.verbrauch[17] + mealcoup.verbrauch[18] + mealcoup.verbrauch[19] + mealcoup.verbrauch[20]
                                      + mealcoup.verbrauch[21] + mealcoup.verbrauch[22] + mealcoup.verbrauch[23] + mealcoup.verbrauch[24] + mealcoup.verbrauch[25]
                                      + mealcoup.verbrauch[26] + mealcoup.verbrauch[27] + mealcoup.verbrauch[28] + mealcoup.verbrauch[29] + mealcoup.verbrauch[30]
                                      + mealcoup.verbrauch[31] + mealcoup.verbrauch[32].
        END.
        /*end*/

        FIND FIRST segment WHERE segment.segmentcode = reservation.segmentcode
            NO-LOCK NO-ERROR.
        IF AVAILABLE segment THEN cl-list.segm = ENTRY(1, segment.bezeich, "$$0").

        IF guest.karteityp NE 0 THEN
          cl-list.company   = guest.name + ", " + guest.vorname1 
            + " " + guest.anrede1 + guest.anredefirma .
        ELSE
          cl-list.company   = guest.name + ", " + guest.vorname1 
            + " " + guest.anrede1 + guest.anredefirma .

        IF cl-list.nat = "" THEN cl-list.nat = "?". 
        IF res-line.resstatus = 13 OR res-line.zimmerfix THEN cl-list.qty = 0. 
     
        IF NOT split-rsv-print THEN /*ORIG*/
        DO:
            /*M 22 Jan 2011 - addition guest's comment */
            IF incl-gcomment THEN
            DO:
                FIND FIRST gbuff WHERE gbuff.gastnr = res-line.gastnrmember 
                    USE-INDEX gastnr_index NO-LOCK NO-ERROR.
                IF AVAILABLE gbuff THEN
                DO:
                    DO i = 1 TO LENGTH(gbuff.bemerk): 
                        IF SUBSTR(gbuff.bemerk,i,1) = CHR(10) THEN 
                            cl-list.bemerk = cl-list.bemerk + " ". 
                        ELSE cl-list.bemerk = cl-list.bemerk + SUBSTR(TRIM(gbuff.bemerk), i, 1).
                    END.  
                END.
                
                cl-list.bemerk = cl-list.bemerk + " || ".
            END.
            /*IT 200612 add reservation comment*/
            IF incl-rsvcomment THEN        
            DO:
                FIND FIRST rbuff WHERE rbuff.resnr = reservation.resnr NO-LOCK NO-ERROR. /*Alder - Ticket A8CCB8*/
                IF AVAILABLE rbuff THEN
                DO:
                    DO j = 1 TO LENGTH(rbuff.bemerk):
                        IF SUBSTR(rbuff.bemerk,j,1) = CHR(10) THEN 
                            cl-list.bemerk1 = cl-list.bemerk1 + " ". 
                        ELSE cl-list.bemerk1 = cl-list.bemerk1 + SUBSTR(TRIM(rbuff.bemerk), j, 1). 
                    END.
                    
                END.
                /*cl-list.bemerk1 = " || " + cl-list.bemerk1.*/
                cl-list.bemerk = cl-list.bemerk  + cl-list.bemerk1 + " || ".
            END.
            
            DO i = 1 TO length(res-line.bemerk): 
                IF SUBSTR(res-line.bemerk,i,1) = chr(10) THEN 
                cl-list.bemerk = cl-list.bemerk + " ". 
                ELSE cl-list.bemerk = cl-list.bemerk + SUBSTR(TRIM(res-line.bemerk), i, 1).
            END.

            /*DO add remark 1000 char*/
            all-remark = res-line.bemerk.
            all-remark = REPLACE(all-remark,CHR(10)," ").
            all-remark = REPLACE(all-remark,CHR(13)," ").
    
            cl-list.bemerk01 = STRING(SUBSTRING(all-remark,1,225)).
            cl-list.bemerk02 = STRING(SUBSTRING(all-remark,226,225)).
            cl-list.bemerk03 = STRING(SUBSTRING(all-remark,451,225)).
            cl-list.bemerk04 = STRING(SUBSTRING(all-remark,676,225)).
            /*naufal add remarks 2000 char*/
            /*cl-list.bemerk01 = STRING(SUBSTRING(all-remark,1,255)).
            cl-list.bemerk02 = STRING(SUBSTRING(all-remark,256,255)).
            cl-list.bemerk03 = STRING(SUBSTRING(all-remark,511,255)).
            cl-list.bemerk04 = STRING(SUBSTRING(all-remark,766,255)).
            cl-list.bemerk05 = STRING(SUBSTRING(all-remark,1021,255)).
            cl-list.bemerk06 = STRING(SUBSTRING(all-remark,1276,255)).
            cl-list.bemerk07 = STRING(SUBSTRING(all-remark,1531,255)).
            cl-list.bemerk08 = STRING(SUBSTRING(all-remark,1786,255)).*/
            /*end naufal add remarks 2000 char*/
            /*DO add remark 1000 char*/
        END.
        ELSE
        DO:
            DO i = 1 TO length(res-line.bemerk): 
                cl-list.bemerk = cl-list.bemerk + SUBSTR(TRIM(res-line.bemerk), i, 1).
            END.

            FIND FIRST rbuff WHERE rbuff.resnr = reservation.resnr NO-LOCK NO-ERROR. /*Alder - Ticket A8CCB8*/
            IF AVAILABLE rbuff THEN
            DO:
                cl-list.rsv-comment = rbuff.bemerk.                
            END.

            FIND FIRST gbuff WHERE gbuff.gastnr = res-line.gastnrmember 
                USE-INDEX gastnr_index NO-LOCK NO-ERROR.
            IF AVAILABLE gbuff THEN
            DO:
                cl-list.g-comment = gbuff.bemerk.
            END.

            FIND FIRST queasy WHERE queasy.KEY EQ 267
                AND queasy.number1 EQ res-line.resnr
                AND queasy.number2 EQ res-line.reslinnr NO-LOCK NO-ERROR.
            IF AVAILABLE queasy THEN
            DO:
                cl-list.other-comment = queasy.char1.
            END.
        END.        
            
        /*DO j = 1 TO length(reservation.bemerk): 
          IF SUBSTR(reservation.bemerk,j,1) = chr(10) THEN 
          cl-list.bemerk = cl-list.bemerk1 + " ". 
          ELSE cl-list.bemerk = cl-list.bemerk1 + SUBSTR(TRIM(reservation.bemerk), j, 1). 
        END.*/
         
        /*DO j = 1 TO NUM-ENTRIES(res-line.zimmer-wunsch,";") - 1:
            str = ENTRY(j, res-line.zimmer-wunsch, ";").
            IF SUBSTR(str,1,6) = "$CODE$" THEN 
            DO:
              cl-list.ratecode  = SUBSTR(str,7).
              LEAVE.
            END.
        END.*/        

        /* FD Comment 14/06/21, This condition get global ratecode, not ratecode per date
        DO i = 1 TO NUM-ENTRIES(res-line.zimmer-wunsch,";") - 1:
            str = ENTRY(i, res-line.zimmer-wunsch, ";").
            IF SUBSTR(str,1,6) = "$CODE$" THEN 
            DO:
              cl-list.ratecode  = SUBSTR(str,7).
              LEAVE.
            END.
        END.
        */        

        cl-list.pax = STRING(cl-list.a,">9") + "/" + STRING(cl-list.c,"9") 
          + " " + STRING(cl-list.co,"9"). 
     
        IF cl-list.nat = "" THEN cl-list.nat = "?". 
        ELSE 
        DO: 
          FIND FIRST nation WHERE nation.kurzbez = cl-list.nat NO-LOCK NO-ERROR. 
          IF AVAILABLE nation THEN cl-list.nation = nation.bezeich.               
        END.
  
        FIND FIRST zinr-list WHERE zinr-list.zinr = res-line.zinr 
            AND zinr-list.resnr = res-line.resnr 
            AND zinr-list.reslinnr = res-line.reslinnr NO-ERROR.
        IF NOT AVAILABLE zinr-list THEN
        DO: 
          CREATE zinr-list.
          ASSIGN
              zinr-list.resnr = res-line.resnr
              zinr-list.reslinnr = res-line.reslinnr
              zinr-list.zinr  = res-line.zinr.

          FIND FIRST queasy WHERE queasy.key = 14 AND queasy.char1 = res-line.zinr 
            AND queasy.date1 LE curr-date AND queasy.date2 GE curr-date 
            NO-LOCK NO-ERROR. 
          IF zimmer.sleeping AND /*ITA 301213*/ res-line.resstatus NE 13 THEN 
          DO: 
          
              IF NOT AVAILABLE queasy THEN 
              DO: 
                tot-rm = tot-rm + res-line.zimmeranz. 
                tot-rmqty = tot-rmqty + res-line.zimmeranz.
              END.
              ELSE IF AVAILABLE queasy AND queasy.number3 NE res-line.gastnr THEN 
              DO:
                tot-rm = tot-rm + res-line.zimmeranz.
                tot-rmqty = tot-rmqty + res-line.zimmeranz.
              END.
               
          END. 
          /*modify by bernatd EA4782 2025*/
          IF zimmer.sleeping AND (res-line.zipreis GT 0 OR res-line.zipreis = 0) AND res-line.resstatus NE 13 AND res-line.erwachs GT 0 THEN 
          DO: 
             IF NOT AVAILABLE queasy THEN tot-payrm = tot-payrm + res-line.zimmeranz. 
             ELSE IF AVAILABLE queasy AND queasy.number3 NE res-line.gastnr THEN 
               tot-payrm = tot-payrm + res-line.zimmeranz. 
          END. 
          ELSE IF NOT zimmer.sleeping THEN 
          DO: 
            IF AVAILABLE queasy AND queasy.number3 NE res-line.gastnr 
              AND res-line.zipreis GT 0 THEN 
            DO:
              tot-rm = tot-rm + res-line.zimmeranz.
              tot-rmqty = tot-rmqty + res-line.zimmeranz.
            END.      
           
            inactive = inactive + 1.
          END. 
        END. 
     
        tot-a = tot-a + res-line.erwachs. 
        tot-c = tot-c + res-line.kind1 + res-line.kind2. 
        tot-co = tot-co + res-line.gratis. 

        IF exc-compli THEN /*bernatd add 9D155B 2025*/
        DO:
          tot-co = 0.
        END.
    END.
    
    IF NOT disp-accompany THEN
    DO:    
        FIND FIRST cl-list WHERE cl-list.rmno EQ res-line.zinr 
            AND cl-list.resnr EQ res-line.resnr 
            AND cl-list.arrive EQ res-line.ankunft 
            AND cl-list.zipreis EQ 0 AND (cl-list.a + cl-list.c) LT 1
            AND cl-list.co LT 1 EXCLUSIVE-LOCK NO-ERROR.
        IF AVAILABLE cl-list THEN
        DO:
            DELETE cl-list.
            RELEASE cl-list.
        END.
    END.

    /*add exclude Complimetn Bernatd 9D155B 2025*/
    IF exc-compli THEN
    DO:    
        FIND FIRST cl-list WHERE cl-list.rmno EQ res-line.zinr 
            AND cl-list.resnr EQ res-line.resnr 
            AND cl-list.arrive EQ res-line.ankunft 
            AND cl-list.co GT 0 EXCLUSIVE-LOCK NO-ERROR.
        IF AVAILABLE cl-list THEN
        DO:
            DELETE cl-list.
            RELEASE cl-list.
            tot-rm = tot-rm - 1.
        END.
    END.
    /*end bernatd*/
  END. 
  /*MT
  FOR EACH cl-list WHERE cl-list.zipreis NE 0 BY cl-list.nation BY cl-list.bezeich:
      FIND FIRST s-list WHERE s-list.bezeich = cl-list.bezeich
          AND s-list.nat EQ cl-list.nat NO-ERROR.
      IF NOT AVAILABLE s-list THEN
      DO:
          CREATE s-list.
          s-list.rmcat = cl-list.rmcat.
          s-list.bezeich = cl-list.bezeich.
          s-list.nat = cl-list.nat.
      END.
      s-list.anz = s-list.anz + cl-list.qty.
      s-list.adult = s-list.adult + cl-list.a + cl-list.co. 
      s-list.child = s-list.child + cl-list.c.
  END.
  FOR EACH s-list:
      DISP s-list.rmcat s-list.nat.
  END.
  */
  FOR EACH cl-list BY cl-list.nation BY cl-list.bezeich: 
    FIND FIRST s-list WHERE s-list.rmcat = cl-list.kurzbez NO-ERROR. 
    IF NOT AVAILABLE s-list THEN 
    DO: 
      FIND FIRST s-list WHERE s-list.rmcat = "" NO-ERROR. 
      IF AVAILABLE s-list THEN
      DO: 
        s-list.rmcat = cl-list.kurzbez. 
        s-list.bezeich = cl-list.bezeich. 
      END. 
    END. 
    IF NOT AVAILABLE s-list THEN 
    DO: 
      create s-list. 
      s-list.rmcat = cl-list.kurzbez. 
      s-list.bezeich = cl-list.bezeich. 
    END. 
    
    s-list.anz = s-list.anz + cl-list.qty. 
 
    FIND FIRST s-list WHERE s-list.nat = cl-list.nat NO-ERROR. 
    IF NOT AVAILABLE s-list THEN 
    DO: 
      FIND FIRST s-list WHERE s-list.nat = "" NO-ERROR. 
      IF AVAILABLE s-list THEN s-list.nat = cl-list.nat. 
    END. 
    IF NOT AVAILABLE s-list THEN 
    DO: 
      create s-list. 
      IF AVAILABLE s-list THEN s-list.nat = cl-list.nat. 
    END. 
    
    s-list.adult = s-list.adult + cl-list.a + cl-list.co. 
    s-list.child = s-list.child + cl-list.c.

    s-list.rmqty = s-list.rmqty + cl-list.qty.
  END. 
 

  IF (tot-a + tot-co) NE 0 THEN 
  FOR EACH s-list WHERE s-list.nat NE "": 
    FIND FIRST nation WHERE nation.kurzbez = s-list.nat NO-LOCK NO-ERROR. 
    IF AVAILABLE nation THEN s-list.nat = nation.bezeich. 
    s-list.proz = s-list.adult / (tot-a + tot-co) * 100. 
  END. 
END. 


PROCEDURE create-genstat-inhouse: 
DEFINE VARIABLE i           AS INTEGER.
DEFINE VARIABLE j           AS INTEGER.
DEFINE VARIABLE vip-flag    AS CHAR. 
DEFINE VARIABLE nr          AS INTEGER INITIAL 0. 
DEFINE VARIABLE str AS CHAR.
DEFINE VARIABLE actflag1    AS INTEGER. 
DEFINE VARIABLE actflag2    AS INTEGER. 
DEFINE VARIABLE do-it       AS LOGICAL.
DEFINE buffer gmember       FOR guest. 
DEFINE BUFFER gbuff         FOR guest.
DEFINE BUFFER rbuff         FOR reservation.

  FOR EACH zinr-list:
      DELETE zinr-list.
  END.

  IF datum = curr-date THEN 
  DO: 
    actflag1 = 1. 
    actflag2 = 1. 
  END. 
  ELSE 
  DO: 
    actflag1 = 1. 
    actflag2 = 2. 
  END. 
 
  tot-payrm = 0. 
  tot-rm = 0. 
  tot-a = 0. 
  tot-c = 0. 
  tot-co = 0. 
  inactive = 0. 
 
  FOR EACH s-list: 
   delete s-list. 
  END. 
 
  FOR EACH cl-list: 
    delete cl-list. 
  END. 
 
  FOR EACH str-list: 
    delete str-list. 
  END. 
 
  tot-avail = 0. 
  FOR EACH zkstat WHERE zkstat.datum = datum NO-LOCK:
      tot-avail = tot-avail + zkstat.anz100.
  END.
/*
  FOR EACH zimmer WHERE zimmer.sleeping = YES NO-LOCK: 
    tot-avail = tot-avail + 1. 
  END. 
*/ 
  DEF VAR z AS INT.
  FOR EACH genstat WHERE genstat.datum = datum
      AND genstat.zinr GE froom AND genstat.zinr LE troom NO-LOCK,
    FIRST zimkateg WHERE zimkateg.zikatnr = genstat.zikatnr NO-LOCK, 
    FIRST reservation WHERE reservation.resnr = genstat.resnr NO-LOCK, 
    FIRST guest WHERE guest.gastnr = genstat.gastnr NO-LOCK, 
    FIRST gmember WHERE gmember.gastnr = genstat.gastnrmember NO-LOCK
    BY genstat.zinr BY genstat.erwachs DESCENDING BY gmember.name: 
    
    IF genstat.res-date[1] LT datum AND genstat.res-date[2] = datum
          AND genstat.resstatus = 8 THEN . /*FD Juni 22, 2020*/
    ELSE IF exc-depart AND genstat.res-date[1] LE datum AND genstat.res-date[2] = datum
          AND genstat.resstatus = 8 THEN . /*M exclude day use  181010*/
    ELSE
    DO:
        FIND FIRST res-line WHERE res-line.resnr = genstat.resnr
           AND res-line.reslinnr = genstat.res-int[1] NO-LOCK .
        FIND FIRST setup-list WHERE setup-list.nr = res-line.setup + 1. 

        FIND FIRST zimmer WHERE zimmer.zinr = genstat.zinr NO-LOCK NO-ERROR. 
     
        nr = nr + 1. 
        vip-flag = "". 
        FIND FIRST guestseg WHERE guestseg.gastnr = gmember.gastnr 
          AND (guestseg.segmentcode = vipnr1 OR 
          guestseg.segmentcode = vipnr2 OR 
          guestseg.segmentcode = vipnr3 OR 
          guestseg.segmentcode = vipnr4 OR 
          guestseg.segmentcode = vipnr5 OR 
          guestseg.segmentcode = vipnr6 OR 
          guestseg.segmentcode = vipnr7 OR 
          guestseg.segmentcode = vipnr8 OR 
          guestseg.segmentcode = vipnr9) NO-LOCK NO-ERROR. 
        IF AVAILABLE guestseg THEN 
        DO: 
          FIND FIRST segment WHERE segment.segmentcode = guestseg.segmentcode
            NO-LOCK.
          vip-flag = REPLACE(segment.bezeich, " ", "").
        END.
     
        create cl-list. 
        ASSIGN 
          cl-list.nr        = nr 
    /* 
          cl-list.groupname = reservation.groupname 
    */ 
          cl-list.rmcat     = zimkateg.kurzbez + setup-list.char 
          cl-list.kurzbez   = zimkateg.kurzbez 
          cl-list.bezeich   = zimkateg.bezeich 
          cl-list.nat       = gmember.nation1 
          cl-list.resnr     = genstat.resnr 
          cl-list.vip       = vip-flag 
          cl-list.name      = gmember.name  + ", " + gmember.vorname1 
                            + " " + gmember.anrede1
          cl-list.rmno      = genstat.zinr 
          cl-list.zipreis   = genstat.zipreis
          cl-list.arrive    = genstat.res-date[1] 
          cl-list.depart    = genstat.res-date[2] 
          cl-list.qty       = 1 
          cl-list.a         = genstat.erwachs
          cl-list.c         = genstat.kind1 + genstat.kind2 + genstat.kind3
          cl-list.co        = genstat.gratis 
          cl-list.argt      = genstat.argt 
          cl-list.flight    = SUBSTR(res-line.flight-nr, 12, 6) 
          cl-list.etd       = SUBSTR(res-line.flight-nr, 18, 5) 
          cl-list.ci-time   = STRING(res-line.ankzeit, "HH:MM")
          cl-list.paym      = genstat.segmentcode
          cl-list.created   = reservation.resdat
          cl-list.createID  = reservation.useridanlage
          cl-list.etage     = zimmer.etage  
          cl-list.zinr-bez  = zimmer.bezeich
          cl-list.birthdate = gmember.geburtdatum1
          cl-list.telefon   = gmember.telefon /*add by bernatd 70F06C*/
          cl-list.mobil-tel = gmember.mobil-telefon /*add by bernatd 70F06C*/
          .

        IF res-line.resstatus NE 11 AND res-line.resstatus NE 13 THEN ASSIGN cl-list.flag-guest = 1.
        ELSE ASSIGN cl-list.flag-guest = 2.

        /*DODY 01/07/16 penambahan membership number dan type of membership */
        FIND FIRST mc-guest WHERE mc-guest.gastnr = gmember.gastnr NO-LOCK NO-ERROR.
        IF AVAILABLE mc-guest THEN /*FT serverless*/
        DO:
            cl-list.telefon   = gmember.telefon + ";" + mc-guest.cardnum.      /*SIS 31/01/13 */
            FIND FIRST mc-types WHERE mc-types.nr = mc-guest.nr NO-LOCK NO-ERROR.
            IF AVAILABLE mc-types THEN 
             cl-list.mobil-tel = gmember.mobil-telefon + ";" + mc-types.bezeich. /*SIS 31/01/13 */
            ELSE
             cl-list.mobil-tel = gmember.mobil-telefon. 
        END.                                            
        ELSE cl-list.telefon   = gmember.telefon.

        /*FD 15 April, 2021*/
        FIND FIRST nation WHERE nation.kurzbez EQ gmember.nation2 NO-LOCK NO-ERROR.
        IF AVAILABLE nation THEN cl-list.local-reg = nation.bezeich.

        /*/* new Jun 30 09 by LN*/
        FIND FIRST waehrung WHERE waehrung.waehrungsnr = res-line.betriebsnr 
            NO-LOCK NO-ERROR.
        IF AVAILABLE waehrung THEN
            cl-list.curr = waehrung.wabkurz.*/

       /*dody 23/09/16 penambahan email*/
        FIND FIRST waehrung WHERE waehrung.waehrungsnr = res-line.betriebsnr 
            NO-LOCK NO-ERROR.
        IF AVAILABLE waehrung THEN
            cl-list.curr = waehrung.wabkurz + ";" + gmember.email-adr.
        /*end dody*/

        /*ITA 130717 --> Add Request Patra*/
        FIND FIRST reslin-queasy WHERE reslin-queasy.KEY = "specialRequest"
             AND reslin-queasy.resnr = res-line.resnr 
             AND reslin-queasy.reslinnr = res-line.reslinnr NO-LOCK NO-ERROR.
        IF AVAILABLE reslin-queasy THEN
             ASSIGN cl-list.spreq = reslin-queasy.char3 + "," + cl-list.spreq.
        /*end*/

        /*FD Juny 14, 2021 => Get ratecode per date*/
        FIND FIRST reslin-queasy WHERE reslin-queasy.key EQ "arrangement" 
          AND reslin-queasy.resnr EQ res-line.resnr 
          AND reslin-queasy.reslinnr EQ res-line.reslinnr 
          AND datum GE reslin-queasy.date1 
          AND datum LE reslin-queasy.date2 NO-LOCK NO-ERROR. 
        IF AVAILABLE reslin-queasy THEN 
        DO:
          IF reslin-queasy.char2 NE "" THEN cl-list.ratecode = reslin-queasy.char2.                       
          ELSE
          DO:
            DO i = 1 TO NUM-ENTRIES(res-line.zimmer-wunsch,";") - 1:
              str = ENTRY(i, res-line.zimmer-wunsch, ";").
              IF SUBSTR(str,1,6) EQ "$CODE$" THEN 
              DO:
                cl-list.ratecode = SUBSTR(str,7).
                LEAVE.
              END.
            END.           
          END.
        END.
        /*End FD*/

        FIND FIRST segment WHERE segment.segmentcode = genstat.segmentcode
            NO-LOCK NO-ERROR.
        IF AVAILABLE segment THEN cl-list.segm = ENTRY(1, segment.bezeich, "$$0").

        IF guest.karteityp NE 0 THEN
          cl-list.company   = guest.name + ", " + guest.vorname1 
            + " " + guest.anrede1 + guest.anredefirma .
        ELSE
          cl-list.company   = guest.name + ", " + guest.vorname1 
            + " " + guest.anrede1 + guest.anredefirma .

        IF cl-list.nat = "" THEN cl-list.nat = "?". 
        IF genstat.resstatus = 13 THEN cl-list.qty = 0. 
     
        /*M 22 Jan 2011 - addition guest's comment */
        
        IF NOT split-rsv-print THEN
        DO:
            IF incl-gcomment THEN
            DO:
                FIND FIRST gbuff WHERE gbuff.gastnr = res-line.gastnrmember 
                    USE-INDEX gastnr_index NO-LOCK NO-ERROR.
                IF AVAILABLE gbuff THEN
                DO:
                    DO i = 1 TO LENGTH(gbuff.bemerk): 
                        IF SUBSTR(gbuff.bemerk,i,1) = CHR(10) THEN 
                            cl-list.bemerk = cl-list.bemerk + " ". 
                        ELSE cl-list.bemerk = cl-list.bemerk + SUBSTR(TRIM(gbuff.bemerk), i, 1). 
                    END. 
                END.
    
                cl-list.bemerk = cl-list.bemerk + " || ".
            END. 
            
            /*IT 200612 add reservation comment*/
            IF incl-rsvcomment THEN
            DO:
                FIND FIRST rbuff WHERE rbuff.resnr = reservation.resnr NO-LOCK NO-ERROR. /*Alder - Ticket A8CCB8*/
                IF AVAILABLE rbuff THEN
                DO:
                    DO j = 1 TO LENGTH(rbuff.bemerk):
                        IF SUBSTR(rbuff.bemerk,j,1) = CHR(10) THEN 
                            cl-list.bemerk1 = cl-list.bemerk1 + " ". 
                        ELSE cl-list.bemerk1 = cl-list.bemerk1 + SUBSTR(TRIM(rbuff.bemerk), j, 1). 
                    END.
                    
                END.
                /*cl-list.bemerk1 = " || " + cl-list.bemerk1.*/
                cl-list.bemerk = cl-list.bemerk  + cl-list.bemerk1 + " || ".     
            END.
            
            DO i = 1 TO LENGTH(res-line.bemerk): 
              IF SUBSTR(res-line.bemerk,i,1) = chr(10) THEN 
                  cl-list.bemerk = cl-list.bemerk + " ". 
              ELSE cl-list.bemerk = cl-list.bemerk + 
                  SUBSTR(TRIM(res-line.bemerk), i, 1). 
            END.

            /*DO add remark 1000 char*/
            all-remark = res-line.bemerk.
            all-remark = REPLACE(all-remark,CHR(10)," ").
            all-remark = REPLACE(all-remark,CHR(13)," ").
    
            cl-list.bemerk01 = STRING(SUBSTRING(all-remark,1,225)).
            cl-list.bemerk02 = STRING(SUBSTRING(all-remark,226,225)).
            cl-list.bemerk03 = STRING(SUBSTRING(all-remark,451,225)).
            cl-list.bemerk04 = STRING(SUBSTRING(all-remark,676,225)).
            /*naufal add remarks 2000 char*/
            /*cl-list.bemerk01 = STRING(SUBSTRING(all-remark,1,255)).
            cl-list.bemerk02 = STRING(SUBSTRING(all-remark,256,255)).
            cl-list.bemerk03 = STRING(SUBSTRING(all-remark,511,255)).
            cl-list.bemerk04 = STRING(SUBSTRING(all-remark,766,255)).
            cl-list.bemerk05 = STRING(SUBSTRING(all-remark,1021,255)).
            cl-list.bemerk06 = STRING(SUBSTRING(all-remark,1276,255)).
            cl-list.bemerk07 = STRING(SUBSTRING(all-remark,1531,255)).
            cl-list.bemerk08 = STRING(SUBSTRING(all-remark,1786,255)).*/
            /*end naufal add remarks 2000 char*/
            /*DO add remark 1000 char*/
        END.
        ELSE
        DO:
            DO i = 1 TO length(res-line.bemerk): 
                cl-list.bemerk = cl-list.bemerk + SUBSTR(TRIM(res-line.bemerk), i, 1).
            END.

            FIND FIRST rbuff WHERE rbuff.resnr = reservation.resnr NO-LOCK NO-ERROR. /*Alder - Ticket A8CCB8*/
            IF AVAILABLE rbuff THEN
            DO:
                cl-list.rsv-comment = rbuff.bemerk.                
            END.

            FIND FIRST gbuff WHERE gbuff.gastnr = res-line.gastnrmember 
                USE-INDEX gastnr_index NO-LOCK NO-ERROR.
            IF AVAILABLE gbuff THEN
            DO:
                cl-list.g-comment = gbuff.bemerk.
            END.

            FIND FIRST queasy WHERE queasy.KEY EQ 267
                AND queasy.number1 EQ res-line.resnr
                AND queasy.number2 EQ res-line.reslinnr NO-LOCK NO-ERROR.
            IF AVAILABLE queasy THEN
            DO:
                cl-list.other-comment = queasy.char1.
            END.
        END.        

        /* FD Comment 14/06/21, This condition get global ratecode, not ratecode per date
        DO i = 1 TO NUM-ENTRIES(res-line.zimmer-wunsch,";") - 1:
                    str = ENTRY(i, res-line.zimmer-wunsch, ";").
                    IF SUBSTR(str,1,6) = "$CODE$" THEN 
                    DO:
                      cl-list.ratecode  = SUBSTR(str,7).
                      LEAVE.
                    END.
        END.
        */
        /*DO j = 1 TO length(reservation.bemerk): 
          IF SUBSTR(reservation.bemerk,j,1) = chr(10) THEN 
          cl-list.bemerk1 = cl-list.bemerk1 + " ". 
          ELSE cl-list.bemerk1 = cl-list.bemerk1 + SUBSTR(TRIM(reservation.bemerk), j, 1). 
        DISP cl-list.bemerk1.
        END.*/

        /*DO j = 1 TO NUM-ENTRIES(res-line.zimmer-wunsch,";") - 1:
            str = ENTRY(i, res-line.zimmer-wunsch, ";").
            IF SUBSTR(str,1,6) = "$CODE$" THEN 
            DO:
              cl-list.ratecode  = SUBSTR(str,7).
              LEAVE.
            END.
        END.*/


        cl-list.pax = STRING(cl-list.a,">9") + "/" + STRING(cl-list.c,"9") 
          + " " + STRING(cl-list.co,"9"). 
     
        IF cl-list.nat = "" THEN cl-list.nat = "?". 
        ELSE 
        DO: 
          FIND FIRST nation WHERE nation.kurzbez = cl-list.nat NO-LOCK NO-ERROR. 
          IF AVAILABLE nation THEN cl-list.nation = nation.bezeich. 
        END. 

     
        FIND FIRST zinr-list WHERE zinr-list.zinr = genstat.zinr 
            AND zinr-list.resnr = res-line.resnr 
            AND zinr-list.reslinnr = res-line.reslinnr NO-ERROR.
        IF NOT AVAILABLE zinr-list THEN
        DO: 
          CREATE zinr-list.
          ASSIGN
              zinr-list.resnr = res-line.resnr
              zinr-list.reslinnr = res-line.reslinnr
              zinr-list.zinr  = genstat.zinr.

          FIND FIRST queasy WHERE queasy.key = 14 AND queasy.char1 = genstat.zinr 
            AND queasy.date1 LE curr-date AND queasy.date2 GE curr-date 
            NO-LOCK NO-ERROR. 
          IF zimmer.sleeping /*MT*/ /*ITA 301213*/ AND genstat.resstatus NE 13 THEN 
          DO: 
             IF NOT AVAILABLE queasy THEN
             DO:
               tot-rm = tot-rm + 1.
               tot-rmqty = tot-rmqty + 1.
             END.                  
             ELSE IF AVAILABLE queasy AND queasy.number3 NE genstat.gastnr THEN 
             DO:
               tot-rm = tot-rm + 1.
               tot-rmqty = tot-rmqty + 1.
             END.
                
          END. 
          /*modify by bernatd EA4782 2025*/
          IF zimmer.sleeping AND (genstat.zipreis GT 0 OR genstat.zipreis = 0 ) AND genstat.erwachs GT 0 AND genstat.resstatus NE 13 THEN 
          DO: z = z + 1.
             IF NOT AVAILABLE queasy THEN 
             DO:
                 tot-payrm = tot-payrm + 1.
             END.
             ELSE IF AVAILABLE queasy AND queasy.number3 NE genstat.gastnr THEN 
               tot-payrm = tot-payrm + 1. 
          END. 
          ELSE IF NOT zimmer.sleeping THEN 
          DO: 
            IF AVAILABLE queasy AND queasy.number3 NE genstat.gastnr 
              AND genstat.zipreis GT 0 THEN
            DO:
              tot-rm = tot-rm + 1.
              tot-rmqty = tot-rmqty + 1.
            END.     

            inactive = inactive + 1.
          END. 
        END. 
     
        tot-a = tot-a + genstat.erwachs. 
        tot-c = tot-c + genstat.kind1 + genstat.kind2 + genstat.kind3. 
        tot-co = tot-co + genstat.gratis. 

        IF exc-compli THEN /*bernatd add 9D155B 2025*/
        DO:
          tot-co = 0.
        END.
    END.
    
    IF NOT disp-accompany THEN
    DO:    
        FIND FIRST cl-list WHERE cl-list.rmno EQ res-line.zinr 
            AND cl-list.resnr EQ res-line.resnr 
            AND cl-list.arrive EQ res-line.ankunft 
            AND cl-list.zipreis EQ 0 AND (cl-list.a + cl-list.c) LT 1
            AND cl-list.co LT 1 EXCLUSIVE-LOCK NO-ERROR.
        IF AVAILABLE cl-list THEN
        DO:
            DELETE cl-list.
            RELEASE cl-list.
        END.
    END.
    /*add exclude Complimetn Bernatd 9D155B 2025*/
    IF exc-compli THEN
    DO:   
        FIND FIRST cl-list WHERE cl-list.rmno EQ res-line.zinr 
            AND cl-list.resnr EQ res-line.resnr 
            AND cl-list.arrive EQ res-line.ankunft 
            AND cl-list.co GT 0 EXCLUSIVE-LOCK NO-ERROR.
        IF AVAILABLE cl-list THEN
        DO:
            DELETE cl-list.
            RELEASE cl-list.
            tot-rm = tot-rm - 1.
        END.
    END.
    /*end bernatd*/

  END. 
  /*MT
  FOR EACH cl-list WHERE cl-list.zipreis NE 0 BY cl-list.nation BY cl-list.bezeich:
      FIND FIRST s-list WHERE s-list.bezeich = cl-list.bezeich
          AND s-list.nat EQ cl-list.nat NO-ERROR.
      IF NOT AVAILABLE s-list THEN
      DO:
          CREATE s-list.
          s-list.rmcat = cl-list.rmcat.
          s-list.bezeich = cl-list.bezeich.
          s-list.nat = cl-list.nat.
      END.
      s-list.anz = s-list.anz + cl-list.qty.
      s-list.adult = s-list.adult + cl-list.a + cl-list.co. 
      s-list.child = s-list.child + cl-list.c.
      
  END.
  */
  
  /*FOR EACH zinr-list BY zinr-list.zinr BY zinr-list.resnr :
      z = z + 1.
  END.*/
  FOR EACH cl-list BY cl-list.nation BY cl-list.bezeich: 
    /*ITA 021117*/
    FIND FIRST mealcoup WHERE mealcoup.NAME = "Breakfast" 
        AND mealcoup.resnr = cl-list.resnr
        AND mealcoup.zinr = cl-list.rmno  NO-LOCK NO-ERROR.
    IF AVAILABLE mealcoup THEN DO:
        ASSIGN cl-list.tot-bfast = mealcoup.verbrauch[1] + mealcoup.verbrauch[2] + mealcoup.verbrauch[3] + mealcoup.verbrauch[4] + mealcoup.verbrauch[5]
                                  + mealcoup.verbrauch[6] + mealcoup.verbrauch[7] + mealcoup.verbrauch[8] + mealcoup.verbrauch[9] + mealcoup.verbrauch[10]
                                  + mealcoup.verbrauch[11] + mealcoup.verbrauch[12] + mealcoup.verbrauch[13] + mealcoup.verbrauch[14] + mealcoup.verbrauch[15]
                                  + mealcoup.verbrauch[16] + mealcoup.verbrauch[17] + mealcoup.verbrauch[18] + mealcoup.verbrauch[19] + mealcoup.verbrauch[20]
                                  + mealcoup.verbrauch[21] + mealcoup.verbrauch[22] + mealcoup.verbrauch[23] + mealcoup.verbrauch[24] + mealcoup.verbrauch[25]
                                  + mealcoup.verbrauch[26] + mealcoup.verbrauch[27] + mealcoup.verbrauch[28] + mealcoup.verbrauch[29] + mealcoup.verbrauch[30]
                                  + mealcoup.verbrauch[31] + mealcoup.verbrauch[32].
    END.

    FIND FIRST s-list WHERE s-list.rmcat = cl-list.kurzbez NO-ERROR. 
    IF NOT AVAILABLE s-list THEN 
    DO: 
      FIND FIRST s-list WHERE s-list.rmcat = "" NO-ERROR. 
      IF AVAILABLE s-list THEN 
      DO: 
        s-list.rmcat = cl-list.kurzbez. 
        s-list.bezeich = cl-list.bezeich. 
      END. 
    END. 
    IF NOT AVAILABLE s-list THEN 
    DO: 
      create s-list. 
      s-list.rmcat = cl-list.kurzbez. 
      s-list.bezeich = cl-list.bezeich. 
    END. 
    
    s-list.anz = s-list.anz + cl-list.qty. 
 
    FIND FIRST s-list WHERE s-list.nat = cl-list.nat NO-ERROR. 
    IF NOT AVAILABLE s-list THEN 
    DO: 
      FIND FIRST s-list WHERE s-list.nat = "" NO-ERROR. 
      IF AVAILABLE s-list THEN s-list.nat = cl-list.nat. 
    END. 
    IF NOT AVAILABLE s-list THEN 
    DO: 
      create s-list. 
      IF AVAILABLE s-list THEN s-list.nat = cl-list.nat. 
    END. 
    s-list.adult = s-list.adult + cl-list.a + cl-list.co. 
    s-list.child = s-list.child + cl-list.c. 

    s-list.rmqty = s-list.rmqty + cl-list.qty.
  END. 
  
  
  IF (tot-a + tot-co) NE 0 THEN 
  FOR EACH s-list WHERE s-list.nat NE "": 
    FIND FIRST nation WHERE nation.kurzbez = s-list.nat NO-LOCK NO-ERROR. 
    IF AVAILABLE nation THEN s-list.nat = nation.bezeich. 
    s-list.proz = s-list.adult / (tot-a + tot-co) * 100. 
  END. 
 
END. 


PROCEDURE create-inhouse1: 
DEFINE VARIABLE i           AS INTEGER.
DEFINE VARIABLE j           AS INTEGER.
DEFINE VARIABLE vip-flag    AS CHAR. 
DEFINE VARIABLE str         AS CHAR.
DEFINE VARIABLE nr          AS INTEGER INITIAL 0. 
DEFINE VARIABLE curr-gastnr AS INTEGER INITIAL 0. 
DEFINE VARIABLE actflag1    AS INTEGER. 
DEFINE VARIABLE actflag2    AS INTEGER. 
DEFINE buffer gmember       FOR guest. 
DEFINE BUFFER gbuff         FOR guest.
DEFINE BUFFER rbuff         FOR reservation.

  FOR EACH zinr-list:
      DELETE zinr-list.
  END.

  IF datum = curr-date THEN 
  DO: 
    actflag1 = 1. 
    actflag2 = 1. 
  END. 
  ELSE 
  DO: 
    actflag1 = 1. 
    actflag2 = 2. 
  END. 
 
  tot-payrm = 0. 
  tot-rm = 0. 
  tot-a = 0. 
  tot-c = 0. 
  tot-co = 0. 
  inactive = 0. 
 
  FOR EACH s-list: 
   delete s-list. 
  END. 
 
  FOR EACH cl-list: 
    delete cl-list. 
  END. 
 
  FOR EACH str-list: 
    delete str-list. 
  END. 
 
  tot-avail = 0. 
  FOR EACH zimmer WHERE zimmer.sleeping = YES NO-LOCK: 
    tot-avail = tot-avail + 1. 
  END. 
 
  FOR EACH res-line WHERE res-line.active-flag GE actflag1 
    AND res-line.active-flag LE actflag2 
    AND res-line.resstatus NE 9 AND res-line.resstatus NE 10 
    AND res-line.resstatus NE 12 AND res-line.ankunft LE datum 
    AND res-line.abreise GE datum 
    AND res-line.zinr GE froom AND res-line.zinr LE troom NO-LOCK, 
    FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr NO-LOCK, 
    FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
    FIRST guest WHERE guest.gastnr = reservation.gastnr NO-LOCK, 
    FIRST gmember WHERE gmember.gastnr = res-line.gastnrmember NO-LOCK 
    BY guest.karteityp descending BY guest.name BY guest.gastnr 
    BY res-line.name BY res-line.zinr: 

    IF exc-depart AND res-line.abreise = datum THEN.
    ELSE
    DO:
        FIND FIRST setup-list WHERE setup-list.nr = res-line.setup + 1. 
        FIND FIRST zimmer WHERE zimmer.zinr = res-line.zinr NO-LOCK. 
     
        IF curr-gastnr NE guest.gastnr THEN 
        DO: 
          nr = 0. 
          curr-gastnr = guest.gastnr. 
        END. 
        IF guest.karteityp GT 0 THEN nr = nr + 1. 
        vip-flag = "". 
        FIND FIRST guestseg WHERE guestseg.gastnr = gmember.gastnr 
          AND (guestseg.segmentcode = vipnr1 OR 
          guestseg.segmentcode = vipnr2 OR 
          guestseg.segmentcode = vipnr3 OR 
          guestseg.segmentcode = vipnr4 OR 
          guestseg.segmentcode = vipnr5 OR 
          guestseg.segmentcode = vipnr6 OR 
          guestseg.segmentcode = vipnr7 OR 
          guestseg.segmentcode = vipnr8 OR 
          guestseg.segmentcode = vipnr9) NO-LOCK NO-ERROR. 
        IF AVAILABLE guestseg THEN 
        DO: 
          FIND FIRST segment WHERE segment.segmentcode = guestseg.segmentcode
              NO-LOCK.
            ASSIGN vip-flag = segment.bezeich. 
        END.
     
        create cl-list. 
        ASSIGN 
          cl-list.nr        = nr 
    /* 
          cl-list.groupname = reservation.groupname 
    */ 
          cl-list.karteityp = guest.karteityp 
          cl-list.rmcat     = zimkateg.kurzbez + setup-list.char 
          cl-list.kurzbez   = zimkateg.kurzbez 
          cl-list.bezeich   = zimkateg.bezeich 
          cl-list.nat       = gmember.nation1 
          cl-list.resnr     = res-line.resnr 
          cl-list.vip       = vip-flag 
          cl-list.name      = res-line.name 
          cl-list.rmno      = res-line.zinr 
          cl-list.zipreis   = res-line.zipreis
          cl-list.arrive    = res-line.ankunft 
          cl-list.depart    = res-line.abreise 
          cl-list.qty       = res-line.zimmeranz 
          cl-list.a         = res-line.erwachs 
          cl-list.c         = res-line.kind1 + res-line.kind2 
          cl-list.co        = res-line.gratis 
          cl-list.argt      = res-line.arrangement 
          cl-list.flight    = SUBSTR(res-line.flight-nr, 12, 6) 
          cl-list.etd       = SUBSTR(res-line.flight-nr, 18, 5) 
          cl-list.ci-time = STRING(res-line.ankzeit, "HH:MM")
    /*    cl-list.paym      = INTEGER(res-line.code).  */ 
          cl-list.paym      = reservation.segmentcode
          cl-list.created   = reservation.resdat
          cl-list.createID  = reservation.useridanlage
          cl-list.etage     = zimmer.etage  
          cl-list.zinr-bez  = zimmer.bezeich
          cl-list.birthdate = gmember.geburtdatum1
          cl-list.telefon   = gmember.telefon /*add by bernatd 70F06C*/
          cl-list.mobil-tel = gmember.mobil-telefon /*add by bernatd 70F06C*/
          .

        IF res-line.resstatus NE 11 AND res-line.resstatus NE 13 THEN ASSIGN cl-list.flag-guest = 1.
        ELSE ASSIGN cl-list.flag-guest = 2.

        /*DODY 01/07/16 penambahan membership number dan type of membership */
        FIND FIRST mc-guest WHERE mc-guest.gastnr = gmember.gastnr NO-LOCK NO-ERROR.
        IF AVAILABLE mc-guest THEN /*FT serverless*/
        DO:
            cl-list.telefon   = gmember.telefon + ";" + mc-guest.cardnum.      /*SIS 31/01/13 */
            FIND FIRST mc-types WHERE mc-types.nr = mc-guest.nr NO-LOCK NO-ERROR.
            IF AVAILABLE mc-types THEN 
             cl-list.mobil-tel = gmember.mobil-telefon + ";" + mc-types.bezeich. /*SIS 31/01/13 */
            ELSE
             cl-list.mobil-tel = gmember.mobil-telefon. 
        END.                                            
        ELSE cl-list.telefon   = gmember.telefon.
        
        /*FD 15 April, 2021*/
        FIND FIRST nation WHERE nation.kurzbez EQ gmember.nation2 NO-LOCK NO-ERROR.
        IF AVAILABLE nation THEN cl-list.local-reg = nation.bezeich.

        /*/* new Jun 30 09 by LN*/
        FIND FIRST waehrung WHERE waehrung.waehrungsnr = res-line.betriebsnr 
            NO-LOCK NO-ERROR.
        IF AVAILABLE waehrung THEN
            cl-list.curr = waehrung.wabkurz.*/

       /*dody 23/09/16 penambahan email*/
        FIND FIRST waehrung WHERE waehrung.waehrungsnr = res-line.betriebsnr 
            NO-LOCK NO-ERROR.
        IF AVAILABLE waehrung THEN
            cl-list.curr = waehrung.wabkurz + ";" + gmember.email-adr.
       /*end dody*/ 

        /*ITA 130717 --> Add Request Patra*/
        FIND FIRST reslin-queasy WHERE reslin-queasy.KEY = "specialRequest"
             AND reslin-queasy.resnr = res-line.resnr 
             AND reslin-queasy.reslinnr = res-line.reslinnr NO-LOCK NO-ERROR.
        IF AVAILABLE reslin-queasy THEN
             ASSIGN cl-list.spreq = reslin-queasy.char3 + "," + cl-list.spreq.
        /*end*/

        /*FD Juny 14, 2021 => Get ratecode per date*/
        FIND FIRST reslin-queasy WHERE reslin-queasy.key EQ "arrangement" 
          AND reslin-queasy.resnr EQ res-line.resnr 
          AND reslin-queasy.reslinnr EQ res-line.reslinnr 
          AND datum GE reslin-queasy.date1 
          AND datum LE reslin-queasy.date2 NO-LOCK NO-ERROR. 
        IF AVAILABLE reslin-queasy THEN 
        DO:
          IF reslin-queasy.char2 NE "" THEN cl-list.ratecode = reslin-queasy.char2.
          ELSE
          DO:
            DO i = 1 TO NUM-ENTRIES(res-line.zimmer-wunsch,";") - 1:
              str = ENTRY(i, res-line.zimmer-wunsch, ";").
              IF SUBSTR(str,1,6) EQ "$CODE$" THEN 
              DO:
                cl-list.ratecode = SUBSTR(str,7).
                LEAVE.
              END.
            END.
          END.
        END.
        /*End FD*/

        /*ITA 021117*/
        FIND FIRST mealcoup WHERE mealcoup.NAME = "Breakfast" 
            AND mealcoup.resnr = res-line.resnr
            AND mealcoup.zinr = res-line.zinr  NO-LOCK NO-ERROR.
        IF AVAILABLE mealcoup THEN DO:
            ASSIGN cl-list.tot-bfast = mealcoup.verbrauch[1] + mealcoup.verbrauch[2] + mealcoup.verbrauch[3] + mealcoup.verbrauch[4] + mealcoup.verbrauch[5]
                                      + mealcoup.verbrauch[6] + mealcoup.verbrauch[7] + mealcoup.verbrauch[8] + mealcoup.verbrauch[9] + mealcoup.verbrauch[10]
                                      + mealcoup.verbrauch[11] + mealcoup.verbrauch[12] + mealcoup.verbrauch[13] + mealcoup.verbrauch[14] + mealcoup.verbrauch[15]
                                      + mealcoup.verbrauch[16] + mealcoup.verbrauch[17] + mealcoup.verbrauch[18] + mealcoup.verbrauch[19] + mealcoup.verbrauch[20]
                                      + mealcoup.verbrauch[21] + mealcoup.verbrauch[22] + mealcoup.verbrauch[23] + mealcoup.verbrauch[24] + mealcoup.verbrauch[25]
                                      + mealcoup.verbrauch[26] + mealcoup.verbrauch[27] + mealcoup.verbrauch[28] + mealcoup.verbrauch[29] + mealcoup.verbrauch[30]
                                      + mealcoup.verbrauch[31] + mealcoup.verbrauch[32].
        END.

        FIND FIRST segment WHERE segment.segmentcode = reservation.segmentcode
            NO-LOCK NO-ERROR.
        IF AVAILABLE segment THEN cl-list.segm = ENTRY(1, segment.bezeich, "$$0").
        
        IF guest.karteityp NE 0 THEN
          cl-list.company   = guest.name + ", " + guest.vorname1 
            + " " + guest.anrede1 + guest.anredefirma .
        ELSE
          cl-list.company   = guest.name + ", " + guest.vorname1 
            + " " + guest.anrede1 + guest.anredefirma .

        IF cl-list.nat = "" THEN cl-list.nat = "?". 
        IF res-line.resstatus = 13 OR res-line.zimmerfix = YES THEN cl-list.qty = 0. 
     
        IF NOT split-rsv-print THEN /*ORIG*/
        DO:
            /*M 22 Jan 2011 - addition guest's comment */
            IF incl-gcomment THEN
            DO:
                FIND FIRST gbuff WHERE gbuff.gastnr = res-line.gastnrmember 
                    USE-INDEX gastnr_index NO-LOCK NO-ERROR.
                IF AVAILABLE gbuff THEN
                DO:
                    DO i = 1 TO LENGTH(gbuff.bemerk): 
                        IF SUBSTR(gbuff.bemerk,i,1) = CHR(10) THEN 
                            cl-list.bemerk = cl-list.bemerk + " ". 
                        ELSE cl-list.bemerk = cl-list.bemerk + SUBSTR(TRIM(gbuff.bemerk), i, 1). 
                    END.
                END.
                
                cl-list.bemerk = cl-list.bemerk + " || ".
            END.
    
            /*IT 200612 add reservation comment*/
            IF incl-rsvcomment THEN
            DO:
                FIND FIRST rbuff WHERE rbuff.resnr = reservation.resnr NO-LOCK NO-ERROR. /*Alder - Ticket A8CCB8*/
                IF AVAILABLE rbuff THEN
                DO:
                    DO j = 1 TO LENGTH(rbuff.bemerk):
                        IF SUBSTR(rbuff.bemerk,j,1) = CHR(10) THEN 
                            cl-list.bemerk1 = cl-list.bemerk1 + " ". 
                        ELSE cl-list.bemerk1 = cl-list.bemerk1 + SUBSTR(TRIM(rbuff.bemerk), j, 1). 
                    END.
                    
                END.
                /*cl-list.bemerk1 = " || " + cl-list.bemerk1.*/
                cl-list.bemerk = cl-list.bemerk  + cl-list.bemerk1 + " || ".
            END.
    
            DO i = 1 TO length(res-line.bemerk): 
                IF SUBSTR(res-line.bemerk,i,1) = chr(10) THEN 
                cl-list.bemerk = cl-list.bemerk + " ". 
                ELSE cl-list.bemerk = cl-list.bemerk + SUBSTR(TRIM(res-line.bemerk), i, 1). 
            END.

            /*DO add remark 1000 char*/    
            all-remark = res-line.bemerk.
            all-remark = REPLACE(all-remark,CHR(10)," ").
            all-remark = REPLACE(all-remark,CHR(13)," ").
            
            cl-list.bemerk01 = STRING(SUBSTRING(all-remark,1,225)).
            cl-list.bemerk02 = STRING(SUBSTRING(all-remark,226,225)).
            cl-list.bemerk03 = STRING(SUBSTRING(all-remark,451,225)).
            cl-list.bemerk04 = STRING(SUBSTRING(all-remark,676,225)).
            /*DO add remark 1000 char*/
        END.
        ELSE
        DO:
            DO i = 1 TO length(res-line.bemerk): 
                cl-list.bemerk = cl-list.bemerk + SUBSTR(TRIM(res-line.bemerk), i, 1).
            END.

            FIND FIRST rbuff WHERE rbuff.resnr = reservation.resnr NO-LOCK NO-ERROR. /*Alder - Ticket A8CCB8*/
            IF AVAILABLE rbuff THEN
            DO:
                cl-list.rsv-comment = rbuff.bemerk.                
            END.

            FIND FIRST gbuff WHERE gbuff.gastnr = res-line.gastnrmember 
                USE-INDEX gastnr_index NO-LOCK NO-ERROR.
            IF AVAILABLE gbuff THEN
            DO:
                cl-list.g-comment = gbuff.bemerk.
            END.

            FIND FIRST queasy WHERE queasy.KEY EQ 267
                AND queasy.number1 EQ res-line.resnr
                AND queasy.number2 EQ res-line.reslinnr NO-LOCK NO-ERROR.
            IF AVAILABLE queasy THEN
            DO:
                cl-list.other-comment = queasy.char1.
            END.
        END.        

        /* FD Comment 14/06/21, This condition get global ratecode, not ratecode per date
        DO i = 1 TO NUM-ENTRIES(res-line.zimmer-wunsch,";") - 1:
            str = ENTRY(i, res-line.zimmer-wunsch, ";").
            IF SUBSTR(str,1,6) = "$CODE$" THEN 
            DO:
              cl-list.ratecode  = SUBSTR(str,7).
              LEAVE.
            END.
        END.
        */

         /*DO j = 1 TO length(reservation.bemerk): 
          IF SUBSTR(reservation.bemerk,j,1) = chr(10) THEN 
          cl-list.bemerk1 = cl-list.bemerk1 + " ". 
          ELSE cl-list.bemerk1 = cl-list.bemerk1 + SUBSTR(TRIM(reservation.bemerk), j, 1). 
        DISP cl-list.bemerk1.
        END.*/

        /*DO j = 1 TO NUM-ENTRIES(res-line.zimmer-wunsch,";") - 1:
                str = ENTRY(i, res-line.zimmer-wunsch, ";").
                IF SUBSTR(str,1,6) = "$CODE$" THEN 
                DO:
                  cl-list.ratecode  = SUBSTR(str,7).
                  LEAVE.
                END.
            END.*/
        
        cl-list.pax = STRING(cl-list.a,">9") + "/" + STRING(cl-list.c,"9") 
          + " " + STRING(cl-list.co,"9"). 
     
        IF cl-list.nat = "" THEN cl-list.nat = "?". 
        ELSE 
        DO: 
          FIND FIRST nation WHERE nation.kurzbez = cl-list.nat NO-LOCK NO-ERROR. 
          IF AVAILABLE nation THEN cl-list.nation = nation.bezeich. 
        END. 

        FIND FIRST zinr-list WHERE zinr-list.zinr = res-line.zinr 
            AND zinr-list.resnr = res-line.resnr 
            AND zinr-list.reslinnr = res-line.reslinnr NO-ERROR.
        IF NOT AVAILABLE zinr-list THEN
        DO: 
          CREATE zinr-list.
          ASSIGN 
              zinr-list.resnr = res-line.resnr
              zinr-list.reslinnr = res-line.reslinnr
              zinr-list.zinr  = res-line.zinr.

          FIND FIRST queasy WHERE queasy.key = 14 AND queasy.char1 = res-line.zinr 
            AND queasy.date1 LE curr-date AND queasy.date2 GE curr-date 
            NO-LOCK NO-ERROR. 
          IF zimmer.sleeping /*MT*/ /*ITA 301213*/ AND res-line.resstatus NE 13 THEN 
          DO: 
             IF NOT AVAILABLE queasy THEN 
             DO:
               tot-rm = tot-rm + res-line.zimmeranz.
               tot-rmqty = tot-rmqty + res-line.zimmeranz.
             END.                  
             ELSE IF AVAILABLE queasy AND queasy.number3 NE res-line.gastnr THEN
             DO:
               tot-rm = tot-rm + res-line.zimmeranz.
               tot-rmqty = tot-rmqty + res-line.zimmeranz.
             END.                
          END.
          /*modify by bernatd EA4782 2025*/ 
          IF zimmer.sleeping AND (res-line.zipreis GT 0 OR res-line.zipreis = 0) AND res-line.resstatus NE 13 AND res-line.erwachs GT 0 THEN 
          DO: 
             IF NOT AVAILABLE queasy THEN tot-payrm = tot-payrm + res-line.zimmeranz. 
             ELSE IF AVAILABLE queasy AND queasy.number3 NE res-line.gastnr THEN 
               tot-payrm = tot-payrm + res-line.zimmeranz. 
          END. 
          ELSE IF NOT zimmer.sleeping THEN 
          DO: 
            IF AVAILABLE queasy AND queasy.number3 NE res-line.gastnr 
              AND res-line.zipreis GT 0 THEN
            DO:
              tot-rm = tot-rm + res-line.zimmeranz.
              tot-rmqty = tot-rmqty + res-line.zimmeranz.
            END.
                 
            inactive = inactive + 1.
          END. 
        END. 
     
        tot-a = tot-a + res-line.erwachs. 
        tot-c = tot-c + res-line.kind1 + res-line.kind2. 
        tot-co = tot-co + res-line.gratis. 

        IF exc-compli THEN /*bernatd add 9D155B 2025*/
        DO:
          tot-co = 0.
        END.
    END.
    
    IF NOT disp-accompany THEN
    DO:    
        FIND FIRST cl-list WHERE cl-list.rmno EQ res-line.zinr 
            AND cl-list.resnr EQ res-line.resnr 
            AND cl-list.arrive EQ res-line.ankunft 
            AND cl-list.zipreis EQ 0 AND (cl-list.a + cl-list.c) LT 1
            AND cl-list.co LT 1 EXCLUSIVE-LOCK NO-ERROR.
        IF AVAILABLE cl-list THEN
        DO:
            DELETE cl-list.
            RELEASE cl-list.
        END.
    END.

     /*add exclude Complimetn Bernatd 9D155B 2025*/
     IF exc-compli THEN
     DO:    
         FIND FIRST cl-list WHERE cl-list.rmno EQ res-line.zinr 
             AND cl-list.resnr EQ res-line.resnr 
             AND cl-list.arrive EQ res-line.ankunft 
             AND cl-list.co GT 0 EXCLUSIVE-LOCK NO-ERROR.
         IF AVAILABLE cl-list THEN
         DO:
             DELETE cl-list.
             RELEASE cl-list.
             tot-rm = tot-rm - 1.
         END.
     END.
     /*end bernatd*/
  END. 
  /*MT
  FOR EACH cl-list WHERE cl-list.zipreis NE 0 BY cl-list.nation BY cl-list.bezeich:
      FIND FIRST s-list WHERE s-list.bezeich = cl-list.bezeich
          AND s-list.nat EQ cl-list.nat NO-ERROR.
      IF NOT AVAILABLE s-list THEN
      DO:
          CREATE s-list.
          s-list.rmcat = cl-list.rmcat.
          s-list.bezeich = cl-list.bezeich.
          s-list.nat = cl-list.nat.
      END.
      s-list.anz = s-list.anz + cl-list.qty.
      s-list.adult = s-list.adult + cl-list.a + cl-list.co. 
      s-list.child = s-list.child + cl-list.c.
      
  END.
  */
  FOR EACH cl-list BY cl-list.nation BY cl-list.bezeich: 
    FIND FIRST s-list WHERE s-list.rmcat = cl-list.kurzbez NO-ERROR. 
    IF NOT AVAILABLE s-list THEN 
    DO: 
      FIND FIRST s-list WHERE s-list.rmcat = "" NO-ERROR. 
      IF AVAILABLE s-list THEN 
      DO: 
        s-list.rmcat = cl-list.kurzbez. 
        s-list.bezeich = cl-list.bezeich. 
      END. 
    END. 
    IF NOT AVAILABLE s-list THEN 
    DO: 
      create s-list. 
      s-list.rmcat = cl-list.kurzbez. 
      s-list.bezeich = cl-list.bezeich. 
    END. 
    s-list.anz = s-list.anz + cl-list.qty. 
 
    FIND FIRST s-list WHERE s-list.nat = cl-list.nat NO-ERROR. 
    IF NOT AVAILABLE s-list THEN 
    DO: 
      FIND FIRST s-list WHERE s-list.nat = "" NO-ERROR. 
      IF AVAILABLE s-list THEN s-list.nat = cl-list.nat. 
    END. 
    IF NOT AVAILABLE s-list THEN 
    DO: 
      create s-list. 
      IF AVAILABLE s-list THEN s-list.nat = cl-list.nat. 
    END. 
    s-list.adult = s-list.adult + cl-list.a + cl-list.co. 
    s-list.child = s-list.child + cl-list.c. 

    s-list.rmqty = s-list.rmqty + cl-list.qty.
  END. 
  
  IF (tot-a + tot-co) NE 0 THEN 
  FOR EACH s-list WHERE s-list.nat NE "": 
    FIND FIRST nation WHERE nation.kurzbez = s-list.nat NO-LOCK NO-ERROR. 
    IF AVAILABLE nation THEN s-list.nat = nation.bezeich. 
    s-list.proz = s-list.adult / (tot-a + tot-co) * 100. 
  END. 
 
END. 


PROCEDURE create-genstat-inhouse1: 
DEFINE VARIABLE i           AS INTEGER.
DEFINE VARIABLE j           AS INTEGER.
DEFINE VARIABLE vip-flag    AS CHAR. 
DEFINE VARIABLE nr          AS INTEGER INITIAL 0. 
DEFINE VARIABLE str AS CHAR.
DEFINE VARIABLE actflag1    AS INTEGER. 
DEFINE VARIABLE actflag2    AS INTEGER. 
DEFINE VARIABLE do-it       AS LOGICAL.
DEFINE BUFFER gmember       FOR guest. 
DEFINE BUFFER gbuff         FOR guest.
DEFINE BUFFER rbuff         FOR reservation.
 
  FOR EACH zinr-list:
      DELETE zinr-list.
  END.

  IF datum = curr-date THEN 
  DO: 
    actflag1 = 1. 
    actflag2 = 1. 
  END. 
  ELSE 
  DO: 
    actflag1 = 1. 
    actflag2 = 2. 
  END. 
 
  tot-payrm = 0. 
  tot-rm = 0. 
  tot-a = 0. 
  tot-c = 0. 
  tot-co = 0. 
  inactive = 0. 
 
  FOR EACH s-list: 
   delete s-list. 
  END. 
 
  FOR EACH cl-list: 
    delete cl-list. 
  END. 
 
  FOR EACH str-list: 
    delete str-list. 
  END. 
 
  tot-avail = 0. 
  FOR EACH zkstat WHERE zkstat.datum = datum NO-LOCK:
      tot-avail = tot-avail + zkstat.anz100.
  END.
/*
  FOR EACH zimmer WHERE zimmer.sleeping = YES NO-LOCK: 
    tot-avail = tot-avail + 1. 
  END. 
*/
  FOR EACH genstat WHERE genstat.datum = datum
    AND genstat.zinr GE froom AND genstat.zinr LE troom NO-LOCK,
    FIRST zimkateg WHERE zimkateg.zikatnr = genstat.zikatnr NO-LOCK, 
    FIRST reservation WHERE reservation.resnr = genstat.resnr NO-LOCK, 
    FIRST guest WHERE guest.gastnr = genstat.gastnr NO-LOCK, 
    FIRST gmember WHERE gmember.gastnr = genstat.gastnrmember NO-LOCK
    BY guest.karteityp descending BY guest.name BY guest.gastnr 
    BY gmember.name BY genstat.zinr
    /*BY genstat.zinr BY genstat.erwachs DESCENDING BY gmember.name*/
    :
    IF genstat.res-date[1] LT datum AND genstat.res-date[2] = datum
          AND genstat.resstatus = 8 THEN . /*FD Juni 22, 2020*/
    ELSE IF exc-depart AND genstat.res-date[1] LE datum AND genstat.res-date[2] = datum
        AND genstat.resstatus = 8 THEN . /*M exclude day use  181010*/
    ELSE
    DO:
        FIND FIRST res-line WHERE res-line.resnr = genstat.resnr
           AND res-line.reslinnr = genstat.res-int[1] NO-LOCK .
          FIND FIRST setup-list WHERE setup-list.nr = res-line.setup + 1. 

        FIND FIRST zimmer WHERE zimmer.zinr = genstat.zinr NO-LOCK NO-ERROR. 
        
        /*change*/
        IF curr-gastnr NE guest.gastnr THEN 
        DO: 
          nr = 0. 
          curr-gastnr = guest.gastnr. 
        END. 
        IF guest.karteityp GT 0 THEN nr = nr + 1. 

        /*nr = nr + 1. */
        vip-flag = "". 
        FIND FIRST guestseg WHERE guestseg.gastnr = gmember.gastnr 
          AND (guestseg.segmentcode = vipnr1 OR 
          guestseg.segmentcode = vipnr2 OR 
          guestseg.segmentcode = vipnr3 OR 
          guestseg.segmentcode = vipnr4 OR 
          guestseg.segmentcode = vipnr5 OR 
          guestseg.segmentcode = vipnr6 OR 
          guestseg.segmentcode = vipnr7 OR 
          guestseg.segmentcode = vipnr8 OR 
          guestseg.segmentcode = vipnr9) NO-LOCK NO-ERROR. 
        IF AVAILABLE guestseg THEN 
        DO: 
          FIND FIRST segment WHERE segment.segmentcode = guestseg.segmentcode
              NO-LOCK.
            ASSIGN vip-flag = segment.bezeich. 
        END.
     
        create cl-list. 
        ASSIGN 
          cl-list.nr        = nr 
    /* 
          cl-list.groupname = reservation.groupname 
    */ 
          cl-list.karteityp = guest.karteityp
          cl-list.rmcat     = zimkateg.kurzbez + setup-list.char 
          cl-list.kurzbez   = zimkateg.kurzbez 
          cl-list.bezeich   = zimkateg.bezeich 
          cl-list.nat       = gmember.nation1 
          cl-list.resnr     = genstat.resnr 
          cl-list.vip       = vip-flag 
          cl-list.name      = gmember.name  + ", " + gmember.vorname1 
                            + " " + gmember.anrede1
          cl-list.rmno      = genstat.zinr 
          cl-list.zipreis   = genstat.zipreis
          cl-list.arrive    = genstat.res-date[1] 
          cl-list.depart    = genstat.res-date[2] 
          cl-list.qty       = 1 
          cl-list.a         = genstat.erwachs
          cl-list.c         = genstat.kind1 + genstat.kind2 + genstat.kind3
          cl-list.co        = genstat.gratis 
          cl-list.argt      = genstat.argt 
          cl-list.flight    = SUBSTR(res-line.flight-nr, 12, 6) 
          cl-list.etd       = SUBSTR(res-line.flight-nr, 18, 5)
          cl-list.ci-time   = STRING(res-line.ankzeit, "HH:MM")
          cl-list.paym      = genstat.segmentcode
          cl-list.created   = reservation.resdat
          cl-list.createID  = reservation.useridanlage
          cl-list.etage     = zimmer.etage  
          cl-list.zinr-bez  = zimmer.bezeich
          cl-list.birthdate = gmember.geburtdatum1
          cl-list.telefon   = gmember.telefon /*add by bernatd 70F06C*/
          cl-list.mobil-tel = gmember.mobil-telefon /*add by bernatd 70F06C*/
          .

        IF res-line.resstatus NE 11 AND res-line.resstatus NE 13 THEN ASSIGN cl-list.flag-guest = 1.
        ELSE ASSIGN cl-list.flag-guest = 2.

        /*DODY 01/07/16 penambahan membership number dan type of membership */
        FIND FIRST mc-guest WHERE mc-guest.gastnr = gmember.gastnr NO-LOCK NO-ERROR.
        IF AVAILABLE mc-guest THEN /*FT serverless*/
        DO:
            cl-list.telefon   = gmember.telefon + ";" + mc-guest.cardnum.      /*SIS 31/01/13 */
            FIND FIRST mc-types WHERE mc-types.nr = mc-guest.nr NO-LOCK NO-ERROR.
            IF AVAILABLE mc-types THEN 
             cl-list.mobil-tel = gmember.mobil-telefon + ";" + mc-types.bezeich. /*SIS 31/01/13 */
            ELSE
             cl-list.mobil-tel = gmember.mobil-telefon. 
        END.                                            
        ELSE cl-list.telefon   = gmember.telefon.

        /*FD 15 April, 2021*/
        FIND FIRST nation WHERE nation.kurzbez EQ gmember.nation2 NO-LOCK NO-ERROR.
        IF AVAILABLE nation THEN cl-list.local-reg = nation.bezeich.

       /*/* new Jun 30 09 by LN*/
        FIND FIRST waehrung WHERE waehrung.waehrungsnr = res-line.betriebsnr 
            NO-LOCK NO-ERROR.
        IF AVAILABLE waehrung THEN
            cl-list.curr = waehrung.wabkurz.*/

       /*dody 23/09/16 penambahan email*/
        FIND FIRST waehrung WHERE waehrung.waehrungsnr = res-line.betriebsnr 
            NO-LOCK NO-ERROR.
        IF AVAILABLE waehrung THEN
            cl-list.curr = waehrung.wabkurz + ";" + gmember.email-adr.
       /*end dody*/ 

        /*ITA 130717 --> Add Request Patra*/
        FIND FIRST reslin-queasy WHERE reslin-queasy.KEY = "specialRequest"
             AND reslin-queasy.resnr = res-line.resnr 
             AND reslin-queasy.reslinnr = res-line.reslinnr NO-LOCK NO-ERROR.
        IF AVAILABLE reslin-queasy THEN
             ASSIGN cl-list.spreq = reslin-queasy.char3 + "," + cl-list.spreq.
        /*end*/

        /*FD Juny 14, 2021 => Get ratecode per date*/
        FIND FIRST reslin-queasy WHERE reslin-queasy.key EQ "arrangement" 
          AND reslin-queasy.resnr EQ res-line.resnr 
          AND reslin-queasy.reslinnr EQ res-line.reslinnr 
          AND datum GE reslin-queasy.date1 
          AND datum LE reslin-queasy.date2 NO-LOCK NO-ERROR. 
        IF AVAILABLE reslin-queasy THEN 
        DO:
          IF reslin-queasy.char2 NE "" THEN cl-list.ratecode = reslin-queasy.char2.
          ELSE
          DO:
            DO i = 1 TO NUM-ENTRIES(res-line.zimmer-wunsch,";") - 1:
              str = ENTRY(i, res-line.zimmer-wunsch, ";").
              IF SUBSTR(str,1,6) EQ "$CODE$" THEN 
              DO:
                cl-list.ratecode = SUBSTR(str,7).
                LEAVE.
              END.
            END.
          END.
        END.
        /*End FD*/

        FIND FIRST segment WHERE segment.segmentcode = genstat.segmentcode
            NO-LOCK NO-ERROR.
        IF AVAILABLE segment THEN cl-list.segm = ENTRY(1, segment.bezeich, "$$0").

        IF guest.karteityp NE 0 THEN
          cl-list.company   = guest.name + ", " + guest.vorname1 
            + " " + guest.anrede1 + guest.anredefirma .
        ELSE
          cl-list.company   = guest.name + ", " + guest.vorname1 
            + " " + guest.anrede1 + guest.anredefirma .

        IF cl-list.nat = "" THEN cl-list.nat = "?". 
        IF genstat.resstatus = 13 THEN cl-list.qty = 0. 
     
        IF NOT split-rsv-print THEN /*ORIG*/
        DO:
            /*M 22 Jan 2011 - addition guest's comment */
            IF incl-gcomment THEN
            DO:
                FIND FIRST gbuff WHERE gbuff.gastnr = res-line.gastnrmember 
                    USE-INDEX gastnr_index NO-LOCK NO-ERROR.
                IF AVAILABLE gbuff THEN
                DO:
                    DO i = 1 TO LENGTH(gbuff.bemerk): 
                        IF SUBSTR(gbuff.bemerk,i,1) = CHR(10) THEN 
                            cl-list.bemerk = cl-list.bemerk + " ". 
                        ELSE cl-list.bemerk = cl-list.bemerk + SUBSTR(TRIM(gbuff.bemerk), i, 1). 
                    END. 
                END.
                
                cl-list.bemerk = cl-list.bemerk + " || ".
            END.
           
            /*IT 200612 add reservation comment*/
            IF incl-rsvcomment THEN
            DO:
                FIND FIRST rbuff WHERE rbuff.resnr = reservation.resnr NO-LOCK NO-ERROR. /*Alder - Ticket A8CCB8*/
                IF AVAILABLE rbuff THEN
                DO:
                    DO j = 1 TO LENGTH(rbuff.bemerk):
                        IF SUBSTR(rbuff.bemerk,j,1) = CHR(10) THEN 
                            cl-list.bemerk1 = cl-list.bemerk1 + " ". 
                        ELSE cl-list.bemerk1 = cl-list.bemerk1 + SUBSTR(TRIM(rbuff.bemerk), j, 1). 
                    END.
                    
                END.
                /*cl-list.bemerk1 = " || " + cl-list.bemerk1.*/
                cl-list.bemerk = cl-list.bemerk  + cl-list.bemerk1 + " || ".
            END.
            
            DO i = 1 TO length(res-line.bemerk): 
                IF SUBSTR(res-line.bemerk,i,1) = chr(10) THEN 
                cl-list.bemerk = cl-list.bemerk + " ". 
                ELSE cl-list.bemerk = cl-list.bemerk + SUBSTR(TRIM(res-line.bemerk), i, 1). 
            END.

            /*DO add remark 1000 char*/
            all-remark = res-line.bemerk.
            all-remark = REPLACE(all-remark,CHR(10)," ").
            all-remark = REPLACE(all-remark,CHR(13)," ").
    
            cl-list.bemerk01 = STRING(SUBSTRING(all-remark,1,225)).
            cl-list.bemerk02 = STRING(SUBSTRING(all-remark,226,225)).
            cl-list.bemerk03 = STRING(SUBSTRING(all-remark,451,225)).
            cl-list.bemerk04 = STRING(SUBSTRING(all-remark,676,225)).
            /*naufal add remarks 2000 char*/
            /*cl-list.bemerk01 = STRING(SUBSTRING(all-remark,1,255)).
            cl-list.bemerk02 = STRING(SUBSTRING(all-remark,256,255)).
            cl-list.bemerk03 = STRING(SUBSTRING(all-remark,511,255)).
            cl-list.bemerk04 = STRING(SUBSTRING(all-remark,766,255)).
            cl-list.bemerk05 = STRING(SUBSTRING(all-remark,1021,255)).
            cl-list.bemerk06 = STRING(SUBSTRING(all-remark,1276,255)).
            cl-list.bemerk07 = STRING(SUBSTRING(all-remark,1531,255)).
            cl-list.bemerk08 = STRING(SUBSTRING(all-remark,1786,255)).*/
            /*end naufal add remarks 2000 char*/
            /*DO add remark 1000 char*/
        END.
        ELSE
        DO:
            DO i = 1 TO length(res-line.bemerk): 
                cl-list.bemerk = cl-list.bemerk + SUBSTR(TRIM(res-line.bemerk), i, 1).
            END.

            FIND FIRST rbuff WHERE rbuff.resnr = reservation.resnr NO-LOCK NO-ERROR. /*Alder - Ticket A8CCB8*/
            IF AVAILABLE rbuff THEN
            DO:
                cl-list.rsv-comment = rbuff.bemerk.                
            END.

            FIND FIRST gbuff WHERE gbuff.gastnr = res-line.gastnrmember 
                USE-INDEX gastnr_index NO-LOCK NO-ERROR.
            IF AVAILABLE gbuff THEN
            DO:
                cl-list.g-comment = gbuff.bemerk.
            END.

            FIND FIRST queasy WHERE queasy.KEY EQ 267
                AND queasy.number1 EQ res-line.resnr
                AND queasy.number2 EQ res-line.reslinnr NO-LOCK NO-ERROR.
            IF AVAILABLE queasy THEN
            DO:
                cl-list.other-comment = queasy.char1.
            END.
        END.        
        
        /* FD Comment 14/06/21, This condition get global ratecode, not ratecode per date
        DO i = 1 TO NUM-ENTRIES(res-line.zimmer-wunsch,";") - 1:
            str = ENTRY(i, res-line.zimmer-wunsch, ";").
            IF SUBSTR(str,1,6) = "$CODE$" THEN 
            DO:
              cl-list.ratecode  = SUBSTR(str,7).
              LEAVE.
            END.
        END.
        */

        /*DO j = 1 TO length(reservation.bemerk): 
          IF SUBSTR(reservation.bemerk,j,1) = chr(10) THEN 
          cl-list.bemerk1 = cl-list.bemerk1 + " ". 
          ELSE cl-list.bemerk1 = cl-list.bemerk1 + SUBSTR(TRIM(reservation.bemerk), j, 1). 
        DISP cl-list.bemerk1.
        END.*/

        /*DO j = 1 TO NUM-ENTRIES(res-line.zimmer-wunsch,";") - 1:
            str = ENTRY(i, res-line.zimmer-wunsch, ";").
            IF SUBSTR(str,1,6) = "$CODE$" THEN 
            DO:
              cl-list.ratecode  = SUBSTR(str,7).
              LEAVE.
            END.
        END.*/

        cl-list.pax = STRING(cl-list.a,">9") + "/" + STRING(cl-list.c,"9") 
          + " " + STRING(cl-list.co,"9"). 
     
        IF cl-list.nat = "" THEN cl-list.nat = "?". 
        ELSE 
        DO: 
          FIND FIRST nation WHERE nation.kurzbez = cl-list.nat NO-LOCK NO-ERROR. 
          IF AVAILABLE nation THEN cl-list.nation = nation.bezeich. 
        END. 

            
        FIND FIRST zinr-list WHERE zinr-list.zinr = genstat.zinr 
            AND zinr-list.resnr = res-line.resnr 
            AND zinr-list.reslinnr = res-line.reslinnr NO-ERROR.
        IF NOT AVAILABLE zinr-list THEN
        DO: 
          CREATE zinr-list.
          ASSIGN
              zinr-list.resnr = res-line.resnr
              zinr-list.reslinnr = res-line.reslinnr
              zinr-list.zinr  = genstat.zinr.

          FIND FIRST queasy WHERE queasy.key = 14 AND queasy.char1 = genstat.zinr 
            AND queasy.date1 LE curr-date AND queasy.date2 GE curr-date 
            NO-LOCK NO-ERROR. 
          IF zimmer.sleeping /*MT*/ /*ITA 301213*/ AND genstat.resstatus NE 13 THEN 
          DO: 
             IF NOT AVAILABLE queasy THEN
             DO:
               tot-rm = tot-rm + 1.
               tot-rmqty = tot-rmqty + 1.
             END.                  
             ELSE IF AVAILABLE queasy AND queasy.number3 NE genstat.gastnr THEN 
             DO:
               tot-rm = tot-rm + 1.
               tot-rmqty = tot-rmqty + 1.
             END.                  
          END. 
          /*modify by bernatd EA4782 2025*/
          IF zimmer.sleeping AND (genstat.zipreis GT 0 OR genstat.zipreis = 0 ) AND genstat.erwachs GT 0 AND genstat.resstatus NE 13 THEN 
          DO: 
             IF NOT AVAILABLE queasy THEN tot-payrm = tot-payrm + 1. 
             ELSE IF AVAILABLE queasy AND queasy.number3 NE genstat.gastnr THEN 
               tot-payrm = tot-payrm + 1. 
          END. 
          ELSE IF NOT zimmer.sleeping THEN 
          DO: 
            IF AVAILABLE queasy AND queasy.number3 NE genstat.gastnr 
              AND genstat.zipreis GT 0 THEN 
            DO:
              tot-rm = tot-rm + 1.
              tot-rmqty = tot-rmqty + 1.
            END.               
             
            inactive = inactive + 1.
          END. 
        END. 
     
        tot-a = tot-a + genstat.erwachs. 
        tot-c = tot-c + genstat.kind1 + genstat.kind2 + genstat.kind3. 
        tot-co = tot-co + genstat.gratis. 

        IF exc-compli THEN /*bernatd add 9D155B 2025*/
        DO:
          tot-co = 0.
        END.
    END.
    
    IF NOT disp-accompany THEN
    DO:    
        FIND FIRST cl-list WHERE cl-list.rmno EQ res-line.zinr 
            AND cl-list.resnr EQ res-line.resnr 
            AND cl-list.arrive EQ res-line.ankunft 
            AND cl-list.zipreis EQ 0 AND (cl-list.a + cl-list.c) LT 1
            AND cl-list.co LT 1 EXCLUSIVE-LOCK NO-ERROR.
        IF AVAILABLE cl-list THEN
        DO:
            DELETE cl-list.
            RELEASE cl-list.
        END.
    END.

     /*add exclude Complimetn Bernatd 9D155B 2025*/
     IF exc-compli THEN
     DO:    
         FIND FIRST cl-list WHERE cl-list.rmno EQ res-line.zinr 
             AND cl-list.resnr EQ res-line.resnr 
             AND cl-list.arrive EQ res-line.ankunft 
             AND cl-list.co GT 0 EXCLUSIVE-LOCK NO-ERROR.
         IF AVAILABLE cl-list THEN
         DO:
             DELETE cl-list.
             RELEASE cl-list.
             tot-rm = tot-rm - 1.
         END.
     END.
     /*end bernatd*/
  END. 
  /*MT
  FOR EACH cl-list WHERE cl-list.zipreis NE 0 BY cl-list.nation BY cl-list.bezeich:
      FIND FIRST s-list WHERE s-list.bezeich = cl-list.bezeich
          AND s-list.nat EQ cl-list.nat NO-ERROR.
      IF NOT AVAILABLE s-list THEN
      DO:
          CREATE s-list.
          s-list.rmcat = cl-list.rmcat.
          s-list.bezeich = cl-list.bezeich.
          s-list.nat = cl-list.nat.
      END.
      s-list.anz = s-list.anz + cl-list.qty.
      s-list.adult = s-list.adult + cl-list.a + cl-list.co. 
      s-list.child = s-list.child + cl-list.c.
      
  END.
  */
  FOR EACH cl-list BY cl-list.nation BY cl-list.bezeich: 
    /*ITA 021117*/
    FIND FIRST mealcoup WHERE mealcoup.NAME = "Breakfast" 
        AND mealcoup.resnr = cl-list.resnr
        AND mealcoup.zinr = cl-list.rmno  NO-LOCK NO-ERROR.
    IF AVAILABLE mealcoup THEN DO:
        ASSIGN cl-list.tot-bfast = mealcoup.verbrauch[1] + mealcoup.verbrauch[2] + mealcoup.verbrauch[3] + mealcoup.verbrauch[4] + mealcoup.verbrauch[5]
                                  + mealcoup.verbrauch[6] + mealcoup.verbrauch[7] + mealcoup.verbrauch[8] + mealcoup.verbrauch[9] + mealcoup.verbrauch[10]
                                  + mealcoup.verbrauch[11] + mealcoup.verbrauch[12] + mealcoup.verbrauch[13] + mealcoup.verbrauch[14] + mealcoup.verbrauch[15]
                                  + mealcoup.verbrauch[16] + mealcoup.verbrauch[17] + mealcoup.verbrauch[18] + mealcoup.verbrauch[19] + mealcoup.verbrauch[20]
                                  + mealcoup.verbrauch[21] + mealcoup.verbrauch[22] + mealcoup.verbrauch[23] + mealcoup.verbrauch[24] + mealcoup.verbrauch[25]
                                  + mealcoup.verbrauch[26] + mealcoup.verbrauch[27] + mealcoup.verbrauch[28] + mealcoup.verbrauch[29] + mealcoup.verbrauch[30]
                                  + mealcoup.verbrauch[31] + mealcoup.verbrauch[32].
    END.

    FIND FIRST s-list WHERE s-list.bezeich = cl-list.bezeich NO-ERROR. 
    IF NOT AVAILABLE s-list THEN 
    DO: 
      FIND FIRST s-list WHERE s-list.rmcat = "" NO-ERROR. 
      IF AVAILABLE s-list THEN 
      DO: 
        s-list.rmcat = cl-list.kurzbez. 
        s-list.bezeich = cl-list.bezeich. 
      END. 
    END. 
    IF NOT AVAILABLE s-list THEN 
    DO: 
      create s-list. 
      s-list.rmcat = cl-list.kurzbez. 
      s-list.bezeich = cl-list.bezeich. 
    END. 
    
    s-list.anz = s-list.anz + cl-list.qty. 
 
    FIND FIRST s-list WHERE s-list.nat = cl-list.nat NO-ERROR. 
    IF NOT AVAILABLE s-list THEN 
    DO: 
      FIND FIRST s-list WHERE s-list.nat = "" NO-ERROR. 
      IF AVAILABLE s-list THEN s-list.nat = cl-list.nat. 
    END. 
    IF NOT AVAILABLE s-list THEN 
    DO: 
      create s-list. 
      IF AVAILABLE s-list THEN s-list.nat = cl-list.nat. 
    END. 
    s-list.adult = s-list.adult + cl-list.a + cl-list.co. 
    s-list.child = s-list.child + cl-list.c. 

    s-list.rmqty = s-list.rmqty + cl-list.qty.
  END.
 
  IF (tot-a + tot-co) NE 0 THEN 
  FOR EACH s-list WHERE s-list.nat NE "": 
    FIND FIRST nation WHERE nation.kurzbez = s-list.nat NO-LOCK NO-ERROR. 
    IF AVAILABLE nation THEN s-list.nat = nation.bezeich. 
    s-list.proz = s-list.adult / (tot-a + tot-co) * 100. 
  END. 
 
END. 

PROCEDURE create-inhouse2: 
DEFINE VARIABLE i           AS INTEGER.
DEFINE VARIABLE j           AS INTEGER.
DEFINE VARIABLE vip-flag    AS CHAR. 
DEFINE VARIABLE nr          AS INTEGER INITIAL 0. 
DEFINE VARIABLE str         AS CHAR.
DEFINE VARIABLE actflag1    AS INTEGER. 
DEFINE VARIABLE actflag2    AS INTEGER. 
DEFINE VARIABLE do-it       AS LOGICAL.
DEFINE buffer gmember       FOR guest. 
DEFINE BUFFER gbuff         FOR guest.
DEFINE BUFFER rbuff         FOR reservation.
/*bernatd paying*/
  FOR EACH zinr-list:
      DELETE zinr-list.
  END.

  IF datum = curr-date THEN 
  DO: 
    actflag1 = 1. 
    actflag2 = 1. 
  END. 
  ELSE 
  DO: 
    actflag1 = 1. 
    actflag2 = 2. 
  END. 
 
  tot-payrm = 0. 
  tot-rm = 0. 
  tot-a = 0. 
  tot-c = 0. 
  tot-co = 0. 
  inactive = 0. 
 
  FOR EACH s-list: 
   delete s-list. 
  END. 
 
  FOR EACH cl-list: 
    delete cl-list. 
  END. 
 
  FOR EACH str-list: 
    delete str-list. 
  END. 
 
  tot-avail = 0. 
  FOR EACH zimmer WHERE zimmer.sleeping = YES NO-LOCK: 
    tot-avail = tot-avail + 1. 
  END. 
  
  FOR EACH res-line WHERE res-line.active-flag GE actflag1 
    AND res-line.active-flag LE actflag2 
    AND res-line.resstatus NE 9 AND res-line.resstatus NE 10 
    AND res-line.resstatus NE 12 AND res-line.ankunft LE datum 
    AND res-line.abreise GE datum 
    AND res-line.zinr GE froom AND res-line.zinr LE troom NO-LOCK, 
    FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr NO-LOCK, 
    FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
    FIRST guest WHERE guest.gastnr = reservation.gastnr NO-LOCK, 
    FIRST gmember WHERE gmember.gastnr = res-line.gastnrmember NO-LOCK,
    FIRST zimmer WHERE zimmer.zinr = res-line.zinr AND zimmer.sleeping NO-LOCK

    BY res-line.zinr BY res-line.erwachs DESCENDING BY res-line.name: 
    IF exc-depart AND res-line.abreise = datum THEN .
    ELSE
    DO:
        FIND FIRST setup-list WHERE setup-list.nr = res-line.setup + 1. 
        /*FIND FIRST zimmer WHERE zimmer.zinr = res-line.zinr NO-LOCK. */ /*Comment FD April 06, 2021*/
     
        nr = nr + 1. 
        vip-flag = "". 
        FIND FIRST guestseg WHERE guestseg.gastnr = gmember.gastnr 
          AND (guestseg.segmentcode = vipnr1 OR 
          guestseg.segmentcode = vipnr2 OR 
          guestseg.segmentcode = vipnr3 OR 
          guestseg.segmentcode = vipnr4 OR 
          guestseg.segmentcode = vipnr5 OR 
          guestseg.segmentcode = vipnr6 OR 
          guestseg.segmentcode = vipnr7 OR 
          guestseg.segmentcode = vipnr8 OR 
          guestseg.segmentcode = vipnr9) NO-LOCK NO-ERROR. 
        IF AVAILABLE guestseg THEN 
        DO: 
          FIND FIRST segment WHERE segment.segmentcode = guestseg.segmentcode
              NO-LOCK.
            ASSIGN vip-flag = segment.bezeich. 
        END.
     
        CREATE cl-list. 
        ASSIGN 
          cl-list.nr        = nr 
    /* 
          cl-list.groupname = reservation.groupname 
    */ 
          cl-list.rmcat     = zimkateg.kurzbez + setup-list.char 
          cl-list.kurzbez   = zimkateg.kurzbez 
          cl-list.bezeich   = zimkateg.bezeich 
          cl-list.nat       = gmember.nation1 
          cl-list.resnr     = res-line.resnr 
          cl-list.vip       = vip-flag 
          cl-list.name      = res-line.name 
          cl-list.rmno      = res-line.zinr 
          cl-list.zipreis   = res-line.zipreis
          cl-list.arrive    = res-line.ankunft 
          cl-list.depart    = res-line.abreise 
          cl-list.qty       = res-line.zimmeranz 
          cl-list.a         = res-line.erwachs 
          cl-list.c         = res-line.kind1 + res-line.kind2 
          cl-list.co        = res-line.gratis 
          cl-list.argt      = res-line.arrangement 
          cl-list.flight    = SUBSTR(res-line.flight-nr, 12, 6) 
          cl-list.etd       = SUBSTR(res-line.flight-nr, 18, 5) 
          cl-list.ci-time   = STRING(res-line.ankzeit, "HH:MM")
    /*    cl-list.paym      = INTEGER(res-line.code).  */ 
          cl-list.paym      = reservation.segmentcode
          cl-list.created   = reservation.resdat
          cl-list.createID  = reservation.useridanlage
          cl-list.etage     = zimmer.etage  
          cl-list.zinr-bez  = zimmer.bezeich
          cl-list.birthdate = gmember.geburtdatum1
          cl-list.telefon   = gmember.telefon /*add by bernatd*/
          cl-list.mobil-tel = gmember.mobil-telefon /*add by bernatd*/
          .

        IF res-line.resstatus NE 11 AND res-line.resstatus NE 13 THEN ASSIGN cl-list.flag-guest = 1.
        ELSE ASSIGN cl-list.flag-guest = 2.

        /*DODY 01/07/16 penambahan membership number dan type of membership */
        FIND FIRST mc-guest WHERE mc-guest.gastnr = gmember.gastnr NO-LOCK NO-ERROR.
        IF AVAILABLE mc-guest THEN /*FT serverless*/
        DO:
            cl-list.telefon   = gmember.telefon + ";" + mc-guest.cardnum.      /*SIS 31/01/13 */
            FIND FIRST mc-types WHERE mc-types.nr = mc-guest.nr NO-LOCK NO-ERROR.
            IF AVAILABLE mc-types THEN 
             cl-list.mobil-tel = gmember.mobil-telefon + ";" + mc-types.bezeich. /*SIS 31/01/13 */
            ELSE
             cl-list.mobil-tel = gmember.mobil-telefon. 
        END.                                            
        ELSE cl-list.telefon   = gmember.telefon.
        
        /*FD 15 April, 2021*/
        FIND FIRST nation WHERE nation.kurzbez EQ gmember.nation2 NO-LOCK NO-ERROR.
        IF AVAILABLE nation THEN cl-list.local-reg = nation.bezeich.

        /*/* new Jun 30 09 by LN*/
        FIND FIRST waehrung WHERE waehrung.waehrungsnr = res-line.betriebsnr 
            NO-LOCK NO-ERROR.
        IF AVAILABLE waehrung THEN
            cl-list.curr = waehrung.wabkurz.*/

       /*dody 23/09/16 penambahan email*/
        FIND FIRST waehrung WHERE waehrung.waehrungsnr = res-line.betriebsnr 
            NO-LOCK NO-ERROR.
        IF AVAILABLE waehrung THEN
            cl-list.curr = waehrung.wabkurz + ";" + gmember.email-adr.
        /*end dody*/
        
        /*ITA 130717 --> Add Request Patra*/
        FIND FIRST reslin-queasy WHERE reslin-queasy.KEY = "specialRequest"
             AND reslin-queasy.resnr = res-line.resnr 
             AND reslin-queasy.reslinnr = res-line.reslinnr NO-LOCK NO-ERROR.
        IF AVAILABLE reslin-queasy THEN
             ASSIGN cl-list.spreq = reslin-queasy.char3 + "," + cl-list.spreq.
        /*end*/

        /*FD Juny 14, 2021 => Get ratecode per date*/
        FIND FIRST reslin-queasy WHERE reslin-queasy.key EQ "arrangement" 
          AND reslin-queasy.resnr EQ res-line.resnr 
          AND reslin-queasy.reslinnr EQ res-line.reslinnr 
          AND datum GE reslin-queasy.date1 
          AND datum LE reslin-queasy.date2 NO-LOCK NO-ERROR. 
        IF AVAILABLE reslin-queasy THEN 
        DO:
          IF reslin-queasy.char2 NE "" THEN cl-list.ratecode = reslin-queasy.char2.
          ELSE
          DO:
            DO i = 1 TO NUM-ENTRIES(res-line.zimmer-wunsch,";") - 1:
              str = ENTRY(i, res-line.zimmer-wunsch, ";").
              IF SUBSTR(str,1,6) EQ "$CODE$" THEN 
              DO:
                cl-list.ratecode = SUBSTR(str,7).
                LEAVE.
              END.
            END.
          END.
        END.
        /*End FD*/

        /*ITA 021117*/
        FIND FIRST mealcoup WHERE mealcoup.NAME = "Breakfast" 
            AND mealcoup.resnr = res-line.resnr
            AND mealcoup.zinr = res-line.zinr  NO-LOCK NO-ERROR.
        IF AVAILABLE mealcoup THEN DO:
            ASSIGN cl-list.tot-bfast = mealcoup.verbrauch[1] + mealcoup.verbrauch[2] + mealcoup.verbrauch[3] + mealcoup.verbrauch[4] + mealcoup.verbrauch[5]
                                      + mealcoup.verbrauch[6] + mealcoup.verbrauch[7] + mealcoup.verbrauch[8] + mealcoup.verbrauch[9] + mealcoup.verbrauch[10]
                                      + mealcoup.verbrauch[11] + mealcoup.verbrauch[12] + mealcoup.verbrauch[13] + mealcoup.verbrauch[14] + mealcoup.verbrauch[15]
                                      + mealcoup.verbrauch[16] + mealcoup.verbrauch[17] + mealcoup.verbrauch[18] + mealcoup.verbrauch[19] + mealcoup.verbrauch[20]
                                      + mealcoup.verbrauch[21] + mealcoup.verbrauch[22] + mealcoup.verbrauch[23] + mealcoup.verbrauch[24] + mealcoup.verbrauch[25]
                                      + mealcoup.verbrauch[26] + mealcoup.verbrauch[27] + mealcoup.verbrauch[28] + mealcoup.verbrauch[29] + mealcoup.verbrauch[30]
                                      + mealcoup.verbrauch[31] + mealcoup.verbrauch[32].
        END.
        /*end*/

        FIND FIRST segment WHERE segment.segmentcode = reservation.segmentcode
            NO-LOCK NO-ERROR.
        IF AVAILABLE segment THEN cl-list.segm = ENTRY(1, segment.bezeich, "$$0").

        IF guest.karteityp NE 0 THEN
          cl-list.company   = guest.name + ", " + guest.vorname1 
            + " " + guest.anrede1 + guest.anredefirma .
        ELSE
          cl-list.company   = guest.name + ", " + guest.vorname1 
            + " " + guest.anrede1 + guest.anredefirma .

        IF cl-list.nat = "" THEN cl-list.nat = "?". 
        IF res-line.resstatus = 13 OR res-line.zimmerfix THEN cl-list.qty = 0. 
     
        IF NOT split-rsv-print THEN /*ORIG*/
        DO:
            /*M 22 Jan 2011 - addition guest's comment */
            IF incl-gcomment THEN
            DO:
                FIND FIRST gbuff WHERE gbuff.gastnr = res-line.gastnrmember 
                    USE-INDEX gastnr_index NO-LOCK NO-ERROR.
                IF AVAILABLE gbuff THEN
                DO:
                    DO i = 1 TO LENGTH(gbuff.bemerk): 
                        IF SUBSTR(gbuff.bemerk,i,1) = CHR(10) THEN 
                            cl-list.bemerk = cl-list.bemerk + " ". 
                        ELSE cl-list.bemerk = cl-list.bemerk + SUBSTR(TRIM(gbuff.bemerk), i, 1).
                    END.
                    
                END.
                
                cl-list.bemerk = cl-list.bemerk + " || ".
            END.
            /*IT 200612 add reservation comment*/
            IF incl-rsvcomment THEN        
            DO:
                FIND FIRST rbuff WHERE rbuff.resnr = reservation.resnr NO-LOCK NO-ERROR. /*Alder - Ticket A8CCB8*/
                IF AVAILABLE rbuff THEN
                DO:
                    DO j = 1 TO LENGTH(rbuff.bemerk):
                        IF SUBSTR(rbuff.bemerk,j,1) = CHR(10) THEN 
                            cl-list.bemerk1 = cl-list.bemerk1 + " ". 
                        ELSE cl-list.bemerk1 = cl-list.bemerk1 + SUBSTR(TRIM(rbuff.bemerk), j, 1). 
                    END.
                    
                END.
                /*cl-list.bemerk1 = " || " + cl-list.bemerk1.*/
                cl-list.bemerk = cl-list.bemerk  + cl-list.bemerk1 + " || ".
            END.
                
            DO i = 1 TO length(res-line.bemerk): 
                IF SUBSTR(res-line.bemerk,i,1) = chr(10) THEN 
                cl-list.bemerk = cl-list.bemerk + " ". 
                ELSE cl-list.bemerk = cl-list.bemerk + SUBSTR(TRIM(res-line.bemerk), i, 1).
            END.

            /*DO add remark 1000 char*/
            all-remark = res-line.bemerk.
            all-remark = REPLACE(all-remark,CHR(10)," ").
            all-remark = REPLACE(all-remark,CHR(13)," ").
    
            cl-list.bemerk01 = STRING(SUBSTRING(all-remark,1,225)).
            cl-list.bemerk02 = STRING(SUBSTRING(all-remark,226,225)).
            cl-list.bemerk03 = STRING(SUBSTRING(all-remark,451,225)).
            cl-list.bemerk04 = STRING(SUBSTRING(all-remark,676,225)).
            /*DO add remark 1000 char*/
        END.
        ELSE
        DO:
            DO i = 1 TO length(res-line.bemerk): 
                cl-list.bemerk = cl-list.bemerk + SUBSTR(TRIM(res-line.bemerk), i, 1).
            END.

            FIND FIRST rbuff WHERE rbuff.resnr = reservation.resnr NO-LOCK NO-ERROR. /*Alder - Ticket A8CCB8*/
            IF AVAILABLE rbuff THEN
            DO:
                cl-list.rsv-comment = rbuff.bemerk.                
            END.

            FIND FIRST gbuff WHERE gbuff.gastnr = res-line.gastnrmember 
                USE-INDEX gastnr_index NO-LOCK NO-ERROR.
            IF AVAILABLE gbuff THEN
            DO:
                cl-list.g-comment = gbuff.bemerk.
            END.

            FIND FIRST queasy WHERE queasy.KEY EQ 267
                AND queasy.number1 EQ res-line.resnr
                AND queasy.number2 EQ res-line.reslinnr NO-LOCK NO-ERROR.
            IF AVAILABLE queasy THEN
            DO:
                cl-list.other-comment = queasy.char1.
            END.
        END.
        /*DO j = 1 TO length(reservation.bemerk): 
          IF SUBSTR(reservation.bemerk,j,1) = chr(10) THEN 
          cl-list.bemerk = cl-list.bemerk1 + " ". 
          ELSE cl-list.bemerk = cl-list.bemerk1 + SUBSTR(TRIM(reservation.bemerk), j, 1). 
        END.*/
         
        /*DO j = 1 TO NUM-ENTRIES(res-line.zimmer-wunsch,";") - 1:
            str = ENTRY(j, res-line.zimmer-wunsch, ";").
            IF SUBSTR(str,1,6) = "$CODE$" THEN 
            DO:
              cl-list.ratecode  = SUBSTR(str,7).
              LEAVE.
            END.
        END.*/        

        /* FD Comment 14/06/21, This condition get global ratecode, not ratecode per date
        DO i = 1 TO NUM-ENTRIES(res-line.zimmer-wunsch,";") - 1:
            str = ENTRY(i, res-line.zimmer-wunsch, ";").
            IF SUBSTR(str,1,6) = "$CODE$" THEN 
            DO:
              cl-list.ratecode  = SUBSTR(str,7).
              LEAVE.
            END.
        END.
        */        

        cl-list.pax = STRING(cl-list.a,">9") + "/" + STRING(cl-list.c,"9") 
          + " " + STRING(cl-list.co,"9"). 
     
        IF cl-list.nat = "" THEN cl-list.nat = "?". 
        ELSE 
        DO: 
          FIND FIRST nation WHERE nation.kurzbez = cl-list.nat NO-LOCK NO-ERROR. 
          IF AVAILABLE nation THEN cl-list.nation = nation.bezeich. 
        END.
  
        FIND FIRST zinr-list WHERE zinr-list.zinr = res-line.zinr 
            AND zinr-list.resnr = res-line.resnr 
            AND zinr-list.reslinnr = res-line.reslinnr NO-ERROR.
        IF NOT AVAILABLE zinr-list THEN
        DO: 
          CREATE zinr-list.
          ASSIGN
              zinr-list.resnr = res-line.resnr
              zinr-list.reslinnr = res-line.reslinnr
              zinr-list.zinr  = res-line.zinr.

          FIND FIRST queasy WHERE queasy.key = 14 AND queasy.char1 = res-line.zinr 
            AND queasy.date1 LE curr-date AND queasy.date2 GE curr-date 
            NO-LOCK NO-ERROR. 
          IF zimmer.sleeping AND /*ITA 301213*/ res-line.resstatus NE 13 THEN 
          DO: 
             IF NOT AVAILABLE queasy THEN 
             DO: 
               tot-rm = tot-rm + res-line.zimmeranz. 
               tot-rmqty = tot-rmqty + res-line.zimmeranz.
             END.
             ELSE IF AVAILABLE queasy AND queasy.number3 NE res-line.gastnr THEN 
             DO:
               tot-rm = tot-rm + res-line.zimmeranz.
               tot-rmqty = tot-rmqty + res-line.zimmeranz.
             END.
               
          END. 

          /*modify by bernatd EA4782 2025*/
          IF zimmer.sleeping AND (res-line.zipreis GT 0 OR res-line.zipreis = 0) AND res-line.resstatus NE 13 AND res-line.erwachs GT 0 THEN 
          DO: 
             IF NOT AVAILABLE queasy THEN tot-payrm = tot-payrm + res-line.zimmeranz. 
             ELSE IF AVAILABLE queasy AND queasy.number3 NE res-line.gastnr THEN 
               tot-payrm = tot-payrm + res-line.zimmeranz. 
          END. 
          ELSE IF NOT zimmer.sleeping THEN 
          DO: 
            IF AVAILABLE queasy AND queasy.number3 NE res-line.gastnr 
              AND res-line.zipreis GT 0 THEN 
            DO:
              tot-rm = tot-rm + res-line.zimmeranz.
              tot-rmqty = tot-rmqty + res-line.zimmeranz.
            END.      
           
            inactive = inactive + 1.
          END. 
        END. 
     
        tot-a = tot-a + res-line.erwachs. 
        tot-c = tot-c + res-line.kind1 + res-line.kind2. 
        tot-co = tot-co + res-line.gratis. 

        IF exc-compli THEN /*bernatd add 9D155B 2025*/
        DO:
          tot-co = 0.
        END.
    END.
    
    IF NOT disp-accompany THEN
    DO:    
        FIND FIRST cl-list WHERE cl-list.rmno EQ res-line.zinr 
            AND cl-list.resnr EQ res-line.resnr 
            AND cl-list.arrive EQ res-line.ankunft 
            AND cl-list.zipreis EQ 0 AND (cl-list.a + cl-list.c) LT 1
            AND cl-list.co LT 1 EXCLUSIVE-LOCK NO-ERROR.
        IF AVAILABLE cl-list THEN
        DO:
            DELETE cl-list.
            RELEASE cl-list.
        END.
    END.

     /*add exclude Complimetn Bernatd 9D155B 2025*/
     IF exc-compli THEN
     DO:    
         FIND FIRST cl-list WHERE cl-list.rmno EQ res-line.zinr 
             AND cl-list.resnr EQ res-line.resnr 
             AND cl-list.arrive EQ res-line.ankunft 
             AND cl-list.co GT 0 EXCLUSIVE-LOCK NO-ERROR.
         IF AVAILABLE cl-list THEN
         DO:
             DELETE cl-list.
             RELEASE cl-list.
             tot-rm = tot-rm - 1.
         END.
     END.
     /*end bernatd*/
  END. 
  /*MT
  FOR EACH cl-list WHERE cl-list.zipreis NE 0 BY cl-list.nation BY cl-list.bezeich:
      FIND FIRST s-list WHERE s-list.bezeich = cl-list.bezeich
          AND s-list.nat EQ cl-list.nat NO-ERROR.
      IF NOT AVAILABLE s-list THEN
      DO:
          CREATE s-list.
          s-list.rmcat = cl-list.rmcat.
          s-list.bezeich = cl-list.bezeich.
          s-list.nat = cl-list.nat.
      END.
      s-list.anz = s-list.anz + cl-list.qty.
      s-list.adult = s-list.adult + cl-list.a + cl-list.co. 
      s-list.child = s-list.child + cl-list.c.
  END.
  FOR EACH s-list:
      DISP s-list.rmcat s-list.nat.
  END.
  */
  FOR EACH cl-list BY cl-list.nation BY cl-list.bezeich: 
    FIND FIRST s-list WHERE s-list.rmcat = cl-list.kurzbez NO-ERROR. 
    IF NOT AVAILABLE s-list THEN 
    DO: 
      FIND FIRST s-list WHERE s-list.rmcat = "" NO-ERROR. 
      IF AVAILABLE s-list THEN
      DO: 
        s-list.rmcat = cl-list.kurzbez. 
        s-list.bezeich = cl-list.bezeich. 
      END. 
    END. 
    IF NOT AVAILABLE s-list THEN 
    DO: 
      create s-list. 
      s-list.rmcat = cl-list.kurzbez. 
      s-list.bezeich = cl-list.bezeich. 
    END. 
    
    s-list.anz = s-list.anz + cl-list.qty. 
 
    FIND FIRST s-list WHERE s-list.nat = cl-list.nat NO-ERROR. 
    IF NOT AVAILABLE s-list THEN 
    DO: 
      FIND FIRST s-list WHERE s-list.nat = "" NO-ERROR. 
      IF AVAILABLE s-list THEN s-list.nat = cl-list.nat. 
    END. 
    IF NOT AVAILABLE s-list THEN 
    DO: 
      create s-list. 
      IF AVAILABLE s-list THEN s-list.nat = cl-list.nat. 
    END. 
    
    s-list.adult = s-list.adult + cl-list.a + cl-list.co. 
    s-list.child = s-list.child + cl-list.c.

    s-list.rmqty = s-list.rmqty + cl-list.qty.
  END. 
 

  IF (tot-a + tot-co) NE 0 THEN 
  FOR EACH s-list WHERE s-list.nat NE "": 
    FIND FIRST nation WHERE nation.kurzbez = s-list.nat NO-LOCK NO-ERROR. 
    IF AVAILABLE nation THEN s-list.nat = nation.bezeich. 
    s-list.proz = s-list.adult / (tot-a + tot-co) * 100. 
  END. 
END. 

PROCEDURE create-genstat-inhouse2: 
DEFINE VARIABLE i           AS INTEGER.
DEFINE VARIABLE j           AS INTEGER.
DEFINE VARIABLE vip-flag    AS CHAR. 
DEFINE VARIABLE nr          AS INTEGER INITIAL 0. 
DEFINE VARIABLE str AS CHAR.
DEFINE VARIABLE actflag1    AS INTEGER. 
DEFINE VARIABLE actflag2    AS INTEGER. 
DEFINE VARIABLE do-it       AS LOGICAL.
DEFINE buffer gmember       FOR guest. 
DEFINE BUFFER gbuff         FOR guest.
DEFINE BUFFER rbuff         FOR reservation.

  FOR EACH zinr-list:
      DELETE zinr-list.
  END.

  IF datum = curr-date THEN 
  DO: 
    actflag1 = 1. 
    actflag2 = 1. 
  END. 
  ELSE 
  DO: 
    actflag1 = 1. 
    actflag2 = 2. 
  END. 
 
  tot-payrm = 0. 
  tot-rm = 0. 
  tot-a = 0. 
  tot-c = 0. 
  tot-co = 0. 
  inactive = 0. 
 
  FOR EACH s-list: 
   delete s-list. 
  END. 
 
  FOR EACH cl-list: 
    delete cl-list. 
  END. 
 
  FOR EACH str-list: 
    delete str-list. 
  END. 
 
  tot-avail = 0. 
  FOR EACH zkstat WHERE zkstat.datum = datum NO-LOCK:
      tot-avail = tot-avail + zkstat.anz100.
  END.
/*
  FOR EACH zimmer WHERE zimmer.sleeping = YES NO-LOCK: 
    tot-avail = tot-avail + 1. 
  END. 
*/ 
  DEF VAR z AS INT.
  FOR EACH genstat WHERE genstat.datum = datum
      AND genstat.zinr GE froom AND genstat.zinr LE troom NO-LOCK,
    FIRST zimkateg WHERE zimkateg.zikatnr = genstat.zikatnr NO-LOCK, 
    FIRST reservation WHERE reservation.resnr = genstat.resnr NO-LOCK, 
    FIRST guest WHERE guest.gastnr = genstat.gastnr NO-LOCK, 
    FIRST gmember WHERE gmember.gastnr = genstat.gastnrmember NO-LOCK,
    FIRST zimmer WHERE zimmer.zinr = genstat.zinr AND zimmer.sleeping NO-LOCK
    BY genstat.zinr BY genstat.erwachs DESCENDING BY gmember.name: 
    
    IF genstat.res-date[1] LT datum AND genstat.res-date[2] = datum
          AND genstat.resstatus = 8 THEN . /*FD Juni 22, 2020*/
    ELSE IF exc-depart AND genstat.res-date[1] LE datum AND genstat.res-date[2] = datum
          AND genstat.resstatus = 8 THEN . /*M exclude day use  181010*/
    ELSE
    DO:
        FIND FIRST res-line WHERE res-line.resnr = genstat.resnr
           AND res-line.reslinnr = genstat.res-int[1] NO-LOCK .
        FIND FIRST setup-list WHERE setup-list.nr = res-line.setup + 1. 

        /*FIND FIRST zimmer WHERE zimmer.zinr = genstat.zinr NO-LOCK . */ /*Comment FD April 06, 2021*/
     
        nr = nr + 1. 
        vip-flag = "". 
        FIND FIRST guestseg WHERE guestseg.gastnr = gmember.gastnr 
          AND (guestseg.segmentcode = vipnr1 OR 
          guestseg.segmentcode = vipnr2 OR 
          guestseg.segmentcode = vipnr3 OR 
          guestseg.segmentcode = vipnr4 OR 
          guestseg.segmentcode = vipnr5 OR 
          guestseg.segmentcode = vipnr6 OR 
          guestseg.segmentcode = vipnr7 OR 
          guestseg.segmentcode = vipnr8 OR 
          guestseg.segmentcode = vipnr9) NO-LOCK NO-ERROR. 
        IF AVAILABLE guestseg THEN 
        DO: 
          FIND FIRST segment WHERE segment.segmentcode = guestseg.segmentcode
            NO-LOCK.
          vip-flag = REPLACE(segment.bezeich, " ", "").
        END.
     
        create cl-list. 
        ASSIGN 
          cl-list.nr        = nr 
    /* 
          cl-list.groupname = reservation.groupname 
    */ 
          cl-list.rmcat     = zimkateg.kurzbez + setup-list.char 
          cl-list.kurzbez   = zimkateg.kurzbez 
          cl-list.bezeich   = zimkateg.bezeich 
          cl-list.nat       = gmember.nation1 
          cl-list.resnr     = genstat.resnr 
          cl-list.vip       = vip-flag 
          cl-list.name      = gmember.name  + ", " + gmember.vorname1 
                            + " " + gmember.anrede1
          cl-list.rmno      = genstat.zinr 
          cl-list.zipreis   = genstat.zipreis
          cl-list.arrive    = genstat.res-date[1] 
          cl-list.depart    = genstat.res-date[2] 
          cl-list.qty       = 1 
          cl-list.a         = genstat.erwachs
          cl-list.c         = genstat.kind1 + genstat.kind2 + genstat.kind3
          cl-list.co        = genstat.gratis 
          cl-list.argt      = genstat.argt 
          cl-list.flight    = SUBSTR(res-line.flight-nr, 12, 6) 
          cl-list.etd       = SUBSTR(res-line.flight-nr, 18, 5) 
          cl-list.ci-time   = STRING(res-line.ankzeit, "HH:MM")
          cl-list.paym      = genstat.segmentcode
          cl-list.created   = reservation.resdat
          cl-list.createID  = reservation.useridanlage
          cl-list.etage     = zimmer.etage  
          cl-list.zinr-bez  = zimmer.bezeich
          cl-list.birthdate = gmember.geburtdatum1
          cl-list.telefon   = gmember.telefon /*add by bernatd 70F06C*/
          cl-list.mobil-tel = gmember.mobil-telefon /*add by bernatd 70F06C*/
          .

        IF res-line.resstatus NE 11 AND res-line.resstatus NE 13 THEN ASSIGN cl-list.flag-guest = 1.
        ELSE ASSIGN cl-list.flag-guest = 2.

        /*DODY 01/07/16 penambahan membership number dan type of membership */
        FIND FIRST mc-guest WHERE mc-guest.gastnr = gmember.gastnr NO-LOCK NO-ERROR.
        IF AVAILABLE mc-guest THEN /*FT serverless*/
        DO:
            cl-list.telefon   = gmember.telefon + ";" + mc-guest.cardnum.      /*SIS 31/01/13 */
            FIND FIRST mc-types WHERE mc-types.nr = mc-guest.nr NO-LOCK NO-ERROR.
            IF AVAILABLE mc-types THEN 
             cl-list.mobil-tel = gmember.mobil-telefon + ";" + mc-types.bezeich. /*SIS 31/01/13 */
            ELSE
             cl-list.mobil-tel = gmember.mobil-telefon. 
        END.                                            
        ELSE cl-list.telefon   = gmember.telefon.
        
        /*FD 15 April, 2021*/
        FIND FIRST nation WHERE nation.kurzbez EQ gmember.nation2 NO-LOCK NO-ERROR.
        IF AVAILABLE nation THEN cl-list.local-reg = nation.bezeich.

        /*/* new Jun 30 09 by LN*/
        FIND FIRST waehrung WHERE waehrung.waehrungsnr = res-line.betriebsnr 
            NO-LOCK NO-ERROR.
        IF AVAILABLE waehrung THEN
            cl-list.curr = waehrung.wabkurz.*/

       /*dody 23/09/16 penambahan email*/
        FIND FIRST waehrung WHERE waehrung.waehrungsnr = res-line.betriebsnr 
            NO-LOCK NO-ERROR.
        IF AVAILABLE waehrung THEN
            cl-list.curr = waehrung.wabkurz + ";" + gmember.email-adr.
        /*end dody*/

        /*ITA 130717 --> Add Request Patra*/
        FIND FIRST reslin-queasy WHERE reslin-queasy.KEY = "specialRequest"
             AND reslin-queasy.resnr = res-line.resnr 
             AND reslin-queasy.reslinnr = res-line.reslinnr NO-LOCK NO-ERROR.
        IF AVAILABLE reslin-queasy THEN
             ASSIGN cl-list.spreq = reslin-queasy.char3 + "," + cl-list.spreq.
        /*end*/

        /*FD Juny 14, 2021 => Get ratecode per date*/
        FIND FIRST reslin-queasy WHERE reslin-queasy.key EQ "arrangement" 
          AND reslin-queasy.resnr EQ res-line.resnr 
          AND reslin-queasy.reslinnr EQ res-line.reslinnr 
          AND datum GE reslin-queasy.date1 
          AND datum LE reslin-queasy.date2 NO-LOCK NO-ERROR. 
        IF AVAILABLE reslin-queasy THEN 
        DO:
          IF reslin-queasy.char2 NE "" THEN cl-list.ratecode = reslin-queasy.char2.
          ELSE
          DO:
            DO i = 1 TO NUM-ENTRIES(res-line.zimmer-wunsch,";") - 1:
              str = ENTRY(i, res-line.zimmer-wunsch, ";").
              IF SUBSTR(str,1,6) EQ "$CODE$" THEN 
              DO:
                cl-list.ratecode = SUBSTR(str,7).
                LEAVE.
              END.
            END.
          END.
        END.
        /*End FD*/

        FIND FIRST segment WHERE segment.segmentcode = genstat.segmentcode
            NO-LOCK NO-ERROR.
        IF AVAILABLE segment THEN cl-list.segm = ENTRY(1, segment.bezeich, "$$0").

        IF guest.karteityp NE 0 THEN
          cl-list.company   = guest.name + ", " + guest.vorname1 
            + " " + guest.anrede1 + guest.anredefirma .
        ELSE
          cl-list.company   = guest.name + ", " + guest.vorname1 
            + " " + guest.anrede1 + guest.anredefirma .

        IF cl-list.nat = "" THEN cl-list.nat = "?". 
        IF genstat.resstatus = 13 THEN cl-list.qty = 0. 
     
        IF NOT split-rsv-print THEN
        DO:
            /*M 22 Jan 2011 - addition guest's comment */        
            IF incl-gcomment THEN
            DO:
                FIND FIRST gbuff WHERE gbuff.gastnr = res-line.gastnrmember 
                    USE-INDEX gastnr_index NO-LOCK NO-ERROR.
                IF AVAILABLE gbuff THEN
                DO:
                    DO i = 1 TO LENGTH(gbuff.bemerk): 
                        IF SUBSTR(gbuff.bemerk,i,1) = CHR(10) THEN 
                            cl-list.bemerk = cl-list.bemerk + " ". 
                        ELSE cl-list.bemerk = cl-list.bemerk + SUBSTR(TRIM(gbuff.bemerk), i, 1). 
                    END. 
                END.
    
                cl-list.bemerk = cl-list.bemerk + " || ".
            END. 
            
            /*IT 200612 add reservation comment*/
            IF incl-rsvcomment THEN
            DO:
                FIND FIRST rbuff WHERE rbuff.resnr = reservation.resnr NO-LOCK NO-ERROR. /*Alder - Ticket A8CCB8*/
                IF AVAILABLE rbuff THEN
                DO:
                    DO j = 1 TO LENGTH(rbuff.bemerk):
                        IF SUBSTR(rbuff.bemerk,j,1) = CHR(10) THEN 
                            cl-list.bemerk1 = cl-list.bemerk1 + " ". 
                        ELSE cl-list.bemerk1 = cl-list.bemerk1 + SUBSTR(TRIM(rbuff.bemerk), j, 1). 
                    END.
                    
                END.
                /*cl-list.bemerk1 = " || " + cl-list.bemerk1.*/
                cl-list.bemerk = cl-list.bemerk  + cl-list.bemerk1 + " || ".
            END.
            
            DO i = 1 TO LENGTH(res-line.bemerk): 
              IF SUBSTR(res-line.bemerk,i,1) = chr(10) THEN 
                  cl-list.bemerk = cl-list.bemerk + " ". 
              ELSE cl-list.bemerk = cl-list.bemerk + 
                  SUBSTR(TRIM(res-line.bemerk), i, 1). 
            END.

            /*DO add remark 1000 char*/
            all-remark = res-line.bemerk.
            all-remark = REPLACE(all-remark,CHR(10)," ").
            all-remark = REPLACE(all-remark,CHR(13)," ").
    
            cl-list.bemerk01 = STRING(SUBSTRING(all-remark,1,225)).
            cl-list.bemerk02 = STRING(SUBSTRING(all-remark,226,225)).
            cl-list.bemerk03 = STRING(SUBSTRING(all-remark,451,225)).
            cl-list.bemerk04 = STRING(SUBSTRING(all-remark,676,225)).
            /*DO add remark 1000 char*/
        END.
        ELSE
        DO:
            DO i = 1 TO length(res-line.bemerk): 
                cl-list.bemerk = cl-list.bemerk + SUBSTR(TRIM(res-line.bemerk), i, 1).
            END.

            FIND FIRST rbuff WHERE rbuff.resnr = reservation.resnr NO-LOCK NO-ERROR. /*Alder - Ticket A8CCB8*/
            IF AVAILABLE rbuff THEN
            DO:
                cl-list.rsv-comment = rbuff.bemerk.                
            END.

            FIND FIRST gbuff WHERE gbuff.gastnr = res-line.gastnrmember 
                USE-INDEX gastnr_index NO-LOCK NO-ERROR.
            IF AVAILABLE gbuff THEN
            DO:
                cl-list.g-comment = gbuff.bemerk.
            END.

            FIND FIRST queasy WHERE queasy.KEY EQ 267
                AND queasy.number1 EQ res-line.resnr
                AND queasy.number2 EQ res-line.reslinnr NO-LOCK NO-ERROR.
            IF AVAILABLE queasy THEN
            DO:
                cl-list.other-comment = queasy.char1.
            END.
        END.        

        /* FD Comment 14/06/21, This condition get global ratecode, not ratecode per date
        DO i = 1 TO NUM-ENTRIES(res-line.zimmer-wunsch,";") - 1:
                    str = ENTRY(i, res-line.zimmer-wunsch, ";").
                    IF SUBSTR(str,1,6) = "$CODE$" THEN 
                    DO:
                      cl-list.ratecode  = SUBSTR(str,7).
                      LEAVE.
                    END.
        END.
        */
        
        /*DO j = 1 TO length(reservation.bemerk): 
          IF SUBSTR(reservation.bemerk,j,1) = chr(10) THEN 
          cl-list.bemerk1 = cl-list.bemerk1 + " ". 
          ELSE cl-list.bemerk1 = cl-list.bemerk1 + SUBSTR(TRIM(reservation.bemerk), j, 1). 
        DISP cl-list.bemerk1.
        END.*/

        /*DO j = 1 TO NUM-ENTRIES(res-line.zimmer-wunsch,";") - 1:
            str = ENTRY(i, res-line.zimmer-wunsch, ";").
            IF SUBSTR(str,1,6) = "$CODE$" THEN 
            DO:
              cl-list.ratecode  = SUBSTR(str,7).
              LEAVE.
            END.
        END.*/


        cl-list.pax = STRING(cl-list.a,">9") + "/" + STRING(cl-list.c,"9") 
          + " " + STRING(cl-list.co,"9"). 
     
        IF cl-list.nat = "" THEN cl-list.nat = "?". 
        ELSE 
        DO: 
          FIND FIRST nation WHERE nation.kurzbez = cl-list.nat NO-LOCK NO-ERROR. 
          IF AVAILABLE nation THEN cl-list.nation = nation.bezeich. 
        END. 

     
        FIND FIRST zinr-list WHERE zinr-list.zinr = genstat.zinr 
            AND zinr-list.resnr = res-line.resnr 
            AND zinr-list.reslinnr = res-line.reslinnr NO-ERROR.
        IF NOT AVAILABLE zinr-list THEN
        DO: 
          CREATE zinr-list.
          ASSIGN
              zinr-list.resnr = res-line.resnr
              zinr-list.reslinnr = res-line.reslinnr
              zinr-list.zinr  = genstat.zinr.

          FIND FIRST queasy WHERE queasy.key = 14 AND queasy.char1 = genstat.zinr 
            AND queasy.date1 LE curr-date AND queasy.date2 GE curr-date 
            NO-LOCK NO-ERROR. 
          IF zimmer.sleeping /*MT*/ /*ITA 301213*/ AND genstat.resstatus NE 13 THEN 
          DO: 
             IF NOT AVAILABLE queasy THEN
             DO:
               tot-rm = tot-rm + 1.
               tot-rmqty = tot-rmqty + 1.
             END.                  
             ELSE IF AVAILABLE queasy AND queasy.number3 NE genstat.gastnr THEN 
             DO:
               tot-rm = tot-rm + 1.
               tot-rmqty = tot-rmqty + 1.
             END.
                
          END. 
          /*modify by bernatd EA4782 2025*/
          IF zimmer.sleeping AND (genstat.zipreis GT 0 OR genstat.zipreis = 0 ) AND genstat.erwachs GT 0 AND genstat.resstatus NE 13 THEN 
          DO: z = z + 1.
             IF NOT AVAILABLE queasy THEN 
             DO:
                 tot-payrm = tot-payrm + 1.
             END.
             ELSE IF AVAILABLE queasy AND queasy.number3 NE genstat.gastnr THEN 
               tot-payrm = tot-payrm + 1. 
          END. 
          ELSE IF NOT zimmer.sleeping THEN 
          DO: 
            IF AVAILABLE queasy AND queasy.number3 NE genstat.gastnr 
              AND genstat.zipreis GT 0 THEN
            DO:
              tot-rm = tot-rm + 1.
              tot-rmqty = tot-rmqty + 1.
            END.     

            inactive = inactive + 1.
          END. 
        END. 
     
        tot-a = tot-a + genstat.erwachs. 
        tot-c = tot-c + genstat.kind1 + genstat.kind2 + genstat.kind3. 
        tot-co = tot-co + genstat.gratis. 

        IF exc-compli THEN /*bernatd add 9D155B 2025*/
        DO:
          tot-co = 0.
        END.
    END.
    
    IF NOT disp-accompany THEN
    DO:    
        FIND FIRST cl-list WHERE cl-list.rmno EQ res-line.zinr 
            AND cl-list.resnr EQ res-line.resnr 
            AND cl-list.arrive EQ res-line.ankunft 
            AND cl-list.zipreis EQ 0 AND (cl-list.a + cl-list.c) LT 1
            AND cl-list.co LT 1 EXCLUSIVE-LOCK NO-ERROR.
        IF AVAILABLE cl-list THEN
        DO:
            DELETE cl-list.
            RELEASE cl-list.
        END.
    END.

     /*add exclude Complimetn Bernatd 9D155B 2025*/
     IF exc-compli THEN
     DO:    
         FIND FIRST cl-list WHERE cl-list.rmno EQ res-line.zinr 
             AND cl-list.resnr EQ res-line.resnr 
             AND cl-list.arrive EQ res-line.ankunft 
             AND cl-list.co GT 0 EXCLUSIVE-LOCK NO-ERROR.
         IF AVAILABLE cl-list THEN
         DO:
             DELETE cl-list.
             RELEASE cl-list.
             tot-rm = tot-rm - 1.
         END.
     END.
     /*end bernatd*/
  END. 
  /*MT
  FOR EACH cl-list WHERE cl-list.zipreis NE 0 BY cl-list.nation BY cl-list.bezeich:
      FIND FIRST s-list WHERE s-list.bezeich = cl-list.bezeich
          AND s-list.nat EQ cl-list.nat NO-ERROR.
      IF NOT AVAILABLE s-list THEN
      DO:
          CREATE s-list.
          s-list.rmcat = cl-list.rmcat.
          s-list.bezeich = cl-list.bezeich.
          s-list.nat = cl-list.nat.
      END.
      s-list.anz = s-list.anz + cl-list.qty.
      s-list.adult = s-list.adult + cl-list.a + cl-list.co. 
      s-list.child = s-list.child + cl-list.c.
      
  END.
  */
  
  /*FOR EACH zinr-list BY zinr-list.zinr BY zinr-list.resnr :
      z = z + 1.
  END.*/
  FOR EACH cl-list BY cl-list.nation BY cl-list.bezeich: 
    /*ITA 021117*/
    FIND FIRST mealcoup WHERE mealcoup.NAME = "Breakfast" 
        AND mealcoup.resnr = cl-list.resnr
        AND mealcoup.zinr = cl-list.rmno  NO-LOCK NO-ERROR.
    IF AVAILABLE mealcoup THEN DO:
        ASSIGN cl-list.tot-bfast = mealcoup.verbrauch[1] + mealcoup.verbrauch[2] + mealcoup.verbrauch[3] + mealcoup.verbrauch[4] + mealcoup.verbrauch[5]
                                  + mealcoup.verbrauch[6] + mealcoup.verbrauch[7] + mealcoup.verbrauch[8] + mealcoup.verbrauch[9] + mealcoup.verbrauch[10]
                                  + mealcoup.verbrauch[11] + mealcoup.verbrauch[12] + mealcoup.verbrauch[13] + mealcoup.verbrauch[14] + mealcoup.verbrauch[15]
                                  + mealcoup.verbrauch[16] + mealcoup.verbrauch[17] + mealcoup.verbrauch[18] + mealcoup.verbrauch[19] + mealcoup.verbrauch[20]
                                  + mealcoup.verbrauch[21] + mealcoup.verbrauch[22] + mealcoup.verbrauch[23] + mealcoup.verbrauch[24] + mealcoup.verbrauch[25]
                                  + mealcoup.verbrauch[26] + mealcoup.verbrauch[27] + mealcoup.verbrauch[28] + mealcoup.verbrauch[29] + mealcoup.verbrauch[30]
                                  + mealcoup.verbrauch[31] + mealcoup.verbrauch[32].
    END.

    FIND FIRST s-list WHERE s-list.rmcat = cl-list.kurzbez NO-ERROR. 
    IF NOT AVAILABLE s-list THEN 
    DO: 
      FIND FIRST s-list WHERE s-list.rmcat = "" NO-ERROR. 
      IF AVAILABLE s-list THEN 
      DO: 
        s-list.rmcat = cl-list.kurzbez. 
        s-list.bezeich = cl-list.bezeich. 
      END. 
    END. 
    IF NOT AVAILABLE s-list THEN 
    DO: 
      create s-list. 
      s-list.rmcat = cl-list.kurzbez. 
      s-list.bezeich = cl-list.bezeich. 
    END. 
    
    s-list.anz = s-list.anz + cl-list.qty. 
 
    FIND FIRST s-list WHERE s-list.nat = cl-list.nat NO-ERROR. 
    IF NOT AVAILABLE s-list THEN 
    DO: 
      FIND FIRST s-list WHERE s-list.nat = "" NO-ERROR. 
      IF AVAILABLE s-list THEN s-list.nat = cl-list.nat. 
    END. 
    IF NOT AVAILABLE s-list THEN 
    DO: 
      create s-list. 
      IF AVAILABLE s-list THEN s-list.nat = cl-list.nat. 
    END. 
    s-list.adult = s-list.adult + cl-list.a + cl-list.co. 
    s-list.child = s-list.child + cl-list.c. 

    s-list.rmqty = s-list.rmqty + cl-list.qty.
  END. 
  
  
  IF (tot-a + tot-co) NE 0 THEN 
  FOR EACH s-list WHERE s-list.nat NE "": 
    FIND FIRST nation WHERE nation.kurzbez = s-list.nat NO-LOCK NO-ERROR. 
    IF AVAILABLE nation THEN s-list.nat = nation.bezeich. 
    s-list.proz = s-list.adult / (tot-a + tot-co) * 100. 
  END. 
 
END. 

PROCEDURE create-inhouse3: 
DEFINE VARIABLE i           AS INTEGER.
DEFINE VARIABLE j           AS INTEGER.
DEFINE VARIABLE vip-flag    AS CHAR. 
DEFINE VARIABLE str         AS CHAR.
DEFINE VARIABLE nr          AS INTEGER INITIAL 0. 
DEFINE VARIABLE curr-gastnr AS INTEGER INITIAL 0. 
DEFINE VARIABLE actflag1    AS INTEGER. 
DEFINE VARIABLE actflag2    AS INTEGER. 
DEFINE buffer gmember       FOR guest. 
DEFINE BUFFER gbuff         FOR guest.
DEFINE BUFFER rbuff         FOR reservation.

  FOR EACH zinr-list:
      DELETE zinr-list.
  END.

  IF datum = curr-date THEN 
  DO: 
    actflag1 = 1. 
    actflag2 = 1. 
  END. 
  ELSE 
  DO: 
    actflag1 = 1. 
    actflag2 = 2. 
  END. 
 
  tot-payrm = 0. 
  tot-rm = 0. 
  tot-a = 0. 
  tot-c = 0. 
  tot-co = 0. 
  inactive = 0. 
 
  FOR EACH s-list: 
   delete s-list. 
  END. 
 
  FOR EACH cl-list: 
    delete cl-list. 
  END. 
 
  FOR EACH str-list: 
    delete str-list. 
  END. 
 
  tot-avail = 0. 
  FOR EACH zimmer WHERE zimmer.sleeping = YES NO-LOCK: 
    tot-avail = tot-avail + 1. 
  END. 
 
  FOR EACH res-line WHERE res-line.active-flag GE actflag1 
    AND res-line.active-flag LE actflag2 
    AND res-line.resstatus NE 9 AND res-line.resstatus NE 10 
    AND res-line.resstatus NE 12 AND res-line.ankunft LE datum 
    AND res-line.abreise GE datum 
    AND res-line.zinr GE froom AND res-line.zinr LE troom NO-LOCK, 
    FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr NO-LOCK, 
    FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
    FIRST guest WHERE guest.gastnr = reservation.gastnr NO-LOCK, 
    FIRST gmember WHERE gmember.gastnr = res-line.gastnrmember NO-LOCK,
    FIRST zimmer WHERE zimmer.zinr = res-line.zinr AND zimmer.sleeping NO-LOCK

    BY guest.karteityp descending BY guest.name BY guest.gastnr 
    BY res-line.name BY res-line.zinr: 

    IF exc-depart AND res-line.abreise = datum THEN.
    ELSE
    DO:
        FIND FIRST setup-list WHERE setup-list.nr = res-line.setup + 1. 
        /*FIND FIRST zimmer WHERE zimmer.zinr = res-line.zinr NO-LOCK. */ /*Comment FD April 06, 2021*/
     
        IF curr-gastnr NE guest.gastnr THEN 
        DO: 
          nr = 0. 
          curr-gastnr = guest.gastnr. 
        END. 
        IF guest.karteityp GT 0 THEN nr = nr + 1. 
        vip-flag = "". 
        FIND FIRST guestseg WHERE guestseg.gastnr = gmember.gastnr 
          AND (guestseg.segmentcode = vipnr1 OR 
          guestseg.segmentcode = vipnr2 OR 
          guestseg.segmentcode = vipnr3 OR 
          guestseg.segmentcode = vipnr4 OR 
          guestseg.segmentcode = vipnr5 OR 
          guestseg.segmentcode = vipnr6 OR 
          guestseg.segmentcode = vipnr7 OR 
          guestseg.segmentcode = vipnr8 OR 
          guestseg.segmentcode = vipnr9) NO-LOCK NO-ERROR. 
        IF AVAILABLE guestseg THEN 
        DO: 
          FIND FIRST segment WHERE segment.segmentcode = guestseg.segmentcode
              NO-LOCK.
            ASSIGN vip-flag = segment.bezeich. 
        END.
     
        create cl-list. 
        ASSIGN 
          cl-list.nr        = nr 
    /* 
          cl-list.groupname = reservation.groupname 
    */ 
          cl-list.karteityp = guest.karteityp 
          cl-list.rmcat     = zimkateg.kurzbez + setup-list.char 
          cl-list.kurzbez   = zimkateg.kurzbez 
          cl-list.bezeich   = zimkateg.bezeich 
          cl-list.nat       = gmember.nation1 
          cl-list.resnr     = res-line.resnr 
          cl-list.vip       = vip-flag 
          cl-list.name      = res-line.name 
          cl-list.rmno      = res-line.zinr 
          cl-list.zipreis   = res-line.zipreis
          cl-list.arrive    = res-line.ankunft 
          cl-list.depart    = res-line.abreise 
          cl-list.qty       = res-line.zimmeranz 
          cl-list.a         = res-line.erwachs 
          cl-list.c         = res-line.kind1 + res-line.kind2 
          cl-list.co        = res-line.gratis 
          cl-list.argt      = res-line.arrangement 
          cl-list.flight    = SUBSTR(res-line.flight-nr, 12, 6) 
          cl-list.etd       = SUBSTR(res-line.flight-nr, 18, 5) 
          cl-list.ci-time = STRING(res-line.ankzeit, "HH:MM")
    /*    cl-list.paym      = INTEGER(res-line.code).  */ 
          cl-list.paym      = reservation.segmentcode
          cl-list.created   = reservation.resdat
          cl-list.createID  = reservation.useridanlage
          cl-list.etage     = zimmer.etage  
          cl-list.zinr-bez  = zimmer.bezeich
          cl-list.birthdate = gmember.geburtdatum1
          cl-list.telefon   = gmember.telefon /*add by bernatd 70F06C*/
          cl-list.mobil-tel = gmember.mobil-telefon /*add by bernatd 70F06C*/
          .

        IF res-line.resstatus NE 11 AND res-line.resstatus NE 13 THEN ASSIGN cl-list.flag-guest = 1.
        ELSE ASSIGN cl-list.flag-guest = 2.

        /*DODY 01/07/16 penambahan membership number dan type of membership */
        FIND FIRST mc-guest WHERE mc-guest.gastnr = gmember.gastnr NO-LOCK NO-ERROR.
        IF AVAILABLE mc-guest THEN /*FT serverless*/
        DO:
            cl-list.telefon   = gmember.telefon + ";" + mc-guest.cardnum.      /*SIS 31/01/13 */
            FIND FIRST mc-types WHERE mc-types.nr = mc-guest.nr NO-LOCK NO-ERROR.
            IF AVAILABLE mc-types THEN 
             cl-list.mobil-tel = gmember.mobil-telefon + ";" + mc-types.bezeich. /*SIS 31/01/13 */
            ELSE
             cl-list.mobil-tel = gmember.mobil-telefon. 
        END.                                            
        ELSE cl-list.telefon   = gmember.telefon.
        
        /*FD 15 April, 2021*/
        FIND FIRST nation WHERE nation.kurzbez EQ gmember.nation2 NO-LOCK NO-ERROR.
        IF AVAILABLE nation THEN cl-list.local-reg = nation.bezeich.

        /*/* new Jun 30 09 by LN*/
        FIND FIRST waehrung WHERE waehrung.waehrungsnr = res-line.betriebsnr 
            NO-LOCK NO-ERROR.
        IF AVAILABLE waehrung THEN
            cl-list.curr = waehrung.wabkurz.*/

       /*dody 23/09/16 penambahan email*/
        FIND FIRST waehrung WHERE waehrung.waehrungsnr = res-line.betriebsnr 
            NO-LOCK NO-ERROR.
        IF AVAILABLE waehrung THEN
            cl-list.curr = waehrung.wabkurz + ";" + gmember.email-adr.
       /*end dody*/ 

        /*ITA 130717 --> Add Request Patra*/
        FIND FIRST reslin-queasy WHERE reslin-queasy.KEY = "specialRequest"
             AND reslin-queasy.resnr = res-line.resnr 
             AND reslin-queasy.reslinnr = res-line.reslinnr NO-LOCK NO-ERROR.
        IF AVAILABLE reslin-queasy THEN
             ASSIGN cl-list.spreq = reslin-queasy.char3 + "," + cl-list.spreq.
        /*end*/

        /*FD Juny 14, 2021 => Get ratecode per date*/
        FIND FIRST reslin-queasy WHERE reslin-queasy.key EQ "arrangement" 
          AND reslin-queasy.resnr EQ res-line.resnr 
          AND reslin-queasy.reslinnr EQ res-line.reslinnr 
          AND datum GE reslin-queasy.date1 
          AND datum LE reslin-queasy.date2 NO-LOCK NO-ERROR. 
        IF AVAILABLE reslin-queasy THEN 
        DO:
          IF reslin-queasy.char2 NE "" THEN cl-list.ratecode = reslin-queasy.char2.
          ELSE
          DO:
            DO i = 1 TO NUM-ENTRIES(res-line.zimmer-wunsch,";") - 1:
              str = ENTRY(i, res-line.zimmer-wunsch, ";").
              IF SUBSTR(str,1,6) EQ "$CODE$" THEN 
              DO:
                cl-list.ratecode = SUBSTR(str,7).
                LEAVE.
              END.
            END.
          END.
        END.
        /*End FD*/

        /*ITA 021117*/
        FIND FIRST mealcoup WHERE mealcoup.NAME = "Breakfast" 
            AND mealcoup.resnr = res-line.resnr
            AND mealcoup.zinr = res-line.zinr  NO-LOCK NO-ERROR.
        IF AVAILABLE mealcoup THEN DO:
            ASSIGN cl-list.tot-bfast = mealcoup.verbrauch[1] + mealcoup.verbrauch[2] + mealcoup.verbrauch[3] + mealcoup.verbrauch[4] + mealcoup.verbrauch[5]
                                      + mealcoup.verbrauch[6] + mealcoup.verbrauch[7] + mealcoup.verbrauch[8] + mealcoup.verbrauch[9] + mealcoup.verbrauch[10]
                                      + mealcoup.verbrauch[11] + mealcoup.verbrauch[12] + mealcoup.verbrauch[13] + mealcoup.verbrauch[14] + mealcoup.verbrauch[15]
                                      + mealcoup.verbrauch[16] + mealcoup.verbrauch[17] + mealcoup.verbrauch[18] + mealcoup.verbrauch[19] + mealcoup.verbrauch[20]
                                      + mealcoup.verbrauch[21] + mealcoup.verbrauch[22] + mealcoup.verbrauch[23] + mealcoup.verbrauch[24] + mealcoup.verbrauch[25]
                                      + mealcoup.verbrauch[26] + mealcoup.verbrauch[27] + mealcoup.verbrauch[28] + mealcoup.verbrauch[29] + mealcoup.verbrauch[30]
                                      + mealcoup.verbrauch[31] + mealcoup.verbrauch[32].
        END.

        FIND FIRST segment WHERE segment.segmentcode = reservation.segmentcode
            NO-LOCK NO-ERROR.
        IF AVAILABLE segment THEN cl-list.segm = ENTRY(1, segment.bezeich, "$$0").
        
        IF guest.karteityp NE 0 THEN
          cl-list.company   = guest.name + ", " + guest.vorname1 
            + " " + guest.anrede1 + guest.anredefirma .
        ELSE
          cl-list.company   = guest.name + ", " + guest.vorname1 
            + " " + guest.anrede1 + guest.anredefirma .

        IF cl-list.nat = "" THEN cl-list.nat = "?". 
        IF res-line.resstatus = 13 OR res-line.zimmerfix = YES THEN cl-list.qty = 0. 
     
        IF split-rsv-print THEN
        DO:
            /*M 22 Jan 2011 - addition guest's comment */
            IF incl-gcomment THEN
            DO:
                FIND FIRST gbuff WHERE gbuff.gastnr = res-line.gastnrmember 
                    USE-INDEX gastnr_index NO-LOCK NO-ERROR.
                IF AVAILABLE gbuff THEN
                DO:
                    DO i = 1 TO LENGTH(gbuff.bemerk): 
                        IF SUBSTR(gbuff.bemerk,i,1) = CHR(10) THEN 
                            cl-list.bemerk = cl-list.bemerk + " ". 
                        ELSE cl-list.bemerk = cl-list.bemerk + SUBSTR(TRIM(gbuff.bemerk), i, 1). 
                    END.
                END.
                
                cl-list.bemerk = cl-list.bemerk + " || ".
            END.
    
            /*IT 200612 add reservation comment*/
            IF incl-rsvcomment THEN
            DO:
                FIND FIRST rbuff WHERE rbuff.resnr = reservation.resnr NO-LOCK NO-ERROR. /*Alder - Ticket A8CCB8*/
                IF AVAILABLE rbuff THEN
                DO:
                    DO j = 1 TO LENGTH(rbuff.bemerk):
                        IF SUBSTR(rbuff.bemerk,j,1) = CHR(10) THEN 
                            cl-list.bemerk1 = cl-list.bemerk1 + " ". 
                        ELSE cl-list.bemerk1 = cl-list.bemerk1 + SUBSTR(TRIM(rbuff.bemerk), j, 1). 
                    END.
                    
                END.
                /*cl-list.bemerk1 = " || " + cl-list.bemerk1.*/
                cl-list.bemerk = cl-list.bemerk  + cl-list.bemerk1 + " || ".
            END.
    
            DO i = 1 TO length(res-line.bemerk): 
                IF SUBSTR(res-line.bemerk,i,1) = chr(10) THEN 
                cl-list.bemerk = cl-list.bemerk + " ". 
                ELSE cl-list.bemerk = cl-list.bemerk + SUBSTR(TRIM(res-line.bemerk), i, 1). 
            END.

            /*DO add remark 1000 char*/    
            all-remark = res-line.bemerk.
            all-remark = REPLACE(all-remark,CHR(10)," ").
            all-remark = REPLACE(all-remark,CHR(13)," ").
            
            cl-list.bemerk01 = STRING(SUBSTRING(all-remark,1,225)).
            cl-list.bemerk02 = STRING(SUBSTRING(all-remark,226,225)).
            cl-list.bemerk03 = STRING(SUBSTRING(all-remark,451,225)).
            cl-list.bemerk04 = STRING(SUBSTRING(all-remark,676,225)).
            /*DO add remark 1000 char*/
        END.
        ELSE
        DO:
            DO i = 1 TO length(res-line.bemerk): 
                cl-list.bemerk = cl-list.bemerk + SUBSTR(TRIM(res-line.bemerk), i, 1).
            END.

            FIND FIRST rbuff WHERE rbuff.resnr = reservation.resnr NO-LOCK NO-ERROR. /*Alder - Ticket A8CCB8*/
            IF AVAILABLE rbuff THEN
            DO:
                cl-list.rsv-comment = rbuff.bemerk.                
            END.

            FIND FIRST gbuff WHERE gbuff.gastnr = res-line.gastnrmember 
                USE-INDEX gastnr_index NO-LOCK NO-ERROR.
            IF AVAILABLE gbuff THEN
            DO:
                cl-list.g-comment = gbuff.bemerk.
            END.

            FIND FIRST queasy WHERE queasy.KEY EQ 267
                AND queasy.number1 EQ res-line.resnr
                AND queasy.number2 EQ res-line.reslinnr NO-LOCK NO-ERROR.
            IF AVAILABLE queasy THEN
            DO:
                cl-list.other-comment = queasy.char1.
            END.
        END.        

        /* FD Comment 14/06/21, This condition get global ratecode, not ratecode per date
        DO i = 1 TO NUM-ENTRIES(res-line.zimmer-wunsch,";") - 1:
            str = ENTRY(i, res-line.zimmer-wunsch, ";").
            IF SUBSTR(str,1,6) = "$CODE$" THEN 
            DO:
              cl-list.ratecode  = SUBSTR(str,7).
              LEAVE.
            END.
        END.
        */

         /*DO j = 1 TO length(reservation.bemerk): 
          IF SUBSTR(reservation.bemerk,j,1) = chr(10) THEN 
          cl-list.bemerk1 = cl-list.bemerk1 + " ". 
          ELSE cl-list.bemerk1 = cl-list.bemerk1 + SUBSTR(TRIM(reservation.bemerk), j, 1). 
        DISP cl-list.bemerk1.
        END.*/

        /*DO j = 1 TO NUM-ENTRIES(res-line.zimmer-wunsch,";") - 1:
                str = ENTRY(i, res-line.zimmer-wunsch, ";").
                IF SUBSTR(str,1,6) = "$CODE$" THEN 
                DO:
                  cl-list.ratecode  = SUBSTR(str,7).
                  LEAVE.
                END.
            END.*/
        
        cl-list.pax = STRING(cl-list.a,">9") + "/" + STRING(cl-list.c,"9") 
          + " " + STRING(cl-list.co,"9"). 
     
        IF cl-list.nat = "" THEN cl-list.nat = "?". 
        ELSE 
        DO: 
          FIND FIRST nation WHERE nation.kurzbez = cl-list.nat NO-LOCK NO-ERROR. 
          IF AVAILABLE nation THEN cl-list.nation = nation.bezeich. 
        END. 

        FIND FIRST zinr-list WHERE zinr-list.zinr = res-line.zinr 
            AND zinr-list.resnr = res-line.resnr 
            AND zinr-list.reslinnr = res-line.reslinnr NO-ERROR.
        IF NOT AVAILABLE zinr-list THEN
        DO: 
          CREATE zinr-list.
          ASSIGN 
              zinr-list.resnr = res-line.resnr
              zinr-list.reslinnr = res-line.reslinnr
              zinr-list.zinr  = res-line.zinr.

          FIND FIRST queasy WHERE queasy.key = 14 AND queasy.char1 = res-line.zinr 
            AND queasy.date1 LE curr-date AND queasy.date2 GE curr-date 
            NO-LOCK NO-ERROR. 
          IF zimmer.sleeping /*MT*/ /*ITA 301213*/ AND res-line.resstatus NE 13 THEN 
          DO: 
             IF NOT AVAILABLE queasy THEN 
             DO:
               tot-rm = tot-rm + res-line.zimmeranz.
               tot-rmqty = tot-rmqty + res-line.zimmeranz.
             END.                  
             ELSE IF AVAILABLE queasy AND queasy.number3 NE res-line.gastnr THEN
             DO:
               tot-rm = tot-rm + res-line.zimmeranz.
               tot-rmqty = tot-rmqty + res-line.zimmeranz.
             END.                
          END. 
          /*modify by bernatd EA4782 2025*/
          IF zimmer.sleeping AND (res-line.zipreis GT 0 OR res-line.zipreis = 0) AND res-line.resstatus NE 13 AND res-line.erwachs GT 0 THEN 
          DO: 
             IF NOT AVAILABLE queasy THEN tot-payrm = tot-payrm + res-line.zimmeranz. 
             ELSE IF AVAILABLE queasy AND queasy.number3 NE res-line.gastnr THEN 
               tot-payrm = tot-payrm + res-line.zimmeranz. 
          END. 
          ELSE IF NOT zimmer.sleeping THEN 
          DO: 
            IF AVAILABLE queasy AND queasy.number3 NE res-line.gastnr 
              AND res-line.zipreis GT 0 THEN
            DO:
              tot-rm = tot-rm + res-line.zimmeranz.
              tot-rmqty = tot-rmqty + res-line.zimmeranz.
            END.
                 
            inactive = inactive + 1.
          END. 
        END. 
     
        tot-a = tot-a + res-line.erwachs. 
        tot-c = tot-c + res-line.kind1 + res-line.kind2. 
        tot-co = tot-co + res-line.gratis. 

        IF exc-compli THEN /*bernatd add 9D155B 2025*/
        DO:
          tot-co = 0.
        END.
    END.
    
    IF NOT disp-accompany THEN
    DO:    
        FIND FIRST cl-list WHERE cl-list.rmno EQ res-line.zinr 
            AND cl-list.resnr EQ res-line.resnr 
            AND cl-list.arrive EQ res-line.ankunft 
            AND cl-list.zipreis EQ 0 AND (cl-list.a + cl-list.c) LT 1
            AND cl-list.co LT 1 EXCLUSIVE-LOCK NO-ERROR.
        IF AVAILABLE cl-list THEN
        DO:
            DELETE cl-list.
            RELEASE cl-list.
        END.
    END.

     /*add exclude Complimetn Bernatd 9D155B 2025*/
     IF exc-compli THEN
     DO:    
         FIND FIRST cl-list WHERE cl-list.rmno EQ res-line.zinr 
             AND cl-list.resnr EQ res-line.resnr 
             AND cl-list.arrive EQ res-line.ankunft 
             AND cl-list.co GT 0 EXCLUSIVE-LOCK NO-ERROR.
         IF AVAILABLE cl-list THEN
         DO:
             DELETE cl-list.
             RELEASE cl-list.
             tot-rm = tot-rm - 1.
         END.
     END.
     /*end bernatd*/
  END. 
  /*MT
  FOR EACH cl-list WHERE cl-list.zipreis NE 0 BY cl-list.nation BY cl-list.bezeich:
      FIND FIRST s-list WHERE s-list.bezeich = cl-list.bezeich
          AND s-list.nat EQ cl-list.nat NO-ERROR.
      IF NOT AVAILABLE s-list THEN
      DO:
          CREATE s-list.
          s-list.rmcat = cl-list.rmcat.
          s-list.bezeich = cl-list.bezeich.
          s-list.nat = cl-list.nat.
      END.
      s-list.anz = s-list.anz + cl-list.qty.
      s-list.adult = s-list.adult + cl-list.a + cl-list.co. 
      s-list.child = s-list.child + cl-list.c.
      
  END.
  */
  FOR EACH cl-list BY cl-list.nation BY cl-list.bezeich: 
    FIND FIRST s-list WHERE s-list.rmcat = cl-list.kurzbez NO-ERROR. 
    IF NOT AVAILABLE s-list THEN 
    DO: 
      FIND FIRST s-list WHERE s-list.rmcat = "" NO-ERROR. 
      IF AVAILABLE s-list THEN 
      DO: 
        s-list.rmcat = cl-list.kurzbez. 
        s-list.bezeich = cl-list.bezeich. 
      END. 
    END. 
    IF NOT AVAILABLE s-list THEN 
    DO: 
      create s-list. 
      s-list.rmcat = cl-list.kurzbez. 
      s-list.bezeich = cl-list.bezeich. 
    END. 
    s-list.anz = s-list.anz + cl-list.qty. 
 
    FIND FIRST s-list WHERE s-list.nat = cl-list.nat NO-ERROR. 
    IF NOT AVAILABLE s-list THEN 
    DO: 
      FIND FIRST s-list WHERE s-list.nat = "" NO-ERROR. 
      IF AVAILABLE s-list THEN s-list.nat = cl-list.nat. 
    END. 
    IF NOT AVAILABLE s-list THEN 
    DO: 
      create s-list. 
      IF AVAILABLE s-list THEN s-list.nat = cl-list.nat. 
    END. 
    s-list.adult = s-list.adult + cl-list.a + cl-list.co. 
    s-list.child = s-list.child + cl-list.c. 

    s-list.rmqty = s-list.rmqty + cl-list.qty.
  END. 
  
  IF (tot-a + tot-co) NE 0 THEN 
  FOR EACH s-list WHERE s-list.nat NE "": 
    FIND FIRST nation WHERE nation.kurzbez = s-list.nat NO-LOCK NO-ERROR. 
    IF AVAILABLE nation THEN s-list.nat = nation.bezeich. 
    s-list.proz = s-list.adult / (tot-a + tot-co) * 100. 
  END. 
 
END. 

PROCEDURE create-genstat-inhouse3: 
DEFINE VARIABLE i           AS INTEGER.
DEFINE VARIABLE j           AS INTEGER.
DEFINE VARIABLE vip-flag    AS CHAR. 
DEFINE VARIABLE nr          AS INTEGER INITIAL 0. 
DEFINE VARIABLE str AS CHAR.
DEFINE VARIABLE actflag1    AS INTEGER. 
DEFINE VARIABLE actflag2    AS INTEGER. 
DEFINE VARIABLE do-it       AS LOGICAL.
DEFINE BUFFER gmember       FOR guest. 
DEFINE BUFFER gbuff         FOR guest.
DEFINE BUFFER rbuff         FOR reservation.
 
  FOR EACH zinr-list:
      DELETE zinr-list.
  END.

  IF datum = curr-date THEN 
  DO: 
    actflag1 = 1. 
    actflag2 = 1. 
  END. 
  ELSE 
  DO: 
    actflag1 = 1. 
    actflag2 = 2. 
  END. 
 
  tot-payrm = 0. 
  tot-rm = 0. 
  tot-a = 0. 
  tot-c = 0. 
  tot-co = 0. 
  inactive = 0. 
 
  FOR EACH s-list: 
   delete s-list. 
  END. 
 
  FOR EACH cl-list: 
    delete cl-list. 
  END. 
 
  FOR EACH str-list: 
    delete str-list. 
  END. 
 
  tot-avail = 0. 
  FOR EACH zkstat WHERE zkstat.datum = datum NO-LOCK:
      tot-avail = tot-avail + zkstat.anz100.
  END.
/*
  FOR EACH zimmer WHERE zimmer.sleeping = YES NO-LOCK: 
    tot-avail = tot-avail + 1. 
  END. 
*/
  FOR EACH genstat WHERE genstat.datum = datum
    AND genstat.zinr GE froom AND genstat.zinr LE troom NO-LOCK,
    FIRST zimkateg WHERE zimkateg.zikatnr = genstat.zikatnr NO-LOCK, 
    FIRST reservation WHERE reservation.resnr = genstat.resnr NO-LOCK, 
    FIRST guest WHERE guest.gastnr = genstat.gastnr NO-LOCK, 
    FIRST gmember WHERE gmember.gastnr = genstat.gastnrmember NO-LOCK,
    FIRST zimmer WHERE zimmer.zinr = genstat.zinr AND zimmer.sleeping NO-LOCK
    BY guest.karteityp descending BY guest.name BY guest.gastnr 
    BY gmember.name BY genstat.zinr
    /*BY genstat.zinr BY genstat.erwachs DESCENDING BY gmember.name*/
    :
    IF genstat.res-date[1] LT datum AND genstat.res-date[2] = datum
          AND genstat.resstatus = 8 THEN . /*FD Juni 22, 2020*/
    ELSE IF exc-depart AND genstat.res-date[1] LE datum AND genstat.res-date[2] = datum
        AND genstat.resstatus = 8 THEN . /*M exclude day use  181010*/
    ELSE
    DO:
        FIND FIRST res-line WHERE res-line.resnr = genstat.resnr
           AND res-line.reslinnr = genstat.res-int[1] NO-LOCK .
          FIND FIRST setup-list WHERE setup-list.nr = res-line.setup + 1. 

        /*FIND FIRST zimmer WHERE zimmer.zinr = genstat.zinr NO-LOCK .*/ /*Comment FD April 06, 2021*/
        
        /*change*/
        IF curr-gastnr NE guest.gastnr THEN 
        DO: 
          nr = 0. 
          curr-gastnr = guest.gastnr. 
        END. 
        IF guest.karteityp GT 0 THEN nr = nr + 1. 

        /*nr = nr + 1. */
        vip-flag = "". 
        FIND FIRST guestseg WHERE guestseg.gastnr = gmember.gastnr 
          AND (guestseg.segmentcode = vipnr1 OR 
          guestseg.segmentcode = vipnr2 OR 
          guestseg.segmentcode = vipnr3 OR 
          guestseg.segmentcode = vipnr4 OR 
          guestseg.segmentcode = vipnr5 OR 
          guestseg.segmentcode = vipnr6 OR 
          guestseg.segmentcode = vipnr7 OR 
          guestseg.segmentcode = vipnr8 OR 
          guestseg.segmentcode = vipnr9) NO-LOCK NO-ERROR. 
        IF AVAILABLE guestseg THEN 
        DO: 
          FIND FIRST segment WHERE segment.segmentcode = guestseg.segmentcode
              NO-LOCK.
            ASSIGN vip-flag = segment.bezeich. 
        END.
     
        create cl-list. 
        ASSIGN 
          cl-list.nr        = nr 
    /* 
          cl-list.groupname = reservation.groupname 
    */ 
          cl-list.karteityp = guest.karteityp
          cl-list.rmcat     = zimkateg.kurzbez + setup-list.char 
          cl-list.kurzbez   = zimkateg.kurzbez 
          cl-list.bezeich   = zimkateg.bezeich 
          cl-list.nat       = gmember.nation1 
          cl-list.resnr     = genstat.resnr 
          cl-list.vip       = vip-flag 
          cl-list.name      = gmember.name  + ", " + gmember.vorname1 
                            + " " + gmember.anrede1
          cl-list.rmno      = genstat.zinr 
          cl-list.zipreis   = genstat.zipreis
          cl-list.arrive    = genstat.res-date[1] 
          cl-list.depart    = genstat.res-date[2] 
          cl-list.qty       = 1 
          cl-list.a         = genstat.erwachs
          cl-list.c         = genstat.kind1 + genstat.kind2 + genstat.kind3
          cl-list.co        = genstat.gratis 
          cl-list.argt      = genstat.argt 
          cl-list.flight    = SUBSTR(res-line.flight-nr, 12, 6) 
          cl-list.etd       = SUBSTR(res-line.flight-nr, 18, 5)
          cl-list.ci-time   = STRING(res-line.ankzeit, "HH:MM")
          cl-list.paym      = genstat.segmentcode
          cl-list.created   = reservation.resdat
          cl-list.createID  = reservation.useridanlage
          cl-list.etage     = zimmer.etage  
          cl-list.zinr-bez  = zimmer.bezeich
          cl-list.birthdate = gmember.geburtdatum1
          cl-list.telefon   = gmember.telefon /*add by bernatd 70F06C*/
          cl-list.mobil-tel = gmember.mobil-telefon /*add by bernatd 70F06C*/
          .

        IF res-line.resstatus NE 11 AND res-line.resstatus NE 13 THEN ASSIGN cl-list.flag-guest = 1.
        ELSE ASSIGN cl-list.flag-guest = 2.

        /*DODY 01/07/16 penambahan membership number dan type of membership */
        FIND FIRST mc-guest WHERE mc-guest.gastnr = gmember.gastnr NO-LOCK NO-ERROR.
        IF AVAILABLE mc-guest THEN /*FT serverless*/
        DO:
            cl-list.telefon   = gmember.telefon + ";" + mc-guest.cardnum.      /*SIS 31/01/13 */
            FIND FIRST mc-types WHERE mc-types.nr = mc-guest.nr NO-LOCK NO-ERROR.
            IF AVAILABLE mc-types THEN 
             cl-list.mobil-tel = gmember.mobil-telefon + ";" + mc-types.bezeich. /*SIS 31/01/13 */
            ELSE
             cl-list.mobil-tel = gmember.mobil-telefon. 
        END.                                            
        ELSE cl-list.telefon   = gmember.telefon.

        /*FD 15 April, 2021*/
        FIND FIRST nation WHERE nation.kurzbez EQ gmember.nation2 NO-LOCK NO-ERROR.
        IF AVAILABLE nation THEN cl-list.local-reg = nation.bezeich.

       /*/* new Jun 30 09 by LN*/
        FIND FIRST waehrung WHERE waehrung.waehrungsnr = res-line.betriebsnr 
            NO-LOCK NO-ERROR.
        IF AVAILABLE waehrung THEN
            cl-list.curr = waehrung.wabkurz.*/

       /*dody 23/09/16 penambahan email*/
        FIND FIRST waehrung WHERE waehrung.waehrungsnr = res-line.betriebsnr 
            NO-LOCK NO-ERROR.
        IF AVAILABLE waehrung THEN
            cl-list.curr = waehrung.wabkurz + ";" + gmember.email-adr.
       /*end dody*/ 

        /*ITA 130717 --> Add Request Patra*/
        FIND FIRST reslin-queasy WHERE reslin-queasy.KEY = "specialRequest"
             AND reslin-queasy.resnr = res-line.resnr 
             AND reslin-queasy.reslinnr = res-line.reslinnr NO-LOCK NO-ERROR.
        IF AVAILABLE reslin-queasy THEN
             ASSIGN cl-list.spreq = reslin-queasy.char3 + "," + cl-list.spreq.
        /*end*/

        /*FD Juny 14, 2021 => Get ratecode per date*/
        FIND FIRST reslin-queasy WHERE reslin-queasy.key EQ "arrangement" 
          AND reslin-queasy.resnr EQ res-line.resnr 
          AND reslin-queasy.reslinnr EQ res-line.reslinnr 
          AND datum GE reslin-queasy.date1 
          AND datum LE reslin-queasy.date2 NO-LOCK NO-ERROR. 
        IF AVAILABLE reslin-queasy THEN 
        DO:
          IF reslin-queasy.char2 NE "" THEN cl-list.ratecode = reslin-queasy.char2.
          ELSE
          DO:
            DO i = 1 TO NUM-ENTRIES(res-line.zimmer-wunsch,";") - 1:
              str = ENTRY(i, res-line.zimmer-wunsch, ";").
              IF SUBSTR(str,1,6) EQ "$CODE$" THEN 
              DO:
                cl-list.ratecode = SUBSTR(str,7).
                LEAVE.
              END.
            END.
          END.
        END.
        /*End FD*/

        FIND FIRST segment WHERE segment.segmentcode = genstat.segmentcode
            NO-LOCK NO-ERROR.
        IF AVAILABLE segment THEN cl-list.segm = ENTRY(1, segment.bezeich, "$$0").

        IF guest.karteityp NE 0 THEN
          cl-list.company   = guest.name + ", " + guest.vorname1 
            + " " + guest.anrede1 + guest.anredefirma .
        ELSE
          cl-list.company   = guest.name + ", " + guest.vorname1 
            + " " + guest.anrede1 + guest.anredefirma .

        IF cl-list.nat = "" THEN cl-list.nat = "?". 
        IF genstat.resstatus = 13 THEN cl-list.qty = 0. 
     
        IF NOT split-rsv-print THEN
        DO:
            /*M 22 Jan 2011 - addition guest's comment */
            IF incl-gcomment THEN
            DO:
                FIND FIRST gbuff WHERE gbuff.gastnr = res-line.gastnrmember 
                    USE-INDEX gastnr_index NO-LOCK NO-ERROR.
                IF AVAILABLE gbuff THEN
                DO:
                    DO i = 1 TO LENGTH(gbuff.bemerk): 
                        IF SUBSTR(gbuff.bemerk,i,1) = CHR(10) THEN 
                            cl-list.bemerk = cl-list.bemerk + " ". 
                        ELSE cl-list.bemerk = cl-list.bemerk + SUBSTR(TRIM(gbuff.bemerk), i, 1). 
                    END. 
                END.
                
                cl-list.bemerk = cl-list.bemerk + " || ".
            END.
           
            /*IT 200612 add reservation comment*/
            IF incl-rsvcomment THEN
            DO:
                FIND FIRST rbuff WHERE rbuff.resnr = reservation.resnr NO-LOCK NO-ERROR. /*Alder - Ticket A8CCB8*/
                IF AVAILABLE rbuff THEN
                DO:
                    DO j = 1 TO LENGTH(rbuff.bemerk):
                        IF SUBSTR(rbuff.bemerk,j,1) = CHR(10) THEN 
                            cl-list.bemerk1 = cl-list.bemerk1 + " ". 
                        ELSE cl-list.bemerk1 = cl-list.bemerk1 + SUBSTR(TRIM(rbuff.bemerk), j, 1). 
                    END.
                    
                END.
                /*cl-list.bemerk1 = " || " + cl-list.bemerk1.*/
                cl-list.bemerk = cl-list.bemerk  + cl-list.bemerk1 + " || ".
            END.
            
            DO i = 1 TO length(res-line.bemerk): 
                IF SUBSTR(res-line.bemerk,i,1) = chr(10) THEN 
                cl-list.bemerk = cl-list.bemerk + " ". 
                ELSE cl-list.bemerk = cl-list.bemerk + SUBSTR(TRIM(res-line.bemerk), i, 1). 
            END.

            /*DO add remark 1000 char*/
            all-remark = res-line.bemerk.
            all-remark = REPLACE(all-remark,CHR(10)," ").
            all-remark = REPLACE(all-remark,CHR(13)," ").
    
            cl-list.bemerk01 = STRING(SUBSTRING(all-remark,1,225)).
            cl-list.bemerk02 = STRING(SUBSTRING(all-remark,226,225)).
            cl-list.bemerk03 = STRING(SUBSTRING(all-remark,451,225)).
            cl-list.bemerk04 = STRING(SUBSTRING(all-remark,676,225)).
            /*naufal add remarks 2000 char*/
            /*cl-list.bemerk01 = STRING(SUBSTRING(all-remark,1,255)).
            cl-list.bemerk02 = STRING(SUBSTRING(all-remark,256,255)).
            cl-list.bemerk03 = STRING(SUBSTRING(all-remark,511,255)).
            cl-list.bemerk04 = STRING(SUBSTRING(all-remark,766,255)).
            cl-list.bemerk05 = STRING(SUBSTRING(all-remark,1021,255)).
            cl-list.bemerk06 = STRING(SUBSTRING(all-remark,1276,255)).
            cl-list.bemerk07 = STRING(SUBSTRING(all-remark,1531,255)).
            cl-list.bemerk08 = STRING(SUBSTRING(all-remark,1786,255)).*/
            /*end naufal add remarks 2000 char*/
            /*DO add remark 1000 char*/
        END.
        ELSE
        DO:
            DO i = 1 TO length(res-line.bemerk): 
                cl-list.bemerk = cl-list.bemerk + SUBSTR(TRIM(res-line.bemerk), i, 1).
            END.

            FIND FIRST rbuff WHERE rbuff.resnr = reservation.resnr NO-LOCK NO-ERROR. /*Alder - Ticket A8CCB8*/
            IF AVAILABLE rbuff THEN
            DO:
                cl-list.rsv-comment = rbuff.bemerk.                
            END.

            FIND FIRST gbuff WHERE gbuff.gastnr = res-line.gastnrmember 
                USE-INDEX gastnr_index NO-LOCK NO-ERROR.
            IF AVAILABLE gbuff THEN
            DO:
                cl-list.g-comment = gbuff.bemerk.
            END.

            FIND FIRST queasy WHERE queasy.KEY EQ 267
                AND queasy.number1 EQ res-line.resnr
                AND queasy.number2 EQ res-line.reslinnr NO-LOCK NO-ERROR.
            IF AVAILABLE queasy THEN
            DO:
                cl-list.other-comment = queasy.char1.
            END.
        END.                   
        
        /* FD Comment 14/06/21, This condition get global ratecode, not ratecode per date
        DO i = 1 TO NUM-ENTRIES(res-line.zimmer-wunsch,";") - 1:
            str = ENTRY(i, res-line.zimmer-wunsch, ";").
            IF SUBSTR(str,1,6) = "$CODE$" THEN 
            DO:
              cl-list.ratecode  = SUBSTR(str,7).
              LEAVE.
            END.
        END.
        */

        /*DO j = 1 TO length(reservation.bemerk): 
          IF SUBSTR(reservation.bemerk,j,1) = chr(10) THEN 
          cl-list.bemerk1 = cl-list.bemerk1 + " ". 
          ELSE cl-list.bemerk1 = cl-list.bemerk1 + SUBSTR(TRIM(reservation.bemerk), j, 1). 
        DISP cl-list.bemerk1.
        END.*/

        /*DO j = 1 TO NUM-ENTRIES(res-line.zimmer-wunsch,";") - 1:
            str = ENTRY(i, res-line.zimmer-wunsch, ";").
            IF SUBSTR(str,1,6) = "$CODE$" THEN 
            DO:
              cl-list.ratecode  = SUBSTR(str,7).
              LEAVE.
            END.
        END.*/

        cl-list.pax = STRING(cl-list.a,">9") + "/" + STRING(cl-list.c,"9") 
          + " " + STRING(cl-list.co,"9"). 
     
        IF cl-list.nat = "" THEN cl-list.nat = "?". 
        ELSE 
        DO: 
          FIND FIRST nation WHERE nation.kurzbez = cl-list.nat NO-LOCK NO-ERROR. 
          IF AVAILABLE nation THEN cl-list.nation = nation.bezeich. 
        END. 

            
        FIND FIRST zinr-list WHERE zinr-list.zinr = genstat.zinr 
            AND zinr-list.resnr = res-line.resnr 
            AND zinr-list.reslinnr = res-line.reslinnr NO-ERROR.
        IF NOT AVAILABLE zinr-list THEN
        DO: 
          CREATE zinr-list.
          ASSIGN
              zinr-list.resnr = res-line.resnr
              zinr-list.reslinnr = res-line.reslinnr
              zinr-list.zinr  = genstat.zinr.

          FIND FIRST queasy WHERE queasy.key = 14 AND queasy.char1 = genstat.zinr 
            AND queasy.date1 LE curr-date AND queasy.date2 GE curr-date 
            NO-LOCK NO-ERROR. 
          IF zimmer.sleeping /*MT*/ /*ITA 301213*/ AND genstat.resstatus NE 13 THEN 
          DO: 
             IF NOT AVAILABLE queasy THEN
             DO:
               tot-rm = tot-rm + 1.
               tot-rmqty = tot-rmqty + 1.
             END.                  
             ELSE IF AVAILABLE queasy AND queasy.number3 NE genstat.gastnr THEN 
             DO:
               tot-rm = tot-rm + 1.
               tot-rmqty = tot-rmqty + 1.
             END.                  
          END. 
          /*modify by bernatd EA4782 2025*/
          IF zimmer.sleeping AND (genstat.zipreis GT 0 OR genstat.zipreis = 0 ) AND genstat.erwachs GT 0 AND genstat.resstatus NE 13 THEN 
          DO: 
             IF NOT AVAILABLE queasy THEN tot-payrm = tot-payrm + 1. 
             ELSE IF AVAILABLE queasy AND queasy.number3 NE genstat.gastnr THEN 
               tot-payrm = tot-payrm + 1. 
          END. 
          ELSE IF NOT zimmer.sleeping THEN 
          DO: 
            IF AVAILABLE queasy AND queasy.number3 NE genstat.gastnr 
              AND genstat.zipreis GT 0 THEN 
            DO:
              tot-rm = tot-rm + 1.
              tot-rmqty = tot-rmqty + 1.
            END.               
             
            inactive = inactive + 1.
          END. 
        END. 
     
        tot-a = tot-a + genstat.erwachs. 
        tot-c = tot-c + genstat.kind1 + genstat.kind2 + genstat.kind3. 
        tot-co = tot-co + genstat.gratis. 

        IF exc-compli THEN /*bernatd add 9D155B 2025*/
        DO:
          tot-co = 0.
        END.
    END.
    
    IF NOT disp-accompany THEN
    DO:    
        FIND FIRST cl-list WHERE cl-list.rmno EQ res-line.zinr 
            AND cl-list.resnr EQ res-line.resnr 
            AND cl-list.arrive EQ res-line.ankunft 
            AND cl-list.zipreis EQ 0 AND (cl-list.a + cl-list.c) LT 1
            AND cl-list.co LT 1 EXCLUSIVE-LOCK NO-ERROR.
        IF AVAILABLE cl-list THEN
        DO:
            DELETE cl-list.
            RELEASE cl-list.
        END.
    END.

     /*add exclude Complimetn Bernatd 9D155B 2025*/
     IF exc-compli THEN
     DO:    
         FIND FIRST cl-list WHERE cl-list.rmno EQ res-line.zinr 
             AND cl-list.resnr EQ res-line.resnr 
             AND cl-list.arrive EQ res-line.ankunft 
             AND cl-list.co GT 0 EXCLUSIVE-LOCK NO-ERROR.
         IF AVAILABLE cl-list THEN
         DO:
             DELETE cl-list.
             RELEASE cl-list.
             tot-rm = tot-rm - 1.
         END.
     END.
     /*end bernatd*/
  END. 
  /*MT
  FOR EACH cl-list WHERE cl-list.zipreis NE 0 BY cl-list.nation BY cl-list.bezeich:
      FIND FIRST s-list WHERE s-list.bezeich = cl-list.bezeich
          AND s-list.nat EQ cl-list.nat NO-ERROR.
      IF NOT AVAILABLE s-list THEN
      DO:
          CREATE s-list.
          s-list.rmcat = cl-list.rmcat.
          s-list.bezeich = cl-list.bezeich.
          s-list.nat = cl-list.nat.
      END.
      s-list.anz = s-list.anz + cl-list.qty.
      s-list.adult = s-list.adult + cl-list.a + cl-list.co. 
      s-list.child = s-list.child + cl-list.c.
      
  END.
  */
  FOR EACH cl-list BY cl-list.nation BY cl-list.bezeich: 
    /*ITA 021117*/
    FIND FIRST mealcoup WHERE mealcoup.NAME = "Breakfast" 
        AND mealcoup.resnr = cl-list.resnr
        AND mealcoup.zinr = cl-list.rmno  NO-LOCK NO-ERROR.
    IF AVAILABLE mealcoup THEN DO:
        ASSIGN cl-list.tot-bfast = mealcoup.verbrauch[1] + mealcoup.verbrauch[2] + mealcoup.verbrauch[3] + mealcoup.verbrauch[4] + mealcoup.verbrauch[5]
                                  + mealcoup.verbrauch[6] + mealcoup.verbrauch[7] + mealcoup.verbrauch[8] + mealcoup.verbrauch[9] + mealcoup.verbrauch[10]
                                  + mealcoup.verbrauch[11] + mealcoup.verbrauch[12] + mealcoup.verbrauch[13] + mealcoup.verbrauch[14] + mealcoup.verbrauch[15]
                                  + mealcoup.verbrauch[16] + mealcoup.verbrauch[17] + mealcoup.verbrauch[18] + mealcoup.verbrauch[19] + mealcoup.verbrauch[20]
                                  + mealcoup.verbrauch[21] + mealcoup.verbrauch[22] + mealcoup.verbrauch[23] + mealcoup.verbrauch[24] + mealcoup.verbrauch[25]
                                  + mealcoup.verbrauch[26] + mealcoup.verbrauch[27] + mealcoup.verbrauch[28] + mealcoup.verbrauch[29] + mealcoup.verbrauch[30]
                                  + mealcoup.verbrauch[31] + mealcoup.verbrauch[32].
    END.

    FIND FIRST s-list WHERE s-list.bezeich = cl-list.bezeich NO-ERROR. 
    IF NOT AVAILABLE s-list THEN 
    DO: 
      FIND FIRST s-list WHERE s-list.rmcat = "" NO-ERROR. 
      IF AVAILABLE s-list THEN 
      DO: 
        s-list.rmcat = cl-list.kurzbez. 
        s-list.bezeich = cl-list.bezeich. 
      END. 
    END. 
    IF NOT AVAILABLE s-list THEN 
    DO: 
      create s-list. 
      s-list.rmcat = cl-list.kurzbez. 
      s-list.bezeich = cl-list.bezeich. 
    END. 
    
    s-list.anz = s-list.anz + cl-list.qty. 
 
    FIND FIRST s-list WHERE s-list.nat = cl-list.nat NO-ERROR. 
    IF NOT AVAILABLE s-list THEN 
    DO: 
      FIND FIRST s-list WHERE s-list.nat = "" NO-ERROR. 
      IF AVAILABLE s-list THEN s-list.nat = cl-list.nat. 
    END. 
    IF NOT AVAILABLE s-list THEN 
    DO: 
      create s-list. 
      IF AVAILABLE s-list THEN s-list.nat = cl-list.nat. 
    END. 
    s-list.adult = s-list.adult + cl-list.a + cl-list.co. 
    s-list.child = s-list.child + cl-list.c. 

    s-list.rmqty = s-list.rmqty + cl-list.qty.
  END.
 
  IF (tot-a + tot-co) NE 0 THEN 
  FOR EACH s-list WHERE s-list.nat NE "": 
    FIND FIRST nation WHERE nation.kurzbez = s-list.nat NO-LOCK NO-ERROR. 
    IF AVAILABLE nation THEN s-list.nat = nation.bezeich. 
    s-list.proz = s-list.adult / (tot-a + tot-co) * 100. 
  END. 
 
END. 

PROCEDURE create-buf-queasy:
    FOR EACH t-buff-queasy:
        DELETE t-buff-queasy.
    END.

    FOR EACH queasy WHERE queasy.KEY = 140 AND queasy.char1 = prog-name 
         NO-LOCK :
        CREATE t-buff-queasy.
        BUFFER-COPY queasy TO t-buff-queasy.
    END.
END.
