from dbConn import orcl
from flask import jsonify

with orcl() as db:
  def getProjects(environment):
    sql = "SELECT \'<a vlink=\"#551A8B\" href=\"https://phire.uc.edu/\' || PHI_CR_NUM || \'\" target=\"_blank\">\' || PHI_CR_NUM || \'</a>\', PHI_CR_TYPE, PHI_CR_STATUS, PHI_TITLE"
    sql = sql + " FROM PS_PHI_CR_TBL"
    sql = sql + " WHERE PHI_CR_TYPE IN (\'QRY\',\'PROJ\')"
    ## Conditional logic based on environment... This is not the best way but its lazy and should work
    if environment == 'TESTC':
      sql = sql + " AND PHI_CR_STATUS IN (\'MIGC\',\'MIGB\',\'MIGU\', \'MIGZ\', \'MIGP\',\'TSTC\', \'TSTB\', \'TSTP\', \'TSTU\', \'APVP\')"
    elif environment == 'TESTB':
      sql = sql + " AND PHI_CR_STATUS IN (\'MIGB\',\'MIGU\', \'MIGZ\', \'MIGP\',\'TSTB\', \'TSTP\', \'TSTU\', \'APVP\')"
    else:
      sql = sql + " AND PHI_CR_STATUS IN (\'MIGU\', \'MIGZ\', \'MIGP\', \'TSTP\', \'TSTU\', \'APVP\')"
    issues = db.dbExecuteFetchAll(sql)
    return jsonify(issues)
