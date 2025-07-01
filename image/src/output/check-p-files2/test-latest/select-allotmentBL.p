DEF TEMP-TABLE t-kontline LIKE kontline.

DEFINE INPUT  PARAMETER main-gastnr  AS INTEGER     NO-UNDO.
DEFINE INPUT  PARAMETER gastnr       AS INTEGER     NO-UNDO.
DEFINE INPUT  PARAMETER kType        AS INTEGER     NO-UNDO.
DEFINE INPUT  PARAMETER zikatnr      AS INTEGER     NO-UNDO. 
DEFINE INPUT  PARAMETER argt         AS CHAR        NO-UNDO. 
DEFINE INPUT  PARAMETER erwachs      AS INTEGER     NO-UNDO. 
DEFINE INPUT  PARAMETER ankunft      AS DATE        NO-UNDO. 
DEFINE INPUT  PARAMETER abreise      AS DATE        NO-UNDO. 
DEFINE INPUT  PARAMETER qty          AS INTEGER     NO-UNDO. 
DEFINE INPUT  PARAMETER resNo        AS INTEGER     NO-UNDO. 
DEFINE INPUT  PARAMETER reslinNo     AS INTEGER     NO-UNDO. 
DEFINE OUTPUT PARAMETER kCode  AS CHAR INITIAL ""   NO-UNDO.
DEFINE OUTPUT PARAMETER remark AS CHAR INITIAL ""   NO-UNDO.
DEFINE OUTPUT PARAMETER TABLE FOR t-kontline.

DEF TEMP-TABLE allot-list
    FIELD kontcode    AS CHAR
    FIELD ruecktage   AS INTEGER
.
DEFINE TEMP-TABLE overbook-list
    FIELD kontcode AS CHAR
    FIELD overbook AS INTEGER INIT 0
.
DEF TEMP-TABLE s-list
    FIELD datum     AS DATE
    FIELD zimmeranz AS INTEGER INIT 0
.

DEF VAR ci-date         AS DATE     NO-UNDO.
DEF VAR delta           AS INTEGER  NO-UNDO.
DEF VAR do-it           AS LOGICAL  NO-UNDO.
DEF VAR overbook-flag   AS LOGICAL  NO-UNDO.
DEF VAR found-kontcode  AS CHAR     NO-UNDO INIT "".

DEF BUFFER kline FOR kontline.

