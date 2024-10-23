DEFINE TEMP-TABLE l-list LIKE l-lager.

DEF INPUT PARAMETER case-type AS INT.
DEF INPUT PARAMETER TABLE FOR l-list.

FIND FIRST l-list.
IF case-type = 1 THEN   /**add**/
DO:
    create l-lager.
    RUN fill-new-l-lager.
END.
ELSE IF case-type = 2 THEN /**chg**/
DO:
    FIND FIRST l-lager WHERE l-lager.lager-nr = l-list.lager-nr EXCLUSIVE-LOCK.
    l-lager.bezeich = l-list.bezeich. 
    l-lager.betriebsnr = l-list.betriebsnr.
    FIND CURRENT l-lager NO-LOCK.
END.

PROCEDURE fill-new-l-lager: 
  l-lager.lager-nr = l-list.lager-nr. 
  l-lager.bezeich = l-list.bezeich. 
  l-lager.betriebsnr = l-list.betriebsnr. 
END. 

