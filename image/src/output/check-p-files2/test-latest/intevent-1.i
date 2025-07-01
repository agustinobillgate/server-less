/* intevent.i  1.0         Larry Barnhill jr.     07/09/95 */

DO TRANSACTION:
  CREATE interface.
  ASSIGN
    interface.key         = {1}
    interface.zinr        = {3}
    interface.nebenstelle = {5}
    interface.intfield    = {6}
    interface.decfield    = {2}
    interface.int-time    = TIME
    interface.intdate     = TODAY
    interface.parameters  = {4}
    interface.resnr       = {7}
    interface.reslinnr    = {8}
  .
  FIND CURRENT interface NO-LOCK.
  RELEASE interface.
END. /* ... DO TRANSACTION */
