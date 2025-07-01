DEF TEMP-TABLE s-list 
    FIELD datum        LIKE l-op.datum 
    FIELD lager-nr     LIKE l-op.lager-nr COLUMN-LABEL "StNo" 
    FIELD artnr        LIKE l-artikel.artnr 
    FIELD bezeich      LIKE l-artikel.bezeich 
    FIELD einzelpreis  LIKE l-op.einzelpreis FORMAT "->>>,>>>,>>9.99" LABEL "Unit Price" 
    FIELD anzahl       LIKE l-op.anzahl 
    FIELD warenwert    LIKE l-op.warenwert   FORMAT "->>>,>>>,>>9.99" LABEL "Amount" 
    FIELD stornogrund  LIKE gl-acct.fibukonto 
    FIELD lscheinnr    LIKE l-op.lscheinnr 
    FIELD lflag        AS LOGICAL. 

DEF TEMP-TABLE t-gl-acct LIKE gl-acct.

DEF INPUT  PARAMETER fibu AS CHAR.
DEF INPUT  PARAMETER from-date AS DATE.
DEF INPUT  PARAMETER bemerk AS CHAR.
DEF OUTPUT PARAMETER close-date AS DATE.
DEF OUTPUT PARAMETER TABLE FOR t-gl-acct.
DEF OUTPUT PARAMETER TABLE FOR s-list.

FIND FIRST gl-acct WHERE gl-acct.fibukonto = fibu NO-LOCK.
CREATE t-gl-acct.
BUFFER-COPY gl-acct TO t-gl-acct.

FIND FIRST htparam WHERE htparam.paramnr = 224 NO-LOCK. 
close-date = htparam.fdate.

IF from-date GE DATE(MONTH(close-date), 1, YEAR(close-date)) THEN RUN disp-it. 
ELSE RUN disp-hist.


PROCEDURE disp-it: 
DEF VAR lscheinnr       AS CHAR    NO-UNDO. 
DEF VAR lbezeich        AS CHAR    NO-UNDO. 
DEF VAR delta           AS DECIMAL NO-UNDO. 
DEF BUFFER gl-acc1      FOR gl-acct. 
 
  lscheinnr = ENTRY(4, bemerk, ";"). 
  lbezeich   =  SUBSTR(ENTRY(1, bemerk, ";"), LENGTH(lscheinnr) + 5, LENGTH(bemerk)). 

  FOR EACH l-op WHERE l-op.pos GT 0 AND l-op.op-art = 3 
    AND l-op.loeschflag LT 2 AND l-op.datum EQ from-date 
    AND l-op.lager-nr GT 0 AND l-op.lscheinnr = lscheinnr NO-LOCK, 
    FIRST l-ophdr WHERE l-ophdr.lscheinnr = l-op.lscheinnr 
    AND l-ophdr.op-typ = "STT" AND l-ophdr.fibukonto NE "" NO-LOCK, 
    FIRST l-artikel WHERE l-artikel.artnr = l-op.artnr NO-LOCK, 
    FIRST l-untergrup WHERE l-untergrup.zwkum = l-artikel.zwkum NO-LOCK 
    BY l-op.stornogrund BY l-op.artnr: 
 
      delta = l-op.warenwert - warenwert. 
      IF delta LT 0 THEN delta = - delta. 
 
      CREATE s-list. 
      BUFFER-COPY l-op TO s-list. 
 
      IF gl-acct.acc-type = 2 OR gl-acct.acc-type = 5 THEN 
      DO: 
        FIND FIRST gl-acc1 WHERE gl-acc1.fibukonto = l-op.stornogrund 
          NO-LOCK NO-ERROR. 
        IF NOT AVAILABLE gl-acc1 THEN 
        FIND FIRST gl-acc1 WHERE gl-acc1.fibukonto = l-ophdr.fibukonto 
          NO-LOCK NO-ERROR. 
      END. 
      ELSE 
      DO: 
        FIND FIRST gl-acc1 WHERE gl-acc1.fibukonto = l-untergrup.fibukonto 
          NO-LOCK NO-ERROR. 
        IF NOT AVAILABLE gl-acc1 THEN 
        FIND FIRST gl-acc1 WHERE gl-acc1.fibukonto = l-artikel.fibukonto 
          NO-LOCK NO-ERROR. 
      END. 
      IF AVAILABLE gl-acc1 THEN 
        ASSIGN 
          s-list.stornogrund = gl-acc1.fibukonto. 
      ASSIGN 
        s-list.bezeich = l-artikel.bezeich. 
      IF gl-acct.acc-type = 2 OR gl-acct.acc-type = 5 THEN 
        s-list.lflag  = (fibu = gl-acc1.fibukonto). 
      ELSE s-list.lflag  = ((lbezeich = l-artikel.bezeich) AND delta LE 0.01). 
  END. 
