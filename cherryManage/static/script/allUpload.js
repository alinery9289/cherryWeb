
$(function(){
	// 初始化插件
	$("#allupload").zyUpload({
		width            :   "850px",                 // 宽度
//		height           :   "200px",                 // 宽度
		itemWidth        :   "120px",                 // 文件项的宽度
		itemHeight       :   "100px",                 // 文件项的高度
		url              :   "mediafile",  // 上传文件的路径
		multiple         :   true,                    // 是否可以多个文件上传
		dragDrop         :   true,                    // 是否可以拖动上传文件
		del              :   true,                    // 是否可以删除文件
		finishDel        :   false,  				  // 是否在上传文件完成后删除预览
		/* 外部获得的回调接口 */
		onSelect: function(files, allFiles){                    // 选择文件的回调方法
			console.info("You select these files:");
			console.info(files);
			console.info("Files Unuploaded:");
			console.info(allFiles);
		},
		onDelete: function(file, surplusFiles){                     // 删除一个文件的回调方法
			console.info("You delete these files:");
			console.info(file);
			console.info("Files will be upload:");
			console.info(surplusFiles);
		},
		onSuccess: function(file){                    // 文件上传成功的回调方法
			console.info("This file upload succeed:");
			console.info(file);
		},
		onFailure: function(file){                    // 文件上传失败的回调方法
			console.info("Files upload failed:");
			console.info(file);
		},
		onComplete: function(response){           // 上传完成的回调方法
			console.info("Files upload complete:");
		}
	});
});

