 
 
DEFINE INPUT PARAMETER pvILanguage      AS INTEGER NO-UNDO.
DEFINE INPUT PARAMETER res-mode         AS CHAR. 
DEFINE INPUT PARAMETER curr-resnr       AS INTEGER. 
DEFINE INPUT PARAMETER curr-reslinnr    AS INTEGER. 
DEFINE INPUT PARAMETER kontignr         AS INTEGER. 
DEFINE INPUT PARAMETER zikatnr          AS INTEGER. 
DEFINE INPUT PARAMETER bed-setup        AS INTEGER. 
DEFINE INPUT PARAMETER argt             AS CHAR. 
DEFINE INPUT PARAMETER erwachs          AS INTEGER. 
DEFINE INPUT PARAMETER ankunft          AS DATE. 
DEFINE INPUT PARAMETER abreise          AS DATE. 
DEFINE INPUT PARAMETER qty              AS INTEGER. 
DEFINE INPUT PARAMETER user-init        AS CHAR. 

DEFINE OUTPUT PARAMETER error-flag      AS LOGICAL INITIAL NO. 
DEFINE OUTPUT PARAMETER msg-str         AS CHAR INITIAL "".

/*
DEFINE VARIABLE res-mode AS CHAR INITIAL "modify". 
DEFINE VARIABLE curr-resnr AS INTEGER INITIAL 17. 
DEFINE VARIABLE curr-reslinnr AS INTEGER INITIAL 1. 
DEFINE VARIABLE kontignr AS INTEGER INITIAL 9. 
DEFINE VARIABLE bed-setup AS INTEGER INITIAL 1. 
DEFINE VARIABLE zikatnr AS INTEGER INITIAL 1. 
DEFINE VARIABLE argt AS CHAR INITIAL "BB$". 
DEFINE VARIABLE erwachs AS INTEGER INITIAL 2. 
DEFINE VARIABLE ankunft AS DATE INITIAL 08/01/09. 
DEFINE VARIABLE abreise AS DATE INITIAL 08/04/09. 
DEFINE VARIABLE qty AS INTEGER INITIAL 4. 
DEFINE VARIABLE error-flag AS LOGICAL. 
DEFINE VARIABLE user-init AS CHAR INITIAL "01". 
RUN add-persist-procedure. 
PROCEDURE add-persist-procedure: 
    DEFINE VARIABLE lvHS AS HANDLE              NO-UNDO. 
    DEFINE VARIABLE lvI AS INTEGER              NO-UNDO. 
    DEFINE VARIABLE lFound AS LOGICAL INIT FALSE    NO-UNDO. 
 
    DO lvI = 1 TO NUM-ENTRIES(SESSION:SUPER-PROCEDURES): 
        lvHS = WIDGET-HANDLE(ENTRY(lvI, SESSION:SUPER-PROCEDURES)). 
        IF VALID-HANDLE(lvHS) THEN DO: 
            IF lvHS:NAME BEGINS "supertrans" THEN 
                lFound = TRUE. 
        END. 
    END. 
 
    IF NOT lFound THEN DO: 
        RUN supertrans.p PERSISTENT SET lvHS. 
        SESSION:ADD-SUPER-PROCEDURE(lvHS). 
    END. 
END. 
*/ 

{supertransBL.i} 
DEF VAR lvCAREA AS CHAR INITIAL "allot-overbook". 

DEFINE VARIABLE cutoff-date     AS DATE NO-UNDO.
DEFINE VARIABLE changed         AS LOGICAL. 
DEFINE VARIABLE ci-date         AS DATE. 
DEFINE VARIABLE overbook        AS INTEGER. 

DEFINE BUFFER kline FOR kontline. 
 
DEFINE WORKFILE allot-list 
  FIELD k-recid AS INTEGER 
  FIELD datum AS DATE 
  FIELD allot-exist AS LOGICAL INITIAL NO 
  FIELD anz AS INTEGER 
  FIELD overbook AS INTEGER 
  FIELD cutoff AS INTEGER. 
 
DEFINE WORKFILE s-list 
  FIELD datum AS DATE LABEL "Date" 
  FIELD tag AS CHAR FORMAT "x(3)" LABEL "Day" 
  FIELD qty AS INTEGER FORMAT "->>>9" LABEL "RmQty" 
  FIELD occ AS INTEGER FORMAT "->>>9" LABEL "Occu" 
  FIELD vac AS INTEGER FORMAT "->>>9" LABEL "avail" 
  FIELD ovb AS INTEGER FORMAT "->>>9" LABEL "Overb". 
 
