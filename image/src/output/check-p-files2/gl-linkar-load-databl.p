
DEFINE TEMP-TABLE g-list 
  FIELD  rechnr     AS INTEGER 
  FIELD  dept       AS INTEGER 
  FIELD  jnr        LIKE gl-journal.jnr 
  FIELD  fibukonto  LIKE gl-journal.fibukonto 
  FIELD  debit      LIKE gl-journal.debit 
  FIELD  credit     LIKE gl-journal.credit 
  FIELD  bemerk     AS CHAR FORMAT "x(50)" 
  FIELD  userinit   LIKE gl-journal.userinit 
  FIELD  sysdate    LIKE gl-journal.sysdate INITIAL today 
  FIELD  zeit       LIKE gl-journal.zeit 
  FIELD  chginit    LIKE gl-journal.chginit 
  FIELD  chgdate    LIKE gl-journal.chgdate INITIAL ? 
  FIELD  duplicate  AS LOGICAL INITIAL YES 
  FIELD  add-info   AS CHAR 
  FIELD  counter    AS INTEGER
  FIELD  acct-fibukonto LIKE gl-acct.fibukonto
  FIELD  bezeich LIKE gl-acct.bezeich.
 
DEFINE TEMP-TABLE s-list 
  FIELD fibukonto   LIKE gl-acct.fibukonto 
  FIELD bezeich     AS CHAR FORMAT "x(28)" 
  FIELD credit      AS DECIMAL FORMAT ">>,>>>,>>>,>>9.99" 
  FIELD debit       AS DECIMAL FORMAT ">>,>>>,>>>,>>9.99". 


DEFINE INPUT PARAMETER pvILanguage      AS INTEGER NO-UNDO.
DEFINE INPUT PARAMETER merge-flag       AS LOGICAL NO-UNDO.
DEFINE INPUT PARAMETER from-date        AS DATE    NO-UNDO.
DEFINE INPUT PARAMETER to-date          AS DATE    NO-UNDO.
DEFINE INPUT PARAMETER user-init        AS CHAR    NO-UNDO.
DEFINE INPUT PARAMETER refno            AS CHAR    NO-UNDO.
DEFINE OUTPUT PARAMETER curr-anz        AS INTEGER NO-UNDO.
DEFINE OUTPUT PARAMETER msg-str         AS CHAR    NO-UNDO.
DEFINE OUTPUT PARAMETER TABLE FOR g-list.
DEFINE OUTPUT PARAMETER TABLE FOR s-list.


DEFINE VARIABLE acct-error AS INTEGER NO-UNDO INIT 0.

DEFINE VARIABLE debit1      AS DECIMAL NO-UNDO.
DEFINE VARIABLE credit1     AS DECIMAL NO-UNDO.
DEFINE VARIABLE remain1     AS DECIMAL NO-UNDO.
DEFINE VARIABLE art-artnr   AS INTEGER NO-UNDO.
DEFINE VARIABLE art-bezeich AS CHAR    NO-UNDO.

{supertransBL.i} 
DEF VAR lvCAREA AS CHAR INITIAL "gl-linkar-load-data". 


RUN gl-linkarbl.p (merge-flag, from-date, to-date, user-init, refno,
                 INPUT-OUTPUT curr-anz, OUTPUT acct-error, OUTPUT debit1,
                 OUTPUT credit1, OUTPUT remain1, OUTPUT TABLE g-list,
                 OUTPUT TABLE s-list,
                 OUTPUT art-artnr, OUTPUT art-bezeich).
IF acct-error = 1 THEN
DO: 
    ASSIGN msg-str = translateExtended ("Reference number already exists.",lvCAREA,"").
    RETURN NO-APPLY. 
END. 
ELSE IF acct-error = 2 THEN
DO:
    ASSIGN msg-str = translateExtended ("Chart of Account not defined ",lvCAREA,"") + CHR(13) + CHR(10) +
                     translateExtended ("ArticleNo",lvCAREA,"") + " " + STRING(art-artnr) + " - " + art-bezeich .
    RETURN NO-APPLY. 
END.

