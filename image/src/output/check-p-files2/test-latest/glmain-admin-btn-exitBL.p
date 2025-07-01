DEF TEMP-TABLE g-list LIKE gl-main.

DEF INPUT  PARAMETER pvILanguage    AS INTEGER  NO-UNDO.
DEF INPUT  PARAMETER case-type      AS INTEGER.
DEF INPUT  PARAMETER TABLE FOR g-list.
DEF OUTPUT PARAMETER code-0         AS LOGICAL INIT NO.
DEF OUTPUT PARAMETER msg-str        AS CHAR.
DEF OUTPUT PARAMETER success-flag   AS LOGICAL INIT NO.

{SupertransBL.i} 
DEF VAR lvCAREA AS CHAR INITIAL "glmain-admin". 

DEFINE buffer gl-main1 FOR gl-main. 

FIND FIRST g-list.

RUN validate-it.
IF code-0 THEN RETURN.

IF case-type = 1 THEN   /** add **/
DO:
    CREATE gl-main.
    BUFFER-COPY g-list TO gl-main.
    RELEASE gl-main.
    ASSIGN success-flag = YES.
END.
IF case-type = 2 THEN   /** chg **/
DO:
    FIND FIRST gl-main WHERE gl-main.nr = g-list.nr EXCLUSIVE-LOCK NO-ERROR.
    IF AVAILABLE gl-main THEN BUFFER-COPY g-list TO gl-main.
    FIND CURRENT gl-main.
    RELEASE gl-main.
    ASSIGN success-flag = YES.
END.


PROCEDURE validate-it:
  FIND FIRST gl-main1 WHERE gl-main1.code = g-list.code 
     AND gl-main1.nr NE g-list.nr NO-LOCK NO-ERROR. 
  IF AVAILABLE gl-main1 THEN 
  DO: 
    msg-str = msg-str + CHR(2)
            + translateExtended ("Other G/L Main Account with the same code exists.",lvCAREA,"").
    code-0 = YES.
  END.

  FIND FIRST gl-main1 WHERE gl-main1.bezeich = g-list.bezeich 
     AND gl-main1.nr NE g-list.nr NO-LOCK NO-ERROR. 
  IF AVAILABLE gl-main1 THEN 
  DO: 
    msg-str = msg-str + CHR(2) + "&W"
            + translateExtended ("Other G/L Main Account exists with the same description.",lvCAREA,"").
  END.
END.
