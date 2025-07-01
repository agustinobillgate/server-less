DEFINE TEMP-TABLE b2-list
    FIELD fibukonto LIKE gl-acct.fibukonto 
    FIELD debit     LIKE gl-journal.debit
    FIELD credit    LIKE gl-journal.credit
    FIELD bemerk    AS CHAR
    FIELD userinit  LIKE gl-journal.userinit
    FIELD sysdate   LIKE gl-journal.sysdate
    FIELD zeit      LIKE gl-journal.zeit
    FIELD chginit   LIKE gl-journal.chginit
    FIELD chgdate   LIKE gl-journal.chgdate
    FIELD bezeich   LIKE gl-acct.bezeich.

DEF WORKFILE note-list 
  FIELD s-recid AS INTEGER 
  FIELD bemerk AS CHAR. 

DEF INPUT PARAMETER jnr AS INT.
DEF OUTPUT PARAMETER TABLE FOR b2-list.

FUNCTION get-bemerk RETURNS CHAR(bemerk AS CHAR):
DEF VAR n AS INTEGER.
DEF VAR s1 AS CHAR.
  n = INDEX(bemerk, ";&&").
  IF n > 0 THEN RETURN SUBSTR(bemerk, 1, n - 1).
  ELSE RETURN bemerk.
END.

FOR EACH note-list:
    DELETE note-list.
END.
FOR EACH gl-journal WHERE gl-journal.jnr = jnr NO-LOCK:
    CREATE note-list.
    note-list.s-recid = RECID(gl-journal).
    note-list.bemerk = get-bemerk(gl-journal.bemerk).
END.

FOR EACH gl-journal WHERE gl-journal.jnr = jnr NO-LOCK,
    FIRST gl-acct WHERE gl-acct.fibukonto = gl-journal.fibukonto NO-LOCK,
    FIRST note-list WHERE note-list.s-recid = INTEGER(RECID(gl-journal))
    NO-LOCK BY gl-journal.sysdate BY gl-journal.zeit:
    RUN assign-b2.
END.

PROCEDURE assign-b2:
    CREATE b2-list.
    ASSIGN
        b2-list.fibukonto = gl-acct.fibukonto 
        b2-list.debit     = gl-journal.debit
        b2-list.credit    = gl-journal.credit
        b2-list.bemerk    = note-list.bemerk
        b2-list.userinit  = gl-journal.userinit
        b2-list.sysdate   = gl-journal.sysdate
        b2-list.zeit      = gl-journal.zeit
        b2-list.chginit   = gl-journal.chginit
        b2-list.chgdate   = gl-journal.chgdate
        b2-list.bezeich   = gl-acct.bezeich.
END.
