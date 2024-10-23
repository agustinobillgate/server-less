
/******************** TEMP TABLE ********************/
DEFINE WORKFILE cl-list 
  FIELD segm AS INTEGER 
  FIELD bezeich AS CHAR FORMAT "x(16)" 
  FIELD zimmeranz AS INTEGER 
  FIELD pax AS INTEGER. 

DEFINE TEMP-TABLE walkin-glist 
  FIELD datum       AS DATE                 LABEL "Date" 
  FIELD zinr        LIKE zimmer.zinr        LABEL "RmNo"        INIT ""
  FIELD name        AS CHAR FORMAT "x(32)"  LABEL "Guest Name" 
  FIELD rsv-name    AS CHAR FORMAT "x(32)"  LABEL "Reserve Name"
  FIELD zimmeranz   AS INTEGER FORMAT ">>>" LABEL "Qty" 
  FIELD pax         AS INTEGER FORMAT ">>>" LABEL "Pax" 
  FIELD ankunft     AS DATE                 LABEL "Arrival" 
  FIELD abreise     AS DATE                 LABEL "Departure" 
  FIELD segm        AS CHAR FORMAT "x(24)"  LABEL "Segment Code" 
  FIELD zipreis     AS CHAR FORMAT "x(13)"  LABEL "    Room Rate" 
  FIELD curr        AS CHAR FORMAT "x(4)"   LABEL "Curr" 
  FIELD rstatus     AS CHAR FORMAT "x(8)"   LABEL "Status"
  FIELD rec-id      AS INT. 

DEFINE INPUT PARAMETER pvILanguage  AS INTEGER              NO-UNDO.
DEFINE INPUT PARAMETER arrival-flag  AS LOGICAL.
DEFINE INPUT PARAMETER walkin-flag  AS LOGICAL.
DEFINE INPUT PARAMETER sameday-flag AS LOGICAL.
DEFINE INPUT PARAMETER from-date  AS DATE.
DEFINE INPUT PARAMETER to-date  AS DATE.
DEFINE INPUT PARAMETER ci-date  AS DATE.
DEFINE INPUT PARAMETER walk-in  AS INTEGER.
DEFINE INPUT PARAMETER wi-grp  AS INTEGER.
DEFINE OUTPUT PARAMETER TABLE FOR walkin-glist.

/******************** MAIN LOGIC ********************/
DEFINE VARIABLE wi-int                          AS INTEGER.
FIND FIRST htparam WHERE htparam.paramnr = 109 
    AND htparam.paramgruppe = 7.
    ASSIGN wi-int = htparam.finteger.

DEFINE VARIABLE long-digit AS LOGICAL. 
FIND FIRST htparam WHERE paramnr = 246 NO-LOCK. 
long-digit = htparam.flogical. 
/* >>,>>>,>>>.99 >,>>>,>>>,>>9 */ 

IF NOT arrival-flag THEN RUN create-list.
ELSE RUN create-list1.

