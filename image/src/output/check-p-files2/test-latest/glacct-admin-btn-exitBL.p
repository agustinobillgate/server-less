DEFINE TEMP-TABLE b1-list LIKE gl-acct
    FIELD main-bezeich   LIKE gl-main.bezeich
    FIELD kurzbez        LIKE gl-fstype.kurzbez
    FIELD dept-bezeich   LIKE gl-department.bezeich
    FIELD fstype-bezeich LIKE gl-fstype.bezeich.

DEFINE TEMP-TABLE g-list LIKE gl-acct. 

DEF INPUT  PARAMETER TABLE FOR g-list.
DEF INPUT  PARAMETER case-type AS INT.
DEF INPUT  PARAMETER comments  AS CHAR.
DEF INPUT  PARAMETER curr-mode AS CHAR.
DEF INPUT  PARAMETER user-init AS CHAR.
DEF INPUT  PARAMETER map-acct  AS CHAR.
DEF INPUT  PARAMETER prev-fibukonto AS CHAR.
DEF INPUT  PARAMETER tax-code  AS CHAR NO-UNDO.
DEF OUTPUT PARAMETER from-acct AS CHAR.
DEF OUTPUT PARAMETER found     AS LOGICAL INITIAL NO.
DEF OUTPUT PARAMETER success-flag AS LOGICAL INIT NO.
DEF OUTPUT PARAMETER TABLE FOR b1-list.


FIND FIRST g-list.
IF case-type = 1 THEN DO: /*ITA 280318*/
    FIND FIRST gl-acct WHERE gl-acct.fibukonto  = g-list.fibukonto 
        NO-LOCK NO-ERROR.
    IF AVAILABLE gl-acct THEN RETURN.
END.

FIND FIRST gl-main WHERE gl-main.nr = g-list.main-nr NO-LOCK NO-ERROR.
IF NOT AVAILABLE gl-main THEN RETURN.

FIND FIRST gl-fstype WHERE gl-fstype.nr = g-list.fs-type NO-LOCK NO-ERROR.
IF NOT AVAILABLE gl-fstype THEN RETURN.

FIND FIRST gl-department WHERE gl-department.nr = g-list.deptnr 
    NO-LOCK NO-ERROR.
IF NOT AVAILABLE gl-department THEN RETURN.

IF case-type = 1 THEN   /* add */
DO :
    CREATE gl-acct.
    RUN fill-gl-acct.
    RUN create-b1-list.
    from-acct = g-list.fibukonto.
END.
ELSE IF case-type = 2 THEN   /* chg */
DO:
    FIND FIRST gl-acct WHERE gl-acct.fibukonto = /*g-list.fibukonto*/ prev-fibukonto EXCLUSIVE-LOCK.
    RUN fill-gl-acct. 
    RUN create-b1-list.
END.


PROCEDURE fill-gl-acct: 
  DEFINE VARIABLE i         AS INTEGER              NO-UNDO. 
  DEFINE VARIABLE answer    AS LOGICAL INITIAL YES  NO-UNDO.

  IF tax-code NE " " THEN comments = comments + ";" + tax-code.
  ASSIGN
    gl-acct.fibukonto  = g-list.fibukonto
    gl-acct.bezeich    = g-list.bezeich
    gl-acct.main-nr    = g-list.main-nr 
    gl-acct.acc-type   = g-list.acc-type 
    gl-acct.fs-type    = g-list.fs-type
    gl-acct.deptnr     = g-list.deptnr
    gl-acct.activeflag = g-list.activeflag
    gl-acct.bemerk     = /*MTcomments:SCREEN-VALUE IN FRAME frame1*/ comments
  . 
    IF curr-mode = "chg" THEN 
    DO:
      DO i = 1 TO 12: 
        ASSIGN
          gl-acct.budget[i]    = g-list.budget[i]
          gl-acct.ly-budget[i] = g-list.ly-budget[i] 
          gl-acct.debit[i]     = g-list.debit[i]
          gl-acct.actual[i]    = g-list.actual[i] 
          gl-acct.last-yr[i]   = g-list.last-yr[i]
        . 
      END.

      answer = YES.
      IF gl-acct.acc-type = 1 THEN
      DO:
        DO i = 1 TO 12:
           IF gl-acct.budget[i] GT 0    THEN found = YES.
           IF gl-acct.ly-budget[i] GT 0 THEN found = YES.
           IF gl-acct.debit[i] GT 0     THEN found = YES.
        END.
        /*MTIF found THEN
        DO:
          HIDE MESSAGE NO-PAUSE.
          MESSAGE translateExtended ("Account Type = REVENUE but budget value > 0, is this correct?",lvCAREA,"")
              VIEW-AS ALERT-BOX QUESTION BUTTONS YES-NO UPDATE answer.
          IF NOT answer THEN
          DO i = 1 TO 12:
            IF gl-acct.budget[i] GT 0 THEN gl-acct.budget[i] = - gl-acct.budget[i]. 
            IF gl-acct.ly-budget[i] GT 0 THEN gl-acct.ly-budget[i] = - gl-acct.ly-budget[i]. 
            IF gl-acct.debit[i] GT 0 THEN gl-acct.debit[i] = - gl-acct.debit[i]. 
          END.
        END.*/
      END.
      ASSIGN
        gl-acct.chginit = user-init
        gl-acct.userinit = TRIM(ENTRY(1, gl-acct.userinit, ";")) + ";" + map-acct

        gl-acct.m-date = TODAY.
    END.
    ELSE IF curr-mode = "add" THEN
    DO:
       ASSIGN
         gl-acct.userinit = user-init + ";" + map-acct
         gl-acct.c-date = TODAY.
    END.

    success-flag = YES.
END.


PROCEDURE create-b1-list:
    FIND FIRST gl-acct WHERE gl-acct.fibukonto  = g-list.fibukonto NO-LOCK.
    FIND FIRST gl-main WHERE gl-main.nr = gl-acct.main-nr NO-LOCK.
    FIND FIRST gl-fstype WHERE gl-fstype.nr = gl-acct.fs-type NO-LOCK.
    FIND FIRST gl-department WHERE gl-department.nr = gl-acct.deptnr NO-LOCK.
    CREATE b1-list.
    BUFFER-COPY gl-acct TO b1-list.
    ASSIGN
      b1-list.main-bezeich   = gl-main.bezeich
      b1-list.kurzbez        = gl-fstype.kurzbez
      b1-list.dept-bezeich   = gl-department.bezeich
      b1-list.fstype-bezeich = gl-fstype.bezeich.
END.
