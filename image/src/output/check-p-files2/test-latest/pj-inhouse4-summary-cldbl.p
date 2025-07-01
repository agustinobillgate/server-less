DEFINE WORKFILE setup-list 
  FIELD nr          AS INTEGER 
  FIELD CHAR        AS CHAR FORMAT "x(1)". 

DEFINE TEMP-TABLE cl-list 
  FIELD resnr      AS INTEGER   FORMAT ">>>>>9" 
  FIELD qty        AS INTEGER   FORMAT ">>9" 
  FIELD rmcat      AS CHAR      FORMAT "x(6)" 
  FIELD rmno       LIKE zimmer.zinr	 
  FIELD nation     AS CHAR 
  FIELD arrive     AS DATE 
  FIELD depart     AS DATE 
  FIELD zipreis    AS DECIMAL   FORMAT "->>,>>>,>>>,>>9.99" 
  FIELD kurzbez    AS CHAR 
  FIELD bezeich    AS CHAR  
  FIELD a          AS INTEGER   FORMAT "9" 
  FIELD c          AS INTEGER   FORMAT "9" 
  FIELD co         AS INTEGER   FORMAT ">9" 
  FIELD nat        AS CHAR      FORMAT "x(3)" 
  FIELD lodging    AS DECIMAL   FORMAT "->>,>>>,>>>,>>9.99"  
  FIELD breakfast  AS DECIMAL   FORMAT "->>,>>>,>>>,>>9.99"      
  FIELD lunch      AS DECIMAL   FORMAT "->>,>>>,>>>,>>9.99"      
  FIELD dinner     AS DECIMAL   FORMAT "->>,>>>,>>>,>>9.99"    
  FIELD otherev    AS DECIMAL   FORMAT "->>,>>>,>>>,>>9.99" 
  FIELD curr       AS CHAR      FORMAT "x(4)"
  FIELD paym       AS INTEGER   FORMAT ">>9" 
  FIELD segm       AS CHAR      FORMAT "x(12)"
  .                             

DEFINE TEMP-TABLE s-list 
  FIELD rmcat       AS CHAR FORMAT "x(6)" 
  FIELD bezeich     AS CHAR FORMAT "x(24)" 
  FIELD nat         AS CHAR FORMAT "x(24)" 
  FIELD anz         AS INTEGER FORMAT ">>9" 
  FIELD adult       AS INTEGER FORMAT ">>9" 
  FIELD proz        AS DECIMAL FORMAT ">>9.99" 
  FIELD child       AS INTEGER FORMAT ">>9"
  FIELD proz-qty    AS DECIMAL FORMAT ">>9.99"
  FIELD rev         AS DECIMAL FORMAT "->>,>>>,>>>,>>9.99"
  FIELD proz-rev    AS DECIMAL FORMAT ">>9.99"
  FIELD arr         AS DECIMAL FORMAT "->>,>>>,>>>,>>9.99"
 . 

DEFINE TEMP-TABLE zinr-list
    FIELD resnr     AS INTEGER
    FIELD reslinnr  AS INTEGER
    FIELD zinr      AS CHAR
    FIELD datum     AS DATE
    FIELD arrival   AS DATE
    FIELD departed  AS DATE.

DEFINE TEMP-TABLE t-buff-queasy LIKE queasy.

DEFINE TEMP-TABLE zikat-list 
    FIELD selected AS LOGICAL INITIAL NO 
    FIELD zikatnr  AS INTEGER 
    FIELD kurzbez  AS CHAR 
    FIELD bezeich  AS CHAR FORMAT "x(32)"
.

