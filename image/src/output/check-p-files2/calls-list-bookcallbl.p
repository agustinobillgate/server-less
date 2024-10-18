
DEF INPUT  PARAMETER pvILanguage  AS INTEGER  NO-UNDO.
DEF INPUT  PARAMETER s-recid      AS INTEGER  NO-UNDO.
DEF INPUT  PARAMETER bill-recid   AS INTEGER  NO-UNDO.
DEF INPUT  PARAMETER room-no      AS CHAR     NO-UNDO.
DEF INPUT  PARAMETER user-init    AS CHAR. 
DEF OUTPUT PARAMETER success      AS LOGICAL  NO-UNDO.
DEF OUTPUT PARAMETER rechnr       AS INTEGER  NO-UNDO.

FIND FIRST calls WHERE RECID(calls) = s-recid NO-LOCK.

IF room-no NE "" THEN 
    RUN bookcall2bl.p (pvILanguage, room-no, calls.datum, calls.zeit,
                     calls.satz-id, calls.dauer, calls.rufnummer,
                     calls.gastbetrag, user-init, OUTPUT success, OUTPUT rechnr). 

ELSE RUN bookcall3bl.p (pvILanguage, bill-recid, calls.datum, calls.zeit,
                        calls.satz-id, calls.dauer, calls.rufnummer,
                        calls.gastbetrag, user-init, OUTPUT success, OUTPUT rechnr). 

IF success THEN
DO:
  FIND FIRST calls WHERE RECID(calls) = s-recid EXCLUSIVE-LOCK.
  ASSIGN 
    calls.buchflag = 1 
    calls.rechnr = rechnr 
    calls.zinr = room-no
  .
  FIND CURRENT calls NO-LOCK.
END.