DEFINE VARIABLE datum       AS DATE. 
DEFINE VARIABLE error-code  AS INTEGER INITIAL 0. 
DEFINE VARIABLE qty1        AS INTEGER. 
DEFINE VARIABLE answer      AS LOGICAL INITIAL NO. 
 
FIND FIRST bediener WHERE bediener.userinit = user-init NO-LOCK. 
 
FIND FIRST htparam WHERE paramnr = 87 NO-LOCK. 
ci-date = htparam.fdate. 
 
IF kontignr GT 0 THEN 
DO: 
  FIND FIRST kontline WHERE kontline.kontignr = kontignr 
    AND kontline.kontstatus = 1 NO-LOCK NO-ERROR. 
  IF NOT AVAILABLE kontline THEN 
  DO: 
    error-flag = YES. 
    msg-str = translateExtended ("Allotment does not exist.",lvCAREA,"").
    RETURN. 
  END. 
END. 
 
ELSE IF kontignr LT 0 THEN 
DO: 
  FIND FIRST kontline WHERE kontline.kontignr = - kontignr 
     AND kontline.kontstatus = 1 NO-LOCK NO-ERROR. 
  IF NOT AVAILABLE kontline THEN 
  DO: 
    error-flag = YES. 
    msg-str = translateExtended ("Global Reservation does not exist.",lvCAREA,"").
    RETURN. 
  END. 
END. 
 
IF (kontignr GT 0) AND (kontline.erwachs NE 0) AND 
    (kontline.erwachs LT erwachs) THEN 
DO: 
  error-flag = YES. 
  msg-str = translateExtended ("Number of adults does not match to selected AllotNo :",lvCAREA,"") 
    + STRING(kontline.kontignr). 
  RETURN. 
END. 
 
IF kontline.zikatnr NE 0 AND (kontline.zikatnr NE zikatnr) THEN 
DO: 
DEFINE VARIABLE res-overbook    AS LOGICAL.
DEFINE VARIABLE overmax         AS LOGICAL INITIAL NO.
DEFINE VARIABLE overanz         AS INTEGER.
DEFINE VARIABLE overdate        AS DATE.
DEFINE VARIABLE incl-allot      AS LOGICAL.
DEF VAR zimkateg-overbook AS INT.
  overmax = NO.
  IF SUBSTR(bediener.perm, 36, 1) GE "1" THEN
  DO:
    FIND FIRST zimkateg WHERE zimkateg.zikatnr = kontline.zikatnr NO-LOCK.
    RUN res-overbookbl.p(pvILanguage, res-mode, curr-resnr, curr-reslinnr, ankunft, abreise,
      qty, zimkateg.kurzbez, bed-setup, NO, OUTPUT res-overbook, OUTPUT overmax,
      OUTPUT overanz, OUTPUT overdate, OUTPUT incl-allot, OUTPUT msg-str,
      OUTPUT zimkateg-overbook).
  END.
  IF NOT overmax THEN
  DO:
    error-flag = YES. 
    msg-str = translateExtended ("Room Type does not match to selected Code :",lvCAREA,"") 
      + STRING(kontline.kontignr). 
    RETURN.
  END.
END. 
 
IF kontline.arrangement NE "" AND kontline.arrangement NE argt THEN 
DO: 
  error-flag = YES. 
  msg-str = translateExtended ("Arrangement does not match to selected Code :",lvCAREA,"") 
    + STRING(kontline.kontignr). 
  RETURN. 
END. 
 
IF res-mode = "inhouse" AND kontignr GT 0 THEN RETURN. 
 
RUN check-allotment. 
 
