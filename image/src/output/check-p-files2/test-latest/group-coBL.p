
/* Modified 27012020 pada for each by gerald agar group checkout bisa liat data tanggal history */

DEFINE TEMP-TABLE mainres-list 
  FIELD resnr       AS INTEGER FORMAT ">>>,>>>,>>9" LABEL "ResNo" 
  FIELD gastnr      AS INTEGER 
  FIELD name        AS CHAR    FORMAT "x(36)"       LABEL "Reservation Name" 
  FIELD zimanz      AS INTEGER FORMAT ">>9"         LABEL "RmQty" 
  FIELD arr         AS INTEGER FORMAT ">>9"         LABEL "Arr" 
  FIELD co          AS INTEGER FORMAT ">>9"         LABEL " C/O " 
  FIELD res         AS INTEGER FORMAT ">>9"         LABEL "Resident" 
  FIELD dep         AS INTEGER FORMAT ">>9"         LABEL "Depart" 
  FIELD groupname   AS CHAR    FORMAT "x(28)"       LABEL "Group Name"
  FIELD res-address AS CHAR
  FIELD res-city    AS CHAR
  FIELD res-bemerk  AS CHAR
. 

DEFINE INPUT PARAMETER case-type            AS INTEGER.
DEFINE INPUT PARAMETER ci-date              AS DATE.
DEFINE OUTPUT PARAMETER TABLE FOR mainres-list.


CASE case-type:
    WHEN 1 THEN
    DO:
        FOR EACH reservation WHERE reservation.grpflag = YES NO-LOCK,
            FIRST res-line WHERE res-line.resnr = reservation.resnr AND res-line.abreise = ci-date NO-LOCK,
            FIRST guest WHERE guest.gastnr = res-line.gastnr NO-LOCK BY reservation.resnr :

            DO: 
              CREATE mainres-list. 
              ASSIGN
                mainres-list.gastnr       = reservation.gastnr
                mainres-list.name         = reservation.NAME
                mainres-list.resnr        = reservation.resnr 
                mainres-list.groupname    = reservation.groupname
                mainres-list.res-address  = guest.adresse1
                mainres-list.res-city     = guest.wohnort + " " + guest.plz
                mainres-list.res-bemerk   = reservation.bemerk
              .
              RUN update-mainres. 
            END. 
         END. 
    END.
END CASE.

    /* ITA 10/04/25 -> optimalisasi serverless
CASE case-type:
    WHEN 1 THEN
    DO:
        FOR EACH reservation WHERE reservation.grpflag = YES 
          /*AND reservation.activeflag = 0 */ NO-LOCK BY reservation.resnr: 
            FIND FIRST res-line WHERE res-line.resnr = reservation.resnr /*AND (resstatus = 6 OR resstatus = 13)*/ 
                AND res-line.abreise = ci-date NO-LOCK NO-ERROR. 
            IF AVAILABLE res-line THEN 
            DO: 
              FIND FIRST guest WHERE guest.gastnr = res-line.gastnr NO-LOCK.
              CREATE mainres-list. 
              ASSIGN
                mainres-list.gastnr       = reservation.gastnr
                mainres-list.name         = reservation.NAME
                mainres-list.resnr        = reservation.resnr 
                mainres-list.groupname    = reservation.groupname
                mainres-list.res-address  = guest.adresse1
                mainres-list.res-city     = guest.wohnort + " " + guest.plz
                mainres-list.res-bemerk   = reservation.bemerk
              .
              RUN update-mainres. 
            END. 
         END. 
    END.
END CASE.*/

PROCEDURE update-mainres: 
  mainres-list.zimanz = 0. 
  mainres-list.co = 0. 
  mainres-list.res = 0. 
  mainres-list.dep = 0. 
  mainres-list.arr = 0. 
   FOR EACH res-line WHERE res-line.resnr = mainres-list.resnr AND 
    (resstatus NE 9 AND resstatus NE 10 AND resstatus NE 12) NO-LOCK: 
    mainres-list.zimanz = mainres-list.zimanz + res-line.zimmeranz. 
    IF res-line.active-flag = 0 THEN mainres-list.arr = mainres-list.arr + 1. 
    IF res-line.active-flag = 1 THEN 
    DO: 
      IF res-line.abreise GT ci-date THEN 
        mainres-list.res = mainres-list.res + 1. 
      ELSE mainres-list.dep = mainres-list.dep + 1. 
    END. 
    IF res-line.active-flag = 2 THEN mainres-list.co = mainres-list.co + 1. 
  END. 
END. 

