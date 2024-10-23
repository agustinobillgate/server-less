DEF TEMP-TABLE cost-list
  FIELD month-i     AS INTEGER FORMAT ">9"   COLUMN-LABEL "mm"
  FIELD year-i      AS INTEGER FORMAT "9999" COLUMN-LABEL "Year"
  FIELD budget      AS DECIMAL FORMAT ">>>,>>>,>>9" INIT 0
  FIELD actual      AS DECIMAL FORMAT "->,>>>,>>>,>>9" INIT 0
  FIELD ytd-budget  AS DECIMAL FORMAT ">>>,>>>,>>9" INIT 0
  FIELD ytd-actual  AS DECIMAL FORMAT "->,>>>,>>>,>>9" INIT 0
.

DEFINE TEMP-TABLE alloc-list 
  FIELD fibu  LIKE gl-acct.fibukonto LABEL "Account Number". 

DEF INPUT  PARAMETER deptno      AS INTEGER  NO-UNDO.
DEF INPUT  PARAMETER artno       AS INTEGER  NO-UNDO.
DEF INPUT  PARAMETER from-date   AS DATE     NO-UNDO.
DEF OUTPUT PARAMETER TABLE       FOR cost-list.

/*
DEF VAR from-date   AS DATE    INIT 02/01/2010  NO-UNDO.
DEF VAR deptno      AS INTEGER INIT 11          NO-UNDO. 
DEF VAR artno       AS INTEGER INIT 3300041     NO-UNDO.
DEF VAR ytd-flag    AS LOGICAL INIT NO          NO-UNDO.
*/


DEF VAR to-date         AS DATE             NO-UNDO.
DEF VAR curr-date       AS DATE             NO-UNDO.
DEF VAR inv-close-date  AS DATE             NO-UNDO.

DEF BUFFER pbuff FOR parameters.

FIND FIRST parameters WHERE parameters.progname = "CostCenter" 
  AND parameters.section = "Name"  
  AND INTEGER(parameters.varname) = deptno NO-LOCK NO-ERROR.
IF NOT AVAILABLE parameters THEN RETURN.

FOR EACH pbuff WHERE pbuff.progname = "CostCenter" 
  AND pbuff.section = "Alloc" 
  AND pbuff.varname = parameters.varname NO-LOCK: 
  FIND FIRST gl-acct WHERE gl-acct.fibukonto = pbuff.vstring NO-LOCK 
    NO-ERROR. 
  IF AVAILABLE gl-acct THEN 
  DO: 
    CREATE alloc-list.
    ASSIGN alloc-list.fibu = pbuff.vstring. 
  END. 
END.

FIND FIRST l-artikel WHERE l-artikel.artnr = artno NO-LOCK.

FIND FIRST htparam WHERE htparam.paramnr = 110 NO-LOCK.
ASSIGN to-date = htparam.fdate.

IF artno LE 2999999 THEN FIND FIRST htparam 
  WHERE htparam.paramnr = 224 NO-LOCK. /* FB closing */
ELSE FIND FIRST htparam 
  WHERE htparam.paramnr = 221 NO-LOCK. /* Mat closing */
ASSIGN inv-close-date = htparam.fdate.

DO curr-date = from-date TO to-date:
  RUN create-costlist.
END.

RUN calc-ytd.

PROCEDURE create-costlist:
DEF VAR fdate AS DATE NO-UNDO.
DEF VAR tdate AS DATE NO-UNDO.
DEF VAR cdate AS DATE NO-UNDO.

  ASSIGN 
      fdate = DATE(MONTH(curr-date), 1, YEAR(curr-date))
      tdate = tdate + 31
      tdate = DATE(MONTH(tdate), 1, YEAR(tdate)) - 1
  .
  FIND FIRST cost-list WHERE cost-list.month-i = MONTH(curr-date)
      AND cost-list.year-i = YEAR(curr-date) NO-ERROR.
  IF NOT AVAILABLE cost-list THEN
  DO:
    CREATE cost-list.
    ASSIGN 
        cost-list.month-i = MONTH(curr-date)
        cost-list.year-i  = YEAR(curr-date)
    .

    DO cdate = fdate TO tdate:
      FIND FIRST costbudget WHERE costbudget.departement = deptno
        AND costbudget.zwkum = l-artikel.zwkum
        AND costbudget.artnr = artno
        AND costbudget.datum = cdate USE-INDEX depart_ix 
        NO-LOCK NO-ERROR.
      IF NOT AVAILABLE costbudget THEN
      FIND FIRST costbudget WHERE costbudget.departement = deptno
        AND costbudget.zwkum = l-artikel.zwkum
        AND costbudget.artnr = 0
        AND costbudget.datum = cdate USE-INDEX depart_ix
        NO-LOCK NO-ERROR.
      IF AVAILABLE costbudget THEN
      ASSIGN cost-list.budget = cost-list.budget + costbudget.betrag.
    END.
  END.
  IF MONTH(curr-date) = MONTH(inv-close-date)
     AND YEAR(curr-date) = YEAR(inv-close-date) THEN
  FOR EACH l-op WHERE l-op.artnr = artno AND l-op.op-art = 3 
    AND l-op.datum GE fdate AND l-op.datum LE to-date
    AND l-op.loeschflag LE 1 NO-LOCK:
    FIND FIRST alloc-list WHERE alloc-list.fibu = l-op.stornogrund
      NO-ERROR.
    IF AVAILABLE alloc-list THEN
      ASSIGN cost-list.actual = cost-list.actual + l-op.warenwert.
  END.
  ELSE IF curr-date LT DATE(MONTH(inv-close-date), 1, YEAR(inv-close-date)) THEN
  FOR EACH l-ophis WHERE l-ophis.artnr = artno AND l-ophis.op-art = 3 
    AND l-ophis.datum GE fdate AND l-ophis.datum LE tdate NO-LOCK:
    FIND FIRST alloc-list WHERE alloc-list.fibu = l-ophis.fibukonto
      NO-ERROR.
    IF AVAILABLE alloc-list THEN
    ASSIGN cost-list.actual = cost-list.actual + l-ophis.warenwert.
  END.
END.

PROCEDURE calc-ytd:
DEF BUFFER cbuff FOR cost-list.
  FOR EACH cost-list:
    FOR EACH cbuff WHERE ((cbuff.month-i LE cost-list.month-i)
        AND (cbuff.year-i EQ cost-list.year-i))
        OR (cbuff.year-i LT cost-list.year-i):
      ASSIGN
        cost-list.ytd-budget = cost-list.ytd-budget + cbuff.budget
        cost-list.ytd-actual = cost-list.ytd-actual + cbuff.actual
      .
    END.
  END.
END.
