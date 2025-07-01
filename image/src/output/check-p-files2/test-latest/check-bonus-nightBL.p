DEFINE TEMP-TABLE Res-Dynarate
    FIELD date1  AS DATE
    FIELD date2  AS DATE
    FIELD rate   AS DECIMAL
    FIELD rmCat  AS CHAR
    FIELD argt   AS CHAR
    FIELD prcode AS CHAR
    FIELD rCode  AS CHAR
    FIELD markNo AS INTEGER
    FIELD setup  AS INTEGER
    FIELD adult  AS INTEGER
    FIELD child  AS INTEGER
    INDEX date1_ix date1
.
DEFINE TEMP-TABLE stay-pay
    FIELD startDate AS DATE INITIAL ?
    FIELD f-date    AS DATE                      LABEL "FromDate"
    FIELD t-date    AS DATE                      LABEL "ToDate"
    FIELD stay      AS INTEGER FORMAT "     >>>" LABEL "Stay(Nights)"
    FIELD pay       AS INTEGER FORMAT "     >>>" LABEL "Pay(Nights)"
.

DEF INPUT PARAMETER ci-date AS DATE NO-UNDO.
DEF INPUT PARAMETER co-date AS DATE NO-UNDO.
DEF INPUT-OUTPUT PARAMETER TABLE FOR Res-Dynarate.

DEFINE VARIABLE niteOfStay          AS INTEGER              NO-UNDO.
DEFINE VARIABLE niteNo              AS INTEGER              NO-UNDO.
DEFINE VARIABLE compNo              AS INTEGER INITIAL 0    NO-UNDO.
DEFINE VARIABLE usedCompliment      AS INTEGER INITIAL 0    NO-UNDO.
DEFINE VARIABLE datum               AS DATE                 NO-UNDO.
DEFINE VARIABLE fdatum              AS DATE                 NO-UNDO.
DEFINE VARIABLE tdatum              AS DATE                 NO-UNDO.
DEFINE VARIABLE argtNo              AS INTEGER              NO-UNDO.
DEFINE VARIABLE rmcatNo             AS INTEGER              NO-UNDO.
DEFINE VARIABLE w-day               AS INTEGER              NO-UNDO.
DEFINE VARIABLE n                   AS INTEGER              NO-UNDO.
DEFINE VARIABLE prcode              AS CHAR                 NO-UNDO.
DEFINE VARIABLE ct                  AS CHAR                 NO-UNDO.

DEFINE VARIABLE wd-array            AS INTEGER EXTENT 8     NO-UNDO 
       INITIAL [7, 1, 2, 3, 4, 5, 6, 7]. 

/* Rulita 131224 | Fixing serverless issue git 260 */
/* Rulita 191224 | Fixing serverless temp-table res-dynarate dan fieldnya jadi huruf kecil issue git 260 */
FIND FIRST res-dynarate NO-LOCK NO-ERROR.
IF AVAILABLE res-dynarate THEN
DO:
    FIND CURRENT res-dynarate EXCLUSIVE-LOCK.

    FIND FIRST arrangement WHERE arrangement.arrangement = res-dynarate.argt NO-LOCK NO-ERROR.
    IF AVAILABLE arrangement THEN 
    DO:
      FIND FIRST zimkateg WHERE zimkateg.kurzbez = res-dynarate.rmcat NO-LOCK NO-ERROR.
      IF AVAILABLE zimkateg THEN
      DO:
        ASSIGN
            niteOfStay = co-date - ci-date
            argtNo     = arrangement.argtnr 
            rmcatNo    = zimkateg.zikatnr
            prcode     = res-dynarate.rcode
        .
    
        FOR EACH res-dynarate BY res-dynarate.date1:
          ASSIGN 
              datum = res-dynarate.date1
              w-day = wd-array[WEEKDAY(datum - 1)]
          .
          FOR EACH stay-pay:
              DELETE stay-pay.
          END.
          FIND FIRST ratecode WHERE ratecode.code = prcode 
            AND ratecode.marknr = res-dynarate.markno
            AND ratecode.argtnr = argtNo 
            AND ratecode.zikatnr = rmcatNo
            AND ratecode.startperiode LE datum AND ratecode.endperiode GE datum
            NO-LOCK NO-ERROR. 
          IF AVAILABLE ratecode AND (NUM-ENTRIES(ratecode.char1[3], ";") GE 2) THEN
          DO:
              DO n = 1 TO NUM-ENTRIES(ratecode.char1[3], ";") - 1:
                ASSIGN
                  ct     = ENTRY(n, ratecode.char1[3], ";")
                  fdatum = DATE(INTEGER(SUBSTR(ENTRY(1, ct, ","),5,2)),
                        INTEGER(SUBSTR(ENTRY(1, ct, ","),7,2)), 
                        INTEGER(SUBSTR(ENTRY(1, ct, ","),1,4)))
                  tdatum = DATE(INTEGER(SUBSTR(ENTRY(2, ct, ","),5,2)),
                        INTEGER(SUBSTR(ENTRY(2, ct, ","),7,2)), 
                        INTEGER(SUBSTR(ENTRY(2, ct, ","),1,4)))
                .
                IF datum GT fdatum AND datum LE tdatum THEN
                DO:
                  CREATE stay-pay.
                  ASSIGN
                    stay-pay.f-date    = fdatum
                    stay-pay.t-date    = tdatum
                    stay-pay.stay      = INTEGER(ENTRY(3, ct, ","))
                    stay-pay.pay       = INTEGER(ENTRY(4, ct, ","))
                  .
                  IF ci-date LT fdatum THEN ASSIGN stay-pay.startDate = fdatum.
                  ELSE stay-pay.startDate = ci-date.
                  IF stay-pay.stay = stay-pay.pay THEN DELETE stay-pay.
                END.
              END.
              FOR EACH stay-pay BY stay-pay.stay:
                  ASSIGN
                      niteNo       = datum - stay-pay.startDate + 1
                      stay-pay.pay = stay-pay.pay + usedCompliment
                      compNo       = stay-pay.stay - stay-pay.pay
                  .
                  IF stay-pay.stay LT niteNo THEN usedCompliment = usedCompliment + compNo.
                  ELSE IF (niteOfStay GE stay-pay.stay) AND (niteNo GT stay-pay.pay) THEN
                  DO:
                      res-dynarate.rate = 0.
                      LEAVE.
                  END.
              END.
          END.
        END.
      END.
    END.

    FIND CURRENT res-dynarate NO-LOCK.
    RELEASE res-dynarate.
END.
/* End Rulita */
