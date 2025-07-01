/* Oscar - User for VHP Cloud only */
DEFINE TEMP-TABLE sartnr-list
    FIELD artnr         LIKE l-artikel.artnr
    FIELD bezeich       LIKE l-artikel.bezeich
    FIELD anz-anf-best  LIKE l-bestand.anz-anf-best
    FIELD anz-eingang   LIKE l-bestand.anz-eingang 
    FIELD anz-ausgang   LIKE l-bestand.anz-ausgang
    FIELD masseinheit   LIKE l-artikel.masseinheit
    FIELD is-receipt    AS LOGICAL /* Oscar - 6C220A */
    FIELD hrecipe-nr    AS INTEGER. /* Oscar - 6C220A */

DEFINE INPUT PARAMETER curr-lager       AS INT      NO-UNDO.
DEFINE INPUT PARAMETER recipe           AS LOGICAL  NO-UNDO.
DEFINE INPUT PARAMETER sorttype         AS INT      NO-UNDO.
DEFINE INPUT PARAMETER s-artnr          AS INT      NO-UNDO.
DEFINE INPUT PARAMETER s-bezeich        AS CHAR     NO-UNDO.
DEFINE OUTPUT PARAMETER TABLE FOR sartnr-list.


IF curr-lager = 0 THEN 
DO: 
    IF sorttype = 1 THEN 
    DO: 
      FOR EACH l-artikel WHERE l-artikel.artnr GE s-artnr 
          NO-LOCK BY l-artikel.artnr:

          CREATE sartnr-list.
          BUFFER-COPY l-artikel TO sartnr-list.
          sartnr-list.is-receipt = NO. /* Oscar - 6C220A */
          sartnr-list.hrecipe-nr = 0. /* Oscar - 6C220A */
      END.
    END. 
    ELSE 
    DO: 
      IF SUBSTR(s-bezeich,1,1) NE "*" THEN 
        FOR EACH l-artikel WHERE l-artikel.bezeich 
            GE s-bezeich NO-LOCK BY l-artikel.bezeich:
              
            CREATE sartnr-list.
            BUFFER-COPY l-artikel TO sartnr-list.
            sartnr-list.is-receipt = NO. /* Oscar - 6C220A */
            sartnr-list.hrecipe-nr = 0. /* Oscar - 6C220A */
        END.
      ELSE 
      DO: 
        IF SUBSTR(s-bezeich,length(s-bezeich),1) NE "*" THEN 
        s-bezeich = s-bezeich + "*". 
        FOR EACH l-artikel WHERE l-artikel.bezeich 
            MATCHES(s-bezeich) NO-LOCK BY l-artikel.bezeich:

            CREATE sartnr-list.
            BUFFER-COPY l-artikel TO sartnr-list.
            sartnr-list.is-receipt = NO. /* Oscar - 6C220A */
            sartnr-list.hrecipe-nr = 0. /* Oscar - 6C220A */
        END.
      END. 
    END. 
    RETURN.
END. 

IF NOT recipe THEN 
DO: 
    IF sorttype = 1 THEN 
    DO: 
      FOR EACH l-artikel WHERE l-artikel.artnr GE s-artnr NO-LOCK, 
          FIRST l-bestand WHERE l-bestand.artnr = l-artikel.artnr 
          AND l-bestand.lager-nr = curr-lager NO-LOCK BY l-artikel.artnr:

          CREATE sartnr-list.
          BUFFER-COPY l-artikel TO sartnr-list.
          BUFFER-COPY l-bestand TO sartnr-list.
          sartnr-list.is-receipt = NO. /* Oscar - 6C220A */
          sartnr-list.hrecipe-nr = 0. /* Oscar - 6C220A */
      END.
    END. 
    ELSE 
    DO: 
      IF SUBSTR(s-bezeich,1,1) NE "*" THEN 
        FOR EACH l-artikel WHERE l-artikel.bezeich GE s-bezeich NO-LOCK, 
            FIRST l-bestand WHERE l-bestand.artnr = l-artikel.artnr 
            AND l-bestand.lager-nr = curr-lager NO-LOCK BY l-artikel.bezeich:

            CREATE sartnr-list.
            BUFFER-COPY l-artikel TO sartnr-list.
            BUFFER-COPY l-bestand TO sartnr-list.
            sartnr-list.is-receipt = NO. /* Oscar - 6C220A */
            sartnr-list.hrecipe-nr = 0. /* Oscar - 6C220A */
        END.
      ELSE 
      DO: 
        IF SUBSTR(s-bezeich,length(s-bezeich),1) NE "*" THEN 
        s-bezeich = s-bezeich + "*". 
        FOR EACH l-artikel WHERE l-artikel.bezeich MATCHES(s-bezeich) NO-LOCK, 
            FIRST l-bestand WHERE l-bestand.artnr = l-artikel.artnr 
            AND l-bestand.lager-nr = curr-lager NO-LOCK BY l-artikel.bezeich:

            CREATE sartnr-list.
            BUFFER-COPY l-artikel TO sartnr-list.
            BUFFER-COPY l-bestand TO sartnr-list.
            sartnr-list.is-receipt = NO. /* Oscar - 6C220A */
            sartnr-list.hrecipe-nr = 0. /* Oscar - 6C220A */
        END.
      END. 
    END. 
END. 
ELSE 
DO: 
    IF sorttype = 1 THEN 
    DO: 
      FOR EACH l-artikel WHERE l-artikel.artnr GE s-artnr 
        AND l-artikel.betriebsnr NE 0 NO-LOCK BY l-artikel.artnr:
           
        CREATE sartnr-list.
        BUFFER-COPY l-artikel TO sartnr-list.
        /*BUFFER-COPY l-bestand TO sartnr-list.*/
        sartnr-list.is-receipt = YES. /* Oscar - 6C220A */
        sartnr-list.hrecipe-nr = l-artikel.betriebsnr. /* Oscar - 6C220A */
      END.
    END. 
    ELSE 
    DO: 
      FOR EACH l-artikel WHERE l-artikel.bezeich GE s-bezeich 
        AND l-artikel.betriebsnr NE 0 NO-LOCK BY l-artikel.bezeich:

        CREATE sartnr-list.
        BUFFER-COPY l-artikel TO sartnr-list.
        /*BUFFER-COPY l-bestand TO sartnr-list.*/
        sartnr-list.is-receipt = YES. /* Oscar - 6C220A */
        sartnr-list.hrecipe-nr = l-artikel.betriebsnr. /* Oscar - 6C220A */
      END.
    END. 
END. 
