DEFINE TEMP-TABLE output-list 
  FIELD marked    AS CHAR FORMAT "x(1)" LABEL "M" 
  FIELD fibukonto AS CHAR 
  FIELD jnr       AS INTEGER INITIAL 0 
  FIELD bemerk    AS CHAR
  FIELD str       AS CHAR. 

DEFINE TEMP-TABLE t-ouput-list
      FIELD marked    AS CHAR FORMAT "x(1)" LABEL "M" 
      FIELD fibukonto AS CHAR 
      FIELD jnr       AS INTEGER INITIAL 0 
      FIELD bemerk    AS CHAR FORMAT "x(50)"
      FIELD datum     AS CHAR
      FIELD refno     AS CHAR FORMAT "x(15)"
      FIELD bezeich   AS CHAR FORMAT "x(40)"
      FIELD debit     AS CHAR FORMAT "->>,>>>,>>>,>>>,>>9.99"
      FIELD credit    AS CHAR FORMAT "->>,>>>,>>>,>>>,>>9.99" 
      FIELD user-init AS CHAR FORMAT "x(3)"
      FIELD created   AS CHAR
      FIELD chgid     AS CHAR FORMAT "x(3)"
      FIELD chgdate   AS CHAR  
      FIELD balance   AS CHAR FORMAT "->>,>>>,>>>,>>>,>>9.99" 
 .


DEF INPUT  PARAMETER sorttype   AS INTEGER.
DEF INPUT  PARAMETER from-fibu  AS CHAR.
DEF INPUT  PARAMETER to-fibu    AS CHAR.
DEF INPUT  PARAMETER from-dept  AS INTEGER.
DEF INPUT  PARAMETER from-date  AS DATE.
DEF INPUT  PARAMETER to-date    AS DATE.
DEF INPUT  PARAMETER close-year AS DATE.
DEF OUTPUT PARAMETER TABLE FOR t-ouput-list.

DEFINE VARIABLE curr-date AS DATE NO-UNDO.
DEFINE VARIABLE scurr-date AS CHAR NO-UNDO.



RUN gl-jouhislist-create-listbl.p (sorttype, from-fibu, to-fibu, from-dept, from-date, to-date,
                 close-year, OUTPUT TABLE output-list).


FOR EACH output-list :
       
    ASSIGN curr-date = DATE(INTEGER(ENTRY(2, SUBSTR(output-list.str, 111, 8), "/")),
                            INTEGER(ENTRY(1, SUBSTR(output-list.str, 111, 8), "/")),
                            INTEGER(ENTRY(3, SUBSTR(output-list.str, 111, 8), "/")))
           scurr-date = STRING(curr-date, "99/99/9999").

    CREATE t-ouput-list.
    ASSIGN 
       t-ouput-list.marked      = output-list.marked
       t-ouput-list.fibukonto   = output-list.fibukonto
       t-ouput-list.jnr         = output-list.jnr
       t-ouput-list.bemerk      = output-list.bemerk
       t-ouput-list.datum       = SUBSTR(output-list.str, 1, 8)
       t-ouput-list.refno       = SUBSTR(output-list.str, 9, 15)
       t-ouput-list.bezeich     = SUBSTR(output-list.str, 24, 40)
       t-ouput-list.debit       = SUBSTR(output-list.str, 64, 22)
       t-ouput-list.credit      = SUBSTR(output-list.str, 86, 22)
       t-ouput-list.balance     = SUBSTR(output-list.str, 180,22)
       t-ouput-list.user-init   = SUBSTR(output-list.str, 108, 3)
       t-ouput-list.created     = scurr-date
       t-ouput-list.chgid       = SUBSTR(output-list.str, 119, 3)
       t-ouput-list.chgdate     = SUBSTR(output-list.str, 122,8)
    .           
END.
