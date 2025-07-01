
DEFINE TEMP-TABLE room-list 
  FIELD nr AS INTEGER 
  FIELD flag AS CHAR 
  FIELD bez1 AS CHAR 
  FIELD bezeich AS CHAR FORMAT "x(19)" 
  FIELD room AS DECIMAL EXTENT 19 FORMAT "->>>9" 
  FIELD coom AS CHAR EXTENT 19 FORMAT "x(5)". 

DEFINE TEMP-TABLE sum-list 
  FIELD bezeich AS CHAR FORMAT "x(19)" 
  FIELD summe AS INTEGER EXTENT 19 FORMAT "->>>9". 

DEFINE TEMP-TABLE segm-list 
  FIELD segmentcode AS INTEGER 
  FIELD bezeich AS CHAR FORMAT "x(19)" 
  FIELD segm AS INTEGER EXTENT 19 FORMAT "->>>9". 

/*****************************************/

DEFINE INPUT  PARAMETER pvILanguage      AS INTEGER NO-UNDO.
DEFINE INPUT  PARAMETER inhouse-flag     AS LOGICAL .
DEFINE INPUT  PARAMETER disp-flag        AS LOGICAL.
DEFINE INPUT  PARAMETER lessOO           AS LOGICAL.
DEFINE INPUT  PARAMETER incl-tent        AS LOGICAL.
DEFINE INPUT  PARAMETER curr-date        AS DATE.
DEFINE INPUT  PARAMETER printer-nr       AS INTEGER.
DEFINE INPUT  PARAMETER call-from        AS INTEGER.
DEFINE INPUT  PARAMETER txt-file         AS CHAR.
DEFINE INPUT  PARAMETER vhp-limited      AS LOGICAL.
DEFINE OUTPUT PARAMETER TABLE FOR room-list.
DEFINE OUTPUT PARAMETER TABLE FOR sum-list.
DEFINE OUTPUT PARAMETER TABLE FOR segm-list.


DEFINE VARIABLE tab-label               AS CHAR EXTENT 19 NO-UNDO. 
DEFINE VARIABLE datum                   AS DATE. 
DEFINE VARIABLE ci-date                 AS DATE. 
DEFINE VARIABLE wlist                   AS CHAR FORMAT "x(133)". 
DEFINE VARIABLE dlist                   AS CHAR FORMAT "x(133)". 
DEFINE VARIABLE curr-day                AS INTEGER. 
DEFINE VARIABLE week-list               AS CHAR EXTENT 14 FORMAT "x(5)" 
  INITIAL [" Mon ", " Tue ", " Wed ", " Thu ", " Fri ", " Sat ", " Sun "]. 

DEFINE VARIABLE i                       AS INTEGER INITIAL 0 NO-UNDO.
DEFINE VARIABLE inhouse                 AS INTEGER EXTENT 19. 
DEFINE VARIABLE tot-room                AS INTEGER. 
DEFINE VARIABLE inactive                AS INTEGER. 
DEFINE VARIABLE pax                     AS INTEGER NO-UNDO. 
DEFINE VARIABLE from-date               AS DATE. 
DEFINE VARIABLE to-date                 AS DATE. 
DEFINE VARIABLE tmp-date                AS INTEGER.         /* Rulita 090125 | Fixing serverless issue git 190 */

/* Rulita 090125 | Fixing serverless issue git 190 */
FIND FIRST htparam WHERE htparam.paramnr = 87 NO-LOCK NO-ERROR. 
IF AVAILABLE htparam THEN
DO:
  /* ci-date = fdate. */      /* Rulita 181024 | Fixing for serverless */
  ci-date = htparam.fdate. 
END.
/* End Rulita */

{ Supertransbl.i } 
DEFINE VARIABLE lvCAREA AS CHAR INITIAL "dayfcastBL". 
/********************MAIN LOGIC****************/
FOR EACH segm-list:
    DELETE segm-list.
END.
FOR EACH sum-list:
    DELETE sum-list.
END.
FOR EACH room-list:
    DELETE room-list.
END.
RUN sum-rooms.
RUN create-browse.

/*************PROCEDURE***************/
PROCEDURE sum-rooms: 
  tot-room = 0. 
  inactive = 0. 
  FOR EACH zimkateg WHERE zimkateg.verfuegbarkeit = YES NO-LOCK: 
    FOR EACH zimmer WHERE zimmer.zikatnr = zimkateg.zikatnr NO-LOCK: 
      IF sleeping THEN tot-room = tot-room + 1. 
      ELSE inactive = inactive + 1. 
    END. 
  END. 
END. 

PROCEDURE create-browse: 
DEFINE VARIABLE to-date     AS DATE. 
DEFINE VARIABLE datum1      AS DATE. 
DEFINE VARIABLE datum2      AS DATE. 
DEFINE VARIABLE abreise1    AS DATE. 
DEFINE VARIABLE tmp-list    AS DECIMAL EXTENT 19. 
DEFINE VARIABLE pers-list   AS INTEGER EXTENT 19. 
DEFINE VARIABLE avail-list  AS INTEGER EXTENT 19. 
DEFINE VARIABLE black-list  AS INTEGER. 
DEFINE VARIABLE last-resnr  AS INTEGER INITIAL 0. 
 
