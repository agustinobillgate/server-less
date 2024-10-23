DEFINE TEMP-TABLE rc-list
    FIELD grpflag      AS LOGICAL  
    FIELD resnr        AS INTEGER      FORMAT ">>>>>>9" 
    FIELD reslinnr     AS INTEGER      FORMAT ">>9" 
    FIELD gastnrmember AS INTEGER      FORMAT ">>>>>>>>>9" 
    FIELD name         AS CHARACTER    
    FIELD zinr         AS CHARACTER    
    FIELD gname        AS CHARACTER
    FIELD ankunft      AS DATE
    FIELD anztage      AS INTEGER
    FIELD abreise      AS DATE
    FIELD zimmeranz    AS INTEGER
    FIELD kurzbez      AS CHARACTER
    FIELD erwachs      AS INTEGER      FORMAT "99" 
    FIELD gratis       AS INTEGER
    FIELD resstatus    AS INTEGER
    FIELD arrangement  AS CHARACTER
    FIELD zipreis      AS DECIMAL      FORMAT ">>>,>>>,>>>,>>9.99" 
    FIELD ankzeit      AS INTEGER
    FIELD abreisezeit  AS INTEGER
    FIELD groupname    AS CHARACTER
    FIELD depositgef   AS DECIMAL       /*wen 051216*/
    FIELD depositbez   AS DECIMAL      /*wen 051216*/
    FIELD segment      AS CHAR
    FIELD gastnr       AS INTEGER /*gerald kebutuhan web*/
    FIELD karteityp    AS INTEGER. /*gerald kebutuhan web*/

DEFINE INPUT PARAMETER sorttype     AS INTEGER      NO-UNDO.
DEFINE INPUT PARAMETER last-sort    AS INTEGER      NO-UNDO.
DEFINE INPUT PARAMETER lname        AS CHARACTER    NO-UNDO.
DEFINE INPUT PARAMETER fdate        AS DATE         NO-UNDO.
DEFINE INPUT PARAMETER lresnr       AS INTEGER      NO-UNDO.
DEFINE INPUT PARAMETER room         AS CHARACTER    NO-UNDO.
/*M DEFINE INPUT PARAMETER rcNum        AS INTEGER      NO-UNDO. */
DEFINE OUTPUT PARAMETER TABLE FOR rc-list.
DEFINE OUTPUT PARAMETER msg-str     AS CHARACTER INITIAL "".

DEFINE VARIABLE ci-date         AS DATE.
DEFINE VARIABLE iNumOfRec       AS INTEGER  NO-UNDO INITIAL 0.

DEFINE BUFFER gmember FOR guest.

/******************* Main Logic ****************************/

