
DEFINE TEMP-TABLE b1-list
    FIELD grpflag       LIKE reservation.grpflag
    FIELD resnr         LIKE reservation.resnr
    FIELD reser-name    LIKE reservation.name
    FIELD groupname     LIKE reservation.groupname
    FIELD resli-name    LIKE res-line.name
    FIELD ankunft       LIKE res-line.ankunft
    FIELD limitdate     LIKE reservation.limitdate
    FIELD depositgef    LIKE reservation.depositgef
    FIELD depositbez    LIKE reservation.depositbez
    FIELD depositbez2   LIKE reservation.depositbez2
    FIELD zahldatum     LIKE reservation.zahldatum
    FIELD zahlkonto     LIKE reservation.zahlkonto
    FIELD zahldatum2    LIKE reservation.zahldatum2
    FIELD zahlkonto2    LIKE reservation.zahlkonto2
    
    /*for soAsia*/
    FIELD abreise       LIKE res-line.abreise
    FIELD qty           LIKE res-line.zimmeranz
    FIELD rmrate        LIKE res-line.zipreis
    FIELD rate-code     AS CHAR
    FIELD argt-code     AS CHAR
    FIELD remark        AS CHAR
    FIELD stafid        AS CHAR
    FIELD adult         LIKE res-line.erwachs
    FIELD rmtype        AS CHAR
    FIELD zipreis       AS DECIMAL
    FIELD rsv-status    AS INTEGER.

DEFINE TEMP-TABLE b1-print LIKE b1-list.

DEFINE TEMP-TABLE depo-list
    FIELD group-str     AS CHAR FORMAT "x(1)"
    FIELD resnr         LIKE reservation.resnr COLUMN-LABEL "ResNr" FORMAT ">>>>>>9"
    FIELD reserve-name  LIKE reservation.NAME 
    FIELD grpname       LIKE reservation.groupname
    FIELD guestname     LIKE res-line.NAME
    FIELD ankunft       LIKE res-line.ankunft
    FIELD depositgef    AS DECIMAL FORMAT "->>,>>>,>>>,>>>,>>>,>>9.99"
    FIELD limitdate     LIKE reservation.limitdate COLUMN-LABEL "Due Date"
    FIELD bal           AS DECIMAL FORMAT "->>,>>>,>>>,>>>,>>>,>>9.99" COLUMN-LABEL "Balance"
    FIELD depo1         AS DECIMAL FORMAT "->>,>>>,>>>,>>>,>>>,>>9.99" COLUMN-LABEL ""
    FIELD depositbez    LIKE reservation.depositbez
    FIELD datum1        LIKE reservation.zahldatum
    FIELD depo2         AS DECIMAL FORMAT "->>,>>>,>>>,>>>,>>>,>>9.99" COLUMN-LABEL ""
    FIELD depositbez2    LIKE reservation.depositbez2
    FIELD datum2        LIKE reservation.zahldatum2
    
    /*for soAsia*/
    FIELD abreise       LIKE res-line.abreise
    FIELD qty           LIKE res-line.zimmeranz
    FIELD rmrate        LIKE res-line.zipreis
    FIELD rate-code     AS CHAR
    FIELD argt-code     AS CHAR
    FIELD remark        AS CHAR
    FIELD stafid        AS CHAR
    FIELD adult         LIKE res-line.erwachs
    FIELD rmtype        AS CHAR
    FIELD rsv-status    AS INTEGER.

DEFINE INPUT PARAMETER case-type    AS INTEGER.
DEFINE INPUT PARAMETER depo-foreign AS LOGICAL.
DEFINE INPUT PARAMETER lname        AS CHAR.
DEFINE INPUT PARAMETER deposittype  AS INTEGER.
DEFINE INPUT PARAMETER sorttype     AS INTEGER.
DEFINE INPUT PARAMETER lresnr       AS INTEGER.
DEFINE INPUT PARAMETER fdate        AS DATE.
DEFINE INPUT PARAMETER exrate       AS DECIMAL.
DEFINE INPUT PARAMETER bill-date    AS DATE.
DEFINE INPUT PARAMETER depo-curr    AS INTEGER.

/* Naufal Afthar - 7B91F7 -> add period by payment date*/
DEFINE INPUT PARAMETER flag     AS INTEGER.
DEFINE INPUT PARAMETER tdate        AS DATE.
/* end Naufal Afthar*/

DEFINE OUTPUT PARAMETER total-saldo AS DECIMAL.
DEFINE OUTPUT PARAMETER arriv-saldo AS DECIMAL.
DEFINE OUTPUT PARAMETER TABLE FOR depo-list.
DEFINE OUTPUT PARAMETER TABLE FOR b1-list.
DEFINE OUTPUT PARAMETER TABLE FOR b1-print.

DEFINE VARIABLE grpstr      AS CHAR FORMAT "x(1)" EXTENT 2 
  INITIAL [" ", "G"] LABEL "   ". 
DEFINE VARIABLE xrate-change AS DECIMAL.

/*
DEFINE BUFFER reservation FOR reservation. 
DEFINE BUFFER res-line FOR res-line.
*/
DEFINE BUFFER bresline FOR res-line.

/* SY 05 Sept 2015 */
xrate-change = exrate.
IF flag EQ 1 THEN RUN create-itlist.
ELSE RUN create-itlist2. /* Naufal Afthar - 7B91F7 -> add period by payment date*/