/******************** PROCEDURE ********************/
PROCEDURE create-list:
DEFINE VARIABLE datum   AS DATE. 
DEFINE VARIABLE t-anz   AS INTEGER INITIAL 0. 
DEFINE VARIABLE t-pax   AS INTEGER INITIAL 0. 
DEFINE VARIABLE tot-anz AS INTEGER INITIAL 0. 
DEFINE VARIABLE tot-pax AS INTEGER INITIAL 0. 
  FOR EACH walkin-glist: 
    delete walkin-glist. 
  END. 
  FOR EACH cl-list: 
    delete cl-list. 
  END. 
  
  DO datum = from-date TO to-date: 
    t-anz = 0. 
    t-pax = 0. 
    IF datum GE ci-date THEN 
    DO:
      IF NOT walkin-flag THEN
      DO:
        FOR EACH res-line WHERE res-line.active-flag = 1 AND 
            res-line.resstatus NE 12 AND res-line.gastnr EQ wi-int
            NO-LOCK BY res-line.zinr : 
            FIND FIRST reservation WHERE reservation.resnr = res-line.resnr
              NO-LOCK.
            FIND FIRST segment WHERE segment.segmentcode = reservation.segmentcode
              NO-LOCK.
            DO:
              CREATE walkin-glist. 
              ASSIGN 
                walkin-glist.datum = datum 
                walkin-glist.zinr = res-line.zinr 
                walkin-glist.name = res-line.name 
                walkin-glist.rsv-name = reservation.name
                walkin-glist.zimmeranz = res-line.zimmeranz 
                walkin-glist.pax = res-line.erwachs + res-line.gratis 
                walkin-glist.ankunft = res-line.ankunft 
                walkin-glist.abreise = res-line.abreise 
                walkin-glist.segm = ENTRY(1, segment.bezeich, "$$0") 
                walkin-glist.rstatus = "In-House"
                walkin-glist.rec-id = RECID(res-line)
              . 
              IF long-digit THEN 
                walkin-glist.zipreis = STRING(res-line.zipreis, ">,>>>,>>>,>>9"). 
              ELSE walkin-glist.zipreis = STRING(res-line.zipreis, ">>,>>>,>>9.99"). 
              FIND FIRST waehrung WHERE waehrung.waehrungsnr = res-line.betriebsnr 
                NO-LOCK NO-ERROR. 
              IF AVAILABLE waehrung THEN walkin-glist.curr = waehrung.wabkurz. 
              t-anz = t-anz + 1. 
              t-pax = t-pax + res-line.erwachs + res-line.gratis. 
            END.
          END.
          IF t-anz NE 0 THEN 
          DO: 
            CREATE walkin-glist. 
            walkin-glist.name = "Total". /*MTWalk-In Segment*/
            walkin-glist.zimmeranz = t-anz. 
            walkin-glist.pax = t-pax. 
            
            create walkin-glist.
            walkin-glist.zinr = "".
        END.
      END.
      ELSE
      DO: 
          FOR EACH res-line WHERE res-line.active-flag = 1 AND 
              res-line.resstatus NE 12 NO-LOCK BY res-line.zinr: 
            FIND FIRST reservation WHERE reservation.resnr = res-line.resnr
              NO-LOCK.
            FIND FIRST segment WHERE segment.segmentcode = reservation.segmentcode
              NO-LOCK.
            IF segment.segmentcode = walk-in OR res-line.gastnr EQ wi-int AND segment.segmentgrup NE 0 THEN
            DO: 
              CREATE walkin-glist. 
              ASSIGN 
                walkin-glist.datum = datum 
                walkin-glist.zinr = res-line.zinr 
                walkin-glist.name = res-line.name 
                walkin-glist.rsv-name = reservation.name
                walkin-glist.zimmeranz = res-line.zimmeranz 
                walkin-glist.pax = res-line.erwachs + res-line.gratis 
                walkin-glist.ankunft = res-line.ankunft 
                walkin-glist.abreise = res-line.abreise 
                walkin-glist.segm = ENTRY(1, segment.bezeich, "$$0") 
                walkin-glist.rstatus = "In-House"
                walkin-glist.rec-id = RECID(res-line)
              . 
              IF long-digit THEN 
                walkin-glist.zipreis = STRING(res-line.zipreis, ">,>>>,>>>,>>9"). 
              ELSE walkin-glist.zipreis = STRING(res-line.zipreis, ">>,>>>,>>9.99"). 
              FIND FIRST waehrung WHERE waehrung.waehrungsnr = res-line.betriebsnr 
                NO-LOCK NO-ERROR. 
              IF AVAILABLE waehrung THEN walkin-glist.curr = waehrung.wabkurz. 
              t-anz = t-anz + 1. 
              t-pax = t-pax + res-line.erwachs + res-line.gratis. 
            END.
          END.
          IF t-anz NE 0 THEN 
          DO: 
            CREATE walkin-glist. 
            walkin-glist.name = "Total". 
            walkin-glist.zimmeranz = t-anz. 
            walkin-glist.pax = t-pax. 
            
            create walkin-glist.
            walkin-glist.zinr = "".
          END.
      END.
      IF sameday-flag THEN RUN proc-sameday-flag(datum).
    END.
    ELSE 
    DO:
      IF NOT walkin-flag THEN
      DO: 
        FOR EACH res-line WHERE (res-line.active-flag = 1 AND 
            res-line.resstatus NE 12 
            AND res-line.ankunft LE datum AND res-line.abreise GE datum) 
            OR (res-line.active-flag = 2 AND res-line.resstatus = 8 
                AND ((res-line.ankunft LE datum AND res-line.abreise GT datum) OR 
                    (res-line.ankunft = res-line.abreise AND res-line.ankunft = datum)) 
                AND (res-line.gratis + res-line.erwachs) GT 0) 
            NO-LOCK BY res-line.zinr:
            FIND FIRST reservation WHERE reservation.resnr = res-line.resnr
              NO-LOCK.
            FIND FIRST segment WHERE segment.segmentcode = reservation.segmentcode
              NO-LOCK.
            IF res-line.gastnr EQ wi-int THEN
            DO:
              CREATE walkin-glist. 
              ASSIGN 
                walkin-glist.datum = datum 
                walkin-glist.zinr = res-line.zinr 
                walkin-glist.name = res-line.name 
                walkin-glist.rsv-name = reservation.name
                walkin-glist.zimmeranz = res-line.zimmeranz 
                walkin-glist.pax = res-line.erwachs + res-line.gratis 
                walkin-glist.ankunft = res-line.ankunft 
                walkin-glist.abreise = res-line.abreise 
                walkin-glist.segm = ENTRY(1, segment.bezeich, "$$0")
                walkin-glist.rec-id = RECID(res-line)
              . 
              IF res-line.active-flag = 1 THEN walkin-glist.rstatus = "In-House". 
              ELSE walkin-glist.rstatus = "Departed". 
              IF long-digit THEN 
                walkin-glist.zipreis = STRING(res-line.zipreis, ">,>>>,>>>,>>9"). 
              ELSE walkin-glist.zipreis = STRING(res-line.zipreis, ">>,>>>,>>9.99"). 
              FIND FIRST waehrung WHERE waehrung.waehrungsnr = res-line.betriebsnr 
                NO-LOCK NO-ERROR. 
              IF AVAILABLE waehrung THEN walkin-glist.curr = waehrung.wabkurz. 
              t-anz = t-anz + 1. 
              t-pax = t-pax + res-line.erwachs + res-line.gratis. 
            END.
          END.
          IF t-anz NE 0 THEN 
          DO: 
            create walkin-glist. 
            walkin-glist.name = "Total". 
            walkin-glist.zimmeranz = t-anz. 
            walkin-glist.pax = t-pax. 
            
            create walkin-glist.
            walkin-glist.zinr = "".
        END.
      END. 
      ELSE
      DO:
          FOR EACH res-line WHERE (res-line.active-flag = 1 AND 
            res-line.resstatus NE 12 
            AND res-line.ankunft LE datum AND res-line.abreise GE datum) 
            OR (res-line.active-flag = 2 AND res-line.resstatus = 8 
                AND ((res-line.ankunft LE datum AND res-line.abreise GT datum) OR 
                    (res-line.ankunft = res-line.abreise AND res-line.ankunft = datum)) 
                AND (res-line.gratis + res-line.erwachs) GT 0) 
            NO-LOCK
            BY res-line.zinr:
            FIND FIRST reservation WHERE reservation.resnr = res-line.resnr
              NO-LOCK.
            FIND FIRST segment WHERE segment.segmentcode = reservation.segmentcode
              NO-LOCK.
            IF segment.segmentcode = walk-in OR res-line.gastnr EQ wi-int AND segment.segmentgrup NE 0 THEN
            DO:
              CREATE walkin-glist. 
              ASSIGN 
                walkin-glist.datum = datum 
                walkin-glist.zinr = res-line.zinr 
                walkin-glist.name = res-line.name 
                walkin-glist.rsv-name = reservation.name
                walkin-glist.zimmeranz = res-line.zimmeranz 
                walkin-glist.pax = res-line.erwachs + res-line.gratis 
                walkin-glist.ankunft = res-line.ankunft 
                walkin-glist.abreise = res-line.abreise 
                walkin-glist.segm = ENTRY(1, segment.bezeich, "$$0")
                walkin-glist.rec-id = RECID(res-line)
              . 
              IF res-line.active-flag = 1 THEN walkin-glist.rstatus = "In-House". 
              ELSE walkin-glist.rstatus = "Departed". 
              IF long-digit THEN 
                walkin-glist.zipreis = STRING(res-line.zipreis, ">,>>>,>>>,>>9"). 
              ELSE walkin-glist.zipreis = STRING(res-line.zipreis, ">>,>>>,>>9.99"). 
              FIND FIRST waehrung WHERE waehrung.waehrungsnr = res-line.betriebsnr 
                NO-LOCK NO-ERROR. 
              IF AVAILABLE waehrung THEN walkin-glist.curr = waehrung.wabkurz. 
              t-anz = t-anz + 1. 
              t-pax = t-pax + res-line.erwachs + res-line.gratis. 
            END.
          END.
          IF t-anz NE 0 THEN 
          DO: 
            create walkin-glist. 
            walkin-glist.name = "Total". 
            walkin-glist.zimmeranz = t-anz. 
            walkin-glist.pax = t-pax. 
            
            create walkin-glist.
            walkin-glist.zinr = "".
          END.
      END.
      IF sameday-flag THEN RUN proc-sameday-flag(datum).
    END. 
  END. 

  DEF VAR gtot-pax AS INT.
  DEF VAR gtot-anz AS INT.
  DEF VAR gtot-smday-pax AS INT.
  DEF VAR gtot-smday-anz AS INT.
  FOR EACH walkin-glist WHERE walkin-glist.NAME MATCHES "Total" 
      OR walkin-glist.NAME MATCHES "Total Same day Rsv":
      IF walkin-glist.NAME MATCHES "Total" THEN
          ASSIGN
          gtot-pax = gtot-pax + walkin-glist.pax
          gtot-anz = gtot-anz + walkin-glist.zimmeranz.
      ELSE  IF walkin-glist.NAME MATCHES "Total Same day Rsv" THEN
          ASSIGN
          gtot-smday-pax = gtot-smday-pax + walkin-glist.pax
          gtot-smday-anz = gtot-smday-anz + walkin-glist.zimmeranz.
  END.
  
  create walkin-glist. 
  walkin-glist.name = "Grand Total".
  walkin-glist.zimmeranz = gtot-anz. 
  walkin-glist.pax = gtot-pax. 
  IF sameday-flag THEN
  DO:
      create walkin-glist. 
      walkin-glist.name = "Grand Total Same Day Rsv". 
      walkin-glist.zimmeranz = gtot-smday-anz. 
      walkin-glist.pax = gtot-smday-pax. 
  END.
  create walkin-glist.
  walkin-glist.zinr = "".
