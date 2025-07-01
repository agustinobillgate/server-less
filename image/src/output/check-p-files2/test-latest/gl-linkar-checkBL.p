
DEFINE INPUT  PARAMETER pvILanguage AS INTEGER NO-UNDO.
DEFINE INPUT  PARAMETER user-init   AS CHAR    NO-UNDO.
DEFINE INPUT  PARAMETER array-nr    AS INTEGER NO-UNDO.   
DEFINE INPUT  PARAMETER expected-nr AS INTEGER NO-UNDO.   
DEFINE OUTPUT PARAMETER flag-msg    AS INTEGER NO-UNDO.
DEFINE OUTPUT PARAMETER msg-str     AS CHAR    NO-UNDO.

DEFINE VARIABLE zugriff  AS LOGICAL NO-UNDO INIT YES.
DEFINE VARIABLE flogical AS LOGICAL NO-UNDO.
DEFINE VARIABLE n        AS INTEGER.   
DEFINE VARIABLE perm     AS INTEGER EXTENT 120 FORMAT "9".  /* Malik 4CD2E2 */ 
DEFINE VARIABLE s1       AS CHAR FORMAT "x(2)".   
DEFINE VARIABLE s2       AS CHAR FORMAT "x(1)".  
DEFINE VARIABLE fdate    AS DATE NO-UNDO.

{supertransBL.i} 
DEF VAR lvCAREA AS CHAR INITIAL "gl-linkar-check". 

RUN htplogic.p (2000, OUTPUT flogical).  
IF flogical =  NO THEN   
DO:   
    ASSIGN 
        msg-str = translateExtended ("No License for this module.",lvCAREA,"") + CHR(13) + CHR(10) + 
                  translateExtended ("Please contact our local Technical Support for further information.",lvCAREA,"")
        flag-msg = 1.        
    RETURN.     
END.   
ELSE DO:
    IF user-init = " " THEN DO:
        ASSIGN 
            msg-str     = translateExtended ("User not defined.",lvCAREA,"")
            flag-msg    = 1
            zugriff     = NO.    
        RETURN.
    END.
    ELSE DO:
        FIND FIRST bediener WHERE bediener.userinit = user-init NO-LOCK NO-ERROR.
        IF AVAILABLE bediener THEN DO:
              DO n = 1 TO LENGTH(bediener.permissions):   
                perm[n] = INTEGER(SUBSTR(bediener.permissions, n, 1)).   
              END.   

              IF perm[array-nr] LT expected-nr THEN   
              DO:   
                    zugriff = NO.   
                    s1 = STRING(array-nr, "999").   
                    s2 = STRING(expected-nr).    
                    
                    ASSIGN
                        msg-str = translateExtended ("Sorry, No Access Right.",lvCAREA,"") + CHR(13) + CHR(10) +   
                                  translateExtended ("Access Code =",lvCAREA,"") + " " + s1 + s2
                        flag-msg = 1. 
                    RETURN.                    
              END.   
        END.
    END.

    IF zugriff THEN DO:
        RUN htpdate.p (1014, OUTPUT fdate).  
        IF fdate = ? THEN   
        DO:   
             ASSIGN 
                 msg-str  = translateExtended ("Last transfer date in (parameter 1014) not yet defined.",lvCAREA,"")
                 flag-msg = 1.
             RETURN.
        END.   
        ELSE DO:   
            ASSIGN  
                msg-str  = translateExtended ("Do you really want to transfer A/R Payments to GL Journals?",lvCAREA,"")
                flag-msg = 2.   
            RETURN.            
        END.   
    END.
END.

