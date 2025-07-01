/*gerald 070920 search for word and number 72D15D*/

DEFINE TEMP-TABLE str-list 
  FIELD flag        AS INTEGER 
  FIELD line1       AS CHAR FORMAT "x(61)" 
  FIELD line2       AS CHAR FORMAT "x(79)"
  FIELD address     AS CHAR FORMAT "x(100)". 
 
DEFINE TEMP-TABLE s-list 
  FIELD rmcat       AS CHAR FORMAT "x(6)" 
  FIELD bezeich     AS CHAR FORMAT "x(40)" 
  FIELD nat         AS CHAR FORMAT "x(24)" 
  FIELD anz         AS INTEGER FORMAT ">>9" 
  FIELD adult       AS INTEGER FORMAT ">>9" 
  FIELD proz        AS DECIMAL FORMAT ">>9.99" 
  FIELD child       AS INTEGER FORMAT ">>9". 
 
 DEFINE TEMP-TABLE cl-list 
  FIELD flag       AS INTEGER 
  FIELD nr         AS INTEGER   FORMAT ">,>>>" /*sis 181113 before ">>9"*/
  FIELD vip        AS CHAR      FORMAT "x(4)" 
  FIELD resnr      AS INTEGER   FORMAT ">>>>>>>" 
  FIELD name       AS CHAR      FORMAT "x(30)" 
  FIELD groupname  AS CHAR      FORMAT "x(24)" 
  FIELD rmno       LIKE zimmer.zinr /*MT 24/07/12 */
  FIELD qty        AS INTEGER   FORMAT ">>>>>9" /*MT 12/06/13 */
  FIELD arrive     AS CHARACTER FORMAT "x(10)" 
  FIELD depart     AS CHARACTER FORMAT "x(10)" 
  FIELD rmcat      AS CHAR      FORMAT "x(6)" 
  FIELD kurzbez    AS CHAR 
  FIELD bezeich    AS CHAR      FORMAT "x(40)"
  FIELD a          AS INTEGER   FORMAT "9" 
  FIELD c          AS INTEGER   FORMAT "9" 
  FIELD co         AS INTEGER   FORMAT ">>" 
  FIELD pax        AS CHAR      FORMAT "x(6)" 
  FIELD nat        AS CHAR      FORMAT "x(4)" 
  FIELD nation     AS CHAR      
  FIELD argt       AS CHAR      FORMAT "x(7)" 
  FIELD company    AS CHAR      FORMAT "x(30)" 
  FIELD flight     AS CHAR      FORMAT "x(6)" 
  FIELD etd        AS CHAR      FORMAT "99:99" 
  FIELD outstand   AS DECIMAL   FORMAT "->>>,>>>,>>9.99"
  FIELD bemerk     AS CHAR      FORMAT "x(2000)"
  /*naufal Add Remarks 1000 Char*/                              
  FIELD bemerk01   AS CHAR      FORMAT "x(255)"
  FIELD bemerk02   AS CHAR      FORMAT "x(255)"
  FIELD bemerk03   AS CHAR      FORMAT "x(255)"
  FIELD bemerk04   AS CHAR      FORMAT "x(255)"
  FIELD bemerk05   AS CHAR      FORMAT "x(255)"
  FIELD bemerk06   AS CHAR      FORMAT "x(255)"
  FIELD bemerk07   AS CHAR      FORMAT "x(255)"
  FIELD bemerk08   AS CHAR      FORMAT "x(255)"
  /*end naufal*/       
  FIELD email      AS CHAR      FORMAT "x(24)"
  FIELD email-adr  AS CHAR      FORMAT "x(40)" /*ITA 150813*/ /*ITA 190813*/
  FIELD tot-night  AS INT       
  FIELD ratecode   AS CHAR      FORMAT "x(10)"
  FIELD full-name  AS CHAR      
                                
  FIELD address    AS CHAR      FORMAT "x(100)"
  FIELD memberno   AS CHAR      FORMAT "x(20)"
  FIELD membertype AS CHAR      FORMAT "x(20)".

DEFINE TEMP-TABLE setup-list 
  FIELD nr          AS INTEGER 
  FIELD CHAR        AS CHAR FORMAT "x(1)". 

DEFINE INPUT  PARAMETER pvILanguage     AS INTEGER NO-UNDO.
DEFINE INPUT  PARAMETER case-type       AS INTEGER.
DEFINE INPUT  PARAMETER disptype        AS INTEGER.
DEFINE INPUT  PARAMETER curr-date       AS DATE.
DEFINE INPUT  PARAMETER froom           AS CHAR.
DEFINE INPUT  PARAMETER troom           AS CHAR.
DEFINE OUTPUT PARAMETER tot-rm          AS INTEGER INITIAL 0. 
DEFINE OUTPUT PARAMETER tot-a           AS INTEGER INITIAL 0. 
DEFINE OUTPUT PARAMETER tot-c           AS INTEGER INITIAL 0. 
DEFINE OUTPUT PARAMETER tot-co          AS INTEGER INITIAL 0. 
DEFINE INPUT  PARAMETER TABLE FOR setup-list.
DEFINE OUTPUT PARAMETER TABLE FOR str-list.
DEFINE OUTPUT PARAMETER TABLE FOR s-list.
DEFINE OUTPUT PARAMETER TABLE FOR cl-list.


DEFINE VARIABLE vipnr1 AS INTEGER INITIAL 999999999. 
DEFINE VARIABLE vipnr2 AS INTEGER INITIAL 999999999. 
DEFINE VARIABLE vipnr3 AS INTEGER INITIAL 999999999. 
DEFINE VARIABLE vipnr4 AS INTEGER INITIAL 999999999. 
DEFINE VARIABLE vipnr5 AS INTEGER INITIAL 999999999. 
DEFINE VARIABLE vipnr6 AS INTEGER INITIAL 999999999. 
DEFINE VARIABLE vipnr7 AS INTEGER INITIAL 999999999. 
DEFINE VARIABLE vipnr8 AS INTEGER INITIAL 999999999. 
DEFINE VARIABLE vipnr9 AS INTEGER INITIAL 999999999. 

{SupertransBL.i} 
DEF VAR lvCAREA AS CHAR INITIAL "PJ-depart". 

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

DEFINE VARIABLE all-remark AS LONGCHAR.

CASE case-type :
    WHEN 1 THEN RUN create-departure.
    WHEN 2 THEN RUN create-departure1.
    WHEN 3 THEN RUN create-actual.
    WHEN 4 THEN RUN create-expected.

END CASE.

