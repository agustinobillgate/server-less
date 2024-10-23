DEFINE TEMP-TABLE cost-list 
  FIELD rec-id AS INTEGER 
  FIELD num    AS INTEGER FORMAT "9999" 
  FIELD name   AS CHAR   FORMAT "x(24)". 

DEF INPUT PARAMETER num1 AS INT.
DEF INPUT PARAMETER name1 AS CHAR.
DEF OUTPUT PARAMETER TABLE FOR cost-list.

RUN add-costlist.

PROCEDURE add-costlist: 
DEFINE VARIABLE i AS INTEGER. 
DEFINE VARIABLE m AS INTEGER INITIAL 1. 
DEFINE VARIABLE n AS INTEGER INITIAL 0. 
  create parameters. 
  parameters.progname = "CostCenter". 
  parameters.section = "Name". 
  parameters.varname = STRING(num1). 
  parameters.vtype = 1. 
  parameters.vstring = name1.

  create cost-list. 
  cost-list.rec-id = RECID(parameters). 
  cost-list.num  = INTEGER(parameters.varname). 
  cost-list.name = parameters.vstring.
END. 
