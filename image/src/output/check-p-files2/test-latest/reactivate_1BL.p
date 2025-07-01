DEFINE TEMP-TABLE t-reactivate
    FIELD resnr                 LIKE res-line.resnr
    FIELD reslinnr              LIKE res-line.reslinnr
    FIELD gastnr                LIKE res-line.gastnr
    FIELD rsvname               LIKE reservation.NAME
    FIELD rsname                LIKE res-line.NAME
    FIELD ankunft               LIKE res-line.ankunft
    FIELD abreise               LIKE res-line.abreise
    FIELD resstatus             LIKE res-line.resstatus
    FIELD zimmeranz             LIKE res-line.zimmeranz
    FIELD kurzbez               LIKE zimkateg.kurzbez
    FIELD erwachs               LIKE res-line.erwachs
    FIELD gratis                LIKE res-line.gratis
    FIELD arrangement           LIKE res-line.arrangement
    FIELD zipreis               LIKE res-line.zipreis
    FIELD zinr                  LIKE res-line.zinr
    FIELD cancelled             LIKE res-line.CANCELLED
    FIELD cancelled-id          LIKE res-line.cancelled-id
    FIELD bemerk                LIKE res-line.bemerk
    FIELD bemerk1               LIKE reservation.bemerk
    FIELD rsv-gastnr            LIKE reservation.gastnr
    FIELD anztage               LIKE res-line.anztage   
    FIELD active-flag           LIKE res-line.active-flag
    FIELD activeflag            LIKE reservation.activeflag
    FIELD betrieb-gastpay       LIKE res-line.betrieb-gastpay
    FIELD kind1                 LIKE res-line.kind1
    FIELD kind2                 LIKE res-line.kind2
    FIELD changed               LIKE res-line.changed
    FIELD changed-id            LIKE res-line.changed-id
    FIELD address               LIKE guest.adresse1
    FIELD city                  LIKE guest.wohnort
    FIELD deposit               AS LOGICAL.

DEFINE INPUT PARAMETER fresnr               AS INTEGER.
DEFINE INPUT PARAMETER fdate                AS DATE.
DEFINE INPUT PARAMETER fname                AS CHAR.
DEFINE INPUT-OUTPUT PARAMETER comments      AS CHAR.
DEFINE OUTPUT PARAMETER resname             AS CHAR.
DEFINE OUTPUT PARAMETER address             AS CHAR.
DEFINE OUTPUT PARAMETER city                AS CHAR.
DEFINE OUTPUT PARAMETER stat-avail          AS LOGICAL.
DEFINE OUTPUT PARAMETER TABLE FOR t-reactivate.

