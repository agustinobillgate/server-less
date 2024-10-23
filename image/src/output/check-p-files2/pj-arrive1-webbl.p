
DEFINE TEMP-TABLE setup-list 
  FIELD nr      AS INTEGER 
  FIELD CHAR    AS CHAR FORMAT "x(1)". 

DEFINE TEMP-TABLE cl-list 
  FIELD ci-id      AS CHAR      /*MT 04/09/13 */
  FIELD stat-flag  AS CHAR FORMAT "x(1)" INITIAL " " 
  FIELD datum      AS DATE FORMAT "99/99/99"
  FIELD flag       AS INTEGER 
  FIELD nr         AS INTEGER FORMAT ">,>>>" 
  FIELD vip        AS CHAR FORMAT "x(3)" 
  FIELD gastnr     AS INTEGER INITIAL 0 
  FIELD resnr      AS INTEGER FORMAT ">>>>>>>" 
  FIELD name       AS CHAR FORMAT "x(24)" 
  FIELD groupname  AS CHAR FORMAT "x(24)" 
  FIELD zimmeranz  AS INTEGER 
  FIELD rmno       LIKE res-line.zinr /*MT 24/07/12 */
  FIELD qty        AS INTEGER FORMAT ">>9" 
  FIELD zipreis    AS CHAR    FORMAT "x(15)"
  FIELD arrival    AS CHAR    FORMAT "x(10)" 
  FIELD depart     AS CHAR    FORMAT "x(10)" 
  FIELD rmcat      AS CHAR    FORMAT "x(6)" 
  FIELD kurzbez    AS CHAR 
  FIELD bezeich    AS CHAR 
  FIELD a          AS INTEGER FORMAT "9" 
  FIELD c          AS INTEGER FORMAT "9" 
  FIELD co         AS INTEGER FORMAT ">>" 
  FIELD pax        AS CHAR FORMAT "x(6)" 
  FIELD nat        AS CHAR FORMAT "x(4)" 
  FIELD nation     AS CHAR 
  FIELD argt       AS CHAR FORMAT "x(7)" 
  FIELD company    AS CHAR FORMAT "x(30)" 
  FIELD flight     AS CHAR FORMAT "x(6)" 
  FIELD etd        AS CHAR FORMAT "99:99" 
  FIELD stay       AS INTEGER 
  FIELD segment    AS CHARACTER FORMAT "x(16)" /*sis 070814*/
  FIELD rate-code  AS CHARACTER FORMAT "x(7)" /*sis 070814*/
  FIELD eta        AS CHARACTER FORMAT "99:99" /*sis 070814*/
  FIELD Email      LIKE guest.email-adr /*Eko 051214*/
  FIELD bemerk     AS CHAR FORMAT "x(2000)"
  /*naufal Add Remarks 2000 Char*/                              
  FIELD bemerk01   AS CHAR      FORMAT "x(255)"
  FIELD bemerk02   AS CHAR      FORMAT "x(255)"
  FIELD bemerk03   AS CHAR      FORMAT "x(255)"
  FIELD bemerk04   AS CHAR      FORMAT "x(255)"
  FIELD bemerk05   AS CHAR      FORMAT "x(255)"
  FIELD bemerk06   AS CHAR      FORMAT "x(255)"
  FIELD bemerk07   AS CHAR      FORMAT "x(255)"
  FIELD bemerk08   AS CHAR      FORMAT "x(255)"
  /*end naufal*/
  FIELD spreq      AS CHAR
  FIELD memberno   AS CHAR      FORMAT "x(20)"
  FIELD resdate    AS CHAR      FORMAT "x(10)"  
  FIELD sob        AS CHAR      FORMAT "x(25)" 
  /*FD*/
  FIELD created-by AS CHARACTER
  FIELD ci-time    AS CHARACTER
  FIELD city       AS CHARACTER
  FIELD res-stat   AS INTEGER
  FIELD res-stat-str AS CHARACTER
  FIELD nation2    AS CHARACTER     /*Gerald EF94D9*/
  FIELD birthdate  AS DATE          /*Gerald 043D6C*/
  FIELD rsv-comment AS CHARACTER /*FDL August 28, 2023 => Req Kayu Manis Group*/    
  FIELD other-comment AS CHARACTER /*FDL August 28, 2023 => Req Kayu Manis Group*/
  FIELD g-comment   AS CHARACTER /*FDL August 28, 2023 => Req Kayu Manis Group*/
  FIELD zinr-bez    AS CHAR     /*Gerald 7E2311*/
  FIELD flag-guest  AS INTEGER  /*Gerald 7E2311*/
. 

DEFINE TEMP-TABLE t-cl-list
  FIELD ci-id      AS CHAR      /*MT 04/09/13 */
  FIELD stat-flag  AS CHAR FORMAT "x(1)" INITIAL " "
  FIELD datum      AS DATE FORMAT "99/99/99"
  FIELD flag       AS INTEGER
  FIELD nr         AS INTEGER FORMAT ">,>>>"
  FIELD vip        AS CHAR FORMAT "x(4)"
  FIELD gastnr     AS INTEGER INITIAL 0
  FIELD resnr      AS INTEGER FORMAT ">>>>>>>"
  FIELD name       AS CHAR FORMAT "x(24)"
  FIELD groupname  AS CHAR FORMAT "x(24)"
  FIELD zimmeranz  AS INTEGER
  FIELD rmno       LIKE res-line.zinr /*MT 24/07/12 */
  FIELD qty        AS INTEGER FORMAT ">>9"
  FIELD zipreis    AS CHAR    FORMAT "x(15)"
  FIELD arrival    AS CHAR    FORMAT "x(10)"
  FIELD depart     AS CHAR    FORMAT "x(10)"
  FIELD rmcat      AS CHAR    FORMAT "x(6)"
  FIELD kurzbez    AS CHAR
  FIELD bezeich    AS CHAR
  FIELD a          AS INTEGER FORMAT "9"
  FIELD c          AS INTEGER FORMAT "9"
  FIELD co         AS INTEGER FORMAT ">>"
  FIELD pax        AS CHAR FORMAT "x(6)"
  FIELD nat        AS CHAR FORMAT "x(4)"
  FIELD nation     AS CHAR
  FIELD argt       AS CHAR FORMAT "x(7)"
  FIELD company    AS CHAR FORMAT "x(30)"
  FIELD flight     AS CHAR FORMAT "x(6)"
  FIELD etd        AS CHAR FORMAT "99:99"
  FIELD stay       AS INTEGER
  FIELD segment    AS CHARACTER FORMAT "x(16)" /*sis 070814*/
  FIELD rate-code  AS CHARACTER FORMAT "x(7)" /*sis 070814*/
  FIELD eta        AS CHARACTER FORMAT "99:99" /*sis 070814*/
  FIELD Email      LIKE guest.email-adr
  FIELD bemerk     AS CHAR FORMAT "x(2000)"
  /*naufal Add Remarks 2000 Char*/                              
  FIELD bemerk01   AS CHAR      FORMAT "x(255)"
  FIELD bemerk02   AS CHAR      FORMAT "x(255)"
  FIELD bemerk03   AS CHAR      FORMAT "x(255)"
  FIELD bemerk04   AS CHAR      FORMAT "x(255)"
  FIELD bemerk05   AS CHAR      FORMAT "x(255)"
  FIELD bemerk06   AS CHAR      FORMAT "x(255)"
  FIELD bemerk07   AS CHAR      FORMAT "x(255)"
  FIELD bemerk08   AS CHAR      FORMAT "x(255)"
  /*end naufal*/
  FIELD spreq      AS CHAR
  FIELD memberno   AS CHAR      FORMAT "x(20)"   
  FIELD resdate    AS CHAR      FORMAT "x(10)"
  FIELD sob        AS CHAR      FORMAT "x(25)" 
  /*FD*/
  FIELD created-by AS CHARACTER
  FIELD ci-time    AS CHARACTER
  /*End FD*/
  FIELD phonenum        AS CHARACTER
  FIELD member-typ      AS CHARACTER
  FIELD repeat-guest    AS CHARACTER FORMAT "x(1)"
  FIELD night           AS INTEGER /*FD*/
  FIELD city       AS CHARACTER
  FIELD res-stat   AS INTEGER
  FIELD res-stat-str AS CHARACTER
  FIELD nation2    AS CHARACTER     /*Gerald EF94D9*/
  FIELD birthdate  AS DATE          /*Gerald 043D6C*/
  FIELD rsv-comment AS CHARACTER /*FDL August 28, 2023 => Req Kayu Manis Group*/    
  FIELD other-comment AS CHARACTER /*FDL August 28, 2023 => Req Kayu Manis Group*/
  FIELD g-comment   AS CHARACTER /*FDL August 28, 2023 => Req Kayu Manis Group*/
  FIELD zinr-bez    AS CHAR     /*Gerald 7E2311*/
  FIELD flag-guest  AS INTEGER  /*Gerald 7E2311*/
.

DEFINE TEMP-TABLE s-list 
  FIELD rmcat   AS CHAR FORMAT "x(6)" 
  FIELD bezeich AS CHAR FORMAT "x(24)" 
  FIELD nat     AS CHAR FORMAT "x(24)" 
  FIELD anz     AS INTEGER FORMAT ">>9" 
  FIELD adult   AS INTEGER FORMAT ">>9" 
  FIELD proz    AS DECIMAL FORMAT ">>9.99" 
  FIELD child   AS INTEGER FORMAT ">>9". 

DEFINE TEMP-TABLE t-list
  FIELD gastnr  AS INTEGER
  FIELD company AS CHAR
  FIELD counter AS CHAR
  FIELD int-counter AS INTEGER INITIAL 0
  FIELD anzahl      AS INTEGER INITIAL 0
  FIELD erwachs     AS INTEGER INITIAL 0
  FIELD kind        AS INTEGER INITIAL 0.

