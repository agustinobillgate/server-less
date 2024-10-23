DEFINE TEMP-TABLE t-bk-reser    LIKE bk-reser.
DEFINE TEMP-TABLE t-guest       LIKE guest.
DEFINE TEMP-TABLE t-htparam     LIKE htparam.
DEFINE TEMP-TABLE t-bk-veran    LIKE bk-veran.
DEFINE TEMP-TABLE t-bill        LIKE bill
    FIELD bl-recid  AS INTEGER.
DEFINE TEMP-TABLE t-bill-line   LIKE bill-line
    FIELD bl-recid  AS INTEGER
    FIELD artart    AS INTEGER
    FIELD tool-tip  AS CHAR
.
DEFINE TEMP-TABLE spbill-list 
    FIELD selected AS LOGICAL INITIAL YES 
    FIELD bl-recid AS INTEGER. 

DEFINE INPUT PARAMETER bil-recid        AS INTEGER.
DEFINE INPUT PARAMETER foreign-rate     AS LOGICAL. 
DEFINE INPUT PARAMETER double-currency  AS LOGICAL INITIAL NO. 
DEFINE INPUT PARAMETER ba-dept          AS INTEGER.

DEFINE OUTPUT PARAMETER invno           AS CHAR.
DEFINE OUTPUT PARAMETER gname           AS CHAR.
DEFINE OUTPUT PARAMETER resname         AS CHAR.
DEFINE OUTPUT PARAMETER rescomment      AS CHAR.
DEFINE OUTPUT PARAMETER printed         AS CHAR.
DEFINE OUTPUT PARAMETER rechnr          AS DECIMAL.
DEFINE OUTPUT PARAMETER balance         AS DECIMAL.
DEFINE OUTPUT PARAMETER balance-foreign AS DECIMAL.
DEFINE OUTPUT PARAMETER kreditlimit     AS DECIMAL.
DEFINE OUTPUT PARAMETER enbtn-bareserve AS LOGICAL. 

DEFINE OUTPUT PARAMETER TABLE FOR t-bill-line. 
DEFINE OUTPUT PARAMETER TABLE FOR t-bill. 

DEFINE VARIABLE curr-select  AS CHAR.
DEFINE VARIABLE telbill-flag AS LOGICAL NO-UNDO.
DEFINE VARIABLE babill-flag  AS LOGICAL NO-UNDO.
DEFINE VARIABLE curr-gname   AS CHAR INITIAL "". 
DEFINE VARIABLE curr-invno   AS INTEGER. 
DEFINE VARIABLE curr-b-recid AS INTEGER. 
DEFINE VARIABLE art-no       AS INTEGER  NO-UNDO.

curr-select = "".
RUN read-bill2bl.p (5, bil-recid, ?, ?, ?, ?, ?, ?, ?, ?,
OUTPUT telbill-flag, OUTPUT babill-flag, OUTPUT TABLE t-bill).
FIND FIRST t-bill NO-ERROR.
    
ASSIGN
  invno         = STRING(t-bill.rechnr) 
  curr-invno    = t-bill.rechnr 
  curr-gname    = gname
  curr-b-recid  = bil-recid
.

RUN read-guestbl.p(1, t-bill.gastnr, ?, ?, OUTPUT TABLE t-guest).
FIND FIRST t-guest NO-LOCK. 
ASSIGN
    resname = t-guest.name + ", " + t-guest.vorname1 + t-guest.anredefirma 
          + " " + t-guest.anrede1 
          + chr(10) + t-guest.adresse1 
          + chr(10) + t-guest.wohnort + " " + t-guest.plz 
          + chr(10) + t-guest.land
    rescomment = t-guest.bemerk
    art-no     = t-guest.zahlungsart
    . 

IF t-bill.bilname NE "" AND t-bill.NAME NE t-bill.bilname THEN
    rescomment = "Guest Name: " + 
                 t-bill.bilname + CHR(10) + rescomment.

IF t-bill.vesrdepot NE "" THEN
ASSIGN
/*       rescomment:BGCOL IN FRAME frame1 = 12 */
/*       rescomment:FGCOL IN FRAME frame1 = 15 */
  rescomment = rescomment + CHR(10) + t-bill.vesrdepot + CHR(10)
    . 
/*     ELSE                                   */
/*     ASSIGN                                 */
/*       rescomment:BGCOL IN FRAME frame1 = 8 */
/*       rescomment:FGCOL IN FRAME frame1 = 0 */
/*     .                                      */

IF t-bill.rgdruck = 0 THEN printed = "". 
ELSE printed = "*". 
rechnr  = t-bill.rechnr. 
balance = t-bill.saldo. 
IF double-currency OR foreign-rate THEN balance-foreign = t-bill.mwst[99]. 
IF t-guest.kreditlimit NE 0 THEN kreditlimit = t-guest.kreditlimit. 
ELSE 
DO: 
    RUN read-htparambl.p (1, 68, ?, OUTPUT TABLE t-htparam).
    FIND FIRST t-htparam NO-LOCK. 
    IF t-htparam.fdecimal NE 0 THEN kreditlimit = t-htparam.fdecimal. 
    ELSE kreditlimit = t-htparam.finteger. 
END. 
/* IF balance LE kreditlimit THEN bcol = 2. */
/* ELSE bcol = 12.                          */

FOR EACH spbill-list: 
    DELETE spbill-list. 
END. 

RUN disp-bill-line(YES). 

IF t-bill.flag = 0 AND t-bill.rechnr > 0 AND t-bill.billtyp = ba-dept AND (t-bill.rechnr NE int(invno)) THEN 
DO: 
    RUN read-bk-veranbl.p (3, ?, ?, t-bill.rechnr, 0, OUTPUT TABLE t-bk-veran).
    FIND FIRST t-bk-veran NO-LOCK NO-ERROR. 
    IF AVAILABLE t-bk-veran THEN 
    DO: 
        RUN read-bk-reserbl.p (4, t-bk-veran.veran-nr, ?, 1, ?, OUTPUT TABLE t-bk-reser).
        FIND FIRST t-bk-reser NO-LOCK NO-ERROR. 
        IF AVAILABLE t-bk-reser THEN enbtn-bareserve = YES.
        ELSE enbtn-bareserve = NO. 
    END. 
END. 
ELSE enbtn-bareserve = NO. 

PROCEDURE disp-bill-line: 
    DEF INPUT PARAMETER read-flag AS LOGICAL NO-UNDO.
    
    IF read-flag THEN
    RUN read-bill-line1bl.p (3, 1, t-bill.rechnr, ?, ?, ?, ?, ?,OUTPUT TABLE t-bill-line).
    FOR EACH t-bill-line NO-LOCK :
        FIND FIRST spbill-list WHERE spbill-list.bl-recid = t-bill-line.bl-recid NO-LOCK NO-ERROR. 
        IF NOT AVAILABLE spbill-list THEN 
        DO: 
            CREATE spbill-list. 
            ASSIGN 
            spbill-list.selected = NO 
            spbill-list.bl-recid = t-bill-line.bl-recid. 
        END.
    END.
/*             OPEN QUERY q1 FOR EACH t-bill-line NO-LOCK,                     */
/*         FIRST spbill-list WHERE spbill-list.bl-recid = t-bill-line.bl-recid */
/*         BY t-bill-line.sysdate DESC BY t-bill-line.zeit DESC.               */
END. 
