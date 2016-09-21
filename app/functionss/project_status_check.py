from app import app, db
from app.models import project, hardwareSetup

def project_check(projectId):
	prjct = project.Project.query.get(projectId)
	if not prjct.hwsetupId:
		prjct.status = 'incomplete'
	else:
		hwsetupStatus = hardwareSetup.HardwareSetup.query.get(prjct.hwsetupId).status
		if not hwsetupStatus == 'success':
			prjct.status = 'incomplete'
		else:
			prjct.status = 'complete'

	db.session.commit()