PROCEDURE create-departure: 
    DEFINE VARIABLE i AS INTEGER. 
    DEFINE VARIABLE vip-flag AS CHAR. 
    DEFINE VARIABLE nr AS INTEGER INITIAL 0. 
    DEFINE buffer gmember FOR guest. 
    DEFINE VARIABLE str AS CHARACTER.
    DEFINE VARIABLE do-it AS LOGICAL. 
     
    tot-rm = 0. 
    tot-a = 0. 
    tot-c = 0. 
    tot-co = 0. 
    
    FOR EACH s-list: 
        delete s-list. 
    END. 
    
    FOR EACH cl-list: 
        delete cl-list. 
    END. 
    
    FOR EACH str-list: 
        delete str-list. 
    END. 
 
    IF disptype = 1 THEN 
    FOR EACH res-line WHERE (res-line.resstatus LE 2 OR res-line.resstatus = 5
        OR res-line.resstatus = 6 OR res-line.resstatus = 13 
        OR res-line.resstatus = 8) AND res-line.abreise = curr-date 
        AND ((res-line.zinr GE froom AND res-line.zinr LE troom)
        OR (res-line.zinr GE froom)) NO-LOCK, 
        FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr NO-LOCK, 
        FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
        FIRST guest WHERE guest.gastnr = reservation.gastnr NO-LOCK, 
        FIRST gmember WHERE gmember.gastnr = res-line.gastnrmember NO-LOCK 
        BY reservation.groupname BY res-line.name BY res-line.zinr: 
    
        do-it = YES. 
    
        IF res-line.resstatus = 8 AND 
            (res-line.ankunft = res-line.abreise) THEN 
        DO: 
            FIND FIRST history WHERE history.resnr = res-line.resnr 
            AND history.reslinnr = res-line.reslinnr 
            AND history.gesamtumsatz GT 0 NO-LOCK NO-ERROR. 
            IF NOT AVAILABLE history THEN do-it = NO. 
        END. 
     
    /* NEW: 01/12/2004 - aston bali : ignore the history validation */ 
        do-it = YES. 
     
        IF do-it THEN 
        DO: 
            /*FIND FIRST setup-list WHERE setup-list.nr = res-line.setup + 1. */ 

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
            IF AVAILABLE guestseg THEN vip-flag = "VIP". 
            create cl-list. 
            ASSIGN 
                cl-list.nr        = nr 
                cl-list.groupname = reservation.groupname 
                /*cl-list.rmcat     = zimkateg.kurzbez + setup-list.char */
                cl-list.kurzbez   = zimkateg.kurzbez 
                cl-list.bezeich   = zimkateg.bezeich 
                cl-list.nat       = gmember.nation1 
                cl-list.resnr     = res-line.resnr 
                cl-list.vip       = vip-flag 
                cl-list.name      = res-line.name 
                cl-list.rmno      = res-line.zinr 
                cl-list.arrive    = STRING(res-line.ankunft, "99/99/99")
                cl-list.depart    = STRING(res-line.abreise, "99/99/99")
                cl-list.a         = res-line.erwachs 
                cl-list.c         = res-line.kind1 + res-line.kind2 
                cl-list.co        = res-line.gratis 
                cl-list.argt      = res-line.arrangement 
                cl-list.flight    = SUBSTR(res-line.flight-nr, 12, 6) 
                cl-list.etd       = SUBSTR(res-line.flight-nr, 18, 5)
                cl-list.email-adr = gmember.email-adr 
                cl-list.address   = gmember.adresse1 + ", " + gmember.adresse2 + ", " + gmember.adresse3   
                .

            FIND FIRST setup-list WHERE setup-list.nr EQ res-line.setup + 1 NO-LOCK NO-ERROR.
            IF AVAILABLE setup-list THEN cl-list.rmcat = zimkateg.kurzbez + setup-list.char .
            ELSE cl-list.rmcat = zimkateg.kurzbez.
   
            DO i = 1 TO NUM-ENTRIES(res-line.zimmer-wunsch,";") - 1:
              str = ENTRY(i, res-line.zimmer-wunsch, ";").
              IF SUBSTR(str,1,6) = "$CODE$" THEN 
              DO:
                cl-list.ratecode  = SUBSTR(str,7).
                LEAVE.
              END.
            END.

            IF guest.karteityp NE 0 THEN
                cl-list.company   = guest.name + ", " + guest.vorname1 
                + " " + guest.anrede1 + guest.anredefirma.
            IF gmember.telefon NE "" THEN
                cl-list.company   = cl-list.company + ";" + gmember.telefon.
            
            IF (cl-list.etd = "0000" OR cl-list.etd = "") AND res-line.abreisezeit NE 0 THEN 
            DO: 
                cl-list.etd = STRING(res-line.abreisezeit, "HH:MM"). 
                cl-list.etd = SUBSTR(cl-list.etd,1,2) + SUBSTR(cl-list.etd,4,2). 
            END. 
            
            IF res-line.zinr = "" THEN cl-list.rmno = "#" + STRING(res-line.zimmeranz). 
            
            IF cl-list.nat = "" THEN cl-list.nat = "?". 
            ELSE 
            DO: 
                FIND FIRST nation WHERE nation.kurzbez = cl-list.nat NO-LOCK NO-ERROR. 
                IF AVAILABLE nation THEN cl-list.nation = nation.bezeich. 
            END. 
            IF res-line.resstatus LE 2 OR res-line.resstatus = 5 OR 
                res-line.resstatus = 6 OR (res-line.resstatus = 8 AND 
                (res-line.erwachs + res-line.gratis) GT 0) THEN 
            DO: 
                cl-list.qty = res-line.zimmeranz. 
                tot-rm = tot-rm + res-line.zimmeranz. 
            END. 
            /*
            DO i = 1 TO length(res-line.bemerk): 
                IF SUBSTR(res-line.bemerk,i,1) = chr(10) THEN 
                cl-list.bemerk = cl-list.bemerk + " ". 
                ELSE cl-list.bemerk = cl-list.bemerk + SUBSTR(res-line.bemerk, i, 1). 
            END.
            */
            DO i = 1 TO length(res-line.bemerk): 
                IF SUBSTR(res-line.bemerk,i,1) = chr(10) THEN 
                      cl-list.bemerk = cl-list.bemerk + " ". 
                ELSE cl-list.bemerk = cl-list.bemerk + SUBSTR(TRIM(res-line.bemerk), i, 1).
            END.
            /*naufal add remarks 1000 char*/
            all-remark = res-line.bemerk.
            all-remark = REPLACE(all-remark,CHR(10)," ").
            all-remark = REPLACE(all-remark,CHR(13)," ").
            
            cl-list.bemerk01 = STRING(SUBSTRING(all-remark,1,255)).
            cl-list.bemerk02 = STRING(SUBSTRING(all-remark,256,255)).
            cl-list.bemerk03 = STRING(SUBSTRING(all-remark,511,255)).
            cl-list.bemerk04 = STRING(SUBSTRING(all-remark,766,255)).
            cl-list.bemerk05 = STRING(SUBSTRING(all-remark,1021,255)).
            cl-list.bemerk06 = STRING(SUBSTRING(all-remark,1276,255)).
            cl-list.bemerk07 = STRING(SUBSTRING(all-remark,1531,255)).
            cl-list.bemerk08 = STRING(SUBSTRING(all-remark,1786,255)).
            /*end naufal add remarks 1000 char*/
            
            cl-list.pax = STRING(cl-list.a,"9") + "/" + STRING(cl-list.c,"9"). 
 
            IF res-line.active-flag = 1 THEN 
            FOR EACH bill WHERE bill.zinr = res-line.zinr 
                AND bill.parent-nr = res-line.reslinnr AND bill.flag = 0 NO-LOCK: 
                cl-list.outstand = cl-list.outstand + bill.saldo. 
            END. 
            
            /*DODY 16/10/18 penambahan membership number dan type of membership */
            FIND FIRST mc-guest WHERE mc-guest.gastnr = gmember.gastnr NO-LOCK NO-ERROR.
            IF AVAILABLE mc-guest THEN 
            DO:
                cl-list.memberno = mc-guest.cardnum.  
                FIND FIRST mc-types WHERE mc-types.nr = mc-guest.nr NO-LOCK NO-ERROR.
                IF AVAILABLE mc-types THEN cl-list.membertype = mc-types.bezeich. 
            END.
            
            tot-a = tot-a + res-line.erwachs. 
            tot-c = tot-c + res-line.kind1 + res-line.kind2. 
            tot-co = tot-co + res-line.gratis. 
        END. 
    END. 
    ELSE IF disptype = 3 THEN 
    FOR EACH res-line WHERE (res-line.resstatus LE 2 OR res-line.resstatus = 5
        OR res-line.resstatus = 6 OR res-line.resstatus EQ 13 
        OR res-line.resstatus = 8) AND res-line.abreise = curr-date 
        AND ((res-line.zinr GE froom AND res-line.zinr LE troom)
        OR (res-line.zinr GE froom)) NO-LOCK, 
        FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr NO-LOCK, 
        FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
        FIRST guest WHERE guest.gastnr = reservation.gastnr NO-LOCK, 
        FIRST gmember WHERE gmember.gastnr = res-line.gastnrmember NO-LOCK 
        BY reservation.name BY reservation.groupname 
        BY res-line.name BY res-line.zinr: 
        
        do-it = YES. 
        IF res-line.resstatus = 8 AND 
            (res-line.ankunft = res-line.abreise) THEN 
        DO: 
            FIND FIRST history WHERE history.resnr = res-line.resnr 
                AND history.reslinnr = res-line.reslinnr 
                AND history.gesamtumsatz GT 0 NO-LOCK NO-ERROR. 
            IF NOT AVAILABLE history THEN do-it = NO. 
        END. 
 
        /* NEW: 01/12/2004 - aston bali : ignore the history validation */ 
        do-it = YES. 
        
        IF do-it THEN 
        DO: 
            /*FIND FIRST setup-list WHERE setup-list.nr = res-line.setup + 1. */

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
            IF AVAILABLE guestseg THEN vip-flag = "VIP". 
            create cl-list. 
            ASSIGN 
                cl-list.nr        = nr 
                cl-list.groupname = reservation.groupname 
                /*cl-list.rmcat     = zimkateg.kurzbez + setup-list.char */
                cl-list.kurzbez   = zimkateg.kurzbez 
                cl-list.bezeich   = zimkateg.bezeich 
                cl-list.nat       = gmember.nation1 
                cl-list.resnr     = res-line.resnr 
                cl-list.vip       = vip-flag 
                cl-list.name      = res-line.name 
                cl-list.rmno      = res-line.zinr 
                cl-list.arrive    = STRING(res-line.ankunft, "99/99/99")
                cl-list.depart    = STRING(res-line.abreise, "99/99/99")
                cl-list.a         = res-line.erwachs 
                cl-list.c         = res-line.kind1 + res-line.kind2 
                cl-list.co        = res-line.gratis 
                cl-list.argt      = res-line.arrangement 
                cl-list.flight    = SUBSTR(res-line.flight-nr, 12, 6) 
                cl-list.etd       = SUBSTR(res-line.flight-nr, 18, 5) 
                cl-list.email-adr = gmember.email-adr
                cl-list.address   = gmember.adresse1 + ", " + gmember.adresse2 + ", " + gmember.adresse3     
                .

            FIND FIRST setup-list WHERE setup-list.nr EQ res-line.setup + 1 NO-LOCK NO-ERROR.
            IF AVAILABLE setup-list THEN cl-list.rmcat = zimkateg.kurzbez + setup-list.char .
            ELSE cl-list.rmcat = zimkateg.kurzbez.

            DO i = 1 TO NUM-ENTRIES(res-line.zimmer-wunsch,";") - 1:
              str = ENTRY(i, res-line.zimmer-wunsch, ";").
              IF SUBSTR(str,1,6) = "$CODE$" THEN 
              DO:
                cl-list.ratecode  = SUBSTR(str,7).
                LEAVE.
              END.
            END.

            IF guest.karteityp NE 0 THEN
                cl-list.company   = guest.name + ", " + guest.vorname1 
                + " " + guest.anrede1 + guest.anredefirma.
            IF gmember.telefon NE "" THEN
                cl-list.company   = cl-list.company + ";" + gmember.telefon.
        
            IF (cl-list.etd = "0000" OR cl-list.etd = "") AND res-line.abreisezeit NE 0 THEN 
            DO: 
                cl-list.etd = STRING(res-line.abreisezeit, "HH:MM"). 
                cl-list.etd = SUBSTR(cl-list.etd,1,2) + SUBSTR(cl-list.etd,4,2). 
            END. 
            
            IF res-line.zinr = "" THEN cl-list.rmno = "#" + STRING(res-line.zimmeranz). 
            
            IF cl-list.nat = "" THEN cl-list.nat = "?". 
            ELSE 
            DO: 
                FIND FIRST nation WHERE nation.kurzbez = cl-list.nat NO-LOCK NO-ERROR. 
                IF AVAILABLE nation THEN cl-list.nation = nation.bezeich. 
            END. 
 
            IF res-line.resstatus LE 2 OR res-line.resstatus = 5 OR 
               res-line.resstatus = 6 OR (res-line.resstatus = 8 AND 
              (res-line.erwachs + res-line.gratis) GT 0) THEN 
            DO: 
                cl-list.qty = res-line.zimmeranz. 
                tot-rm = tot-rm + res-line.zimmeranz. 
            END. 
            /*
            DO i = 1 TO length(res-line.bemerk): 
                IF SUBSTR(res-line.bemerk,i,1) = chr(10) THEN 
                cl-list.bemerk = cl-list.bemerk + " ". 
                ELSE cl-list.bemerk = cl-list.bemerk + SUBSTR(res-line.bemerk, i, 1). 
            END.
            */
            DO i = 1 TO length(res-line.bemerk): 
                IF SUBSTR(res-line.bemerk,i,1) = chr(10) THEN 
                      cl-list.bemerk = cl-list.bemerk + " ". 
                ELSE cl-list.bemerk = cl-list.bemerk + SUBSTR(TRIM(res-line.bemerk), i, 1).
            END.
            /*naufal add remarks 1000 char*/
            all-remark = res-line.bemerk.
            all-remark = REPLACE(all-remark,CHR(10)," ").
            all-remark = REPLACE(all-remark,CHR(13)," ").
            
            cl-list.bemerk01 = STRING(SUBSTRING(all-remark,1,255)).
            cl-list.bemerk02 = STRING(SUBSTRING(all-remark,256,255)).
            cl-list.bemerk03 = STRING(SUBSTRING(all-remark,511,255)).
            cl-list.bemerk04 = STRING(SUBSTRING(all-remark,766,255)).
            cl-list.bemerk05 = STRING(SUBSTRING(all-remark,1021,255)).
            cl-list.bemerk06 = STRING(SUBSTRING(all-remark,1276,255)).
            cl-list.bemerk07 = STRING(SUBSTRING(all-remark,1531,255)).
            cl-list.bemerk08 = STRING(SUBSTRING(all-remark,1786,255)).
            /*end naufal add remarks 1000 char*/
            
            cl-list.pax = STRING(cl-list.a,"9") + "/" + STRING(cl-list.c,"9"). 
            
            IF res-line.active-flag = 1 THEN 
            FOR EACH bill WHERE bill.zinr = res-line.zinr 
                AND bill.parent-nr = res-line.reslinnr AND bill.flag = 0 NO-LOCK: 
                cl-list.outstand = cl-list.outstand + bill.saldo. 
            END. 
            /*DODY 16/10/18 penambahan membership number dan type of membership */
            FIND FIRST mc-guest WHERE mc-guest.gastnr = gmember.gastnr NO-LOCK NO-ERROR.
            IF AVAILABLE mc-guest THEN 
            DO:
                cl-list.memberno = mc-guest.cardnum.  
                FIND FIRST mc-types WHERE mc-types.nr = mc-guest.nr NO-LOCK NO-ERROR.
                IF AVAILABLE mc-types THEN cl-list.membertype = mc-types.bezeich. 
            END.
            
            tot-a = tot-a + res-line.erwachs. 
            tot-c = tot-c + res-line.kind1 + res-line.kind2. 
            tot-co = tot-co + res-line.gratis. 
        END. 
    END. 
    ELSE IF disptype = 2 THEN 
    FOR EACH res-line WHERE (res-line.resstatus LE 2 OR res-line.resstatus = 5
        OR res-line.resstatus = 6 OR res-line.resstatus = 13 
        OR res-line.resstatus = 8) AND res-line.abreise = curr-date 
        AND ((res-line.zinr GE froom AND res-line.zinr LE troom)
        OR (res-line.zinr GE froom))  NO-LOCK, 
        FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr NO-LOCK, 
        FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
        FIRST guest WHERE guest.gastnr = reservation.gastnr NO-LOCK, 
        FIRST gmember WHERE gmember.gastnr = res-line.gastnrmember NO-LOCK 
        BY res-line.zinr BY res-line.name: 
     
        do-it = YES. 
        IF res-line.resstatus = 8 AND 
        (res-line.ankunft = res-line.abreise) THEN 
        DO: 
            FIND FIRST history WHERE history.resnr = res-line.resnr 
                AND history.reslinnr = res-line.reslinnr 
                AND history.gesamtumsatz GT 0 NO-LOCK NO-ERROR. 
            IF NOT AVAILABLE history THEN do-it = NO. 
        END. 
        
        /* NEW: 01/12/2004 - aston bali : ignore the history validation */ 
        do-it = YES. 
        
        IF do-it THEN 
        DO: 
            /*FIND FIRST setup-list WHERE setup-list.nr = res-line.setup + 1. */

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
            IF AVAILABLE guestseg THEN vip-flag = "VIP". 
            create cl-list. 
            ASSIGN 
                cl-list.nr        = nr 
                cl-list.groupname = reservation.groupname 
                /*cl-list.rmcat     = zimkateg.kurzbez + setup-list.char */
                cl-list.kurzbez   = zimkateg.kurzbez 
                cl-list.bezeich   = zimkateg.bezeich 
                cl-list.nat       = gmember.nation1 
                cl-list.resnr     = res-line.resnr 
                cl-list.vip       = vip-flag 
                cl-list.name      = res-line.name 
                cl-list.rmno      = res-line.zinr 
                cl-list.arrive    = STRING(res-line.ankunft, "99/99/99")
                cl-list.depart    = STRING(res-line.abreise, "99/99/99")
                cl-list.a         = res-line.erwachs 
                cl-list.c         = res-line.kind1 + res-line.kind2 
                cl-list.co        = res-line.gratis 
                cl-list.argt      = res-line.arrangement 
                cl-list.flight    = SUBSTR(res-line.flight-nr, 12, 6) 
                cl-list.etd       = SUBSTR(res-line.flight-nr, 18, 5)
                cl-list.email-adr = gmember.email-adr
                cl-list.address   = gmember.adresse1 + ", " + gmember.adresse2 + ", " + gmember.adresse3             
                .

            FIND FIRST setup-list WHERE setup-list.nr EQ res-line.setup + 1 NO-LOCK NO-ERROR.
            IF AVAILABLE setup-list THEN cl-list.rmcat = zimkateg.kurzbez + setup-list.char .
            ELSE cl-list.rmcat = zimkateg.kurzbez.

            DO i = 1 TO NUM-ENTRIES(res-line.zimmer-wunsch,";") - 1:
              str = ENTRY(i, res-line.zimmer-wunsch, ";").
              IF SUBSTR(str,1,6) = "$CODE$" THEN 
              DO:
                cl-list.ratecode  = SUBSTR(str,7).
                LEAVE.
              END.
            END.

            IF guest.karteityp NE 0 THEN
                cl-list.company   = guest.name + ", " + guest.vorname1 
                + " " + guest.anrede1 + guest.anredefirma.
            IF gmember.telefon NE "" THEN
                cl-list.company   = cl-list.company + ";" + gmember.telefon.
            
            IF (cl-list.etd = "0000" OR cl-list.etd = "") AND res-line.abreisezeit NE 0 THEN 
            DO: 
                cl-list.etd = STRING(res-line.abreisezeit, "HH:MM"). 
                cl-list.etd = SUBSTR(cl-list.etd,1,2) + SUBSTR(cl-list.etd,4,2). 
            END. 
            
            IF res-line.zinr = "" THEN cl-list.rmno = "#" + STRING(res-line.zimmeranz). 
            
            IF cl-list.nat = "" THEN cl-list.nat = "?". 
            ELSE 
            DO: 
                FIND FIRST nation WHERE nation.kurzbez = cl-list.nat NO-LOCK NO-ERROR. 
                IF AVAILABLE nation THEN cl-list.nation = nation.bezeich. 
            END. 
 
            IF res-line.resstatus LE 2 OR res-line.resstatus = 5 OR 
                res-line.resstatus = 6 OR (res-line.resstatus = 8 AND 
                (res-line.erwachs + res-line.gratis) GT 0) THEN 
            DO: 
                cl-list.qty = res-line.zimmeranz. 
                tot-rm = tot-rm + res-line.zimmeranz. 
            END. 
            /*
            DO i = 1 TO length(res-line.bemerk): 
                IF SUBSTR(res-line.bemerk,i,1) = chr(10) THEN 
                cl-list.bemerk = cl-list.bemerk + " ". 
                ELSE cl-list.bemerk = cl-list.bemerk + SUBSTR(res-line.bemerk, i, 1). 
            END.
            */
            DO i = 1 TO length(res-line.bemerk): 
                IF SUBSTR(res-line.bemerk,i,1) = chr(10) THEN 
                      cl-list.bemerk = cl-list.bemerk + " ". 
                ELSE cl-list.bemerk = cl-list.bemerk + SUBSTR(TRIM(res-line.bemerk), i, 1).
            END.
            /*naufal add remarks 1000 char*/
            all-remark = res-line.bemerk.
            all-remark = REPLACE(all-remark,CHR(10)," ").
            all-remark = REPLACE(all-remark,CHR(13)," ").
            
            cl-list.bemerk01 = STRING(SUBSTRING(all-remark,1,255)).
            cl-list.bemerk02 = STRING(SUBSTRING(all-remark,256,255)).
            cl-list.bemerk03 = STRING(SUBSTRING(all-remark,511,255)).
            cl-list.bemerk04 = STRING(SUBSTRING(all-remark,766,255)).
            cl-list.bemerk05 = STRING(SUBSTRING(all-remark,1021,255)).
            cl-list.bemerk06 = STRING(SUBSTRING(all-remark,1276,255)).
            cl-list.bemerk07 = STRING(SUBSTRING(all-remark,1531,255)).
            cl-list.bemerk08 = STRING(SUBSTRING(all-remark,1786,255)).
            /*end naufal add remarks 1000 char*/
            
            cl-list.pax = STRING(cl-list.a,"9") + "/" + STRING(cl-list.c,"9"). 
            
            IF res-line.active-flag = 1 THEN 
            FOR EACH bill WHERE bill.zinr = res-line.zinr 
                AND bill.parent-nr = res-line.reslinnr AND bill.flag = 0 NO-LOCK: 
                cl-list.outstand = cl-list.outstand + bill.saldo. 
            END. 
            /*DODY 16/10/18 penambahan membership number dan type of membership */
            FIND FIRST mc-guest WHERE mc-guest.gastnr = gmember.gastnr NO-LOCK NO-ERROR.
            IF AVAILABLE mc-guest THEN 
            DO:
                cl-list.memberno = mc-guest.cardnum.  
                FIND FIRST mc-types WHERE mc-types.nr = mc-guest.nr NO-LOCK NO-ERROR.
                IF AVAILABLE mc-types THEN cl-list.membertype = mc-types.bezeich. 
            END.
            
            tot-a = tot-a + res-line.erwachs. 
            tot-c = tot-c + res-line.kind1 + res-line.kind2. 
            tot-co = tot-co + res-line.gratis. 
        END. 
    END. 
 
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
    END. 
 
    IF (tot-a + tot-co) NE 0 THEN 
    FOR EACH s-list WHERE s-list.nat NE "": 
        FIND FIRST nation WHERE nation.kurzbez = s-list.nat NO-LOCK NO-ERROR. 
        IF AVAILABLE nation THEN s-list.nat = nation.bezeich. 
        ELSE s-list.nat = translateExtended ("UNKNOWN",lvCAREA,""). 
        s-list.proz = s-list.adult / (tot-a + tot-co) * 100. 
    END. 
