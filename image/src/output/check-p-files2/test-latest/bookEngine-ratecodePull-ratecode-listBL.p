
DEF TEMP-TABLE ratecode-detail-list
    FIELD id     AS INT
    FIELD marknr AS INT
    FIELD rCode  AS CHAR
    /* Rd, 12-Des-24, rmType -> rmtype, */
    /* FIELD rmType AS CHAR */
    FIELD rmtype AS CHAR
    FIELD argmt  AS CHAR
    FIELD cstr   AS CHAR FORMAT "x(1)" EXTENT 2 INITIAL ["", "*"]
    FIELD flag   AS INTEGER INIT 0.

DEF INPUT  PARAMETER prcode AS CHAR.
DEF OUTPUT PARAMETER TABLE FOR ratecode-detail-list.

/* Test Local 
DEF VAR prcode AS CHAR NO-UNDO.
prcode = "BARFB3".

DEF VAR prcode AS CHAR INIT "TEST".
*/

DEFINE BUFFER prtable0 FOR prtable.
DEFINE VARIABLE i                   AS INT              NO-UNDO.
DEFINE VARIABLE j                   AS INT              NO-UNDO.
DEFINE VARIABLE k                   AS INT              NO-UNDO.
DEFINE VARIABLE zikatnr             AS INTEGER          NO-UNDO.
DEFINE VARIABLE argtnr              AS INTEGER          NO-UNDO.
DEFINE VARIABLE found1              AS LOGICAL          NO-UNDO.
DEFINE VARIABLE pr-str              AS CHAR             NO-UNDO.
DEFINE VARIABLE curr-id             AS INT      INIT 0  NO-UNDO.
DEFINE VARIABLE ifTask              AS CHAR             NO-UNDO.
DEFINE VARIABLE tokcounter          AS INT              NO-UNDO.
DEFINE VARIABLE mesToken            AS CHAR             NO-UNDO.
DEFINE VARIABLE mesValue            AS CHAR             NO-UNDO.
DEFINE VARIABLE dyna-flag           AS LOGICAL  INIT NO NO-UNDO.
DEFINE VARIABLE prev-prcode         AS CHAR             NO-UNDO.
DEFINE VARIABLE has-contract-rate   AS LOGICAL          NO-UNDO.
prev-prcode = prcode.

DEFINE VARIABLE cat-flag    AS LOGICAL INIT NO NO-UNDO.
DEFINE VARIABLE roomtype    AS CHAR.
DEFINE BUFFER qsy FOR queasy.
DEFINE BUFFER rc-check FOR ratecode.
                  

FIND FIRST queasy WHERE queasy.KEY = 152 NO-LOCK NO-ERROR.
IF AVAILABLE queasy THEN cat-flag = YES.

FIND FIRST queasy WHERE queasy.KEY = 2 AND queasy.char1 = prcode NO-LOCK.
IF queasy.logi2 THEN 
DO:
    dyna-flag = YES.
    FIND FIRST ratecode WHERE ratecode.code = prcode NO-LOCK.
    ifTask = ratecode.char1[5].
    DO tokcounter = 1 TO NUM-ENTRIES(ifTask, ";") - 1:  
        mesToken = SUBSTRING(ENTRY(tokcounter, ifTask, ";"), 1, 2).  
        mesValue = SUBSTRING(ENTRY(tokcounter, ifTask, ";"), 3).  
        CASE mesToken:
            WHEN "RC" THEN prcode = mesValue.  
        END CASE.  
    END.
END.

