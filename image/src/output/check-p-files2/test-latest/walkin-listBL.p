DEFINE TEMP-TABLE t-walkin-list
    FIELD resnr         LIKE res-line.resnr 
    FIELD zinr          LIKE res-line.zinr
    FIELD NAME          LIKE res-line.NAME
    FIELD ankunft       LIKE res-line.ankunft
    FIELD anztage       LIKE res-line.anztage
    FIELD abreise       LIKE res-line.abreise
    FIELD zimmeranz     LIKE res-line.zimmeranz
    FIELD kurzbez       LIKE zimkateg.kurzbez 
    FIELD erwachs       LIKE res-line.erwachs
    FIELD kind1         LIKE res-line.kind1
    FIELD gratis        LIKE res-line.gratis
    FIELD resstatus     LIKE res-line.resstatus
    FIELD arrangement   LIKE res-line.arrangement
    FIELD zipreis       LIKE res-line.zipreis
    FIELD ankzeit       LIKE res-line.ankzeit
    FIELD abreisezeit   LIKE res-line.abreisezeit
    FIELD bezeich       LIKE segment.bezeich
    FIELD bemerk        LIKE res-line.bemerk
    FIELD gastnr        LIKE reservation.gastnr
    FIELD res-address   AS CHAR
    FIELD res-city      AS CHAR
    FIELD res-bemerk    AS CHAR
    .

DEFINE INPUT PARAMETER  case-type       AS INTEGER.
DEFINE INPUT PARAMETER  fdate           AS DATE.
DEFINE INPUT PARAMETER  walk-in         AS INTEGER.
DEFINE INPUT PARAMETER  wi-grp          AS INTEGER.
DEFINE INPUT PARAMETER  walkin-flag     AS LOGICAL.
DEFINE OUTPUT PARAMETER TABLE FOR t-walkin-list.

DEFINE VARIABLE wi-int                          AS INTEGER.
FIND FIRST htparam WHERE htparam.paramnr = 109 
    AND htparam.paramgruppe = 7.
    ASSIGN wi-int = htparam.finteger.

CASE case-type :
    WHEN 1 THEN RUN disp-arlist1.
    WHEN 2 THEN RUN disp-arlist2.
END CASE.

PROCEDURE disp-arlist1:
    
  IF fdate = ? THEN 
  DO:
     IF NOT walkin-flag THEN
     DO: 
         FOR EACH res-line WHERE 
           (resstatus = 6 OR resstatus = 13) AND active-flag = 1 
           AND res-line.gastnr EQ wi-int NO-LOCK, 
           FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
           FIRST segment WHERE (segment.segmentcode = reservation.segmentcode) 
             NO-LOCK,
           FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr 
           NO-LOCK BY res-line.name:
             RUN create-walkin-list.
         END.
      END.
      ELSE
      DO:
         FOR EACH res-line WHERE 
           (resstatus = 6 OR resstatus = 13) AND active-flag = 1 NO-LOCK, 
           FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
           FIRST segment WHERE (segment.segmentcode = reservation.segmentcode) AND 
           ((segment.segmentcode = walk-in)
             OR (segment.segmentgrup = wi-grp AND wi-grp NE 0)) NO-LOCK,
           FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr 
           NO-LOCK BY res-line.name:
             RUN create-walkin-list.
         END.
       END.
  END.
      
 
  ELSE IF fdate NE ? THEN 
  DO:
     IF NOT walkin-flag THEN
     DO:
         FOR EACH res-line WHERE 
            res-line.ankunft EQ fdate AND res-line.gastnr EQ wi-int 
           AND (resstatus NE 9 AND resstatus NE 10 AND resstatus NE 12) 
           AND active-flag LE 2 NO-LOCK, 
           FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
           FIRST segment WHERE (segment.segmentcode = reservation.segmentcode) NO-LOCK,
           FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr 
           NO-LOCK BY res-line.name:
             RUN create-walkin-list.
         END.
     END.
     ELSE
     DO:
         FOR EACH res-line WHERE 
            res-line.ankunft EQ fdate 
           AND (resstatus NE 9 AND resstatus NE 10 AND resstatus NE 12) 
           AND active-flag LE 2 NO-LOCK, 
           FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
           FIRST segment WHERE (segment.segmentcode = reservation.segmentcode) AND 
           ((segment.segmentcode = walk-in)
             OR (segment.segmentgrup = wi-grp AND wi-grp NE 0)) NO-LOCK,
           FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr 
           NO-LOCK BY res-line.name:
             RUN create-walkin-list.
         END.
     END.
  END.
    
    /*
    IF fdate = ? THEN 
    DO:
        IF NOT walkin-flag THEN
        FOR EACH res-line WHERE 
            (resstatus = 6 OR resstatus = 13) AND active-flag = 1 
            AND res-line.gastnr EQ wi-int NO-LOCK, 
            FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
            FIRST segment WHERE (segment.segmentcode = reservation.segmentcode) 
            NO-LOCK,
            FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr 
            NO-LOCK BY res-line.name:
            RUN create-walkin-list.
        END.
    END.
    ELSE IF fdate NE ? THEN
    DO:
        FOR EACH res-line WHERE res-line.ankunft EQ fdate 
            AND (resstatus NE 9 AND resstatus NE 10 AND resstatus NE 12) 
            AND active-flag LE 2 NO-LOCK, 
            FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
            FIRST segment WHERE (segment.segmentcode = reservation.segmentcode) 
            AND ((segment.segmentcode = walk-in)
                 OR (segment.segmentgrup = wi-grp AND wi-grp NE 0)) NO-LOCK,
            FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr 
            NO-LOCK BY res-line.NAME :
            RUN create-walkin-list.
        END.
    END.
    */
