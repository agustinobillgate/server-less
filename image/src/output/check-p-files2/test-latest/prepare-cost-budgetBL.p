DEFINE TEMP-TABLE alloc-list 
  FIELD rec-id AS INTEGER 
  FIELD name AS CHAR 
  FIELD bezeich AS CHAR FORMAT "x(36)" 
  FIELD fibu  LIKE gl-acct.fibukonto LABEL "Account Number". 

DEFINE TEMP-TABLE cost-list 
  FIELD rec-id AS INTEGER 
  FIELD num    AS INTEGER FORMAT "9999" 
  FIELD name   AS CHAR   FORMAT "x(24)". 

DEF OUTPUT PARAMETER TABLE FOR alloc-list.
DEF OUTPUT PARAMETER TABLE FOR cost-list.

RUN create-costlist. 
RUN create-alloclist. 


PROCEDURE create-costlist: 
DEFINE VARIABLE i AS INTEGER. 
DEFINE VARIABLE m AS INTEGER INITIAL 1. 
DEFINE VARIABLE n AS INTEGER INITIAL 0. 
  FOR EACH parameters WHERE progname = "CostCenter" 
    AND section = "Name" AND varname GT "" NO-LOCK: 
    create cost-list. 
    cost-list.rec-id = RECID(parameters). 
    cost-list.num = INTEGER(parameters.varname). 
    cost-list.name = parameters.vstring. 
  END. 
END. 
 
PROCEDURE create-alloclist: 
DEFINE VARIABLE i AS INTEGER. 
DEFINE VARIABLE m AS INTEGER INITIAL 1. 
DEFINE VARIABLE n AS INTEGER INITIAL 0. 
  FOR EACH parameters WHERE progname = "CostCenter" 
    AND section = "Alloc" AND varname GT "" NO-LOCK: 
    FIND FIRST gl-acct WHERE gl-acct.fibukonto = parameters.vstring 
      NO-LOCK NO-ERROR. 
    IF AVAILABLE gl-acct THEN 
    DO: 
      create alloc-list. 
      alloc-list.rec-id = RECID(parameters). 
      alloc-list.name = parameters.varname. 
      alloc-list.fibu = parameters.vstring. 
      alloc-list.bezeich = gl-acct.bezeich. 
    END. 
  END. 
END. 