PROCEDURE create-itlist: /* filter by single date*/
DEFINE VARIABLE to-name AS CHAR INITIAL "". 
  
  IF lname NE "" THEN to-name = CHR(ASC(SUBSTR(lname,1,1)) + 1). 
  
  IF lname = "" THEN 
  DO: 
    IF deposittype = 1 THEN 
    DO: 
      IF sorttype = 1 THEN 
      FOR EACH reservation WHERE activeflag = 0 
           AND reservation.depositgef NE 0 
           AND reservation.resnr GE lresnr NO-LOCK, 
         FIRST res-line WHERE res-line.resnr = reservation.resnr 
           AND res-line.resstatus LE 8 AND res-line.ankunft GE fdate 
           NO-LOCK BY reservation.NAME BY reservation.resnr:
          RUN create-it.
      END.
      /*Geral sorting resnr CACFF0*/
      ELSE IF sorttype = 2 THEN 
      DO:
         IF lresnr NE 0 THEN
           FOR EACH reservation WHERE activeflag = 0 
                AND reservation.depositgef NE 0 
                AND reservation.resnr EQ lresnr NO-LOCK, 
              FIRST res-line WHERE res-line.resnr = reservation.resnr 
                AND res-line.resstatus LE 8 AND res-line.ankunft GE fdate 
                NO-LOCK BY reservation.resnr BY reservation.NAME:
               RUN create-it.
           END.
         ELSE
           FOR EACH reservation WHERE activeflag = 0 
                AND reservation.depositgef NE 0 
                AND reservation.resnr GE lresnr NO-LOCK, 
              FIRST res-line WHERE res-line.resnr = reservation.resnr 
                AND res-line.resstatus LE 8 AND res-line.ankunft GE fdate 
                NO-LOCK BY reservation.resnr BY reservation.NAME:
               RUN create-it.
           END.
      END.
      ELSE IF sorttype = 3 THEN 
      FOR EACH reservation WHERE activeflag = 0 
         AND reservation.depositgef NE 0 
         AND reservation.resnr GE lresnr NO-LOCK, 
         FIRST res-line WHERE res-line.resnr = reservation.resnr 
         AND res-line.resstatus LE 8 AND res-line.ankunft GE fdate 
         NO-LOCK BY res-line.ankunft:
         RUN create-it.
      END.
      ELSE IF sorttype = 4 THEN 
      FOR EACH reservation WHERE activeflag = 0 
         AND reservation.depositgef NE 0 
         AND reservation.resnr GE lresnr 
         AND reservation.limitdate GE fdate NO-LOCK, 
         FIRST res-line WHERE res-line.resnr = reservation.resnr 
         AND res-line.resstatus LE 8 
         NO-LOCK BY reservation.limitdate BY reservation.NAME:
         RUN create-it.
      END.
      /* Naufal Afthar - 7B91F7 -> add sorting by payment date*/
      ELSE IF sorttype EQ 5 THEN 
      FOR EACH reservation WHERE activeflag = 0 
         AND reservation.depositgef NE 0 
         AND reservation.resnr GE lresnr NO-LOCK, 
         FIRST res-line WHERE res-line.resnr = reservation.resnr 
         AND res-line.resstatus LE 8 AND res-line.ankunft GE fdate 
         NO-LOCK BY reservation.zahldatum:
         RUN create-it.
      END.
    END. 
    ELSE IF deposittype = 2 THEN 
    DO: 
      IF sorttype = 1 THEN 
      FOR EACH reservation WHERE reservation.activeflag LE 1 
         AND reservation.depositgef NE 0 AND reservation.depositbez NE 0 
         AND reservation.resnr GE lresnr NO-LOCK, 
         FIRST res-line WHERE res-line.resnr = reservation.resnr 
         AND (res-line.resstatus LE 5 OR res-line.resstatus = 9 
         OR res-line.resstatus = 10) NO-LOCK BY reservation.NAME BY reservation.resnr:
         RUN create-it.   
         /*FD March 18, 2022 => ticket 7B1C21
         FIND FIRST bresline WHERE bresline.resnr EQ res-line.resnr
             AND bresline.reslinnr NE res-line.reslinnr
             AND (bresline.resstatus NE 9 OR bresline.resstatus NE 10) NO-LOCK NO-ERROR.
         IF NOT AVAILABLE bresline THEN RUN create-it.*/         
      END.
      /*Geral sorting resnr CACFF0*/
      IF sorttype = 2 THEN 
      DO:
         IF lresnr NE 0 THEN
            FOR EACH reservation WHERE reservation.activeflag LE 1 
               AND reservation.depositgef NE 0 AND reservation.depositbez NE 0 
               AND reservation.resnr EQ lresnr NO-LOCK, 
               FIRST res-line WHERE res-line.resnr = reservation.resnr 
               AND (res-line.resstatus LE 5 OR res-line.resstatus = 9 
               OR res-line.resstatus = 10) NO-LOCK BY reservation.resnr BY reservation.NAME:
               RUN create-it.
               /*FD March 18, 2022 => ticket 7B1C21
               FIND FIRST bresline WHERE bresline.resnr EQ res-line.resnr
                   AND bresline.reslinnr NE res-line.reslinnr
                   AND (bresline.resstatus NE 9 OR bresline.resstatus NE 10) NO-LOCK NO-ERROR.
               IF NOT AVAILABLE bresline THEN RUN create-it. */        
            END.
         ELSE
            FOR EACH reservation WHERE reservation.activeflag LE 1 
               AND reservation.depositgef NE 0 AND reservation.depositbez NE 0 
               AND reservation.resnr GE lresnr NO-LOCK, 
               FIRST res-line WHERE res-line.resnr = reservation.resnr 
               AND (res-line.resstatus LE 5 OR res-line.resstatus = 9 
               OR res-line.resstatus = 10) NO-LOCK BY reservation.resnr BY reservation.NAME:
               RUN create-it. 
               /*FD March 18, 2022 => ticket 7B1C21
               FIND FIRST bresline WHERE bresline.resnr EQ res-line.resnr
                   AND bresline.reslinnr NE res-line.reslinnr
                   AND (bresline.resstatus NE 9 OR bresline.resstatus NE 10) NO-LOCK NO-ERROR.
               IF NOT AVAILABLE bresline THEN RUN create-it.*/         
            END.
      END.
      ELSE IF sorttype = 3 THEN 
      FOR EACH reservation WHERE reservation.activeflag LE 1 
         AND reservation.depositgef NE 0 AND reservation.depositbez NE 0 
         AND reservation.resnr GE lresnr NO-LOCK, 
         FIRST res-line WHERE res-line.resnr = reservation.resnr 
         AND (res-line.resstatus LE 5 OR res-line.resstatus = 9 
         OR res-line.resstatus = 10) AND res-line.ankunft GE fdate 
         NO-LOCK BY res-line.ankunft:
         RUN create-it.
         /*FD March 18, 2022 => ticket 7B1C21
         FIND FIRST bresline WHERE bresline.resnr EQ res-line.resnr
             AND bresline.reslinnr NE res-line.reslinnr
             AND (bresline.resstatus NE 9 OR bresline.resstatus NE 10) NO-LOCK NO-ERROR.
         IF NOT AVAILABLE bresline THEN RUN create-it.*/
      END.
      ELSE IF sorttype = 4 THEN 
      FOR EACH reservation WHERE reservation.activeflag LE 1 
         AND reservation.depositgef NE 0 
         AND reservation.resnr GE lresnr 
         AND reservation.limitdate GE fdate NO-LOCK, 
         FIRST res-line WHERE res-line.resnr = reservation.resnr 
         AND (res-line.resstatus LE 5 OR res-line.resstatus = 9 
         OR res-line.resstatus = 10)
         NO-LOCK BY reservation.limitdate BY reservation.NAME:
         RUN create-it.
         /*FD March 18, 2022 => ticket 7B1C21
         FIND FIRST bresline WHERE bresline.resnr EQ res-line.resnr
             AND bresline.reslinnr NE res-line.reslinnr
             AND (bresline.resstatus NE 9 OR bresline.resstatus NE 10) NO-LOCK NO-ERROR.
         IF NOT AVAILABLE bresline THEN RUN create-it.*/
      END.
      /* Naufal Afthar - 7B91F7 -> add sorting by payment date*/
      ELSE IF sorttype EQ 5 THEN
      FOR EACH reservation WHERE reservation.activeflag LE 1 
         AND reservation.depositgef NE 0 AND reservation.depositbez NE 0 
         AND reservation.resnr GE lresnr NO-LOCK, 
         FIRST res-line WHERE res-line.resnr = reservation.resnr 
         AND (res-line.resstatus LE 5 OR res-line.resstatus = 9 
         OR res-line.resstatus = 10) AND res-line.ankunft GE fdate 
         NO-LOCK BY reservation.zahldatum:
         RUN create-it.
         /*FD March 18, 2022 => ticket 7B1C21
         FIND FIRST bresline WHERE bresline.resnr EQ res-line.resnr
             AND bresline.reslinnr NE res-line.reslinnr
             AND (bresline.resstatus NE 9 OR bresline.resstatus NE 10) NO-LOCK NO-ERROR.
         IF NOT AVAILABLE bresline THEN RUN create-it.*/
      END.
    END. 
    /* SY: 15/11/2019 */
    ELSE IF deposittype = 3 THEN /* sorttype is always = 3 */
    DO:
        FOR EACH reservation WHERE reservation.activeflag LE 1 
           AND reservation.depositgef EQ 0 
           AND reservation.resnr GE lresnr NO-LOCK, 
           FIRST res-line WHERE res-line.resnr = reservation.resnr 
           AND (res-line.resstatus LE 5 OR res-line.resstatus = 9 
           OR res-line.resstatus = 10) AND res-line.ankunft GE fdate 
           NO-LOCK BY res-line.ankunft:
           RUN create-it.
        END.
    END.
  END. 
  ELSE IF lname NE "" THEN  
  DO: 
    IF deposittype = 1 THEN 
    DO: 
      IF sorttype LE 2 THEN 
      DO:
        FOR EACH reservation WHERE activeflag = 0 
            AND reservation.depositgef NE 0 
            AND reservation.name MATCHES ("*" + lname + "*") 
            AND reservation.resnr GE lresnr NO-LOCK, 
            FIRST res-line WHERE res-line.resnr = reservation.resnr 
            AND res-line.resstatus LE 8 AND res-line.ankunft GE fdate 
            NO-LOCK BY reservation.NAME:
          RUN create-it.
        END.
        FOR EACH reservation WHERE activeflag = 0 
            AND reservation.depositgef NE 0 
            AND reservation.resnr GE lresnr NO-LOCK, 
            FIRST res-line WHERE res-line.resnr = reservation.resnr 
            AND res-line.resstatus LE 8 AND res-line.ankunft GE fdate 
            AND res-line.NAME MATCHES ("*" + lname + "*")
            NO-LOCK BY reservation.NAME:
          RUN create-it.
        END.
      END.
      ELSE IF sorttype = 3 THEN 
      DO:
        FOR EACH reservation WHERE activeflag = 0 
          AND reservation.depositgef NE 0 
          AND reservation.name MATCHES ("*" + lname + "*")
          AND reservation.resnr GE lresnr NO-LOCK, 
          FIRST res-line WHERE res-line.resnr = reservation.resnr 
          AND res-line.resstatus LE 8 AND res-line.ankunft GE fdate 
          NO-LOCK BY res-line.ankunft:
          RUN create-it.
        END.
        FOR EACH reservation WHERE activeflag = 0 
          AND reservation.depositgef NE 0 
          AND reservation.resnr GE lresnr NO-LOCK, 
          FIRST res-line WHERE res-line.resnr = reservation.resnr 
          AND res-line.resstatus LE 8 AND res-line.ankunft GE fdate 
          AND res-line.name MATCHES ("*" + lname + "*")
          NO-LOCK BY res-line.ankunft:
          RUN create-it.
        END.
      END.
      ELSE IF sorttype = 4 THEN 
      DO:
        FOR EACH reservation WHERE activeflag = 0 
          AND reservation.depositgef NE 0 
          AND reservation.name MATCHES ("*" + lname + "*")
          AND reservation.resnr GE lresnr 
          AND reservation.limitdate GE fdate, 
          FIRST res-line WHERE res-line.resnr = reservation.resnr 
          AND res-line.resstatus LE 8
          NO-LOCK BY reservation.limitdate BY reservation.NAME:
          RUN create-it.
        END.
        FOR EACH reservation WHERE activeflag = 0 
          AND reservation.depositgef NE 0 
          AND reservation.resnr GE lresnr 
          AND reservation.limitdate GE fdate, 
          FIRST res-line WHERE res-line.resnr = reservation.resnr 
          AND res-line.resstatus LE 8
          AND res-line.name MATCHES ("*" + lname + "*")
          NO-LOCK BY reservation.limitdate BY reservation.NAME:
          RUN create-it.
        END.
      END.
      /* Naufal Afthar - 7B91F7 -> add sorting by payment date*/
      ELSE IF sorttype EQ 5 THEN
      DO:
        FOR EACH reservation WHERE activeflag = 0 
          AND reservation.depositgef NE 0 
          AND reservation.name MATCHES ("*" + lname + "*")
          AND reservation.resnr GE lresnr NO-LOCK, 
          FIRST res-line WHERE res-line.resnr = reservation.resnr 
          AND res-line.resstatus LE 8 AND res-line.ankunft GE fdate 
          NO-LOCK BY reservation.zahldatum:
          RUN create-it.
        END.
        FOR EACH reservation WHERE activeflag = 0 
          AND reservation.depositgef NE 0 
          AND reservation.resnr GE lresnr NO-LOCK, 
          FIRST res-line WHERE res-line.resnr = reservation.resnr 
          AND res-line.resstatus LE 8 AND res-line.ankunft GE fdate 
          AND res-line.name MATCHES ("*" + lname + "*")
          NO-LOCK BY reservation.zahldatum:
          RUN create-it.
        END.
      END.
    END. 
    ELSE IF deposittype = 2 THEN 
    DO: 
      IF sorttype LE 2 THEN 
      DO:
        FOR EACH reservation WHERE activeflag LE 1 
            AND reservation.depositgef NE 0 AND reservation.depositbez NE 0 
            AND reservation.NAME MATCHES ("*" + lname + "*")  
            AND reservation.resnr GE lresnr NO-LOCK, 
          FIRST res-line WHERE res-line.resnr = reservation.resnr 
            AND (res-line.resstatus LE 5 OR res-line.resstatus = 9 
            OR res-line.resstatus = 10) NO-LOCK BY reservation.NAME:
            RUN create-it.
            /*FD March 18, 2022 => ticket 7B1C21
            FIND FIRST bresline WHERE bresline.resnr EQ res-line.resnr
                AND bresline.reslinnr NE res-line.reslinnr
                AND (bresline.resstatus NE 9 OR bresline.resstatus NE 10) NO-LOCK NO-ERROR.
            IF NOT AVAILABLE bresline THEN RUN create-it.  */        
        END.
        FOR EACH reservation WHERE activeflag LE 1 
            AND reservation.depositgef NE 0 AND reservation.depositbez NE 0 
            AND reservation.resnr GE lresnr NO-LOCK, 
          FIRST res-line WHERE res-line.resnr = reservation.resnr 
            AND (res-line.resstatus LE 5 OR res-line.resstatus = 9 
            OR res-line.resstatus = 10) 
            AND res-line.NAME MATCHES ("*" + lname + "*")
            NO-LOCK BY reservation.NAME:
            RUN create-it.
            /*FD March 18, 2022 => ticket 7B1C21
            FIND FIRST bresline WHERE bresline.resnr EQ res-line.resnr
                AND bresline.reslinnr NE res-line.reslinnr
                AND (bresline.resstatus NE 9 OR bresline.resstatus NE 10) NO-LOCK NO-ERROR.
            IF NOT AVAILABLE bresline THEN RUN create-it.*/
        END.
      END.
      ELSE IF sorttype = 3 THEN 
      DO:
        FOR EACH reservation WHERE activeflag LE 1
          AND reservation.depositgef NE 0 AND reservation.depositbez NE 0 
          AND reservation.name MATCHES ("*" + lname + "*") 
          AND reservation.resnr GE lresnr NO-LOCK, 
          FIRST res-line WHERE res-line.resnr = reservation.resnr 
          AND (res-line.resstatus LE 5 OR res-line.resstatus = 9 
          OR res-line.resstatus = 10) AND res-line.ankunft GE fdate 
          NO-LOCK BY res-line.ankunft:
            RUN create-it.    
            /*FD March 18, 2022 => ticket 7B1C21
            FIND FIRST bresline WHERE bresline.resnr EQ res-line.resnr
                AND bresline.reslinnr NE res-line.reslinnr
                AND (bresline.resstatus NE 9 OR bresline.resstatus NE 10) NO-LOCK NO-ERROR.
            IF NOT AVAILABLE bresline THEN RUN create-it.*/
        END.
        FOR EACH reservation WHERE activeflag LE 1
          AND reservation.depositgef NE 0 AND reservation.depositbez NE 0 
          AND reservation.resnr GE lresnr NO-LOCK, 
          FIRST res-line WHERE res-line.resnr = reservation.resnr 
          AND (res-line.resstatus LE 5 OR res-line.resstatus = 9 
          OR res-line.resstatus = 10) AND res-line.ankunft GE fdate 
          AND res-line.name MATCHES ("*" + lname + "*") 
          NO-LOCK BY res-line.ankunft:
            RUN create-it.
            /*FD March 18, 2022 => ticket 7B1C21
            FIND FIRST bresline WHERE bresline.resnr EQ res-line.resnr
                AND bresline.reslinnr NE res-line.reslinnr
                AND (bresline.resstatus NE 9 OR bresline.resstatus NE 10) NO-LOCK NO-ERROR.
            IF NOT AVAILABLE bresline THEN RUN create-it.*/
        END.
      END.
      ELSE IF sorttype = 4 THEN 
      DO:
        FOR EACH reservation WHERE activeflag LE 1
          AND reservation.depositgef NE 0 
          AND reservation.name MATCHES ("*" + lname + "*")
          AND reservation.resnr GE lresnr 
          AND reservation.limitdate GE fdate NO-LOCK, 
          FIRST res-line WHERE res-line.resnr = reservation.resnr 
          AND (res-line.resstatus LE 5 OR res-line.resstatus = 9 
          OR res-line.resstatus = 10) 
          NO-LOCK BY reservation.limitdate BY reservation.NAME:
            RUN create-it.
            /*FD March 18, 2022 => ticket 7B1C21
            FIND FIRST bresline WHERE bresline.resnr EQ res-line.resnr
                AND bresline.reslinnr NE res-line.reslinnr
                AND (bresline.resstatus NE 9 OR bresline.resstatus NE 10) NO-LOCK NO-ERROR.
            IF NOT AVAILABLE bresline THEN RUN create-it.*/
        END.
        FOR EACH reservation WHERE activeflag LE 1
          AND reservation.depositgef NE 0 
          AND reservation.resnr GE lresnr 
          AND reservation.limitdate GE fdate NO-LOCK, 
          FIRST res-line WHERE res-line.resnr = reservation.resnr 
          AND (res-line.resstatus LE 5 OR res-line.resstatus = 9 
          OR res-line.resstatus = 10) 
          AND res-line.name MATCHES ("*" + lname + "*")
          NO-LOCK BY reservation.limitdate BY reservation.NAME:
            RUN create-it.
            /*FD March 18, 2022 => ticket 7B1C21
            FIND FIRST bresline WHERE bresline.resnr EQ res-line.resnr
                AND bresline.reslinnr NE res-line.reslinnr
                AND (bresline.resstatus NE 9 OR bresline.resstatus NE 10) NO-LOCK NO-ERROR.
            IF NOT AVAILABLE bresline THEN RUN create-it.*/
        END.
      END.
      /* Naufal Afthar - 7B91F7 -> add sorting by payment date*/
      ELSE IF sorttype EQ 5 THEN
      DO:
        FOR EACH reservation WHERE activeflag LE 1
          AND reservation.depositgef NE 0 AND reservation.depositbez NE 0 
          AND reservation.name MATCHES ("*" + lname + "*") 
          AND reservation.resnr GE lresnr NO-LOCK, 
          FIRST res-line WHERE res-line.resnr = reservation.resnr 
          AND (res-line.resstatus LE 5 OR res-line.resstatus = 9 
          OR res-line.resstatus = 10) AND res-line.ankunft GE fdate 
          NO-LOCK BY reservation.zahldatum:
            RUN create-it.
            /*FD March 18, 2022 => ticket 7B1C21
            FIND FIRST bresline WHERE bresline.resnr EQ res-line.resnr
                AND bresline.reslinnr NE res-line.reslinnr
                AND (bresline.resstatus NE 9 OR bresline.resstatus NE 10) NO-LOCK NO-ERROR.
            IF NOT AVAILABLE bresline THEN RUN create-it.*/
        END.
        FOR EACH reservation WHERE activeflag LE 1
          AND reservation.depositgef NE 0 AND reservation.depositbez NE 0 
          AND reservation.resnr GE lresnr NO-LOCK, 
          FIRST res-line WHERE res-line.resnr = reservation.resnr 
          AND (res-line.resstatus LE 5 OR res-line.resstatus = 9 
          OR res-line.resstatus = 10) AND res-line.ankunft GE fdate 
          AND res-line.name MATCHES ("*" + lname + "*") 
          NO-LOCK BY reservation.zahldatum:
            RUN create-it.
            /*FD March 18, 2022 => ticket 7B1C21
            FIND FIRST bresline WHERE bresline.resnr EQ res-line.resnr
                AND bresline.reslinnr NE res-line.reslinnr
                AND (bresline.resstatus NE 9 OR bresline.resstatus NE 10) NO-LOCK NO-ERROR.
            IF NOT AVAILABLE bresline THEN RUN create-it.*/
        END.
      END.
    END. 
    /* SY: 15/11/2019 */
    ELSE IF deposittype = 3 THEN /* sorttype is always = 3 */
    DO:
        FOR EACH reservation WHERE reservation.activeflag LE 1 
           AND reservation.depositgef EQ 0 
           AND reservation.resnr GE lresnr NO-LOCK, 
           FIRST res-line WHERE res-line.resnr = reservation.resnr 
           AND (res-line.resstatus LE 5 OR res-line.resstatus = 9 
           OR res-line.resstatus = 10) AND res-line.ankunft GE fdate 
           AND res-line.name MATCHES ("*" + lname + "*")
           NO-LOCK BY res-line.ankunft:
           RUN create-it.
        END.
    END.
  END. 
 
  total-saldo = 0.
  arriv-saldo = 0.
  
  IF case-type = 1 THEN
  DO:
    IF depo-foreign THEN
    DO:
      FOR EACH depo-list:
        total-saldo = total-saldo + depo-list.depositgef - depo-list.depositbez - depo-list.depositbez2.
        FIND FIRST res-line WHERE res-line.resnr = depo-list.resnr
          AND res-line.active-flag = 1 NO-LOCK NO-ERROR.
        IF NOT AVAILABLE res-line THEN 
          arriv-saldo = arriv-saldo + depo-list.depositbez + depo-list.depositbez2.
      END.  
      ASSIGN
        total-saldo = total-saldo 
        arriv-saldo = arriv-saldo
      .
    END.
    ELSE
    DO:
      FOR EACH b1-list:
        total-saldo = total-saldo + b1-list.depositgef - b1-list.depositbez - b1-list.depositbez2.
        FIND FIRST res-line WHERE res-line.resnr = b1-list.resnr
            AND res-line.active-flag = 1 NO-LOCK NO-ERROR.
        IF NOT AVAILABLE res-line THEN 
          arriv-saldo = arriv-saldo + b1-list.depositbez + b1-list.depositbez2.
      END.
      ASSIGN
        total-saldo = total-saldo * xrate-change
        arriv-saldo = arriv-saldo * xrate-change
      .
    END.
  END.
  ELSE IF case-type = 2 THEN
  DO:
      FOR EACH b1-print:
          total-saldo = total-saldo + b1-print.depositgef - b1-print.depositbez - b1-print.depositbez2.
          FIND FIRST res-line WHERE res-line.resnr = b1-print.resnr
              AND res-line.active-flag = 1 NO-LOCK NO-ERROR.
          IF NOT AVAILABLE res-line THEN 
            arriv-saldo = arriv-saldo + b1-print.depositbez + b1-print.depositbez2.
      END.

      ASSIGN
          total-saldo = total-saldo * xrate-change
          arriv-saldo = arriv-saldo * xrate-change
          .
  END.