/* Not Used for web
DEFINE TEMP-TABLE zikat-list 
    FIELD selected AS LOGICAL INITIAL NO 
    FIELD zikatnr  AS INTEGER 
    FIELD kurzbez  AS CHAR 
    FIELD bezeich  AS CHAR FORMAT "x(32)"
.
*/
DEFINE INPUT PARAMETER pvILanguage      AS INTEGER NO-UNDO.
DEFINE INPUT PARAMETER from-date        AS DATE    NO-UNDO.
DEFINE INPUT PARAMETER to-date          AS DATE    NO-UNDO.
DEFINE INPUT PARAMETER ci-date          AS DATE    NO-UNDO.
DEFINE INPUT PARAMETER disptype         AS INTEGER NO-UNDO.
DEFINE INPUT PARAMETER incl-tentative   AS LOGICAL NO-UNDO.
DEFINE INPUT PARAMETER sorttype         AS INTEGER NO-UNDO.
DEFINE INPUT PARAMETER comment-type     AS INTEGER NO-UNDO.
DEFINE INPUT PARAMETER incl-accompany   AS LOGICAL NO-UNDO.
DEFINE INPUT PARAMETER split-rsv-print  AS LOGICAL. /*FDL August 28, 2023 => Req Kayu Manis Group*/
/*DEFINE INPUT PARAMETER TABLE FOR zikat-list.   /*FD Jan 06, 2022 => Req Prime Plaza*/*/
DEFINE INPUT PARAMETER total-flag       AS LOGICAL.

DEFINE OUTPUT PARAMETER tot-rm          AS INTEGER INITIAL 0. 
DEFINE OUTPUT PARAMETER tot-a           AS INTEGER INITIAL 0. 
DEFINE OUTPUT PARAMETER tot-c           AS INTEGER INITIAL 0. 
DEFINE OUTPUT PARAMETER tot-co          AS INTEGER INITIAL 0.
/*DEFINE OUTPUT PARAMETER TABLE FOR cl-list.*/
DEFINE OUTPUT PARAMETER TABLE FOR s-list.
DEFINE OUTPUT PARAMETER TABLE FOR t-cl-list.

{supertransBL.i} 
DEF VAR lvCAREA AS CHAR INITIAL "PJ-arrive".

DEFINE VARIABLE curr-date        AS DATE    NO-UNDO.
DEFINE VARIABLE vipnr1 AS INTEGER INITIAL 999999999. 
DEFINE VARIABLE vipnr2 AS INTEGER INITIAL 999999999. 
DEFINE VARIABLE vipnr3 AS INTEGER INITIAL 999999999. 
DEFINE VARIABLE vipnr4 AS INTEGER INITIAL 999999999. 
DEFINE VARIABLE vipnr5 AS INTEGER INITIAL 999999999. 
DEFINE VARIABLE vipnr6 AS INTEGER INITIAL 999999999. 
DEFINE VARIABLE vipnr7 AS INTEGER INITIAL 999999999. 
DEFINE VARIABLE vipnr8 AS INTEGER INITIAL 999999999. 
DEFINE VARIABLE vipnr9 AS INTEGER INITIAL 999999999. 


DEFINE VARIABLE OL-gastnr   AS INTEGER NO-UNDO.
DEFINE VARIABLE sms-gastnr  AS INTEGER NO-UNDO.
DEFINE VARIABLE WG-gastnr   AS INTEGER NO-UNDO.
DEFINE VARIABLE indi-gastnr AS INTEGER NO-UNDO.
DEFINE VARIABLE nr          AS INTEGER INITIAL 0.
DEFINE VARIABLE vip-flag    AS CHAR. 
DEFINE VARIABLE i           AS INTEGER.            
DEFINE VARIABLE dummy-flag  AS LOGICAL           NO-UNDO.
DEFINE VARIABLE do-it       AS LOGICAL           NO-UNDO. 
DEFINE VARIABLE last-gcf    AS INTEGER INITIAL 0 NO-UNDO. 
DEFINE VARIABLE tentres     AS INTEGER INITIAL 3 NO-UNDO.   

DEFINE VARIABLE all-remark AS LONGCHAR. /*naufal add remark 2000 char*/

DEFINE VARIABLE stat-list AS CHAR EXTENT 14 FORMAT "x(9)" NO-UNDO. 
stat-list[1]  = translateExtended ("Guaranteed",lvCAREA,""). 
stat-list[2]  = translateExtended ("6 PM",lvCAREA,""). 
stat-list[3]  = translateExtended ("Tentative",lvCAREA,""). 
stat-list[4]  = translateExtended ("WaitList",lvCAREA,""). 
stat-list[5]  = translateExtended ("Verbal Confirm",lvCAREA,""). 
stat-list[6]  = translateExtended ("Inhouse",lvCAREA,""). 
stat-list[7]  = "". 
stat-list[8]  = translateExtended ("Departed",lvCAREA,""). 
stat-list[9]  = translateExtended ("Cancelled",lvCAREA,""). 
stat-list[10] = translateExtended ("NoShow",lvCAREA,""). 
stat-list[11] = translateExtended ("ShareRes",lvCAREA,""). 
stat-list[12] = translateExtended ("AccGuest",lvCAREA,""). 
stat-list[13] = translateExtended ("RmSharer",lvCAREA,""). 
stat-list[14] = translateExtended ("AccGuest",lvCAREA,"").

DEFINE BUFFER gmember FOR guest.
DEFINE BUFFER gbuff   FOR guest.

/*************** MAIN LOGIC ***************/
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


RUN bed-setup. 
FIND FIRST htparam WHERE paramnr = 39 NO-LOCK.
OL-gastnr = htparam.finteger.
FIND FIRST htparam WHERE paramnr = 109 NO-LOCK.
WG-gastnr = htparam.finteger.
FIND FIRST htparam WHERE paramnr = 123 NO-LOCK.
indi-gastnr = htparam.finteger.
FIND FIRST htparam WHERE paramnr = 577 NO-LOCK.
sms-gastnr = htparam.finteger.


DO curr-date = from-date TO to-date:
  IF (curr-date GT ci-date) THEN RUN create-arrival(curr-date). 
  ELSE IF curr-date LT ci-date THEN RUN create-arrival1(curr-date). 
  ELSE IF curr-date = ci-date THEN 
  DO: 
    IF disptype = 1 THEN RUN create-arrival(curr-date). 
    ELSE IF disptype = 2 THEN RUN create-actual(curr-date). 
    ELSE IF disptype = 3 THEN RUN create-expected(curr-date). 
  END. 
END.
RUN create-summary.
RUN create-browse.
 
