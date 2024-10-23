DEFINE TEMP-TABLE g-list 
  FIELD jnr             LIKE gl-journal.jnr 
  FIELD fibukonto       LIKE gl-journal.fibukonto
  FIELD acct-fibukonto  LIKE gl-acct.fibukonto
  FIELD debit           LIKE gl-journal.debit 
  FIELD credit          LIKE gl-journal.credit 
  FIELD userinit        LIKE gl-journal.userinit 
  FIELD sysdate         LIKE gl-journal.sysdate INITIAL today 
  FIELD zeit            LIKE gl-journal.zeit 
  FIELD chginit         LIKE gl-journal.chginit 
  FIELD chgdate         LIKE gl-journal.chgdate INITIAL ? 
  FIELD bemerk          LIKE gl-journal.bemerk
  FIELD bezeich         LIKE gl-acct.bezeich
  FIELD duplicate       AS LOGICAL INITIAL YES
  /*gst for penang*/
  FIELD tax-code    AS CHAR
  FIELD tax-amount  AS CHAR
  FIELD tot-amt     AS CHAR.


DEF INPUT  PARAMETER TABLE FOR g-list.
DEF INPUT  PARAMETER pvILanguage    AS INTEGER      NO-UNDO.
DEF INPUT  PARAMETER curr-step      AS INTEGER.
DEF INPUT  PARAMETER bezeich        AS CHAR.
DEF INPUT  PARAMETER credits        LIKE gl-acct.actual[1].
DEF INPUT  PARAMETER debits         LIKE gl-acct.actual[1].
DEF INPUT  PARAMETER remains        LIKE gl-acct.actual[1].
DEF INPUT  PARAMETER refno          AS CHAR.
DEF INPUT  PARAMETER datum          AS DATE.
DEF INPUT  PARAMETER adjust-flag    AS LOGICAL.
DEF INPUT  PARAMETER journaltype    AS INTEGER  NO-UNDO.
DEF OUTPUT PARAMETER curr-jnr       AS INTEGER  INIT 0.
DEF OUTPUT PARAMETER msg-str        AS CHAR     INIT "".
DEF OUTPUT PARAMETER error-flag     AS LOGICAL  NO-UNDO.
DEF OUTPUT PARAMETER msg-str1       AS CHAR     NO-UNDO.

{SupertransBL.i} 
DEF VAR lvCAREA AS CHAR INITIAL "gl-postjourn".

IF curr-step = 1 THEN DO:
    IF datum = ? OR refno = "" THEN DO:
        ASSIGN msg-str1 = translateExtended ("Unfilled field(s) detected.",lvCAREA,"").
        RETURN.
    END.
    ELSE DO:
        RUN gl-postjourn-btn-gobl.p (INPUT TABLE g-list, 
                pvILanguage, curr-step, bezeich, credits, debits, remains, 
                refno, datum, adjust-flag, journaltype, OUTPUT curr-jnr, 
                OUTPUT msg-str, OUTPUT error-flag).
    END.
END.
IF curr-step = 2 THEN DO:
    FIND FIRST g-list NO-LOCK NO-ERROR.
    IF NOT AVAILABLE g-list THEN 
    DO: 
      ASSIGN msg-str1 = translateExtended ("Journal Transaction not yet entered.",lvCAREA,"").       
      RETURN. 
    END.
    IF remains NE 0 THEN 
    DO: 
      ASSIGN msg-str1 = translateExtended ("Journal Transaction not yet balanced.",lvCAREA,"").        
      RETURN.
    END.
    ELSE DO:
        RUN gl-postjourn-btn-gobl.p (INPUT TABLE g-list, 
                    pvILanguage, curr-step, bezeich, credits, debits, remains, 
                    refno, datum, adjust-flag, journaltype, OUTPUT curr-jnr,
                    OUTPUT msg-str, OUTPUT error-flag).
    END.    
END.





