/*FD Nov 03, 2020 => BL for vhp web based*/
/* This PROCEDURE update a BROWSE */

DEFINE TEMP-TABLE spbill-list
    FIELD selected AS LOGICAL INITIAL YES 
    FIELD bl-recid AS INTEGER
. 

DEFINE TEMP-TABLE bill1             LIKE bill  
    FIELD bl-recid AS INTEGER.

DEFINE TEMP-TABLE t-guest           LIKE guest.
DEFINE TEMP-TABLE t-htparam         LIKE htparam.

DEFINE TEMP-TABLE t-bline1          LIKE bill-line
    FIELD bl-recid  AS INTEGER  
    FIELD artart    AS INTEGER  
    FIELD tool-tip  AS CHAR
.
DEFINE TEMP-TABLE t-bline2          LIKE bill-line
    FIELD bl-recid  AS INTEGER  
    FIELD artart    AS INTEGER  
    FIELD tool-tip  AS CHAR
.
DEFINE TEMP-TABLE t-bline3          LIKE bill-line
    FIELD bl-recid  AS INTEGER  
    FIELD artart    AS INTEGER  
    FIELD tool-tip  AS CHAR
.
DEFINE TEMP-TABLE t-bline4          LIKE bill-line
    FIELD bl-recid  AS INTEGER  
    FIELD artart    AS INTEGER  
    FIELD tool-tip  AS CHAR
.

DEFINE INPUT PARAMETER pvILanguage      AS INTEGER.
DEFINE INPUT PARAMETER j                AS INTEGER.
DEFINE INPUT PARAMETER recid-array      AS INTEGER EXTENT 4.

DEFINE OUTPUT PARAMETER balance1        AS DECIMAL.
DEFINE OUTPUT PARAMETER balance2        AS DECIMAL.
DEFINE OUTPUT PARAMETER balance3        AS DECIMAL.
DEFINE OUTPUT PARAMETER balance4        AS DECIMAL.
DEFINE OUTPUT PARAMETER bcol1           AS INTEGER INITIAL 2.
DEFINE OUTPUT PARAMETER bcol2           AS INTEGER INITIAL 2.
DEFINE OUTPUT PARAMETER bcol3           AS INTEGER INITIAL 2.
DEFINE OUTPUT PARAMETER bcol4           AS INTEGER INITIAL 2.
DEFINE OUTPUT PARAMETER TABLE FOR t-bline1.
DEFINE OUTPUT PARAMETER TABLE FOR t-bline2.
DEFINE OUTPUT PARAMETER TABLE FOR t-bline3.
DEFINE OUTPUT PARAMETER TABLE FOR t-bline4.

{SupertransBL.i}
DEFINE VARIABLE lvCAREA     AS CHAR INITIAL "split-bill-update-billine-webbl".

RUN update-browse (j).       

/****************************** PROCEDURE ****************************/
PROCEDURE update-browse:   
    DEFINE INPUT PARAMETER j AS INTEGER.   

    IF (recid-array[j] NE 0) THEN   
    DO:           
        RUN read-bill1bl.p(5, recid-array[j], ?, ?, ?, ?, ?, ?, ?, ?, OUTPUT TABLE bill1).  
        FIND FIRST bill1 NO-LOCK.   
        IF j = 1 AND bill1.rechnr NE 0 THEN   
        DO:   
            RUN read-bill-line1bl.p
                (3, pvILanguage, bill1.rechnr, ?, ?, ?, ?, ?, OUTPUT TABLE t-bline1).   
            balance1 = bill1.saldo.   
            RUN saldo-color(bill1.gastnr, balance1, OUTPUT bcol1).  
        END.   
        ELSE IF j = 2 AND bill1.rechnr NE 0 THEN   
        DO:   
            RUN read-bill-line1bl.p
                (3, pvILanguage, bill1.rechnr, ?, ?, ?, ?, ?, OUTPUT TABLE t-bline2).    
            balance2 = bill1.saldo.   
            RUN saldo-color(bill1.gastnr, balance2, OUTPUT bcol2).   
        END.   
        ELSE IF j = 3 AND bill1.rechnr NE 0 THEN   
        DO:   
            RUN read-bill-line1bl.p
                (3, pvILanguage, bill1.rechnr, ?, ?, ?, ?, ?, OUTPUT TABLE t-bline3).    
            balance3 = bill1.saldo.   
            RUN saldo-color(bill1.gastnr, balance3, OUTPUT bcol3).   
        END.   
        ELSE IF j = 4 AND bill1.rechnr NE 0 THEN   
        DO:   
            RUN read-bill-line1bl.p
                (3, pvILanguage, bill1.rechnr, ?, ?, ?, ?, ?, OUTPUT TABLE t-bline4).    
            balance4 = bill1.saldo.   
            RUN saldo-color(bill1.gastnr, balance4, OUTPUT bcol4).     
        END.   
    END.   
END.

PROCEDURE saldo-color:   
    DEFINE INPUT PARAMETER gastnr AS INTEGER.   
    DEFINE INPUT PARAMETER saldo AS DECIMAL.   
    DEFINE OUTPUT PARAMETER bg-col AS INTEGER.   
    DEFINE VARIABLE kreditlimit AS DECIMAL.   
  
    RUN read-guestbl.p(1, gastnr, ?, ?, OUTPUT TABLE t-guest).  
    FIND FIRST t-guest NO-LOCK.   
    kreditlimit = t-guest.kreditlimit.   
    IF kreditlimit EQ 0 THEN   
    DO:   
        RUN read-htparambl.p(1, 68, ?, OUTPUT TABLE t-htparam).  
        FIND FIRST t-htparam NO-LOCK.   
        IF t-htparam.fdecimal NE 0 THEN kreditlimit = t-htparam.fdecimal.   
        ELSE kreditlimit = t-htparam.finteger.   
    END.   
    IF saldo LE kreditlimit THEN bg-col = 2.   
    ELSE bg-col = 12.   
END. 