/*************** PROCEDURES ***************/
PROCEDURE create-arrival: 
 DEFINE INPUT PARAMETER curr-date AS DATE.
  IF incl-tentative THEN tentres = 12. 
  ASSIGN
      vip-flag = ""
      do-it = NO
      last-gcf = 0.
  
  nr = 0.
  IF sorttype = 1 THEN
  FOR EACH res-line WHERE res-line.active-flag LE 1 
    AND res-line.resstatus NE 12 AND res-line.resstatus NE tentres 
    AND res-line.ankunft = curr-date, 
    FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr NO-LOCK,
    /*FIRST zikat-list WHERE zikat-list.zikatnr = res-line.zikatnr
      AND zikat-list.SELECTED = YES NO-LOCK,*/
    FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
    FIRST sourccod WHERE Sourccod.source-code = reservation.resart NO-LOCK,
    FIRST guest WHERE guest.gastnr = reservation.gastnr NO-LOCK, 
    FIRST gmember WHERE gmember.gastnr = res-line.gastnrmember NO-LOCK 
    /*BY reservation.NAME*/ BY reservation.groupname 
    BY res-line.name BY res-line.zinr: 
    
    RUN add-cllist.
    IF NOT incl-accompany THEN
    DO:    
        FIND FIRST cl-list WHERE cl-list.rmno EQ res-line.zinr 
            AND cl-list.resnr EQ res-line.resnr
            AND DATE(cl-list.arrival) EQ res-line.ankunft 
            AND DEC(cl-list.zipreis) EQ 0 AND cl-list.co LT 1 EXCLUSIVE-LOCK NO-ERROR.
        IF AVAILABLE cl-list THEN
        DO:
            DELETE cl-list.
            RELEASE cl-list.
            nr = nr - 1.
        END.
    END.
  END. 
  ELSE IF sorttype = 2 THEN
  FOR EACH res-line WHERE res-line.active-flag LE 1 
    AND res-line.resstatus NE 12 AND res-line.resstatus NE tentres 
    AND res-line.ankunft = curr-date , 
    FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr NO-LOCK, 
    /*FIRST zikat-list WHERE zikat-list.zikatnr = res-line.zikatnr
      AND zikat-list.SELECTED = YES NO-LOCK,*/
    FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
    FIRST sourccod WHERE Sourccod.source-code = reservation.resart NO-LOCK,
    FIRST guest WHERE guest.gastnr = reservation.gastnr NO-LOCK, 
    FIRST gmember WHERE gmember.gastnr = res-line.gastnrmember NO-LOCK 
    BY res-line.zinr BY reservation.NAME BY reservation.groupname 
    BY res-line.name : 
 
    RUN add-cllist.
    IF NOT incl-accompany THEN
    DO:    
        FIND FIRST cl-list WHERE cl-list.rmno EQ res-line.zinr 
            AND cl-list.resnr EQ res-line.resnr 
            AND DATE(cl-list.arrival) EQ res-line.ankunft 
            AND DEC(cl-list.zipreis) EQ 0 AND cl-list.co LT 1 EXCLUSIVE-LOCK NO-ERROR.
        IF AVAILABLE cl-list THEN
        DO:
            DELETE cl-list.
            RELEASE cl-list.
            nr = nr - 1.
        END.
    END.
  END. 
  ELSE IF sorttype = 3 THEN
  FOR EACH res-line WHERE res-line.active-flag LE 1 
    AND res-line.resstatus NE 12 AND res-line.resstatus NE tentres 
    AND res-line.ankunft = curr-date , 
    FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr NO-LOCK, 
    /*FIRST zikat-list WHERE zikat-list.zikatnr = res-line.zikatnr
      AND zikat-list.SELECTED = YES NO-LOCK,*/
    FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
    FIRST sourccod WHERE Sourccod.source-code = reservation.resart NO-LOCK,
    FIRST guest WHERE guest.gastnr = reservation.gastnr NO-LOCK, 
    FIRST gmember WHERE gmember.gastnr = res-line.gastnrmember NO-LOCK 
    BY reservation.resdat BY res-line.zinr  /* BY reservation.groupname 
    BY res-line.name*/ : 
 
    RUN add-cllist.
    IF NOT incl-accompany THEN
    DO:    
        FIND FIRST cl-list WHERE cl-list.rmno EQ res-line.zinr 
            AND cl-list.resnr EQ res-line.resnr 
            AND DATE(cl-list.arrival) EQ res-line.ankunft 
            AND DEC(cl-list.zipreis) EQ 0 AND cl-list.co LT 1 EXCLUSIVE-LOCK NO-ERROR.
        IF AVAILABLE cl-list THEN
        DO:
            DELETE cl-list.
            RELEASE cl-list.
            nr = nr - 1.
        END.
    END.
  END.  
  ELSE IF sorttype = 4 THEN /* add by gerald tiket 393740 */
  FOR EACH res-line WHERE res-line.active-flag LE 1 
    AND res-line.resstatus NE 12 AND res-line.resstatus NE tentres 
    AND res-line.ankunft = curr-date, 
    FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr NO-LOCK, 
    /*FIRST zikat-list WHERE zikat-list.zikatnr = res-line.zikatnr
      AND zikat-list.SELECTED = YES NO-LOCK,*/
    FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
    FIRST sourccod WHERE Sourccod.source-code = reservation.resart NO-LOCK,
    FIRST guest WHERE guest.gastnr = reservation.gastnr NO-LOCK, 
    FIRST gmember WHERE gmember.gastnr = res-line.gastnrmember NO-LOCK 
    BY res-line.arrangement BY reservation.NAME BY reservation.groupname 
    BY res-line.name : 

    RUN add-cllist.
    IF NOT incl-accompany THEN
    DO:    
        FIND FIRST cl-list WHERE cl-list.rmno EQ res-line.zinr 
            AND cl-list.resnr EQ res-line.resnr 
            AND DATE(cl-list.arrival) EQ res-line.ankunft 
            AND DEC(cl-list.zipreis) EQ 0 AND cl-list.co LT 1 EXCLUSIVE-LOCK NO-ERROR.
        IF AVAILABLE cl-list THEN
        DO:
            DELETE cl-list.
            RELEASE cl-list.
            nr = nr - 1.
        END.
    END.
  END.  
  ELSE
  FOR EACH res-line WHERE res-line.active-flag LE 1 
    AND res-line.resstatus NE 12 AND res-line.resstatus NE tentres 
    AND res-line.ankunft = curr-date, 
    FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr NO-LOCK, 
    /*FIRST zikat-list WHERE zikat-list.zikatnr = res-line.zikatnr
      AND zikat-list.SELECTED = YES NO-LOCK,*/
    FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
    FIRST sourccod WHERE Sourccod.source-code = reservation.resart NO-LOCK,
    FIRST guest WHERE guest.gastnr = reservation.gastnr NO-LOCK, 
    FIRST gmember WHERE gmember.gastnr = res-line.gastnrmember NO-LOCK 
    BY res-line.resstatus BY reservation.NAME BY reservation.groupname 
    BY res-line.name : 

    RUN add-cllist.
    IF NOT incl-accompany THEN
    DO:    
        FIND FIRST cl-list WHERE cl-list.rmno EQ res-line.zinr 
            AND cl-list.resnr EQ res-line.resnr 
            AND DATE(cl-list.arrival) EQ res-line.ankunft 
            AND DEC(cl-list.zipreis) EQ 0 AND cl-list.co LT 1 EXCLUSIVE-LOCK NO-ERROR.
        IF AVAILABLE cl-list THEN
        DO:
            DELETE cl-list.
            RELEASE cl-list.
            nr = nr - 1.
        END.
    END.
  END. 
END. 

