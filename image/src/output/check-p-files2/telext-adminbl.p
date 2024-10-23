DEFINE TEMP-TABLE cost-list 
  FIELD num    AS INTEGER FORMAT "9999" 
  FIELD name   AS CHAR   FORMAT "x(24)". 

DEFINE TEMP-TABLE t-nebenst     LIKE nebenst
    FIELD n-id AS INT.

DEF INPUT PARAMETER sorttype AS INT.
DEF OUTPUT PARAMETER TABLE FOR t-nebenst.
DEF OUTPUT PARAMETER TABLE FOR cost-list.

RUN disp-it.
RUN create-costlist.

PROCEDURE disp-it: 
  IF sorttype = 1 THEN 
  FOR EACH nebenst NO-LOCK BY nebenst.departement 
    BY nebenst.nebenstelle:
      RUN assign-it.
  END.
  ELSE 
  FOR EACH nebenst NO-LOCK BY nebenst.nebenstelle:
      RUN assign-it.
  END.
END. 

PROCEDURE assign-it:
    CREATE t-nebenst.
    BUFFER-COPY nebenst TO t-nebenst.
    ASSIGN t-nebenst.n-id = RECID(nebenst).
END.

PROCEDURE create-costlist: 
DEFINE VARIABLE i AS INTEGER. 
DEFINE VARIABLE m AS INTEGER INITIAL 1. 
DEFINE VARIABLE n AS INTEGER INITIAL 0. 
  FOR EACH parameters WHERE progname = "CostCenter" 
    AND section = "Name" AND varname GT "" NO-LOCK: 
    create cost-list. 
    cost-list.num = INTEGER(parameters.varname). 
    cost-list.name = parameters.vstring. 
  END. 
END. 
 
