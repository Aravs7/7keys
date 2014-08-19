from flask import Flask, render_template, request, redirect, url_for
from flask.ext import login
from utils.models import *
from flask.ext.security import login_required
import json
from datetime import *
import logging
import os
from subtest.subroutes import subapp


logger = logging.getLogger('SuperBets')
hdlr = logging.FileHandler('/var/tmp/SuperBets.log')
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
hdlr.setFormatter(formatter)
logger.addHandler(hdlr)
logger.setLevel(logging.WARNING)

app = Flask(__name__)
app.register_blueprint(subapp);


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
@login_required
def createform():
    pr = Project.select().order_by(Project.id.desc()).get()

    recformexists = 0
    form=""

    #get the most recent form if available
    if Form.select().where(Form.createdby == login.current_user.id).exists():
        recformexists = 1
        recform = Form.select().where(Form.createdby == login.current_user.id).order_by(Form.id.desc()).get()


    if recformexists == 0:
        form = Form.create(formstatus = "DRAFT",createdby = login.current_user.id, reportdate = date.today(), project = pr)
        for k in Key.select():
                keyins = Keyinstance.create(keyid=k.id,formid=form.id)
    else:
        form = Form.create(project = recform.project,formstatus = 'DRAFT',createdby=login.current_user.id, reportdate = date.today())
        # clone key instances
        if Keyinstance.select().where(Keyinstance.formid == recform.id).exists():
            prevweekstatus="null"
            prevweekcomments="null"
            for ki in Keyinstance.select().where(Keyinstance.formid == recform.id):
                Keyinstance.create(keyid=ki.keyid,formid=form.id,keyval=ki.keyval,keycomments=ki.keycomments)

            newki = Keyinstance.select().where(Keyinstance.formid == form.id, Keyinstance.keyid == 1).get()
            prevki = Keyinstance.select().where(Keyinstance.formid == recform.id, Keyinstance.keyid == 2).get()
            newki.keyval = prevki.keyval
            newki.keycomments = prevki.keycomments
            newki.save()



    return str(form.id)



@app.route('/form/<fid>')
@login_required
def form(fid):
    form = Form.select().where(Form.id == fid).get()
        #pass
    return render_template('addnew.html',form=form)


@app.route('/saveReportDate/<fid>/<m>/<d>/<y>')
@login_required
def saveReportDate(fid,m,d,y):
     if Form.select().where(Form.id == fid).exists():
        form = Form.select().where(Form.id == fid).get()
        form.reportdate = date(int(y),int(m),int(d))
        form.save()

     return 'suc'

@app.route('/saveDate/<did>/<m>/<d>/<y>/<type>/<field>')
@login_required
def saveDate(did,m,d,y,type,field):
    if type == 'milestone':
        ms = Milestone.select().where(Milestone.id == did).get()
        if field == 'planneddate':
            ms.baseline = date(int(y),int(m),int(d))
            ms.save()
        elif field == 'actualdate':
            ms.current = date(int(y),int(m),int(d))
            ms.save()
        elif field == 'originalplan':
            ms.planperc = date(int(y),int(m),int(d))
            ms.save()
    if type == 'issue':
        isd = Issue.select().where(Issue.id == did).get()
        if field == 'duedate':
            isd.resdate = date(int(y),int(m),int(d))
            isd.save()
    return 'suc'

@app.route('/getReportDate/<fid>')
@login_required
def getReportDate(fid):
     if Form.select().where(Form.id == fid).exists():
        form = Form.select().where(Form.id == fid).get()
        l=str(form.reportdate).split('-')
        return l[1]+"-"+l[2]+"-"+l[0]



@app.route('/chooseproject')
@login_required
def choose():
    return render_template('choose.html')

@app.route('/getMgrProjects/<uid>')
@login_required
def getMgrProjects(uid):
    plist = []
    user = User.select().where(User.id == uid).get()
    if Useracc.select().where(Useracc.userid == user,Useracc.type=='MGR-PROJ').exists():
        for a in Useracc.select().where(Useracc.userid == user,Useracc.type=='MGR-PROJ'):
            proj = Project.select().where(Project.id == a.projectid.id).get()
            plist.append({"name":proj.pname,"id":proj.id})
    return json.dumps(plist)

