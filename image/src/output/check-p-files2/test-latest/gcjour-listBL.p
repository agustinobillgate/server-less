DEF WORKFILE note-list 
  FIELD s-recid AS INTEGER 
  FIELD bemerk AS CHAR. 

DEFINE TEMP-TABLE gl-jouhdr-list
    FIELD datum LIKE gl-jouhdr.datum 
    FIELD refno LIKE gl-jouhdr.refno
    FIELD bezeich LIKE gl-jouhdr.bezeich
    FIELD debit LIKE gl-jouhdr.debit
    FIELD credit LIKE gl-jouhdr.credit
    FIELD remain LIKE gl-jouhdr.remain
    FIELD jnr LIKE gl-jouhdr.jnr
    FIELD activeflag LIKE gl-jouhdr.activeflag.


DEF TEMP-TABLE b2-list
    FIELD fibukonto LIKE gl-acct.fibukonto
    FIELD debit LIKE gl-journal.debit
    FIELD credit LIKE gl-journal.credit
    FIELD bemerk LIKE note-list.bemerk
    FIELD userinit LIKE gl-journal.userinit
    FIELD sysdate LIKE gl-journal.sysdate
    FIELD zeit LIKE gl-journal.zeit
    FIELD chginit LIKE gl-journal.chginit
    FIELD chgdate LIKE gl-journal.chgdate
    FIELD bezeich LIKE gl-acct.bezeich.

DEF INPUT PARAMETER case-type AS INTEGER.
DEF INPUT PARAMETER from-refno LIKE gl-jouhdr.refno.
DEF INPUT PARAMETER sorttype AS INTEGER.
DEF INPUT PARAMETER journaltype AS INTEGER.
DEF INPUT PARAMETER jtype1 AS INTEGER.
DEF INPUT PARAMETER from-date AS DATE.
DEF INPUT PARAMETER to-date AS DATE.

DEF OUTPUT PARAMETER TABLE FOR gl-jouhdr-list.
DEF OUTPUT PARAMETER TABLE FOR b2-list.

DEF VAR yy AS INTEGER.

FUNCTION get-bemerk RETURNS CHAR(bemerk AS CHAR): 
DEF VAR n AS INTEGER. 
DEF VAR s1 AS CHAR. 
  bemerk = REPLACE(bemerk, CHR(10), " ").
  n = INDEX(bemerk, ";&&"). 
  IF n > 0 THEN s1 = SUBSTR(bemerk, 1, n - 1). 
  ELSE s1 = bemerk.
  RETURN s1. 
END. 

IF case-type = 1 THEN
RUN display-it.
ELSE RUN disp-it-2-1.

PROCEDURE display-it: 
  
  IF from-refno = "" THEN 
  DO: 
    IF sorttype = 0 THEN
    FOR EACH gl-jouhdr 
       WHERE gl-jouhdr.activeflag = sorttype 
       AND (gl-jouhdr.jtype = journaltype OR gl-jouhdr.jtype = jtype1) 
       AND gl-jouhdr.batch = YES 
       AND gl-jouhdr.datum GE from-date 
       AND gl-jouhdr.datum LE to-date NO-LOCK 
       USE-INDEX datype_ix 
       BY gl-jouhdr.datum BY gl-jouhdr.refno BY gl-jouhdr.bezeich:
       RUN assign-it.
    END.
    ELSE IF sorttype = 1 THEN
    FOR EACH gl-jouhdr 
       WHERE gl-jouhdr.activeflag = sorttype 
       AND (gl-jouhdr.jtype = journaltype OR gl-jouhdr.jtype = jtype1) 
       AND gl-jouhdr.batch = NO 
       AND gl-jouhdr.datum GE from-date 
       AND gl-jouhdr.datum LE to-date NO-LOCK 
       USE-INDEX datype_ix 
       BY gl-jouhdr.datum BY gl-jouhdr.refno BY gl-jouhdr.bezeich:
       RUN assign-it.
    END.

    FIND FIRST gl-jouhdr-list NO-ERROR.
    IF AVAILABLE gl-jouhdr-list THEN 
    RUN disp-it2. 
    
  END. 
  ELSE IF SUBSTR(from-refno,1,1) = "*" THEN
  DO: 
    IF sorttype = 0 THEN
    FOR EACH gl-jouhdr 
       WHERE gl-jouhdr.activeflag = sorttype 
       AND (gl-jouhdr.jtype = journaltype OR gl-jouhdr.jtype = jtype1) 
       AND gl-jouhdr.batch = YES 
       AND gl-jouhdr.refno MATCHES(from-refno) 
       AND gl-jouhdr.datum GE from-date 
       AND gl-jouhdr.datum LE to-date NO-LOCK 
       USE-INDEX datype_ix 
       BY gl-jouhdr.datum BY gl-jouhdr.refno BY gl-jouhdr.bezeich:
       RUN assign-it.
    END.
    ELSE IF sorttype = 1 THEN
    FOR EACH gl-jouhdr 
       WHERE gl-jouhdr.activeflag = sorttype 
       AND (gl-jouhdr.jtype = journaltype OR gl-jouhdr.jtype = jtype1) 
       AND gl-jouhdr.batch = NO 
       AND gl-jouhdr.refno MATCHES(from-refno) 
       AND gl-jouhdr.datum GE from-date 
       AND gl-jouhdr.datum LE to-date NO-LOCK 
       USE-INDEX datype_ix 
       BY gl-jouhdr.datum BY gl-jouhdr.refno BY gl-jouhdr.bezeich:
       RUN assign-it.
    END.

    FIND FIRST gl-jouhdr-list NO-ERROR.
    IF AVAILABLE gl-jouhdr-list THEN 
    RUN disp-it2. 
    
  END. 
  ELSE 
  DO: 
    IF sorttype = 0 THEN
    FOR EACH gl-jouhdr 
       WHERE gl-jouhdr.activeflag = sorttype 
       AND (gl-jouhdr.jtype = journaltype OR gl-jouhdr.jtype = jtype1) 
       AND gl-jouhdr.batch = YES 
       AND gl-jouhdr.refno EQ from-refno 
       AND gl-jouhdr.datum GE from-date 
       AND gl-jouhdr.datum LE to-date NO-LOCK 
       USE-INDEX datype_ix 
       BY gl-jouhdr.datum BY gl-jouhdr.refno BY gl-jouhdr.bezeich:
       RUN assign-it.
    END.
    ELSE IF sorttype = 1 THEN
    FOR EACH gl-jouhdr 
       WHERE gl-jouhdr.activeflag = sorttype 
       AND (gl-jouhdr.jtype = journaltype OR gl-jouhdr.jtype = jtype1) 
       AND gl-jouhdr.batch = NO 
       AND gl-jouhdr.refno EQ from-refno 
       AND gl-jouhdr.datum GE from-date 
       AND gl-jouhdr.datum LE to-date NO-LOCK 
       USE-INDEX datype_ix 
       BY gl-jouhdr.datum BY gl-jouhdr.refno BY gl-jouhdr.bezeich:
       RUN assign-it.
    END.

    FIND FIRST gl-jouhdr-list NO-ERROR.
    IF AVAILABLE gl-jouhdr-list THEN 
    RUN disp-it2.
   
  END. 