DEFINE VARIABLE fdate       AS DATE. 
DEFINE VARIABLE tdate       AS DATE. 
DEFINE VARIABLE res-allot   AS INTEGER EXTENT 19. 
DEFINE VARIABLE om-flag     AS LOGICAL INITIAL NO. 
DEFINE VARIABLE glob-res    AS INTEGER EXTENT 19.
DEFINE VARIABLE ooo-tot     AS INTEGER EXTENT 19.
DEFINE VARIABLE avl-tot     AS INTEGER EXTENT 19.
 
DEFINE VARIABLE do-it   AS LOGICAL. 
DEFINE buffer room      FOR zimmer. 
 
  to-date = curr-date + 18. 
 
  FOR EACH room-list: 
    DELETE room-list. 
  END. 
  FOR EACH sum-list: 
    DELETE sum-list. 
  END. 
  FOR EACH segm-list: 
    DELETE segm-list. 
  END. 
 
  DO i = 1 TO 19: 
    res-allot[i] = 0. 
    inhouse[i] = 0. 
  END. 
 
  fdate = curr-date. 
  tdate = curr-date + 18. 
  
  FOR EACH res-line WHERE res-line.resstatus LE 6 AND res-line.resstatus NE 3 
    AND res-line.active-flag LE 1 AND res-line.kontignr GT 0 
    AND res-line.l-zuordnung[3] = 0
    AND NOT res-line.ankunft GT tdate 
    /* Rulita 060125 | Fixing res-line.abreise LE fdate issue git 190 */
    AND NOT res-line.abreise LE curr-date NO-LOCK:                      

    IF NOT vhp-limited THEN 
    DO:    
      IF NOT inhouse-flag THEN do-it = YES.
      ELSE do-it = res-line.active-flag = 0.
    END.
    ELSE
    DO:
      FIND FIRST reservation WHERE reservation.resnr = res-line.resnr
        NO-LOCK NO-ERROR.
      FIND FIRST segment WHERE segment.segmentcode = reservation.segmentcode
        NO-LOCK NO-ERROR.
      do-it = AVAILABLE segment AND segment.vip-level = 0.
      IF inhouse-flag AND do-it THEN do-it = res-line.active-flag = 0.
    END.

    IF do-it THEN
    DO i = 1 TO 19: 
      datum = curr-date + i - 1. 
      IF datum GE res-line.ankunft AND datum LT res-line.abreise THEN 
      DO: 
        FIND FIRST kontline WHERE kontline.betriebsnr = 0 
          AND kontline.kontignr = res-line.kontignr 
          AND datum GE kontline.ankunft AND datum LT kontline.abreise 
          AND datum GE (ci-date + kontline.ruecktage) NO-LOCK NO-ERROR. 
        IF AVAILABLE kontline THEN 
        res-allot[i] = res-allot[i] + res-line.zimmeranz. 
      END. 
    END. 
  END. 
 
  FIND FIRST htparam WHERE paramnr = 709 NO-LOCK. 
  black-list = htparam.finteger. 
  FOR EACH segment WHERE segment.segmentcode NE black-list
     AND NOT segment.bezeich MATCHES "*$$0" NO-LOCK: 
    CREATE segm-list. 
    segm-list.segmentcode = segment.segmentcode. 
    segm-list.bezeich = ENTRY(1, segment.bezeich, "$$0"). 
  END. 
  CREATE segm-list. 
  ASSIGN 
    segm-list.segmentcode = 99999 
    segm-list.bezeich = translateExtended ("Global Reserve",lvCAREA,""). 
 
  CREATE room-list. 
  room-list.nr = 1. 
  room-list.bezeich = translateExtended ("Total Rooms",lvCAREA,""). 
  DO i = 1 TO 19: 
    room-list.room[i] = tot-room + inactive. 
  END. 
 
  CREATE room-list. 
  room-list.nr = 2. 
  room-list.bezeich = translateExtended ("Active Rooms",lvCAREA,""). 
  DO i = 1 TO 19: 
    room-list.room[i] = tot-room. 
    tmp-list[i] = 0. 
    pers-list[i] = 0. 
    avail-list[i] = 0. 
  END. 

  CREATE room-list. 
  room-list.nr = 3. 
  room-list.bez1 = "Resident". 
  room-list.bezeich = translateExtended ("Resident",lvCAREA,""). 
  last-resnr = 0. 

  /*IF fdate = ci-date THEN
  FOR EACH res-line WHERE res-line.ankunft = ci-date
    AND res-line.abreise = ci-date AND res-line.resstatus = 8 
    AND res-line.l-zuordnung[3] = 0 AND NOT res-line.zimmerfix NO-LOCK:
    FIND FIRST bill WHERE bill.resnr = res-line.resnr 
      AND bill.reslinnr = res-line.reslinnr NO-LOCK NO-ERROR. 
    IF AVAILABLE bill AND bill.argtumsatz GT 0 THEN 
    DO:
      FIND FIRST reservation WHERE reservation.resnr = res-line.resnr
        NO-LOCK.
      FIND FIRST segment WHERE segment.segmentcode = reservation.segmentcode
        NO-LOCK NO-ERROR.
      FIND FIRST segm-list 
        WHERE segm-list.segmentcode = reservation.segmentcode NO-ERROR. 
      IF AVAILABLE segm-list THEN segm-list.segm[1] = segm-list.segm[1] + 1. 
      ASSIGN
        tmp-list[1]       = tmp-list[1] + 1
        room-list.room[1] = room-list.room[1] + 1
        pers-list[1]      = pers-list[1] + res-line.erwachs + res-line.kind1 
          + res-line.kind2 + res-line.l-zuordnung[4] + res-line.gratis. 
      . 
    END.
  END.*/

  FOR EACH res-line WHERE (resstatus = 6 OR resstatus = 13) AND active-flag = 1 
    AND NOT (res-line.ankunft GT to-date) 
    AND NOT (res-line.abreise LT curr-date) 
    AND res-line.l-zuordnung[3] = 0 NO-LOCK, 
    FIRST zimmer WHERE zimmer.zinr = res-line.zinr /* AND zimmer.sleeping */ 
    NO-LOCK BY res-line.resnr: 
    IF last-resnr NE res-line.resnr THEN FIND FIRST reservation 
      WHERE reservation.resnr = res-line.resnr NO-LOCK NO-ERROR. 
    last-resnr = res-line.resnr. 


    IF NOT vhp-limited THEN 
    DO:    
      IF NOT inhouse-flag THEN do-it = YES.
      ELSE do-it = res-line.active-flag = 0.
    END.
    ELSE
    DO:
      FIND FIRST segment WHERE segment.segmentcode = reservation.segmentcode
        NO-LOCK NO-ERROR.
      do-it = AVAILABLE segment AND segment.vip-level = 0.
      IF inhouse-flag AND do-it THEN do-it = res-line.active-flag = 0.
    END.
    IF do-it THEN
    DO:
      i = 1. 
      datum1 = curr-date. 

      IF res-line.ankunft GT datum1 THEN datum1 = res-line.ankunft. 
      datum2 = to-date. 
      IF res-line.abreise LT datum2 THEN datum2 = res-line.abreise. 
 
      DO datum = datum1 TO datum2: 
        pax = res-line.erwachs. 
        FIND FIRST reslin-queasy WHERE reslin-queasy.key = "arrangement" 
          AND reslin-queasy.resnr = res-line.resnr 
          AND reslin-queasy.reslinnr = res-line.reslinnr 
          AND reslin-queasy.date1 LE datum 
          AND reslin-queasy.date2 GE datum NO-LOCK NO-ERROR. 
        IF AVAILABLE reslin-queasy AND reslin-queasy.number3 NE 0 THEN 
          pax = reslin-queasy.number3. 
        do-it = NO. 
        FIND FIRST queasy WHERE queasy.key = 14 AND queasy.char1 = res-line.zinr 
          AND queasy.date1 LE datum AND queasy.date2 GE datum NO-LOCK NO-ERROR. 
        IF zimmer.sleeping THEN 
        DO: 
          IF NOT AVAILABLE queasy THEN do-it = YES. 
          ELSE IF AVAILABLE queasy AND queasy.number3 NE res-line.gastnr THEN 
            do-it = YES. 
        END. 
        ELSE 
        DO: 
          IF AVAILABLE queasy AND queasy.number3 NE res-line.gastnr 
            AND res-line.zipreis GT 0 THEN do-it = YES. 
        END. 
