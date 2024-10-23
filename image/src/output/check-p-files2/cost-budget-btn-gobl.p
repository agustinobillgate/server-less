DEFINE TEMP-TABLE alloc-list 
  FIELD rec-id AS INTEGER 
  FIELD name AS CHAR 
  FIELD bezeich AS CHAR FORMAT "x(36)" 
  FIELD fibu  LIKE gl-acct.fibukonto LABEL "Account Number". 

DEF INPUT PARAMETER fibu1 AS CHAR.
DEF INPUT PARAMETER curr-select AS CHAR.
DEF INPUT PARAMETER cost-list-num AS INT.
DEF OUTPUT PARAMETER flag AS INT INIT 0.
DEF OUTPUT PARAMETER TABLE FOR alloc-list.

DEFINE VARIABLE bezeich1 AS CHAR.

FIND FIRST gl-acct WHERE gl-acct.fibukonto = fibu1 NO-LOCK NO-ERROR. 
IF NOT AVAILABLE gl-acct THEN 
DO:
  flag = 1.
  RETURN NO-APPLY. 
END. 

IF curr-select = "add-alloc" THEN 
DO: 
  bezeich1 = gl-acct.bezeich. 
  RUN add-alloclist. 
  flag = 2.
  /*MTbezeich1 = "". 
  fibu1 = "000000000000000".
  DISP fibu1 WITH FRAME frame1. 
  APPLY "entry" TO fibu1.*/
  RETURN NO-APPLY. 
END. 
IF curr-select = "chg-alloc" THEN 
DO: 
  RUN update-alloclist.
  flag = 3.
  /*MThide fibu1. 
  DISABLE btn-help btn-go WITH FRAME frame1. 
  APPLY "entry" TO b1.*/
END. 


PROCEDURE add-alloclist: 
  create parameters. 
  parameters.progname = "CostCenter". 
  parameters.section = "Alloc". 
  parameters.varname = STRING(cost-list-num). 
  parameters.vtype = 1. 
  parameters.vstring = fibu1. 
  create alloc-list. 
  alloc-list.rec-id = RECID(parameters). 
  alloc-list.name = STRING(cost-list-num). 
  alloc-list.bezeich = bezeich1. 
  alloc-list.fibu = fibu1. 
  /*MTlast-name = "". 
  RUN open-query2.*/
END. 


PROCEDURE update-alloclist: 
  FIND FIRST parameters WHERE RECID(parameters) = alloc-list.rec-id 
    EXCLUSIVE-LOCK. 
  parameters.vstring = fibu1. 
  FIND CURRENT parameters NO-LOCK. 
  /*MTb2:REFRESH() IN FRAME frame1. 
  bezeich1 = "". 
  fibu1 = "000000000000000".*/
END. 
