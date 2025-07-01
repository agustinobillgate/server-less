DEFINE TEMP-TABLE dml-list 
  FIELD bezeich     AS CHAR FORMAT "x(36)" COLUMN-LABEL "Description"
  FIELD anzahl      LIKE dml-art.anzahl
  FIELD geliefert   LIKE dml-art.geliefert
  FIELD einzelpreis LIKE dml-art.einzelpreis FORMAT ">,>>>,>>>,>>9.99"
  FIELD artnr       LIKE l-artikel.artnr COLUMN-LABEL "ArtNo"
  FIELD departement LIKE dml-artdep.departement
  FIELD lief-nr     AS INTEGER
  FIELD supplier    AS CHAR FORMAT "x(24)" COLUMN-LABEL "Supplier"
.

DEF INPUT PARAMETER curr-dept AS INT.
DEF INPUT PARAMETER billdate AS DATE.
DEF OUTPUT PARAMETER TABLE FOR dml-list.

RUN create-dml-list.

PROCEDURE create-dml-list:
DEF VAR liefNo AS INTEGER NO-UNDO.
/*MT*/
DEF BUFFER buf-l-lieferant FOR l-lieferant.
  FOR EACH dml-list:
    DELETE dml-list.
  END.
  IF curr-dept = 0 THEN
  FOR EACH dml-art WHERE dml-art.datum = billdate 
    AND dml-art.anzahl GT 0 NO-LOCK:
    FIND FIRST l-artikel WHERE l-artikel.artnr = dml-art.artnr NO-LOCK.
    CREATE dml-list.
    BUFFER-COPY dml-art TO dml-list.
    ASSIGN
      dml-list.bezeich = l-artikel.bezeich
      liefNo = 0
      liefNo = INTEGER(ENTRY(2, dml-art.userinit, ";")) NO-ERROR.
    IF liefNo GT 0 THEN
    DO:
      FIND FIRST buf-l-lieferant WHERE buf-l-lieferant.lief-nr = liefNo
        NO-LOCK.
      ASSIGN
        dml-list.lief-nr  = liefNo
        dml-list.supplier = buf-l-lieferant.firma. 
    END.
  END.
  ELSE
  FOR EACH dml-artdep WHERE dml-artdep.datum = billdate 
    AND dml-artdep.departement = curr-dept 
    AND dml-artdep.anzahl GT 0 NO-LOCK:
    FIND FIRST l-artikel WHERE l-artikel.artnr = dml-artdep.artnr NO-LOCK.
    CREATE dml-list.
    BUFFER-COPY dml-artdep TO dml-list.
    ASSIGN
      dml-list.bezeich = l-artikel.bezeich
      liefNo = 0
      liefNo = INTEGER(ENTRY(2, dml-artdep.userinit, ";")) NO-ERROR.
    IF liefNo GT 0 THEN
    DO:
      FIND FIRST buf-l-lieferant WHERE buf-l-lieferant.lief-nr = liefNo
        NO-LOCK.
      ASSIGN
        dml-list.lief-nr  = liefNo
        dml-list.supplier = buf-l-lieferant.firma. 
    END.
  END.
END.