FIND FIRST htparam WHERE htparam.paramnr = 87 NO-LOCK. 
ci-date = htparam.fdate. 

  IF sorttype = 1 THEN  /* Reservation  */ 
  DO: 
    IF last-sort = 1 THEN 
    DO: 
      IF fdate = ? THEN 
      DO:
          FOR EACH res-line WHERE (resstatus LE 5 OR resstatus = 11) 
              AND res-line.name GE lname NO-LOCK, 
              FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK,
              FIRST guest WHERE guest.gastnr = res-line.gastnr NO-LOCK,
              FIRST segment WHERE segment.segmentcode = reservation.segmentcode NO-LOCK,
              FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr 
              NO-LOCK BY res-line.NAME:
              RUN cr-rc-list.
          END.
      END.
      ELSE
      DO:
          FOR EACH res-line WHERE (resstatus LE 5 OR resstatus = 11) 
              AND res-line.name GE lname AND res-line.ankunft = fdate NO-LOCK,
              FIRST guest WHERE guest.gastnr = res-line.gastnr NO-LOCK,
              FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
              FIRST segment WHERE segment.segmentcode = reservation.segmentcode NO-LOCK,
              FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr 
              NO-LOCK BY res-line.NAME:
              RUN cr-rc-list.
          END.
      END.
    END. 
    ELSE IF last-sort = 2 THEN 
    DO: 
        IF fdate = ? THEN 
        DO:
            FOR EACH res-line WHERE (resstatus LE 5 OR resstatus = 11) NO-LOCK,
                FIRST reservation WHERE reservation.resnr = res-line.resnr 
                AND reservation.name GE lname NO-LOCK, 
                FIRST guest WHERE guest.gastnr = res-line.gastnr NO-LOCK,
                FIRST segment WHERE segment.segmentcode = reservation.segmentcode NO-LOCK,
                FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr 
                NO-LOCK BY (STRING( 1 - INTEGER(reservation.grpflag)) + 
                            reservation.name + STRING(reservation.resnr)) :
                RUN cr-rc-list.
            END.
        END.
      ELSE
      DO:
          FOR EACH res-line WHERE (resstatus LE 5 OR resstatus = 11) 
              AND res-line.ankunft = fdate NO-LOCK, 
              FIRST reservation WHERE reservation.resnr = res-line.resnr 
              AND reservation.name GE lname NO-LOCK,
              FIRST guest WHERE guest.gastnr = res-line.gastnr NO-LOCK,
              FIRST segment WHERE segment.segmentcode = reservation.segmentcode NO-LOCK,
              FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr 
              NO-LOCK BY (STRING( 1 - INTEGER(reservation.grpflag)) + 
                          reservation.name + STRING(reservation.resnr)):
              RUN cr-rc-list.
          END.
      END.
    END. 
    ELSE IF last-sort = 3 THEN
    DO:
        FOR EACH res-line WHERE (resstatus LE 5 OR resstatus = 11) 
            AND res-line.resnr GE lresnr NO-LOCK, 
            FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK,
            FIRST guest WHERE guest.gastnr = res-line.gastnr NO-LOCK,
            FIRST segment WHERE segment.segmentcode = reservation.segmentcode NO-LOCK,
            FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr 
            NO-LOCK BY res-line.resnr:
            RUN cr-rc-list.
        END.
    END.
  END. 
  ELSE IF sorttype = 2 THEN   /* Arrival Today */ 
  DO: 
    IF last-sort = 1 THEN 
    DO:    
        IF lname EQ "" AND room NE "" THEN 
        DO:
            FOR EACH res-line WHERE (resstatus LE 5 OR resstatus = 11) 
                AND res-line.ankunft = ci-date AND res-line.name GE lname 
                AND res-line.zinr GE room NO-LOCK, 
                FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK,
                FIRST guest WHERE guest.gastnr = res-line.gastnr NO-LOCK,
                FIRST segment WHERE segment.segmentcode = reservation.segmentcode NO-LOCK,
                FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr 
                NO-LOCK BY res-line.zinr:
                RUN cr-rc-list.
            END.
        END.
      ELSE
      DO:
          FOR EACH res-line WHERE (resstatus LE 5 OR resstatus = 11) 
              AND res-line.ankunft = ci-date AND res-line.name GE lname 
              AND res-line.zinr GE room NO-LOCK, 
              FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK,
              FIRST guest WHERE guest.gastnr = res-line.gastnr NO-LOCK,
              FIRST segment WHERE segment.segmentcode = reservation.segmentcode NO-LOCK,
              FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr 
              NO-LOCK BY res-line.NAME:
              RUN cr-rc-list.
          END.
      END.
    END. 
    IF last-sort = 2 THEN 
    DO: 
        FOR EACH res-line WHERE (resstatus LE 5 OR resstatus = 11) 
            AND res-line.ankunft = ci-date NO-LOCK, 
            FIRST reservation WHERE reservation.resnr = res-line.resnr 
            AND reservation.name GE lname NO-LOCK,
            FIRST guest WHERE guest.gastnr = res-line.gastnr NO-LOCK,
            FIRST segment WHERE segment.segmentcode = reservation.segmentcode NO-LOCK,
            FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr 
            NO-LOCK BY (STRING( 1 - INTEGER(reservation.grpflag)) + 
                        reservation.name + STRING(reservation.resnr)):
            RUN cr-rc-list.
        END.
    END. 
    ELSE IF last-sort = 3 THEN 
    DO:
        FOR EACH res-line WHERE (resstatus LE 5 OR resstatus = 11) 
            AND res-line.ankunft = ci-date AND res-line.resnr GE lresnr NO-LOCK, 
            FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK,
            FIRST guest WHERE guest.gastnr = res-line.gastnr NO-LOCK,
            FIRST segment WHERE segment.segmentcode = reservation.segmentcode NO-LOCK,
            FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr 
            NO-LOCK BY res-line.resnr:
            RUN cr-rc-list.
        END.
    END.
  END. 
  ELSE IF sorttype = 3 THEN   /* In-house Guests */ 
  DO: 
    IF last-sort = 1 THEN 
    DO: 
        IF lname EQ "" AND room NE "" THEN 
        DO:
            FOR EACH res-line WHERE (resstatus = 6 OR resstatus = 13) 
                AND res-line.name GE lname AND res-line.zinr GE room NO-LOCK, 
                FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK,
                FIRST guest WHERE guest.gastnr = res-line.gastnr NO-LOCK,
                FIRST segment WHERE segment.segmentcode = reservation.segmentcode NO-LOCK,
                FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr 
                NO-LOCK BY res-line.zinr:
                RUN cr-rc-list.
            END.
        END.
        ELSE
        DO:
            FOR EACH res-line WHERE (resstatus = 6 OR resstatus = 13) 
                AND res-line.name GE lname AND res-line.zinr GE room NO-LOCK, 
                FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK,
                FIRST guest WHERE guest.gastnr = res-line.gastnr NO-LOCK,
                FIRST segment WHERE segment.segmentcode = reservation.segmentcode NO-LOCK,
                FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr 
                NO-LOCK BY res-line.NAME:
                RUN cr-rc-list.
            END.
        END.
    END. 
    IF last-sort = 2 THEN 
    DO: 
        FOR EACH res-line WHERE (resstatus = 6 OR resstatus = 13) 
            AND res-line.zinr GE room NO-LOCK, 
            FIRST reservation WHERE reservation.resnr = res-line.resnr 
            AND reservation.name GE lname NO-LOCK, 
            FIRST segment WHERE segment.segmentcode = reservation.segmentcode NO-LOCK,
            FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr 
            NO-LOCK BY (STRING( 1 - INTEGER(reservation.grpflag)) + 
                        reservation.name + STRING(reservation.resnr)):
            RUN cr-rc-list.
        END.
    END. 
    ELSE IF last-sort = 3 THEN
    DO:
        FOR EACH res-line WHERE (resstatus = 6 OR resstatus = 13) 
            AND res-line.resnr GE lresnr NO-LOCK, 
            FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
            FIRST segment WHERE segment.segmentcode = reservation.segmentcode NO-LOCK,
            FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr 
            NO-LOCK BY res-line.resnr :
            RUN cr-rc-list.
        END.
    END.
  END. 
  ELSE IF sorttype = 4 THEN   /* All */ 
  DO: 
    IF last-sort = 1 THEN 
    DO:
        IF fdate NE ? THEN 
        DO:
            FOR EACH res-line WHERE active-flag LT 2 AND resstatus NE 12 
                AND res-line.ankunft EQ fdate AND res-line.name GE lname NO-LOCK, 
                FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK,
                FIRST guest WHERE guest.gastnr = res-line.gastnr NO-LOCK,
                FIRST segment WHERE segment.segmentcode = reservation.segmentcode NO-LOCK,
                FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr 
                NO-LOCK BY res-line.NAME:
                RUN cr-rc-list.
            END.
        END.
      ELSE 
      DO:
          FOR EACH res-line WHERE active-flag LT 2 AND resstatus NE 12 
              AND res-line.name GE lname NO-LOCK, 
              FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
              FIRST guest WHERE guest.gastnr = res-line.gastnr NO-LOCK,
              FIRST segment WHERE segment.segmentcode = reservation.segmentcode NO-LOCK,
              FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr 
              NO-LOCK BY res-line.NAME:
              RUN cr-rc-list.
          END.
      END.
    END. 
    IF last-sort = 2 THEN 
    DO: 
        IF fdate NE ? THEN 
        DO:
            FOR EACH res-line WHERE active-flag LT 2 
                AND res-line.ankunft EQ fdate NO-LOCK, 
                FIRST reservation WHERE reservation.resnr = res-line.resnr 
                AND reservation.name GE lname NO-LOCK,
                FIRST guest WHERE guest.gastnr = res-line.gastnr NO-LOCK,
                FIRST segment WHERE segment.segmentcode = reservation.segmentcode NO-LOCK,
                FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr 
                NO-LOCK BY reservation.NAME:
                RUN cr-rc-list.
            END.
        END.
      ELSE
      DO:
          FOR EACH res-line WHERE active-flag LT 2, 
              FIRST reservation WHERE reservation.resnr = res-line.resnr 
              AND reservation.name GE lname NO-LOCK,
              FIRST guest WHERE guest.gastnr = res-line.gastnr NO-LOCK,
              FIRST segment WHERE segment.segmentcode = reservation.segmentcode NO-LOCK,
              FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr 
              NO-LOCK BY (STRING( 1 - INTEGER(reservation.grpflag)) + 
                          reservation.name + STRING(reservation.resnr)):
              RUN cr-rc-list.
          END.
      END.
    END. 
    ELSE IF last-sort = 3 THEN 
    DO:
        FOR EACH res-line WHERE active-flag LT 2 AND resstatus NE 12 
            AND res-line.resnr GE lresnr NO-LOCK, 
            FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
            FIRST guest WHERE guest.gastnr = res-line.gastnr NO-LOCK,
            FIRST segment WHERE segment.segmentcode = reservation.segmentcode NO-LOCK,
            FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr 
            NO-LOCK BY res-line.resnr:
            RUN cr-rc-list.
        END.
    END.
  END. 

  /* Add by Michael @ 08/10/2018 for Harris Riverview Kuta request - ticket no BE33F1 */
  ELSE IF sorttype = 5 THEN   /* Arrival Tomorrow */ 
  DO: 
    IF last-sort = 1 THEN 
    DO:
      FOR EACH res-line WHERE active-flag LT 2 AND resstatus NE 12 
          AND res-line.ankunft EQ (ci-date + 1) NO-LOCK, 
          FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK,
          FIRST guest WHERE guest.gastnr = res-line.gastnr NO-LOCK,
          FIRST segment WHERE segment.segmentcode = reservation.segmentcode NO-LOCK,
          FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr 
          NO-LOCK BY res-line.NAME:
          RUN cr-rc-list.
      END.
    END. 
    IF last-sort = 2 THEN 
    DO: 
      FOR EACH res-line WHERE active-flag LT 2
          AND res-line.ankunft EQ (ci-date + 1), 
          FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
          FIRST guest WHERE guest.gastnr = res-line.gastnr NO-LOCK,
          FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr 
          NO-LOCK BY (STRING( 1 - INTEGER(reservation.grpflag)) + 
                      reservation.name + STRING(reservation.resnr)):
          RUN cr-rc-list.
      END.
    END. 
    ELSE IF last-sort = 3 THEN 
    DO:
        FOR EACH res-line WHERE active-flag LT 2 AND resstatus NE 12
            AND res-line.ankunft EQ (ci-date + 1)NO-LOCK, 
            FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK,
            FIRST guest WHERE guest.gastnr = res-line.gastnr NO-LOCK,
            FIRST segment WHERE segment.segmentcode = reservation.segmentcode NO-LOCK,
            FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr 
            NO-LOCK BY res-line.resnr:
            RUN cr-rc-list.
        END.
    END.
  END.
  /* End of add */

