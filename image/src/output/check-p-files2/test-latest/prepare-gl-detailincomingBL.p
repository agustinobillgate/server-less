DEF TEMP-TABLE s-list 
    FIELD datum        LIKE l-op.datum 
    FIELD lager-nr     LIKE l-op.lager-nr    COLUMN-LABEL "StNo" 
    FIELD artnr        LIKE l-artikel.artnr 
    FIELD bezeich      LIKE l-artikel.bezeich 
    FIELD einzelpreis  LIKE l-op.einzelpreis FORMAT "->>>,>>>,>>9.99" LABEL "Unit Price" 
    FIELD anzahl       LIKE l-op.anzahl 
    FIELD warenwert    LIKE l-op.warenwert   FORMAT "->>>,>>>,>>9.99" LABEL "Amount" 
    FIELD firma        LIKE l-lieferant.firma 
    FIELD docu-nr      LIKE l-op.docu-nr     COLUMN-LABEL "Document No" 
    FIELD lscheinnr    LIKE l-op.lscheinnr   COLUMN-LABEL "Delivery Note" 
    FIELD fibu         LIKE gl-acct.fibukonto 
    FIELD lief-nr      LIKE l-op.lief-nr 
    FIELD lflag        AS LOGICAL INITIAL NO
    FIELD avail-l-ord  AS LOGICAL INIT NO.

DEF TEMP-TABLE t-gl-acct LIKE gl-acct.

DEF INPUT  PARAMETER fibu           AS CHAR.
DEF INPUT  PARAMETER from-date      AS DATE.
DEF INPUT  PARAMETER bemerk         AS CHAR. 
DEF OUTPUT PARAMETER close-date     AS DATE.
DEF OUTPUT PARAMETER TABLE FOR s-list.
DEF OUTPUT PARAMETER TABLE FOR t-gl-acct.

FIND FIRST gl-acct WHERE gl-acct.fibukonto = fibu NO-LOCK.
CREATE t-gl-acct.
BUFFER-COPY gl-acct TO t-gl-acct.

FIND FIRST htparam WHERE htparam.paramnr = 224 NO-LOCK. 
close-date = htparam.fdate.

IF from-date GE DATE(MONTH(close-date), 1, YEAR(close-date)) THEN 
RUN disp-it. 
ELSE RUN disp-hist.

FOR EACH s-list:
  FIND FIRST l-orderhdr WHERE l-orderhdr.lief-nr = s-list.lief-nr 
    AND l-orderhdr.docu-nr = s-list.docu-nr 
    AND l-orderhdr.betriebsnr LE 1 NO-LOCK NO-ERROR. 
  IF AVAILABLE l-orderhdr THEN s-list.avail-l-ord = YES.
END.


PROCEDURE disp-it: 
DEF VAR lager-nr        AS INTEGER NO-UNDO. 
DEF VAR lief-nr         AS INTEGER NO-UNDO. 
DEF VAR docu-nr         AS CHAR    NO-UNDO. 
DEF VAR lscheinnr       AS CHAR    NO-UNDO. 
DEF VAR bezeich         AS CHAR    NO-UNDO INIT "". 
   
  IF gl-acct.acc-type = 3 THEN 
  DO: 
    IF bemerk NE ""  THEN DO:
        ASSIGN 
            lager-nr  =  INTEGER(ENTRY(4, bemerk, ";"))
            lief-nr   =  INTEGER(ENTRY(5, bemerk, ";")) 
            docu-nr   =  ENTRY(6, bemerk, ";") 
            lscheinnr =  ENTRY(7, bemerk, ";") 
            bezeich   =  SUBSTR(ENTRY(1, bemerk, ";"), LENGTH(lscheinnr) + 2, LENGTH(bemerk)). 
    END.
  END. 
  ELSE /* A/P*/ 
  DO: 
    IF bemerk NE " " THEN DO:
        ASSIGN 
            lager-nr  =  INTEGER(ENTRY(3, bemerk, ";"))
            lief-nr   =  INTEGER(ENTRY(4, bemerk, ";")) 
            docu-nr   =  ENTRY(5, bemerk, ";")
            lscheinnr =  ENTRY(6, bemerk, ";"). 

    END.
  END. 
 
  FOR EACH l-op WHERE l-op.pos GT 0 AND l-op.op-art = 1 
    AND l-op.loeschflag LT 2 AND l-op.datum EQ from-date 
    AND l-op.lager-nr = lager-nr AND l-op.lief-nr = lief-nr 
    AND l-op.lscheinnr = lscheinnr NO-LOCK, 
