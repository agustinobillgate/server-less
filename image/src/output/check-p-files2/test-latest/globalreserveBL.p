DEFINE TEMP-TABLE allot-list 
  FIELD datum AS DATE 
  FIELD anz AS INTEGER. 
DEFINE WORKFILE z-list LIKE zimkateg. 
DEFINE TEMP-TABLE k-list LIKE kontline.

DEFINE TEMP-TABLE globalreserve-list
    FIELD kontcode      LIKE kontline.kontcode
    FIELD ankunft       LIKE kontline.ankunft
    FIELD abreise       LIKE kontline.abreise
    FIELD kurzbez       LIKE z-list.kurzbez
    FIELD arrangement   LIKE kontline.arrangement
    FIELD zimmeranz     LIKE kontline.zimmeranz
    FIELD erwachs       LIKE kontline.erwachs
    FIELD kind1         LIKE kontline.kind1
    FIELD kind2         LIKE kontline.kind2
    FIELD userinit      LIKE bediener.userinit
    FIELD useridanlage  LIKE kontline.useridanlage
    FIELD resdat        LIKE kontline.resdat
    FIELD ansprech      LIKE kontline.ansprech
    FIELD bemerk        LIKE kontline.bemerk
    FIELD kontignr      LIKE kontline.kontignr
    FIELD zikatnr       LIKE kontline.zikatnr
    FIELD overbooking   LIKE kontline.overbooking
    FIELD ruecktage     LIKE kontline.ruecktage
    FIELD rueckdatum    LIKE kontline.rueckdatum.

DEFINE INPUT  PARAMETER case-type   AS INTEGER  NO-UNDO.
DEFINE INPUT  PARAMETER TABLE FOR k-list. 
DEFINE INPUT  PARAMETER rmcat       AS CHAR     NO-UNDO.
DEFINE INPUT  PARAMETER gastnr      AS INTEGER  NO-UNDO.
DEFINE INPUT  PARAMETER curr-mode   AS CHAR     NO-UNDO.
DEFINE INPUT  PARAMETER last-code   AS CHAR     NO-UNDO.
DEFINE INPUT  PARAMETER argt        AS CHAR     NO-UNDO.
DEFINE INPUT  PARAMETER comments    AS CHAR     NO-UNDO.
DEFINE INPUT  PARAMETER user-init   AS CHAR     NO-UNDO.

DEFINE OUTPUT PARAMETER msg-int     AS INT      NO-UNDO.
DEFINE OUTPUT PARAMETER TABLE FOR globalreserve-list.
DEFINE OUTPUT PARAMETER TABLE FOR allot-list.


DEFINE VARIABLE katnr AS INTEGER INITIAL 0  NO-UNDO.
DEFINE VARIABLE ok    AS LOGICAL            NO-UNDO.
DEFINE VARIABLE ERROR AS LOGICAL            NO-UNDO.
DEFINE buffer kline FOR kontline.


IF case-type = 2 THEN
DO:
    RUN create-zlist.
    RUN open-query.
    RETURN NO-APPLY.
END.

FIND FIRST bediener WHERE bediener.userinit = user-init NO-LOCK. 
FIND FIRST k-list.

  IF k-list.kontcode = "" OR k-list.ankunft = ? 
    OR k-list.abreise = ? OR k-list.zimmeranz = 0 THEN 
  DO:
    msg-int = 1.
    RETURN NO-APPLY. 
  END. 
 
  IF k-list.abreise LT k-list.ankunft THEN 
  DO:
    msg-int = 2.
    RETURN NO-APPLY. 
  END. 
 
  FIND FIRST zimkateg WHERE zimkateg.kurzbez = rmcat 
    NO-LOCK NO-ERROR. 
  IF NOT AVAILABLE zimkateg THEN 
  DO:
    msg-int = 3.
    RETURN NO-APPLY. 
  END. 
  katnr = zimkateg.zikatnr. 
 
  FIND FIRST kline WHERE kline.gastnr = gastnr AND kline.betriebsnr = 1 
    AND kline.kontcode = k-list.kontcode AND kline.kontignr NE k-list.kontignr 
    AND kline.zikatnr NE katnr AND kline.kontstat = 1 NO-LOCK NO-ERROR. 
  IF AVAILABLE kline THEN 
  DO:
    msg-int = 4.
    RETURN NO-APPLY. 
  END. 
 
  FIND FIRST kline WHERE kline.gastnr = gastnr 
    AND kline.kontcode EQ k-list.kontcode 
    AND kline.betriebsnr = 1 
    AND kline.kontstat = 1 
    AND kline.kontignr NE k-list.kontignr 
    AND NOT kline.ankunft GT k-list.abreise 
    AND NOT kline.abreise LT k-list.ankunft 
    AND kline.zikatnr = katnr NO-LOCK NO-ERROR.
  IF AVAILABLE kline THEN
  DO:
    msg-int = 5.
    RETURN NO-APPLY.
  END.
 
  RUN check-allotment(OUTPUT ERROR).
  IF ERROR THEN
  DO:
    msg-int = 6.
    RETURN NO-APPLY.
  END.
 
  IF curr-mode = "new" THEN RUN create-allotment.
  ELSE IF curr-mode = "chg" THEN RUN chg-allotment.


