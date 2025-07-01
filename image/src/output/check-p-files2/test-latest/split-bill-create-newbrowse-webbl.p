/*FD Nov 03, 2020 => BL for vhp web based*/
/*Create new bill in visual transfer bill*/

DEFINE TEMP-TABLE bill1             LIKE bill  
    FIELD bl-recid AS INTEGER.
DEFINE TEMP-TABLE t-guest           LIKE guest.
DEFINE TEMP-TABLE t-htparam         LIKE htparam.

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
DEFINE INPUT PARAMETER newbill-recid    AS INTEGER.
DEFINE INPUT PARAMETER recid-array2     AS INTEGER.
DEFINE INPUT PARAMETER recid-array3     AS INTEGER.
DEFINE INPUT PARAMETER recid-array4     AS INTEGER.

DEFINE OUTPUT PARAMETER recid-array     AS INTEGER EXTENT 4.
DEFINE OUTPUT PARAMETER title-str2      AS CHARACTER.
DEFINE OUTPUT PARAMETER title-str3      AS CHARACTER.
DEFINE OUTPUT PARAMETER title-str4      AS CHARACTER.
DEFINE OUTPUT PARAMETER balance2        AS DECIMAL.
DEFINE OUTPUT PARAMETER balance3        AS DECIMAL.
DEFINE OUTPUT PARAMETER balance4        AS DECIMAL.
DEFINE OUTPUT PARAMETER bcol2           AS INTEGER INITIAL 2.
DEFINE OUTPUT PARAMETER bcol3           AS INTEGER INITIAL 2.
DEFINE OUTPUT PARAMETER bcol4           AS INTEGER INITIAL 2.
DEFINE OUTPUT PARAMETER TABLE FOR t-bline2. 
DEFINE OUTPUT PARAMETER TABLE FOR t-bline3.
DEFINE OUTPUT PARAMETER TABLE FOR t-bline4.

{SupertransBL.i}
DEFINE VARIABLE lvCAREA         AS CHAR INITIAL "split-bill-create-newbrowse-webbl".

DEFINE VARIABLE zinr LIKE zimmer.zinr.		/*MT 25/07/12 */
DEFINE VARIABLE ind AS INTEGER INITIAL 0.

IF recid-array2 EQ 0 THEN ind = 2.   
ELSE IF recid-array3 EQ 0 THEN ind = 3.   
ELSE IF recid-array4 EQ 0 THEN ind = 4.
IF ind NE 0 THEN   
DO:   
    recid-array[ind] = newbill-recid.   
    RUN read-bill1bl.p(5, newbill-recid, ?, ?, ?, ?, ?, ?, ?, ?, OUTPUT TABLE bill1).  
    FIND FIRST bill1 NO-LOCK.   
    DO:   
        zinr = bill1.zinr.   
        IF ind = 2 THEN   
        DO:   
            balance2 = bill1.saldo.   
            RUN saldo-color(bill1.gastnr, balance2, OUTPUT bcol2).   
            RUN read-bill-line1bl.p
                (3, pvILanguage, bill1.rechnr, ?, ?, ?, ?, ?, OUTPUT TABLE t-bline2).    
            title-str2 = translateExtended ("Folio Number : ",lvCAREA,"" )   
                        + STRING(bill1.rechnr) + " / "   
                        + bill1.name + " / "   
                        + translateExtended ("Room Number : ",lvCAREA,"")   
                        + zinr.      
        END.   
        ELSE IF ind = 3 THEN   
        DO:   
            balance3 = bill1.saldo.   
            RUN saldo-color(bill1.gastnr, balance3, OUTPUT bcol3).   
            RUN read-bill-line1bl.p
                (3, pvILanguage, bill1.rechnr, ?, ?, ?, ?, ?, OUTPUT TABLE t-bline3).        
            title-str3 = translateExtended ("Folio Number : ",lvCAREA,"")   
                        + STRING(bill1.rechnr) + " / "   
                        + bill1.name + " / "   
                        + translateExtended ("Room Number : ",lvCAREA,"")   
                        + zinr.    
        END.   
        ELSE IF ind = 4 THEN   
        DO:   
            balance4 = bill1.saldo.   
            RUN saldo-color(bill1.gastnr, balance4, OUTPUT bcol4).   
            RUN read-bill-line1bl.p
                (3, pvILanguage, bill1.rechnr, ?, ?, ?, ?, ?, OUTPUT TABLE t-bline4).     
            title-str4 = translateExtended ("Folio Number : ",lvCAREA,"")   
                        + STRING(bill1.rechnr) + " / "   
                        + bill1.name + " / "   
                        + translateExtended ("Room Number : ",lvCAREA,"")   
                        + zinr.       
        END.   
    END.   
END. 

/**************************** PROCEDURE ****************************/
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

