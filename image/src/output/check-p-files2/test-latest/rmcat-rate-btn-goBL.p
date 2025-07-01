
DEFINE TEMP-TABLE p-list LIKE katpreis.

DEF INPUT PARAMETER TABLE FOR p-list.
DEF INPUT PARAMETER case-type AS INT.
DEF INPUT PARAMETER curr-arg  AS CHAR.
DEF INPUT PARAMETER rec-id    AS INT.

FIND FIRST p-list.
IF case-type = 1 THEN       /* add */
DO:
    create katpreis. 
    RUN fill-katpreis. 
END.

ELSE IF case-type = 2 THEN  /* chg */
DO: 
    FIND FIRST katpreis WHERE RECID(katpreis) = rec-id NO-LOCK NO-ERROR.
    IF AVAILABLE katpreis THEN
    DO:
        FIND CURRENT katpreis EXCLUSIVE-LOCK. 
        RUN fill-katpreis. 
        FIND CURRENT katpreis NO-LOCK.
        RELEASE katpreis.
    END.                 
END.


PROCEDURE fill-katpreis: 
DEFINE buffer arr FOR arrangement. 
  FIND FIRST arr WHERE arr.arrangement = curr-arg NO-LOCK NO-ERROR. 
  IF AVAILABLE arr THEN katpreis.argtnr = arr.argtnr. /*FT serverless*/
  ASSIGN 
    katpreis.zikatnr = p-list.zikatnr 
    katpreis.startperiode = p-list.startperiode 
    katpreis.endperiode   = p-list.endperiode 
    katpreis.betriebsnr   = p-list.betriebsnr 
    katpreis.perspreis[1] = p-list.perspreis[1] 
    katpreis.perspreis[2] = p-list.perspreis[2] 
    katpreis.perspreis[3] = p-list.perspreis[3] 
    katpreis.perspreis[4] = p-list.perspreis[4] 
    katpreis.kindpreis[1] = p-list.kindpreis[1] 
    katpreis.kindpreis[2] = p-list.kindpreis[2] 
  . 
END. 
