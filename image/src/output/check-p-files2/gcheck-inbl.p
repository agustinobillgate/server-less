DEFINE TEMP-TABLE gcheck-in
    FIELD resnr     LIKE res-line.resnr
    FIELD zinr      LIKE res-line.zinr
    FIELD NAME      LIKE res-line.name 
    FIELD abreise   LIKE res-line.abreise 
    FIELD anztage   LIKE res-line.anztage 
    FIELD zimmeranz LIKE res-line.zimmeranz 
    FIELD kurzbez   LIKE zimkateg.kurzbez 
    FIELD erwachs   LIKE res-line.erwachs 
    FIELD gratis    LIKE res-line.gratis 
    FIELD resstatus LIKE res-line.resstatus 
    FIELD arrangement LIKE res-line.arrangement 
    FIELD zipreis     LIKE res-line.zipreis 
    FIELD wabkurz     LIKE waehrung.wabkurz 
    FIELD l-zuordnung LIKE res-line.l-zuordnung[3]
    FIELD ankzeit     LIKE res-line.ankzeit
    FIELD gastnr      LIKE res-line.gastnr
    FIELD reslinnr    LIKE res-line.reslinnr
    FIELD gastnrmember LIKE res-line.gastnrmember
    FIELD grpflag     LIKE reservation.grpflag.

DEFINE INPUT PARAMETER input-resnr AS INTEGER. 
DEFINE INPUT PARAMETER ci-date AS DATE. 
DEFINE OUTPUT PARAMETER TABLE FOR gcheck-in.


RUN disp-arlist.


PROCEDURE disp-arlist: 
  FOR EACH res-line WHERE 
    (res-line.resstatus LE 5 OR res-line.resstatus = 11) AND res-line.resnr EQ input-resnr 
     AND res-line.ankunft = ci-date NO-LOCK, 
     FIRST waehrung WHERE waehrung.waehrungsnr = res-line.betriebsnr NO-LOCK, 
     FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr NO-LOCK, 
     FIRST guest WHERE guest.gastnr = res-line.gastnr NO-LOCK, 
     FIRST reservation WHERE reservation.resnr = res-line.resnr 
     NO-LOCK BY res-line.resnr:
     CREATE gcheck-in.
     ASSIGN
     gcheck-in.resnr     = res-line.resnr
     gcheck-in.zinr      = res-line.zinr
     gcheck-in.NAME      = res-line.name 
     gcheck-in.abreise   = res-line.abreise 
     gcheck-in.anztage   = res-line.anztage 
     gcheck-in.zimmeranz = res-line.zimmeranz 
     gcheck-in.kurzbez   = zimkateg.kurzbez 
     gcheck-in.erwachs   = res-line.erwachs 
     gcheck-in.gratis    = res-line.gratis 
     gcheck-in.resstatus = res-line.resstatus 
     gcheck-in.arrangement = res-line.arrangement 
     gcheck-in.zipreis     = res-line.zipreis 
     gcheck-in.wabkurz     = waehrung.wabkurz 
     gcheck-in.l-zuordnung = res-line.l-zuordnung[3]
     gcheck-in.ankzeit     = res-line.ankzeit
     gcheck-in.gastnr      = res-line.gastnr
     gcheck-in.reslinnr    = res-line.reslinnr
     gcheck-in.gastnrmember    = res-line.gastnrmember    
     gcheck-in.grpflag     = reservation.grpflag.    .
  END.
END.