DEF INPUT PARAMETER sorttype        AS INT.
DEF INPUT PARAMETER from-date       AS DATE.
DEF INPUT PARAMETER to-date         AS DATE.
DEF INPUT PARAMETER curr-date       AS DATE.
DEF INPUT PARAMETER curr-gastnr     AS INT.
DEF INPUT PARAMETER froom           LIKE zimmer.zinr.
DEF INPUT PARAMETER troom           LIKE zimmer.zinr.
DEF INPUT PARAMETER exc-depart      AS LOGICAL.
DEF INPUT PARAMETER incl-gcomment   AS LOGICAL.
DEF INPUT PARAMETER incl-rsvcomment AS LOGICAL.
DEF INPUT PARAMETER prog-name       AS CHAR.
DEF INPUT PARAMETER disp-accompany  AS LOGICAL.
DEF INPUT PARAMETER TABLE FOR zikat-list.   /*FD Jan 06, 2022 => Req Prime Plaza*/
DEF OUTPUT PARAMETER tot-payrm      AS INTEGER INITIAL 0. 
DEF OUTPUT PARAMETER tot-rm         AS INTEGER INITIAL 0. 
DEF OUTPUT PARAMETER tot-a          AS INTEGER INITIAL 0. 
DEF OUTPUT PARAMETER tot-c          AS INTEGER INITIAL 0. 
DEF OUTPUT PARAMETER tot-co         AS INTEGER INITIAL 0. 
DEF OUTPUT PARAMETER tot-avail      AS INTEGER INITIAL 0. 
DEF OUTPUT PARAMETER inactive       AS INTEGER INITIAL 0. 
DEF OUTPUT PARAMETER tot-keycard    AS INTEGER INITIAL 0. /*FD*/
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
DEFINE VARIABLE frate       AS DECIMAL FORMAT ">,>>>,>>9.9999".
DEFINE VARIABLE exchg-rate  AS DECIMAL INITIAL 1. 
DEFINE VARIABLE ct          AS CHAR.
DEFINE VARIABLE contcode    AS CHAR.
DEFINE VARIABLE bfast-art     AS INTEGER. 
DEFINE VARIABLE lunch-art     AS INTEGER. 
DEFINE VARIABLE dinner-art    AS INTEGER. 
DEFINE VARIABLE lundin-art    AS INTEGER. 
DEFINE VARIABLE fb-dept       AS INTEGER. 
DEFINE VARIABLE argt-betrag   AS DECIMAL. 
DEFINE VARIABLE take-it       AS LOGICAL. 
DEFINE VARIABLE prcode        AS INTEGER. 

DEFINE VARIABLE qty           AS INTEGER. 
DEFINE VARIABLE r-qty         AS INTEGER INITIAL 0. 
DEFINE VARIABLE lodge-betrag  AS DECIMAL. 
DEFINE VARIABLE f-betrag      AS DECIMAL. 
DEFINE VARIABLE s             AS CHAR.
DEFINE VARIABLE tot-qty       AS INTEGER.
DEFINE VARIABLE tot-rev       AS DECIMAL.


DEFINE BUFFER waehrung1 FOR waehrung. 
DEFINE BUFFER artikel1 FOR artikel. 
DEFINE BUFFER nation1 FOR nation. 
/***********************************************************/

FIND FIRST htparam WHERE paramnr = 125 NO-LOCK. 
bfast-art = htparam.finteger.               /* Rulita 211024 | Fixing for serverless */  
FIND FIRST htparam WHERE paramnr = 126 NO-LOCK. 
fb-dept = htparam.finteger.               /* Rulita 211024 | Fixing for serverless */  
FIND FIRST htparam WHERE paramnr = 227 NO-LOCK. 
lunch-art = htparam.finteger.               /* Rulita 211024 | Fixing for serverless */  
FIND FIRST htparam WHERE paramnr = 228 NO-LOCK. 
dinner-art = htparam.finteger.               /* Rulita 211024 | Fixing for serverless */  

RUN bed-setup.
IF sorttype = 1 THEN 
DO:
  IF from-date GE curr-date THEN RUN create-inhouse.
  ELSE RUN create-genstat-inhouse.
END.

RUN create-buf-queasy.

