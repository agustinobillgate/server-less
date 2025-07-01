
DEFINE TEMP-TABLE g-list      LIKE mc-guest.
DEFINE TEMP-TABLE t-mc-guest  LIKE mc-guest.
DEFINE TEMP-TABLE t-mc-types  LIKE mc-types.

DEF INPUT PARAMETER pvILanguage     AS INTEGER  NO-UNDO.
DEF INPUT  PARAMETER gastno         AS INTEGER  NO-UNDO.

DEF OUTPUT PARAMETER ci-date        AS DATE     NO-UNDO.
DEF OUTPUT PARAMETER card-exist     AS LOGICAL  NO-UNDO.
DEF OUTPUT PARAMETER f-tittle       AS CHAR     NO-UNDO.
DEF OUTPUT PARAMETER bezeich        AS CHAR     NO-UNDO.
DEF OUTPUT PARAMETER last-paydate   AS DATE     NO-UNDO.
DEF OUTPUT PARAMETER gname          AS CHAR     NO-UNDO.
DEF OUTPUT PARAMETER TABLE FOR g-list.
DEF OUTPUT PARAMETER TABLE FOR t-mc-guest.
DEF OUTPUT PARAMETER TABLE FOR t-mc-types.

{SupertransBL.i} 
DEF VAR lvCAREA AS CHAR INITIAL "mc-gcf". 


FIND FIRST htparam WHERE paramnr = 87 NO-LOCK.
ci-date = htparam.fdate.

FIND FIRST guest WHERE guest.gastnr = gastno NO-LOCK.
ASSIGN gname = guest.NAME + ", " + guest.vorname1 
             + " " + guest.anrede1.

FIND FIRST mc-guest WHERE mc-guest.gastnr = gastno NO-LOCK NO-ERROR.
card-exist = AVAILABLE mc-guest.
IF AVAILABLE mc-guest THEN
DO:
    CREATE t-mc-guest.
    BUFFER-COPY mc-guest TO t-mc-guest.
END.

f-tittle = translateExtended ("Card's Member",lvCAREA,"")
    + " - " + guest.NAME + " " + guest.vorname1 + ", " + guest.anrede1.

IF card-exist THEN
DO:
  FIND FIRST mc-types WHERE mc-types.nr = mc-guest.nr NO-LOCK NO-ERROR.
  IF AVAILABLE mc-types THEN 
  DO: 
      CREATE t-mc-types.
      BUFFER-COPY mc-types TO t-mc-types.
      bezeich = mc-types.bezeich.
  END.
  CREATE g-list.
  BUFFER-COPY mc-guest TO g-list.
END.

IF card-exist THEN
DO:
  FIND FIRST mc-fee WHERE mc-fee.gastnr = gastno AND mc-fee.bis-datum
    = mc-guest.tdate NO-LOCK NO-ERROR.
  IF AVAILABLE mc-fee THEN
  DO:
    last-paydate = mc-fee.bez-datum.
    /*MTDISP last-paydate WITH FRAME frame1.*/
  END.
END.
