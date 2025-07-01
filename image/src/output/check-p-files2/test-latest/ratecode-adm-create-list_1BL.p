DEFINE TEMP-TABLE pr-list 
    FIELD cstr    AS CHAR FORMAT "x(1)" EXTENT 2 INITIAL ["", "*"] 
    FIELD prcode  AS CHAR 
    FIELD rmcat   AS CHAR FORMAT "x(6)" LABEL "RmCat " 
    FIELD argt    AS CHAR FORMAT "x(27)" LABEL "Arrangement" 
    FIELD zikatnr AS INTEGER 
    FIELD argtnr  AS INTEGER 
    FIELD i-typ   AS INTEGER INIT 0
    FIELD flag    AS INTEGER INITIAL 0  /* 0 = NOT selected */ 
.

DEF INPUT  PARAMETER prcode     AS CHAR     NO-UNDO.
DEF INPUT  PARAMETER market-nr  AS INTEGER  NO-UNDO.
DEF OUTPUT PARAMETER childflag  AS LOGICAL  INIT NO.
DEF OUTPUT PARAMETER TABLE FOR pr-list.
/*
DEF VAR prcode      AS CHAR     NO-UNDO INIT "PKGOLF".
DEF VAR market-nr   AS INTEGER  NO-UNDO INIT 1.
DEF VAR childflag   AS LOGICAL  NO-UNDO.
DEF VAR count-i     AS INTEGER  NO-UNDO INIT 0.
*/
RUN create-list.
/* Rulita 300125 | Fixing serverless issue git 321 */
FIND FIRST ratecode WHERE ratecode.code EQ prcode NO-LOCK NO-ERROR.
IF AVAILABLE ratecode THEN
DO:
  FIND FIRST queasy WHERE queasy.KEY EQ 2 
    AND queasy.char1 EQ ratecode.code NO-LOCK NO-ERROR.
  IF AVAILABLE queasy THEN
  DO:
      IF NUM-ENTRIES(queasy.char3,";") GT 2 THEN
      DO:
          childflag = YES.
      END.
  END.
END.
/* End Rulita */
/*
CURRENT-WINDOW:WIDTH = 200.
FOR EACH pr-list NO-LOCK BY pr-list.argt BY pr-list.rmcat:
    count-i = count-i + 1.
    DISP
        count-i
        pr-list.cstr[pr-list.flag + 1]  
        pr-list.rmcat
        pr-list.zikatnr
        pr-list.argtnr
        pr-list.argt
        pr-list.flag
        WITH WIDTH 190.
END.
*/
PROCEDURE create-list: 
DEFINE VARIABLE i       AS INTEGER NO-UNDO. 
DEFINE VARIABLE j       AS INTEGER NO-UNDO. 
DEFINE VARIABLE k       AS INTEGER NO-UNDO. 
DEFINE VARIABLE argtnr  AS INTEGER NO-UNDO. 
DEFINE VARIABLE zikatnr AS INTEGER NO-UNDO. 
DEFINE VARIABLE found1  AS LOGICAL NO-UNDO. 
DEFINE VARIABLE found2  AS LOGICAL NO-UNDO. 
DEFINE VARIABLE pr-str  AS CHAR    NO-UNDO.

DEFINE BUFFER prtable0 FOR prtable.

  IF market-nr GT 0 THEN 
  DO: 
/* prtable0 (prtable0,prcode = "") was created BY market segment administration. 
   It contains all selected zimkateg AND arrangement  
*/ 
   FIND FIRST prtable0 WHERE prtable0.marknr = market-nr 
      AND prtable0.prcode = "" NO-LOCK NO-ERROR. 
    
    IF AVAILABLE prtable0 THEN 
    DO: 
      FIND FIRST prtable WHERE prtable.marknr = market-nr 
        AND prtable.prcode = prcode NO-LOCK NO-ERROR. 
      DO i = 1 TO 99: 
        IF prtable0.zikatnr[i] NE 0 THEN 
        DO: 
          FIND FIRST zimkateg WHERE zimkateg.zikatnr = prtable0.zikatnr[i] NO-LOCK NO-ERROR. 
          IF AVAILABLE zimkateg THEN 
          DO j = 1 TO 99: 
            IF prtable0.argtnr[j] NE 0 THEN 
            DO: 
              FIND FIRST arrangement WHERE arrangement.argtnr 
                = prtable0.argtnr[j] NO-LOCK NO-ERROR. 
              ASSIGN
                found1 = NO 
                k      = 1
              . 
              IF AVAILABLE arrangement THEN 
              DO WHILE k LE 99 AND NOT found1 AND AVAILABLE prtable: 
                
                /* SY 28/07/2014 */
                IF prtable.product[k] GT 10000 THEN
                DO:
                    ASSIGN
                        pr-str  = STRING(prtable.product[k])
                        zikatnr = INTEGER(SUBSTR(pr-str,1,2))
                        argtnr  = INTEGER(SUBSTR(pr-str,3))
                    .                                       
                    IF zikatnr GE 91 THEN zikatnr = zikatnr - 90.                     
                END.
                ELSE IF prtable.product[k] GT 100000 THEN /*FD August 18, 2022 => Ticket FAF793 for prtable.argtnr GE 999*/
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
    
              CREATE pr-list. 
              ASSIGN
                pr-list.rmcat   = zimkateg.kurzbez 
                pr-list.argt    = arrangement.argt-bez 
                pr-list.zikatnr = zimkateg.zikatnr
                pr-list.argtnr  = arrangement.argtnr 
                pr-list.prcode  = prcode 
                pr-list.i-typ   = zimkateg.typ
                pr-list.flag    = INTEGER(found1)
              .               
            END. 
          END. 
        END. 
      END. 
    END. 
  END. 
END. 