@app.route('/getFormKeys/<fid>')
@login_required
def formkeys(fid):
    kl=[]
    for ki in Keyinstance.select().where(Keyinstance.formid == fid):
        k = Key.select().where(Key.id == ki.keyid).get()
        kl.append({"kiid":ki.id,"kival":ki.keyval,"keyname":k.keyname,"keyfname":k.keydescr,"keycom":ki.keycomments,"keyldescr":k.longdescr})
    return json.dumps(kl)


@app.route('/saveKeyInstVal/<kiid>/<val>')
@login_required
def saveKeyInstVal(kiid,val):
    keyi = Keyinstance.select().where(Keyinstance.id == kiid).get()
    keyi.keyval = val
    keyi.save()
    return 'suc'

@app.route('/saveComment/<kiid>/<val>')
@login_required
def saveComment(kiid,val):
    keyi = Keyinstance.select().where(Keyinstance.id == kiid).get()
    keyi.keycomments = val
    keyi.save()
    return 'suc'

@app.route('/addIssueRec/<fid>')
@login_required
def addIssueRec(fid):
    resd=""
    isr = Issue.create(formid = fid,issuedescr=' ',action=' ',owner=' ',itype="IS",status="OP")
    isro = Issue.select().where(Issue.id == isr.id).get()
    if len(str(isro.resdate)) > 4:
        l=str(isro.resdate).split('-')
        resd=l[1]+"-"+l[2]+"-"+l[0]
    return json.dumps({"isrid":isro.id,"descr":isro.issuedescr,"itype":isro.itype,"action":isro.action,"owner":isro.owner,"duedate":resd,"status":isro.status})


@app.route('/deleteIssue/<isid>')
@login_required
def deleteIssue(isid):
    resd=""
    Issue.delete().where(Issue.id ==isid ).execute()
    return 'suc'

@app.route('/deleteMilestone/<msid>')
@login_required
def deleteMilestone(msid):
    resd=""
    Milestone.delete().where(Milestone.id ==msid ).execute()
    return 'suc'



@app.route('/addMilestoneRec/<fid>')
@login_required
def addMilestoneRec(fid):
    mst = Milestone.create(formid = fid,mdescr = ' ',comments='NS',planperc=0)
    mst = Milestone.select().where(Milestone.id == mst.id).get()
    return json.dumps({"mstid":mst.id,"descr":mst.mdescr,"planneddate":mst.baseline,"originalplan":mst.planperc,"actualdate":mst.current,"status":mst.comments,"original":mst.planperc})


@app.route('/getIssueRecs/<fid>')
@login_required
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
@login_required
def getMilestoneRecs(fid):
    mlist =[]
    for mst in Milestone.select().where(Milestone.formid == fid):
        bsl=""
        crn=""
        orp=""
        if len(str(mst.baseline)) > 4:
            l=str(mst.baseline).split('-')
            bsl=l[1]+"-"+l[2]+"-"+l[0]
        if len(str(mst.current)) > 4:
            l=str(mst.current).split('-')
            crn=l[1]+"-"+l[2]+"-"+l[0]
        if len(str(mst.planperc)) > 4:
            l=str(mst.planperc).split('-')
            orp=l[1]+"-"+l[2]+"-"+l[0]
        mlist.append({"mstid":mst.id,"descr":mst.mdescr,"planneddate":bsl,"actualdate":crn,"status":mst.comments,"orignalplan":orp})
    return json.dumps(mlist)

@app.route('/saveIssueRec/<rid>/<t>/<s>/<d>/<a>/<o>/') #/<p>/<o>/<a>/<r>
@login_required
def saveIssueRec(rid,t,s,d,a,o):  #,p,o,a,r
    isr = Issue.select().where(Issue.id == rid).get()
    isr.issuedescr=d
    isr.itype=t
    isr.status=s
    isr.owner=o
    isr.action=a
    isr.save()
    return 'suc'