PROCEDURE add-cllist:
    DEFINE VARIABLE loop-i      AS INTEGER.
    DEFINE VARIABLE str-rsv     AS CHARACTER.
    DEFINE VARIABLE contcode    AS CHARACTER.
    DEFINE VARIABLE segmentcode AS CHARACTER.

    DEFINE BUFFER gbuff         FOR guest.
    DEFINE BUFFER rbuff         FOR reservation.

    dummy-flag  = NO.
    IF res-line.gastnr = Ol-gastnr OR res-line.gastnr = WG-gastnr
        OR res-line.gastnr = indi-gastnr OR res-line.gastnr = sms-gastnr
        THEN dummy-flag = YES.
    FIND FIRST setup-list WHERE setup-list.nr = res-line.setup + 1. 
 
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

    FIND FIRST segment WHERE segment.segmentcode = reservation.segmentcode NO-LOCK NO-ERROR.
    IF AVAILABLE segment THEN segmentcode = segment.bezeich.


     DO loop-i = 1 TO NUM-ENTRIES(res-line.zimmer-wunsch,";") - 1:
        str-rsv = ENTRY(loop-i, res-line.zimmer-wunsch, ";").
        IF SUBSTR(str-rsv,1,6)   = "$CODE$"   THEN contcode     = SUBSTR(str-rsv,7).
     END.

    CREATE cl-list. /*2*/
    ASSIGN 
      cl-list.nr        = nr 
      cl-list.datum     = res-line.ankunft
      cl-list.groupname = reservation.groupname 
      cl-list.rmcat     = zimkateg.kurzbez + setup-list.char 
      cl-list.kurzbez   = zimkateg.kurzbez 
      cl-list.bezeich   = zimkateg.bezeich
      /*cl-list.rmcat     = zikat-list.kurzbez + setup-list.char 
      cl-list.kurzbez   = zikat-list.kurzbez 
      cl-list.bezeich   = zikat-list.bezeich*/ 
      cl-list.nat       = gmember.nation1 
      cl-list.gastnr    = res-line.gastnr 
      cl-list.resnr     = res-line.resnr
      cl-list.vip       = vip-flag 
      cl-list.name      = res-line.name 
      cl-list.zipreis   = STRING(res-line.zipreis, " >>>,>>>,>>9.99")
      cl-list.zimmeranz = res-line.zimmeranz 
      cl-list.rmno      = res-line.zinr 
      cl-list.arrival   = STRING(res-line.ankunft, "99/99/99")
      cl-list.depart    = STRING(res-line.abreise, "99/99/99")
      cl-list.a         = res-line.erwachs 
      cl-list.c         = res-line.kind1 + res-line.kind2 
      cl-list.co        = res-line.gratis 
      cl-list.argt      = res-line.arrangement 
      cl-list.flight    = SUBSTR(res-line.flight-nr, 1, 6) 
      cl-list.eta       = SUBSTR(res-line.flight-nr, 7, 4) /*sis 070814*/
      cl-list.etd       = SUBSTR(res-line.flight-nr, 18, 4) /*sis 070814*/ 
      cl-list.rate-code = contcode  /*sis 070814*/
      cl-list.segment   = segmentcode   /*sis 070814*/
      cl-list.stay      = gmember.aufenthalte
      cl-list.Email    = gmember.email-adr /*guest.email-adr*/
      cl-list.sob       = sourccod.bezeich
      cl-list.ci-id     = res-line.cancelled-id    /*MT 04/09/13 */
      cl-list.ci-time   = STRING(res-line.ankzeit, "HH:MM")
      cl-list.city      = gmember.wohnort
      cl-list.res-stat  = res-line.resstatus
      cl-list.res-stat-str  = STRING(cl-list.res-stat) + " - " + stat-list[res-line.resstatus]
      cl-list.birthdate = gmember.geburtdatum1
    .

    FIND FIRST zimmer WHERE zimmer.zinr = res-line.zinr NO-LOCK NO-ERROR.
    IF AVAILABLE zimmer THEN
    DO:
      ASSIGN cl-list.zinr-bez = zimmer.bezeich.
    END.

    IF res-line.resstatus NE 11 AND res-line.resstatus NE 13 THEN ASSIGN cl-list.flag-guest = 1.
    ELSE ASSIGN cl-list.flag-guest = 2.

    IF guest.karteityp NE 0 THEN
      cl-list.company   = guest.name + ", " + guest.vorname1 
        + " " + guest.anrede1 + guest.anredefirma.
    IF gmember.telefon NE "" THEN
      cl-list.company   = cl-list.company + ";" + gmember.telefon.
 
    IF cl-list.nat = "" THEN cl-list.nat = "?". 
    ELSE 
    DO: 
      FIND FIRST nation WHERE nation.kurzbez = cl-list.nat NO-LOCK NO-ERROR. 
      IF AVAILABLE nation THEN cl-list.nation = nation.bezeich. 
    END.

    FIND FIRST nation WHERE nation.kurzbez = gmember.nation2 AND nation.natcode GT 0 NO-LOCK NO-ERROR.
    IF AVAILABLE nation THEN
    DO:
        cl-list.nation2 = nation.bezeich.
    END.

    IF res-line.resstatus NE 11 AND res-line.resstatus NE 13 THEN 
    DO: 
      cl-list.qty = res-line.zimmeranz. 
      tot-rm = tot-rm + res-line.zimmeranz. 
    END. 
    
    /*DODY 27/02/18 penambahan membership number*/
    FIND FIRST mc-guest WHERE mc-guest.gastnr = gmember.gastnr NO-LOCK NO-ERROR.
    IF AVAILABLE mc-guest THEN
    DO:
        cl-list.memberno = mc-guest.cardnum.
        FIND FIRST mc-types WHERE mc-types.nr = mc-guest.nr NO-LOCK NO-ERROR. /*FD*/
        IF AVAILABLE mc-types THEN
        DO:
           cl-list.memberno = mc-guest.cardnum + ";" + mc-types.bezeich.
        END.
    END.

    cl-list.resdate = STRING(reservation.resdat, "99/99/99").
    cl-list.created-by = reservation.useridanlage.

    IF comment-type = 0 THEN
    DO:
        IF NOT split-rsv-print THEN /*ORIG*/
        DO:
            DO i = 1 TO length(res-line.bemerk): 
              IF SUBSTR(res-line.bemerk,i,1) = chr(10) THEN 
                cl-list.bemerk = cl-list.bemerk + " ". 
              ELSE cl-list.bemerk = cl-list.bemerk + 
                  SUBSTR(TRIM(res-line.bemerk), i, 1). 
            END.
            /*naufal add remark 2000 char*/
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
            /*end naufal*/
        END.        
        ELSE
        DO:
            DO i = 1 TO LENGTH(res-line.bemerk): 
                cl-list.bemerk = cl-list.bemerk + SUBSTR(TRIM(res-line.bemerk), i, 1). 
            END.

            cl-list.rsv-comment = reservation.bemerk. /*FDL Feb 12, 2024 => Ticket 1BB9DD | FCB614*/
            /* FDL Comment
            FIND FIRST rbuff WHERE rbuff.gastnr = reservation.gastnr NO-LOCK NO-ERROR.
            IF AVAILABLE rbuff THEN
            DO:
                cl-list.rsv-comment = reservation.bemerk.                
            END.
            */
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
    END.
    ELSE
    DO:
        IF dummy-flag OR guest.bemerk = "" THEN
        DO:
            FIND FIRST gbuff WHERE gbuff.gastnr = res-line.gastnrmember USE-INDEX
                gastnr_index NO-LOCK NO-ERROR.
            IF AVAILABLE gbuff THEN
            DO:
                DO i = 1 TO length(gbuff.bemerk): 
                  IF SUBSTR(gbuff.bemerk,i,1) = chr(10) THEN 
                      cl-list.bemerk = cl-list.bemerk + " ". 
                  ELSE cl-list.bemerk = cl-list.bemerk + 
                      SUBSTR(gbuff.bemerk, i, 1). 
                END.
            END.
        END.
        ELSE
            DO i = 1 TO length(guest.bemerk): 
              IF SUBSTR(guest.bemerk,i,1) = chr(10) THEN 
                  cl-list.bemerk = cl-list.bemerk + " ". 
              ELSE cl-list.bemerk = cl-list.bemerk + 
                  SUBSTR(guest.bemerk, i, 1). 
            END.
    END.
 
    IF cl-list.rmno = "" AND cl-list.qty GT 1 THEN 
      cl-list.rmno = STRING(cl-list.qty, ">>>9"). 
 
    IF res-line.resstatus = 3 THEN 
    DO: 
      IF cl-list.qty LE 9 THEN cl-list.rmno = "  T" + STRING(cl-list.qty,"9"). 
      ELSE IF cl-list.qty LE 99 THEN cl-list.rmno = 
         " T" + STRING(cl-list.qty,"99"). 
      ELSE IF cl-list.qty LE 999 THEN cl-list.rmno = 
         "T" + STRING(cl-list.qty,"999"). 
    END. 
    ELSE IF res-line.resstatus = 4 THEN 
    DO: 
      IF cl-list.qty LE 9 THEN cl-list.rmno = "  W" + STRING(cl-list.qty,"9"). 
      ELSE IF cl-list.qty LE 99 THEN cl-list.rmno = 
         " W" + STRING(cl-list.qty,"99"). 
      ELSE IF cl-list.qty LE 999 THEN cl-list.rmno = 
         "W" + STRING(cl-list.qty,"999"). 
    END. 
 
    cl-list.pax = STRING(cl-list.a,"9") + "/" + STRING(cl-list.c,"9"). 
    
    /*ITA 040617 --> for special request*/
    FIND FIRST reslin-queasy WHERE reslin-queasy.KEY = "specialRequest"
        AND reslin-queasy.resnr = res-line.resnr 
        AND reslin-queasy.reslinnr = res-line.reslinnr NO-LOCK NO-ERROR.
    IF AVAILABLE reslin-queasy THEN
        ASSIGN cl-list.spreq = reslin-queasy.char3.
    /*end*/
 
    tot-a = tot-a + res-line.erwachs * res-line.zimmeranz. 
    tot-c = tot-c + (res-line.kind1 + res-line.kind2) * res-line.zimmeranz. 
    tot-co = tot-co + res-line.gratis * res-line.zimmeranz. 
END.
 
PROCEDURE create-actual: 
  DEFINE INPUT PARAMETER curr-date AS DATE .
  ASSIGN
      vip-flag = ""
      do-it = NO
      last-gcf = 0.

  nr = 0.
  IF sorttype = 1 THEN
  FOR EACH res-line WHERE res-line.active-flag = 1 
    AND (res-line.resstatus = 6 OR res-line.resstatus = 13) 
    AND res-line.ankunft = curr-date, 
    FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr NO-LOCK, 
    /*FIRST zikat-list WHERE zikat-list.zikatnr = res-line.zikatnr
      AND zikat-list.SELECTED = YES NO-LOCK,*/
    FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK,
    FIRST sourccod WHERE Sourccod.source-code = reservation.resart NO-LOCK,
    FIRST guest WHERE guest.gastnr = reservation.gastnr NO-LOCK, 
    FIRST gmember WHERE gmember.gastnr = res-line.gastnrmember NO-LOCK 
    BY reservation.NAME BY reservation.groupname 
    BY res-line.name BY res-line.zinr: 
    RUN add-cllist.
    IF NOT incl-accompany THEN
    DO:    
        FIND FIRST cl-list WHERE cl-list.rmno EQ res-line.zinr 
            AND cl-list.resnr EQ res-line.resnr
            AND DATE(cl-list.arrival) EQ res-line.ankunft 
            AND DEC(cl-list.zipreis) EQ 0 AND cl-list.co LT 1 EXCLUSIVE-LOCK NO-ERROR.
        IF AVAILABLE cl-list THEN
        DO:
            DELETE cl-list.
            RELEASE cl-list.
            nr = nr - 1.
        END.
    END.
  END. 
  ELSE IF sorttype = 2 THEN
  FOR EACH res-line WHERE res-line.active-flag = 1 
    AND (res-line.resstatus = 6 OR res-line.resstatus = 13) 
    AND res-line.ankunft = curr-date, 
    FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr NO-LOCK, 
    /*FIRST zikat-list WHERE zikat-list.zikatnr = res-line.zikatnr
      AND zikat-list.SELECTED = YES NO-LOCK,*/
    FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
    FIRST sourccod WHERE Sourccod.source-code = reservation.resart NO-LOCK,
    FIRST guest WHERE guest.gastnr = reservation.gastnr NO-LOCK, 
    FIRST gmember WHERE gmember.gastnr = res-line.gastnrmember NO-LOCK 
    BY res-line.zinr BY reservation.NAME BY reservation.groupname 
    BY res-line.name : 
    RUN add-cllist.
    IF NOT incl-accompany THEN
    DO:    
        FIND FIRST cl-list WHERE cl-list.rmno EQ res-line.zinr 
            AND cl-list.resnr EQ res-line.resnr
            AND DATE(cl-list.arrival) EQ res-line.ankunft 
            AND DEC(cl-list.zipreis) EQ 0 AND cl-list.co LT 1 EXCLUSIVE-LOCK NO-ERROR.
        IF AVAILABLE cl-list THEN
        DO:
            DELETE cl-list.
            RELEASE cl-list.
            nr = nr - 1.
        END.
    END.
  END.
  ELSE IF sorttype = 3 THEN
  FOR EACH res-line WHERE res-line.active-flag = 1 
    AND (res-line.resstatus = 6 OR res-line.resstatus = 13) 
    AND res-line.ankunft = curr-date, 
    FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr NO-LOCK, 
    FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
    /*FIRST zikat-list WHERE zikat-list.zikatnr = res-line.zikatnr
      AND zikat-list.SELECTED = YES NO-LOCK,*/
    FIRST sourccod WHERE Sourccod.source-code = reservation.resart NO-LOCK,
    FIRST guest WHERE guest.gastnr = reservation.gastnr NO-LOCK, 
    FIRST gmember WHERE gmember.gastnr = res-line.gastnrmember NO-LOCK 
    BY reservation.resdat BY res-line.zinr: 
    RUN add-cllist.
    IF NOT incl-accompany THEN
    DO:    
        FIND FIRST cl-list WHERE cl-list.rmno EQ res-line.zinr 
            AND cl-list.resnr EQ res-line.resnr
            AND DATE(cl-list.arrival) EQ res-line.ankunft 
            AND DEC(cl-list.zipreis) EQ 0 AND cl-list.co LT 1 EXCLUSIVE-LOCK NO-ERROR.
        IF AVAILABLE cl-list THEN
        DO:
            DELETE cl-list.
            RELEASE cl-list.
            nr = nr - 1.
        END.
    END.
  END. 
  ELSE IF sorttype = 4 THEN
  FOR EACH res-line WHERE res-line.active-flag = 1 
    AND (res-line.resstatus = 6 OR res-line.resstatus = 13) 
    AND res-line.ankunft = curr-date, 
    FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr NO-LOCK, 
    FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
    /*FIRST zikat-list WHERE zikat-list.zikatnr = res-line.zikatnr
      AND zikat-list.SELECTED = YES NO-LOCK,*/
    FIRST sourccod WHERE Sourccod.source-code = reservation.resart NO-LOCK,
    FIRST guest WHERE guest.gastnr = reservation.gastnr NO-LOCK, 
    FIRST gmember WHERE gmember.gastnr = res-line.gastnrmember NO-LOCK 
    BY res-line.arrangement BY reservation.NAME BY reservation.groupname 
    BY res-line.name: 
    RUN add-cllist.
    IF NOT incl-accompany THEN
    DO:    
        FIND FIRST cl-list WHERE cl-list.rmno EQ res-line.zinr 
            AND cl-list.resnr EQ res-line.resnr
            AND DATE(cl-list.arrival) EQ res-line.ankunft 
            AND DEC(cl-list.zipreis) EQ 0 AND cl-list.co LT 1 EXCLUSIVE-LOCK NO-ERROR.
        IF AVAILABLE cl-list THEN
        DO:
            DELETE cl-list.
            RELEASE cl-list.
            nr = nr - 1.
        END.
    END.
  END. 
  ELSE
  FOR EACH res-line WHERE res-line.active-flag = 1 
    AND (res-line.resstatus = 6 OR res-line.resstatus = 13) 
    AND res-line.ankunft = curr-date, 
    FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr NO-LOCK, 
    FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
    /*FIRST zikat-list WHERE zikat-list.zikatnr = res-line.zikatnr
      AND zikat-list.SELECTED = YES NO-LOCK,*/
    FIRST sourccod WHERE Sourccod.source-code = reservation.resart NO-LOCK,
    FIRST guest WHERE guest.gastnr = reservation.gastnr NO-LOCK, 
    FIRST gmember WHERE gmember.gastnr = res-line.gastnrmember NO-LOCK 
    BY res-line.resstatus BY reservation.NAME BY reservation.groupname 
    BY res-line.name: 
    RUN add-cllist.
    IF NOT incl-accompany THEN
    DO:    
        FIND FIRST cl-list WHERE cl-list.rmno EQ res-line.zinr 
            AND cl-list.resnr EQ res-line.resnr
            AND DATE(cl-list.arrival) EQ res-line.ankunft 
            AND DEC(cl-list.zipreis) EQ 0 AND cl-list.co LT 1 EXCLUSIVE-LOCK NO-ERROR.
        IF AVAILABLE cl-list THEN
        DO:
            DELETE cl-list.
            RELEASE cl-list.
            nr = nr - 1.
        END.
    END.
  END. 
