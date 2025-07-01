DEFINE TEMP-TABLE output-list 
  FIELD marked    AS CHAR FORMAT "x(1)" LABEL "M" 
  FIELD fibukonto AS CHAR 
  FIELD jnr       AS INTEGER INITIAL 0 
  FIELD bemerk    AS CHAR
  FIELD str       AS CHAR. 


DEF INPUT  PARAMETER sorttype   AS INTEGER.
DEF INPUT  PARAMETER from-fibu  AS CHAR.
DEF INPUT  PARAMETER to-fibu    AS CHAR.
DEF INPUT  PARAMETER from-dept  AS INTEGER.
DEF INPUT  PARAMETER from-date  AS DATE.
DEF INPUT  PARAMETER to-date    AS DATE.
DEF INPUT  PARAMETER close-year AS DATE.
DEF OUTPUT PARAMETER TABLE FOR output-list.

/*MT
DEF VAR sorttype AS INTEGER INIT 2.
DEF VAR from-fibu AS CHAR INIT "00000000".
DEF VAR to-fibu AS CHAR INIT "99999999".
DEF VAR from-dept AS INT INIT 0.
DEF VAR from-date AS DATE INIT 01/01/07.
DEF VAR to-date AS DATE INIT 01/01/07.
DEF VAR close-year AS DATE INIT 12/31/11.
*/

FUNCTION get-bemerk RETURNS CHAR(bemerk AS CHAR): 
DEF VAR n AS INTEGER. 
DEF VAR s1 AS CHAR. 
  bemerk = REPLACE(bemerk, CHR(10), " ").
  n = INDEX(bemerk, ";&&"). 
  IF n > 0 THEN s1 = SUBSTR(bemerk, 1, n - 1). 
  ELSE s1 = bemerk.
  RETURN s1. 
END. 

RUN create-list.

PROCEDURE create-list: 
DEFINE VARIABLE debit AS DECIMAL FORMAT "->>>,>>>,>>>,>>9.99" INITIAL 0. 
DEFINE VARIABLE credit AS DECIMAL FORMAT "->>>,>>>,>>>,>>9.99" INITIAL 0. 
DEFINE VARIABLE balance AS DECIMAL FORMAT "->>>,>>>,>>>,>>9.99" INITIAL 0. 
DEFINE VARIABLE konto LIKE gl-acct.fibukonto INITIAL "". 
DEFINE VARIABLE i AS INTEGER. 
DEFINE VARIABLE c AS CHAR. 
DEFINE VARIABLE bezeich AS CHAR. 
DEFINE VARIABLE datum AS DATE. 
DEFINE VARIABLE refno AS CHAR. 
DEFINE VARIABLE h-bezeich AS CHAR. 
DEFINE VARIABLE id AS CHAR FORMAT "x(2)". 
DEFINE VARIABLE chgdate AS CHAR FORMAT "x(8)". 
DEFINE VARIABLE beg-date AS DATE. 
DEFINE VARIABLE beg-day AS INTEGER. 
 
DEFINE VARIABLE t-debit LIKE debit INITIAL 0. 
DEFINE VARIABLE t-credit LIKE credit INITIAL 0. 
DEFINE VARIABLE tot-debit LIKE debit INITIAL 0. 
DEFINE VARIABLE tot-credit LIKE credit INITIAL 0. 
 
DEFINE VARIABLE e-bal AS DECIMAL INITIAL 0. 
DEFINE VARIABLE delta AS DECIMAL INITIAL 0. 
DEFINE VARIABLE fdate AS DATE. 
DEFINE VARIABLE tdate AS DATE. 
 
DEFINE buffer gl-account FOR gl-acct. 
DEFINE buffer gl-jour1 FOR gl-jourhis. 
DEFINE buffer gl-jouh1 FOR gl-jhdrhis. 
 
DEFINE VARIABLE prev-mm AS INTEGER. 
DEFINE VARIABLE prev-yr AS INTEGER.
DEFINE VARIABLE prev-bal AS DECIMAL FORMAT "->>>,>>>,>>>,>>9.99" INITIAL 0. 
DEFINE VARIABLE end-bal AS DECIMAL FORMAT "->>>,>>>,>>>,>>9.99" INITIAL 0. 
 
