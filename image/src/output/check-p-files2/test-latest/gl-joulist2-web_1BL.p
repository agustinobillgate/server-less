DEFINE TEMP-TABLE out-list
    FIELD s-recid       AS INTEGER
    FIELD marked        AS CHARACTER FORMAT "x(1)" LABEL "M"
    FIELD fibukonto     AS CHARACTER
    FIELD jnr           AS INTEGER INITIAL 0 FORMAT ">>>,>>>,>>9"
    FIELD jtype         AS INTEGER
    FIELD bemerk        AS CHARACTER FORMAT "x(100)"
    FIELD trans-date    AS DATE
    FIELD bezeich       AS CHARACTER FORMAT "x(40)"
    FIELD number1       AS CHARACTER FORMAT "x(10)"
    FIELD debit         AS DECIMAL FORMAT "->>>,>>>,>>>,>>9.99"
    FIELD credit        AS DECIMAL FORMAT "->>>,>>>,>>>,>>9.99"
    FIELD balance       AS DECIMAL FORMAT "->>>,>>>,>>>,>>9.99"
    FIELD debit-str     AS CHARACTER FORMAT "x(21)"
    FIELD credit-str    AS CHARACTER FORMAT "x(21)"
    FIELD balance-str   AS CHARACTER FORMAT "x(22)"
    FIELD refno         AS CHARACTER FORMAT "x(30)"
    FIELD uid           AS CHARACTER FORMAT "x(3)"
    FIELD created       AS DATE
    FIELD chgID         AS CHARACTER FORMAT "x(3)"
    FIELD chgDate       AS DATE
    FIELD tax-code      AS CHAR FORMAT "x(10)"
    FIELD tax-amount    AS CHAR FORMAT "x(19)"
    FIELD tot-amt       AS CHAR
    FIELD approved      AS LOGICAL INIT NO
    FIELD prev-bal      AS CHARACTER /* add by gerald budget awal 080420 */
    FIELD dept-code   AS INTEGER
    FIELD coa-bezeich AS CHAR /*MCH Dec 20, 2024 => 600A0F Req Amaranta Prambanan*/
 .


DEFINE TEMP-TABLE g-list
    FIELD grecid    AS INTEGER
    FIELD fibu      AS CHARACTER
    INDEX fibu_ix fibu.

DEFINE TEMP-TABLE j-list
    FIELD grecid    AS INTEGER
    FIELD fibu      AS CHARACTER
    FIELD datum     AS DATE
    INDEX fibu_ix fibu.

DEFINE INPUT PARAMETER from-date    AS DATE.
DEFINE INPUT PARAMETER to-date      AS DATE.
DEFINE INPUT PARAMETER last-2yr     AS DATE.
DEFINE INPUT PARAMETER close-year   AS DATE.
DEFINE INPUT PARAMETER journaltype  AS INT.
DEFINE INPUT PARAMETER excl-other   AS LOGICAL.
DEFINE INPUT PARAMETER other-dept   AS LOGICAL.
DEFINE INPUT PARAMETER summ-date    AS LOGICAL.
DEFINE INPUT PARAMETER from-fibu    AS CHAR.
DEFINE INPUT PARAMETER to-fibu      AS CHAR.
DEFINE INPUT PARAMETER sorttype     AS INT.
DEFINE INPUT PARAMETER from-dept    AS INT.
DEFINE INPUT PARAMETER journaltype1 AS INT.
DEFINE INPUT PARAMETER cashflow     AS LOGICAL.
DEFINE INPUT PARAMETER f-note       AS CHAR.   
DEFINE INPUT PARAMETER from-main    AS INTEGER. 
DEFINE INPUT PARAMETER idFlag       AS CHAR.

DEFINE VARIABLE str    AS CHAR NO-UNDO.
DEFINE VARIABLE htl-no AS CHAR NO-UNDO.
DEFINE STREAM s1.

DEFINE VARIABLE tdate AS CHAR NO-UNDO.
DEFINE VARIABLE crdate AS CHAR NO-UNDO.
DEFINE VARIABLE cgdate AS CHAR NO-UNDO.
DEFINE VARIABLE counter AS INTEGER NO-UNDO INITIAL 0.

DEFINE BUFFER bqueasy FOR queasy.
DEFINE BUFFER tqueasy FOR queasy.



CREATE queasy.
ASSIGN queasy.KEY      = 285
       queasy.char1    = "General Ledger"
       queasy.number1  = 1
       queasy.char2    = idFlag.
RELEASE queasy.


DEFINE VARIABLE curr-time AS INTEGER.
ASSIGN curr-time = TIME.

