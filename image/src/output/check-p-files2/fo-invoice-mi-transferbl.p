
DEF INPUT-OUTPUT PARAMETER room         AS CHAR.
DEF INPUT  PARAMETER case-type          AS INT.
DEF INPUT  PARAMETER bil-recid          AS INT.
DEF INPUT  PARAMETER user-init          AS CHAR.
DEF OUTPUT PARAMETER resline-resnr      AS INT.
DEF OUTPUT PARAMETER resline-reslinnr   AS INT.
DEF OUTPUT PARAMETER run-create-logfile AS LOGICAL INIT NO.

DEFINE BUFFER resline FOR res-line. 
DEFINE VARIABLE memoRmNo AS CHAR INITIAL "".

FIND FIRST bill WHERE RECID(bill) = bil-recid NO-LOCK.

IF case-type = 1 THEN
DO:
    FIND FIRST resline WHERE resline.resnr = bill.resnr 
    AND resline.reslinnr = bill.reslinnr NO-LOCK.
 
    room = ENTRY(1, resline.memozinr, ";").
END.
ELSE
DO:
    FIND FIRST resline WHERE resline.resnr = bill.resnr 
    AND resline.reslinnr = bill.reslinnr NO-LOCK.

    DO TRANSACTION: 
      FIND CURRENT resline EXCLUSIVE-LOCK. 
      IF resline.memozinr EQ ? THEN resline.memozinr = ";;".
      FIND CURRENT resline NO-LOCK.

      IF room EQ ? THEN room = "".
      memoRmNo = ENTRY(2, resline.memozinr, ";").
      IF memoRmNo EQ ? THEN memoRmNo = "".
      
      FIND CURRENT resline EXCLUSIVE-LOCK. 
      ASSIGN 
        resline.memozinr = room + ";" + memoRmNo + ";"
        resline.memodatum = today 
        resline.memousercode = user-init NO-ERROR. 
      FIND CURRENT resline NO-LOCK.
    END.
    IF resline.resstatus NE 12 THEN 
        ASSIGN
        run-create-logfile = YES
        resline-resnr = resline.resnr
        resline-reslinnr = resline.reslinnr.
    /*MT
    IF resline.resstatus NE 12 THEN 
        RUN create-logfile(resline.resnr, resline.reslinnr, room). 
    RUN fill-rescomment (NO). 
    */
END.