IF to-date LT curr-date THEN
DO:
    FOR EACH zkstat WHERE zkstat.datum = to-date NO-LOCK:
        tot-room = tot-room + zkstat.anz100.
    END.
    FIND FIRST zinrstat WHERE zinrstat.zinr = "tot-rm" AND zinrstat.datum = to-date NO-LOCK NO-ERROR.
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
DEFINE BUFFER buff-art      FOR artikel.

  FOR EACH zinr-list:
      DELETE zinr-list.
  END.

  IF from-date = curr-date AND to-date = curr-date THEN 
  DO: 
    actflag1 = 1. 
    actflag2 = 1. 
  END. 
  ELSE 
  DO: 
    actflag1 = 1. 
    actflag2 = 2. 
  END. 
 
  tot-payrm     = 0. 
  tot-rm        = 0. 
  tot-a         = 0. 
  tot-c         = 0. 
  tot-co        = 0. 
  inactive      = 0. 
  tot-qty       = 0.
  tot-rev       = 0.
 
  FOR EACH s-list: 
   delete s-list. 
  END. 
 
  FOR EACH cl-list: 
    delete cl-list. 
  END. 
 
  tot-avail = 0. 
  FOR EACH zimmer WHERE zimmer.sleeping = YES NO-LOCK,
      FIRST zikat-list WHERE zikat-list.zikatnr = zimmer.zikatnr
      AND zikat-list.SELECTED = YES NO-LOCK:

    tot-avail = tot-avail + 1. 
  END. 
  
  FOR EACH res-line WHERE res-line.active-flag GE actflag1 
    AND res-line.active-flag LE actflag2 
    AND res-line.resstatus NE 9 
    AND res-line.resstatus NE 10 
    AND res-line.resstatus NE 12 
    AND res-line.ankunft LE from-date 
    AND res-line.abreise GE to-date 
    AND res-line.zinr GE froom AND res-line.zinr LE troom NO-LOCK, 
    /*FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr NO-LOCK, */
    FIRST zikat-list WHERE zikat-list.zikatnr = res-line.zikatnr
      AND zikat-list.SELECTED = YES NO-LOCK,
    FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
    FIRST guest WHERE guest.gastnr = reservation.gastnr NO-LOCK, 
    FIRST gmember WHERE gmember.gastnr = res-line.gastnrmember NO-LOCK,
    FIRST sourccod WHERE Sourccod.source-code = reservation.resart NO-LOCK,
    FIRST arrangement WHERE arrangement.arrangement = res-line.arrangement NO-LOCK,
    FIRST artikel WHERE artikel.artnr = arrangement.argt-artikelnr AND artikel.departement = 0 NO-LOCK,
    FIRST bill WHERE bill.resnr = res-line.resnr AND bill.reslinnr = res-line.reslinnr AND bill.zinr = res-line.zinr NO-LOCK
    BY res-line.zinr BY res-line.ankunft BY res-line.erwachs DESCENDING BY res-line.name: 
    IF exc-depart AND res-line.abreise = to-date THEN .
    ELSE
    DO:
        FIND FIRST waehrung1 WHERE waehrung1.waehrungsnr = res-line.betriebsnr NO-LOCK NO-ERROR. 
        exchg-rate = waehrung1.ankauf / waehrung1.einheit. 
        IF res-line.reserve-dec NE 0 THEN frate = res-line.reserve-dec. 
        ELSE frate = exchg-rate. 

        IF res-line.reserve-int NE 0 THEN 
        FIND FIRST guest-pr WHERE guest-pr.gastnr = guest.gastnr NO-LOCK NO-ERROR. 
        IF AVAILABLE guest-pr THEN 
        DO: 
            contcode = guest-pr.CODE.
            ct = res-line.zimmer-wunsch.
            IF ct MATCHES("*$CODE$*") THEN
            DO:
                ct = SUBSTR(ct,INDEX(ct,"$CODE$") + 6).
                contcode = SUBSTR(ct, 1, INDEX(ct,";") - 1).
            END.
        END.

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
     
        create cl-list. 
        ASSIGN 
          cl-list.resnr       = res-line.resnr 
          cl-list.rmcat       = zikat-list.kurzbez + setup-list.char 
          cl-list.kurzbez     = zikat-list.kurzbez 
          cl-list.bezeich     = zikat-list.bezeich
          cl-list.nat         = gmember.nation1
          cl-list.arrive      = res-line.ankunft 
          cl-list.depart      = res-line.abreise 
          cl-list.rmno        = res-line.zinr 
          cl-list.zipreis     = res-line.zipreis
          cl-list.qty         = res-line.zimmeranz 
          cl-list.a           = res-line.erwachs 
          cl-list.c           = res-line.kind1 + res-line.kind2 
          cl-list.co          = res-line.gratis 
          cl-list.lodging     = cl-list.zipreis
          cl-list.paym        = reservation.segmentcode
          .

        FIND FIRST segment WHERE segment.segmentcode = reservation.segmentcode NO-LOCK NO-ERROR.
        IF AVAILABLE segment THEN cl-list.segm = ENTRY(1, segment.bezeich, "$$0").
        
        FIND FIRST waehrung WHERE waehrung.waehrungsnr = res-line.betriebsnr NO-LOCK NO-ERROR.
        IF AVAILABLE waehrung THEN
           cl-list.curr = waehrung.wabkurz.

        FOR EACH argt-line WHERE argt-line.argtnr = arrangement.argtnr AND NOT argt-line.kind2 NO-LOCK: 
            FIND FIRST artikel1 WHERE artikel1.artnr = argt-line.argt-artnr 
                AND artikel1.departement = argt-line.departement NO-LOCK NO-ERROR.
                IF NOT AVAILABLE artikel1 THEN take-it = NO.
            ELSE RUN get-argtline-rate(contcode, RECID(argt-line), OUTPUT take-it, 
            OUTPUT f-betrag, OUTPUT argt-betrag, OUTPUT qty). 
            IF take-it THEN
            DO:
                IF artikel1.zwkum EQ bfast-art AND (artikel1.umsatzart = 3 OR artikel1.umsatzart GE 5) THEN 
                DO:
                    cl-list.breakfast = cl-list.breakfast + argt-betrag. 
                    cl-list.lodging   = cl-list.lodging - argt-betrag.
                END.
                ELSE IF artikel1.zwkum EQ lunch-art AND (artikel1.umsatzart = 3 OR artikel1.umsatzart GE 5) THEN 
                DO:
                    cl-list.lunch     = cl-list.lunch + argt-betrag. 
                    cl-list.lodging   = cl-list.lodging - argt-betrag.
                END.
                ELSE IF artikel1.zwkum EQ dinner-art AND (artikel1.umsatzart = 3 OR artikel1.umsatzart GE 5) THEN 
                DO:
                    cl-list.dinner    = cl-list.dinner + argt-betrag. 
                    cl-list.lodging   = cl-list.lodging - argt-betrag.
                END.
                ELSE 
                DO:
                    cl-list.otherev   = cl-list.otherev + argt-betrag. 
                    cl-list.lodging   = cl-list.lodging - argt-betrag.
                END.
            END.
        END.

        IF cl-list.nat = "" THEN cl-list.nat = "?".
        ELSE 
        DO: 
          FIND FIRST nation WHERE nation.kurzbez = cl-list.nat NO-LOCK NO-ERROR. 
          IF AVAILABLE nation THEN cl-list.nation = nation.bezeich. 
        END.

        IF res-line.resstatus = 13 OR res-line.zimmerfix THEN cl-list.qty = 0. 
     
        FIND FIRST zinr-list WHERE zinr-list.zinr = res-line.zinr 
            AND zinr-list.resnr = res-line.resnr 
            AND zinr-list.reslinnr = res-line.reslinnr
            AND zinr-list.arrival = res-line.ankunft
            AND zinr-list.departed = res-line.abreise NO-ERROR.
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
             IF NOT AVAILABLE queasy THEN tot-rm = tot-rm + res-line.zimmeranz. 
             ELSE IF AVAILABLE queasy AND queasy.number3 NE res-line.gastnr THEN 
               tot-rm = tot-rm + res-line.zimmeranz.
          END. 
          IF zimmer.sleeping AND res-line.zipreis GT 0 AND res-line.resstatus NE 13 THEN 
          DO: 
             IF NOT AVAILABLE queasy THEN tot-payrm = tot-payrm + res-line.zimmeranz. 
             ELSE IF AVAILABLE queasy AND queasy.number3 NE res-line.gastnr THEN 
               tot-payrm = tot-payrm + res-line.zimmeranz. 
          END. 
          ELSE IF NOT zimmer.sleeping THEN 
          DO: 
            IF AVAILABLE queasy AND queasy.number3 NE res-line.gastnr 
              AND res-line.zipreis GT 0 THEN tot-rm = tot-rm + res-line.zimmeranz. 
            inactive = inactive + 1. 
         END. 
        END. 
     
        tot-a = tot-a + res-line.erwachs. 
        tot-c = tot-c + res-line.kind1 + res-line.kind2. 
        tot-co = tot-co + res-line.gratis. 
        tot-keycard = tot-keycard + res-line.betrieb-gast.
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
    
    ASSIGN
        s-list.anz = s-list.anz + cl-list.qty
        s-list.rev = s-list.rev + cl-list.zipreis
        s-list.arr = s-list.arr + cl-list.lodging
        tot-qty    = tot-qty + cl-list.qty
        tot-rev    = tot-rev + cl-list.zipreis
    . 

 
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
    ASSIGN s-list.proz     = s-list.adult / (tot-a + tot-co) * 100. 
  END. 

  FOR EACH s-list :
      ASSIGN
          s-list.proz-qty = (s-list.anz / tot-qty) * 100
          s-list.proz-rev = (s-list.rev / tot-rev) * 100
      .
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
DEFINE BUFFER buff-art      FOR artikel.

  FOR EACH zinr-list:
      DELETE zinr-list.
  END.

  IF from-date = curr-date AND to-date = curr-date THEN 
  DO: 
    actflag1 = 1. 
    actflag2 = 1. 
  END. 
  ELSE 
  DO: 
    actflag1 = 1. 
    actflag2 = 2. 
  END. 
 
  tot-payrm     = 0. 
  tot-rm        = 0. 
  tot-a         = 0. 
  tot-c         = 0. 
  tot-co        = 0. 
  inactive      = 0.
  tot-qty       = 0.
  tot-rev       = 0.
 
  FOR EACH s-list: 
   delete s-list. 
  END. 
 
  FOR EACH cl-list: 
    delete cl-list. 
  END. 
 
  tot-avail = 0. 
  FOR EACH zkstat WHERE zkstat.datum GE from-date AND zkstat.datum LE to-date NO-LOCK,
      FIRST zikat-list WHERE zikat-list.zikatnr = zkstat.zikatnr
      AND zikat-list.SELECTED = YES NO-LOCK:

      tot-avail = tot-avail + zkstat.anz100.
  END.

  DEF VAR z AS INT.
  FOR EACH genstat WHERE genstat.datum GE from-date
      AND genstat.datum LE to-date      
      AND genstat.zinr GE froom 
      AND genstat.zinr LE troom NO-LOCK,
    /*FIRST zimkateg WHERE zimkateg.zikatnr = genstat.zikatnr NO-LOCK, */
    FIRST zikat-list WHERE zikat-list.zikatnr = genstat.zikatnr
      AND zikat-list.SELECTED = YES NO-LOCK,
    FIRST reservation WHERE reservation.resnr = genstat.resnr NO-LOCK, 
    FIRST guest WHERE guest.gastnr = genstat.gastnr NO-LOCK, 
    FIRST gmember WHERE gmember.gastnr = genstat.gastnrmember NO-LOCK,
    FIRST sourccod WHERE Sourccod.source-code = reservation.resart NO-LOCK
    BY genstat.zinr BY genstat.datum BY genstat.erwachs DESCENDING BY gmember.name: 
    
    IF exc-depart AND genstat.res-date[1] LE /*from-date*/ genstat.datum
          AND genstat.res-date[2] = /*to-date*/ genstat.datum
          AND genstat.resstatus = 8 THEN . 
    ELSE
    DO:
        FIND FIRST res-line WHERE res-line.resnr = genstat.resnr
           AND res-line.reslinnr = genstat.res-int[1] NO-LOCK.
          FIND FIRST setup-list WHERE setup-list.nr = res-line.setup + 1. 

        FIND FIRST zimmer WHERE zimmer.zinr = genstat.zinr NO-LOCK NO-ERROR. 
        FIND FIRST bill WHERE bill.resnr = genstat.resnr /*AND bill.zinr = genstat.zinr*/ NO-LOCK NO-ERROR.

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
          cl-list.resnr       = genstat.resnr 
          cl-list.rmcat       = zikat-list.kurzbez + setup-list.char 
          cl-list.kurzbez     = zikat-list.kurzbez 
          cl-list.bezeich     = zikat-list.bezeich
          cl-list.nat         = gmember.nation1
          cl-list.arrive      = genstat.res-date[1] 
          cl-list.depart      = genstat.res-date[2] 
          cl-list.rmno        = genstat.zinr 
          cl-list.zipreis     = genstat.zipreis
          cl-list.qty         = 1
          cl-list.a           = genstat.erwachs                                 
          cl-list.c           = genstat.kind1 + genstat.kind2 + genstat.kind3   
          cl-list.co          = genstat.gratis                                  
          cl-list.lodging     = genstat.logis
          cl-list.breakfast   = genstat.res-deci[2]
          cl-list.lunch       = genstat.res-deci[3]
          cl-list.dinner      = genstat.res-deci[4]
          cl-list.otherev     = genstat.res-deci[5]
          cl-list.paym        = genstat.segmentcode
        .

        FIND FIRST segment WHERE segment.segmentcode = reservation.segmentcode NO-LOCK NO-ERROR.
        IF AVAILABLE segment THEN cl-list.segm = ENTRY(1, segment.bezeich, "$$0").
        
        FIND FIRST waehrung WHERE waehrung.waehrungsnr = res-line.betriebsnr NO-LOCK NO-ERROR.
        IF AVAILABLE waehrung THEN
           cl-list.curr = waehrung.wabkurz.
        
        IF cl-list.nat = "" THEN cl-list.nat = "?". 
        IF genstat.resstatus = 13 THEN cl-list.qty = 0. 
     
        IF cl-list.nat = "" THEN cl-list.nat = "?". 
        ELSE 
        DO: 
          FIND FIRST nation WHERE nation.kurzbez = cl-list.nat NO-LOCK NO-ERROR. 
          IF AVAILABLE nation THEN cl-list.nation = nation.bezeich. 
        END. 

     
        FIND FIRST zinr-list WHERE zinr-list.zinr = genstat.zinr 
            AND zinr-list.resnr = res-line.resnr 
            AND zinr-list.reslinnr = res-line.reslinnr
            AND zinr-list.datum = genstat.datum NO-ERROR.
        IF NOT AVAILABLE zinr-list THEN
        DO: 
          CREATE zinr-list.
          ASSIGN
              zinr-list.resnr = res-line.resnr
              zinr-list.reslinnr = res-line.reslinnr
              zinr-list.zinr  = genstat.zinr
              zinr-list.datum = genstat.datum.

          FIND FIRST queasy WHERE queasy.key = 14 AND queasy.char1 = genstat.zinr 
            AND queasy.date1 LE curr-date AND queasy.date2 GE curr-date 
            NO-LOCK NO-ERROR. 
          IF zimmer.sleeping /*MT*/ /*ITA 301213*/ AND genstat.resstatus NE 13 THEN 
          DO: 
             IF NOT AVAILABLE queasy THEN tot-rm = tot-rm + 1. 
             ELSE IF AVAILABLE queasy AND queasy.number3 NE genstat.gastnr THEN 
               tot-rm = tot-rm + 1. 
          END. 
          IF zimmer.sleeping AND genstat.zipreis GT 0 AND genstat.resstatus NE 13 THEN 
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
              AND genstat.zipreis GT 0 THEN tot-rm = tot-rm + 1. 
            inactive = inactive + 1. 
         END. 
        END. 
     
        tot-a = tot-a + genstat.erwachs. 
        tot-c = tot-c + genstat.kind1 + genstat.kind2 + genstat.kind3. 
        tot-co = tot-co + genstat.gratis. 
        tot-keycard = tot-keycard + res-line.betrieb-gast.
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
    
    ASSIGN
        s-list.anz = s-list.anz + cl-list.qty
        s-list.rev = s-list.rev + cl-list.zipreis
        s-list.arr = s-list.arr + cl-list.lodging
        tot-qty    = tot-qty + cl-list.qty
        tot-rev    = tot-rev + cl-list.zipreis
    . 
 
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
    ASSIGN s-list.proz = s-list.adult / (tot-a + tot-co) * 100. 
  END. 

  FOR EACH s-list :
      ASSIGN
          s-list.proz-qty = (s-list.anz / tot-qty) * 100
          s-list.proz-rev = (s-list.rev / tot-rev) * 100
      .
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
                      
PROCEDURE get-argtline-rate: 
DEFINE INPUT PARAMETER contcode     AS CHAR. 
DEFINE INPUT PARAMETER argt-recid   AS INTEGER. 
DEFINE OUTPUT PARAMETER add-it      AS LOGICAL INITIAL NO. 
DEFINE OUTPUT PARAMETER f-betrag    AS DECIMAL. 
DEFINE OUTPUT PARAMETER argt-betrag AS DECIMAL INITIAL 0. 
DEFINE OUTPUT PARAMETER qty         AS INTEGER INITIAL 0. 
 
DEFINE VARIABLE curr-zikatnr AS INTEGER NO-UNDO. 
DEFINE BUFFER argtline FOR argt-line. 
 
  IF res-line.l-zuordnung[1] NE 0 THEN curr-zikatnr = res-line.l-zuordnung[1]. 
  ELSE curr-zikatnr = res-line.zikatnr. 
 
  FIND FIRST argtline WHERE RECID(argtline) = argt-recid NO-LOCK NO-ERROR. 
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
        AND curr-date GE reslin-queasy.date1 
        AND curr-date LE reslin-queasy.date2 NO-LOCK NO-ERROR. 
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


                        

