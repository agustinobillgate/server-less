/* Delete OR cancel Reservation Line Records */   
   
DEFINE INPUT  PARAMETER pvILanguage  AS INTEGER NO-UNDO.  
DEFINE INPUT  PARAMETER res-mode   AS char.    /* "delete" OR "cancel" */   
DEFINE INPUT  PARAMETER resnr      AS INTEGER.   
DEFINE INPUT  PARAMETER user-init  AS CHAR.   
DEFINE INPUT  PARAMETER cancel-str AS CHAR.  
DEFINE OUTPUT PARAMETER msg-str    AS CHAR.  
  
DEFINE VARIABLE del-mainres AS LOGICAL     NO-UNDO.  
  
DEF BUFFER rline FOR res-line.  
  
{ supertransbl.i }  
DEF VAR lvCAREA AS CHAR INITIAL "del-reserve".   
/**********  MAIN LOGIC  **********/   
   
FIND FIRST bediener WHERE bediener.userinit = user-init NO-LOCK.   
  
FIND FIRST htparam WHERE htparam.paramnr = 87 NO-LOCK.  
  
IF res-mode = "cancel" OR res-mode = "delete" THEN   
DO TRANSACTION:   
   
  FIND FIRST res-line WHERE res-line.resnr = resnr   
    AND res-line.active-flag = 0   
    AND res-line.l-zuordnung[3] = 0 NO-LOCK NO-ERROR.   
  DO WHILE AVAILABLE res-line:   
    RUN del-reslinebl.p(pvILanguage, res-mode, res-line.resnr,  
                        res-line.reslinnr,user-init, cancel-str,  
                        OUTPUT del-mainres, OUTPUT msg-str).  
    FIND NEXT res-line WHERE res-line.resnr = resnr   
      AND res-line.active-flag = 0  
      AND res-line.l-zuordnung[3] = 0 NO-LOCK NO-ERROR.   
  END.  
END.   
