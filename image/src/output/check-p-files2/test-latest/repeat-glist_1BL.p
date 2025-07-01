/******************** DEFINE TEMP TABLE ********************/
DEFINE WORKFILE setup-list 
  FIELD nr AS INTEGER 
  FIELD CHAR AS CHAR FORMAT "x(1)". 

DEF TEMP-TABLE g-list
    FIELD resnr         LIKE res-line.resnr
    FIELD gastnr        AS INTEGER
    FIELD NAME          AS CHAR FORMAT "x(50)"      LABEL "Guest Name"
    FIELD ankunft       AS DATE LABEL "Check-in"
    FIELD abreise       AS DATE LABEL "Check-out"
    FIELD zinr          LIKE zimmer.zinr
    FIELD reslinnr      AS INTEGER
    FIELD zipreis       LIKE res-line.zipreis
    FIELD currency      AS CHAR FORMAT "x(5)"
    FIELD argt          AS CHAR FORMAT "x(6)"
    FIELD erwachs       AS INTEGER FORMAT ">9" LABEL "A"
    FIELD kind1         AS INTEGER FORMAT ">9" LABEL "Ch"
    FIELD gratis        AS INTEGER FORMAT ">9" LABEL "CO"
    FIELD arrFlag       AS LOGICAL INITIAL NO
    FIELD resname       AS CHARACTER
    FIELD lodging       AS DECIMAL
    INDEX g_ix resnr reslinnr gastnr
    INDEX s_ix resnr gastnr
.

DEF TEMP-TABLE repeat-list
    FIELD flag      AS INTEGER INITIAL 0 /* 1=arrival 2=inhouse */ 
    FIELD gastnr    AS INTEGER
    FIELD NAME      AS CHAR FORMAT "x(32)"      LABEL "Guest Name"
    FIELD nation    AS CHAR FORMAT "x(16)"      LABEL "Nationality"
    FIELD birthdate AS DATE FORMAT "99/99/9999" LABEL "BirthDate"
    FIELD email     AS CHARACTER FORMAT "x(32)" LABEL "Email"      /*dody 10/10/16 add email&telp*/
    FIELD telefon   AS CHARACTER FORMAT "x(16)" LABEL "Telephone"
    FIELD vip       AS CHAR FORMAT "x(5)"       LABEL "VIP"
    FIELD city      AS CHAR FORMAT "X(16)"      LABEL "City"
    FIELD stay      AS INTEGER FORMAT ">>9"     LABEL "Stay"    INITIAL 0
    FIELD rmnite    AS INTEGER FORMAT ">>>9"    LABEL "RmNite"  INITIAL 0
    FIELD ankunft   AS DATE                     LABEL "Arrival" INITIAL ?
    FIELD arrFlag   AS LOGICAL INITIAL NO
    FIELD zinr      LIKE zimmer.zinr
    FIELD remark    AS CHAR FORMAT "x(36)"      LABEL "Guest Remark"
    FIELD resname   AS CHARACTER FORMAT "x(32)" LABEL "Reserve Name"
    FIELD lodging   AS DECIMAL                  LABEL "Lodging"
    FIELD pax       AS INTEGER                  LABEL "Pax"
    FIELD mobil-telefon LIKE guest.mobil-telefon    
.

DEF TEMP-TABLE cur-date
    FIELD curr-date AS DATE FORMAT "99/99/9999".

DEFINE INPUT PARAMETER pvILanguage  AS INTEGER  NO-UNDO.
DEFINE INPUT PARAMETER from-date   AS DATE. 
DEFINE INPUT PARAMETER to-date   AS DATE. 
DEFINE INPUT PARAMETER ci-date   AS DATE. 
DEFINE INPUT PARAMETER create-inhouse   AS LOGICAL. 
DEFINE OUTPUT PARAMETER TABLE FOR g-list.
DEFINE OUTPUT PARAMETER TABLE FOR repeat-list.
DEFINE OUTPUT PARAMETER TABLE FOR cur-date.

DEFINE VARIABLE tot-payrm AS INTEGER INITIAL 0. 
DEFINE VARIABLE tot-rm    AS INTEGER INITIAL 0. 
DEFINE VARIABLE tot-a     AS INTEGER INITIAL 0. 
DEFINE VARIABLE tot-c     AS INTEGER INITIAL 0. 
DEFINE VARIABLE tot-co    AS INTEGER INITIAL 0. 
DEFINE VARIABLE tot-avail  AS INTEGER INITIAL 0. 
DEFINE VARIABLE inactive   AS INTEGER INITIAL 0.
DEFINE VARIABLE curr-date   AS DATE.