DO:
  FIND FIRST htparam WHERE htparam.paramnr = 87 NO-LOCK.
  ci-date = htparam.fdate.

  IF ankunft LT ci-date THEN delta = 9999.
  ELSE delta = ankunft - ci-date.

  FIND FIRST kline WHERE kline.gastnr = gastnr AND kline.betriebsnr = ktype 
    NO-LOCK NO-ERROR. 
  IF AVAILABLE kline THEN 
  DO: 
    FOR EACH kontline WHERE kontline.gastnr = gastnr 
      AND kontline.betriebsnr = ktype NO-LOCK 
      BY kontline.ruecktage DESCENDING:
      do-it = YES.
      IF main-gastnr NE gastnr THEN do-it = (kontline.pr-code NE "").
      IF do-it THEN
      DO:
        FIND FIRST allot-list WHERE allot-list.kontcode = kontline.kontcode
          AND allot-list.ruecktage = kontline.ruecktage NO-ERROR.
        IF NOT AVAILABLE allot-list THEN
        DO:
          CREATE allot-list.
          ASSIGN
            allot-list.kontcode  = kontline.kontcode
            allot-list.ruecktage = kontline.ruecktage
          .
        END.
      END.
    END.
    FOR EACH allot-list BY allot-list.ruecktage DESCENDING:
      FIND FIRST kontline WHERE kontline.gastnr = gastnr 
        AND kontline.kontcode = allot-list.kontcode
        AND kontline.betriebsnr = ktype 
        AND kontline.zikatnr = zikatnr 
        AND kontline.arrangement = argt 
        AND kontline.erwachs EQ erwachs 
        AND (ankunft GE kontline.ankunft) 
        AND (ankunft LE kontline.abreise)
        AND delta GE kontline.ruecktage NO-LOCK NO-ERROR.
      IF NOT AVAILABLE kontline THEN
      FIND FIRST kontline WHERE kontline.gastnr = gastnr 
        AND kontline.kontcode = allot-list.kontcode
        AND kontline.betriebsnr = ktype 
        AND kontline.zikatnr = zikatnr 
        AND kontline.arrangement = ""
        AND kontline.erwachs EQ erwachs 
        AND (ankunft GE kontline.ankunft) 
        AND (ankunft LE kontline.abreise)
        AND delta GE kontline.ruecktage NO-LOCK NO-ERROR.
      IF NOT AVAILABLE kontline THEN
      FIND FIRST kontline WHERE kontline.gastnr = gastnr 
        AND kontline.kontcode = allot-list.kontcode
        AND kontline.betriebsnr = ktype 
        AND kontline.zikatnr = zikatnr 
        AND kontline.arrangement = argt 
        AND kontline.erwachs GE erwachs 
        AND (ankunft GE kontline.ankunft) 
        AND (ankunft LE kontline.abreise)
        AND delta GE kontline.ruecktage NO-LOCK NO-ERROR.
      IF NOT AVAILABLE kontline THEN 
      FIND FIRST kontline WHERE kontline.gastnr = gastnr 
          AND kontline.kontcode = allot-list.kontcode
          AND kontline.betriebsnr = ktype 
          AND kontline.zikatnr = zikatnr 
          AND kontline.arrangement = "" 
          AND kontline.erwachs GE erwachs 
          AND (ankunft GE kontline.ankunft) 
          AND (ankunft LE kontline.abreise)
          AND delta GE kontline.ruecktage NO-LOCK NO-ERROR.
      IF NOT AVAILABLE kontline THEN 
      FIND FIRST kontline WHERE kontline.gastnr = gastnr 
        AND kontline.kontcode = allot-list.kontcode
        AND kontline.betriebsnr = ktype 
        AND kontline.zikatnr = 0 
        AND kontline.arrangement = argt 
        AND kontline.erwachs EQ erwachs 
        AND (ankunft GE kontline.ankunft) 
        AND (ankunft LE kontline.abreise)
        AND delta GE kontline.ruecktage NO-LOCK NO-ERROR.
      IF NOT AVAILABLE kontline THEN 
      FIND FIRST kontline WHERE kontline.gastnr = gastnr 
          AND kontline.kontcode = allot-list.kontcode
          AND kontline.betriebsnr = ktype 
          AND kontline.zikatnr = 0 
          AND kontline.arrangement = "" 
          AND kontline.erwachs EQ erwachs 
          AND (ankunft GE kontline.ankunft) 
          AND (ankunft LE kontline.abreise) 
          AND kontline.kontstat = 1 
          AND delta GE kontline.ruecktage NO-LOCK NO-ERROR.
      IF NOT AVAILABLE kontline THEN 
      FIND FIRST kontline WHERE kontline.gastnr = gastnr 
        AND kontline.kontcode = allot-list.kontcode
        AND kontline.betriebsnr = ktype 
        AND kontline.zikatnr = 0 
        AND kontline.arrangement = argt 
        AND kontline.erwachs GE erwachs 
        AND (ankunft GE kontline.ankunft) 
        AND (ankunft LE kontline.abreise)
        AND delta GE kontline.ruecktage NO-LOCK NO-ERROR.
      IF NOT AVAILABLE kontline THEN 
      FIND FIRST kontline WHERE kontline.gastnr = gastnr 
          AND kontline.kontcode = allot-list.kontcode
          AND kontline.betriebsnr = ktype 
          AND kontline.zikatnr = 0 
          AND kontline.arrangement = "" 
          AND kontline.erwachs GE erwachs 
          AND (ankunft GE kontline.ankunft) 
          AND (ankunft LE kontline.abreise) 
          AND kontline.kontstat = 1
          AND delta GE kontline.ruecktage NO-LOCK NO-ERROR.
      IF NOT AVAILABLE kontline THEN 
      FIND FIRST kontline WHERE kontline.gastnr = gastnr 
        AND kontline.kontcode = allot-list.kontcode
        AND kontline.betriebsnr = ktype 
        AND kontline.zikatnr = zikatnr 
        AND kontline.arrangement = argt 
        AND kontline.erwachs = 0
        AND (ankunft GE kontline.ankunft) 
        AND (ankunft LE kontline.abreise)
        AND delta GE kontline.ruecktage NO-LOCK NO-ERROR.
      IF NOT AVAILABLE kontline THEN 
      FIND FIRST kontline WHERE kontline.gastnr = gastnr 
        AND kontline.kontcode = allot-list.kontcode
        AND kontline.betriebsnr = ktype 
        AND kontline.zikatnr = zikatnr 
        AND kontline.arrangement = "" 
        AND kontline.erwachs = 0
        AND (ankunft GE kontline.ankunft) 
        AND (ankunft LE kontline.abreise)
        AND delta GE kontline.ruecktage NO-LOCK NO-ERROR.
      IF NOT AVAILABLE kontline THEN 
      FIND FIRST kontline WHERE kontline.gastnr = gastnr 
        AND kontline.kontcode = allot-list.kontcode
        AND kontline.betriebsnr = ktype 
        AND kontline.zikatnr = 0 
        AND kontline.arrangement = argt 
        AND kontline.erwachs = 0
        AND (ankunft GE kontline.ankunft) 
        AND (ankunft LE kontline.abreise)
        AND delta GE kontline.ruecktage NO-LOCK NO-ERROR.
      IF NOT AVAILABLE kontline THEN 
      FIND FIRST kontline WHERE kontline.gastnr = gastnr 
        AND kontline.kontcode = allot-list.kontcode
        AND kontline.betriebsnr = ktype 
        AND kontline.zikatnr = 0 
        AND kontline.arrangement = "" 
        AND kontline.erwachs = 0
        AND (ankunft GE kontline.ankunft) 
        AND (ankunft LE kontline.abreise) 
        AND kontline.kontstat = 1
        AND delta GE kontline.ruecktage NO-LOCK NO-ERROR.
      
      IF AVAILABLE kontline THEN 
      DO: 
        RUN check-allot-overbook(OUTPUT overbook-flag).
        IF NOT overbook-flag THEN
        DO:
          found-kontcode = kontline.kontcode.
          LEAVE.
        END.
      END.
    
    END.
  END.

  IF found-kontcode = "" THEN
  FOR EACH overbook-list BY overbook-list.overbook DESCENDING:
    found-kontcode = overbook-list.kontcode.
    LEAVE.
  END.

  IF found-kontcode NE "" THEN 
  DO: 
    FIND FIRST kontline WHERE kontline.kontcode = found-kontcode
        AND kontline.kontstat = 1 NO-LOCK.
    ASSIGN
      kCode  = kontline.kontcode
      remark = kontline.bemerk
    .
    CREATE t-kontline.
    BUFFER-COPY kontline TO t-kontline.
  END. 