END.

/* Naufal Afthar - 7B91F7 -> add period by payment date*/
PROCEDURE create-itlist2:
DEFINE VARIABLE to-name AS CHAR INITIAL "". 

  IF lname NE "" THEN to-name = CHR(ASC(SUBSTR(lname,1,1)) + 1). 
  
  IF lname = "" THEN 
  DO: 
    IF deposittype = 1 THEN 
    DO: 
      IF sorttype = 1 THEN 
      FOR EACH reservation WHERE activeflag = 0 
           AND reservation.depositgef NE 0 
           AND reservation.resnr GE lresnr AND reservation.zahldatum NE ? NO-LOCK, 
         FIRST res-line WHERE res-line.resnr = reservation.resnr 
           AND res-line.resstatus LE 8 
           AND res-line.ankunft GE fdate AND res-line.ankunft LE tdate NO-LOCK /* Naufal Afthar - 7B91F7*/
           BY reservation.NAME BY reservation.resnr:
          RUN create-it.
      END.
      /*Geral sorting resnr CACFF0*/
      ELSE IF sorttype = 2 THEN 
      DO:
         IF lresnr NE 0 THEN
           FOR EACH reservation WHERE activeflag = 0 
                AND reservation.depositgef NE 0 
                AND reservation.resnr EQ lresnr AND reservation.zahldatum NE ? NO-LOCK, 
              FIRST res-line WHERE res-line.resnr = reservation.resnr 
                AND res-line.resstatus LE 8 
                AND res-line.ankunft GE fdate AND res-line.ankunft LE tdate NO-LOCK /* Naufal Afthar - 7B91F7*/
                BY reservation.resnr BY reservation.NAME:
               RUN create-it.
           END.
         ELSE
           FOR EACH reservation WHERE activeflag = 0 
                AND reservation.depositgef NE 0 
                AND reservation.resnr GE lresnr AND reservation.zahldatum NE ? NO-LOCK, 
              FIRST res-line WHERE res-line.resnr = reservation.resnr 
                AND res-line.resstatus LE 8 
                AND res-line.ankunft GE fdate AND res-line.ankunft LE tdate NO-LOCK /* Naufal Afthar - 7B91F7*/
                BY reservation.resnr BY reservation.NAME:
               RUN create-it.
           END.
      END.
      ELSE IF sorttype = 3 THEN 
      FOR EACH reservation WHERE activeflag = 0 
         AND reservation.depositgef NE 0 
         AND reservation.resnr GE lresnr AND reservation.zahldatum NE ? NO-LOCK, /* Naufal Afthar - 7B91F7*/ 
         FIRST res-line WHERE res-line.resnr = reservation.resnr 
         AND res-line.resstatus LE 8 
         AND res-line.ankunft GE fdate AND res-line.ankunft LE tdate NO-LOCK /* Naufal Afthar - 7B91F7*/
         BY res-line.ankunft:
         RUN create-it.
      END.
      ELSE IF sorttype = 4 THEN 
      FOR EACH reservation WHERE activeflag = 0 
         AND reservation.depositgef NE 0 
         AND reservation.resnr GE lresnr AND reservation.zahldatum NE ?
         AND reservation.limitdate GE fdate AND reservation.limitdate LE tdate NO-LOCK, /* Naufal Afthar - 7B91F7*/
         FIRST res-line WHERE res-line.resnr = reservation.resnr 
         AND res-line.resstatus LE 8 NO-LOCK 
         BY reservation.limitdate BY reservation.NAME:
         RUN create-it.
      END.
      /* Naufal Afthar - 7B91F7 -> add sort by payment date*/
      ELSE IF sorttype EQ 5 THEN
      FOR EACH reservation WHERE activeflag = 0 
         AND reservation.depositgef NE 0 
         AND reservation.resnr GE lresnr AND reservation.zahldatum NE ? NO-LOCK,
         FIRST res-line WHERE res-line.resnr = reservation.resnr 
         AND res-line.resstatus LE 8 
         AND res-line.ankunft GE fdate AND res-line.ankunft LE tdate NO-LOCK
         BY reservation.zahldatum:
         RUN create-it.
      END.
    END. 
    ELSE IF deposittype = 2 THEN 
    DO: 
      IF sorttype = 1 THEN 
      FOR EACH reservation WHERE reservation.activeflag LE 1 
         AND reservation.depositgef NE 0 AND reservation.depositbez NE 0 
         AND reservation.resnr GE lresnr NO-LOCK, 
         FIRST res-line WHERE res-line.resnr = reservation.resnr 
         AND (res-line.resstatus LE 5 OR res-line.resstatus = 9 
         OR res-line.resstatus = 10) NO-LOCK BY reservation.NAME BY reservation.resnr:
         RUN create-it.
         /*FD March 18, 2022 => ticket 7B1C21
         FIND FIRST bresline WHERE bresline.resnr EQ res-line.resnr
             AND bresline.reslinnr NE res-line.reslinnr
             AND (bresline.resstatus NE 9 OR bresline.resstatus NE 10) NO-LOCK NO-ERROR.
         IF NOT AVAILABLE bresline THEN RUN create-it. */        
      END.
      /*Geral sorting resnr CACFF0*/
      IF sorttype = 2 THEN 
      DO:
         IF lresnr NE 0 THEN
            FOR EACH reservation WHERE reservation.activeflag LE 1 
               AND reservation.depositgef NE 0 AND reservation.depositbez NE 0 
               AND reservation.resnr EQ lresnr NO-LOCK, 
               FIRST res-line WHERE res-line.resnr = reservation.resnr 
               AND (res-line.resstatus LE 5 OR res-line.resstatus = 9 
               OR res-line.resstatus = 10) NO-LOCK BY reservation.resnr BY reservation.NAME:
                RUN create-it.
               /*FD March 18, 2022 => ticket 7B1C21
               FIND FIRST bresline WHERE bresline.resnr EQ res-line.resnr
                   AND bresline.reslinnr NE res-line.reslinnr
                   AND (bresline.resstatus NE 9 OR bresline.resstatus NE 10) NO-LOCK NO-ERROR.
               IF NOT AVAILABLE bresline THEN RUN create-it.   */      
            END.
         ELSE
            FOR EACH reservation WHERE reservation.activeflag LE 1 
               AND reservation.depositgef NE 0 AND reservation.depositbez NE 0 
               AND reservation.resnr GE lresnr NO-LOCK, 
               FIRST res-line WHERE res-line.resnr = reservation.resnr 
               AND (res-line.resstatus LE 5 OR res-line.resstatus = 9 
               OR res-line.resstatus = 10) NO-LOCK BY reservation.resnr BY reservation.NAME:
                RUN create-it.
               /*FD March 18, 2022 => ticket 7B1C21
               FIND FIRST bresline WHERE bresline.resnr EQ res-line.resnr
                   AND bresline.reslinnr NE res-line.reslinnr
                   AND (bresline.resstatus NE 9 OR bresline.resstatus NE 10) NO-LOCK NO-ERROR.
               IF NOT AVAILABLE bresline THEN RUN create-it.*/         
            END.
      END.
      ELSE IF sorttype = 3 THEN 
      FOR EACH reservation WHERE reservation.activeflag LE 1 
         AND reservation.depositgef NE 0 AND reservation.depositbez NE 0 
         AND reservation.resnr GE lresnr AND reservation.zahldatum NE ? NO-LOCK,
         FIRST res-line WHERE res-line.resnr = reservation.resnr 
         AND (res-line.resstatus LE 5 OR res-line.resstatus = 9 OR res-line.resstatus = 10) 
         AND res-line.ankunft GE fdate AND res-line.ankunft LE tdate NO-LOCK /* Naufal Afthar - 7B91F7*/
         BY res-line.ankunft:
         RUN create-it.
         /*FD March 18, 2022 => ticket 7B1C21
         FIND FIRST bresline WHERE bresline.resnr EQ res-line.resnr
             AND bresline.reslinnr NE res-line.reslinnr
             AND (bresline.resstatus NE 9 OR bresline.resstatus NE 10) NO-LOCK NO-ERROR.
         IF NOT AVAILABLE bresline THEN RUN create-it.*/
      END.
      ELSE IF sorttype = 4 THEN 
      FOR EACH reservation WHERE reservation.activeflag LE 1 
         AND reservation.depositgef NE 0 
         AND reservation.resnr GE lresnr AND reservation.zahldatum NE ?
         AND reservation.limitdate GE fdate AND reservation.limitdate LE tdate NO-LOCK, /* Naufal Afthar - 7B91F7*/
         FIRST res-line WHERE res-line.resnr = reservation.resnr 
         AND (res-line.resstatus LE 5 OR res-line.resstatus = 9 
         OR res-line.resstatus = 10)
         NO-LOCK BY reservation.limitdate: 
         RUN create-it.
         /*FD March 18, 2022 => ticket 7B1C21
         FIND FIRST bresline WHERE bresline.resnr EQ res-line.resnr
             AND bresline.reslinnr NE res-line.reslinnr
             AND (bresline.resstatus NE 9 OR bresline.resstatus NE 10) NO-LOCK NO-ERROR.
         IF NOT AVAILABLE bresline THEN RUN create-it.*/
      END.
      /*Naufal Afthar - 7B91F7 -> add sort by payment date*/
      ELSE IF sorttype EQ 5 THEN
      FOR EACH reservation WHERE reservation.activeflag LE 1 
         AND reservation.depositgef NE 0 AND reservation.depositbez NE 0 
         AND reservation.resnr GE lresnr AND reservation.zahldatum NE ? NO-LOCK,
         FIRST res-line WHERE res-line.resnr = reservation.resnr 
         AND (res-line.resstatus LE 5 OR res-line.resstatus = 9 OR res-line.resstatus = 10) 
         AND res-line.ankunft GE fdate AND res-line.ankunft LE tdate NO-LOCK 
         BY reservation.zahldatum:
         RUN create-it.
         /*FD March 18, 2022 => ticket 7B1C21
         FIND FIRST bresline WHERE bresline.resnr EQ res-line.resnr
             AND bresline.reslinnr NE res-line.reslinnr
             AND (bresline.resstatus NE 9 OR bresline.resstatus NE 10) NO-LOCK NO-ERROR.
         IF NOT AVAILABLE bresline THEN RUN create-it.*/
      END.
    END. 
    /* SY: 15/11/2019 */
    ELSE IF deposittype = 3 THEN /* sorttype is always = 3 */
    DO:
        FOR EACH reservation WHERE reservation.activeflag LE 1 
           AND reservation.depositgef EQ 0 
           AND reservation.resnr GE lresnr NO-LOCK, 
           FIRST res-line WHERE res-line.resnr = reservation.resnr 
           AND (res-line.resstatus LE 5 OR res-line.resstatus = 9 
           OR res-line.resstatus = 10) AND res-line.ankunft GE fdate 
           NO-LOCK BY res-line.ankunft:
           RUN create-it.
        END.
    END.
  END. 
  ELSE IF lname NE "" THEN  
  DO: 
    IF deposittype = 1 THEN 
    DO: 
      IF sorttype LE 2 THEN 
      DO:
        FOR EACH reservation WHERE activeflag = 0 
            AND reservation.depositgef NE 0 
            AND reservation.name MATCHES ("*" + lname + "*") 
            AND reservation.resnr GE lresnr AND reservation.zahldatum NE ? NO-LOCK, 
            FIRST res-line WHERE res-line.resnr = reservation.resnr 
            AND res-line.resstatus LE 8 
            AND res-line.ankunft GE fdate AND res-line.ankunft LE tdate NO-LOCK /* Naufal Afthar - 7B91F7*/
            BY reservation.NAME:
          RUN create-it.
        END.
        FOR EACH reservation WHERE activeflag = 0 
            AND reservation.depositgef NE 0 
            AND reservation.resnr GE lresnr AND reservation.zahldatum NE ? NO-LOCK,
            FIRST res-line WHERE res-line.resnr = reservation.resnr 
            AND res-line.resstatus LE 8 
            AND res-line.NAME MATCHES ("*" + lname + "*")
            AND res-line.ankunft GE fdate AND res-line.ankunft LE tdate NO-LOCK /* Naufal Afthar - 7B91F7*/
            BY reservation.NAME:
          RUN create-it.
        END.
      END.
      ELSE IF sorttype = 3 THEN 
      DO:
        FOR EACH reservation WHERE activeflag = 0 
          AND reservation.depositgef NE 0 
          AND reservation.name MATCHES ("*" + lname + "*")
          AND reservation.resnr GE lresnr AND reservation.zahldatum NE ? NO-LOCK,
          FIRST res-line WHERE res-line.resnr = reservation.resnr 
          AND res-line.resstatus LE 8 
          AND res-line.ankunft GE fdate AND res-line.ankunft LE tdate NO-LOCK /* Naufal Afthar - 7B91F7*/
          BY res-line.ankunft:
          RUN create-it.
        END.
        FOR EACH reservation WHERE activeflag = 0 
          AND reservation.depositgef NE 0 
          AND reservation.resnr GE lresnr AND reservation.zahldatum NE ? NO-LOCK,
          FIRST res-line WHERE res-line.resnr = reservation.resnr 
          AND res-line.resstatus LE 8
          AND res-line.name MATCHES ("*" + lname + "*") 
          AND res-line.ankunft GE fdate AND res-line.ankunft LE tdate NO-LOCK /* Naufal Afthar - 7B91F7*/
          BY res-line.ankunft:
          RUN create-it.
        END.
      END.
      ELSE IF sorttype = 4 THEN 
      DO:
        FOR EACH reservation WHERE activeflag = 0 
          AND reservation.depositgef NE 0 
          AND reservation.name MATCHES ("*" + lname + "*")
          AND reservation.resnr GE lresnr AND reservation.zahldatum NE ?
          AND reservation.limitdate GE fdate AND reservation.limitdate LE tdate NO-LOCK, /* Naufal Afthar - 7B91F7*/
          FIRST res-line WHERE res-line.resnr = reservation.resnr 
          AND res-line.resstatus LE 8 NO-LOCK 
          BY reservation.limitdate BY reservation.NAME:
          RUN create-it.
        END.
        FOR EACH reservation WHERE activeflag = 0 
          AND reservation.depositgef NE 0 
          AND reservation.resnr GE lresnr AND reservation.zahldatum NE ?
          AND reservation.limitdate GE fdate AND reservation.limitdate LE tdate NO-LOCK, /* Naufal Afthar - 7B91F7*/
          FIRST res-line WHERE res-line.resnr = reservation.resnr 
          AND res-line.resstatus LE 8
          AND res-line.name MATCHES ("*" + lname + "*")
          NO-LOCK BY reservation.limitdate BY reservation.NAME:
          RUN create-it.
        END.
      END.
      /*Naufal Afthar - 7B91F7 -> add sort by payment date*/
      ELSE IF sorttype EQ 5 THEN
      DO:
        FOR EACH reservation WHERE activeflag = 0 
          AND reservation.depositgef NE 0 
          AND reservation.name MATCHES ("*" + lname + "*")
          AND reservation.resnr GE lresnr AND reservation.zahldatum NE ? NO-LOCK,
          FIRST res-line WHERE res-line.resnr = reservation.resnr 
          AND res-line.resstatus LE 8 
          AND res-line.ankunft GE fdate AND res-line.ankunft LE tdate NO-LOCK 
          BY reservation.zahldatum:
          RUN create-it.
        END.
        FOR EACH reservation WHERE activeflag = 0 
          AND reservation.depositgef NE 0 
          AND reservation.resnr GE lresnr AND reservation.zahldatum NE ? NO-LOCK,
          FIRST res-line WHERE res-line.resnr = reservation.resnr 
          AND res-line.resstatus LE 8
          AND res-line.name MATCHES ("*" + lname + "*") 
          AND res-line.ankunft GE fdate AND res-line.ankunft LE tdate NO-LOCK 
          BY reservation.zahldatum:
          RUN create-it.
        END.
      END.
    END. 
    ELSE IF deposittype = 2 THEN 
    DO: 
      IF sorttype LE 2 THEN 
      DO:
        FOR EACH reservation WHERE activeflag LE 1 
            AND reservation.depositgef NE 0 AND reservation.depositbez NE 0 
            AND reservation.NAME MATCHES ("*" + lname + "*")  
            AND reservation.resnr GE lresnr NO-LOCK, 
          FIRST res-line WHERE res-line.resnr = reservation.resnr 
            AND (res-line.resstatus LE 5 OR res-line.resstatus = 9 
            OR res-line.resstatus = 10) NO-LOCK BY reservation.NAME:
            RUN create-it.
            /*FD March 18, 2022 => ticket 7B1C21
            FIND FIRST bresline WHERE bresline.resnr EQ res-line.resnr
                AND bresline.reslinnr NE res-line.reslinnr
                AND (bresline.resstatus NE 9 OR bresline.resstatus NE 10) NO-LOCK NO-ERROR.
            IF NOT AVAILABLE bresline THEN RUN create-it. */         
        END.
        FOR EACH reservation WHERE activeflag LE 1 
            AND reservation.depositgef NE 0 AND reservation.depositbez NE 0 
            AND reservation.resnr GE lresnr NO-LOCK, 
          FIRST res-line WHERE res-line.resnr = reservation.resnr 
            AND (res-line.resstatus LE 5 OR res-line.resstatus = 9 
            OR res-line.resstatus = 10) 
            AND res-line.NAME MATCHES ("*" + lname + "*")
            NO-LOCK BY reservation.NAME:
            RUN create-it.
            /*FD March 18, 2022 => ticket 7B1C21
            FIND FIRST bresline WHERE bresline.resnr EQ res-line.resnr
                AND bresline.reslinnr NE res-line.reslinnr
                AND (bresline.resstatus NE 9 OR bresline.resstatus NE 10) NO-LOCK NO-ERROR.
            IF NOT AVAILABLE bresline THEN RUN create-it.*/
        END.
      END.
      ELSE IF sorttype = 3 THEN 
      DO:
        FOR EACH reservation WHERE activeflag LE 1
          AND reservation.depositgef NE 0 AND reservation.depositbez NE 0 
          AND reservation.name MATCHES ("*" + lname + "*") 
          AND reservation.resnr GE lresnr AND reservation.zahldatum NE ? NO-LOCK, 
          FIRST res-line WHERE res-line.resnr = reservation.resnr 
          AND (res-line.resstatus LE 5 OR res-line.resstatus = 9 OR res-line.resstatus = 10) 
          AND res-line.ankunft GE fdate AND res-line.ankunft LE tdate NO-LOCK /* Naufal Afthar - 7B91F7*/
          BY res-line.ankunft:
            RUN create-it.
            /*FD March 18, 2022 => ticket 7B1C21
            FIND FIRST bresline WHERE bresline.resnr EQ res-line.resnr
                AND bresline.reslinnr NE res-line.reslinnr
                AND (bresline.resstatus NE 9 OR bresline.resstatus NE 10) NO-LOCK NO-ERROR.
            IF NOT AVAILABLE bresline THEN RUN create-it.*/
        END.
        FOR EACH reservation WHERE activeflag LE 1
          AND reservation.depositgef NE 0 AND reservation.depositbez NE 0 
          AND reservation.resnr GE lresnr AND reservation.zahldatum NE ? NO-LOCK, /* Naufal Afthar - 7B91F7*/
          FIRST res-line WHERE res-line.resnr = reservation.resnr 
          AND (res-line.resstatus LE 5 OR res-line.resstatus = 9 
          OR res-line.resstatus = 10) 
          AND res-line.name MATCHES ("*" + lname + "*") 
          AND res-line.ankunft GE fdate AND res-line.ankunft LE tdate NO-LOCK /* Naufal Afthar - 7B91F7*/
          BY res-line.ankunft:
            RUN create-it.
            /*FD March 18, 2022 => ticket 7B1C21
            FIND FIRST bresline WHERE bresline.resnr EQ res-line.resnr
                AND bresline.reslinnr NE res-line.reslinnr
                AND (bresline.resstatus NE 9 OR bresline.resstatus NE 10) NO-LOCK NO-ERROR.
            IF NOT AVAILABLE bresline THEN RUN create-it.*/
        END.
      END.
      ELSE IF sorttype = 4 THEN 
      DO:
        FOR EACH reservation WHERE activeflag LE 1
          AND reservation.depositgef NE 0 
          AND reservation.name MATCHES ("*" + lname + "*")
          AND reservation.resnr GE lresnr AND reservation.zahldatum NE ?
          AND reservation.limitdate GE fdate AND reservation.limitdate LE tdate NO-LOCK, /* Naufal Afthar - 7B91F7*/
          FIRST res-line WHERE res-line.resnr = reservation.resnr 
          AND (res-line.resstatus LE 5 OR res-line.resstatus = 9 OR res-line.resstatus = 10) NO-LOCK 
          BY reservation.limitdate BY reservation.NAME:
            RUN create-it.
            /*FD March 18, 2022 => ticket 7B1C21
            FIND FIRST bresline WHERE bresline.resnr EQ res-line.resnr
                AND bresline.reslinnr NE res-line.reslinnr
                AND (bresline.resstatus NE 9 OR bresline.resstatus NE 10) NO-LOCK NO-ERROR.
            IF NOT AVAILABLE bresline THEN RUN create-it.*/
        END.
        FOR EACH reservation WHERE activeflag LE 1
          AND reservation.depositgef NE 0 
          AND reservation.resnr GE lresnr AND reservation.zahldatum NE ?
          AND reservation.limitdate GE fdate AND reservation.limitdate LE tdate NO-LOCK, /* Naufal Afthar - 7B91F7*/
          FIRST res-line WHERE res-line.resnr = reservation.resnr 
          AND (res-line.resstatus LE 5 OR res-line.resstatus = 9 OR res-line.resstatus = 10) 
          AND res-line.name MATCHES ("*" + lname + "*") NO-LOCK 
          BY reservation.limitdate BY reservation.NAME:
            RUN create-it.
            /*FD March 18, 2022 => ticket 7B1C21
            FIND FIRST bresline WHERE bresline.resnr EQ res-line.resnr
                AND bresline.reslinnr NE res-line.reslinnr
                AND (bresline.resstatus NE 9 OR bresline.resstatus NE 10) NO-LOCK NO-ERROR.
            IF NOT AVAILABLE bresline THEN RUN create-it.*/
        END.
      END.
      /*Naufal Afthar - 7B91F7 -> add sort by payment date*/
      ELSE IF sorttype EQ 5 THEN
      DO:
        FOR EACH reservation WHERE activeflag LE 1
          AND reservation.depositgef NE 0 AND reservation.depositbez NE 0 
          AND reservation.name MATCHES ("*" + lname + "*") 
          AND reservation.resnr GE lresnr AND reservation.zahldatum NE ? NO-LOCK, 
          FIRST res-line WHERE res-line.resnr = reservation.resnr 
          AND (res-line.resstatus LE 5 OR res-line.resstatus = 9 OR res-line.resstatus = 10) 
          AND res-line.ankunft GE fdate AND res-line.ankunft LE tdate NO-LOCK /* Naufal Afthar - 7B91F7*/
          BY reservation.zahldatum:
            RUN create-it.
            /*FD March 18, 2022 => ticket 7B1C21
            FIND FIRST bresline WHERE bresline.resnr EQ res-line.resnr
                AND bresline.reslinnr NE res-line.reslinnr
                AND (bresline.resstatus NE 9 OR bresline.resstatus NE 10) NO-LOCK NO-ERROR.
            IF NOT AVAILABLE bresline THEN RUN create-it.*/
        END.
        FOR EACH reservation WHERE activeflag LE 1
          AND reservation.depositgef NE 0 AND reservation.depositbez NE 0 
          AND reservation.resnr GE lresnr AND reservation.zahldatum NE ? NO-LOCK,
          FIRST res-line WHERE res-line.resnr = reservation.resnr 
          AND (res-line.resstatus LE 5 OR res-line.resstatus = 9 
          OR res-line.resstatus = 10) 
          AND res-line.name MATCHES ("*" + lname + "*") 
          AND res-line.ankunft GE fdate AND res-line.ankunft LE tdate NO-LOCK
          BY reservation.zahldatum:
          RUN create-it.
            /*FD March 18, 2022 => ticket 7B1C21
            FIND FIRST bresline WHERE bresline.resnr EQ res-line.resnr
                AND bresline.reslinnr NE res-line.reslinnr
                AND (bresline.resstatus NE 9 OR bresline.resstatus NE 10) NO-LOCK NO-ERROR.
            IF NOT AVAILABLE bresline THEN RUN create-it.*/
        END.
      END.
    END. 
    /* SY: 15/11/2019 */
    ELSE IF deposittype = 3 THEN /* sorttype is always = 3 */
    DO:
        FOR EACH reservation WHERE reservation.activeflag LE 1 
           AND reservation.depositgef EQ 0 
           AND reservation.resnr GE lresnr NO-LOCK, 
           FIRST res-line WHERE res-line.resnr = reservation.resnr 
           AND (res-line.resstatus LE 5 OR res-line.resstatus = 9 
           OR res-line.resstatus = 10) AND res-line.ankunft GE fdate 
           AND res-line.name MATCHES ("*" + lname + "*")
           NO-LOCK BY res-line.ankunft:
           RUN create-it.
        END.
    END.
  END. 
 
  total-saldo = 0.
  arriv-saldo = 0.
  
  IF case-type = 1 THEN
  DO:
    IF depo-foreign THEN
    DO:
      FOR EACH depo-list:
        total-saldo = total-saldo + depo-list.depositgef - depo-list.depositbez - depo-list.depositbez2.
        FIND FIRST res-line WHERE res-line.resnr = depo-list.resnr
          AND res-line.active-flag = 1 NO-LOCK NO-ERROR.
        IF NOT AVAILABLE res-line THEN 
          arriv-saldo = arriv-saldo + depo-list.depositbez + depo-list.depositbez2.
      END.  
      ASSIGN
        total-saldo = total-saldo 
        arriv-saldo = arriv-saldo
      .
    END.
    ELSE
    DO:
      FOR EACH b1-list:
        total-saldo = total-saldo + b1-list.depositgef - b1-list.depositbez - b1-list.depositbez2.
        FIND FIRST res-line WHERE res-line.resnr = b1-list.resnr
            AND res-line.active-flag = 1 NO-LOCK NO-ERROR.
        IF NOT AVAILABLE res-line THEN 
          arriv-saldo = arriv-saldo + b1-list.depositbez + b1-list.depositbez2.
      END.
      ASSIGN
        total-saldo = total-saldo * xrate-change
        arriv-saldo = arriv-saldo * xrate-change
      .
    END.
  END.
  ELSE IF case-type = 2 THEN
  DO:
      FOR EACH b1-print:
          total-saldo = total-saldo + b1-print.depositgef - b1-print.depositbez - b1-print.depositbez2.
          FIND FIRST res-line WHERE res-line.resnr = b1-print.resnr
              AND res-line.active-flag = 1 NO-LOCK NO-ERROR.
          IF NOT AVAILABLE res-line THEN 
            arriv-saldo = arriv-saldo + b1-print.depositbez + b1-print.depositbez2.
      END.

      ASSIGN
          total-saldo = total-saldo * xrate-change
          arriv-saldo = arriv-saldo * xrate-change
          .
  END.