END. 
 
PROCEDURE disp-hist: 
DEF VAR lscheinnr       AS CHAR    NO-UNDO. 
DEF VAR lbezeich         AS CHAR    NO-UNDO. 
DEF VAR delta           AS DECIMAL NO-UNDO. 
DEF BUFFER gl-acc1      FOR gl-acct. 
 
  lscheinnr = ENTRY(4, bemerk, ";"). 
  lbezeich   =  SUBSTR(ENTRY(1, bemerk, ";"), LENGTH(lscheinnr) + 5, LENGTH(bemerk)). 
 
  FOR EACH l-ophis WHERE l-ophis.lscheinnr = lscheinnr AND l-ophis.op-art = 3 
    AND l-ophis.datum EQ from-date NO-LOCK , 
    /*FIRST l-ophhis WHERE l-ophhis.lscheinnr = l-ophis.lscheinnr 
    AND l-ophhis.op-typ = "STT" AND l-ophhis.datum EQ from-date NO-LOCK,*/ 
    FIRST l-artikel WHERE l-artikel.artnr = l-ophis.artnr NO-LOCK, 
    FIRST l-untergrup WHERE l-untergrup.zwkum = l-artikel.zwkum NO-LOCK 
    BY l-ophis.fibukonto BY l-ophis.artnr: 
 
      delta = l-ophis.warenwert - warenwert. 
      IF delta LT 0 THEN delta = - delta. 
 
      CREATE s-list. 
      BUFFER-COPY l-ophis TO s-list. 
 
      IF gl-acct.acc-type = 2 OR gl-acct.acc-type = 5 THEN 
      DO: 
        FIND FIRST gl-acc1 WHERE gl-acc1.fibukonto = l-ophis.fibukonto 
          NO-LOCK NO-ERROR. 
        IF NOT AVAILABLE gl-acc1 THEN 
        FIND FIRST gl-acc1 WHERE gl-acc1.fibukonto = l-ophhis.fibukonto 
          NO-LOCK NO-ERROR. 
      END. 
      ELSE 
      DO: 
        FIND FIRST gl-acc1 WHERE gl-acc1.fibukonto = l-untergrup.fibukonto 
          NO-LOCK NO-ERROR. 
        IF NOT AVAILABLE gl-acc1 THEN 
        FIND FIRST gl-acc1 WHERE gl-acc1.fibukonto = l-artikel.fibukonto 
          NO-LOCK NO-ERROR. 
      END. 
      IF AVAILABLE gl-acc1 THEN 
        ASSIGN 
          s-list.stornogrund = gl-acc1.fibukonto. 
      ASSIGN 
        s-list.bezeich = l-artikel.bezeich. 
      IF gl-acct.acc-type = 2 OR gl-acct.acc-type = 5 THEN 
        s-list.lflag  = (fibu = gl-acc1.fibukonto). 
      ELSE s-list.lflag  = ((lbezeich = l-artikel.bezeich) AND delta LE 0.01). 
  END. 
  
END. 
