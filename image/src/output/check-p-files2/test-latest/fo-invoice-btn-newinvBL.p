
DEF INPUT  PARAMETER bil-recid      AS INT.
DEF INPUT  PARAMETER bill-anzahl    AS INT.

FIND FIRST bill WHERE RECID(bill) = bil-recid NO-LOCK.
IF NOT AVAILABLE bill THEN RETURN. /*FT serverless*/

FIND FIRST res-line WHERE res-line.resnr = bill.resnr 
    AND res-line.reslinnr = bill.reslinnr NO-LOCK. 
RUN create-newbillbl.p(res-line.resnr, res-line.reslinnr, bill.parent-nr, 
                       bill-anzahl, OUTPUT bil-recid).
