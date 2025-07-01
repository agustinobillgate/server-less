DEFINE TEMP-TABLE s-list 
  FIELD frdate   AS DATE LABEL "FrDate"
  FIELD date     AS DATE LABEL "ToDate" 
  FIELD name     AS CHAR LABEL "Guest Name" FORMAT "x(24)" 
  FIELD zinr     LIKE zimmer.zinr LABEL "RmNo"  /*MT 20/07/12 change zinr format */
  FIELD flag     AS LOGICAL LABEL "InH" 
  FIELD ci       AS LOGICAL LABEL "C/I" INIT NO
  FIELD co       AS LOGICAL LABEL "C/O"
  FIELD ankunft  AS DATE LABEL "Arrival" 
  FIELD abreise  AS DATE LABEL "Depart" 
  FIELD urgent   AS LOGICAL INITIAL NO   LABEL "Urgent" 
  FIELD done     AS LOGICAL INITIAL NO   LABEL "Done" 
  FIELD id       AS CHAR FORMAT "x(15)"  LABEL "UserID"      /*Gerald ID "x(4)" to UserID "x(15)" 37157D*/
  FIELD dept     AS CHAR FORMAT "x(24)"  LABEL "Departments"
  FIELD bemerk   AS CHAR FORMAT "x(158)" LABEL "Note" 
  FIELD resnr    AS INTEGER 
  FIELD reslinnr AS INTEGER 
  FIELD ind      AS INTEGER
  FIELD s-recid  AS INTEGER
. 

DEF INPUT  PARAMETER user-init      AS CHAR.
DEF INPUT  PARAMETER f-date         AS DATE.
DEF INPUT  PARAMETER t-date         AS DATE.
DEF INPUT  PARAMETER sorttype       AS INT.
DEF INPUT  PARAMETER alldept-flag   AS LOGICAL.
DEF INPUT  PARAMETER curr-dept      AS INT.
DEF OUTPUT PARAMETER TABLE FOR s-list.
               
FIND FIRST bediener WHERE bediener.userinit = user-init NO-LOCK.

RUN create-list.