PROCEDURE create-allotment: 
DEFINE VARIABLE n       AS INTEGER INITIAL 1 NO-UNDO.
DEFINE VARIABLE datum   AS DATE              NO-UNDO.
 
  last-code = k-list.kontcode. 
  DO datum = k-list.ankunft TO k-list.abreise: 
    FIND FIRST counters WHERE counters.counter-no = 10 EXCLUSIVE-LOCK NO-ERROR. 
    IF NOT AVAILABLE counters THEN 
    DO: 
      create counters. 
      counters.counter-no = 10. 
      counters.counter-bez = "Allotment counter". 
    END. 
    counters.counter = counters.counter + 1. 
 
    create kontline. 
    kontline.kontignr = counters.counter. 
    FIND CURRENT counter NO-LOCK. 
    kontline.gastnr = gastnr. 
    kontline.useridanlage = "". 
 
    ASSIGN 
      kontline.betriebsnr = 1 
      kontline.kontcode = k-list.kontcode 
      kontline.ankunft = datum 
      kontline.abreise = datum 
      kontline.zikatnr = zimkateg.zikatnr 
      kontline.arrangement = argt 
      kontline.zimmeranz = k-list.zimmeranz 
      kontline.erwachs = k-list.erwachs 
      kontline.kind1 = k-list.kind1 
      kontline.kind2 = k-list.kind2 
      kontline.overbooking = k-list.overbooking 
      kontline.ruecktage = k-list.ruecktage 
      kontline.rueckdatum = k-list.rueckdatum 
      kontline.ansprech = k-list.ansprech 
      kontline.resdat = today 
      kontline.bemerk = comments 
      kontline.bediener-nr = bediener.nr. 
 
    FIND CURRENT kontline NO-LOCK. 
  END. 
END. 


PROCEDURE chg-allotment: 
DEFINE VARIABLE n AS INTEGER INITIAL 1 NO-UNDO. 
  last-code = k-list.kontcode. 
  FIND FIRST kontline WHERE kontline.kontignr = k-list.kontignr 
      AND kontline.gastnr = gastnr EXCLUSIVE-LOCK NO-ERROR.
  IF AVAILABLE kontline THEN
     ASSIGN 
        kontline.betriebsnr = 1 
        kontline.kontcode = k-list.kontcode 
        kontline.ankunft = k-list.ankunft 
        kontline.abreise = k-list.abreise 
        kontline.zikatnr = zimkateg.zikatnr 
        kontline.arrangement = argt 
        kontline.zimmeranz = k-list.zimmeranz 
        kontline.erwachs = k-list.erwachs 
        kontline.kind1 = k-list.kind1 
        kontline.kind2 = k-list.kind2 
        kontline.overbooking = k-list.overbooking 
        kontline.ruecktage = k-list.ruecktage 
        kontline.rueckdatum = k-list.rueckdatum 
        kontline.ansprech = k-list.ansprech 
        kontline.resdat = today 
        kontline.bemerk = comments 
        kontline.useridanlage = bediener.userinit.
 
  FIND CURRENT kontline NO-LOCK.
