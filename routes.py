from flask import Flask, render_template, request, redirect, url_for
from flask.ext import login
from utils.models import *
from flask.ext.security import login_required
import json
from datetime import *
import logging
import os

logger = logging.getLogger('SuperBets')
hdlr = logging.FileHandler('/var/tmp/SuperBets.log')
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
hdlr.setFormatter(formatter)
logger.addHandler(hdlr)
logger.setLevel(logging.WARNING)

app = Flask(__name__)


UPLOAD_FOLDER = './static/data/pics'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route('/fileupload/<uid>', methods=['GET', 'POST'])
def upload_file(uid):
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
            usr = User.select().where(User.id == uid).get()
            usr.image = file.filename
            usr.save()
            return "success"
    return "failure"

def init_login():
    login_manager = login.LoginManager()
    login_manager.init_app(app)

    # Creating user loader function
    @login_manager.user_loader
    def load_user(user_id):
        return User.select().where(User.id==user_id).get()

init_login()

@app.route('/')
def home():
    if login.current_user.is_authenticated():
        return login.redirect('/app')
    else:
        return render_template('login.html')

@app.route('/app')
@login_required
def appm():
    return render_template('app.html')

@app.route('/admin')
@login_required
def admin():
    return render_template('admin.html')

@app.route("/loginu/<uid>/<pwd>", methods=["GET", "POST"])
def loginu(uid, pwd):
    if User.select().where(User.email==uid, User.password==pwd).exists():
        login.login_user(User.select().where(User.email==uid).get())
        return login.current_user.type
    return "Wrong userid/password"

@app.route("/logout")
@login_required
def logout():
    login.logout_user()
    return render_template('login.html')

@app.route("/register/<name>/<uname>/<pwd>")
def register(name,uname,pwd):
    if User.select().where(User.uname==uname).exists():
        return "User Id already exists"
    User.create(name=name,uname=uname, password=pwd)
    if User.select().where(User.uname==uname).exists():
        return "Successfully registered. Sign in and start betting!"
    else:
        return "Something went wrong. Please contact Aravind!"



@app.route('/createform')
def createform():
    pr = Project.select().order_by(Project.id.desc()).get()
    form = Form.create(formstatus = "DRAFT",createdby = login.current_user.id, reportdate = date.today(), project = pr)
    for k in Key.select():
        keyins = Keyinstance.create(keyid=k.id,formid=form.id)
    return str(form.id)



@app.route('/form/<fid>')
def form(fid):
    form = Form.select().where(Form.id == fid).get()
        #pass
    return render_template('addnew.html',form=form)


@app.route('/saveReportDate/<fid>/<m>/<d>/<y>')
def saveReportDate(fid,m,d,y):
     if Form.select().where(Form.id == fid).exists():
        form = Form.select().where(Form.id == fid).get()
        form.reportdate = date(int(y),int(m),int(d))
        form.save()

     return 'suc'

@app.route('/saveDate/<did>/<m>/<d>/<y>/<type>/<field>')
def saveDate(did,m,d,y,type,field):
    if type == 'milestone':
        ms = Milestone.select().where(Milestone.id == did).get()
        if field == 'planneddate':
            ms.baseline = date(int(y),int(m),int(d))
            ms.save()
        elif field == 'actualdate':
            ms.current = date(int(y),int(m),int(d))
            ms.save()
    if type == 'issue':
        isd = Issue.select().where(Issue.id == did).get()
        if field == 'duedate':
            isd.resdate = date(int(y),int(m),int(d))
            isd.save()
    return 'suc'

@app.route('/getReportDate/<fid>')
def getReportDate(fid):
     if Form.select().where(Form.id == fid).exists():
        form = Form.select().where(Form.id == fid).get()
        l=str(form.reportdate).split('-')
        return l[1]+"-"+l[2]+"-"+l[0]






@app.route('/chooseproject')
def choose():
    return render_template('choose.html')

@app.route('/getMgrProjects/<uid>')
def getMgrProjects(uid):
    plist = []
    user = User.select().where(User.id == uid).get()
    if Useracc.select().where(Useracc.userid == user,Useracc.type=='MGR-PROJ').exists():
        for a in Useracc.select().where(Useracc.userid == user,Useracc.type=='MGR-PROJ'):
            proj = Project.select().where(Project.id == a.projectid.id).get()
            plist.append({"name":proj.pname,"id":proj.id})
    return json.dumps(plist)

@app.route('/getFormKeys/<fid>')
def formkeys(fid):
    kl=[]
    for ki in Keyinstance.select().where(Keyinstance.formid == fid):
        k = Key.select().where(Key.id == ki.keyid).get()
        kl.append({"kiid":ki.id,"kival":ki.keyval,"keyname":k.keyname,"keyfname":k.keydescr,"keycom":ki.keycomments,"keyldescr":k.longdescr})
    return json.dumps(kl)


