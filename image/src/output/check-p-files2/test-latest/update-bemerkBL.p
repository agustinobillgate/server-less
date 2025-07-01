
DEF WORKFILE note-list 
  FIELD s-recid   AS INTEGER 
  FIELD bemerk    AS CHAR 
  FIELD add-note  AS CHAR 
  FIELD orig-note AS CHAR. 

DEF INPUT PARAMETER jou-recid AS INTEGER.

FIND FIRST gl-journal WHERE RECID(gl-journal) = jou-recid.
/* Malik Serverless */
IF AVAILABLE gl-journal THEN
DO:
  RUN create-new-note.
  RUN update-bemerk.
END.
/* END Malik */

PROCEDURE create-new-note:
  DEF VAR s1 AS CHAR. 
  DEF VAR s2 AS CHAR. 
  DEF VAR n AS INTEGER. 
  CREATE note-list. 
  note-list.s-recid = RECID(gl-journal). 
  n = INDEX(gl-journal.bemerk, ";&&"). 
  IF n > 0 THEN 
  DO: 
      s1 = SUBSTR(gl-journal.bemerk, 1, n - 1). 
      ASSIGN 
        note-list.s-recid = RECID(gl-journal) 
        note-list.bemerk = SUBSTR(gl-journal.bemerk, 1, n - 1) 
        note-list.add-note = SUBSTR(gl-journal.bemerk, n, 
          LENGTH(gl-journal.bemerk)). 
  END. 
  ELSE 
  DO: 
    ASSIGN 
        note-list.s-recid = RECID(gl-journal) 
        note-list.bemerk = gl-journal.bemerk. 
  END. 
  note-list.orig-note = note-list.bemerk. 
END. 


PROCEDURE update-bemerk: 
  DEF BUFFER gl-jou FOR gl-journal.

 FOR EACH note-list WHERE note-list.bemerk NE orig-note: 
    note-list.orig-note = note-list.bemerk. 
    FIND FIRST gl-jou WHERE RECID(gl-jou) = note-list.s-recid NO-LOCK 
      NO-ERROR. 
    IF AVAILABLE gl-jou THEN 
    DO TRANSACTION: 
      FIND CURRENT gl-jou EXCLUSIVE-LOCK. 
      gl-jou.bemerk = note-list.bemerk + note-list.add-note. 
      FIND CURRENT gl-jou NO-LOCK. 
    END. 
  END.
END. 