/* inhouse guest */ 
        IF res-line.abreise GT datum AND do-it THEN 
        DO: 
          IF res-line.resstatus NE 13 THEN 
          DO:
            tmp-list[i] = tmp-list[i] + res-line.zimmeranz. 
            room-list.room[i] = room-list.room[i] + res-line.zimmeranz. 
          END.
          FIND FIRST segm-list 
            WHERE segm-list.segmentcode = reservation.segmentcode NO-ERROR. 
          IF AVAILABLE segm-list AND res-line.resstatus NE 13 THEN 
            segm-list.segm[i] = segm-list.segm[i] + res-line.zimmeranz. 
          pers-list[i] = pers-list[i] + pax + res-line.kind1 + res-line.kind2 
            + res-line.l-zuordnung[4] + res-line.gratis. 
        END. 
 
/* will be vacant */ 
        ELSE IF res-line.abreise = datum AND do-it AND res-line.resstatus NE 13 THEN 
        DO: 
          avail-list[i] = avail-list[i] + res-line.zimmeranz. 
        END. 
        i = i + 1. 
      END. 
    END.  /* if do it... */
  END. 
 
  i = 0. 
  DO datum = curr-date TO to-date: 
    i = i + 1. 
    FOR EACH queasy WHERE queasy.key = 14 AND 
      queasy.date1 LE datum AND queasy.date2 GE datum NO-LOCK, 
      FIRST room WHERE room.zinr = queasy.char1 AND room.sleeping NO-LOCK: 
      room-list.room[i] = room-list.room[i] + 1. 
      /*tmp-list[i] = tmp-list[i] + 1. */
      pers-list[i] = pers-list[i] + queasy.number1. 
      FIND FIRST guestseg WHERE guestseg.gastnr = queasy.number3 
        AND guestseg.reihenfolge = 1 NO-LOCK NO-ERROR. 
      IF NOT AVAILABLE guestseg THEN 
      FIND FIRST guestseg WHERE guestseg.gastnr = queasy.number3 
        NO-LOCK NO-ERROR. 
      IF AVAILABLE guestseg THEN 
      DO: 
        FIND FIRST segm-list WHERE segm-list.segmentcode 
          = guestseg.segmentcode NO-ERROR. 
        IF AVAILABLE segm-list THEN segm-list.segm[i] = segm-list.segm[i] + 1. 
      END. 
    END. 
  END. 
 
  CREATE room-list. 
  room-list.nr = 4. 
  room-list.bezeich = translateExtended ("Guaranted",lvCAREA,""). 
  last-resnr = 0. 

  FOR EACH res-line WHERE (resstatus = 1) 
    AND active-flag = 0 
    AND NOT (res-line.ankunft GT to-date) 
    AND NOT (res-line.abreise LT curr-date) 
    AND res-line.l-zuordnung[3] = 0 
    NO-LOCK: 
 
    IF NOT vhp-limited THEN do-it = YES.
    ELSE
    DO:
      FIND FIRST reservation WHERE reservation.resnr = res-line.resnr
        NO-LOCK NO-ERROR.
      FIND FIRST segment WHERE segment.segmentcode = reservation.segmentcode
        NO-LOCK NO-ERROR.
      do-it = AVAILABLE segment AND segment.vip-level = 0.
    END.

    IF do-it THEN
    DO:
      do-it = NO. 
      FIND FIRST zimmer WHERE zimmer.zinr = res-line.zinr NO-LOCK NO-ERROR. 
      IF NOT AVAILABLE zimmer THEN do-it = YES. 
      ELSE 
      DO: 
        FIND FIRST queasy WHERE queasy.key = 14 AND queasy.char1 = res-line.zinr 
          AND queasy.date1 LE datum AND queasy.date2 GE datum NO-LOCK NO-ERROR. 
        IF zimmer.sleeping THEN 
        DO: 
          IF NOT AVAILABLE queasy THEN do-it = YES. 
          ELSE IF AVAILABLE queasy AND queasy.number3 NE res-line.gastnr THEN 
            do-it = YES. 
        END. 
        ELSE 
        DO: 
          IF AVAILABLE queasy AND queasy.number3 NE res-line.gastnr 
            AND res-line.zipreis GT 0 THEN do-it = YES. 
        END. 
      END. 
 
      IF do-it THEN 
      DO: 
        IF last-resnr NE res-line.resnr THEN 
          FIND FIRST reservation WHERE reservation.resnr = res-line.resnr 
            NO-LOCK NO-ERROR. 
        last-resnr = res-line.resnr. 
 