END. 


PROCEDURE check-allotment: 
DEFINE OUTPUT PARAMETER ERROR AS LOGICAL INITIAL NO. 
DEFINE VARIABLE datum AS DATE   NO-UNDO.
DEFINE VARIABLE d1    AS DATE   NO-UNDO.
DEFINE VARIABLE d2    AS DATE   NO-UNDO.
DEFINE buffer kline FOR kontline. 
  FOR EACH allot-list: 
    delete allot-list. 
  END. 
  FOR EACH res-line WHERE res-line.kontignr LT 0 
    AND res-line.gastnr = gastnr 
    AND res-line.active-flag LT 2 AND res-line.resstatus LT 11 
    AND NOT (res-line.ankunft GT k-list.abreise) 
    AND NOT (res-line.abreise LT k-list.ankunft) NO-LOCK, 
    FIRST kline WHERE kline.kontignr = - res-line.kontignr 
    AND kline.kontcode = k-list.kontcode 
    AND kline.kontstat = 1 NO-LOCK: 
    IF res-line.ankunft GE k-list.ankunft THEN d1 = res-line.ankunft. 
    ELSE d1 = k-list.ankunft. 
    IF res-line.abreise LE k-list.abreise THEN d2 = res-line.abreise - 1. 
    ELSE d2 = k-list.abreise. 
    DO datum = d1 TO d2: 
      FIND FIRST allot-list WHERE allot-list.datum = datum NO-ERROR. 
      IF NOT AVAILABLE allot-list THEN 
      DO: 
        create allot-list. 
        allot-list.datum = datum. 
        allot-list.anz = k-list.zimmeranz. 
      END. 
      allot-list.anz = allot-list.anz - res-line.zimmeranz. 
    END. 
  END. 
  FIND FIRST allot-list WHERE (allot-list.anz + k-list.overbooking) LT 0 
    NO-ERROR. 
  IF AVAILABLE allot-list THEN 
  DO: 
    ERROR = YES.
    msg-int = 7.
  END. 
END. 


PROCEDURE open-query:
    FOR EACH kontline WHERE kontline.gastnr = gastnr
        AND kontline.kontignr GT 0 AND kontline.betriebsnr = 1
        AND kontline.kontstat = 1 NO-LOCK,
        FIRST z-list WHERE z-list.zikatnr = kontline.zikatnr NO-LOCK,
        FIRST bediener WHERE bediener.nr = kontline.bediener-nr NO-LOCK
        BY kontline.kontcode BY kontline.zikatnr BY kontline.ankunft:
        CREATE globalreserve-list.
        ASSIGN
            globalreserve-list.kontcode      = kontline.kontcode
            globalreserve-list.ankunft       = kontline.ankunft
            globalreserve-list.abreise       = kontline.abreise
            globalreserve-list.kurzbez       = z-list.kurzbez
            globalreserve-list.arrangement   = kontline.arrangement
            globalreserve-list.zimmeranz     = kontline.zimmeranz
            globalreserve-list.erwachs       = kontline.erwachs
            globalreserve-list.kind1         = kontline.kind1
            globalreserve-list.kind2         = kontline.kind2
            globalreserve-list.userinit      = bediener.userinit
            globalreserve-list.useridanlage  = kontline.useridanlage
            globalreserve-list.resdat        = kontline.resdat
            globalreserve-list.ansprech      = kontline.ansprech
            globalreserve-list.bemerk        = kontline.bemerk
            globalreserve-list.kontignr      = kontline.kontignr
            globalreserve-list.zikatnr       = kontline.zikatnr
            globalreserve-list.overbooking   = kontline.overbooking
            globalreserve-list.ruecktage     = kontline.ruecktage
            globalreserve-list.rueckdatum    = kontline.rueckdatum.
    END.
END.


PROCEDURE create-zlist: 
  create z-list. 
  z-list.zikatnr = 0. 
  z-list.kurzbez = "". 
  FOR EACH zimkateg NO-LOCK: 
    create z-list. 
    z-list.zikatnr = zimkateg.zikatnr. 
    z-list.kurzbez = zimkateg.kurzbez. 
  END. 
END. 
