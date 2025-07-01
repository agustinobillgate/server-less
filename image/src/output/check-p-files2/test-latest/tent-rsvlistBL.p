DEFINE TEMP-TABLE t-tent-rsvlist
    FIELD ankunft       LIKE res-line.ankunft
    FIELD abreise       LIKE res-line.abreise
    FIELD arrangement   LIKE res-line.arrangement
    FIELD kurzbez       LIKE zimkateg.kurzbez
    FIELD rsvname       LIKE reservation.NAME
    FIELD rsname        LIKE res-line.NAME
    FIELD segmentcode   LIKE reservation.segmentcode
    FIELD nation1       LIKE guest.nation1
    FIELD zimmeranz     LIKE res-line.zimmeranz
    FIELD erwachs       LIKE res-line.erwachs
    FIELD gratis        LIKE res-line.gratis
    FIELD resstatus     LIKE res-line.resstatus
    FIELD bemerk        LIKE res-line.bemerk
    FIELD l-zuordnung   LIKE res-line.l-zuordnung 
    FIELD resnr         LIKE res-line.resnr
    .

DEFINE INPUT PARAMETER case-type        AS INTEGER.
DEFINE INPUT PARAMETER sorttype         AS INTEGER.
DEFINE INPUT PARAMETER from-date        AS DATE.
DEFINE INPUT PARAMETER to-date          AS DATE.
DEFINE OUTPUT PARAMETER TABLE FOR t-tent-rsvlist.

FOR EACH t-tent-rsvlist :
    DELETE t-tent-rsvlist.
    RELEASE t-tent-rsvlist.
END.

CASE case-type :
    WHEN 1 THEN RUN rsvlist1.
    WHEN 2 THEN RUN disp-ankunft.
    WHEN 3 THEN RUN disp-abreise.
    WHEN 4 THEN RUN disp-name.
    WHEN 5 THEN RUN disp-argt.
    WHEN 6 THEN RUN disp-rmcat.
END CASE.

PROCEDURE rsvlist1 :
    IF sorttype = 0 THEN
    DO:
       FOR EACH res-line WHERE (res-line.resstatus = 3 OR
         res-line.resstatus  = 4) AND res-line.active-flag = 0
         AND res-line.ankunft GE from-date AND res-line.ankunft LE to-date
         NO-LOCK, 
         FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
         FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr NO-LOCK, 
         FIRST guest WHERE guest.gastnr = res-line.gastnrmember NO-LOCK 
         BY res-line.ankunft :
           RUN create-tent-rsvlist.
       END.
    END.
        
   ELSE IF sorttype = 1 THEN
   DO:
      FOR EACH res-line WHERE res-line.resstatus = 3 AND res-line.active-flag = 0
         AND res-line.ankunft GE from-date AND res-line.ankunft LE to-date
         NO-LOCK, 
         FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
         FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr NO-LOCK, 
         FIRST guest WHERE guest.gastnr = res-line.gastnrmember NO-LOCK 
         BY res-line.ankunft :
          RUN create-tent-rsvlist.
      END.
   END.
   ELSE
   DO:
       FOR EACH res-line WHERE res-line.resstatus = 4 
         AND res-line.active-flag = 0 AND res-line.ankunft GE from-date 
         AND res-line.ankunft LE to-date NO-LOCK, 
         FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
         FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr NO-LOCK, 
         FIRST guest WHERE guest.gastnr = res-line.gastnrmember NO-LOCK 
         BY res-line.ankunft :
           RUN create-tent-rsvlist.
       END.
  END.
END.

PROCEDURE disp-ankunft:
    IF sorttype = 0 THEN
    DO:
       FOR EACH res-line WHERE (res-line.resstatus = 3 OR
           res-line.resstatus  = 4) AND res-line.active-flag = 0 AND 
           res-line.ankunft GE from-date AND res-line.ankunft LE to-date
           NO-LOCK, 
           FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
           FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr NO-LOCK, 
           FIRST guest WHERE guest.gastnr = res-line.gastnrmember NO-LOCK 
           BY res-line.ankunft :
            RUN create-tent-rsvlist.
       END.
    END.
    ELSE IF sorttype = 1 THEN
    DO:
       FOR EACH res-line WHERE res-line.resstatus = 3 
           AND res-line.active-flag = 0 AND res-line.ankunft GE from-date 
           AND res-line.ankunft LE to-date NO-LOCK, 
           FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
           FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr NO-LOCK,
           FIRST guest WHERE guest.gastnr = res-line.gastnrmember NO-LOCK 
           BY res-line.ankunft :
            RUN create-tent-rsvlist.
       END.
    END.
    ELSE
    DO:
       FOR EACH res-line WHERE res-line.resstatus = 4 
           AND res-line.active-flag = 0 AND res-line.ankunft GE from-date 
           AND res-line.ankunft LE to-date NO-LOCK, 
           FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK,
           FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr NO-LOCK, 
           FIRST guest WHERE guest.gastnr = res-line.gastnrmember NO-LOCK 
           BY res-line.ankunft :
             RUN create-tent-rsvlist.
       END.
    END.
