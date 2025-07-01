DEF TEMP-TABLE t-parameters
    FIELD varname LIKE parameters.varname
    FIELD vstring LIKE parameters.vstring.

DEF TEMP-TABLE t-l-orderhdr LIKE l-orderhdr
    FIELD rec-id AS INT.

DEF TEMP-TABLE t-l-artikel
    FIELD rec-id        AS INT
    FIELD artnr         LIKE l-artikel.artnr
    FIELD bezeich       LIKE l-artikel.bezeich
    FIELD betriebsnr    LIKE l-artikel.betriebsnr
    FIELD traubensort   LIKE l-artikel.traubensort
    FIELD lief-einheit  LIKE l-artikel.lief-einheit
    FIELD jahrgang      LIKE l-artikel.jahrgang
    FIELD inhalt        LIKE l-artikel.inhalt
    FIELD masseinheit   LIKE l-artikel.masseinheit
    FIELD zwkum         LIKE l-artikel.zwkum
    FIELD soh           AS DECIMAL. /*545FBD gerald*/
    .

DEF TEMP-TABLE s-list LIKE l-order
    FIELD s-recid AS INTEGER.

DEF INPUT-OUTPUT PARAMETER docu-nr          AS CHAR.
DEF INPUT  PARAMETER tp-bediener-user-group AS INT.
DEF INPUT  PARAMETER tp-bediener-username   AS CHAR.
DEF INPUT  PARAMETER dml-flag               AS LOGICAL.
DEF INPUT  PARAMETER dml-grp                AS INT.
DEF INPUT  PARAMETER dml-datum              AS DATE.
DEF INPUT  PARAMETER cost-acct              LIKE gl-acct.fibukonto.

DEF OUTPUT PARAMETER billdate               AS DATE.
DEF OUTPUT PARAMETER eng-dept               AS INT INIT 0 NO-UNDO.
DEF OUTPUT PARAMETER pos                    AS INT.
DEF OUTPUT PARAMETER dml-created            AS LOGICAL INIT NO.
DEF OUTPUT PARAMETER p-370                  AS LOGICAL INIT NO.
DEF OUTPUT PARAMETER TABLE FOR t-l-orderhdr.
DEF OUTPUT PARAMETER TABLE FOR s-list.
DEF OUTPUT PARAMETER TABLE FOR t-l-artikel.
DEF OUTPUT PARAMETER TABLE FOR t-parameters.

FIND FIRST htparam WHERE paramnr = 110 NO-LOCK. 
billdate = htparam.fdate. 
 
FIND FIRST htparam WHERE htparam.paramnr = 1060 NO-LOCK.
IF htparam.finteger NE 0 AND tp-bediener-user-group = htparam.finteger THEN
DO:
  FIND FIRST htparam WHERE htparam.paramnr = 1062 NO-LOCK.
  eng-dept = htparam.finteger.
END.

FIND FIRST htparam WHERE htparam.paramnr = 370 NO-LOCK NO-ERROR.
IF AVAILABLE htparam THEN DO:
    ASSIGN p-370 = htparam.flogical.
END.

RUN new-pr-number.


DO TRANSACTION:
  CREATE l-orderhdr.
  ASSIGN
    l-orderhdr.betriebsnr       = 9
    l-orderhdr.bestelldatum     = billdate 
    l-orderhdr.lieferdatum      = billdate + 1 
    l-orderhdr.besteller        = tp-bediener-username 
    l-orderhdr.gedruckt         = ?
    l-orderhdr.angebot-lief[1]  = eng-dept
    l-orderhdr.lief-fax[2]      = " ; ; ; "
  .
  l-orderhdr.docu-nr = docu-nr. 

  FIND CURRENT l-orderhdr.
  CREATE t-l-orderhdr.
  BUFFER-COPY l-orderhdr TO t-l-orderhdr.
  ASSIGN t-l-orderhdr.rec-id = RECID(l-orderhdr).
  /*MTASSIGN
    t-l-orderhdr.betriebsnr       = 9
    t-l-orderhdr.bestelldatum     = billdate 
    t-l-orderhdr.lieferdatum      = billdate + 1 
    t-l-orderhdr.besteller        = tp-bediener-username 
    t-l-orderhdr.gedruckt         = ?
    t-l-orderhdr.angebot-lief[1]  = eng-dept
    t-l-orderhdr.lief-fax[2]      = " ; ; ; "
  .
  t-l-orderhdr.docu-nr = docu-nr. 
  t-l-orderhdr.rec-id = RECID(l-orderhdr).*/
END.

IF dml-flag THEN RUN create-dml-pr. 

