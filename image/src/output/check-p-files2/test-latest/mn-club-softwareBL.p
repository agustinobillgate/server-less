  
  
  
FIND FIRST htparam WHERE htparam.paramnr = 1114 NO-LOCK.   
IF htparam.flogical THEN RUN clclosingbl.p.   
  
FIND FIRST htparam WHERE paramnr = 592 NO-LOCK.   
IF htparam.flogical THEN RETURN.   
DO TRANSACTION:   
  FIND CURRENT htparam EXCLUSIVE-LOCK.   
  htparam.flogical = YES.   
  FIND CURRENT htparam NO-LOCK.   
  FIND FIRST htparam WHERE paramnr = 592 EXCLUSIVE-LOCK.   
  htparam.fchar = "Midnight Program".   
  htparam.fdate = today.   
  htparam.finteger = time.   
  htparam.flogical = NO.   
  FIND CURRENT htparam NO-LOCK.   
END.   