PROCEDURE check-allotment: 
DEFINE VARIABLE anz   AS INTEGER. 
DEFINE VARIABLE datum AS DATE. 
DEFINE BUFFER kline   FOR kontline. 
  
  FIND FIRST res-line WHERE res-line.resnr = curr-resnr 
    AND res-line.reslinnr = curr-reslinnr NO-LOCK. 
 
  DO datum = ankunft TO (abreise - 1): 
    CREATE allot-list. 
    allot-list.datum = datum. 
    FIND FIRST kline WHERE kline.kontcode = kontline.kontcode AND kline.kontstatus = 1 
      AND datum GE kline.ankunft AND datum LE kline.abreise 
      NO-LOCK NO-ERROR. 
    IF AVAILABLE kline AND kline.rueckdatum NE ? 
      AND ci-date GT kline.rueckdatum 
      AND (res-mode = "new" OR res-mode = "insert") THEN 
    DO: 
      error-flag = YES. 
      msg-str = translateExtended ("Today's date is beyond allotment's Cut-Off-Date :",lvCAREA,"") 
        + STRING(kline.rueckdatum). 
      RETURN. 
    END. 
    IF AVAILABLE kline AND kline.ruecktage GT 0 
      AND (datum - ci-date) LT kline.ruecktage 
      AND (res-mode = "new" OR res-mode = "insert") THEN 
    DO: 
      error-flag = YES. 
      msg-str = translateExtended ("Arrival less than allotment's Cut-Off-Days :",lvCAREA,"") 
        + STRING(kline.ruecktage). 
      RETURN. 
    END. 
    IF AVAILABLE kline THEN 
    DO: 
      IF res-mode = "inhouse" THEN anz = 0. 
      ELSE IF res-mode = "modify" OR res-mode = "new" THEN 
      DO: 
        IF res-line.kontignr LT 0 THEN anz = 0. 
        ELSE anz = kline.ruecktage. 
      END. 
      IF /* res-mode = "inhouse" AND */ datum GE (ci-date + anz) THEN 
      DO: 
        ASSIGN 
          allot-list.allot-exist = YES 
          allot-list.k-recid = RECID(kline) 
          allot-list.anz = kline.zimmeranz - qty 
          allot-list.overbook = kline.overbooking 
          allot-list.cutoff = kline.ruecktage. 
      END. 
    END. 
  END. 
  FIND FIRST allot-list WHERE NOT allot-list.allot-exist NO-ERROR. 
  IF AVAILABLE allot-list THEN 
  DO: 
    error-flag = YES. 
    msg-str = translateExtended ("Date out of period range found",lvCAREA,"") + " - " + 
      STRING(allot-list.datum). 
    RETURN. 
  END. 
 
  IF kontignr GT 0 THEN 
  DO:
    FIND FIRST queasy WHERE queasy.KEY = 147 AND queasy.number1 = kontline.gastnr
      NO-LOCK NO-ERROR.
    IF NOT AVAILABLE queasy THEN
    FOR EACH res-line WHERE res-line.kontignr GT 0 
      AND res-line.gastnr = kontline.gastnr 
      AND res-line.active-flag LT 2 AND res-line.resstatus LE 6 NO-LOCK, 
      FIRST kline WHERE kline.kontignr = res-line.kontignr 
      AND kline.kontcode = kontline.kontcode AND kline.kontstatus = 1 NO-LOCK: 
      IF res-line.resnr = curr-resnr AND res-line.reslinnr = curr-reslinnr THEN . 
      ELSE 
      DO datum = res-line.ankunft TO (res-line.abreise - 1): 
        FIND FIRST allot-list WHERE allot-list.datum = datum NO-ERROR. 
        IF AVAILABLE allot-list THEN 
          allot-list.anz = allot-list.anz - res-line.zimmeranz. 
      END.
    END.
    ELSE /* global allotment */
    FOR EACH res-line WHERE res-line.kontignr GT 0 
      AND res-line.active-flag LT 2 AND res-line.resstatus LE 6 NO-LOCK, 
      FIRST kline WHERE kline.kontignr = res-line.kontignr 
      AND kline.kontcode = kontline.kontcode AND kline.kontstatus = 1 NO-LOCK: 
      IF res-line.resnr = curr-resnr AND res-line.reslinnr = curr-reslinnr THEN . 
      ELSE 
      DO datum = res-line.ankunft TO (res-line.abreise - 1): 
        FIND FIRST allot-list WHERE allot-list.datum = datum NO-ERROR. 
        IF AVAILABLE allot-list THEN 
          allot-list.anz = allot-list.anz - res-line.zimmeranz. 
      END.
    END.
  END. 
  
  ELSE IF kontignr LT 0 THEN 
  FOR EACH res-line WHERE res-line.kontignr LT 0 
    AND res-line.active-flag LT 2 AND res-line.resstatus LE 6 
    AND res-line.resstatus NE 3 AND res-line.resstatus NE 4 NO-LOCK, 
    FIRST kline WHERE kline.kontignr = - res-line.kontignr 
    AND kline.kontcode = kontline.kontcode AND kline.kontstatus = 1 NO-LOCK: 
    IF res-line.resnr = curr-resnr AND res-line.reslinnr = curr-reslinnr THEN . 
    ELSE 
    DO datum = res-line.ankunft TO (res-line.abreise - 1): 
      FIND FIRST allot-list WHERE allot-list.datum = datum NO-ERROR. 
      IF AVAILABLE allot-list THEN 
        allot-list.anz = allot-list.anz - res-line.zimmeranz. 
    END. 
  END. 
 
  FIND FIRST allot-list WHERE (allot-list.anz + allot-list.overbook) LT 0 
    NO-ERROR. 
  IF AVAILABLE allot-list THEN 
  DO: 
    error-flag = YES. 
    IF res-mode = "inhouse" THEN cutoff-date = ci-date.
    ELSE cutoff-date = ankunft - allot-list.cutoff.

    IF kontignr GT 0 THEN 
    msg-str = translateExtended ("Allotment: Overbooking found on :",lvCAREA,"") + STRING(allot-list.datum) 
      + CHR(10)
      + translateExtended ("Cut-off Date :",lvCAREA,"") + STRING(cutoff-date) 
      + CHR(10)
      + translateExtended ("Maxium Overbooking :",lvCAREA,"") + STRING(allot-list.overbook) + "  " 
      + translateExtended ("Actual Overbooking :",lvCAREA,"") + STRING(- allot-list.anz).
    
    ELSE IF kontignr LT 0 THEN 
    msg-str = translateExtended ("Global Reservation: Overbooking found on :",lvCAREA,"") 
      + STRING(allot-list.datum)
      + CHR(10)
      + translateExtended ("Maxium Overbooking :",lvCAREA,"") + STRING(allot-list.overbook) + "  " 
      + translateExtended ("Actual Overbooking :",lvCAREA,"") + STRING(- allot-list.anz).
    
    IF SUBSTR(bediener.perm, 36, 1) GE "2" THEN 
      msg-str = msg-str + CHR(2) + "&Q" 
        + translateExtended ("Do you wish to modify the record?",lvCAREA,"").
    RETURN.
  END. 
 
  FIND FIRST allot-list WHERE allot-list.anz LT 0 NO-ERROR. 
  IF AVAILABLE allot-list THEN 
  DO: 
    IF kontignr GT 0 THEN 
    msg-str = "&W"
      + (translateExtended ("Allotment: Overbooking = ",lvCAREA,"") + STRING(- allot-list.anz) 
      + " - " + STRING(allot-list.datum)) + "\".
    ELSE IF kontignr LT 0 THEN 
    msg-str = "&W"
      + (translateExtended ("Global Reservation: Overbooking = ",lvCAREA,"") + STRING(- allot-list.anz) 
      + " - " + STRING(allot-list.datum)) + "\".
  END. 
