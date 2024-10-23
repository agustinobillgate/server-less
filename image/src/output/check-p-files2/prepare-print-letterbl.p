DEF TEMP-TABLE q1-list  
    FIELD resnr          LIKE reservation.resnr  
    FIELD grpflag        LIKE reservation.grpflag  
    FIELD gastnr         LIKE reservation.gastnr  
    FIELD name           LIKE guest.name  
    FIELD vorname1       LIKE guest.vorname1  
    FIELD anrede1        LIKE guest.anrede1  
    FIELD anredefirma    LIKE guest.anredefirma  
    FIELD briefnr        LIKE reservation.briefnr  
    FIELD ankunft        LIKE res-line.ankunft  
    FIELD anztage        LIKE res-line.anztage  
    FIELD abreise        LIKE res-line.abreise  
    FIELD kurzbez        LIKE zimkateg.kurzbez  
    FIELD resstatus      LIKE res-line.resstatus  
    FIELD groupname      LIKE reservation.groupname  
    FIELD activeflag     LIKE reservation.activeflag
/*gerald 19BC08*/
    FIELD roomrate       AS DECIMAL FORMAT "->,>>>,>>>,>>>,>>9.99"
    FIELD room-night     AS INTEGER
    FIELD bedsetup       AS CHARACTER.

  
DEF INPUT PARAMETER last-sort AS INTEGER.  
DEF INPUT PARAMETER fdate     AS DATE.  
DEF INPUT PARAMETER lname     AS CHAR.  
DEF OUTPUT PARAMETER ci-date  AS DATE.  
DEF OUTPUT PARAMETER briefnr  AS INTEGER.  
DEF OUTPUT PARAMETER TABLE FOR q1-list.  
  
FIND FIRST htparam WHERE htparam.paramnr = 87 NO-LOCK.   
ci-date = htparam.fdate.   
FIND FIRST htparam WHERE htparam.paramnr = 435 NO-LOCK.   
briefnr = htparam.finteger.  
  
RUN print-letter-disp-arlistbl.p(last-sort, fdate, lname, OUTPUT TABLE q1-list).  
