/*FD Nov 02, 0202 => BL for vhp web based*/
/* This PROCEDURE creates a BROWSE through btn-search */ 

DEFINE TEMP-TABLE t-bediener LIKE bediener. 

DEFINE TEMP-TABLE bill1 LIKE bill  
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
DEFINE INPUT PARAMETER bill-type        AS INTEGER.
DEFINE INPUT PARAMETER bil-recid1       AS INTEGER.   
DEFINE INPUT PARAMETER ind              AS INTEGER.
DEFINE INPUT PARAMETER user-init        AS CHARACTER.
DEFINE INPUT PARAMETER tbill-resnr      AS INTEGER.
DEFINE INPUT PARAMETER tbill-reslinnr   AS INTEGER.
DEFINE INPUT PARAMETER tbill-zinr       AS CHARACTER.

DEFINE OUTPUT PARAMETER title-str2      AS CHARACTER.
DEFINE OUTPUT PARAMETER title-str3      AS CHARACTER.
DEFINE OUTPUT PARAMETER title-str4      AS CHARACTER.
DEFINE OUTPUT PARAMETER balance2        AS DECIMAL.
DEFINE OUTPUT PARAMETER balance3        AS DECIMAL.
DEFINE OUTPUT PARAMETER balance4        AS DECIMAL.
DEFINE OUTPUT PARAMETER bcol2           AS INTEGER INITIAL 2.
DEFINE OUTPUT PARAMETER bcol3           AS INTEGER INITIAL 2.
DEFINE OUTPUT PARAMETER bcol4           AS INTEGER INITIAL 2.
DEFINE OUTPUT PARAMETER msg-str         AS CHARACTER.
DEFINE OUTPUT PARAMETER TABLE FOR t-bline2. 
DEFINE OUTPUT PARAMETER TABLE FOR t-bline3.
DEFINE OUTPUT PARAMETER TABLE FOR t-bline4.

/* For Testing
DEFINE VARIABLE pvILanguage      AS INTEGER INIT 1.
DEFINE VARIABLE bill-type        AS INTEGER INIT 1.
DEFINE VARIABLE bil-recid1       AS INTEGER INIT 178344.   
DEFINE VARIABLE ind              AS INTEGER INIT 2.
DEFINE VARIABLE user-init        AS CHARACTER INIT "01".
DEFINE VARIABLE tbill-resnr      AS INTEGER INIT 28259.
DEFINE VARIABLE tbill-reslinnr   AS INTEGER INIT 1.
DEFINE VARIABLE tbill-zinr       AS CHARACTER INIT "308".

DEFINE VARIABLE title-str2      AS CHARACTER.
DEFINE VARIABLE title-str3      AS CHARACTER.
DEFINE VARIABLE title-str4      AS CHARACTER.
DEFINE VARIABLE balance2        AS DECIMAL.
DEFINE VARIABLE balance3        AS DECIMAL.
DEFINE VARIABLE balance4        AS DECIMAL.
DEFINE VARIABLE bcol2           AS INTEGER INITIAL 2.
DEFINE VARIABLE bcol3           AS INTEGER INITIAL 2.
DEFINE VARIABLE bcol4           AS INTEGER INITIAL 2.
DEFINE VARIABLE msg-str         AS CHARACTER.
*/
{SupertransBL.i}
DEFINE VARIABLE lvCAREA         AS CHAR INITIAL "split-bill-create-browse1-webbl".

DEFINE VARIABLE zinr AS CHARACTER NO-UNDO.
DEFINE VARIABLE i AS INTEGER INITIAL 1 NO-UNDO.
DEFINE VARIABLE recid-array AS INTEGER EXTENT 4 NO-UNDO.
DEFINE VARIABLE zugriff AS LOGICAL NO-UNDO.

RUN read-bedienerbl.p(0, user-init, OUTPUT TABLE t-bediener).
FIND FIRST t-bediener NO-ERROR.

