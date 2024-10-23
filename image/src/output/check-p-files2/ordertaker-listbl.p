/*DEFINE TEMP-TABLE output-list 
  FIELD STR AS CHAR.*/ 

DEFINE TEMP-TABLE output-list 
  FIELD datum   AS DATE
  FIELD tischnr AS INTEGER
  FIELD rechnr  AS INTEGER
  FIELD artnr   AS INTEGER
  FIELD bezeich AS CHARACTER
  FIELD dept    AS INTEGER
  FIELD anzahl  AS INTEGER
  FIELD betrag  AS DECIMAL
  FIELD zeit    AS INTEGER
  FIELD kellnr1 AS INTEGER
  FIELD kellnr2 AS INTEGER
  . 

DEFINE TEMP-TABLE odtaker-list
    FIELD datum         AS DATE
    FIELD tableno       AS CHAR
    FIELD billno        AS INTEGER
    FIELD artno         AS INTEGER
    FIELD bezeich       AS CHAR
    FIELD qty           AS INTEGER
    FIELD amount        AS DECIMAL
    FIELD departement   AS CHARACTER
    FIELD zeit          AS CHAR
    FIELD id            AS CHAR
    FIELD tb            AS CHAR.

DEFINE INPUT PARAMETER usr-nr    AS INTEGER INITIAL 0. 
DEFINE INPUT PARAMETER from-date AS DATE LABEL "&From Date". 
DEFINE INPUT PARAMETER to-date   AS DATE LABEL "T&o Date". 

DEFINE OUTPUT PARAMETER TABLE FOR odtaker-list.

/*DEFINE VARIABLE long-digit AS LOGICAL INIT NO.*/ 

DEFINE VARIABLE long-digit AS LOGICAL. 
FIND FIRST htparam WHERE paramnr = 246 NO-LOCK. 
long-digit = htparam.flogical. 


RUN rest-odtakerlist-btn-gobl.p (from-date, to-date, usr-nr, long-digit, OUTPUT TABLE output-list).
 
FOR EACH odtaker-list:
    DELETE odtaker-list.
END.

/*FOR EACH output-list:
    CREATE odtaker-list.
    ASSIGN 
    datum       = DATE(substring(output-list.str,1,8)) 
    tableno     = substring(output-list.str,9,4) 
    billno      = int(substring(output-list.str,13,9)) 
    artno       = int(substring(output-list.str,22,5)) 
    bezeich     = substring(output-list.str,27,28) 
    qty         = int(substring(output-list.str,75,5)) 
    amount      = decimal(substring(output-list.str,80,17)) 
    departement = substring(output-list.str,55,20) 
    zeit        = substring(output-list.str,97,5) 
    id          = substring(output-list.str,102,3) 
    tb          = substring(output-list.str,105,3) 
    .
END.*/

FOR EACH output-list:
    CREATE odtaker-list.
    ASSIGN 
        odtaker-list.datum       = output-list.datum 
        odtaker-list.tableno     = STRING(output-list.tischnr, ">>>9") 
        odtaker-list.billno      = output-list.rechnr 
        odtaker-list.artno       = output-list.artnr 
        odtaker-list.bezeich     = output-list.bezeich 
        odtaker-list.qty         = output-list.anzahl 
        odtaker-list.amount      = output-list.betrag 
        odtaker-list.departement = STRING(output-list.dept, ">>>9") 
        odtaker-list.zeit        = STRING(output-list.zeit, "HH:MM") 
        odtaker-list.id          = STRING(output-list.kellnr1, ">9") 
        odtaker-list.tb          = STRING(output-list.kellnr2, ">9") 
        .
END.