END.

PROCEDURE create-it:
  IF case-type = 1 THEN
  DO:
    IF depo-foreign THEN RUN create-depo.
    ELSE RUN create-b1.
  END.
  ELSE RUN create-b1-print.
END.

PROCEDURE create-depo:
    DEF VAR found-it        AS LOGICAL INITIAL YES NO-UNDO.
    DEF VAR exchg-rate      AS DECIMAL NO-UNDO.
    DEF VAR exchg-rate1     AS DECIMAL NO-UNDO.
    DEFINE VARIABLE loopi   AS INTEGER.
    DEFINE VARIABLE str     AS CHAR.

    FIND FIRST depo-list WHERE depo-list.resnr = reservation.resnr
        NO-ERROR.
    IF AVAILABLE depo-list THEN RETURN.

    CREATE depo-list.
    ASSIGN
        depo-list.group-str     = grpstr[INTEGER(reservation.grpflag) + 1]
        depo-list.resnr         = reservation.resnr
        depo-list.reserve-name  = reservation.NAME
        depo-list.grpname       = reservation.groupname
        depo-list.guestname     = res-line.NAME
        depo-list.ankunft       = res-line.ankunft
        depo-list.depositgef    = reservation.depositgef
        depo-list.bal           = reservation.depositgef - reservation.depositbez - reservation.depositbez2
        depo-list.limitdate     = reservation.limitdate
        depo-list.datum1        = reservation.zahldatum
        depo-list.datum2        = reservation.zahldatum2
        depo-list.depositbez    = reservation.depositbez
        depo-list.depositbez2   = reservation.depositbez2.

    IF depo-list.datum1 LT bill-date AND depo-list.datum1 NE ? THEN
    DO:
        FIND FIRST exrate WHERE exrate.artnr = depo-curr AND exrate.datum 
            = depo-list.datum1 NO-LOCK NO-ERROR.
        IF AVAILABLE exrate THEN
            exchg-rate = exrate.betrag.
        ELSE found-it = NO.
    END.

    ELSE IF (depo-list.datum1 GE bill-date AND depo-list.datum1 NE ?) OR
        NOT found-it THEN
    DO:
        FIND FIRST waehrung WHERE waehrung.waehrungsnr = depo-curr NO-LOCK NO-ERROR.
        IF AVAILABLE waehrung THEN
            exchg-rate = waehrung.ankauf / waehrung.einheit.
    END.
    IF exchg-rate = 0 THEN exchg-rate = 1.

    depo-list.depo1 = reservation.depositbez * exchg-rate.
    found-it = YES.    

   IF depo-list.datum2 LT bill-date AND depo-list.datum2 NE ? THEN
   DO:
       FIND FIRST exrate WHERE exrate.artnr = depo-curr AND exrate.datum 
           = depo-list.datum2 NO-LOCK NO-ERROR.
       IF AVAILABLE exrate THEN
           exchg-rate = exrate.betrag.
       ELSE found-it = NO.
   END.

   ELSE IF (depo-list.datum2 GE bill-date AND depo-list.datum2 NE ?) OR
       NOT found-it THEN
   DO:
       FIND FIRST waehrung WHERE waehrung.waehrungsnr = depo-curr NO-LOCK NO-ERROR.
       IF AVAILABLE waehrung THEN
           exchg-rate = waehrung.ankauf / waehrung.einheit.
   END.

   IF exchg-rate = 0 THEN exchg-rate = 1.
   depo-list.depo2 = reservation.depositbez2 * exchg-rate.
   found-it = YES.

   ASSIGN             
        depo-list.abreise       = res-line.abreise
        depo-list.qty           = res-line.zimmeranz
        depo-list.rmrate        = res-line.zipreis
        depo-list.remark        = " "
        depo-list.stafid        = " "
        depo-list.adult         = res-line.erwach
        depo-list.rsv-status    = res-line.resstatus.

     
    FIND FIRST arrangement WHERE arrangement.arrangement = res-line.arrangement NO-LOCK NO-ERROR.
    IF AVAILABLE arrangement THEN depo-list.argt-code = arrangement.argt-bez.

    DO loopi = 1 TO NUM-ENTRIES(res-line.zimmer-wunsch,";") - 1:
        str = ENTRY(loopi, res-line.zimmer-wunsch, ";").
        IF SUBSTR(str,1,6) = "$CODE$" THEN DO:
            depo-list.rate-code  = SUBSTR(str,7).
            LEAVE.
        END.
    END.

    FIND FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr NO-LOCK NO-ERROR.
    IF AVAILABLE zimkateg THEN ASSIGN depo-list.rmtype = zimkateg.bezeichnung.
        
