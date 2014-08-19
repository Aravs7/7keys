keysapp = angular.module('keys',[]);

keysapp.config(
function($interpolateProvider) {
$interpolateProvider.startSymbol('||');
$interpolateProvider.endSymbol('||');
}
);


keysapp.directive('tooltip', function($compile) {
   //$('.toolt').tooltip();
   return{
   restrict: 'A',
      scope: {
        tooltip: '='
      },

    link: function(scope, element, attrs){
   console.log(attrs.val);

   $(element).popover({html:true,trigger:'hover'})
          .attr('data-content', attrs.val).attr('html',true);

   }
   }
  });


  keysapp.directive('conditionalediting', function($compile) {

   return{
   restrict: 'A',
      scope: {
        tooltip: '='
      },

    link: function(scope, element, attr){

   console.log("*********"+$('#formstatus').val());
   if($('#formstatus').val() == 'SUBMITTED'){
   $(element).css('pointer-events','none');
   }

   }
   }
  });

  keysapp.directive('sliderdiv', function($compile) {
   //$('.toolt').tooltip();
   return{
   restrict: 'A',
      scope: {
        tooltip: '='
      },

    link: function(scope, element, attr){
    $compile(element.contents())(scope);
   $(element).slider();

   }
   }
  });

  keysapp.directive('datepicker', function($compile) {
   //$('.toolt').tooltip();
   return{
   restrict: 'A',
      scope: {
        tooltip: '='
      },

    link: function(scope, element, attr){
    $compile(element.contents())(scope);
    console.log("cval is ::::::"+ attr.cval);
    $(element).datepicker('setValue',attr.cval).on('changeDate', function(ev){
        console.log("date changed ");
        var repDay = ev.date.getDate();
        var repMonth = ev.date.getMonth()+1;
        var repYear = ev.date.getFullYear();
        //scope.saveDate(attr.isid,repMonth,repDay,repYear);

        $.ajax({
         url: '/saveDate'+'/'+attr.isid+'/'+repMonth+'/'+repDay+'/'+repYear+'/'+attr.type+'/'+attr.field,
         data: {},
         success: function(data){console.log(data);}
        });

       console.log(attr.isid);
    });

     console.log(attr.cval+'pp---');

   }
   }
  });

  keysapp.directive('xeditablename', function($compile,$http) {

   return{
   restrict: 'A',
      scope: {
        tooltip: '='
      },

    link: function(scope, element, attr){
   console.log("making name editable");

   //$(element).editable();

   $(element).addClass("editable editable-click editable-empty");

   $(element).editable({

   value:attr.val,
   validate: function(value) {
           if($.trim(value) == '') return 'This field is required';
        },
   success:function(response, newValue) {
        console.log(newValue+" "+attr.val);



        var l = $http.get("/saveProjectParam/"+attr.pid+"/"+"pname"+"/"+newValue);

        l.success(function(data, status, headers, config) {
        console.log(data);

        });
        l.error(function(data, status, headers, config) {
         console.log(data);
        });



    },
    emptytext:"Project Name"

    });

   }
   }
  });


  keysapp.directive('xeditablevalue', function($compile,$http) {

   return{
   restrict: 'A',
      scope: {
        tooltip: '='
      },

    link: function(scope, element, attr){
   console.log("making editable");

   //$(element).editable();

   $(element).addClass("editable editable-click editable-empty");

   $(element).editable({

   value:attr.val,
   validate: function(value) {
           if($.trim(value) == '') return 'This field is required';
        },
   success:function(response, newValue) {
        console.log(newValue+" "+attr.val);
        var l = $http.get("/saveProjectParam/"+attr.pid+"/"+"value"+"/"+newValue);

        l.success(function(data, status, headers, config) {
        console.log(data);

        });
        l.error(function(data, status, headers, config) {
         console.log(data);
        });
    }

    });

   }
   }
  });


   keysapp.directive('xeditablephase', function($compile,$http) {

   return{
   restrict: 'A',
      scope: {
        tooltip: '='
      },

   link: function(scope, element, attr){

   console.log("im here");


   $(element).addClass("editable editable-click editable-empty");

    console.log("im here2");

   $(element).editable({


   validate: function(value) {
           if($.trim(value) == '') return 'This field is required';
        },
   success:function(response, newValue) {
        console.log(newValue+" "+attr.val);
        var l = $http.get("/saveProjectParam/"+attr.pid+"/"+"phase"+"/"+newValue);

        l.success(function(data, status, headers, config) {
        console.log(data);

        });
        l.error(function(data, status, headers, config) {
         console.log(data);
        });
    },
    source: [
              {value: 'Inception', text: 'Inception'},
              {value: 'Elaboration', text: 'Elaboration'},
              {value: 'Construction', text: 'Construction'},
              {value: 'Verification', text: 'Verification'},
              {value: 'Transition', text: 'Transition'},
              {value: 'Support', text: 'Support'}

           ],
    defaultValue:'Inception'


    });

     console.log("im here");


   }
   }
  });


 keysapp.directive('xeditabledept', function($compile,$http) {

   return{
   restrict: 'A',
      scope: {
        tooltip: '='
      },

   link: function(scope, element, attr){


   $(element).addClass("editable editable-click editable-empty");

   $(element).editable({


   validate: function(value) {
           if($.trim(value) == '') return 'This field is required';
        },
   success:function(response, newValue) {
        console.log(newValue+" "+attr.val);
        var l = $http.get("/saveProjectParam/"+attr.pid+"/"+"parea"+"/"+newValue);

        l.success(function(data, status, headers, config) {
        console.log(data);

        });
        l.error(function(data, status, headers, config) {
         console.log(data);
        });
    },
    source: [
              {value: 'AS', text: 'AS'},
              {value: 'PS', text: 'PS'},
              {value: 'PD', text: 'PD'}
           ]

    });

   }
   }
  });


   keysapp.directive('xeditablesmi', function($compile,$http) {

   return{
   restrict: 'A',
      scope: {
        tooltip: '='
      },

   link: function(scope, element, attr){


   $(element).addClass("editable editable-click editable-empty");

   $(element).editable({


   validate: function(value) {
           if($.trim(value) == '') return 'This field is required';
        },
   success:function(response, newValue) {
        console.log(newValue+" "+attr.val);
        var l = $http.get("/saveProjectParam/"+attr.pid+"/"+"smi"+"/"+newValue);

        l.success(function(data, status, headers, config) {
        console.log(data);

        });
        l.error(function(data, status, headers, config) {
         console.log(data);
        });
    },
    source: [
              {value: 'LS', text: 'LS'},
              {value: 'HT', text: 'HT'}
           ]

    });

   }
   }
  });


   keysapp.directive('xeditableversion', function($compile,$http) {

   return{
   restrict: 'A',
      scope: {
        tooltip: '='
      },

   link: function(scope, element, attr){


   $(element).addClass("editable editable-click editable-empty");

   $(element).editable({


   validate: function(value) {
           if($.trim(value) == '') return 'This field is required';
        },
   success:function(response, newValue) {
        console.log(newValue+" "+attr.val);

        var l = $http.get("/saveProjectParam/"+attr.pid+"/"+"mnversion"+"/"+newValue);

        l.success(function(data, status, headers, config) {
        console.log(data);

        });
        l.error(function(data, status, headers, config) {
         console.log(data);
        });

    },
    source: [
              {value: '5.4', text: '5.4'},
              {value: '5.5', text: '5.5'},
              {value: '5.6', text: '5.6'},
              {value: '5.7', text: '5.7'}

           ]

    });

   }
   }
  });


  keysapp.directive('xeditablemanager', function($compile,$http) {

   return{
   restrict: 'A',
      scope: {
        tooltip: '='
      },

   link: function(scope, element, attr){


   $(element).addClass("editable editable-click editable-empty");

   $(element).editable({


   validate: function(value) {
           if($.trim(value) == '') return 'This field is required';
        },
   success:function(response, newValue) {
        console.log(newValue+" "+attr.val);

        var l = $http.get("/saveProjectParam/"+attr.pid+"/"+"manager"+"/"+newValue);

        l.success(function(data, status, headers, config) {
        console.log(data);

        });
        l.error(function(data, status, headers, config) {
         console.log(data);
        });


    },


    });

   }
   }
  });