DEFINE VARIABLE vipnr1 AS INTEGER INITIAL 999999999. 
DEFINE VARIABLE vipnr2 AS INTEGER INITIAL 999999999. 
DEFINE VARIABLE vipnr3 AS INTEGER INITIAL 999999999. 
DEFINE VARIABLE vipnr4 AS INTEGER INITIAL 999999999. 
DEFINE VARIABLE vipnr5 AS INTEGER INITIAL 999999999. 
DEFINE VARIABLE vipnr6 AS INTEGER INITIAL 999999999. 
DEFINE VARIABLE vipnr7 AS INTEGER INITIAL 999999999. 
DEFINE VARIABLE vipnr8 AS INTEGER INITIAL 999999999. 
DEFINE VARIABLE vipnr9 AS INTEGER INITIAL 999999999. 

DEFINE VARIABLE integerFlag AS INTEGER NO-UNDO.

{supertransBL.i} 
DEFINE VARIABLE lvCAREA AS CHARACTER INITIAL "pickup-list". 


/******************** MAIN LOGIC ********************/
RUN htpint.p(700, OUTPUT integerFlag).
IF integerFlag GT 0 THEN vipnr1 = integerFlag.
RUN htpint.p(701, OUTPUT integerFlag).
IF integerFlag GT 0 THEN vipnr2 = integerFlag.
RUN htpint.p(702, OUTPUT integerFlag).
IF integerFlag GT 0 THEN vipnr3 = integerFlag.
RUN htpint.p(703, OUTPUT integerFlag).
IF integerFlag GT 0 THEN vipnr4 = integerFlag.
RUN htpint.p(704, OUTPUT integerFlag).
IF integerFlag GT 0 THEN vipnr5 = integerFlag.
RUN htpint.p(705, OUTPUT integerFlag).
IF integerFlag GT 0 THEN vipnr6 = integerFlag.
RUN htpint.p(706, OUTPUT integerFlag).
IF integerFlag GT 0 THEN vipnr7 = integerFlag.
RUN htpint.p(707, OUTPUT integerFlag).
IF integerFlag GT 0 THEN vipnr8 = integerFlag.
RUN htpint.p(708, OUTPUT integerFlag).
IF integerFlag GT 0 THEN vipnr9 = integerFlag.

RUN bed-setup.
RUN create-inhouse.



/******************** PROCEDURE ********************/
PROCEDURE create-inhouse: 
DEFINE VARIABLE i           AS INTEGER. 
DEFINE VARIABLE vip-flag    AS CHAR. 
DEFINE VARIABLE nr          AS INTEGER INITIAL 0. 
DEFINE VARIABLE curr-gastnr AS INTEGER INITIAL 0.
DEFINE VARIABLE curr-resnr  AS INTEGER NO-UNDO.
DEFINE VARIABLE datum       AS DATE    NO-UNDO.
DEFINE VARIABLE datum1      AS DATE    NO-UNDO.
DEFINE VARIABLE datum2      AS DATE    NO-UNDO.
DEFINE VARIABLE curr-i      AS INTEGER.
DEFINE VARIABLE net-lodg    AS DECIMAL.
DEFINE VARIABLE Fnet-lodg   AS DECIMAL.
DEFINE VAR tot-breakfast    AS DECIMAL.
DEFINE VAR tot-Lunch        AS DECIMAL.
DEFINE VAR tot-dinner       AS DECIMAL.
DEFINE VAR tot-Other        AS DECIMAL.
DEFINE VAR tot-rmrev        AS DECIMAL INITIAL 0.
DEFINE VAR tot-vat          AS DECIMAL INITIAL 0.
DEFINE VAR tot-service      AS DECIMAL INITIAL 0.
DEFINE VAR tot-lodging      AS DECIMAL INITIAL 0.

DEF VAR zeit AS INT.

