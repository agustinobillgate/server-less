
DEFINE TEMP-TABLE s-list 
  FIELD zikatnr     LIKE zimkateg.zikatnr
  FIELD kurzbez     LIKE zimkateg.kurzbez
  FIELD bezeichnung LIKE zimkateg.bezeichnung
  FIELD reihenfolge     AS INTEGER INITIAL 0 
  FIELD flag            AS INTEGER INITIAL 0 
  FIELD marknr          AS INTEGER 
  FIELD market          AS CHAR FORMAT "x(18)" 
  FIELD contcode        AS CHAR FORMAT "x(6)" LABEL "Code"
  FIELD kurzbez1        AS CHAR FORMAT "x(6)" COLUMN-LABEL "RmCat  " 
  FIELD setup           AS CHAR FORMAT "x(18)" COLUMN-LABEL "Bed Setup" 
  FIELD nr              AS INTEGER
. 

/* SY 21/09/2014 no longer used ? 
DEFINE TEMP-TABLE rmcat-list
    FIELD rmType    AS CHAR
    FIELD occ-rooms AS INTEGER.
*/

DEFINE TEMP-TABLE dynaRate-list
  FIELD counter  AS INTEGER
  FIELD w-day    AS INTEGER FORMAT "9"     LABEL "WeekDay" INIT 0 /* week day 0=ALL, 1=Mon..7=Sun */
  FIELD rmType   AS CHAR    FORMAT "x(10)" LABEL "Room Type"
  FIELD fr-room  AS INTEGER FORMAT ">,>>9" LABEL "FrRoom" 
  FIELD to-room  AS INTEGER FORMAT ">,>>9" LABEL "ToRoom" 
  FIELD days1    AS INTEGER FORMAT ">>9"   LABEL ">Days2CI"
  FIELD days2    AS INTEGER FORMAT ">>9"   LABEL "<Days2CI"
  FIELD rCode    AS CHAR    FORMAT "x(10)" LABEL "RateCode" /* statcode */
  FIELD dynaCode AS CHAR    FORMAT "x(10)" LABEL "RateCode" /* dynacode */.

DEF INPUT  PARAMETER datum         AS DATE    NO-UNDO.
DEF INPUT  PARAMETER origCode      AS CHAR    NO-UNDO.
DEF INPUT-OUTPUT  PARAMETER prcode AS CHAR    NO-UNDO.
DEF INPUT  PARAMETER curr-marknr   AS INTEGER NO-UNDO.
DEF OUTPUT PARAMETER TABLE FOR s-list.
/*
DEF VAR datum AS DATE INIT 03/01/2010.
DEF VAR origcode AS CHAR INIT "POP".
DEF VAR prcode AS CHAR.
DEF VAR curr-marknr AS INTEGER INIT 0.
*/

DEFINE VARIABLE new-contrate AS LOGICAL                      NO-UNDO.
DEFINE VARIABLE csetup-array AS CHAR FORMAT "x(1)" EXTENT 99 NO-UNDO. 
DEFINE VARIABLE isetup-array AS INTEGER EXTENT 99            NO-UNDO. 
DEFINE VARIABLE anz-setup    AS INTEGER INITIAL 0            NO-UNDO. 
DEFINE VARIABLE ci-date      AS DATE                         NO-UNDO.

DEFINE VARIABLE global-occ  AS LOGICAL INIT NO               NO-UNDO.
DEFINE VARIABLE i-param439  AS INTEGER                       NO-UNDO.

FIND FIRST queasy WHERE queasy.KEY = 2 AND queasy.char1 = origCode 
    NO-LOCK NO-ERROR.
IF NOT AVAILABLE queasy THEN RETURN.

RUN htpint.p(439,    OUTPUT i-param439).
RUN htpdate.p (87,   OUTPUT ci-date).
RUN htplogic.p (550, OUTPUT new-contrate).

RUN get-bedsetup. 

IF new-contrate THEN 
DO:    
  IF queasy.logi2 THEN 
  DO: 
    prcode = origCode.
    RUN create-dynaRate-list.
  END.
  ELSE RUN new-create-list. 
END.
ELSE RUN create-list.

