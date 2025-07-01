DEFINE TEMP-TABLE reslin-list LIKE res-line.
DEFINE TEMP-TABLE s-list 
  FIELD datum   AS DATE                     LABEL "Date" 
  FIELD tag     AS CHAR     FORMAT "x(3)"   LABEL "Day" 
  FIELD qty     AS INTEGER  FORMAT "->>>9"  LABEL "RmQty" 
  FIELD occ     AS INTEGER  FORMAT "->>>9"  LABEL "Occu" 
  FIELD vac     AS INTEGER  FORMAT "->>>9"  LABEL "avail" 
  FIELD ovb     AS INTEGER  FORMAT "->>>9"  LABEL "Overb". 

DEFINE INPUT PARAMETER i-case       AS INTEGER NO-UNDO.
DEFINE INPUT PARAMETER user-init    AS CHAR    NO-UNDO.
DEFINE INPUT PARAMETER TABLE        FOR reslin-list.
DEFINE OUTPUT PARAMETER overbook    AS INTEGER NO-UNDO.
DEFINE OUTPUT PARAMETER allotcode   AS CHAR NO-UNDO.
DEFINE INPUT-OUTPUT PARAMETER TABLE FOR s-list.

DEFINE VARIABLE curr-resnr       AS INTEGER NO-UNDO. 
DEFINE VARIABLE curr-reslinnr    AS INTEGER NO-UNDO. 
DEFINE VARIABLE kontignr         AS INTEGER NO-UNDO. 
DEFINE VARIABLE zikatnr          AS INTEGER NO-UNDO. 
DEFINE VARIABLE argt             AS CHAR    NO-UNDO. 
DEFINE VARIABLE erwachs          AS INTEGER NO-UNDO. 
DEFINE VARIABLE ankunft          AS DATE    NO-UNDO. 
DEFINE VARIABLE abreise          AS DATE    NO-UNDO. 
DEFINE VARIABLE qty              AS INTEGER NO-UNDO. 
DEFINE VARIABLE qty1             AS INTEGER NO-UNDO.

FIND FIRST reslin-list.
FIND FIRST bediener WHERE bediener.userinit = user-init NO-LOCK.

IF reslin-list.kontignr GT 0 THEN 
FIND FIRST kontline WHERE kontline.kontignr = reslin-list.kontignr 
    AND kontline.kontstatus = 1 NO-LOCK NO-ERROR. 
ELSE IF reslin-list.kontignr LT 0 THEN 
FIND FIRST kontline WHERE kontline.kontignr = - reslin-list.kontignr 
    AND kontline.kontstatus = 1 NO-LOCK NO-ERROR. 
IF NOT AVAILABLE kontline THEN RETURN.

ASSIGN
    overbook  = kontline.overbook
    allotcode = kontline.kontcode
.

IF i-case = 2 THEN
DO:
    IF reslin-list.kontignr GT 0 THEN RUN check-slist.
    ELSE IF reslin-list.kontignr LT 0 THEN RUN check-slist1.
    RETURN.
END.

ASSIGN
    curr-resnr      = reslin-list.resnr
    curr-reslinnr   = reslin-list.reslinnr
    kontignr        = reslin-list.kontignr
    zikatnr         = reslin-list.zikatnr
    argt            = reslin-list.arrangement
    erwachs         = reslin-list.erwachs
    ankunft         = reslin-list.ankunft
    abreise         = reslin-list.abreise
    qty             = reslin-list.zimmeranz
.
IF abreise = ankunft THEN abreise = ankunft + 1.
IF reslin-list.active-flag = 1 THEN /* inhouse */ 
    RUN htpdate.p(87, OUTPUT ankunft).
IF abreise = ankunft THEN RETURN.

IF kontignr GT 0 THEN RUN create-slist.
ELSE RUN create-slist1.

