DEFINE WORKFILE str-list 
  FIELD flag AS INTEGER INITIAL 0 
  FIELD long-stay AS LOGICAL INITIAL NO 
  FIELD line1 AS CHAR FORMAT "x(61)" 
  FIELD line2 AS CHAR FORMAT "x(69)". 

/*UPDATE cl-list resstatus dari integer ke character RVN 22/12/2022*/
DEFINE TEMP-TABLE cl-list 
  FIELD flag       AS INTEGER 
  FIELD nr         AS INTEGER FORMAT ">>9" 
  FIELD vip        AS CHAR FORMAT "x(3)" 
  FIELD resnr      AS INTEGER FORMAT ">>>>>>9" 
  FIELD name       AS CHAR FORMAT "x(24)" 
  FIELD groupname  AS CHAR FORMAT "x(24)" 
  FIELD rmno       LIKE zimmer.zinr
  FIELD qty        AS INTEGER FORMAT ">>9" 
  FIELD arrive     AS DATE 
  FIELD depart     AS DATE 
  FIELD resstatus  AS CHAR 
  FIELD rmcat      AS CHAR FORMAT "x(6)" 
  FIELD kurzbez    AS CHAR 
  FIELD bezeich    AS CHAR 
  FIELD a          AS INTEGER FORMAT "9" 
  FIELD c          AS INTEGER FORMAT "9" 
  FIELD co         AS INTEGER FORMAT ">9" 
  FIELD pax        AS CHAR FORMAT "x(5)" 
  FIELD nat        AS CHAR FORMAT "x(3)" 
  FIELD nation     AS CHAR 
  FIELD argt       AS CHAR FORMAT "x(7)" 
  FIELD company    AS CHAR FORMAT "x(18)" 
  FIELD flight     AS CHAR FORMAT "x(6)" 
  FIELD etd        AS CHAR FORMAT "99:99" 
  FIELD bemerk     AS CHAR FORMAT "x(16)"
    
  /* Naufal Afthar - 0430A4*/
  FIELD ratecode   AS CHAR FORMAT "x(4)"
  FIELD lodging    AS DECIMAL FORMAT ">>>,>>>,>>>,>>9.99" .


DEFINE TEMP-TABLE s-list 
  FIELD rmcat AS CHAR FORMAT "x(6)" 
  FIELD bezeich AS CHAR FORMAT "x(24)" 
  FIELD nat   AS CHAR FORMAT "x(24)" 
  FIELD anz   AS INTEGER FORMAT ">>9" 
  FIELD adult AS INTEGER FORMAT ">>9" 
  FIELD proz  AS DECIMAL FORMAT ">>9.99" 
  FIELD child AS INTEGER FORMAT ">>9". 

DEFINE WORKFILE setup-list 
  FIELD nr AS INTEGER 
  FIELD CHAR AS CHAR FORMAT "x(1)". 
 

DEF INPUT  PARAMETER sorttype   AS INT.
DEF INPUT  PARAMETER to-date    AS DATE.
DEF INPUT  PARAMETER from-date  AS DATE.
DEF INPUT  PARAMETER long-stay  AS INTEGER.
DEF OUTPUT PARAMETER tot-rm     AS INTEGER INITIAL 0. 
DEF OUTPUT PARAMETER tot-a      AS INTEGER INITIAL 0. 
DEF OUTPUT PARAMETER tot-c      AS INTEGER INITIAL 0. 
DEF OUTPUT PARAMETER tot-co     AS INTEGER INITIAL 0. 
DEF OUTPUT PARAMETER tot-avail  AS INTEGER INITIAL 0. 
DEF OUTPUT PARAMETER inactive   AS INTEGER INITIAL 0.
DEF OUTPUT PARAMETER TABLE FOR cl-list.
DEF OUTPUT PARAMETER TABLE FOR s-list.


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


RUN bed-setup. 
IF sorttype = 1 THEN RUN longstay-list. 
ELSE RUN shortstay-list. 


PROCEDURE bed-setup: 
  create setup-list. 
  setup-list.nr = 1. 
  setup-list.char = " ". 
  FOR EACH zimmer WHERE zimmer.setup NE 0 NO-LOCK: 
    FIND FIRST paramtext WHERE (paramtext.txtnr - 9200) = zimmer.setup 
      NO-LOCK NO-ERROR. 
    IF AVAILABLE paramtext THEN 
    DO: 
      FIND FIRST setup-list WHERE setup-list.nr = (zimmer.setup + 1) 
        NO-LOCK NO-ERROR. 
      IF NOT AVAILABLE setup-list THEN 
      DO: 
        create setup-list. 
        setup-list.nr = zimmer.setup + 1. 
        setup-list.char = SUBSTR(paramtext.notes,1,1). 
      END. 
    END. 
  END. 
