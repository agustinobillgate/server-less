DEFINE BUFFER gmember FOR guest. 
 
DEFINE TEMP-TABLE telop-list
    FIELD resli-wabkurz   LIKE res-line.wabkurz
    FIELD voucher-nr      LIKE res-line.voucher-nr
    FIELD grpflag         LIKE reservation.grpflag
    FIELD reser-name      LIKE reservation.name
    FIELD zinr            LIKE res-line.zinr 
    FIELD resli-name      LIKE res-line.name
    FIELD segmentcode     LIKE reservation.segmentcode 
    FIELD nation1         LIKE gmember.nation1
    FIELD resstatus       LIKE res-line.resstatus 
    FIELD l-zuordnung     LIKE res-line.l-zuordnung[3]
    FIELD ankunft         LIKE res-line.ankunft 
    FIELD abreise         LIKE res-line.abreise 
    FIELD ankzeit         LIKE res-line.ankzeit
    FIELD abreisezeit     LIKE res-line.abreisezeit
    FIELD flight-nr       LIKE res-line.flight-nr
    FIELD zimmeranz       LIKE res-line.zimmeranz 
    FIELD kurzbez         LIKE zimkateg.kurzbez 
    FIELD erwachs         LIKE res-line.erwachs
    FIELD kind1           LIKE res-line.kind1
    FIELD gratis          LIKE res-line.gratis
    FIELD waeh-wabkurz    LIKE waehrung.wabkurz
    FIELD resnr           LIKE res-line.resnr
    FIELD reslinnr        LIKE res-line.reslinnr
    FIELD betrieb-gast    LIKE res-line.betrieb-gast
    FIELD groupname       LIKE reservation.groupname 
    FIELD cancelled-id    LIKE res-line.cancelled-id 
    FIELD changed-id      LIKE res-line.changed-id 
    FIELD bemerk          LIKE res-line.bemerk
    FIELD active-flag     LIKE res-line.active-flag
    FIELD gastnrmember    LIKE res-line.gastnrmember
    FIELD gastnr          LIKE res-line.gastnr
    FIELD betrieb-gastmem LIKE res-line.betrieb-gastmem
    FIELD pseudofix       LIKE res-line.pseudofix
    FIELD zikatnr         LIKE res-line.zikatnr
    FIELD arrangement     LIKE res-line.arrangement
    FIELD zipreis         LIKE res-line.zipreis
    FIELD resname         AS CHAR FORMAT "x(25)"
    FIELD address         AS CHAR FORMAT "x(25)"
    FIELD city            AS CHAR FORMAT "x(25)"
    FIELD b-comments      AS CHAR
    FIELD message-flag    AS LOGICAL INIT NO
    FIELD flag-color      AS INTEGER INIT 0
    FIELD flight1         AS CHARACTER
    FIELD eta             AS CHARACTER
    FIELD flight2         AS CHARACTER
    FIELD etd             AS CHARACTER
.

DEF INPUT PARAMETER sorttype AS INTEGER.
DEF INPUT PARAMETER room     AS CHAR.
DEF INPUT PARAMETER fdate1   AS DATE.
DEF INPUT PARAMETER fdate2   AS DATE.
DEF INPUT PARAMETER ci-date  AS DATE.
DEF INPUT PARAMETER lname    AS CHAR.
DEF INPUT PARAMETER last-sort AS INT.
DEF INPUT PARAMETER lnat     AS CHAR.
DEF INPUT PARAMETER lresnr   AS INT.


DEF OUTPUT PARAMETER troom   AS CHAR.
DEF OUTPUT PARAMETER tpax    AS CHAR.
DEF OUTPUT PARAMETER TABLE FOR telop-list.


DEFINE VARIABLE rmlen       AS INTEGER. 
DEFINE VARIABLE temp-total  AS INTEGER INITIAL 0.
DEFINE VARIABLE temp-total2 AS INTEGER INITIAL 0.

IF sorttype = 1   /* Reservation  */  THEN DO:
  RUN disp-arl1.       
  /*RUN count-al1.*/
END.
ELSE IF sorttype = 2 THEN do:
  RUN disp-arl2.  /* Inhouse Guest */ 
  /*RUN COUNT-all2.*/
END.
ELSE IF sorttype = 4 THEN DO:
    RUN disp-arl4.  /* departure Today */ 
    /*RUN count-all4.*/
END.
ELSE IF sorttype = 5 THEN DO:
  RUN disp-arl5.  /* Departed Guests */
  /*RUN count-all5.*/
END.
  
ELSE IF sorttype = 6 THEN do:
  RUN disp-arl6.  /* All Today */ 
  /*RUN count-all6.*/
END.


PROCEDURE disp-arl1: 
  DEFINE VARIABLE to-name AS CHAR. 
  rmlen = length(room). 
  IF fdate1 = ? THEN 
  DO: 
    IF fdate2 NE ? THEN fdate1 = fdate2. 
    ELSE 
    DO: 
      fdate1 = ci-date. 
      fdate2 = ci-date + 30. 
    END. 
  END. 
  IF fdate2 = ? THEN 
  DO: 
    IF fdate1 NE ? THEN fdate2 = fdate1. 
    ELSE 
    DO: 
      fdate1 = ci-date. 
      fdate2 = ci-date + 30. 
    END. 
  END. 
  IF lname NE "" AND SUBSTR(lname,1,1) NE "*" THEN 
    to-name = chr(asc(SUBSTR(lname,1,1)) + 1). 
 
  IF last-sort = 1 THEN 
  DO: 
    IF lname = "" THEN DO:
        FOR EACH res-line WHERE 
           res-line.active-flag = 0 AND res-line.ankunft GE fdate1 
           AND res-line.ankunft LE fdate2 NO-LOCK, 
           FIRST waehrung WHERE waehrung.waehrungsnr = res-line.betriebsnr 
            NO-LOCK, 
           FIRST reservation WHERE reservation.resnr = res-line.resnr, 
           FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr, 
           FIRST gmember WHERE gmember.gastnr = res-line.gastnrmember 
           NO-LOCK BY (res-line.kontakt-nr * res-line.resnr) BY res-line.resstatus 
           BY res-line.NAME:
                RUN assign-it.
                IF res-line.resstatus NE 13 AND res-line.resstatus NE 11 AND res-line.l-zuordnung[3] NE 1 THEN
                    temp-total2 = temp-total2 + res-line.zimmeranz.
                ASSIGN temp-total = INT(temp-total) + INT(res-line.erwachs).
        END.
        ASSIGN troom = string(temp-total2)
               tpax  = string(temp-total). 
    END.
    ELSE IF lname NE "" AND SUBSTR(lname,1,1) NE "*" THEN DO:
        FOR EACH res-line WHERE 
           res-line.active-flag = 0 AND res-line.ankunft GE fdate1 
           AND res-line.ankunft LE fdate2 AND res-line.name GE lname 
           AND res-line.name LE to-name NO-LOCK, 
           FIRST waehrung WHERE waehrung.waehrungsnr = res-line.betriebsnr 
            NO-LOCK, 
           FIRST reservation WHERE reservation.resnr = res-line.resnr, 
           FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr, 
           FIRST gmember WHERE gmember.gastnr = res-line.gastnrmember 
           NO-LOCK BY res-line.name:
                RUN assign-it.

                IF res-line.resstatus NE 13 AND res-line.resstatus NE 11 AND res-line.l-zuordnung[3] NE 1 THEN
                    temp-total2 = temp-total2 + res-line.zimmeranz.
                ASSIGN temp-total = INT(temp-total) + INT(res-line.erwachs).
        END.
         ASSIGN troom = string(temp-total2)
                tpax  = string(temp-total).
    END.
    
    ELSE IF lname NE "" AND SUBSTR(lname,1,1) EQ "*" THEN DO:
        FOR EACH res-line WHERE 
           res-line.active-flag = 0 AND res-line.ankunft GE fdate1 
           AND res-line.ankunft LE fdate2 AND res-line.name MATCHES(lname) NO-LOCK, 
           FIRST waehrung WHERE waehrung.waehrungsnr = res-line.betriebsnr 
            NO-LOCK, 
           FIRST reservation WHERE reservation.resnr = res-line.resnr, 
           FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr, 
           FIRST gmember WHERE gmember.gastnr = res-line.gastnrmember 
           NO-LOCK BY res-line.name:
                RUN assign-it.
                IF res-line.resstatus NE 13 AND res-line.resstatus NE 11 AND res-line.l-zuordnung[3] NE 1 THEN
                    temp-total2 = temp-total2 + res-line.zimmeranz.
                ASSIGN temp-total = INT(temp-total) + INT(res-line.erwachs).
        END.
        ASSIGN troom = string(temp-total2)
               tpax  = string(temp-total).
    END.
    
  END. 
  ELSE IF last-sort = 2 THEN 
  DO: 
    IF lname = "" THEN DO:
        FOR EACH res-line WHERE 
           res-line.active-flag = 0 AND res-line.ankunft GE fdate1 
           AND res-line.ankunft LE fdate2 NO-LOCK, 
           FIRST waehrung WHERE waehrung.waehrungsnr = res-line.betriebsnr 
           NO-LOCK, 
           FIRST reservation WHERE reservation.resnr = res-line.resnr, 
           FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr, 
           FIRST gmember WHERE gmember.gastnr = res-line.gastnrmember 
           NO-LOCK BY reservation.NAME /*res-line.resname*/ BY res-line.ankunft 
           BY res-line.resnr BY (res-line.kontakt-nr * res-line.resnr) 
           BY res-line.resstatus BY res-line.NAME:
                RUN assign-it.
                IF res-line.resstatus NE 13 AND res-line.resstatus NE 11 AND res-line.l-zuordnung[3] NE 1 THEN
                    temp-total2 = temp-total2 + res-line.zimmeranz.
                ASSIGN temp-total = INT(temp-total) + INT(res-line.erwachs).
        END.
        ASSIGN troom = string(temp-total2)
               tpax  = string(temp-total).
    END.
    ELSE IF lname NE "" AND SUBSTR(lname,1,1) NE "*" THEN DO:
        FOR EACH res-line WHERE 
           res-line.active-flag = 0 AND res-line.ankunft GE fdate1 
           AND res-line.ankunft LE fdate2 /*AND res-line.resname reservation.NAME GE lname 
           AND reservation.NAME res-line.resname LE to-name */NO-LOCK, 
           FIRST waehrung WHERE waehrung.waehrungsnr = res-line.betriebsnr 
           NO-LOCK, 
           FIRST reservation WHERE reservation.resnr = res-line.resnr AND reservation.NAME GE lname
            AND reservation.NAME LE to-name, 
           FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr, 
           FIRST gmember WHERE gmember.gastnr = res-line.gastnrmember 
           NO-LOCK BY /*res-line.resname*/reservation.NAME BY res-line.ankunft 
           BY res-line.resnr BY (res-line.kontakt-nr * res-line.resnr) 
           BY res-line.resstatus BY res-line.NAME:
                RUN assign-it.
                IF res-line.resstatus NE 13 AND res-line.resstatus NE 11 AND res-line.l-zuordnung[3] NE 1 THEN
                    temp-total2 = temp-total2 + res-line.zimmeranz.
                ASSIGN temp-total = INT(temp-total) + INT(res-line.erwachs).
        END.
        ASSIGN troom = string(temp-total2)
               tpax  = string(temp-total).
    END.
    ELSE IF lname NE "" AND SUBSTR(lname,1,1) EQ "*" THEN DO: 
        FOR EACH res-line WHERE 
           res-line.active-flag = 0 AND res-line.ankunft GE fdate1 
           AND res-line.ankunft LE fdate2 AND res-line.resname MATCHES(lname) 
           NO-LOCK, 
           FIRST waehrung WHERE waehrung.waehrungsnr = res-line.betriebsnr 
           NO-LOCK, 
           FIRST reservation WHERE reservation.resnr = res-line.resnr, 
           FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr, 
           FIRST gmember WHERE gmember.gastnr = res-line.gastnrmember 
           NO-LOCK BY res-line.resname BY res-line.ankunft 
           BY res-line.resnr BY (res-line.kontakt-nr * res-line.resnr) 
           BY res-line.resstatus BY res-line.NAME:
                RUN assign-it.
                IF res-line.resstatus NE 13 AND res-line.resstatus NE 11 AND res-line.l-zuordnung[3] NE 1 THEN
                        temp-total2 = temp-total2 + res-line.zimmeranz.
                ASSIGN temp-total = INT(temp-total) + INT(res-line.erwachs).
    
        END.
        ASSIGN troom = string(temp-total2)
               tpax  = string(temp-total).
    END.
  END. 
  ELSE IF last-sort = 3 AND lnat EQ "" THEN 
  DO: 
    IF lname = "" THEN DO:
        FOR EACH res-line WHERE res-line.active-flag = 0 
          AND res-line.ankunft EQ fdate2 NO-LOCK, 
          FIRST waehrung WHERE waehrung.waehrungsnr = res-line.betriebsnr 
          NO-LOCK, 
          FIRST reservation WHERE reservation.resnr = res-line.resnr, 
          FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr, 
          FIRST gmember WHERE gmember.gastnr = res-line.gastnrmember 
          NO-LOCK BY gmember.nation1 BY (res-line.kontakt-nr * res-line.resnr) 
          BY res-line.resstatus BY res-line.NAME:
                RUN assign-it.
                IF res-line.resstatus NE 13 AND res-line.resstatus NE 11 AND res-line.l-zuordnung[3] NE 1 THEN
                        temp-total2 = temp-total2 + res-line.zimmeranz.
                ASSIGN temp-total = INT(temp-total) + INT(res-line.erwachs).
        END.
        ASSIGN troom = string(temp-total2)
               tpax  = string(temp-total).
    END.
    ELSE IF lname NE "" AND SUBSTR(lname,1,1) NE "*" THEN DO:
        FOR EACH res-line WHERE res-line.active-flag = 0 
          AND res-line.ankunft EQ fdate2 
          AND res-line.name GE lname AND res-line.name LE to-name NO-LOCK, 
          FIRST waehrung WHERE waehrung.waehrungsnr = res-line.betriebsnr 
          NO-LOCK, 
          FIRST reservation WHERE reservation.resnr = res-line.resnr, 
          FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr, 
          FIRST gmember WHERE gmember.gastnr = res-line.gastnrmember 
          NO-LOCK BY gmember.nation1 BY (res-line.kontakt-nr * res-line.resnr) 
          BY res-line.resstatus BY res-line.NAME:
                RUN assign-it.
                IF res-line.resstatus NE 13 AND res-line.resstatus NE 11 AND res-line.l-zuordnung[3] NE 1 THEN
                        temp-total2 = temp-total2 + res-line.zimmeranz.
                ASSIGN temp-total = INT(temp-total) + INT(res-line.erwachs).
        END.
        ASSIGN troom = string(temp-total2)
               tpax  = string(temp-total).
    END.    
    ELSE IF lname NE "" AND SUBSTR(lname,1,1) EQ "*" THEN DO:
        FOR EACH res-line WHERE res-line.active-flag = 0 
          AND res-line.ankunft EQ fdate2 
          AND res-line.name MATCHES(lname) NO-LOCK, 
          FIRST waehrung WHERE waehrung.waehrungsnr = res-line.betriebsnr 
          NO-LOCK, 
          FIRST reservation WHERE reservation.resnr = res-line.resnr, 
          FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr, 
          FIRST gmember WHERE gmember.gastnr = res-line.gastnrmember 
          NO-LOCK BY gmember.nation1 BY (res-line.kontakt-nr * res-line.resnr) 
          BY res-line.resstatus BY res-line.NAME:
                RUN assign-it.
                IF res-line.resstatus NE 13 AND res-line.resstatus NE 11 AND res-line.l-zuordnung[3] NE 1 THEN
                        temp-total2 = temp-total2 + res-line.zimmeranz.
                ASSIGN temp-total = INT(temp-total) + INT(res-line.erwachs).
        END.
        ASSIGN troom = string(temp-total2)
               tpax  = string(temp-total).
    END.
    
  END. 
  ELSE IF last-sort = 3 AND lnat NE "" THEN 
  DO: 
    IF lname = "" THEN DO:
        FOR EACH res-line WHERE res-line.active-flag = 0 
          AND res-line.ankunft EQ fdate2 NO-LOCK, 
          FIRST waehrung WHERE waehrung.waehrungsnr = res-line.betriebsnr 
          NO-LOCK, 
          FIRST reservation WHERE reservation.resnr = res-line.resnr, 
          FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr, 
          FIRST gmember WHERE gmember.gastnr = res-line.gastnrmember 
          AND gmember.nation1 = lnat NO-LOCK 
          BY (res-line.kontakt-nr * res-line.resnr) 
          BY res-line.resstatus BY res-line.NAME:
                RUN assign-it.
                IF res-line.resstatus NE 13 AND res-line.resstatus NE 11 AND res-line.l-zuordnung[3] NE 1 THEN
                        temp-total2 = temp-total2 + res-line.zimmeranz.
                ASSIGN temp-total = INT(temp-total) + INT(res-line.erwachs).
        END.
        ASSIGN troom = string(temp-total2)
               tpax  = string(temp-total).
    END.    
    ELSE IF lname NE "" AND SUBSTR(lname,1,1) NE "*" THEN DO:
        FOR EACH res-line WHERE res-line.active-flag = 0 
          AND res-line.ankunft EQ fdate2 
          AND res-line.name GE lname AND res-line.name LE to-name NO-LOCK, 
          FIRST waehrung WHERE waehrung.waehrungsnr = res-line.betriebsnr 
          NO-LOCK, 
          FIRST reservation WHERE reservation.resnr = res-line.resnr, 
          FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr, 
          FIRST gmember WHERE gmember.gastnr = res-line.gastnrmember 
          AND gmember.nation1 = lnat NO-LOCK BY gmember.nation1
          BY (res-line.kontakt-nr * res-line.resnr) 
          BY res-line.resstatus BY res-line.NAME:
                RUN assign-it.
                IF res-line.resstatus NE 13 AND res-line.resstatus NE 11 AND res-line.l-zuordnung[3] NE 1 THEN
                        temp-total2 = temp-total2 + res-line.zimmeranz.
                ASSIGN temp-total = INT(temp-total) + INT(res-line.erwachs).
        END.
        ASSIGN troom = string(temp-total2)
               tpax  = string(temp-total).
    END.    
    ELSE IF lname NE "" AND SUBSTR(lname,1,1) EQ "*" THEN DO:
        FOR EACH res-line WHERE res-line.active-flag = 0 
          AND res-line.ankunft EQ fdate2 
          AND res-line.name MATCHES(lname) NO-LOCK, 
          FIRST waehrung WHERE waehrung.waehrungsnr = res-line.betriebsnr 
          NO-LOCK, 
          FIRST reservation WHERE reservation.resnr = res-line.resnr, 
          FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr, 
          FIRST gmember WHERE gmember.gastnr = res-line.gastnrmember 
          AND gmember.nation1 = lnat NO-LOCK BY gmember.nation1
          BY (res-line.kontakt-nr * res-line.resnr) 
          BY res-line.resstatus BY res-line.NAME:
                RUN assign-it.
                IF res-line.resstatus NE 13 AND res-line.resstatus NE 11 AND res-line.l-zuordnung[3] NE 1 THEN
                        temp-total2 = temp-total2 + res-line.zimmeranz.
                ASSIGN temp-total = INT(temp-total) + INT(res-line.erwachs).
        END.
        ASSIGN troom = string(temp-total2)
               tpax  = string(temp-total).
    END.    
  END. 
  ELSE IF last-sort = 4 THEN 
  DO: 
    IF lresnr = 0 THEN DO:
        FOR EACH res-line WHERE res-line.active-flag = 0 
          AND res-line.ankunft EQ ci-date NO-LOCK, 
          FIRST waehrung WHERE waehrung.waehrungsnr = res-line.betriebsnr 
          NO-LOCK, 
          FIRST reservation WHERE reservation.resnr = res-line.resnr, 
          FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr, 
          FIRST gmember WHERE gmember.gastnr = res-line.gastnrmember 
          NO-LOCK BY res-line.resnr
          BY (res-line.kontakt-nr * res-line.resnr) 
          BY res-line.resstatus BY res-line.NAME:
                RUN assign-it.
                IF res-line.resstatus NE 13 AND res-line.resstatus NE 11 AND res-line.l-zuordnung[3] NE 1 THEN
                        temp-total2 = temp-total2 + res-line.zimmeranz.
                ASSIGN temp-total = INT(temp-total) + INT(res-line.erwachs).
        END.
        ASSIGN troom = string(temp-total2)
               tpax  = string(temp-total).
    END.    
    ELSE DO:
        FOR EACH res-line WHERE res-line.active-flag = 0 
          AND res-line.resnr EQ lresnr NO-LOCK, 
          FIRST waehrung WHERE waehrung.waehrungsnr = res-line.betriebsnr 
          NO-LOCK, 
          FIRST reservation WHERE reservation.resnr = res-line.resnr, 
          FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr, 
          FIRST gmember WHERE gmember.gastnr = res-line.gastnrmember 
          NO-LOCK BY (res-line.kontakt-nr * res-line.resnr) 
          BY res-line.resstatus BY res-line.NAME:
                RUN assign-it.
                IF res-line.resstatus NE 13 AND res-line.resstatus NE 11 AND res-line.l-zuordnung[3] NE 1 THEN
                        temp-total2 = temp-total2 + res-line.zimmeranz.
                ASSIGN temp-total = INT(temp-total) + INT(res-line.erwachs).
        END.
        ASSIGN troom = string(temp-total2)
               tpax  = string(temp-total).
    END.
  END. 
END. 
 
