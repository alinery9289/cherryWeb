function judgeUserid(inputid,textid){
	var value=document.getElementById(inputid).value;
	var filter=/^s*[.A-Za-z0-9_-]{5,15}s*$/;
	if (value==""){
		document.getElementById(textid).innerHTML="The username can't be empty!";
	}
	else {
		if (!filter.test(value)) { 
			document.getElementById(textid).innerHTML="Username is incorrect, please input again! " +
					"The characters (A-Za-z0-9_-.) are supported. Username should be more than 5, less than 20 characters."; 
		} 
		else {
			document.getElementById(textid).innerHTML="";
		}
	}
}

function judgePassword(inputid,textid){
	var value=document.getElementById(inputid).value;
	var filter=/^s*[.A-Za-z0-9_-]{5,20}s*$/;
	if (value==""){
		document.getElementById(textid).innerHTML="The password can't be empty!";
	}
	else {
		if (!filter.test(value)) { 
			document.getElementById(textid).innerHTML="Password is incorrect, please input again! " +
			"The characters (A-Za-z0-9_-.) are supported. Password should be more than 5, less than 20 characters."; 
		} 
		else {document.getElementById(textid).innerHTML="";}
	}
}

function judgeUseridorEmail(uidorpw){
	var value=document.getElementById(uidorpw).value;
	var filter1=/^s*[.A-Za-z0-9_-]{5,15}s*$/;
	var filter2=/[a-zA-Z0-9_\-\.]+@[a-zA-Z0-9\.]+(\.(com|cn|org|edu|hk|gov|mil|net|tw))/;
	if (value==""){
		document.getElementById("useridnotes").innerHTML="Username/Email can't be empty!";
	}
	else {
		if (!filter1.test(value) && !filter2.test(value)) { 
			document.getElementById("useridnotes").innerHTML="Username/Email is incorrect, please input again! "; 
		} 
		else {
			document.getElementById("useridnotes").innerHTML="";
		}
	}
}

function judgeEmail(inputid,textid){
	var value=document.getElementById(inputid).value;
	var filter=/[a-zA-Z0-9_\-\.]+@[a-zA-Z0-9\.]+(\.(com|cn|org|edu|hk|gov|mil|net|tw))/;
	if (value==""){
		document.getElementById(textid).innerHTML="Email can't be empty!";
	}
	else {
		if (!filter.test(value)) { 
			document.getElementById(textid).innerHTML="Email is incorrect, please input again!"; 
		} 
		else {document.getElementById(textid).innerHTML="";}
	}
}

function checkpassword(){
	var value1=document.getElementById('check_reg_password').value;
	var value2=document.getElementById('reg_password').value;
	if (value1!=value2){
		document.getElementById('check_reg_passwordnotes').innerHTML="This password is different from your first input.";
	}
	else {document.getElementById('check_reg_passwordnotes').innerHTML="";
	}
}

function checkBeforeLogin(){
	var value1= document.getElementById("passwordnotes").innerHTML;
	var value2= document.getElementById("useridnotes").innerHTML;
	var value3=document.getElementById("userid").value;
	var value4=document.getElementById("password").value;
	if ( value1=="" && value2=="" &&value3!="" && value4!=""){
		return true;
	}
	else {
		alert("There are error in your input form, please make sure correct!");	
		return false;
	}
}

function checkBeforeReg(){
	var value1= document.getElementById("reg_passwordnotes").innerHTML;
	var value2= document.getElementById("reg_useridnotes").innerHTML;
	var value3=document.getElementById("reg_userid").value;
	var value4=document.getElementById("reg_password").value;
	var value5= document.getElementById("check_reg_passwordnotes").innerHTML;
	var value6= document.getElementById("reg_emailnotes").innerHTML;
	var value7=document.getElementById("reg_email").value;
	var value8=document.getElementById("check_reg_password").value;
	if ( value1=="" && value2=="" && value3!="" && value4!="" && value5=="" && value6=="" && value7!="" &&value8!=""){
		return true;
	}
	else {
		alert("There are error in your input form, please make sure correct!");
		return false;
	}
}