END.

PROCEDURE create-b1:
    DEFINE VARIABLE loopi   AS INTEGER.
    DEFINE VARIABLE str     AS CHAR.
    DEFINE VARIABLE datum   AS DATE.
    DEFINE VARIABLE post-it AS LOGICAL.
    
    FIND FIRST b1-list WHERE b1-list.resnr = reservation.resnr NO-ERROR.
    IF AVAILABLE b1-list THEN RETURN.

    CREATE b1-list.
    ASSIGN
        b1-list.grpflag       = reservation.grpflag
        b1-list.resnr         = reservation.resnr
        b1-list.reser-name    = reservation.name
        b1-list.groupname     = reservation.groupname
        b1-list.resli-name    = res-line.name
        b1-list.ankunft       = res-line.ankunft
        b1-list.limitdate     = reservation.limitdate
        b1-list.depositgef    = reservation.depositgef
        b1-list.depositbez    = reservation.depositbez
        b1-list.depositbez2   = reservation.depositbez2
        b1-list.zahldatum     = reservation.zahldatum
        b1-list.zahlkonto     = reservation.zahlkonto
        b1-list.zahldatum2    = reservation.zahldatum2
        b1-list.zahlkonto2    = reservation.zahlkonto2
        b1-list.abreise       = res-line.abreise
        b1-list.qty           = res-line.zimmeranz
        b1-list.rmrate        = res-line.zipreis
        b1-list.remark        = " "
        b1-list.stafid        = " "
        b1-list.adult         = res-line.erwach
        b1-list.zipreis       = res-line.zipreis
        b1-list.rsv-status    = res-line.resstatus.

     
    FIND FIRST arrangement WHERE arrangement.arrangement = res-line.arrangement NO-LOCK NO-ERROR.
    IF AVAILABLE arrangement THEN b1-list.argt-code = arrangement.argt-bez.

    DO loopi = 1 TO NUM-ENTRIES(res-line.zimmer-wunsch,";") - 1:
        str = ENTRY(loopi, res-line.zimmer-wunsch, ";").
        IF SUBSTR(str,1,6) = "$CODE$" THEN DO:
            b1-list.rate-code  = SUBSTR(str,7).
            LEAVE.
        END.
    END.

    FIND FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr NO-LOCK NO-ERROR.
    IF AVAILABLE zimkateg THEN ASSIGN b1-list.rmtype = zimkateg.bezeichnung.
    
    DO datum = res-line.ankunft TO res-line.abreise - 1:
        FOR EACH fixleist WHERE fixleist.resnr = res-line.resnr
            AND fixleist.reslinnr = res-line.reslinnr NO-LOCK: 
    
            RUN check-fixleist-posted(datum , fixleist.artnr, fixleist.departement, 
                                      fixleist.sequenz, fixleist.dekade, 
                                      fixleist.lfakt, OUTPUT post-it). 
               
            IF post-it THEN DO:
                b1-list.zipreis = b1-list.zipreis + (fixleist.betrag * fixleist.number).
            END.                
        END.
    END.

