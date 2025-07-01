
DEF TEMP-TABLE s-list 
    FIELD rgdatum      LIKE l-kredit.rgdatum 
    FIELD artnr        LIKE artikel.artnr FORMAT ">>>>" 
    FIELD bezeich      LIKE artikel.bezeich 
    FIELD saldo        LIKE l-kredit.saldo       FORMAT "->>>,>>>,>>9.99" LABEL "Amount" 
    FIELD NAME         LIKE l-kredit.NAME     COLUMN-LABEL "Document No" 
    FIELD lscheinnr    LIKE l-kredit.lscheinnr   COLUMN-LABEL "Delivery Note" 
    FIELD fibu         LIKE gl-acct.fibukonto 
    FIELD lief-nr      LIKE l-kredit.lief-nr 
    FIELD lflag        AS LOGICAL INITIAL NO. 

DEF TEMP-TABLE t-gl-acct LIKE gl-acct.

DEF INPUT PARAMETER pvILanguage    AS INTEGER      NO-UNDO.
DEF INPUT  PARAMETER fibu AS CHAR.
DEF INPUT  PARAMETER bemerk AS CHAR.
DEF OUTPUT PARAMETER receive-date AS DATE.
DEF OUTPUT PARAMETER TABLE FOR t-gl-acct.
DEF OUTPUT PARAMETER TABLE FOR s-list.

{SupertransBL.i} 
DEF VAR lvCAREA AS CHAR INITIAL "gl-detailAP".

FIND FIRST gl-acct WHERE gl-acct.fibukonto = fibu NO-LOCK.
CREATE t-gl-acct.
BUFFER-COPY gl-acct TO t-gl-acct.

RUN disp-it.


PROCEDURE disp-it: 
DEF VAR counter         AS INTEGER NO-UNDO. 
DEF VAR zahlkonto       AS INTEGER NO-UNDO. 
DEF VAR lief-nr         AS INTEGER NO-UNDO. 
DEF VAR saldo           AS DECIMAL NO-UNDO. 
DEF VAR docu-nr         AS CHAR    NO-UNDO. 
DEF VAR lscheinnr       AS CHAR    NO-UNDO. 
DEF VAR bezeich         AS CHAR    NO-UNDO INIT "". 
DEF VAR ltype           AS INTEGER NO-UNDO. 
 
  ltype = INTEGER(SUBSTR(ENTRY(2, bemerk, ";"),3,1)). 
  IF ltype = 2 THEN   /* AP Payment */ 
  DO: 
    counter   =  INTEGER(ENTRY(3, bemerk, ";")). 
    lief-nr   =  INTEGER(ENTRY(4, bemerk, ";")). 
    zahlkonto =  INTEGER(ENTRY(5, bemerk, ";")). 
    saldo     =  DECIMAL(ENTRY(6, bemerk, ";")) / 100. 
  END. 
  ELSE 
  DO: 
    counter   =  INTEGER(ENTRY(3, bemerk, ";")). 
    lief-nr   =  INTEGER(ENTRY(4, bemerk, ";")). 
  END. 
 
  FOR EACH l-kredit WHERE l-kredit.counter = counter NO-LOCK 
      BY l-kredit.zahlkonto: 
 
      IF l-kredit.zahlkonto = 0 THEN receive-date = l-kredit.rgdatum. 
 
      CREATE s-list. 
      BUFFER-COPY l-kredit TO s-list. 
 
      IF l-kredit.zahlkonto > 0 THEN 
      DO: 
          FIND FIRST artikel WHERE artikel.artnr = l-kredit.zahlkonto 
              AND artikel.departement = 0 NO-LOCK. 
          ASSIGN 
              s-list.artnr = artikel.artnr 
              s-list.bezeich = artikel.bezeich. 
      END. 
      ELSE s-list.bezeich = translateExtended ("A/P Trade",lvCAREA,""). 
 
      IF ltype = 2 THEN s-list.lflag = (s-list.saldo = saldo). 
      ELSE s-list.lflag = (l-kredit.zahlkonto = 0). 
  END.
END. 