END. 

PROCEDURE create-departure1:   /* OK */ 
    DEFINE VARIABLE i AS INTEGER. 
    DEFINE VARIABLE vip-flag AS CHAR. 
    DEFINE VARIABLE nr AS INTEGER INITIAL 0. 
    DEFINE VARIABLE str AS CHARACTER.
    DEFINE buffer gmember FOR guest. 
    DEFINE VARIABLE do-it AS LOGICAL. 
     
    tot-rm = 0. 
    tot-a = 0. 
    tot-c = 0. 
    tot-co = 0. 
    
    FOR EACH s-list: 
        delete s-list. 
    END. 
    
    FOR EACH cl-list: 
        delete cl-list. 
    END. 
    
    FOR EACH str-list: 
        delete str-list. 
    END. 
 
    IF disptype = 1 THEN 
    FOR EACH res-line WHERE res-line.resstatus = 8 
        AND res-line.abreise = curr-date 
        AND ((res-line.zinr GE froom AND res-line.zinr LE troom)
        OR (res-line.zinr GE froom)) NO-LOCK, 
        FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr NO-LOCK, 
        FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
        FIRST guest WHERE guest.gastnr = reservation.gastnr NO-LOCK, 
        FIRST gmember WHERE gmember.gastnr = res-line.gastnrmember NO-LOCK 
        BY reservation.groupname BY res-line.name BY res-line.zinr: 
    
        do-it = YES. 
        IF res-line.ankunft = res-line.abreise THEN 
        DO: 
            FIND FIRST history WHERE history.resnr = res-line.resnr 
                AND history.reslinnr = res-line.reslinnr 
                AND history.gesamtumsatz GT 0 NO-LOCK NO-ERROR. 
            IF NOT AVAILABLE history THEN do-it = NO. 
        END. 
 
        /* NEW: 01/12/2004 - aston bali : ignore the history validation */ 
        do-it = YES. 
 
        IF do-it THEN 
        DO: 
            /*FIND FIRST setup-list WHERE setup-list.nr = res-line.setup + 1. */
            
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
            IF AVAILABLE guestseg THEN vip-flag = "VIP". 
 
            create cl-list. 
            ASSIGN 
                cl-list.nr        = nr 
                cl-list.groupname = reservation.groupname 
                /*cl-list.rmcat     = zimkateg.kurzbez + setup-list.char*/
                cl-list.kurzbez   = zimkateg.kurzbez 
                cl-list.bezeich   = zimkateg.bezeich 
                cl-list.nat       = gmember.nation1 
                cl-list.resnr     = res-line.resnr 
                cl-list.vip       = vip-flag 
                cl-list.name      = res-line.name 
                cl-list.rmno      = res-line.zinr 
                cl-list.arrive    = STRING(res-line.ankunft, "99/99/99")
                cl-list.depart    = STRING(res-line.abreise, "99/99/99") 
                cl-list.a         = res-line.erwachs 
                cl-list.c         = res-line.kind1 + res-line.kind2 
                cl-list.co        = res-line.gratis 
                cl-list.argt      = res-line.arrangement 
                cl-list.flight    = SUBSTR(res-line.flight-nr, 12, 6) 
                cl-list.etd       = SUBSTR(res-line.flight-nr, 18, 5)
                cl-list.email-adr = gmember.email-adr
                cl-list.address   = gmember.adresse1 + ", " + gmember.adresse2 + ", " + gmember.adresse3             
                .

            FIND FIRST setup-list WHERE setup-list.nr EQ res-line.setup + 1 NO-LOCK NO-ERROR.
            IF AVAILABLE setup-list THEN cl-list.rmcat = zimkateg.kurzbez + setup-list.char .
            ELSE cl-list.rmcat = zimkateg.kurzbez.

            DO i = 1 TO NUM-ENTRIES(res-line.zimmer-wunsch,";") - 1:
              str = ENTRY(i, res-line.zimmer-wunsch, ";").
              IF SUBSTR(str,1,6) = "$CODE$" THEN 
              DO:
                cl-list.ratecode  = SUBSTR(str,7).
                LEAVE.
              END.
            END.

            IF guest.karteityp NE 0 THEN
                cl-list.company   = guest.name + ", " + guest.vorname1 
                + " " + guest.anrede1 + guest.anredefirma.
            IF gmember.telefon NE "" THEN
                cl-list.company   = cl-list.company + ";" + gmember.telefon.
            
            IF (cl-list.etd = "0000" OR cl-list.etd = "") AND res-line.abreisezeit NE 0 THEN 
            DO: 
                cl-list.etd = STRING(res-line.abreisezeit, "HH:MM"). 
                cl-list.etd = SUBSTR(cl-list.etd,1,2) + SUBSTR(cl-list.etd,4,2). 
            END. 
 
            IF cl-list.nat = "" THEN cl-list.nat = "?". 
            ELSE 
            DO: 
                FIND FIRST nation WHERE nation.kurzbez = cl-list.nat NO-LOCK NO-ERROR. 
                IF AVAILABLE nation THEN cl-list.nation = nation.bezeich. 
            END. 
            
            IF (res-line.erwachs + res-line.gratis) GT 0 THEN 
            DO: 
                tot-rm = tot-rm + 1. 
                cl-list.qty = res-line.zimmeranz. 
            END. 
            /*
            DO i = 1 TO length(res-line.bemerk): 
                IF SUBSTR(res-line.bemerk,i,1) = chr(10) THEN 
                cl-list.bemerk = cl-list.bemerk + " ". 
                ELSE cl-list.bemerk = cl-list.bemerk + SUBSTR(res-line.bemerk, i, 1). 
            END.
            */
            DO i = 1 TO length(res-line.bemerk): 
                IF SUBSTR(res-line.bemerk,i,1) = chr(10) THEN 
                      cl-list.bemerk = cl-list.bemerk + " ". 
                ELSE cl-list.bemerk = cl-list.bemerk + SUBSTR(TRIM(res-line.bemerk), i, 1).
            END.
            /*naufal add remarks 1000 char*/
            all-remark = res-line.bemerk.
            all-remark = REPLACE(all-remark,CHR(10)," ").
            all-remark = REPLACE(all-remark,CHR(13)," ").
            
            cl-list.bemerk01 = STRING(SUBSTRING(all-remark,1,255)).
            cl-list.bemerk02 = STRING(SUBSTRING(all-remark,256,255)).
            cl-list.bemerk03 = STRING(SUBSTRING(all-remark,511,255)).
            cl-list.bemerk04 = STRING(SUBSTRING(all-remark,766,255)).
            cl-list.bemerk05 = STRING(SUBSTRING(all-remark,1021,255)).
            cl-list.bemerk06 = STRING(SUBSTRING(all-remark,1276,255)).
            cl-list.bemerk07 = STRING(SUBSTRING(all-remark,1531,255)).
            cl-list.bemerk08 = STRING(SUBSTRING(all-remark,1786,255)).
            /*end naufal add remarks 1000 char*/
 
            cl-list.pax = STRING(cl-list.a,"9") + "/" + STRING(cl-list.c,"9"). 
            /*DODY 16/10/18 penambahan membership number dan type of membership */
            FIND FIRST mc-guest WHERE mc-guest.gastnr = gmember.gastnr NO-LOCK NO-ERROR.
            IF AVAILABLE mc-guest THEN 
            DO:
                cl-list.memberno = mc-guest.cardnum.  
                FIND FIRST mc-types WHERE mc-types.nr = mc-guest.nr NO-LOCK NO-ERROR.
                IF AVAILABLE mc-types THEN cl-list.membertype = mc-types.bezeich. 
            END.
        
            tot-a = tot-a + res-line.erwachs. 
            tot-c = tot-c + res-line.kind1 + res-line.kind2. 
            tot-co = tot-co + res-line.gratis. 
        END. 
    END. 
 
    ELSE IF disptype = 2 THEN 
    FOR EACH res-line WHERE res-line.resstatus = 8 
        AND res-line.abreise = curr-date 
        AND ((res-line.zinr GE froom AND res-line.zinr LE troom)
        OR (res-line.zinr GE froom)) NO-LOCK, 
        FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr NO-LOCK, 
        FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
        FIRST guest WHERE guest.gastnr = reservation.gastnr NO-LOCK, 
        FIRST gmember WHERE gmember.gastnr = res-line.gastnrmember NO-LOCK 
        BY res-line.zinr BY res-line.NAME: 
 
        do-it = YES. 
        IF res-line.ankunft = res-line.abreise THEN 
        DO: 
            FIND FIRST history WHERE history.resnr = res-line.resnr 
                AND history.reslinnr = res-line.reslinnr 
                AND history.gesamtumsatz GT 0 NO-LOCK NO-ERROR. 
            IF NOT AVAILABLE history THEN do-it = NO. 
        END. 
 
        /* NEW: 01/12/2004 - aston bali : ignore the history validation */ 
        do-it = YES. 
 
        IF do-it THEN 
        DO: 
            /*FIND FIRST setup-list WHERE setup-list.nr = res-line.setup + 1.*/
 
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
            IF AVAILABLE guestseg THEN vip-flag = "VIP". 
 
            create cl-list. 
            ASSIGN 
                cl-list.nr        = nr 
                cl-list.groupname = reservation.groupname 
                /*cl-list.rmcat     = zimkateg.kurzbez + setup-list.char*/ 
                cl-list.kurzbez   = zimkateg.kurzbez 
                cl-list.bezeich   = zimkateg.bezeich 
                cl-list.nat       = gmember.nation1 
                cl-list.resnr     = res-line.resnr 
                cl-list.vip       = vip-flag 
                cl-list.name      = res-line.name 
                cl-list.rmno      = res-line.zinr 
                cl-list.arrive    = STRING(res-line.ankunft, "99/99/99")
                cl-list.depart    = STRING(res-line.abreise, "99/99/99")
                cl-list.a         = res-line.erwachs 
                cl-list.c         = res-line.kind1 + res-line.kind2 
                cl-list.co        = res-line.gratis 
                cl-list.argt      = res-line.arrangement 
                cl-list.flight    = SUBSTR(res-line.flight-nr, 12, 6) 
                cl-list.etd       = SUBSTR(res-line.flight-nr, 18, 5)
                cl-list.email-adr = gmember.email-adr
                cl-list.address   = gmember.adresse1 + ", " + gmember.adresse2 + ", " + gmember.adresse3             
                .

            FIND FIRST setup-list WHERE setup-list.nr EQ res-line.setup + 1 NO-LOCK NO-ERROR.
            IF AVAILABLE setup-list THEN cl-list.rmcat = zimkateg.kurzbez + setup-list.char .
            ELSE cl-list.rmcat = zimkateg.kurzbez.

            DO i = 1 TO NUM-ENTRIES(res-line.zimmer-wunsch,";") - 1:
              str = ENTRY(i, res-line.zimmer-wunsch, ";").
              IF SUBSTR(str,1,6) = "$CODE$" THEN 
              DO:
                cl-list.ratecode  = SUBSTR(str,7).
                LEAVE.
              END.
            END.

            IF guest.karteityp NE 0 THEN
                cl-list.company   = guest.name + ", " + guest.vorname1 
                + " " + guest.anrede1 + guest.anredefirma.
            IF gmember.telefon NE "" THEN
                cl-list.company   = cl-list.company + ";" + gmember.telefon.
 
            IF (cl-list.etd = "0000" OR cl-list.etd = "") AND res-line.abreisezeit NE 0 THEN 
            DO: 
                cl-list.etd = STRING(res-line.abreisezeit, "HH:MM"). 
                cl-list.etd = SUBSTR(cl-list.etd,1,2) + SUBSTR(cl-list.etd,4,2). 
            END. 
            
            IF cl-list.nat = "" THEN cl-list.nat = "?". 
            ELSE 
            DO: 
              FIND FIRST nation WHERE nation.kurzbez = cl-list.nat NO-LOCK NO-ERROR. 
              IF AVAILABLE nation THEN cl-list.nation = nation.bezeich. 
            END. 
 
            IF (res-line.erwachs + res-line.gratis) GT 0 THEN 
            DO: 
              tot-rm = tot-rm + 1. 
              cl-list.qty = res-line.zimmeranz. 
            END. 
            /*
            DO i = 1 TO length(res-line.bemerk): 
              IF SUBSTR(res-line.bemerk,i,1) = chr(10) THEN 
              cl-list.bemerk = cl-list.bemerk + " ". 
              ELSE cl-list.bemerk = cl-list.bemerk + SUBSTR(res-line.bemerk, i, 1). 
            END.
            */
            DO i = 1 TO length(res-line.bemerk): 
                IF SUBSTR(res-line.bemerk,i,1) = chr(10) THEN 
                      cl-list.bemerk = cl-list.bemerk + " ". 
                ELSE cl-list.bemerk = cl-list.bemerk + SUBSTR(TRIM(res-line.bemerk), i, 1).
            END.
            /*naufal add remarks 1000 char*/
            all-remark = res-line.bemerk.
            all-remark = REPLACE(all-remark,CHR(10)," ").
            all-remark = REPLACE(all-remark,CHR(13)," ").
            
            cl-list.bemerk01 = STRING(SUBSTRING(all-remark,1,255)).
            cl-list.bemerk02 = STRING(SUBSTRING(all-remark,256,255)).
            cl-list.bemerk03 = STRING(SUBSTRING(all-remark,511,255)).
            cl-list.bemerk04 = STRING(SUBSTRING(all-remark,766,255)).
            cl-list.bemerk05 = STRING(SUBSTRING(all-remark,1021,255)).
            cl-list.bemerk06 = STRING(SUBSTRING(all-remark,1276,255)).
            cl-list.bemerk07 = STRING(SUBSTRING(all-remark,1531,255)).
            cl-list.bemerk08 = STRING(SUBSTRING(all-remark,1786,255)).
            /*end naufal add remarks 1000 char*/
 
            cl-list.pax = STRING(cl-list.a,"9") + "/" + STRING(cl-list.c,"9"). 
            /*DODY 16/10/18 penambahan membership number dan type of membership */
            FIND FIRST mc-guest WHERE mc-guest.gastnr = gmember.gastnr NO-LOCK NO-ERROR.
            IF AVAILABLE mc-guest THEN 
            DO:
                cl-list.memberno = mc-guest.cardnum.  
                FIND FIRST mc-types WHERE mc-types.nr = mc-guest.nr NO-LOCK NO-ERROR.
                IF AVAILABLE mc-types THEN cl-list.membertype = mc-types.bezeich. 
            END.
 
            tot-a = tot-a + res-line.erwachs. 
            tot-c = tot-c + res-line.kind1 + res-line.kind2. 
            tot-co = tot-co + res-line.gratis. 
        END. 
    END. 
 
    ELSE IF disptype = 3 THEN 
    FOR EACH res-line WHERE res-line.resstatus = 8 
        AND res-line.abreise = curr-date 
        AND ((res-line.zinr GE froom AND res-line.zinr LE troom)
        OR (res-line.zinr GE froom)) NO-LOCK, 
        FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr NO-LOCK, 
        FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
        FIRST guest WHERE guest.gastnr = reservation.gastnr NO-LOCK, 
        FIRST gmember WHERE gmember.gastnr = res-line.gastnrmember NO-LOCK 
        BY reservation.name BY reservation.groupname 
        BY res-line.name BY res-line.zinr: 
 
        do-it = YES. 
        IF res-line.ankunft = res-line.abreise THEN 
        DO: 
            FIND FIRST history WHERE history.resnr = res-line.resnr 
                AND history.reslinnr = res-line.reslinnr 
                AND history.gesamtumsatz GT 0 NO-LOCK NO-ERROR. 
            IF NOT AVAILABLE history THEN do-it = NO. 
        END. 
 
        /* NEW: 01/12/2004 - aston bali : ignore the history validation */ 
        do-it = YES. 
        
        IF do-it THEN 
        DO: 
            /*FIND FIRST setup-list WHERE setup-list.nr = res-line.setup + 1. */
 
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
            IF AVAILABLE guestseg THEN vip-flag = "VIP". 
 
            create cl-list. 
            ASSIGN 
                cl-list.nr        = nr 
                cl-list.groupname = reservation.groupname 
                /*cl-list.rmcat     = zimkateg.kurzbez + setup-list.char */
                cl-list.kurzbez   = zimkateg.kurzbez 
                cl-list.bezeich   = zimkateg.bezeich 
                cl-list.nat       = gmember.nation1 
                cl-list.resnr     = res-line.resnr 
                cl-list.vip       = vip-flag 
                cl-list.name      = res-line.name 
                cl-list.rmno      = res-line.zinr 
                cl-list.arrive    = STRING(res-line.ankunft, "99/99/99")
                cl-list.depart    = STRING(res-line.abreise, "99/99/99") 
                cl-list.a         = res-line.erwachs 
                cl-list.c         = res-line.kind1 + res-line.kind2 
                cl-list.co        = res-line.gratis 
                cl-list.argt      = res-line.arrangement 
                cl-list.flight    = SUBSTR(res-line.flight-nr, 12, 6) 
                cl-list.etd       = SUBSTR(res-line.flight-nr, 18, 5)
                cl-list.email-adr = gmember.email-adr
                cl-list.address   = gmember.adresse1 + ", " + gmember.adresse2 + ", " + gmember.adresse3             
                .
            
            FIND FIRST setup-list WHERE setup-list.nr EQ res-line.setup + 1 NO-LOCK NO-ERROR.
            IF AVAILABLE setup-list THEN cl-list.rmcat = zimkateg.kurzbez + setup-list.char .
            ELSE cl-list.rmcat = zimkateg.kurzbez.

            DO i = 1 TO NUM-ENTRIES(res-line.zimmer-wunsch,";") - 1:
              str = ENTRY(i, res-line.zimmer-wunsch, ";").
              IF SUBSTR(str,1,6) = "$CODE$" THEN 
              DO:
                cl-list.ratecode  = SUBSTR(str,7).
                LEAVE.
              END.
            END.

            IF guest.karteityp NE 0 THEN
                cl-list.company   = guest.name + ", " + guest.vorname1 
                + " " + guest.anrede1 + guest.anredefirma.
            IF gmember.telefon NE "" THEN
                cl-list.company   = cl-list.company + ";" + gmember.telefon.
            
            IF (cl-list.etd = "0000" OR cl-list.etd = "") AND res-line.abreisezeit NE 0 THEN 
            DO: 
                cl-list.etd = STRING(res-line.abreisezeit, "HH:MM"). 
                cl-list.etd = SUBSTR(cl-list.etd,1,2) + SUBSTR(cl-list.etd,4,2). 
            END. 
            
            IF cl-list.nat = "" THEN cl-list.nat = "?". 
            ELSE 
            DO: 
                FIND FIRST nation WHERE nation.kurzbez = cl-list.nat NO-LOCK NO-ERROR. 
                IF AVAILABLE nation THEN cl-list.nation = nation.bezeich. 
            END. 
            
            IF (res-line.erwachs + res-line.gratis) GT 0 THEN 
            DO: 
                tot-rm = tot-rm + 1. 
                cl-list.qty = res-line.zimmeranz. 
            END. 
            /*
            DO i = 1 TO length(res-line.bemerk): 
                IF SUBSTR(res-line.bemerk,i,1) = chr(10) THEN 
                    cl-list.bemerk = cl-list.bemerk + " ". 
                ELSE cl-list.bemerk = cl-list.bemerk + SUBSTR(res-line.bemerk, i, 1). 
            END.
            */
            DO i = 1 TO length(res-line.bemerk): 
                IF SUBSTR(res-line.bemerk,i,1) = chr(10) THEN 
                      cl-list.bemerk = cl-list.bemerk + " ". 
                ELSE cl-list.bemerk = cl-list.bemerk + SUBSTR(TRIM(res-line.bemerk), i, 1).
            END.
            /*naufal add remarks 1000 char*/
            all-remark = res-line.bemerk.
            all-remark = REPLACE(all-remark,CHR(10)," ").
            all-remark = REPLACE(all-remark,CHR(13)," ").
            
            cl-list.bemerk01 = STRING(SUBSTRING(all-remark,1,255)).
            cl-list.bemerk02 = STRING(SUBSTRING(all-remark,256,255)).
            cl-list.bemerk03 = STRING(SUBSTRING(all-remark,511,255)).
            cl-list.bemerk04 = STRING(SUBSTRING(all-remark,766,255)).
            cl-list.bemerk05 = STRING(SUBSTRING(all-remark,1021,255)).
            cl-list.bemerk06 = STRING(SUBSTRING(all-remark,1276,255)).
            cl-list.bemerk07 = STRING(SUBSTRING(all-remark,1531,255)).
            cl-list.bemerk08 = STRING(SUBSTRING(all-remark,1786,255)).
            /*end naufal add remarks 1000 char*/
            
            cl-list.pax = STRING(cl-list.a,"9") + "/" + STRING(cl-list.c,"9"). 
            
            /*DODY 16/10/18 penambahan membership number dan type of membership */
            FIND FIRST mc-guest WHERE mc-guest.gastnr = gmember.gastnr NO-LOCK NO-ERROR.
            IF AVAILABLE mc-guest THEN 
            DO:
                cl-list.memberno = mc-guest.cardnum.  
                FIND FIRST mc-types WHERE mc-types.nr = mc-guest.nr NO-LOCK NO-ERROR.
                IF AVAILABLE mc-types THEN cl-list.membertype = mc-types.bezeich. 
            END.
            
            tot-a = tot-a + res-line.erwachs. 
            tot-c = tot-c + res-line.kind1 + res-line.kind2. 
            tot-co = tot-co + res-line.gratis. 
        END. 
    END. 
 
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
    END. 
 
    IF (tot-a + tot-co) NE 0 THEN 
    FOR EACH s-list WHERE s-list.nat NE "": 
        FIND FIRST nation WHERE nation.kurzbez = s-list.nat NO-LOCK NO-ERROR. 
        IF AVAILABLE nation THEN s-list.nat = nation.bezeich. 
        ELSE s-list.nat = translateExtended ("UNKNOWN",lvCAREA,""). 
        s-list.proz = s-list.adult / (tot-a + tot-co) * 100. 
    END.     
