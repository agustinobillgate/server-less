
DEF TEMP-TABLE t-paramtext   LIKE paramtext.

DEF INPUT PARAMETER case-type     AS INTEGER.
DEF INPUT PARAMETER TABLE         FOR t-paramtext.
DEF OUTPUT PARAMETER success-flag AS LOGICAL INITIAL NO.

FIND FIRST t-paramtext NO-ERROR.
IF NOT AVAILABLE t-paramtext THEN
    RETURN NO-APPLY.

CASE case-type :
    WHEN 1 THEN
    DO: 
        FIND FIRST paramtext WHERE
            paramtext.txtnr EQ t-paramtext.txtnr
            AND paramtext.number EQ t-paramtext.number
            AND paramtext.sprachcode EQ t-paramtext.sprachcode
          EXCLUSIVE-LOCK NO-ERROR.
        IF AVAILABLE paramtext THEN
        DO:
          BUFFER-COPY t-paramtext TO paramtext.
          FIND CURRENT paramtext NO-LOCK.
          success-flag = YES.
        END.
    END.
    WHEN 2 THEN
    DO:
        CREATE paramtext.
        BUFFER-COPY t-paramtext TO paramtext.
        success-flag = YES.
        FIND CURRENT paramtext NO-LOCK.
    END.
    WHEN 3 THEN /*add & modify*/
    DO:
        FOR EACH t-paramtext NO-LOCK:
            FIND FIRST paramtext WHERE paramtext.txtnr EQ t-paramtext.txtnr
                AND paramtext.number EQ t-paramtext.number
                AND paramtext.sprachcode EQ t-paramtext.sprachcode NO-LOCK NO-ERROR.
            IF NOT AVAILABLE paramtext THEN 
                FIND FIRST paramtext WHERE paramtext.txtnr EQ t-paramtext.betriebsnr
                    AND paramtext.number EQ t-paramtext.number
                    AND paramtext.sprachcode EQ t-paramtext.sprachcode NO-LOCK NO-ERROR.
            IF AVAILABLE paramtext THEN
            DO:
              FIND CURRENT paramtext EXCLUSIVE-LOCK.
              BUFFER-COPY t-paramtext TO paramtext.
              FIND CURRENT paramtext NO-LOCK.
              RELEASE paramtext.
              success-flag = YES.
            END.
            ELSE DO:
                CREATE paramtext.
                BUFFER-COPY t-paramtext TO paramtext.
                success-flag = YES.
                FIND CURRENT paramtext NO-LOCK.
            END.
        END.
    END.
    WHEN 4 THEN /* SY 05 JUL 2017: Overwrite happy hours */
    DO: 
        FIND FIRST paramtext WHERE
            paramtext.txtnr EQ t-paramtext.txtnr
          EXCLUSIVE-LOCK NO-ERROR.
        IF NOT AVAILABLE paramtext THEN CREATE paramtext.
        DO:
          BUFFER-COPY t-paramtext TO paramtext.
          FIND CURRENT paramtext NO-LOCK.
          success-flag = YES.
        END.
    END.
END CASE.