PROCEDURE create-slist: 
  DEFINE VARIABLE weekdays AS CHAR EXTENT 8  FORMAT "x(3)" 
    INITIAL ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"] NO-UNDO. 
  DEFINE VARIABLE d         AS DATE NO-UNDO. 
  DEFINE VARIABLE arrival   AS DATE NO-UNDO. 
  DEFINE VARIABLE depart    AS DATE NO-UNDO. 
  DEFINE BUFFER kline       FOR kontline. 
  qty1 = qty. 
  IF reslin-list.active-flag = 0 THEN 
  DO: 
    FIND FIRST res-line WHERE res-line.resnr = curr-resnr 
      AND res-line.reslinnr = curr-reslinnr NO-LOCK. 
    IF res-line.kontignr NE 0 THEN 
    DO:    
      FIND FIRST kline WHERE kline.gastnr = res-line.gastnr
        AND kline.kontignr = res-line.kontignr 
        AND kline.kontstatus = 1 NO-LOCK NO-ERROR.
      IF AVAILABLE kline AND kline.kontcode = kontline.kontcode THEN
        qty1 = qty - res-line.zimmeranz. 
    END.
  END. 
  DO d = ankunft TO abreise - 1: 
    CREATE s-list. 
    ASSIGN 
      s-list.datum = d 
      s-list.qty = kontline.zimmeranz 
      s-list.vac = kontline.zimmeranz 
      s-list.tag = weekdays[WEEKDAY(s-list.datum)]
      s-list.vac = s-list.vac - qty1
      s-list.occ = s-list.occ + qty1
    . 
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
  DEFINE VARIABLE qty1 AS INTEGER. 
  DEFINE buffer kline FOR kontline. 
  qty1 = qty. 
  IF reslin-list.active-flag = 0 THEN 
  DO: 
    FIND FIRST res-line WHERE res-line.resnr = curr-resnr 
      AND res-line.reslinnr = curr-reslinnr NO-LOCK. 
    qty1 = qty - res-line.zimmeranz. 
  END. 

  DO d = ankunft TO abreise - 1:
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
DEFINE VARIABLE anz             AS INTEGER NO-UNDO INITIAL 0. 
DEFINE VARIABLE d1              AS DATE    NO-UNDO. 
DEFINE VARIABLE i               AS INTEGER NO-UNDO INITIAL 0. 
DEFINE VARIABLE changed         AS LOGICAL NO-UNDO.  
DEFINE VARIABLE create-it       AS LOGICAL NO-UNDO.  

DEFINE BUFFER kline             FOR kontline. 
DEFINE BUFFER kline1            FOR kontline. 
DEFINE BUFFER kline2            FOR kontline. 
  
  FOR EACH s-list BY s-list.datum: 
    ASSIGN create-it = YES.
    FIND FIRST kline1 WHERE kline1.gastnr = kontline.gastnr
        AND kline1.kontcode     = kontline.kontcode
        AND kline1.zikatnr      = kontline.zikatnr
        AND kline1.arrangement  = kontline.arrangement
        AND kline1.ankunft LE s-list.datum
        AND kline1.abreise GE s-list.datum.
    IF s-list.qty NE kline1.zimmeranz THEN 
    DO: 
      changed = YES. 
      IF kline1.ankunft = s-list.datum
          AND kline1.abreise = s-list.datum THEN
      DO:
        ASSIGN 
            create-it        = NO
            kline1.zimmeranz = s-list.qty
        .
      END.
      ELSE IF kline1.ankunft = s-list.datum
          AND kline1.abreise GT s-list.datum THEN
          ASSIGN kline1.abreise   = s-list.datum + 1.
      ELSE IF kline1.abreise = s-list.datum THEN
          ASSIGN kline1.abreise   = s-list.datum - 1.
      ELSE 
      DO:
          FIND FIRST counters WHERE counters.counter-no = 10 EXCLUSIVE-LOCK. 
          counters.counter = counters.counter + 1. 
          FIND CURRENT counter NO-LOCK. 
          CREATE kline2. 
          BUFFER-COPY kline1 EXCEPT kontignr ankunft TO kline2.
          ASSIGN 
            kline2.kontignr      = counters.counter 
            kline2.ankunft       = s-list.datum + 1
            kline2.bediener-nr   = bediener.nr 
            kline2.resdat        = TODAY 
            kline2.bemerk        = kontline.bemerk
          . 
          ASSIGN kline1.abreise = s-list.datum - 1.
      END.
      IF create-it THEN
      DO:
          FIND FIRST counters WHERE counters.counter-no = 10 EXCLUSIVE-LOCK. 
          counters.counter = counters.counter + 1. 
          FIND CURRENT counter NO-LOCK. 
          CREATE kline. 
          BUFFER-COPY kline1 EXCEPT kontignr ankunft abreise TO kline.
          ASSIGN 
            kline.kontignr      = counters.counter 
            kline.useridanlage  = "" 
            kline.ankunft       = s-list.datum 
            kline.abreise       = s-list.datum 
            kline.zimmeranz     = s-list.qty
            kline.bediener-nr   = bediener.nr 
            kline.resdat        = TODAY 
            kline.bemerk        = kontline.bemerk
          . 
      END.
    END. 
  END. 
  
  IF changed THEN
  DO:
    FIND FIRST queasy WHERE queasy.KEY = 147 AND queasy.number1 = kontline.gastnr
      NO-LOCK NO-ERROR.
    IF AVAILABLE queasy THEN
    FOR EACH kline WHERE kline.gastnr = kontline.gastnr
      AND kline.kontstatus = 1
      AND kline.kontcode = kontline.kontcode
      AND RECID(kline) NE RECID(kontline):
      kline.pr-code = queasy.char3.
    END.
  END.
END. 

