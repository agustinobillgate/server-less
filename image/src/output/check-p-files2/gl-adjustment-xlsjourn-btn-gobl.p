DEFINE TEMP-TABLE g-list 
  FIELD  jnr        LIKE gl-journal.jnr 
  FIELD  fibukonto  LIKE gl-journal.fibukonto 
  FIELD  fibukonto2 LIKE gl-journal.fibukonto
  FIELD  debit      LIKE gl-journal.debit 
  FIELD  credit     LIKE gl-journal.credit 
  FIELD  userinit   LIKE gl-journal.userinit 
  FIELD  sysdate    LIKE gl-journal.sysdate INITIAL today 
  FIELD  zeit       LIKE gl-journal.zeit 
  FIELD  chginit    LIKE gl-journal.chginit 
  FIELD  chgdate    LIKE gl-journal.chgdate INITIAL ? 
  FIELD  bemerk     LIKE gl-journal.bemerk 
  FIELD  descr      LIKE gl-acct.bezeich
  FIELD  duplicate  AS LOGICAL INITIAL YES
  FIELD  correct    AS INT INITIAL 0.

DEF INPUT-OUTPUT PARAMETER TABLE FOR g-list.
DEF OUTPUT PARAMETER debits   LIKE gl-acct.actual[1].
DEF OUTPUT PARAMETER credits  LIKE gl-acct.actual[1].
DEF OUTPUT PARAMETER remains  LIKE gl-acct.actual[1].

RUN check-acc.
RUN debt-credit.

PROCEDURE check-acc:
    FOR EACH g-list:
        FIND FIRST gl-acct WHERE gl-acct.fibukonto = g-list.fibukonto2 
            NO-LOCK NO-ERROR. 
        IF NOT AVAILABLE gl-acct THEN
            correct = 2.
    END.
END.

PROCEDURE debt-credit:
    debits = 0.
    credits = 0.
    remains = 0.
    FOR EACH g-list:
        IF AVAILABLE g-list THEN
        DO:
            debits = debits + g-list.debit.
            credits = credits + g-list.credit.
        END.                                  
    END.
    remains = debits - credits.
END.