PROCEDURE get-bedsetup: 
  FOR EACH paramtext WHERE paramtext.txtnr GE 9201 
    AND paramtext.txtnr LE 9299 NO-LOCK BY paramtext.txtnr: 
    IF paramtext.notes NE "" THEN 
    DO: 
      anz-setup = anz-setup + 1. 
      csetup-array[anz-setup] = SUBSTR(notes,1,1). 
      isetup-array[anz-setup] = paramtext.txtnr - 9200. 
    END. 
  END. 
END. 

PROCEDURE create-list: 
DEFINE VARIABLE i AS INTEGER. 
  FOR EACH pricecod WHERE pricecod.code = prcode NO-LOCK: 
      FIND FIRST zimkateg WHERE zimkateg.zikatnr = pricecod.zikatnr NO-LOCK 
        NO-ERROR. 
      IF AVAILABLE zimkateg THEN 
      DO: 
        FIND FIRST s-list WHERE s-list.marknr EQ pricecod.marknr 
          AND s-list.zikatnr  EQ zimkateg.zikatnr 
          AND s-list.contcode EQ prcode NO-LOCK NO-ERROR. 
        IF NOT AVAILABLE s-list THEN 
        DO: 
          IF anz-setup GT 0 THEN 
          DO: 
            FIND FIRST zimmer WHERE zimmer.zikatnr = zimkateg.zikatnr 
              AND zimmer.setup = 0 NO-LOCK NO-ERROR. 
            IF AVAILABLE zimmer THEN 
            DO: 
              CREATE s-list. 
              ASSIGN
                s-list.contcode     = prcode
                s-list.zikatnr      = zimkateg.zikatnr
                s-list.kurzbez      = zimkateg.kurzbez 
                s-list.kurzbez1     = zimkateg.kurzbez 
                s-list.bezeichnung  = zimkateg.bezeichnung 
                s-list.marknr       = pricecod.marknr
              . 
              FIND FIRST prmarket WHERE prmarket.nr = pricecod.marknr NO-LOCK 
                NO-ERROR. 
              IF AVAILABLE prmarket THEN s-list.market = prmarket.bezeich. 
            END. 
            DO i = 1 TO anz-setup: 
              FIND FIRST paramtext WHERE paramtext.txtnr 
                = (isetup-array[i] + 9200) NO-LOCK. 
              FIND FIRST zimmer WHERE zimmer.zikatnr = zimkateg.zikatnr 
                AND zimmer.setup = isetup-array[i] NO-LOCK NO-ERROR. 
              IF AVAILABLE zimmer THEN 
              DO: 
                CREATE s-list. 
                ASSIGN
                  s-list.contcode       = prcode
                  s-list.zikatnr        = zimkateg.zikatnr 
                  s-list.kurzbez        = zimkateg.kurzbez 
                  s-list.kurzbez1       = zimkateg.kurzbez 
                    + SUBSTR(paramtext.notes,1,1)
                  s-list.bezeichnung    = zimkateg.bezeichnung 
                  s-list.marknr         = pricecod.marknr
                  s-list.setup          = paramtext.ptexte 
                  s-list.nr             = i
                . 
                FIND FIRST prmarket WHERE prmarket.nr = pricecod.marknr NO-LOCK 
                  NO-ERROR. 
                IF AVAILABLE prmarket THEN s-list.market = prmarket.bezeich. 
              END. 
            END. 
          END. 
          ELSE 
          DO: 
            CREATE s-list. 
            ASSIGN
              s-list.contcode       = prcode
              s-list.zikatnr        = zimkateg.zikatnr
              s-list.kurzbez        = zimkateg.kurzbez 
              s-list.kurzbez1       = zimkateg.kurzbez
              s-list.bezeichnung    = zimkateg.bezeichnung
              s-list.marknr         = pricecod.marknr
            . 
            FIND FIRST prmarket WHERE prmarket.nr = pricecod.marknr NO-LOCK 
              NO-ERROR. 
            IF AVAILABLE prmarket THEN s-list.market = prmarket.bezeich. 
          END. 
        END.
      END.
  END. 
  FOR EACH zimkateg NO-LOCK: 
    FIND FIRST s-list WHERE s-list.zikatnr = zimkateg.zikatnr NO-LOCK NO-ERROR. 
    IF NOT AVAILABLE s-list THEN 
    DO: 
      IF anz-setup GT 0 THEN 
      DO: 
        FIND FIRST zimmer WHERE zimmer.zikatnr = zimkateg.zikatnr 
          AND zimmer.setup = 0 NO-LOCK NO-ERROR. 
        IF AVAILABLE zimmer THEN 
        DO: 
          CREATE s-list. 
          ASSIGN
            s-list.zikatnr      = zimkateg.zikatnr
            s-list.kurzbez      = zimkateg.kurzbez 
            s-list.kurzbez1     = zimkateg.kurzbez 
            s-list.bezeichnung  = zimkateg.bezeichnung 
            s-list.flag     = 1
          . 
        END. 
        DO i = 1 TO anz-setup: 
          FIND FIRST paramtext WHERE paramtext.txtnr 
            = (isetup-array[i] + 9200) NO-LOCK. 
          FIND FIRST zimmer WHERE zimmer.zikatnr = zimkateg.zikatnr 
            AND zimmer.setup = isetup-array[i] NO-LOCK NO-ERROR. 
          IF AVAILABLE zimmer THEN 
          DO: 
            CREATE s-list. 
            ASSIGN
              s-list.zikatnr        = zimkateg.zikatnr
              s-list.kurzbez        = zimkateg.kurzbez 
              s-list.kurzbez1       = zimkateg.kurzbez 
                + SUBSTR(paramtext.notes,1,1)
              s-list.bezeichnung    = zimkateg.bezeichnung
              s-list.setup          = paramtext.ptexte 
              s-list.nr             = i 
              s-list.flag           = 1
            . 
          END. 
        END. 
      END. 
      ELSE 
      DO: 
        CREATE s-list.
        ASSIGN
          s-list.zikatnr        = zimkateg.zikatnr
          s-list.kurzbez        = zimkateg.kurzbez 
          s-list.kurzbez1       = zimkateg.kurzbez 
          s-list.bezeichnung    = zimkateg.bezeichnung 
          s-list.flag     = 1
        . 
      END. 
    END. 
  END. 
  IF curr-marknr NE 0 THEN 
  FOR EACH s-list WHERE s-list.marknr = curr-marknr: 
    s-list.reihenfolge = curr-marknr. 
  END. 
