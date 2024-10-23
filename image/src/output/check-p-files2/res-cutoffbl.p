DEFINE TEMP-TABLE t-rescutoff
    FIELD resnr                 LIKE res-line.resnr
    FIELD gastnr                LIKE res-line.gastnr
    FIELD rsname                LIKE res-line.NAME
    FIELD ankunft               LIKE res-line.ankunft
    FIELD abreise               LIKE res-line.abreise
    FIELD zimmeranz             LIKE res-line.zimmeranz
    FIELD arrangement           LIKE res-line.arrangement
    FIELD zikatnr               LIKE res-line.zikatnr
    FIELD zipreis               LIKE res-line.zipreis
    FIELD anztage               LIKE res-line.anztage 
    FIELD erwachs               LIKE res-line.erwachs
    FIELD kind1                 LIKE res-line.kind1
    FIELD gratis                LIKE res-line.gratis
    FIELD resstatus             LIKE res-line.resstatus
    FIELD kurzbez               LIKE zimkateg.kurzbez
    FIELD rsv-resnr             LIKE reservation.resnr
    FIELD grpflag               LIKE reservation.grpflag
    FIELD rsvname               LIKE reservation.NAME
    FIELD point-resnr           LIKE reservation.point-resnr
    FIELD resdat                LIKE reservation.resdat
    FIELD groupname             LIKE reservation.groupname
    FIELD cutoffdate            AS DATE
    .

DEFINE INPUT  PARAMETER guaranteed                  AS LOGICAL NO-UNDO.
DEFINE INPUT  PARAMETER fr-date                     AS DATE.
DEFINE INPUT  PARAMETER to-date                     AS DATE.
DEFINE OUTPUT PARAMETER TABLE FOR t-rescutoff.

/* SY 30/07/2015 valid for terntavie booking only*/  
  
IF guaranteed = NO THEN
FOR EACH res-line WHERE res-line.active-flag = 0 
    AND res-line.resstatus = 3 NO-LOCK, 
    FIRST reservation WHERE reservation.resnr = res-line.resnr 
    AND ((reservation.point-resnr GT 0 AND res-line.ankunft = fr-date) 
    OR (reservation.point-resnr GT 0 AND (res-line.ankunft - reservation.point-resnr) GE fr-date
    AND (res-line.ankunft - reservation.point-resnr) LE to-date)),
    FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr NO-LOCK 
    BY reservation.point-resnr BY res-line.ankunft BY reservation.name BY reservation.resnr :
        CREATE t-rescutoff.
        ASSIGN 
            t-rescutoff.resnr        = res-line.resnr
            t-rescutoff.grpflag      = reservation.grpflag
            t-rescutoff.rsvname      = reservation.name
            t-rescutoff.rsname       = res-line.name
            t-rescutoff.point-resnr  = reservation.point-resnr
            t-rescutoff.cutoffdate   = res-line.ankunft - reservation.point-resnr
            t-rescutoff.ankunft      = res-line.ankunft
            t-rescutoff.abreise      = res-line.abreise
            t-rescutoff.zimmeranz    = res-line.zimmeranz
            t-rescutoff.kurzbez      = zimkateg.kurzbez 
            t-rescutoff.arrangement  = res-line.arrangement
            t-rescutoff.zipreis      = res-line.zipreis
            t-rescutoff.anztage      = res-line.anztage
            t-rescutoff.erwachs      = res-line.erwachs
            t-rescutoff.gratis       = res-line.gratis
            t-rescutoff.kind1        = res-line.kind1
            t-rescutoff.resstatus    = res-line.resstatus
            t-rescutoff.resdat       = reservation.resdat
            t-rescutoff.groupname    = reservation.groupname
            .
 END.
 ELSE IF guaranteed = YES THEN
 FOR EACH res-line WHERE res-line.active-flag = 0 
    AND res-line.resstatus = 1 NO-LOCK, 
    FIRST reservation WHERE reservation.resnr = res-line.resnr 
    AND ((reservation.point-resnr GT 0 AND res-line.ankunft = fr-date) 
    OR (reservation.point-resnr GT 0 AND (res-line.ankunft - reservation.point-resnr) GE fr-date
    AND (res-line.ankunft - reservation.point-resnr) LE to-date)),
    FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr NO-LOCK 
    BY reservation.point-resnr BY res-line.ankunft BY reservation.name BY reservation.resnr :
        CREATE t-rescutoff.
        ASSIGN 
            t-rescutoff.resnr        = res-line.resnr
            t-rescutoff.grpflag      = reservation.grpflag
            t-rescutoff.rsvname      = reservation.name
            t-rescutoff.rsname       = res-line.name
            t-rescutoff.point-resnr  = reservation.point-resnr
            t-rescutoff.cutoffdate   = res-line.ankunft - reservation.point-resnr
            t-rescutoff.ankunft      = res-line.ankunft
            t-rescutoff.abreise      = res-line.abreise
            t-rescutoff.zimmeranz    = res-line.zimmeranz
            t-rescutoff.kurzbez      = zimkateg.kurzbez 
            t-rescutoff.arrangement  = res-line.arrangement
            t-rescutoff.zipreis      = res-line.zipreis
            t-rescutoff.anztage      = res-line.anztage
            t-rescutoff.erwachs      = res-line.erwachs
            t-rescutoff.gratis       = res-line.gratis
            t-rescutoff.kind1        = res-line.kind1
            t-rescutoff.resstatus    = res-line.resstatus
            t-rescutoff.resdat       = reservation.resdat
            t-rescutoff.groupname    = reservation.groupname
            .
 END.