/*
    FIRST l-ophdr WHERE l-ophdr.lscheinnr = l-op.lscheinnr 
    AND l-ophdr.op-typ = "STI" AND l-ophdr.lager-nr = lager-nr NO-LOCK, 
*/
    FIRST l-artikel WHERE l-artikel.artnr = l-op.artnr NO-LOCK, 
    FIRST l-untergrup WHERE l-untergrup.zwkum = l-artikel.zwkum NO-LOCK 
    BY l-op.artnr: 
 
 
      CREATE s-list. 
      BUFFER-COPY l-op TO s-list. 
 
      FIND FIRST l-lieferant WHERE l-lieferant.lief-nr = l-op.lief-nr 
          NO-LOCK. 
 
      FIND FIRST gl-acct WHERE gl-acct.fibukonto = l-untergrup.fibukonto 
          NO-LOCK NO-ERROR. 
      IF NOT AVAILABLE gl-acct THEN 
      FIND FIRST gl-acct WHERE gl-acct.fibukonto = l-artikel.fibukonto 
          NO-LOCK NO-ERROR. 
      IF AVAILABLE gl-acct THEN 
      ASSIGN 
        s-list.fibu = gl-acct.fibukonto. 
      ASSIGN 
        s-list.firma   = l-lieferant.firma 
        s-list.bezeich = l-artikel.bezeich 
        s-list.lflag   = (bezeich = l-artikel.bezeich). 
  END. 
  /*MTOPEN QUERY q1 FOR EACH s-list.*/
END. 
 
PROCEDURE disp-hist: 
DEF VAR lager-nr        AS INTEGER NO-UNDO. 
DEF VAR lief-nr         AS INTEGER NO-UNDO. 
DEF VAR docu-nr         AS CHAR    NO-UNDO. 
DEF VAR lscheinnr       AS CHAR    NO-UNDO. 
DEF VAR bezeich         AS CHAR    NO-UNDO INIT "". 
     
  IF gl-acct.acc-type = 3 THEN 
  DO: 
    lager-nr  =  INTEGER(ENTRY(4, bemerk, ";")). 
    lief-nr   =  INTEGER(ENTRY(5, bemerk, ";")). 
    docu-nr   =  ENTRY(6, bemerk, ";"). 
    lscheinnr =  ENTRY(7, bemerk, ";"). 
    bezeich   =  SUBSTR(ENTRY(1, bemerk, ";"), LENGTH(lscheinnr) + 2, LENGTH(bemerk)). 
  END. 
  ELSE /* A/P*/ 
  DO: 
    lager-nr  =  INTEGER(ENTRY(3, bemerk, ";")). 
    lief-nr   =  INTEGER(ENTRY(4, bemerk, ";")). 
    docu-nr   =  ENTRY(5, bemerk, ";"). 
    lscheinnr =  ENTRY(6, bemerk, ";"). 
   END. 
 
  FOR EACH l-ophis WHERE l-ophis.lscheinnr = lscheinnr AND l-ophis.op-art = 1 
    AND l-ophis.datum EQ from-date AND l-ophis.lief-nr = lief-nr 
    NO-LOCK USE-INDEX schein-op_ix, 
/*
    FIRST l-ophhis WHERE l-ophhis.lscheinnr = l-ophis.lscheinnr 
    AND l-ophhis.op-typ = "STI" NO-LOCK, 
*/    
    FIRST l-artikel WHERE l-artikel.artnr = l-ophis.artnr NO-LOCK, 
    FIRST l-untergrup WHERE l-untergrup.zwkum = l-artikel.zwkum NO-LOCK 
    BY l-ophis.artnr: 
 
 
      CREATE s-list. 
      BUFFER-COPY l-ophis TO s-list. 
 
      FIND FIRST l-lieferant WHERE l-lieferant.lief-nr = l-ophis.lief-nr 
          NO-LOCK. 
 
      FIND FIRST gl-acct WHERE gl-acct.fibukonto = l-untergrup.fibukonto 
          NO-LOCK NO-ERROR. 
      IF NOT AVAILABLE gl-acct THEN 
      FIND FIRST gl-acct WHERE gl-acct.fibukonto = l-artikel.fibukonto 
          NO-LOCK NO-ERROR. 
      IF AVAILABLE gl-acct THEN 
      ASSIGN 
        s-list.fibu = gl-acct.fibukonto. 
      ASSIGN 
        s-list.firma   = l-lieferant.firma 
        s-list.bezeich = l-artikel.bezeich 
        s-list.docu-nr = l-ophis.docu-nr 
        s-list.lflag   = (bezeich = l-artikel.bezeich). 
  END. 
  /*MTOPEN QUERY q1 FOR EACH s-list. */
END. 
