 
DEFINE INPUT PARAMETER resnr LIKE bk-reser.veran-nr. 
DEFINE INPUT PARAMETER resline LIKE bk-reser.veran-resnr. 
 
DEFINE buffer mres FOR bk-veran. 
DEFINE buffer rline FOR bk-reser. 
DEFINE buffer fsl FOR bk-func. 
 
FIND FIRST rline WHERE rline.veran-nr = resnr AND rline.veran-resnr = resline 
  NO-LOCK NO-ERROR. 
IF AVAILABLE rline THEN 
DO: 
  FIND CURRENT rline EXCLUSIVE-LOCK. 
  rline.resstatus = 9. 
  FIND CURRENT rline NO-LOCK. 
END. 
 
FIND FIRST bk-func WHERE bk-func.veran-nr = resnr 
  AND bk-func.veran-seite = resline EXCLUSIVE-LOCK NO-ERROR. 
IF AVAILABLE bk-func THEN 
DO: 
  bk-func.resstatus = 9. 
  bk-func.r-resstatus[1] = 9. 
  bk-func.c-resstatus[1] = "C". 
  FIND CURRENT bk-func NO-LOCK. 
END. 
 
FIND FIRST rline WHERE rline.veran-nr = resnr 
  AND rline.resstatus LE 2 NO-LOCK NO-ERROR. 
IF NOT AVAILABLE rline THEN 
DO: 
  FIND FIRST mres WHERE mres.veran-nr = resnr NO-LOCK NO-ERROR. 
  IF AVAILABLE mres THEN 
  DO: 
    FIND CURRENT mres EXCLUSIVE-LOCK. 
    mres.activeflag = 1. 
    FIND CURRENT mres NO-LOCK. 
  END. 
END. 
 