/* will be vacant */ 
/* Rulita 090125 | Fixing serverless issue git 190  */
        /* i = res-line.abreise - curr-date + 1.  */
        tmp-date  = res-line.abreise - curr-date.
        i         = tmp-date + 1.
/* End Rulita */

        IF i GE 1 AND i LE 19 THEN 
          avail-list[i] = avail-list[i] + res-line.zimmeranz. 
 
        datum1 = curr-date. 
        i = 1. 
        IF res-line.ankunft GT curr-date THEN 
        DO: 
          datum1 = res-line.ankunft. 
          /* Rulita 090125 | Fixing serverless issue git 190  */
          /* i = res-line.ankunft - curr-date + 1.  */
          tmp-date  = res-line.ankunft - curr-date.
          i         = tmp-date + 1.
          /* End Rulita */
        END. 
        datum2 = curr-date + 18. 
        abreise1 = res-line.abreise - 1. 
        IF abreise1 LT datum2 THEN datum2 = abreise1. 
        /*Day use*/
        IF res-line.ankunft = res-line.abreise THEN datum2 = res-line.abreise.

        DO datum = datum1 TO datum2: 
          pax = res-line.erwachs. 
          FIND FIRST reslin-queasy WHERE reslin-queasy.key = "arrangement" 
            AND reslin-queasy.resnr = res-line.resnr 
            AND reslin-queasy.reslinnr = res-line.reslinnr 
            AND reslin-queasy.date1 LE datum 
            AND reslin-queasy.date2 GE datum NO-LOCK NO-ERROR. 
          IF AVAILABLE reslin-queasy AND reslin-queasy.number3 NE 0 THEN 
            pax = reslin-queasy.number3. 
          IF resstatus = 1 THEN 
          DO: 
            IF disp-flag THEN 
            DO: 
              IF res-line.ankunft LT datum THEN 
              DO: 
                inhouse[i] = inhouse[i] + res-line.zimmeranz. 
              END. 
              ELSE 
              room-list.room[i] = room-list.room[i] + res-line.zimmeranz. 
            END. 
            ELSE room-list.room[i] = room-list.room[i] + res-line.zimmeranz. 
            tmp-list[i] = tmp-list[i] + res-line.zimmeranz. 
            FIND FIRST segm-list 
              WHERE segm-list.segmentcode = reservation.segmentcode NO-ERROR. 
            IF AVAILABLE segm-list THEN 
              segm-list.segm[i] = segm-list.segm[i] + res-line.zimmeranz. 
          END. 
          pers-list[i] = pers-list[i] 
            + (pax + res-line.kind1 + res-line.kind2 + res-line.l-zuordnung[4] 
               + res-line.gratis) * res-line.zimmeranz. 
          i = i + 1. 
        END. 
      END.
    END.  /* IF do-it */
  END. 
 
  CREATE room-list. 
  room-list.nr = 5. 
  room-list.bezeich = translateExtended ("6 PM",lvCAREA,""). 
  FIND FIRST htparam WHERE htparam.paramnr = 297 NO-LOCK.
  IF htparam.finteger NE 0 THEN room-list.bezeich = STRING(htparam.finteger) 
    + " " + translateExtended ("PM",lvCAREA,""). 

  last-resnr = 0. 
  
  FOR EACH res-line WHERE res-line.resstatus = 2 AND active-flag = 0 
    AND NOT (res-line.ankunft GT to-date) 
    AND NOT (res-line.abreise LT curr-date) 
    AND res-line.l-zuordnung[3] = 0 NO-LOCK: 
 
    IF NOT vhp-limited THEN do-it = YES.
    ELSE
    DO:
      FIND FIRST reservation WHERE reservation.resnr = res-line.resnr
        NO-LOCK NO-ERROR.
      FIND FIRST segment WHERE segment.segmentcode = reservation.segmentcode
        NO-LOCK NO-ERROR.
      do-it = AVAILABLE segment AND segment.vip-level = 0.
    END.

    IF do-it THEN
    DO:
      do-it = NO. 
      FIND FIRST zimmer WHERE zimmer.zinr = res-line.zinr NO-LOCK NO-ERROR. 
      IF NOT AVAILABLE zimmer THEN do-it = YES. 
      ELSE 
      DO: 
        FIND FIRST queasy WHERE queasy.key = 14 AND queasy.char1 = res-line.zinr 
          AND queasy.date1 LE datum AND queasy.date2 GE datum NO-LOCK NO-ERROR. 
        IF zimmer.sleeping THEN 
        DO: 
          IF NOT AVAILABLE queasy THEN do-it = YES. 
          ELSE IF AVAILABLE queasy AND queasy.number3 NE res-line.gastnr THEN 
            do-it = YES. 
        END. 
        ELSE 
        DO: 
          IF AVAILABLE queasy AND queasy.number3 NE res-line.gastnr 
            AND res-line.zipreis GT 0 THEN do-it = YES. 
        END. 
      END. 
 
      IF do-it THEN 
      DO: 
        IF last-resnr NE res-line.resnr THEN 
          FIND FIRST reservation WHERE reservation.resnr = res-line.resnr 
            NO-LOCK NO-ERROR. 
        last-resnr = res-line.resnr. 
 
