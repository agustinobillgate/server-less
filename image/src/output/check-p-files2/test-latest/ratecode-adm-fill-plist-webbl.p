DEFINE TEMP-TABLE early-discount
    FIELD disc-rate AS DECIMAL FORMAT ">9.99" LABEL "Disc%"
    FIELD min-days  AS INTEGER FORMAT ">>>"   LABEL "Min to C/I(days)"
    FIELD min-stay  AS INTEGER FORMAT ">>>"   LABEL "Min Stays"
    FIELD max-occ   AS INTEGER FORMAT " >>"   LABEL "Upto Occ"
    FIELD from-date AS DATE                   LABEL "Fr BookDate"
    FIELD to-date   AS DATE                   LABEL "To BookDate".

DEFINE TEMP-TABLE kickback-discount
    FIELD disc-rate AS DECIMAL FORMAT ">9.99" LABEL "Disc%"
    FIELD max-days  AS INTEGER FORMAT ">>>"   LABEL "Max to C/I(days)"
    FIELD min-stay  AS INTEGER FORMAT ">>>"   LABEL "Min Stays"
    FIELD max-occ   AS INTEGER FORMAT " >>"   LABEL "Upto Occ".

DEFINE TEMP-TABLE stay-pay
    FIELD f-date    AS DATE                      LABEL "FromDate"
    FIELD t-date    AS DATE                      LABEL "ToDate"
    FIELD stay      AS INTEGER FORMAT "     >>>" LABEL "Stay(Nights)"
    FIELD pay       AS INTEGER FORMAT "     >>>" LABEL "Pay(Nights)".

DEFINE INPUT PARAMETER tb3-char1-1  AS CHARACTER.
DEFINE INPUT PARAMETER tb3-char1-2  AS CHARACTER.
DEFINE INPUT PARAMETER tb3-char1-3  AS CHARACTER.
DEFINE INPUT PARAMETER tb3-char1-4  AS CHARACTER.
DEFINE OUTPUT PARAMETER book-room   AS INTEGER.
DEFINE OUTPUT PARAMETER comp-room   AS INTEGER.
DEFINE OUTPUT PARAMETER max-room    AS INTEGER.
DEFINE OUTPUT PARAMETER TABLE FOR early-discount.
DEFINE OUTPUT PARAMETER TABLE FOR kickback-discount.
DEFINE OUTPUT PARAMETER TABLE FOR stay-pay.

DEFINE VARIABLE n AS INTEGER NO-UNDO.
DEFINE VARIABLE ct AS CHARACTER NO-UNDO.
DEFINE VARIABLE fdatum AS DATE NO-UNDO.
DEFINE VARIABLE tdatum AS DATE NO-UNDO.

DEFINE VARIABLE i AS INTEGER NO-UNDO.  
DO i = 1 TO 10:  
    CREATE kickback-discount.  
END.  
DO i = 1 TO 20:  
    CREATE early-discount.  
END.  
DO i = 1 TO 30:  
    CREATE stay-pay.  
END.  

RUN init-buff.

IF NUM-ENTRIES(tb3-char1-1, ";") GE 2 THEN                             
DO                                                                      
    n = 1 TO NUM-ENTRIES(tb3-char1-1, ";") - 1:                        
    ct = ENTRY(n, tb3-char1-1, ";").                                   
                                                                        
    FIND FIRST early-discount WHERE early-discount.disc-rate = 0.
    ASSIGN                                                              
        early-discount.disc-rate = INTEGER(ENTRY(1, ct, ",")) / 100              
        early-discount.min-days  = INTEGER(ENTRY(2, ct, ","))                    
        early-discount.min-stay  = INTEGER(ENTRY(3, ct, ","))                    
        early-discount.max-occ   = INTEGER(ENTRY(4, ct, ","))                    
        .                                                               
                                                                        
    IF NUM-ENTRIES(ct, ",") GE 5 AND TRIM(ENTRY(5,ct,",")) NE "" THEN   
        early-discount.from-date = DATE(INTEGER(SUBSTR(ENTRY(5, ct, ","),5,2)),  
                          INTEGER(SUBSTR(ENTRY(5, ct, ","),7,2)),       
                          INTEGER(SUBSTR(ENTRY(5, ct, ","),1,4))).      
                                                                        
    IF NUM-ENTRIES(ct, ",") GE 6 AND TRIM(ENTRY(6,ct,",")) NE "" THEN   
        early-discount.to-date   = DATE(INTEGER(SUBSTR(ENTRY(6, ct, ","),5,2)),  
                          INTEGER(SUBSTR(ENTRY(6, ct, ","),7,2)),       
                          INTEGER(SUBSTR(ENTRY(6, ct, ","),1,4))).      
