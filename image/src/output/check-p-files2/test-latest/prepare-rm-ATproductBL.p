
DEF TEMP-TABLE t-bediener LIKE bediener.

DEF OUTPUT PARAMETER ci-date        AS DATE.
DEF OUTPUT PARAMETER to-date        AS DATE.
DEF OUTPUT PARAMETER fdate          AS DATE.
DEF OUTPUT PARAMETER tdate          AS DATE.
DEF OUTPUT PARAMETER p-143          AS LOGICAL.
DEF OUTPUT PARAMETER TABLE FOR t-bediener.

RUN htpdate.p(87, OUTPUT ci-date).
ASSIGN
  to-date = ci-date - 1 
  fdate   = to-date
  tdate   = to-date
.

FIND FIRST htparam WHERE paramnr = 143 NO-LOCK. 
p-143 = htparam.flogical.

RUN create-sales-combo.


PROCEDURE create-sales-combo:
DEF VAR sales-grp AS INTEGER NO-UNDO.
  RUN htpint.p(547, OUTPUT sales-grp).
  
  FOR EACH bediener WHERE bediener.user-group = sales-grp NO-LOCK
      BY bediener.userinit:
      CREATE t-bediener.
      BUFFER-COPY bediener TO t-bediener.
  END.
END.

