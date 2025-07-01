
DEF INPUT PARAMETER pvILanguage  AS INTEGER     NO-UNDO.
DEF INPUT  PARAMETER gastno      AS INTEGER     NO-UNDO.
DEF INPUT  PARAMETER gcfmember   AS INTEGER     NO-UNDO.
DEF INPUT  PARAMETER reslin-list-active-flag AS INTEGER NO-UNDO.
DEF INPUT  PARAMETER master-exist   AS LOGICAL  NO-UNDO.
DEF OUTPUT PARAMETER guestname      AS CHAR     NO-UNDO.
DEF OUTPUT PARAMETER msg-str        AS CHAR     NO-UNDO.
DEF OUTPUT PARAMETER msg-str1       AS CHAR     NO-UNDO.
DEF OUTPUT PARAMETER answer         AS LOGICAL  NO-UNDO INIT NO.

DEFINE VARIABLE ind-gastnr          AS INTEGER NO-UNDO.
DEFINE VARIABLE wig-gastnr          AS INTEGER NO-UNDO.

DEFINE BUFFER member1 FOR guest. 
DEFINE BUFFER mbuff   FOR master.

{SupertransBL.i} 
DEF VAR lvCAREA AS CHAR INITIAL "mk-resline".

RUN htpint.p(109, OUTPUT wig-gastnr).
RUN htpint.p(123, OUTPUT ind-gastnr).

FIND FIRST member1 WHERE member1.gastnr = gcfmember NO-LOCK. 
guestname = member1.name + ", " + member1.vorname1 
                       + " " + member1.anrede1. 

IF member1.karteityp = 0 THEN 
    RUN black-vip-listbl.p(pvILanguage, gcfmember, OUTPUT msg-str).

IF (gastno = wig-gastnr) OR (gastno = ind-gastnr) THEN answer = YES.
ELSE 
DO: 
  FIND FIRST htparam WHERE htparam.paramnr = 76 NO-LOCK. 
  IF htparam.flogical OR master-exist THEN 
  DO: 
    msg-str1 = "&Q" + translateExtended ("Use the same guest name for Bill Receiver?", lvCAREA, "":U).
  END. 
END. 