FOR EACH prtable WHERE prtable.prcode = prcode,
    FIRST prmarket WHERE prmarket.nr = prtable.marknr NO-LOCK,
    FIRST prtable0 WHERE prtable0.marknr = prtable.marknr
      AND prtable0.prcode = "" NO-LOCK :
    
    DO i = 1 TO 99:
        
        FIND FIRST zimkateg WHERE zimkateg.zikatnr = prtable0.zikatnr[i] 
            NO-LOCK NO-ERROR. 
        IF AVAILABLE zimkateg THEN 
        DO j = 1 TO 99: 
            IF prtable0.argtnr[j] NE 0 THEN 
            DO: 
              FIND FIRST arrangement WHERE arrangement.argtnr = prtable0.argtnr[j] NO-LOCK NO-ERROR. 
              ASSIGN
                found1 = NO 
                k      = 1
              . 
              IF AVAILABLE arrangement THEN 
              DO WHILE k LE 99 AND NOT found1 AND AVAILABLE prtable:
                  IF prtable.product[k] GT 10000 THEN
                  DO:
                      ASSIGN
                          pr-str  = STRING(prtable.product[k])
                          zikatnr = INTEGER(SUBSTR(pr-str,1,2))
                          argtnr  = INTEGER(SUBSTR(pr-str,3))
                      .
                      IF zikatnr GE 91 THEN zikatnr = zikatnr - 90.
                  END.

                  ELSE IF prtable.product[k] GT 0 AND prtable0.argtnr[j] LE 99 THEN 
                  ASSIGN
                    zikatnr = ROUND((prtable.product[k] / 100 - 0.5), 0)
                    argtnr  = prtable.product[k] - zikatnr * 100 
                    zikatnr = ROUND((prtable.product[k] / 100 - 0.5), 0) 
                    argtnr  =  prtable.product[k] - zikatnr * 100
                  . 
                  ELSE IF prtable.product[k] GT 0 AND prtable0.argtnr[j] GE 100 THEN
                  ASSIGN 
                    zikatnr = ROUND((prtable.product[k] / 1000 - 0.5), 0)
                    argtnr  = prtable.product[k] - zikatnr * 1000
                    zikatnr = ROUND((prtable.product[k] / 1000 - 0.5), 0) 
                    argtnr  =  prtable.product[k] - zikatnr * 1000
                  . 
                  IF zikatnr = prtable0.zikatnr[i] 
                    AND argtnr = prtable0.argtnr[j] THEN found1 = YES. 
                  k = k + 1. 
              END. 
              
              curr-id = curr-id + 1.
              
              IF cat-flag THEN
              DO:
                  FIND FIRST qsy WHERE qsy.KEY = 152 AND qsy.number1 = zimkateg.typ NO-LOCK NO-ERROR.
                  IF AVAILABLE qsy THEN roomtype = qsy.char1.
              END.
              ELSE roomtype = zimkateg.kurzbez.
              /* Rd, 12-Des-24, rmType -> rmtype, */
              /* FIND FIRST ratecode-detail-list WHERE ratecode-detail-list.rmType = roomtype AND  */
              FIND FIRST ratecode-detail-list WHERE ratecode-detail-list.rmtype = roomtype AND 
                ratecode-detail-list.argmt  = arrangement.arrangement 
                AND ratecode-detail-list.flag = 1 NO-LOCK NO-ERROR.
              IF NOT AVAILABLE ratecode-detail-list THEN  
              DO:
                  /* Adding Validation BLY(08042025) - 8FF0D9 */
                  has-contract-rate = NO.

                  /* check contract rate */
                  FIND FIRST rc-check WHERE rc-check.CODE = prcode
                      AND rc-check.zikatnr = prtable0.zikatnr[i]
                      AND rc-check.argtnr = prtable0.argtnr[j] NO-LOCK NO-ERROR.

                  IF AVAILABLE rc-check THEN
                      has-contract-rate = YES.

                  IF has-contract-rate THEN
                  DO:
                      CREATE ratecode-detail-list.
                      ASSIGN
                          ratecode-detail-list.id     = curr-id
                          ratecode-detail-list.marknr = prmarket.nr
                          ratecode-detail-list.rCode  = prcode
                           /* Rd, 12-Des-24, rmType -> rmtype, */
                          /* ratecode-detail-list.rmType = roomtype */
                          ratecode-detail-list.rmtype = roomtype
                          ratecode-detail-list.argmt  = arrangement.arrangement
                          ratecode-detail-list.flag   = INTEGER(found1).
                      IF dyna-flag THEN
                          ratecode-detail-list.rCode  = prev-prcode.
                  END.
                  /* End Adding Validation BLY(08042025) - 8FF0D9 */
              END.
            END. 
        END.
    END.
END.

FOR EACH ratecode-detail-list WHERE ratecode-detail-list.cstr[ratecode-detail-list.flag + 1] EQ "":
    DELETE ratecode-detail-list.
END.

/*
CURRENT-WINDOW:WIDTH = 200.

FOR EACH ratecode-detail-list BY ratecode-detail-list.id:
    DISP ratecode-detail-list WITH WIDTH 190.
END.
*/