END.  


PROCEDURE create-list1: 
DEFINE VARIABLE datum   AS DATE. 
DEFINE VARIABLE t-anz   AS INTEGER INITIAL 0. 
DEFINE VARIABLE t-pax   AS INTEGER INITIAL 0. 
DEFINE VARIABLE tot-anz AS INTEGER INITIAL 0. 
DEFINE VARIABLE tot-pax AS INTEGER INITIAL 0. 
  FOR EACH walkin-glist: 
    delete walkin-glist. 
  END. 
  FOR EACH cl-list: 
    delete cl-list. 
  END. 
  
  DO datum = from-date TO to-date: 
    t-anz = 0. 
    t-pax = 0. 
    IF datum GE ci-date THEN 
    DO: 
      IF NOT walkin-flag THEN
      DO:
        FOR EACH res-line WHERE res-line.active-flag = 1 AND 
            res-line.resstatus NE 12 AND res-line.gastnr EQ wi-int
            AND res-line.ankunft = datum
            NO-LOCK BY res-line.zinr : 
            FIND FIRST reservation WHERE reservation.resnr = res-line.resnr
              NO-LOCK.
            FIND FIRST segment WHERE segment.segmentcode = reservation.segmentcode
              NO-LOCK.
            DO:
              CREATE walkin-glist. 
              ASSIGN 
                walkin-glist.datum = datum 
                walkin-glist.zinr = res-line.zinr 
                walkin-glist.name = res-line.name 
                walkin-glist.rsv-name = reservation.name
                walkin-glist.zimmeranz = res-line.zimmeranz 
                walkin-glist.pax = res-line.erwachs + res-line.gratis 
                walkin-glist.ankunft = res-line.ankunft 
                walkin-glist.abreise = res-line.abreise 
                walkin-glist.segm = ENTRY(1, segment.bezeich, "$$0") 
                walkin-glist.rstatus = "In-House"
                walkin-glist.rec-id = RECID(res-line)
              . 
              IF long-digit THEN 
                walkin-glist.zipreis = STRING(res-line.zipreis, ">,>>>,>>>,>>9"). 
              ELSE walkin-glist.zipreis = STRING(res-line.zipreis, ">>,>>>,>>9.99"). 
              FIND FIRST waehrung WHERE waehrung.waehrungsnr = res-line.betriebsnr 
                NO-LOCK NO-ERROR. 
              IF AVAILABLE waehrung THEN walkin-glist.curr = waehrung.wabkurz. 
              t-anz = t-anz + 1. 
              t-pax = t-pax + res-line.erwachs + res-line.gratis. 
            END.
          END.
          IF t-anz NE 0 THEN 
          DO: 
            CREATE walkin-glist. 
            walkin-glist.name = "Total". /*MTWalk-In Segment*/
            walkin-glist.zimmeranz = t-anz. 
            walkin-glist.pax = t-pax. 
            
            create walkin-glist.
            walkin-glist.zinr = "".
        END.
      END.
      ELSE
      DO: 
          FOR EACH res-line WHERE res-line.active-flag = 1 AND 
              res-line.resstatus NE 12
              AND res-line.ankunft = datum NO-LOCK BY res-line.zinr: 
            FIND FIRST reservation WHERE reservation.resnr = res-line.resnr
              NO-LOCK.
            FIND FIRST segment WHERE segment.segmentcode = reservation.segmentcode
              NO-LOCK.
            IF segment.segmentcode = walk-in OR res-line.gastnr EQ wi-int AND segment.segmentgrup NE 0 THEN
            DO:
              CREATE walkin-glist. 
              ASSIGN 
                walkin-glist.datum = datum 
                walkin-glist.zinr = res-line.zinr 
                walkin-glist.name = res-line.name 
                walkin-glist.rsv-name = reservation.name
                walkin-glist.zimmeranz = res-line.zimmeranz 
                walkin-glist.pax = res-line.erwachs + res-line.gratis 
                walkin-glist.ankunft = res-line.ankunft 
                walkin-glist.abreise = res-line.abreise 
                walkin-glist.segm = ENTRY(1, segment.bezeich, "$$0") 
                walkin-glist.rstatus = "In-House"
                walkin-glist.rec-id = RECID(res-line)
              . 
              IF long-digit THEN 
                walkin-glist.zipreis = STRING(res-line.zipreis, ">,>>>,>>>,>>9"). 
              ELSE walkin-glist.zipreis = STRING(res-line.zipreis, ">>,>>>,>>9.99"). 
              FIND FIRST waehrung WHERE waehrung.waehrungsnr = res-line.betriebsnr 
                NO-LOCK NO-ERROR. 
              IF AVAILABLE waehrung THEN walkin-glist.curr = waehrung.wabkurz. 
              t-anz = t-anz + 1. 
              t-pax = t-pax + res-line.erwachs + res-line.gratis. 
            END.
          END.
          IF t-anz NE 0 THEN 
          DO: 
            CREATE walkin-glist. 
            walkin-glist.name = "Total". 
            walkin-glist.zimmeranz = t-anz. 
            walkin-glist.pax = t-pax. 
            
            create walkin-glist.
            walkin-glist.zinr = "".
          END.
      END.
      IF sameday-flag THEN RUN proc-sameday-flag-show-arr(datum).
    END.

    ELSE 
    DO:
      IF NOT walkin-flag THEN
      DO: 
        FOR EACH res-line WHERE 
            (
             (res-line.active-flag = 1 AND 
              res-line.resstatus NE 12 
              AND res-line.ankunft LE datum AND res-line.abreise GE datum) 
             OR (res-line.active-flag = 2 AND res-line.resstatus = 8 
                AND ((res-line.ankunft LE datum AND res-line.abreise GT datum) OR 
                    (res-line.ankunft = res-line.abreise AND res-line.ankunft = datum)) 
                AND (res-line.gratis + res-line.erwachs) GT 0) 
            )
            AND res-line.ankunft = datum NO-LOCK BY res-line.zinr:
            FIND FIRST reservation WHERE reservation.resnr = res-line.resnr
              NO-LOCK.
            FIND FIRST segment WHERE segment.segmentcode = reservation.segmentcode
              NO-LOCK.
            IF res-line.gastnr EQ wi-int THEN
            DO:
              CREATE walkin-glist. 
              ASSIGN 
                walkin-glist.datum = datum 
                walkin-glist.zinr = res-line.zinr 
                walkin-glist.name = res-line.name 
                walkin-glist.rsv-name = reservation.name
                walkin-glist.zimmeranz = res-line.zimmeranz 
                walkin-glist.pax = res-line.erwachs + res-line.gratis 
                walkin-glist.ankunft = res-line.ankunft 
                walkin-glist.abreise = res-line.abreise 
                walkin-glist.segm = ENTRY(1, segment.bezeich, "$$0")
                walkin-glist.rec-id = RECID(res-line)
              . 
              IF res-line.active-flag = 1 THEN walkin-glist.rstatus = "In-House". 
              ELSE walkin-glist.rstatus = "Departed". 
              IF long-digit THEN 
                walkin-glist.zipreis = STRING(res-line.zipreis, ">,>>>,>>>,>>9"). 
              ELSE walkin-glist.zipreis = STRING(res-line.zipreis, ">>,>>>,>>9.99"). 
              FIND FIRST waehrung WHERE waehrung.waehrungsnr = res-line.betriebsnr 
                NO-LOCK NO-ERROR. 
              IF AVAILABLE waehrung THEN walkin-glist.curr = waehrung.wabkurz. 
              t-anz = t-anz + 1. 
              t-pax = t-pax + res-line.erwachs + res-line.gratis. 
            END.
          END.
          IF t-anz NE 0 THEN 
          DO: 
            create walkin-glist. 
            walkin-glist.name = "Total". 
            walkin-glist.zimmeranz = t-anz. 
            walkin-glist.pax = t-pax. 
            
            create walkin-glist. 
            walkin-glist.zinr = "".
        END.
      END. 
      ELSE
      DO:
          FOR EACH res-line WHERE 
             (
              (res-line.active-flag = 1 AND 
               res-line.resstatus NE 12 
               AND res-line.ankunft LE datum AND res-line.abreise GE datum)
              OR (res-line.active-flag = 2 AND res-line.resstatus = 8 
                AND ((res-line.ankunft LE datum AND res-line.abreise GT datum) OR 
                    (res-line.ankunft = res-line.abreise AND res-line.ankunft = datum)) 
                AND (res-line.gratis + res-line.erwachs) GT 0) 
             )
             AND res-line.ankunft = datum
            NO-LOCK
            BY res-line.zinr:
            FIND FIRST reservation WHERE reservation.resnr = res-line.resnr
              NO-LOCK.
            FIND FIRST segment WHERE segment.segmentcode = reservation.segmentcode
              NO-LOCK.
            IF segment.segmentcode = walk-in OR res-line.gastnr EQ wi-int AND segment.segmentgrup NE 0 THEN
            DO:
              CREATE walkin-glist. 
              ASSIGN 
                walkin-glist.datum = datum 
                walkin-glist.zinr = res-line.zinr 
                walkin-glist.name = res-line.name 
                walkin-glist.rsv-name = reservation.name
                walkin-glist.zimmeranz = res-line.zimmeranz 
                walkin-glist.pax = res-line.erwachs + res-line.gratis 
                walkin-glist.ankunft = res-line.ankunft 
                walkin-glist.abreise = res-line.abreise 
                walkin-glist.segm = ENTRY(1, segment.bezeich, "$$0")
                walkin-glist.rec-id = RECID(res-line)
              . 
              IF res-line.active-flag = 1 THEN walkin-glist.rstatus = "In-House". 
              ELSE walkin-glist.rstatus = "Departed". 
              IF long-digit THEN 
                walkin-glist.zipreis = STRING(res-line.zipreis, ">,>>>,>>>,>>9"). 
              ELSE walkin-glist.zipreis = STRING(res-line.zipreis, ">>,>>>,>>9.99"). 
              FIND FIRST waehrung WHERE waehrung.waehrungsnr = res-line.betriebsnr 
                NO-LOCK NO-ERROR. 
              IF AVAILABLE waehrung THEN walkin-glist.curr = waehrung.wabkurz. 
              t-anz = t-anz + 1. 
              t-pax = t-pax + res-line.erwachs + res-line.gratis. 
            END.
          END.
          IF t-anz NE 0 THEN 
          DO: 
            create walkin-glist. 
            walkin-glist.name = "Total". 
            walkin-glist.zimmeranz = t-anz. 
            walkin-glist.pax = t-pax. 
            
            create walkin-glist. 
            walkin-glist.zinr = "".
          END.
      END.
      IF sameday-flag THEN RUN proc-sameday-flag-show-arr(datum).
    END. 
  END. 
