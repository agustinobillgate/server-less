
DEFINE TEMP-TABLE b1-list
    FIELD fibukonto            LIKE gl-acct.fibukonto
    FIELD glacct-bezeich       LIKE gl-acct.bezeich
    FIELD glmain-bezeich       LIKE gl-main.bezeich
    FIELD acc-type             LIKE gl-acct.acc-type
    FIELD glfstype-bezeich     LIKE gl-fstype.bezeich
    FIELD gldepartment-bezeich LIKE gl-department.bezeich
    FIELD glsubdept            AS CHARACTER FORMAT "x(24)"
    FIELD bemerk               LIKE gl-acct.bemerk
    FIELD nr                   LIKE gl-main.nr
    FIELD code                 LIKE gl-main.code
    .

DEF INPUT PARAMETER fibukonto   AS CHAR.
DEF INPUT PARAMETER from-main   AS INT.
DEF INPUT PARAMETER from-fstype AS INT.
DEF INPUT PARAMETER from-depart AS INT.
DEF OUTPUT PARAMETER TABLE FOR b1-list.

RUN display-it.

PROCEDURE display-it:
  IF from-main = 0 AND from-fstype = 0 AND from-depart = 0 THEN 
  FOR EACH gl-acct WHERE gl-acct.fibukonto GE fibukonto 
    AND gl-acct.activeflag = YES NO-LOCK, 
    FIRST gl-main WHERE gl-main.nr = gl-acct.main-nr NO-LOCK , 
    FIRST gl-fstype WHERE gl-fstype.nr = gl-acct.fs-type NO-LOCK , 
    FIRST gl-department WHERE gl-department.nr = gl-acct.deptnr NO-LOCK /*,
    FIRST bediener WHERE bediener.userinit = gl-acct.chginit NO-LOCK*/
       BY gl-acct.fibukonto:
      RUN assign-it.
  END.
  ELSE IF from-main NE 0 THEN 
  FOR EACH gl-acct WHERE gl-acct.fibukonto GE fibukonto 
    AND gl-acct.activeflag = YES NO-LOCK, 
     FIRST gl-main WHERE gl-main.nr = gl-acct.main-nr 
       AND gl-main.code EQ from-main NO-LOCK, 
     FIRST gl-fstype WHERE gl-fstype.nr = gl-acct.fs-type NO-LOCK, 
     FIRST gl-department WHERE gl-department.nr = gl-acct.deptnr NO-LOCK /*,
     FIRST bediener WHERE bediener.userinit = gl-acct.chginit NO-LOCK */
     BY gl-acct.fibukonto:
      RUN assign-it.
  END.
  ELSE IF from-fstype NE 0 THEN 
  FOR EACH gl-acct WHERE gl-acct.fibukonto GE fibukonto 
    AND gl-acct.activeflag = YES NO-LOCK, 
     FIRST gl-main WHERE gl-main.nr = gl-acct.main-nr NO-LOCK, 
     FIRST gl-fstype WHERE gl-fstype.nr = gl-acct.fs-type 
       AND gl-fstype.nr EQ from-fstype NO-LOCK, 
     FIRST gl-department WHERE gl-department.nr = gl-acct.deptnr NO-LOCK /*,
    FIRST bediener WHERE bediener.userinit = gl-acct.chginit NO-LOCK */
       BY gl-acct.fibukonto:
      RUN assign-it.
  END.
  ELSE IF from-depart NE 0 THEN 
  FOR EACH gl-acct WHERE gl-acct.fibukonto GE fibukonto 
    AND gl-acct.activeflag = YES NO-LOCK, 
     FIRST gl-main WHERE gl-main.nr = gl-acct.main-nr NO-LOCK, 
     FIRST gl-fstype WHERE gl-fstype.nr = gl-acct.fs-type NO-LOCK, 
     FIRST gl-department WHERE gl-department.nr = gl-acct.deptnr 
       AND gl-department.nr EQ from-depart NO-LOCK /*,
    FIRST bediener WHERE bediener.userinit = gl-acct.chginit NO-LOCK */
     BY gl-acct.fibukonto:
      RUN assign-it.
  END.
END. 

PROCEDURE assign-it:
    DEFINE VARIABLE usrname AS CHAR NO-UNDO INIT " ".

    IF TRIM(gl-acct.chginit) NE "" THEN DO:
        FIND FIRST bediener WHERE bediener.userinit = gl-acct.chginit NO-LOCK NO-ERROR.
        IF AVAILABLE bediener THEN ASSIGN usrname = bediener.username.
    END.
    
    CREATE b1-list.
    ASSIGN
    b1-list.fibukonto            = gl-acct.fibukonto
    b1-list.glacct-bezeich       = gl-acct.bezeich
    b1-list.glmain-bezeich       = gl-main.bezeich
    b1-list.acc-type             = gl-acct.acc-type
    b1-list.glfstype-bezeich     = gl-fstype.bezeich
    b1-list.gldepartment-bezeich = gl-department.bezeich
    b1-list.nr                   = gl-main.nr
    b1-list.code                 = gl-main.code.

    IF NUM-ENTRIES(gl-acct.bemerk, ";") GT 1 THEN
        ASSIGN b1-list.bemerk  = ENTRY(1, gl-acct.bemerk, ";") + ";" + usrname.
    ELSE 
        ASSIGN b1-list.bemerk  = gl-acct.bemerk + ";" + usrname.
END.