END. 

PROCEDURE create-expected: 
  DEFINE INPUT PARAMETER curr-date AS DATE.
  tentres = 3.
  IF incl-tentative THEN tentres = 12. 
  ASSIGN
      vip-flag = ""
      do-it = NO
      last-gcf = 0.
 
  nr = 0.
  IF sorttype = 1 THEN
  FOR EACH res-line WHERE res-line.active-flag EQ 0 
    AND res-line.resstatus NE tentres 
    AND res-line.ankunft = curr-date, 
    FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr NO-LOCK, 
    /*FIRST zikat-list WHERE zikat-list.zikatnr = res-line.zikatnr
      AND zikat-list.SELECTED = YES NO-LOCK,*/
    FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
    FIRST sourccod WHERE Sourccod.source-code = reservation.resart NO-LOCK,
    FIRST guest WHERE guest.gastnr = reservation.gastnr NO-LOCK, 
    FIRST gmember WHERE gmember.gastnr = res-line.gastnrmember NO-LOCK 
    BY reservation.NAME BY reservation.groupname 
    BY res-line.name BY res-line.zinr: 
 
    RUN add-cllist.
    IF NOT incl-accompany THEN
    DO:    
        FIND FIRST cl-list WHERE cl-list.rmno EQ res-line.zinr 
            AND cl-list.resnr EQ res-line.resnr
            AND DATE(cl-list.arrival) EQ res-line.ankunft 
            AND DEC(cl-list.zipreis) EQ 0 AND cl-list.co LT 1 EXCLUSIVE-LOCK NO-ERROR.
        IF AVAILABLE cl-list THEN
        DO:
            DELETE cl-list.
            RELEASE cl-list.
            nr = nr - 1.
        END.
    END.
  END. 
  ELSE IF sorttype = 2 THEN
  FOR EACH res-line WHERE res-line.active-flag EQ 0 
    AND res-line.resstatus NE tentres 
    AND res-line.ankunft = curr-date, 
    FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr NO-LOCK, 
    /*FIRST zikat-list WHERE zikat-list.zikatnr = res-line.zikatnr
      AND zikat-list.SELECTED = YES NO-LOCK,*/
    FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
    FIRST sourccod WHERE Sourccod.source-code = reservation.resart NO-LOCK,
    FIRST guest WHERE guest.gastnr = reservation.gastnr NO-LOCK, 
    FIRST gmember WHERE gmember.gastnr = res-line.gastnrmember NO-LOCK 
    BY res-line.zinr BY reservation.NAME BY reservation.groupname 
    BY res-line.name: 
    RUN add-cllist.
    IF NOT incl-accompany THEN
    DO:    
        FIND FIRST cl-list WHERE cl-list.rmno EQ res-line.zinr 
            AND cl-list.resnr EQ res-line.resnr
            AND DATE(cl-list.arrival) EQ res-line.ankunft 
            AND DEC(cl-list.zipreis) EQ 0 AND cl-list.co LT 1 EXCLUSIVE-LOCK NO-ERROR.
        IF AVAILABLE cl-list THEN
        DO:
            DELETE cl-list.
            RELEASE cl-list.
            nr = nr - 1.
        END.
    END.
  END.
  ELSE IF sorttype = 3 THEN
  FOR EACH res-line WHERE res-line.active-flag EQ 0 
    AND res-line.resstatus NE tentres 
    AND res-line.ankunft = curr-date, 
    FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr NO-LOCK, 
    /*FIRST zikat-list WHERE zikat-list.zikatnr = res-line.zikatnr
      AND zikat-list.SELECTED = YES NO-LOCK,*/
    FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
    FIRST sourccod WHERE Sourccod.source-code = reservation.resart NO-LOCK,
    FIRST guest WHERE guest.gastnr = reservation.gastnr NO-LOCK, 
    FIRST gmember WHERE gmember.gastnr = res-line.gastnrmember NO-LOCK 
    BY reservation.resdat BY res-line.zinr: 
 
    RUN add-cllist.
    IF NOT incl-accompany THEN
    DO:    
        FIND FIRST cl-list WHERE cl-list.rmno EQ res-line.zinr 
            AND cl-list.resnr EQ res-line.resnr
            AND DATE(cl-list.arrival) EQ res-line.ankunft 
            AND DEC(cl-list.zipreis) EQ 0 AND cl-list.co LT 1 EXCLUSIVE-LOCK NO-ERROR.
        IF AVAILABLE cl-list THEN
        DO:
            DELETE cl-list.
            RELEASE cl-list.
            nr = nr - 1.
        END.
    END.
  END. 
  ELSE IF sorttype = 4 THEN
  FOR EACH res-line WHERE res-line.active-flag EQ 0 
    AND res-line.resstatus NE tentres 
    AND res-line.ankunft = curr-date, 
    FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr NO-LOCK, 
    /*FIRST zikat-list WHERE zikat-list.zikatnr = res-line.zikatnr
      AND zikat-list.SELECTED = YES NO-LOCK,*/
    FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
    FIRST sourccod WHERE Sourccod.source-code = reservation.resart NO-LOCK,
    FIRST guest WHERE guest.gastnr = reservation.gastnr NO-LOCK, 
    FIRST gmember WHERE gmember.gastnr = res-line.gastnrmember NO-LOCK 
    BY res-line.arrangement BY reservation.NAME BY reservation.groupname 
    BY res-line.name: 
 
    RUN add-cllist.
    IF NOT incl-accompany THEN
    DO:    
        FIND FIRST cl-list WHERE cl-list.rmno EQ res-line.zinr 
            AND cl-list.resnr EQ res-line.resnr
            AND DATE(cl-list.arrival) EQ res-line.ankunft 
            AND DEC(cl-list.zipreis) EQ 0 AND cl-list.co LT 1 EXCLUSIVE-LOCK NO-ERROR.
        IF AVAILABLE cl-list THEN
        DO:
            DELETE cl-list.
            RELEASE cl-list.
            nr = nr - 1.
        END.
    END.
  END. 
  ELSE
  FOR EACH res-line WHERE res-line.active-flag EQ 0 
    AND res-line.resstatus NE tentres 
    AND res-line.ankunft = curr-date, 
    FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr NO-LOCK, 
    /*FIRST zikat-list WHERE zikat-list.zikatnr = res-line.zikatnr
      AND zikat-list.SELECTED = YES NO-LOCK,*/
    FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
    FIRST sourccod WHERE Sourccod.source-code = reservation.resart NO-LOCK,
    FIRST guest WHERE guest.gastnr = reservation.gastnr NO-LOCK, 
    FIRST gmember WHERE gmember.gastnr = res-line.gastnrmember NO-LOCK 
    BY res-line.resstatus BY reservation.NAME BY reservation.groupname 
    BY res-line.name: 
 
    RUN add-cllist.
    IF NOT incl-accompany THEN
    DO:    
        FIND FIRST cl-list WHERE cl-list.rmno EQ res-line.zinr 
            AND cl-list.resnr EQ res-line.resnr
            AND DATE(cl-list.arrival) EQ res-line.ankunft 
            AND DEC(cl-list.zipreis) EQ 0 AND cl-list.co LT 1 EXCLUSIVE-LOCK NO-ERROR.
        IF AVAILABLE cl-list THEN
        DO:
            DELETE cl-list.
            RELEASE cl-list.
            nr = nr - 1.
        END.
    END.
  END. 