END. 
 
PROCEDURE create-slist: 
  DEFINE VARIABLE weekdays AS CHAR EXTENT 8  FORMAT "x(3)" 
    INITIAL ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]. 
  DEFINE VARIABLE d         AS DATE. 
  DEFINE VARIABLE arrival   AS DATE. 
  DEFINE VARIABLE depart    AS DATE. 
  DEFINE BUFFER kline       FOR kontline. 
  qty1 = qty. 
  IF res-mode = "modify" THEN 
  DO: 
    FIND FIRST res-line WHERE res-line.resnr = curr-resnr 
      AND res-line.reslinnr = curr-reslinnr NO-LOCK. 
    IF res-line.kontignr NE 0 THEN 
    DO:    
      FIND FIRST kline WHERE kline.kontignr = res-line.kontignr 
        AND kline.kontstatus = 1 NO-LOCK NO-ERROR.
      IF AVAILABLE kline AND kline.kontcode = kontline.kontcode THEN
        qty1 = qty - res-line.zimmeranz. 
    END.
  END. 
  DO d = kontline.ankunft TO kontline.abreise: 
    create s-list. 
    ASSIGN 
      s-list.datum = d 
      s-list.qty = kontline.zimmeranz 
      s-list.vac = kontline.zimmeranz 
      s-list.tag = weekdays[weekday(s-list.datum)]. 
   IF d GE ankunft AND d LE (abreise - 1) THEN 
   DO: 
     s-list.vac = s-list.vac - qty1. 
     s-list.occ = s-list.occ + qty1. 
   END. 
  END. 
 
  FIND FIRST queasy WHERE queasy.KEY = 147 AND queasy.number1 = kontline.gastnr
    NO-LOCK NO-ERROR.
  IF NOT AVAILABLE queasy THEN
  FOR EACH res-line WHERE res-line.kontignr GT 0 
      AND res-line.gastnr = kontline.gastnr AND res-line.active-flag LE 1
      AND res-line.resstatus LE 6 NO-LOCK, 
      FIRST kline WHERE kline.kontignr = res-line.kontignr 
      AND kline.kontcode = kontline.kontcode AND kline.kontstatus = 1 NO-LOCK: 
      IF res-line.resnr = curr-resnr AND res-line.reslinnr = curr-reslinnr THEN 
      ASSIGN 
        arrival = ankunft 
        depart  = abreise
      . 
      ELSE 
      ASSIGN 
        arrival = res-line.ankunft 
        depart  = res-line.abreise
      . 
      IF depart LE kontline.ankunft 
      OR arrival GT kontline.abreise THEN . 
      ELSE 
      DO d = arrival TO (depart - 1): 
        FIND FIRST s-list WHERE s-list.datum = d NO-ERROR. 
        IF AVAILABLE s-list THEN 
        ASSIGN 
          s-list.vac = s-list.vac - res-line.zimmeranz 
          s-list.occ = s-list.occ + res-line.zimmeranz
        . 
      END.
  END.
  ELSE /* global allotment */
  FOR EACH res-line WHERE res-line.kontignr GT 0 
      AND res-line.active-flag LE 1
      AND res-line.resstatus LE 6 NO-LOCK, 
      FIRST kline WHERE kline.kontignr = res-line.kontignr 
      AND kline.kontcode = kontline.kontcode AND kline.kontstatus = 1 NO-LOCK: 
      IF res-line.resnr = curr-resnr AND res-line.reslinnr = curr-reslinnr THEN 
      ASSIGN 
        arrival = ankunft 
        depart  = abreise
      . 
      ELSE 
      ASSIGN 
        arrival = res-line.ankunft 
        depart  = res-line.abreise
      . 
      IF depart LE kontline.ankunft 
      OR arrival GT kontline.abreise THEN . 
      ELSE 
      DO d = arrival TO (depart - 1): 
        FIND FIRST s-list WHERE s-list.datum = d NO-ERROR. 
        IF AVAILABLE s-list THEN 
        ASSIGN 
          s-list.vac = s-list.vac - res-line.zimmeranz 
          s-list.occ = s-list.occ + res-line.zimmeranz
        . 
      END. 
  END. 
 
  FOR EACH s-list WHERE s-list.vac LT 0: 
    s-list.ovb = - s-list.vac. 
    s-list.vac = 0. 
  END. 
