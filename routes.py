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
        return "success"
    return "Wrong userid/password. Please ask Aravind."

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
    pr = Project.select().where(Project.id == 99999).get()
    form = Form.create(formproject=pr,formstatus = "DRAFT",createdby = login.current_user.id, reportdate = date.today())
    for k in Key.select():
        keyins = Keyinstance.create(keyid=k.id,formid=form.id)
    return str(form.id)



@app.route('/form/<fid>')
def form(fid):
    form = Form.select().where(Form.id == fid).get()
        #pass
    return render_template('addnew.html',form=form)



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
        kl.append({"kiid":ki.id,"kival":ki.keyval,"keyname":k.keyname,"keyfname":k.keydescr,"keycom":ki.keycomments})
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
    isr = Issue.create(formid = fid)
    isro = Issue.select().where(Issue.id == isr.id).get()
    return json.dumps({"isrid":isro.id,"descr":isro.issuedescr,"priority":isro.priority,"action":isro.action,"owner":isro.owner,"resdate":isro.resdate})

@app.route('/getIssueRecs/<fid>')
def getIssueRec(fid):
    ilist =[]
    for isro in Issue.select().where(Issue.formid == fid):
        ilist.append({"isrid":isro.id,"descr":isro.issuedescr,"priority":isro.priority,"action":isro.action,"owner":isro.owner,"resdate":isro.resdate})
    return json.dumps(ilist)

@app.route('/saveIssueRec/<rid>/<d>') #/<p>/<o>/<a>/<r>
def saveIssueRec(rid,d):  #,p,o,a,r
    isr = Issue.select().where(Issue.id == rid).get()
    isr.issuedescr=d
    # isr.priority=p
    # isr.owner=o
    # isr.action=a
    # isr.resdate=r
    isr.save()
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
            return str(pr.pname)
        else:
            return 'na'
    else:
        return 'na'


@app.route('/getProjects/<uid>')
def getProjects(uid):

    plist = [];

    if Form.select().where(Form.createdby == uid).exists():
        for f in Form.select().where(Form.createdby == uid):
            pr = Project.select().where(Project.id == f.project).get()
            ky = Key.select().where(Key.keyname == 'cws').get()
            kyi = Keyinstance.select().where(Keyinstance.keyid == ky.id,Keyinstance.formid == f.id).get()
            plist.append({"fid":f.id,"pid":pr.id,"pname":pr.pname,"status":kyi.keyval,"date":str(f.reportdate),"formstatus":f.formstatus})

    return json.dumps(plist)




# set the secret key.  keep this really secret:
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'


if __name__ == '__main__':
  app.run(debug=True)