END.                                                                    
                                                                        
IF NUM-ENTRIES(tb3-char1-2, ";") GE 2 THEN                             
DO n = 1 TO NUM-ENTRIES(tb3-char1-2, ";") - 1:                         
    ct = ENTRY(n, tb3-char1-2, ";").                                   
    FIND FIRST kickback-discount WHERE kickback-discount.disc-rate = 0.
    ASSIGN                                                              
        kickback-discount.disc-rate = INTEGER(ENTRY(1, ct, ",")) / 100              
        kickback-discount.max-days  = INTEGER(ENTRY(2, ct, ","))                    
        kickback-discount.min-stay  = INTEGER(ENTRY(3, ct, ","))                    
        kickback-discount.max-occ   = INTEGER(ENTRY(4, ct, ","))                    
        .                                                               
END.                                                                    
                                                                        
IF NUM-ENTRIES(tb3-char1-3, ";") GE 2 THEN                             
DO n = 1 TO NUM-ENTRIES(tb3-char1-3, ";") - 1:                         
    ct = ENTRY(n, tb3-char1-3, ";").                                   
    FIND FIRST stay-pay WHERE stay-pay.stay = 0.
    fdatum = DATE(INTEGER(SUBSTR(ENTRY(1, ct, ","),5,2)),               
                  INTEGER(SUBSTR(ENTRY(1, ct, ","),7,2)),               
                  INTEGER(SUBSTR(ENTRY(1, ct, ","),1,4))).              
    tdatum = DATE(INTEGER(SUBSTR(ENTRY(2, ct, ","),5,2)),               
                  INTEGER(SUBSTR(ENTRY(2, ct, ","),7,2)),               
                  INTEGER(SUBSTR(ENTRY(2, ct, ","),1,4))).              
                                                                        
    ASSIGN                                                              
        stay-pay.f-date    = fdatum                                        
        stay-pay.t-date    = tdatum                                        
        stay-pay.stay      = INTEGER(ENTRY(3, ct, ","))                    
        stay-pay.pay       = INTEGER(ENTRY(4, ct, ","))                    
        .                                                               
END.                                                                    
                                                                        
IF NUM-ENTRIES(tb3-char1-4, ";") GE 3 THEN                             
ASSIGN                                                                  
    book-room = INTEGER(ENTRY(1, tb3-char1-4, ";"))                    
    comp-room = INTEGER(ENTRY(2, tb3-char1-4, ";"))                    
    max-room  = INTEGER(ENTRY(3, tb3-char1-4, ";"))                    
.                                                     

PROCEDURE init-buff:       
    FOR EACH early-discount:  
        ASSIGN  
            early-discount.disc-rate = 0  
            early-discount.min-days  = 0  
            early-discount.min-stay  = 0  
            early-discount.max-occ   = 0  
            early-discount.from-date = ?  
            early-discount.to-date   = ?  
        .  
    END.  
      
    FOR EACH kickback-discount:  
        ASSIGN  
            kickback-discount.disc-rate = 0  
            kickback-discount.max-days  = 0  
            kickback-discount.min-stay  = 0  
            kickback-discount.max-occ   = 0  
        .  
    END.  
      
    FOR EACH stay-pay:  
        ASSIGN  
            stay-pay.f-date = ?  
            stay-pay.t-date = ?  
            stay-pay.stay   = 0  
            stay-pay.pay    = 0  
        .  
    END.  
END.
