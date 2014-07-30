__author__ = 'A'

from peewee import *
from datetime import date
from datetime import time
import logging
logger = logging.getLogger('myapp')
hdlr = logging.FileHandler('/var/tmp/myapp.log')
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
hdlr.setFormatter(formatter)
logger.addHandler(hdlr) 
logger.setLevel(logging.WARNING)

db = MySQLDatabase('7keys', host="localhost", port=3306, user='root', password='admin')
db.connect()

class MySQLModel(Model):
    """A base model that will use our MySQL database"""
    class Meta:
        database = db


class User(MySQLModel):

    name = CharField()
    email = CharField()
    password = CharField()
    image = CharField(default='no-user.jpg')
    type = CharField()

    def is_admin(self):
        if self.type == 'ADM':
            return True
        else:
            return False

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.id

    # Required for administrative interface
    def __unicode__(self):
        return self.name

    class Meta:
        database = db

class Project(MySQLModel):

    pname = CharField(null=True)
    pobj = TextField(null=True)
    smi = CharField(null=True)
    parea = CharField(null=True)
    phase = CharField(null=True)
    golive = DateField(null=True)
    value = IntegerField(null=True)
    mnversion = CharField(null=True)
    dept = CharField(null=True)


class Form(MySQLModel):

    project = ForeignKeyField(Project, related_name='formproject', null=True)
    formstatus = CharField(null= True)
    reportdate = DateField(null= True)
    createdby = ForeignKeyField(User, related_name='createdby', null= True)
    projectstatus = IntegerField(null= True)


class Key(MySQLModel):

    keyname = CharField(null= True)
    keydescr = TextField(null= True)
    defaultval = IntegerField(null= True)
    hascomments = BooleanField(null= True)

class Keyinstance(MySQLModel):

    keyid = ForeignKeyField(Key, related_name='key',null= True)
    formid = ForeignKeyField(Form, related_name='keyform',null= True)
    keyval = IntegerField(null= True)
    keycomments = TextField(null= True)

class Issue(MySQLModel):

    formid = ForeignKeyField(Form, related_name='issueform',null= True)
    issuedescr = TextField(null= True)
    priority = IntegerField(null= True)
    action = TextField(null= True)
    owner = CharField(null= True)
    resdate = DateField(null= True)

class Milestone(MySQLModel):

    formid = ForeignKeyField(Form, related_name='milestoneform',null= True)
    mdescr = TextField(null= True)
    baseline = DateField(null= True)
    current = DateField(null= True)
    planperc = IntegerField(null= True)
    actualperc = IntegerField(null= True)
    comments = TextField(null= True)

class Useracc(MySQLModel):

    projectid = ForeignKeyField(Project, related_name='project',null= True)
    userid = ForeignKeyField(User, related_name='user',null= True)
    type = CharField(null= True)
    dateadded = DateField(null= True)

class Projectparams(MySQLModel):

    projectid = ForeignKeyField(Project, related_name='paramproject',null= True)
    propname = CharField(null= True)
    propvalue = CharField(null= True)
    proptype = CharField(null= True)



class CreateTables():

    def create(self):
        User.create_table()
        Project.create_table()
        Form.create_table()
        Key.create_table()
        Keyinstance.create_table()
        Issue.create_table()
        Milestone.create_table()
        Useracc.create_table()
        Projectparams.create_table()

    def createuserprojs(self):
        user = User.create(name="manager2",email="manager@modeln.com",password="manager",type="MGR")
        project = Project.create(pname="Bristol-Myers Squibb")
        project1 = Project.create(pname="Amgen")
        project2 = Project.create(pname="EMD")
        usracc = Useracc.create(projectid = project,userid = user, type = 'MGR-PROJ',dateadded = date.today())
        usracc = Useracc.create(projectid = project1,userid = user, type = 'MGR-PROJ',dateadded = date.today())
        usracc = Useracc.create(projectid = project2,userid = user, type = 'MGR-PROJ',dateadded = date.today())

    def createKeys(self):

        Key.create(keyname="lws",keydescr="Last week overall status",keyhascomments=True)
        Key.create(keyname="cws",keydescr="Current week overall status",keyhascomments=True)
        Key.create(keyname="stk",keydescr="Stakeholders",keyhascomments=True)
        Key.create(keyname="bnb",keydescr="Business & Benefits",keyhascomments=True)
        Key.create(keyname="wns",keydescr="Work & Schedule",keyhascomments=True)
        Key.create(keyname="tem",keydescr="Team",keyhascomments=True)
        Key.create(keyname="scp",keydescr="Scope",keyhascomments=True)
        Key.create(keyname="rsk",keydescr="Risks",keyhascomments=True)






