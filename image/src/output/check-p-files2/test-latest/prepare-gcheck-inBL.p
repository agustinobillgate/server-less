DEF TEMP-TABLE t-reservation LIKE reservation.  
  
DEFINE TEMP-TABLE gcheck-in  
    FIELD resnr       LIKE res-line.resnr  
    FIELD zinr        LIKE res-line.zinr  
    FIELD NAME        LIKE res-line.name   
    FIELD abreise     LIKE res-line.abreise   
    FIELD anztage     LIKE res-line.anztage   
    FIELD zimmeranz   LIKE res-line.zimmeranz   
    FIELD kurzbez     LIKE zimkateg.kurzbez   
    FIELD erwachs     LIKE res-line.erwachs   
    FIELD gratis      LIKE res-line.gratis   
    FIELD resstatus   LIKE res-line.resstatus   
    FIELD arrangement LIKE res-line.arrangement   
    FIELD zipreis     LIKE res-line.zipreis   
    FIELD wabkurz     LIKE waehrung.wabkurz   
    FIELD l-zuordnung LIKE res-line.l-zuordnung[3]  
    FIELD ankzeit     LIKE res-line.ankzeit  
    FIELD gastnr      LIKE res-line.gastnr  
    FIELD reslinnr    LIKE res-line.reslinnr  
    FIELD gastnrmember LIKE res-line.gastnrmember  
    FIELD grpflag     LIKE reservation.grpflag  
.  
  
DEF INPUT PARAMETER  input-resnr AS INTEGER  NO-UNDO.  
DEF OUTPUT PARAMETER i-slist2    AS INTEGER  NO-UNDO INIT 0.  
DEF OUTPUT PARAMETER ci-date     AS DATE     NO-UNDO.  
  
DEF OUTPUT PARAMETER TABLE FOR t-reservation.  
DEF OUTPUT PARAMETER TABLE FOR gcheck-in.  
  
RUN htpint.p (297, OUTPUT i-slist2).  
RUN htpdate.p(87, OUTPUT ci-date).  
  
FIND FIRST reservation WHERE reservation.resnr = input-resnr NO-LOCK.   
CREATE t-reservation.  
BUFFER-COPY reservation TO t-reservation.  
  
RUN gcheck-inbl.p (input-resnr, ci-date, OUTPUT TABLE gcheck-in).  