@app.route('/saveKeyInstVal/<kiid>/<val>')
def saveKeyInstVal(kiid,val):
    keyi = Keyinstance.select().where(Keyinstance.id == kiid).get()
    keyi.keyval = val
    keyi.save()
    return 'suc'

@app.route('/saveComment/<kiid>/<val>')
def saveComment(kiid,val):
    keyi = Keyinstance.select().where(Keyinstance.id == kiid).get()
    keyi.keycomments = val
    keyi.save()
    return 'suc'

@app.route('/addIssueRec/<fid>')
def addIssueRec(fid):
    resd=""
    isr = Issue.create(formid = fid,issuedescr=' ',action=' ',owner=' ',itype="IS",status="OP")
    isro = Issue.select().where(Issue.id == isr.id).get()
    if len(str(isro.resdate)) > 4:
        l=str(isro.resdate).split('-')
        resd=l[1]+"-"+l[2]+"-"+l[0]
    return json.dumps({"isrid":isro.id,"descr":isro.issuedescr,"itype":isro.itype,"action":isro.action,"owner":isro.owner,"duedate":resd,"status":isro.status})


@app.route('/addMilestoneRec/<fid>')
def addMilestoneRec(fid):
    mst = Milestone.create(formid = fid,mdescr = ' ',comments='NS',planperc=0)
    mst = Milestone.select().where(Milestone.id == mst.id).get()
    return json.dumps({"mstid":mst.id,"descr":mst.mdescr,"planneddate":mst.baseline,"actualdate":mst.current,"status":mst.comments,"original":mst.planperc})


@app.route('/getIssueRecs/<fid>')
def getIssueRec(fid):
    ilist =[]
    resd=""

    for isro in Issue.select().where(Issue.formid == fid):
        if len(str(isro.resdate)) > 4:
            l=str(isro.resdate).split('-')
            resd=l[1]+"-"+l[2]+"-"+l[0]
        ilist.append({"isrid":isro.id,"descr":isro.issuedescr,"itype":isro.itype,"action":isro.action,"owner":isro.owner,"duedate":resd,"status":isro.status})
    return json.dumps(ilist)

@app.route('/getMilestoneRecs/<fid>')
def getMilestoneRecs(fid):
    mlist =[]
    for mst in Milestone.select().where(Milestone.formid == fid):
        bsl=""
        crn=""
        if len(str(mst.baseline)) > 4:
            l=str(mst.baseline).split('-')
            bsl=l[1]+"-"+l[2]+"-"+l[0]
        if len(str(mst.current)) > 4:
            l=str(mst.current).split('-')
            crn=l[1]+"-"+l[2]+"-"+l[0]
        mlist.append({"mstid":mst.id,"descr":mst.mdescr,"planneddate":bsl,"actualdate":crn,"status":mst.comments,"original":mst.planperc})
    return json.dumps(mlist)

@app.route('/saveIssueRec/<rid>/<t>/<s>/<d>/<a>/<o>/') #/<p>/<o>/<a>/<r>
def saveIssueRec(rid,t,s,d,a,o):  #,p,o,a,r
    isr = Issue.select().where(Issue.id == rid).get()
    isr.issuedescr=d
    isr.itype=t
    isr.status=s
    isr.owner=o
    isr.action=a
    isr.save()
    return 'suc'

@app.route('/saveMilestoneRec/<rid>/<d>/<s>/<o>') #/<p>/<o>/<a>/<r>
def saveMilestoneRec(rid,d,s,o):  #,p,o,a,r
    mst = Milestone.select().where(Issue.id == rid).get()
    mst.mdescr=d
    mst.planperc=o
    mst.comments=s
    mst.save()
    return 'suc'

@app.route('/updateProj/<fid>/<pid>')
def updateProj(fid,pid):
    form = Form.select().where(Form.id == fid).get()

    pr = Project.select().where(Project.id == pid).get()
    form.project = pr.id
    form.save()
    return str(pr.pname)

@app.route('/getFormProj/<fid>')
def getFormProj(fid):

    if Form.select().where(Form.id == fid).exists():
        form = Form.select().where(Form.id == fid).get()
        if Project.select().where(Project.id == form.project).exists():
            pr = Project.select().where(Project.id == form.project).get()
            ua = Useracc.select().where(Useracc.projectid == pr.id).get()
            u  = User.select().where(User.id == ua.userid).get()
            return json.dumps({"name":pr.pname,"manager":u.name,"version":pr.mnversion,"value":pr.value,"area":pr.parea,"golive":str(pr.golive),"phase":pr.phase})
        else:
            return 'na'
    else:
        return 'na'