END. 

PROCEDURE create-summary:
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
      CREATE s-list. 
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
      CREATE s-list. 
      IF AVAILABLE s-list THEN s-list.nat = cl-list.nat. 
    END. 
    s-list.adult = s-list.adult + (cl-list.a + cl-list.co) * cl-list.qty. 
    s-list.child = s-list.child + cl-list.c * cl-list.qty. 
  END. 
 
  IF (tot-a + tot-co) NE 0 THEN 
  FOR EACH s-list WHERE s-list.nat NE "": 
    FIND FIRST nation WHERE nation.kurzbez = s-list.nat NO-LOCK NO-ERROR. 
    IF AVAILABLE nation THEN s-list.nat = nation.bezeich. 
    ELSE s-list.nat = translateExtended ("UNKNOWN",lvCAREA,""). 
    s-list.proz = s-list.adult / (tot-a + tot-co) * 100. 
  END.
END.
 
PROCEDURE create-arrival1:    
  DEFINE INPUT PARAMETER curr-date AS DATE.
  ASSIGN
      vip-flag = ""
      do-it = NO
      last-gcf = 0.

  nr = 0.
  /*disptype = 2. */
  IF sorttype = 1 THEN
  FOR EACH res-line WHERE (res-line.resstatus = 6 OR resstatus = 8 
    OR resstatus = 13) AND res-line.ankunft = curr-date NO-LOCK, 
    FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr NO-LOCK, 
    /*FIRST zikat-list WHERE zikat-list.zikatnr = res-line.zikatnr
      AND zikat-list.SELECTED = YES NO-LOCK,*/
    FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
    FIRST sourccod WHERE Sourccod.source-code = reservation.resart NO-LOCK,
    FIRST guest WHERE guest.gastnr = reservation.gastnr NO-LOCK, 
    FIRST gmember WHERE gmember.gastnr = res-line.gastnrmember NO-LOCK 
    BY reservation.NAME BY reservation.groupname 
    BY res-line.name BY res-line.zinr: 
    do-it = YES. 
    IF (res-line.ankunft = res-line.abreise) AND res-line.resstatus = 8 THEN 
    DO: 
      FIND FIRST history WHERE history.resnr = res-line.resnr 
        AND history.reslinnr = res-line.reslinnr 
        AND history.gesamtumsatz GT 0 NO-LOCK NO-ERROR. 
      IF NOT AVAILABLE history THEN do-it = NO. 
    END. 
    IF do-it THEN 
    DO: 
        RUN add-cllist1.
        IF NOT incl-accompany THEN
        DO:    
            FIND FIRST cl-list WHERE cl-list.rmno EQ res-line.zinr 
                AND cl-list.resnr EQ res-line.resnr
                AND DATE(cl-list.arrival) EQ res-line.ankunft 
                AND DEC(cl-list.zipreis) EQ 0 AND cl-list.co LT 1 EXCLUSIVE-LOCK NO-ERROR.
            IF AVAILABLE cl-list THEN
            DO:
                DELETE cl-list.
                RELEASE cl-list.
                nr = nr - 1.
            END.
        END.
    END. 
  END. 
  ELSE IF sorttype = 2 THEN
  FOR EACH res-line WHERE (res-line.resstatus = 6 OR resstatus = 8 
    OR resstatus = 13) AND res-line.ankunft = curr-date NO-LOCK, 
    FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr NO-LOCK, 
    /*FIRST zikat-list WHERE zikat-list.zikatnr = res-line.zikatnr
      AND zikat-list.SELECTED = YES NO-LOCK,*/
    FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
    FIRST sourccod WHERE Sourccod.source-code = reservation.resart NO-LOCK,
    FIRST guest WHERE guest.gastnr = reservation.gastnr NO-LOCK, 
    FIRST gmember WHERE gmember.gastnr = res-line.gastnrmember NO-LOCK 
    BY res-line.zinr BY reservation.NAME BY reservation.groupname 
    BY res-line.name : 
    do-it = YES. 
    IF (res-line.ankunft = res-line.abreise) AND res-line.resstatus = 8 THEN 
    DO: 
      FIND FIRST history WHERE history.resnr = res-line.resnr 
        AND history.reslinnr = res-line.reslinnr 
        AND history.gesamtumsatz GT 0 NO-LOCK NO-ERROR. 
      IF NOT AVAILABLE history THEN do-it = NO. 
    END. 
    IF do-it THEN 
    DO: 
        RUN add-cllist1.
        IF NOT incl-accompany THEN
        DO:    
            FIND FIRST cl-list WHERE cl-list.rmno EQ res-line.zinr 
            AND cl-list.resnr EQ res-line.resnr
            AND DATE(cl-list.arrival) EQ res-line.ankunft 
            AND DEC(cl-list.zipreis) EQ 0 AND cl-list.co LT 1 EXCLUSIVE-LOCK NO-ERROR.
            IF AVAILABLE cl-list THEN
            DO:
                DELETE cl-list.
                RELEASE cl-list.
                nr = nr - 1.
            END.
        END.
    END. 
  END.
  ELSE IF sorttype = 3 THEN
  FOR EACH res-line WHERE (res-line.resstatus = 6 OR resstatus = 8 
    OR resstatus = 13) AND res-line.ankunft = curr-date NO-LOCK, 
    FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr NO-LOCK, 
    /*FIRST zikat-list WHERE zikat-list.zikatnr = res-line.zikatnr
      AND zikat-list.SELECTED = YES NO-LOCK,*/
    FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
    FIRST sourccod WHERE Sourccod.source-code = reservation.resart NO-LOCK,
    FIRST guest WHERE guest.gastnr = reservation.gastnr NO-LOCK, 
    FIRST gmember WHERE gmember.gastnr = res-line.gastnrmember NO-LOCK 
    BY reservation.resdat BY res-line.zinr: 
    do-it = YES. 
    IF (res-line.ankunft = res-line.abreise) AND res-line.resstatus = 8 THEN 
    DO: 
      FIND FIRST history WHERE history.resnr = res-line.resnr 
        AND history.reslinnr = res-line.reslinnr 
        AND history.gesamtumsatz GT 0 NO-LOCK NO-ERROR. 
      IF NOT AVAILABLE history THEN do-it = NO. 
    END. 
    IF do-it THEN 
    DO: 
        RUN add-cllist1.
        IF NOT incl-accompany THEN
        DO:    
            FIND FIRST cl-list WHERE cl-list.rmno EQ res-line.zinr 
                AND cl-list.resnr EQ res-line.resnr
                AND DATE(cl-list.arrival) EQ res-line.ankunft 
                AND DEC(cl-list.zipreis) EQ 0 AND cl-list.co LT 1 EXCLUSIVE-LOCK NO-ERROR.
            IF AVAILABLE cl-list THEN
            DO:
                DELETE cl-list.
                RELEASE cl-list.
                nr = nr - 1.
            END.
        END.
    END. 
  END. 
  ELSE IF sorttype = 4 THEN
  FOR EACH res-line WHERE (res-line.resstatus = 6 OR resstatus = 8 
    OR resstatus = 13) AND res-line.ankunft = curr-date NO-LOCK, 
    FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr NO-LOCK, 
    /*FIRST zikat-list WHERE zikat-list.zikatnr = res-line.zikatnr
      AND zikat-list.SELECTED = YES NO-LOCK,*/
    FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
    FIRST sourccod WHERE Sourccod.source-code = reservation.resart NO-LOCK,
    FIRST guest WHERE guest.gastnr = reservation.gastnr NO-LOCK, 
    FIRST gmember WHERE gmember.gastnr = res-line.gastnrmember NO-LOCK 
    BY res-line.arrangement BY reservation.NAME BY reservation.groupname 
    BY res-line.name: 
    do-it = YES. 
    IF (res-line.ankunft = res-line.abreise) AND res-line.resstatus = 8 THEN 
    DO: 
      FIND FIRST history WHERE history.resnr = res-line.resnr 
        AND history.reslinnr = res-line.reslinnr 
        AND history.gesamtumsatz GT 0 NO-LOCK NO-ERROR. 
      IF NOT AVAILABLE history THEN do-it = NO. 
    END. 
    IF do-it THEN 
    DO: 
        RUN add-cllist1.
        IF NOT incl-accompany THEN
        DO:    
            FIND FIRST cl-list WHERE cl-list.rmno EQ res-line.zinr 
                AND cl-list.resnr EQ res-line.resnr
                AND DATE(cl-list.arrival) EQ res-line.ankunft 
                AND DEC(cl-list.zipreis) EQ 0 AND cl-list.co LT 1 EXCLUSIVE-LOCK NO-ERROR.
            IF AVAILABLE cl-list THEN
            DO:
                DELETE cl-list.
                RELEASE cl-list.
                nr = nr - 1.
            END.
        END.
    END. 
  END.   
  ELSE
  FOR EACH res-line WHERE (res-line.resstatus = 6 OR resstatus = 8 
    OR resstatus = 13) AND res-line.ankunft = curr-date NO-LOCK, 
    FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr NO-LOCK, 
    /*FIRST zikat-list WHERE zikat-list.zikatnr = res-line.zikatnr
      AND zikat-list.SELECTED = YES NO-LOCK,*/
    FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
    FIRST sourccod WHERE Sourccod.source-code = reservation.resart NO-LOCK,
    FIRST guest WHERE guest.gastnr = reservation.gastnr NO-LOCK, 
    FIRST gmember WHERE gmember.gastnr = res-line.gastnrmember NO-LOCK 
    BY res-line.resstatus BY reservation.NAME BY reservation.groupname 
    BY res-line.name: 
    do-it = YES. 
    IF (res-line.ankunft = res-line.abreise) AND res-line.resstatus = 8 THEN 
    DO: 
      FIND FIRST history WHERE history.resnr = res-line.resnr 
        AND history.reslinnr = res-line.reslinnr 
        AND history.gesamtumsatz GT 0 NO-LOCK NO-ERROR. 
      IF NOT AVAILABLE history THEN do-it = NO. 
    END. 
    IF do-it THEN 
    DO: 
        RUN add-cllist1.
        IF NOT incl-accompany THEN
        DO:    
            FIND FIRST cl-list WHERE cl-list.rmno EQ res-line.zinr 
                AND cl-list.resnr EQ res-line.resnr
                AND DATE(cl-list.arrival) EQ res-line.ankunft 
                AND DEC(cl-list.zipreis) EQ 0 AND cl-list.co LT 1 EXCLUSIVE-LOCK NO-ERROR.
            IF AVAILABLE cl-list THEN
            DO:
                DELETE cl-list.
                RELEASE cl-list.
                nr = nr - 1.
            END.
        END.
    END. 
  END.
