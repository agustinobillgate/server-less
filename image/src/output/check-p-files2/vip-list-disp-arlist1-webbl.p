
DEF TEMP-TABLE t-vip-list
    FIELD resnr         LIKE res-line.resnr
    FIELD zinr          LIKE res-line.zinr
    FIELD name          LIKE res-line.name
    FIELD ankunft       LIKE res-line.ankunft
    FIELD anztage       LIKE res-line.anztage
    FIELD abreise       LIKE res-line.abreise
    FIELD zimmeranz     LIKE res-line.zimmeranz
    FIELD kurzbez       LIKE zimkateg.kurzbez
    FIELD erwachs       LIKE res-line.erwachs
    FIELD gratis        LIKE res-line.gratis
    FIELD resstatus     LIKE res-line.resstatus
    FIELD arrangement   LIKE res-line.arrangement
    FIELD zipreis       LIKE res-line.zipreis
    FIELD ankzeit       LIKE res-line.ankzeit
    FIELD abreisezeit   LIKE res-line.abreisezeit
    FIELD bezeich       LIKE segment.bezeich
    FIELD karteityp     LIKE guest.karteityp
    FIELD gastnr        LIKE guest.gastnr
    FIELD resname       AS CHAR
    FIELD address       AS CHAR
    FIELD city          AS CHAR
    FIELD comments      AS CHAR.

DEF INPUT PARAMETER show-rate AS LOGICAL.
DEF INPUT PARAMETER sorttype AS INT.
DEF INPUT PARAMETER fdate AS DATE.
DEF INPUT PARAMETER lname AS CHAR.
DEF INPUT PARAMETER room AS CHAR.
DEF INPUT PARAMETER ci-date AS DATE.
DEF INPUT PARAMETER tdate   AS DATE.
DEF INPUT PARAMETER by-period AS LOGICAL.
DEF OUTPUT PARAMETER TABLE FOR t-vip-list.

DEFINE VARIABLE vip-nr  AS INTEGER EXTENT 10.

RUN fill-vipnr.
RUN disp-arlist.

PROCEDURE disp-arlist:
  IF show-rate THEN RUN disp-arlist1. 
  ELSE RUN disp-arlist2. 
END. 


PROCEDURE fill-vipnr: 
  FIND FIRST htparam WHERE paramnr = 700 NO-LOCK. 
  vip-nr[1] = htparam.finteger. 
  FIND FIRST htparam WHERE paramnr = 701 NO-LOCK. 
  vip-nr[2] = htparam.finteger. 
  FIND FIRST htparam WHERE paramnr =  702 NO-LOCK. 
  vip-nr[3] = htparam.finteger. 
  FIND FIRST htparam WHERE paramnr = 703 NO-LOCK. 
  vip-nr[4] = htparam.finteger. 
  FIND FIRST htparam WHERE paramnr = 704 NO-LOCK. 
  vip-nr[5] = htparam.finteger. 
  FIND FIRST htparam WHERE paramnr = 705 NO-LOCK. 
  vip-nr[6] = htparam.finteger. 
  FIND FIRST htparam WHERE paramnr = 706 NO-LOCK. 
  vip-nr[7] = htparam.finteger. 
  FIND FIRST htparam WHERE paramnr = 707 NO-LOCK. 
  vip-nr[8] = htparam.finteger. 
  FIND FIRST htparam WHERE paramnr = 708 NO-LOCK. 
  vip-nr[9] = htparam.finteger. 
  FIND FIRST htparam WHERE paramnr = 712 NO-LOCK. 
  vip-nr[10] = htparam.finteger. 
END. 