PROCEDURE disp-arl2: 
  DEFINE VARIABLE to-name AS CHAR. 
  rmlen = length(room). 
  IF lname NE "" AND SUBSTR(lname,1,1) NE "*" THEN 
    to-name = chr(asc(SUBSTR(lname,1,1)) + 1). 
 
  IF last-sort = 1 THEN 
  DO: 
    IF room NE "" THEN 
    DO: 
      IF lname = "" THEN DO:
        FOR EACH res-line WHERE 
           res-line.active-flag = 1  AND res-line.resstatus NE 12 /* Malik Serverless 285 : resstatus -> res-line.resstatus */
           AND (SUBSTR(res-line.zinr,1,INTEGER(rmlen))) GE room 
           AND res-line.ankunft LE ci-date AND res-line.abreise GE ci-date 
           NO-LOCK, 
           FIRST waehrung WHERE waehrung.waehrungsnr = res-line.betriebsnr 
           NO-LOCK, 
           FIRST reservation WHERE reservation.resnr = res-line.resnr, 
           FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr, 
           FIRST gmember WHERE gmember.gastnr = res-line.gastnrmember 
           NO-LOCK BY res-line.zinr BY (res-line.kontakt-nr * res-line.resnr) 
           BY res-line.resstatus BY res-line.NAME:
                RUN assign-it.
                IF res-line.resstatus NE 13 AND res-line.resstatus NE 11 AND res-line.l-zuordnung[3] NE 1 THEN
                        temp-total2 = temp-total2 + res-line.zimmeranz.
                ASSIGN temp-total = INT(temp-total) + INT(res-line.erwachs).
          END.
          ASSIGN troom = string(temp-total2)
                 tpax  = string(temp-total).
      END.      
      ELSE IF lname NE "" AND SUBSTR(lname,1,1) EQ "*" THEN DO:
        FOR EACH res-line WHERE 
           res-line.active-flag = 1  AND res-line.resstatus NE 12 
           AND (SUBSTR(res-line.zinr,1,INTEGER(rmlen))) GE room 
           AND res-line.name MATCHES(lname) 
           AND res-line.ankunft LE ci-date AND res-line.abreise GE ci-date NO-LOCK, 
           FIRST waehrung WHERE waehrung.waehrungsnr = res-line.betriebsnr 
           NO-LOCK, 
           FIRST reservation WHERE reservation.resnr = res-line.resnr, 
           FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr, 
           FIRST gmember WHERE gmember.gastnr = res-line.gastnrmember 
           NO-LOCK BY res-line.zinr BY (res-line.kontakt-nr * res-line.resnr) 
           BY res-line.resstatus BY res-line.NAME:
                RUN assign-it.
                IF res-line.resstatus NE 13 AND res-line.resstatus NE 11 AND res-line.l-zuordnung[3] NE 1 THEN
                        temp-total2 = temp-total2 + res-line.zimmeranz.
                ASSIGN temp-total = INT(temp-total) + INT(res-line.erwachs).
          END.
          ASSIGN troom = string(temp-total2)
                 tpax  = string(temp-total).
      END.      
      ELSE IF lname NE "" AND SUBSTR(lname,1,1) NE "*" THEN 
      DO:
        IF ci-date NE ? THEN DO : /* Malik Serverless 285 */
            FOR EACH res-line WHERE 
              res-line.active-flag = 1  AND res-line.resstatus NE 12 
              AND (SUBSTR(res-line.zinr,1,INTEGER(rmlen))) GE room 
              AND res-line.name GE lname AND res-line.name LE to-name 
              AND res-line.ankunft LE ci-date AND res-line.abreise GE ci-date NO-LOCK, 
              FIRST waehrung WHERE waehrung.waehrungsnr = res-line.betriebsnr 
              NO-LOCK, 
              FIRST reservation WHERE reservation.resnr = res-line.resnr, 
              FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr, 
              FIRST gmember WHERE gmember.gastnr = res-line.gastnrmember 
              NO-LOCK BY res-line.zinr BY (res-line.kontakt-nr * res-line.resnr) 
              BY res-line.resstatus BY res-line.NAME:
                  RUN assign-it.
                  IF res-line.resstatus NE 13 AND res-line.resstatus NE 11 AND res-line.l-zuordnung[3] NE 1 THEN
                            temp-total2 = temp-total2 + res-line.zimmeranz.
                  ASSIGN temp-total = INT(temp-total) + INT(res-line.erwachs).
            END.
            ASSIGN troom = string(temp-total2)
                   tpax  = string(temp-total).
        END.       
      END.
    END. 
    ELSE IF room = "" THEN 
    DO: 
      IF lname = "" THEN DO:
        FOR EACH res-line WHERE 
           res-line.active-flag = 1  AND res-line.resstatus NE 12 
           AND res-line.ankunft LE ci-date AND res-line.abreise GE ci-date, 
           FIRST waehrung WHERE waehrung.waehrungsnr = res-line.betriebsnr 
           NO-LOCK, 
           FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
           FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr, 
           FIRST gmember WHERE gmember.gastnr = res-line.gastnrmember 
           NO-LOCK BY (res-line.kontakt-nr * res-line.resnr) 
           BY res-line.resstatus BY res-line.NAME:
                RUN assign-it.
                IF res-line.resstatus NE 13 AND res-line.resstatus NE 11 AND res-line.l-zuordnung[3] NE 1 THEN
                            temp-total2 = temp-total2 + res-line.zimmeranz.
                ASSIGN temp-total = INT(temp-total) + INT(res-line.erwachs).
          END.
          ASSIGN troom = string(temp-total2)
                 tpax  = string(temp-total).
      END.      
      ELSE IF lname NE "" AND SUBSTR(lname,1,1) EQ "*" THEN DO:
          FOR EACH res-line WHERE 
           res-line.active-flag = 1  AND res-line.resstatus NE 12 
           AND res-line.name MATCHES(lname) 
           AND res-line.ankunft LE ci-date AND res-line.abreise GE ci-date NO-LOCK, 
           FIRST waehrung WHERE waehrung.waehrungsnr = res-line.betriebsnr 
           NO-LOCK, 
           FIRST reservation WHERE reservation.resnr = res-line.resnr, 
           FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr, 
           FIRST gmember WHERE gmember.gastnr = res-line.gastnrmember 
           NO-LOCK BY res-line.name:
                RUN assign-it.
                IF res-line.resstatus NE 13 AND res-line.resstatus NE 11 AND res-line.l-zuordnung[3] NE 1 THEN
                            temp-total2 = temp-total2 + res-line.zimmeranz.
                ASSIGN temp-total = INT(temp-total) + INT(res-line.erwachs).
          END.
          ASSIGN troom = string(temp-total2)
                 tpax  = string(temp-total).
      END.
      ELSE IF lname NE "" AND SUBSTR(lname,1,1) NE "*" THEN DO:
         FOR EACH res-line WHERE 
           res-line.active-flag = 1  AND res-line.resstatus NE 12 
           AND res-line.name GE lname AND res-line.name LE to-name 
           AND res-line.ankunft LE ci-date AND res-line.abreise GE ci-date NO-LOCK, 
           FIRST waehrung WHERE waehrung.waehrungsnr = res-line.betriebsnr 
           NO-LOCK, 
           FIRST reservation WHERE reservation.resnr = res-line.resnr, 
           FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr, 
           FIRST gmember WHERE gmember.gastnr = res-line.gastnrmember 
           NO-LOCK BY res-line.name:
                RUN assign-it.
                IF res-line.resstatus NE 13 AND res-line.resstatus NE 11 AND res-line.l-zuordnung[3] NE 1 THEN
                            temp-total2 = temp-total2 + res-line.zimmeranz.
                ASSIGN temp-total = INT(temp-total) + INT(res-line.erwachs).
          END.
          ASSIGN troom = string(temp-total2)
                 tpax  = string(temp-total).
      END.
    END. 
  END. 
  ELSE IF last-sort = 2 THEN 
  DO: 
    IF lname = "" AND room = "" THEN DO:
        FOR EACH res-line WHERE 
           res-line.active-flag = 1 AND res-line.resstatus NE 12 
           AND (SUBSTR(res-line.zinr,1,INTEGER(rmlen))) GE room 
           AND res-line.ankunft LE ci-date AND res-line.abreise GE ci-date NO-LOCK, 
           FIRST waehrung WHERE waehrung.waehrungsnr = res-line.betriebsnr 
           NO-LOCK, 
           FIRST reservation WHERE reservation.resnr = res-line.resnr, 
           FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr, 
           FIRST gmember WHERE gmember.gastnr = res-line.gastnrmember 
           NO-LOCK BY res-line.resname BY res-line.resnr BY res-line.zinr
           BY (res-line.kontakt-nr * res-line.resnr) BY res-line.resstatus 
           BY res-line.NAME:
                RUN assign-it.

                IF res-line.resstatus NE 13 AND res-line.resstatus NE 11 AND res-line.l-zuordnung[3] NE 1 THEN
                            temp-total2 = temp-total2 + res-line.zimmeranz.
                ASSIGN temp-total = INT(temp-total) + INT(res-line.erwachs).
        END.
        ASSIGN troom = string(temp-total2)
               tpax  = string(temp-total).
    END.
    ELSE IF lname = "" AND room NE "" THEN DO:
        FOR EACH res-line WHERE 
           res-line.active-flag = 1 AND res-line.resstatus NE 12 
           AND (SUBSTR(res-line.zinr,1,INTEGER(rmlen))) GE room 
           AND res-line.ankunft LE ci-date AND res-line.abreise GE ci-date NO-LOCK, 
           FIRST waehrung WHERE waehrung.waehrungsnr = res-line.betriebsnr 
           NO-LOCK, 
           FIRST reservation WHERE reservation.resnr = res-line.resnr, 
           FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr, 
           FIRST gmember WHERE gmember.gastnr = res-line.gastnrmember 
           NO-LOCK BY res-line.zinr BY res-line.resname
           BY (res-line.kontakt-nr * res-line.resnr) BY res-line.resstatus 
           BY res-line.NAME:
                RUN assign-it.
                IF res-line.resstatus NE 13 AND res-line.resstatus NE 11 AND res-line.l-zuordnung[3] NE 1 THEN
                            temp-total2 = temp-total2 + res-line.zimmeranz.
                ASSIGN temp-total = INT(temp-total) + INT(res-line.erwachs).
        END.
        ASSIGN troom = string(temp-total2)
               tpax  = string(temp-total).
    END.
    ELSE IF lname NE "" AND SUBSTR(lname,1,1) EQ "*" THEN DO:
        FOR EACH res-line WHERE 
           res-line.active-flag = 1  AND res-line.resstatus NE 12 
           AND (SUBSTR(res-line.zinr,1,INTEGER(rmlen))) GE room 
           AND res-line.resname MATCHES(lname) 
           AND res-line.ankunft LE ci-date AND res-line.abreise GE ci-date NO-LOCK, 
           FIRST waehrung WHERE waehrung.waehrungsnr = res-line.betriebsnr 
           NO-LOCK, 
           FIRST reservation WHERE reservation.resnr = res-line.resnr, 
           FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr, 
           FIRST gmember WHERE gmember.gastnr = res-line.gastnrmember 
           NO-LOCK BY res-line.resname BY res-line.zinr
           BY (res-line.kontakt-nr * res-line.resnr) 
           BY res-line.resstatus BY res-line.NAME:
                RUN assign-it.
                IF res-line.resstatus NE 13 AND res-line.resstatus NE 11 AND res-line.l-zuordnung[3] NE 1 THEN
                            temp-total2 = temp-total2 + res-line.zimmeranz.
                ASSIGN temp-total = INT(temp-total) + INT(res-line.erwachs).
        END.
        ASSIGN troom = string(temp-total2)
               tpax  = string(temp-total).
    END.    
    ELSE IF lname NE "" AND SUBSTR(lname,1,1) NE "*" THEN DO:
        FOR EACH res-line WHERE 
           res-line.active-flag = 1  AND res-line.resstatus NE 12 
           AND (SUBSTR(res-line.zinr,1,INTEGER(rmlen))) GE room 
           AND res-line.resname GE lname AND res-line.resname LE to-name 
           AND res-line.ankunft LE ci-date AND res-line.abreise GE ci-date NO-LOCK, 
           FIRST waehrung WHERE waehrung.waehrungsnr = res-line.betriebsnr 
           NO-LOCK, 
           FIRST reservation WHERE reservation.resnr = res-line.resnr, 
           FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr, 
           FIRST gmember WHERE gmember.gastnr = res-line.gastnrmember 
           NO-LOCK BY res-line.resname BY res-line.zinr
           BY (res-line.kontakt-nr * res-line.resnr) 
           BY res-line.resstatus BY res-line.NAME:
                RUN assign-it.
                IF res-line.resstatus NE 13 AND res-line.resstatus NE 11 AND res-line.l-zuordnung[3] NE 1 THEN
                            temp-total2 = temp-total2 + res-line.zimmeranz.
                ASSIGN temp-total = INT(temp-total) + INT(res-line.erwachs).
        END.
        ASSIGN troom = string(temp-total2)
               tpax  = string(temp-total).
    END.    
  END. 
  ELSE IF last-sort = 3 AND lnat = "" THEN 
  DO: 
    IF lname = "" THEN DO:
        FOR EACH res-line WHERE 
           res-line.active-flag = 1 AND res-line.resstatus NE 12 
           AND res-line.ankunft LE ci-date AND res-line.abreise GE ci-date NO-LOCK, 
           FIRST waehrung WHERE waehrung.waehrungsnr = res-line.betriebsnr 
           NO-LOCK, 
           FIRST reservation WHERE reservation.resnr = res-line.resnr, 
           FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr, 
           FIRST gmember WHERE gmember.gastnr = res-line.gastnrmember 
           NO-LOCK BY gmember.nation1 BY (res-line.kontakt-nr * res-line.resnr) 
           BY res-line.resstatus BY res-line.NAME:
                RUN assign-it.
                IF res-line.resstatus NE 13 AND res-line.resstatus NE 11 AND res-line.l-zuordnung[3] NE 1 THEN
                            temp-total2 = temp-total2 + res-line.zimmeranz.
                ASSIGN temp-total = INT(temp-total) + INT(res-line.erwachs).
        END.
        ASSIGN troom = string(temp-total2)
               tpax  = string(temp-total).
    END.    
    ELSE IF lname NE "" AND SUBSTR(lname,1,1) EQ "*" THEN DO:
        FOR EACH res-line WHERE 
           res-line.active-flag = 1  AND res-line.resstatus NE 12 
           AND res-line.resname MATCHES(lname) 
           AND res-line.ankunft LE ci-date AND res-line.abreise GE ci-date NO-LOCK, 
           FIRST waehrung WHERE waehrung.waehrungsnr = res-line.betriebsnr 
           NO-LOCK, 
           FIRST reservation WHERE reservation.resnr = res-line.resnr, 
           FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr, 
           FIRST gmember WHERE gmember.gastnr = res-line.gastnrmember 
           NO-LOCK BY gmember.nation1 BY (res-line.kontakt-nr * res-line.resnr) 
           BY res-line.resstatus BY res-line.NAME:
                RUN assign-it.
                IF res-line.resstatus NE 13 AND res-line.resstatus NE 11 AND res-line.l-zuordnung[3] NE 1 THEN
                            temp-total2 = temp-total2 + res-line.zimmeranz.
                ASSIGN temp-total = INT(temp-total) + INT(res-line.erwachs).
        END.
        ASSIGN troom = string(temp-total2)
               tpax  = string(temp-total).
    END.    
    ELSE IF lname NE "" AND SUBSTR(lname,1,1) NE "*" THEN DO:
        FOR EACH res-line WHERE 
           res-line.active-flag = 1  AND res-line.resstatus NE 12 
           AND res-line.resname GE lname AND res-line.resname LE to-name 
           AND res-line.ankunft LE ci-date AND res-line.abreise GE ci-date NO-LOCK, 
           FIRST waehrung WHERE waehrung.waehrungsnr = res-line.betriebsnr 
           NO-LOCK, 
           FIRST reservation WHERE reservation.resnr = res-line.resnr, 
           FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr, 
           FIRST gmember WHERE gmember.gastnr = res-line.gastnrmember 
           NO-LOCK BY gmember.nation1 BY (res-line.kontakt-nr * res-line.resnr) 
           BY res-line.resstatus BY res-line.NAME:
                RUN assign-it.
                IF res-line.resstatus NE 13 AND res-line.resstatus NE 11 AND res-line.l-zuordnung[3] NE 1 THEN
                            temp-total2 = temp-total2 + res-line.zimmeranz.
                ASSIGN temp-total = INT(temp-total) + INT(res-line.erwachs).
        END.
        ASSIGN troom = string(temp-total2)
               tpax  = string(temp-total).
    END.    
  END. 
  ELSE IF last-sort = 3 AND lnat NE "" THEN 
  DO: 
    IF lname = "" THEN DO:
        FOR EACH res-line WHERE 
           res-line.active-flag = 1 AND res-line.resstatus NE 12 
           AND res-line.ankunft LE ci-date AND res-line.abreise GE ci-date NO-LOCK, 
           FIRST waehrung WHERE waehrung.waehrungsnr = res-line.betriebsnr 
           NO-LOCK, 
           FIRST reservation WHERE reservation.resnr = res-line.resnr, 
           FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr, 
           FIRST gmember WHERE gmember.gastnr = res-line.gastnrmember 
           AND gmember.nation1 = lnat 
           NO-LOCK BY gmember.nation1 BY (res-line.kontakt-nr * res-line.resnr) 
           BY res-line.resstatus BY res-line.NAME:
                RUN assign-it.
                IF res-line.resstatus NE 13 AND res-line.resstatus NE 11 AND res-line.l-zuordnung[3] NE 1 THEN
                            temp-total2 = temp-total2 + res-line.zimmeranz.
                ASSIGN temp-total = INT(temp-total) + INT(res-line.erwachs).
        END.
        ASSIGN troom = string(temp-total2)
               tpax  = string(temp-total).
    END.    
    ELSE IF lname NE "" AND SUBSTR(lname,1,1) EQ "*" THEN DO:
        FOR EACH res-line WHERE 
           res-line.active-flag = 1  AND res-line.resstatus NE 12 
           AND res-line.resname MATCHES(lname) 
           AND res-line.ankunft LE ci-date AND res-line.abreise GE ci-date NO-LOCK, 
           FIRST waehrung WHERE waehrung.waehrungsnr = res-line.betriebsnr 
           NO-LOCK, 
           FIRST reservation WHERE reservation.resnr = res-line.resnr, 
           FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr, 
           FIRST gmember WHERE gmember.gastnr = res-line.gastnrmember 
           AND gmember.nation1 = lnat 
           NO-LOCK BY gmember.nation1 BY (res-line.kontakt-nr * res-line.resnr) 
           BY res-line.resstatus BY res-line.NAME:
                RUN assign-it.
                IF res-line.resstatus NE 13 AND res-line.resstatus NE 11 AND res-line.l-zuordnung[3] NE 1 THEN
                            temp-total2 = temp-total2 + res-line.zimmeranz.
                ASSIGN temp-total = INT(temp-total) + INT(res-line.erwachs).
        END.
        ASSIGN troom = string(temp-total2)
               tpax  = string(temp-total).
    END.    
    ELSE IF lname NE "" AND SUBSTR(lname,1,1) NE "*" THEN DO:
        FOR EACH res-line WHERE 
           res-line.active-flag = 1  AND res-line.resstatus NE 12 
           AND res-line.resname GE lname AND res-line.resname LE to-name 
           AND res-line.ankunft LE ci-date AND res-line.abreise GE ci-date NO-LOCK, 
           FIRST waehrung WHERE waehrung.waehrungsnr = res-line.betriebsnr 
           NO-LOCK, 
           FIRST reservation WHERE reservation.resnr = res-line.resnr, 
           FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr, 
           FIRST gmember WHERE gmember.gastnr = res-line.gastnrmember 
           AND gmember.nation1 = lnat 
           NO-LOCK BY gmember.nation1 BY (res-line.kontakt-nr * res-line.resnr) 
           BY res-line.resstatus BY res-line.NAME:
                RUN assign-it.
                IF res-line.resstatus NE 13 AND res-line.resstatus NE 11 AND res-line.l-zuordnung[3] NE 1 THEN
                            temp-total2 = temp-total2 + res-line.zimmeranz.
                ASSIGN temp-total = INT(temp-total) + INT(res-line.erwachs).
        END.
        ASSIGN troom = string(temp-total2)
               tpax  = string(temp-total).
    END.    
  END. 
  ELSE IF last-sort = 4 THEN 
  DO: 
    IF lresnr = 0 THEN DO:
        FOR EACH res-line WHERE res-line.active-flag = 1 
          AND res-line.resstatus NE 12 NO-LOCK, 
          FIRST waehrung WHERE waehrung.waehrungsnr = res-line.betriebsnr 
          NO-LOCK, 
          FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
          FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr NO-LOCK, 
          FIRST gmember WHERE gmember.gastnr = res-line.gastnrmember 
          NO-LOCK BY res-line.resnr BY (res-line.kontakt-nr * res-line.resnr) 
          BY res-line.resstatus BY res-line.NAME:
                RUN assign-it.
                IF res-line.resstatus NE 13 AND res-line.resstatus NE 11 AND res-line.l-zuordnung[3] NE 1 THEN
                            temp-total2 = temp-total2 + res-line.zimmeranz.
                ASSIGN temp-total = INT(temp-total) + INT(res-line.erwachs).
        END.
        ASSIGN troom = string(temp-total2)
               tpax  = string(temp-total).
    END.    
    ELSE DO:
        FOR EACH res-line WHERE res-line.active-flag = 1 
          AND res-line.resstatus NE 12 AND res-line.resnr = lresnr NO-LOCK, 
          FIRST waehrung WHERE waehrung.waehrungsnr = res-line.betriebsnr 
          NO-LOCK, 
          FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
          FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr NO-LOCK, 
          FIRST gmember WHERE gmember.gastnr = res-line.gastnrmember 
          NO-LOCK BY res-line.name:
                RUN assign-it.
                IF res-line.resstatus NE 13 AND res-line.resstatus NE 11 AND res-line.l-zuordnung[3] NE 1 THEN
                            temp-total2 = temp-total2 + res-line.zimmeranz.
                ASSIGN temp-total = INT(temp-total) + INT(res-line.erwachs).
        END.
        ASSIGN troom = string(temp-total2)
               tpax  = string(temp-total).
    END.    
  END. 
END. 
 
PROCEDURE disp-arl4: 
  DEFINE VARIABLE to-name AS CHAR. 
  rmlen = length(room). 
  IF lname NE "" AND SUBSTR(lname,1,1) NE "*" THEN 
    to-name = chr(asc(SUBSTR(lname,1,1)) + 1). 
 
  IF last-sort = 1 THEN 
  DO: 
    IF room NE "" THEN 
    DO: 
      IF lname = "" AND room = "" THEN DO:
        FOR EACH res-line WHERE 
           res-line.active-flag = 1  AND res-line.resstatus NE 12 
           AND (SUBSTR(res-line.zinr,1,INTEGER(rmlen))) GE room 
           AND res-line.abreise EQ ci-date NO-LOCK, 
           FIRST waehrung WHERE waehrung.waehrungsnr = res-line.betriebsnr 
           NO-LOCK, 
           FIRST reservation WHERE reservation.resnr = res-line.resnr, 
           FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr, 
           FIRST gmember WHERE gmember.gastnr = res-line.gastnrmember 
           NO-LOCK BY res-line.zinr BY (res-line.kontakt-nr * res-line.resnr) 
           BY res-line.resstatus BY res-line.NAME:
                RUN assign-it.
                IF res-line.resstatus NE 13 AND res-line.resstatus NE 11 AND res-line.l-zuordnung[3] NE 1 THEN
                            temp-total2 = temp-total2 + res-line.zimmeranz.
                ASSIGN temp-total = INT(temp-total) + INT(res-line.erwachs).
          END.
          ASSIGN troom = string(temp-total2)
                 tpax  = string(temp-total).
      END.      
      ELSE IF lname NE "" AND SUBSTR(lname,1,1) EQ "*" THEN DO:
            FOR EACH res-line WHERE 
               res-line.active-flag = 1  AND res-line.resstatus NE 12 
               AND (SUBSTR(res-line.zinr,1,INTEGER(rmlen))) GE room 
               AND res-line.name MATCHES(lname) 
               AND res-line.abreise EQ ci-date NO-LOCK, 
               FIRST waehrung WHERE waehrung.waehrungsnr = res-line.betriebsnr 
               NO-LOCK, 
               FIRST reservation WHERE reservation.resnr = res-line.resnr, 
               FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr, 
               FIRST gmember WHERE gmember.gastnr = res-line.gastnrmember 
               NO-LOCK BY res-line.zinr BY (res-line.kontakt-nr * res-line.resnr) 
               BY res-line.resstatus BY res-line.NAME:
                    RUN assign-it.
                    IF res-line.resstatus NE 13 AND res-line.resstatus NE 11 AND res-line.l-zuordnung[3] NE 1 THEN
                            temp-total2 = temp-total2 + res-line.zimmeranz.
                    ASSIGN temp-total = INT(temp-total) + INT(res-line.erwachs).
            END.
            ASSIGN troom = string(temp-total2)
                   tpax  = string(temp-total).
      END.      
      ELSE IF lname NE "" AND SUBSTR(lname,1,1) NE "*" THEN DO:
          FOR EACH res-line WHERE 
               res-line.active-flag = 1  AND res-line.resstatus NE 12 
               AND (SUBSTR(res-line.zinr,1,INTEGER(rmlen))) GE room 
               AND res-line.name GE lname AND res-line.name LE to-name 
               AND res-line.abreise EQ ci-date NO-LOCK, 
               FIRST waehrung WHERE waehrung.waehrungsnr = res-line.betriebsnr 
               NO-LOCK, 
               FIRST reservation WHERE reservation.resnr = res-line.resnr, 
               FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr, 
               FIRST gmember WHERE gmember.gastnr = res-line.gastnrmember 
               NO-LOCK BY res-line.zinr BY (res-line.kontakt-nr * res-line.resnr) 
               BY res-line.resstatus BY res-line.NAME:
                RUN assign-it.
                IF res-line.resstatus NE 13 AND res-line.resstatus NE 11 AND res-line.l-zuordnung[3] NE 1 THEN
                        temp-total2 = temp-total2 + res-line.zimmeranz.
                ASSIGN temp-total = INT(temp-total) + INT(res-line.erwachs).
          END.
          ASSIGN troom = string(temp-total2)
                 tpax  = string(temp-total).
      END.      
    END. 
    ELSE IF room = "" THEN 
    DO: 
      IF lname = "" THEN DO:
          FOR EACH res-line WHERE 
               res-line.active-flag = 1  AND res-line.resstatus NE 12 
               AND res-line.abreise EQ ci-date NO-LOCK, 
               FIRST waehrung WHERE waehrung.waehrungsnr = res-line.betriebsnr 
               NO-LOCK, 
               FIRST reservation WHERE reservation.resnr = res-line.resnr, 
               FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr, 
               FIRST gmember WHERE gmember.gastnr = res-line.gastnrmember 
               NO-LOCK BY res-line.zinr BY (res-line.kontakt-nr * res-line.resnr) 
               BY res-line.resstatus BY res-line.NAME:
                    RUN assign-it.
                    IF res-line.resstatus NE 13 AND res-line.resstatus NE 11 AND res-line.l-zuordnung[3] NE 1 THEN
                            temp-total2 = temp-total2 + res-line.zimmeranz.
                    ASSIGN temp-total = INT(temp-total) + INT(res-line.erwachs).
          END.
          ASSIGN troom = string(temp-total2)
                 tpax  = string(temp-total).
      END.      
      ELSE IF lname NE "" AND SUBSTR(lname,1,1) EQ "*" THEN DO:
             FOR EACH res-line WHERE 
                   res-line.active-flag = 1  AND res-line.resstatus NE 12 
                   AND res-line.name MATCHES(lname) AND res-line.abreise EQ ci-date NO-LOCK, 
                   FIRST waehrung WHERE waehrung.waehrungsnr = res-line.betriebsnr 
                   NO-LOCK, 
                   FIRST reservation WHERE reservation.resnr = res-line.resnr, 
                   FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr, 
                   FIRST gmember WHERE gmember.gastnr = res-line.gastnrmember 
                   NO-LOCK BY res-line.name BY res-line.zinr:
                    RUN assign-it.
                    IF res-line.resstatus NE 13 AND res-line.resstatus NE 11 AND res-line.l-zuordnung[3] NE 1 THEN
                            temp-total2 = temp-total2 + res-line.zimmeranz.
                    ASSIGN temp-total = INT(temp-total) + INT(res-line.erwachs).
             END.
             ASSIGN troom = string(temp-total2)
                    tpax  = string(temp-total).
      END.      
      ELSE IF lname NE "" AND SUBSTR(lname,1,1) NE "*" THEN DO:
             FOR EACH res-line WHERE 
                   res-line.active-flag = 1  AND res-line.resstatus NE 12 
                   AND res-line.name GE lname AND res-line.name LE to-name 
                   AND res-line.abreise EQ ci-date NO-LOCK, 
                   FIRST waehrung WHERE waehrung.waehrungsnr = res-line.betriebsnr 
                   NO-LOCK, 
                   FIRST reservation WHERE reservation.resnr = res-line.resnr, 
                   FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr, 
                   FIRST gmember WHERE gmember.gastnr = res-line.gastnrmember 
                   NO-LOCK BY res-line.name BY res-line.zinr:
                    RUN assign-it.
                    IF res-line.resstatus NE 13 AND res-line.resstatus NE 11 AND res-line.l-zuordnung[3] NE 1 THEN
                            temp-total2 = temp-total2 + res-line.zimmeranz.
                    ASSIGN temp-total = INT(temp-total) + INT(res-line.erwachs).
             END.
             ASSIGN troom = string(temp-total2)
                    tpax  = string(temp-total).
      END.      
    END. 
  END. 
  ELSE IF last-sort = 2 THEN 
  DO: 
    IF lname = "" THEN 
    DO: 
      IF room = "" THEN DO:
            FOR EACH res-line WHERE 
                res-line.active-flag = 1 AND res-line.resstatus NE 12 
                AND (SUBSTR(res-line.zinr,1,INTEGER(rmlen))) GE room 
                AND res-line.abreise EQ ci-date NO-LOCK, 
                FIRST waehrung WHERE waehrung.waehrungsnr = res-line.betriebsnr 
                NO-LOCK, 
                FIRST reservation WHERE reservation.resnr = res-line.resnr, 
                FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr, 
                FIRST gmember WHERE gmember.gastnr = res-line.gastnrmember 
                NO-LOCK BY res-line.resname BY res-line.resnr BY res-line.zinr
                BY (res-line.kontakt-nr * res-line.resnr) 
                BY res-line.resstatus BY res-line.NAME:
                    RUN assign-it.
                    IF res-line.resstatus NE 13 AND res-line.resstatus NE 11 AND res-line.l-zuordnung[3] NE 1 THEN
                            temp-total2 = temp-total2 + res-line.zimmeranz.
                    ASSIGN temp-total = INT(temp-total) + INT(res-line.erwachs).
            END.
            ASSIGN troom = string(temp-total2)
                    tpax  = string(temp-total).
      END.      
      ELSE IF room NE "" THEN DO:
            FOR EACH res-line WHERE 
                res-line.active-flag = 1 AND res-line.resstatus NE 12 
                AND (SUBSTR(res-line.zinr,1,INTEGER(rmlen))) GE room 
                AND res-line.abreise EQ ci-date NO-LOCK, 
                FIRST waehrung WHERE waehrung.waehrungsnr = res-line.betriebsnr 
                NO-LOCK, 
                FIRST reservation WHERE reservation.resnr = res-line.resnr, 
                FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr, 
                FIRST gmember WHERE gmember.gastnr = res-line.gastnrmember 
                NO-LOCK BY res-line.zinr BY (res-line.kontakt-nr * res-line.resnr) 
                BY res-line.resstatus BY res-line.NAME:
                    RUN assign-it.
                    IF res-line.resstatus NE 13 AND res-line.resstatus NE 11 AND res-line.l-zuordnung[3] NE 1 THEN
                            temp-total2 = temp-total2 + res-line.zimmeranz.
                    ASSIGN temp-total = INT(temp-total) + INT(res-line.erwachs).
            END.
            ASSIGN troom = string(temp-total2)
                    tpax  = string(temp-total).
      END.      
    END. 
    ELSE IF lname NE "" AND SUBSTR(lname,1,1) EQ "*" THEN DO:
            FOR EACH res-line WHERE 
               res-line.active-flag = 1  AND res-line.resstatus NE 12 
               AND (SUBSTR(res-line.zinr,1,INTEGER(rmlen))) GE room 
               AND res-line.resname MATCHES(lname) 
               AND res-line.abreise EQ ci-date NO-LOCK, 
               FIRST waehrung WHERE waehrung.waehrungsnr = res-line.betriebsnr 
               NO-LOCK, 
               FIRST reservation WHERE reservation.resnr = res-line.resnr, 
               FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr, 
               FIRST gmember WHERE gmember.gastnr = res-line.gastnrmember 
               NO-LOCK BY res-line.resname BY res-line.zinr
               BY (res-line.kontakt-nr * res-line.resnr) 
               BY res-line.resstatus BY res-line.NAME:
                    RUN assign-it.
                    IF res-line.resstatus NE 13 AND res-line.resstatus NE 11 AND res-line.l-zuordnung[3] NE 1 THEN
                            temp-total2 = temp-total2 + res-line.zimmeranz.
                    ASSIGN temp-total = INT(temp-total) + INT(res-line.erwachs).
            END.
            ASSIGN troom = string(temp-total2)
                    tpax  = string(temp-total).
    END.    
    ELSE IF lname NE "" AND SUBSTR(lname,1,1) NE "*" THEN DO:
        FOR EACH res-line WHERE 
           res-line.active-flag = 1  AND res-line.resstatus NE 12 
           AND (SUBSTR(res-line.zinr,1,INTEGER(rmlen))) GE room 
           AND res-line.resname GE lname AND res-line.resname LE to-name 
           AND res-line.abreise EQ ci-date NO-LOCK, 
           FIRST waehrung WHERE waehrung.waehrungsnr = res-line.betriebsnr 
           NO-LOCK, 
           FIRST reservation WHERE reservation.resnr = res-line.resnr, 
           FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr, 
           FIRST gmember WHERE gmember.gastnr = res-line.gastnrmember 
           NO-LOCK BY res-line.resname BY res-line.zinr
           BY (res-line.kontakt-nr * res-line.resnr) 
           BY res-line.resstatus BY res-line.NAME:
                RUN assign-it.
                IF res-line.resstatus NE 13 AND res-line.resstatus NE 11 AND res-line.l-zuordnung[3] NE 1 THEN
                        temp-total2 = temp-total2 + res-line.zimmeranz.
                ASSIGN temp-total = INT(temp-total) + INT(res-line.erwachs).
        END.
        ASSIGN troom = string(temp-total2)
               tpax  = string(temp-total).
    END.    
  END. 
  ELSE IF last-sort = 3 AND lnat = "" THEN 
  DO: 
    IF lname = "" THEN DO:
        FOR EACH res-line WHERE 
           res-line.active-flag = 1 AND res-line.resstatus NE 12 
           AND res-line.abreise EQ ci-date NO-LOCK, 
           FIRST waehrung WHERE waehrung.waehrungsnr = res-line.betriebsnr 
           NO-LOCK, 
           FIRST reservation WHERE reservation.resnr = res-line.resnr, 
           FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr, 
           FIRST gmember WHERE gmember.gastnr = res-line.gastnrmember 
           NO-LOCK BY gmember.nation1 BY (res-line.kontakt-nr * res-line.resnr) 
           BY res-line.resstatus BY res-line.NAME:
                RUN assign-it.
                IF res-line.resstatus NE 13 AND res-line.resstatus NE 11 AND res-line.l-zuordnung[3] NE 1 THEN
                        temp-total2 = temp-total2 + res-line.zimmeranz.
                ASSIGN temp-total = INT(temp-total) + INT(res-line.erwachs).
        END.
        ASSIGN troom = string(temp-total2)
               tpax  = string(temp-total).
    END.    
    ELSE IF lname NE "" AND SUBSTR(lname,1,1) EQ "*" THEN DO:
        FOR EACH res-line WHERE 
           res-line.active-flag = 1  AND res-line.resstatus NE 12 
           AND res-line.name MATCHES(lname) 
           AND res-line.abreise EQ ci-date NO-LOCK, 
           FIRST waehrung WHERE waehrung.waehrungsnr = res-line.betriebsnr 
           NO-LOCK, 
           FIRST reservation WHERE reservation.resnr = res-line.resnr, 
           FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr, 
           FIRST gmember WHERE gmember.gastnr = res-line.gastnrmember 
           AND gmember.nation1 = lnat 
           NO-LOCK BY gmember.nation1 BY (res-line.kontakt-nr * res-line.resnr) 
           BY res-line.resstatus BY res-line.NAME:
                RUN assign-it.
                IF res-line.resstatus NE 13 AND res-line.resstatus NE 11 AND res-line.l-zuordnung[3] NE 1 THEN
                        temp-total2 = temp-total2 + res-line.zimmeranz.
                ASSIGN temp-total = INT(temp-total) + INT(res-line.erwachs).
        END.
        ASSIGN troom = string(temp-total2)
               tpax  = string(temp-total).
    END.    
    ELSE IF lname NE "" AND SUBSTR(lname,1,1) NE "*" THEN DO:
        FOR EACH res-line WHERE 
           res-line.active-flag = 1  AND res-line.resstatus NE 12 
           AND res-line.name GE lname AND res-line.name LE to-name 
           AND res-line.abreise EQ ci-date NO-LOCK, 
           FIRST waehrung WHERE waehrung.waehrungsnr = res-line.betriebsnr 
           NO-LOCK, 
           FIRST reservation WHERE reservation.resnr = res-line.resnr, 
           FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr, 
           FIRST gmember WHERE gmember.gastnr = res-line.gastnrmember 
           NO-LOCK BY gmember.nation1 BY (res-line.kontakt-nr * res-line.resnr) 
           BY res-line.resstatus BY res-line.NAME:
                RUN assign-it.
                IF res-line.resstatus NE 13 AND res-line.resstatus NE 11 AND res-line.l-zuordnung[3] NE 1 THEN
                        temp-total2 = temp-total2 + res-line.zimmeranz.
                ASSIGN temp-total = INT(temp-total) + INT(res-line.erwachs).
        END.
        ASSIGN troom = string(temp-total2)
               tpax  = string(temp-total).
    END.    
  END. 
  ELSE IF last-sort = 3 AND lnat NE "" THEN 
  DO: 
    IF lname = "" THEN DO:
       FOR EACH res-line WHERE 
           res-line.active-flag = 1 AND res-line.resstatus NE 12 
           AND res-line.abreise EQ ci-date NO-LOCK, 
           FIRST waehrung WHERE waehrung.waehrungsnr = res-line.betriebsnr 
           NO-LOCK, 
           FIRST reservation WHERE reservation.resnr = res-line.resnr, 
           FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr, 
           FIRST gmember WHERE gmember.gastnr = res-line.gastnrmember 
           AND gmember.nation1 = lnat 
           NO-LOCK BY gmember.nation1 BY (res-line.kontakt-nr * res-line.resnr) 
           BY res-line.resstatus BY res-line.NAME:
                RUN assign-it.
                IF res-line.resstatus NE 13 AND res-line.resstatus NE 11 AND res-line.l-zuordnung[3] NE 1 THEN
                        temp-total2 = temp-total2 + res-line.zimmeranz.
                ASSIGN temp-total = INT(temp-total) + INT(res-line.erwachs).
        END.
        ASSIGN troom = string(temp-total2)
               tpax  = string(temp-total).
    END.
    ELSE IF lname NE "" AND SUBSTR(lname,1,1) EQ "*" THEN DO:
        FOR EACH res-line WHERE 
           res-line.active-flag = 1  AND res-line.resstatus NE 12 
           AND res-line.name MATCHES(lname) AND res-line.abreise EQ ci-date NO-LOCK, 
           FIRST waehrung WHERE waehrung.waehrungsnr = res-line.betriebsnr 
           NO-LOCK, 
           FIRST reservation WHERE reservation.resnr = res-line.resnr, 
           FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr, 
           FIRST gmember WHERE gmember.gastnr = res-line.gastnrmember 
           AND gmember.nation1 = lnat 
           NO-LOCK BY gmember.nation1 BY (res-line.kontakt-nr * res-line.resnr) 
           BY res-line.resstatus BY res-line.NAME:
                RUN assign-it.
                IF res-line.resstatus NE 13 AND res-line.resstatus NE 11 AND res-line.l-zuordnung[3] NE 1 THEN
                        temp-total2 = temp-total2 + res-line.zimmeranz.
                ASSIGN temp-total = INT(temp-total) + INT(res-line.erwachs).
        END.
        ASSIGN troom = string(temp-total2)
               tpax  = string(temp-total).
    END.    
    ELSE IF lname NE "" AND SUBSTR(lname,1,1) NE "*" THEN DO:
            FOR EACH res-line WHERE 
               res-line.active-flag = 1  AND res-line.resstatus NE 12 
               AND res-line.name GE lname AND res-line.name LE to-name 
               AND res-line.abreise EQ ci-date NO-LOCK, 
               FIRST waehrung WHERE waehrung.waehrungsnr = res-line.betriebsnr 
               NO-LOCK, 
               FIRST reservation WHERE reservation.resnr = res-line.resnr, 
               FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr, 
               FIRST gmember WHERE gmember.gastnr = res-line.gastnrmember 
               AND gmember.nation1 = lnat 
               NO-LOCK BY gmember.nation1 BY (res-line.kontakt-nr * res-line.resnr) 
               BY res-line.resstatus BY res-line.NAME:
                    RUN assign-it.
                    IF res-line.resstatus NE 13 AND res-line.resstatus NE 11 AND res-line.l-zuordnung[3] NE 1 THEN
                            temp-total2 = temp-total2 + res-line.zimmeranz.
                    ASSIGN temp-total = INT(temp-total) + INT(res-line.erwachs).
            END.
            ASSIGN troom = string(temp-total2)
                   tpax  = string(temp-total).
    END.    
  END. 
  ELSE IF last-sort = 4 THEN 
  DO: 
    IF lresnr = 0 THEN DO:
           FOR EACH res-line WHERE res-line.active-flag = 1 
              AND res-line.resstatus NE 12 AND res-line.abreise = ci-date NO-LOCK, 
              FIRST waehrung WHERE waehrung.waehrungsnr = res-line.betriebsnr 
              NO-LOCK, 
              FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
              FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr NO-LOCK, 
              FIRST gmember WHERE gmember.gastnr = res-line.gastnrmember 
              NO-LOCK BY res-line.resnr BY (res-line.kontakt-nr * res-line.resnr) 
              BY res-line.resstatus BY res-line.NAME:
                    RUN assign-it.
                    IF res-line.resstatus NE 13 AND res-line.resstatus NE 11 AND res-line.l-zuordnung[3] NE 1 THEN
                            temp-total2 = temp-total2 + res-line.zimmeranz.
                    ASSIGN temp-total = INT(temp-total) + INT(res-line.erwachs).
            END.
            ASSIGN troom = string(temp-total2)
                   tpax  = string(temp-total).
    END.    
    ELSE DO:
            FOR EACH res-line WHERE res-line.active-flag = 1 
              AND res-line.resstatus NE 12 AND res-line.resnr = lresnr 
              AND res-line.abreise = ci-date NO-LOCK, 
              FIRST waehrung WHERE waehrung.waehrungsnr = res-line.betriebsnr 
              NO-LOCK, 
              FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
              FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr NO-LOCK, 
              FIRST gmember WHERE gmember.gastnr = res-line.gastnrmember 
              NO-LOCK BY res-line.name:
                    RUN assign-it.
                    IF res-line.resstatus NE 13 AND res-line.resstatus NE 11 AND res-line.l-zuordnung[3] NE 1 THEN
                            temp-total2 = temp-total2 + res-line.zimmeranz.
                    ASSIGN temp-total = INT(temp-total) + INT(res-line.erwachs).
            END.
            ASSIGN troom = string(temp-total2)
                   tpax  = string(temp-total).
    END.    
  END. 
