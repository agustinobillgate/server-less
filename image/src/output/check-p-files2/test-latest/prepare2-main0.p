
DEF INPUT PARAMETER pvILanguage AS INTEGER         NO-UNDO.
DEF OUTPUT PARAMETER stop-it    AS LOGICAL INIT NO NO-UNDO.
DEF OUTPUT PARAMETER quit-it    AS LOGICAL INIT NO NO-UNDO.
DEF OUTPUT PARAMETER dummy-str  AS CHAR            NO-UNDO.
DEF OUTPUT PARAMETER msg-str    AS CHAR INIT ""    NO-UNDO.

DEFINE VARIABLE notice-day  AS INTEGER INITIAL 14 NO-UNDO.

{SupertransBL.i} 
DEF VAR lvCAREA AS CHAR INITIAL "e1-main0". 

ASSIGN dummy-str = "MyLord".
RUN check-license-date.

PROCEDURE check-license-date: 
DEFINE VARIABLE billdate        AS DATE. 
DEFINE VARIABLE condo-flag      AS LOGICAL INITIAL NO. 
DEFINE BUFFER htp1 FOR htparam. 
DEFINE BUFFER htp2 FOR htparam. 
 
  FIND FIRST htparam WHERE paramnr = 981 NO-LOCK. /* License FOR Condominium */ 
  IF htparam.flogical THEN 
  DO: 
    FIND FIRST htparam WHERE paramnr = 724 NO-LOCK. 
    condo-flag = htparam.flogical. 
  END. 
 
  FIND FIRST htparam WHERE paramnr = 975 NO-LOCK. 
  IF (htparam.finteger EQ 1) OR condo-flag THEN 
  DO: 
    FIND FIRST htp1 WHERE htp1.paramnr = 985 NO-LOCK. /* Banquet License */ 
    FIND FIRST htp2 WHERE htp2.paramnr = 724 NO-LOCK. 
    FIND FIRST htparam WHERE htparam.paramnr = 110 NO-LOCK. 
    IF htparam.fdate NE TODAY THEN 
    DO: 
      FIND CURRENT htparam EXCLUSIVE-LOCK. 
      htparam.fdate = TODAY. 
      FIND CURRENT htparam NO-LOCK. 
    END. 
    FIND FIRST htparam WHERE htparam.paramnr = 87 NO-LOCK. 
    IF htparam.fdate NE TODAY THEN 
    DO: 
      FIND CURRENT htparam EXCLUSIVE-LOCK. 
      htparam.fdate = TODAY. 
      FIND CURRENT htparam NO-LOCK. 
      IF htp1.flogical THEN RUN nt-bahistory.p. 
    END. 
 
    IF htp1.flogical AND htp2.flogical THEN RUN nt-bapostbill.p. 
  END. 
 
  FIND FIRST htparam WHERE htparam.paramnr = 110 NO-LOCK. 
  billdate = htparam.fdate. 
  IF billdate = ? OR billdate GT TODAY THEN billdate = TODAY.

  FIND FIRST htparam WHERE htparam.paramnr = 976 NO-LOCK. 
  IF htparam.fdate NE ? THEN 
  DO: 
    IF htparam.fdate LT TODAY OR htparam.fdate LT billdate THEN 
    DO: 
      stop-it = YES. 
      msg-str = translateExtended( "Your License was valid until : ", lvCAREA, "":U) 
        + STRING(htparam.fdate, "99/99/9999") 
        + CHR(10)
        + translateExtended( "Please contact your next Our Technical Support for further information.", lvCAREA, "":U) 
        + CHR(2).
    END. 
    ELSE IF (htparam.fdate - notice-day) LE TODAY THEN 
    DO: 
      FIND FIRST htp1 WHERE htp1.paramnr = 1072 /* Payroll */ EXCLUSIVE-LOCK.
      ASSIGN htp1.finteger = 1072.
      FIND CURRENT htp1 NO-LOCK.
      msg-str = translateExtended( "Your License is valid until :", lvCAREA, "":U) 
          + STRING(htparam.fdate, "99/99/9999")
          + CHR(10)
          + translateExtended( "Please contact your next Our Technical Support for further information", lvCAREA,"")
          + CHR(2).
      RETURN.
    END. 
  END. 
  ELSE stop-it = YES. 
  
  FIND FIRST htp1 WHERE htp1.paramnr = 1072 /* Payroll */ NO-LOCK.
  IF htp1.finteger = 1027 THEN
  DO:
    stop-it = YES.
    quit-it = YES.
  END.

  IF stop-it THEN 
  DO: 
    FIND FIRST htparam WHERE htparam.paramnr = 999 NO-LOCK.  /* demo version */
    IF htparam.flogical OR (htp1.finteger = 1072) THEN 
    DO: 
      FIND FIRST htparam WHERE htparam.paramnr = 996 EXCLUSIVE-LOCK. 
      htparam.fchar = "". 
      FIND CURRENT htparam NO-LOCK. 
      FIND CURRENT htp1 EXCLUSIVE-LOCK.
      ASSIGN htp1.finteger = 1027.
      FIND CURRENT htp1 NO-LOCK.
    END. 
  END. 
END. 