PROCEDURE create-list:
DEF VAR do-it    AS LOGICAL NO-UNDO.
DEF VAR ci-flag  AS LOGICAL NO-UNDO.
DEF VAR dept-str AS CHAR    NO-UNDO.
DEF VAR frdate   AS DATE    NO-UNDO.
DEF VAR t-id     AS CHAR.

  FOR EACH s-list:
    DELETE s-list. 
    RELEASE s-list.
  END.

  FOR EACH reslin-queasy WHERE reslin-queasy.key = "flag" 
      AND reslin-queasy.date1 GE f-date NO-LOCK BY reslin-queasy.date1:
      RUN check-do-it(reslin-queasy.char1, reslin-queasy.date1,
          LOGICAL(reslin-queasy.deci1),
          OUTPUT do-it, OUTPUT ci-flag, OUTPUT dept-str, OUTPUT frdate).
      IF do-it THEN
      DO:
        IF reslin-queasy.date1 LE f-date AND reslin-queasy.date1 GT t-date THEN    
        FIND FIRST res-line WHERE res-line.resnr = reslin-queasy.resnr 
          AND res-line.reslinnr = reslin-queasy.reslinnr 
          AND res-line.active-flag LE 1 NO-LOCK NO-ERROR.
        
        ELSE 
        FIND FIRST res-line WHERE res-line.resnr = reslin-queasy.resnr 
          AND res-line.reslinnr = reslin-queasy.reslinnr 
          AND res-line.active-flag LE 2 
          AND res-line.resstatus NE 9
          AND res-line.resstatus NE 10 NO-LOCK NO-ERROR.

        IF AVAILABLE res-line THEN
        DO: 
          CREATE s-list. 
          ASSIGN 
            s-list.date     = reslin-queasy.date1 
            s-list.name     = res-line.NAME 
            s-list.zinr     = res-line.zinr 
            s-list.flag     = (res-line.active-flag = 1) 
            s-list.co       = (res-line.active-flag = 2)
            s-list.ankunft  = res-line.ankunft 
            s-list.abreise  = res-line.abreise 
            /*s-list.id       = ENTRY(2, reslin-queasy.char1, CHR(2))*/ 
            s-list.bemerk   = ENTRY(1, reslin-queasy.char1, CHR(2)) 
            s-list.resnr    = reslin-queasy.resnr 
            s-list.reslinnr = reslin-queasy.reslinnr 
            s-list.urgent   = (reslin-queasy.number1 = 1)
            s-list.done     = (reslin-queasy.deci1 = 1) 
            s-list.ind      = 1 
            s-list.ci       = ci-flag
            s-list.frdate   = frdate
            s-list.dept     = dept-str
            s-list.s-recid  = RECID(reslin-queasy)
          . 

          /*Gerald ID "x(4)" to UserID "x(15)" 37157D*/
          IF ENTRY(2, reslin-queasy.char1, CHR(2)) NE "" THEN
          DO:
            t-id = ENTRY(2, reslin-queasy.char1, CHR(2)).
            FIND FIRST bediener WHERE bediener.userinit = t-id NO-LOCK NO-ERROR.
            IF AVAILABLE bediener THEN
            DO:
              s-list.id = bediener.username.
            END.
          END.
        END.
      END. 
  END.
  FOR EACH reslin-queasy WHERE reslin-queasy.key = "flag" 
      AND reslin-queasy.date2 GE f-date NO-LOCK BY reslin-queasy.date2:
      RUN check-do-it(reslin-queasy.char2, reslin-queasy.date2,
          LOGICAL(reslin-queasy.deci2),
          OUTPUT do-it, OUTPUT ci-flag, OUTPUT dept-str, OUTPUT frdate).

      IF do-it THEN
      DO:
        IF reslin-queasy.date2 LE f-date AND reslin-queasy.date2 GT t-date THEN    
        FIND FIRST res-line WHERE res-line.resnr = reslin-queasy.resnr 
          AND res-line.reslinnr = reslin-queasy.reslinnr 
          AND res-line.active-flag LE 1 NO-LOCK NO-ERROR.
        
        ELSE 
        FIND FIRST res-line WHERE res-line.resnr = reslin-queasy.resnr 
          AND res-line.reslinnr = reslin-queasy.reslinnr 
          AND res-line.active-flag LE 2 
          AND res-line.resstatus NE 9
          AND res-line.resstatus NE 10 NO-LOCK NO-ERROR.

        IF AVAILABLE res-line THEN
        DO: 
          CREATE s-list. 
          ASSIGN 
            s-list.date     = reslin-queasy.date2 
            s-list.name     = res-line.NAME 
            s-list.zinr     = res-line.zinr 
            s-list.flag     = (res-line.active-flag = 1) 
            s-list.co       = (res-line.active-flag = 2)
            s-list.ankunft  = res-line.ankunft 
            s-list.abreise  = res-line.abreise 
            /*s-list.id       = ENTRY(2, reslin-queasy.char2, CHR(2))*/
            s-list.bemerk   = ENTRY(1, reslin-queasy.char2, CHR(2)) 
            s-list.resnr    = reslin-queasy.resnr 
            s-list.reslinnr = reslin-queasy.reslinnr 
            s-list.urgent   = (reslin-queasy.number2 = 1)
            s-list.done     = (reslin-queasy.deci2 = 1) 
            s-list.ind      = 2 
            s-list.ci       = ci-flag
            s-list.frdate   = frdate
            s-list.dept     = dept-str
            s-list.s-recid  = RECID(reslin-queasy)
          . 

          /*Gerald ID "x(4)" to UserID "x(15)" 37157D*/
          IF ENTRY(2, reslin-queasy.char1, CHR(2)) NE "" THEN
          DO:
            t-id = ENTRY(2, reslin-queasy.char1, CHR(2)).
            FIND FIRST bediener WHERE bediener.userinit = t-id NO-LOCK NO-ERROR.
            IF AVAILABLE bediener THEN
            DO:
              s-list.id = bediener.username.
            END.
          END.
        END.
      END. 
  END.
  FOR EACH reslin-queasy WHERE reslin-queasy.key = "flag" 
      AND reslin-queasy.date3 GE f-date NO-LOCK BY reslin-queasy.date3:
      RUN check-do-it(reslin-queasy.char3, reslin-queasy.date3,
          LOGICAL(reslin-queasy.deci3),
          OUTPUT do-it, OUTPUT ci-flag, OUTPUT dept-str, OUTPUT frdate).

      IF do-it THEN
      DO:
        IF reslin-queasy.date3 LE f-date AND reslin-queasy.date3 GT t-date THEN    
        FIND FIRST res-line WHERE res-line.resnr = reslin-queasy.resnr 
          AND res-line.reslinnr = reslin-queasy.reslinnr 
          AND res-line.active-flag LE 1 NO-LOCK NO-ERROR.
        
        ELSE 
        FIND FIRST res-line WHERE res-line.resnr = reslin-queasy.resnr 
          AND res-line.reslinnr = reslin-queasy.reslinnr 
          AND res-line.active-flag LE 2 
          AND res-line.resstatus NE 9
          AND res-line.resstatus NE 10 NO-LOCK NO-ERROR.

        IF AVAILABLE res-line THEN
        DO: 
          CREATE s-list. 
          ASSIGN 
            s-list.date     = reslin-queasy.date3 
            s-list.name     = res-line.NAME 
            s-list.zinr     = res-line.zinr 
            s-list.flag     = (res-line.active-flag = 1) 
            s-list.co       = (res-line.active-flag = 2)
            s-list.ankunft  = res-line.ankunft 
            s-list.abreise  = res-line.abreise 
            /*s-list.id       = ENTRY(2, reslin-queasy.char3, CHR(2)) */
            s-list.bemerk   = ENTRY(1, reslin-queasy.char3, CHR(2)) 
            s-list.resnr    = reslin-queasy.resnr 
            s-list.reslinnr = reslin-queasy.reslinnr 
            s-list.urgent   = (reslin-queasy.number3 = 1)
            s-list.done     = (reslin-queasy.deci3 = 1) 
            s-list.ind      = 3 
            s-list.ci       = ci-flag
            s-list.frdate   = frdate
            s-list.dept     = dept-str
            s-list.s-recid  = RECID(reslin-queasy)
          . 

          /*Gerald ID "x(4)" to UserID "x(15)" 37157D*/
          IF ENTRY(2, reslin-queasy.char1, CHR(2)) NE "" THEN
          DO:
            t-id = ENTRY(2, reslin-queasy.char1, CHR(2)).
            FIND FIRST bediener WHERE bediener.userinit = t-id NO-LOCK NO-ERROR.
            IF AVAILABLE bediener THEN
            DO:
              s-list.id = bediener.username.
            END.
          END.
        END.
      END. 
  END.