END. 
 
PROCEDURE disp-arl5: 
  DEFINE VARIABLE to-name AS CHAR INITIAL "zzz". 
  rmlen = length(room). 
  IF lname NE "" AND SUBSTR(lname,1,1) NE "*" THEN 
    to-name = chr(asc(SUBSTR(lname,1,1)) + 1). 
  IF fdate2 = ? THEN 
  DO: 
    fdate2 = ci-date.
  END. 
  
  IF last-sort = 1 AND room NE "" THEN 
  DO: 
    IF lname = "" THEN DO:
        FOR EACH res-line WHERE res-line.resstatus EQ 8 
           AND res-line.abreise EQ fdate2 
           AND res-line.zinr GE room NO-LOCK, 
           FIRST waehrung WHERE waehrung.waehrungsnr = res-line.betriebsnr 
           NO-LOCK, 
           FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
           FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr NO-LOCK, 
           FIRST gmember WHERE gmember.gastnr = res-line.gastnrmember 
           NO-LOCK BY res-line.zinr BY (res-line.kontakt-nr * res-line.resnr) 
           BY res-line.resstatus BY res-line.NAME:
                 RUN assign-it.
                 IF res-line.resstatus NE 13 AND res-line.resstatus NE 11 AND res-line.l-zuordnung[3] NE 1 THEN
                        temp-total2 = temp-total2 + res-line.zimmeranz.
                 ASSIGN temp-total = INT(temp-total) + INT(res-line.erwachs).
        END.
         ASSIGN troom = string(temp-total2)
                tpax  = string(temp-total).
    END.    
    ELSE IF lname NE "" AND SUBSTR(lname,1,1) EQ "*" THEN DO:
            FOR EACH res-line WHERE res-line.resstatus EQ 8 
               AND res-line.name MATCHES(lname) AND res-line.abreise EQ fdate2 
               AND res-line.zinr GE room NO-LOCK, 
               FIRST waehrung WHERE waehrung.waehrungsnr = res-line.betriebsnr 
               NO-LOCK, 
               FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
               FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr NO-LOCK, 
               FIRST gmember WHERE gmember.gastnr = res-line.gastnrmember 
               NO-LOCK BY res-line.zinr BY (res-line.kontakt-nr * res-line.resnr) 
               BY res-line.resstatus BY res-line.NAME:
                    RUN assign-it.
                    IF res-line.resstatus NE 13 AND res-line.resstatus NE 11 AND res-line.l-zuordnung[3] NE 1 THEN
                        temp-total2 = temp-total2 + res-line.zimmeranz.
                    ASSIGN temp-total = INT(temp-total) + INT(res-line.erwachs).
            END.
            ASSIGN troom = string(temp-total2)
                   tpax  = string(temp-total).
    END.    
    ELSE IF lname NE "" AND SUBSTR(lname,1,1) NE "*" THEN DO:
        FOR EACH res-line WHERE res-line.resstatus EQ 8 
           AND res-line.name GE lname AND res-line.name LE to-name 
           AND res-line.abreise EQ fdate2 AND res-line.zinr GE room NO-LOCK, 
           FIRST waehrung WHERE waehrung.waehrungsnr = res-line.betriebsnr 
           NO-LOCK, 
           FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
           FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr NO-LOCK, 
           FIRST gmember WHERE gmember.gastnr = res-line.gastnrmember 
           NO-LOCK BY res-line.name:
                RUN assign-it.
                IF res-line.resstatus NE 13 AND res-line.resstatus NE 11 AND res-line.l-zuordnung[3] NE 1 THEN
                    temp-total2 = temp-total2 + res-line.zimmeranz.
                ASSIGN temp-total = INT(temp-total) + INT(res-line.erwachs).
        END.
        ASSIGN troom = string(temp-total2)
               tpax  = string(temp-total).
    END.    
  END. 
  ELSE IF last-sort = 1 AND room = "" THEN 
  DO: 
    IF lname = "" THEN DO:
        FOR EACH res-line WHERE res-line.resstatus EQ 8 
           AND res-line.abreise EQ fdate2 NO-LOCK, 
           FIRST waehrung WHERE waehrung.waehrungsnr = res-line.betriebsnr 
           NO-LOCK, 
           FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
           FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr NO-LOCK, 
           FIRST gmember WHERE gmember.gastnr = res-line.gastnrmember 
           NO-LOCK BY (res-line.kontakt-nr * res-line.resnr) 
           BY res-line.resstatus BY res-line.NAME:
                RUN assign-it.
                IF res-line.resstatus NE 13 AND res-line.resstatus NE 11 AND res-line.l-zuordnung[3] NE 1 THEN
                    temp-total2 = temp-total2 + res-line.zimmeranz.
                ASSIGN temp-total = INT(temp-total) + INT(res-line.erwachs).
        END.
        ASSIGN troom = string(temp-total2)
               tpax  = string(temp-total).
    END.    
    ELSE IF lname NE "" AND SUBSTR(lname,1,1) EQ "*" THEN DO:
        FOR EACH res-line WHERE res-line.resstatus EQ 8 
           AND res-line.name MATCHES(lname) AND res-line.abreise EQ fdate2 NO-LOCK, 
           FIRST waehrung WHERE waehrung.waehrungsnr = res-line.betriebsnr 
           NO-LOCK, 
           FIRST reservation WHERE reservation.resnr = res-line.resnr, 
           FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr, 
           FIRST gmember WHERE gmember.gastnr = res-line.gastnrmember 
           NO-LOCK BY res-line.name:
                RUN assign-it.
                IF res-line.resstatus NE 13 AND res-line.resstatus NE 11 AND res-line.l-zuordnung[3] NE 1 THEN
                    temp-total2 = temp-total2 + res-line.zimmeranz.
                ASSIGN temp-total = INT(temp-total) + INT(res-line.erwachs).
        END.
        ASSIGN troom = string(temp-total2)
               tpax  = string(temp-total).
    END.    
    ELSE IF lname NE "" AND SUBSTR(lname,1,1) NE "*" THEN DO:
            FOR EACH res-line WHERE res-line.resstatus EQ 8 
               AND res-line.name GE lname AND res-line.name LE to-name 
               AND res-line.abreise EQ fdate2 NO-LOCK, 
               FIRST waehrung WHERE waehrung.waehrungsnr = res-line.betriebsnr 
               NO-LOCK, 
               FIRST reservation WHERE reservation.resnr = res-line.resnr, 
               FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr, 
               FIRST gmember WHERE gmember.gastnr = res-line.gastnrmember 
               NO-LOCK BY res-line.name:
                    RUN assign-it.
                    IF res-line.resstatus NE 13 AND res-line.resstatus NE 11 AND res-line.l-zuordnung[3] NE 1 THEN
                        temp-total2 = temp-total2 + res-line.zimmeranz.
                    ASSIGN temp-total = INT(temp-total) + INT(res-line.erwachs).
            END.
            ASSIGN troom = string(temp-total2)
                   tpax  = string(temp-total).
    END.    
  END. 
  ELSE IF last-sort = 2 AND room NE "" THEN 
  DO: 
    IF lname = "" THEN DO:
        FOR EACH res-line WHERE res-line.resstatus EQ 8 
           AND res-line.abreise EQ fdate2 AND res-line.zinr GE room NO-LOCK, 
           FIRST waehrung WHERE waehrung.waehrungsnr = res-line.betriebsnr 
           NO-LOCK, 
           FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
           FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr NO-LOCK, 
           FIRST gmember WHERE gmember.gastnr = res-line.gastnrmember 
           NO-LOCK BY res-line.zinr 
           BY reservation.NAME /*res-line.resname*/ BY res-line.resnr BY (res-line.kontakt-nr * res-line.resnr) 
           BY res-line.resstatus BY res-line.NAME:
                RUN assign-it.
                IF res-line.resstatus NE 13 AND res-line.resstatus NE 11 AND res-line.l-zuordnung[3] NE 1 THEN
                    temp-total2 = temp-total2 + res-line.zimmeranz.
                ASSIGN temp-total = INT(temp-total) + INT(res-line.erwachs).
        END.
        ASSIGN troom = string(temp-total2)
               tpax  = string(temp-total).
    END.    
    ELSE IF lname NE "" AND SUBSTR(lname,1,1) EQ "*" THEN DO:
        FOR EACH res-line WHERE res-line.resstatus EQ 8 
           AND res-line.resname MATCHES(lname) AND res-line.abreise EQ fdate2 
           AND res-line.zinr GE room NO-LOCK, 
           FIRST waehrung WHERE waehrung.waehrungsnr = res-line.betriebsnr 
           NO-LOCK, 
           FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
           FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr NO-LOCK, 
           FIRST gmember WHERE gmember.gastnr = res-line.gastnrmember 
           NO-LOCK BY res-line.zinr 
           BY res-line.resname BY res-line.resnr
           BY (res-line.kontakt-nr * res-line.resnr) 
           BY res-line.resstatus BY res-line.NAME:
                RUN assign-it.
                IF res-line.resstatus NE 13 AND res-line.resstatus NE 11 AND res-line.l-zuordnung[3] NE 1 THEN
                    temp-total2 = temp-total2 + res-line.zimmeranz.
                ASSIGN temp-total = INT(temp-total) + INT(res-line.erwachs).
        END.
        ASSIGN troom = string(temp-total2)
               tpax  = string(temp-total).
    END.    
    ELSE IF lname NE "" AND SUBSTR(lname,1,1) NE "*" THEN 
    DO: 
      FOR EACH res-line WHERE res-line.resstatus EQ 8 
       AND res-line.resname GE lname AND 
       res-line.resname  LE to-name 
       AND res-line.abreise EQ fdate2 AND res-line.zinr GE room NO-LOCK, 
       FIRST waehrung WHERE waehrung.waehrungsnr = res-line.betriebsnr 
       NO-LOCK, 
       FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
       FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr NO-LOCK, 
       FIRST gmember WHERE gmember.gastnr = res-line.gastnrmember 
       NO-LOCK BY res-line.zinr 
       BY res-line.resname BY res-line.resnr
       BY (res-line.kontakt-nr * res-line.resnr) 
       BY res-line.resstatus BY res-line.NAME:
            RUN assign-it.
            IF res-line.resstatus NE 13 AND res-line.resstatus NE 11 AND res-line.l-zuordnung[3] NE 1 THEN
                temp-total2 = temp-total2 + res-line.zimmeranz.
            ASSIGN temp-total = INT(temp-total) + INT(res-line.erwachs).
      END.
      ASSIGN troom = string(temp-total2)
             tpax  = string(temp-total).
    END.
  END. 
  ELSE IF last-sort = 2 AND room = "" THEN 
  DO: 
    IF lname = "" THEN DO:
        FOR EACH res-line WHERE res-line.resstatus EQ 8 
           AND res-line.abreise EQ fdate2 NO-LOCK, 
           FIRST waehrung WHERE waehrung.waehrungsnr = res-line.betriebsnr 
           NO-LOCK, 
           FIRST reservation WHERE reservation.resnr = res-line.resnr, 
           FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr, 
           FIRST gmember WHERE gmember.gastnr = res-line.gastnrmember 
           NO-LOCK BY reservation.NAME /*res-line.resname*/ BY res-line.resnr
           BY (res-line.kontakt-nr * res-line.resnr) 
           BY res-line.resstatus BY res-line.NAME:
                RUN assign-it.
                IF res-line.resstatus NE 13 AND res-line.resstatus NE 11 AND res-line.l-zuordnung[3] NE 1 THEN
                    temp-total2 = temp-total2 + res-line.zimmeranz.
                ASSIGN temp-total = INT(temp-total) + INT(res-line.erwachs).
        END.
        ASSIGN troom = string(temp-total2)
               tpax  = string(temp-total).
    END.    
    ELSE IF lname NE "" AND SUBSTR(lname,1,1) EQ "*" THEN DO:
            FOR EACH res-line WHERE res-line.resstatus EQ 8 
               AND res-line.resname MATCHES(lname) AND res-line.abreise EQ fdate2 NO-LOCK, 
               FIRST waehrung WHERE waehrung.waehrungsnr = res-line.betriebsnr 
               NO-LOCK, 
               FIRST reservation WHERE reservation.resnr = res-line.resnr, 
               FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr, 
               FIRST gmember WHERE gmember.gastnr = res-line.gastnrmember 
               NO-LOCK BY res-line.resname BY res-line.resnr
               BY (res-line.kontakt-nr * res-line.resnr) 
               BY res-line.resstatus BY res-line.NAME:
                    RUN assign-it.
                    IF res-line.resstatus NE 13 AND res-line.resstatus NE 11 AND res-line.l-zuordnung[3] NE 1 THEN
                        temp-total2 = temp-total2 + res-line.zimmeranz.
                    ASSIGN temp-total = INT(temp-total) + INT(res-line.erwachs).
            END.
            ASSIGN troom = string(temp-total2)
                   tpax  = string(temp-total).
    END.    
    ELSE IF lname NE "" AND SUBSTR(lname,1,1) NE "*" THEN DO:
        FOR EACH res-line WHERE res-line.resstatus EQ 8 
           AND res-line.abreise EQ fdate2 NO-LOCK, 
           FIRST waehrung WHERE waehrung.waehrungsnr = res-line.betriebsnr 
           NO-LOCK, 
           FIRST reservation WHERE reservation.resnr = res-line.resnr 
           AND reservation.NAME GE lname AND reservation.NAME LE to-name , 
           FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr, 
           FIRST gmember WHERE gmember.gastnr = res-line.gastnrmember 
           NO-LOCK BY /*res-line.resname */ reservation.NAME BY res-line.resnr
           BY (res-line.kontakt-nr * res-line.resnr) 
           BY res-line.resstatus BY res-line.NAME:
                RUN assign-it.
                IF res-line.resstatus NE 13 AND res-line.resstatus NE 11 AND res-line.l-zuordnung[3] NE 1 THEN
                    temp-total2 = temp-total2 + res-line.zimmeranz.
                ASSIGN temp-total = INT(temp-total) + INT(res-line.erwachs).
        END.
        ASSIGN troom = string(temp-total2)
               tpax  = string(temp-total).
    END.    
  END.  
  ELSE IF last-sort = 3 AND lnat = "" THEN 
  DO: 
    IF lname = "" THEN DO:
        FOR EACH res-line WHERE res-line.resstatus EQ 8 
           AND res-line.abreise EQ fdate2 NO-LOCK, 
           FIRST waehrung WHERE waehrung.waehrungsnr = res-line.betriebsnr 
           NO-LOCK, 
           FIRST reservation WHERE reservation.resnr = res-line.resnr, 
           FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr, 
           FIRST gmember WHERE gmember.gastnr = res-line.gastnrmember 
           NO-LOCK BY gmember.nation1
           BY (res-line.kontakt-nr * res-line.resnr) 
           BY res-line.resstatus BY res-line.NAME:
                RUN assign-it.
                IF res-line.resstatus NE 13 AND res-line.resstatus NE 11 AND res-line.l-zuordnung[3] NE 1 THEN
                    temp-total2 = temp-total2 + res-line.zimmeranz.
                ASSIGN temp-total = INT(temp-total) + INT(res-line.erwachs).
        END.
        ASSIGN troom = string(temp-total2)
               tpax  = string(temp-total).
    END.    
    ELSE IF lname NE "" AND SUBSTR(lname,1,1) EQ "*" THEN DO:
        FOR EACH res-line WHERE res-line.resstatus EQ 8 
           AND res-line.resname MATCHES(lname) AND res-line.abreise EQ fdate2 
           NO-LOCK, 
           FIRST waehrung WHERE waehrung.waehrungsnr = res-line.betriebsnr 
           NO-LOCK, 
           FIRST reservation WHERE reservation.resnr = res-line.resnr, 
           FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr, 
           FIRST gmember WHERE gmember.gastnr = res-line.gastnrmember 
           NO-LOCK BY gmember.nation1
           BY (res-line.kontakt-nr * res-line.resnr) 
           BY res-line.resstatus BY res-line.NAME:
                RUN assign-it.
                IF res-line.resstatus NE 13 AND res-line.resstatus NE 11 AND res-line.l-zuordnung[3] NE 1 THEN
                    temp-total2 = temp-total2 + res-line.zimmeranz.
                ASSIGN temp-total = INT(temp-total) + INT(res-line.erwachs).
        END.
        ASSIGN troom = string(temp-total2)
               tpax  = string(temp-total).
    END.    
    ELSE IF lname NE "" AND SUBSTR(lname,1,1) NE "*" THEN DO:
        FOR EACH res-line WHERE res-line.resstatus EQ 8 
           AND res-line.resname GE lname AND res-line.resname LE to-name 
           AND res-line.abreise EQ fdate2 NO-LOCK, 
           FIRST waehrung WHERE waehrung.waehrungsnr = res-line.betriebsnr 
           NO-LOCK, 
           FIRST reservation WHERE reservation.resnr = res-line.resnr, 
           FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr, 
           FIRST gmember WHERE gmember.gastnr = res-line.gastnrmember 
           NO-LOCK BY gmember.nation1
           BY (res-line.kontakt-nr * res-line.resnr) 
           BY res-line.resstatus BY res-line.NAME:
                RUN assign-it.
                IF res-line.resstatus NE 13 AND res-line.resstatus NE 11 AND res-line.l-zuordnung[3] NE 1 THEN
                    temp-total2 = temp-total2 + res-line.zimmeranz.
                ASSIGN temp-total = INT(temp-total) + INT(res-line.erwachs).
        END.
        ASSIGN troom = string(temp-total2)
               tpax  = string(temp-total).
    END.    
  END. 
  ELSE IF last-sort = 3 AND lnat NE "" THEN 
  DO: 
    IF lname = "" THEN DO:
        FOR EACH res-line WHERE res-line.resstatus EQ 8 
           AND res-line.abreise EQ fdate2 NO-LOCK, 
           FIRST waehrung WHERE waehrung.waehrungsnr = res-line.betriebsnr 
           NO-LOCK, 
           FIRST reservation WHERE reservation.resnr = res-line.resnr, 
           FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr, 
           FIRST gmember WHERE gmember.gastnr = res-line.gastnrmember 
           AND gmember.nation1 = lnat 
           NO-LOCK BY gmember.nation1
           BY (res-line.kontakt-nr * res-line.resnr) 
           BY res-line.resstatus BY res-line.NAME:
                RUN assign-it.
                IF res-line.resstatus NE 13 AND res-line.resstatus NE 11 AND res-line.l-zuordnung[3] NE 1 THEN
                    temp-total2 = temp-total2 + res-line.zimmeranz.
                ASSIGN temp-total = INT(temp-total) + INT(res-line.erwachs).
        END.
        ASSIGN troom = string(temp-total2)
               tpax  = string(temp-total).
    END.    
    ELSE IF lname NE "" AND SUBSTR(lname,1,1) EQ "*" THEN DO:
        FOR EACH res-line WHERE res-line.resstatus EQ 8 
           AND res-line.resname MATCHES(lname) AND res-line.abreise EQ fdate2 
           NO-LOCK, 
           FIRST waehrung WHERE waehrung.waehrungsnr = res-line.betriebsnr 
           NO-LOCK, 
           FIRST reservation WHERE reservation.resnr = res-line.resnr, 
           FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr, 
           FIRST gmember WHERE gmember.gastnr = res-line.gastnrmember 
           AND gmember.nation1 = lnat 
           NO-LOCK BY gmember.nation1
           BY (res-line.kontakt-nr * res-line.resnr) 
           BY res-line.resstatus BY res-line.NAME:
                RUN assign-it.
                IF res-line.resstatus NE 13 AND res-line.resstatus NE 11 AND res-line.l-zuordnung[3] NE 1 THEN
                    temp-total2 = temp-total2 + res-line.zimmeranz.
                ASSIGN temp-total = INT(temp-total) + INT(res-line.erwachs).
        END.
        ASSIGN troom = string(temp-total2)
               tpax  = string(temp-total).
    END.    
    ELSE IF lname NE "" AND SUBSTR(lname,1,1) NE "*" THEN DO:
        FOR EACH res-line WHERE res-line.resstatus EQ 8 
           AND res-line.resname GE lname AND res-line.resname LE to-name 
           AND res-line.abreise EQ fdate2 NO-LOCK, 
           FIRST waehrung WHERE waehrung.waehrungsnr = res-line.betriebsnr 
           NO-LOCK, 
           FIRST reservation WHERE reservation.resnr = res-line.resnr, 
           FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr, 
           FIRST gmember WHERE gmember.gastnr = res-line.gastnrmember 
           AND gmember.nation1 = lnat 
           NO-LOCK BY gmember.nation1
           BY (res-line.kontakt-nr * res-line.resnr) 
           BY res-line.resstatus BY res-line.NAME:
                RUN assign-it.
                IF res-line.resstatus NE 13 AND res-line.resstatus NE 11 AND res-line.l-zuordnung[3] NE 1 THEN
                    temp-total2 = temp-total2 + res-line.zimmeranz.
                ASSIGN temp-total = INT(temp-total) + INT(res-line.erwachs).
        END.
        ASSIGN troom = string(temp-total2)
               tpax  = string(temp-total).
    END.    
  END. 
  ELSE IF last-sort = 4 THEN 
  DO: 
    IF lresnr = 0 THEN DO:
        FOR EACH res-line WHERE res-line.active-flag = 2 
          AND res-line.resstatus EQ 8 
          AND res-line.abreise EQ fdate2 NO-LOCK, 
          FIRST waehrung WHERE waehrung.waehrungsnr = res-line.betriebsnr 
          NO-LOCK, 
          FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
          FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr NO-LOCK, 
          FIRST gmember WHERE gmember.gastnr = res-line.gastnrmember 
          NO-LOCK BY res-line.resnr
          BY (res-line.kontakt-nr * res-line.resnr) 
          BY res-line.resstatus BY res-line.NAME:
                RUN assign-it.
                IF res-line.resstatus NE 13 AND res-line.resstatus NE 11 AND res-line.l-zuordnung[3] NE 1 THEN
                    temp-total2 = temp-total2 + res-line.zimmeranz.
                ASSIGN temp-total = INT(temp-total) + INT(res-line.erwachs).
        END.
        ASSIGN troom = string(temp-total2)
               tpax  = string(temp-total).
    END.    
    ELSE DO:
        FOR EACH res-line WHERE res-line.active-flag = 2 
          AND res-line.resstatus EQ 8 AND res-line.resnr = lresnr NO-LOCK, 
          FIRST waehrung WHERE waehrung.waehrungsnr = res-line.betriebsnr 
          NO-LOCK, 
          FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
          FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr NO-LOCK, 
          FIRST gmember WHERE gmember.gastnr = res-line.gastnrmember 
          NO-LOCK BY (res-line.kontakt-nr * res-line.resnr) 
          BY res-line.resstatus BY res-line.NAME:
                RUN assign-it.
                IF res-line.resstatus NE 13 AND res-line.resstatus NE 11 AND res-line.l-zuordnung[3] NE 1 THEN
                    temp-total2 = temp-total2 + res-line.zimmeranz.
                ASSIGN temp-total = INT(temp-total) + INT(res-line.erwachs).
        END.
        ASSIGN troom = string(temp-total2)
               tpax  = string(temp-total).
    END.    
  END. 