stat-avail = NO.
DEFINE VARIABLE tname                       AS CHAR. 
DEFINE VARIABLE loopi                       AS INTEGER.
DEFINE VARIABLE str                         AS CHAR.

  IF fresnr = 0 AND fdate = ? THEN 
  DO: 
    tname = CHR(ASC(SUBSTR(fname,1,1)) + 1). 
    FOR EACH res-line WHERE res-line.active-flag = 2 
          AND (resstatus = 9 OR resstatus = 10) AND res-line.resname GE fname 
          AND res-line.resname LT tname AND res-line.l-zuordnung[3] = 0 NO-LOCK, 
        FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
        FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr 
        NO-LOCK BY reservation.NAME :
          RUN create-t-reactive.
    END.

    FOR EACH res-line WHERE 
          res-line.active-flag = 0 
          AND (resstatus = 9 OR resstatus = 10) /*ragung*/
          AND res-line.zimmer-wunsch MATCHES "*cancel*" 
          AND res-line.resname GE fname 
          AND res-line.resname LT tname AND res-line.l-zuordnung[3] = 0 NO-LOCK, 
          FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK, 
          FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr 
          NO-LOCK BY reservation.NAME :
            RUN create-t-reactive.          
    END.
  END. 
  ELSE 
  DO: 
    IF fresnr EQ 0 THEN 
    DO:
      FOR EACH res-line WHERE 
          res-line.active-flag = 2 AND res-line.l-zuordnung[3] = 0
          AND (resstatus = 9 OR resstatus = 10) AND res-line.ankunft EQ fdate NO-LOCK, 
          FIRST reservation WHERE reservation.resnr = res-line.resnr 
          AND reservation.name GE fname NO-LOCK, 
          FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr 
          NO-LOCK BY reservation.NAME :
            RUN create-t-reactive.
      END.

      FOR EACH res-line WHERE 
          res-line.active-flag = 0 AND res-line.l-zuordnung[3] = 0
          AND (resstatus = 9 OR resstatus = 10) /*ragung*/
          AND res-line.zimmer-wunsch MATCHES "*cancel*" NO-LOCK, 
          FIRST reservation WHERE reservation.resnr = res-line.resnr 
          AND reservation.name GE fname NO-LOCK, 
          FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr 
          NO-LOCK BY reservation.NAME :

          DO loopi = 1 TO NUM-ENTRIES(res-line.zimmer-wunsch,";") - 1:
              str = ENTRY(loopi, res-line.zimmer-wunsch, ";").
              IF str MATCHES "*$arrival$*" THEN DO:
                  IF DATE(INT(SUBSTR(str, 13, 2)), INT(SUBSTR(str, 10, 2)), INT(SUBSTR(str, 16, 4))) EQ fdate THEN DO:
                        RUN create-t-reactive.
                        LEAVE.
                  END.
              END.
          END.
      END.
    END.
    ELSE
    DO:
      FOR EACH res-line WHERE res-line.active-flag = 2 
          AND (resstatus = 9 OR resstatus = 10) AND res-line.resnr GE fresnr 
          AND res-line.resnr LE (fresnr + 100) AND res-line.l-zuordnung[3] = 0 
          NO-LOCK, 
          FIRST reservation WHERE reservation.resnr = res-line.resnr 
          AND reservation.name GE fname NO-LOCK, 
          FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr 
          NO-LOCK BY res-line.resnr :
            RUN create-t-reactive.
      END.

      FOR EACH res-line WHERE 
          res-line.active-flag = 0 
          AND (resstatus = 9 OR resstatus = 10) /*ragung*/
          AND res-line.zimmer-wunsch MATCHES "*cancel*" 
          AND res-line.resnr GE fresnr 
          AND res-line.resnr LE (fresnr + 100) 
          AND res-line.l-zuordnung[3] = 0 NO-LOCK, 
          FIRST reservation WHERE reservation.resnr = res-line.resnr 
          AND reservation.name GE fname NO-LOCK, 
          FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr 
          NO-LOCK BY res-line.resnr :
            RUN create-t-reactive.          
      END.
    END.
  END. 

  FIND FIRST t-reactivate NO-LOCK NO-ERROR.
  IF AVAILABLE t-reactivate THEN 
  DO: 
    stat-avail = YES.
    resname = t-reactivate.rsvname. 
    FIND FIRST guest WHERE guest.gastnr = t-reactivate.rsv-gastnr NO-LOCK NO-ERROR. 
    address = guest.adresse1. 
    city = guest.wohnort + " " + guest.plz. 
    comments = t-reactivate.bemerk1 + chr(10) + t-reactivate.bemerk. 
  END. 

PROCEDURE create-t-reactive:

    FIND FIRST guest WHERE guest.gastnr = res-line.gastnr NO-LOCK. 

    CREATE t-reactivate.
    ASSIGN 
       t-reactivate.resnr           = res-line.resnr
       t-reactivate.reslinnr        = res-line.reslinnr
       t-reactivate.rsvname         = reservation.name
       t-reactivate.rsname          = res-line.name
       t-reactivate.ankunft         = res-line.ankunft
       t-reactivate.abreise         = res-line.abreise
       t-reactivate.resstatus       = res-line.resstatus
       t-reactivate.zimmeranz       = res-line.zimmeranz
       t-reactivate.kurzbez         = zimkateg.kurzbez 
       t-reactivate.erwachs         = res-line.erwachs
       t-reactivate.gratis          = res-line.gratis
       t-reactivate.arrangement     = res-line.arrangement
       t-reactivate.zipreis         = res-line.zipreis
       t-reactivate.zinr            = res-line.zinr
       t-reactivate.cancelled       = res-line.cancelled
       t-reactivate.cancelled-id    = res-line.cancelled-id
       t-reactivate.bemerk          = res-line.bemerk
       t-reactivate.bemerk1         = reservation.bemerk
       t-reactivate.rsv-gastnr      = reservation.gastnr
       t-reactivate.anztage         = res-line.anztage
       t-reactivate.gastnr          = res-line.gastnr
       t-reactivate.active-flag     = res-line.active-flag
       t-reactivate.activeflag      = reservation.activeflag
       t-reactivate.betrieb-gastpay = res-line.betrieb-gastpay
       t-reactivate.kind1           = res-line.kind1
       t-reactivate.kind2           = res-line.kind2
       t-reactivate.changed         = res-line.changed
       t-reactivate.changed-id      = res-line.changed-id
       t-reactivate.address         = guest.adresse1. 
       t-reactivate.city            = guest.wohnort + " " 
                                    + guest.plz. 

       IF reservation.depositgef NE 0 THEN ASSIGN t-reactivate.deposit = YES.
       ELSE ASSIGN t-reactivate.deposit = NO.
END.
