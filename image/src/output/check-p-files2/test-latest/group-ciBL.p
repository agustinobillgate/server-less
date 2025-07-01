DEFINE TEMP-TABLE mainres-list 
    FIELD resnr         AS INTEGER FORMAT ">>>,>>>,>>9"     LABEL "ResNo" 
    FIELD gastnr        AS INTEGER 
    FIELD name          AS CHAR    FORMAT "x(32)"           LABEL "Reservation Name" 
    FIELD zimanz        AS INTEGER FORMAT ">>9"             LABEL "Qty" 
    FIELD ci            AS INTEGER FORMAT ">>9"             LABEL "C/I" 
    FIELD co            AS INTEGER FORMAT ">>9"             LABEL "C/O" 
    FIELD arr           AS INTEGER FORMAT ">>9"             LABEL "Arr" 
    FIELD abreise       AS DATE    INITIAL 01/01/1998       LABEL "DepDate" 
    FIELD segm          AS INTEGER FORMAT ">>9"             LABEL "Seg" 
    FIELD deposit       AS DECIMAL FORMAT "->,>>>,>>>,>>9.99" LABEL "Deposit" 
    FIELD until         AS DATE                             LABEL "DueDate" 
    FIELD paid          AS DECIMAL FORMAT "->,>>>,>>>,>>9.99" LABEL "Paid Amount" 
    FIELD groupname     AS CHAR    FORMAT "x(29)"           LABEL "Group Name"
    FIELD res-address   AS CHAR INIT ""
    FIELD res-city      AS CHAR INIT ""
    FIELD res-bemerk    AS CHAR INIT ""
. 


DEFINE INPUT PARAMETER pvILanguage  AS INTEGER   NO-UNDO.
DEFINE INPUT  PARAMETER ci-date  AS DATE.
DEFINE OUTPUT PARAMETER TABLE FOR mainres-list.



{supertransBL.i} 
DEFINE VARIABLE lvCAREA AS CHARACTER INITIAL "group-ci". 
/************************  MAIN LOGIC   **************************/ 
RUN fill-mainres.

/************************  PROCEDURE   **************************/ 
PROCEDURE fill-mainres: 
  FOR EACH reservation WHERE reservation.activeflag = 0 
    AND reservation.grpflag = YES 
    AND reservation.name GT "" AND reservation.gastnr GT 0 
    NO-LOCK USE-INDEX group_ix BY reservation.name BY reservation.resnr: 
    FIND FIRST res-line WHERE res-line.resnr = reservation.resnr AND 
      (resstatus LE 5 OR resstatus = 11) AND 
       res-line.ankunft = ci-date NO-LOCK NO-ERROR. 
    IF AVAILABLE res-line THEN 
    DO: 
      FIND FIRST guest WHERE guest.gastnr = reservation.gastnr NO-LOCK.
      CREATE mainres-list. 
      ASSIGN
        mainres-list.gastnr       = reservation.gastnr
        mainres-list.name         = reservation.NAME
        mainres-list.resnr        = reservation.resnr 
        mainres-list.deposit      = reservation.depositgef
        mainres-list.until        = reservation.limitdate 
        mainres-list.paid         = reservation.depositbez + reservation.depositbez2 /* Malik serverless for case 472 : depositbez + depositbez2 -> reservation.depositbez + reservation.depositbez2 */
        mainres-list.segm         = reservation.segmentcode 
        mainres-list.groupname    = reservation.groupname
        mainres-list.res-address  = guest.adresse1
        mainres-list.res-city     = guest.wohnort + " " + guest.plz
      .
      RUN update-mainres. 
    END. 
  END. 
END. 

PROCEDURE update-mainres: 

  ASSIGN
    mainres-list.abreise    = 01/01/1998
    mainres-list.zimanz     = 0
    mainres-list.ci         = 0 
    mainres-list.co         = 0 
    mainres-list.arr        = 0
  . 
  FOR EACH res-line WHERE res-line.resnr = reservation.resnr AND 
    res-line.grpflag = YES AND res-line.ankunft = ci-date 
    USE-INDEX Grp_index NO-LOCK: 
    IF res-line.resstatus NE 9 AND res-line.resstatus NE 10 
      AND res-line.resstatus NE 12 THEN 
    DO: 
      mainres-list.zimanz = mainres-list.zimanz + res-line.zimmeranz. 
      IF res-line.active-flag = 1 THEN  mainres-list.ci = mainres-list.ci + 1. 
      IF res-line.active-flag = 2 THEN  mainres-list.co = mainres-list.co + 1. 
      IF res-line.active-flag = 0 AND res-line.ankunft = ci-date 
        THEN mainres-list.arr = mainres-list.arr + res-line.zimmeranz. 
      IF mainres-list.abreise < res-line.abreise THEN 
       mainres-list.abreise = res-line.abreise. 
    END. 
  END.
END. 