END. 
 
PROCEDURE disp-arl6: 
  DEFINE VARIABLE to-name AS CHAR. 
  rmlen = length(room). 
  IF lname NE "" AND SUBSTR(lname,1,1) NE "*" THEN 
    to-name = chr(asc(SUBSTR(lname,1,1)) + 1). 
 
  IF last-sort = 1 THEN 
  DO: 
    IF room NE "" THEN 
    DO: 
      IF lname = "" THEN DO:
            FOR EACH res-line WHERE 
               (res-line.active-flag = 1  AND res-line.resstatus NE 12 
               AND (SUBSTR(res-line.zinr,1,INTEGER(rmlen))) GE room 
               AND res-line.ankunft LE ci-date AND res-line.abreise GE ci-date) OR 
               (res-line.active-flag = 0 
               AND (SUBSTR(res-line.zinr,1,INTEGER(rmlen))) GE room 
               AND res-line.ankunft EQ ci-date) OR 
               (res-line.active-flag = 2 AND res-line.resstatus = 8 
               AND (SUBSTR(res-line.zinr,1,INTEGER(rmlen))) GE room 
               AND res-line.abreise EQ ci-date) NO-LOCK, 
               FIRST waehrung WHERE waehrung.waehrungsnr = res-line.betriebsnr 
               NO-LOCK, 
               FIRST reservation WHERE reservation.resnr = res-line.resnr, 
               FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr, 
               FIRST gmember WHERE gmember.gastnr = res-line.gastnrmember 
               NO-LOCK BY res-line.zinr BY (res-line.kontakt-nr * res-line.resnr) 
               BY res-line.resstatus BY res-line.NAME:
                  RUN assign-it.
                  IF res-line.resstatus NE 13 AND res-line.resstatus NE 11 AND res-line.l-zuordnung[3] NE 1 THEN
                        temp-total2 = temp-total2 + res-line.zimmeranz.
                  ASSIGN temp-total = INT(temp-total) + INT(res-line.erwachs).
            END.
            ASSIGN troom = string(temp-total2)
                   tpax  = string(temp-total).
      END.
      ELSE IF lname NE "" AND SUBSTR(lname,1,1) EQ "*" THEN DO:
            FOR EACH res-line WHERE 
               (res-line.active-flag = 1  AND res-line.resstatus NE 12 
               AND (SUBSTR(res-line.zinr,1,INTEGER(rmlen))) GE room 
               AND res-line.name MATCHES(lname) 
               AND res-line.ankunft LE ci-date AND res-line.abreise GE ci-date) OR 
               (res-line.active-flag = 0 
               AND (SUBSTR(res-line.zinr,1,INTEGER(rmlen))) GE room 
               AND res-line.name MATCHES(lname) 
               AND res-line.ankunft EQ ci-date) OR 
               (res-line.active-flag = 2  AND res-line.resstatus EQ 8 
               AND (SUBSTR(res-line.zinr,1,INTEGER(rmlen))) GE room 
               AND res-line.name MATCHES(lname) 
               AND res-line.abreise EQ ci-date) NO-LOCK, 
               FIRST waehrung WHERE waehrung.waehrungsnr = res-line.betriebsnr 
               NO-LOCK, 
               FIRST reservation WHERE reservation.resnr = res-line.resnr, 
               FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr, 
               FIRST gmember WHERE gmember.gastnr = res-line.gastnrmember 
               NO-LOCK BY res-line.zinr BY (res-line.kontakt-nr * res-line.resnr) 
               BY res-line.resstatus BY res-line.NAME:
                    RUN assign-it.

                    IF res-line.resstatus NE 13 AND res-line.resstatus NE 11 AND res-line.l-zuordnung[3] NE 1 THEN
                            temp-total2 = temp-total2 + res-line.zimmeranz.
                    ASSIGN temp-total = INT(temp-total) + INT(res-line.erwachs).
            END.
            ASSIGN troom = string(temp-total2)
                   tpax  = string(temp-total).
      END.
      ELSE IF lname NE "" AND SUBSTR(lname,1,1) NE "*" THEN DO:
          FOR EACH res-line WHERE 
               (res-line.active-flag = 1  AND res-line.resstatus NE 12 
               AND (SUBSTR(res-line.zinr,1,INTEGER(rmlen))) GE room 
               AND res-line.name GE lname AND res-line.name LE to-name 
               AND res-line.ankunft LE ci-date AND res-line.abreise GE ci-date) OR 
               (res-line.active-flag = 0 
               AND (SUBSTR(res-line.zinr,1,INTEGER(rmlen))) GE room 
               AND res-line.name GE lname AND res-line.name LE to-name 
               AND res-line.ankunft EQ ci-date) OR 
               (res-line.active-flag = 2  AND res-line.resstatus = 8 
               AND (SUBSTR(res-line.zinr,1,INTEGER(rmlen))) GE room 
               AND res-line.name GE lname AND res-line.name LE to-name 
               AND res-line.abreise EQ ci-date) NO-LOCK, 
               FIRST waehrung WHERE waehrung.waehrungsnr = res-line.betriebsnr 
               NO-LOCK, 
               FIRST reservation WHERE reservation.resnr = res-line.resnr, 
               FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr, 
               FIRST gmember WHERE gmember.gastnr = res-line.gastnrmember 
               NO-LOCK BY res-line.zinr BY (res-line.kontakt-nr * res-line.resnr) 
               BY res-line.resstatus BY res-line.NAME:
                    RUN assign-it.
                    IF res-line.resstatus NE 13 AND res-line.resstatus NE 11 AND res-line.l-zuordnung[3] NE 1 THEN
                            temp-total2 = temp-total2 + res-line.zimmeranz.
                    ASSIGN temp-total = INT(temp-total) + INT(res-line.erwachs).
          END.
          ASSIGN troom = string(temp-total2)
                 tpax  = string(temp-total).
      END.      
    END. 
    ELSE IF room = "" THEN 
    DO: 
      IF lname = "" THEN DO:
          FOR EACH res-line WHERE 
           (res-line.active-flag = 1  AND res-line.resstatus NE 12 
           AND res-line.ankunft LE ci-date AND res-line.abreise GE ci-date) OR 
           (res-line.active-flag = 0 AND res-line.ankunft EQ ci-date) OR 
           (res-line.active-flag = 2 AND res-line.resstatus EQ 8 
           AND res-line.abreise EQ ci-date) NO-LOCK, 
           FIRST waehrung WHERE waehrung.waehrungsnr = res-line.betriebsnr 
           NO-LOCK, 
           FIRST reservation WHERE reservation.resnr = res-line.resnr, 
           FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr, 
           FIRST gmember WHERE gmember.gastnr = res-line.gastnrmember 
           NO-LOCK BY (res-line.kontakt-nr * res-line.resnr) 
           BY res-line.resstatus BY res-line.NAME:
                RUN assign-it.
                IF res-line.resstatus NE 13 AND res-line.resstatus NE 11 AND res-line.l-zuordnung[3] NE 1 THEN
                        temp-total2 = temp-total2 + res-line.zimmeranz.
                ASSIGN temp-total = INT(temp-total) + INT(res-line.erwachs).
          END.
          ASSIGN troom = string(temp-total2)
                 tpax  = string(temp-total).
      END.
      ELSE IF lname NE "" AND SUBSTR(lname,1,1) EQ "*" THEN DO:
          FOR EACH res-line WHERE 
           (res-line.active-flag = 1  AND res-line.resstatus NE 12 
           AND res-line.name MATCHES(lname) 
           AND res-line.ankunft LE ci-date AND res-line.abreise GE ci-date) OR 
           (res-line.active-flag = 0 AND res-line.name MATCHES(lname) 
           AND res-line.ankunft EQ ci-date) OR 
           (res-line.active-flag = 2 AND res-line.resstatus EQ 8 
           AND res-line.name MATCHES(lname) 
           AND res-line.abreise EQ ci-date) NO-LOCK, 
           FIRST waehrung WHERE waehrung.waehrungsnr = res-line.betriebsnr 
           NO-LOCK, 
           FIRST reservation WHERE reservation.resnr = res-line.resnr, 
           FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr, 
           FIRST gmember WHERE gmember.gastnr = res-line.gastnrmember 
           NO-LOCK BY res-line.name:
                RUN assign-it.
                IF res-line.resstatus NE 13 AND res-line.resstatus NE 11 AND res-line.l-zuordnung[3] NE 1 THEN
                        temp-total2 = temp-total2 + res-line.zimmeranz.
                ASSIGN temp-total = INT(temp-total) + INT(res-line.erwachs).
          END.
          ASSIGN troom = string(temp-total2)
                 tpax  = string(temp-total).
      END.      
      ELSE IF lname NE "" AND SUBSTR(lname,1,1) NE "*" THEN DO:
            FOR EACH res-line WHERE 
               (res-line.active-flag = 1  AND res-line.resstatus NE 12 
               AND res-line.name GE lname AND res-line.name LE to-name 
               AND res-line.ankunft LE ci-date AND res-line.abreise GE ci-date) OR 
               (res-line.active-flag = 0 
               AND res-line.name GE lname AND res-line.name LE to-name 
               AND res-line.ankunft EQ ci-date) OR 
               (res-line.active-flag = 2  AND res-line.resstatus EQ 8 
               AND res-line.name GE lname AND res-line.name LE to-name 
               AND res-line.abreise EQ ci-date) NO-LOCK, 
               FIRST waehrung WHERE waehrung.waehrungsnr = res-line.betriebsnr 
               NO-LOCK, 
               FIRST reservation WHERE reservation.resnr = res-line.resnr, 
               FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr, 
               FIRST gmember WHERE gmember.gastnr = res-line.gastnrmember 
               NO-LOCK BY res-line.name:
                    RUN assign-it.
                    IF res-line.resstatus NE 13 AND res-line.resstatus NE 11 AND res-line.l-zuordnung[3] NE 1 THEN
                            temp-total2 = temp-total2 + res-line.zimmeranz.
                    ASSIGN temp-total = INT(temp-total) + INT(res-line.erwachs).
            END.
            ASSIGN troom = string(temp-total2)
                 tpax  = string(temp-total).
      END.      
    END. 
  END. 
  ELSE IF last-sort = 2 THEN 
  DO: 
    IF lname = "" AND room = "" THEN DO:
        FOR EACH res-line WHERE 
           (res-line.active-flag = 1 AND res-line.resstatus NE 12 
           AND (SUBSTR(res-line.zinr,1,INTEGER(rmlen))) GE room 
           AND res-line.ankunft LE ci-date AND res-line.abreise GE ci-date) OR 
           (res-line.active-flag = 0 
           AND (SUBSTR(res-line.zinr,1,INTEGER(rmlen))) GE room 
           AND res-line.ankunft EQ ci-date) OR 
           (res-line.active-flag = 2 AND res-line.resstatus EQ 8 
           AND (SUBSTR(res-line.zinr,1,INTEGER(rmlen))) GE room 
           AND res-line.abreise EQ ci-date) NO-LOCK, 
           FIRST waehrung WHERE waehrung.waehrungsnr = res-line.betriebsnr 
           NO-LOCK, 
           FIRST reservation WHERE reservation.resnr = res-line.resnr, 
           FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr, 
           FIRST gmember WHERE gmember.gastnr = res-line.gastnrmember 
           NO-LOCK BY res-line.resname BY res-line.resnr BY res-line.zinr
           BY (res-line.kontakt-nr * res-line.resnr) 
           BY res-line.resstatus BY res-line.NAME:
                RUN assign-it.
                IF res-line.resstatus NE 13 AND res-line.resstatus NE 11 AND res-line.l-zuordnung[3] NE 1 THEN
                        temp-total2 = temp-total2 + res-line.zimmeranz.
                ASSIGN temp-total = INT(temp-total) + INT(res-line.erwachs).
        END.
        ASSIGN troom = string(temp-total2)
               tpax  = string(temp-total).
    END.
    ELSE IF lname = "" AND room NE "" THEN DO:
        FOR EACH res-line WHERE 
           (res-line.active-flag = 1 AND res-line.resstatus NE 12 
           AND (SUBSTR(res-line.zinr,1,INTEGER(rmlen))) GE room 
           AND res-line.ankunft LE ci-date AND res-line.abreise GE ci-date) OR 
           (res-line.active-flag = 0 
           AND (SUBSTR(res-line.zinr,1,INTEGER(rmlen))) GE room 
           AND res-line.ankunft EQ ci-date) OR 
           (res-line.active-flag = 2 AND res-line.resstatus EQ 8 
           AND (SUBSTR(res-line.zinr,1,INTEGER(rmlen))) GE room 
           AND res-line.abreise EQ ci-date) NO-LOCK, 
           FIRST waehrung WHERE waehrung.waehrungsnr = res-line.betriebsnr 
           NO-LOCK, 
           FIRST reservation WHERE reservation.resnr = res-line.resnr, 
           FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr, 
           FIRST gmember WHERE gmember.gastnr = res-line.gastnrmember 
           NO-LOCK BY res-line.zinr
           BY (res-line.kontakt-nr * res-line.resnr) 
           BY res-line.resstatus BY res-line.NAME:
                RUN assign-it.
                IF res-line.resstatus NE 13 AND res-line.resstatus NE 11 AND res-line.l-zuordnung[3] NE 1 THEN
                        temp-total2 = temp-total2 + res-line.zimmeranz.
                ASSIGN temp-total = INT(temp-total) + INT(res-line.erwachs).
        END.
        ASSIGN troom = string(temp-total2)
               tpax  = string(temp-total).
    END.
    ELSE IF lname NE "" AND SUBSTR(lname,1,1) EQ "*" THEN DO:
        FOR EACH res-line WHERE 
           (res-line.active-flag = 1  AND res-line.resstatus NE 12 
           AND (SUBSTR(res-line.zinr,1,INTEGER(rmlen))) GE room 
           AND res-line.resname MATCHES(lname) 
           AND res-line.ankunft LE ci-date AND res-line.abreise GE ci-date) OR 
           (res-line.active-flag = 0 
           AND (SUBSTR(res-line.zinr,1,INTEGER(rmlen))) GE room 
           AND res-line.resname MATCHES(lname) 
           AND res-line.ankunft EQ ci-date) OR 
           (res-line.active-flag = 2  AND res-line.resstatus EQ 8 
           AND (SUBSTR(res-line.zinr,1,INTEGER(rmlen))) GE room 
           AND res-line.resname MATCHES(lname) 
           AND res-line.abreise EQ ci-date) NO-LOCK, 
           FIRST waehrung WHERE waehrung.waehrungsnr = res-line.betriebsnr 
           NO-LOCK, 
           FIRST reservation WHERE reservation.resnr = res-line.resnr, 
           FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr, 
           FIRST gmember WHERE gmember.gastnr = res-line.gastnrmember 
           NO-LOCK BY res-line.resname BY res-line.zinr
           BY (res-line.kontakt-nr * res-line.resnr) 
           BY res-line.resstatus BY res-line.NAME:
                RUN assign-it.
                IF res-line.resstatus NE 13 AND res-line.resstatus NE 11 AND res-line.l-zuordnung[3] NE 1 THEN
                        temp-total2 = temp-total2 + res-line.zimmeranz.
                ASSIGN temp-total = INT(temp-total) + INT(res-line.erwachs).
        END.
        ASSIGN troom = string(temp-total2)
               tpax  = string(temp-total).
    END.
    ELSE IF lname NE "" AND SUBSTR(lname,1,1) NE "*" THEN DO:
        FOR EACH res-line WHERE 
           (res-line.active-flag = 1  AND res-line.resstatus NE 12 
           AND (SUBSTR(res-line.zinr,1,INTEGER(rmlen))) GE room 
           AND res-line.resname GE lname AND res-line.resname LE to-name 
           AND res-line.ankunft LE ci-date AND res-line.abreise GE ci-date) OR 
           (res-line.active-flag = 0 
           AND (SUBSTR(res-line.zinr,1,INTEGER(rmlen))) GE room 
           AND res-line.resname GE lname AND res-line.resname LE to-name 
           AND res-line.ankunft EQ ci-date) OR 
           (res-line.active-flag = 2  AND res-line.resstatus EQ 8 
           AND (SUBSTR(res-line.zinr,1,INTEGER(rmlen))) GE room 
           AND res-line.resname GE lname AND res-line.resname LE to-name 
           AND res-line.abreise EQ ci-date) NO-LOCK, 
           FIRST waehrung WHERE waehrung.waehrungsnr = res-line.betriebsnr 
           NO-LOCK, 
           FIRST reservation WHERE reservation.resnr = res-line.resnr, 
           FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr, 
           FIRST gmember WHERE gmember.gastnr = res-line.gastnrmember 
           NO-LOCK BY res-line.resname BY res-line.zinr
           BY (res-line.kontakt-nr * res-line.resnr) 
           BY res-line.resstatus BY res-line.NAME:
                RUN assign-it.
                IF res-line.resstatus NE 13 AND res-line.resstatus NE 11 AND res-line.l-zuordnung[3] NE 1 THEN
                        temp-total2 = temp-total2 + res-line.zimmeranz.
                ASSIGN temp-total = INT(temp-total) + INT(res-line.erwachs).
        END.
        ASSIGN troom = string(temp-total2)
               tpax  = string(temp-total).
    END.
  END. 
  ELSE IF last-sort = 3 AND lnat = "" THEN 
  DO: 
    IF lname = "" THEN DO:
        FOR EACH res-line WHERE 
           (res-line.active-flag = 1 AND res-line.resstatus NE 12 
           AND res-line.ankunft LE ci-date AND res-line.abreise GE ci-date) OR 
           (res-line.active-flag = 0 
           AND res-line.ankunft EQ ci-date) OR 
           (res-line.active-flag = 2 AND res-line.resstatus EQ 8 
           AND res-line.abreise EQ ci-date) NO-LOCK, 
           FIRST waehrung WHERE waehrung.waehrungsnr = res-line.betriebsnr 
           NO-LOCK, 
           FIRST reservation WHERE reservation.resnr = res-line.resnr, 
           FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr, 
           FIRST gmember WHERE gmember.gastnr = res-line.gastnrmember 
           NO-LOCK BY gmember.nation1
           BY (res-line.kontakt-nr * res-line.resnr) 
           BY res-line.resstatus BY res-line.NAME:
                RUN assign-it.
                IF res-line.resstatus NE 13 AND res-line.resstatus NE 11 AND res-line.l-zuordnung[3] NE 1 THEN
                        temp-total2 = temp-total2 + res-line.zimmeranz.
                ASSIGN temp-total = INT(temp-total) + INT(res-line.erwachs).
        END.
        ASSIGN troom = string(temp-total2)
               tpax  = string(temp-total).
    END.
    ELSE IF lname NE "" AND SUBSTR(lname,1,1) EQ "*" THEN DO:
        FOR EACH res-line WHERE 
           (res-line.active-flag = 1  AND res-line.resstatus NE 12 
           AND res-line.resname MATCHES(lname) 
           AND res-line.ankunft LE ci-date AND res-line.abreise GE ci-date) OR 
           (res-line.active-flag = 0 
           AND res-line.resname MATCHES(lname) 
           AND res-line.ankunft EQ ci-date) OR 
           (res-line.active-flag = 2  AND res-line.resstatus EQ 8 
           AND res-line.resname MATCHES(lname) 
           AND res-line.abreise EQ ci-date) NO-LOCK, 
           FIRST waehrung WHERE waehrung.waehrungsnr = res-line.betriebsnr 
           NO-LOCK, 
           FIRST reservation WHERE reservation.resnr = res-line.resnr, 
           FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr, 
           FIRST gmember WHERE gmember.gastnr = res-line.gastnrmember 
           NO-LOCK BY gmember.nation1
           BY (res-line.kontakt-nr * res-line.resnr) 
           BY res-line.resstatus BY res-line.NAME:
                RUN assign-it.
                IF res-line.resstatus NE 13 AND res-line.resstatus NE 11 AND res-line.l-zuordnung[3] NE 1 THEN
                        temp-total2 = temp-total2 + res-line.zimmeranz.
                ASSIGN temp-total = INT(temp-total) + INT(res-line.erwachs).
        END.
        ASSIGN troom = string(temp-total2)
               tpax  = string(temp-total).
    END.
    ELSE IF lname NE "" AND SUBSTR(lname,1,1) NE "*" THEN DO:
        FOR EACH res-line WHERE 
           (res-line.active-flag = 1  AND res-line.resstatus NE 12 
           AND res-line.resname GE lname AND res-line.resname LE to-name 
           AND res-line.ankunft LE ci-date AND res-line.abreise GE ci-date) OR 
           (res-line.active-flag = 0 
           AND res-line.resname GE lname AND res-line.resname LE to-name 
           AND res-line.ankunft EQ ci-date) OR 
           (res-line.active-flag = 2  AND res-line.resstatus EQ 8 
           AND res-line.resname GE lname AND res-line.resname LE to-name 
           AND res-line.abreise EQ ci-date) NO-LOCK, 
           FIRST waehrung WHERE waehrung.waehrungsnr = res-line.betriebsnr 
           NO-LOCK, 
           FIRST reservation WHERE reservation.resnr = res-line.resnr, 
           FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr, 
           FIRST gmember WHERE gmember.gastnr = res-line.gastnrmember 
           NO-LOCK BY gmember.nation1
           BY (res-line.kontakt-nr * res-line.resnr) 
           BY res-line.resstatus BY res-line.NAME:
                RUN assign-it.
                IF res-line.resstatus NE 13 AND res-line.resstatus NE 11 AND res-line.l-zuordnung[3] NE 1 THEN
                        temp-total2 = temp-total2 + res-line.zimmeranz.
                ASSIGN temp-total = INT(temp-total) + INT(res-line.erwachs).
        END.
        ASSIGN troom = string(temp-total2)
               tpax  = string(temp-total).
    END.    
  END. 
  ELSE IF last-sort = 3 AND lnat NE "" THEN 
  DO: 
    IF lname = "" THEN DO:
        FOR EACH res-line WHERE 
           (res-line.active-flag = 1 AND res-line.resstatus NE 12 
           AND res-line.ankunft LE ci-date AND res-line.abreise GE ci-date) OR 
           (res-line.active-flag = 0 AND res-line.ankunft EQ ci-date) OR 
           (res-line.active-flag = 2 AND res-line.resstatus EQ 8 
           AND res-line.abreise EQ ci-date) NO-LOCK, 
           FIRST waehrung WHERE waehrung.waehrungsnr = res-line.betriebsnr 
           NO-LOCK, 
           FIRST reservation WHERE reservation.resnr = res-line.resnr, 
           FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr, 
           FIRST gmember WHERE gmember.gastnr = res-line.gastnrmember 
           AND gmember.nation1 = lnat 
           NO-LOCK BY gmember.nation1
           BY (res-line.kontakt-nr * res-line.resnr) 
           BY res-line.resstatus BY res-line.NAME:
                RUN assign-it.
                IF res-line.resstatus NE 13 AND res-line.resstatus NE 11 AND res-line.l-zuordnung[3] NE 1 THEN
                        temp-total2 = temp-total2 + res-line.zimmeranz.
                ASSIGN temp-total = INT(temp-total) + INT(res-line.erwachs).
        END.
        ASSIGN troom = string(temp-total2)
               tpax  = string(temp-total).
    END.
    ELSE IF lname NE "" AND SUBSTR(lname,1,1) EQ "*" THEN DO:
        FOR EACH res-line WHERE 
           (res-line.active-flag = 1  AND res-line.resstatus NE 12 
           AND res-line.resname MATCHES(lname) 
           AND res-line.ankunft LE ci-date AND res-line.abreise GE ci-date) OR 
           (res-line.active-flag = 0 
           AND res-line.resname MATCHES(lname) 
           AND res-line.ankunft EQ ci-date) OR 
           (res-line.active-flag = 2  AND res-line.resstatus EQ 8 
           AND res-line.resname MATCHES(lname) 
           AND res-line.abreise EQ ci-date) NO-LOCK, 
           FIRST waehrung WHERE waehrung.waehrungsnr = res-line.betriebsnr 
           NO-LOCK, 
           FIRST reservation WHERE reservation.resnr = res-line.resnr, 
           FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr, 
           FIRST gmember WHERE gmember.gastnr = res-line.gastnrmember 
           AND gmember.nation1 = lnat 
           NO-LOCK BY gmember.nation1
           BY (res-line.kontakt-nr * res-line.resnr) 
           BY res-line.resstatus BY res-line.NAME:
                RUN assign-it.
                IF res-line.resstatus NE 13 AND res-line.resstatus NE 11 AND res-line.l-zuordnung[3] NE 1 THEN
                        temp-total2 = temp-total2 + res-line.zimmeranz.
                ASSIGN temp-total = INT(temp-total) + INT(res-line.erwachs).
        END.
        ASSIGN troom = string(temp-total2)
               tpax  = string(temp-total).
    END.
    ELSE IF lname NE "" AND SUBSTR(lname,1,1) NE "*" THEN DO:
        FOR EACH res-line WHERE 
           (res-line.active-flag = 1  AND res-line.resstatus NE 12 
           AND res-line.resname GE lname AND res-line.resname LE to-name 
           AND res-line.ankunft LE ci-date AND res-line.abreise GE ci-date) OR 
           (res-line.active-flag = 0 
           AND res-line.resname GE lname AND res-line.resname LE to-name 
           AND res-line.ankunft EQ ci-date) OR 
           (res-line.active-flag = 2 AND res-line.resstatus EQ 8 
           AND res-line.resname GE lname AND res-line.resname LE to-name 
           AND res-line.abreise EQ ci-date) NO-LOCK, 
           FIRST waehrung WHERE waehrung.waehrungsnr = res-line.betriebsnr 
           NO-LOCK, 
           FIRST reservation WHERE reservation.resnr = res-line.resnr, 
           FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr, 
           FIRST gmember WHERE gmember.gastnr = res-line.gastnrmember 
           AND gmember.nation1 = lnat 
           NO-LOCK BY gmember.nation1
           BY (res-line.kontakt-nr * res-line.resnr) 
           BY res-line.resstatus BY res-line.NAME:
                RUN assign-it.
                IF res-line.resstatus NE 13 AND res-line.resstatus NE 11 AND res-line.l-zuordnung[3] NE 1 THEN
                        temp-total2 = temp-total2 + res-line.zimmeranz.
                ASSIGN temp-total = INT(temp-total) + INT(res-line.erwachs).
        END.
        ASSIGN troom = string(temp-total2)
               tpax  = string(temp-total).
    END.    
  END. 
  ELSE IF last-sort = 4 THEN 
  DO: 
    IF lresnr = 0 THEN DO:
        FOR EACH res-line WHERE 
          (res-line.active-flag = 1 AND res-line.resstatus NE 12) OR 
          (res-line.active-flag = 0 
          AND res-line.ankunft EQ ci-date) OR 
          (res-line.active-flag = 2 AND res-line.resstatus EQ 8 
          AND res-line.abreise EQ ci-date) NO-LOCK, 
          FIRST waehrung WHERE waehrung.waehrungsnr = res-line.betriebsnr 
          NO-LOCK, 
          FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
          FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr NO-LOCK, 
          FIRST gmember WHERE gmember.gastnr = res-line.gastnrmember 
          NO-LOCK BY res-line.resnr BY (res-line.kontakt-nr * res-line.resnr) 
          BY res-line.resstatus BY res-line.NAME:
                RUN assign-it.
                IF res-line.resstatus NE 13 AND res-line.resstatus NE 11 AND res-line.l-zuordnung[3] NE 1 THEN
                        temp-total2 = temp-total2 + res-line.zimmeranz.
                ASSIGN temp-total = INT(temp-total) + INT(res-line.erwachs).
        END.
        ASSIGN troom = string(temp-total2)
               tpax  = string(temp-total).
    END.    
    ELSE DO:
        FOR EACH res-line WHERE 
          (res-line.active-flag = 1 
          AND res-line.resstatus NE 12 AND res-line.resnr = lresnr) OR 
          (res-line.active-flag = 0 AND res-line.resnr = lresnr 
          AND res-line.ankunft EQ ci-date) OR 
          (res-line.active-flag = 2 AND res-line.resstatus EQ 8 AND res-line.resnr = lresnr 
          AND res-line.abreise EQ ci-date) NO-LOCK, 
          FIRST waehrung WHERE waehrung.waehrungsnr = res-line.betriebsnr 
          NO-LOCK, 
          FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
          FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr NO-LOCK, 
          FIRST gmember WHERE gmember.gastnr = res-line.gastnrmember 
          NO-LOCK BY (res-line.kontakt-nr * res-line.resnr) 
          BY res-line.resstatus BY res-line.NAME:
                RUN assign-it.
                IF res-line.resstatus NE 13 AND res-line.resstatus NE 11 AND res-line.l-zuordnung[3] NE 1 THEN
                        temp-total2 = temp-total2 + res-line.zimmeranz.
                ASSIGN temp-total = INT(temp-total) + INT(res-line.erwachs).
        END.
        ASSIGN troom = string(temp-total2)
               tpax  = string(temp-total).
    END.    
  END. 