DEFINE VARIABLE blankchar AS CHAR FORMAT "x(70)" INITIAL "". 
 

  DO i = 1 TO 72: 
    blankchar = blankchar + " ". 
  END. 
 
  ASSIGN
    prev-mm = MONTH(from-date) - 1
    prev-yr = YEAR(from-date)
  .
  IF prev-mm = 0 THEN 
  ASSIGN
    prev-mm = 12
    prev-yr = prev-yr - 1
  .
 
  beg-date = DATE(MONTH(from-date), 1, YEAR(from-date)). 
 
  FOR EACH output-list: 
    delete output-list. 
  END. 

  DO: 
    IF sorttype = 2 THEN 
     DO: 
         /*MTIF CONNECTED("vhparch") THEN 
         DO: 
             /*RUN gljouhislist-arch.p ("sort2", from-fibu ,to-fibu, from-date, to-date, "", close-year, 0, "", 0, OUTPUT changed, OUTPUT done, OUTPUT jnr2).*/
         END.
         ELSE 
         DO: */
               FOR EACH vhp.gl-jourhis WHERE  vhp.gl-jourhis.fibukonto GE from-fibu 
                 AND vhp.gl-jourhis.fibukonto LE to-fibu NO-LOCK,
                 FIRST vhp.gl-jhdrhis WHERE vhp.gl-jhdrhis.jnr = vhp.gl-jourhis.jnr 
                 AND vhp.gl-jhdrhis.datum GE from-date AND vhp.gl-jhdrhis.datum LE to-date NO-LOCK, 
                 FIRST gl-acct WHERE gl-acct.fibukonto = vhp.gl-jourhis.fibukonto NO-LOCK 
                 BY vhp.gl-jourhis.fibukonto BY vhp.gl-jhdrhis.datum 
                 BY vhp.gl-jhdrhis.refno BY SUBSTR(vhp.gl-jourhis.bemerk,1,24): 
        
                 IF vhp.gl-jourhis.chgdate = ? THEN chgdate = "". 
                 ELSE chgdate = STRING(gl-jourhis.chgdate). 
                 IF konto = "" THEN 
                 DO:    
                   prev-bal = 0. 
                   FIND FIRST gl-account WHERE gl-account.fibukonto = gl-acct.fibukonto
                     NO-LOCK.
                   /*IF (gl-account.acc-type = 3 OR gl-account.acc-type = 4) THEN 
                   DO: */
                     IF prev-yr LT YEAR(close-year) THEN
                     DO:
                       FIND FIRST gl-accthis WHERE 
                         gl-accthis.fibukonto = gl-account.fibukonto AND
                         gl-accthis.YEAR = prev-yr NO-LOCK NO-ERROR.
                       IF AVAILABLE gl-accthis THEN 
                         prev-bal = gl-accthis.actual[prev-mm].
                     END.
                     ELSE IF prev-yr = YEAR(close-year) THEN
                       prev-bal = gl-account.actual[prev-mm].
                     IF gl-account.acc-type = 1 OR gl-account.acc-type = 4 THEN
                     DO:
                         prev-bal = - prev-bal.
                     END.  
                     IF gl-account.acc-type = 3 OR gl-account.acc-type = 4 THEN
                         balance = prev-bal.
                     ELSE balance = 0.
                     /*e-bal = prev-bal.*/
                   /*END.*/
                   CREATE output-list. 
                   RUN convert-fibu(gl-acct.fibukonto, OUTPUT c). 
                   STR = "        " + STRING(c, "x(15)") 
                     + STRING(gl-acct.bezeich, "x(40)") /*+
                       FILL(" ", 108) + STRING(prev-bal, "->>>,>>>,>>>,>>9.99")*/. 
                   konto = gl-acct.fibukonto.
                 END.
                 
                 IF konto NE gl-acct.fibukonto THEN 
                 DO: 
                   CREATE output-list. 
                   DO i = 1 TO 30: 
                     STR = STR + " ". 
                   END. 
                  
                   STR = STR + "T O T A L  " 
                       /*+ FILL(" ", 19)*/
                       + STRING(prev-bal, "->>,>>>,>>>,>>>,>>9.99") 
                       + STRING(t-debit, "->>,>>>,>>>,>>>,>>9.99") 
                       + STRING(t-credit, "->>,>>>,>>>,>>>,>>9.99") 
                       + blankchar 
                       + STRING(balance, "->>,>>>,>>>,>>>,>>9.99"). 
                   CREATE output-list. 
        
                   balance = 0. 
                   t-debit = 0. 
                   t-credit = 0. 
        
                   prev-bal = 0. 
                   FIND FIRST gl-account WHERE gl-account.fibukonto = gl-acct.fibukonto
                     NO-LOCK.
                   /*IF AVAILABLE gl-account AND (gl-account.acc-type = 3 OR gl-account.acc-type = 4) THEN 
                   DO: */
                     IF prev-yr LT YEAR(close-year) THEN
                     DO:
                       FIND FIRST gl-accthis WHERE 
                         gl-accthis.fibukonto = gl-account.fibukonto AND
                         gl-accthis.YEAR = prev-yr NO-LOCK NO-ERROR.
                       IF AVAILABLE gl-accthis THEN 
                         prev-bal = gl-accthis.actual[prev-mm].
                     END.
                     ELSE IF prev-yr = YEAR(close-year) THEN
                       prev-bal = gl-account.actual[prev-mm].
                     IF gl-account.acc-type = 1 OR gl-account.acc-type = 4 THEN
                     DO:
                         prev-bal = - prev-bal.
                     END.
                   /*  e-bal = prev-bal.
                   END.*/
                   IF gl-account.acc-type = 3 OR gl-account.acc-type = 4 THEN
                         balance = prev-bal.
                   ELSE balance = 0.
                   
                   CREATE output-list. 
                   RUN convert-fibu(gl-acct.fibukonto, OUTPUT c). 
                   STR = "        " + STRING(c, "x(15)") 
                     + STRING(gl-acct.bezeich, "x(40)") /*+ 
                     FILL(" ", 108) + STRING(prev-bal, "->>>,>>>,>>>,>>9.99")*/. 
                   konto = gl-acct.fibukonto. 
                 END.
        
                 FIND FIRST gl-account WHERE gl-account.fibukonto 
                   = vhp.gl-jourhis.fibukonto NO-LOCK. 
                 IF gl-account.acc-type = 1 OR gl-account.acc-type = 4 THEN
                    balance = balance - vhp.gl-jourhis.debit + vhp.gl-jourhis.credit.
                 ELSE
                    balance = balance + gl-jourhis.debit - gl-jourhis.credit.
                 /*balance = balance + gl-jourhis.debit - gl-jourhis.credit. */
                 t-debit = t-debit + vhp.gl-jourhis.debit. 
                 t-credit = t-credit + vhp.gl-jourhis.credit. 
                 tot-debit = tot-debit + vhp.gl-jourhis.debit. 
                 tot-credit = tot-credit + vhp.gl-jourhis.credit. 
                 
                 CREATE output-list. 
                 ASSIGN
                   output-list.fibukonto = gl-jourhis.fibukonto
                   output-list.jnr = vhp.gl-jhdrhis.jnr
                   STR = STRING(vhp.gl-jhdrhis.datum) 
                       + STRING(vhp.gl-jhdrhis.refno, "x(15)") 
                       + STRING(vhp.gl-jhdrhis.bezeich, "x(40)") 
                       + STRING(vhp.gl-jourhis.debit, "->>,>>>,>>>,>>>,>>9.99") 
                       + STRING(vhp.gl-jourhis.credit, "->>,>>>,>>>,>>>,>>9.99") 
                       + STRING(vhp.gl-jourhis.userinit, "x(3)") 
                       + STRING(vhp.gl-jourhis.sysdate) 
                       + STRING(vhp.gl-jourhis.chginit, "x(3)") 
                       + STRING(chgdate, "x(8)") 
                       + STRING(get-bemerk(vhp.gl-jourhis.bemerk), "x(50)")
                       + STRING(balance, "->>,>>>,>>>,>>>,>>9.99")
                 . 
                 output-list.bemerk = get-bemerk(gl-jourhis.bemerk).
                 
                 /*IF NOT too-old THEN 
                 DO:
                     IF gl-account.acc-type = 1 OR gl-account.acc-type = 4 THEN
                        e-bal = e-bal - gl-jourhis.debit + gl-jourhis.credit. 
                     ELSE e-bal = e-bal + gl-jourhis.debit - gl-jourhis.credit. 
                 END.
                 str = str + STRING(e-bal, "->>>,>>>,>>>,>>9.99").*/
                 /*IF gl-acct.acc-type = 1 OR gl-acct.acc-type = 4 THEN 
                   STR = STR + STRING(- e-bal, "->>>,>>>,>>>,>>9.99"). 
                 ELSE STR = STR + STRING(e-bal, "->>>,>>>,>>>,>>9.99"). */
               END.  
         /*MTEND. /* end konek db2*/*/
       CREATE output-list. 
       DO i = 1 TO 30: 
         STR = STR + " ". 
       END. 
       
       STR = STR + "T O T A L  " 
           /*+ FILL(" ", 19)*/
           + STRING(prev-bal, "->>,>>>,>>>,>>>,>>9.99") 
           + STRING(t-debit, "->>,>>>,>>>,>>>,>>9.99") 
           + STRING(t-credit, "->>,>>>,>>>,>>>,>>9.99") 
           + blankchar 
           + STRING(balance, "->>,>>>,>>>,>>>,>>9.99"). 
       CREATE output-list. 
       CREATE output-list. 
       DO i = 1 TO 30: 
           STR = STR + " ". 
       END. 

       STR = STR + "GRAND T O T A L                  " 
               + STRING(tot-debit, "->>,>>>,>>>,>>>,>>9.99") 
               + STRING(tot-credit, "->>,>>>,>>>,>>>,>>9.99"). 
     END. 
     
     ELSE IF sorttype = 1 THEN 
     DO: 
         /*MT
         IF CONNECTED("vhparch") THEN RUN gljouhislist-arch.p ("sort1", from-fibu ,to-fibu, from-date, to-date, "",close-year, 0, "", gl-main.nr, OUTPUT changed, OUTPUT done, OUTPUT jnr2).
         ELSE 
         DO:*/
               FOR EACH vhp.gl-jourhis WHERE  vhp.gl-jourhis.fibukonto GE from-fibu 
                 AND vhp.gl-jourhis.fibukonto LE to-fibu NO-LOCK, 
                 FIRST vhp.gl-jhdrhis WHERE vhp.gl-jhdrhis.jnr = vhp.gl-jourhis.jnr 
                 AND vhp.gl-jhdrhis.datum GE from-date AND vhp.gl-jhdrhis.datum LE to-date NO-LOCK, 
                 FIRST gl-acct WHERE gl-acct.fibukonto = vhp.gl-jourhis.fibukonto 
                   AND gl-acct.main-nr = gl-main.nr NO-LOCK 
                 BY vhp.gl-jourhis.fibukonto BY vhp.gl-jhdrhis.datum 
                 BY vhp.gl-jhdrhis.refno BY SUBSTR(vhp.gl-jourhis.bemerk,1,24): 
         
                 IF vhp.gl-jourhis.chgdate = ? THEN chgdate = "". 
                 ELSE chgdate = STRING(gl-jourhis.chgdate). 
                 IF konto = "" THEN 
                 DO:    
                   prev-bal = 0. 
                   FIND FIRST gl-account WHERE gl-account.fibukonto = gl-acct.fibukonto
                     NO-LOCK.
                   /*IF (gl-account.acc-type = 3 OR gl-account.acc-type = 4) THEN 
                   DO: */
                     IF prev-yr LT YEAR(close-year) THEN
                     DO:
                       FIND FIRST gl-accthis WHERE 
                         gl-accthis.fibukonto = gl-account.fibukonto AND
                         gl-accthis.YEAR = prev-yr NO-LOCK NO-ERROR.
                       IF AVAILABLE gl-accthis THEN 
                         prev-bal = gl-accthis.actual[prev-mm].
                     END.
                     ELSE IF prev-yr = YEAR(close-year) THEN
                       prev-bal = gl-account.actual[prev-mm].
                     IF gl-account.acc-type = 1 OR gl-account.acc-type = 4 THEN
                     DO:
                         prev-bal = - prev-bal.
                     END.       
                     IF gl-account.acc-type = 3 OR gl-account.acc-type = 4 THEN
                         balance = prev-bal.
                     ELSE balance = 0.
                     /*e-bal = prev-bal.
                   END.*/
                   CREATE output-list. 
                   RUN convert-fibu(gl-acct.fibukonto, OUTPUT c). 
                   STR = "        " + STRING(c, "x(15)") 
                     + STRING(gl-acct.bezeich, "x(40)") /*+
                       FILL(" ", 108) + STRING(prev-bal, "->>>,>>>,>>>,>>9.99")*/. 
                   konto = gl-acct.fibukonto.
                 END.
                 
                 IF konto NE gl-acct.fibukonto THEN 
                 DO: 
                     CREATE output-list. 
                   DO i = 1 TO 30: 
                     STR = STR + " ". 
                   END. 
                  
                   STR = STR + "T O T A L  " 
                       /*+ FILL(" ", 19)*/
                       + STRING(prev-bal, "->>,>>>,>>>,>>>,>>9.99") 
                       + STRING(t-debit, "->>,>>>,>>>,>>>,>>9.99") 
                       + STRING(t-credit, "->>,>>>,>>>,>>>,>>9.99") 
                       + blankchar 
                       + STRING(balance, "->>,>>>,>>>,>>>,>>9.99"). 
                   CREATE output-list. 
        
                   balance = 0. 
                   t-debit = 0. 
                   t-credit = 0. 
        
                   prev-bal = 0. 
                   FIND FIRST gl-account WHERE gl-account.fibukonto = gl-acct.fibukonto
                     NO-LOCK.
                   /*IF (gl-account.acc-type = 3 OR gl-account.acc-type = 4) THEN 
                   DO: */
                     IF prev-yr LT YEAR(close-year) THEN
                     DO:
                       FIND FIRST gl-accthis WHERE 
                         gl-accthis.fibukonto = gl-account.fibukonto AND
                         gl-accthis.YEAR = prev-yr NO-LOCK NO-ERROR.
                       IF AVAILABLE gl-accthis THEN 
                         prev-bal = gl-accthis.actual[prev-mm].
                     END.
                     ELSE IF prev-yr = YEAR(close-year) THEN
                       prev-bal = gl-account.actual[prev-mm].
                     IF gl-account.acc-type = 1 OR gl-account.acc-type = 4 THEN
                     DO:
                         prev-bal = - prev-bal.
                     END.
                     IF gl-account.acc-type = 3 OR gl-account.acc-type = 4 THEN
                         balance = prev-bal.
                     ELSE balance = 0.
                     /*e-bal = prev-bal.
                   END.*/
                   
                   CREATE output-list. 
                   RUN convert-fibu(gl-acct.fibukonto, OUTPUT c). 
                   STR = "        " + STRING(c, "x(15)") 
                     + STRING(gl-acct.bezeich, "x(40)") /*+ 
                     FILL(" ", 108) + STRING(prev-bal, "->>>,>>>,>>>,>>9.99")*/. 
                   konto = gl-acct.fibukonto.
                 END. 
        
                 FIND FIRST gl-account WHERE gl-account.fibukonto 
                   = gl-jourhis.fibukonto NO-LOCK. 
                 IF gl-account.acc-type = 1 OR gl-account.acc-type = 4 THEN
                    balance = balance - vhp.gl-jourhis.debit + vhp.gl-jourhis.credit.
                 ELSE
                     balance = balance + vhp.gl-jourhis.debit - vhp.gl-jourhis.credit.
                     t-debit = t-debit + vhp.gl-jourhis.debit. 
                     t-credit = t-credit + vhp.gl-jourhis.credit. 
                     tot-debit = tot-debit + vhp.gl-jourhis.debit. 
                     tot-credit = tot-credit + vhp.gl-jourhis.credit. 
                 
                 CREATE output-list. 
                 ASSIGN
                   output-list.fibukonto = vhp.gl-jourhis.fibukonto
                   output-list.jnr = vhp.gl-jhdrhis.jnr
                   STR = STRING(vhp.gl-jhdrhis.datum) 
                       + STRING(vhp.gl-jhdrhis.refno, "x(15)") 
                       + STRING(vhp.gl-jhdrhis.bezeich, "x(40)") 
                       + STRING(vhp.gl-jourhis.debit, "->>,>>>,>>>,>>>,>>9.99") 
                       + STRING(vhp.gl-jourhis.credit, "->>,>>>,>>>,>>>,>>9.99") 
                       + STRING(vhp.gl-jourhis.userinit, "x(3)") 
                       + STRING(vhp.gl-jourhis.sysdate) 
                       + STRING(vhp.gl-jourhis.chginit, "x(3)") 
                       + STRING(chgdate, "x(8)") 
                       + STRING(get-bemerk(vhp.gl-jourhis.bemerk), "x(50)")
                       + STRING(balance, "->>,>>>,>>>,>>>,>>9.99")
                 . 
                 output-list.bemerk = get-bemerk(vhp.gl-jourhis.bemerk).
                 
                 /*
                 IF NOT too-old THEN 
                 DO:
                   IF gl-account.acc-type = 1 OR gl-account.acc-type = 4 THEN
                        e-bal = e-bal - gl-jourhis.debit + gl-jourhis.credit. 
                   ELSE e-bal = e-bal + gl-jourhis.debit - gl-jourhis.credit. 
                 END.
                 STR = STR + STRING(e-bal, "->>>,>>>,>>>,>>9.99").
                     
                 IF gl-acct.acc-type = 1 OR gl-acct.acc-type = 4 THEN 
                   STR = STR + STRING(- e-bal, "->>>,>>>,>>>,>>9.99"). 
                 ELSE STR = STR + STRING(e-bal, "->>>,>>>,>>>,>>9.99"). 
                 */
               END.  
           /*MTEND. /*if not connected*/*/
                   
           CREATE output-list. 
           DO i = 1 TO 30: 
             STR = STR + " ". 
           END. 
           
           STR = STR + "T O T A L  " 
               /*+ FILL(" ", 19)*/
               + STRING(prev-bal, "->>,>>>,>>>,>>>,>>9.99") 
               + STRING(t-debit, "->>,>>>,>>>,>>>,>>9.99") 
               + STRING(t-credit, "->>,>>>,>>>,>>>,>>9.99") 
               + blankchar 
               + STRING(balance, "->>,>>>,>>>,>>>,>>9.99"). 
           CREATE output-list. 
           CREATE output-list. 
           DO i = 1 TO 30: 
               STR = STR + " ". 
           END. 
    
           STR = STR + "GRAND T O T A L                  " 
                   + STRING(tot-debit, "->>,>>>,>>>,>>>,>>9.99") 
                   + STRING(tot-credit, "->>,>>>,>>>,>>>,>>9.99"). 
            
        
     END. /*sorttype = 1 */


     ELSE IF sorttype = 3 THEN 
     DO:
         /*MTIF CONNECTED("vhparch") THEN 
          DO:
              RUN gljouhislist-arch.p ("sort3", from-fibu ,to-fibu, from-date, to-date, from-dept, close-year, 0, "", 0, OUTPUT changed , OUTPUT done , OUTPUT jnr2).
         END.
         ELSE 
         DO:*/
              FOR EACH vhp.gl-jourhis WHERE  vhp.gl-jourhis.fibukonto GE from-fibu 
                 AND vhp.gl-jourhis.fibukonto LE to-fibu NO-LOCK, 
                 FIRST vhp.gl-jhdrhis WHERE vhp.gl-jhdrhis.jnr = vhp.gl-jourhis.jnr 
                 AND vhp.gl-jhdrhis.datum GE from-date AND vhp.gl-jhdrhis.datum LE to-date NO-LOCK, 
                 FIRST gl-acct WHERE gl-acct.fibukonto = vhp.gl-jourhis.fibukonto 
                 AND gl-acct.deptnr = from-dept NO-LOCK 
                 BY vhp.gl-jourhis.fibukonto BY vhp.gl-jhdrhis.datum 
                 BY vhp.gl-jhdrhis.refno BY SUBSTR(vhp.gl-jourhis.bemerk,1,24): 
         
                 IF vhp.gl-jourhis.chgdate = ? THEN chgdate = "". 
                 ELSE chgdate = STRING(gl-jourhis.chgdate). 
                 IF konto = "" THEN 
                 DO:    
                   prev-bal = 0. 
                   FIND FIRST gl-account WHERE gl-account.fibukonto = gl-acct.fibukonto
                     NO-LOCK.
                   /*IF (gl-account.acc-type = 3 OR gl-account.acc-type = 4) THEN 
                   DO: */
                     IF prev-yr LT YEAR(close-year) THEN
                     DO:
                       FIND FIRST gl-accthis WHERE 
                         gl-accthis.fibukonto = gl-account.fibukonto AND
                         gl-accthis.YEAR = prev-yr NO-LOCK NO-ERROR.
                       IF AVAILABLE gl-accthis THEN 
                         prev-bal = gl-accthis.actual[prev-mm].
                     END.
                     ELSE IF prev-yr = YEAR(close-year) THEN
                       prev-bal = gl-account.actual[prev-mm].
                     IF gl-account.acc-type = 1 OR gl-account.acc-type = 4 THEN
                     DO:
                         prev-bal = - prev-bal.
                     END.      
                     IF gl-account.acc-type = 3 OR gl-account.acc-type = 4 THEN
                         balance = prev-bal.
                     ELSE balance = 0.
                     /*e-bal = prev-bal.
                   END.*/
                   CREATE output-list. 
                   RUN convert-fibu(gl-acct.fibukonto, OUTPUT c). 
                   STR = "        " + STRING(c, "x(15)") 
                     + STRING(gl-acct.bezeich, "x(40)") /*+
                       FILL(" ", 108) + STRING(prev-bal, "->>>,>>>,>>>,>>9.99")*/. 
                   konto = gl-acct.fibukonto.
                 END.
                 
                 IF konto NE gl-acct.fibukonto THEN 
                 DO: 
                     CREATE output-list. 
                   DO i = 1 TO 30: 
                     STR = STR + " ". 
                   END. 
                  
                   STR = STR + "T O T A L  " 
                       /*+ FILL(" ", 19)*/
                       + STRING(prev-bal, "->>,>>>,>>>,>>>,>>9.99") 
                       + STRING(t-debit, "->>,>>>,>>>,>>>,>>9.99") 
                       + STRING(t-credit, "->>,>>>,>>>,>>>,>>9.99") 
                       + blankchar 
                       + STRING(balance, "->>,>>>,>>>,>>>,>>9.99"). 
                   CREATE output-list. 
        
                   balance = 0. 
                   t-debit = 0. 
                   t-credit = 0. 
        
                   prev-bal = 0. 
                   FIND FIRST gl-account WHERE gl-account.fibukonto = gl-acct.fibukonto
                     NO-LOCK.
                   /*IF (gl-account.acc-type = 3 OR gl-account.acc-type = 4) THEN 
                   DO: */
                     IF prev-yr LT YEAR(close-year) THEN
                     DO:
                       FIND FIRST gl-accthis WHERE 
                         gl-accthis.fibukonto = gl-account.fibukonto AND
                         gl-accthis.YEAR = prev-yr NO-LOCK NO-ERROR.
                       IF AVAILABLE gl-accthis THEN 
                         prev-bal = gl-accthis.actual[prev-mm].
                     END.
                     ELSE IF prev-yr = YEAR(close-year) THEN
                       prev-bal = gl-account.actual[prev-mm].
                     IF gl-account.acc-type = 1 OR gl-account.acc-type = 4 THEN
                     DO:
                         prev-bal = - e-bal.
                     END.
                     IF gl-account.acc-type = 3 OR gl-account.acc-type = 4 THEN
                         balance = prev-bal.
                     ELSE balance = 0.
                     /*e-bal = prev-bal.
                   END.
                   IF gl-account.acc-type = 1 OR gl-account.acc-type = 4 THEN
                    end-bal = prev-bal - t-debit + t-credit.
                   ELSE
                     end-bal = prev-bal + t-debit - t-credit.*/
                   
                   CREATE output-list. 
                   RUN convert-fibu(gl-acct.fibukonto, OUTPUT c). 
                   STR = "        " + STRING(c, "x(15)") 
                     + STRING(gl-acct.bezeich, "x(40)") /* + 
                     FILL(" ", 108) + STRING(prev-bal, "->>>,>>>,>>>,>>9.99")*/. 
                   konto = gl-acct.fibukonto.
                 END. 
        
                 FIND FIRST gl-account WHERE gl-account.fibukonto 
                   = gl-jourhis.fibukonto NO-LOCK. 
                 IF gl-account.acc-type = 1 OR gl-account.acc-type = 4 THEN
                    balance = balance - gl-jourhis.debit + gl-jourhis.credit.
                 ELSE
                    balance = balance + vhp.gl-jourhis.debit - vhp.gl-jourhis.credit.
                 t-debit = t-debit + vhp.gl-jourhis.debit. 
                 t-credit = t-credit + vhp.gl-jourhis.credit. 
                 tot-debit = tot-debit + vhp.gl-jourhis.debit. 
                 tot-credit = tot-credit + vhp.gl-jourhis.credit. 
                 
                 CREATE output-list. 
                 ASSIGN
                   output-list.fibukonto = vhp.gl-jourhis.fibukonto
                   output-list.jnr = vhp.gl-jhdrhis.jnr
                   STR = STRING(vhp.gl-jhdrhis.datum) 
                       + STRING(vhp.gl-jhdrhis.refno, "x(15)") 
                       + STRING(vhp.gl-jhdrhis.bezeich, "x(40)") 
                       + STRING(vhp.gl-jourhis.debit, "->>,>>>,>>>,>>>,>>9.99") 
                       + STRING(vhp.gl-jourhis.credit, "->>,>>>,>>>,>>>,>>9.99") 
                       + STRING(vhp.gl-jourhis.userinit, "x(3)") 
                       + STRING(vhp.gl-jourhis.sysdate) 
                       + STRING(vhp.gl-jourhis.chginit, "x(3)") 
                       + STRING(chgdate, "x(8)") 
                       + STRING(get-bemerk(vhp.gl-jourhis.bemerk), "x(50)")
                       + STRING(balance, "->>,>>>,>>>,>>>,>>9.99")
                 . 
                 output-list.bemerk = get-bemerk(vhp.gl-jourhis.bemerk).
        
                 /*IF NOT too-old THEN 
                 DO:
                   IF gl-account.acc-type = 1 OR gl-account.acc-type = 4 THEN
                        e-bal = e-bal - gl-jourhis.debit + gl-jourhis.credit. 
                   ELSE e-bal = e-bal + gl-jourhis.debit - gl-jourhis.credit.
                 END.
                   
                 STR = STR + STRING(e-bal, "->>>,>>>,>>>,>>9.99").
                 */
                 /*IF gl-acct.acc-type = 1 OR gl-acct.acc-type = 4 THEN 
                   STR = STR + STRING(- e-bal, "->>>,>>>,>>>,>>9.99"). 
                 ELSE STR = STR + STRING(e-bal, "->>>,>>>,>>>,>>9.99"). */
                 
              END.  /*end for*/
         /*MTEND. /*if not connected*/*/

           CREATE output-list. 
           DO i = 1 TO 30: 
             STR = STR + " ". 
           END. 
           
           STR = STR + "T O T A L  " 
              /*+ FILL(" ", 19)*/
               + STRING(prev-bal, "->>,>>>,>>>,>>>,>>9.99") 
               + STRING(t-debit, "->>,>>>,>>>,>>>,>>9.99") 
               + STRING(t-credit, "->>,>>>,>>>,>>>,>>9.99") 
               + blankchar 
               + STRING(balance, "->>,>>>,>>>,>>>,>>9.99"). 
           CREATE output-list. 
           CREATE output-list. 
           DO i = 1 TO 30: 
               STR = STR + " ". 
           END. 
    
           STR = STR + "GRAND T O T A L                  " 
                   + STRING(tot-debit, "->>,>>>,>>>,>>>,>>9.99") 
                   + STRING(tot-credit, "->>,>>>,>>>,>>>,>>9.99"). 
                   
       END. /*if sorttype = 3*/
   END.
END. 



PROCEDURE convert-fibu: 
DEFINE INPUT PARAMETER konto AS CHAR. 
DEFINE OUTPUT PARAMETER s AS CHAR INITIAL "". 
DEFINE VARIABLE ch AS CHAR. 
DEFINE VARIABLE i AS INTEGER. 
DEFINE VARIABLE j AS INTEGER. 
  
  FIND FIRST htparam WHERE htparam.paramnr = 977 NO-LOCK NO-ERROR.
  IF AVAILABLE htparam THEN ch = htparam.fchar.

  j = 0. 
  DO i = 1 TO LENGTH(ch): 
    IF SUBSTR(ch, i, 1) GE "0" AND SUBSTR(ch, i, 1) LE  "9" THEN 
    DO: 
      j = j + 1. 
      s = s + SUBSTR(konto, j, 1). 
    END. 
    ELSE s = s + SUBSTR(ch, i, 1). 
  END. 
END. 
 