END. 

PROCEDURE proc-sameday-flag:
DEF INPUT PARAMETER datum AS DATE.
DEFINE VARIABLE t-anz-sameday AS INTEGER INITIAL 0. 
DEFINE VARIABLE t-pax-sameday AS INTEGER INITIAL 0. 
DEFINE VARIABLE tot-anz-sameday AS INTEGER INITIAL 0. 
DEFINE VARIABLE tot-pax-sameday AS INTEGER INITIAL 0. 
DEF VAR create-date AS DATE.
DEF VAR a AS INT.

    t-anz-sameday = 0. 
    t-pax-sameday = 0. 
    IF datum GT ci-date THEN
    FOR EACH res-line WHERE res-line.active-flag = 1 AND 
        res-line.resstatus NE 12 AND res-line.gastnr NE wi-int 
        AND res-line.ankunft EQ datum /*MTAND res-line.abreise GE datum*/
        NO-LOCK BY res-line.zinr :
        
        FIND FIRST reservation WHERE reservation.resnr = res-line.resnr
          NO-LOCK.
        FIND FIRST segment WHERE segment.segmentcode = reservation.segmentcode
          NO-LOCK.
        DO: 
          a = RECID(res-line).
          FIND FIRST walkin-glist WHERE walkin-glist.rec-id = a NO-ERROR.
          IF NOT AVAILABLE walkin-glist THEN
          DO: 
              create-date = /*MTDATE(string(res-line.reserve-char, "x(8)")).*/
                  reservation.resdat.
              IF create-date = res-line.ankunft THEN
              DO: 
                  CREATE walkin-glist. 
                  ASSIGN 
                    walkin-glist.datum = from-date 
                    walkin-glist.zinr = res-line.zinr 
                    walkin-glist.name = res-line.name 
                    walkin-glist.rsv-name = reservation.name
                    walkin-glist.zimmeranz = res-line.zimmeranz 
                    walkin-glist.pax = res-line.erwachs + res-line.gratis 
                    walkin-glist.ankunft = res-line.ankunft 
                    walkin-glist.abreise = res-line.abreise 
                    walkin-glist.segm = ENTRY(1, segment.bezeich, "$$0")
                    walkin-glist.rec-id = RECID(res-line)
                  . 
                  IF res-line.active-flag = 1 THEN walkin-glist.rstatus = "In-House".
                  ELSE walkin-glist.rstatus = "Departed".
                  IF long-digit THEN 
                    walkin-glist.zipreis = STRING(res-line.zipreis, ">,>>>,>>>,>>9"). 
                  ELSE walkin-glist.zipreis = STRING(res-line.zipreis, ">>,>>>,>>9.99"). 
                  
                  FIND FIRST waehrung WHERE waehrung.waehrungsnr = res-line.betriebsnr 
                    NO-LOCK NO-ERROR. 
                  IF AVAILABLE waehrung THEN walkin-glist.curr = waehrung.wabkurz. 
                  t-anz-sameday = t-anz-sameday + 1. 
                  t-pax-sameday = t-pax-sameday + res-line.erwachs + res-line.gratis. 
              END.
          END.
        END.
    END. 
    ELSE
    FOR EACH res-line WHERE res-line.active-flag = 1 AND 
        res-line.resstatus NE 12 AND res-line.gastnr NE wi-int 
        AND res-line.ankunft LE datum AND res-line.abreise GE datum
        NO-LOCK BY res-line.zinr :
         
        FIND FIRST reservation WHERE reservation.resnr = res-line.resnr
          NO-LOCK.
        FIND FIRST segment WHERE segment.segmentcode = reservation.segmentcode
          NO-LOCK.
        DO: 
          a = RECID(res-line).
          FIND FIRST walkin-glist WHERE walkin-glist.rec-id = a NO-ERROR.
          IF NOT AVAILABLE walkin-glist THEN
          DO: 
              create-date = /*MTDATE(string(res-line.reserve-char, "x(8)"))*/
                  reservation.resdat.
              IF create-date = res-line.ankunft THEN
              DO: 
                  CREATE walkin-glist. 
                  ASSIGN 
                    walkin-glist.datum = datum 
                    walkin-glist.zinr = res-line.zinr 
                    walkin-glist.name = res-line.name 
                    walkin-glist.rsv-name = reservation.name
                    walkin-glist.zimmeranz = res-line.zimmeranz 
                    walkin-glist.pax = res-line.erwachs + res-line.gratis 
                    walkin-glist.ankunft = res-line.ankunft 
                    walkin-glist.abreise = res-line.abreise 
                    walkin-glist.segm = ENTRY(1, segment.bezeich, "$$0")
                    walkin-glist.rec-id = RECID(res-line)
                  . 
                  IF res-line.active-flag = 1 THEN walkin-glist.rstatus = "In-House".
                  ELSE walkin-glist.rstatus = "Departed".
                  IF long-digit THEN 
                    walkin-glist.zipreis = STRING(res-line.zipreis, ">,>>>,>>>,>>9"). 
                  ELSE walkin-glist.zipreis = STRING(res-line.zipreis, ">>,>>>,>>9.99"). 
                  
                  FIND FIRST waehrung WHERE waehrung.waehrungsnr = res-line.betriebsnr 
                    NO-LOCK NO-ERROR. 
                  IF AVAILABLE waehrung THEN walkin-glist.curr = waehrung.wabkurz. 
                  t-anz-sameday = t-anz-sameday + 1. 
                  t-pax-sameday = t-pax-sameday + res-line.erwachs + res-line.gratis. 
              END.
          END.
        END.
    END. 
    IF t-anz-sameday NE 0 THEN
    DO:
        CREATE walkin-glist. 
        walkin-glist.name = "Total Same day Rsv".
        walkin-glist.zimmeranz = t-anz-sameday.
        walkin-glist.pax = t-pax-sameday. 
        
        create walkin-glist.
        walkin-glist.zinr = "".
    END.
