DEFINE TEMP-TABLE b-list LIKE brief
    FIELD fname2 AS CHAR LABEL "Email Message File". 

DEF INPUT PARAMETER TABLE FOR b-list.
DEF INPUT PARAMETER case-type   AS INT.
DEF INPUT PARAMETER kateg       AS INT.
DEF INPUT PARAMETER rec-id      AS INT.

FIND FIRST b-list NO-LOCK.
IF case-type = 1 THEN
DO:
    CREATE brief.
    RUN fill-brief.
END.
ELSE IF case-type = 2 THEN
DO:
    FIND FIRST brief WHERE RECID(brief) = rec-id EXCLUSIVE-LOCK NO-ERROR.
    IF AVAILABLE brief THEN
    DO:
        RUN fill-brief.
        FIND CURRENT brief NO-LOCK. 
    END.                            
END.


PROCEDURE fill-brief: 
  ASSIGN
    brief.briefnr       = b-list.briefnr
    brief.briefbezeich  = b-list.briefbezeich
    brief.fname         = b-list.fname
    brief.briefkateg    = kateg
  . 
  IF b-list.fname NE "" THEN
  ASSIGN brief.fname = brief.fname + ";" + b-list.fname2 + ";".
END. 