/* will be vacant */ 
/* Rulita 090125 | Fixing serverless issue git 190  */
        /* i = res-line.abreise - curr-date + 1.  */
        tmp-date  = res-line.abreise - curr-date.
        i         = tmp-date + 1.
/* End Rulita */

        IF i GE 1 AND i LE 19 THEN avail-list[i] = avail-list[i] 
          + res-line.zimmeranz. 
 
        datum1 = curr-date. 
        i = 1. 
        IF res-line.ankunft GT curr-date THEN 
        DO: 
          datum1 = res-line.ankunft. 
          /* Rulita 090125 | Fixing serverless issue git 190  */
          /* i = res-line.ankunft - curr-date + 1.  */
          tmp-date  = res-line.ankunft - curr-date.
          i         = tmp-date + 1.
          /* End Rulita */
        END. 
        datum2 = curr-date + 18. 
        abreise1 = res-line.abreise - 1. 
        IF abreise1 LT datum2 THEN datum2 = abreise1. 
        /*Day use*/
        IF res-line.ankunft = res-line.abreise THEN datum2 = res-line.abreise.
        DO datum = datum1 TO datum2: 
          pax = res-line.erwachs. 
          FIND FIRST reslin-queasy WHERE reslin-queasy.key = "arrangement" 
            AND reslin-queasy.resnr = res-line.resnr 
            AND reslin-queasy.reslinnr = res-line.reslinnr 
            AND reslin-queasy.date1 LE datum 
            AND reslin-queasy.date2 GE datum NO-LOCK NO-ERROR. 
          IF AVAILABLE reslin-queasy AND reslin-queasy.number3 NE 0 THEN 
            pax = reslin-queasy.number3. 
          IF disp-flag THEN 
          DO: 
            IF res-line.ankunft LT datum THEN 
            DO: 
              inhouse[i] = inhouse[i] + res-line.zimmeranz. 
            END. 
            ELSE 
            room-list.room[i] = room-list.room[i] + res-line.zimmeranz. 
          END. 
          ELSE room-list.room[i] = room-list.room[i] + res-line.zimmeranz. 
          tmp-list[i] = tmp-list[i] + res-line.zimmeranz. 
          pers-list[i] = pers-list[i] 
            + (pax + res-line.kind1 + res-line.kind2 + res-line.l-zuordnung[4] 
              + res-line.gratis) * res-line.zimmeranz. 
          FIND FIRST segm-list 
            WHERE segm-list.segmentcode = reservation.segmentcode NO-ERROR. 
          IF AVAILABLE segm-list THEN 
            segm-list.segm[i] = segm-list.segm[i] + res-line.zimmeranz. 
          i = i + 1. 
        END. 
      END.
    END.  /* IF do-it */
  END. 
 
  CREATE room-list. 
  room-list.nr = 6. 
  room-list.bezeich = translateExtended ("Verbal Confirmed",lvCAREA,""). 
  last-resnr = 0. 
  
  FOR EACH res-line WHERE res-line.resstatus = 5 AND active-flag = 0 
    AND NOT (res-line.ankunft GT to-date) 
    AND NOT (res-line.abreise LT curr-date) 
    AND res-line.l-zuordnung[3] = 0 NO-LOCK: 
 
    IF NOT vhp-limited THEN do-it = YES.
    ELSE
    DO:
      FIND FIRST reservation WHERE reservation.resnr = res-line.resnr
        NO-LOCK NO-ERROR.
      FIND FIRST segment WHERE segment.segmentcode = reservation.segmentcode
        NO-LOCK NO-ERROR.
      do-it = AVAILABLE segment AND segment.vip-level = 0.
    END.

    IF do-it THEN
    DO:
      do-it = NO. 
      FIND FIRST zimmer WHERE zimmer.zinr = res-line.zinr NO-LOCK NO-ERROR. 
      IF NOT AVAILABLE zimmer THEN do-it = YES. 
      ELSE 
      DO: 
        FIND FIRST queasy WHERE queasy.key = 14 AND queasy.char1 = res-line.zinr 
          AND queasy.date1 LE datum AND queasy.date2 GE datum NO-LOCK NO-ERROR. 
        IF zimmer.sleeping THEN 
        DO: 
          IF NOT AVAILABLE queasy THEN do-it = YES. 
          ELSE IF AVAILABLE queasy AND queasy.number3 NE res-line.gastnr THEN 
            do-it = YES. 
        END. 
        ELSE 
        DO: 
          IF AVAILABLE queasy AND queasy.number3 NE res-line.gastnr 
            AND res-line.zipreis GT 0 THEN do-it = YES. 
        END. 
      END. 
 
      IF do-it THEN 
      DO: 
        IF last-resnr NE res-line.resnr THEN 
          FIND FIRST reservation WHERE reservation.resnr = res-line.resnr 
            NO-LOCK NO-ERROR. 
        last-resnr = res-line.resnr. 
 
