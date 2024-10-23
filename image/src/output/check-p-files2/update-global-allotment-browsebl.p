
DEFINE TEMP-TABLE allot-list
    FIELD datum     AS DATE                 COLUMN-LABEL "Date"
    FIELD w-day     AS CHAR    FORMAT "x(3)" COLUMN-LABEL "WD"
    FIELD tot-rm    AS INTEGER FORMAT ">>>" COLUMN-LABEL "TotRm"
    FIELD ooo       AS INTEGER FORMAT ">>>" COLUMN-LABEL "OOO"
    FIELD occ       AS INTEGER FORMAT ">>>" COLUMN-LABEL "Occ"
    FIELD avl-rm    AS INTEGER FORMAT ">>>" COLUMN-LABEL "Saleable"
    FIELD stat1     AS INTEGER FORMAT ">>>" COLUMN-LABEL "Guaranted"
    FIELD stat2     AS INTEGER FORMAT ">>>" COLUMN-LABEL "6 PM"
    FIELD stat5     AS INTEGER FORMAT ">>>" COLUMN-LABEL "VerbalConf"
    FIELD glres     AS INTEGER FORMAT ">>>" COLUMN-LABEL "Gl-Res"
    FIELD avail1    AS INTEGER FORMAT ">>>" COLUMN-LABEL "Avail"
    FIELD ovb1      AS INTEGER FORMAT ">>>" COLUMN-LABEL "OVB"
    FIELD allot1    AS INTEGER FORMAT ">>>" COLUMN-LABEL "Gl-Allot"
    FIELD gl-allot  AS INTEGER FORMAT ">>9" COLUMN-LABEL "Chg To"
    FIELD gl-used   AS INTEGER FORMAT ">>9" COLUMN-LABEL "Used"
    FIELD gl-remain AS INTEGER FORMAT ">>9" COLUMN-LABEL "Remain"
    FIELD allot2    AS INTEGER FORMAT ">>>" COLUMN-LABEL "OthAllot"
    FIELD blank-str AS CHAR    FORMAT "x(1)" COLUMN-LABEL "" 
    FIELD avail2    AS INTEGER FORMAT ">>>" COLUMN-LABEL "AVAIL"
    FIELD ovb2      AS INTEGER FORMAT ">>>" COLUMN-LABEL "OVB"
    FIELD s-avail2  AS INTEGER
    FIELD expired   AS LOGICAL INIT NO
.

DEF INPUT PARAMETER  pvILanguage  AS INTEGER NO-UNDO.
DEF INPUT PARAMETER  input-date   AS DATE    NO-UNDO.
DEF INPUT PARAMETER  currcode     AS CHAR    NO-UNDO.
DEF INPUT PARAMETER  rmtype       AS CHAR    NO-UNDO.
DEF OUTPUT PARAMETER TABLE        FOR allot-list.

{SupertransBL.i} 
DEF VAR lvCAREA AS CHAR INITIAL "update-global-allotment". 

DEF VAR curr-date   AS DATE     NO-UNDO.
DEF VAR from-date   AS DATE     NO-UNDO.
DEF VAR to-date     AS DATE     NO-UNDO.
DEF VAR ci-date     AS DATE     NO-UNDO.

RUN create-allot-list.
RUN create-browse.

PROCEDURE create-allot-list:
DEF VAR curr-wday   AS INTEGER  NO-UNDO.
DEF VAR ci-date     AS DATE     NO-UNDO.
DEF VAR day-name    AS CHAR EXTENT 8 NO-UNDO.

  ASSIGN
    day-name[1] = translateExtended("SUN",lvCAREA,"")
    day-name[2] = translateExtended("MON",lvCAREA,"")
    day-name[3] = translateExtended("TUE",lvCAREA,"")
    day-name[4] = translateExtended("WED",lvCAREA,"")
    day-name[5] = translateExtended("THU",lvCAREA,"")
    day-name[6] = translateExtended("FRI",lvCAREA,"")
    day-name[7] = translateExtended("SAT",lvCAREA,"")
    day-name[8] = translateExtended("SUN",lvCAREA,"")
  . 

  RUN htpdate.p(87, OUTPUT ci-date).
  ASSIGN 
      from-date = input-date
      to-date   = from-date + 35
      to-date   = DATE(MONTH(to-date), 1, YEAR(to-date)) - 1
  .
  IF from-date LT ci-date THEN from-date = ci-date.

   DO curr-date = from-date TO to-date:
       curr-wday = WEEKDAY(curr-date) - 1.
       IF curr-wday = 0 THEN curr-wday = 7.
       CREATE allot-list.
       ASSIGN
           allot-list.w-day = day-name[curr-wday]
           allot-list.datum = curr-date
       .
   END.

