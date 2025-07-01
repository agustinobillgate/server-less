DEFINE TEMP-TABLE mainres-list 
  FIELD resnr      AS INTEGER FORMAT ">>>>>>9"             LABEL "ResNo" 
  FIELD zimanz     AS INTEGER FORMAT ">>9"                 LABEL "Qty" 
  FIELD ankunft    AS DATE    INITIAL 01/01/2099           LABEL "Arrival" 
  FIELD abreise    AS DATE    INITIAL 01/01/1998           LABEL "Depart" 
  FIELD segm       AS INTEGER FORMAT ">>9"                 LABEL "Seg" 
  FIELD deposit    AS DECIMAL FORMAT "->>>,>>>,>>>,>>9.99" LABEL "Deposit" 
  FIELD until      AS DATE                                 LABEL "DueDate" 
  FIELD paid       AS DECIMAL FORMAT "->>>,>>>,>>>,>>9.99" LABEL "Paid Amount" 
  FIELD id1        AS CHAR    FORMAT "x(3)"                LABEL "ID" 
  FIELD id2        AS CHAR    FORMAT "x(3)"                LABEL "ID" 
  FIELD id2-date   AS DATE                                 LABEL "ChgDate" 
  FIELD groupname  AS CHAR    FORMAT "x(29)"               LABEL "Group Name" 
  FIELD grpflag    AS LOGICAL 
  FIELD bemerk     AS CHAR    FORMAT "x(32)" 
  FIELD voucher    AS CHAR    FORMAT "x(20)"               LABEL "Voucher No"
  FIELD vesrdepot2 AS CHAR
  FIELD arrival    AS LOGICAL INITIAL NO 
  FIELD resident   AS LOGICAL INITIAL NO 
  FIELD arr-today  AS LOGICAL INITIAL NO
.

DEFINE INPUT-OUTPUT PARAMETER TABLE FOR mainres-list.
DEFINE VARIABLE ci-date AS DATE NO-UNDO.

RUN htpdate.p(87, OUTPUT ci-date).
FIND FIRST mainres-list.
RUN update-mainres.

PROCEDURE update-mainres: 
  ASSIGN
    mainres-list.ankunft   = 01/01/2099
    mainres-list.abreise   = 01/01/1998 
    mainres-list.zimanz    = 0 
    mainres-list.arrival   = NO 
    mainres-list.arr-today = NO 
    mainres-list.resident  = NO
  . 
  FOR EACH res-line WHERE res-line.resnr = mainres-list.resnr 
    AND resstatus NE 9 AND resstatus NE 10 AND resstatus NE 12 NO-LOCK: 
    IF res-line.resstatus LE 6 THEN
      mainres-list.zimanz   = mainres-list.zimanz + res-line.zimmeranz. 
    IF mainres-list.ankunft > res-line.ankunft THEN 
       mainres-list.ankunft = res-line.ankunft. 
    IF mainres-list.abreise < res-line.abreise THEN 
       mainres-list.abreise = res-line.abreise. 
    IF (resstatus LE 5 OR resstatus = 11) THEN 
       mainres-list.arrival = YES. 
    IF mainres-list.arrival = YES AND res-line.ankunft = ci-date THEN 
       mainres-list.arr-today = YES. 
    IF res-line.resstatus = 6 OR res-line.resstatus = 13 THEN 
       mainres-list.resident = YES. 
  END. 
END. 
