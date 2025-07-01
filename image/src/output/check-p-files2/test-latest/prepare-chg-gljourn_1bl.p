DEF TEMP-TABLE t-gl-jouhdr LIKE gl-jouhdr
    FIELD rec-id AS INT.

DEF WORKFILE note-list 
  FIELD s-recid   AS INTEGER 
  FIELD bemerk    AS CHAR 
  FIELD add-note  AS CHAR 
  FIELD orig-note AS CHAR.

DEFINE TEMP-TABLE g-list 
  FIELD jnr         LIKE gl-journal.jnr 
  FIELD fibukonto   LIKE gl-acct.fibukonto 
  FIELD debit       LIKE gl-journal.debit 
  FIELD credit      LIKE gl-journal.credit 
  FIELD userinit    LIKE gl-journal.userinit 
  FIELD sysdate     LIKE gl-journal.sysdate INITIAL today 
  FIELD zeit        LIKE gl-journal.zeit 
  FIELD chginit     LIKE gl-journal.chginit 
  FIELD chgdate     LIKE gl-journal.chgdate INITIAL ? 
  FIELD duplicate   AS LOGICAL INITIAL YES. 

DEF TEMP-TABLE b1-list
  FIELD fibukonto    LIKE gl-acct.fibukonto 
  FIELD debit        LIKE gl-journal.debit 
  FIELD credit       LIKE gl-journal.credit 
  FIELD bemerk       AS CHAR
  FIELD bezeich      LIKE gl-acct.bezeich FORMAT "x(36)" 
  FIELD chginit      LIKE gl-journal.chginit FORMAT "x(3)" 
  FIELD chgdate      LIKE gl-journal.chgdate
  FIELD sysdate      LIKE gl-journal.sysdate
  FIELD zeit         LIKE gl-journal.zeit
  FIELD activeflag   LIKE gl-journal.activeflag
  FIELD rec-gl-journ AS INTEGER
  FIELD tax-code    AS CHAR
  FIELD tax-amount  AS CHAR
  FIELD tot-amt     AS CHAR.

DEF INPUT  PARAMETER jnr AS INT.
DEF OUTPUT PARAMETER closedate AS DATE.
DEF OUTPUT PARAMETER f-integer AS INT.
DEF OUTPUT PARAMETER gst-flag  AS LOGICAL.
DEF OUTPUT PARAMETER TABLE FOR b1-list.
DEF OUTPUT PARAMETER TABLE FOR t-gl-jouhdr.

FIND FIRST gl-jouhdr WHERE gl-jouhdr.jnr = jnr /* EXCLUSIVE-LOCK */ NO-LOCK NO-ERROR.
IF NOT AVAILABLE gl-jouhdr THEN RETURN.
CREATE t-gl-jouhdr.
BUFFER-COPY gl-jouhdr TO t-gl-jouhdr.
ASSIGN t-gl-jouhdr.rec-id = RECID(gl-jouhdr).

FIND FIRST htparam WHERE paramnr = 221 NO-LOCK. 
/* ASSIGN closedate = fdate. */               /* Rulita 211024 | Fixing for serverless */
ASSIGN closedate = htparam.fdate.
FIND FIRST htparam WHERE paramnr = 224 NO-LOCK.
/* IF MONTH(fdate) GT MONTH(closedate) THEN closedate = fdate. */       /* Rulita 211024 | Fixing for serverless */
IF MONTH(htparam.fdate) GT MONTH(closedate) THEN closedate = htparam.fdate.

FIND FIRST htparam WHERE htparam.paramnr = 1012 NO-LOCK.
IF htparam.paramgr = 38 AND htparam.feldtyp = 1 THEN
    f-integer = htparam.finteger.



create g-list.
RUN create-notelist. 
RUN disp-it1.

/*gst for penang*/
FIND FIRST l-lieferant WHERE l-lieferant.firma = "GST" NO-LOCK NO-ERROR.
IF AVAILABLE l-lieferant THEN ASSIGN gst-flag = YES.
ELSE ASSIGN gst-flag = NO.


PROCEDURE create-notelist: 
DEF VAR s1 AS CHAR. 
DEF VAR s2 AS CHAR. 
DEF VAR n AS INTEGER. 
  FOR EACH gl-journal WHERE gl-journal.jnr = jnr NO-LOCK: 
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
END. 


PROCEDURE disp-it1: 
  
  FOR EACH gl-journal WHERE gl-journal.jnr = jnr NO-LOCK,
      FIRST gl-acct WHERE gl-acct.fibukonto = gl-journal.fibukonto  NO-LOCK,
      FIRST note-list WHERE note-list.s-recid = INTEGER(RECID(gl-journal))
      NO-LOCK BY gl-acct.fibukonto BY gl-journal.sysdate BY gl-journal.zeit:
      CREATE b1-list.
      ASSIGN 
        b1-list.fibukonto    = gl-acct.fibukonto
        b1-list.debit        = gl-journal.debit
        b1-list.credit       = gl-journal.credit
        b1-list.bemerk       = note-list.bemerk
        b1-list.bezeich      = gl-acct.bezeich
        b1-list.chginit      = gl-journal.chginit
        b1-list.chgdate      = gl-journal.chgdate
        b1-list.activeflag   = gl-journal.activeflag
        b1-list.rec-gl-journ = RECID(gl-journal)
        b1-list.sysdate      = gl-journal.sysdate
        b1-list.zeit         = gl-journal.zeit.

      IF NUM-ENTRIES(gl-acct.bemerk, ";") GT 1 THEN
          ASSIGN b1-list.tax-code = ENTRY(2, gl-acct.bemerk, ";").
  END.

END. 
