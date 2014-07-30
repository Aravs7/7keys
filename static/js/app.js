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

    link: function(scope, element, attr){
    $compile(element.contents())(scope);
   $(element).tooltip();

   }
   }
  });


keysapp.controller('loginCtrl',function($scope,$http){



$scope.loginUser=function(){


var l = $http.get("/loginu/"+$('#login-uname').val()+"/"+$('#login-pwd').val());

l.success(function(data, status, headers, config) {
    if(data=="success")
    window.location.replace("/app");
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




$scope.loadProj= function(){

$scope.p="";
$scope.prsn="";
$scope.prsi="";

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
$scope.prsn = data;
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



$scope.updateRec=function(recid){

var srec = $http.get("/saveIssueRec/"+recid+"/"+$("#d"+recid).val());

srec.success(function(data, status, headers, config) {
console.log(data);
});

srec.error(function(data, status, headers, config) {
    $("#error").html(data);
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




keysapp.controller('adminController',function($scope,$http){
console.log("in admin ctrl");
});



$(document).ready(function () {


        //alert("init");

});







