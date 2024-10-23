DEFINE TEMP-TABLE t-bill-line       LIKE bill-line
    FIELD bl-recid  AS INTEGER
    FIELD artart    AS INTEGER
    FIELD tool-tip  AS CHAR
.
DEFINE TEMP-TABLE t-blinebuff   LIKE bill-line
    FIELD bl-recid  AS INTEGER
    FIELD artart    AS INTEGER
    FIELD tool-tip  AS CHAR
.
DEFINE TEMP-TABLE t-bill        LIKE bill
    FIELD bl-recid          AS INTEGER.

DEFINE INPUT PARAMETER pvILanguage           AS INTEGER. /*FD*/
DEFINE INPUT PARAMETER bil-flag              AS INTEGER. /*FD*/
DEFINE INPUT PARAMETER b-recid               AS INTEGER. /*FD*/

DEFINE INPUT PARAMETER t-bill-rechnr         AS INTEGER.
DEFINE INPUT PARAMETER bill-line-departement AS INTEGER.
DEFINE INPUT PARAMETER transdate             AS DATE.
DEFINE INPUT PARAMETER billart               AS INTEGER.
DEFINE INPUT PARAMETER qty                   AS INTEGER.
DEFINE INPUT PARAMETER price                 AS DECIMAL.
DEFINE INPUT PARAMETER amount                AS DECIMAL.
DEFINE INPUT PARAMETER amount-foreign        AS DECIMAL.
DEFINE INPUT PARAMETER DESCRIPTION           AS CHAR.
DEFINE INPUT PARAMETER voucher-nr            AS CHAR.
DEFINE INPUT PARAMETER cancel-str            AS CHAR.
DEFINE INPUT PARAMETER user-init             AS CHAR.
DEFINE INPUT-OUTPUT PARAMETER rechnr                AS INTEGER.
DEFINE INPUT-OUTPUT PARAMETER balance               AS DECIMAL.
DEFINE INPUT-OUTPUT PARAMETER balance-foreign       AS DECIMAL.
DEFINE OUTPUT PARAMETER msg-str       AS CHAR     NO-UNDO.
DEFINE OUTPUT PARAMETER success-flag  AS LOGICAL  NO-UNDO.
DEFINE OUTPUT PARAMETER TABLE FOR t-bill.
DEFINE OUTPUT PARAMETER TABLE FOR t-bill-line.

/* FD For Testing
DEFINE VARIABLE pvILanguage           AS INTEGER INIT 1. 
DEFINE VARIABLE bil-flag              AS INTEGER INIT 0. 
DEFINE VARIABLE b-recid               AS INTEGER INIT 4670030. 
DEFINE VARIABLE t-bill-rechnr         AS INTEGER INIT 37182.
DEFINE VARIABLE bill-line-departement AS INTEGER INIT 0.
DEFINE VARIABLE transdate             AS DATE INIT ?.
DEFINE VARIABLE billart               AS INTEGER INIT 131.
DEFINE VARIABLE qty                   AS INTEGER INIT 2.
DEFINE VARIABLE price                 AS DECIMAL INIT 10000.
DEFINE VARIABLE amount                AS DECIMAL INIT 10000.
DEFINE VARIABLE amount-foreign        AS DECIMAL INIT 10000.
DEFINE VARIABLE DESCRIPTION           AS CHAR INIT "BC Internet".
DEFINE VARIABLE voucher-nr            AS CHAR INIT "Testing Papul".
DEFINE VARIABLE cancel-str            AS CHAR INIT "".
DEFINE VARIABLE user-init             AS CHAR INIT "01".
DEFINE VARIABLE rechnr                AS INTEGER INIT 37182.
DEFINE VARIABLE balance               AS DECIMAL INIT 20000.
DEFINE VARIABLE balance-foreign       AS DECIMAL INIT 20000.
DEFINE VARIABLE msg-str               AS CHAR     NO-UNDO.
DEFINE VARIABLE success-flag          AS LOGICAL  NO-UNDO.
*/
{SupertransBL.i}
DEFINE VARIABLE lvCAREA         AS CHAR INITIAL "ns-web-update-billbl".

DEFINE VARIABLE master-str    AS CHAR       NO-UNDO.
DEFINE VARIABLE master-rechnr AS CHAR       NO-UNDO.
DEFINE VARIABLE master-flag   AS LOGICAL    NO-UNDO.
DEFINE VARIABLE msg-answer    AS LOGICAL    NO-UNDO.
DEFINE VARIABLE str1          AS CHARACTER  NO-UNDO INIT "NS".
DEFINE VARIABLE bline-dept    AS INTEGER    NO-UNDO.
DEFINE VARIABLE gname         AS CHARACTER  NO-UNDO.
DEFINE VARIABLE bil-recid     AS INTEGER    NO-UNDO.

DEFINE VARIABLE telbill-flag AS LOGICAL NO-UNDO.
DEFINE VARIABLE babill-flag  AS LOGICAL NO-UNDO.

bline-dept = bill-line-departement.

IF t-bill-rechnr NE 0 THEN
DO:    
    RUN ns-invoice-check-saldobl.p (0, t-bill-rechnr, OUTPUT TABLE t-bill, OUTPUT TABLE t-bill-line).
    FIND FIRST t-bill NO-LOCK NO-ERROR. 
    IF AVAILABLE t-bill AND t-bill.resnr = 0 AND t-bill.flag = 0 THEN 
    DO: 
        bil-recid   = t-bill.bl-recid. 
        gname       = t-bill.name.            
    END.         
END.

RUN inv-update-billbl.p (pvILanguage, bil-flag, str1,
    transdate, b-recid, bline-dept, billart,
    qty, price, amount, amount-foreign, DESCRIPTION,
    voucher-nr, cancel-str, user-init, INPUT-OUTPUT rechnr,
    INPUT-OUTPUT master-str, INPUT-OUTPUT master-rechnr,
    INPUT-OUTPUT balance, INPUT-OUTPUT balance-foreign, 
    OUTPUT master-flag, OUTPUT msg-str, OUTPUT success-flag,
    OUTPUT TABLE t-blinebuff).
/* Comment FD
ASSIGN
    t-bill.rechnr = rechnr. 

IF NOT master-flag THEN  
ASSIGN 
    t-bill.saldo    = t-bill.saldo + amount
    t-bill.mwst[99] = t-bill.mwst[99] + amount-foreign.
*/
RUN read-bill2bl.p (5, b-recid, ?, ?, ?, ?, ?, ?, ?, ?,             /*FD*/
    OUTPUT telbill-flag, OUTPUT babill-flag, OUTPUT TABLE t-bill).

FIND FIRST t-blinebuff NO-ERROR.
IF AVAILABLE t-blinebuff THEN
DO:
    CREATE t-bill-line.
    BUFFER-COPY t-blinebuff TO t-bill-line.
END.