DO WHILE i LE 4:   
    IF bil-recid1 = recid-array[i] AND i NE ind THEN   
    DO:   
        msg-str = translateExtended ("This bill has been selected on the viewport ",lvCAREA,"") 
            + STRING(i) + CHR(10) + translateExtended ("Ignored the selection.",lvCAREA,"").
        RETURN.   
    END.   
    i = i + 1.   
END. 

IF bil-recid1 = 0 THEN RETURN.

RUN read-bill1bl.p(5, bil-recid1, ?, ?, ?, ?, ?, ?, ?, ?, OUTPUT TABLE bill1).
FIND FIRST bill1 NO-LOCK.   
IF tbill-resnr GT 0 THEN   
DO:  
    IF tbill-zinr NE "" AND bill1.resnr = tbill-resnr   
        AND (bill1.zinr = tbill-zinr OR bill1.reslinnr = 0) THEN .   
    ELSE IF tbill-zinr NE "" AND bill1.resnr = tbill-resnr   
        AND (bill1.zinr NE "" AND bill1.zinr NE tbill-zinr   
             AND SUBSTR(t-bediener.permission, 12, 1) GE "1") THEN .   
    ELSE IF tbill-reslinnr = 0 AND bill1.resnr = tbill-resnr   
        AND bill1.reslinnr > 0   
        AND SUBSTR(t-bediener.permission, 12, 1) GE "1" THEN .   
    ELSE   
    DO:   
         RUN zugriff-test(user-init, 12, 2, OUTPUT zugriff).
         IF NOT zugriff THEN RETURN.
    END.   
END.   
ELSE IF tbill-resnr = 0 THEN  
DO:  
    RUN zugriff-test(user-init, 55, 2, OUTPUT zugriff).
    IF NOT zugriff THEN RETURN.
END.

IF bill-type = 1 THEN zinr = bill1.zinr.   
ELSE zinr = "".   
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

/*************************** PROCEDURE ************************/
PROCEDURE zugriff-test:
DEFINE INPUT PARAMETER user-init   AS CHAR FORMAT "x(2)".   
DEFINE INPUT PARAMETER array-nr    AS INTEGER.   
DEFINE INPUT PARAMETER expected-nr AS INTEGER.   
DEFINE OUTPUT PARAMETER zugriff    AS LOGICAL INITIAL YES.   
    
DEFINE VARIABLE mail-exist      AS LOGICAL NO-UNDO.  
DEFINE VARIABLE logical-flag    AS LOGICAL NO-UNDO.  
DEFINE VARIABLE n               AS INTEGER.   
DEFINE VARIABLE perm            AS INTEGER EXTENT 120 FORMAT "9". /* Malik 4CD2E2 */   
DEFINE VARIABLE s1              AS CHAR FORMAT "x(2)".   
DEFINE VARIABLE s2              AS CHAR FORMAT "x(1)".   
DEFINE VARIABLE mn-date         AS DATE.   
DEFINE VARIABLE anz             AS INTEGER.   
DEFINE VARIABLE hAsync          AS HANDLE               NO-UNDO.  
DEFINE VARIABLE email-checked   AS LOGICAL INITIAL NO   NO-UNDO.
DEFINE VARIABLE p-786           AS CHARACTER NO-UNDO.
  
    RUN htpchar.p(786, OUTPUT p-786).
          
    IF user-init = "" THEN  
    DO:   
      zugriff = NO.   
      msg-str = translateExtended ("User not defined.",lvCAREA,"").   
    END.
    ELSE   
    DO:   
      DO n = 1 TO LENGTH(t-bediener.permissions):   
        perm[n] = INTEGER(SUBSTR(t-bediener.permissions, n, 1)).   
      END.   
      IF perm[array-nr] LT expected-nr THEN   
      DO:   
        zugriff = NO.   
        s1 = STRING(array-nr, "999").   
        s2 = STRING(expected-nr).   
        msg-str = translateExtended ("Sorry, No Access Right.",lvCAREA,"") + CHR(10)   
              + translateExtended ("Access Code =",lvCAREA,"") + " " + s1 + s2.                
      END.   
    END. 
END PROCEDURE.

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