FOR EACH l-artikel USE-INDEX artnr_ix NO-LOCK:
    CREATE t-l-artikel.
    ASSIGN
    t-l-artikel.rec-id        = RECID(l-artikel)
    t-l-artikel.artnr         = l-artikel.artnr
    t-l-artikel.bezeich       = l-artikel.bezeich
    t-l-artikel.betriebsnr    = l-artikel.betriebsnr
    t-l-artikel.traubensort   = l-artikel.traubensort
    t-l-artikel.lief-einheit  = l-artikel.lief-einheit
    t-l-artikel.jahrgang      = l-artikel.jahrgang
    t-l-artikel.inhalt        = l-artikel.inhalt
    t-l-artikel.masseinheit   = l-artikel.masseinheit
    t-l-artikel.zwkum         = l-artikel.zwkum.

    /*545FBD gerald*/
    FIND FIRST l-bestand WHERE l-bestand.artnr = l-artikel.artnr 
        AND l-bestand.lager-nr = 0 NO-LOCK NO-ERROR.
    IF AVAILABLE l-bestand THEN
    DO:
        ASSIGN t-l-artikel.soh = l-bestand.anz-anf-best + l-bestand.anz-eingang - l-bestand.anz-ausgang.
    END.
END.

FOR EACH parameters WHERE parameters.progname = "CostCenter" 
    AND parameters.section = "Name" NO-LOCK:
    CREATE t-parameters.
    ASSIGN
    t-parameters.varname = parameters.varname
    t-parameters.vstring = parameters.vstring.
END.


PROCEDURE new-pr-number: 
DEFINE buffer l-orderhdr1 FOR l-orderhdr. 
DEFINE VARIABLE s AS CHAR. 
DEFINE VARIABLE i AS INTEGER INITIAL 1. 
  s = "R" + SUBSTR(STRING(year(billdate)),3,2) + STRING(month(billdate), "99") 
     + STRING(day(billdate), "99"). 
/* 
  FIND FIRST counters WHERE counters.counter-no = 9 EXCLUSIVE-LOCK. 
  counters.counter = counters.counter + 1. 
  i = counters.counter. 
  FIND CURRENT counter NO-LOCK. 
*/ 
  FOR EACH l-orderhdr1 WHERE l-orderhdr1.bestelldatum = billdate 
    NO-LOCK BY l-orderhdr1.docu-nr DESCENDING: 
    i = INTEGER(SUBSTR(l-orderhdr1.docu-nr,8,3)). 
    i = i + 1. 
    docu-nr = s + STRING(i, "999"). 
    RETURN. 
  END. 
  docu-nr = s + STRING(i, "999"). 
END.


PROCEDURE create-dml-pr: 
  IF pos = 0 THEN 
  DO: 
    CREATE s-list. 
    ASSIGN 
      s-list.docu-nr = docu-nr 
      s-list.pos = 0 
      s-list.bestelldatum = l-orderhdr.bestelldatum 
      s-list.op-art = 1. 
  END. 
  IF dml-grp = 0 THEN 
  DO:
    FOR EACH dml-art WHERE dml-art.datum = dml-datum 
      AND dml-art.anzahl NE 0 NO-LOCK, 
      FIRST l-artikel WHERE l-artikel.artnr = dml-art.artnr NO-LOCK 
      BY l-artikel.bezeich: 
      pos = pos + 1. 
      CREATE s-list. 
      ASSIGN 
        s-list.docu-nr = docu-nr 
        s-list.artnr = l-artikel.artnr 
        s-list.anzahl = dml-art.anzahl 
        s-list.lieferdatum = dml-art.datum 
        s-list.pos = pos 
        s-list.bestelldatum = l-orderhdr.bestelldatum 
        s-list.op-art = 1 
        s-list.lief-fax[1] = tp-bediener-username 
/*    RESERVE: lief-fax[2] FOR P/O docu-nr !!!  */ 
        s-list.lief-fax[3] = l-artikel.traubensort /* delivery Unit */ 
        s-list.flag = YES. 
      IF l-artikel.lief-einheit NE 0 THEN 
         s-list.txtnr = l-artikel.lief-einheit. 
      IF INTEGER(cost-acct) NE 0 THEN s-list.stornogrund = cost-acct. 
    END.
  END.
  ELSE
  DO:
    FOR EACH dml-art WHERE dml-art.datum = dml-datum NO-LOCK, 
      FIRST l-artikel WHERE l-artikel.artnr = dml-art.artnr 
        AND l-artikel.zwkum = dml-grp NO-LOCK 
      BY l-artikel.bezeich:
      pos = pos + 1.
      CREATE s-list.
      ASSIGN 
        s-list.docu-nr = docu-nr 
        s-list.artnr = l-artikel.artnr 
        s-list.anzahl = dml-art.anzahl 
        s-list.lieferdatum = dml-art.datum 
        s-list.stornogrund = cost-acct 
        s-list.pos = pos 
        s-list.bestelldatum = l-orderhdr.bestelldatum 
        s-list.op-art = 1 
        s-list.lief-fax[1] = tp-bediener-username 
/*    RESERVE: lief-fax[2] FOR P/O docu-nr !!!  */ 
        s-list.lief-fax[3] = l-artikel.traubensort /* delivery Unit */ 
        s-list.flag = YES.
      IF l-artikel.lief-einheit NE 0 THEN
         s-list.txtnr = l-artikel.lief-einheit.
      IF INTEGER(cost-acct) NE 0 THEN s-list.stornogrund = cost-acct.
    END.
  END.
  
  ASSIGN
    dml-created = YES
    l-orderhdr.lieferdatum = dml-datum.
END.