END.

PROCEDURE disp-it2:
  /*yy =YEAR(from-date).*/
  FOR EACH note-list: 
    DELETE note-list. 
  END. 
  FOR EACH gl-journal WHERE gl-journal.jnr = gl-jouhdr-list.jnr NO-LOCK: 
    CREATE note-list. 
    note-list.s-recid = RECID(gl-journal).      
    note-list.bemerk = get-bemerk(gl-journal.bemerk). 
  END. 

  FOR EACH gl-journal WHERE gl-journal.jnr = gl-jouhdr-list.jnr 
    /*AND YEAR(gl-journal.sysdate) EQ yy*/ NO-LOCK, 
    FIRST gl-acct WHERE gl-acct.fibukonto = gl-journal.fibukonto NO-LOCK, 
    FIRST note-list WHERE note-list.s-recid = INTEGER(RECID(gl-journal)) 
    NO-LOCK BY gl-journal.sysdate BY gl-journal.zeit:
    CREATE b2-list.
    ASSIGN
      b2-list.fibukonto = gl-acct.fibukonto
      b2-list.debit = gl-journal.debit
      b2-list.credit = gl-journal.credit
      b2-list.bemerk = note-list.bemerk
      b2-list.userinit = gl-journal.userinit
      b2-list.sysdate = gl-journal.sysdate
      b2-list.zeit = gl-journal.zeit
      b2-list.chginit = gl-journal.chginit
      b2-list.chgdate = gl-journal.chgdate
      b2-list.bezeich = gl-acct.bezeich.
  END.
END. 

PROCEDURE disp-it-2-1:
  /*yy =YEAR(from-date).*/
  FOR EACH note-list: 
    DELETE note-list. 
  END. 
  FOR EACH gl-journal WHERE gl-journal.jnr = sorttype NO-LOCK:
    CREATE note-list. 
    note-list.s-recid = RECID(gl-journal). 
    note-list.bemerk = get-bemerk(gl-journal.bemerk). 
  END. 

  FOR EACH gl-journal WHERE gl-journal.jnr = sorttype
    /*AND YEAR(gl-journal.sysdate) EQ yy*/ NO-LOCK,
    FIRST gl-acct WHERE gl-acct.fibukonto = gl-journal.fibukonto NO-LOCK, 
    FIRST note-list WHERE note-list.s-recid = INTEGER(RECID(gl-journal)) 
    NO-LOCK BY gl-journal.sysdate BY gl-journal.zeit:
    CREATE b2-list.
    ASSIGN
      b2-list.fibukonto = gl-acct.fibukonto
      b2-list.debit = gl-journal.debit
      b2-list.credit = gl-journal.credit
      b2-list.bemerk = note-list.bemerk
      b2-list.userinit = gl-journal.userinit
      b2-list.sysdate = gl-journal.sysdate
      b2-list.zeit = gl-journal.zeit
      b2-list.chginit = gl-journal.chginit
      b2-list.chgdate = gl-journal.chgdate
      b2-list.bezeich = gl-acct.bezeich.
  END.
END. 


PROCEDURE assign-it:
    CREATE gl-jouhdr-list.
    ASSIGN
      gl-jouhdr-list.datum = gl-jouhdr.datum 
      gl-jouhdr-list.refno = gl-jouhdr.refno
      gl-jouhdr-list.bezeich = gl-jouhdr.bezeich
      gl-jouhdr-list.debit = gl-jouhdr.debit
      gl-jouhdr-list.credit = gl-jouhdr.credit
      gl-jouhdr-list.remain = gl-jouhdr.remain
      gl-jouhdr-list.jnr = gl-jouhdr.jnr
      gl-jouhdr-list.activeflag = gl-jouhdr.activeflag.
END.