END. 
 
PROCEDURE new-create-list: 
DEFINE VARIABLE i AS INTEGER. 
  FOR EACH ratecode WHERE ratecode.code = prcode NO-LOCK: 
      FIND FIRST zimkateg WHERE zimkateg.zikatnr = ratecode.zikatnr NO-LOCK 
        NO-ERROR. 
      IF AVAILABLE zimkateg THEN 
      DO: 
        FIND FIRST s-list WHERE s-list.marknr EQ ratecode.marknr 
          AND s-list.zikatnr EQ zimkateg.zikatnr 
          AND s-list.contcode EQ prcode NO-LOCK NO-ERROR. 
        IF NOT AVAILABLE s-list THEN 
        DO: 
          IF anz-setup GT 0 THEN 
          DO: 
            FIND FIRST zimmer WHERE zimmer.zikatnr = zimkateg.zikatnr 
              AND zimmer.setup = 0 NO-LOCK NO-ERROR. 
            IF AVAILABLE zimmer THEN 
            DO: 
              CREATE s-list. 
              BUFFER-COPY zimkateg TO s-list.
              ASSIGN
                s-list.contcode = prcode
                s-list.kurzbez1 = zimkateg.kurzbez 
                s-list.marknr   = ratecode.marknr
              . 
              FIND FIRST prmarket WHERE prmarket.nr = ratecode.marknr NO-LOCK 
                NO-ERROR. 
              IF AVAILABLE prmarket THEN s-list.market = prmarket.bezeich. 
            END. 
            DO i = 1 TO anz-setup: 
              FIND FIRST paramtext WHERE paramtext.txtnr 
                = (isetup-array[i] + 9200) NO-LOCK. 
              FIND FIRST zimmer WHERE zimmer.zikatnr = zimkateg.zikatnr 
                AND zimmer.setup = isetup-array[i] NO-LOCK NO-ERROR. 
              IF AVAILABLE zimmer THEN 
              DO: 
                CREATE s-list. 
                BUFFER-COPY zimkateg TO s-list.
                ASSIGN
                  s-list.contcode = prcode
                  s-list.kurzbez1 = zimkateg.kurzbez 
                    + SUBSTR(paramtext.notes,1,1)
                  s-list.marknr   = ratecode.marknr 
                  s-list.setup    = paramtext.ptexte 
                  s-list.nr       = i
                . 
                FIND FIRST prmarket WHERE prmarket.nr = ratecode.marknr NO-LOCK 
                  NO-ERROR. 
                IF AVAILABLE prmarket THEN s-list.market = prmarket.bezeich. 
              END. 
            END. 
          END. 
          ELSE 
          DO: 
            CREATE s-list. 
            BUFFER-COPY zimkateg TO s-list.
            ASSIGN
              s-list.contcode = prcode
              s-list.kurzbez1 = zimkateg.kurzbez 
              s-list.marknr   = ratecode.marknr
            . 
            FIND FIRST prmarket WHERE prmarket.nr = ratecode.marknr NO-LOCK 
              NO-ERROR. 
            IF AVAILABLE prmarket THEN s-list.market = prmarket.bezeich. 
          END. 
        END. 
      END.
  END. 
  FOR EACH zimkateg NO-LOCK: 
    FIND FIRST s-list WHERE s-list.zikatnr = zimkateg.zikatnr NO-LOCK NO-ERROR. 
    IF NOT AVAILABLE s-list THEN 
    DO: 
      IF anz-setup GT 0 THEN 
      DO: 
        FIND FIRST zimmer WHERE zimmer.zikatnr = zimkateg.zikatnr 
          AND zimmer.setup = 0 NO-LOCK NO-ERROR. 
        IF AVAILABLE zimmer THEN 
        DO: 
          CREATE s-list. 
          BUFFER-COPY zimkateg TO s-list.
          ASSIGN
            s-list.kurzbez1 = zimkateg.kurzbez 
            s-list.flag     = 1
          . 
        END. 
        DO i = 1 TO anz-setup: 
          FIND FIRST paramtext WHERE paramtext.txtnr 
            = (isetup-array[i] + 9200) NO-LOCK. 
          FIND FIRST zimmer WHERE zimmer.zikatnr = zimkateg.zikatnr 
            AND zimmer.setup = isetup-array[i] NO-LOCK NO-ERROR. 
          IF AVAILABLE zimmer THEN 
          DO:
            CREATE s-list. 
            BUFFER-COPY zimkateg TO s-list.
            ASSIGN
              s-list.kurzbez1 = zimkateg.kurzbez 
                + SUBSTR(paramtext.notes,1,1)
              s-list.setup    = paramtext.ptexte 
              s-list.nr       = i 
              s-list.flag     = 1
            . 
          END. 
        END. 
      END. 
      ELSE 
      DO: 
        CREATE s-list. 
        BUFFER-COPY zimkateg TO s-list.
        ASSIGN
          s-list.kurzbez1 = zimkateg.kurzbez 
          s-list.flag     = 1
        . 
      END. 
    END. 
  END. 
  IF curr-marknr NE 0 THEN 
  FOR EACH s-list WHERE s-list.marknr = curr-marknr: 
    s-list.reihenfolge = curr-marknr. 
  END. 