END.

PROCEDURE disp-arlist2: 

  IF fdate = ? THEN 
  DO:
     IF NOT walkin-flag THEN
     DO:
        FOR EACH res-line WHERE 
           (resstatus = 6 OR resstatus = 13) 
            AND res-line.gastnr EQ wi-int AND active-flag = 1 NO-LOCK, 
           FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
           FIRST segment WHERE (segment.segmentcode = reservation.segmentcode) 
            NO-LOCK,
           FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr 
           NO-LOCK BY res-line.name:
            RUN create-walkin-list.
        END.
     END.
     ELSE
     DO:
        FOR EACH res-line WHERE 
           (resstatus = 6 OR resstatus = 13) AND active-flag = 1 NO-LOCK, 
           FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
           FIRST segment WHERE (segment.segmentcode = reservation.segmentcode) AND 
           ((segment.segmentcode = walk-in)
             OR (segment.segmentgrup = wi-grp AND wi-grp NE 0)) NO-LOCK,
           FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr 
           NO-LOCK BY res-line.NAME:
            RUN create-walkin-list.
        END.
     END.

  END.
 
  ELSE IF fdate NE ? THEN 
  DO:
     IF NOT walkin-flag THEN
     DO:
         FOR EACH res-line WHERE 
            res-line.ankunft EQ fdate AND res-line.gastnr EQ wi-int
           AND (resstatus NE 9 AND resstatus NE 10 AND resstatus NE 12) 
           AND active-flag LE 2 NO-LOCK, 
           FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
           FIRST segment WHERE (segment.segmentcode = reservation.segmentcode) 
             NO-LOCK,
           FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr 
           NO-LOCK BY res-line.name:
             RUN create-walkin-list.
         END.
     END.
     ELSE
     DO:
         FOR EACH res-line WHERE 
            res-line.ankunft EQ fdate 
           AND (resstatus NE 9 AND resstatus NE 10 AND resstatus NE 12) 
           AND active-flag LE 2 NO-LOCK, 
           FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
           FIRST segment WHERE (segment.segmentcode = reservation.segmentcode) AND 
           ((segment.segmentcode = walk-in)
             OR (segment.segmentgrup = wi-grp AND wi-grp NE 0)) NO-LOCK,
           FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr 
           NO-LOCK BY res-line.name:
             RUN create-walkin-list.
         END.
     END.
  END.
    /*MT
    IF fdate = ? THEN 
    DO:
        FOR EACH res-line WHERE (resstatus = 6 OR resstatus = 13) 
            AND active-flag = 1 NO-LOCK, 
            FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
            FIRST segment WHERE (segment.segmentcode = reservation.segmentcode) 
            AND ((segment.segmentcode = walk-in) 
                 OR (segment.segmentgrup = wi-grp AND wi-grp NE 0)) NO-LOCK,
            FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr NO-LOCK
            BY res-line.NAME :
            RUN create-walkin-list.
        END.
    END.
    ELSE IF fdate NE ? THEN 
    DO:
        FOR EACH res-line WHERE res-line.ankunft EQ fdate 
            AND (resstatus NE 9 AND resstatus NE 10 AND resstatus NE 12) 
            AND active-flag LE 2 NO-LOCK, 
            FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
            FIRST segment WHERE (segment.segmentcode = reservation.segmentcode) 
            AND ((segment.segmentcode = walk-in) 
                 OR (segment.segmentgrup = wi-grp AND wi-grp NE 0)) NO-LOCK,
            FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr NO-LOCK 
            BY res-line.NAME :
            RUN create-walkin-list.
        END.
    END.
    */
END.

PROCEDURE create-walkin-list:
    FIND FIRST guest WHERE guest.gastnr = reservation.gastnr NO-LOCK.
    CREATE t-walkin-list.
    BUFFER-COPY res-line TO t-walkin-list.
    ASSIGN 
      t-walkin-list.kurzbez     = zimkateg.kurzbez
      t-walkin-list.bezeich     = segment.bezeich
      t-walkin-list.res-address = guest.adresse1
      t-walkin-list.res-city    = guest.wohnort + " " + guest.plz
      t-walkin-list.res-bemerk  = reservation.bemerk
    .
END.
