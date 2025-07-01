 
/*************** Copy Fixed-rates AND argt-lines ***********************/ 
 
DEFINE INPUT PARAMETER resnr AS INTEGER. 
DEFINE INPUT PARAMETER reslinnr AS INTEGER. 


DEFINE buffer resmember FOR res-line. 
DEFINE buffer rqueasy FOR reslin-queasy. 
 
FIND FIRST res-line WHERE res-line.resnr = resnr 
  AND res-line.reslinnr = reslinnr NO-LOCK. 
FIND FIRST arrangement WHERE arrangement.arrangement = res-line.arrangement 
  NO-LOCK. 
 
FIND FIRST resmember WHERE resmember.resnr = resnr 
  AND resmember.reslinnr NE reslinnr AND res-line.active-flag NE 2 
  AND resmember.resstatus NE 12 AND resmember.resstatus NE 11 
  AND resmember.resstatus NE 13 
  AND resmember.arrangement = res-line.arrangement NO-LOCK NO-ERROR. 
DO WHILE AVAILABLE resmember: 
 
  FIND CURRENT resmember EXCLUSIVE-LOCK. 
  resmember.zipreis = res-line.zipreis. 
  resmember.betriebsnr = res-line.betriebsnr. 
  resmember.reserve-dec = res-line.reserve-dec. 
  FIND CURRENT resmember NO-LOCK. 
 
  FOR EACH rqueasy WHERE rqueasy.key = "fargt-line" 
    AND rqueasy.char1 = "" AND rqueasy.resnr = resnr 
    AND rqueasy.number2 =  arrangement.argtnr 
    AND rqueasy.reslinnr = resmember.reslinnr: 
    delete rqueasy. 
  END. 
  FOR EACH reslin-queasy WHERE reslin-queasy.key = "fargt-line" 
    AND reslin-queasy.char1 = "" AND reslin-queasy.resnr = resnr 
    AND reslin-queasy.number2 =  arrangement.argtnr 
    AND reslin-queasy.reslinnr = reslinnr NO-LOCK: 
    create rqueasy. 
    rqueasy.key = "fargt-line". 
    rqueasy.number1 = reslin-queasy.number1. 
    rqueasy.number2 = reslin-queasy.number2. 
    rqueasy.number3 = reslin-queasy.number3. 
    rqueasy.resnr = resnr. 
    rqueasy.reslinnr = resmember.reslinnr. 
    rqueasy.deci1 = reslin-queasy.deci1. 
    rqueasy.date1 = reslin-queasy.date1. 
    rqueasy.date2 = reslin-queasy.date2. 
    FIND CURRENT rqueasy NO-LOCK. 
  END. 
 
  FOR EACH rqueasy WHERE rqueasy.key = "arrangement" 
    AND rqueasy.resnr = resnr 
    AND rqueasy.reslinnr = resmember.reslinnr: 
    delete rqueasy. 
  END. 
  FOR EACH reslin-queasy WHERE key = "arrangement" 
    AND reslin-queasy.resnr = resnr 
    AND reslin-queasy.reslinnr = reslinnr NO-LOCK: 
    create rqueasy. 
    rqueasy.key = "arrangement". 
    rqueasy.resnr = resnr. 
    rqueasy.reslinnr = resmember.reslinnr. 
    rqueasy.deci1 = reslin-queasy.deci1. 
    rqueasy.date1 = reslin-queasy.date1. 
    rqueasy.date2 = reslin-queasy.date2. 
    rqueasy.char1 = reslin-queasy.char1. 
    rqueasy.number3 = reslin-queasy.number3. 
    FIND CURRENT rqueasy NO-LOCK. 
  END. 
  FIND NEXT resmember WHERE resmember.resnr = resnr 
    AND resmember.reslinnr NE reslinnr AND res-line.active-flag NE 2 
    AND resmember.resstatus NE 12 AND resmember.resstatus NE 11 
    AND resmember.resstatus NE 13 
    AND resmember.arrangement = res-line.arrangement NO-LOCK NO-ERROR. 
END. 
 