END.

PROCEDURE disp-abreise:
    IF sorttype = 0 THEN
    DO:
      FOR EACH res-line WHERE (res-line.resstatus = 3 OR 
          res-line.resstatus  = 4) AND res-line.active-flag = 0
          AND res-line.ankunft GE from-date AND res-line.ankunft LE to-date
          NO-LOCK, 
          FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK,
          FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr NO-LOCK,
          FIRST guest WHERE guest.gastnr = res-line.gastnrmember NO-LOCK 
          BY res-line.abreise :
            RUN create-tent-rsvlist.
      END.
    END.
    ELSE IF sorttype = 1 THEN
    DO:
       FOR EACH res-line WHERE res-line.resstatus = 3 
           AND res-line.active-flag = 0 AND res-line.ankunft GE from-date 
           AND res-line.ankunft LE to-date NO-LOCK,
           FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK,
           FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr NO-LOCK,
           FIRST guest WHERE guest.gastnr = res-line.gastnrmember NO-LOCK 
           BY res-line.abreise :
             RUN create-tent-rsvlist.
       END.
    END.
    ELSE 
    DO:
       FOR EACH res-line WHERE res-line.resstatus = 4 
           AND res-line.active-flag = 0 AND res-line.ankunft GE from-date 
           AND res-line.ankunft LE to-date NO-LOCK,
           FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK,
           FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr NO-LOCK,
           FIRST guest WHERE guest.gastnr = res-line.gastnrmember NO-LOCK 
           BY res-line.abreise :
             RUN create-tent-rsvlist.
       END.
    END.
END.

PROCEDURE disp-name:
    IF sorttype = 0 THEN
    DO:
       FOR EACH res-line WHERE (res-line.resstatus = 3 
           OR res-line.resstatus  = 4) AND res-line.active-flag = 0
           AND res-line.ankunft GE from-date AND res-line.ankunft LE to-date
           NO-LOCK,
           FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK,
           FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr NO-LOCK,
           FIRST guest WHERE guest.gastnr = res-line.gastnrmember NO-LOCK 
           BY reservation.NAME :
            RUN create-tent-rsvlist.
       END.
    END.
    ELSE IF sorttype = 1 THEN
    DO:
       FOR EACH res-line WHERE res-line.resstatus = 3 
           AND res-line.active-flag = 0 AND res-line.ankunft GE from-date 
           AND res-line.ankunft LE to-date NO-LOCK,
           FIRST reservation WHERE reservation.resnr = res-line.resnr
           NO-LOCK,
           FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr NO-LOCK,
           FIRST guest WHERE guest.gastnr = res-line.gastnrmember NO-LOCK 
           BY reservation.NAME :
            RUN create-tent-rsvlist.
       END.
    END.
    ELSE 
    DO:
       FOR EACH res-line WHERE res-line.resstatus = 4 AND res-line.active-flag = 0
           AND res-line.ankunft GE from-date AND res-line.ankunft LE to-date
           NO-LOCK, 
           FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK,
           FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr NO-LOCK,
           FIRST guest WHERE guest.gastnr = res-line.gastnrmember NO-LOCK 
           BY reservation.NAME :
            RUN create-tent-rsvlist.
       END.
    END.
END.