END. 

PROCEDURE create-actual: 
    DEFINE VARIABLE i AS INTEGER. 
    DEFINE VARIABLE vip-flag AS CHAR. 
    DEFINE VARIABLE nr AS INTEGER INITIAL 0. 
    DEFINE VARIABLE str AS CHARACTER.
    DEFINE buffer gmember FOR guest. 
    DEFINE VARIABLE do-it AS LOGICAL. 
 
    tot-rm = 0. 
    tot-a = 0. 
    tot-c = 0. 
    tot-co = 0. 
 
    FOR EACH s-list: 
        delete s-list. 
    END. 
    
    FOR EACH cl-list: 
        delete cl-list. 
    END. 
    
    FOR EACH str-list: 
        delete str-list. 
    END. 
 
    IF disptype = 2 THEN 
    FOR EACH res-line WHERE res-line.resstatus = 8 
        AND res-line.abreise = curr-date 
        AND ((res-line.zinr GE froom AND res-line.zinr LE troom)
        OR (res-line.zinr GE froom)) NO-LOCK, 
        FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr NO-LOCK, 
        FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
        FIRST guest WHERE guest.gastnr = reservation.gastnr NO-LOCK, 
        FIRST gmember WHERE gmember.gastnr = res-line.gastnrmember NO-LOCK 
        BY res-line.zinr BY res-line.name: 
 
        do-it = YES. 
        IF res-line.ankunft = res-line.abreise THEN 
        DO: 
            FIND FIRST history WHERE history.resnr = res-line.resnr 
                AND history.reslinnr = res-line.reslinnr 
                AND history.gesamtumsatz GT 0 NO-LOCK NO-ERROR. 
            IF NOT AVAILABLE history THEN do-it = NO. 
        END. 
 
        /* NEW: 01/12/2004 - aston bali : ignore the history validation */ 
        do-it = YES. 
        
        IF do-it THEN 
        DO: 
            /*FIND FIRST setup-list WHERE setup-list.nr = res-line.setup + 1. */
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
            IF AVAILABLE guestseg THEN vip-flag = "VIP". 
            create cl-list. 
            ASSIGN 
                cl-list.nr        = nr 
                cl-list.groupname = reservation.groupname 
                /*cl-list.rmcat     = zimkateg.kurzbez + setup-list.char */
                cl-list.kurzbez   = zimkateg.kurzbez 
                cl-list.bezeich   = zimkateg.bezeich 
                cl-list.nat       = gmember.nation1 
                cl-list.resnr     = res-line.resnr 
                cl-list.vip       = vip-flag 
                cl-list.name      = res-line.name 
                cl-list.rmno      = res-line.zinr 
                cl-list.arrive    = STRING(res-line.ankunft, "99/99/99")
                cl-list.depart    = STRING(res-line.abreise, "99/99/99")
                cl-list.a         = res-line.erwachs 
                cl-list.c         = res-line.kind1 + res-line.kind2 
                cl-list.co        = res-line.gratis 
                cl-list.argt      = res-line.arrangement 
                cl-list.flight    = SUBSTR(res-line.flight-nr, 12, 6) 
                cl-list.etd       = SUBSTR(res-line.flight-nr, 18, 5)
                cl-list.email-adr = gmember.email-adr
                cl-list.address   = gmember.adresse1 + ", " + gmember.adresse2 + ", " + gmember.adresse3             
                .

            FIND FIRST setup-list WHERE setup-list.nr EQ res-line.setup + 1 NO-LOCK NO-ERROR.
            IF AVAILABLE setup-list THEN cl-list.rmcat = zimkateg.kurzbez + setup-list.char .
            ELSE cl-list.rmcat = zimkateg.kurzbez.

            DO i = 1 TO NUM-ENTRIES(res-line.zimmer-wunsch,";") - 1:
              str = ENTRY(i, res-line.zimmer-wunsch, ";").
              IF SUBSTR(str,1,6) = "$CODE$" THEN 
              DO:
                cl-list.ratecode  = SUBSTR(str,7).
                LEAVE.
              END.
            END.

            IF guest.karteityp NE 0 THEN
                cl-list.company   = guest.name + ", " + guest.vorname1 
                + " " + guest.anrede1 + guest.anredefirma.
            IF gmember.telefon NE "" THEN
                cl-list.company   = cl-list.company + ";" + gmember.telefon.
            
            IF (cl-list.etd = "0000" OR cl-list.etd = "") AND res-line.abreisezeit NE 0 THEN 
            DO: 
                cl-list.etd = STRING(res-line.abreisezeit, "HH:MM"). 
                cl-list.etd = SUBSTR(cl-list.etd,1,2) + SUBSTR(cl-list.etd,4,2). 
            END. 
 
            IF cl-list.nat = "" THEN cl-list.nat = "?". 
            ELSE 
            DO: 
                FIND FIRST nation WHERE nation.kurzbez = cl-list.nat NO-LOCK NO-ERROR. 
                IF AVAILABLE nation THEN cl-list.nation = nation.bezeich. 
            END. 
            IF (res-line.erwachs + res-line.gratis) GT 0 THEN 
            DO: 
                cl-list.qty = 1. 
                tot-rm = tot-rm + 1. 
            END. 
            /*
            DO i = 1 TO length(res-line.bemerk): 
                IF SUBSTR(res-line.bemerk,i,1) = chr(10) THEN 
                cl-list.bemerk = cl-list.bemerk + " ". 
                ELSE cl-list.bemerk = cl-list.bemerk + SUBSTR(res-line.bemerk, i, 1). 
            END.
            */
            DO i = 1 TO length(res-line.bemerk): 
                IF SUBSTR(res-line.bemerk,i,1) = chr(10) THEN 
                      cl-list.bemerk = cl-list.bemerk + " ". 
                ELSE cl-list.bemerk = cl-list.bemerk + SUBSTR(TRIM(res-line.bemerk), i, 1).
            END.
            /*naufal add remarks 1000 char*/
            all-remark = res-line.bemerk.
            all-remark = REPLACE(all-remark,CHR(10)," ").
            all-remark = REPLACE(all-remark,CHR(13)," ").
            
            cl-list.bemerk01 = STRING(SUBSTRING(all-remark,1,255)).
            cl-list.bemerk02 = STRING(SUBSTRING(all-remark,256,255)).
            cl-list.bemerk03 = STRING(SUBSTRING(all-remark,511,255)).
            cl-list.bemerk04 = STRING(SUBSTRING(all-remark,766,255)).
            cl-list.bemerk05 = STRING(SUBSTRING(all-remark,1021,255)).
            cl-list.bemerk06 = STRING(SUBSTRING(all-remark,1276,255)).
            cl-list.bemerk07 = STRING(SUBSTRING(all-remark,1531,255)).
            cl-list.bemerk08 = STRING(SUBSTRING(all-remark,1786,255)).
            /*end naufal add remarks 1000 char*/
            
            cl-list.pax = STRING(cl-list.a,"9") + "/" + STRING(cl-list.c,"9"). 
            
            IF res-line.active-flag = 1 THEN 
            FOR EACH bill WHERE bill.zinr = res-line.zinr 
                AND bill.parent-nr = res-line.reslinnr AND bill.flag = 0 NO-LOCK: 
                cl-list.outstand = cl-list.outstand + bill.saldo. 
            END. 
            /*DODY 16/10/18 penambahan membership number dan type of membership */
            FIND FIRST mc-guest WHERE mc-guest.gastnr = gmember.gastnr NO-LOCK NO-ERROR.
            IF AVAILABLE mc-guest THEN 
            DO:
                cl-list.memberno = mc-guest.cardnum.  
                FIND FIRST mc-types WHERE mc-types.nr = mc-guest.nr NO-LOCK NO-ERROR.
                IF AVAILABLE mc-types THEN cl-list.membertype = mc-types.bezeich. 
            END.
 
            tot-a = tot-a + res-line.erwachs. 
            tot-c = tot-c + res-line.kind1 + res-line.kind2. 
            tot-co = tot-co + res-line.gratis. 
        END. 
    END. 
    ELSE IF disptype = 3 THEN 
    FOR EACH res-line WHERE res-line.resstatus = 8 
        AND res-line.abreise = curr-date 
        AND ((res-line.zinr GE froom AND res-line.zinr LE troom)
        OR (res-line.zinr GE froom)) NO-LOCK, 
        FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr NO-LOCK, 
        FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
        FIRST guest WHERE guest.gastnr = reservation.gastnr NO-LOCK, 
        FIRST gmember WHERE gmember.gastnr = res-line.gastnrmember NO-LOCK 
        BY reservation.name BY reservation.groupname 
        BY res-line.name BY res-line.zinr: 
 
        do-it = YES. 
        IF res-line.ankunft = res-line.abreise THEN 
        DO: 
            FIND FIRST history WHERE history.resnr = res-line.resnr 
                AND history.reslinnr = res-line.reslinnr 
                AND history.gesamtumsatz GT 0 NO-LOCK NO-ERROR. 
            IF NOT AVAILABLE history THEN do-it = NO. 
        END. 
 
        /* NEW: 01/12/2004 - aston bali : ignore the history validation */ 
        do-it = YES. 
        
        IF do-it THEN 
        DO: 
            /*FIND FIRST setup-list WHERE setup-list.nr = res-line.setup + 1.*/
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
            IF AVAILABLE guestseg THEN vip-flag = "VIP". 
            create cl-list. 
            ASSIGN 
                cl-list.nr        = nr 
                cl-list.groupname = reservation.groupname 
                /*cl-list.rmcat     = zimkateg.kurzbez + setup-list.char */
                cl-list.kurzbez   = zimkateg.kurzbez 
                cl-list.bezeich   = zimkateg.bezeich 
                cl-list.nat       = gmember.nation1 
                cl-list.resnr     = res-line.resnr 
                cl-list.vip       = vip-flag 
                cl-list.name      = res-line.name 
                cl-list.rmno      = res-line.zinr 
                cl-list.arrive    = STRING(res-line.ankunft, "99/99/99")
                cl-list.depart    = STRING(res-line.abreise, "99/99/99") 
                cl-list.a         = res-line.erwachs 
                cl-list.c         = res-line.kind1 + res-line.kind2 
                cl-list.co        = res-line.gratis 
                cl-list.argt      = res-line.arrangement 
                cl-list.flight    = SUBSTR(res-line.flight-nr, 12, 6) 
                cl-list.etd       = SUBSTR(res-line.flight-nr, 18, 5)
                cl-list.email-adr = gmember.email-adr
                cl-list.address   = gmember.adresse1 + ", " + gmember.adresse2 + ", " + gmember.adresse3             
                .

            FIND FIRST setup-list WHERE setup-list.nr EQ res-line.setup + 1 NO-LOCK NO-ERROR.
            IF AVAILABLE setup-list THEN cl-list.rmcat = zimkateg.kurzbez + setup-list.char .
            ELSE cl-list.rmcat = zimkateg.kurzbez.

            DO i = 1 TO NUM-ENTRIES(res-line.zimmer-wunsch,";") - 1:
              str = ENTRY(i, res-line.zimmer-wunsch, ";").
              IF SUBSTR(str,1,6) = "$CODE$" THEN 
              DO:
                cl-list.ratecode  = SUBSTR(str,7).
                LEAVE.
              END.
            END.

            IF guest.karteityp NE 0 THEN
                cl-list.company   = guest.name + ", " + guest.vorname1 
                + " " + guest.anrede1 + guest.anredefirma.
            IF gmember.telefon NE "" THEN
                cl-list.company   = cl-list.company + ";" + gmember.telefon.
 
            IF (cl-list.etd = "0000" OR cl-list.etd = "") AND res-line.abreisezeit NE 0 THEN 
            DO: 
                cl-list.etd = STRING(res-line.abreisezeit, "HH:MM"). 
                cl-list.etd = SUBSTR(cl-list.etd,1,2) + SUBSTR(cl-list.etd,4,2). 
            END. 
 
            IF cl-list.nat = "" THEN cl-list.nat = "?". 
            ELSE 
            DO: 
                FIND FIRST nation WHERE nation.kurzbez = cl-list.nat NO-LOCK NO-ERROR. 
                IF AVAILABLE nation THEN cl-list.nation = nation.bezeich. 
            END. 
            IF (res-line.erwachs + res-line.gratis) GT 0 THEN 
            DO: 
                cl-list.qty = 1. 
                tot-rm = tot-rm + 1. 
            END. 
            /*
            DO i = 1 TO length(res-line.bemerk): 
                IF SUBSTR(res-line.bemerk,i,1) = chr(10) THEN 
                cl-list.bemerk = cl-list.bemerk + " ". 
                ELSE cl-list.bemerk = cl-list.bemerk + SUBSTR(res-line.bemerk, i, 1). 
            END.
            */
            DO i = 1 TO length(res-line.bemerk): 
                IF SUBSTR(res-line.bemerk,i,1) = chr(10) THEN 
                      cl-list.bemerk = cl-list.bemerk + " ". 
                ELSE cl-list.bemerk = cl-list.bemerk + SUBSTR(TRIM(res-line.bemerk), i, 1).
            END.
            /*naufal add remarks 1000 char*/
            all-remark = res-line.bemerk.
            all-remark = REPLACE(all-remark,CHR(10)," ").
            all-remark = REPLACE(all-remark,CHR(13)," ").
            
            cl-list.bemerk01 = STRING(SUBSTRING(all-remark,1,255)).
            cl-list.bemerk02 = STRING(SUBSTRING(all-remark,256,255)).
            cl-list.bemerk03 = STRING(SUBSTRING(all-remark,511,255)).
            cl-list.bemerk04 = STRING(SUBSTRING(all-remark,766,255)).
            cl-list.bemerk05 = STRING(SUBSTRING(all-remark,1021,255)).
            cl-list.bemerk06 = STRING(SUBSTRING(all-remark,1276,255)).
            cl-list.bemerk07 = STRING(SUBSTRING(all-remark,1531,255)).
            cl-list.bemerk08 = STRING(SUBSTRING(all-remark,1786,255)).
            /*end naufal add remarks 1000 char*/
            
            cl-list.pax = STRING(cl-list.a,"9") + "/" + STRING(cl-list.c,"9"). 
            
            IF res-line.active-flag = 1 THEN 
            FOR EACH bill WHERE bill.zinr = res-line.zinr 
                AND bill.parent-nr = res-line.reslinnr AND bill.flag = 0 NO-LOCK: 
                cl-list.outstand = cl-list.outstand + bill.saldo. 
            END. 
            /*DODY 16/10/18 penambahan membership number dan type of membership */
            FIND FIRST mc-guest WHERE mc-guest.gastnr = gmember.gastnr NO-LOCK NO-ERROR.
            IF AVAILABLE mc-guest THEN 
            DO:
                cl-list.memberno = mc-guest.cardnum.  
                FIND FIRST mc-types WHERE mc-types.nr = mc-guest.nr NO-LOCK NO-ERROR.
                IF AVAILABLE mc-types THEN cl-list.membertype = mc-types.bezeich. 
            END.
 
            tot-a = tot-a + res-line.erwachs. 
            tot-c = tot-c + res-line.kind1 + res-line.kind2. 
            tot-co = tot-co + res-line.gratis. 
        END. 
    END. 
    ELSE IF disptype = 1 THEN 
    FOR EACH res-line WHERE res-line.resstatus = 8 
        AND res-line.abreise = curr-date 
        AND ((res-line.zinr GE froom AND res-line.zinr LE troom)
        OR (res-line.zinr GE froom)) NO-LOCK, 
        FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr NO-LOCK, 
        FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
        FIRST guest WHERE guest.gastnr = reservation.gastnr NO-LOCK, 
        FIRST gmember WHERE gmember.gastnr = res-line.gastnrmember NO-LOCK 
        BY reservation.groupname BY res-line.name BY res-line.zinr: 
 
        do-it = YES. 
        IF res-line.ankunft = res-line.abreise THEN 
        DO: 
            FIND FIRST history WHERE history.resnr = res-line.resnr 
                AND history.reslinnr = res-line.reslinnr 
                AND history.gesamtumsatz GT 0 NO-LOCK NO-ERROR. 
            IF NOT AVAILABLE history THEN do-it = NO. 
        END. 
 
        /* NEW: 01/12/2004 - aston bali : ignore the history validation */ 
        do-it = YES. 
 
        IF do-it THEN 
        DO: 
            /*FIND FIRST setup-list WHERE setup-list.nr = res-line.setup + 1. */
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
            IF AVAILABLE guestseg THEN vip-flag = "VIP". 
            create cl-list. 
            ASSIGN 
                cl-list.nr        = nr 
                cl-list.groupname = reservation.groupname 
                /*cl-list.rmcat     = zimkateg.kurzbez + setup-list.char */
                cl-list.kurzbez   = zimkateg.kurzbez 
                cl-list.bezeich   = zimkateg.bezeich 
                cl-list.nat       = gmember.nation1 
                cl-list.resnr     = res-line.resnr 
                cl-list.vip       = vip-flag 
                cl-list.name      = res-line.name 
                cl-list.rmno      = res-line.zinr 
                cl-list.arrive    = STRING(res-line.ankunft, "99/99/99")
                cl-list.depart    = STRING(res-line.abreise, "99/99/99")
                cl-list.a         = res-line.erwachs
                cl-list.c         = res-line.kind1 + res-line.kind2 
                cl-list.co        = res-line.gratis 
                cl-list.argt      = res-line.arrangement 
                cl-list.flight    = SUBSTR(res-line.flight-nr, 12, 6) 
                cl-list.etd       = SUBSTR(res-line.flight-nr, 18, 5)
                cl-list.email-adr = gmember.email-adr
                cl-list.address   = gmember.adresse1 + ", " + gmember.adresse2 + ", " + gmember.adresse3             
                .

            FIND FIRST setup-list WHERE setup-list.nr EQ res-line.setup + 1 NO-LOCK NO-ERROR.
            IF AVAILABLE setup-list THEN cl-list.rmcat = zimkateg.kurzbez + setup-list.char .
            ELSE cl-list.rmcat = zimkateg.kurzbez.

            DO i = 1 TO NUM-ENTRIES(res-line.zimmer-wunsch,";") - 1:
              str = ENTRY(i, res-line.zimmer-wunsch, ";").
              IF SUBSTR(str,1,6) = "$CODE$" THEN 
              DO:
                cl-list.ratecode  = SUBSTR(str,7).
                LEAVE.
              END.
            END.

            IF guest.karteityp NE 0 THEN
                cl-list.company   = guest.name + ", " + guest.vorname1 
                + " " + guest.anrede1 + guest.anredefirma.
            IF gmember.telefon NE "" THEN
                cl-list.company   = cl-list.company + ";" + gmember.telefon.
            
            IF (cl-list.etd = "0000" OR cl-list.etd = "") AND res-line.abreisezeit NE 0 THEN 
            DO: 
                cl-list.etd = STRING(res-line.abreisezeit, "HH:MM"). 
                cl-list.etd = SUBSTR(cl-list.etd,1,2) + SUBSTR(cl-list.etd,4,2). 
            END. 
            
            IF cl-list.nat = "" THEN cl-list.nat = "?". 
            ELSE 
            DO: 
                FIND FIRST nation WHERE nation.kurzbez = cl-list.nat NO-LOCK NO-ERROR. 
                IF AVAILABLE nation THEN cl-list.nation = nation.bezeich. 
            END. 
            IF (res-line.erwachs + res-line.gratis) GT 0 THEN 
            DO: 
                cl-list.qty = 1. 
                tot-rm = tot-rm + 1. 
            END. 
            /*
            DO i = 1 TO length(res-line.bemerk): 
                IF SUBSTR(res-line.bemerk,i,1) = chr(10) THEN 
                cl-list.bemerk = cl-list.bemerk + " ". 
                ELSE cl-list.bemerk = cl-list.bemerk + SUBSTR(res-line.bemerk, i, 1). 
            END.
            */
            DO i = 1 TO length(res-line.bemerk): 
                IF SUBSTR(res-line.bemerk,i,1) = chr(10) THEN 
                      cl-list.bemerk = cl-list.bemerk + " ". 
                ELSE cl-list.bemerk = cl-list.bemerk + SUBSTR(TRIM(res-line.bemerk), i, 1).
            END.
            /*naufal add remarks 1000 char*/
            all-remark = res-line.bemerk.
            all-remark = REPLACE(all-remark,CHR(10)," ").
            all-remark = REPLACE(all-remark,CHR(13)," ").
            
            cl-list.bemerk01 = STRING(SUBSTRING(all-remark,1,255)).
            cl-list.bemerk02 = STRING(SUBSTRING(all-remark,256,255)).
            cl-list.bemerk03 = STRING(SUBSTRING(all-remark,511,255)).
            cl-list.bemerk04 = STRING(SUBSTRING(all-remark,766,255)).
            cl-list.bemerk05 = STRING(SUBSTRING(all-remark,1021,255)).
            cl-list.bemerk06 = STRING(SUBSTRING(all-remark,1276,255)).
            cl-list.bemerk07 = STRING(SUBSTRING(all-remark,1531,255)).
            cl-list.bemerk08 = STRING(SUBSTRING(all-remark,1786,255)).
            /*end naufal add remarks 1000 char*/
            
            cl-list.pax = STRING(cl-list.a,"9") + "/" + STRING(cl-list.c,"9"). 
            
            IF res-line.active-flag = 1 THEN 
            FOR EACH bill WHERE bill.zinr = res-line.zinr 
                AND bill.parent-nr = res-line.reslinnr AND bill.flag = 0 NO-LOCK: 
                cl-list.outstand = cl-list.outstand + bill.saldo. 
            END. 
            /*DODY 16/10/18 penambahan membership number dan type of membership */
            FIND FIRST mc-guest WHERE mc-guest.gastnr = gmember.gastnr NO-LOCK NO-ERROR.
            IF AVAILABLE mc-guest THEN 
            DO:
                cl-list.memberno = mc-guest.cardnum.  
                FIND FIRST mc-types WHERE mc-types.nr = mc-guest.nr NO-LOCK NO-ERROR.
                IF AVAILABLE mc-types THEN cl-list.membertype = mc-types.bezeich. 
            END.
 
            tot-a = tot-a + res-line.erwachs. 
            tot-c = tot-c + res-line.kind1 + res-line.kind2. 
            tot-co = tot-co + res-line.gratis. 
        END. 
    END. 
 
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
    END. 
 
    IF (tot-a + tot-co) NE 0 THEN 
    FOR EACH s-list WHERE s-list.nat NE "": 
        FIND FIRST nation WHERE nation.kurzbez = s-list.nat NO-LOCK NO-ERROR. 
        IF AVAILABLE nation THEN s-list.nat = nation.bezeich. 
        ELSE s-list.nat = translateExtended ("UNKNOWN",lvCAREA,""). 
        s-list.proz = s-list.adult / (tot-a + tot-co) * 100. 
    END. 
