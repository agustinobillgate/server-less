DEFINE TEMP-TABLE cost-list 
  FIELD nr AS INTEGER 
  FIELD bezeich AS CHAR FORMAT "x(24)". 

DEFINE TEMP-TABLE t-bediener
    FIELD userinit      LIKE bediener.userinit
    FIELD username      LIKE bediener.username
    FIELD nr            LIKE bediener.nr
    FIELD permissions   LIKE bediener.permissions.

DEF OUTPUT PARAMETER enforce-rflag  AS LOGICAL.
DEF OUTPUT PARAMETER billdate       AS DATE.
DEF OUTPUT PARAMETER TABLE FOR t-bediener.
DEF OUTPUT PARAMETER TABLE FOR cost-list.

FIND FIRST htparam WHERE paramnr = 222 NO-LOCK.
enforce-rflag = flogical.


FIND FIRST htparam WHERE paramnr = 110 NO-LOCK.
billdate = htparam.fdate.

RUN create-costlist.

FOR EACH bediener:
    CREATE t-bediener.
    ASSIGN
    t-bediener.userinit      = bediener.userinit
    t-bediener.username      = bediener.username
    t-bediener.nr            = bediener.nr
    t-bediener.permissions   = bediener.permissions.
END.

PROCEDURE create-costlist: 
DEFINE VARIABLE i AS INTEGER. 
DEFINE VARIABLE m AS INTEGER INITIAL 1. 
DEFINE VARIABLE n AS INTEGER INITIAL 0. 
  FOR EACH parameters WHERE progname = "CostCenter" 
    AND section = "Name" AND varname GT "" NO-LOCK: 
    create cost-list. 
    cost-list.nr = INTEGER(parameters.varname). 
    cost-list.bezeich = parameters.vstring. 
  END. 
END. 