END. 

PROCEDURE add-cllist1:
    DEFINE BUFFER gbuff         FOR guest.
    DEFINE BUFFER rbuff         FOR reservation.

    dummy-flag  = NO.
    IF res-line.gastnr = Ol-gastnr OR res-line.gastnr = WG-gastnr
        OR res-line.gastnr = indi-gastnr OR res-line.gastnr = sms-gastnr
        THEN dummy-flag = YES.

    FIND FIRST setup-list WHERE setup-list.nr = res-line.setup + 1. 
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
 
      CREATE cl-list.  /*1*/
      ASSIGN 
        cl-list.nr        = nr 
        cl-list.datum     = res-line.ankunft
        cl-list.groupname = reservation.groupname 
        cl-list.rmcat     = zimkateg.kurzbez + setup-list.char 
        cl-list.kurzbez   = zimkateg.kurzbez 
        cl-list.bezeich   = zimkateg.bezeich
        /*cl-list.rmcat     = zikat-list.kurzbez + setup-list.char 
        cl-list.kurzbez   = zikat-list.kurzbez 
        cl-list.bezeich   = zikat-list.bezeich*/
        cl-list.nat       = gmember.nation1 
        cl-list.gastnr    = res-line.gastnr 
        cl-list.resnr     = res-line.resnr 
        cl-list.vip       = vip-flag 
        cl-list.name      = res-line.name 
        cl-list.zipreis   = STRING(res-line.zipreis, " >>>,>>>,>>9.99")
        cl-list.zimmeranz = res-line.zimmeranz 
        cl-list.rmno      = res-line.zinr 
        cl-list.arrival   = STRING(res-line.ankunft, "99/99/99")
        cl-list.depart    = STRING(res-line.abreise, "99/99/99")
        cl-list.a         = res-line.erwachs 
        cl-list.c         = res-line.kind1 + res-line.kind2 
        cl-list.co        = res-line.gratis 
        cl-list.argt      = res-line.arrangement 
        cl-list.flight    = SUBSTR(res-line.flight-nr, 1, 6) 
        cl-list.eta       = SUBSTR(res-line.flight-nr, 7, 4) /*sis 070814*/
        cl-list.etd       = SUBSTR(res-line.flight-nr, 18, 4) /*sis 070814*/  
        cl-list.stay      = gmember.aufenthalte
        cl-list.Email    = gmember.email-adr /*guest.email-adr*/
        cl-list.sob       = sourccod.bezeich
        cl-list.ci-id     = res-line.cancelled-id    /*MT 04/09/13 */
        cl-list.ci-time   = STRING(res-line.ankzeit, "HH:MM")
        cl-list.city      = gmember.wohnort
        cl-list.res-stat  = res-line.resstatus
        cl-list.res-stat-str  = STRING(cl-list.res-stat) + " - " + stat-list[res-line.resstatus]
        cl-list.birthdate = gmember.geburtdatum1
      .

      FIND FIRST zimmer WHERE zimmer.zinr = res-line.zinr NO-LOCK NO-ERROR.
      IF AVAILABLE zimmer THEN
      DO:
        ASSIGN cl-list.zinr-bez = zimmer.bezeich.
      END.
      
      IF res-line.resstatus NE 11 AND res-line.resstatus NE 13 THEN ASSIGN cl-list.flag-guest = 1.
      ELSE ASSIGN cl-list.flag-guest = 2.

      IF guest.karteityp NE 0 THEN
        cl-list.company   = guest.name + ", " + guest.vorname1 
          + " " + guest.anrede1 + guest.anredefirma.
      IF gmember.telefon NE "" THEN
      cl-list.company   = cl-list.company + ";" + gmember.telefon.
 
      IF cl-list.nat = "" THEN cl-list.nat = "?". 
      ELSE 
      DO: 
        FIND FIRST nation WHERE nation.kurzbez = cl-list.nat NO-LOCK NO-ERROR. 
        IF AVAILABLE nation THEN cl-list.nation = nation.bezeich. 
      END. 

      FIND FIRST nation WHERE nation.kurzbez = gmember.nation2 AND nation.natcode GT 0 NO-LOCK NO-ERROR.
      IF AVAILABLE nation THEN
      DO:
          cl-list.nation2 = nation.bezeich.
      END.
 
      /*DODY 27/02/18 penambahan membership number*/
      FIND FIRST mc-guest WHERE mc-guest.gastnr = gmember.gastnr NO-LOCK NO-ERROR.
      IF AVAILABLE mc-guest THEN
      DO:
          cl-list.memberno = mc-guest.cardnum.
          FIND FIRST mc-types WHERE mc-types.nr = mc-guest.nr NO-LOCK NO-ERROR. /*FD*/
          IF AVAILABLE mc-types THEN
          DO:
             cl-list.memberno = mc-guest.cardnum + ";" + mc-types.bezeich.             
          END.
      END.

      cl-list.resdate = STRING(reservation.resdat, "99/99/99").
      cl-list.created-by = reservation.useridanlage.

      IF res-line.resstatus EQ 6 THEN 
      DO: 
        tot-rm = tot-rm + res-line.zimmeranz. 
        cl-list.qty = res-line.zimmeranz. 
      END. 
      ELSE IF res-line.resstatus EQ 8 AND 
      (res-line.erwachs + res-line.gratis) GT 0 THEN 
      DO: 
        tot-rm = tot-rm + res-line.zimmeranz. 
        cl-list.qty = res-line.zimmeranz. 
      END. 
 
      
      IF comment-type = 0 THEN
      DO:
          IF NOT split-rsv-print THEN /*Orig*/
          DO:
              DO i = 1 TO length(res-line.bemerk): 
                IF SUBSTR(res-line.bemerk,i,1) = chr(10) THEN 
                    cl-list.bemerk = cl-list.bemerk + " ". 
                ELSE cl-list.bemerk = cl-list.bemerk + 
                    SUBSTR(TRIM(res-line.bemerk), i, 1). 
              END.
              /*naufal add remark 2000 char*/
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
              /*end naufal*/
          END.
          ELSE
          DO:
              DO i = 1 TO LENGTH(res-line.bemerk): 
                  cl-list.bemerk = cl-list.bemerk + SUBSTR(TRIM(res-line.bemerk), i, 1). 
              END.
    
              cl-list.rsv-comment = reservation.bemerk. /*FDL Feb 12, 2024 => Ticket 1BB9DD | FCB614*/
              /*
              FIND FIRST rbuff WHERE rbuff.gastnr = reservation.gastnr NO-LOCK NO-ERROR.
              IF AVAILABLE rbuff THEN
              DO:
                  cl-list.rsv-comment = rbuff.bemerk.                
              END.
              */
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
      END.
      ELSE IF comment-type = 1 THEN
      DO:
         IF dummy-flag OR guest.bemerk = "" THEN
         DO:
             FIND FIRST gbuff WHERE gbuff.gastnr = res-line.gastnrmember USE-INDEX
                 gastnr_index NO-LOCK NO-ERROR.
             IF AVAILABLE gbuff THEN
             DO:
                 DO i = 1 TO length(gbuff.bemerk): 
                   IF SUBSTR(gbuff.bemerk,i,1) = chr(10) THEN 
                       cl-list.bemerk = cl-list.bemerk + " ". 
                   ELSE cl-list.bemerk = cl-list.bemerk + 
                       SUBSTR(TRIM(gbuff.bemerk), i, 1). 
                 END. 
             END.
         END.
         ELSE
          DO i = 1 TO length(guest.bemerk): 
            IF SUBSTR(guest.bemerk,i,1) = chr(10) THEN 
                cl-list.bemerk = guest.bemerk + " ". 
            ELSE cl-list.bemerk = guest.bemerk + 
                SUBSTR(TRIM(guest.bemerk), i, 1). 
          END. 
      END.
      ELSE /*M additional comment type */
      DO:
          IF dummy-flag OR guest.bemerk = "" THEN
          DO:
              FIND FIRST gbuff WHERE gbuff.gastnr = res-line.gastnrmember 
                  USE-INDEX gastnr_index NO-LOCK NO-ERROR.
              IF AVAILABLE gbuff THEN
              DO:
                  DO i = 1 TO LENGTH(gbuff.bemerk): 
                    IF SUBSTR(gbuff.bemerk,i,1) = CHR(10) THEN 
                        cl-list.bemerk = cl-list.bemerk + " ". 
                    ELSE cl-list.bemerk = cl-list.bemerk + 
                        SUBSTR(TRIM(gbuff.bemerk), i, 1). 
                  END. 
              END.
          END.
          ELSE
          DO i = 1 TO LENGTH(guest.bemerk): 
              IF SUBSTR(guest.bemerk,i,1) = CHR(10) THEN 
                  cl-list.bemerk = cl-list.bemerk + " ". 
              ELSE cl-list.bemerk = cl-list.bemerk + 
                  SUBSTR(TRIM(guest.bemerk), i, 1). 
          END. 

          cl-list.bemerk = cl-list.bemerk + " || ".

          DO i = 1 TO LENGTH(res-line.bemerk): 
            IF SUBSTR(res-line.bemerk,i,1) = chr(10) THEN 
                cl-list.bemerk = cl-list.bemerk + " ". 
            ELSE cl-list.bemerk = cl-list.bemerk + 
                SUBSTR(TRIM(res-line.bemerk), i, 1). 
          END. 
      END.

 
      IF cl-list.rmno = "" AND cl-list.qty GT 1 THEN 
        cl-list.rmno = STRING(cl-list.qty, ">>>>>9"). 
 
      IF res-line.resstatus = 3 THEN 
      DO: 
        IF cl-list.qty LE 9 THEN cl-list.rmno = "    T" + STRING(cl-list.qty,"9"). 
        ELSE IF cl-list.qty LE 99 THEN cl-list.rmno = 
          "   T" + STRING(cl-list.qty,"99"). 
        ELSE IF cl-list.qty LE 999 THEN cl-list.rmno = 
          "  T" + STRING(cl-list.qty,"999"). 
      END. 
      ELSE IF res-line.resstatus = 4 THEN 
      DO: 
        IF cl-list.qty LE 9 THEN cl-list.rmno = "    W" + STRING(cl-list.qty,"9"). 
        ELSE IF cl-list.qty LE 99 THEN cl-list.rmno = 
           "   W" + STRING(cl-list.qty,"99"). 
        ELSE IF cl-list.qty LE 999 THEN cl-list.rmno = 
           "  W" + STRING(cl-list.qty,"999"). 
      END. 
 
      cl-list.pax = STRING(cl-list.a,"9") + "/" + STRING(cl-list.c,"9"). 

      /*ITA 040617 --> for special request*/
     FIND FIRST reslin-queasy WHERE reslin-queasy.KEY = "specialRequest"
         AND reslin-queasy.resnr = res-line.resnr 
         AND reslin-queasy.reslinnr = res-line.reslinnr NO-LOCK NO-ERROR.
     IF AVAILABLE reslin-queasy THEN
         ASSIGN cl-list.spreq = reslin-queasy.char3.
     /*end*/
 
      tot-a = tot-a + res-line.erwachs * res-line.zimmeranz. 
      tot-c = tot-c + (res-line.kind1 + res-line.kind2) * res-line.zimmeranz. 
      tot-co = tot-co + res-line.gratis * res-line.zimmeranz. 