END. 

PROCEDURE create-expected: /* OK */ 
DEFINE VARIABLE i AS INTEGER. 
DEFINE VARIABLE vip-flag AS CHAR. 
DEFINE VARIABLE nr AS INTEGER INITIAL 0. 
DEFINE VARIABLE str AS CHARACTER.
DEFINE buffer gmember FOR guest. 
 
  tot-rm = 0. 
  tot-a = 0. 
  tot-c = 0. 
  tot-co = 0. 
 
  FOR EACH s-list: 
   delete s-list. 
  END. 
 
  FOR EACH cl-list: 
    delete cl-list. 
  END. 
 
  FOR EACH str-list: 
    delete str-list. 
  END. 
 
  IF disptype = 1 THEN 
  FOR EACH res-line WHERE res-line.active-flag = 1 
    AND (res-line.resstatus = 6 OR resstatus = 13) 
    AND res-line.abreise = curr-date 
    AND ((res-line.zinr GE froom AND res-line.zinr LE troom)
        OR (res-line.zinr GE froom)) NO-LOCK, 
    FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr NO-LOCK, 
    FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
    FIRST guest WHERE guest.gastnr = reservation.gastnr NO-LOCK, 
    FIRST gmember WHERE gmember.gastnr = res-line.gastnrmember NO-LOCK 
    BY reservation.groupname BY res-line.name BY res-line.zinr: 
 
    /*FIND FIRST setup-list WHERE setup-list.nr = res-line.setup + 1. */
 
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
    IF AVAILABLE guestseg THEN vip-flag = "VIP". 
 
    create cl-list. 
    ASSIGN 
      cl-list.nr        = nr 
      cl-list.groupname = reservation.groupname 
      /*cl-list.rmcat     = zimkateg.kurzbez + setup-list.char */
      cl-list.kurzbez   = zimkateg.kurzbez 
      cl-list.bezeich   = zimkateg.bezeich 
      cl-list.nat       = gmember.nation1 
      cl-list.resnr     = res-line.resnr 
      cl-list.vip       = vip-flag 
      cl-list.name      = res-line.name 
      cl-list.rmno      = res-line.zinr 
      cl-list.arrive    = STRING(res-line.ankunft, "99/99/99")
      cl-list.depart    = STRING(res-line.abreise, "99/99/99") 
      cl-list.a         = res-line.erwachs 
      cl-list.c         = res-line.kind1 + res-line.kind2 
      cl-list.co        = res-line.gratis 
      cl-list.argt      = res-line.arrangement 
      cl-list.flight    = SUBSTR(res-line.flight-nr, 12, 6) 
      cl-list.etd       = SUBSTR(res-line.flight-nr, 18, 5)
      cl-list.email-adr = gmember.email-adr
      cl-list.address   = gmember.adresse1 + ", " + gmember.adresse2 + ", " + gmember.adresse3             
          .

    FIND FIRST setup-list WHERE setup-list.nr EQ res-line.setup + 1 NO-LOCK NO-ERROR.
    IF AVAILABLE setup-list THEN cl-list.rmcat = zimkateg.kurzbez + setup-list.char .
    ELSE cl-list.rmcat = zimkateg.kurzbez.

    DO i = 1 TO NUM-ENTRIES(res-line.zimmer-wunsch,";") - 1:
      str = ENTRY(i, res-line.zimmer-wunsch, ";").
      IF SUBSTR(str,1,6) = "$CODE$" THEN 
      DO:
        cl-list.ratecode  = SUBSTR(str,7).
        LEAVE.
      END.
    END.

    IF guest.karteityp NE 0 THEN
      cl-list.company   = guest.name + ", " + guest.vorname1 
        + " " + guest.anrede1 + guest.anredefirma.
    IF gmember.telefon NE "" THEN
      cl-list.company   = cl-list.company + ";" + gmember.telefon.
 
    IF (cl-list.etd = "0000" OR cl-list.etd = "") AND res-line.abreisezeit NE 0 THEN 
    DO: 
        cl-list.etd = STRING(res-line.abreisezeit, "HH:MM"). 
        cl-list.etd = SUBSTR(cl-list.etd,1,2) + SUBSTR(cl-list.etd,4,2). 
    END. 
 
    IF cl-list.nat = "" THEN cl-list.nat = "?". 
    ELSE 
    DO: 
        FIND FIRST nation WHERE nation.kurzbez = cl-list.nat NO-LOCK NO-ERROR. 
        IF AVAILABLE nation THEN cl-list.nation = nation.bezeich. 
    END. 
 
    IF res-line.resstatus = 6 THEN 
    DO: 
        tot-rm = tot-rm + 1. 
        cl-list.qty = 1. 
    END. 
    /*
    DO i = 1 TO length(res-line.bemerk): 
        IF SUBSTR(res-line.bemerk,i,1) = chr(10) THEN 
        cl-list.bemerk = cl-list.bemerk + " ". 
        ELSE cl-list.bemerk = cl-list.bemerk + SUBSTR(res-line.bemerk, i, 1). 
    END.
    */
    DO i = 1 TO length(res-line.bemerk): 
        IF SUBSTR(res-line.bemerk,i,1) = chr(10) THEN 
            cl-list.bemerk = cl-list.bemerk + " ". 
        ELSE cl-list.bemerk = cl-list.bemerk + SUBSTR(TRIM(res-line.bemerk), i, 1).
    END.
    /*naufal add remarks 1000 char*/
    all-remark = res-line.bemerk.
    all-remark = REPLACE(all-remark,CHR(10)," ").
    all-remark = REPLACE(all-remark,CHR(13)," ").
    
    cl-list.bemerk01 = STRING(SUBSTRING(all-remark,1,255)).
    cl-list.bemerk02 = STRING(SUBSTRING(all-remark,256,255)).
    cl-list.bemerk03 = STRING(SUBSTRING(all-remark,511,255)).
    cl-list.bemerk04 = STRING(SUBSTRING(all-remark,766,255)).
    cl-list.bemerk05 = STRING(SUBSTRING(all-remark,1021,255)).
    cl-list.bemerk06 = STRING(SUBSTRING(all-remark,1276,255)).
    cl-list.bemerk07 = STRING(SUBSTRING(all-remark,1531,255)).
    cl-list.bemerk08 = STRING(SUBSTRING(all-remark,1786,255)).
    /*end naufal add remarks 1000 char*/
 
    cl-list.pax = STRING(cl-list.a,"9") + "/" + STRING(cl-list.c,"9"). 
 
    IF res-line.active-flag = 1 THEN 
    FOR EACH bill WHERE bill.zinr = res-line.zinr 
      AND bill.parent-nr = res-line.reslinnr AND bill.flag = 0 NO-LOCK: 
      cl-list.outstand = cl-list.outstand + bill.saldo. 
    END. 
    /*DODY 16/10/18 penambahan membership number dan type of membership */
    FIND FIRST mc-guest WHERE mc-guest.gastnr = gmember.gastnr NO-LOCK NO-ERROR.
    IF AVAILABLE mc-guest THEN 
    DO:
        cl-list.memberno = mc-guest.cardnum.  
        FIND FIRST mc-types WHERE mc-types.nr = mc-guest.nr NO-LOCK NO-ERROR.
        IF AVAILABLE mc-types THEN cl-list.membertype = mc-types.bezeich. 
    END.
 
    tot-a = tot-a + res-line.erwachs. 
    tot-c = tot-c + res-line.kind1 + res-line.kind2. 
    tot-co = tot-co + res-line.gratis. 
  END. 
  ELSE IF disptype = 3 THEN 
  FOR EACH res-line WHERE res-line.active-flag = 1 
    AND (res-line.resstatus = 6 OR resstatus = 13) 
    AND res-line.abreise = curr-date 
    AND ((res-line.zinr GE froom AND res-line.zinr LE troom)
        OR (res-line.zinr GE froom)) NO-LOCK, 
    FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr NO-LOCK, 
    FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
    FIRST guest WHERE guest.gastnr = reservation.gastnr NO-LOCK, 
    FIRST gmember WHERE gmember.gastnr = res-line.gastnrmember NO-LOCK 
    BY reservation.name BY reservation.groupname 
    BY res-line.name BY res-line.zinr: 
 
    /*FIND FIRST setup-list WHERE setup-list.nr = res-line.setup + 1. */
 
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
    IF AVAILABLE guestseg THEN vip-flag = "VIP". 
 
    create cl-list. 
    ASSIGN 
      cl-list.nr        = nr 
      cl-list.groupname = reservation.groupname 
      /*cl-list.rmcat     = zimkateg.kurzbez + setup-list.char */
      cl-list.kurzbez   = zimkateg.kurzbez 
      cl-list.bezeich   = zimkateg.bezeich 
      cl-list.nat       = gmember.nation1 
      cl-list.resnr     = res-line.resnr 
      cl-list.vip       = vip-flag 
      cl-list.name      = res-line.name 
      cl-list.rmno      = res-line.zinr 
      cl-list.arrive    = STRING(res-line.ankunft, "99/99/99")
      cl-list.depart    = STRING(res-line.abreise, "99/99/99")
      cl-list.a         = res-line.erwachs 
      cl-list.c         = res-line.kind1 + res-line.kind2 
      cl-list.co        = res-line.gratis 
      cl-list.argt      = res-line.arrangement 
      cl-list.flight    = SUBSTR(res-line.flight-nr, 12, 6) 
      cl-list.etd       = SUBSTR(res-line.flight-nr, 18, 5)
      cl-list.email-adr = gmember.email-adr
      cl-list.address   = gmember.adresse1 + ", " + gmember.adresse2 + ", " + gmember.adresse3             
          .

    FIND FIRST setup-list WHERE setup-list.nr EQ res-line.setup + 1 NO-LOCK NO-ERROR.
    IF AVAILABLE setup-list THEN cl-list.rmcat = zimkateg.kurzbez + setup-list.char .
    ELSE cl-list.rmcat = zimkateg.kurzbez.

    DO i = 1 TO NUM-ENTRIES(res-line.zimmer-wunsch,";") - 1:
      str = ENTRY(i, res-line.zimmer-wunsch, ";").
      IF SUBSTR(str,1,6) = "$CODE$" THEN 
      DO:
        cl-list.ratecode  = SUBSTR(str,7).
        LEAVE.
      END.
    END.

    IF guest.karteityp NE 0 THEN
      cl-list.company   = guest.name + ", " + guest.vorname1 
        + " " + guest.anrede1 + guest.anredefirma.
    IF gmember.telefon NE "" THEN
      cl-list.company   = cl-list.company + ";" + gmember.telefon.
 
    IF (cl-list.etd = "0000" OR cl-list.etd = "") AND res-line.abreisezeit NE 0 THEN 
    DO: 
        cl-list.etd = STRING(res-line.abreisezeit, "HH:MM"). 
        cl-list.etd = SUBSTR(cl-list.etd,1,2) + SUBSTR(cl-list.etd,4,2). 
    END. 
 
    IF cl-list.nat = "" THEN cl-list.nat = "?". 
    ELSE 
    DO: 
        FIND FIRST nation WHERE nation.kurzbez = cl-list.nat NO-LOCK NO-ERROR. 
        IF AVAILABLE nation THEN cl-list.nation = nation.bezeich. 
    END. 
 
    IF res-line.resstatus = 6 THEN 
    DO: 
        tot-rm = tot-rm + 1. 
        cl-list.qty = 1. 
    END. 
    /*
    DO i = 1 TO length(res-line.bemerk): 
        IF SUBSTR(res-line.bemerk,i,1) = chr(10) THEN 
        cl-list.bemerk = cl-list.bemerk + " ". 
        ELSE cl-list.bemerk = cl-list.bemerk + SUBSTR(res-line.bemerk, i, 1). 
    END.
    */
    DO i = 1 TO length(res-line.bemerk): 
        IF SUBSTR(res-line.bemerk,i,1) = chr(10) THEN 
              cl-list.bemerk = cl-list.bemerk + " ". 
        ELSE cl-list.bemerk = cl-list.bemerk + SUBSTR(TRIM(res-line.bemerk), i, 1).
    END.
    /*naufal add remarks 1000 char*/
    all-remark = res-line.bemerk.
    all-remark = REPLACE(all-remark,CHR(10)," ").
    all-remark = REPLACE(all-remark,CHR(13)," ").
    
    cl-list.bemerk01 = STRING(SUBSTRING(all-remark,1,255)).
    cl-list.bemerk02 = STRING(SUBSTRING(all-remark,256,255)).
    cl-list.bemerk03 = STRING(SUBSTRING(all-remark,511,255)).
    cl-list.bemerk04 = STRING(SUBSTRING(all-remark,766,255)).
    cl-list.bemerk05 = STRING(SUBSTRING(all-remark,1021,255)).
    cl-list.bemerk06 = STRING(SUBSTRING(all-remark,1276,255)).
    cl-list.bemerk07 = STRING(SUBSTRING(all-remark,1531,255)).
    cl-list.bemerk08 = STRING(SUBSTRING(all-remark,1786,255)).
    /*end naufal add remarks 1000 char*/
 
    cl-list.pax = STRING(cl-list.a,"9") + "/" + STRING(cl-list.c,"9"). 
 
    IF res-line.active-flag = 1 THEN 
    FOR EACH bill WHERE bill.zinr = res-line.zinr 
      AND bill.parent-nr = res-line.reslinnr AND bill.flag = 0 NO-LOCK: 
      cl-list.outstand = cl-list.outstand + bill.saldo. 
    END. 
    /*DODY 16/10/18 penambahan membership number dan type of membership */
    FIND FIRST mc-guest WHERE mc-guest.gastnr = gmember.gastnr NO-LOCK NO-ERROR.
    IF AVAILABLE mc-guest THEN 
    DO:
        cl-list.memberno = mc-guest.cardnum.  
        FIND FIRST mc-types WHERE mc-types.nr = mc-guest.nr NO-LOCK NO-ERROR.
        IF AVAILABLE mc-types THEN cl-list.membertype = mc-types.bezeich. 
    END.
 
    tot-a = tot-a + res-line.erwachs. 
    tot-c = tot-c + res-line.kind1 + res-line.kind2. 
    tot-co = tot-co + res-line.gratis. 
  END. 
  ELSE IF disptype = 2 THEN 
  FOR EACH res-line WHERE res-line.active-flag = 1 
    AND (res-line.resstatus = 6 OR resstatus = 13) 
    AND res-line.abreise = curr-date 
    AND ((res-line.zinr GE froom AND res-line.zinr LE troom)
        OR (res-line.zinr GE froom)) NO-LOCK, 
    FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr NO-LOCK, 
    FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
    FIRST guest WHERE guest.gastnr = reservation.gastnr NO-LOCK, 
    FIRST gmember WHERE gmember.gastnr = res-line.gastnrmember NO-LOCK 
    BY res-line.zinr BY res-line.name: 
 
    /*FIND FIRST setup-list WHERE setup-list.nr = res-line.setup + 1. */
 
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
    IF AVAILABLE guestseg THEN vip-flag = "VIP". 
 
    create cl-list. 
    ASSIGN 
      cl-list.nr        = nr 
      cl-list.groupname = reservation.groupname 
      /*cl-list.rmcat     = zimkateg.kurzbez + setup-list.char */
      cl-list.kurzbez   = zimkateg.kurzbez 
      cl-list.bezeich   = zimkateg.bezeich 
      cl-list.nat       = gmember.nation1 
      cl-list.resnr     = res-line.resnr 
      cl-list.vip       = vip-flag 
      cl-list.name      = res-line.name 
      cl-list.rmno      = res-line.zinr 
      cl-list.arrive    = STRING(res-line.ankunft, "99/99/99")
      cl-list.depart    = STRING(res-line.abreise, "99/99/99")
      cl-list.a         = res-line.erwachs 
      cl-list.c         = res-line.kind1 + res-line.kind2 
      cl-list.co        = res-line.gratis 
      cl-list.argt      = res-line.arrangement 
      cl-list.flight    = SUBSTR(res-line.flight-nr, 12, 6) 
      cl-list.etd       = SUBSTR(res-line.flight-nr, 18, 5)
      cl-list.email-adr = gmember.email-adr
      cl-list.address   = gmember.adresse1 + ", " + gmember.adresse2 + ", " + gmember.adresse3             
      .

    FIND FIRST setup-list WHERE setup-list.nr EQ res-line.setup + 1 NO-LOCK NO-ERROR.
    IF AVAILABLE setup-list THEN cl-list.rmcat = zimkateg.kurzbez + setup-list.char .
    ELSE cl-list.rmcat = zimkateg.kurzbez.

    DO i = 1 TO NUM-ENTRIES(res-line.zimmer-wunsch,";") - 1:
      str = ENTRY(i, res-line.zimmer-wunsch, ";").
      IF SUBSTR(str,1,6) = "$CODE$" THEN 
      DO:
        cl-list.ratecode  = SUBSTR(str,7).
        LEAVE.
      END.
    END.

    IF guest.karteityp NE 0 THEN
      cl-list.company   = guest.name + ", " + guest.vorname1 
        + " " + guest.anrede1 + guest.anredefirma.
    IF gmember.telefon NE "" THEN
      cl-list.company   = cl-list.company + ";" + gmember.telefon.
 
    IF (cl-list.etd = "0000" OR cl-list.etd = "") AND res-line.abreisezeit NE 0 THEN 
    DO: 
        cl-list.etd = STRING(res-line.abreisezeit, "HH:MM"). 
        cl-list.etd = SUBSTR(cl-list.etd,1,2) + SUBSTR(cl-list.etd,4,2). 
    END. 
 
    IF cl-list.nat = "" THEN cl-list.nat = "?". 
    ELSE 
    DO: 
        FIND FIRST nation WHERE nation.kurzbez = cl-list.nat NO-LOCK NO-ERROR. 
        IF AVAILABLE nation THEN cl-list.nation = nation.bezeich. 
    END. 
 
    IF res-line.resstatus = 6 THEN 
    DO: 
        tot-rm = tot-rm + 1. 
        cl-list.qty = 1. 
    END. 
    /*
    DO i = 1 TO length(res-line.bemerk): 
        IF SUBSTR(res-line.bemerk,i,1) = chr(10) THEN 
        cl-list.bemerk = cl-list.bemerk + " ". 
        ELSE cl-list.bemerk = cl-list.bemerk + SUBSTR(res-line.bemerk, i, 1). 
    END.
    */
    DO i = 1 TO length(res-line.bemerk): 
        IF SUBSTR(res-line.bemerk,i,1) = chr(10) THEN 
            cl-list.bemerk = cl-list.bemerk + " ". 
        ELSE cl-list.bemerk = cl-list.bemerk + SUBSTR(TRIM(res-line.bemerk), i, 1).
    END.
    /*naufal add remarks 1000 char*/
    all-remark = res-line.bemerk.
    all-remark = REPLACE(all-remark,CHR(10)," ").
    all-remark = REPLACE(all-remark,CHR(13)," ").
    
    cl-list.bemerk01 = STRING(SUBSTRING(all-remark,1,255)).
    cl-list.bemerk02 = STRING(SUBSTRING(all-remark,256,255)).
    cl-list.bemerk03 = STRING(SUBSTRING(all-remark,511,255)).
    cl-list.bemerk04 = STRING(SUBSTRING(all-remark,766,255)).
    cl-list.bemerk05 = STRING(SUBSTRING(all-remark,1021,255)).
    cl-list.bemerk06 = STRING(SUBSTRING(all-remark,1276,255)).
    cl-list.bemerk07 = STRING(SUBSTRING(all-remark,1531,255)).
    cl-list.bemerk08 = STRING(SUBSTRING(all-remark,1786,255)).
    /*end naufal add remarks 1000 char*/
 
    cl-list.pax = STRING(cl-list.a,"9") + "/" + STRING(cl-list.c,"9"). 
 
    IF res-line.active-flag = 1 THEN 
    FOR EACH bill WHERE bill.zinr = res-line.zinr 
      AND bill.parent-nr = res-line.reslinnr AND bill.flag = 0 NO-LOCK: 
      cl-list.outstand = cl-list.outstand + bill.saldo. 
    END. 
    /*DODY 16/10/18 penambahan membership number dan type of membership */
    FIND FIRST mc-guest WHERE mc-guest.gastnr = gmember.gastnr NO-LOCK NO-ERROR.
    IF AVAILABLE mc-guest THEN 
    DO:
        cl-list.memberno = mc-guest.cardnum.  
        FIND FIRST mc-types WHERE mc-types.nr = mc-guest.nr NO-LOCK NO-ERROR.
        IF AVAILABLE mc-types THEN cl-list.membertype = mc-types.bezeich. 
    END.
 
    tot-a = tot-a + res-line.erwachs. 
    tot-c = tot-c + res-line.kind1 + res-line.kind2. 
    tot-co = tot-co + res-line.gratis. 
  END. 
 
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
  END. 
 
  IF (tot-a + tot-co) NE 0 THEN 
  FOR EACH s-list WHERE s-list.nat NE "": 
    FIND FIRST nation WHERE nation.kurzbez = s-list.nat NO-LOCK NO-ERROR. 
    IF AVAILABLE nation THEN s-list.nat = nation.bezeich. 
    ELSE s-list.nat = translateExtended ("UNKNOWN",lvCAREA,""). 
    s-list.proz = s-list.adult / (tot-a + tot-co) * 100. 
  END. 
END. 