PROCEDURE check-slist1: 
DEFINE BUFFER kline             FOR kontline.   
  FOR EACH s-list: 
    FIND FIRST kline WHERE kline.kontcode = kontline.kontcode 
      AND kline.ankunft = s-list.datum NO-LOCK NO-ERROR.
    IF AVAILABLE kline AND kline.zimmeranz LT s-list.qty THEN 
    DO: 
      FIND CURRENT kline EXCLUSIVE-LOCK. 
      ASSIGN kline.zimmeranz = s-list.qty. 
      FIND CURRENT kline NO-LOCK. 
    END. 
  END. 
END. 


/*
DEFINE TEMP-TABLE t-kontline LIKE kontline.
DEFINE TEMP-TABLE s-list 
  FIELD datum   AS DATE LABEL "Date" 
  FIELD tag     AS CHAR FORMAT "x(3)" LABEL "Day" 
  FIELD qty     AS INTEGER FORMAT "->>>9" LABEL "RmQty" 
  FIELD occ     AS INTEGER FORMAT "->>>9" LABEL "Occu" 
  FIELD vac     AS INTEGER FORMAT "->>>9" LABEL "avail" 
  FIELD ovb     AS INTEGER FORMAT "->>>9" LABEL "Overb". 

DEF INPUT PARAMETER kontigNo AS INTEGER NO-UNDO.
DEF INPUT PARAMETER user-init AS CHAR.
DEF INPUT PARAMETER TABLE FOR t-kontline.
DEF INPUT PARAMETER TABLE FOR s-list.

DEF BUFFER kline FOR kontline. 

FIND FIRST bediener WHERE bediener.userinit = user-init NO-ERROR.
FIND FIRST t-kontline NO-ERROR.
FIND FIRST s-list NO-ERROR.
DO WHILE AVAILABLE s-list:
    FIND NEXT s-list NO-ERROR.
END.
IF kontignr GT 0 THEN RUN check-slist.
ELSE RUN check-slist1.

PROCEDURE check-slist: 
DEFINE VARIABLE changed         AS LOGICAL INITIAL NO. 
DEFINE VARIABLE anz             AS INTEGER INITIAL 0. 
DEFINE VARIABLE d1              AS DATE. 
DEFINE VARIABLE i               AS INTEGER INITIAL 0. 
  
  FOR EACH s-list: 
    i = i + 1. 
    IF anz = 0 THEN 
    DO: 
      anz = s-list.qty. 
      d1 = s-list.datum. 
    END. 
    IF s-list.qty NE anz THEN 
    DO: 
      changed = YES. 
      FIND FIRST counters WHERE counters.counter-no = 10 EXCLUSIVE-LOCK. 
      counters.counter = counters.counter + 1. 
      FIND CURRENT counter NO-LOCK. 
      CREATE kline. 
      ASSIGN 
        kline.betriebsnr    = INTEGER(kontignr LT 0) 
        kline.kontignr      = counters.counter 
        kline.gastnr        = t-kontline.gastnr 
        kline.useridanlage  = "" 
        kline.kontcode      = t-kontline.kontcode 
        kline.ankunft       = d1 
        kline.abreise       = s-list.datum - 1 
        kline.zikatnr       = t-kontline.zikatnr 
        kline.arrangement   = t-kontline.arrangement 
        kline.zimmeranz     = anz 
        kline.erwachs       = t-kontline.erwachs 
        kline.kind1         = t-kontline.kind1 
        kline.overbooking   = t-kontline.overbooking 
        kline.ruecktage     = t-kontline.ruecktage 
        kline.rueckdatum    = t-kontline.rueckdatum 
        kline.ansprech      = t-kontline.ansprech 
        kline.bediener-nr   = bediener.nr 
        kline.resdat        = TODAY 
        kline.bemerk        = t-kontline.bemerk
        d1                  = s-list.datum. 
        anz                 = s-list.qty
      . 
    END. 
  END. 
  IF changed THEN 
  DO: 
    FIND FIRST kline WHERE kline.gastnr = t-kontline.gastnr
      AND kline.kontignr = t-kontline.kontignr
      AND kline.kontcode = t-kontline.kontcode EXCLUSIVE-LOCK.
    ASSIGN 
      kline.ankunft = d1 
      kline.zimmeranz = anz. 
    FIND CURRENT kline NO-LOCK. 
  END. 
  ELSE IF i = 1 THEN 
  DO: 
    FIND FIRST kline WHERE kline.gastnr = t-kontline.gastnr
      AND kline.kontignr = t-kontline.kontignr
      AND kline.kontcode = t-kontline.kontcode EXCLUSIVE-LOCK.
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
  FOR EACH s-list: 
    FIND FIRST kline WHERE kline.kontcode = t-kontline.kontcode 
      AND kline.ankunft = s-list.datum NO-LOCK NO-ERROR.
    IF AVAILABLE kline AND kline.zimmeranz LT s-list.qty THEN 
    DO: 
      FIND CURRENT kline EXCLUSIVE-LOCK. 
      ASSIGN kline.zimmeranz = s-list.qty. 
      FIND CURRENT kline NO-LOCK. 
    END. 
  END. 
END. 
*/
