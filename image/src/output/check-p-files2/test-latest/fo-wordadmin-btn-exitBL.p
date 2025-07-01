DEF TEMP-TABLE t-brief LIKE brief.

DEF INPUT  PARAMETER TABLE FOR t-brief.
DEF INPUT  PARAMETER case-type    AS INTEGER.
DEF INPUT  PARAMETER last-column  AS CHAR.
DEF INPUT  PARAMETER kateg        AS INTEGER.
DEF INPUT  PARAMETER user-init    AS CHAR.       /*add input userinit - william C3D765 16-06-23*/
DEF OUTPUT PARAMETER success-flag AS LOGICAL INIT NO.


DEFINE VARIABLE v-log AS LOGICAL.
DEF VAR ChCol   AS CHAR EXTENT 52 INITIAL
    ["A","B","C","D","E","F","G","H","I","J","K","L","M",
     "N","O","P","Q","R","S","T","U","V","W","X","Y","Z",
     "AA","AB","AC","AD","AE","AF","AG","AH","AI","AJ","AK","AL","AM",
     "AN","AO","AP","AQ","AR","AS","AT","AU","AV","AW","AX","AY","AZ"].


FIND FIRST t-brief.
IF case-type = 1 THEN   /* add */
DO:
    CREATE brief. 
    RUN fill-brief.
    success-flag = YES.
END.
ELSE IF case-type = 2 THEN   /* chg */
DO:
    FIND FIRST brief WHERE brief.briefnr = t-brief.briefnr EXCLUSIVE-LOCK. 
    IF AVAILABLE brief THEN
    DO:
        RUN fill-brief.
        success-flag = YES.
    END.
END.



PROCEDURE fill-brief: 
DEF VAR ind AS INTEGER.
RUN get-columnno(INPUT last-column, OUTPUT ind).
  IF case-type EQ 2 THEN                                                                                /*start*//*add system log changed input - william C3D765 16-06-23*/
    DO:        
        IF TRIM(brief.briefbezeich) NE TRIM(t-brief.briefbezeich)
            OR brief.fname      NE t-brief.fname
            OR brief.ftyp       NE ind
            OR brief.etk-anzahl NE t-brief.etk-anzahl THEN
        DO:
            v-log = YES.
        END.

        IF v-log THEN
        DO:
            FIND FIRST bediener WHERE bediener.userinit EQ user-init NO-LOCK NO-ERROR.

            CREATE res-history.
            ASSIGN
                res-history.nr          = bediener.nr
                res-history.datum       = TODAY
                res-history.zeit        = TIME
                res-history.action      = "F/O Excel Program Setup"
                res-history.aenderung   = "Modify FileNo " + STRING(brief.briefnr) + " => "
                .

            IF TRIM(brief.briefbezeich) NE TRIM(t-brief.briefbezeich) THEN
            DO:
                res-history.aenderung = res-history.aenderung + brief.briefbezeich 
                    + " to " + t-brief.briefbezeich + ";".
            END.
            IF brief.fname NE t-brief.fname THEN
            DO:
                res-history.aenderung = res-history.aenderung + "NameFile " + STRING(brief.fname)
                    + " to " + STRING(t-brief.fname) + ";".
            END.
            IF brief.ftyp NE ind THEN
            DO:
                res-history.aenderung = res-history.aenderung + "Lastcolomn " + STRING(brief.ftyp)
                    + " to " + STRING(ind) + ";".
            END.
            IF brief.etk-anzahl NE t-brief.etk-anzahl THEN
            DO:
                res-history.aenderung = res-history.aenderung + "Lastrow " + STRING(brief.etk-anzahl)
                    + " to " + STRING(t-brief.etk-anzahl) + ";".
            END.
        END.                                                                                             /*end*/
    END.
  
  ASSIGN
    brief.briefnr       = t-brief.briefnr 
    brief.briefbezeich  = t-brief.briefbezeich 
    brief.fname         = t-brief.fname
    brief.briefkateg    = kateg
    brief.ftyp          = ind
    brief.etk-anzahl    = t-brief.etk-anzahl
  .
END. 


PROCEDURE get-columnNo:
DEF INPUT PARAMETER last-column AS CHAR.
DEF OUTPUT PARAMETER ind        AS INTEGER INITIAL 1.
DEF VAR i                       AS INTEGER.
DEF VAR ind1                    AS INTEGER.
DEF VAR ind2                    AS INTEGER. 
  IF LENGTH(last-column) = 2 THEN   /*FT130513*/
  DO:
    DO i = 1 TO 26:
      IF chCol[i] = SUBSTRING(last-column,1,1) THEN ind1 = i * 26.
    END.
    DO i = 1 TO 26:
      IF chCol[i] = SUBSTRING(last-column,2,1) THEN  ind2 = i.
    END.
    ind = ind1 + ind2.
  END.
  ELSE 
    DO i = 1 TO 26:
      IF chCol[i] = last-column THEN
      DO:
        ind = i.
        RETURN.
      END.
    END.
END.
