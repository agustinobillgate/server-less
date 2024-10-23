DEFINE TEMP-TABLE check-out-list
    FIELD zinr          LIKE res-line.zinr
    FIELD reser-name    LIKE reservation.name 
    FIELD resli-name    LIKE res-line.name 
    FIELD g-name        LIKE guest.name 
    FIELD ankunft       LIKE res-line.ankunft
    FIELD abreise       LIKE res-line.abreise
    /*   anztage   */ 
    FIELD kurzbez       LIKE zimkateg.kurzbez 
    FIELD erwachs       LIKE res-line.erwachs
    FIELD gratis        LIKE res-line.gratis
    FIELD resstatus     LIKE res-line.resstatus
    FIELD arrangement   LIKE res-line.arrangement
    FIELD zipreis       LIKE res-line.zipreis
    FIELD groupname     LIKE reservation.groupname 
    FIELD resnr         LIKE res-line.resnr
    FIELD gastnr        LIKE res-line.gastnr
    FIELD bemerk        LIKE res-line.bemerk
    FIELD gastnrmember  LIKE res-line.gastnrmember
    FIELD reslinnr      LIKE res-line.reslinnr
    FIELD zimmeranz     LIKE res-line.zimmeranz
    FIELD res-address   AS CHAR
    FIELD res-city      AS CHAR
    FIELD res-bemerk    AS CHAR
    FIELD recid-resline AS INTEGER /*ITA 060913*/
    .

DEFINE INPUT PARAMETER sorttype     AS INTEGER.
DEFINE INPUT PARAMETER input-resnr  AS INTEGER.
DEFINE INPUT PARAMETER lzinr        AS CHAR.
DEFINE INPUT PARAMETER lname        AS CHAR.
DEFINE INPUT PARAMETER gname        AS CHAR.

DEFINE OUTPUT PARAMETER ci-date     AS DATE.
DEFINE OUTPUT PARAMETER TABLE FOR check-out-list.

RUN htpdate.p (87, OUTPUT ci-date).
RUN disp-arlist.
 
/***************************  PROCEDURE   **************************************/ 
 
PROCEDURE disp-arlist: 
  IF sorttype = 1 THEN  /* Roon Number*/ 
  DO: 
    IF input-resnr = 0 THEN 
       FOR EACH res-line WHERE (res-line.resstatus = 6 OR res-line.resstatus = 13) 
          AND res-line.zinr GE lzinr 
          AND res-line.abreise = ci-date NO-LOCK, 
          FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr, 
          FIRST guest WHERE guest.gastnr = res-line.gastnr, 
          FIRST reservation WHERE reservation.resnr = res-line.resnr 
          NO-LOCK BY (res-line.zinr + res-line.name):
            RUN assign-it.
       END.
    ELSE
       FOR EACH res-line WHERE (res-line.resstatus = 6 OR res-line.resstatus = 13) 
          AND res-line.zinr GE lzinr 
          AND res-line.resnr = input-resnr NO-LOCK, 
          FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr, 
          FIRST guest WHERE guest.gastnr = res-line.gastnr, 
          FIRST reservation WHERE reservation.resnr = res-line.resnr 
          NO-LOCK BY (res-line.zinr + res-line.name):
            RUN assign-it.
       END.
  END. 
  ELSE IF sorttype = 2 THEN   /* Guest Name */ 
  DO: 
    IF input-resnr = 0 THEN 
       FOR EACH res-line WHERE (res-line.resstatus = 6 OR res-line.resstatus = 13) 
          AND res-line.zinr GE lzinr AND res-line.abreise = ci-date NO-LOCK, 
          FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr, 
          FIRST guest WHERE guest.gastnr = res-line.gastnrmember AND guest.name GE lname, 
          FIRST reservation WHERE reservation.resnr = res-line.resnr
          NO-LOCK BY res-line.name:
            RUN assign-it.
       END.
    ELSE 
       FOR EACH res-line WHERE (res-line.resstatus = 6 OR res-line.resstatus = 13) 
          AND res-line.zinr GE lzinr AND res-line.resnr = input-resnr NO-LOCK, 
          FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr, 
          FIRST guest WHERE guest.gastnr = res-line.gastnrmember AND guest.name GE lname, 
          FIRST reservation WHERE reservation.resnr = res-line.resnr 
          NO-LOCK BY res-line.name:
            RUN assign-it.
       END.
  END. 
  ELSE IF sorttype = 3 THEN   /* Company Name / Group Reservation*/ 
  DO: 
    IF input-resnr = 0 THEN 
       FOR EACH res-line WHERE (res-line.resstatus = 6 OR res-line.resstatus = 13) 
          AND res-line.abreise = ci-date NO-LOCK, 
          FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr, 
          FIRST guest WHERE guest.gastnr = res-line.gastnr AND guest.name GE gname, 
          FIRST reservation WHERE reservation.resnr = res-line.resnr AND reservation.grpflag = YES 
          NO-LOCK BY (guest.name + STRING(res-line.resnr)):
            RUN assign-it.
       END.
    ELSE 
       FOR EACH res-line WHERE (res-line.resstatus = 6 OR res-line.resstatus = 13) 
          AND res-line.resnr = input-resnr NO-LOCK, 
          FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr, 
          FIRST guest WHERE guest.gastnr = res-line.gastnr AND guest.name GE gname, 
          FIRST reservation WHERE reservation.resnr = res-line.resnr AND reservation.grpflag = YES 
          NO-LOCK BY (guest.name + STRING(res-line.resnr)):
            RUN assign-it.
       END.
  END. 
END. 


PROCEDURE assign-it:
    CREATE check-out-list.
    ASSIGN
        check-out-list.zinr          = res-line.zinr
        check-out-list.reser-name    = reservation.name 
        check-out-list.resli-name    = res-line.name 
        check-out-list.g-name        = guest.name 
        check-out-list.ankunft       = res-line.ankunft
        check-out-list.abreise       = res-line.abreise
       /*   anztage   */ 
        check-out-list.kurzbez       = zimkateg.kurzbez 
        check-out-list.erwachs       = res-line.erwachs
        check-out-list.gratis        = res-line.gratis
        check-out-list.resstatus     = res-line.resstatus
        check-out-list.arrangement   = res-line.arrangement
        check-out-list.zipreis       = res-line.zipreis
        check-out-list.groupname     = reservation.groupname 
        check-out-list.resnr         = res-line.resnr
        check-out-list.gastnr        = res-line.gastnr
        check-out-list.bemerk        = res-line.bemerk
        check-out-list.gastnrmember  = res-line.gastnrmember
        check-out-list.reslinnr      = res-line.reslinnr
        check-out-list.zimmeranz     = res-line.zimmeranz
        check-out-list.res-address   = guest.adresse1
        check-out-list.res-city      = guest.wohnort + " " + guest.plz
        check-out-list.res-bemerk    = reservation.bemerk
        check-out-list.recid-resline = RECID(res-line)
    .
END.