@app.route('/getProjects/<uid>')
def getProjects(uid):

    plist = [];
    if Useracc.select().where(Useracc.userid == uid).exists():
        for u in Useracc.select().where(Useracc.userid == uid):
            pr = Project.select().where(Project.id == u.projectid).get()
            flist =[]
            for f in Form.select().where(Form.project == pr).order_by(Form.reportdate.desc()):
                ky = Key.select().where(Key.keyname == 'cws').get()
                kyi = Keyinstance.select().where(Keyinstance.keyid == ky.id,Keyinstance.formid == f.id).get()
                ref= str(f.reportdate).split('-')
                ref = ref[1]+'-'+ref[2]+"-"+ref[0]
                flist.append({"fid":f.id,"pid":pr.id,"pname":pr.pname,"status":kyi.keyval,"date":ref,"formstatus":f.formstatus})
            plist.append({"name":pr.pname,"forms":flist})


    return json.dumps(plist)



@app.route('/getAdminReports')
def getAdminReports():
    flist =[]
    for f in Form.select().where(Form.project != None).order_by(Form.reportdate.desc()):
        ky = Key.select().where(Key.keyname == 'cws').get()
        kyi = Keyinstance.select().where(Keyinstance.keyid == ky.id,Keyinstance.formid == f.id).get()
        ref= str(f.reportdate).split('-')
        ref = ref[1]+'-'+ref[2]+"-"+ref[0]
        pr = Project.select().where(Project.id == f.project).get()
        flist.append({"fid":f.id,"pid":pr.id,"pname":pr.pname,"status":kyi.keyval,"date":ref,"formstatus":f.formstatus})

    return json.dumps(flist)





@app.route('/currentWeek')
def getCurrentWeekReports():

    plist=[]

    for pr in Project.select():
                ua = Useracc.select().where(Useracc.projectid == pr.id).get()
                u  = User.select().where(User.id == ua.userid).get()
                plist.append({"name":pr.pname,"manager":u,"version":pr.mnversion,"value":pr.value,"area":pr.parea,"golive":pr.golive,"phase":pr.phase})

    return json.dumps(plist)


@app.route('/addProjectWithDetails/<pn>/<pvalue>/<version>/<pmgr>/<pmd>/<ptype>/<pphase>/<gld>/')
def addProjectWithDetails(pn,pvalue,version,pmgr,pmd,ptype,pphase,gld):
    pm = User.select().where(User.id == pmgr).get()
    gldl = gld.split("-")
    gd = date(int(gldl[2]),int(gldl[0]),int(gldl[1]))
    pr = Project.create(pname=pn,value=pvalue,mnversion=version,parea=ptype,smi=pphase,gld=gd)
    Useracc.create(projectid = pr.id,userid = pm.id,type="MGR-PROJ",dateadded = date.today())
    return 'suc'


@app.route('/addProject')
def addProject():
    pr = Project.create(pname="Project name",value="0",mnversion="5.4",phase='Inception',parea='AS',smi='LS')
    return json.dumps(str(pr))



@app.route('/getManagers')
def getManagers():
    mgrlist = []
    for mgr in User.select().where(User.type=='MGR'):
        mgrlist.append({"id":mgr.id,"name":mgr.name});

    return json.dumps(mgrlist)

@app.route('/getManagerNames')
def getManagerNames():
    mgrlist = []
    for mgr in User.select().where(User.type=='MGR'):
        mgrlist.append(mgr.name);

    return json.dumps(mgrlist)

@app.route('/getAdminProjects')
def getAdminProjects():
    palist = []
    mgrname=""
    for p in Project.select().order_by(Project.id.desc()):
        if Useracc.select().where(Useracc.projectid == p.id, Useracc.type == 'MGR-PROJ').exists():
            ua = Useracc.select().where(Useracc.projectid == p.id, Useracc.type == 'MGR-PROJ').get()
            u = User.select().where(User.id == ua.userid).get()
            mgrname = u.name

        palist.append({"pid":p.id,"name":p.pname,"phase":p.phase,"dept":p.parea,"smi":p.smi,"golive":str(p.golive),"value":p.value,"version":p.mnversion,"manager":mgrname})

    return json.dumps(palist)

@app.route('/saveProjectParam/<pid>/<paramname>/<val>')
def saveProjectParam(pid,paramname,val):
    if paramname != 'manager':
        pr = Project.select().where(Project.id == pid).get()
        #Project.update(''+paramname+'' = val).where(Project.id == pid)
        pru = "update project set "+paramname+" = '"+val+"' where id ="+pid
        db.execute_sql(pru)
        return 'suc'+paramname
    else:
        u = User.select().where(User.name == val).get()
        pr = Project.select().where(Project.id == pid).get()
        ua = Useracc.create(projectid = pr.id,userid = u.id, type = 'MGR-PROJ')
        return 'suc'





# set the secret key.  keep this really secret:
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'


if __name__ == '__main__':
  app.run(debug=True)