keysapp.directive('xeditablemd', function($compile,$http) {

   return{
   restrict: 'A',
      scope: {
        tooltip: '='
      },

   link: function(scope, element, attr){


   $(element).addClass("editable editable-click editable-empty");

   $(element).editable({


   validate: function(value) {
           if($.trim(value) == '') return 'This field is required';
        },
   success:function(response, newValue) {
        console.log(newValue+" "+attr.val);

        var l = $http.get("/saveProjectParam/"+attr.pid+"/"+"md"+"/"+newValue);

        l.success(function(data, status, headers, config) {
        console.log(data);

        });
        l.error(function(data, status, headers, config) {
         console.log(data);
        });


    },


    });

   }
   }
  });






keysapp.controller('loginCtrl',function($scope,$http){



$scope.loginUser=function(){


var l = $http.get("/loginu/"+$('#login-uname').val()+"/"+$('#login-pwd').val());

l.success(function(data, status, headers, config) {

    if(data=="MGR")
    window.location.replace("/app");
    else if(data=='ADM')
    window.location.replace("/admin");
    else
    alert(data);
});
l.error(function(data, status, headers, config) {
$("#error").html(data);
    alert("AJAX failed!" + data);
});

};

});


keysapp.controller('formController',function($scope,$http){


$scope.deleteIssue=function(id){
console.log(id);

var deli = $http.get("/deleteIssue/"+id);

deli.success(function(data, status, headers, config) {
console.log(data);


$scope.isrl = jQuery.grep($scope.isrl, function(value) {
  return value.isrid != id;
});


});

deli.error(function(data, status, headers, config) {
    $("#error").html(data);
});


};




$scope.deleteMilestone=function(id){
console.log(id);

var deli = $http.get("/deleteMilestone/"+id);

deli.success(function(data, status, headers, config) {
console.log(data);


$scope.mstl = jQuery.grep($scope.mstl, function(value) {
  return value.mstid != id;
});


});

deli.error(function(data, status, headers, config) {
    $("#error").html(data);
});


};





$scope.submitReport=function(){



 //---------


        bootbox.dialog({
  message: "Please review and update all three tabs prior to submitting your report as required. Once submitted, report will not be editable. Click Ok to submit the report",
  title: "Submit Report",
  buttons: {
    Submit: {
      label: "Submit",
      className: "btn-success",
      callback: function() {


      var fid = $('#fid').val();

console.log(fid);

$scope.formstatus="";

var reps = $http.get("/submitReport/"+fid+"/"+$scope.pdata.phase);

reps.success(function(data, status, headers, config) {
console.log(data);
$scope.formstatus="SUBMITTED";
$('#tabs-container').css('pointer-events','none');
});

reps.error(function(data, status, headers, config) {
    $("#error").html(data);
});



      }
    },
    Cancel: {
      label: "Cancel",
      className: "btn-danger",
      callback: function() {

       //  bootbox.alert("<a href=https://help.modeln.com/GCS/COE/00_Methodology_Description%2F%2FGoals/04_Phase_Detail>Click here to access GATE review form</a>", function() {
       // });

      }
    }
  }
});


        //---------



};



$scope.getFormStatus=function(){

var reps = $http.get("/getFormStatus/"+$('#fid').val());

reps.success(function(data, status, headers, config) {
$scope.formstatus=data;
});

reps.error(function(data, status, headers, config) {
    $("#error").html(data);
});

};

$scope.getFormStatus();

$scope.saveReportDate= function(m,d,y){

var proje = $http.get("/saveReportDate/"+$("#fid").val()+"/"+m+"/"+d+"/"+y);

proje.success(function(data, status, headers, config) {
//do nothing
});

proje.error(function(data, status, headers, config) {
    $("#error").html(data);
});

};

$('#dp3').datepicker().on('changeDate', function(ev){
    console.log("date changed ");
    var repDay = ev.date.getDate();
    var repMonth = ev.date.getMonth()+1;
    var repYear = ev.date.getFullYear();
    $scope.saveReportDate(repMonth,repDay,repYear);

  });

$scope.saveDate=function(){
   console.log("in Save Date");
};


$scope.loadProj= function(){

$scope.p="";
$scope.prsn="";
$scope.prsi="";
$scope.pdata="";
$scope.rdate="";

var d = new Date();

var month = d.getMonth()+1;
var day = d.getDate();

$scope.today = (month<10 ? '0' : '') + month + '-'+ (day<10 ? '0' : '') + day+'-'+d.getFullYear();



var rd = $http.get("/getReportDate/"+$("#fid").val());

rd.success(function(data, status, headers, config) {
$scope.rdate=data;
console.log(data);
});



$scope.togglePrdet=function(){
$('#prdetails').toggle();
};

var proje = $http.get("/getMgrProjects/"+$("#uid").val());

proje.success(function(data, status, headers, config) {
$scope.p=data;
$scope.prsn = data[0]["name"];
});

proje.error(function(data, status, headers, config) {
    $("#error").html(data);
});


var proje = $http.get("/getFormProj/"+$("#fid").val());

proje.success(function(data, status, headers, config) {
if(data != 'na'){
$scope.prsn = data.name;
$scope.pdata = data;
}
});

proje.error(function(data, status, headers, config) {
    $("#error").html(data);
});

};

$scope.loadProj();


$scope.ks="";

$scope.populatekeys=function(){

var kys = $http.get("/getFormKeys/"+$("#fid").val());

kys.success(function(data, status, headers, config) {
$scope.ks=data;
});

kys.error(function(data, status, headers, config) {
    $("#error").html(data);
});

};

$scope.populatekeys();



$scope.saveComment=function(kiid){

var kyc = $http.get("/saveComment/"+kiid+"/"+$("#"+kiid+"com").val());

kyc.success(function(data, status, headers, config) {
console.log(data);
});

kyc.error(function(data, status, headers, config) {
    $("#error").html(data);
});

};



$scope.saveKeyVal=function(k,kiid,val,keyn){

k.kival=val;

var kyins = $http.get("/saveKeyInstVal/"+kiid+"/"+val);

kyins.success(function(data, status, headers, config) {
console.log(data);
});

kyins.error(function(data, status, headers, config) {
    $("#error").html(data);
});


};



$scope.tabShift= function(id){
$('#'+id+'tab').removeClass('app_form_tab');
$('.app_form_tab_active').addClass('app_form_tab');
$('.app_form_tab_active').removeClass('app_form_tab_active');
$('#'+id+'tab').addClass('app_form_tab_active');
$('.app_form_tab_div').hide();
$('#'+id).show();


};

$scope.selProj=function(i,n){

var sproj = $http.get("/updateProj/"+$("#fid").val()+"/"+i);

sproj.success(function(data, status, headers, config) {
console.log(data);
$scope.prsn = data;
});

sproj.error(function(data, status, headers, config) {
    $("#error").html(data);
});

$scope.loadProj();

};

$scope.isrl=[];

$scope.addIssueRecord=function(){



var isr = $http.get("/addIssueRec/"+$("#fid").val());

isr.success(function(data, status, headers, config) {
$scope.isrl.push(data);
console.log(data);
});

isr.error(function(data, status, headers, config) {
    $("#error").html(data);
});

};


$scope.mstl=[];

$scope.addMilestoneRecord=function(){



var mst = $http.get("/addMilestoneRec/"+$("#fid").val());

mst.success(function(data, status, headers, config) {
$scope.mstl.push(data);
console.log(data);
});

mst.error(function(data, status, headers, config) {
    $("#error").html(data);
});

};


$scope.populateIssueRecs = function(){
var isr2 = $http.get("/getIssueRecs/"+$("#fid").val());

isr2.success(function(data, status, headers, config) {
$scope.isrl = data;
console.log(data);
});

isr2.error(function(data, status, headers, config) {
    $("#error").html(data);
});
};



$scope.populateIssueRecs();


$scope.mststatusdum="";

$scope.populateMilestoneRecs = function(){
var mst2 = $http.get("/getMilestoneRecs/"+$("#fid").val());

mst2.success(function(data, status, headers, config) {
$scope.mstl = data;
});

mst2.error(function(data, status, headers, config) {
    $("#error").html(data);
});
};


$scope.populateMilestoneRecs();



$scope.updateIssueRec=function(recid){

var d = $("#d"+recid).val();
var a = $("#a"+recid).val();
var o = $("#o"+recid).val();

if(d==""){
d = " ";
console.log("d null");
}
if(a==""){
a = " ";
}
if(o==""){
o= " ";
}

var srec = $http.get("/saveIssueRec/"+recid+"/"+$("#t"+recid).val()+"/"+$("#s"+recid).val()+"/"+d+"/"+a+"/"+o+"/");

srec.success(function(data, status, headers, config) {
console.log(data);
});

srec.error(function(data, status, headers, config) {
    $("#error").html(data);
});

};



$scope.updateMilestoneRec=function(recid){

console.log("yoyo "+$('#s'+recid).val());

var mrec = $http.get("/saveMilestoneRec/"+recid+"/"+$("#d"+recid).val()+"/"+$("#s"+recid).val());

mrec.success(function(data, status, headers, config) {
console.log(data);
});

mrec.error(function(data, status, headers, config) {
    $("#error").html(data);
});


};


$scope.editPhase=function(pid,phase){

console.log(pid+' '+phase);


$scope.pdata.phase = phase;

var l = $http.get("/saveProjectParam/"+pid+"/"+"phase"+"/"+phase);

        l.success(function(data, status, headers, config) {
        console.log(data);


        //---------


        bootbox.dialog({
  message: "You're trying to change project phase. Is Gate Review completed?",
  title: "GATE review completed?",
  buttons: {
    Yes: {
      label: "Yes",
      className: "btn-success",
      callback: function() {

      }
    },
    No: {
      label: "No",
      className: "btn-danger",
      callback: function() {

         bootbox.alert("<a href=https://help.modeln.com/GCS/COE/00_Methodology_Description%2F%2FGoals/04_Phase_Detail>Click here to access GATE review form</a>", function() {
        });

      }
    }
  }
});


        //---------




        });
        l.error(function(data, status, headers, config) {
         console.log(data);
        });



};



});