END. 

PROCEDURE create-dynaRate-list: 
DEF VAR i                   AS INTEGER           NO-UNDO.
DEF VAR tokcounter          AS INTEGER           NO-UNDO.
DEF VAR ifTask              AS CHAR              NO-UNDO.
DEF VAR mesToken            AS CHAR              NO-UNDO.
DEF VAR mesValue            AS CHAR              NO-UNDO.
DEF VAR mapcode             AS CHAR              NO-UNDO.
DEF VAR occ-rooms           AS INTEGER INITIAL 0 NO-UNDO.
DEF VAR use-it              AS LOGICAL           NO-UNDO.
DEF BUFFER dybuff           FOR dynaRate-list.

  FOR EACH ratecode WHERE ratecode.code = prcode NO-LOCK: 
      CREATE dynaRate-list.
      ifTask = ratecode.char1[5].
      DO tokcounter = 1 TO NUM-ENTRIES(ifTask, ";") - 1:
          mesToken = SUBSTRING(ENTRY(tokcounter, ifTask, ";"), 1, 2).
          mesValue = SUBSTRING(ENTRY(tokcounter, ifTask, ";"), 3).
          CASE mesToken:
              WHEN "CN" THEN dynarate-list.counter = INTEGER(mesValue).
              WHEN "RT" THEN dynaRate-list.rmType = mesValue.
              WHEN "WD" THEN dynarate-list.w-day   = INTEGER(mesValue).
              WHEN "FR" THEN dynaRate-list.fr-room = INTEGER(mesValue).
              WHEN "TR" THEN dynaRate-list.to-room = INTEGER(mesValue).
              WHEN "D1" THEN dynaRate-list.days1   = INTEGER(mesValue).
              WHEN "D2" THEN dynaRate-list.days2   = INTEGER(mesValue).
              WHEN "RC" THEN dynaRate-list.rCode   = mesValue.
          END CASE.
      END.
  END.

