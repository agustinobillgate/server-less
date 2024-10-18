
DEFINE TEMP-TABLE cost-list 
  FIELD num    AS INTEGER FORMAT "9999" 
  FIELD name   AS CHAR   FORMAT "x(24)". 

DEF OUTPUT PARAMETER double-currency    AS LOGICAL. 
DEF OUTPUT PARAMETER price-decimal      AS INTEGER. 
DEF OUTPUT PARAMETER cost1              AS INTEGER. 
DEF OUTPUT PARAMETER cost2              AS INTEGER. 
DEF OUTPUT PARAMETER TABLE FOR cost-list.

FIND FIRST htparam WHERE paramnr = 240 NO-LOCK. 
double-currency = htparam.flogical. 
FIND FIRST htparam WHERE htparam.paramnr = 491 NO-LOCK. 
price-decimal = htparam.finteger. 
 
RUN create-costlist. 


PROCEDURE create-costlist: 
DEFINE VARIABLE i AS INTEGER. 
DEFINE VARIABLE m AS INTEGER INITIAL 1. 
DEFINE VARIABLE n AS INTEGER INITIAL 0. 

  FOR EACH cost-list:
      DELETE cost-list.
  END.

  FOR EACH parameters WHERE progname = "CostCenter" 
      AND section = "Name" AND varname GT "" NO-LOCK: 
      create cost-list. 
      cost-list.num = INTEGER(parameters.varname). 
      cost-list.name = parameters.vstring. 
      IF cost1 GT cost-list.num THEN cost1 = cost-list.num. 
      IF cost2 LT cost-list.num THEN cost2 = cost-list.num. 
  END. 
END. 
