DEFINE TEMP-TABLE out-list
    FIELD s-recid       AS INTEGER
    FIELD marked        AS CHARACTER    FORMAT "x(1)" LABEL "M"
    FIELD fibukonto     AS CHARACTER
    FIELD jnr           AS INTEGER      INITIAL 0
    FIELD jtype         AS INTEGER
    FIELD bemerk        AS CHARACTER
    FIELD trans-date    AS DATE
    FIELD bezeich       AS CHARACTER
    FIELD number1       AS CHARACTER /*wenni*/
    FIELD debit         AS DECIMAL
    FIELD credit        AS DECIMAL 
    FIELD balance       AS DECIMAL
    FIELD debit-str     AS CHARACTER
    FIELD credit-str    AS CHARACTER
    FIELD balance-str   AS CHARACTER
    FIELD refno         AS CHARACTER
    FIELD uid           AS CHARACTER
    FIELD created       AS DATE
    FIELD chgID         AS CHARACTER
    FIELD chgDate       AS DATE
    /*gst for penang*/
    FIELD tax-code    AS CHAR
    FIELD tax-amount  AS CHAR
    FIELD tot-amt     AS CHAR
    FIELD approved    AS LOGICAL INIT NO
    FIELD prev-bal    AS CHARACTER /* add by gerald budget awal 080420 */
    FIELD dept-code   AS INTEGER
    FIELD coa-bezeich AS CHAR /*MCH Dec 20, 2024 => 600A0F Req Amaranta Prambanan*/
 .


DEFINE INPUT PARAMETER idFlag       AS CHAR.
DEFINE OUTPUT PARAMETER doneFlag    AS LOGICAL NO-UNDO INITIAL NO.
DEFINE INPUT-OUTPUT PARAMETER TABLE FOR out-list.

DEFINE VARIABLE counter   AS INTEGER NO-UNDO INITIAL 0.
DEFINE VARIABLE htl-no    AS CHAR NO-UNDO.
DEFINE VARIABLE temp-char AS CHAR NO-UNDO.
DEFINE STREAM s1.

DEFINE BUFFER bqueasy FOR queasy.
DEFINE BUFFER pqueasy FOR queasy.
DEFINE BUFFER tqueasy FOR queasy.


FIND FIRST paramtext WHERE paramtext.txtnr = 243 NO-LOCK NO-ERROR. 
IF AVAILABLE paramtext AND paramtext.ptexte NE "" THEN
  RUN decode-string(paramtext.ptexte, OUTPUT htl-no). 

DEFINE VARIABLE curr-time AS INTEGER NO-UNDO.
ASSIGN curr-time = TIME.
/*FOR EACH queasy WHERE queasy.KEY = 280 AND queasy.char1 = "General Ledger" 
    AND queasy.char3 = idFlag NO-LOCK BY queasy.number1:*/

FIND FIRST queasy WHERE queasy.KEY = 280 AND queasy.char1 = "General Ledger" 
    AND queasy.char3 = idFlag NO-LOCK NO-ERROR.
