DEFINE WORKFILE user-printers 
  FIELD nr AS INTEGER 
  FIELD selected AS LOGICAL INITIAL YES. 

DEFINE TEMP-TABLE s-list 
  FIELD ind     AS INTEGER INITIAL 1
  FIELD nr      AS INTEGER 
  FIELD bezeich AS CHAR FORMAT "x(34)" LABEL "Bill Layout". 

DEFINE TEMP-TABLE b1-list
    FIELD nr        LIKE printer.nr
    FIELD position  LIKE printer.position
    FIELD path      LIKE printer.path
    FIELD make      LIKE printer.make.

DEF INPUT-OUTPUT PARAMETER printer-nr AS INTEGER.
DEF INPUT-OUTPUT PARAMETER briefnr AS INTEGER. 
DEF OUTPUT PARAMETER n1 AS INTEGER INITIAL 0.
DEF OUTPUT PARAMETER rate AS LOGICAL INIT YES.
DEF OUTPUT PARAMETER usr-pr-defined AS LOGICAL INIT NO.
DEF OUTPUT PARAMETER found AS LOGICAL INIT NO.
DEF OUTPUT PARAMETER briefnr2 AS INTEGER INITIAL 0.
DEF OUTPUT PARAMETER flag AS LOGICAL INIT NO.
DEF OUTPUT PARAMETER TABLE FOR b1-list.
DEF OUTPUT PARAMETER TABLE FOR s-list.

RUN selected-printers. 
FOR EACH PRINTER WHERE bondrucker = NO
    AND opsysname = "DOS" NO-LOCK,
    FIRST user-printers WHERE user-printers.nr = printer.nr
    AND user-printers.selected NO-LOCK:
    CREATE b1-list.
    ASSIGN
    b1-list.nr        = printer.nr
    b1-list.position  = printer.position
    b1-list.path      = printer.path
    b1-list.make      = printer.make.
END.
 
FIND FIRST htparam WHERE paramnr = 137 NO-LOCK. 
rate = htparam.flogical. 
 
IF printer-nr NE 0 AND AVAILABLE PRINTER AND NOT usr-pr-defined THEN 
DO:
  IF printer.nr = printer-nr THEN found = YES. 
  ELSE DO: 
    found = NO. 
    n1 = 0. 
    FIND FIRST PRINTER WHERE bondrucker = NO AND opsysname = "DOS" 
      NO-LOCK NO-ERROR. 
    DO WHILE NOT found AND AVAILABLE PRINTER: 
      n1 = n1 + 1. 
      IF printer.nr = printer-nr THEN found = YES. 
      ELSE FIND NEXT PRINTER WHERE bondrucker = NO  AND opsysname = "DOS" NO-LOCK NO-ERROR. 
    END. 
    flag = YES.
    /*MT
    IF n1 LE 9 THEN b1:select-row(n1). 
    ELSE DO: 
      found = NO. 
      result = YES. 
      b1:select-row(9). 
      DO WHILE result AND NOT found: 
        result = b1:SELECT-NEXT-ROW() IN FRAME frame1. 
        IF result AND printer.nr = printer-nr THEN found = YES. 
      END. 
    END. */
  END. 
END. 
 
FIND FIRST brief WHERE brief.briefnr = briefnr NO-LOCK. 
CREATE s-list. 
ASSIGN
  s-list.ind = 1
  s-list.nr = briefnr
  s-list.bezeich = brief.briefbezeich
. 
 
FIND FIRST htparam WHERE htparam.paramnr = 415 NO-LOCK. 
briefnr2 = htparam.finteger. 
 
/*IF briefnr2 = 0 THEN 
DO: 
  hide b2. 
  ENABLE b1 sorttype btn-exit btn-cancel WITH FRAME Frame1. 
END. */
IF briefnr2 NE 0 THEN 
DO: 
  FIND FIRST brief WHERE brief.briefnr = briefnr2 NO-LOCK. 
  CREATE s-list. 
  ASSIGN
    s-list.ind     = 2
    s-list.nr      = briefnr2
    s-list.bezeich = brief.briefbezeich
  . 
  /*MTENABLE b1 b2 sorttype btn-exit btn-cancel WITH FRAME Frame1. 
  OPEN QUERY q2 FOR EACH s-list /* BY s-list.ind DESCENDING */. */
END. 
 
IF AVAILABLE PRINTER THEN printer-nr = printer.nr. 
/*MTIF found THEN APPLY "entry" TO btn-exit. 
ELSE APPLY "entry" TO btn-cancel. */




PROCEDURE selected-printers: 
DEFINE VARIABLE i AS INTEGER NO-UNDO. 
DEFINE VARIABLE s1 AS CHAR NO-UNDO. 
DEFINE VARIABLE s2 AS CHAR NO-UNDO. 
 
  FOR EACH PRINTER WHERE bondrucker = NO AND opsysname = "DOS" NO-LOCK: 
    create user-printers. 
    user-printers.nr = printer.nr. 
  END. 
  /*
  IF SESSION:PARAMETER MATCHES("*PRINTERS=*") THEN 
  DO: 
    FOR EACH user-printers: 
      user-printers.selected = NO. 
    END. 
    s1 = SESSION:PARAMETER. 
    DO i = 1 TO length(s1): 
      IF SUBSTR(s1,i,9) = "PRINTERS=" THEN 
      DO: 
        s2 = SUBSTR(s1, (i + 9), length(s1)). 
         i = 999. 
      END. 
    END. 
    s1 = "". 
    DO i = 1 TO length(s2): 
      IF SUBSTR(s2,i,1) = ";" THEN 
      DO: 
        FIND FIRST user-printers WHERE user-printers.nr = INTEGER(s1) 
          NO-ERROR. 
        IF AVAILABLE user-printers THEN user-printers.selected = YES. 
        usr-pr-defined = YES. 
        RETURN. 
      END. 
      IF SUBSTR(s2,i,1) = "," THEN 
      DO: 
        FIND FIRST user-printers WHERE user-printers.nr = INTEGER(s1) 
          NO-ERROR. 
        IF AVAILABLE user-printers THEN user-printers.selected = YES. 
        s1 = "". 
      END. 
      ELSE IF SUBSTR(s2,i,1) GE "0" AND SUBSTR(s2,i,1) LE "9" THEN 
        s1 = s1 + SUBSTR(s2,i,1). 
    END. 
    usr-pr-defined = YES. 
  END.*/ 
END. 