PROCEDURE disp-arlist1: 
  /*MTENABLE b1 btn-print btn-stop btn-gcf  WITH FRAME f-reserve.*/
  IF sorttype = 1 THEN  /* Reservation  */ 
  DO: 
    /*MTENABLE lname fdate btn-start sorttype WITH FRAME f-reserve. 
    room = "". 
    DISP room WITH FRAME f-reserve. 
    DISABLE room WITH FRAME f-reserve.*/
    IF fdate = ? THEN 
    FOR EACH res-line WHERE 
       (resstatus LE 5 OR resstatus = 11) 
       AND res-line.name GE lname NO-LOCK,
       /*AND res-line.NAME MATCHES ("*" + lname + "*") NO-LOCK,*/
       FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr NO-LOCK, 
       EACH guestseg WHERE guestseg.gastnr = res-line.gastnrmember AND 
         (guestseg.segmentcode = vip-nr[1] OR 
          guestseg.segmentcode = vip-nr[2] OR 
          guestseg.segmentcode = vip-nr[3] OR 
          guestseg.segmentcode = vip-nr[4] OR 
          guestseg.segmentcode = vip-nr[5] OR 
          guestseg.segmentcode = vip-nr[6] OR 
          guestseg.segmentcode = vip-nr[7] OR 
          guestseg.segmentcode = vip-nr[8] OR 
          guestseg.segmentcode = vip-nr[9] OR 
          guestseg.segmentcode = vip-nr[10]) NO-LOCK, 
       FIRST segment WHERE segment.segmentcode = guestseg.segmentcode 
       NO-LOCK BY res-line.name:
        RUN assign-it.
    END.
    ELSE
    DO:
        IF by-period THEN
        DO:
            FOR EACH res-line WHERE 
               (resstatus LE 5 OR resstatus = 11) 
               AND res-line.name GE lname
               AND res-line.zinr GE room
               /*AND res-line.NAME MATCHES ("*" + lname + "*")*/
               AND res-line.ankunft GE fdate
               AND res-line.ankunft LE tdate NO-LOCK, 
               FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr NO-LOCK, 
               EACH guestseg WHERE guestseg.gastnr = res-line.gastnrmember AND 
                 (guestseg.segmentcode = vip-nr[1] OR 
                  guestseg.segmentcode = vip-nr[2] OR 
                  guestseg.segmentcode = vip-nr[3] OR 
                  guestseg.segmentcode = vip-nr[4] OR 
                  guestseg.segmentcode = vip-nr[5] OR 
                  guestseg.segmentcode = vip-nr[6] OR 
                  guestseg.segmentcode = vip-nr[7] OR 
                  guestseg.segmentcode = vip-nr[8] OR 
                  guestseg.segmentcode = vip-nr[9] OR 
                  guestseg.segmentcode = vip-nr[10]) NO-LOCK, 
                  FIRST segment WHERE segment.segmentcode = guestseg.segmentcode 
                  NO-LOCK BY res-line.name:
                RUN assign-it.
            END.
        END.
        ELSE
        DO:
            FOR EACH res-line WHERE 
               (resstatus LE 5 OR resstatus = 11) 
               AND res-line.name GE lname
               AND res-line.zinr GE room
               /*AND res-line.NAME MATCHES ("*" + lname + "*")*/
               AND res-line.ankunft EQ fdate NO-LOCK, 
               FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr NO-LOCK, 
               EACH guestseg WHERE guestseg.gastnr = res-line.gastnrmember AND 
                 (guestseg.segmentcode = vip-nr[1] OR 
                  guestseg.segmentcode = vip-nr[2] OR 
                  guestseg.segmentcode = vip-nr[3] OR 
                  guestseg.segmentcode = vip-nr[4] OR 
                  guestseg.segmentcode = vip-nr[5] OR 
                  guestseg.segmentcode = vip-nr[6] OR 
                  guestseg.segmentcode = vip-nr[7] OR 
                  guestseg.segmentcode = vip-nr[8] OR 
                  guestseg.segmentcode = vip-nr[9] OR 
                  guestseg.segmentcode = vip-nr[10]) NO-LOCK, 
                  FIRST segment WHERE segment.segmentcode = guestseg.segmentcode 
                  NO-LOCK BY res-line.name:
                RUN assign-it.
            END.
        END.
    END.            
  END. 
  ELSE IF sorttype = 2 THEN   /* In-house Guests */ 
  DO: 
    /*MTENABLE  lname room btn-start sorttype WITH FRAME f-reserve. 
    DISP fdate WITH FRAME f-reserve. 
    DISABLE fdate WITH FRAME f-reserve.*/
    IF lname EQ "" AND room NE "" THEN 
    FOR EACH res-line WHERE (resstatus = 6 OR resstatus = 13) 
        AND res-line.name GE lname 
        /*AND res-line.NAME MATCHES ("*" + lname + "*")*/
        AND res-line.zinr GE room NO-LOCK, 
        FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr NO-LOCK, 
        EACH guestseg WHERE guestseg.gastnr = res-line.gastnrmember AND 
        (guestseg.segmentcode = vip-nr[1] OR 
         guestseg.segmentcode = vip-nr[2] OR 
         guestseg.segmentcode = vip-nr[3] OR 
         guestseg.segmentcode = vip-nr[4] OR 
         guestseg.segmentcode = vip-nr[5] OR 
         guestseg.segmentcode = vip-nr[6] OR 
         guestseg.segmentcode = vip-nr[7] OR 
         guestseg.segmentcode = vip-nr[8] OR 
         guestseg.segmentcode = vip-nr[9] OR 
         guestseg.segmentcode = vip-nr[10]) NO-LOCK, 
         FIRST segment WHERE segment.segmentcode = guestseg.segmentcode 
         NO-LOCK BY res-line.zinr:
        RUN assign-it.
    END.
    ELSE 
    FOR EACH res-line WHERE (resstatus = 6 OR resstatus = 13) 
        /*AND res-line.name GE lname*/
        AND res-line.NAME MATCHES ("*" + lname + "*")
        AND res-line.zinr GE room NO-LOCK, 
        FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr NO-LOCK, 
        EACH guestseg WHERE guestseg.gastnr = res-line.gastnrmember AND 
        (guestseg.segmentcode = vip-nr[1] OR 
         guestseg.segmentcode = vip-nr[2] OR 
         guestseg.segmentcode = vip-nr[3] OR 
         guestseg.segmentcode = vip-nr[4] OR 
         guestseg.segmentcode = vip-nr[5] OR 
         guestseg.segmentcode = vip-nr[6] OR 
         guestseg.segmentcode = vip-nr[7] OR 
         guestseg.segmentcode = vip-nr[8] OR 
         guestseg.segmentcode = vip-nr[9] OR 
         guestseg.segmentcode = vip-nr[10]) NO-LOCK, 
         FIRST segment WHERE segment.segmentcode = guestseg.segmentcode 
         NO-LOCK BY res-line.name:
        RUN assign-it.
    END.
  END. 
  ELSE IF sorttype = 3 THEN   /* Arrival Today */ 
  DO: 
    /*MTENABLE lname btn-start sorttype WITH FRAME f-reserve. 
    room = "". 
    DISP room fdate WITH FRAME f-reserve. 
    DISABLE room fdate WITH FRAME f-reserve.*/
    FOR EACH res-line WHERE 
       (resstatus LE 5 OR resstatus = 11) 
        AND res-line.name GE lname
        AND res-line.zinr GE room
        /*AND res-line.NAME MATCHES ("*" + lname + "*")*/
        AND res-line.ankunft = ci-date NO-LOCK, 
        FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr NO-LOCK, 
        EACH guestseg WHERE guestseg.gastnr = res-line.gastnrmember AND 
        (guestseg.segmentcode = vip-nr[1] OR 
         guestseg.segmentcode = vip-nr[2] OR 
         guestseg.segmentcode = vip-nr[3] OR 
         guestseg.segmentcode = vip-nr[4] OR 
         guestseg.segmentcode = vip-nr[5] OR 
         guestseg.segmentcode = vip-nr[6] OR 
         guestseg.segmentcode = vip-nr[7] OR 
         guestseg.segmentcode = vip-nr[8] OR 
         guestseg.segmentcode = vip-nr[9] OR 
         guestseg.segmentcode = vip-nr[10]) NO-LOCK, 
        FIRST segment WHERE segment.segmentcode = guestseg.segmentcode 
        NO-LOCK BY res-line.name:
        RUN assign-it.
    END.
  END. 
  ELSE IF sorttype = 4 THEN   /* Departure Today */ 
  DO: 
    /*MTENABLE lname btn-start sorttype WITH FRAME f-reserve. 
    room = "". 
    DISP room fdate WITH FRAME f-reserve. 
    DISABLE room fdate WITH FRAME f-reserve.*/
    FOR EACH res-line WHERE 
        (resstatus = 6 OR resstatus = 13) 
        AND res-line.name GE lname
        AND res-line.zinr GE room
        /*AND res-line.NAME MATCHES ("*" + lname + "*")*/
        AND res-line.abreise =  ci-date NO-LOCK, 
        FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr NO-LOCK, 
        EACH guestseg WHERE guestseg.gastnr = res-line.gastnrmember AND 
         (guestseg.segmentcode = vip-nr[1] OR 
          guestseg.segmentcode = vip-nr[2] OR 
          guestseg.segmentcode = vip-nr[3] OR 
          guestseg.segmentcode = vip-nr[4] OR 
          guestseg.segmentcode = vip-nr[5] OR 
          guestseg.segmentcode = vip-nr[6] OR 
          guestseg.segmentcode = vip-nr[7] OR 
          guestseg.segmentcode = vip-nr[8] OR 
          guestseg.segmentcode = vip-nr[9] OR 
          guestseg.segmentcode = vip-nr[10]) NO-LOCK, 
          FIRST segment WHERE segment.segmentcode = guestseg.segmentcode 
          NO-LOCK BY res-line.name:
        RUN assign-it.
    END.
  END. 
  ELSE IF sorttype = 5 THEN   /* All */ 
  DO: 
    /*MTENABLE lname fdate btn-start sorttype WITH FRAME f-reserve. 
    room = "". 
    DISP room WITH FRAME f-reserve. 
    DISABLE WITH FRAME f-reserve.*/
    IF fdate NE ? THEN 
    DO:
        IF by-period THEN
        DO:
            FOR EACH res-line WHERE 
                 ((active-flag = 0 AND res-line.ankunft GE fdate AND res-line.ankunft LE tdate
                 AND res-line.name GE lname AND res-line.zinr GE room /*AND res-line.NAME MATCHES ("*" + lname + "*")*/) OR 
                 (active-flag = 1 AND res-line.abreise GE fdate /*AND res-line.abreise LE tdate*/
                 AND res-line.name GE lname AND res-line.zinr GE room /*AND res-line.NAME MATCHES ("*" + lname + "*")*/))
                 AND resstatus NE 12 NO-LOCK, 
                 FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr NO-LOCK, 
                 EACH guestseg WHERE guestseg.gastnr = res-line.gastnrmember AND 
                 (guestseg.segmentcode = vip-nr[1] OR 
                  guestseg.segmentcode = vip-nr[2] OR 
                  guestseg.segmentcode = vip-nr[3] OR 
                  guestseg.segmentcode = vip-nr[4] OR 
                  guestseg.segmentcode = vip-nr[5] OR 
                  guestseg.segmentcode = vip-nr[6] OR 
                  guestseg.segmentcode = vip-nr[7] OR 
                  guestseg.segmentcode = vip-nr[8] OR 
                  guestseg.segmentcode = vip-nr[9] OR 
                  guestseg.segmentcode = vip-nr[10]) NO-LOCK, 
                  FIRST segment WHERE segment.segmentcode = guestseg.segmentcode 
                  NO-LOCK BY res-line.name:
                RUN assign-it.
            END.
        END. 
        ELSE
        DO:
            FOR EACH res-line WHERE 
                 ((active-flag = 0 AND res-line.ankunft GE fdate 
                 AND res-line.name GE lname AND res-line.zinr GE room /*AND res-line.NAME MATCHES ("*" + lname + "*")*/) OR 
                 (active-flag = 1 AND res-line.abreise GE fdate 
                 AND res-line.name GE lname AND res-line.zinr GE room /*AND res-line.NAME MATCHES ("*" + lname + "*")*/)) 
                 AND resstatus NE 12 NO-LOCK, 
                 FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr NO-LOCK, 
                 EACH guestseg WHERE guestseg.gastnr = res-line.gastnrmember AND 
                 (guestseg.segmentcode = vip-nr[1] OR 
                  guestseg.segmentcode = vip-nr[2] OR 
                  guestseg.segmentcode = vip-nr[3] OR 
                  guestseg.segmentcode = vip-nr[4] OR 
                  guestseg.segmentcode = vip-nr[5] OR 
                  guestseg.segmentcode = vip-nr[6] OR 
                  guestseg.segmentcode = vip-nr[7] OR 
                  guestseg.segmentcode = vip-nr[8] OR 
                  guestseg.segmentcode = vip-nr[9] OR 
                  guestseg.segmentcode = vip-nr[10]) NO-LOCK, 
                  FIRST segment WHERE segment.segmentcode = guestseg.segmentcode 
                  NO-LOCK BY res-line.name:
                RUN assign-it.
            END.
        END.
    END.
    ELSE 
    DO:
      FOR EACH res-line WHERE 
          resstatus NE 9 AND resstatus NE 10
          AND resstatus NE 12 AND res-line.name GE lname
          /*AND res-line.NAME MATCHES ("*" + lname + "*")*/ NO-LOCK, 
          FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr NO-LOCK, 
          EACH guestseg WHERE guestseg.gastnr = res-line.gastnrmember AND 
           (guestseg.segmentcode = vip-nr[1] OR 
            guestseg.segmentcode = vip-nr[2] OR 
            guestseg.segmentcode = vip-nr[3] OR 
            guestseg.segmentcode = vip-nr[4] OR 
            guestseg.segmentcode = vip-nr[5] OR 
            guestseg.segmentcode = vip-nr[6] OR 
            guestseg.segmentcode = vip-nr[7] OR 
            guestseg.segmentcode = vip-nr[8] OR 
            guestseg.segmentcode = vip-nr[9] OR 
            guestseg.segmentcode = vip-nr[10]) NO-LOCK, 
            FIRST segment WHERE segment.segmentcode = guestseg.segmentcode 
            NO-LOCK BY res-line.name:
          RUN assign-it.
      END.
    END.
  END. 
  ELSE IF sorttype EQ 6 THEN /*Arrival Date*/
  DO:
      IF by-period THEN
      DO:
          FOR EACH res-line WHERE 
               ((active-flag = 0 AND res-line.ankunft GE fdate AND res-line.ankunft LE tdate
               AND res-line.NAME MATCHES ("*" + lname + "*") AND res-line.zinr GE room /*AND res-line.NAME MATCHES ("*" + lname + "*")*/) OR 
               (active-flag = 1 AND res-line.abreise GE fdate /*AND res-line.abreise LE tdate*/
               AND res-line.NAME MATCHES ("*" + lname + "*") AND res-line.zinr GE room /*AND res-line.NAME MATCHES ("*" + lname + "*")*/))
               AND resstatus NE 12 NO-LOCK, 
               FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr NO-LOCK, 
               EACH guestseg WHERE guestseg.gastnr = res-line.gastnrmember AND 
               (guestseg.segmentcode = vip-nr[1] OR 
                guestseg.segmentcode = vip-nr[2] OR 
                guestseg.segmentcode = vip-nr[3] OR 
                guestseg.segmentcode = vip-nr[4] OR 
                guestseg.segmentcode = vip-nr[5] OR 
                guestseg.segmentcode = vip-nr[6] OR 
                guestseg.segmentcode = vip-nr[7] OR 
                guestseg.segmentcode = vip-nr[8] OR 
                guestseg.segmentcode = vip-nr[9] OR 
                guestseg.segmentcode = vip-nr[10]) NO-LOCK, 
                FIRST segment WHERE segment.segmentcode = guestseg.segmentcode 
                NO-LOCK BY res-line.ankunft:
              RUN assign-it.
          END.
      END. 
      ELSE
      DO:
          FOR EACH res-line WHERE 
               ((active-flag = 0 AND res-line.ankunft GE fdate 
               AND res-line.NAME MATCHES ("*" + lname + "*") AND res-line.zinr GE room /*AND res-line.NAME MATCHES ("*" + lname + "*")*/) OR 
               (active-flag = 1 AND res-line.abreise GE fdate 
               AND res-line.NAME MATCHES ("*" + lname + "*") AND res-line.zinr GE room /*AND res-line.NAME MATCHES ("*" + lname + "*")*/)) 
               AND resstatus NE 12 NO-LOCK, 
               FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr NO-LOCK, 
               EACH guestseg WHERE guestseg.gastnr = res-line.gastnrmember AND 
               (guestseg.segmentcode = vip-nr[1] OR 
                guestseg.segmentcode = vip-nr[2] OR 
                guestseg.segmentcode = vip-nr[3] OR 
                guestseg.segmentcode = vip-nr[4] OR 
                guestseg.segmentcode = vip-nr[5] OR 
                guestseg.segmentcode = vip-nr[6] OR 
                guestseg.segmentcode = vip-nr[7] OR 
                guestseg.segmentcode = vip-nr[8] OR 
                guestseg.segmentcode = vip-nr[9] OR 
                guestseg.segmentcode = vip-nr[10]) NO-LOCK, 
                FIRST segment WHERE segment.segmentcode = guestseg.segmentcode 
                NO-LOCK BY res-line.ankunft:
              RUN assign-it.
          END.
      END.
  END.
  /*MT
  IF AVAILABLE res-line THEN 
  DO: 
    FIND FIRST reservation WHERE reservation.resnr = res-line.resnr 
      AND reservation.gastnr = res-line.gastnr NO-LOCK NO-ERROR. 
    IF AVAILABLE reservation THEN 
    DO: 
      /*MTresname = reservation.name. 
      FIND FIRST guest WHERE guest.gastnr = reservation.gastnr NO-LOCK NO-ERROR. 
      address = guest.adresse1. 
      city = guest.wohnort + " " + guest.plz. 
      comments = reservation.bemerk + chr(10) + res-line.bemerk. 
      DISP resname address city comments WITH FRAME f-reserve.*/
    END. 
  END. 
  */