END. 
 
PROCEDURE create-slist1: 
  DEFINE VARIABLE weekdays AS CHAR EXTENT 8  FORMAT "x(3)" 
    INITIAL ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]. 
  DEFINE VARIABLE d AS DATE. 
  DEFINE VARIABLE arrival AS DATE. 
  DEFINE VARIABLE depart AS DATE. 
  DEFINE buffer kline FOR kontline. 
  qty1 = qty. 
  IF res-mode = "modify" THEN 
  DO: 
    FIND FIRST res-line WHERE res-line.resnr = curr-resnr 
      AND res-line.reslinnr = curr-reslinnr NO-LOCK. 
    qty1 = qty - res-line.zimmeranz. 
  END. 

  DO d = ankunft TO abreise:
    FIND FIRST kline WHERE kline.kontcode = kontline.kontcode 
      AND kline.ankunft = d NO-LOCK NO-ERROR.
    IF AVAILABLE kline THEN
    DO:
      CREATE s-list. 
      ASSIGN 
        s-list.datum = d 
        s-list.qty = kline.zimmeranz 
        s-list.vac = kline.zimmeranz - qty1
        s-list.tag = weekdays[WEEKDAY(s-list.datum)]
        s-list.occ = qty1
      . 
    END. 
  END. 
 
  FOR EACH res-line WHERE res-line.kontignr LT 0 
    AND res-line.gastnr = kontline.gastnr AND res-line.active-flag LE 1 
    AND res-line.resstatus LE 6 NO-LOCK, 
    FIRST kline WHERE kline.kontignr = - res-line.kontignr 
    AND kline.kontcode = kontline.kontcode AND kline.kontstatus = 1 NO-LOCK: 
    IF res-line.resnr = curr-resnr AND res-line.reslinnr = curr-reslinnr THEN 
    DO: 
      arrival = ankunft. 
      depart = abreise. 
    END. 
    ELSE 
    DO: 
      arrival = res-line.ankunft. 
      depart = res-line.abreise. 
    END. 
    DO d = arrival TO (depart - 1): 
      FIND FIRST s-list WHERE s-list.datum = d NO-ERROR. 
      IF AVAILABLE s-list THEN 
      DO: 
        s-list.vac = s-list.vac - res-line.zimmeranz. 
        s-list.occ = s-list.occ + res-line.zimmeranz. 
      END. 
    END. 
  END. 
 
  FOR EACH s-list WHERE s-list.vac LT 0: 
    s-list.ovb = - s-list.vac. 
    s-list.vac = 0. 
  END. 
