 
DEFINE INPUT PARAMETER resnr LIKE bk-reser.veran-nr. 
DEFINE INPUT PARAMETER resline LIKE bk-reser.veran-resnr. 
DEFINE INPUT PARAMETER r-status LIKE bk-reser.resstatus. 
/* 
DEFINE VARIABLE resnr LIKE bk-reser.veran-nr INITIAL 152. 
DEFINE VARIABLE resline LIKE bk-reser.veran-resnr INITIAL 1. 
DEFINE VARIABLE r-status LIKE bk-reser.resstatus INITIAL 1. 
*/ 
DEFINE buffer mres FOR bk-veran. 
DEFINE buffer rline FOR bk-reser. 
DEFINE buffer fsl FOR bk-func. 
 
FIND FIRST fsl WHERE fsl.veran-nr = resnr AND fsl.veran-seite = resline NO-LOCK NO-ERROR. 
IF AVAILABLE fsl THEN 
DO: 
  IF fsl.resstatus NE r-status THEN 
  DO: 
    IF r-status = 1 THEN 
    DO: 
      FIND CURRENT fsl EXCLUSIVE-LOCK. 
      fsl.resstatus = 1. 
      fsl.c-resstatus[1] = "F". 
      fsl.r-resstatus[1] = 1. 
      FIND CURRENT fsl NO-LOCK. 
    END. 
    ELSE IF r-status = 2 THEN 
    DO: 
      FIND CURRENT fsl EXCLUSIVE-LOCK. 
      fsl.resstatus = 2. 
      fsl.c-resstatus[1] = "T". 
      fsl.r-resstatus[1] = 2. 
      FIND CURRENT fsl NO-LOCK. 
    END. 
  END. 
END. 
FIND FIRST rline WHERE rline.veran-nr = resnr AND rline.veran-seite = resline NO-LOCK NO-ERROR. 
IF AVAILABLE rline THEN 
DO: 
  IF rline.resstatus NE r-status THEN 
  DO: 
    FIND CURRENT rline EXCLUSIVE-LOCK. 
    rline.resstatus = r-status. 
    FIND CURRENT rline NO-LOCK. 
  END. 
END. 
FIND FIRST rline WHERE rline.veran-nr = resnr AND rline.resstatus NE r-status NO-LOCK NO-ERROR. 
IF NOT AVAILABLE rline THEN 
DO: 
  FIND FIRST mres WHERE mres.veran-nr = resnr NO-LOCK NO-ERROR. 
  IF AVAILABLE mres THEN 
  DO: 
    FIND CURRENT mres EXCLUSIVE-LOCK. 
    mres.resstatus = r-status. 
    FIND CURRENT mres NO-LOCK. 
  END. 
END. 
 