@app.route('/saveMilestoneRec/<rid>/<d>/<s>') #/<p>/<o>/<a>/<r>
@login_required
def saveMilestoneRec(rid,d,s):  #,p,o,a,r
    mst = Milestone.select().where(Issue.id == rid).get()
    mst.mdescr=d
    #mst.planperc=o
    mst.comments=s
    mst.save()
    return 'suc'

@app.route('/updateProj/<fid>/<pid>')
@login_required
def updateProj(fid,pid):
    form = Form.select().where(Form.id == fid).get()

    pr = Project.select().where(Project.id == pid).get()
    form.project = pr.id
    form.save()
    return str(pr.pname)

@app.route('/getFormProj/<fid>')
@login_required
def getFormProj(fid):

    if Form.select().where(Form.id == fid).exists():
        form = Form.select().where(Form.id == fid).get()
        if Project.select().where(Project.id == form.project).exists():
            mdname=""
            pr = Project.select().where(Project.id == form.project).get()
            if Useracc.select().where(Useracc.projectid == pr.id,Useracc.type == 'MD-PROJ').exists():
                ua = Useracc.select().where(Useracc.projectid == pr.id,Useracc.type == 'MD-PROJ').get()
                u  = User.select().where(User.id == ua.userid).get()
                mdname= u.name
            return json.dumps({"pid":pr.id,"name":pr.pname,"md":mdname,"version":pr.mnversion,"value":pr.value,"area":pr.parea,"golive":str(pr.golive),"phase":pr.phase})
        else:
            return 'na'
    else:
        return 'na'




@app.route('/getProjects/<uid>')
@login_required
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
@login_required
def getAdminReports():
    flist =[]
    for f in Form.select().where(Form.project != None).order_by(Form.reportdate.desc()):
        ky = Key.select().where(Key.keyname == 'cws').get()
        kyi = Keyinstance.select().where(Keyinstance.keyid == ky.id,Keyinstance.formid == f.id).get()
        ref= str(f.reportdate).split('-')
        ref = ref[1]+'-'+ref[2]+"-"+ref[0]
        pr = Project.select().where(Project.id == f.project).get()
        #mgrname="**" +str(pr.id)+"**"+ str(Useracc.select().where(Useracc.projectid == pr, Useracc.type == 'MGR-PROJ').exists())
        #mdname="**" + str(pr.id)+"**"+ str(Useracc.select().where(Useracc.projectid == pr and Useracc.type == 'MD-PROJ').exists())
        mgrname=""
        mdname=""
        if Useracc.select().where(Useracc.projectid == pr.id, Useracc.type == 'MGR-PROJ').exists():
            mua = Useracc.select().where(Useracc.projectid == pr, Useracc.type == 'MGR-PROJ').get()
            mu = User.select().where(User.id == mua.userid).get()
            mgrname = Useracc.select().where(Useracc.projectid == pr, Useracc.type == 'MGR-PROJ').sql()
            mgrname = mu.name
        if Useracc.select().where(Useracc.projectid == pr, Useracc.type == 'MD-PROJ').exists():
            mdua = Useracc.select().where(Useracc.projectid == pr, Useracc.type == 'MD-PROJ').get()
            mdu = User.select().where(User.id == mdua.userid).get()
            mdname = mdu.name
        icount = Issue.select().where(Issue.formid == f.id).count()
        mcount = Milestone.select().where(Milestone.formid == f.id).count()
        flist.append({"fid":f.id,"pid":pr.id,"pname":pr.pname,"status":kyi.keyval,"date":ref,"formstatus":f.formstatus,"manager":mgrname,'md':mdname,"icount":icount,"mcount":mcount})
        #flist.append({"md":mdname})

    return json.dumps(flist)


@app.route('/getUsers')
@login_required
def getUsers():
    ulist=[]
    for u in User.select().where(User.type == 'MGR' or User.type == 'MD'):
        plist=[]

        if Useracc.select().where(Useracc.userid == u.id, Useracc.type == 'MGR-PROJ' or Useracc.type == 'MD-PROJ').exists():
            for ua in Useracc.select().where(Useracc.userid == u.id, Useracc.type == 'MGR-PROJ' or Useracc.type == 'MD-PROJ'):
                p = Project.select().where(Project.id == ua.projectid).get()
                plist.append(p.pname)

        ulist.append({'name':u.name,'role':u.type,'email':u.email, 'projects':plist})

    return json.dumps(ulist)



