DEFINE TEMP-TABLE s-list 
  FIELD newflag AS LOGICAL INITIAL YES
  FIELD id      AS CHAR FORMAT "x(3)"   LABEL "ID"
  FIELD frdate  AS DATE LABEL "FrDate" 
  FIELD datum   AS DATE LABEL "ToDate" 
  FIELD note    AS CHAR FORMAT "x(158)" LABEL "Note"
  FIELD urgent  AS LOGICAL INITIAL NO   LABEL "Urgent" 
  FIELD done    AS LOGICAL INITIAL NO   LABEL "Done" 
  FIELD dept    AS CHAR FORMAT "x(32)"  LABEL "Department"
  FIELD ciflag  AS LOGICAL LABEL "Disp C/I"
  FIELD coflag  AS LOGICAL LABEL "Disp C/O"
  FIELD rsv-detail AS LOGICAL LABEL "Disp Reservation Detail"
  FIELD bill-flag  AS LOGICAL LABEL "Disp Bill". 
DEFINE TEMP-TABLE t-res-line LIKE res-line.

DEF INPUT  PARAMETER resnr          AS INT  NO-UNDO.
DEF INPUT  PARAMETER reslinnr       AS INT  NO-UNDO.
DEF INPUT  PARAMETER user-init      AS CHAR NO-UNDO.
DEF OUTPUT PARAMETER perm-bediener  AS LOGICAL INIT NO.
DEF OUTPUT PARAMETER spreq          AS CHAR NO-UNDO.
DEF OUTPUT PARAMETER TABLE FOR s-list.
DEF OUTPUT PARAMETER TABLE FOR t-res-line.

DEF VAR n     AS INTEGER.
DEF VAR loopi AS INTEGER.

REPEAT n = 0 TO 2. 
    FIND FIRST reslin-queasy WHERE reslin-queasy.key = "flag" 
      AND reslin-queasy.resnr = resnr 
      AND reslin-queasy.reslinnr = reslinnr 
      AND reslin-queasy.betriebsnr = n NO-LOCK NO-ERROR. 
     
    CREATE s-list. 
    IF AVAILABLE reslin-queasy THEN 
    DO: 
        ASSIGN
          s-list.datum   = reslin-queasy.date1
          s-list.coflag  = reslin-queasy.logi1. 
        IF s-list.datum NE ? THEN 
            ASSIGN s-list.newflag = NO
                   s-list.note    = ENTRY(1, reslin-queasy.char1, CHR(2)).

        IF reslin-queasy.number1 = 1 THEN s-list.urgent = YES. 
        ELSE s-list.urgent = NO. 

        IF reslin-queasy.deci1 = 1 THEN s-list.done = YES. 
        ELSE s-list.done = NO. 

        RUN fill-additionals(reslin-queasy.char1).
    END.
    
    CREATE s-list. 
    IF AVAILABLE reslin-queasy THEN 
    DO: 
        ASSIGN
          s-list.datum   = reslin-queasy.date2
          s-list.coflag  = reslin-queasy.logi2
        . 
        IF s-list.datum NE ? THEN 
            ASSIGN s-list.newflag = NO
                   s-list.note    = ENTRY(1, reslin-queasy.char2, CHR(2)) .

        IF reslin-queasy.number2 = 1 THEN s-list.urgent = YES. 
        ELSE s-list.urgent = NO. 

        IF reslin-queasy.deci2 = 1 THEN s-list.done = YES. 
        ELSE s-list.done = NO. 

        RUN fill-additionals(reslin-queasy.char2).
    END.
    
    CREATE s-list. 
    IF AVAILABLE reslin-queasy THEN 
    DO: 
        ASSIGN
          s-list.datum   = reslin-queasy.date3
          s-list.coflag  = reslin-queasy.logi3
        . 
        IF s-list.datum NE ? THEN 
            ASSIGN s-list.newflag = NO         
                   s-list.note    = ENTRY(1, reslin-queasy.char3, CHR(2)) .

        IF reslin-queasy.number3 = 1 THEN s-list.urgent = YES. 
        ELSE s-list.urgent = NO. 

        IF reslin-queasy.deci3 = 1 THEN s-list.done = YES. 
        ELSE s-list.done = NO. 

        RUN fill-additionals(reslin-queasy.char3).
    END.

END. 

FIND FIRST res-line WHERE res-line.resnr = resnr 
  AND res-line.reslinnr = reslinnr NO-LOCK NO-ERROR.
IF AVAILABLE res-line THEN
DO:
  CREATE t-res-line.
  BUFFER-COPY res-line TO t-res-line.
END.
FIND FIRST bediener WHERE bediener.userinit = user-init NO-LOCK. 
IF SUBSTR(bediener.permissions,3,1) GE "2" THEN perm-bediener = YES. 

/*ITA 040617 --> for special request*/
 FIND FIRST reslin-queasy WHERE reslin-queasy.KEY = "specialRequest"
     AND reslin-queasy.resnr = resnr 
     AND reslin-queasy.reslinnr = reslinnr NO-LOCK NO-ERROR.
 IF AVAILABLE reslin-queasy THEN DO:
     DO loopi = 1 TO NUM-ENTRIES(reslin-queasy.char3, ";"):
         FIND FIRST queasy WHERE queasy.KEY = 189 
             AND queasy.char1 = ENTRY(loopi,reslin-queasy.char3, ";") NO-LOCK NO-ERROR.
         IF AVAILABLE queasy AND queasy.logi3 = YES THEN
             ASSIGN spreq = ENTRY(loopi,reslin-queasy.char3, ";") + ";" + spreq.
     END.
 END.
/*end*/


PROCEDURE fill-additionals:
DEF INPUT PARAMETER inp-char  AS CHAR    NO-UNDO.    
DEF VARIABLE curr-i           AS INTEGER NO-UNDO.
DEF VARIABLE mesValue         AS CHAR    NO-UNDO.

  ASSIGN s-list.frdate = s-list.datum.
  IF NUM-ENTRIES(inp-char, CHR(2)) LT 2 THEN RETURN.

  DO curr-i = 2 TO NUM-ENTRIES(inp-char, CHR(2)):
      IF curr-i = 2 THEN s-list.id = ENTRY(2, inp-char, CHR(2)).
      ELSE IF curr-i = 3 THEN
      ASSIGN
        mesValue      = ENTRY(3, inp-char, CHR(2))
        s-list.frdate = DATE(INTEGER(SUBSTR(mesValue,1,2)),
                             INTEGER(SUBSTR(mesValue,3,2)),
                             INTEGER(SUBSTR(mesValue,5)))
      .
      ELSE IF curr-i = 4 THEN s-list.dept = ENTRY(4, inp-char, CHR(2)).
      ELSE IF curr-i = 5 THEN 
      ASSIGN    
        mesValue      = ENTRY(5, inp-char, CHR(2))
        s-list.ciflag = LOGICAL(INTEGER(mesValue))
      .
      ELSE IF curr-i = 6 THEN 
      ASSIGN    
        mesValue      = ENTRY(6, inp-char, CHR(2))
        s-list.rsv-detail = LOGICAL(INTEGER(mesValue))
      .
      ELSE IF curr-i = 7 THEN 
      ASSIGN    
        mesValue      = ENTRY(7, inp-char, CHR(2))
        s-list.bill-flag = LOGICAL(INTEGER(mesValue))
      .
  END.
END.