PROCEDURE cr-rc-list:
    CREATE rc-list.
    ASSIGN rc-list.grpflag        = reservation.grpflag
           rc-list.resnr          = res-line.resnr
           rc-list.reslinnr       = res-line.reslinnr
           rc-list.gastnrmember   = res-line.gastnrmember
           rc-list.name           = reservation.name
           rc-list.zinr           = res-line.zinr
           rc-list.gname          = res-line.name
           rc-list.ankunft        = res-line.ankunft
           rc-list.anztage        = res-line.anztage
           rc-list.abreise        = res-line.abreise
           rc-list.zimmeranz      = res-line.zimmeranz
           rc-list.kurzbez        = zimkateg.kurzbez
           rc-list.erwachs        = res-line.erwachs
           rc-list.gratis         = res-line.gratis
           rc-list.resstatus      = res-line.resstatus
           rc-list.arrangement    = res-line.arrangement
           rc-list.zipreis        = res-line.zipreis
           rc-list.ankzeit        = res-line.ankzeit
           rc-list.abreisezeit    = res-line.abreisezeit
           rc-list.groupname      = reservation.groupname
           rc-list.depositgef     = reservation.depositgef   /*wen 051216*/
           rc-list.depositbez     = reservation.depositbez
           rc-list.segment        = segment.bezeich
           rc-list.gastnr         = res-line.gastnr.

    FIND FIRST gmember WHERE gmember.gastnr = res-line.gastnrmember NO-LOCK NO-ERROR.
    IF AVAILABLE gmember THEN ASSIGN rc-list.karteityp = gmember.karteityp.
END.