@app.route('/submitReport/<fid>/<phase>')
@login_required
def submitReport(fid,phase):
    f = Form.select().where(Form.id == fid).get()
    f.formstatus = 'SUBMITTED'

    pr = Project.select().where(Project.id == f.project).get()

    #create a snapshot of the project
    pinst = Projectinstance.create(project = pr,forform = f)
    pinst.form = f
    pinst.project = pr
    pinst.pobj = pr.pobj
    pinst.smi = pr.smi
    pinst.parea = pr.parea
    pinst.phase = phase
    pinst.golive = pr.golive
    pinst.mnversion = pr.mnversion
    pinst.value = pr.value
    pinst.dept = pr.dept
    pinst.save()
    f.save()

    return 'suc'

@app.route('/getFormStatus/<fid>')
@login_required
def getFormStatus(fid):
    f = Form.select().where(Form.id == fid).get()
    return f.formstatus



@app.route('/currentWeek')
@login_required
def getCurrentWeekReports():

    plist=[]

    for pr in Project.select():
                ua = Useracc.select().where(Useracc.projectid == pr.id).get()
                u  = User.select().where(User.id == ua.userid).get()
                plist.append({"name":pr.pname,"manager":u,"version":pr.mnversion,"value":pr.value,"area":pr.parea,"golive":pr.golive,"phase":pr.phase})

    return json.dumps(plist)


@app.route('/addProjectWithDetails/<pn>/<pvalue>/<version>/<pmgr>/<pmd>/<ptype>/<pphase>/<gld>/')
@login_required
def addProjectWithDetails(pn,pvalue,version,pmgr,pmd,ptype,pphase,gld):
    pm = User.select().where(User.id == pmgr).get()
    gldl = gld.split("-")
    gd = date(int(gldl[2]),int(gldl[0]),int(gldl[1]))
    pr = Project.create(pname=pn,value=pvalue,mnversion=version,parea=ptype,smi=pphase,gld=gd)
    Useracc.create(projectid = pr.id,userid = pm.id,type="MGR-PROJ",dateadded = date.today())
    return 'suc'


@app.route('/addProject')
@login_required
def addProject():
    pr = Project.create(pname="Project name",value="0",mnversion="5.4",phase='Inception',parea='AS',smi='LS')
    return json.dumps(str(pr))



@app.route('/getManagers')
@login_required
def getManagers():
    mgrlist = []
    for mgr in User.select().where(User.type=='MGR'):
        mgrlist.append({"id":mgr.id,"name":mgr.name});

    return json.dumps(mgrlist)

@app.route('/getManagerNames')
@login_required
def getManagerNames():
    mgrlist = []
    for mgr in User.select().where(User.type=='MGR'):
        mgrlist.append(mgr.name);

    return json.dumps(mgrlist)


@app.route('/getMDNames')
@login_required
def getMDNames():
    mdlist = []
    for md in User.select().where(User.type=='MD'):
        mdlist.append(md.name);

    return json.dumps(mdlist)



@app.route('/getAdminProjects')
@login_required
def getAdminProjects():
    palist = []

    for p in Project.select().order_by(Project.id.desc()):

        mgrname=""
        mdname=""

        if Useracc.select().where(Useracc.projectid == p.id, Useracc.type == 'MGR-PROJ').exists():
            ua = Useracc.select().where(Useracc.projectid == p.id, Useracc.type == 'MGR-PROJ').get()
            u = User.select().where(User.id == ua.userid).get()
            mgrname = u.name

        if Useracc.select().where(Useracc.projectid == p.id, Useracc.type == 'MD-PROJ').exists():
            ua = Useracc.select().where(Useracc.projectid == p.id, Useracc.type == 'MD-PROJ').get()
            u = User.select().where(User.id == ua.userid).get()
            mdname = u.name

        palist.append({"pid":p.id,"name":p.pname,"phase":p.phase,"dept":p.parea,"smi":p.smi,"golive":str(p.golive),"value":p.value,"version":p.mnversion,"manager":mgrname,"md":mdname})

    return json.dumps(palist)