FIND FIRST paramtext WHERE paramtext.txtnr = 243 NO-LOCK NO-ERROR. 
IF AVAILABLE paramtext AND paramtext.ptexte NE "" THEN
  RUN decode-string(paramtext.ptexte, OUTPUT htl-no). 

RUN gl-joulist_2-webbl.p(from-date, to-date, last-2yr, close-year, journaltype,
                 excl-other, other-dept, summ-date, from-fibu, to-fibu, sorttype,
                 from-dept, journaltype1, cashflow, f-note, from-main, OUTPUT TABLE out-list).

/*MESSAGE "a" STRING(TIME - curr-time, "HH:MM:SS") VIEW-AS ALERT-BOX INFO.*/
  

ASSIGN curr-time = TIME.

FIND FIRST out-list NO-ERROR.
DO WHILE AVAILABLE out-list:
    
    IF LENGTH(out-list.bemerk) GT 100 THEN
        ASSIGN out-list.bemerk = SUBSTR(out-list.bemerk, 1, 100).

    IF LENGTH(out-list.bezeich) GT 100 THEN
        ASSIGN out-list.bezeich = SUBSTR(out-list.bezeich, 1, 100).

    IF LENGTH(out-list.refno) GT 100 THEN
        ASSIGN out-list.refno = SUBSTR(out-list.refno, 1, 100).

    ASSIGN out-list.bezeich = REPLACE(out-list.bezeich, CHR(10),"")
           out-list.bezeich = REPLACE(out-list.bezeich, CHR(13),"")           
           out-list.refno   = REPLACE(out-list.refno, CHR(10),"")
           out-list.refno   = REPLACE(out-list.refno, CHR(13),"")
           out-list.bemerk  = REPLACE(out-list.bemerk, CHR(10),"")
           out-list.bemerk  = REPLACE(out-list.bemerk, CHR(13),"")
           out-list.bemerk  = REPLACE(out-list.bemerk, "|"," ")
           out-list.bezeich = REPLACE(out-list.bezeich, "|"," ")
           out-list.refno   = REPLACE(out-list.refno, "|"," ")
           counter          = counter + 1
        .

    IF out-list.uid = ? THEN ASSIGN out-list.uid = "".

    IF out-list.trans-date = ? THEN ASSIGN tdate = "".
    ELSE ASSIGN tdate = STRING(out-list.trans-date).

    IF out-list.created = ? THEN ASSIGN crdate = "".
    ELSE ASSIGN crdate = STRING(out-list.created).

    IF out-list.chgDate = ? THEN ASSIGN cgdate = "".
    ELSE ASSIGN cgdate = STRING(out-list.chgDate).
    
    CREATE queasy.
    ASSIGN queasy.KEY   = 280
           queasy.char1 = "General Ledger"
           queasy.char3 = idFlag
           queasy.char2 = STRING(out-list.s-recid)      + "|" + 
                          out-list.marked               + "|" +
                          out-list.fibukonto            + "|" +
                          STRING(out-list.jnr)          + "|" +
                          STRING(out-list.jtype)        + "|" +
                          out-list.bemerk               + "|" +
                          tdate                         + "|" +
                          out-list.bezeich              + "|" +
                          out-list.number1              + "|" +
                          STRING(out-list.debit)        + "|" +
                          STRING(out-list.credit)       + "|" +
                          STRING(out-list.balance)      + "|" +
                          out-list.debit-str            + "|" +
                          out-list.credit-str           + "|" +
                          out-list.balance-str          + "|" +
                          out-list.refno                + "|" +
                          out-list.uid                  + "|" +
                          crdate                        + "|" +
                          out-list.chgID                + "|" +
                          cgdate                        + "|" +
                          out-list.tax-code             + "|" +
                          out-list.tax-amount           + "|" +
                          out-list.tot-amt              + "|" +
                          STRING(out-list.approved)     + "|" +
                          out-list.prev-bal             + "|" +
                          STRING(out-list.dept-code)    + "|" +
                          STRING(out-list.coa-bezeich)
            queasy.number1 = counter.
    FIND NEXT out-list NO-ERROR.
END.

/*MESSAGE "b" STRING(TIME - curr-time, "HH:MM:SS") VIEW-AS ALERT-BOX INFO.*/


FIND FIRST bqueasy WHERE bqueasy.KEY = 285
    AND bqueasy.char1 = "General Ledger"
    AND bqueasy.char2 = idFlag NO-LOCK NO-ERROR.
IF AVAILABLE bqueasy THEN DO:
    FIND CURRENT bqueasy EXCLUSIVE-LOCK.
    ASSIGN bqueasy.number1 = 0.
    FIND CURRENT bqueasy NO-LOCK.
    RELEASE bqueasy.
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
