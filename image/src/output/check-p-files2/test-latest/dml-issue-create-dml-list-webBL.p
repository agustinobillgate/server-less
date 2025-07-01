DEFINE TEMP-TABLE dml-list 
  FIELD bezeich     AS CHAR FORMAT "x(36)" COLUMN-LABEL "Description"
  FIELD anzahl      LIKE dml-art.anzahl
  FIELD geliefert   LIKE dml-art.geliefert
  FIELD einzelpreis LIKE dml-art.einzelpreis FORMAT ">,>>>,>>>,>>9.99"
  FIELD artnr       LIKE l-artikel.artnr COLUMN-LABEL "ArtNo"
  FIELD departement LIKE dml-artdep.departement
  FIELD lief-nr     AS INTEGER
  FIELD supplier    AS CHAR FORMAT "x(24)" COLUMN-LABEL "Supplier"
  FIELD content		AS INTEGER /*Web enhancement*/
  FIELD dml-code    AS CHAR FORMAT "x(32)"
.
DEF TEMP-TABLE t-l-artikel LIKE l-artikel.

DEF INPUT  PARAMETER curr-dept AS INT.
DEF INPUT  PARAMETER billdate  AS DATE.
DEF OUTPUT PARAMETER TABLE FOR dml-list.
DEF OUTPUT PARAMETER TABLE FOR t-l-artikel.

RUN create-dml-list.
FOR EACH dml-list:
    /* FDL Comment
    FIND FIRST l-artikel WHERE l-artikel.artnr = dml-list.artnr NO-LOCK.
    CREATE t-l-artikel.
    BUFFER-COPY l-artikel TO t-l-artikel.
    */
    /*FDL Ticket C3EDE0*/
    FIND FIRST l-artikel WHERE l-artikel.artnr EQ dml-list.artnr NO-LOCK NO-ERROR.
    IF AVAILABLE l-artikel THEN
    DO:
        FIND FIRST t-l-artikel WHERE t-l-artikel.artnr EQ l-artikel.artnr NO-LOCK NO-ERROR.
        IF NOT AVAILABLE t-l-artikel THEN
        DO:
            CREATE t-l-artikel.
            BUFFER-COPY l-artikel TO t-l-artikel.
        END.        
    END.
END.

PROCEDURE create-dml-list:
DEF VAR liefNo AS INTEGER NO-UNDO.
 

  FOR EACH dml-list:
    DELETE dml-list.
  END.
  IF curr-dept = 0 THEN DO:
      FOR EACH dml-art WHERE dml-art.datum = billdate 
         AND dml-art.anzahl GT 0
         AND dml-art.chginit MATCHES "*!*" NO-LOCK:
         FIND FIRST l-artikel WHERE l-artikel.artnr = dml-art.artnr NO-LOCK.
         CREATE dml-list.
         BUFFER-COPY dml-art TO dml-list.
         ASSIGN
           dml-list.bezeich = l-artikel.bezeich
           dml-list.content = l-artikel.lief-einheit
           dml-list.dml-code = ENTRY(2, dml-art.chginit, ";")
           liefNo = 0
           liefNo = INTEGER(ENTRY(2, dml-art.userinit, ";")) NO-ERROR.
         IF liefNo GT 0 THEN
         DO:
           FIND FIRST l-lieferant WHERE l-lieferant.lief-nr = liefNo
             NO-LOCK.
           ASSIGN
             dml-list.lief-nr  = liefNo
             dml-list.supplier = l-lieferant.firma. 
         END.
        END.
  END.
  ELSE DO:
      FOR EACH dml-artdep WHERE dml-artdep.datum = billdate 
        AND dml-artdep.departement = curr-dept 
        AND dml-artdep.anzahl GT 0 
        AND dml-artdep.chginit MATCHES "*!*" NO-LOCK:
        FIND FIRST l-artikel WHERE l-artikel.artnr = dml-artdep.artnr NO-LOCK.
        CREATE dml-list.
        BUFFER-COPY dml-artdep TO dml-list.
        ASSIGN
          dml-list.bezeich = l-artikel.bezeich
          dml-list.content = l-artikel.lief-einheit
          dml-list.dml-code = ENTRY(2, dml-artdep.chginit, ";")
          liefNo = 0
          liefNo = INTEGER(ENTRY(2, dml-artdep.userinit, ";")) NO-ERROR.
        IF liefNo GT 0 THEN
        DO:
          FIND FIRST l-lieferant WHERE l-lieferant.lief-nr = liefNo
            NO-LOCK.
          ASSIGN
            dml-list.lief-nr  = liefNo
            dml-list.supplier = l-lieferant.firma. 
        END.
      END.
    
      FIND FIRST reslin-queasy WHERE reslin-queasy.KEY EQ "DML"
            AND reslin-queasy.date1 EQ billdate
            AND INT(ENTRY(2,reslin-queasy.char1,";")) EQ curr-dept 
            AND reslin-queasy.deci2 GT 0
            AND reslin-queasy.char3 MATCHES "*!*" NO-LOCK NO-ERROR.
      DO WHILE AVAILABLE reslin-queasy:
          FIND FIRST l-artikel WHERE l-artikel.artnr = INT(ENTRY(1,reslin-queasy.char1,";")) NO-LOCK.
          CREATE dml-list.
          ASSIGN dml-list.bezeich       = l-artikel.bezeich
                 dml-list.content       = l-artikel.lief-einheit
                 dml-list.anzahl        = reslin-queasy.deci2
                 dml-list.einzelpreis   = reslin-queasy.deci1
                 dml-list.artnr         = INTEGER(ENTRY(1, reslin-queasy.char1, ";"))
                 dml-list.departement   = INTEGER(ENTRY(2, reslin-queasy.char1, ";"))
                 dml-list.dml-code      = ENTRY(2, reslin-queasy.char3, ";")
                 dml-list.geliefert     = reslin-queasy.deci3
                 liefNo                 = 0
                 liefNo                 = INTEGER(ENTRY(2, reslin-queasy.char2, ";")) NO-ERROR.
         IF liefNo GT 0 THEN
         DO:
            FIND FIRST l-lieferant WHERE l-lieferant.lief-nr = liefNo NO-LOCK.
            ASSIGN
                dml-list.lief-nr  = liefNo
                dml-list.supplier = l-lieferant.firma. 
         END.

          FIND NEXT reslin-queasy WHERE reslin-queasy.KEY EQ "DML"
              AND reslin-queasy.date1 EQ billdate
              AND INT(ENTRY(2,reslin-queasy.char1,";")) EQ curr-dept 
              AND reslin-queasy.deci2 GT 0 
              AND reslin-queasy.char3 MATCHES "*!*" NO-LOCK NO-ERROR.
      END.
  END.
END.