END. 
 
 
PROCEDURE count-al1:
  DEFINE VARIABLE to-name AS CHAR. 
 DEFINE BUFFER rline FOR res-line.
 DEFINE BUFFER whrg FOR waehrung.
 DEFINE BUFFER reserv FOR reserv.
 DEFINE BUFFER gme FOR guest.
 DEFINE BUFFER zk FOR zk.
  IF fdate1 = ? THEN 
  DO: 
    IF fdate2 NE ? THEN fdate1 = fdate2. 
    ELSE 
    DO: 
      fdate1 = ci-date. 
      fdate2 = ci-date + 30. 
    END. 
  END. 
  IF fdate2 = ? THEN 
  DO: 
    IF fdate1 NE ? THEN fdate2 = fdate1. 
    ELSE 
    DO: 
      fdate1 = ci-date. 
      fdate2 = ci-date + 30. 
    END. 
  END. 
  IF lname NE "" AND SUBSTR(lname,1,1) NE "*" THEN 
    to-name = chr(asc(SUBSTR(lname,1,1)) + 1). 
 
  IF last-sort = 1 THEN 
  DO: 
    IF lname = "" THEN 
    DO: 
       FOR EACH rline WHERE 
       rline.active-flag = 0 AND rline.ankunft GE fdate1 
       AND rline.ankunft LE fdate2 NO-LOCK, 
       FIRST whrg WHERE whrg.waehrungsnr = rline.betriebsnr 
        NO-LOCK, 
       FIRST reserv WHERE reserv.resnr = rline.resnr, 
       FIRST zk WHERE zk.zikatnr = rline.zikatnr, 
       FIRST gme WHERE gme.gastnr = rline.gastnrmember 
       NO-LOCK BY (rline.kontakt-nr * rline.resnr) BY rline.resstatus 
       BY rline.NAME:
           IF rline.resstatus NE 13 AND rline.resstatus NE 11 AND rline.l-zuordnung[3] NE 1 THEN
            temp-total2 = temp-total2 + rline.zimmeranz.
           temp-total = INT(temp-total) + INT(rline.erwachs).
       END.
       ASSIGN troom = string(temp-total2). 
       ASSIGN tpax = string(temp-total). 
    END.
    ELSE IF lname NE "" AND SUBSTR(lname,1,1) NE "*" THEN 
    DO:
       FOR EACH rline WHERE 
       rline.active-flag = 0 AND rline.ankunft GE fdate1 
       AND rline.ankunft LE fdate2 AND rline.name GE lname 
       AND rline.name LE to-name NO-LOCK, 
       FIRST whrg WHERE whrg.waehrungsnr = rline.betriebsnr 
        NO-LOCK, 
       FIRST reserv WHERE reserv.resnr = rline.resnr, 
       FIRST zk WHERE zk.zikatnr = rline.zikatnr, 
       FIRST gme WHERE gme.gastnr = rline.gastnrmember 
       NO-LOCK BY rline.NAME:
           IF rline.resstatus NE 13 AND rline.resstatus NE 11 AND rline.l-zuordnung[3] NE 1 THEN
            temp-total2 = temp-total2 + rline.zimmeranz.
           temp-total = INT(temp-total) + INT(rline.erwachs).
       END.
       ASSIGN troom = string(temp-total2). 
       ASSIGN tpax = string(temp-total).
    END.
    ELSE IF lname NE "" AND SUBSTR(lname,1,1) EQ "*" THEN 
    DO:
       FOR EACH rline WHERE 
       rline.active-flag = 0 AND rline.ankunft GE fdate1 
       AND rline.ankunft LE fdate2 AND rline.name MATCHES(lname) NO-LOCK, 
       FIRST whrg WHERE whrg.waehrungsnr = rline.betriebsnr 
        NO-LOCK, 
       FIRST reserv WHERE reserv.resnr = rline.resnr, 
       FIRST zk WHERE zk.zikatnr = rline.zikatnr, 
       FIRST gme WHERE gme.gastnr = rline.gastnrmember 
       NO-LOCK BY rline.NAME:
           IF rline.resstatus NE 13 AND rline.resstatus NE 11 AND rline.l-zuordnung[3] NE 1 THEN
            temp-total2 = temp-total2 + rline.zimmeranz.
           temp-total = INT(temp-total) + INT(rline.erwachs).
       END.
       ASSIGN troom = string(temp-total2). 
       ASSIGN tpax = string(temp-total).
    END.
  END. 
  ELSE IF last-sort = 2 THEN 
  DO: 
    IF lname = "" THEN 
    DO:
       FOR EACH rline WHERE 
       rline.active-flag = 0 AND rline.ankunft GE fdate1 
       AND rline.ankunft LE fdate2 NO-LOCK, 
       FIRST whrg WHERE whrg.waehrungsnr = rline.betriebsnr 
       NO-LOCK, 
       FIRST reserv WHERE reserv.resnr = rline.resnr, 
       FIRST zk WHERE zk.zikatnr = rline.zikatnr, 
       FIRST gme WHERE gme.gastnr = rline.gastnrmember 
       NO-LOCK BY rline.resname BY rline.ankunft 
       BY rline.resnr BY (rline.kontakt-nr * rline.resnr) 
       BY rline.resstatus BY rline.NAME:
           IF rline.resstatus NE 13 AND rline.resstatus NE 11 AND rline.l-zuordnung[3] NE 1 THEN
            temp-total2 = temp-total2 + rline.zimmeranz.
           temp-total = INT(temp-total) + INT(rline.erwachs).
       END.
       ASSIGN troom = string(temp-total2).
       ASSIGN tpax = string(temp-total).
    END.
    ELSE IF lname NE "" AND SUBSTR(lname,1,1) NE "*" THEN 
    DO:
       FOR EACH rline WHERE 
       rline.active-flag = 0 AND rline.ankunft GE fdate1 
       AND rline.ankunft LE fdate2 AND rline.resname GE lname 
       AND rline.resname LE to-name NO-LOCK, 
       FIRST whrg WHERE whrg.waehrungsnr = rline.betriebsnr 
       NO-LOCK, 
       FIRST reserv WHERE reserv.resnr = rline.resnr, 
       FIRST zk WHERE zk.zikatnr = rline.zikatnr, 
       FIRST gme WHERE gme.gastnr = rline.gastnrmember 
       NO-LOCK BY rline.resname BY rline.ankunft 
       BY rline.resnr BY (rline.kontakt-nr * rline.resnr) 
       BY rline.resstatus BY rline.NAME:
           IF rline.resstatus NE 13 AND rline.resstatus NE 11 AND rline.l-zuordnung[3] NE 1 THEN
            temp-total2 = temp-total2 + rline.zimmeranz.
           temp-total = INT(temp-total) + INT(rline.erwachs).
       END.
       ASSIGN troom = string(temp-total2).
       ASSIGN tpax = string(temp-total).
    END.
    ELSE IF lname NE "" AND SUBSTR(lname,1,1) EQ "*" THEN 
    DO:
       FOR EACH rline WHERE 
       rline.active-flag = 0 AND rline.ankunft GE fdate1 
       AND rline.ankunft LE fdate2 AND rline.resname MATCHES(lname) 
       NO-LOCK, 
       FIRST whrg WHERE whrg.waehrungsnr = rline.betriebsnr 
       NO-LOCK, 
       FIRST reserv WHERE reserv.resnr = rline.resnr, 
       FIRST zk WHERE zk.zikatnr = rline.zikatnr, 
       FIRST gme WHERE gme.gastnr = rline.gastnrmember 
       NO-LOCK BY rline.resname BY rline.ankunft 
       BY rline.resnr BY (rline.kontakt-nr * rline.resnr) 
       BY rline.resstatus BY rline.NAME:
           IF rline.resstatus NE 13 AND rline.resstatus NE 11 AND rline.l-zuordnung[3] NE 1 THEN
            temp-total2 = temp-total2 + rline.zimmeranz.
           temp-total = INT(temp-total) + INT(rline.erwachs).
       END.
       ASSIGN troom = string(temp-total2).
       ASSIGN tpax = string(temp-total).
    END.
  END. 
  ELSE IF last-sort = 3 AND lnat EQ "" THEN 
  DO: 
    IF lname = "" THEN 
    DO:
      FOR EACH rline WHERE rline.active-flag = 0 
      AND rline.ankunft EQ fdate2 NO-LOCK, 
      FIRST whrg WHERE whrg.waehrungsnr = rline.betriebsnr 
      NO-LOCK, 
      FIRST reserv WHERE reserv.resnr = rline.resnr, 
      FIRST zk WHERE zk.zikatnr = rline.zikatnr, 
      FIRST gme WHERE gme.gastnr = rline.gastnrmember 
      NO-LOCK BY gme.nation1 BY (rline.kontakt-nr * rline.resnr) 
      BY rline.resstatus BY rline.NAME:
        IF rline.resstatus NE 13 AND rline.resstatus NE 11 AND rline.l-zuordnung[3] NE 1 THEN
            temp-total2 = temp-total2 + rline.zimmeranz.
         temp-total = INT(temp-total) + INT(rline.erwachs).
      END.
      ASSIGN troom = string(temp-total2).
      ASSIGN tpax = string(temp-total).
    END.
    ELSE IF lname NE "" AND SUBSTR(lname,1,1) NE "*" THEN 
    DO:
      FOR EACH rline WHERE rline.active-flag = 0 
      AND rline.ankunft EQ fdate2 
      AND rline.name GE lname AND rline.name LE to-name NO-LOCK, 
      FIRST whrg WHERE whrg.waehrungsnr = rline.betriebsnr 
      NO-LOCK, 
      FIRST reserv WHERE reserv.resnr = rline.resnr, 
      FIRST zk WHERE zk.zikatnr = rline.zikatnr, 
      FIRST gme WHERE gme.gastnr = rline.gastnrmember 
      NO-LOCK BY gme.nation1 BY (rline.kontakt-nr * rline.resnr) 
      BY rline.resstatus BY rline.NAME:
          IF rline.resstatus NE 13 AND rline.resstatus NE 11 AND rline.l-zuordnung[3] NE 1 THEN
            temp-total2 = temp-total2 + rline.zimmeranz.
          temp-total = INT(temp-total) + INT(rline.erwachs).
      END.
      ASSIGN troom = string(temp-total2).
      ASSIGN tpax = string(temp-total).
    END.
    ELSE IF lname NE "" AND SUBSTR(lname,1,1) EQ "*" THEN 
    DO:
      FOR EACH rline WHERE rline.active-flag = 0 
      AND rline.ankunft EQ fdate2 
      AND rline.name MATCHES(lname) NO-LOCK, 
      FIRST whrg WHERE whrg.waehrungsnr = rline.betriebsnr 
      NO-LOCK, 
      FIRST reserv WHERE reserv.resnr = rline.resnr, 
      FIRST zk WHERE zk.zikatnr = rline.zikatnr, 
      FIRST gme WHERE gme.gastnr = rline.gastnrmember 
      NO-LOCK BY gme.nation1 BY (rline.kontakt-nr * rline.resnr) 
      BY rline.resstatus BY rline.NAME:
         IF rline.resstatus NE 13 AND rline.resstatus NE 11 AND rline.l-zuordnung[3] NE 1 THEN
            temp-total2 = temp-total2 + rline.zimmeranz.
          temp-total = INT(temp-total) + INT(rline.erwachs).
      END.
      ASSIGN troom = string(temp-total2).
      ASSIGN tpax = string(temp-total).
    END.
  END. 
  ELSE IF last-sort = 3 AND lnat NE "" THEN 
  DO: 
    IF lname = "" THEN 
    DO:
      FOR EACH rline WHERE rline.active-flag = 0 
      AND rline.ankunft EQ fdate2 NO-LOCK, 
      FIRST whrg WHERE whrg.waehrungsnr = rline.betriebsnr 
      NO-LOCK, 
      FIRST reserv WHERE reserv.resnr = rline.resnr, 
      FIRST zk WHERE zk.zikatnr = rline.zikatnr, 
      FIRST gme WHERE gme.gastnr = rline.gastnrmember 
      AND gme.nation1 = lnat NO-LOCK 
      BY (rline.kontakt-nr * rline.resnr) 
      BY rline.resstatus BY rline.NAME:
         IF rline.resstatus NE 13 AND rline.resstatus NE 11 AND rline.l-zuordnung[3] NE 1 THEN
            temp-total2 = temp-total2 + rline.zimmeranz.
          temp-total = INT(temp-total) + INT(rline.erwachs).
      END.
      ASSIGN troom = string(temp-total2).
      ASSIGN tpax = string(temp-total).
    END.
    ELSE IF lname NE "" AND SUBSTR(lname,1,1) NE "*" THEN 
    DO:
      FOR EACH rline WHERE rline.active-flag = 0 
      AND rline.ankunft EQ fdate2 
      AND rline.name GE lname AND rline.name LE to-name NO-LOCK, 
      FIRST whrg WHERE whrg.waehrungsnr = rline.betriebsnr 
      NO-LOCK, 
      FIRST reserv WHERE reserv.resnr = rline.resnr, 
      FIRST zk WHERE zk.zikatnr = rline.zikatnr, 
      FIRST gme WHERE gme.gastnr = rline.gastnrmember 
      AND gme.nation1 = lnat NO-LOCK BY gme.nation1
      BY (rline.kontakt-nr * rline.resnr) 
      BY rline.resstatus BY rline.NAME:
          IF rline.resstatus NE 13 AND rline.resstatus NE 11 AND rline.l-zuordnung[3] NE 1 THEN
            temp-total2 = temp-total2 + rline.zimmeranz.
          temp-total = INT(temp-total) + INT(rline.erwachs).
      END.
      ASSIGN troom = string(temp-total2).
      ASSIGN tpax = string(temp-total).
    END.
    ELSE IF lname NE "" AND SUBSTR(lname,1,1) EQ "*" THEN 
    DO:
      FOR EACH rline WHERE rline.active-flag = 0 
      AND rline.ankunft EQ fdate2 
      AND rline.name MATCHES(lname) NO-LOCK, 
      FIRST whrg WHERE whrg.waehrungsnr = rline.betriebsnr 
      NO-LOCK, 
      FIRST reserv WHERE reserv.resnr = rline.resnr, 
      FIRST zk WHERE zk.zikatnr = rline.zikatnr, 
      FIRST gme WHERE gme.gastnr = rline.gastnrmember 
      AND gme.nation1 = lnat NO-LOCK BY gme.nation1
      BY (rline.kontakt-nr * rline.resnr) 
      BY rline.resstatus BY rline.NAME:
          IF rline.resstatus NE 13 AND rline.resstatus NE 11 AND rline.l-zuordnung[3] NE 1 THEN
            temp-total2 = temp-total2 + rline.zimmeranz.
          temp-total = INT(temp-total) + INT(rline.erwachs).
      END.
      ASSIGN troom = string(temp-total2).
      ASSIGN tpax = string(temp-total).
    END.
  END. 
  ELSE IF last-sort = 4 THEN 
  DO: 
    IF lresnr = 0 THEN 
    DO:
      FOR EACH rline WHERE rline.active-flag = 0 
      AND rline.ankunft EQ ci-date NO-LOCK, 
      FIRST whrg WHERE whrg.waehrungsnr = rline.betriebsnr 
      NO-LOCK, 
      FIRST reserv WHERE reserv.resnr = rline.resnr, 
      FIRST zk WHERE zk.zikatnr = rline.zikatnr, 
      FIRST gme WHERE gme.gastnr = rline.gastnrmember 
      NO-LOCK BY rline.resnr
      BY (rline.kontakt-nr * rline.resnr) 
      BY rline.resstatus BY rline.NAME:
           IF rline.resstatus NE 13 AND rline.resstatus NE 11 AND rline.l-zuordnung[3] NE 1 THEN
            temp-total2 = temp-total2 + rline.zimmeranz.
          temp-total = INT(temp-total) + INT(rline.erwachs).
      END.
      ASSIGN troom = string(temp-total2).
      ASSIGN tpax = string(temp-total).
    END.
    ELSE 
    DO:
      FOR EACH rline WHERE rline.active-flag = 0 
      AND rline.resnr EQ lresnr NO-LOCK, 
      FIRST whrg WHERE whrg.waehrungsnr = rline.betriebsnr 
      NO-LOCK, 
      FIRST reserv WHERE reserv.resnr = rline.resnr, 
      FIRST zk WHERE zk.zikatnr = rline.zikatnr, 
      FIRST gme WHERE gme.gastnr = rline.gastnrmember 
      NO-LOCK BY (rline.kontakt-nr * rline.resnr) 
      BY rline.resstatus BY rline.NAME:
           IF rline.resstatus NE 13 AND rline.resstatus NE 11 AND rline.l-zuordnung[3] NE 1 THEN
            temp-total2 = temp-total2 + rline.zimmeranz.
          temp-total = INT(temp-total) + INT(rline.erwachs).
      END.
      ASSIGN troom = string(temp-total2).
      ASSIGN tpax = string(temp-total).
    END.
  END. 
END.
PROCEDURE count-all2:
 DEFINE VARIABLE to-name AS CHAR. 
 DEFINE BUFFER rline FOR res-line.
 DEFINE BUFFER whrg FOR waehrung.
 DEFINE BUFFER reserv FOR reserv.
 DEFINE BUFFER gme FOR guest.
 DEFINE BUFFER zk FOR zk.
  IF lname NE "" AND SUBSTR(lname,1,1) NE "*" THEN 
    to-name = chr(asc(SUBSTR(lname,1,1)) + 1). 
 
  IF last-sort = 1 THEN 
  DO: 
    IF room NE "" THEN 
    DO: 
      IF lname = "" THEN 
      DO:
       FOR EACH rline WHERE 
       rline.active-flag = 1  AND rline.resstatus NE 12 
       AND (SUBSTR(rline.zinr,1,INTEGER(rmlen))) GE room 
       AND rline.ankunft LE ci-date AND rline.abreise GE ci-date 
       NO-LOCK, 
       FIRST whrg WHERE whrg.waehrungsnr = rline.betriebsnr 
       NO-LOCK, 
       FIRST reserv WHERE reserv.resnr = rline.resnr, 
       FIRST zk WHERE zk.zikatnr = rline.zikatnr, 
       FIRST gme WHERE gme.gastnr = rline.gastnrmember 
       NO-LOCK BY rline.zinr BY (rline.kontakt-nr * rline.resnr) 
       BY rline.resstatus BY rline.NAME:
          IF rline.resstatus NE 13 AND rline.resstatus NE 11 AND rline.l-zuordnung[3] NE 1 THEN
            temp-total2 = temp-total2 + rline.zimmeranz.
          temp-total = INT(temp-total) + INT(rline.erwachs).
       END.
       ASSIGN troom = string(temp-total2).
       ASSIGN tpax = string(temp-total).
      END.
      ELSE IF lname NE "" AND SUBSTR(lname,1,1) EQ "*" THEN 
      DO:
       FOR EACH rline WHERE 
       rline.active-flag = 1  AND rline.resstatus NE 12 
       AND (SUBSTR(rline.zinr,1,INTEGER(rmlen))) GE room 
       AND rline.name MATCHES(lname) 
       AND rline.ankunft LE ci-date AND rline.abreise GE ci-date NO-LOCK, 
       FIRST whrg WHERE whrg.waehrungsnr = rline.betriebsnr 
       NO-LOCK, 
       FIRST reserv WHERE reserv.resnr = rline.resnr, 
       FIRST zk WHERE zk.zikatnr = rline.zikatnr, 
       FIRST gme WHERE gme.gastnr = rline.gastnrmember 
       NO-LOCK BY rline.zinr BY (rline.kontakt-nr * rline.resnr) 
       BY rline.resstatus BY rline.NAME:
           IF rline.resstatus NE 13 AND rline.resstatus NE 11 AND rline.l-zuordnung[3] NE 1 THEN
            temp-total2 = temp-total2 + rline.zimmeranz.
           temp-total = INT(temp-total) + INT(rline.erwachs).
       END.
       ASSIGN troom = string(temp-total2).
       ASSIGN tpax = string(temp-total).
      END.
      ELSE IF lname NE "" AND SUBSTR(lname,1,1) NE "*" THEN 
      DO:
       IF ci-date NE ? THEN /* Malik Samansya 285 */
       DO: 
        FOR EACH rline WHERE 
        rline.active-flag = 1  AND rline.resstatus NE 12 
        AND (SUBSTR(rline.zinr,1,INTEGER(rmlen))) GE room 
        AND rline.name GE lname AND rline.name LE to-name 
        AND rline.ankunft LE ci-date AND rline.abreise GE ci-date NO-LOCK, 
        FIRST whrg WHERE whrg.waehrungsnr = rline.betriebsnr 
        NO-LOCK, 
        FIRST reserv WHERE reserv.resnr = rline.resnr, 
        FIRST zk WHERE zk.zikatnr = rline.zikatnr, 
        FIRST gme WHERE gme.gastnr = rline.gastnrmember 
        NO-LOCK BY rline.zinr BY (rline.kontakt-nr * rline.resnr) 
        BY rline.resstatus BY rline.NAME:
            IF rline.resstatus NE 13 AND rline.resstatus NE 11 AND rline.l-zuordnung[3] NE 1 THEN
              temp-total2 = temp-total2 + rline.zimmeranz.
            temp-total = INT(temp-total) + INT(rline.erwachs).
        END.
        ASSIGN troom = string(temp-total2).
        ASSIGN tpax = string(temp-total).
       END.
       /* END Malik */
      END.
    END. 
    ELSE IF room = "" THEN 
    DO: 
      IF lname = "" THEN 
      DO:
       FOR EACH rline WHERE 
       rline.active-flag = 1  AND rline.resstatus NE 12 
       AND rline.ankunft LE ci-date AND rline.abreise GE ci-date, 
       FIRST whrg WHERE whrg.waehrungsnr = rline.betriebsnr 
       NO-LOCK, 
       FIRST reserv WHERE reserv.resnr = rline.resnr NO-LOCK, 
       FIRST zk WHERE zk.zikatnr = rline.zikatnr, 
       FIRST gme WHERE gme.gastnr = rline.gastnrmember 
       NO-LOCK BY (rline.kontakt-nr * rline.resnr) 
       BY rline.resstatus BY rline.NAME:
            IF rline.resstatus NE 13 AND rline.resstatus NE 11 AND rline.l-zuordnung[3] NE 1 THEN
            temp-total2 = temp-total2 + rline.zimmeranz.
           temp-total = INT(temp-total) + INT(rline.erwachs).
       END.
       ASSIGN troom = string(temp-total2).
       ASSIGN tpax = string(temp-total).
      END.
      ELSE IF lname NE "" AND SUBSTR(lname,1,1) EQ "*" THEN 
      DO:
       FOR EACH rline WHERE 
       rline.active-flag = 1  AND rline.resstatus NE 12 
       AND rline.name MATCHES(lname) 
       AND rline.ankunft LE ci-date AND rline.abreise GE ci-date NO-LOCK, 
       FIRST whrg WHERE whrg.waehrungsnr = rline.betriebsnr 
       NO-LOCK, 
       FIRST reserv WHERE reserv.resnr = rline.resnr, 
       FIRST zk WHERE zk.zikatnr = rline.zikatnr, 
       FIRST gme WHERE gme.gastnr = rline.gastnrmember 
       NO-LOCK BY rline.NAME:
           IF rline.resstatus NE 13 AND rline.resstatus NE 11 AND rline.l-zuordnung[3] NE 1 THEN
            temp-total2 = temp-total2 + rline.zimmeranz.
           temp-total = INT(temp-total) + INT(rline.erwachs).
       END.
       ASSIGN troom = string(temp-total2).
       ASSIGN tpax = string(temp-total).
      END.
      ELSE IF lname NE "" AND SUBSTR(lname,1,1) NE "*" THEN 
      DO:
       FOR EACH rline WHERE 
       rline.active-flag = 1  AND rline.resstatus NE 12 
       AND rline.name GE lname AND rline.name LE to-name 
       AND rline.ankunft LE ci-date AND rline.abreise GE ci-date NO-LOCK, 
       FIRST whrg WHERE whrg.waehrungsnr = rline.betriebsnr 
       NO-LOCK, 
       FIRST reserv WHERE reserv.resnr = rline.resnr, 
       FIRST zk WHERE zk.zikatnr = rline.zikatnr, 
       FIRST gme WHERE gme.gastnr = rline.gastnrmember 
       NO-LOCK BY rline.NAME:
          IF rline.resstatus NE 13 AND rline.resstatus NE 11 AND rline.l-zuordnung[3] NE 1 THEN
            temp-total2 = temp-total2 + rline.zimmeranz.
           temp-total = INT(temp-total) + INT(rline.erwachs).
       END.
       ASSIGN troom = string(temp-total2).
       ASSIGN tpax = string(temp-total).
      END.
    END. 
  END. 
  ELSE IF last-sort = 2 THEN 
  DO: 
    IF lname = "" AND room = "" THEN 
    DO:
       FOR EACH rline WHERE 
       rline.active-flag = 1 AND rline.resstatus NE 12 
       AND (SUBSTR(rline.zinr,1,INTEGER(rmlen))) GE room 
       AND rline.ankunft LE ci-date AND rline.abreise GE ci-date NO-LOCK, 
       FIRST whrg WHERE whrg.waehrungsnr = rline.betriebsnr 
       NO-LOCK, 
       FIRST reserv WHERE reserv.resnr = rline.resnr, 
       FIRST zk WHERE zk.zikatnr = rline.zikatnr, 
       FIRST gme WHERE gme.gastnr = rline.gastnrmember 
       NO-LOCK BY rline.resname BY rline.resnr BY rline.zinr
       BY (rline.kontakt-nr * rline.resnr) BY rline.resstatus 
       BY rline.NAME:
            IF rline.resstatus NE 13 AND rline.resstatus NE 11 AND rline.l-zuordnung[3] NE 1 THEN
            temp-total2 = temp-total2 + rline.zimmeranz.
           temp-total = INT(temp-total) + INT(rline.erwachs).
       END.
       ASSIGN troom = string(temp-total2).
       ASSIGN tpax = string(temp-total).
    END.
    ELSE IF lname = "" AND room NE "" THEN 
    DO:
       FOR EACH rline WHERE 
       rline.active-flag = 1 AND rline.resstatus NE 12 
       AND (SUBSTR(rline.zinr,1,INTEGER(rmlen))) GE room 
       AND rline.ankunft LE ci-date AND rline.abreise GE ci-date NO-LOCK, 
       FIRST whrg WHERE whrg.waehrungsnr = rline.betriebsnr 
       NO-LOCK, 
       FIRST reserv WHERE reserv.resnr = rline.resnr, 
       FIRST zk WHERE zk.zikatnr = rline.zikatnr, 
       FIRST gme WHERE gme.gastnr = rline.gastnrmember 
       NO-LOCK BY rline.zinr BY rline.resname
       BY (rline.kontakt-nr * rline.resnr) BY rline.resstatus 
       BY rline.NAME:
            IF rline.resstatus NE 13 AND rline.resstatus NE 11 AND rline.l-zuordnung[3] NE 1 THEN
            temp-total2 = temp-total2 + rline.zimmeranz.
           temp-total = INT(temp-total) + INT(rline.erwachs).
       END.
       ASSIGN troom = string(temp-total2).
       ASSIGN tpax = string(temp-total).
    END.
    ELSE IF lname NE "" AND SUBSTR(lname,1,1) EQ "*" THEN 
    DO:
       FOR EACH rline WHERE 
       rline.active-flag = 1  AND rline.resstatus NE 12 
       AND (SUBSTR(rline.zinr,1,INTEGER(rmlen))) GE room 
       AND rline.resname MATCHES(lname) 
       AND rline.ankunft LE ci-date AND rline.abreise GE ci-date NO-LOCK, 
       FIRST whrg WHERE whrg.waehrungsnr = rline.betriebsnr 
       NO-LOCK, 
       FIRST reserv WHERE reserv.resnr = rline.resnr, 
       FIRST zk WHERE zk.zikatnr = rline.zikatnr, 
       FIRST gme WHERE gme.gastnr = rline.gastnrmember 
       NO-LOCK BY rline.resname BY rline.zinr
       BY (rline.kontakt-nr * rline.resnr) 
       BY rline.resstatus BY rline.NAME:
           IF rline.resstatus NE 13 AND rline.resstatus NE 11 AND rline.l-zuordnung[3] NE 1 THEN
            temp-total2 = temp-total2 + rline.zimmeranz.
           temp-total = INT(temp-total) + INT(rline.erwachs).
       END.
       ASSIGN troom = string(temp-total2).
       ASSIGN tpax = string(temp-total).
    END.
    ELSE IF lname NE "" AND SUBSTR(lname,1,1) NE "*" THEN 
    DO:
       FOR EACH rline WHERE 
       rline.active-flag = 1  AND rline.resstatus NE 12 
       AND (SUBSTR(rline.zinr,1,INTEGER(rmlen))) GE room 
       AND rline.resname GE lname AND rline.resname LE to-name 
       AND rline.ankunft LE ci-date AND rline.abreise GE ci-date NO-LOCK, 
       FIRST whrg WHERE whrg.waehrungsnr = rline.betriebsnr 
       NO-LOCK, 
       FIRST reserv WHERE reserv.resnr = rline.resnr, 
       FIRST zk WHERE zk.zikatnr = rline.zikatnr, 
       FIRST gme WHERE gme.gastnr = rline.gastnrmember 
       NO-LOCK BY rline.resname BY rline.zinr
       BY (rline.kontakt-nr * rline.resnr) 
       BY rline.resstatus BY rline.NAME:
            IF rline.resstatus NE 13 AND rline.resstatus NE 11 AND rline.l-zuordnung[3] NE 1 THEN
            temp-total2 = temp-total2 + rline.zimmeranz.
           temp-total = INT(temp-total) + INT(rline.erwachs).
       END.
       ASSIGN troom = string(temp-total2).
       ASSIGN tpax = string(temp-total).
    END.
  END. 
  ELSE IF last-sort = 3 AND lnat = "" THEN 
  DO: 
    IF lname = "" THEN 
    DO:
       FOR EACH rline WHERE 
       rline.active-flag = 1 AND rline.resstatus NE 12 
       AND rline.ankunft LE ci-date AND rline.abreise GE ci-date NO-LOCK, 
       FIRST whrg WHERE whrg.waehrungsnr = rline.betriebsnr 
       NO-LOCK, 
       FIRST reserv WHERE reserv.resnr = rline.resnr, 
       FIRST zk WHERE zk.zikatnr = rline.zikatnr, 
       FIRST gme WHERE gme.gastnr = rline.gastnrmember 
       NO-LOCK BY gme.nation1 BY (rline.kontakt-nr * rline.resnr) 
       BY rline.resstatus BY rline.NAME:
           IF rline.resstatus NE 13 AND rline.resstatus NE 11 AND rline.l-zuordnung[3] NE 1 THEN
            temp-total2 = temp-total2 + rline.zimmeranz.
           temp-total = INT(temp-total) + INT(rline.erwachs).
       END.
       ASSIGN troom = string(temp-total2).
       ASSIGN tpax = string(temp-total).
    END.
    ELSE IF lname NE "" AND SUBSTR(lname,1,1) EQ "*" THEN 
    DO:
       FOR EACH rline WHERE 
       rline.active-flag = 1  AND rline.resstatus NE 12 
       AND rline.resname MATCHES(lname) 
       AND rline.ankunft LE ci-date AND rline.abreise GE ci-date NO-LOCK, 
       FIRST whrg WHERE whrg.waehrungsnr = rline.betriebsnr 
       NO-LOCK, 
       FIRST reserv WHERE reserv.resnr = rline.resnr, 
       FIRST zk WHERE zk.zikatnr = rline.zikatnr, 
       FIRST gme WHERE gme.gastnr = rline.gastnrmember 
       NO-LOCK BY gme.nation1 BY (rline.kontakt-nr * rline.resnr) 
       BY rline.resstatus BY rline.NAME:
          IF rline.resstatus NE 13 AND rline.resstatus NE 11 AND rline.l-zuordnung[3] NE 1 THEN
            temp-total2 = temp-total2 + rline.zimmeranz.
           temp-total = INT(temp-total) + INT(rline.erwachs).
       END.
       ASSIGN troom = string(temp-total2).
       ASSIGN tpax = string(temp-total).
    END.
    ELSE IF lname NE "" AND SUBSTR(lname,1,1) NE "*" THEN 
    DO:                                                   
       FOR EACH rline WHERE 
       rline.active-flag = 1  AND rline.resstatus NE 12 
       AND rline.resname GE lname AND rline.resname LE to-name 
       AND rline.ankunft LE ci-date AND rline.abreise GE ci-date NO-LOCK, 
       FIRST whrg WHERE whrg.waehrungsnr = rline.betriebsnr 
       NO-LOCK, 
       FIRST reserv WHERE reserv.resnr = rline.resnr, 
       FIRST zk WHERE zk.zikatnr = rline.zikatnr, 
       FIRST gme WHERE gme.gastnr = rline.gastnrmember 
       NO-LOCK BY gme.nation1 BY (rline.kontakt-nr * rline.resnr) 
       BY rline.resstatus BY rline.NAME:
          IF rline.resstatus NE 13 AND rline.resstatus NE 11 AND rline.l-zuordnung[3] NE 1 THEN
            temp-total2 = temp-total2 + rline.zimmeranz.
           temp-total = INT(temp-total) + INT(rline.erwachs).
       END.
       ASSIGN troom = string(temp-total2).
       ASSIGN tpax = string(temp-total).
    END.
  END. 
  ELSE IF last-sort = 3 AND lnat NE "" THEN 
  DO: 
    IF lname = "" THEN 
    DO:
       FOR EACH rline WHERE 
       rline.active-flag = 1 AND rline.resstatus NE 12 
       AND rline.ankunft LE ci-date AND rline.abreise GE ci-date NO-LOCK, 
       FIRST whrg WHERE whrg.waehrungsnr = rline.betriebsnr 
       NO-LOCK, 
       FIRST reserv WHERE reserv.resnr = rline.resnr, 
       FIRST zk WHERE zk.zikatnr = rline.zikatnr, 
       FIRST gme WHERE gme.gastnr = rline.gastnrmember 
       AND gme.nation1 = lnat 
       NO-LOCK BY gme.nation1 BY (rline.kontakt-nr * rline.resnr) 
       BY rline.resstatus BY rline.NAME:
          IF rline.resstatus NE 13 AND rline.resstatus NE 11 AND rline.l-zuordnung[3] NE 1 THEN
            temp-total2 = temp-total2 + rline.zimmeranz.
           temp-total = INT(temp-total) + INT(rline.erwachs).
       END.
       ASSIGN troom = string(temp-total2).
       ASSIGN tpax = string(temp-total).
    END.
    ELSE IF lname NE "" AND SUBSTR(lname,1,1) EQ "*" THEN 
    DO:
       FOR EACH rline WHERE 
       rline.active-flag = 1  AND rline.resstatus NE 12 
       AND rline.resname MATCHES(lname) 
       AND rline.ankunft LE ci-date AND rline.abreise GE ci-date NO-LOCK, 
       FIRST whrg WHERE whrg.waehrungsnr = rline.betriebsnr 
       NO-LOCK, 
       FIRST reserv WHERE reserv.resnr = rline.resnr, 
       FIRST zk WHERE zk.zikatnr = rline.zikatnr, 
       FIRST gme WHERE gme.gastnr = rline.gastnrmember 
       AND gme.nation1 = lnat 
       NO-LOCK BY gme.nation1 BY (rline.kontakt-nr * rline.resnr) 
       BY rline.resstatus BY rline.NAME:
           IF rline.resstatus NE 13 AND rline.resstatus NE 11 AND rline.l-zuordnung[3] NE 1 THEN
            temp-total2 = temp-total2 + rline.zimmeranz.
           temp-total = INT(temp-total) + INT(rline.erwachs).
       END.
       ASSIGN troom = string(temp-total2).
       ASSIGN tpax = string(temp-total).
    END.
    ELSE IF lname NE "" AND SUBSTR(lname,1,1) NE "*" THEN 
    DO:
       FOR EACH rline WHERE 
       rline.active-flag = 1  AND rline.resstatus NE 12 
       AND rline.resname GE lname AND rline.resname LE to-name 
       AND rline.ankunft LE ci-date AND rline.abreise GE ci-date NO-LOCK, 
       FIRST whrg WHERE whrg.waehrungsnr = rline.betriebsnr 
       NO-LOCK, 
       FIRST reserv WHERE reserv.resnr = rline.resnr, 
       FIRST zk WHERE zk.zikatnr = rline.zikatnr, 
       FIRST gme WHERE gme.gastnr = rline.gastnrmember 
       AND gme.nation1 = lnat 
       NO-LOCK BY gme.nation1 BY (rline.kontakt-nr * rline.resnr) 
       BY rline.resstatus BY rline.NAME:
           IF rline.resstatus NE 13 AND rline.resstatus NE 11 AND rline.l-zuordnung[3] NE 1 THEN
            temp-total2 = temp-total2 + rline.zimmeranz.
           temp-total = INT(temp-total) + INT(rline.erwachs).
       END.
       ASSIGN troom = string(temp-total2).
       ASSIGN tpax = string(temp-total).
    END.
  END. 
  ELSE IF last-sort = 4 THEN 
  DO: 
    IF lresnr = 0 THEN 
    DO:
      FOR EACH rline WHERE rline.active-flag = 1 
      AND rline.resstatus NE 12 NO-LOCK, 
      FIRST whrg WHERE whrg.waehrungsnr = rline.betriebsnr 
      NO-LOCK, 
      FIRST reserv WHERE reserv.resnr = rline.resnr NO-LOCK, 
      FIRST zk WHERE zk.zikatnr = rline.zikatnr NO-LOCK, 
      FIRST gme WHERE gme.gastnr = rline.gastnrmember 
      NO-LOCK BY rline.resnr BY (rline.kontakt-nr * rline.resnr) 
      BY rline.resstatus BY rline.NAME:
          IF rline.resstatus NE 13 AND rline.resstatus NE 11 AND rline.l-zuordnung[3] NE 1 THEN
            temp-total2 = temp-total2 + rline.zimmeranz.
          temp-total = INT(temp-total) + INT(rline.erwachs).
      END.
      ASSIGN troom = string(temp-total2).
      ASSIGN tpax = string(temp-total).
    END.
    ELSE 
    DO:
      FOR EACH rline WHERE rline.active-flag = 1 
      AND rline.resstatus NE 12 AND rline.resnr = lresnr NO-LOCK, 
      FIRST whrg WHERE whrg.waehrungsnr = rline.betriebsnr 
      NO-LOCK, 
      FIRST reserv WHERE reserv.resnr = rline.resnr NO-LOCK, 
      FIRST zk WHERE zk.zikatnr = rline.zikatnr NO-LOCK, 
      FIRST gme WHERE gme.gastnr = rline.gastnrmember 
      NO-LOCK BY rline.NAME:
          IF rline.resstatus NE 13 AND rline.resstatus NE 11 AND rline.l-zuordnung[3] NE 1 THEN
            temp-total2 = temp-total2 + rline.zimmeranz.
          temp-total = INT(temp-total) + INT(rline.erwachs).
      END.
      ASSIGN troom = string(temp-total2). 
      ASSIGN tpax = string(temp-total). 
    END.                          
  END. 
