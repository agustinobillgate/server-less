
DEFINE TEMP-TABLE temp-bjournal LIKE billjournal
    FIELD item-name     AS CHAR INITIAL "".

DEF INPUT  PARAMETER bill-no    AS INTEGER.
DEF INPUT  PARAMETER billdate   AS DATE.
DEF INPUT  PARAMETER artNo      AS INTEGER.
DEF INPUT  PARAMETER amount     AS DECIMAL.
DEF INPUT  PARAMETER systdate   AS DATE.
DEF INPUT  PARAMETER systtime   AS INTEGER.
DEF OUTPUT PARAMETER created    AS LOGICAL INITIAL NO  NO-UNDO.
DEF OUTPUT PARAMETER found      AS LOGICAL INITIAL NO  NO-UNDO.
DEF OUTPUT PARAMETER err        AS INT INIT 0.
DEF OUTPUT PARAMETER TABLE FOR temp-bjournal.

DEFINE VARIABLE currDate    AS DATE NO-UNDO.
DEFINE VARIABLE ci-dt       AS DATE INITIAL ?.
DEFINE VARIABLE co-dt       AS DATE INITIAL ?.

RUN htpdate.p(110, OUTPUT currDate).

FIND FIRST bill WHERE bill.rechnr = bill-no /* AND bill.flag = 0 */ NO-LOCK NO-ERROR.
IF AVAILABLE bill AND billdate = ? THEN
DO:
  err = 1.
  IF bill.resnr GT 0 AND bill.reslinnr GT 0 THEN
  DO:
    FIND FIRST res-line WHERE res-line.resnr = bill.resnr
        AND res-line.reslinnr = bill.parent-nr NO-LOCK NO-ERROR.
    IF AVAILABLE res-line THEN
    ASSIGN  
      ci-dt = res-line.ankunft
      co-dt = res-line.abreise
    .
  END.
/* SY 02/10/2014: give more accuracy 
  ELSE IF bill.datum NE ? THEN 
  ASSIGN
    ci-dt = bill.datum - 30
    co-dt = bill.datum + 30
  .
  ELSE IF bill.datum = ? THEN
*/
  ELSE
  DO:
  DEF VAR fr-date AS DATE NO-UNDO INIT ?.
  DEF VAR to-date AS DATE NO-UNDO INIT ?.
    FIND FIRST billjournal WHERE billjournal.rechnr = bill.rechnr
         USE-INDEX billjref_ix NO-LOCK NO-ERROR.
    IF AVAILABLE billjournal THEN
    ASSIGN
        fr-date = billjournal.bill-datum
        to-date = billjournal.bill-datum
        ci-dt   = fr-date - 30
        co-dt   = to-date + 30
    .
    FIND LAST billjournal WHERE billjournal.rechnr = bill.rechnr
         USE-INDEX billjref_ix NO-LOCK NO-ERROR.
    IF AVAILABLE billjournal THEN
    DO:
      IF fr-date GT billjournal.bill-datum THEN 
        ASSIGN 
          fr-date = billjournal.bill-datum
          ci-dt   = fr-date - 30
        .
      IF to-date LT billjournal.bill-datum THEN 
        ASSIGN 
          to-date = billjournal.bill-datum
          co-dt   = to-date + 30
        .
    END.
  END.

  err = 2.
  IF ci-dt NE ? THEN
  FOR EACH billjournal WHERE SUBSTR(billjournal.bezeich, 1, 1) EQ "*"
    /*AND billjournal.bill-datum GE ci-dt 
    AND billjournal.bill-datum LE co-dt*/
    AND anzahl = 0 NO-LOCK :
    /*err = INT(REPLACE(ENTRY(1, billjournal.bezeich, ";"), "*", "")).*/
    IF INT(REPLACE(ENTRY(1, billjournal.bezeich, ";"), "*", "")) EQ bill-no THEN 
    DO: err = 4.
        CREATE temp-bjournal.
        BUFFER-COPY billjournal TO temp-bjournal.
        
        FIND FIRST artikel WHERE artikel.artnr = billjournal.artnr
            AND artikel.depart = billjournal.depart NO-LOCK NO-ERROR.
        IF AVAILABLE artikel THEN 
            ASSIGN temp-bjournal.item-name = artikel.bezeich.
        ELSE temp-bjournal.item-name = billjournal.bezeich.
        created = YES.
    END.
  END.
  
END.
ELSE IF AVAILABLE bill AND billdate NE ? THEN 
REPEAT:    
    RUN transdetail.
    IF NOT found THEN LEAVE.
END.

PROCEDURE transdetail:
  found = NO.
  FOR EACH billjournal WHERE SUBSTR(bezeich, 1, 1) EQ "*"
    AND billjournal.bill-datum = billdate
    AND billjournal.artnr = artNo
    /*MT 12/02/13
    AND billjournal.departement = deptNo
    */
    AND billjournal.anzahl = 0 
    AND billjournal.betrag = amount
    AND ((billjournal.sysdate EQ systdate AND billjournal.zeit GT systtime)
      OR (billjournal.sysdate GT systdate)) NO-LOCK
    BY billjournal.sysdate 
    BY billjournal.zeit:

    IF INT(REPLACE(ENTRY(1, billjournal.bezeich, ";"), "*", "")) EQ bill-no THEN 
    DO: err = 5.
        CREATE temp-bjournal.
        BUFFER-COPY billjournal TO temp-bjournal.        
        ASSIGN 
            temp-bjournal.item-name = billjournal.bezeich
            systdate                = billjournal.sysdate
            systtime                = billjournal.zeit
            bill-no                 = billjournal.rechnr
            created                 = YES
            found                   = YES
        .
        LEAVE.
    END.
  END.
END.
