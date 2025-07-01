DEFINE TEMP-TABLE t-bk-reser    LIKE bk-reser.
DEFINE TEMP-TABLE t-guest       LIKE guest.
DEFINE TEMP-TABLE t-htparam     LIKE htparam.
DEFINE TEMP-TABLE t-bk-veran    LIKE bk-veran.
/*FDL Dec 24, 2024: 5A4D76 - Could not update field 'vesrdepot' of target in a BUFFER-COPY statement*/
DEFINE TEMP-TABLE t-bill       
    FIELD zinr              LIKE bill.zinr             
    FIELD flag              LIKE bill.flag             
    FIELD rechnr            LIKE bill.rechnr           
    FIELD resnr             LIKE bill.resnr            
    FIELD gastnr            LIKE bill.gastnr           
    FIELD saldo             LIKE bill.saldo            
    FIELD gesamtumsatz      LIKE bill.gesamtumsatz     
    FIELD logisumsatz       LIKE bill.logisumsatz      
    FIELD arrangemdat       LIKE bill.arrangemdat      
    FIELD rgdruck           LIKE bill.rgdruck          
    FIELD logiernachte      LIKE bill.logiernachte     
    FIELD reslinnr          LIKE bill.reslinnr         
    FIELD argtumsatz        LIKE bill.argtumsatz       
    FIELD f-b-umsatz        LIKE bill.f-b-umsatz       
    FIELD sonst-umsatz      LIKE bill.sonst-umsatz     
    FIELD billnr            LIKE bill.billnr           
    FIELD firstper          LIKE bill.firstper         
    FIELD billkur           LIKE bill.billkur          
    FIELD logidat           LIKE bill.logidat          
    FIELD bilname           LIKE bill.bilname          
    FIELD teleinheit        LIKE bill.teleinheit       
    FIELD telsumme          LIKE bill.telsumme         
    FIELD segmentcode       LIKE bill.segmentcode      
    FIELD printnr           LIKE bill.printnr          
    FIELD billbankett       LIKE bill.billbankett      
    FIELD service           LIKE bill.service          
    FIELD mwst              LIKE bill.mwst             
    FIELD umleit-zinr       LIKE bill.umleit-zinr      
    FIELD billmaster        LIKE bill.billmaster       
    FIELD datum             LIKE bill.datum            
    FIELD taxsumme          LIKE bill.taxsumme         
    FIELD name              LIKE bill.name             
    FIELD billtyp           LIKE bill.billtyp          
    FIELD parent-nr         LIKE bill.parent-nr        
    FIELD restargt          LIKE bill.restargt         
    FIELD init-argt         LIKE bill.init-argt        
    FIELD rest-tage         LIKE bill.rest-tage        
    FIELD ums-kurz          LIKE bill.ums-kurz         
    FIELD ums-lang          LIKE bill.ums-lang         
    FIELD nextargt-bookdate LIKE bill.nextargt-bookdate
    FIELD roomcharge        LIKE bill.roomcharge       
    FIELD oldzinr           LIKE bill.oldzinr          
    FIELD t-rechnr          LIKE bill.t-rechnr         
    FIELD rechnr2           LIKE bill.rechnr2          
    FIELD betriebsnr        LIKE bill.betriebsnr       
    FIELD vesrdep           LIKE bill.vesrdep          
    FIELD vesrdat           LIKE bill.vesrdat          
    FIELD vesrdepot         AS CHARACTER
    FIELD vesrdepot2        AS CHARACTER
    FIELD vesrcod           AS CHARACTER
    FIELD verstat           LIKE bill.verstat     
    FIELD kontakt-nr        LIKE bill.kontakt-nr  
    FIELD betrieb-gast      LIKE bill.betrieb-gast
    FIELD billref           LIKE bill.billref
    FIELD bl-recid          AS INTEGER.
DEFINE TEMP-TABLE t-bill-line   LIKE bill-line
    FIELD bl-recid  AS INTEGER
    FIELD artart    AS INTEGER
    FIELD tool-tip  AS CHAR
    FIELD serv      AS DECIMAL FORMAT "->,>>>,>>>,>>9" 
    FIELD vat       AS DECIMAL FORMAT "->,>>>,>>>,>>9" 
    FIELD netto     AS DECIMAL FORMAT "->,>>>,>>>,>>9" 
    FIELD art-type  AS INTEGER
.
DEFINE TEMP-TABLE spbill-list 
    FIELD selected AS LOGICAL INITIAL YES 
    FIELD bl-recid AS INTEGER. 

DEFINE INPUT PARAMETER bil-recid        AS INTEGER.
DEFINE INPUT PARAMETER foreign-rate     AS LOGICAL. 
DEFINE INPUT PARAMETER double-currency  AS LOGICAL INITIAL NO. 
DEFINE INPUT PARAMETER ba-dept          AS INTEGER.

DEFINE OUTPUT PARAMETER invno           AS CHAR.
DEFINE OUTPUT PARAMETER gname           AS CHAR.
DEFINE OUTPUT PARAMETER resname         AS CHAR.
DEFINE OUTPUT PARAMETER rescomment      AS CHAR.
DEFINE OUTPUT PARAMETER printed         AS CHAR.
DEFINE OUTPUT PARAMETER rechnr          AS DECIMAL.
DEFINE OUTPUT PARAMETER balance         AS DECIMAL.
DEFINE OUTPUT PARAMETER balance-foreign AS DECIMAL.
DEFINE OUTPUT PARAMETER kreditlimit     AS DECIMAL.
DEFINE OUTPUT PARAMETER enbtn-bareserve AS LOGICAL. 
DEFINE OUTPUT PARAMETER guest-taxcode   AS CHAR. /*ragung add guest-taxcode for web*/