END. 
 
PROCEDURE disp-arlist2: 
  /*MTENABLE b2 btn-print btn-stop btn-gcf  WITH FRAME f-reserve.*/
  IF sorttype = 1 THEN  /* Reservation  */ 
  DO: 
    /*MTENABLE lname fdate btn-start sorttype WITH FRAME f-reserve. 
    room = "". 
    DISP room WITH FRAME f-reserve. 
    DISABLE room WITH FRAME f-reserve.*/
    IF fdate = ? THEN 
    DO:
      FOR EACH res-line WHERE 
         (resstatus LE 5 OR resstatus = 11) 
         AND res-line.name GE lname
         AND res-line.zinr GE room
         /*AND res-line.NAME MATCHES ("*" + lname + "*")*/ NO-LOCK, 
         FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr NO-LOCK, 
         EACH guestseg WHERE guestseg.gastnr = res-line.gastnrmember AND 
           (guestseg.segmentcode = vip-nr[1] OR 
            guestseg.segmentcode = vip-nr[2] OR 
            guestseg.segmentcode = vip-nr[3] OR 
            guestseg.segmentcode = vip-nr[4] OR 
            guestseg.segmentcode = vip-nr[5] OR 
            guestseg.segmentcode = vip-nr[6] OR 
            guestseg.segmentcode = vip-nr[7] OR 
            guestseg.segmentcode = vip-nr[8] OR 
            guestseg.segmentcode = vip-nr[9] OR 
            guestseg.segmentcode = vip-nr[10]) NO-LOCK, 
          FIRST segment WHERE segment.segmentcode = guestseg.segmentcode 
          NO-LOCK BY res-line.name:
          RUN assign-it.
      END.
    END.
    ELSE 
    DO:
        IF by-period THEN
        DO:
            FOR EACH res-line WHERE 
               (resstatus LE 5 OR resstatus = 11) 
               AND res-line.name GE lname
               AND res-line.zinr GE room 
               /*AND res-line.NAME MATCHES ("*" + lname + "*")*/
               AND res-line.ankunft GE fdate 
               AND res-line.ankunft LE tdate NO-LOCK, 
               FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr NO-LOCK, 
               EACH guestseg WHERE guestseg.gastnr = res-line.gastnrmember AND 
                 (guestseg.segmentcode = vip-nr[1] OR 
                  guestseg.segmentcode = vip-nr[2] OR 
                  guestseg.segmentcode = vip-nr[3] OR 
                  guestseg.segmentcode = vip-nr[4] OR 
                  guestseg.segmentcode = vip-nr[5] OR 
                  guestseg.segmentcode = vip-nr[6] OR 
                  guestseg.segmentcode = vip-nr[7] OR 
                  guestseg.segmentcode = vip-nr[8] OR 
                  guestseg.segmentcode = vip-nr[9] OR 
                  guestseg.segmentcode = vip-nr[10]) NO-LOCK, 
                  FIRST segment WHERE segment.segmentcode = guestseg.segmentcode 
                  NO-LOCK BY res-line.name:
                RUN assign-it.
            END.
        END.
        ELSE
        DO:
            FOR EACH res-line WHERE 
               (resstatus LE 5 OR resstatus = 11) 
               AND res-line.name GE lname
               AND res-line.zinr GE room 
               /*AND res-line.NAME MATCHES ("*" + lname + "*")*/
               AND res-line.ankunft EQ fdate NO-LOCK, 
               FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr NO-LOCK, 
               EACH guestseg WHERE guestseg.gastnr = res-line.gastnrmember AND 
                 (guestseg.segmentcode = vip-nr[1] OR 
                  guestseg.segmentcode = vip-nr[2] OR 
                  guestseg.segmentcode = vip-nr[3] OR 
                  guestseg.segmentcode = vip-nr[4] OR 
                  guestseg.segmentcode = vip-nr[5] OR 
                  guestseg.segmentcode = vip-nr[6] OR 
                  guestseg.segmentcode = vip-nr[7] OR 
                  guestseg.segmentcode = vip-nr[8] OR 
                  guestseg.segmentcode = vip-nr[9] OR 
                  guestseg.segmentcode = vip-nr[10]) NO-LOCK, 
                  FIRST segment WHERE segment.segmentcode = guestseg.segmentcode 
                  NO-LOCK BY res-line.name:
                RUN assign-it.
            END.
        END.
    END.
  END. 
  ELSE IF sorttype = 2 THEN   /* In-house Guests */ 
  DO: 
    /*MTENABLE  lname room btn-start sorttype WITH FRAME f-reserve. 
    DISP fdate WITH FRAME f-reserve. 
    DISABLE fdate WITH FRAME f-reserve.*/
    IF lname EQ "" AND room NE "" THEN 
    DO:
      FOR EACH res-line WHERE (resstatus = 6 OR resstatus = 13) 
           AND res-line.name GE lname
           /*AND res-line.NAME MATCHES ("*" + lname + "*")*/
           AND res-line.zinr GE room NO-LOCK, 
           FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr NO-LOCK, 
           EACH guestseg WHERE guestseg.gastnr = res-line.gastnrmember AND 
           (guestseg.segmentcode = vip-nr[1] OR 
            guestseg.segmentcode = vip-nr[2] OR 
            guestseg.segmentcode = vip-nr[3] OR 
            guestseg.segmentcode = vip-nr[4] OR 
            guestseg.segmentcode = vip-nr[5] OR 
            guestseg.segmentcode = vip-nr[6] OR 
            guestseg.segmentcode = vip-nr[7] OR 
            guestseg.segmentcode = vip-nr[8] OR 
            guestseg.segmentcode = vip-nr[9] OR 
            guestseg.segmentcode = vip-nr[10]) NO-LOCK, 
            FIRST segment WHERE segment.segmentcode = guestseg.segmentcode 
            NO-LOCK BY res-line.zinr:
          RUN assign-it.
      END.
    END.
    ELSE
    DO:
      FOR EACH res-line WHERE (resstatus = 6 OR resstatus = 13) 
           /*AND res-line.name GE lname*/
           AND res-line.NAME MATCHES ("*" + lname + "*")
           AND res-line.zinr GE room NO-LOCK, 
           FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr NO-LOCK, 
           EACH guestseg WHERE guestseg.gastnr = res-line.gastnrmember AND 
           (guestseg.segmentcode = vip-nr[1] OR 
            guestseg.segmentcode = vip-nr[2] OR 
            guestseg.segmentcode = vip-nr[3] OR 
            guestseg.segmentcode = vip-nr[4] OR 
            guestseg.segmentcode = vip-nr[5] OR 
            guestseg.segmentcode = vip-nr[6] OR 
            guestseg.segmentcode = vip-nr[7] OR 
            guestseg.segmentcode = vip-nr[8] OR 
            guestseg.segmentcode = vip-nr[9] OR 
            guestseg.segmentcode = vip-nr[10]) NO-LOCK, 
            FIRST segment WHERE segment.segmentcode = guestseg.segmentcode 
            NO-LOCK BY res-line.name:
          RUN assign-it.
      END.
    END.
  END. 
  ELSE IF sorttype = 3 THEN   /* Arrival Today */ 
  DO: 
    /*MTENABLE lname btn-start sorttype WITH FRAME f-reserve. 
    room = "". 
    DISP room fdate WITH FRAME f-reserve. 
    DISABLE room fdate WITH FRAME f-reserve.*/
    FOR EACH res-line WHERE 
       (resstatus LE 5 OR resstatus = 11) 
       AND res-line.name GE lname
       AND res-line.zinr GE room 
       /*AND res-line.NAME MATCHES ("*" + lname + "*")*/
       AND res-line.ankunft = ci-date NO-LOCK, 
       FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr NO-LOCK, 
       EACH guestseg WHERE guestseg.gastnr = res-line.gastnrmember AND 
         (guestseg.segmentcode = vip-nr[1] OR 
          guestseg.segmentcode = vip-nr[2] OR 
          guestseg.segmentcode = vip-nr[3] OR 
          guestseg.segmentcode = vip-nr[4] OR 
          guestseg.segmentcode = vip-nr[5] OR 
          guestseg.segmentcode = vip-nr[6] OR 
          guestseg.segmentcode = vip-nr[7] OR 
          guestseg.segmentcode = vip-nr[8] OR 
          guestseg.segmentcode = vip-nr[9] OR 
          guestseg.segmentcode = vip-nr[10]) NO-LOCK, 
          FIRST segment WHERE segment.segmentcode = guestseg.segmentcode 
          NO-LOCK BY res-line.name:
        RUN assign-it.
    END.
  END. 
  ELSE IF sorttype = 4 THEN   /* Departure Today */ 
  DO: 
    /*MTENABLE lname btn-start sorttype WITH FRAME f-reserve. 
    room = "". 
    DISP room fdate WITH FRAME f-reserve. 
    DISABLE room fdate WITH FRAME f-reserve.*/
    FOR EACH res-line WHERE 
      (resstatus = 6 OR resstatus = 13) 
       AND res-line.name GE lname
       AND res-line.zinr GE room
       /*AND res-line.NAME MATCHES ("*" + lname + "*")*/
       AND res-line.abreise =  ci-date NO-LOCK, 
       FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr NO-LOCK, 
       EACH guestseg WHERE guestseg.gastnr = res-line.gastnrmember AND 
         (guestseg.segmentcode = vip-nr[1] OR 
          guestseg.segmentcode = vip-nr[2] OR 
          guestseg.segmentcode = vip-nr[3] OR 
          guestseg.segmentcode = vip-nr[4] OR 
          guestseg.segmentcode = vip-nr[5] OR 
          guestseg.segmentcode = vip-nr[6] OR 
          guestseg.segmentcode = vip-nr[7] OR 
          guestseg.segmentcode = vip-nr[8] OR 
          guestseg.segmentcode = vip-nr[9] OR 
          guestseg.segmentcode = vip-nr[10]) NO-LOCK, 
          FIRST segment WHERE segment.segmentcode = guestseg.segmentcode 
          NO-LOCK BY res-line.name:
        RUN assign-it.
    END.
  END. 
  ELSE IF sorttype = 5 THEN   /* All */ 
  DO: 
    /*MTENABLE lname fdate btn-start sorttype WITH FRAME f-reserve. 
    room = "". 
    DISP room WITH FRAME f-reserve. 
    DISABLE WITH FRAME f-reserve.*/
    IF fdate NE ? THEN 
    DO:
        IF by-period THEN
        DO:
            FOR EACH res-line WHERE 
                 ((active-flag = 0 AND res-line.ankunft GE fdate AND res-line.ankunft LE tdate
                 AND res-line.name GE lname AND res-line.zinr GE room /*AND res-line.NAME MATCHES ("*" + lname + "*")*/) OR 
                 (active-flag = 1 AND res-line.abreise GE fdate /*AND res-line.abreise LE tdate*/
                 AND res-line.name GE lname AND res-line.zinr GE room /*AND res-line.NAME MATCHES ("*" + lname + "*")*/)) 
                 AND resstatus NE 12 NO-LOCK, 
                 FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr NO-LOCK, 
                 EACH guestseg WHERE guestseg.gastnr = res-line.gastnrmember AND 
                 (guestseg.segmentcode = vip-nr[1] OR 
                  guestseg.segmentcode = vip-nr[2] OR 
                  guestseg.segmentcode = vip-nr[3] OR 
                  guestseg.segmentcode = vip-nr[4] OR 
                  guestseg.segmentcode = vip-nr[5] OR 
                  guestseg.segmentcode = vip-nr[6] OR 
                  guestseg.segmentcode = vip-nr[7] OR 
                  guestseg.segmentcode = vip-nr[8] OR 
                  guestseg.segmentcode = vip-nr[9] OR 
                  guestseg.segmentcode = vip-nr[10]) NO-LOCK, 
                  FIRST segment WHERE segment.segmentcode = guestseg.segmentcode 
                  NO-LOCK BY res-line.name:
                RUN assign-it.
            END.
        END.
        ELSE
        DO:
            FOR EACH res-line WHERE 
                 ((active-flag = 0 AND res-line.ankunft GE fdate 
                 AND res-line.name GE lname AND res-line.zinr GE room /*AND res-line.NAME MATCHES ("*" + lname + "*")*/) OR 
                 (active-flag = 1 AND res-line.abreise GE fdate 
                 AND res-line.name GE lname AND res-line.zinr GE room /*AND res-line.NAME MATCHES ("*" + lname + "*")*/)) 
                 AND resstatus NE 12 NO-LOCK, 
                 FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr NO-LOCK, 
                 EACH guestseg WHERE guestseg.gastnr = res-line.gastnrmember AND 
                 (guestseg.segmentcode = vip-nr[1] OR 
                  guestseg.segmentcode = vip-nr[2] OR 
                  guestseg.segmentcode = vip-nr[3] OR 
                  guestseg.segmentcode = vip-nr[4] OR 
                  guestseg.segmentcode = vip-nr[5] OR 
                  guestseg.segmentcode = vip-nr[6] OR 
                  guestseg.segmentcode = vip-nr[7] OR 
                  guestseg.segmentcode = vip-nr[8] OR 
                  guestseg.segmentcode = vip-nr[9] OR 
                  guestseg.segmentcode = vip-nr[10]) NO-LOCK, 
                  FIRST segment WHERE segment.segmentcode = guestseg.segmentcode 
                  NO-LOCK BY res-line.name:
                RUN assign-it.
            END.
        END.
    END.
    ELSE
    DO:
      FOR EACH res-line WHERE
          resstatus NE 9 AND resstatus NE 10 AND resstatus NE 12 
          AND res-line.name GE lname
          /*AND res-line.NAME MATCHES ("*" + lname + "*")*/ NO-LOCK, 
          FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr NO-LOCK, 
          EACH guestseg WHERE guestseg.gastnr = res-line.gastnrmember AND 
           (guestseg.segmentcode = vip-nr[1] OR 
            guestseg.segmentcode = vip-nr[2] OR 
            guestseg.segmentcode = vip-nr[3] OR 
            guestseg.segmentcode = vip-nr[4] OR 
            guestseg.segmentcode = vip-nr[5] OR 
            guestseg.segmentcode = vip-nr[6] OR 
            guestseg.segmentcode = vip-nr[7] OR 
            guestseg.segmentcode = vip-nr[8] OR 
            guestseg.segmentcode = vip-nr[9] OR 
            guestseg.segmentcode = vip-nr[10]) NO-LOCK, 
            FIRST segment WHERE segment.segmentcode = guestseg.segmentcode 
            NO-LOCK BY res-line.name:
          RUN assign-it.
      END.
    END.
  END. 
  /*MT
  IF AVAILABLE res-line THEN 
  DO: 
    FIND FIRST reservation WHERE reservation.resnr = res-line.resnr 
      AND reservation.gastnr = res-line.gastnr NO-LOCK NO-ERROR. 
    IF AVAILABLE reservation THEN 
    DO: 
      /*MTresname = reservation.name. 
      FIND FIRST guest WHERE guest.gastnr = reservation.gastnr NO-LOCK NO-ERROR. 
      address = guest.adresse1. 
      city = guest.wohnort + " " + guest.plz. 
      comments = reservation.bemerk + chr(10) + res-line.bemerk. 
      DISP resname address city comments WITH FRAME f-reserve.*/
    END. 
  END.
  */ 