DEFINE BUFFER gfirma FOR guest. 
DEFINE BUFFER gbuff  FOR g-list.

  ASSIGN
    tot-payrm = 0 
    tot-rm    = 0 
    tot-a     = 0 
    tot-c     = 0 
    tot-co    = 0 
    inactive  = 0
    curr-date = ?
  . 
  
  FOR EACH repeat-list: 
    DELETE repeat-list. 
  END. 
 
  FOR EACH g-list:
      DELETE g-list.
  END.

  tot-avail = 0. 
  FOR EACH zimmer WHERE zimmer.sleeping = YES NO-LOCK: 
    tot-avail = tot-avail + 1. 
  END. 

  FOR EACH cur-date NO-LOCK:
      DELETE cur-date.
  END.

  IF to-date LT ci-date THEN
  DO:
     FOR EACH genstat WHERE genstat.datum GE from-date 
       AND genstat.datum LE to-date 
       AND genstat.gastnrmember GT 0
       AND genstat.zinr NE "" 
       AND genstat.resstatus NE 13 
       AND genstat.res-logic[2] EQ YES NO-LOCK USE-INDEX gastnrmember_ix
       BY genstat.datum:
       
       IF curr-date NE genstat.datum THEN
       DO:
           CREATE cur-date.
           ASSIGN cur-date.curr-date = genstat.datum.
       END.
     
       FIND FIRST g-list WHERE g-list.resnr = genstat.resnr
           AND g-list.reslinnr = genstat.res-int[1]
           AND g-list.gastnr = genstat.gastnrmember USE-INDEX g_ix NO-ERROR.
       IF NOT AVAILABLE g-list THEN
       DO:
           FIND FIRST waehrung WHERE waehrung.waehrungsnr = genstat.wahrungsnr
               NO-LOCK NO-ERROR.
           FIND FIRST guest WHERE guest.gastnr = genstat.gastnrmember
               NO-LOCK NO-ERROR.
           FIND FIRST gfirma WHERE gfirma.gastnr = genstat.gastnr
               NO-LOCK.
           CREATE g-list.
           ASSIGN
               g-list.resnr       = genstat.resnr
               g-list.gastnr      = genstat.gastnrmember
               g-list.NAME        = gfirma.NAME + ", " + gfirma.anredefirma
               g-list.reslinnr    = genstat.res-int[1]
               g-list.ankunft     = genstat.res-date[1]
               g-list.abreise     = genstat.res-date[2]
               g-list.zinr        = genstat.zinr
               g-list.zipreis     = genstat.zipreis
               g-list.argt        = genstat.argt
               g-list.lodging     = g-list.lodging + genstat.logis
               g-list.erwachs     = g-list.erwachs + genstat.erwachs
               g-list.kind1       = g-list.kind1 + genstat.kind1 + genstat.kind2
               g-list.gratis      = g-list.gratis + genstat.gratis.
           
           IF AVAILABLE waehrung THEN g-list.currency = waehrung.wabkurz.
       END.
     END.
  END.         
  ELSE IF to-date GE ci-date THEN
  DO:
    curr-date = ?.
    FOR EACH res-line WHERE res-line.active-flag LE 2 
      AND res-line.resstatus NE 9 AND res-line.resstatus NE 10
      AND res-line.resstatus NE 12 AND res-line.resstatus NE 99 /*FD Oct 15, 2021*/
      AND res-line.ankunft GE from-date AND res-line.ankunft LE to-date 
      NO-LOCK BY res-line.ankunft:
        
      IF curr-date NE res-line.ankunft THEN
      DO:
          CREATE cur-date.
          ASSIGN cur-date.curr-date = res-line.ankunft.
      END.

      FIND FIRST g-list WHERE g-list.resnr = res-line.resnr
        AND g-list.reslinnr = res-line.reslinnr
        AND g-list.gastnr = res-line.gastnrmember USE-INDEX g_ix NO-ERROR.
      IF NOT AVAILABLE g-list THEN
      DO:

        FIND FIRST waehrung WHERE waehrung.waehrungsnr = res-line.betriebsnr
          NO-LOCK NO-ERROR.
        FIND FIRST guest WHERE guest.gastnr = res-line.gastnrmember
          NO-LOCK NO-ERROR.
        FIND FIRST gfirma WHERE gfirma.gastnr = res-line.gastnr NO-LOCK.      
        CREATE g-list.    
        ASSIGN
          g-list.resnr       = res-line.resnr
          g-list.gastnr      = res-line.gastnrmember
          g-list.NAME        = gfirma.NAME + ", " + gfirma.anredefirma 
          g-list.reslinnr    = res-line.reslinnr
          g-list.ankunft     = res-line.ankunft
          g-list.abreise     = res-line.abreise
          g-list.zinr        = res-line.zinr
          g-list.zipreis     = res-line.zipreis
          g-list.argt        = res-line.arrangement
          g-list.arrFlag     = (res-line.active-flag = 0)
          /*wen*/            
          g-list.resname     = res-line.resname
          g-list.erwachs     = res-line.erwachs
          g-list.kind1       = res-line.kind1 + res-line.kind2
          g-list.gratis      = res-line.gratis.
        
        datum1 = res-line.ankunft.
        IF res-line.ankunft = res-line.abreise THEN ASSIGN datum2 = res-line.abreise.
        ELSE ASSIGN datum2 = res-line.abreise - 1.
        ASSIGN curr-i      = 0.
        DO datum = datum1 TO datum2:
            ASSIGN 
               net-lodg      = 0
               tot-breakfast = 0
               tot-lunch     = 0
               tot-dinner    = 0
               tot-other     = 0
               curr-i        = curr-i + 1. 
        
            RUN get-room-breakdown.p(RECID(res-line), datum, curr-i, datum,
                                     OUTPUT Fnet-lodg, OUTPUT net-lodg,
                                     OUTPUT tot-breakfast, OUTPUT tot-lunch ,
                                     OUTPUT tot-dinner, OUTPUT tot-other,
                                     OUTPUT tot-rmrev, OUTPUT tot-vat,
                                     OUTPUT tot-service).
            ASSIGN g-list.lodging  = g-list.lodging + net-lodg.            
        END.

        IF AVAILABLE waehrung THEN g-list.currency = waehrung.wabkurz.
      END.
    END.
  END.

  ASSIGN
    curr-gastnr = 0
    curr-resnr  = 0
  .
  FOR EACH g-list NO-LOCK,
    FIRST guest WHERE guest.gastnr EQ g-list.gastnr NO-LOCK BY g-list.gastnr BY g-list.resnr:
    IF curr-gastnr NE g-list.gastnr THEN
    DO:
      CREATE repeat-list.
      ASSIGN
        curr-gastnr         = g-list.gastnr
        curr-resnr          = g-list.resnr
        repeat-list.gastnr  = g-list.gastnr
        /*repeat-list.zinr    = ""*/
        repeat-list.zinr    = g-list.zinr     /*geral 004FE1*/
        repeat-list.ankunft = g-list.ankunft /*geral 004FE1*/
        repeat-list.pax     = g-list.erwachs + g-list.kind1 + g-list.gratis.
          
      IF NOT g-list.arrFlag THEN repeat-list.stay = 1.
      ELSE repeat-list.arrFlag = YES.

      /*FDL August 02, 2024 => Ticket DD466F*/
      vip-flag = "". 
      FIND FIRST guestseg WHERE guestseg.gastnr = guest.gastnr 
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
          FIND FIRST segment  WHERE segment.segmentcode = guestseg.segmentcode NO-LOCK NO-ERROR.
          IF AVAILABLE segment THEN ASSIGN vip-flag = segment.bezeich. 
      END.
      ASSIGN 
        repeat-list.vip       = vip-flag
        repeat-list.NAME      = guest.NAME + ", " + guest.vorname1 + " " + guest.anrede1
        repeat-list.birthdate = guest.geburtdatum1
        repeat-list.email     = guest.email-adr 
        repeat-list.telefon   = guest.telefon
        repeat-list.city      = guest.wohnort
        repeat-list.remark    = guest.bemerk
        repeat-list.mobil-telefon = guest.mobil-telefon
      .
      FIND FIRST nation WHERE nation.kurzbez = guest.nation1 NO-LOCK NO-ERROR.
      IF AVAILABLE nation THEN repeat-list.nation = nation.bezeich.

      FIND FIRST res-line WHERE res-line.active-flag EQ 1
        AND res-line.gastnrmember EQ g-list.gastnr
        AND res-line.resnr EQ g-list.resnr NO-LOCK NO-ERROR.
      IF AVAILABLE res-line THEN 
      DO:
          ASSIGN 
            repeat-list.flag    = 2
            repeat-list.zinr    = res-line.zinr
            repeat-list.ankunft = res-line.ankunft
            repeat-list.resname = res-line.resname.
      END.      
      ELSE
      DO:
        FOR EACH res-line WHERE (res-line.active-flag EQ 0 OR res-line.active-flag EQ 2)
          AND res-line.gastnrmember EQ g-list.gastnr 
          AND res-line.resnr EQ g-list.resnr
          NO-LOCK BY res-line.ankunft:
          IF res-line.active-flag EQ 2 THEN repeat-list.resname = res-line.resname. 
          ELSE
          DO:
              ASSIGN
                repeat-list.flag    = 1
                repeat-list.ankunft = res-line.ankunft
                repeat-list.resname = res-line.resname.
          END.              
          LEAVE.          
        END.                    
      END.
      /*End FDL*/
    END.
    ELSE
    DO:
      IF g-list.resnr NE curr-resnr THEN
      DO:
        ASSIGN curr-resnr = g-list.resnr.
        IF NOT g-list.arrFlag THEN repeat-list.stay = repeat-list.stay + 1.
        ELSE repeat-list.arrFlag = YES.
      END.
    END.
    IF NOT g-list.arrFlag THEN
        ASSIGN repeat-list.rmnite = repeat-list.rmnite + g-list.abreise - g-list.ankunft.
    ASSIGN repeat-list.lodging = g-list.lodging.
  END.
  
  FOR EACH repeat-list NO-LOCK:
    IF repeat-list.stay LT 2 AND NOT repeat-list.arrFLag THEN DELETE repeat-list.
    /* FDL COmment - Move Above Ticket DD466F
    ELSE
    DO:      
      FIND FIRST genstat WHERE genstat.gastnr = repeat-list.gastnr NO-LOCK NO-ERROR.   /*wen*/
      FIND FIRST guest WHERE guest.gastnr = repeat-list.gastnr NO-LOCK.
      FIND FIRST nation WHERE nation.kurzbez = guest.nation1
        NO-LOCK NO-ERROR.
      vip-flag = "". 
      FIND FIRST guestseg WHERE guestseg.gastnr = guest.gastnr 
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
          FIND FIRST segment  WHERE segment.segmentcode = guestseg.segmentcode NO-LOCK NO-ERROR.
          IF AVAILABLE segment THEN ASSIGN vip-flag = segment.bezeich. 
      END.
      ASSIGN 
        repeat-list.vip       = vip-flag
        repeat-list.NAME      = guest.NAME + ", " + guest.vorname1 + " " + guest.anrede1
        repeat-list.birthdate = guest.geburtdatum1
        repeat-list.email     = guest.email-adr /*dody 18/10/16 add email & telp*/
        repeat-list.telefon   = guest.telefon
        repeat-list.city      = guest.wohnort
        repeat-list.remark    = guest.bemerk
        repeat-list.mobil-telefon = guest.mobil-telefon
      .
      IF AVAILABLE nation THEN repeat-list.nation = nation.bezeich.
      /*IF AVAILABLE res-line THEN repeat-list.resname = res-line.resname.*/
            
      FIND FIRST res-line WHERE res-line.active-flag = 1
        AND res-line.gastnrmember = repeat-list.gastnr NO-LOCK NO-ERROR.
      IF AVAILABLE res-line THEN 
      ASSIGN 
        repeat-list.flag    = 2
        repeat-list.zinr    = res-line.zinr
        repeat-list.ankunft = res-line.ankunft
        repeat-list.resname = res-line.resname. /*wen*/
      ELSE
      DO:
        FOR EACH res-line WHERE res-line.active-flag = 0 
          AND res-line.gastnrmember = repeat-list.gastnr          
          NO-LOCK BY res-line.ankunft:
          ASSIGN
            repeat-list.flag    = 1
            repeat-list.ankunft = res-line.ankunft
            repeat-list.resname = res-line.resname. /*wen*/
          LEAVE.          
        END.        
        /* malik 09D162 */
        FOR EACH res-line WHERE res-line.active-flag = 2 
          AND res-line.gastnrmember = repeat-list.gastnr
          NO-LOCK BY res-line.ankunft:
          ASSIGN
            repeat-list.resname = res-line.resname. 
          LEAVE.
        END.
        /* End malik */        
      END.      
    END.
    */
  END.  
END. 

PROCEDURE bed-setup:
  FOR EACH setup-list:
      DELETE setup-list.
  END.
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
