
DEF INPUT  PARAMETER recid-bk-reser AS INT.
DEF INPUT  PARAMETER o-resnr AS INT.
DEF INPUT  PARAMETER cancel-str AS CHAR.
DEF INPUT  PARAMETER user-init AS CHAR.

FIND FIRST bk-veran WHERE bk-veran.veran-nr = o-resnr USE-INDEX vernr-ix NO-LOCK. 

FIND FIRST bk-reser WHERE RECID(bk-reser) = recid-bk-reser NO-LOCK.
FIND FIRST b-storno WHERE b-storno.bankettnr = bk-reser.veran-nr 
    AND b-storno.breslinnr = bk-reser.veran-resnr EXCLUSIVE-LOCK NO-ERROR. 
IF NOT AVAILABLE b-storno THEN CREATE b-storno. 
ASSIGN 
      b-storno.bankettnr = bk-reser.veran-nr 
      b-storno.breslinnr = bk-reser.veran-resnr 
      b-storno.gastnr = bk-veran.gastnr 
      b-storno.betrieb-gast = bk-veran.gastnrver 
      b-storno.datum = bk-reser.datum 
      b-storno.grund[18] = cancel-str + " D*" 
        + STRING(TODAY,"99/99/99") + " " + STRING(TIME,"hh:mm:ss") 
        + " " + bk-reser.raum. 
      b-storno.usercode = user-init 
  . 
RUN ba-cancreslinebl.p(bk-reser.veran-nr, bk-reser.veran-resnr). 

