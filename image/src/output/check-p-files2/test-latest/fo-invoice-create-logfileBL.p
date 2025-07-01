
DEFINE INPUT PARAMETER resno        AS INTEGER NO-UNDO. 
DEFINE INPUT PARAMETER reslinno     AS INTEGER NO-UNDO. 
DEFINE INPUT PARAMETER rmno         AS CHAR NO-UNDO. 
DEFINE INPUT PARAMETER user-init    AS CHAR NO-UNDO. 

DEFINE BUFFER resline FOR res-line. 
DEFINE BUFFER guest1 FOR guest. 

FIND FIRST resline WHERE resline.resnr = resno 
  AND resline.reslinnr = reslinno NO-LOCK.

CREATE reslin-queasy.
ASSIGN
  reslin-queasy.key = "ResChanges"
  reslin-queasy.resnr = resline.resnr 
  reslin-queasy.reslinnr = resline.reslinnr 
  reslin-queasy.date2 = TODAY 
  reslin-queasy.number2 = TIME
.

reslin-queasy.char3 = STRING(resline.ankunft) + ";"
                      + STRING(resline.ankunft) + ";" 
                      + STRING(resline.abreise) + ";" 
                      + STRING(resline.abreise) + ";" 
                      + STRING(resline.zimmeranz) + ";" 
                      + STRING(resline.zimmeranz) + ";" 
                      + STRING(resline.erwachs) + ";" 
                      + STRING(resline.erwachs) + ";" 
                      + STRING(resline.kind1) + ";" 
                      + STRING(resline.kind1) + ";" 
                      + STRING(resline.gratis) + ";" 
                      + STRING(resline.gratis) + ";" 
                      + STRING(resline.zikatnr) + ";" 
                      + STRING(resline.zikatnr) + ";" 
                      + STRING(resline.zinr) + ";" 
                      + STRING(resline.zinr) + ";" 
                      + STRING(resline.arrangement) + ";" 
                      + STRING(resline.arrangement) + ";" 
                      + STRING(resline.zipreis) + ";" 
                      + STRING(resline.zipreis) + ";".

IF rmno NE "" THEN 
reslin-queasy.char3 = reslin-queasy.char3 
                      + STRING(user-init) + ";" 
                      + STRING(user-init) + ";" 
                      + STRING(TODAY) + ";" 
                      + STRING(TODAY) + ";" 
                      + STRING(resline.NAME) + ";" 
                      + STRING("Transf to " + rmno) + ";". 
ELSE 
reslin-queasy.char3 = reslin-queasy.char3 
                      + STRING(user-init) + ";" 
                      + STRING(user-init) + ";" 
                      + STRING(TODAY) + ";" 
                      + STRING(TODAY) + ";" 
                      + STRING(resline.NAME) + ";" 
                      + STRING("UNDO Transfer") + ";". 

IF resline.was-status = 0 THEN 
  reslin-queasy.char3 = reslin-queasy.char3 + STRING(" NO") + ";" 
  + STRING(" NO") + ";". 
ELSE reslin-queasy.char3 = reslin-queasy.char3 + STRING("YES") + ";" 
  + STRING("YES") + ";". 

FIND CURRENT reslin-queasy NO-LOCK.
RELEASE reslin-queasy. 
