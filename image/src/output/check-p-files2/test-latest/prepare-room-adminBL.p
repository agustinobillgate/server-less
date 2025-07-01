DEF TEMP-TABLE t-zimmer LIKE zimmer.  
  
DEF OUTPUT PARAMETER zikatnr AS INT.  
DEF OUTPUT PARAMETER rmcatbez AS CHAR.  
DEF OUTPUT PARAMETER room-limit AS INT.  
DEF OUTPUT PARAMETER curr-anz AS INT.  
DEF OUTPUT PARAMETER ci-date AS DATE.  
DEF OUTPUT PARAMETER TABLE FOR t-zimmer.  
  
RUN check-rm-limitbl.p(OUTPUT room-limit, OUTPUT curr-anz).   
  
FIND FIRST htparam WHERE paramnr = 87 NO-LOCK.   
ci-date = htparam.fdate.  
  
FIND FIRST zimkateg NO-LOCK.  
zikatnr = zimkateg.zikatnr.  
rmcatbez = zimkateg.kurzbez.  
  
FOR EACH zimmer /*WHERE zimmer.zikatnr = zikatnr*/ NO-LOCK BY zimmer.zinr:  
    CREATE t-zimmer.  
    BUFFER-COPY zimmer TO t-zimmer.  
END.  
  
  