DO WHILE AVAILABLE queasy:
        ASSIGN counter = counter + 1.
        IF counter GT 500 THEN LEAVE.
        
        CREATE out-list.
        ASSIGN
            out-list.s-recid     = INTEGER(ENTRY(1, queasy.char2, "|"))
            out-list.marked      = ENTRY(2, queasy.char2, "|")
            out-list.fibukonto   = ENTRY(3, queasy.char2, "|")
            out-list.jnr         = INTEGER(ENTRY(4, queasy.char2, "|"))
            out-list.jtype       = INTEGER(ENTRY(5, queasy.char2, "|"))
            out-list.bemerk      = ENTRY(6, queasy.char2, "|")
            out-list.bezeich     = ENTRY(8, queasy.char2, "|")
            out-list.number1     = ENTRY(9, queasy.char2, "|")
            out-list.debit       = DECIMAL(ENTRY(10, queasy.char2, "|"))
            out-list.credit      = DECIMAL(ENTRY(11, queasy.char2, "|"))
            out-list.balance     = DECIMAL(ENTRY(12, queasy.char2, "|"))
            out-list.debit-str   = ENTRY(13, queasy.char2, "|")
            out-list.credit-str  = ENTRY(14, queasy.char2, "|")
            out-list.balance-str = ENTRY(15, queasy.char2, "|")
            out-list.refno       = ENTRY(16, queasy.char2, "|")
            out-list.uid         = ENTRY(17, queasy.char2, "|")
            out-list.chgID       = ENTRY(19, queasy.char2, "|")
            out-list.tax-code    = ENTRY(21, queasy.char2, "|")
            out-list.tax-amount  = ENTRY(22, queasy.char2, "|")
            out-list.tot-amt     = ENTRY(23, queasy.char2, "|")
            out-list.prev-bal    = ENTRY(25, queasy.char2, "|")
            out-list.dept-code   = INTEGER(ENTRY(26, queasy.char2, "|"))
            out-list.coa-bezeich = ENTRY(27, queasy.char2, "|")
        .

        IF ENTRY(24, queasy.char2, "|") = "no" THEN ASSIGN out-list.approved = NO.
        ELSE IF ENTRY(24, queasy.char2, "|") = "yes" THEN ASSIGN out-list.approved = YES.

        IF ENTRY(7, queasy.char2, "|") NE "" THEN
            ASSIGN out-list.trans-date  = DATE(INT(ENTRY(2,ENTRY(7, queasy.char2, "|"),"/")), INT(ENTRY(1,ENTRY(7, queasy.char2, "|"),"/")), INT(ENTRY(3,ENTRY(7, queasy.char2, "|"),"/"))).

        IF ENTRY(18, queasy.char2, "|") NE "" AND ENTRY(18, queasy.char2, "|") MATCHES "*/*" THEN
            ASSIGN out-list.created = DATE(INT(ENTRY(2,ENTRY(18, queasy.char2, "|"),"/")), INT(ENTRY(1,ENTRY(18, queasy.char2, "|"),"/")), INT(ENTRY(3,ENTRY(18, queasy.char2, "|"),"/"))).

        IF ENTRY(20, queasy.char2, "|") NE ""  THEN
            ASSIGN out-list.chgDate = DATE(INT(ENTRY(2,ENTRY(20, queasy.char2, "|"),"/")), INT(ENTRY(1,ENTRY(20, queasy.char2, "|"),"/")), INT(ENTRY(3,ENTRY(20, queasy.char2, "|"),"/"))).
        
        FIND FIRST bqueasy WHERE RECID(bqueasy) = RECID(queasy) EXCLUSIVE-LOCK.
        DELETE bqueasy.
        RELEASE bqueasy.


      FIND NEXT queasy WHERE queasy.KEY = 280 AND queasy.char1 = "General Ledger" 
            AND queasy.char3 = idFlag NO-LOCK NO-ERROR.
END.

/*MESSAGE "c" counter STRING(TIME - curr-time, "HH:MM:SS") VIEW-AS ALERT-BOX INFO. */


FIND FIRST pqueasy WHERE pqueasy.KEY = 280 
    AND pqueasy.char1 = "General Ledger"
    AND pqueasy.char3 = idFlag NO-LOCK NO-ERROR.
IF AVAILABLE pqueasy THEN DO:
    ASSIGN doneFlag = NO.
    /*MESSAGE "1" doneFlag VIEW-AS ALERT-BOX INFO.*/
END.
ELSE DO:
    FIND FIRST tqueasy WHERE tqueasy.KEY = 285 
        AND tqueasy.char1 = "General Ledger" 
        AND tqueasy.number1 = 1
        AND tqueasy.char2 = idFlag NO-LOCK NO-ERROR.
    IF AVAILABLE tqueasy THEN DO:
        ASSIGN doneFlag = NO.
        /*MESSAGE "2" doneFlag VIEW-AS ALERT-BOX INFO.*/
    END.
    ELSE DO: 
        ASSIGN doneFlag = YES.
        /*MESSAGE "3" doneFlag VIEW-AS ALERT-BOX INFO.*/
    END.
END.

FIND FIRST tqueasy WHERE tqueasy.KEY = 285 
      AND tqueasy.char1 = "General Ledger" 
      AND tqueasy.number1 = 0
      AND tqueasy.char2 = idFlag NO-LOCK NO-ERROR.
IF AVAILABLE tqueasy THEN DO:
    FIND CURRENT tqueasy EXCLUSIVE-LOCK.
    DELETE tqueasy.
    RELEASE tqueasy.
END.

 


PROCEDURE decode-string: 
DEFINE INPUT PARAMETER in-str   AS CHAR. 
DEFINE OUTPUT PARAMETER out-str AS CHAR INITIAL "". 
DEFINE VARIABLE s   AS CHAR. 
DEFINE VARIABLE j   AS INTEGER. 
DEFINE VARIABLE len AS INTEGER. 
  s = in-str. 
  j = ASC(SUBSTR(s, 1, 1)) - 70. 
  len = LENGTH(in-str) - 1. 
  s = SUBSTR(in-str, 2, len). 
  DO len = 1 TO LENGTH(s): 
    out-str = out-str + chr(asc(SUBSTR(s,len,1)) - j). 
  END. 
END. 