END.

PROCEDURE proc-sameday-flag-show-arr:
    DEFINE VARIABLE t-anz-sameday AS INTEGER INITIAL 0. 
    DEFINE VARIABLE t-pax-sameday AS INTEGER INITIAL 0. 
    DEFINE VARIABLE tot-anz-sameday AS INTEGER INITIAL 0. 
    DEFINE VARIABLE tot-pax-sameday AS INTEGER INITIAL 0. 
    DEF VAR create-date AS DATE.
    DEF INPUT PARAMETER datum AS DATE.
    DEF VAR a AS INT.

    t-anz-sameday = 0. 
    t-pax-sameday = 0.

    IF datum GT ci-date THEN
    FOR EACH res-line WHERE res-line.active-flag = 1 AND 
        res-line.resstatus NE 12 AND res-line.gastnr NE wi-int 
        AND res-line.ankunft EQ datum 
        NO-LOCK BY res-line.zinr :
        FIND FIRST reservation WHERE reservation.resnr = res-line.resnr
          NO-LOCK.
        FIND FIRST segment WHERE segment.segmentcode = reservation.segmentcode
          NO-LOCK.
        DO: 
          a = RECID(res-line).
          FIND FIRST walkin-glist WHERE walkin-glist.rec-id = a NO-ERROR.
          IF NOT AVAILABLE walkin-glist THEN
          DO: 
              create-date = reservation.resdat.
              IF create-date = res-line.ankunft THEN
              DO: 
                  CREATE walkin-glist. 
                  ASSIGN 
                    walkin-glist.datum = from-date 
                    walkin-glist.zinr = res-line.zinr 
                    walkin-glist.name = res-line.name 
                    walkin-glist.rsv-name = reservation.name
                    walkin-glist.zimmeranz = res-line.zimmeranz 
                    walkin-glist.pax = res-line.erwachs + res-line.gratis 
                    walkin-glist.ankunft = res-line.ankunft 
                    walkin-glist.abreise = res-line.abreise 
                    walkin-glist.segm = ENTRY(1, segment.bezeich, "$$0")
                    walkin-glist.rec-id = RECID(res-line)
                  . 
                  IF res-line.active-flag = 1 THEN walkin-glist.rstatus = "In-House".
                  ELSE walkin-glist.rstatus = "Departed".
                  IF long-digit THEN 
                    walkin-glist.zipreis = STRING(res-line.zipreis, ">,>>>,>>>,>>9"). 
                  ELSE walkin-glist.zipreis = STRING(res-line.zipreis, ">>,>>>,>>9.99"). 

                  FIND FIRST waehrung WHERE waehrung.waehrungsnr = res-line.betriebsnr 
                    NO-LOCK NO-ERROR. 
                  IF AVAILABLE waehrung THEN walkin-glist.curr = waehrung.wabkurz. 
                  t-anz-sameday = t-anz-sameday + 1. 
                  t-pax-sameday = t-pax-sameday + res-line.erwachs + res-line.gratis. 
              END.
          END.
        END.
    END. 
    ELSE
    FOR EACH res-line WHERE res-line.active-flag = 1 AND 
        res-line.resstatus NE 12 AND res-line.gastnr NE wi-int 
        AND res-line.ankunft EQ datum NO-LOCK BY res-line.zinr :
        FIND FIRST reservation WHERE reservation.resnr = res-line.resnr
          NO-LOCK.
        FIND FIRST segment WHERE segment.segmentcode = reservation.segmentcode
          NO-LOCK.
        DO: 
          a = RECID(res-line).
          FIND FIRST walkin-glist WHERE walkin-glist.rec-id = a NO-ERROR.
          IF NOT AVAILABLE walkin-glist THEN
          DO: 
              create-date = reservation.resdat.
              IF create-date = res-line.ankunft THEN
              DO: 
                  CREATE walkin-glist. 
                  ASSIGN 
                    walkin-glist.datum = datum 
                    walkin-glist.zinr = res-line.zinr 
                    walkin-glist.name = res-line.name 
                    walkin-glist.rsv-name = reservation.name
                    walkin-glist.zimmeranz = res-line.zimmeranz 
                    walkin-glist.pax = res-line.erwachs + res-line.gratis 
                    walkin-glist.ankunft = res-line.ankunft 
                    walkin-glist.abreise = res-line.abreise 
                    walkin-glist.segm = ENTRY(1, segment.bezeich, "$$0")
                    walkin-glist.rec-id = RECID(res-line)
                  . 
                  IF res-line.active-flag = 1 THEN walkin-glist.rstatus = "In-House".
                  ELSE walkin-glist.rstatus = "Departed".
                  IF long-digit THEN 
                    walkin-glist.zipreis = STRING(res-line.zipreis, ">,>>>,>>>,>>9"). 
                  ELSE walkin-glist.zipreis = STRING(res-line.zipreis, ">>,>>>,>>9.99"). 

                  FIND FIRST waehrung WHERE waehrung.waehrungsnr = res-line.betriebsnr 
                    NO-LOCK NO-ERROR. 
                  IF AVAILABLE waehrung THEN walkin-glist.curr = waehrung.wabkurz. 
                  t-anz-sameday = t-anz-sameday + 1. 
                  t-pax-sameday = t-pax-sameday + res-line.erwachs + res-line.gratis. 
              END.
          END.
        END.
    END. 
    IF t-anz-sameday NE 0 THEN
    DO:
      CREATE walkin-glist. 
      walkin-glist.name = "Total Same day Rsv".
      walkin-glist.zimmeranz = t-anz-sameday.
      walkin-glist.pax = t-pax-sameday. 
      
      create walkin-glist.
      walkin-glist.zinr = "".
    END.
END.