END.

PROCEDURE check-allot-overbook:
DEF OUTPUT PARAMETER overbook-flag AS LOGICAL INIT NO.
DEF VARIABLE datum      AS DATE NO-UNDO.
DEF VARIABLE beg-date   AS DATE NO-UNDO.
DEF VARIABLE end-date   AS DATE NO-UNDO.

DEF BUFFER kline FOR kontline.
DEF BUFFER kbuff FOR kontline.

  FOR EACH kline WHERE kline.kontcode = kontline.kontcode 
    AND kline.kontstatus = 1
    AND NOT kline.ankunft GE abreise
    AND NOT kline.abreise LT ankunft NO-LOCK:

    FOR EACH s-list:
      DELETE s-list.
    END.

    beg-date = kontline.ankunft.
    IF ankunft GT beg-date THEN beg-date = ankunft.
    end-date = kontline.abreise.
    IF (abreise - 1) LT end-date THEN end-date = abreise - 1.

    DO datum = beg-date TO end-date:
      CREATE s-list.
      ASSIGN
          s-list.datum = datum
          s-list.zimmeranz = kontline.zimmeranz - qty.
    END.

    FOR EACH res-line WHERE res-line.kontignr GT 0 
      AND res-line.active-flag LE 1
      AND res-line.resstatus LE 6 
      AND NOT res-line.ankunft GT beg-date
      AND NOT (res-line.abreise - 1) LT end-date NO-LOCK,
      FIRST kbuff WHERE kbuff.kontignr = res-line.kontignr 
      AND kbuff.kontstat = 1 AND kbuff.kontcode = kontline.kontcode
      NO-LOCK:
      IF res-line.resnr = resNo AND res-line.reslinnr = reslinNo THEN .
      ELSE
      DO datum = beg-date TO end-date:
        IF datum GE res-line.ankunft AND datum LT res-line.abreise THEN
        DO:
          FIND FIRST s-list WHERE s-list.datum = datum.
          ASSIGN s-list.zimmeranz = s-list.zimmeranz - res-line.zimmeranz.
        END.
      END.
    END.

    FOR EACH s-list WHERE s-list.zimmeranz LT 0
        BY s-list.zimmeranz:
      FIND FIRST overbook-list WHERE overbook-list.kontcode = kontline.kontcode
          NO-ERROR.
      IF NOT AVAILABLE overbook-list THEN
      DO:
        CREATE overbook-list.
        ASSIGN overbook-list.kontcode = kontline.kontcode.
      END.
      overbook-flag = YES.
      IF overbook-list.overbook GT s-list.zimmeranz THEN
          overbook-list.overbook = s-list.zimmeranz.
      LEAVE.
    END.
  END.
END.