PROCEDURE disp-argt:
    IF sorttype = 0 THEN
    DO:
       FOR EACH res-line WHERE (res-line.resstatus = 3 OR
            res-line.resstatus  = 4) AND res-line.active-flag = 0
            AND res-line.ankunft GE from-date AND res-line.ankunft LE to-date
            NO-LOCK, 
            FIRST reservation WHERE reservation.resnr = res-line.resnr
            NO-LOCK, 
            FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr 
            NO-LOCK, 
            FIRST guest WHERE guest.gastnr = res-line.gastnrmember 
            NO-LOCK BY res-line.arrangement :
                RUN create-tent-rsvlist.
       END.
    END.
    ELSE IF sorttype = 1 THEN
    DO:
        FOR EACH res-line WHERE res-line.resstatus = 3
            AND res-line.active-flag = 0
            AND res-line.ankunft GE from-date AND res-line.ankunft LE to-date
            NO-LOCK, FIRST reservation WHERE reservation.resnr = res-line.resnr
            NO-LOCK, FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr 
            NO-LOCK, FIRST guest WHERE guest.gastnr = res-line.gastnrmember 
            NO-LOCK BY res-line.arrangement :
             RUN create-tent-rsvlist.
        END.
    END.
    ELSE
    DO:
        FOR EACH res-line WHERE res-line.resstatus = 4 AND res-line.active-flag = 0
            AND res-line.ankunft GE from-date AND res-line.ankunft LE to-date
            NO-LOCK, FIRST reservation WHERE reservation.resnr = res-line.resnr
            NO-LOCK, FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr 
            NO-LOCK, FIRST guest WHERE guest.gastnr = res-line.gastnrmember 
            NO-LOCK BY res-line.arrangement :
             RUN create-tent-rsvlist.
        END.
    END.
END.

PROCEDURE disp-rmcat:
    IF sorttype = 0 THEN
    DO:
        FOR EACH res-line WHERE (res-line.resstatus = 3 OR
            res-line.resstatus  = 4) AND res-line.active-flag = 0
            AND res-line.ankunft GE from-date AND res-line.ankunft LE to-date
            NO-LOCK, FIRST reservation WHERE reservation.resnr = res-line.resnr
            NO-LOCK, FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr 
            NO-LOCK, FIRST guest WHERE guest.gastnr = res-line.gastnrmember 
            NO-LOCK BY zimkateg.kurzbez :
                RUN create-tent-rsvlist.
        END.
    END.
    ELSE IF sorttype = 1 THEN
    DO:
       FOR EACH res-line WHERE res-line.resstatus = 3 AND res-line.active-flag = 0
            AND res-line.ankunft GE from-date AND res-line.ankunft LE to-date
            NO-LOCK, FIRST reservation WHERE reservation.resnr = res-line.resnr
            NO-LOCK, FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr 
            NO-LOCK, FIRST guest WHERE guest.gastnr = res-line.gastnrmember 
            NO-LOCK BY zimkateg.kurzbez :
                RUN create-tent-rsvlist.
        END.
    END.
    ELSE 
    DO:
       FOR EACH res-line WHERE res-line.resstatus = 4
            AND res-line.active-flag = 0
            AND res-line.ankunft GE from-date AND res-line.ankunft LE to-date
            NO-LOCK, FIRST reservation WHERE reservation.resnr = res-line.resnr
            NO-LOCK, FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr 
            NO-LOCK, FIRST guest WHERE guest.gastnr = res-line.gastnrmember 
            NO-LOCK BY zimkateg.kurzbez :
                RUN create-tent-rsvlist.
        END.
    END.
END.

PROCEDURE create-tent-rsvlist :
    CREATE t-tent-rsvlist.
    ASSIGN
        t-tent-rsvlist.ankunft          = res-line.ankunft
        t-tent-rsvlist.abreise          = res-line.abreise
        t-tent-rsvlist.arrangement      = res-line.arrangement
        t-tent-rsvlist.kurzbez          = zimkateg.kurzbez
        t-tent-rsvlist.rsvname          = reservation.NAME
        t-tent-rsvlist.rsname           = res-line.NAME
        t-tent-rsvlist.resnr            = res-line.resnr
        t-tent-rsvlist.segmentcode      = reservation.segmentcode 
        t-tent-rsvlist.nation1          = guest.nation1
        t-tent-rsvlist.zimmeranz        = res-line.zimmeranz
        t-tent-rsvlist.erwachs          = res-line.erwachs
        t-tent-rsvlist.gratis           = res-line.gratis
        t-tent-rsvlist.resstatus        = res-line.resstatus
        t-tent-rsvlist.l-zuordnung      = res-line.l-zuordnung[3]
        t-tent-rsvlist.bemerk           = res-line.bemerk
       .

END.