END.


PROCEDURE create-browse:
DEF VAR curr-i      AS INTEGER  NO-UNDO.
DEF VAR i           AS INTEGER  NO-UNDO.  
DEF VAR anz-room    AS INTEGER  NO-UNDO INIT 0.
DEF VAR do-it       AS LOGICAL  NO-UNDO.
DEF VAR tmp-list    AS INTEGER EXTENT 31. 

DEF BUFFER abuff1   FOR allot-list.
DEF BUFFER abuff2   FOR allot-list.
DEF BUFFER kline    FOR kontline.

  DO i = 1 TO 31:
    ASSIGN tmp-list[i] = 0.
  END.
  
  FIND FIRST zimkateg WHERE zimkateg.kurzbez = rmtype NO-LOCK.
  FOR EACH zimmer WHERE zimmer.sleeping 
      AND zimmer.zikatnr = zimkateg.zikatnr NO-LOCK:
      anz-room = anz-room + 1.
  END.

  curr-date = from-date.
  DO i = DAY(from-date) TO DAY(to-date):
    FIND FIRST allot-list WHERE allot-list.datum = curr-date.
    ASSIGN 
      allot-list.tot-rm = anz-room. 
      tmp-list[i]       = anz-room
    . 
    curr-date = curr-date + 1.
  END. 

  FOR EACH outorder WHERE outorder.betriebsnr LE 1 NO-LOCK, 
    FIRST zimmer WHERE zimmer.zinr = outorder.zinr 
    AND zimmer.zikatnr = zimkateg.zikatnr AND zimmer.sleeping 
    AND NOT outorder.gespstart GT to-date
    AND NOT outorder.gespende LT from-date NO-LOCK:     
    curr-date = from-date.
    DO i = DAY(from-date) TO DAY(to-date):
      FIND FIRST allot-list WHERE allot-list.datum = curr-date.
      IF curr-date GE outorder.gespstart AND curr-date LE outorder.gespende THEN 
      ASSIGN 
        allot-list.ooo = allot-list.ooo + 1
        tmp-list[i] = tmp-list[i] - 1 
      . 
       curr-date = curr-date + 1.
    END. 
  END.

  FOR EACH res-line WHERE res-line.resstatus = 6 
    AND res-line.active-flag = 1 
    AND res-line.zikatnr = zimkateg.zikatnr
    AND NOT res-line.ankunft GT to-date
    AND NOT res-line.abreise LE from-date
    AND res-line.l-zuordnung[3] = 0 NO-LOCK,
    FIRST zimmer WHERE zimmer.zikatnr = res-line.zikatnr
    AND zimmer.sleeping NO-LOCK:
    curr-date = from-date.
    DO i = DAY(from-date) TO DAY(to-date):
      FIND FIRST allot-list WHERE allot-list.datum = curr-date.
      IF curr-date GE res-line.ankunft 
        AND curr-date LT res-line.abreise THEN 
      ASSIGN 
        allot-list.occ = allot-list.occ + 1
        tmp-list[i] = tmp-list[i] - 1
      .         . 
      curr-date = curr-date + 1.
    END.
  END.

  curr-date = from-date.
  DO i = DAY(from-date) TO DAY(to-date):
    FIND FIRST allot-list WHERE allot-list.datum = curr-date.
    allot-list.avl-rm = tmp-list[i]. 
    curr-date = curr-date + 1.
  END. 
       
  FOR EACH res-line WHERE res-line.active-flag = 0 
    AND res-line.resstatus = 1 
    AND res-line.zikatnr = zimkateg.zikatnr 
    AND NOT res-line.ankunft GT to-date 
    AND NOT res-line.abreise LE from-date 
    AND res-line.l-zuordnung[3] = 0 NO-LOCK: 
    do-it = YES. 
    IF res-line.zinr NE "" THEN 
    DO: 
      FIND FIRST zimmer WHERE zimmer.zinr = res-line.zinr NO-LOCK. 
      do-it = zimmer.sleeping. 
    END.     
    IF do-it THEN 
    DO: 
      curr-date = from-date.
      DO i = DAY(from-date) TO DAY(to-date):
        FIND FIRST allot-list WHERE allot-list.datum = curr-date.
        IF curr-date GE res-line.ankunft 
          AND curr-date LT res-line.abreise THEN 
        ASSIGN 
          allot-list.stat1 = allot-list.stat1 + res-line.zimmeranz
          tmp-list[i] = tmp-list[i] - res-line.zimmeranz 
        . 
          curr-date = curr-date + 1.
      END.
    END. 
  END.
 
  FOR EACH res-line WHERE res-line.active-flag = 0 
    AND res-line.resstatus = 2 
    AND res-line.zikatnr = zimkateg.zikatnr 
    AND NOT res-line.ankunft GT to-date 
    AND NOT res-line.abreise LE from-date 
    AND res-line.l-zuordnung[3] = 0 NO-LOCK: 
    do-it = YES. 
    IF res-line.zinr NE "" THEN 
    DO: 
      FIND FIRST zimmer WHERE zimmer.zinr = res-line.zinr NO-LOCK. 
      do-it = zimmer.sleeping. 
    END.     
    IF do-it THEN 
    DO: 
      curr-date = from-date.
      DO i = DAY(from-date) TO DAY(to-date):
        FIND FIRST allot-list WHERE allot-list.datum = curr-date.
        IF curr-date GE res-line.ankunft 
          AND curr-date LT res-line.abreise THEN 
        ASSIGN 
          allot-list.stat2 = allot-list.stat2 + res-line.zimmeranz
          tmp-list[i] = tmp-list[i] - res-line.zimmeranz 
        . 
          curr-date = curr-date + 1.
      END.
    END. 
  END.

  FOR EACH res-line WHERE res-line.active-flag = 0 
    AND res-line.resstatus = 5 
    AND res-line.zikatnr = zimkateg.zikatnr 
    AND NOT res-line.ankunft GT to-date 
    AND NOT res-line.abreise LE from-date 
    AND res-line.l-zuordnung[3] = 0 NO-LOCK: 
    do-it = YES. 
    IF res-line.zinr NE "" THEN 
    DO: 
      FIND FIRST zimmer WHERE zimmer.zinr = res-line.zinr NO-LOCK. 
      do-it = zimmer.sleeping. 
    END.     
    IF do-it THEN 
    DO: 
      curr-date = from-date.
      DO i = DAY(from-date) TO DAY(to-date):
        FIND FIRST allot-list WHERE allot-list.datum = curr-date.
        IF curr-date GE res-line.ankunft 
          AND curr-date LT res-line.abreise THEN 
        ASSIGN 
          allot-list.stat5 = allot-list.stat5 + res-line.zimmeranz
          tmp-list[i] = tmp-list[i] - res-line.zimmeranz 
        . 
          curr-date = curr-date + 1.
      END.
    END. 
  END.

  FOR EACH kontline WHERE kontline.kontignr GT 0 
    AND kontline.betriebsnr = 1 
    AND NOT kontline.ankunft GT to-date 
    AND NOT kontline.abreise LT from-date 
    AND kontline.zikatnr = zimkateg.zikatnr 
    AND kontline.kontstat = 1 NO-LOCK: 
    curr-date = from-date.
    DO i = DAY(from-date) TO DAY(to-date):
      FIND FIRST allot-list WHERE allot-list.datum = curr-date.
      IF curr-date GE kontline.ankunft 
        AND curr-date LE kontline.abreise THEN 
      ASSIGN 
        allot-list.glres = allot-list.glres + kontline.zimmeranz
        tmp-list[i] = tmp-list[i] - kontline.zimmeranz 
      . 
      curr-date = curr-date + 1.
    END.
  END. 
 
  FOR EACH res-line WHERE res-line.active-flag LE 1 
    AND res-line.resstatus LE 6
    AND res-line.resstatus NE 3
    AND res-line.resstatus NE 4
    AND res-line.zikatnr = zimkateg.zikatnr 
    AND NOT res-line.ankunft GT to-date 
    AND NOT res-line.abreise LE from-date 
    AND res-line.l-zuordnung[3] = 0 
    AND res-line.kontignr LT 0 NO-LOCK: 
    do-it = YES. 
    IF res-line.zinr NE "" THEN 
    DO: 
      FIND FIRST zimmer WHERE zimmer.zinr = res-line.zinr NO-LOCK. 
      do-it = zimmer.sleeping. 
    END.     
    IF do-it THEN 
    DO: 
      curr-date = from-date.
      DO i = DAY(from-date) TO DAY(to-date):
        FIND FIRST allot-list WHERE allot-list.datum = curr-date.
        IF curr-date GE res-line.ankunft 
          AND curr-date LT res-line.abreise THEN 
        ASSIGN 
          allot-list.glres = allot-list.glres - res-line.zimmeranz
          tmp-list[i] = tmp-list[i] + res-line.zimmeranz 
        . 
        curr-date = curr-date + 1.
      END.
    END. 
  END.
   
  curr-date = from-date.
  DO i = DAY(from-date) TO DAY(to-date):
    FIND FIRST allot-list WHERE allot-list.datum = curr-date.
    IF tmp-list[i] GT 0 THEN allot-list.avail1 = tmp-list[i].
    curr-date = curr-date + 1.
  END. 
 
  curr-date = from-date.
  DO i = DAY(from-date) TO DAY(to-date):
    FIND FIRST allot-list WHERE allot-list.datum = curr-date.
    IF tmp-list[i] LT 0 THEN allot-list.ovb1 = - tmp-list[i].
    curr-date = curr-date + 1.
  END. 

  FOR EACH kontline WHERE kontline.kontignr GT 0 
    AND kontline.betriebsnr = 0 
    AND NOT kontline.ankunft GT to-date 
    AND NOT kontline.abreise LT from-date 
    AND (kontline.zikatnr = zimkateg.zikatnr OR kontline.zikatnr = 0)
    AND kontline.kontstat = 1 NO-LOCK: 
    curr-date = from-date.
    DO i = DAY(from-date) TO DAY(to-date):
      FIND FIRST allot-list WHERE allot-list.datum = curr-date.
      IF curr-date GE kontline.ankunft 
        AND curr-date LE kontline.abreise THEN
      DO:
        IF (curr-date GE ci-date + kontline.ruecktage) THEN
        DO:
          ASSIGN tmp-list[i] = tmp-list[i] - kontline.zimmeranz. 
          IF kontline.kontcode NE currcode THEN 
            allot-list.allot2 = allot-list.allot2 + kontline.zimmeranz.
        END.
        IF kontline.kontcode EQ currcode THEN 
        ASSIGN
          allot-list.allot1  = allot-list.allot1 + kontline.zimmeranz
          allot-list.expired = curr-date LT (ci-date + kontline.ruecktage)
        .
      END.
      curr-date = curr-date + 1.
    END.
  END. 
 
  FOR EACH res-line WHERE res-line.active-flag LE 1 
    AND res-line.resstatus LE 6
    AND res-line.resstatus NE 3
    AND res-line.resstatus NE 4
    AND res-line.zikatnr = zimkateg.zikatnr 
    AND NOT res-line.ankunft GT to-date 
    AND NOT res-line.abreise LE from-date 
    AND res-line.l-zuordnung[3] = 0 
    AND res-line.kontignr GT 0 NO-LOCK: 
    do-it = YES. 
    IF res-line.zinr NE "" THEN 
    DO: 
      FIND FIRST zimmer WHERE zimmer.zinr = res-line.zinr NO-LOCK. 
      do-it = zimmer.sleeping. 
    END.
    IF do-it THEN 
    DO: 
      FIND FIRST kline WHERE kline.kontignr = res-line.kontignr
        NO-LOCK.
      FIND FIRST kontline WHERE kontline.kontcode = kline.kontcode
        AND kontline.betriebsnr = 0 
        AND res-line.ankunft GE kontline.ankunft
        AND res-line.ankunft LE kontline.abreise NO-LOCK.
      curr-date = from-date.
      DO i = DAY(from-date) TO DAY(to-date):
        FIND FIRST allot-list WHERE allot-list.datum = curr-date.
        IF (curr-date GE ci-date + kontline.ruecktage) 
          AND curr-date GE res-line.ankunft 
          AND curr-date LT res-line.abreise THEN
        DO:
          ASSIGN tmp-list[i] = tmp-list[i] + res-line.zimmeranz. 
          IF kontline.kontcode = currcode THEN
            allot-list.gl-used = allot-list.gl-used + res-line.zimmeranz.
          ELSE allot-list.allot2 = allot-list.allot2 - res-line.zimmeranz.
        END.
        curr-date = curr-date + 1.
      END.
    END.
  END.

  curr-date = from-date.
  DO i = DAY(from-date) TO DAY(to-date):
    FIND FIRST allot-list WHERE allot-list.datum = curr-date.
    IF tmp-list[i] GT 0 THEN allot-list.avail2 = tmp-list[i]. 
    curr-date = curr-date + 1.
  END. 

  curr-date = from-date.
  DO i = DAY(from-date) TO DAY(to-date):
    FIND FIRST allot-list WHERE allot-list.datum = curr-date.
    IF tmp-list[i] LT 0 THEN allot-list.ovb2 = - tmp-list[i]. 
    curr-date = curr-date + 1.
  END. 

  FOR EACH allot-list:
    ASSIGN allot-list.gl-allot = allot-list.allot1.
    IF NOT allot-list.expired 
      AND allot-list.allot1 GT allot-list.gl-used THEN
      ASSIGN allot-list.gl-remain = allot-list.allot1 - allot-list.gl-used.
  END.

END.