END.

PROCEDURE check-do-it:
DEF INPUT PARAMETER inp-char    AS CHAR     NO-UNDO.
DEF INPUT PARAMETER todate      AS DATE     NO-UNDO.
DEF INPUT PARAMETER done-flag   AS LOGICAL  NO-UNDO.
DEF OUTPUT PARAMETER do-it      AS LOGICAL  NO-UNDO INIT YES.
DEF OUTPUT PARAMETER ci-flag    AS LOGICAL  NO-UNDO INIT NO.
DEF OUTPUT PARAMETER dept-str   AS CHAR     NO-UNDO INIT "".
DEF OUTPUT PARAMETER frdate     AS DATE     NO-UNDO.

DEF VARIABLE curr-i             AS INTEGER  NO-UNDO.
DEF VARIABLE mesValue           AS CHAR     NO-UNDO.
DEF VARIABLE usrdept-str        AS CHAR     NO-UNDO.
DEF VARIABLE loopi              AS INTEGER  NO-UNDO.
DEF VARIABLE str1               AS CHAR     NO-UNDO.

DEF VARIABLE t-dept AS CHAR.
/*
  IF sorttype = 1 (status done)      --> reslin-queasy.deci1 NE 0     
  IF sorttype = 2 (status not done)  --> reslin-queasy.deci1 EQ 0 
*/
  
  IF (sorttype = 1 AND NOT done-flag) OR (sorttype = 2 AND done-flag) THEN 
  DO:
    do-it = NO.
    RETURN.
  END.

  ASSIGN frdate = todate.
  IF NUM-ENTRIES(inp-char,CHR(2)) LE 2 THEN 
  DO: 
    IF frdate GT t-date THEN do-it = NO.
    RETURN. 
  END.

  DO curr-i = 3 TO NUM-ENTRIES(inp-char, CHR(2)):
      IF curr-i = 3 THEN
      ASSIGN
        mesValue = ENTRY(3, inp-char, CHR(2))
        frdate   = DATE(INTEGER(SUBSTR(mesValue,1,2)),
                        INTEGER(SUBSTR(mesValue,3,2)),
                        INTEGER(SUBSTR(mesValue,5)))
      .
      ELSE IF curr-i = 4 THEN dept-str = ENTRY(4, inp-char, CHR(2)).
      ELSE IF curr-i = 5 THEN 
      ASSIGN    
        mesValue = ENTRY(5, inp-char, CHR(2))
        ci-flag  = LOGICAL(INTEGER(mesValue))
      .
  END.
  /*IF alldept-flag THEN RETURN.
  IF dept-str = "" THEN RETURN.
                                  
  usrdept-str = STRING(bediener.user-group) + ",".
  IF dept-str MATCHES ("*," + usrdept-str + "*") THEN RETURN.
  IF SUBSTR(dept-str, 1, LENGTH(usrdept-str)) = usrdept-str THEN RETURN.
  do-it = NO.*/
  
  /*Gerald current department 37157D
  IF curr-dept = 0 THEN RETURN.
  t-dept = STRING(curr-dept) + ",".
  IF dept-str MATCHES ("*," + t-dept + "*") OR dept-str MATCHES ( t-dept + "*") THEN RETURN.
  do-it = NO.*/
  /*MNAUFAL - Change validation to get data, data not displayed correctly using old validation*/
  IF curr-dept = 0 THEN RETURN.
  IF dept-str MATCHES ("*" + "," + "*") THEN
  DO:
      DO loopi = 1 TO NUM-ENTRIES(dept-str, ","):
          IF INT(ENTRY(loopi, dept-str, ",")) EQ curr-dept THEN RETURN.
      END.
      do-it = NO.
  END.
  ELSE DO:
      IF INT(dept-str) EQ curr-dept THEN RETURN.
      do-it = NO.
  END.
END.
