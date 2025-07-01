

DEF OUTPUT PARAMETER ci-date AS DATE NO-UNDO. 

FIND FIRST htparam WHERE paramnr = 87 no-lock.  /*Invoicing DATE */ 
ci-date = htparam.fdate. 
 