function checkBeforeResetpw(){
	var value1= document.getElementById("reg_passwordnotes").innerHTML;
	var value2= document.getElementById("reg_useridnotes").innerHTML;
	var value3=document.getElementById("reg_userid").value;
	var value4=document.getElementById("reg_password").value;
	var value5= document.getElementById("check_reg_passwordnotes").innerHTML;
	var value6=document.getElementById("check_reg_password").value;
	if ( value1=="" && value2=="" && value3!="" && value4!="" && value5=="" &&value6!=""){
		return true;
	}
	else {
		alert("There are error in your input form, please make sure correct!");
		return false;
	}
}

function checkBeforeGetpw(){
	var value1= document.getElementById("useridnotes").innerHTML;
	var value2=document.getElementById("uidorpw").value;
	if ( value1=="" && value2!="" ){
		getpw_form.action="/medialabWebapp/rest/user/passwordreset/userid/"+value2;
		return true;
	}
	else {
		alert("There are error in your input form, please make sure correct!");	
		return false;
	}
}

$(window).load(function() {
	var value= getCookie("authcode");
	if (value==""|| value=="null"){
		document.getElementById("loginregdiv").style.display="inline";
		document.getElementById("logineddiv").style.display="none";
	}
	else {
		document.getElementById("loginregdiv").style.display="none";
		document.getElementById("logineddiv").style.display="inline";
		refreshUser(value);
	}
//	var loginstate=document.getElementById("judgeloginstate").innerHTML;
//	if (loginstate!=""&& loginstate!="null"&& loginstate!="success"){
//		alert(loginstate);
//	}
});

function logout(){
	deleteCookie("authcode");
	window.location.reload(); 
}

function refreshUser(value){
	$.ajax({
        type : "GET",  
        url : "/user/authcode/"+value,  //should change
        dataType: "json",  
        success : function(data) {  
        	var userid_value=data.username;
        	var userstorage_value=data.storage;
	        document.getElementById('logineduserdiv').innerHTML="<p style=\"color:#fff;font-size:13px;\">User: "+userid_value +"&nbsp|&nbspStorage: "+userstorage_value+"&nbsp|</p>";
        	
        },
		error :  function() {  
           //do something 
        	document.getElementById('logineduserdiv').innerHTML="error" ;
        }
   });
}

function addCookie(name,value){ 
	var cookieString=name+"="+escape(value); 
	var date=new Date(); 
	date.setTime(date.getTime()+ 30*60*1000); 
	cookieString=cookieString+"; expires="+date.toGMTString(); 
	document.cookie=cookieString; 
} 

function getCookie(name){ 
	var strCookie=document.cookie; 
	var arrCookie=strCookie.split("; "); 
	for(var i=0;i<arrCookie.length;i++){ 
		var arr=arrCookie[i].split("="); 
		if(arr[0]==name)return arr[1]; 
	} 
	return ""; 
} 

function deleteCookie(name){ 
	var date=new Date(); 
	date.setTime(date.getTime()-10000); 
	document.cookie=name+"=null;expires="+date.toGMTString(); 
} 



//var imaRec_timeout= [];
var img_timer;
function gettalkword(imageId){
	$.ajax({
        type : "GET",  
        url : "imagerecstate/"+imageId,
        dataType: "text",  
        success : function(data) { 
        	if (data!="Processing"){
        		var imagerec_state=[];
        		imagerec_state=data.split("\n");
        		for (var i=0;i<imagerec_state.length-1;i++){
        			$('#imageInf').append($('<li>').text(imagerec_state[i]));
        		}
        		clearTimeout(img_timer);
//            	var fileIndex=$('#imageInf').find("li").length;
//    	        var fileNum=$('.upload_preview').find("div.upload_append_list").length;
//    	        if (fileIndex >= fileNum){
    	        $("#imageProcessState").text("Upload Successful! Processing Successful!");
//    	        }
        	}
        	else {
        		img_timer=setTimeout("gettalkword('"+imageId+"')",3000);
        	}
        },
		error :  function() {  
        }
   });
}