END. 


PROCEDURE assign-it:
    CREATE t-vip-list.
    ASSIGN
    t-vip-list.resnr         = res-line.resnr
    t-vip-list.zinr          = res-line.zinr
    t-vip-list.name          = res-line.name
    t-vip-list.ankunft       = res-line.ankunft
    t-vip-list.anztage       = res-line.anztage
    t-vip-list.abreise       = res-line.abreise
    t-vip-list.zimmeranz     = res-line.zimmeranz
    t-vip-list.kurzbez       = zimkateg.kurzbez
    t-vip-list.erwachs       = res-line.erwachs
    t-vip-list.gratis        = res-line.gratis
    t-vip-list.resstatus     = res-line.resstatus
    t-vip-list.arrangement   = res-line.arrangement
    t-vip-list.zipreis       = res-line.zipreis
    t-vip-list.ankzeit       = res-line.ankzeit
    t-vip-list.abreisezeit   = res-line.abreisezeit
    t-vip-list.bezeich       = segment.bezeich.


    IF AVAILABLE res-line THEN 
    DO: 
      FIND FIRST reservation WHERE reservation.resnr = res-line.resnr 
        AND reservation.gastnr = res-line.gastnr NO-LOCK NO-ERROR. 
      IF AVAILABLE reservation THEN 
      DO: 
        t-vip-list.resname = reservation.name. 
        FIND FIRST guest WHERE guest.gastnr = reservation.gastnr NO-LOCK NO-ERROR. 
        t-vip-list.address = guest.adresse1. 
        t-vip-list.city = guest.wohnort + " " + guest.plz. 
        t-vip-list.comments = reservation.bemerk + chr(10) + res-line.bemerk.

        FIND FIRST guest WHERE guest.gastnr = res-line.gastnrmember NO-LOCK NO-ERROR.
        t-vip-list.karteityp = guest.karteityp.
        t-vip-list.gastnr = guest.gastnr.
      END. 
    END. 
END.