/* will be vacant */ 
/* Rulita 090125 | Fixing serverless issue git 190  */
        /* i = res-line.abreise - curr-date + 1.  */
        tmp-date  = res-line.abreise - curr-date.
        i         = tmp-date + 1.
/* End Rulita */

        IF i GE 1 AND i LE 19 THEN avail-list[i] = avail-list[i] 
          + res-line.zimmeranz. 
 
        datum1 = curr-date. 
        i = 1. 
        IF res-line.ankunft GT curr-date THEN 
        DO: 
          datum1 = res-line.ankunft. 
          /* Rulita 090125 | Fixing serverless issue git 190  */
          /* i = res-line.ankunft - curr-date + 1.  */
          tmp-date  = res-line.ankunft - curr-date.
          i         = tmp-date + 1.
          /* End Rulita */
        END. 
        datum2 = curr-date + 18. 
        abreise1 = res-line.abreise - 1. 
        IF abreise1 LT datum2 THEN datum2 = abreise1. 
        /*Day use*/
        IF res-line.ankunft = res-line.abreise THEN datum2 = res-line.abreise.
        DO datum = datum1 TO datum2: 
          pax = res-line.erwachs. 
          FIND FIRST reslin-queasy WHERE reslin-queasy.key = "arrangement" 
            AND reslin-queasy.resnr = res-line.resnr 
            AND reslin-queasy.reslinnr = res-line.reslinnr 
            AND reslin-queasy.date1 LE datum 
            AND reslin-queasy.date2 GE datum NO-LOCK NO-ERROR. 
          IF AVAILABLE reslin-queasy AND reslin-queasy.number3 NE 0 THEN 
            pax = reslin-queasy.number3. 
          IF disp-flag THEN 
          DO: 
            IF res-line.ankunft LT datum THEN 
            DO: 
              inhouse[i] = inhouse[i] + res-line.zimmeranz. 
            END. 
            ELSE 
            room-list.room[i] = room-list.room[i] + res-line.zimmeranz. 
          END. 
          ELSE room-list.room[i] = room-list.room[i] + res-line.zimmeranz. 
          tmp-list[i] = tmp-list[i] + res-line.zimmeranz. 
          pers-list[i] = pers-list[i] 
            + (pax + res-line.kind1 + res-line.kind2 + res-line.l-zuordnung[4] 
               + res-line.gratis) * res-line.zimmeranz. 
          FIND FIRST segm-list 
            WHERE segm-list.segmentcode = reservation.segmentcode NO-ERROR. 
          IF AVAILABLE segm-list THEN 
            segm-list.segm[i] = segm-list.segm[i] + res-line.zimmeranz. 
          i = i + 1. 
        END. 
      END.
    END.  /* IF do-it */
  END. 
 
  CREATE room-list. 
  room-list.nr = 7. 
  room-list.bezeich = translateExtended ("Global Reserve",lvCAREA,""). 
  i = 0. 
  DO datum = curr-date TO to-date: 
    i = i + 1. 
    FOR EACH kontline WHERE kontline.betriebsnr = 1 
      AND kontline.ankunft LE datum AND kontline.abreise GE datum 
      AND kontline.kontstat = 1 NO-LOCK: 
      room-list.room[i] = room-list.room[i] + kontline.zimmeranz. 
      tmp-list[i] = tmp-list[i] + kontline.zimmeranz. 
      pers-list[i] = pers-list[i] + (kontline.erwachs + kontline.kind1 
        /*+ kontline.kind2*/) * kontline.zimmeranz. 
      FIND FIRST segm-list  WHERE segm-list.segmentcode = 99999. 
      segm-list.segm[i] = segm-list.segm[i] + kontline.zimmeranz. 
      tmp-list[i] = tmp-list[i] - kontline.zimmeranz. /*added 23 may 08*/
    END. 
 
    FOR EACH res-line WHERE res-line.active-flag LE 1 
      AND res-line.resstatus LE 13 AND res-line.resstatus NE 3 
      AND res-line.resstatus NE 4  AND res-line.resstatus NE 12
      AND res-line.ankunft LE datum AND res-line.abreise GT datum 
      AND res-line.kontignr LT 0 AND res-line.l-zuordnung[3] = 0 NO-LOCK: 

      do-it = YES. 
      IF res-line.zinr NE "" THEN 
      DO: 
        FIND FIRST zimmer WHERE zimmer.zinr = res-line.zinr NO-LOCK. 
        do-it = zimmer.sleeping. 
      END. 
      
      IF do-it AND vhp-limited THEN
      DO:
        FIND FIRST reservation WHERE reservation.resnr = res-line.resnr
          NO-LOCK NO-ERROR.
        FIND FIRST segment WHERE segment.segmentcode = reservation.segmentcode
          NO-LOCK NO-ERROR.
        do-it = AVAILABLE segment AND segment.vip-level = 0.
      END.
      
      IF do-it THEN 
      DO: 
        IF (res-line.resstatus NE 11 AND res-line.resstatus NE 13) THEN
        DO:
          room-list.room[i] = room-list.room[i] - res-line.zimmeranz. 
          /*tmp-list[i] = tmp-list[i] - res-line.zimmeranz.  23 May 08*/
        END.
        FIND FIRST kontline WHERE kontline.gastnr = res-line.gastnr 
          AND kontline.ankunft EQ datum 
          AND kontline.zikatnr EQ res-line.zikatnr 
          AND kontline.betriebsnr = 1 NO-LOCK NO-ERROR. 
        IF AVAILABLE kontline THEN pers-list[i] = pers-list[i] 
            - (kontline.erwachs + kontline.kind1 /*+ kontline.kind2*/) 
            * res-line.zimmeranz. 
        ELSE pers-list[i] = pers-list[i] - res-line.erwachs * res-line.zimmeranz. 
      END. 
    END. 
  END. 
 /*18 Feb 09*/
  CREATE sum-list. 
  sum-list.bezeich = translateExtended ("Tentative",lvCAREA,""). 
  i = 1. 
  datum = curr-date. 
  DO WHILE i LE 19: 
    FOR EACH res-line WHERE res-line.active-flag = 0 AND res-line.ankunft
      LE datum AND res-line.abreise GT datum
      AND res-line.resstatus = 3 AND res-line.l-zuordnung[3] = 0 NO-LOCK:
      sum-list.summe[i] = sum-list.summe[i] + res-line.zimmeranz. 
      IF incl-tent THEN
          ASSIGN 
          /*tmp-list[i] = tmp-list[i] + res-line.zimmeranz*/
          pers-list[i] = pers-list[i] + res-line.erwachs * res-line.zimmeranz.
    END. 
    i = i + 1. 
    datum = datum + 1. 
  END.  
 
  FIND FIRST room-list WHERE room-list.bez1 = "Resident". 
  DO i = 1 TO 19: 
    room-list.room[i] = room-list.room[i] + inhouse[i]. 
  END. 
 
  CREATE room-list. 
  room-list.nr = 8. 
  room-list.bezeich = translateExtended ("Total Guests",lvCAREA,""). 
  DO i = 1 TO 19: 
    room-list.room[i] = pers-list[i]. 
  END. 
 
  CREATE room-list. 
  room-list.nr = 9. 
  room-list.bezeich = translateExtended ("Total OCC Rooms",lvCAREA,""). 
  DO i = 1 TO 19: 
    room-list.room[i] = tmp-list[i]. 
  END. 
 
  CREATE room-list. 
  room-list.nr = 10. 
  room-list.bezeich = translateExtended ("Room Occ. in %",lvCAREA,""). 
  room-list.flag = "*". 
  DO i = 1 TO 19: 
    room-list.room[i] = (tmp-list[i] / tot-room) * 100. 
  END. 
 
  CREATE room-list. 
  room-list.nr = 11. 
  room-list.bezeich = translateExtended ("Available Rooms",lvCAREA,""). 
  DO i = 1 TO 19: 
    room-list.room[i] = tot-room - tmp-list[i]. 
    avl-tot[i] = room-list.room[i].