END.
 
PROCEDURE create-browse:
DEFINE VARIABLE found AS LOGICAL INIT NO.
DEFINE VARIABLE loopi AS INT.
DEFINE VARIABLE counter-str AS CHAR.
DEFINE VARIABLE tot-troom  AS INTEGER.
DEFINE VARIABLE tot-trsv   AS INTEGER.
DEFINE VARIABLE tot-tadult AS INTEGER.
DEFINE VARIABLE tot-tkind  AS INTEGER.

    FOR EACH t-cl-list:
        DELETE t-cl-list.
    END.
    
    FOR EACH t-list:
        DELETE t-list.
    END.

    FOR EACH cl-list:
        CREATE t-cl-list.
        BUFFER-COPY cl-list TO t-cl-list.
        IF NUM-ENTRIES(cl-list.company, ";") GT 1 THEN
            ASSIGN
            t-cl-list.company = ENTRY(1, cl-list.company, ";")
            t-cl-list.phonenum = ENTRY(2, cl-list.company, ";").
        ELSE
            t-cl-list.company = cl-list.company.
    
        IF NUM-ENTRIES(cl-list.memberno, ";") GT 1 THEN /*FD*/
        DO:
            ASSIGN
                t-cl-list.member-typ = ENTRY(2, cl-list.memberno, ";")
                t-cl-list.memberno = ENTRY(1, cl-list.memberno, ";").              
        END.
        ELSE t-cl-list.memberno = cl-list.memberno.
    
        IF t-cl-list.stay GT 1 THEN t-cl-list.repeat-guest = "*".
    
        ASSIGN t-cl-list.night = DATE(cl-list.depart) - DATE(cl-list.arrival).
    END.
    
    CREATE t-cl-list.
    CREATE t-cl-list.
    ASSIGN                       
        t-cl-list.NAME           = "SUMMARY"
        t-cl-list.memberno       = "Room Type"
        t-cl-list.member-typ     = "Nation"
        t-cl-list.vip            = " Qty"
        t-cl-list.argt           = "  Adult"
        t-cl-list.rmcat          = "   (%)"
        t-cl-list.rate-code      = "     Child"
    .
    
    FOR EACH s-list:
        CREATE t-cl-list.
        ASSIGN                     
            t-cl-list.memberno     = s-list.bezeich
            t-cl-list.member-typ   = s-list.nat
            t-cl-list.vip          = STRING(s-list.anz, ">>>9")
            t-cl-list.argt         = STRING(s-list.adult, "  >>>>9")
            t-cl-list.rmcat        = STRING(s-list.proz, ">>9.99")
            t-cl-list.rate-code    = STRING(s-list.child, "     >>>>9")
        .
    END.
    
    CREATE t-cl-list.
    ASSIGN
        t-cl-list.memberno         = "T O T A L"
        t-cl-list.member-typ       = ""
        t-cl-list.vip              = STRING(tot-rm, ">>>9")
        t-cl-list.argt             = STRING(tot-a + tot-co, "  >>>>9")
        t-cl-list.rmcat            = "100.00"
        t-cl-list.rate-code        = STRING(tot-c,"     >>>>9")
    .              
    
    FOR EACH t-cl-list BY t-cl-list.datum BY t-cl-list.nr:
      IF total-flag AND t-cl-list.gastnr > 0 THEN
      DO:
        FIND FIRST t-list WHERE t-list.gastnr = t-cl-list.gastnr NO-ERROR.
        IF NOT AVAILABLE t-list THEN
        DO:
          CREATE t-list.
          ASSIGN
          t-list.gastnr  = t-cl-list.gastnr
          t-list.company = t-cl-list.company.
        END.
        ASSIGN
            t-list.anzahl  = t-list.anzahl + t-cl-list.zimmeranz
            t-list.erwachs = t-list.erwachs + t-cl-list.zimmeranz * t-cl-list.a
            t-list.kind    = t-list.kind + t-cl-list.zimmeranz * t-cl-list.c.
        found = NO.
        DO loopi = 1 TO NUM-ENTRIES(t-list.counter,";"):
            counter-str = ENTRY(loopi,t-list.counter,";").
            IF INT(counter-str) = t-cl-list.resnr THEN found = YES.
        END.
        IF NOT found THEN
            t-list.counter = t-list.counter + STRING(t-cl-list.resnr) + ";". 
      END.
    END.
    
    IF total-flag THEN
    DO:
        CREATE t-cl-list.
        CREATE t-cl-list.
        ASSIGN                            
            t-cl-list.memberno       = "Reserve Name"
            t-cl-list.member-typ     = "               Rooms"
            t-cl-list.argt           = " TotRsv"
            t-cl-list.rmcat          = " Adult"
            t-cl-list.rate-code      = "     Child"
        .
    
        FOR EACH t-list:
            IF NUM-ENTRIES(t-list.counter,";") GE 2 THEN
                t-list.int-counter = NUM-ENTRIES(t-list.counter,";") - 1.
            ELSE t-list.int-counter = 0.
        END.
    
        FOR EACH t-list:
            CREATE t-cl-list.
            ASSIGN
                t-cl-list.rmno           = "#"
                t-cl-list.memberno       = t-list.company
                t-cl-list.member-typ     = STRING(t-list.anzahl, "                >>>9")
                t-cl-list.argt           = STRING(t-list.int-counter, "    >>9")
                t-cl-list.rmcat          = STRING(t-list.erwachs, "   >>9")
                t-cl-list.rate-code      = STRING(t-list.kind, "       >>9")
            .
        END.
    
        FOR EACH t-list:
            ASSIGN
                tot-troom = tot-troom + t-list.anzahl
                tot-trsv  = tot-trsv + t-list.int-counter
                tot-tadult = tot-tadult + t-list.erwachs
                tot-tkind = tot-tkind + t-list.kind
            .
        END.
        CREATE t-cl-list.
        ASSIGN
            t-cl-list.rmno           = "#"
            t-cl-list.memberno       = "T O T A L"
            t-cl-list.member-typ     = STRING(tot-troom, "                >>>9")
            t-cl-list.argt           = STRING(tot-trsv, "    >>9")
            t-cl-list.rmcat          = STRING(tot-tadult, "   >>9")     
            t-cl-list.rate-code      = STRING(tot-tkind, "       >>9")    
        .           
    END. 
END PROCEDURE.

PROCEDURE bed-setup: 
  CREATE setup-list. 
  setup-list.nr = 1. 
  setup-list.char = " ". 
  FOR EACH paramtext WHERE paramtext.txtnr GE 9201 
    AND paramtext.txtnr LE 9299 NO-LOCK: 
    CREATE setup-list. 
    setup-list.nr = paramtext.txtnr - 9199. 
    setup-list.char = SUBSTR(paramtext.notes,1,1). 
  END. 
END.