/* SY 21/09/2014 */
  FIND FIRST dynarate-list WHERE dynarate-list.rmtype EQ "*"
      NO-ERROR.
  global-occ = AVAILABLE dynarate-list AND i-param439 = 1.
  IF global-occ THEN
  FOR EACH dynarate-list WHERE dynarate-list.rmtype NE "*":
      DELETE dynarate-list.
  END.
  ELSE    
  FOR EACH dynarate-list WHERE dynarate-list.rmtype EQ "*":
      DELETE dynarate-list.
  END.

  FOR EACH dynaRate-list:
/* SY 21/09/2014     
      FIND FIRST rmcat-list WHERE rmcat-list.rmType = dynaRate-list.rmType
          NO-ERROR.
      IF NOT AVAILABLE rmcat-list THEN
      DO:
          CREATE rmcat-list.
          RUN calculate-occupied-roomsbl.p(datum, dynaRate-list.rmType,
              global-occ, OUTPUT occ-rooms).
          ASSIGN
              rmcat-list.rmType    = dynaRate-list.rmType
              rmcat-list.occ-rooms = occ-rooms.
      END.
      ELSE occ-rooms = rmcat-list.occ-rooms.
*/
      RUN calculate-occupied-roomsbl.p(datum, dynaRate-list.rmType,
          global-occ, OUTPUT occ-rooms).
      
      use-it = YES.
      IF dynaRate-list.days1 NE 0 AND (datum - ci-date) LE dynaRate-list.days1 
        THEN use-it = NO.
      IF use-it AND dynaRate-list.days2 NE 0 AND 
        (datum - ci-date) GE dynaRate-list.days2 THEN use-it = NO.
      IF use-it THEN use-it = (dynaRate-list.fr-room LE occ-rooms)
        AND (dynaRate-list.to-room GE occ-rooms).
      IF NOT use-it THEN DELETE dynaRate-list.
      ELSE IF (dynaRate-list.days1 NE 0) OR (dynaRate-list.days2 NE 0) THEN
      FOR EACH dybuff WHERE dybuff.days1 = 0 AND dybuff.days2 = 0
          AND (dybuff.rmtype  EQ dynaRate-list.rmtype)
          AND (dybuff.fr-room LE occ-rooms)
          AND (dybuff.to-room GE occ-rooms):
          DELETE dybuff.
      END.
  END.

  IF global-occ THEN
  FOR EACH dynaRate-list:
    FOR EACH ratecode WHERE ratecode.CODE = dynaRate-list.rcode
        AND ratecode.startperiode LE datum
        AND ratecode.endperiode GE datum NO-LOCK:
      IF curr-marknr = 0 THEN use-it = YES.
      ELSE use-it = (ratecode.marknr = curr-marknr).
      IF use-it THEN
      DO:
        FIND FIRST zimkateg WHERE zimkateg.zikatnr = ratecode.zikatnr NO-LOCK. 
        mapcode = ratecode.CODE.
        FIND FIRST queasy WHERE queasy.KEY  = 145
          AND queasy.char1                = origCode
          AND queasy.char2                = mapcode
          AND queasy.number1              = 0
          AND queasy.deci1                = dynarate-list.w-day
          AND queasy.deci2                = dynarate-list.counter
          AND queasy.date1                = datum 
          NO-LOCK NO-ERROR.
        IF AVAILABLE queasy THEN mapcode = queasy.char3.
        FIND FIRST s-list WHERE s-list.marknr EQ ratecode.marknr 
          AND s-list.zikatnr EQ zimkateg.zikatnr 
          AND s-list.contcode EQ mapcode /* SY 21/0914 prcode*/
             NO-LOCK NO-ERROR. 
        IF NOT AVAILABLE s-list THEN 
        DO: 
          IF anz-setup GT 0 THEN 
          DO: 
            FIND FIRST zimmer WHERE zimmer.zikatnr = zimkateg.zikatnr 
              AND zimmer.setup = 0 NO-LOCK NO-ERROR. 
            IF AVAILABLE zimmer THEN 
            DO: 
              CREATE s-list.
              BUFFER-COPY zimkateg TO s-list.
              ASSIGN
                s-list.contcode = mapcode
                s-list.kurzbez1 = zimkateg.kurzbez 
                s-list.marknr   = ratecode.marknr
              . 
              FIND FIRST prmarket WHERE prmarket.nr = ratecode.marknr NO-LOCK 
                NO-ERROR. 
              IF AVAILABLE prmarket THEN s-list.market = prmarket.bezeich. 
            END. 
            DO i = 1 TO anz-setup: 
              FIND FIRST paramtext WHERE paramtext.txtnr 
                = (isetup-array[i] + 9200) NO-LOCK. 
              FIND FIRST zimmer WHERE zimmer.zikatnr = zimkateg.zikatnr 
                AND zimmer.setup = isetup-array[i] NO-LOCK NO-ERROR. 
              IF AVAILABLE zimmer THEN 
              DO: 
                CREATE s-list. 
                BUFFER-COPY zimkateg TO s-list.
                ASSIGN
                  s-list.contcode = mapcode
                  s-list.kurzbez1 = zimkateg.kurzbez 
                    + SUBSTR(paramtext.notes,1,1) 
                  s-list.marknr   = ratecode.marknr 
                  s-list.setup    = paramtext.ptexte 
                  s-list.nr       = i
                .
                FIND FIRST prmarket WHERE prmarket.nr = ratecode.marknr NO-LOCK 
                  NO-ERROR. 
                IF AVAILABLE prmarket THEN s-list.market = prmarket.bezeich. 
              END. 
            END. 
          END. 
          ELSE 
          DO: 
            CREATE s-list. 
            BUFFER-COPY zimkateg TO s-list.
            ASSIGN
              s-list.contcode = mapcode /* SY 21/09/14 prcode. */
              s-list.kurzbez1 = zimkateg.kurzbez
              s-list.marknr   = ratecode.marknr
            . 
            FIND FIRST prmarket WHERE prmarket.nr = ratecode.marknr NO-LOCK 
              NO-ERROR. 
            IF AVAILABLE prmarket THEN s-list.market = prmarket.bezeich. 
          END. 
        END. 
      END.
    END.
  END.
  ELSE
  FOR EACH dynaRate-list:
      FIND FIRST ratecode WHERE ratecode.CODE = dynaRate-list.rcode NO-LOCK.
      FIND FIRST zimkateg WHERE zimkateg.kurzbez = dynaRate-list.rmtype NO-LOCK 
        NO-ERROR. 
      IF AVAILABLE zimkateg THEN 
      DO: 
        mapcode = ratecode.CODE.
        FIND FIRST queasy WHERE queasy.KEY  = 145
            AND queasy.char1                = origCode
            AND queasy.char2                = mapcode
            AND queasy.number1              = zimkateg.zikatnr
            AND queasy.deci1                = dynarate-list.w-day
            AND queasy.deci2                = dynarate-list.counter
            AND queasy.date1                = datum 
            NO-LOCK NO-ERROR.
        IF AVAILABLE queasy THEN mapcode = queasy.char3.
        FIND FIRST s-list WHERE s-list.marknr EQ ratecode.marknr 
          AND s-list.zikatnr EQ zimkateg.zikatnr 
          AND s-list.contcode EQ mapcode /* SY 21/09/14 prcode */ 
          NO-LOCK NO-ERROR. 
        IF NOT AVAILABLE s-list THEN 
        DO: 
          IF anz-setup GT 0 THEN 
          DO: 
            FIND FIRST zimmer WHERE zimmer.zikatnr = zimkateg.zikatnr 
              AND zimmer.setup = 0 NO-LOCK NO-ERROR. 
            IF AVAILABLE zimmer THEN 
            DO: 
              CREATE s-list.
              BUFFER-COPY zimkateg TO s-list.
              ASSIGN
                s-list.contcode = mapcode
                s-list.kurzbez1 = zimkateg.kurzbez 
                s-list.marknr   = ratecode.marknr
              . 
              FIND FIRST prmarket WHERE prmarket.nr = ratecode.marknr NO-LOCK 
                NO-ERROR. 
              IF AVAILABLE prmarket THEN s-list.market = prmarket.bezeich. 
            END. 
            DO i = 1 TO anz-setup: 
              FIND FIRST paramtext WHERE paramtext.txtnr 
                = (isetup-array[i] + 9200) NO-LOCK. 
              FIND FIRST zimmer WHERE zimmer.zikatnr = zimkateg.zikatnr 
                AND zimmer.setup = isetup-array[i] NO-LOCK NO-ERROR. 
              IF AVAILABLE zimmer THEN 
              DO: 
                CREATE s-list. 
                BUFFER-COPY zimkateg TO s-list.
                ASSIGN
                  s-list.contcode = mapcode
                  s-list.kurzbez1 = zimkateg.kurzbez 
                    + SUBSTR(paramtext.notes,1,1) 
                  s-list.marknr   = ratecode.marknr 
                  s-list.setup    = paramtext.ptexte 
                  s-list.nr       = i
                .
                FIND FIRST prmarket WHERE prmarket.nr = ratecode.marknr NO-LOCK 
                  NO-ERROR. 
                IF AVAILABLE prmarket THEN s-list.market = prmarket.bezeich. 
              END. 
            END. 
          END. 
          ELSE 
          DO: 
            CREATE s-list. 
            BUFFER-COPY zimkateg TO s-list.
            ASSIGN
              s-list.contcode = mapcode /* SY 21/09/14 prcode */ 
              s-list.kurzbez1 = zimkateg.kurzbez 
              s-list.marknr   = ratecode.marknr
            . 
            FIND FIRST prmarket WHERE prmarket.nr = ratecode.marknr NO-LOCK 
              NO-ERROR. 
            IF AVAILABLE prmarket THEN s-list.market = prmarket.bezeich. 
          END. 
        END. 
      END.
  END.