/* 
    IF room-list.room[i] LT 0 THEN room-list.room[i] = 0. 
*/ 
  END. 
 
  from-date = curr-date. 
  to-date = from-date + 18. 
  CREATE room-list. 
  room-list.nr = 12. 
  room-list.bezeich = translateExtended ("Allotments",lvCAREA,""). 
  FOR EACH kontline WHERE kontline.betriebsnr = 0 
    AND kontline.kontstat = 1 
    AND NOT (kontline.ankunft GT to-date) 
    AND NOT (kontline.abreise LE from-date) NO-LOCK: 
    i = 1. 
    DO datum = from-date TO to-date: 
      IF datum GE kontline.ankunft AND datum LT kontline.abreise 
        AND datum GE (ci-date + kontline.ruecktage) THEN 
      DO: 
        room-list.room[i] = room-list.room[i] + kontline.zimmeranz. 
        tmp-list[i] = tmp-list[i] + kontline.zimmeranz. 
      END. 
      i = i + 1. 
    END. 
  END. 
  DO i = 1 TO 19: 
    room-list.room[i] = room-list.room[i] - res-allot[i]. 
  END. 
 
  CREATE room-list. 
  room-list.nr = 13. 
  room-list.bezeich = translateExtended ("Occ w/ Allotm %",lvCAREA,""). 
  room-list.flag = "*". 
  DO i = 1 TO 19: 
    room-list.room[i] = (tmp-list[i] / tot-room) * 100. 
  END. 
 
  /* move to --> after create OOO
  FOR EACH room-list WHERE room-list.bezeich NE "" BY room-list.nr: 
    DO i = 1 TO 19: 
      IF room-list.flag = "" THEN coom[i] = STRING(room-list.room[i], "->>>9"). 
      ELSE coom[i] = STRING(room-list.room[i], ">>9.9"). 
    END. 
  END. 
  */
 
 /*
  CREATE sum-list. 
  sum-list.bezeich = translateExtended ("Tentative",lvCAREA,""). 
  i = 1. 
  datum = curr-date. 
  DO WHILE i LE 19: 
    FOR EACH res-line WHERE res-line.active-flag = 0 AND res-line.ankunft
      LE datum AND res-line.abreise GT datum
      AND res-line.resstatus = 3 AND res-line.l-zuordnung[3] = 0 NO-LOCK:
      sum-list.summe[i] = sum-list.summe[i] + res-line.zimmeranz. 
      
    END. 
    i = i + 1. 
    datum = datum + 1. 
  END.  
   */
  CREATE sum-list. 
  sum-list.bezeich = translateExtended ("Waiting List",lvCAREA,""). 
  FOR EACH zimkateg NO-LOCK: 
    i = 1. 
    datum = curr-date. 
    DO WHILE i LE 19: 
      FOR EACH resplan WHERE resplan.datum = datum 
          AND resplan.zikatnr = zimkateg.zikatnr  NO-LOCK: 
        sum-list.summe[i] = sum-list.summe[i] + resplan.anzzim[4]. 
      END. 
      i = i + 1. 
      datum = datum + 1. 
    END. 
  END. 
 
  CREATE sum-list. 
  sum-list.bezeich = translateExtended ("Expect Departure",lvCAREA,""). 
  DO i = 1 TO 19: 
    sum-list.summe[i] = avail-list[i]. 
  END. 

  DO i = 1 TO 19:
      ooo-tot[i] = 0.
  END.
 
  CREATE sum-list. 
  sum-list.bezeich = translateExtended ("Out-of-order",lvCAREA,""). 
  FOR EACH outorder WHERE outorder.betriebsnr LE 1 NO-LOCK, 
    FIRST zimmer WHERE zimmer.zinr = outorder.zinr 
    AND zimmer.sleeping = YES NO-LOCK: 
    datum = curr-date. 
    DO i = 1 TO 19: 
      IF datum GE outorder.gespstart AND datum LE outorder.gespende THEN 
      DO: 
        sum-list.summe[i] = sum-list.summe[i] + 1. 
        ooo-tot[i] = ooo-tot[i] + 1.
      END. 
      datum = datum + 1. 
    END. 
  END. 
  
  IF /*MENU-ITEM mi-lessOOO:CHECKED IN MENU mbar = TRUE*/ lessOO THEN
  DO:
      CREATE room-list.
      ASSIGN 
          room-list.bezeich = translateExtended ("AVL less by OOO",lvCAREA,"")
          room-list.nr = 14. 
      DO i = 1 TO 19:
          room-list.room[i] = avl-tot[i] - ooo-tot[i].
      END.
  END.

  FOR EACH room-list WHERE room-list.bezeich NE "" BY room-list.nr: 
    DO i = 1 TO 19: 
      IF room-list.flag = "" THEN room-list.coom[i] = STRING(room-list.room[i], "->>>9"). 
      ELSE room-list.coom[i] = STRING(room-list.room[i], ">>9.9"). 
    END. 
  END. 
 
  CREATE sum-list. 
  sum-list.bezeich = translateExtended ("Off-Market",lvCAREA,""). 
  FOR EACH outorder WHERE outorder.betriebsnr EQ 2 NO-LOCK, 
    FIRST zimmer WHERE zimmer.zinr = outorder.zinr 
    AND zimmer.sleeping = YES NO-LOCK: 
    datum = curr-date. 
    DO i = 1 TO 19: 
      IF datum GE outorder.gespstart AND datum LE outorder.gespende THEN 
      DO: 
        sum-list.summe[i] = sum-list.summe[i] + 1. 
        om-flag = YES. 
      END. 
      datum = datum + 1. 
    END. 
  END. 
  IF NOT om-flag THEN DELETE sum-list. 
 
END. 