@app.route('/saveProjectParam/<pid>/<paramname>/<val>')
@login_required
def saveProjectParam(pid,paramname,val):
    if paramname != 'manager' and paramname != 'md':
        pr = Project.select().where(Project.id == pid).get()
        #Project.update(''+paramname+'' = val).where(Project.id == pid)
        pru = "update project set "+paramname+" = '"+val+"' where id ="+pid
        db.execute_sql(pru)
        return 'suc'+paramname
    elif paramname == 'manager':
        u = User.select().where(User.name == val).get()
        pr = Project.select().where(Project.id == pid).get()
        q = Useracc.delete().where(Useracc.projectid == pr.id, Useracc.type == 'MGR-PROJ')
        q.execute()
        ua = Useracc.create(projectid = pr.id,userid = u.id, type = 'MGR-PROJ')
        return 'suc'
    elif paramname == 'md':
        u = User.select().where(User.name == val).get()
        pr = Project.select().where(Project.id == pid).get()
        q = Useracc.delete().where(Useracc.projectid == pr.id, Useracc.type == 'MD-PROJ')
        q.execute()
        ua = Useracc.create(projectid = pr.id,userid = u.id, type = 'MD-PROJ')
        return 'suc'



@app.route('/getOverallRedStatus')
@login_required
def getOverallRedStatus():
    l=[]
    dataAr = []
    pru = '''

    select coalesce(hkd,lkd) as kd,coalesce(lcolor,hcolor),coalesce(hdept,'HT') as dept1,coalesce(hperc,0) as perc1,coalesce(ldept,'LS') as dept2,coalesce(lperc,0) as perc2 from (
select * from
(
select d.keydescr as hkd,d.smi as hdept,d.keyval as hcolor,round(((d.keycount/o.total)*100)) as hperc from
(SELECT k.keydescr,p.smi,ki.keyval,count(*) as keycount FROM `keyinstance` ki
LEFT join form f ON (ki.formid_id=f.id)
LEFT join `key` k ON (ki.keyid_id = k.id)
LEFT join project p ON (f.project_id = p.id)
WHERE f.formstatus = 'SUBMITTED' AND ki.keyval is not null AND p.smi ='HT'
GROUP BY k.keydescr,p.smi,ki.keyval) d
LEFT JOIN
(SELECT k.keydescr,p.smi,count(*) as total FROM `keyinstance` ki
LEFT join form f ON (ki.formid_id=f.id)
LEFT join `key` k ON (ki.keyid_id = k.id)
LEFT join project p ON (f.project_id = p.id)
WHERE f.formstatus = 'SUBMITTED' AND ki.keyval is not null AND p.smi ='HT'
GROUP BY k.keydescr,p.smi) o ON (d.keydescr = o.keydescr)
) HT

LEFT JOIN
(
select d.keydescr as lkd,d.smi as ldept,d.keyval as lcolor,round(((d.keycount/o.total)*100)) as lperc from
(SELECT k.keydescr,p.smi,ki.keyval,count(*) as keycount FROM `keyinstance` ki
LEFT join form f ON (ki.formid_id=f.id)
LEFT join `key` k ON (ki.keyid_id = k.id)
LEFT join project p ON (f.project_id = p.id)
WHERE f.formstatus = 'SUBMITTED' AND ki.keyval is not null AND p.smi ='LS'
GROUP BY k.keydescr,p.smi,ki.keyval) d
LEFT JOIN
(SELECT k.keydescr,p.smi,count(*) as total FROM `keyinstance` ki
LEFT join form f ON (ki.formid_id=f.id)
LEFT join `key` k ON (ki.keyid_id = k.id)
LEFT join project p ON (f.project_id = p.id)
WHERE f.formstatus = 'SUBMITTED' AND ki.keyval is not null AND p.smi ='LS'
GROUP BY k.keydescr,p.smi) o ON (d.keydescr = o.keydescr)
    ) LS
    ON (LS.lkd = HT.hkd AND LS.lcolor = HT.hcolor)

    ) lf



    UNION


select coalesce(hkd,lkd) as kd,coalesce(lcolor,hcolor),coalesce(hdept,'HT') as dept1,coalesce(hperc,0) as perc1,coalesce(ldept,'LS') as dept2,coalesce(lperc,0) as perc2 from (
select * from
(
select d.keydescr as hkd,d.smi as hdept,d.keyval as hcolor,round(((d.keycount/o.total)*100)) as hperc from
(SELECT k.keydescr,p.smi,ki.keyval,count(*) as keycount FROM `keyinstance` ki
LEFT join form f ON (ki.formid_id=f.id)
LEFT join `key` k ON (ki.keyid_id = k.id)
LEFT join project p ON (f.project_id = p.id)
WHERE f.formstatus = 'SUBMITTED' AND ki.keyval is not null AND p.smi ='HT'
GROUP BY k.keydescr,p.smi,ki.keyval) d
LEFT JOIN
(SELECT k.keydescr,p.smi,count(*) as total FROM `keyinstance` ki
LEFT join form f ON (ki.formid_id=f.id)
LEFT join `key` k ON (ki.keyid_id = k.id)
LEFT join project p ON (f.project_id = p.id)
WHERE f.formstatus = 'SUBMITTED' AND ki.keyval is not null AND p.smi ='HT'
GROUP BY k.keydescr,p.smi) o ON (d.keydescr = o.keydescr)
) HT

RIGHT JOIN
(
select d.keydescr as lkd,d.smi as ldept,d.keyval as lcolor,round(((d.keycount/o.total)*100)) as lperc from
(SELECT k.keydescr,p.smi,ki.keyval,count(*) as keycount FROM `keyinstance` ki
LEFT join form f ON (ki.formid_id=f.id)
LEFT join `key` k ON (ki.keyid_id = k.id)
LEFT join project p ON (f.project_id = p.id)
WHERE f.formstatus = 'SUBMITTED' AND ki.keyval is not null AND p.smi ='LS'
GROUP BY k.keydescr,p.smi,ki.keyval) d
LEFT JOIN
(SELECT k.keydescr,p.smi,count(*) as total FROM `keyinstance` ki
LEFT join form f ON (ki.formid_id=f.id)
LEFT join `key` k ON (ki.keyid_id = k.id)
LEFT join project p ON (f.project_id = p.id)
WHERE f.formstatus = 'SUBMITTED' AND ki.keyval is not null AND p.smi ='LS'
GROUP BY k.keydescr,p.smi) o ON (d.keydescr = o.keydescr)
    ) LS
    ON (LS.lkd = HT.hkd AND LS.lcolor = HT.hcolor)

    ) rg

    '''
    for i in db.execute_sql(pru):
        l=[]
        if i[1] == 1:
            l=[i[0],int(i[3]),str(i[3])+'%',int(i[5]),str(i[5])+'%']
            dataAr.append(l)

    return json.dumps(dataAr)




@app.route('/getStatusesPie')
@login_required
def getStatusesPie():
    l=[]
    dataAr = [['Status', '# of reports']]
    pru = '''
SELECT ki.keyval,count(*) as keycount FROM `keyinstance` ki
LEFT join form f ON (ki.formid_id=f.id)
LEFT join `key` k ON (ki.keyid_id = k.id)
LEFT join project p ON (f.project_id = p.id)
WHERE f.formstatus = 'SUBMITTED' AND ki.keyval is not null
GROUP BY ki.keyval
    '''
    for i in db.execute_sql(pru):
        l=[]
        if 1 == 1:
            color =""
            if i[0] == 1: color = 'Red'
            if i[0] == 2: color = 'Yellow'
            if i[0] == 3: color = 'Green'
            l=[color,int(i[1])]
            dataAr.append(l)

    return json.dumps(dataAr)



# set the secret key.  keep this really secret:
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'


if __name__ == '__main__':
  app.run(debug=True,host="0.0.0.0")
