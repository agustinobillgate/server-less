
DEF TEMP-TABLE t-nightaudit
    FIELD bezeichnung   LIKE nightaudit.bezeichnung
    FIELD hogarest      LIKE nightaudit.hogarest
    FIELD reihenfolge   LIKE nightaudit.reihenfolge
    FIELD programm      LIKE nightaudit.programm
    FIELD abschlussart  LIKE nightaudit.abschlussart.

 
DEF INPUT PARAMETER case-type AS INT.
DEF INPUT PARAMETER user-init AS CHAR.
DEF INPUT PARAMETER htparam-recid AS INTEGER.
DEF OUTPUT PARAMETER mnstart-flag AS LOGICAL INIT NO NO-UNDO.
DEF OUTPUT PARAMETER store-flag AS LOGICAL INIT NO NO-UNDO.
DEF OUTPUT PARAMETER printer-nr AS INT INIT 0.
DEF OUTPUT PARAMETER TABLE FOR t-nightaudit.
DEF OUTPUT PARAMETER na-date        AS DATE.
DEF OUTPUT PARAMETER na-time        AS INTEGER.
DEF OUTPUT PARAMETER na-name        AS CHAR.


DEF VAR ci-date AS DATE.

FIND FIRST bediener WHERE bediener.userinit = user-init NO-LOCK.
FIND FIRST htparam WHERE paramnr = 230 NO-LOCK. 
IF htparam.feldtyp = 4 AND htparam.flogical THEN store-flag = YES.

IF case-type = 1 THEN
DO:
    DO TRANSACTION:
      FIND FIRST htparam WHERE RECID(htparam) = htparam-recid EXCLUSIVE-LOCK.
      htparam.flogical = YES.
      RUN check-mn-start.
      IF mnstart-flag THEN RETURN NO-APPLY.
      RUN na-prog.
    END. 
END.
IF case-type = 2 THEN
DO:
      RUN na-prog.
END.
IF case-type = 3 THEN
DO:
    DO TRANSACTION:
        FIND FIRST htparam WHERE paramnr = 253 EXCLUSIVE-LOCK.
        htparam.fchar = bediener.username.
        htparam.fdate = today.
        htparam.finteger = time.
        htparam.flogical = NO.
        FIND CURRENT htparam NO-LOCK.
        FIND FIRST htparam WHERE paramnr = 102 EXCLUSIVE-LOCK.
        htparam.fdate = today.
        FIND CURRENT htparam NO-LOCK. 
        FIND FIRST htparam WHERE paramnr = 103 EXCLUSIVE-LOCK. 
        htparam.finteger = time. 
        FIND CURRENT htparam NO-LOCK. 
    END.
    FIND FIRST htparam WHERE htparam.paramnr = 99 NO-LOCK. 
    printer-nr = htparam.finteger. 

    FIND FIRST htparam WHERE paramnr = 102 NO-LOCK. 
    na-date = htparam.fdate. 
    FIND FIRST htparam WHERE paramnr = 103 NO-LOCK. 
    na-time = htparam.finteger. 
    FIND FIRST htparam WHERE paramnr = 253 NO-LOCK. 
    na-name = htparam.fchar.
END.




PROCEDURE na-prog: 
DEFINE VARIABLE night-type AS INTEGER NO-UNDO.
DEFINE VARIABLE mn-stopped AS LOGICAL NO-UNDO.

  FIND FIRST htparam WHERE paramnr = 87 NO-LOCK. 
  ci-date = htparam.fdate.

  FOR EACH nightaudit WHERE nightaudit.selektion NO-LOCK 
      BY (1 - nightaudit.hogarest) BY nightaudit.reihenfolge:
      CREATE t-nightaudit.
      ASSIGN
        t-nightaudit.bezeichnung    = nightaudit.bezeichnung
        t-nightaudit.hogarest       = nightaudit.hogarest
        t-nightaudit.reihenfolge    = nightaudit.reihenfolge
        t-nightaudit.programm       = nightaudit.programm
        t-nightaudit.abschlussart   = nightaudit.abschlussart.
  END.
END. 


PROCEDURE check-mn-start:
    FIND FIRST htparam WHERE paramnr = 105 no-lock.   /* ci-date */ 
    IF htparam.fdate LT today THEN /* RUN midnight program IF NOT yet started */ 
        mnstart-flag = YES.
END.