END. 
 
PROCEDURE check-slist: 
DEFINE OUTPUT PARAMETER changed AS LOGICAL INITIAL NO. 
DEFINE VARIABLE anz             AS INTEGER INITIAL 0. 
DEFINE VARIABLE d1              AS DATE. 
DEFINE VARIABLE i               AS INTEGER INITIAL 0. 
DEFINE BUFFER s-list1           FOR s-list. 
DEFINE BUFFER kline             FOR kontline. 
  
  FOR EACH s-list1: 
    i = i + 1. 
    IF anz = 0 THEN 
    DO: 
      anz = s-list1.qty. 
      d1 = s-list1.datum. 
    END. 
    IF s-list1.qty NE anz THEN 
    DO: 
      changed = YES. 
      FIND FIRST counters WHERE counters.counter-no = 10 EXCLUSIVE-LOCK. 
      counters.counter = counters.counter + 1. 
      FIND CURRENT counter NO-LOCK. 
      create kline. 
      ASSIGN 
        kline.betriebsnr = INTEGER(kontignr LT 0) 
        kline.kontignr = counters.counter 
        kline.gastnr = kontline.gastnr 
        kline.useridanlage = "" 
        kline.kontcode = kontline.kontcode 
        kline.ankunft = d1 
        kline.abreise = s-list1.datum - 1 
        kline.zikatnr = kontline.zikatnr 
        kline.arrangement = kontline.arrangement 
        kline.zimmeranz = anz 
        kline.erwachs = kontline.erwachs 
        kline.kind1 = kontline.kind1 
        kline.overbooking = kontline.overbooking 
        kline.ruecktage = kontline.ruecktage 
        kline.rueckdatum = kontline.rueckdatum 
        kline.ansprech = kontline.ansprech 
        kline.bediener-nr = bediener.nr 
        kline.resdat = today 
        kline.bemerk = kontline.bemerk. 
      d1 = s-list1.datum. 
      anz = s-list1.qty. 
    END. 
  END. 
  IF changed THEN 
  DO: 
    FIND FIRST kline WHERE RECID(kline) = RECID(kontline) EXCLUSIVE-LOCK. 
    ASSIGN 
      kline.ankunft = d1 
      kline.zimmeranz = anz. 
    FIND CURRENT kline NO-LOCK. 
  END. 
  ELSE IF i = 1 THEN 
  DO: 
    FIND FIRST kline WHERE RECID(kline) = RECID(kontline) NO-LOCK. 
    IF kline.zimmeranz NE anz THEN 
    DO: 
      changed = YES. 
      FIND CURRENT kline EXCLUSIVE-LOCK. 
      ASSIGN 
        kline.ankunft = d1 
        kline.zimmeranz = anz. 
      FIND CURRENT kline NO-LOCK. 
    END. 
  END. 
END. 

PROCEDURE check-slist1: 
DEFINE OUTPUT PARAMETER changed AS LOGICAL INITIAL NO. 
DEFINE BUFFER s-list1           FOR s-list. 
DEFINE BUFFER kline             FOR kontline.   
  FOR EACH s-list1: 
    FIND FIRST kline WHERE kline.kontcode = kontline.kontcode 
      AND kline.ankunft = s-list1.datum NO-LOCK NO-ERROR.
    IF AVAILABLE kline AND kline.zimmeranz LT s-list1.qty THEN 
    DO: 
      changed = YES. 
      FIND CURRENT kline EXCLUSIVE-LOCK. 
      ASSIGN kline.zimmeranz = s-list1.qty. 
      FIND CURRENT kline NO-LOCK. 
    END. 
  END. 
END. 
