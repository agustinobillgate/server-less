DEF TEMP-TABLE t-gl-acct LIKE gl-acct.

DEF TEMP-TABLE s-list 
    FIELD bill-datum   LIKE h-journal.bill-datum 
    FIELD departement  AS INTEGER FORMAT "99" LABEL "Dept" 
    FIELD artart       LIKE h-artikel.artart 
    FIELD rechnr       LIKE h-journal.rechnr 
    FIELD artnr        LIKE h-journal.artnr 
    FIELD bezeich      LIKE h-journal.bezeich 
    FIELD anzahl       LIKE h-journal.anzahl 
    FIELD betrag       LIKE h-journal.betrag FORMAT "->>,>>>,>>9.99" 
    FIELD cost         AS DECIMAL FORMAT "->>,>>>,>>9.99" LABEL "Cost" 
    FIELD tischnr      LIKE h-journal.tischnr 
    FIELD sysdate      LIKE h-journal.sysdate 
    FIELD zeit         LIKE h-journal.zeit 
    FIELD gname        AS CHAR FORMAT "x(32)" LABEL "Guest Name" 
    FIELD fibu         LIKE gl-acct.fibukonto 
    FIELD kellner-nr   LIKE h-journal.kellner-nr 
    FIELD waiter       AS CHAR FORMAT "x(24)" LABEL "Waiter Name". 


DEF INPUT PARAMETER fibu AS CHAR.
DEF INPUT PARAMETER bemerk    AS CHAR.
DEF INPUT PARAMETER from-date AS DATE. 
DEF OUTPUT PARAMETER TABLE FOR t-gl-acct.
DEF OUTPUT PARAMETER TABLE FOR s-list.

FIND FIRST gl-acct WHERE gl-acct.fibukonto = fibu NO-LOCK.
CREATE t-gl-acct.
BUFFER-COPY gl-acct TO t-gl-acct.

RUN disp-it.


PROCEDURE disp-it: 
DEF VAR dept            AS INTEGER NO-UNDO. 
DEF VAR billno          AS INTEGER NO-UNDO. 
DEF VAR cost            AS DECIMAL NO-UNDO INITIAL 0. 
DEF VAR rate            AS DECIMAL NO-UNDO INITIAL 1. 
DEF VAR double-currency AS LOGICAL NO-UNDO.

  dept = INTEGER(ENTRY(3, bemerk, ";")). 
  billno = INTEGER(ENTRY(4, bemerk, ";")). 
  
  FIND FIRST htparam WHERE paramnr = 240 NO-LOCK.  /* double currency flag */ 
  double-currency = htparam.flogical. 
  IF double-currency THEN 
  DO: 
    FIND FIRST htparam WHERE htparam.paramnr = 144 NO-LOCK. 
    IF htparam.fchar NE "" THEN 
    DO: 
      FIND FIRST waehrung WHERE waehrung.wabkurz = htparam.fchar 
        NO-LOCK NO-ERROR. 
      IF AVAILABLE waehrung THEN 
      DO: 
        FIND FIRST exrate WHERE exrate.artnr = waehrung.waehrungsnr 
          NO-LOCK NO-ERROR. 
        IF AVAILABLE exrate THEN rate = exrate.betrag. 
        ELSE rate = waehrung.ankauf / waehrung.einheit. 
      END. 
    END. 
  END. 
 
  FOR EACH h-journal WHERE h-journal.bill-datum EQ from-date 
      AND h-journal.departement = dept AND h-journal.rechnr = billno NO-LOCK, 
      FIRST h-artikel WHERE h-artikel.artnr = h-journal.artnr 
      AND h-artikel.departement = h-journal.departement NO-LOCK, 
      FIRST artikel WHERE (artikel.artart = 0 AND artikel.artnr 
      = h-artikel.artnrfront AND artikel.departement = h-artikel.departement) OR 
      (artikel.artnr = h-artikel.artnrfront AND artikel.departement = 0) NO-LOCK 
      BY h-journal.sysdate BY h-journal.zeit: 
 
      CREATE s-list. 
      BUFFER-COPY h-journal TO s-list. 
 
      FIND FIRST kellner WHERE kellner.kellner-nr = s-list.kellner 
          AND kellner.departement = dept NO-LOCK NO-ERROR. 
      IF AVAILABLE kellner THEN s-list.waiter = kellner.kellnername. 
 
      FIND FIRST h-bill WHERE h-bill.rechnr = s-list.rechnr 
         AND h-bill.departement = dept NO-LOCK NO-ERROR. 
      IF AVAILABLE h-bill THEN s-list.gname = h-bill.bilname. 
 
      ASSIGN 
        s-list.artart = artikel.artart 
        s-list.fibu = artikel.fibukonto. 
 
      IF s-list.artart = 0 THEN 
      DO: 
        FIND FIRST h-cost WHERE h-cost.artnr = s-list.artnr 
          AND h-cost.departement = dept AND h-cost.datum = from-date 
          AND h-cost.flag = 1 NO-LOCK NO-ERROR. 
        IF AVAILABLE h-cost AND h-cost.betrag NE 0 THEN 
          s-list.cost = s-list.anzahl * h-cost.betrag. 
        ELSE s-list.cost = h-journal.epreis * h-journal.anzahl 
            * h-artikel.prozent / 100. 
        cost = cost + s-list.cost. 
      END. 
  END. 
  FOR EACH s-list WHERE s-list.artart = 11: 
      IF s-list.betrag < 0 THEN s-list.cost = cost. 
      ELSE IF s-list.betrag > 0 THEN s-list.cost = - cost. 
  END. 
  OPEN QUERY q1 FOR EACH s-list. 
END. 