END. 


PROCEDURE longstay-list: 
DEFINE VARIABLE i AS INTEGER. 
DEFINE VARIABLE vip-flag AS CHAR. 
DEFINE VARIABLE nr AS INTEGER INITIAL 0. 
DEFINE buffer gmember FOR guest. 
DEFINE VAR num-date AS INT. /* Malik Serverless */
DEFINE VAR s        AS CHAR. /* Naufal Afthar - 0430A4*/
 
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
 
  tot-avail = 0. 
  inactive = 0. 
 
  FOR EACH zimmer WHERE zimmer.sleeping = YES NO-LOCK: 
    tot-avail = tot-avail + 1. 
  END. 
  /* Malik Serverless */
  ASSIGN
    num-date = to-date - from-date
    tot-avail = tot-avail * (num-date + 1). 
  /* END Malik */
  /* tot-avail = tot-avail * (to-date - from-date + 1). */
  
 
  FOR EACH res-line WHERE res-line.active-flag LE 2 
    AND res-line.resstatus LE 8 
    AND res-line.resstatus NE 3 AND res-line.resstatus NE 4 
    AND (res-line.abreise - res-line.ankunft) GE long-stay 
    AND NOT res-line.ankunft GT to-date 
    AND NOT res-line.abreise LE from-date 
    AND res-line.erwachs GT 0 NO-LOCK, 
    FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr NO-LOCK, 
    FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
    FIRST guest WHERE guest.gastnr = reservation.gastnr NO-LOCK, 
    FIRST gmember WHERE gmember.gastnr = res-line.gastnrmember NO-LOCK 
    BY res-line.ankunft BY res-line.name: 
 
    FIND FIRST setup-list WHERE setup-list.nr = res-line.setup + 1. 
    FIND FIRST zimmer WHERE zimmer.zinr = res-line.zinr NO-LOCK NO-ERROR. 
 
    nr = nr + 1. 
    vip-flag = "".
    /*FDL Comment
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
    */
    /*FDL: Optimasi for .py */
    FOR EACH guestseg WHERE guestseg.gastnr = gmember.gastnr NO-LOCK:       
        IF guestseg.segmentcode = vipnr1 THEN 
        DO:
            vip-flag = "VIP". 
            LEAVE.
        END.
        ELSE IF guestseg.segmentcode = vipnr2 THEN 
        DO:
            vip-flag = "VIP". 
            LEAVE.
        END.
        ELSE IF guestseg.segmentcode = vipnr3 THEN 
        DO:
            vip-flag = "VIP". 
            LEAVE.
        END.
        ELSE IF guestseg.segmentcode = vipnr4 THEN 
        DO:
            vip-flag = "VIP". 
            LEAVE.
        END.
        ELSE IF guestseg.segmentcode = vipnr5 THEN 
        DO:
            vip-flag = "VIP". 
            LEAVE.
        END.
        ELSE IF guestseg.segmentcode = vipnr6 THEN 
        DO:
            vip-flag = "VIP". 
            LEAVE.
        END.
        ELSE IF guestseg.segmentcode = vipnr7 THEN 
        DO:
            vip-flag = "VIP". 
            LEAVE.
        END.
        ELSE IF guestseg.segmentcode = vipnr8 THEN 
        DO:
            vip-flag = "VIP". 
            LEAVE.
        END.
        ELSE IF guestseg.segmentcode = vipnr9 THEN 
        DO:
            vip-flag = "VIP". 
            LEAVE.
        END.
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
      cl-list.resnr     = res-line.resnr 
      cl-list.vip       = vip-flag 
      cl-list.name      = res-line.name 
      cl-list.rmno      = res-line.zinr 
      cl-list.arrive    = res-line.ankunft 
      cl-list.depart    = res-line.abreise 
      cl-list.resstatus = STRING(res-line.resstatus) /*UPDATE cl-list restatus dari integer ke character RVN 22/12/2022*/
      cl-list.qty       = res-line.zimmeranz 
      cl-list.a         = res-line.erwachs 
      cl-list.c         = res-line.kind1 + res-line.kind2 
      cl-list.co        = res-line.gratis 
      cl-list.argt      = res-line.arrangement 
      cl-list.flight    = SUBSTR(res-line.flight-nr, 12, 6) 
      cl-list.etd       = SUBSTR(res-line.flight-nr, 18, 5) 
      cl-list.company   = guest.name + ", " + guest.vorname1 
        + " " + guest.anrede1 + guest.anredefirma. 
 
    IF cl-list.nat = "" THEN cl-list.nat = "?". 
 
    DO i = 1 TO length(res-line.bemerk): 
      IF SUBSTR(res-line.bemerk,i,1) = chr(10) THEN 
      cl-list.bemerk = cl-list.bemerk + " ". 
      ELSE cl-list.bemerk = cl-list.bemerk + SUBSTR(res-line.bemerk, i, 1). 
    END. 
 
    cl-list.pax = STRING(cl-list.a,"9") + "/" + STRING(cl-list.c,"9") 
      + " " + STRING(cl-list.co,"9"). 
 
    IF cl-list.nat = "" THEN cl-list.nat = "?". 
    ELSE 
    DO: 
      FIND FIRST nation WHERE nation.kurzbez = cl-list.nat NO-LOCK NO-ERROR. 
      IF AVAILABLE nation THEN cl-list.nation = nation.bezeich. 
    END. 
 
    IF res-line.resstatus NE 13 THEN 
    DO: 
      IF AVAILABLE zimmer AND zimmer.sleeping THEN tot-rm = tot-rm + 1. 
      ELSE inactive = inactive + 1. 
    END. 
 
    tot-a = tot-a + res-line.erwachs. 
    tot-c = tot-c + res-line.kind1 + res-line.kind2. 
    tot-co = tot-co + res-line.gratis. 

    /* Naufal Afthar - 0430A4*/
    IF res-line.zimmer-wunsch MATCHES("*$CODE$*") THEN
    DO:
        s = SUBSTR(res-line.zimmer-wunsch, (INDEX(res-line.zimmer-wunsch, "$CODE$") + 6)).
        cl-list.ratecode = TRIM(ENTRY(1, s, ";")).
    END.
    FIND FIRST genstat WHERE genstat.resnr EQ res-line.resnr AND genstat.res-int[1] EQ res-line.reslinnr NO-LOCK NO-ERROR.
    IF AVAILABLE genstat THEN
    DO:
        MESSAGE "zipreis: " res-line.zipreis "lodging: " genstat.logis.
    END.
    cl-list.lodging = res-line.zipreis.
    /* end Naufal Afthar*/
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
    s-list.proz = s-list.adult / (tot-a + tot-co) * 100. 
  END. 
 