END.
PROCEDURE count-all4:
    
 DEFINE VARIABLE to-name AS CHAR. 
 DEFINE BUFFER rline FOR res-line.
 DEFINE BUFFER whrg FOR waehrung.
 DEFINE BUFFER reserv FOR reserv.
 DEFINE BUFFER gme FOR guest.
 DEFINE BUFFER zk FOR zk.
  IF lname NE "" AND SUBSTR(lname,1,1) NE "*" THEN 
    to-name = chr(asc(SUBSTR(lname,1,1)) + 1). 
 
  IF last-sort = 1 THEN 
  DO: 
    IF room NE "" THEN 
    DO: 
      IF lname = "" AND room = "" THEN 
      DO:
       FOR EACH rline WHERE 
       rline.active-flag = 1  AND rline.resstatus NE 12 
       AND (SUBSTR(rline.zinr,1,INTEGER(rmlen))) GE room 
       AND rline.abreise EQ ci-date NO-LOCK, 
       FIRST whrg WHERE whrg.waehrungsnr = rline.betriebsnr 
       NO-LOCK, 
       FIRST reserv WHERE reserv.resnr = rline.resnr, 
       FIRST zk WHERE zk.zikatnr = rline.zikatnr, 
       FIRST gme WHERE gme.gastnr = rline.gastnrmember 
       NO-LOCK BY rline.zinr BY (rline.kontakt-nr * rline.resnr) 
       BY rline.resstatus BY rline.NAME:
            IF rline.resstatus NE 13 AND rline.resstatus NE 11 AND rline.l-zuordnung[3] NE 1 THEN
            temp-total2 = temp-total2 + rline.zimmeranz.
            temp-total = INT(temp-total) + INT(rline.erwachs).
        END.
        ASSIGN troom = string(temp-total2). 
        ASSIGN tpax = string(temp-total). 
      END.
      ELSE IF lname NE "" AND SUBSTR(lname,1,1) EQ "*" THEN 
      DO:
       FOR EACH rline WHERE 
       rline.active-flag = 1  AND rline.resstatus NE 12 
       AND (SUBSTR(rline.zinr,1,INTEGER(rmlen))) GE room 
       AND rline.name MATCHES(lname) 
       AND rline.abreise EQ ci-date NO-LOCK, 
       FIRST whrg WHERE whrg.waehrungsnr = rline.betriebsnr 
       NO-LOCK, 
       FIRST reserv WHERE reserv.resnr = rline.resnr, 
       FIRST zk WHERE zk.zikatnr = rline.zikatnr, 
       FIRST gme WHERE gme.gastnr = rline.gastnrmember 
       NO-LOCK BY rline.zinr BY (rline.kontakt-nr * rline.resnr) 
       BY rline.resstatus BY rline.NAME:
            IF rline.resstatus NE 13 AND rline.resstatus NE 11 AND rline.l-zuordnung[3] NE 1 THEN
            temp-total2 = temp-total2 + rline.zimmeranz.
            temp-total = INT(temp-total) + INT(rline.erwachs).
       END.
       ASSIGN troom = string(temp-total2). 
       ASSIGN tpax = string(temp-total). 
      END.
      ELSE IF lname NE "" AND SUBSTR(lname,1,1) NE "*" THEN 
      DO:
       FOR EACH rline WHERE 
       rline.active-flag = 1  AND rline.resstatus NE 12 
       AND (SUBSTR(rline.zinr,1,INTEGER(rmlen))) GE room 
       AND rline.name GE lname AND rline.name LE to-name 
       AND rline.abreise EQ ci-date NO-LOCK, 
       FIRST whrg WHERE whrg.waehrungsnr = rline.betriebsnr 
       NO-LOCK, 
       FIRST reserv WHERE reserv.resnr = rline.resnr, 
       FIRST zk WHERE zk.zikatnr = rline.zikatnr, 
       FIRST gme WHERE gme.gastnr = rline.gastnrmember 
       NO-LOCK BY rline.zinr BY (rline.kontakt-nr * rline.resnr) 
       BY rline.resstatus BY rline.NAME:
            IF rline.resstatus NE 13 AND rline.resstatus NE 11 AND rline.l-zuordnung[3] NE 1 THEN
            temp-total2 = temp-total2 + rline.zimmeranz.
            temp-total = INT(temp-total) + INT(rline.erwachs).
       END.
       ASSIGN troom = string(temp-total2). 
       ASSIGN tpax = string(temp-total). 
      END. 
    END.
    ELSE IF room = "" THEN 
    DO: 
      IF lname = "" THEN
      DO:
       FOR EACH rline WHERE 
       rline.active-flag = 1  AND rline.resstatus NE 12 
       AND rline.abreise EQ ci-date NO-LOCK, 
       FIRST whrg WHERE whrg.waehrungsnr = rline.betriebsnr 
       NO-LOCK, 
       FIRST reserv WHERE reserv.resnr = rline.resnr, 
       FIRST zk WHERE zk.zikatnr = rline.zikatnr, 
       FIRST gme WHERE gme.gastnr = rline.gastnrmember 
       NO-LOCK BY rline.zinr BY (rline.kontakt-nr * rline.resnr) 
       BY rline.resstatus BY rline.NAME:
           IF rline.resstatus NE 13 AND rline.resstatus NE 11 AND rline.l-zuordnung[3] NE 1 THEN
            temp-total2 = temp-total2 + rline.zimmeranz.
           temp-total = INT(temp-total) + INT(rline.erwachs).
       END.
       ASSIGN troom = string(temp-total2). 
       ASSIGN tpax = string(temp-total). 
      END.
      ELSE IF lname NE "" AND SUBSTR(lname,1,1) EQ "*" THEN 
      DO:
       FOR EACH rline WHERE 
       rline.active-flag = 1  AND rline.resstatus NE 12 
       AND rline.name MATCHES(lname) AND rline.abreise EQ ci-date NO-LOCK, 
       FIRST whrg WHERE whrg.waehrungsnr = rline.betriebsnr 
       NO-LOCK, 
       FIRST reserv WHERE reserv.resnr = rline.resnr, 
       FIRST zk WHERE zk.zikatnr = rline.zikatnr, 
       FIRST gme WHERE gme.gastnr = rline.gastnrmember 
       NO-LOCK BY rline.name BY rline.zinr:
            IF rline.resstatus NE 13 AND rline.resstatus NE 11 AND rline.l-zuordnung[3] NE 1 THEN
            temp-total2 = temp-total2 + rline.zimmeranz.
           temp-total = INT(temp-total) + INT(rline.erwachs).
       END.
       ASSIGN troom = string(temp-total2). 
       ASSIGN tpax = string(temp-total). 
      END.
      ELSE IF lname NE "" AND SUBSTR(lname,1,1) NE "*" THEN 
      DO:
       FOR EACH rline WHERE 
       rline.active-flag = 1  AND rline.resstatus NE 12 
       AND rline.name GE lname AND rline.name LE to-name 
       AND rline.abreise EQ ci-date NO-LOCK, 
       FIRST whrg WHERE whrg.waehrungsnr = rline.betriebsnr 
       NO-LOCK, 
       FIRST reserv WHERE reserv.resnr = rline.resnr, 
       FIRST zk WHERE zk.zikatnr = rline.zikatnr, 
       FIRST gme WHERE gme.gastnr = rline.gastnrmember 
       NO-LOCK BY rline.name BY rline.zinr: 
            IF rline.resstatus NE 13 AND rline.resstatus NE 11 AND rline.l-zuordnung[3] NE 1 THEN
            temp-total2 = temp-total2 + rline.zimmeranz.
           temp-total = INT(temp-total) + INT(rline.erwachs).
       END.
       ASSIGN troom = string(temp-total2). 
       ASSIGN tpax = string(temp-total). 
      END.
    END. 
  END. 
  ELSE IF last-sort = 2 THEN 
  DO: 
    IF lname = "" THEN 
    DO: 
      IF room = "" THEN 
      DO:
        FOR EACH rline WHERE 
        rline.active-flag = 1 AND rline.resstatus NE 12 
        AND (SUBSTR(rline.zinr,1,INTEGER(rmlen))) GE room 
        AND rline.abreise EQ ci-date NO-LOCK, 
        FIRST whrg WHERE whrg.waehrungsnr = rline.betriebsnr 
        NO-LOCK, 
        FIRST reserv WHERE reserv.resnr = rline.resnr, 
        FIRST zk WHERE zk.zikatnr = rline.zikatnr, 
        FIRST gme WHERE gme.gastnr = rline.gastnrmember 
        NO-LOCK BY rline.resname BY rline.resnr BY rline.zinr
        BY (rline.kontakt-nr * rline.resnr) 
        BY rline.resstatus BY rline.NAME:
            IF rline.resstatus NE 13 AND rline.resstatus NE 11 AND rline.l-zuordnung[3] NE 1 THEN
            temp-total2 = temp-total2 + rline.zimmeranz.
            temp-total = INT(temp-total) + INT(rline.erwachs).
        END.
        ASSIGN troom = string(temp-total2). 
        ASSIGN tpax = string(temp-total). 
      END.
      ELSE IF room NE "" THEN 
      DO:
        FOR EACH rline WHERE 
        rline.active-flag = 1 AND rline.resstatus NE 12 
        AND (SUBSTR(rline.zinr,1,INTEGER(rmlen))) GE room 
        AND rline.abreise EQ ci-date NO-LOCK, 
        FIRST whrg WHERE whrg.waehrungsnr = rline.betriebsnr 
        NO-LOCK, 
        FIRST reserv WHERE reserv.resnr = rline.resnr, 
        FIRST zk WHERE zk.zikatnr = rline.zikatnr, 
        FIRST gme WHERE gme.gastnr = rline.gastnrmember 
        NO-LOCK BY rline.zinr BY (rline.kontakt-nr * rline.resnr) 
        BY rline.resstatus BY rline.NAME:
            IF rline.resstatus NE 13 AND rline.resstatus NE 11 AND rline.l-zuordnung[3] NE 1 THEN
            temp-total2 = temp-total2 + rline.zimmeranz.
            temp-total = INT(temp-total) + INT(rline.erwachs).
        END.
        ASSIGN troom = string(temp-total2). 
        ASSIGN tpax = string(temp-total). 
      END.
    END. 
    ELSE IF lname NE "" AND SUBSTR(lname,1,1) EQ "*" THEN 
    DO:
       FOR EACH rline WHERE 
       rline.active-flag = 1  AND rline.resstatus NE 12 
       AND (SUBSTR(rline.zinr,1,INTEGER(rmlen))) GE room 
       AND rline.resname MATCHES(lname) 
       AND rline.abreise EQ ci-date NO-LOCK, 
       FIRST whrg WHERE whrg.waehrungsnr = rline.betriebsnr 
       NO-LOCK, 
       FIRST reserv WHERE reserv.resnr = rline.resnr, 
       FIRST zk WHERE zk.zikatnr = rline.zikatnr, 
       FIRST gme WHERE gme.gastnr = rline.gastnrmember 
       NO-LOCK BY rline.resname BY rline.zinr
       BY (rline.kontakt-nr * rline.resnr) 
       BY rline.resstatus BY rline.NAME:
           IF rline.resstatus NE 13 AND rline.resstatus NE 11 AND rline.l-zuordnung[3] NE 1 THEN
            temp-total2 = temp-total2 + rline.zimmeranz.
            temp-total = INT(temp-total) + INT(rline.erwachs).
       END.
       ASSIGN troom = string(temp-total2). 
       ASSIGN tpax = string(temp-total). 
    END.
    ELSE IF lname NE "" AND SUBSTR(lname,1,1) NE "*" THEN 
    DO:  
       FOR EACH rline WHERE rline.active-flag = 1  AND rline.resstatus NE 12 
       AND (SUBSTR(rline.zinr,1,INTEGER(rmlen))) GE room 
       AND rline.resname GE lname AND rline.resname LE to-name 
       AND rline.abreise EQ ci-date NO-LOCK, 
       FIRST whrg WHERE whrg.waehrungsnr = rline.betriebsnr 
       NO-LOCK, 
       FIRST reserv WHERE reserv.resnr = rline.resnr, 
       FIRST zk WHERE zk.zikatnr = rline.zikatnr, 
       FIRST gme WHERE gme.gastnr = rline.gastnrmember 
       NO-LOCK BY rline.resname BY rline.zinr
       BY (rline.kontakt-nr * rline.resnr) 
       BY rline.resstatus BY rline.NAME:
          IF rline.resstatus NE 13 AND rline.resstatus NE 11 AND rline.l-zuordnung[3] NE 1 THEN
            temp-total2 = temp-total2 + rline.zimmeranz.
           temp-total = INT(temp-total) + INT(rline.erwachs).
       END.
       ASSIGN troom = string(temp-total2). 
       ASSIGN tpax = string(temp-total). 
    END.
  END. 
  ELSE IF last-sort = 3 AND lnat = "" THEN 
  DO: 
    IF lname = "" THEN 
    DO:
       FOR EACH rline WHERE 
       rline.active-flag = 1 AND rline.resstatus NE 12 
       AND rline.abreise EQ ci-date NO-LOCK, 
       FIRST whrg WHERE whrg.waehrungsnr = rline.betriebsnr 
       NO-LOCK, 
       FIRST reserv WHERE reserv.resnr = rline.resnr, 
       FIRST zk WHERE zk.zikatnr = rline.zikatnr, 
       FIRST gme WHERE gme.gastnr = rline.gastnrmember 
       NO-LOCK BY gme.nation1 BY (rline.kontakt-nr * rline.resnr) 
       BY rline.resstatus BY rline.NAME:
            IF rline.resstatus NE 13 AND rline.resstatus NE 11 AND rline.l-zuordnung[3] NE 1 THEN
            temp-total2 = temp-total2 + rline.zimmeranz.
           temp-total = INT(temp-total) + INT(rline.erwachs).
       END.
       ASSIGN troom = string(temp-total2). 
       ASSIGN tpax = string(temp-total). 
    END.
    ELSE IF lname NE "" AND SUBSTR(lname,1,1) EQ "*" THEN 
    DO:
       FOR EACH rline WHERE 
       rline.active-flag = 1  AND rline.resstatus NE 12 
       AND rline.name MATCHES(lname) 
       AND rline.abreise EQ ci-date NO-LOCK, 
       FIRST whrg WHERE whrg.waehrungsnr = rline.betriebsnr 
       NO-LOCK, 
       FIRST reserv WHERE reserv.resnr = rline.resnr, 
       FIRST zk WHERE zk.zikatnr = rline.zikatnr, 
       FIRST gme WHERE gme.gastnr = rline.gastnrmember 
       AND gme.nation1 = lnat 
       NO-LOCK BY gme.nation1 BY (rline.kontakt-nr * rline.resnr) 
       BY rline.resstatus BY rline.NAME:
            IF rline.resstatus NE 13 AND rline.resstatus NE 11 AND rline.l-zuordnung[3] NE 1 THEN
            temp-total2 = temp-total2 + rline.zimmeranz.
           temp-total = INT(temp-total) + INT(rline.erwachs).
       END.
       ASSIGN troom = string(temp-total2). 
       ASSIGN tpax = string(temp-total). 
    END.
    ELSE IF lname NE "" AND SUBSTR(lname,1,1) NE "*" THEN 
    DO:
       FOR EACH rline WHERE 
       rline.active-flag = 1  AND rline.resstatus NE 12 
       AND rline.name GE lname AND rline.name LE to-name 
       AND rline.abreise EQ ci-date NO-LOCK, 
       FIRST whrg WHERE whrg.waehrungsnr = rline.betriebsnr 
       NO-LOCK, 
       FIRST reserv WHERE reserv.resnr = rline.resnr, 
       FIRST zk WHERE zk.zikatnr = rline.zikatnr, 
       FIRST gme WHERE gme.gastnr = rline.gastnrmember 
       NO-LOCK BY gme.nation1 BY (rline.kontakt-nr * rline.resnr) 
       BY rline.resstatus BY rline.NAME:
           IF rline.resstatus NE 13 AND rline.resstatus NE 11 AND rline.l-zuordnung[3] NE 1 THEN
            temp-total2 = temp-total2 + rline.zimmeranz.
           temp-total = INT(temp-total) + INT(rline.erwachs).
       END.
       ASSIGN troom = string(temp-total2). 
       ASSIGN tpax = string(temp-total). 
    END.
  END. 
  ELSE IF last-sort = 3 AND lnat NE "" THEN 
  DO: 
    IF lname = "" THEN 
    DO:
       FOR EACH rline WHERE 
       rline.active-flag = 1 AND rline.resstatus NE 12 
       AND rline.abreise EQ ci-date NO-LOCK, 
       FIRST whrg WHERE whrg.waehrungsnr = rline.betriebsnr 
       NO-LOCK, 
       FIRST reserv WHERE reserv.resnr = rline.resnr, 
       FIRST zk WHERE zk.zikatnr = rline.zikatnr, 
       FIRST gme WHERE gme.gastnr = rline.gastnrmember 
       AND gme.nation1 = lnat 
       NO-LOCK BY gme.nation1 BY (rline.kontakt-nr * rline.resnr) 
       BY rline.resstatus BY rline.NAME:
           IF rline.resstatus NE 13 AND rline.resstatus NE 11 AND rline.l-zuordnung[3] NE 1 THEN
            temp-total2 = temp-total2 + rline.zimmeranz.
           temp-total = INT(temp-total) + INT(rline.erwachs).
       END.
       ASSIGN troom = string(temp-total2). 
       ASSIGN tpax = string(temp-total). 
    END.
    ELSE IF lname NE "" AND SUBSTR(lname,1,1) EQ "*" THEN 
    DO: 
       FOR EACH rline WHERE 
       rline.active-flag = 1  AND rline.resstatus NE 12 
       AND rline.name MATCHES(lname) AND rline.abreise EQ ci-date NO-LOCK, 
       FIRST whrg WHERE whrg.waehrungsnr = rline.betriebsnr 
       NO-LOCK, 
       FIRST reserv WHERE reserv.resnr = rline.resnr, 
       FIRST zk WHERE zk.zikatnr = rline.zikatnr, 
       FIRST gme WHERE gme.gastnr = rline.gastnrmember 
       AND gme.nation1 = lnat 
       NO-LOCK BY gme.nation1 BY (rline.kontakt-nr * rline.resnr) 
       BY rline.resstatus BY rline.NAME:
        IF rline.resstatus NE 13 AND rline.resstatus NE 11 AND rline.l-zuordnung[3] NE 1 THEN
            temp-total2 = temp-total2 + rline.zimmeranz.
         temp-total = INT(temp-total) + INT(rline.erwachs).
       END.
       ASSIGN troom = string(temp-total2). 
       ASSIGN tpax = string(temp-total). 
    END.
    ELSE IF lname NE "" AND SUBSTR(lname,1,1) NE "*" THEN 
    DO:
       FOR EACH rline WHERE 
       rline.active-flag = 1  AND rline.resstatus NE 12 
       AND rline.name GE lname AND rline.name LE to-name 
       AND rline.abreise EQ ci-date NO-LOCK, 
       FIRST whrg WHERE whrg.waehrungsnr = rline.betriebsnr 
       NO-LOCK, 
       FIRST reserv WHERE reserv.resnr = rline.resnr, 
       FIRST zk WHERE zk.zikatnr = rline.zikatnr, 
       FIRST gme WHERE gme.gastnr = rline.gastnrmember 
       AND gme.nation1 = lnat 
       NO-LOCK BY gme.nation1 BY (rline.kontakt-nr * rline.resnr) 
       BY rline.resstatus BY rline.NAME:
          IF rline.resstatus NE 13 AND rline.resstatus NE 11 AND rline.l-zuordnung[3] NE 1 THEN
            temp-total2 = temp-total2 + rline.zimmeranz.
           temp-total = INT(temp-total) + INT(rline.erwachs).
       END.
       ASSIGN troom = string(temp-total2). 
       ASSIGN tpax = string(temp-total). 
    END.
  END. 
  ELSE IF last-sort = 4 THEN 
  DO: 
    IF lresnr = 0 THEN 
    DO: 
      FOR EACH rline WHERE rline.active-flag = 1 
      AND rline.resstatus NE 12 AND rline.abreise = ci-date NO-LOCK, 
      FIRST whrg WHERE whrg.waehrungsnr = rline.betriebsnr 
      NO-LOCK, 
      FIRST reserv WHERE reserv.resnr = rline.resnr NO-LOCK, 
      FIRST zk WHERE zk.zikatnr = rline.zikatnr NO-LOCK, 
      FIRST gme WHERE gme.gastnr = rline.gastnrmember 
      NO-LOCK BY rline.resnr BY (rline.kontakt-nr * rline.resnr) 
      BY rline.resstatus BY rline.NAME:
          IF rline.resstatus NE 13 AND rline.resstatus NE 11 AND rline.l-zuordnung[3] NE 1 THEN
            temp-total2 = temp-total2 + rline.zimmeranz.
          temp-total = INT(temp-total) + INT(rline.erwachs).
      END.
      ASSIGN troom = string(temp-total2). 
      ASSIGN tpax = string(temp-total). 
    END.
    ELSE 
    DO:
      FOR EACH rline WHERE rline.active-flag = 1 
      AND rline.resstatus NE 12 AND rline.resnr = lresnr 
      AND rline.abreise = ci-date NO-LOCK, 
      FIRST whrg WHERE whrg.waehrungsnr = rline.betriebsnr 
      NO-LOCK, 
      FIRST reserv WHERE reserv.resnr = rline.resnr NO-LOCK, 
      FIRST zk WHERE zk.zikatnr = rline.zikatnr NO-LOCK, 
      FIRST gme WHERE gme.gastnr = rline.gastnrmember 
      NO-LOCK BY rline.NAME:
          IF rline.resstatus NE 13 AND rline.resstatus NE 11 AND rline.l-zuordnung[3] NE 1 THEN
            temp-total2 = temp-total2 + rline.zimmeranz.
          temp-total = INT(temp-total) + INT(rline.erwachs).
      END.
      ASSIGN troom = string(temp-total2). 
      ASSIGN tpax = string(temp-total). 
    END.
  END. 