keysapp.controller('choosePcontroller',function($scope,$http){

var proje = $http.get("/getMgrProjects/"+$("#uid").val());

$scope.p="";

proje.success(function(data, status, headers, config) {
$scope.p=data;
});

proje.error(function(data, status, headers, config) {
    $("#error").html(data);
});

});

keysapp.controller('appController',function($scope,$http){


$scope.createForm = function(){



var frmc = $http.get("/createform");


frmc.success(function(data, status, headers, config) {
window.location = "/form/"+data;
});

frmc.error(function(data, status, headers, config) {
    $("#error").html(data);
});


};


$scope.projlist="";

$scope.loadProjects= function(){

var lproj = $http.get("/getProjects/"+$('#uid').val());


lproj.success(function(data, status, headers, config) {
$scope.projlist = data

});

lproj.error(function(data, status, headers, config) {
    $("#error").html(data);
});

};

$scope.loadProjects();



});






//Admin page controller

keysapp.controller('adminController',function($scope,$http){

$.fn.editable.defaults.mode = 'inline';
$scope.pn="";
$scope.pv="";
$scope.pp="Project Phase";
$scope.mnv="Version";
$scope.pt="";
$scope.md="";
$scope.pm="Choose Manager";
$scope.pmid="";
$scope.gld="";
$scope.accnt="";
$scope.mgrs=[];
$scope.allpr="";
$scope.allprtxt="All Results";
$scope.csearch="";
$scope.csearchtxt="All Statuses";


$scope.chPrjSrch=function(pn){
console.log(pn);

if(pn == "All Results"){
$scope.allpr ="";
$scope.allprtxt=pn;
return;
}

$scope.allpr = pn;
$scope.allprtxt = $scope.allpr;
};


$scope.chPrjSrchClr=function(pn,pnn){
console.log(pn);

if(pn == 0){
$scope.csearch ="";
$scope.csearchtxt=pnn;
return;
}


$scope.csearch = pn;
$scope.csearchtxt = pnn;

};





$scope.tabShift= function(id){
$('#'+id+'tab').removeClass('app_form_tab');
$('.app_form_tab_active').addClass('app_form_tab');
$('.app_form_tab_active').removeClass('app_form_tab_active');
$('#'+id+'tab').addClass('app_form_tab_active');
$('.app_form_tab_div').hide();
$('#'+id).show();
console.log(id+"%%%%%%%%%%");
if(id=='charts'){
console.log('charts');
$scope.drawCharts();
}
};





$scope.popMgrs = function(){

var pmgrs = $http.get("/getManagers");

pmgrs.success(function(data, status, headers, config) {
$scope.mgrs = data;
console.log(data);
});

pmgrs.error(function(data, status, headers, config) {
    console.log(data);
});


};

$scope.popMgrs();


$scope.selVersion=function(v){
$scope.mnv=v;
};

$scope.selPhase=function(p){
$scope.pp=p;
};

$scope.selMgr=function(id,name){
$scope.pm=name;
$scope.pmid=id;
};

$('#pgld').datepicker().on('changeDate', function(ev){

        var repDay = ev.date.getDate();
        var repMonth = ev.date.getMonth()+1;
        var repYear = ev.date.getFullYear();

$scope.gld=repMonth+"-"+repDay+"-"+repYear;

});

$scope.addProjWithDetails=function(){

console.log("/addProjectWithDetails/"+$scope.pn+"/"+$scope.pv+"/"+$scope.mnv+"/"+$scope.pmid+"/"+$scope.md+"/"+$scope.pt+"/"+$scope.pp+"/"+$scope.gld);

var addp = $http.get("/addProject/"+$scope.pn+"/"+$scope.pv+"/"+$scope.mnv+"/"+$scope.pmid+"/"+$scope.md+"/"+$scope.pt+"/"+$scope.pp+"/"+$scope.gld);

addp.success(function(data, status, headers, config) {
console.log(data);
});

addp.error(function(data, status, headers, config) {
    console.log(data);
});

};


$scope.palist=[];

$scope.addProj=function(){

console.log("/addProject");

var addp = $http.get("/addProject");

addp.success(function(data, status, headers, config) {
console.log(data);
$scope.loadAdminProjects();
});

addp.error(function(data, status, headers, config) {
    console.log(data);
});

};


$scope.csearch="";
$scope.dsearchf="08-05-2014";

$('#searchdate').datepicker().on('changeDate', function(ev){

console.log("dcdcdc");

        var repDay = ev.date.getDate();
        var repMonth = ev.date.getMonth()+1;
        var repYear = ev.date.getFullYear();

$scope.dsearchf=repMonth+"-"+repDay+"-"+repYear;

});;






$scope.flist=[];
$scope.loadAdminReports=function(){

var prs = $http.get("/getAdminReports");

prs.success(function(data, status, headers, config) {
console.log(data);
$scope.flist = data;
});

prs.error(function(data, status, headers, config) {
    console.log(data);
});

};

$scope.loadAdminReports();







$scope.loadAdminProjects=function(){

var prs = $http.get("/getAdminProjects");

prs.success(function(data, status, headers, config) {
console.log(data);
$scope.palist = data;
});

prs.error(function(data, status, headers, config) {
    console.log(data);
});

};

$scope.loadAdminProjects();




$scope.loadUsers = function(){

var usrs = $http.get("/getUsers");

usrs.success(function(data, status, headers, config) {
console.log(data);
$scope.ulist = data;
});

usrs.error(function(data, status, headers, config) {
    console.log(data);
});


};


$scope.loadUsers();

$scope.cdata=[
    ['Keys', 'LS', 'HT'],
    ['1',  10,      40],
    ['2',  20,      40],
    ['3',  5,       5],
    ['4',  30,      15]
  ];





$scope.drawColumnChart= function(){


var rs = $http.get("/getOverallRedStatus");

rs.success(function(adata, status, headers, config) {

 var data = new google.visualization.DataTable();
 data.addColumn('string', 'Key');
 data.addColumn('number', 'HT');
 data.addColumn({type: 'string', role: 'tooltip'});
 data.addColumn('number', 'LS');
 data.addColumn({type: 'string', role: 'tooltip'});

 data.addRows(adata);

  var options = {
    title: 'Overall Red %  LS & HT',
    hAxis: {title: 'Keys', titleTextStyle: {color: 'blue'}},
    vAxis:{title:'%'},
    chartArea:{left:60,top:20,bottom:10,width:'1200',height:'900'}
  };

  var chart = new google.visualization.ColumnChart(document.getElementById('chart_div'));

  chart.draw(data, options);


});

rs.error(function(data, status, headers, config) {
    console.log(data);
});

};



$scope.drawPieChart= function() {
        var data = google.visualization.arrayToDataTable([
          ['Status', '# of reports'],
          ['Red',     11],
          ['Yellow',      2],
          ['Green',  2]
        ]);

        var rs = $http.get("/getStatusesPie");

rs.success(function(adata, status, headers, config) {

  var data = google.visualization.arrayToDataTable(adata);

  var options = {
          title: 'Statuses Pie',
          is3D: true,
          chartArea:{left:60,top:60,bottom:10,width:'1200',height:'900'},
          slices: [
            { color: 'red' },
            { color: '#ffbf00' },
            { color: 'green' }
          ],
          legend:{position: 'left'}
        };

        var chart = new google.visualization.PieChart(document.getElementById('piechart_3d'));
        chart.draw(data, options);


});

rs.error(function(data, status, headers, config) {
    console.log(data);
});



      };


$scope.drawCharts=function(){

$scope.drawColumnChart();
$scope.drawPieChart();

};


//google.setOnLoadCallback($scope.drawCharts);
console.log("Google Chart "+google);







});


keysapp.filter('dsearchfn', function () {
  return function (forms, date) {
    var filtered = [];

    for (var i = 0; i < forms.length; i++) {
      var form = forms[i];
      var dps=date.split("-");
      if(dps.length != 3){
      return false;
      }
      var fds = form.date.split("-");
      fd = new Date(fds[2],fds[0],fds[1]);
      sd = new Date(dps[2],dps[0],dps[1]);

      if (fd >= sd) {

        filtered.push(form);
      }
    }
    return filtered;
  };
});






keysapp.controller('chartController',function($scope,$http){

$scope.d = "hello world";

$scope.cdata=[
    ['Year', 'Sales', 'Expenses'],
    ['2004',  1000,      400],
    ['2005',  1170,      460],
    ['2006',  660,       1120],
    ['2007',  1030,      540]
  ];






});





$(document).ready(function () {


        //alert("init");



});







