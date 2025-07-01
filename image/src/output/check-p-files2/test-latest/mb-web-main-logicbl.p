DEF TEMP-TABLE f-foinv
    FIELD price-decimal     AS INTEGER
    FIELD briefnr2314       AS INTEGER
    FIELD param60           AS INTEGER
    FIELD param145          AS INTEGER
    FIELD param487          AS INTEGER
    FIELD tel-rechnr        AS INTEGER
    FIELD pos1              AS INTEGER
    FIELD pos2              AS INTEGER
    FIELD ba-dept           AS INTEGER INIT -1
    FIELD exchg-rate        AS DECIMAL
    FIELD max-price         AS DECIMAL
    FIELD param132          AS CHAR
    FIELD ext-char          AS CHAR
    FIELD curr-local        AS CHAR
    FIELD curr-foreign      AS CHAR
    FIELD b-title           AS CHAR
    FIELD gname             AS CHAR
    
    FIELD param219          AS LOGICAL
    FIELD double-currency   AS LOGICAL
    FIELD foreign-rate      AS LOGICAL
    FIELD banquet-flag      AS LOGICAL
    FIELD mc-flag           AS LOGICAL
.
DEFINE TEMP-TABLE t-bill        LIKE bill
    FIELD bl-recid          AS INTEGER.
DEFINE TEMP-TABLE t-guest       LIKE guest.
DEFINE TEMP-TABLE artlist       LIKE artikel.
DEFINE INPUT PARAMETER bil-flag          AS INTEGER. 
DEFINE INPUT PARAMETER curr-department   AS INT.
DEFINE OUTPUT PARAMETER CashDrw-Prog     AS CHAR.
DEFINE OUTPUT PARAMETER combo-pf-file1   AS CHAR     NO-UNDO.
DEFINE OUTPUT PARAMETER combo-pf-file2   AS CHAR     NO-UNDO.
DEFINE OUTPUT PARAMETER combo-gastnr     AS INTEGER  NO-UNDO.
DEFINE OUTPUT PARAMETER combo-ledger     AS INTEGER  NO-UNDO.
DEFINE OUTPUT PARAMETER foreign-rate     AS LOGICAL. 
DEFINE OUTPUT PARAMETER double-currency  AS LOGICAL INITIAL NO. 
DEFINE OUTPUT PARAMETER curr-local       AS CHAR. 
DEFINE OUTPUT PARAMETER curr-foreign     AS CHAR. 
DEFINE OUTPUT PARAMETER exchg-rate       AS DECIMAL INITIAL 1. 
DEFINE OUTPUT PARAMETER price-decimal    AS INTEGER. 
DEFINE OUTPUT PARAMETER ba-dept          AS INTEGER INITIAL -1. 
DEFINE OUTPUT PARAMETER gname            AS CHAR.
DEFINE OUTPUT PARAMETER golf-license     AS LOGICAL INITIAL NO.
DEFINE OUTPUT PARAMETER mc-flag          AS LOGICAL INITIAL NO. 
DEFINE OUTPUT PARAMETER pos1             AS INTEGER INITIAL 0. 
DEFINE OUTPUT PARAMETER pos2             AS INTEGER INITIAL 0. 
DEFINE OUTPUT PARAMETER lvAnzVat         AS INTEGER INITIAL 0 NO-UNDO.
DEFINE OUTPUT PARAMETER cash-refund-str  AS CHAR NO-UNDO INIT "".
DEFINE OUTPUT PARAMETER rebate-str       AS CHAR NO-UNDO INIT "".
DEFINE OUTPUT PARAMETER b1-title         AS CHAR NO-UNDO INIT "".
DEFINE OUTPUT PARAMETER vat-artlist      AS INTEGER EXTENT 4 INITIAL [0,0,0,0].
DEFINE OUTPUT PARAMETER r-zahlungsart    AS INTEGER.
DEFINE OUTPUT PARAMETER tel-rechnr       AS INTEGER.
DEFINE OUTPUT PARAMETER param146         AS LOGICAL. 
DEFINE OUTPUT PARAMETER param199         AS LOGICAL. 
DEFINE OUTPUT PARAMETER param219         AS LOGICAL. 
DEFINE OUTPUT PARAMETER param60          AS INTEGER. 
DEFINE OUTPUT PARAMETER param145         AS INTEGER. 
DEFINE OUTPUT PARAMETER param497         AS INTEGER. 
DEFINE OUTPUT PARAMETER TABLE FOR artlist.
DEFINE VARIABLE lvInt1                   AS INTEGER INITIAL 0 NO-UNDO.
RUN htpchar.p (870,OUTPUT CashDrw-Prog). 
RUN htplogic.p (146, OUTPUT param146).
RUN htplogic.p (199, OUTPUT param199).
RUN htplogic.p (219, OUTPUT param219).
RUN htpint.p (60, OUTPUT param60).
RUN htpint.p (145, OUTPUT param145).
FIND FIRST htparam WHERE paramnr = 497 no-lock. 
IF htparam.finteger GT 0 THEN 
DO: 
  FIND FIRST brief WHERE brief.briefnr = htparam.finteger NO-LOCK NO-ERROR. 
  IF AVAILABLE brief THEN param497 = htparam.finteger. 