END.
PROCEDURE count-all5:
                    
 DEFINE VARIABLE to-name AS CHAR. 
 DEFINE BUFFER rline FOR res-line.
 DEFINE BUFFER whrg FOR waehrung.
 DEFINE BUFFER reserv FOR reservation.
 DEFINE BUFFER gme FOR guest.
 DEFINE BUFFER zk FOR zimkateg.
 IF lname NE "" AND SUBSTR(lname,1,1) NE "*" THEN 
    to-name = chr(asc(SUBSTR(lname,1,1)) + 1). 
 IF last-sort = 1 AND room NE "" THEN 
 DO: 
    IF lname = "" THEN  
    DO:
      FOR EACH rline WHERE rline.resstatus EQ 8 
       AND rline.abreise EQ fdate2 
       AND rline.zinr GE room NO-LOCK, 
       FIRST whrg WHERE whrg.waehrungsnr = rline.betriebsnr 
       NO-LOCK, 
       FIRST reserv WHERE reserv.resnr = rline.resnr NO-LOCK, 
       FIRST zk WHERE zk.zikatnr = rline.zikatnr NO-LOCK, 
       FIRST gme WHERE gme.gastnr = rline.gastnrmember 
       NO-LOCK BY rline.zinr BY (rline.kontakt-nr * rline.resnr) 
       BY rline.resstatus BY rline.NAME:
        IF rline.resstatus NE 13 AND rline.resstatus NE 11 AND rline.l-zuordnung[3] NE 1 THEN
            temp-total2 = temp-total2 + rline.zimmeranz.
        temp-total = INT(temp-total) + INT(rline.erwachs).
      END.
      ASSIGN troom = string(temp-total2). 
      ASSIGN tpax = string(temp-total). 
    END.
    ELSE IF lname NE "" AND SUBSTR(lname,1,1) EQ "*" THEN 
    DO:
      FOR EACH rline WHERE rline.resstatus EQ 8 
       AND rline.name MATCHES(lname) AND rline.abreise EQ fdate2 
       AND rline.zinr GE room NO-LOCK, 
       FIRST whrg WHERE whrg.waehrungsnr = rline.betriebsnr 
       NO-LOCK, 
       FIRST reserv WHERE reserv.resnr = rline.resnr NO-LOCK, 
       FIRST zk WHERE zk.zikatnr = rline.zikatnr NO-LOCK, 
       FIRST gme WHERE gme.gastnr = rline.gastnrmember 
       NO-LOCK BY rline.zinr BY (rline.kontakt-nr * rline.resnr) 
       BY rline.resstatus BY rline.NAME:
          IF rline.resstatus NE 13 AND rline.resstatus NE 11 AND rline.l-zuordnung[3] NE 1 THEN
            temp-total2 = temp-total2 + rline.zimmeranz.
            temp-total = INT(temp-total) + INT(rline.erwachs).
       END.
       ASSIGN troom = string(temp-total2). 
       ASSIGN tpax = string(temp-total). 
    END.
    ELSE IF lname NE "" AND SUBSTR(lname,1,1) NE "*" THEN 
    DO:
       FOR EACH rline WHERE rline.resstatus EQ 8 
       AND rline.name GE lname AND rline.name LE to-name 
       AND rline.abreise EQ fdate2 AND rline.zinr GE room NO-LOCK, 
       FIRST whrg WHERE whrg.waehrungsnr = rline.betriebsnr 
       NO-LOCK, 
       FIRST reserv WHERE reserv.resnr = rline.resnr NO-LOCK, 
       FIRST zk WHERE zk.zikatnr = rline.zikatnr NO-LOCK, 
       FIRST gme WHERE gme.gastnr = rline.gastnrmember 
       NO-LOCK BY rline.NAME:
          IF rline.resstatus NE 13 AND rline.resstatus NE 11 AND rline.l-zuordnung[3] NE 1 THEN
            temp-total2 = temp-total2 + rline.zimmeranz.
             temp-total = INT(temp-total) + INT(rline.erwachs).
       END.
       ASSIGN troom = string(temp-total2). 
       ASSIGN tpax = string(temp-total). 
    END.  
 END.
 ELSE IF last-sort = 1 AND room = "" THEN 
 DO: 
    IF lname = "" THEN 
    DO:
       FOR EACH rline WHERE rline.resstatus EQ 8 
       AND rline.abreise EQ fdate2 NO-LOCK, 
       FIRST whrg WHERE whrg.waehrungsnr = rline.betriebsnr 
       NO-LOCK, 
       FIRST reserv WHERE reserv.resnr = rline.resnr NO-LOCK, 
       FIRST zk WHERE zk.zikatnr = rline.zikatnr NO-LOCK, 
       FIRST gme WHERE gme.gastnr = rline.gastnrmember 
       NO-LOCK BY (rline.kontakt-nr * rline.resnr) 
       BY rline.resstatus BY rline.NAME:
        IF rline.resstatus NE 13 AND rline.resstatus NE 11 AND rline.l-zuordnung[3] NE 1 THEN
            temp-total2 = temp-total2 + rline.zimmeranz.
         temp-total = INT(temp-total) + INT(rline.erwachs).      
       END.
     ASSIGN troom = string(temp-total2). 
     ASSIGN tpax = string(temp-total). 
    END. 
    ELSE IF lname NE "" AND SUBSTR(lname,1,1) EQ "*" THEN 
    DO:
       FOR EACH rline WHERE rline.resstatus EQ 8 
       AND rline.name MATCHES(lname) AND rline.abreise EQ fdate2 NO-LOCK, 
       FIRST whrg WHERE whrg.waehrungsnr = rline.betriebsnr 
       NO-LOCK, 
       FIRST reserv WHERE reserv.resnr = rline.resnr, 
       FIRST zk WHERE zk.zikatnr = rline.zikatnr, 
       FIRST gme WHERE gme.gastnr = rline.gastnrmember 
       NO-LOCK BY rline.NAME:
         IF rline.resstatus NE 13 AND rline.resstatus NE 11 AND rline.l-zuordnung[3] NE 1 THEN
            temp-total2 = temp-total2 + rline.zimmeranz.
         temp-total = INT(temp-total) + INT(rline.erwachs).
     END.
     ASSIGN troom = string(temp-total2). 
     ASSIGN tpax = string(temp-total). 
    END.
    ELSE IF lname NE "" AND SUBSTR(lname,1,1) NE "*" THEN 
    DO:
       FOR EACH rline WHERE rline.resstatus EQ 8 
       AND rline.name GE lname AND rline.name LE to-name 
       AND rline.abreise EQ fdate2 NO-LOCK, 
       FIRST whrg WHERE whrg.waehrungsnr = rline.betriebsnr 
       NO-LOCK, 
       FIRST reserv WHERE reserv.resnr = rline.resnr, 
       FIRST zk WHERE zk.zikatnr = rline.zikatnr, 
       FIRST gme WHERE gme.gastnr = rline.gastnrmember 
       NO-LOCK BY rline.NAME:
        IF rline.resstatus NE 13 AND rline.resstatus NE 11 AND rline.l-zuordnung[3] NE 1 THEN
            temp-total2 = temp-total2 + rline.zimmeranz.
         temp-total = INT(temp-total) + INT(rline.erwachs).
      END.
      ASSIGN troom = string(temp-total2). 
      ASSIGN tpax = string(temp-total). 
    END. 
 END.
 ELSE IF last-sort = 2 AND room NE "" THEN 
 DO: 
    IF lname = "" THEN 
    DO:
      FOR EACH rline WHERE rline.resstatus EQ 8 
       AND rline.abreise EQ fdate2 AND rline.zinr GE room NO-LOCK, 
       FIRST whrg WHERE whrg.waehrungsnr = rline.betriebsnr 
       NO-LOCK, 
       FIRST reserv WHERE reserv.resnr = rline.resnr NO-LOCK, 
       FIRST zk WHERE zk.zikatnr = rline.zikatnr NO-LOCK, 
       FIRST gme WHERE gme.gastnr = rline.gastnrmember 
       NO-LOCK BY rline.zinr 
       BY reserv.NAME /*rline.resname*/ BY rline.resnr BY (rline.kontakt-nr * rline.resnr) 
       BY rline.resstatus BY rline.NAME:
         IF rline.resstatus NE 13 AND rline.resstatus NE 11 AND rline.l-zuordnung[3] NE 1 THEN
            temp-total2 = temp-total2 + rline.zimmeranz.
         temp-total = INT(temp-total) + INT(rline.erwachs).
      END.
      /*RUN count-room.*/
      ASSIGN troom = string(temp-total2).
      ASSIGN tpax = string(temp-total). 
     END.
    ELSE IF lname NE "" AND SUBSTR(lname,1,1) EQ "*" THEN 
    DO:
     FOR EACH rline WHERE rline.resstatus EQ 8 
       AND rline.resname MATCHES(lname) AND rline.abreise EQ fdate2 
       AND rline.zinr GE room NO-LOCK, 
       FIRST whrg WHERE whrg.waehrungsnr = rline.betriebsnr 
       NO-LOCK, 
       FIRST reserv WHERE reserv.resnr = rline.resnr NO-LOCK, 
       FIRST zk WHERE zk.zikatnr = rline.zikatnr NO-LOCK, 
       FIRST gme WHERE gme.gastnr = rline.gastnrmember 
       NO-LOCK BY rline.zinr 
       BY rline.resname BY rline.resnr
       BY (rline.kontakt-nr * rline.resnr) 
       BY rline.resstatus BY rline.NAME:
         IF rline.resstatus NE 13 AND rline.resstatus NE 11 AND rline.l-zuordnung[3] NE 1 THEN
            temp-total2 = temp-total2 + rline.zimmeranz.
         temp-total = INT(temp-total) + INT(rline.erwachs).
     END.
     ASSIGN troom = string(temp-total2). 
     ASSIGN tpax = string(temp-total). 
    END.
    ELSE IF lname NE "" AND SUBSTR(lname,1,1) NE "*" THEN 
    DO: 
     FOR EACH rline WHERE rline.resstatus EQ 8 
       AND rline.resname GE lname AND 
       rline.resname  LE to-name 
       AND rline.abreise EQ fdate2 AND rline.zinr GE room NO-LOCK, 
       FIRST whrg WHERE whrg.waehrungsnr = rline.betriebsnr 
       NO-LOCK, 
       FIRST reserv WHERE reserv.resnr = rline.resnr NO-LOCK, 
       FIRST zk WHERE zk.zikatnr = rline.zikatnr NO-LOCK, 
       FIRST gme WHERE gme.gastnr = rline.gastnrmember 
       NO-LOCK BY rline.zinr 
       BY rline.resname BY rline.resnr
       BY (rline.kontakt-nr * rline.resnr) 
       BY rline.resstatus BY rline.NAME:
         IF rline.resstatus NE 13 AND rline.resstatus NE 11 AND rline.l-zuordnung[3] NE 1 THEN
            temp-total2 = temp-total2 + rline.zimmeranz.
         temp-total = INT(temp-total) + INT(rline.erwachs).
      END.
      ASSIGN troom = string(temp-total2). 
      ASSIGN tpax = string(temp-total). 
    END.
 END.    
 ELSE IF last-sort = 2 AND room = "" THEN 
  DO: 
    IF lname = "" THEN DO:
      FOR EACH rline WHERE rline.resstatus EQ 8 
       AND rline.abreise EQ fdate2 NO-LOCK, 
       FIRST whrg WHERE whrg.waehrungsnr = rline.betriebsnr 
       NO-LOCK, 
       FIRST reserv WHERE reserv.resnr = rline.resnr, 
       FIRST zk WHERE zk.zikatnr = rline.zikatnr, 
       FIRST gme WHERE gme.gastnr = rline.gastnrmember 
       NO-LOCK BY reserv.NAME /*rline.resname*/ BY rline.resnr
       BY (rline.kontakt-nr * rline.resnr) 
       BY rline.resstatus BY rline.NAME:
         IF rline.resstatus NE 13 AND rline.resstatus NE 11 AND rline.l-zuordnung[3] NE 1 THEN
            temp-total2 = temp-total2 + rline.zimmeranz.
             temp-total = INT(temp-total) + INT(rline.erwachs).
       END.
       ASSIGN troom = string(temp-total2).
       ASSIGN tpax = string(temp-total). 
    END.
    ELSE IF lname NE "" AND SUBSTR(lname,1,1) EQ "*" THEN 
    DO:
      FOR EACH rline WHERE rline.resstatus EQ 8 
       AND rline.resname MATCHES(lname) AND rline.abreise EQ fdate2 NO-LOCK, 
       FIRST whrg WHERE whrg.waehrungsnr = rline.betriebsnr 
       NO-LOCK, 
       FIRST reserv WHERE reserv.resnr = rline.resnr, 
       FIRST zk WHERE zk.zikatnr = rline.zikatnr, 
       FIRST gme WHERE gme.gastnr = rline.gastnrmember 
       NO-LOCK BY rline.resname BY rline.resnr
       BY (rline.kontakt-nr * rline.resnr) 
       BY rline.resstatus BY rline.NAME:
          IF rline.resstatus NE 13 AND rline.resstatus NE 11 AND rline.l-zuordnung[3] NE 1 THEN
            temp-total2 = temp-total2 + rline.zimmeranz.
         temp-total = INT(temp-total) + INT(rline.erwachs).
       END.
       ASSIGN troom = string(temp-total2). 
       ASSIGN tpax = string(temp-total). 
    END.
    ELSE IF lname NE "" AND SUBSTR(lname,1,1) NE "*" THEN 
    DO:
     FOR EACH rline WHERE rline.resstatus EQ 8 
       AND rline.abreise EQ fdate2 NO-LOCK, 
       FIRST whrg WHERE whrg.waehrungsnr = rline.betriebsnr 
       NO-LOCK, 
       FIRST reserv WHERE reserv.resnr = rline.resnr 
       AND reserv.NAME GE lname AND reserv.NAME LE to-name , 
       FIRST zk WHERE zk.zikatnr = rline.zikatnr, 
       FIRST gme WHERE gme.gastnr = rline.gastnrmember 
       NO-LOCK BY rline.resname BY rline.resnr
       BY (rline.kontakt-nr * rline.resnr) 
       BY rline.resstatus BY rline.NAME:
         IF rline.resstatus NE 13 AND rline.resstatus NE 11 AND rline.l-zuordnung[3] NE 1 THEN
            temp-total2 = temp-total2 + rline.zimmeranz.
         temp-total = INT(temp-total) + INT(rline.erwachs).
      END.
      ASSIGN troom = string(temp-total2). 
      ASSIGN tpax = string(temp-total). 
    END.
  END. 
  ELSE IF last-sort = 3 AND lnat = "" THEN 
  DO: 
    IF lname = "" THEN
    DO:
    FOR EACH rline WHERE rline.resstatus EQ 8 
       AND rline.abreise EQ fdate2 NO-LOCK, 
       FIRST whrg WHERE whrg.waehrungsnr = rline.betriebsnr 
       NO-LOCK, 
       FIRST reserv WHERE reserv.resnr = rline.resnr, 
       FIRST zk WHERE zk.zikatnr = rline.zikatnr, 
       FIRST gme WHERE gme.gastnr = rline.gastnrmember 
       NO-LOCK BY gme.nation1
       BY (rline.kontakt-nr * rline.resnr) 
       BY rline.resstatus BY rline.NAME:
        IF rline.resstatus NE 13 AND rline.resstatus NE 11 AND rline.l-zuordnung[3] NE 1 THEN
            temp-total2 = temp-total2 + rline.zimmeranz.
         temp-total = INT(temp-total) + INT(rline.erwachs).
     END.
     ASSIGN troom = string(temp-total2). 
     ASSIGN tpax = string(temp-total). 
    END.
    ELSE IF lname NE "" AND SUBSTR(lname,1,1) EQ "*" THEN 
    DO: 
     FOR EACH rline WHERE rline.resstatus EQ 8 
       AND rline.resname MATCHES(lname) AND rline.abreise EQ fdate2 
       NO-LOCK, 
       FIRST whrg WHERE whrg.waehrungsnr = rline.betriebsnr 
       NO-LOCK, 
       FIRST reserv WHERE reserv.resnr = rline.resnr, 
       FIRST zk WHERE zk.zikatnr = rline.zikatnr, 
       FIRST gme WHERE gme.gastnr = rline.gastnrmember 
       NO-LOCK BY gme.nation1
       BY (rline.kontakt-nr * rline.resnr) 
       BY rline.resstatus BY rline.NAME:
         IF rline.resstatus NE 13 AND rline.resstatus NE 11 AND rline.l-zuordnung[3] NE 1 THEN
            temp-total2 = temp-total2 + rline.zimmeranz.
         temp-total = INT(temp-total) + INT(rline.erwachs).
       END.
       ASSIGN troom = string(temp-total2). 
       ASSIGN tpax = string(temp-total). 
    END.
    ELSE IF lname NE "" AND SUBSTR(lname,1,1) NE "*" THEN 
    DO: 
      FOR EACH rline WHERE rline.resstatus EQ 8    
       AND rline.resname GE lname AND rline.resname LE to-name 
       AND rline.abreise EQ fdate2 NO-LOCK, 
       FIRST whrg WHERE whrg.waehrungsnr = rline.betriebsnr 
       NO-LOCK, 
       FIRST reserv WHERE reserv.resnr = rline.resnr, 
       FIRST zk WHERE zk.zikatnr = rline.zikatnr, 
       FIRST gme WHERE gme.gastnr = rline.gastnrmember 
       NO-LOCK BY gme.nation1
       BY (rline.kontakt-nr * rline.resnr) 
       BY rline.resstatus BY rline.NAME:
          IF rline.resstatus NE 13 AND rline.resstatus NE 11 AND rline.l-zuordnung[3] NE 1 THEN
            temp-total2 = temp-total2 + rline.zimmeranz.
         temp-total = INT(temp-total) + INT(rline.erwachs).
       END.
       ASSIGN troom = string(temp-total2). 
       ASSIGN tpax = string(temp-total). 
    END.
 END. 
  ELSE IF last-sort = 3 AND lnat NE "" THEN 
  DO: 
    IF lname = "" THEN 
    DO:
     FOR EACH rline WHERE rline.resstatus EQ 8 
       AND rline.abreise EQ fdate2 NO-LOCK, 
       FIRST whrg WHERE whrg.waehrungsnr = rline.betriebsnr 
       NO-LOCK, 
       FIRST reserv WHERE reserv.resnr = rline.resnr, 
       FIRST zk WHERE zk.zikatnr = rline.zikatnr, 
       FIRST gme WHERE gme.gastnr = rline.gastnrmember 
       AND gme.nation1 = lnat 
       NO-LOCK BY gme.nation1
       BY (rline.kontakt-nr * rline.resnr) 
       BY rline.resstatus BY rline.NAME:
         IF rline.resstatus NE 13 AND rline.resstatus NE 11 AND rline.l-zuordnung[3] NE 1 THEN
            temp-total2 = temp-total2 + rline.zimmeranz.
         temp-total = INT(temp-total) + INT(rline.erwachs).
     END.
     ASSIGN troom = string(temp-total2). 
     ASSIGN tpax = string(temp-total). 
    END.
    ELSE IF lname NE "" AND SUBSTR(lname,1,1) EQ "*" THEN 
    DO:
     FOR EACH rline WHERE rline.resstatus EQ 8 
       AND rline.resname MATCHES(lname) AND rline.abreise EQ fdate2 
       NO-LOCK, 
       FIRST whrg WHERE whrg.waehrungsnr = rline.betriebsnr 
       NO-LOCK, 
       FIRST reserv WHERE reserv.resnr = rline.resnr, 
       FIRST zk WHERE zk.zikatnr = rline.zikatnr, 
       FIRST gme WHERE gme.gastnr = rline.gastnrmember 
       AND gme.nation1 = lnat 
       NO-LOCK BY gme.nation1
       BY (rline.kontakt-nr * rline.resnr) 
       BY rline.resstatus BY rline.NAME:
         IF rline.resstatus NE 13 AND rline.resstatus NE 11 AND rline.l-zuordnung[3] NE 1 THEN
            temp-total2 = temp-total2 + rline.zimmeranz.
         temp-total = INT(temp-total) + INT(rline.erwachs).
       END.
       ASSIGN troom = string(temp-total2). 
       ASSIGN tpax = string(temp-total). 
    END.
    ELSE IF lname NE "" AND SUBSTR(lname,1,1) NE "*" THEN 
    DO:
      FOR EACH rline WHERE rline.resstatus EQ 8 
       AND rline.resname GE lname AND rline.resname LE to-name 
       AND rline.abreise EQ fdate2 NO-LOCK, 
       FIRST whrg WHERE whrg.waehrungsnr = rline.betriebsnr 
       NO-LOCK, 
       FIRST reserv WHERE reserv.resnr = rline.resnr, 
       FIRST zk WHERE zk.zikatnr = rline.zikatnr, 
       FIRST gme WHERE gme.gastnr = rline.gastnrmember 
       AND gme.nation1 = lnat 
       NO-LOCK BY gme.nation1
       BY (rline.kontakt-nr * rline.resnr) 
       BY rline.resstatus BY rline.NAME:
        IF rline.resstatus NE 13 AND rline.resstatus NE 11 AND rline.l-zuordnung[3] NE 1 THEN
            temp-total2 = temp-total2 + rline.zimmeranz.
         temp-total = INT(temp-total) + INT(rline.erwachs).
       END.
       ASSIGN troom = string(temp-total2). 
       ASSIGN tpax = string(temp-total). 
    END.
  END. 
  ELSE IF last-sort = 4 THEN 
  DO: 
    IF lresnr = 0 THEN 
    DO:
    FOR EACH rline WHERE rline.active-flag = 2 
      AND rline.resstatus EQ 8 
      AND rline.abreise EQ fdate2 NO-LOCK, 
      FIRST whrg WHERE whrg.waehrungsnr = rline.betriebsnr 
      NO-LOCK, 
      FIRST reserv WHERE reserv.resnr = rline.resnr NO-LOCK, 
      FIRST zk WHERE zk.zikatnr = rline.zikatnr NO-LOCK, 
      FIRST gme WHERE gme.gastnr = rline.gastnrmember 
      NO-LOCK BY rline.resnr
      BY (rline.kontakt-nr * rline.resnr) 
      BY rline.resstatus BY rline.NAME:
        IF rline.resstatus NE 13 AND rline.resstatus NE 11 AND rline.l-zuordnung[3] NE 1 THEN
            temp-total2 = temp-total2 + rline.zimmeranz.
         temp-total = INT(temp-total) + INT(rline.erwachs).
      END.
      ASSIGN troom = string(temp-total2). 
      ASSIGN tpax = string(temp-total). 
    END.
    ELSE
    DO:
    FOR EACH rline WHERE rline.active-flag = 2 
      AND rline.resstatus EQ 8 AND rline.resnr = lresnr NO-LOCK, 
      FIRST whrg WHERE whrg.waehrungsnr = rline.betriebsnr 
      NO-LOCK, 
      FIRST reserv WHERE reserv.resnr = rline.resnr NO-LOCK, 
      FIRST zk WHERE zk.zikatnr = rline.zikatnr NO-LOCK, 
      FIRST gme WHERE gme.gastnr = rline.gastnrmember 
      NO-LOCK BY (rline.kontakt-nr * rline.resnr) 
      BY rline.resstatus BY rline.NAME:
        IF rline.resstatus NE 13 AND rline.resstatus NE 11 AND rline.l-zuordnung[3] NE 1 THEN
            temp-total2 = temp-total2 + rline.zimmeranz.
         temp-total = INT(temp-total) + INT(rline.erwachs).
     END.
     ASSIGN troom = string(temp-total2). 
     ASSIGN tpax = string(temp-total). 
    END.
  END. 
