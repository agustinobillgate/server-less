/**********  DEFINE TEMP TABLE **********/ 
DEFINE TEMP-TABLE rcode-list 
  FIELD code    AS INTEGER LABEL "No" 
  FIELD name    AS CHAR FORMAT "x(10)" LABEL "Code"
  .

 
DEFINE OUTPUT PARAMETER TABLE FOR rcode-list.

/**********  MAIN LOGIC  **********/ 
FOR EACH queasy WHERE queasy.KEY EQ 287 
  /*AND segment.vip-level = 0 AND NUM-ENTRIES(segment.bezeich, "$$0") = 1*/
  NO-LOCK BY queasy.number1: 
  CREATE rcode-list. 
  ASSIGN
    rcode-list.code   = queasy.number1
    rcode-list.name   = queasy.char1
  . 
END. 