END. 
 
PROCEDURE shortstay-list: 
DEFINE VARIABLE i AS INTEGER. 
DEFINE VARIABLE vip-flag AS CHAR. 
DEFINE VARIABLE nr AS INTEGER INITIAL 0. 
DEFINE VARIABLE num-date AS INTEGER NO-UNDO.
DEFINE VAR s        AS CHAR. /* Naufal Afthar - 0430A4*/
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
 
  tot-avail = 0. 
  inactive = 0. 
 
  FOR EACH zimmer WHERE zimmer.sleeping = YES NO-LOCK: 
    tot-avail = tot-avail + 1. 
  END. 
  ASSIGN
    num-date = to-date - from-date /*FT update serverless*/
    tot-avail = tot-avail * (num-date + 1). 
 
  FOR EACH res-line WHERE res-line.active-flag LE 2 
    AND res-line.resstatus LE 8 
    AND res-line.resstatus NE 3 AND res-line.resstatus NE 4 
    AND (res-line.abreise - res-line.ankunft) LT long-stay 
    AND NOT res-line.ankunft GT to-date 
    AND NOT res-line.abreise LE from-date 
    AND res-line.erwachs GT 0 NO-LOCK, 
    FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr NO-LOCK, 
    FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
    FIRST guest WHERE guest.gastnr = reservation.gastnr NO-LOCK, 
    FIRST gmember WHERE gmember.gastnr = res-line.gastnrmember NO-LOCK 
    BY res-line.ankunft BY res-line.name: 
 
    FIND FIRST setup-list WHERE setup-list.nr = res-line.setup + 1. 
    FIND FIRST zimmer WHERE zimmer.zinr = res-line.zinr NO-LOCK NO-ERROR. 
 
    nr = nr + 1. 
    vip-flag = "". 
    /*FDL Comment
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
    */
    /*FDL: Optimasi for .py */
    FOR EACH guestseg WHERE guestseg.gastnr = gmember.gastnr NO-LOCK:       
        IF guestseg.segmentcode = vipnr1 THEN 
        DO:
            vip-flag = "VIP". 
            LEAVE.
        END.
        ELSE IF guestseg.segmentcode = vipnr2 THEN 
        DO:
            vip-flag = "VIP". 
            LEAVE.
        END.
        ELSE IF guestseg.segmentcode = vipnr3 THEN 
        DO:
            vip-flag = "VIP". 
            LEAVE.
        END.
        ELSE IF guestseg.segmentcode = vipnr4 THEN 
        DO:
            vip-flag = "VIP". 
            LEAVE.
        END.
        ELSE IF guestseg.segmentcode = vipnr5 THEN 
        DO:
            vip-flag = "VIP". 
            LEAVE.
        END.
        ELSE IF guestseg.segmentcode = vipnr6 THEN 
        DO:
            vip-flag = "VIP". 
            LEAVE.
        END.
        ELSE IF guestseg.segmentcode = vipnr7 THEN 
        DO:
            vip-flag = "VIP". 
            LEAVE.
        END.
        ELSE IF guestseg.segmentcode = vipnr8 THEN 
        DO:
            vip-flag = "VIP". 
            LEAVE.
        END.
        ELSE IF guestseg.segmentcode = vipnr9 THEN 
        DO:
            vip-flag = "VIP". 
            LEAVE.
        END.
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
      cl-list.resnr     = res-line.resnr 
      cl-list.vip       = vip-flag 
      cl-list.name      = res-line.name 
      cl-list.rmno      = res-line.zinr 
      cl-list.arrive    = res-line.ankunft 
      cl-list.depart    = res-line.abreise 
      cl-list.resstatus = STRING(res-line.resstatus) /*UPDATE cl-list restatus dari integer ke character RVN 22/12/2022*/
      cl-list.qty       = res-line.zimmeranz 
      cl-list.a         = res-line.erwachs 
      cl-list.c         = res-line.kind1 + res-line.kind2 
      cl-list.co        = res-line.gratis 
      cl-list.argt      = res-line.arrangement 
      cl-list.flight    = SUBSTR(res-line.flight-nr, 12, 6) 
      cl-list.etd       = SUBSTR(res-line.flight-nr, 18, 5) 
      cl-list.company   = guest.name + ", " + guest.vorname1 
        + " " + guest.anrede1 + guest.anredefirma. 
 
    IF cl-list.nat = "" THEN cl-list.nat = "?". 
 
    DO i = 1 TO length(res-line.bemerk): 
      IF SUBSTR(res-line.bemerk,i,1) = chr(10) THEN 
      cl-list.bemerk = cl-list.bemerk + " ". 
      ELSE cl-list.bemerk = cl-list.bemerk + SUBSTR(res-line.bemerk, i, 1). 
    END. 
 
    cl-list.pax = STRING(cl-list.a,"9") + "/" + STRING(cl-list.c,"9") 
      + " " + STRING(cl-list.co,"9"). 
 
    IF cl-list.nat = "" THEN cl-list.nat = "?". 
    ELSE 
    DO: 
      FIND FIRST nation WHERE nation.kurzbez = cl-list.nat NO-LOCK NO-ERROR. 
      IF AVAILABLE nation THEN cl-list.nation = nation.bezeich. 
    END. 
 
    IF res-line.resstatus NE 13 THEN 
    DO: 
      IF AVAILABLE zimmer AND zimmer.sleeping THEN tot-rm = tot-rm + 1. 
      ELSE inactive = inactive + 1. 
    END. 
 
    tot-a = tot-a + res-line.erwachs. 
    tot-c = tot-c + res-line.kind1 + res-line.kind2. 
    tot-co = tot-co + res-line.gratis. 

    /* Naufal Afthar - 0430A4*/
    IF res-line.zimmer-wunsch MATCHES("*$CODE$*") THEN
    DO:
        s = SUBSTR(res-line.zimmer-wunsch, (INDEX(res-line.zimmer-wunsch, "$CODE$") + 6)).
        cl-list.ratecode = TRIM(ENTRY(1, s, ";")).
    END.
    cl-list.lodging = res-line.zipreis.
    /* end Naufal Afthar*/
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
    s-list.proz = s-list.adult / (tot-a + tot-co) * 100. 
  END. 
 
END. 
