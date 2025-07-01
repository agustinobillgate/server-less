/*FD Oct 30, 2020 => BL for vhp web based*/

DEFINE TEMP-TABLE t-bill            LIKE bill.
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
DEFINE INPUT PARAMETER bil-recid        AS INTEGER.

DEFINE OUTPUT PARAMETER closed-bill     AS LOGICAL.
DEFINE OUTPUT PARAMETER bill-anzahl     AS INTEGER.
DEFINE OUTPUT PARAMETER title-str1      AS CHARACTER.
DEFINE OUTPUT PARAMETER title-str2      AS CHARACTER.
DEFINE OUTPUT PARAMETER title-str3      AS CHARACTER.
DEFINE OUTPUT PARAMETER title-str4      AS CHARACTER.
DEFINE OUTPUT PARAMETER recid-array     AS INTEGER EXTENT 4.
DEFINE OUTPUT PARAMETER balance1        AS DECIMAL.
DEFINE OUTPUT PARAMETER balance2        AS DECIMAL.
DEFINE OUTPUT PARAMETER balance3        AS DECIMAL.
DEFINE OUTPUT PARAMETER balance4        AS DECIMAL.
DEFINE OUTPUT PARAMETER bcol1           AS INTEGER INITIAL 2.
DEFINE OUTPUT PARAMETER bcol2           AS INTEGER INITIAL 2.
DEFINE OUTPUT PARAMETER bcol3           AS INTEGER INITIAL 2.
DEFINE OUTPUT PARAMETER bcol4           AS INTEGER INITIAL 2.
DEFINE OUTPUT PARAMETER TABLE FOR t-bill.
DEFINE OUTPUT PARAMETER TABLE FOR t-bline1.
DEFINE OUTPUT PARAMETER TABLE FOR t-bline2.
DEFINE OUTPUT PARAMETER TABLE FOR t-bline3.
DEFINE OUTPUT PARAMETER TABLE FOR t-bline4.
/* For testing
DEFINE VARIABLE pvILanguage      AS INTEGER INITIAL 1.
DEFINE VARIABLE bil-recid        AS INTEGER INITIAL 4642138.

DEFINE VARIABLE closed-bill     AS LOGICAL.
DEFINE VARIABLE bill-anzahl     AS INTEGER.
DEFINE VARIABLE title-str1      AS CHARACTER.
DEFINE VARIABLE title-str2      AS CHARACTER.
DEFINE VARIABLE title-str3      AS CHARACTER.
DEFINE VARIABLE title-str4      AS CHARACTER.
DEFINE VARIABLE recid-array     AS INTEGER EXTENT 4.
DEFINE VARIABLE balance1        AS DECIMAL.
DEFINE VARIABLE balance2        AS DECIMAL.
DEFINE VARIABLE balance3        AS DECIMAL.
DEFINE VARIABLE balance4        AS DECIMAL.
DEFINE VARIABLE bcol1           AS INTEGER INITIAL 2.
DEFINE VARIABLE bcol2           AS INTEGER INITIAL 2.
DEFINE VARIABLE bcol3           AS INTEGER INITIAL 2.
DEFINE VARIABLE bcol4           AS INTEGER INITIAL 2.
DEFINE VARIABLE b1-flag         AS LOGICAL INITIAL YES.
DEFINE VARIABLE b2-flag         AS LOGICAL INITIAL NO.
DEFINE VARIABLE b3-flag         AS LOGICAL INITIAL NO.
DEFINE VARIABLE b4-flag         AS LOGICAL INITIAL NO.
*/
{SupertransBL.i}
DEFINE VARIABLE lvCAREA         AS CHAR INITIAL "prepare-split-bill-webbl".


RUN read-billbl.p(16, bil-recid, ?, ?, ?, OUTPUT TABLE t-bill).  
FIND FIRST t-bill NO-ERROR.   
/* Rulita 021224 | Fixing serverless issue git 216 */
IF AVAILABLE t-bill THEN 
DO:
    
    closed-bill = (t-bill.flag = 1).   
    bill-anzahl = 0.   

    RUN read-bill1bl.p(2, ?, t-bill.resnr, t-bill.parent-nr, 0,  
                        t-bill.zinr, ?, ?, ?, ?, OUTPUT TABLE bill1).  

    FOR EACH bill1 NO-LOCK:   
        bill-anzahl = bill-anzahl + 1.   
    END.

    RUN create-browse.