END.
RUN prepare-ns-invbl.p (0, curr-department, OUTPUT TABLE f-foinv,
  OUTPUT TABLE t-bill, OUTPUT TABLE t-guest, INPUT-OUTPUT combo-pf-file1, 
  INPUT-OUTPUT combo-pf-file2, INPUT-OUTPUT combo-gastnr, INPUT-OUTPUT combo-ledger).
FIND FIRST f-foinv.
FIND FIRST t-bill NO-ERROR.
FIND FIRST t-guest NO-ERROR.
ASSIGN
    price-decimal   = f-foinv.price-decimal
    double-currency = f-foinv.double-currency
    ext-char        = ENTRY(1, f-foinv.ext-char, ";")
    foreign-rate    = f-foinv.foreign-rate
    exchg-rate      = f-foinv.exchg-rate
    pos1            = f-foinv.pos1
    pos2            = f-foinv.pos2
    mc-flag         = f-foinv.mc-flag 
    ba-dept         = f-foinv.ba-dept
    curr-local      = f-foinv.curr-local
    curr-foreign    = f-foinv.curr-foreign
    golf-license    = (ENTRY(1, f-foinv.gname,CHR(2)) = "YES")
    gname           = ENTRY(2, f-foinv.gname, CHR(2)) 
    tel-rechnr      = f-foinv.tel-rechnr NO-ERROR
    .
IF exchg-rate = 0 THEN
    ASSIGN exchg-rate = 1.
IF NUM-ENTRIES(f-foinv.ext-char, ";") GT 1 THEN
ASSIGN
    cash-refund-str = "," + ENTRY(2, f-foinv.ext-char, ";") + ","
    rebate-str      = "," + ENTRY(3, f-foinv.ext-char, ";") + "," 
    cash-refund-str = REPLACE(cash-refund-str," ","")
    rebate-str      = REPLACE(rebate-str," ", "")
    rebate-str      = REPLACE(rebate-str,";", "") NO-ERROR
.
    
ASSIGN lvAnzVat = 0.
IF f-foinv.param132 NE "" THEN
DO lvInt1 = 1 TO NUM-ENTRIES(f-foinv.param132, ";"):
  IF INTEGER(ENTRY(lvInt1, f-foinv.param132, ";")) NE 0 THEN
  ASSIGN
    lvAnzVat              = lvAnzVat + 1
    vat-artlist[lvAnzVat] = INTEGER(ENTRY(lvInt1, f-foinv.param132, ";"))
  .
END.
IF bil-flag = 0 THEN b1-title = "DEPT " + f-foinv.b-title. 
ELSE IF bil-flag = 1 THEN b1-title = "CLOSED BILLS - DEPT " + f-foinv.b-title. 
RUN read-artikel1bl.p(25, ?, curr-department, ?, ?, ?, YES, OUTPUT TABLE artlist).