DEFINE OUTPUT PARAMETER TABLE FOR t-bill-line. 
DEFINE OUTPUT PARAMETER TABLE FOR t-bill. 

DEFINE VARIABLE curr-select  AS CHAR.
DEFINE VARIABLE telbill-flag AS LOGICAL NO-UNDO.
DEFINE VARIABLE babill-flag  AS LOGICAL NO-UNDO.
DEFINE VARIABLE curr-gname   AS CHAR INITIAL "". 
DEFINE VARIABLE curr-invno   AS INTEGER. 
DEFINE VARIABLE curr-b-recid AS INTEGER. 
DEFINE VARIABLE art-no       AS INTEGER  NO-UNDO.

curr-select = "".
FIND FIRST bill WHERE RECID(bill) = bil-recid NO-LOCK NO-ERROR.
IF NOT AVAILABLE bill THEN RETURN. /*FT serverless*/
RUN read-bill2bl.p (5, bil-recid, ?, ?, ?, ?, ?, ?, ?, ?,
OUTPUT telbill-flag, OUTPUT babill-flag, OUTPUT TABLE t-bill).
FIND FIRST t-bill NO-ERROR.
    
ASSIGN
  invno         = STRING(t-bill.rechnr) 
  curr-invno    = t-bill.rechnr 
  curr-gname    = gname
  curr-b-recid  = bil-recid
.

RUN read-guestbl.p(1, t-bill.gastnr, ?, ?, OUTPUT TABLE t-guest).
FIND FIRST t-guest NO-LOCK. 
ASSIGN
    resname = t-guest.name + ", " + t-guest.vorname1 + t-guest.anredefirma 
          + " " + t-guest.anrede1 
          + chr(10) + t-guest.adresse1 
          + chr(10) + t-guest.wohnort + " " + t-guest.plz 
          + chr(10) + t-guest.land
    rescomment = t-guest.bemerk
    art-no     = t-guest.zahlungsart
    guest-taxcode = STRING(t-guest.firmen-nr)
    . 

IF t-bill.bilname NE "" AND t-bill.NAME NE t-bill.bilname THEN
    rescomment = "Guest Name: " + 
                 t-bill.bilname + CHR(10) + rescomment.

IF t-bill.vesrdepot NE "" THEN
ASSIGN
/*       rescomment:BGCOL IN FRAME frame1 = 12 */
/*       rescomment:FGCOL IN FRAME frame1 = 15 */
  rescomment = rescomment + CHR(10) + t-bill.vesrdepot + CHR(10)
    . 
/*     ELSE                                   */
/*     ASSIGN                                 */
/*       rescomment:BGCOL IN FRAME frame1 = 8 */
/*       rescomment:FGCOL IN FRAME frame1 = 0 */
/*     .                                      */

IF t-bill.rgdruck = 0 THEN printed = "". 
ELSE printed = "*". 
rechnr  = t-bill.rechnr. 
balance = t-bill.saldo. 
IF double-currency OR foreign-rate THEN balance-foreign = t-bill.mwst[99]. 
IF t-guest.kreditlimit NE 0 THEN kreditlimit = t-guest.kreditlimit. 
ELSE 
DO: 
    RUN read-htparambl.p (1, 68, ?, OUTPUT TABLE t-htparam).
    FIND FIRST t-htparam NO-LOCK. 
    IF t-htparam.fdecimal NE 0 THEN kreditlimit = t-htparam.fdecimal. 
    ELSE kreditlimit = t-htparam.finteger. 
END. 
/* IF balance LE kreditlimit THEN bcol = 2. */
/* ELSE bcol = 12.                          */

FOR EACH spbill-list: 
    DELETE spbill-list. 
END. 

RUN disp-bill-line(YES). 

IF t-bill.flag = 0 AND t-bill.rechnr > 0 AND t-bill.billtyp = ba-dept AND (t-bill.rechnr NE int(invno)) THEN 
DO: 
    RUN read-bk-veranbl.p (3, ?, ?, t-bill.rechnr, 0, OUTPUT TABLE t-bk-veran).
    FIND FIRST t-bk-veran NO-LOCK NO-ERROR. 
    IF AVAILABLE t-bk-veran THEN 
    DO: 
        RUN read-bk-reserbl.p (4, t-bk-veran.veran-nr, ?, 1, ?, OUTPUT TABLE t-bk-reser).
        FIND FIRST t-bk-reser NO-LOCK NO-ERROR. 
        IF AVAILABLE t-bk-reser THEN enbtn-bareserve = YES.
        ELSE enbtn-bareserve = NO. 
    END. 
END. 
ELSE enbtn-bareserve = NO. 

PROCEDURE disp-bill-line: 
    DEF INPUT PARAMETER read-flag AS LOGICAL NO-UNDO.
    
    IF read-flag THEN
    RUN read-bill-line-cldbl.p (3, 1, t-bill.rechnr, ?, ?, ?, ?, ?,OUTPUT TABLE t-bill-line).
    FOR EACH t-bill-line NO-LOCK :
        FIND FIRST spbill-list WHERE spbill-list.bl-recid = t-bill-line.bl-recid NO-LOCK NO-ERROR. 
        IF NOT AVAILABLE spbill-list THEN 
        DO: 
            CREATE spbill-list. 
            ASSIGN 
            spbill-list.selected = NO 
            spbill-list.bl-recid = t-bill-line.bl-recid. 
        END.
    END.
/*             OPEN QUERY q1 FOR EACH t-bill-line NO-LOCK,                     */
/*         FIRST spbill-list WHERE spbill-list.bl-recid = t-bill-line.bl-recid */
/*         BY t-bill-line.sysdate DESC BY t-bill-line.zeit DESC.               */
END. 