/*
  FOR EACH zimkateg NO-LOCK: 
    FIND FIRST s-list WHERE s-list.zikatnr = zimkateg.zikatnr NO-LOCK NO-ERROR. 
    IF NOT AVAILABLE s-list THEN 
    DO: 
      IF anz-setup GT 0 THEN 
      DO: 
        FIND FIRST zimmer WHERE zimmer.zikatnr = zimkateg.zikatnr 
          AND zimmer.setup = 0 NO-LOCK NO-ERROR. 
        IF AVAILABLE zimmer THEN 
        DO: 
          CREATE s-list.
          ASSIGN
            s-list.zikatnr  = zimkateg.zikatnr
            s-list.kurzbez  = zimkateg.kurzbez 
            s-list.kurzbez1 = zimkateg.kurzbez 
            s-list.bezeich  = zimkateg.bezeich 
            s-list.flag     = 1
          . 
        END. 
        DO i = 1 TO anz-setup: 
          FIND FIRST paramtext WHERE paramtext.txtnr 
            = (isetup-array[i] + 9200) NO-LOCK. 
          FIND FIRST zimmer WHERE zimmer.zikatnr = zimkateg.zikatnr 
            AND zimmer.setup = isetup-array[i] NO-LOCK NO-ERROR. 
          IF AVAILABLE zimmer THEN 
          DO: 
            CREATE s-list. 
            ASSIGN
              s-list.zikatnr  = zimkateg.zikatnr
              s-list.kurzbez  = zimkateg.kurzbez 
              s-list.kurzbez1 = zimkateg.kurzbez 
                + SUBSTR(paramtext.notes,1,1)
              s-list.bezeich  = zimkateg.bezeich 
              s-list.setup    = paramtext.ptexte 
              s-list.nr       = i
              s-list.flag     = 1
            . 
          END. 
        END. 
      END. 
      ELSE 
      DO: 
        CREATE s-list.
        ASSIGN
          s-list.zikatnr  = zimkateg.zikatnr 
          s-list.kurzbez  = zimkateg.kurzbez 
          s-list.kurzbez1 = zimkateg.kurzbez 
          s-list.bezeich  = zimkateg.bezeich 
          s-list.flag     = 1
        . 
      END. 
    END. 
  END. 
*/
  IF curr-marknr NE 0 THEN 
  FOR EACH s-list WHERE s-list.marknr = curr-marknr: 
    s-list.reihenfolge = curr-marknr. 
  END. 

END. 