END. 
PROCEDURE count-all6: 
 DEFINE VARIABLE to-name AS CHAR. 
 DEFINE BUFFER rline FOR res-line.
 DEFINE BUFFER whrg FOR waehrung.
 DEFINE BUFFER reserv FOR reserv.
 DEFINE BUFFER gme FOR guest.
 DEFINE BUFFER zk FOR zk.
  IF lname NE "" AND SUBSTR(lname,1,1) NE "*" THEN 
    to-name = chr(asc(SUBSTR(lname,1,1)) + 1). 
 
  IF last-sort = 1 THEN 
  DO: 
    IF room NE "" THEN 
    DO: 
      IF lname = "" THEN 
      DO:
       FOR EACH rline WHERE 
       (rline.active-flag = 1  AND rline.resstatus NE 12 
       AND (SUBSTR(rline.zinr,1,INTEGER(rmlen))) GE room 
       AND rline.ankunft LE ci-date AND rline.abreise GE ci-date) OR 
       (rline.active-flag = 0 
       AND (SUBSTR(rline.zinr,1,INTEGER(rmlen))) GE room 
       AND rline.ankunft EQ ci-date) OR 
       (rline.active-flag = 2 AND rline.resstatus = 8 
       AND (SUBSTR(rline.zinr,1,INTEGER(rmlen))) GE room 
       AND rline.abreise EQ ci-date) NO-LOCK, 
       FIRST whrg WHERE whrg.waehrungsnr = rline.betriebsnr 
       NO-LOCK, 
       FIRST reserv WHERE reserv.resnr = rline.resnr, 
       FIRST zk WHERE zk.zikatnr = rline.zikatnr, 
       FIRST gme WHERE gme.gastnr = rline.gastnrmember 
       NO-LOCK BY rline.zinr BY (rline.kontakt-nr * rline.resnr) 
       BY rline.resstatus BY rline.NAME:
           IF rline.resstatus NE 13 AND rline.resstatus NE 11 AND rline.l-zuordnung[3] NE 1 THEN
            temp-total2 = temp-total2 + rline.zimmeranz.
           temp-total = INT(temp-total) + INT(rline.erwachs).
       END.
       ASSIGN troom = string(temp-total2). 
       ASSIGN tpax = string(temp-total). 
      END.
      ELSE IF lname NE "" AND SUBSTR(lname,1,1) EQ "*" THEN 
      DO:
       FOR EACH rline WHERE 
       (rline.active-flag = 1  AND rline.resstatus NE 12 
       AND (SUBSTR(rline.zinr,1,INTEGER(rmlen))) GE room 
       AND rline.name MATCHES(lname) 
       AND rline.ankunft LE ci-date AND rline.abreise GE ci-date) OR 
       (rline.active-flag = 0 
       AND (SUBSTR(rline.zinr,1,INTEGER(rmlen))) GE room 
       AND rline.name MATCHES(lname) 
       AND rline.ankunft EQ ci-date) OR 
       (rline.active-flag = 2  AND rline.resstatus EQ 8 
       AND (SUBSTR(rline.zinr,1,INTEGER(rmlen))) GE room 
       AND rline.name MATCHES(lname) 
       AND rline.abreise EQ ci-date) NO-LOCK, 
       FIRST whrg WHERE whrg.waehrungsnr = rline.betriebsnr 
       NO-LOCK, 
       FIRST reserv WHERE reserv.resnr = rline.resnr, 
       FIRST zk WHERE zk.zikatnr = rline.zikatnr, 
       FIRST gme WHERE gme.gastnr = rline.gastnrmember 
       NO-LOCK BY rline.zinr BY (rline.kontakt-nr * rline.resnr) 
       BY rline.resstatus BY rline.NAME:
           IF rline.resstatus NE 13 AND rline.resstatus NE 11 AND rline.l-zuordnung[3] NE 1 THEN
            temp-total2 = temp-total2 + rline.zimmeranz.
           temp-total = INT(temp-total) + INT(rline.erwachs).
       END.
       ASSIGN troom = string(temp-total2). 
       ASSIGN tpax = string(temp-total). 
      END.
      ELSE IF lname NE "" AND SUBSTR(lname,1,1) NE "*" THEN 
      DO:
       FOR EACH rline WHERE 
       (rline.active-flag = 1  AND rline.resstatus NE 12 
       AND (SUBSTR(rline.zinr,1,INTEGER(rmlen))) GE room 
       AND rline.name GE lname AND rline.name LE to-name 
       AND rline.ankunft LE ci-date AND rline.abreise GE ci-date) OR 
       (rline.active-flag = 0 
       AND (SUBSTR(rline.zinr,1,INTEGER(rmlen))) GE room 
       AND rline.name GE lname AND rline.name LE to-name 
       AND rline.ankunft EQ ci-date) OR 
       (rline.active-flag = 2  AND rline.resstatus = 8 
       AND (SUBSTR(rline.zinr,1,INTEGER(rmlen))) GE room 
       AND rline.name GE lname AND rline.name LE to-name 
       AND rline.abreise EQ ci-date) NO-LOCK, 
       FIRST whrg WHERE whrg.waehrungsnr = rline.betriebsnr 
       NO-LOCK, 
       FIRST reserv WHERE reserv.resnr = rline.resnr, 
       FIRST zk WHERE zk.zikatnr = rline.zikatnr, 
       FIRST gme WHERE gme.gastnr = rline.gastnrmember 
       NO-LOCK BY rline.zinr BY (rline.kontakt-nr * rline.resnr) 
       BY rline.resstatus BY rline.NAME:
           IF rline.resstatus NE 13 AND rline.resstatus NE 11 AND rline.l-zuordnung[3] NE 1 THEN
            temp-total2 = temp-total2 + rline.zimmeranz.
           temp-total = INT(temp-total) + INT(rline.erwachs).
       END.
       ASSIGN troom = string(temp-total2). 
       ASSIGN tpax = string(temp-total). 
      END.
    END. 
    ELSE IF room = "" THEN 
    DO: 
      IF lname = "" THEN 
      DO:
       FOR EACH rline WHERE 
       (rline.active-flag = 1  AND rline.resstatus NE 12 
       AND rline.ankunft LE ci-date AND rline.abreise GE ci-date) OR 
       (rline.active-flag = 0 AND rline.ankunft EQ ci-date) OR 
       (rline.active-flag = 2 AND rline.resstatus EQ 8 
       AND rline.abreise EQ ci-date) NO-LOCK, 
       FIRST whrg WHERE whrg.waehrungsnr = rline.betriebsnr 
       NO-LOCK, 
       FIRST reserv WHERE reserv.resnr = rline.resnr, 
       FIRST zk WHERE zk.zikatnr = rline.zikatnr, 
       FIRST gme WHERE gme.gastnr = rline.gastnrmember 
       NO-LOCK BY (rline.kontakt-nr * rline.resnr) 
       BY rline.resstatus BY rline.NAME:
           IF rline.resstatus NE 13 AND rline.resstatus NE 11 AND rline.l-zuordnung[3] NE 1 THEN
            temp-total2 = temp-total2 + rline.zimmeranz.
           temp-total = INT(temp-total) + INT(rline.erwachs).
       END.
       ASSIGN troom = string(temp-total2). 
       ASSIGN tpax = string(temp-total). 
      END.
      ELSE IF lname NE "" AND SUBSTR(lname,1,1) EQ "*" THEN 
      DO:
       FOR EACH rline WHERE 
       (rline.active-flag = 1  AND rline.resstatus NE 12 
       AND rline.name MATCHES(lname) 
       AND rline.ankunft LE ci-date AND rline.abreise GE ci-date) OR 
       (rline.active-flag = 0 AND rline.name MATCHES(lname) 
       AND rline.ankunft EQ ci-date) OR 
       (rline.active-flag = 2 AND rline.resstatus EQ 8 
       AND rline.name MATCHES(lname) 
       AND rline.abreise EQ ci-date) NO-LOCK, 
       FIRST whrg WHERE whrg.waehrungsnr = rline.betriebsnr 
       NO-LOCK, 
       FIRST reserv WHERE reserv.resnr = rline.resnr, 
       FIRST zk WHERE zk.zikatnr = rline.zikatnr, 
       FIRST gme WHERE gme.gastnr = rline.gastnrmember 
       NO-LOCK BY rline.NAME:
           IF rline.resstatus NE 13 AND rline.resstatus NE 11 AND rline.l-zuordnung[3] NE 1 THEN
            temp-total2 = temp-total2 + rline.zimmeranz.
           temp-total = INT(temp-total) + INT(rline.erwachs).
       END.
       ASSIGN troom = string(temp-total2). 
       ASSIGN tpax = string(temp-total). 
      END.
      ELSE IF lname NE "" AND SUBSTR(lname,1,1) NE "*" THEN 
      DO:
        FOR EACH rline WHERE 
       (rline.active-flag = 1  AND rline.resstatus NE 12 
       AND rline.name GE lname AND rline.name LE to-name 
       AND rline.ankunft LE ci-date AND rline.abreise GE ci-date) OR 
       (rline.active-flag = 0 
       AND rline.name GE lname AND rline.name LE to-name 
       AND rline.ankunft EQ ci-date) OR 
       (rline.active-flag = 2  AND rline.resstatus EQ 8 
       AND rline.name GE lname AND rline.name LE to-name 
       AND rline.abreise EQ ci-date) NO-LOCK, 
       FIRST whrg WHERE whrg.waehrungsnr = rline.betriebsnr 
       NO-LOCK, 
       FIRST reserv WHERE reserv.resnr = rline.resnr, 
       FIRST zk WHERE zk.zikatnr = rline.zikatnr, 
       FIRST gme WHERE gme.gastnr = rline.gastnrmember 
       NO-LOCK BY rline.NAME:
            IF rline.resstatus NE 13 AND rline.resstatus NE 11 AND rline.l-zuordnung[3] NE 1 THEN
            temp-total2 = temp-total2 + rline.zimmeranz.
            temp-total = INT(temp-total) + INT(rline.erwachs).
       END.
       ASSIGN troom = string(temp-total2). 
       ASSIGN tpax = string(temp-total). 
      END.
    END. 
  END. 
  ELSE IF last-sort = 2 THEN 
  DO: 
    IF lname = "" AND room = "" THEN 
    DO:
        FOR EACH rline WHERE 
       (rline.active-flag = 1 AND rline.resstatus NE 12 
       AND (SUBSTR(rline.zinr,1,INTEGER(rmlen))) GE room 
       AND rline.ankunft LE ci-date AND rline.abreise GE ci-date) OR 
       (rline.active-flag = 0 
       AND (SUBSTR(rline.zinr,1,INTEGER(rmlen))) GE room 
       AND rline.ankunft EQ ci-date) OR 
       (rline.active-flag = 2 AND rline.resstatus EQ 8 
       AND (SUBSTR(rline.zinr,1,INTEGER(rmlen))) GE room 
       AND rline.abreise EQ ci-date) NO-LOCK, 
       FIRST whrg WHERE whrg.waehrungsnr = rline.betriebsnr 
       NO-LOCK, 
       FIRST reserv WHERE reserv.resnr = rline.resnr, 
       FIRST zk WHERE zk.zikatnr = rline.zikatnr, 
       FIRST gme WHERE gme.gastnr = rline.gastnrmember 
       NO-LOCK BY rline.resname BY rline.resnr BY rline.zinr
       BY (rline.kontakt-nr * rline.resnr) 
       BY rline.resstatus BY rline.NAME:
            IF rline.resstatus NE 13 AND rline.resstatus NE 11 AND rline.l-zuordnung[3] NE 1 THEN
            temp-total2 = temp-total2 + rline.zimmeranz.
            temp-total = INT(temp-total) + INT(rline.erwachs).
       END.
       ASSIGN troom = string(temp-total2). 
       ASSIGN tpax = string(temp-total). 
    END.
    ELSE IF lname = "" AND room NE "" THEN 
    DO:
       FOR EACH rline WHERE 
       (rline.active-flag = 1 AND rline.resstatus NE 12 
       AND (SUBSTR(rline.zinr,1,INTEGER(rmlen))) GE room 
       AND rline.ankunft LE ci-date AND rline.abreise GE ci-date) OR 
       (rline.active-flag = 0 
       AND (SUBSTR(rline.zinr,1,INTEGER(rmlen))) GE room 
       AND rline.ankunft EQ ci-date) OR 
       (rline.active-flag = 2 AND rline.resstatus EQ 8 
       AND (SUBSTR(rline.zinr,1,INTEGER(rmlen))) GE room 
       AND rline.abreise EQ ci-date) NO-LOCK, 
       FIRST whrg WHERE whrg.waehrungsnr = rline.betriebsnr 
       NO-LOCK, 
       FIRST reserv WHERE reserv.resnr = rline.resnr, 
       FIRST zk WHERE zk.zikatnr = rline.zikatnr, 
       FIRST gme WHERE gme.gastnr = rline.gastnrmember 
       NO-LOCK BY rline.zinr
       BY (rline.kontakt-nr * rline.resnr) 
       BY rline.resstatus BY rline.NAME:
           IF rline.resstatus NE 13 AND rline.resstatus NE 11 AND rline.l-zuordnung[3] NE 1 THEN
            temp-total2 = temp-total2 + rline.zimmeranz.
           temp-total = INT(temp-total) + INT(rline.erwachs).
       END.
       ASSIGN troom = string(temp-total2). 
       ASSIGN tpax = string(temp-total). 
    END.
    ELSE IF lname NE "" AND SUBSTR(lname,1,1) EQ "*" THEN 
    DO:
       FOR EACH rline WHERE 
       (rline.active-flag = 1  AND rline.resstatus NE 12 
       AND (SUBSTR(rline.zinr,1,INTEGER(rmlen))) GE room 
       AND rline.resname MATCHES(lname) 
       AND rline.ankunft LE ci-date AND rline.abreise GE ci-date) OR 
       (rline.active-flag = 0 
       AND (SUBSTR(rline.zinr,1,INTEGER(rmlen))) GE room 
       AND rline.resname MATCHES(lname) 
       AND rline.ankunft EQ ci-date) OR 
       (rline.active-flag = 2  AND rline.resstatus EQ 8 
       AND (SUBSTR(rline.zinr,1,INTEGER(rmlen))) GE room 
       AND rline.resname MATCHES(lname) 
       AND rline.abreise EQ ci-date) NO-LOCK, 
       FIRST whrg WHERE whrg.waehrungsnr = rline.betriebsnr 
       NO-LOCK, 
       FIRST reserv WHERE reserv.resnr = rline.resnr, 
       FIRST zk WHERE zk.zikatnr = rline.zikatnr, 
       FIRST gme WHERE gme.gastnr = rline.gastnrmember 
       NO-LOCK BY rline.resname BY rline.zinr
       BY (rline.kontakt-nr * rline.resnr) 
       BY rline.resstatus BY rline.NAME:
           IF rline.resstatus NE 13 AND rline.resstatus NE 11 AND rline.l-zuordnung[3] NE 1 THEN
            temp-total2 = temp-total2 + rline.zimmeranz.
           temp-total = INT(temp-total) + INT(rline.erwachs).
       END.
       ASSIGN troom = string(temp-total2). 
       ASSIGN tpax = string(temp-total). 
    END.
    ELSE IF lname NE "" AND SUBSTR(lname,1,1) NE "*" THEN 
    DO:
       FOR EACH rline WHERE 
       (rline.active-flag = 1  AND rline.resstatus NE 12 
       AND (SUBSTR(rline.zinr,1,INTEGER(rmlen))) GE room 
       AND rline.resname GE lname AND rline.resname LE to-name 
       AND rline.ankunft LE ci-date AND rline.abreise GE ci-date) OR 
       (rline.active-flag = 0 
       AND (SUBSTR(rline.zinr,1,INTEGER(rmlen))) GE room 
       AND rline.resname GE lname AND rline.resname LE to-name 
       AND rline.ankunft EQ ci-date) OR 
       (rline.active-flag = 2  AND rline.resstatus EQ 8 
       AND (SUBSTR(rline.zinr,1,INTEGER(rmlen))) GE room 
       AND rline.resname GE lname AND rline.resname LE to-name 
       AND rline.abreise EQ ci-date) NO-LOCK, 
       FIRST whrg WHERE whrg.waehrungsnr = rline.betriebsnr 
       NO-LOCK, 
       FIRST reserv WHERE reserv.resnr = rline.resnr, 
       FIRST zk WHERE zk.zikatnr = rline.zikatnr, 
       FIRST gme WHERE gme.gastnr = rline.gastnrmember 
       NO-LOCK BY rline.resname BY rline.zinr
       BY (rline.kontakt-nr * rline.resnr) 
       BY rline.resstatus BY rline.NAME:
           IF rline.resstatus NE 13 AND rline.resstatus NE 11 AND rline.l-zuordnung[3] NE 1 THEN
            temp-total2 = temp-total2 + rline.zimmeranz.
           temp-total = INT(temp-total) + INT(rline.erwachs).
       END.
       ASSIGN troom = string(temp-total2). 
       ASSIGN tpax = string(temp-total). 
    END.
  END. 
  ELSE IF last-sort = 3 AND lnat = "" THEN 
  DO: 
    IF lname = "" THEN 
    DO:
       FOR EACH rline WHERE 
       (rline.active-flag = 1 AND rline.resstatus NE 12 
       AND rline.ankunft LE ci-date AND rline.abreise GE ci-date) OR 
       (rline.active-flag = 0 
       AND rline.ankunft EQ ci-date) OR 
       (rline.active-flag = 2 AND rline.resstatus EQ 8 
       AND rline.abreise EQ ci-date) NO-LOCK, 
       FIRST whrg WHERE whrg.waehrungsnr = rline.betriebsnr 
       NO-LOCK, 
       FIRST reserv WHERE reserv.resnr = rline.resnr, 
       FIRST zk WHERE zk.zikatnr = rline.zikatnr, 
       FIRST gme WHERE gme.gastnr = rline.gastnrmember 
       NO-LOCK BY gme.nation1
       BY (rline.kontakt-nr * rline.resnr) 
       BY rline.resstatus BY rline.NAME:
           IF rline.resstatus NE 13 AND rline.resstatus NE 11 AND rline.l-zuordnung[3] NE 1  THEN
            temp-total2 = temp-total2 + rline.zimmeranz.
           temp-total = INT(temp-total) + INT(rline.erwachs).
       END.
       ASSIGN troom = string(temp-total2). 
       ASSIGN tpax = string(temp-total). 
    END.
    ELSE IF lname NE "" AND SUBSTR(lname,1,1) EQ "*" THEN 
    DO:
       FOR EACH rline WHERE 
       (rline.active-flag = 1  AND rline.resstatus NE 12 
       AND rline.resname MATCHES(lname) 
       AND rline.ankunft LE ci-date AND rline.abreise GE ci-date) OR 
       (rline.active-flag = 0 
       AND rline.resname MATCHES(lname) 
       AND rline.ankunft EQ ci-date) OR 
       (rline.active-flag = 2  AND rline.resstatus EQ 8 
       AND rline.resname MATCHES(lname) 
       AND rline.abreise EQ ci-date) NO-LOCK, 
       FIRST whrg WHERE whrg.waehrungsnr = rline.betriebsnr 
       NO-LOCK, 
       FIRST reserv WHERE reserv.resnr = rline.resnr, 
       FIRST zk WHERE zk.zikatnr = rline.zikatnr, 
       FIRST gme WHERE gme.gastnr = rline.gastnrmember 
       NO-LOCK BY gme.nation1
       BY (rline.kontakt-nr * rline.resnr) 
       BY rline.resstatus BY rline.NAME:
           IF rline.resstatus NE 13 AND rline.resstatus NE 11 AND rline.l-zuordnung[3] NE 1  THEN
            temp-total2 = temp-total2 + rline.zimmeranz.
           temp-total = INT(temp-total) + INT(rline.erwachs).
       END.
       ASSIGN troom = string(temp-total2). 
       ASSIGN tpax = string(temp-total). 
    END.
    ELSE IF lname NE "" AND SUBSTR(lname,1,1) NE "*" THEN 
    DO:
       FOR EACH rline WHERE 
       (rline.active-flag = 1  AND rline.resstatus NE 12 
       AND rline.resname GE lname AND rline.resname LE to-name 
       AND rline.ankunft LE ci-date AND rline.abreise GE ci-date) OR 
       (rline.active-flag = 0 
       AND rline.resname GE lname AND rline.resname LE to-name 
       AND rline.ankunft EQ ci-date) OR 
       (rline.active-flag = 2  AND rline.resstatus EQ 8 
       AND rline.resname GE lname AND rline.resname LE to-name 
       AND rline.abreise EQ ci-date) NO-LOCK, 
       FIRST whrg WHERE whrg.waehrungsnr = rline.betriebsnr 
       NO-LOCK, 
       FIRST reserv WHERE reserv.resnr = rline.resnr, 
       FIRST zk WHERE zk.zikatnr = rline.zikatnr, 
       FIRST gme WHERE gme.gastnr = rline.gastnrmember 
       NO-LOCK BY gme.nation1
       BY (rline.kontakt-nr * rline.resnr) 
       BY rline.resstatus BY rline.NAME:
           IF rline.resstatus NE 13 AND rline.resstatus NE 11 AND rline.l-zuordnung[3] NE 1  THEN
            temp-total2 = temp-total2 + rline.zimmeranz.
           temp-total = INT(temp-total) + INT(rline.erwachs).
       END.
       ASSIGN troom = string(temp-total2). 
       ASSIGN tpax = string(temp-total). 
    END.
  END. 
  ELSE IF last-sort = 3 AND lnat NE "" THEN 
  DO: 
    IF lname = "" THEN 
    DO:
        FOR EACH rline WHERE 
       (rline.active-flag = 1 AND rline.resstatus NE 12 
       AND rline.ankunft LE ci-date AND rline.abreise GE ci-date) OR 
       (rline.active-flag = 0 AND rline.ankunft EQ ci-date) OR 
       (rline.active-flag = 2 AND rline.resstatus EQ 8 
       AND rline.abreise EQ ci-date) NO-LOCK, 
       FIRST whrg WHERE whrg.waehrungsnr = rline.betriebsnr 
       NO-LOCK, 
       FIRST reserv WHERE reserv.resnr = rline.resnr, 
       FIRST zk WHERE zk.zikatnr = rline.zikatnr, 
       FIRST gme WHERE gme.gastnr = rline.gastnrmember 
       AND gme.nation1 = lnat 
       NO-LOCK BY gme.nation1
       BY (rline.kontakt-nr * rline.resnr) 
       BY rline.resstatus BY rline.NAME:
            IF rline.resstatus NE 13 AND rline.resstatus NE 11 AND rline.l-zuordnung[3] NE 1  THEN
            temp-total2 = temp-total2 + rline.zimmeranz.
            temp-total = INT(temp-total) + INT(rline.erwachs).
       END.
       ASSIGN troom = string(temp-total2). 
       ASSIGN tpax = string(temp-total). 
    END.
    ELSE IF lname NE "" AND SUBSTR(lname,1,1) EQ "*" THEN 
    DO:
       FOR EACH rline WHERE 
       (rline.active-flag = 1  AND rline.resstatus NE 12 
       AND rline.resname MATCHES(lname) 
       AND rline.ankunft LE ci-date AND rline.abreise GE ci-date) OR 
       (rline.active-flag = 0 
       AND rline.resname MATCHES(lname) 
       AND rline.ankunft EQ ci-date) OR 
       (rline.active-flag = 2  AND rline.resstatus EQ 8 
       AND rline.resname MATCHES(lname) 
       AND rline.abreise EQ ci-date) NO-LOCK, 
       FIRST whrg WHERE whrg.waehrungsnr = rline.betriebsnr 
       NO-LOCK, 
       FIRST reserv WHERE reserv.resnr = rline.resnr, 
       FIRST zk WHERE zk.zikatnr = rline.zikatnr, 
       FIRST gme WHERE gme.gastnr = rline.gastnrmember 
       AND gme.nation1 = lnat 
       NO-LOCK BY gme.nation1
       BY (rline.kontakt-nr * rline.resnr) 
       BY rline.resstatus BY rline.NAME:
          IF rline.resstatus NE 13 AND rline.resstatus NE 11 AND rline.l-zuordnung[3] NE 1  THEN
            temp-total2 = temp-total2 + rline.zimmeranz.
           temp-total = INT(temp-total) + INT(rline.erwachs).
       END.
       ASSIGN troom = string(temp-total2). 
       ASSIGN tpax = string(temp-total). 
    END.
    ELSE IF lname NE "" AND SUBSTR(lname,1,1) NE "*" THEN 
    DO:
       FOR EACH rline WHERE 
       (rline.active-flag = 1  AND rline.resstatus NE 12 
       AND rline.resname GE lname AND rline.resname LE to-name 
       AND rline.ankunft LE ci-date AND rline.abreise GE ci-date) OR 
       (rline.active-flag = 0 
       AND rline.resname GE lname AND rline.resname LE to-name 
       AND rline.ankunft EQ ci-date) OR 
       (rline.active-flag = 2 AND rline.resstatus EQ 8 
       AND rline.resname GE lname AND rline.resname LE to-name 
       AND rline.abreise EQ ci-date) NO-LOCK, 
       FIRST whrg WHERE whrg.waehrungsnr = rline.betriebsnr 
       NO-LOCK, 
       FIRST reserv WHERE reserv.resnr = rline.resnr, 
       FIRST zk WHERE zk.zikatnr = rline.zikatnr, 
       FIRST gme WHERE gme.gastnr = rline.gastnrmember 
       AND gme.nation1 = lnat 
       NO-LOCK BY gme.nation1
       BY (rline.kontakt-nr * rline.resnr) 
       BY rline.resstatus BY rline.NAME:
           IF rline.resstatus NE 13 AND rline.resstatus NE 11 AND rline.l-zuordnung[3] NE 1  THEN
            temp-total2 = temp-total2 + rline.zimmeranz.
           temp-total = INT(temp-total) + INT(rline.erwachs).
       END.
       ASSIGN troom = string(temp-total2). 
       ASSIGN tpax = string(temp-total). 
    END.
  END. 
  ELSE IF last-sort = 4 THEN 
  DO: 
    IF lresnr = 0 THEN 
    DO:
      FOR EACH rline WHERE 
      (rline.active-flag = 1 AND rline.resstatus NE 12) OR 
      (rline.active-flag = 0 
      AND rline.ankunft EQ ci-date) OR 
      (rline.active-flag = 2 AND rline.resstatus EQ 8 
      AND rline.abreise EQ ci-date) NO-LOCK, 
      FIRST whrg WHERE whrg.waehrungsnr = rline.betriebsnr 
      NO-LOCK, 
      FIRST reserv WHERE reserv.resnr = rline.resnr NO-LOCK, 
      FIRST zk WHERE zk.zikatnr = rline.zikatnr NO-LOCK, 
      FIRST gme WHERE gme.gastnr = rline.gastnrmember 
      NO-LOCK BY rline.resnr BY (rline.kontakt-nr * rline.resnr) 
      BY rline.resstatus BY rline.NAME:
       IF rline.resstatus NE 13 AND rline.resstatus NE 11 AND rline.l-zuordnung[3] NE 1  THEN
            temp-total2 = temp-total2 + rline.zimmeranz.
          temp-total = INT(temp-total) + INT(rline.erwachs).
      END.
      ASSIGN troom = string(temp-total2). 
      ASSIGN tpax = string(temp-total). 
    END.
    ELSE 
    DO:
      FOR EACH rline WHERE 
      (rline.active-flag = 1 
      AND rline.resstatus NE 12 AND rline.resnr = lresnr) OR 
      (rline.active-flag = 0 AND rline.resnr = lresnr 
      AND rline.ankunft EQ ci-date) OR 
      (rline.active-flag = 2 AND rline.resstatus EQ 8 AND rline.resnr = lresnr 
      AND rline.abreise EQ ci-date) NO-LOCK, 
      FIRST whrg WHERE whrg.waehrungsnr = rline.betriebsnr 
      NO-LOCK, 
      FIRST reserv WHERE reserv.resnr = rline.resnr NO-LOCK, 
      FIRST zk WHERE zk.zikatnr = rline.zikatnr NO-LOCK, 
      FIRST gme WHERE gme.gastnr = rline.gastnrmember 
      NO-LOCK BY (rline.kontakt-nr * rline.resnr) 
      BY rline.resstatus BY rline.NAME:
          IF rline.resstatus NE 13 AND rline.resstatus NE 11 
              AND rline.l-zuordnung[3] NE 1 THEN
            temp-total2 = temp-total2 + rline.zimmeranz.
          temp-total = INT(temp-total) + INT(rline.erwachs).
      END.
      ASSIGN troom = string(temp-total2). 
      ASSIGN tpax = string(temp-total). 
    END.
  END. 
END.


PROCEDURE assign-it:
    FIND FIRST guest WHERE guest.gastnr = reservation.gastnr NO-LOCK. 
    CREATE telop-list.
    ASSIGN
        telop-list.resli-wabkurz    = res-line.wabkurz
        telop-list.voucher-nr       = res-line.voucher-nr
        telop-list.grpflag          = reservation.grpflag
        telop-list.reser-name       = reservation.name
        telop-list.zinr             = res-line.zinr 
        telop-list.resli-name       = res-line.name
        telop-list.segmentcode      = reservation.segmentcode 
        telop-list.nation1          = gmember.nation1
        telop-list.resstatus        = res-line.resstatus 
        telop-list.l-zuordnung      = res-line.l-zuordnung[3]
        telop-list.ankunft          = res-line.ankunft 
        telop-list.abreise          = res-line.abreise 
        telop-list.ankzeit          = res-line.ankzeit
        telop-list.abreisezeit      = res-line.abreisezeit
        telop-list.flight-nr        = res-line.flight-nr
        telop-list.flight1          = SUBSTR(res-line.flight-nr,1,6)
        telop-list.eta              = STRING(SUBSTR(res-line.flight-nr,7,5), "99:99")
        telop-list.flight2          = SUBSTR(res-line.flight-nr,12,6)
        telop-list.etd              = STRING(SUBSTR(res-line.flight-nr,18,5), "99:99")
        telop-list.zimmeranz        = res-line.zimmeranz 
        telop-list.kurzbez          = zimkateg.kurzbez 
        telop-list.erwachs          = res-line.erwachs
        telop-list.kind1            = res-line.kind1
        telop-list.gratis           = res-line.gratis
        telop-list.waeh-wabkurz     = waehrung.wabkurz
        telop-list.resnr            = res-line.resnr
        telop-list.reslinnr         = res-line.reslinnr
        telop-list.betrieb-gast     = res-line.betrieb-gast
        telop-list.groupname        = reservation.groupname 
        telop-list.cancelled-id     = res-line.cancelled-id 
        telop-list.changed-id       = res-line.changed-id 
        telop-list.bemerk           = res-line.bemerk
        telop-list.active-flag      = res-line.active-flag
        telop-list.gastnrmember     = res-line.gastnrmember
        telop-list.gastnr           = res-line.gastnr
        telop-list.betrieb-gastmem  = res-line.betrieb-gastmem
        telop-list.pseudofix        = res-line.pseudofix
        telop-list.zikatnr          = res-line.zikatnr
        telop-list.arrangement      = res-line.arrangement
        telop-list.zipreis          = res-line.zipreis
        telop-list.resname          = reservation.NAME
        telop-list.address          = guest.adresse1
        telop-list.city             = guest.wohnort + " " + guest.plz
        telop-list.b-comments       = reservation.bemerk
  .

  FIND FIRST reslin-queasy WHERE reslin-queasy.key = "flag" 
      AND reslin-queasy.resnr = res-line.resnr 
      AND reslin-queasy.reslinnr = res-line.reslinnr 
      AND reslin-queasy.betriebsnr = 0 NO-LOCK NO-ERROR. 
  IF AVAILABLE reslin-queasy THEN
  DO:
    IF (reslin-queasy.char1 NE "" AND reslin-queasy.deci1 = 0) 
        OR (reslin-queasy.char2 NE "" AND reslin-queasy.deci2 = 0) 
        OR (reslin-queasy.char3 NE "" AND reslin-queasy.deci3 = 0) THEN
      ASSIGN telop-list.flag-color = 1.
    ELSE ASSIGN telop-list.flag-color = 9.
  END.

  FIND FIRST messages WHERE messages.resnr = res-line.resnr 
    AND messages.reslinnr = res-line.reslinnr NO-LOCK NO-ERROR.
  telop-list.message-flag = AVAILABLE messages.

END.
