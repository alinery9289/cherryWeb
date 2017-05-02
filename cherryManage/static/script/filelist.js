
var authcode="";
$(window).load(function() {
	authcode= getCookie("authcode");
	if (authcode==""|| authcode=="null"){
		document.getElementById("filelistul").innerHTML="Please login first";			
	}
	else {
		refreshFilelist(authcode);
	}
});

function refreshFilelist(authcode){
	$.ajax({
        type : "GET",  
        url : "/mediafile/info/authcode/"+authcode,
        dataType: "json",  
        success : function(data) { 
        	var htmlvalue='';
        	$.each(data,function(idx,item){ 
        		var fileid_value=item.fileid;
        		var filename_value=item.filename; 
        		var location_value=item.location; 
        		var filesize_value=item.filesize;
        		var filetype_value=item.filetype;
        		var uploadtime_value=item.uploadtime;
        		var encodeinfo_value=item.encodeinfo;
        		var encodeinfo_value= encodeinfo_value.replace(/\n/g,"</p><p>");
        		if(filetype_value.indexOf("image/") > -1){
        			htmlvalue+='<li> <img class="filelistimg" src="'+location_value+'" onclick="playimage(\''+ location_value+'\');"/>';
    	        	htmlvalue+='<div class="filelistname"><a href="'+location_value+'" target="_blank"> '+ filename_value+'</a></div>';
    	        	htmlvalue+='<div class="filelistname" >type: '+filetype_value+' | size: '+filesize_value+' | upload time: '+uploadtime_value+'</div>';
    	        	htmlvalue+='<div class="deletebutton"><input type="button" title="delete" value="" onclick="deletefile(\''+ fileid_value+'\');"></input></div>';
    	        	htmlvalue+='<div class="playbutton"><input type="button" title="show" value="" onclick="playimage(\''+ location_value+'\');"></input></div></li>';
        		
        		}
        		else {
        			htmlvalue+='<li id="li_'+fileid_value+'"> <a href="'+location_value+'" class="filelistimg" style="background:url(static/images/file.png)"></a>';
    	        	htmlvalue+='<div class="filelistname"><a href="'+location_value+'" target="_blank"> '+ filename_value+'</a></div>';
    	        	htmlvalue+='<div class="filelistname" >type: '+filetype_value+' | size: '+filesize_value+' | upload time: '+uploadtime_value+' | <a href="javascript:void(0)" onclick="showEncodeInfo(\'li_'+fileid_value+'\')">Encode Info</a></div>';
    	        	htmlvalue+='<div class="deletebutton"><input type="button" title="delete" value="" onclick="deletefile(\''+ fileid_value+'\');"></input></div>';
    	        	htmlvalue+='<div class="playbutton"><input type="button" title="copy to user ftp" value="" onclick="downloadtouserftp(\''+fileid_value+'\');"></input></div>';
    	        	htmlvalue+='<div class="encodeInfodiv"><p>'+encodeinfo_value+'</p></div></li>';
    	        }
	         });
        	
    		document.getElementById("filelistul").innerHTML=htmlvalue;
    		
    		$(function() {

    		    /* initiate plugin */
    		    $("div.holder").jPages({
    		      containerID : "filelistul",
    		      perPage :parseInt($("select").val()),
    		      delay       : 0
    		    });

    		    /* on select change */
    		    $("select").change(function(){
    		      /* get new nº of items per page */
    		      var newPerPage = parseInt( $(this).val() );

    		      /* destroy jPages and initiate plugin again */
    		      $("div.holder").jPages("destroy").jPages({
    		        containerID   : "filelistul",
    		        perPage       : newPerPage,
    		        delay       : 0
    		      });
    		    });

    		 });
  	
        },
		error :  function() {  
           //do something 
        }
   });	
	
}

function refreshDeallogs(){
	$.ajax({
        type : "GET",  
        url : "/medialabWebapp/rest/deallogs/authcode/"+authcode,
        dataType: "xml",  
        success : function(data) { 
        	if ($(data).children("deallogModels").text()!=""){
        		var sumUnSucceed=0;
        		var htmlvalue='<table id="exampletable" ><thead>'+
        			'<tr><th class="th1">原文件</th><th class="th2">处理方式</th><th class="th3">状态</th>'+
        			'<th class="th4">处理后文件</th><th class="th5">开始时间</th><th class="th6">结束时间</th></tr></thead>';	
        	
        		$(data).find("deallogModel").each(function(i){  
        			var filename_value=$(this).children("filename").text(); 
        			var dealmethod_value=$(this).children("dealmethod").text(); 
		    		var dealstate_value=$(this).children("dealstate").text();
		    		var afterfilename_value=$(this).children("afterfilename").text();
		    		var dealtime_value=$(this).children("dealtime").text(); 
		    		var completetime_value=$(this).children("completetime").text(); 
		    		if (dealstate_value!="succeed"){
		    			sumUnSucceed+=1;
		    		}
		    		htmlvalue+='<tr><td>'+filename_value+'</td>';
		    		htmlvalue+='<td>'+dealmethod_value+'</td>';
		    		htmlvalue+='<td>'+dealstate_value+'</td>';
		    		htmlvalue+='<td>'+afterfilename_value+'&nbsp;</td>';
		    		htmlvalue+='<td><p style="word-break:normal; word-wrap:normal;">'+dealtime_value+'</p></td>';
		    		htmlvalue+='<td><p style="word-break:normal; word-wrap:normal;">'+completetime_value+'</p></td></tr>';
		         });
        	
	    		document.getElementById("dealtable").innerHTML =htmlvalue+'</table>';
	    		$(function() {
	    			$("#exampletable").slimtable();
	    		});
	    		if (sumUnSucceed!=0){
//	    			alert("haha");
	    			var unSuc_timeout=setTimeout("refreshDeallogs()",1000);
	    		}
	    		else {
	    			clearTimeout(unSuc_timeout);
	    			refreshFilelist();
	    		}
        	}
        	else{document.getElementById("dealtable").innerHTML="";}
        },
		error :  function() {  
           //do something 
        }
   });	
}

function deletefile(fileid){
	authcode= getCookie("authcode");
	if(confirm('Delete this file now?')){
		$.ajax({
	        type : "DELETE",  
	        url : "/mediafile/fileid/"+fileid+"/authcode/"+authcode,
	        dataType: "text",  
	        success : function(data) { 
	        	refreshFilelist(authcode);
//	        	refreshDeallogs();
	    		refreshUser(authcode);
	        },
			error :  function() {  
	           //do something 
	        }
	   });
	}	
}


function downloadtouserftp(fileid){
	authcode = getCookie("authcode");
	$.ajax({
        type : "GET",  
        url : "/ftpmediafile/fileid/"+fileid+"/authcode/"+authcode,
        dataType: "text",  
        success : function(data) {
        	if (data=="succeed") alert("Save file in ftp /download.");
        },
		error :  function() {  
			alert("Wrong! Please try again.")
        }
   });
}

function showEncodeInfo(li_id){
	$("#"+li_id+" .encodeInfodiv").slideToggle("normal");
	
//	var encodeinfoReal= encodeinfo.replace(/;/g,"<br>");
//	$('#encodeinfotext').text(''+encodeinfoReal+'');
//	$(".playvideomask").fadeIn(500);
//	$("#playEncodeInfoBox").fadeIn(500);
}