END.

PROCEDURE create-b1-print:
    DEFINE VARIABLE loopi   AS INTEGER.
    DEFINE VARIABLE str     AS CHAR.
    DEFINE VARIABLE datum   AS DATE.
    DEFINE VARIABLE post-it AS LOGICAL.
    
    FIND FIRST b1-print WHERE b1-print.resnr = reservation.resnr NO-ERROR.
    IF AVAILABLE b1-print THEN RETURN.
    CREATE b1-print.
    ASSIGN
        b1-print.grpflag       = reservation.grpflag
        b1-print.resnr         = reservation.resnr
        b1-print.reser-name    = reservation.name
        b1-print.groupname     = reservation.groupname
        b1-print.resli-name    = res-line.name
        b1-print.ankunft       = res-line.ankunft
        b1-print.limitdate     = reservation.limitdate
        b1-print.depositgef    = reservation.depositgef
        b1-print.depositbez    = reservation.depositbez
        b1-print.depositbez2   = reservation.depositbez2
        b1-print.zahldatum     = reservation.zahldatum
        b1-print.zahlkonto     = reservation.zahlkonto
        b1-print.zahldatum2    = reservation.zahldatum2
        b1-print.zahlkonto2    = reservation.zahlkonto2
        b1-print.abreise       = res-line.abreise
        b1-print.qty           = res-line.zimmeranz
        b1-print.rmrate        = res-line.zipreis
        b1-print.remark        = " "
        b1-print.stafid        = " "
        b1-print.adult         = res-line.erwach
        b1-print.zipreis       = res-line.zipreis
        b1-print.rsv-status    = res-line.resstatus.

    FIND FIRST arrangement WHERE arrangement.arrangement = res-line.arrangement NO-LOCK NO-ERROR.
    IF AVAILABLE arrangement THEN b1-print.argt-code = arrangement.argt-bez.

    DO loopi = 1 TO NUM-ENTRIES(res-line.zimmer-wunsch,";") - 1:
        str = ENTRY(loopi, res-line.zimmer-wunsch, ";").
        IF SUBSTR(str,1,6) = "$CODE$" THEN DO:
            b1-print.rate-code  = SUBSTR(str,7).
            LEAVE.
        END.
    END.

    FIND FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr NO-LOCK NO-ERROR.
    IF AVAILABLE zimkateg THEN ASSIGN b1-print.rmtype = zimkateg.bezeichnung.

    DO datum = res-line.ankunft TO res-line.abreise - 1:
        FOR EACH fixleist WHERE fixleist.resnr = res-line.resnr
            AND fixleist.reslinnr = res-line.reslinnr NO-LOCK: 
    
            RUN check-fixleist-posted(datum , fixleist.artnr, fixleist.departement, 
                                      fixleist.sequenz, fixleist.dekade, 
                                      fixleist.lfakt, OUTPUT post-it). 
                    
            IF post-it THEN DO:
                b1-print.zipreis = b1-print.zipreis + fixleist.betrag.
            END.                
        END.
    END.
