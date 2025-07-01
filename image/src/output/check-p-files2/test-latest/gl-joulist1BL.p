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
    FIELD prev-bal    AS CHARACTER FORMAT "x(20)".   /* gerald budget awal 080420 */

DEFINE BUFFER g-jour FOR gl-journal.

DEFINE INPUT PARAMETER TABLE FOR out-list.
FOR EACH out-list NO-LOCK:
    FIND FIRST gl-journal WHERE RECID(gl-journal) = out-list.s-recid NO-LOCK NO-ERROR.
    IF AVAILABLE gl-journal THEN DO :
        FIND FIRST g-jour WHERE RECID(g-jour) = RECID(gl-journal) EXCLUSIVE-LOCK.
        IF NUM-ENTRIES(g-jour.bemerk, CHR(2)) GT 1 THEN
            ASSIGN ENTRY (2, g-jour.bemerk, CHR(2)) = out-list.number1.
        ELSE ASSIGN g-jour.bemerk = g-jour.bemerk + CHR(2) + out-list.number1.
        FIND CURRENT g-jour NO-LOCK.
        RELEASE g-jour.
    END.
END.
