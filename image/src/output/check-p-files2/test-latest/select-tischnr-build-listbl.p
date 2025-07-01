DEFINE TEMP-TABLE t-list 
  FIELD tischnr     LIKE tisch.tischnr 
  FIELD bezeich     LIKE tisch.bezeich FORMAT "x(16)" 
  FIELD normalbeleg LIKE tisch.normalbeleg 
  FIELD name        LIKE kellner.kellnername FORMAT "x(12)" INITIAL "" 
                    COLUMN-LABEL "Served by" 
  FIELD occupied    AS LOGICAL FORMAT "Yes/No" LABEL "OCC" INITIAL NO 
  FIELD belegung    LIKE h-bill.belegung COLUMN-LABEL "Pax" 
  FIELD balance     LIKE h-bill.saldo. 

DEF INPUT  PARAMETER dept    AS INT.
DEF INPUT  PARAMETER nr      AS INT.
DEF OUTPUT PARAMETER TABLE FOR t-list.

DEFINE VARIABLE masterkey AS LOGICAL INITIAL NO. 
RUN build-list.

PROCEDURE build-list: 
  FIND FIRST kellner WHERE kellner.departement = dept 
    AND kellner.kellner-nr = nr NO-LOCK NO-ERROR. 
  IF AVAILABLE kellner THEN masterkey = kellner.masterkey. 
  DO: 
    IF masterkey THEN 
    DO: 
      FOR EACH tisch WHERE tisch.departement = dept NO-LOCK BY tisch.tischnr: 
        create t-list. 
        t-list.tischnr = tisch.tischnr. 
        t-list.bezeich = tisch.bezeich. 
        t-list.normalbeleg = tisch.normalbeleg. 
        FIND FIRST h-bill WHERE h-bill.departement = dept 
          AND h-bill.tischnr = tisch.tischnr AND h-bill.flag = 0 
          NO-LOCK NO-ERROR. 
        IF AVAILABLE h-bill THEN 
        DO: 
          FIND FIRST kellner WHERE kellner.kellner-nr = h-bill.kellner-nr 
            AND kellner.departement = dept NO-LOCK NO-ERROR. 
          t-list.occupied = YES. 
          t-list.belegung = h-bill.belegung. 
          IF AVAILABLE kellner THEN t-list.name = kellner.kellnername. 
          t-list.balance = h-bill.saldo. 
        END. 
      END. 
    END. 
    ELSE DO: 
      FOR EACH tisch WHERE tisch.departement = dept 
        AND (tisch.kellner-nr = 0 OR tisch.kellner-nr = nr) NO-LOCK 
        BY tisch.tischnr: 
        create t-list. 
        t-list.tischnr = tisch.tischnr. 
        t-list.bezeich = tisch.bezeich. 
        t-list.normalbeleg = tisch.normalbeleg. 
        FIND FIRST h-bill WHERE h-bill.departement = dept 
          AND h-bill.tischnr = tisch.tischnr AND h-bill.flag = 0 
          NO-LOCK NO-ERROR. 
        IF AVAILABLE h-bill THEN 
        DO: 
          FIND FIRST kellner WHERE kellner.kellner-nr = h-bill.kellner-nr 
            AND kellner.departement = dept NO-LOCK NO-ERROR. 
          t-list.occupied = YES. 
          t-list.belegung = h-bill.belegung. 
          IF AVAILABLE kellner THEN t-list.name = kellner.kellnername. 
          t-list.balance = h-bill.saldo. 
        END. 
      END. 
    END. 
  END. 
  /*MTOPEN QUERY q1 FOR EACH t-list NO-LOCK. 
  IF AVAILABLE t-list THEN tischnr = t-list.tischnr. */
END. 