END.

PROCEDURE check-fixleist-posted: 
DEFINE INPUT PARAMETER curr-date    AS DATE.
DEFINE INPUT PARAMETER artnr        AS INTEGER. 
DEFINE INPUT PARAMETER dept         AS INTEGER. 
DEFINE INPUT PARAMETER fakt-modus   AS INTEGER. 
DEFINE INPUT PARAMETER intervall    AS INTEGER. 
DEFINE INPUT PARAMETER lfakt        AS DATE. 
DEFINE OUTPUT PARAMETER post-it     AS LOGICAL INITIAL NO. 
DEFINE VARIABLE delta AS INTEGER. 
DEFINE VARIABLE start-date AS DATE. 
 
  IF fakt-modus = 1 THEN post-it = YES. 
  ELSE IF fakt-modus = 2 THEN 
  DO: 
    IF res-line.ankunft = curr-date THEN post-it = YES. 
  END. 
  ELSE IF fakt-modus = 3 THEN 
  DO: 
    IF (res-line.ankunft + 1) = curr-date THEN post-it = YES. 
  END. 
  ELSE IF fakt-modus = 4 THEN   /* 1st day OF month  */ 
  DO: 
    IF day(curr-date) EQ 1 THEN post-it = YES. 
  END. 
  ELSE IF fakt-modus = 5 THEN   /* LAST day OF month */ 
  DO: 
    IF day(curr-date + 1) EQ 1 THEN post-it = YES. 
  END. 
  ELSE IF fakt-modus = 6 THEN 
  DO: 
    IF lfakt = ? THEN delta = 0. 
    ELSE 
    DO: 
      delta = lfakt - res-line.ankunft. 
      IF delta LT 0 THEN delta = 0. 
    END. 
    start-date = res-line.ankunft + delta. 
    IF (res-line.abreise - start-date) LT intervall 
      THEN start-date = res-line.ankunft. 
    IF curr-date LE (start-date + (intervall - 1)) 
    THEN post-it = YES. 
    IF curr-date LT start-date THEN post-it = no. /* may NOT post !! */ 
  END. 
END. 