END.
/* End Rulita */

/************************** PROCEDURE ************************/
PROCEDURE create-browse:   
    DEFINE VARIABLE i AS INTEGER INITIAL 1.   
    DEFINE VARIABLE j AS INTEGER INITIAL 2.   
    DEFINE VARIABLE billnr1 AS INTEGER.   
  
    RUN read-billbl.p(16, bil-recid, ?, ?, ?, OUTPUT TABLE t-bill).  
    FIND FIRST t-bill NO-ERROR.   
    billnr1 = t-bill.billnr.
    title-str1 = translateExtended ("Folio Number : ",lvCAREA,"") 
                + STRING(t-bill.rechnr) + " / " + t-bill.name + " / "
                + translateExtended ("Room Number : ",lvCAREA,"") 
                + t-bill.zinr.
      
    IF t-bill.rechnr NE 0 THEN   
    DO:  
        RUN read-bill-line1bl.p
            (3, pvILanguage, t-bill.rechnr, ?, ?, ?, ?, ?, OUTPUT TABLE t-bline1).            
    END.  
  
    recid-array[1] = bil-recid.   
    balance1 = t-bill.saldo.   
    RUN saldo-color(t-bill.gastnr, balance1, OUTPUT bcol1).   
  
    DO WHILE i LE bill-anzahl:   
        IF i NE billnr1 THEN   
        DO:   
            RUN read-bill1bl.p(12, i, t-bill.resnr, t-bill.parent-nr, 0, t-bill.zinr, 
                               ?, ?, ?, ?, OUTPUT TABLE bill1).  
            FIND FIRST bill1 NO-LOCK NO-ERROR.   
            IF AVAILABLE bill1 THEN   
            DO:   
                IF j = 2 THEN   
                DO:   
                    balance2 = bill1.saldo.  
                    RUN saldo-color(bill1.gastnr, balance2, OUTPUT bcol2).   
                    title-str2 = translateExtended ("Folio Number : ",lvCAREA,"")   
                                + STRING(bill1.rechnr) + " / " + bill1.name + " / " 
                                + translateExtended ("Room Number : ",lvCAREA,"")   
                                + bill1.zinr.    
  
                    RUN read-bill-line1bl.p
                        (3, pvILanguage, bill1.rechnr, ?, ?, ?, ?, ?, OUTPUT TABLE t-bline2).  
                END.   
                ELSE IF j = 3 THEN   
                DO:   
                    balance3 = bill1.saldo. 
                    RUN saldo-color(bill1.gastnr, balance3, OUTPUT bcol3).   
                    title-str3 = translateExtended ("Folio Number : ",lvCAREA,"")   
                                + STRING(bill1.rechnr) + " / " + bill1.name + " / " 
                                + translateExtended ("Room Number : ",lvCAREA,"")   
                                + bill1.zinr.                       
                      
                    RUN read-bill-line1bl.p
                        (3, pvILanguage, bill1.rechnr, ?, ?, ?, ?, ?, OUTPUT TABLE t-bline3).    
                END.   
                ELSE IF j = 4  THEN   
                DO:   
                    balance4 = bill1.saldo.   
                    RUN saldo-color(bill1.gastnr, balance4, OUTPUT bcol4).   
                    title-str4 = translateExtended ("Folio Number : ",lvCAREA,"")   
                                + STRING(bill1.rechnr) + " / " + bill1.name + " / " 
                                + translateExtended ("Room Number : ",lvCAREA,"")   
                                + bill1.zinr.                         
  
                    RUN read-bill-line1bl.p
                        (3, pvILanguage, bill1.rechnr, ?, ?, ?, ?, ?, OUTPUT TABLE t-bline4).                     
                END.   
                recid-array[j] = bill1.bl-recid.   
            END.   
            j = j + 1.   
        END.   
        i = i + 1.   
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
