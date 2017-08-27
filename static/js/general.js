$(document).ready(function(){
	/* user functions start */
	
	/* settings */
    $.base64.utf8encode = true;
	$("#main-container-user").height($(document).height()-120);
	
	/* general functions */
	var show_logged_in = function(){
		var user_id = localStorage.user_id;
		var authorization = localStorage.authorization;
		
		if (user_id !== undefined && authorization !== undefined) {
			if (user_id.length > 0 && authorization.length > 0) {
				var firstname = localStorage.firstname;
				var initials = localStorage.initials;
				
				$("#main-container").css("display", "none");
				$("#main-container-user").css("display", "block");
				$("#button-container").css("display", "none");
				$("#profile-container").css("display", "block");
				$('#profile_name').text(firstname);
				$('#profile').text(initials);
				
				getMealList();
			}
		}
	};
	
	var logoutClear = function(){
		localStorage.clear();
		
		$("#main-container").css("display", "block");
		$("#main-container-user").css("display", "none");
		$("#button-container").css("display", "block");
		$("#profile-container").css("display", "none");
		$('#profile_name').text('');
		$('#profile').text('CT');
	};
	
	var getMealList = function(){
		$.ajax({
			url: '/meals/',
			type : "GET",
			headers : {
				'AUTHORIZATION' : localStorage.authorization
			},
			dataType : 'json',
			data : {
				user_id : localStorage.user_id,
				meal_date_from : localStorage.meal_date_from,
				meal_date_to : localStorage.meal_date_to,
				meal_time_from : localStorage.meal_time_from,
				meal_time_to : localStorage.meal_time_to
			},
			complete : function(data) {
				var obj = $.parseJSON(data.responseText);
				
				if (data.status==200){
					var columns = '';
					var objLen = Object.keys(obj.data).length;
					
					if (objLen===0) {
						$("#rows-container").html('<div class="rows-data-line">No meals have been captured or meet your search criteria</div>');
					}else{
						$("#rows-container").html('');
						var i = 0;
						var html = '';
						var date_change = '';
						var daily_calorie = 0;
					
						while (i < objLen) {
							if (date_change != obj.data['meal_'+i].meal_date) {
								if (i!==0) {
									if (parseInt(daily_calorie,10) <= parseInt(localStorage.calories,10)) {
										columns = '<div class="rows-data-column-green" title="below daily target"></div>';
									}else{
										columns = '<div class="rows-data-column-red" title="above daily target"></div>';
									}
									
									columns += '<div class="rows-data-column-desc">Calorie Summary for '+date_change+'</div>';
									columns += '<div class="rows-data-column-desc">Daily Calorie Intake: '+daily_calorie+' (my limit: '+localStorage.calories+')</div>';
									
									summary = '<div class="rows-data-summary">' + columns + '</div>';
									summary += '<div class="rows-data-line-dotted"></div>';
									html = summary + html + '<div class="rows-data-line-line"></div>';
									
									$("#rows-container").append(html);
								}
								
								date_change = obj.data['meal_'+i].meal_date;
								daily_calorie = 0;
								html = '';
							}
							
							daily_calorie += parseInt(obj.data['meal_'+i].calories,10);
							
							columns = '<div class="rows-data-column-spacer"></div>';
							columns += '<div class="rows-data-column-desc">Meal: '+obj.data['meal_'+i].meal_desc+'</div>';
							columns += '<div class="rows-data-column">Calories: '+obj.data['meal_'+i].calories+'</div>';
							columns += '<div class="rows-data-column">Date: '+obj.data['meal_'+i].meal_date+'</div>';
							columns += '<div class="rows-data-column">Time: '+obj.data['meal_'+i].meal_time+'</div>';
							columns += '<div id="meal-edit" title="edit meal" data-meal-id="'+obj.data['meal_'+i].meal_id+'"><img src="'+STATIC_URL+'images/edit.png"></div>';
							
							html += '<div class="rows-data-line">'+columns+'</div>';
							//html += '<div class="rows-data-line-line"></div>';
							i++;
						}
						
						if (html.length > 0) {
							if (parseInt(daily_calorie,10) <= parseInt(localStorage.calories,10)) {
								columns = '<div class="rows-data-column-green" title="below daily target"></div>';
							}else{
								columns = '<div class="rows-data-column-red" title="above daily target"></div>';
							}
							
							columns += '<div class="rows-data-column-desc">Calorie Summary for '+date_change+'</div>';
									columns += '<div class="rows-data-column-desc">Daily Calorie Intake: '+daily_calorie+' (my limit: '+localStorage.calories+')</div>';
							
							summary = '<div class="rows-data-summary">' + columns + '</div>';
							summary += '<div class="rows-data-line-dotted"></div>';
							html = summary + html + '<div class="rows-data-line-line"></div>';
							
							$("#rows-container").append(html);
						}
					}
				} else if (data.status==404){
					$("#rows-container").html('<div class="rows-data-line">No meals have been captured or meet your search criteria</div>');
				} else {
					alert(obj.message);
				}
			}
		});
	};
	
	/* login functions */
	show_logged_in();
	
	$('#login').click(function(){
		$("#login_username").val('');
		$("#login_password").val('');
		$("#login_popup").css("display", "block");
		$("#login_popup").height($(document).height());
		$(document).scrollTop(0);
	});
	
	$('#login_login').click(function(){
		$.ajax({
			url: '/users/',
			type : "GET",
			dataType : 'json',
			headers : {
				'AUTHORIZATION' : $.base64.encode($("#login_username").val() + ":" + $("#login_password").val())
			},
			complete : function(data) {
				var obj = $.parseJSON(data.responseText);
				
				if (data.status==200){
					localStorage.setItem('user_id', obj.data.user_0.user_id);
					localStorage.setItem('authorization', obj.data.user_0.authorization);
					localStorage.setItem('firstname', obj.data.user_0.firstname);
					localStorage.setItem('initials', obj.data.user_0.initials);
					localStorage.setItem('calories', obj.data.user_0.calories);
					
					$("#login_popup").css("display", "none");
					
					show_logged_in();
				} else {
					alert(obj.message);
				}
			}
		});
	});
	
	$('#login_close').click(function(){
		$("#login_popup").css("display", "none");
	});
	
	/* register functions */
	$('#register').click(function(){
		$("#register_username").val('');
		$("#register_password").val('');
		$("#register_firstname").val('');
		$("#register_surname").val('');
		$("#register_calories").val('');
		$("#register_popup").css("display", "block");
		$("#register_popup").height($(document).height());
		$(document).scrollTop(0);
	});
	
	$('#register_register').click(function(){
		$.ajax({
			url: '/users/',
			type : "POST",
			headers : {
				'AUTHORIZATION' : $.base64.encode($("#register_username").val() + ":" + $("#register_password").val())
			},
			dataType : 'json',
			data : {
				firstname : $("#register_firstname").val(),
				surname : $("#register_surname").val(),
				calories : $("#register_calories").val()
			},
			complete : function(data) {
				var obj = $.parseJSON(data.responseText);
				
				if (data.status==201){
					localStorage.setItem('user_id', obj.data.user_id);
					localStorage.setItem('authorization', obj.data.authorization);
					localStorage.setItem('firstname', obj.data.firstname);
					localStorage.setItem('initials', obj.data.initials);
					localStorage.setItem('calories', obj.data.calories);
					
					$("#register_popup").css("display", "none");
					
					show_logged_in();
				} else {
					alert(obj.message);
				}
			}
		});
	});
	
	$('#register_close').click(function(){
		$("#register_popup").css("display", "none");
	});
	
	$("#register_calories").keypress(function(event) {
		var dec = /^[0-9]+$/;
        return dec.test(String.fromCharCode(event.which));
    });
	
	/* profile functions */
	$('#profile').click(function(){
		$.ajax({
			url: '/users/',
			type : "GET",
			headers : {
				'AUTHORIZATION' : localStorage.authorization
			},
			data : {
				user_id : localStorage.user_id
			},
			complete : function(data) {
				var obj = $.parseJSON(data.responseText);
				
				if (data.status==200){
					var authorization = $.base64.decode(obj.data.user_0.authorization).split(':');
					
					$("#profile_username").val(authorization[0]);
					$("#profile_password").val(authorization[1]);
					$("#profile_firstname").val(obj.data.user_0.firstname);
					$("#profile_surname").val(obj.data.user_0.surname);
					$("#profile_calories").val(obj.data.user_0.calories);
					$("#profile_popup").css("display", "block");
					$("#profile_popup").height($(document).height());
					$(document).scrollTop(0);
				} else {
					alert(obj.message);
				}
			}
		});
	});
	
	$('#profile_save').click(function(){
		$.ajax({
			url: '/users/',
			type : "POST",
			headers : {
				'AUTHORIZATION' : localStorage.authorization,
				'UPDATE_AUTHORIZATION' : $.base64.encode($("#profile_username").val() + ":" + $("#profile_password").val()),
				'X_METHODOVERRIDE': 'PUT'
			},
			dataType : 'json',
			data : {
				user_id : localStorage.user_id,
				firstname : $("#profile_firstname").val(),
				surname : $("#profile_surname").val(),
				calories : $("#profile_calories").val()
			},
			complete : function(data) {
				var obj = $.parseJSON(data.responseText);
				
				if (data.status==200){
					localStorage.setItem('user_id', obj.data.user_id);
					localStorage.setItem('authorization', obj.data.authorization);
					localStorage.setItem('firstname', obj.data.firstname);
					localStorage.setItem('initials', obj.data.initials);
					localStorage.setItem('calories', obj.data.calories);
					
					$("#profile_popup").css("display", "none");
					
					show_logged_in();
				} else {
					alert(obj.message);
				}
			}
		});
	});
	
	$('#profile_delete').click(function(){
		if (confirm('Are you sure you wish to delete your profile?')){
			$.ajax({
				url: '/users/',
				type : "POST",
				headers : {
					'AUTHORIZATION' : localStorage.authorization,
					'X_METHODOVERRIDE': 'DELETE'
				},
				dataType : 'json',
				data : {
					user_id : localStorage.user_id
				},
				complete : function(data) {
					var obj = $.parseJSON(data.responseText);
					
					if (data.status==200){
						alert(obj.message);
						$("#profile_popup").css("display", "none");
						logoutClear();
					} else {
						alert(obj.message);
					}
				}
			});
		}
	});
	
	$('#profile_close').click(function(){
		$("#profile_popup").css("display", "none");
	});
	
	/* logout functions */
	$('#logout').click(function(){
		logoutClear();
	});
	
	/* user functions end */
	
	/* meal functions start */
	
	/* meal add functions */
	$('#meal-add').click(function(){
		$("#meal_add_meal_desc").val('');
		$("#meal_add_calories").val('');
		$("#meal_add_meal_date").val('');
		$("#meal_add_popup").css("display", "block");
		$("#meal_add_popup").height($(document).height());
		$(document).scrollTop(0);
	});
	
	$('#meal_add_save').click(function(){
		datemeal = $("#meal_add_meal_date").val().split(' ');
		mealdate ='';
		mealtime ='';
		
		if (datemeal.length == 2) {
			mealdate = datemeal[0];
			mealtime = datemeal[1];
		}
		
		$.ajax({
			url: '/meals/',
			type : "POST",
			headers : {
				'AUTHORIZATION' : localStorage.authorization
			},
			dataType : 'json',
			data : {
				user_id : localStorage.user_id,
				meal_desc : $("#meal_add_meal_desc").val(),
				calories : $("#meal_add_calories").val(),
				meal_date : mealdate,
				meal_time : mealtime
			},
			complete : function(data) {
				var obj = $.parseJSON(data.responseText);
				
				if (data.status==201){
					$("#meal_add_popup").css("display", "none");
					getMealList();
				} else {
					alert(obj.message);
				}
			}
		});
	});
	
	$('#meal_add_close').click(function(){
		$("#meal_add_popup").css("display", "none");
	});
	
	$("#meal_add_calories").keypress(function(event) {
		var dec = /^[0-9]+$/;
        return dec.test(String.fromCharCode(event.which));
    });
	
	$('#meal_add_meal_date').datetimepicker({
		dayOfWeekStart : 1,
		lang:'en',
		format:'Y-m-d H:i',
		formatDate:'Y-m-d',
		step:15
	});
	
	/* meal edit functions */
	$("#rows-container").on("click", "#meal-edit", function() {
		meal_id = $(this).attr("data-meal-id");
		$.ajax({
			url: '/meals/',
			type : "GET",
			headers : {
				'AUTHORIZATION' : localStorage.authorization
			},
			data : {
				user_id : localStorage.user_id,
				meal_id : meal_id
			},
			complete : function(data) {
				var obj = $.parseJSON(data.responseText);
				
				if (data.status==200){
					$("#meal_edit_meal_id").val(meal_id);
					$("#meal_edit_meal_desc").val(obj.data.meal_0.meal_desc);
					$("#meal_edit_calories").val(obj.data.meal_0.calories);
					$("#meal_edit_meal_date").val(obj.data.meal_0.meal_date + ' ' + obj.data.meal_0.meal_time);
					$("#meal_edit_popup").css("display", "block");
					$("#meal_edit_popup").height($(document).height());
					$(document).scrollTop(0);
				} else {
					alert(obj.message);
				}
			}
		});
	});
	
	$('#meal_edit_save').click(function(){
		datemeal = $("#meal_edit_meal_date").val().split(' ');
		mealdate ='';
		mealtime ='';
		
		if (datemeal.length == 2) {
			mealdate = datemeal[0];
			mealtime = datemeal[1];
		}
		
		$.ajax({
			url: '/meals/',
			type : "POST",
			headers : {
				'AUTHORIZATION' : localStorage.authorization,
				'X_METHODOVERRIDE': 'PUT'
			},
			dataType : 'json',
			data : {
				user_id : localStorage.user_id,
				meal_id : $("#meal_edit_meal_id").val(),
				meal_desc : $("#meal_edit_meal_desc").val(),
				calories : $("#meal_edit_calories").val(),
				meal_date : mealdate,
				meal_time : mealtime
			},
			complete : function(data) {
				var obj = $.parseJSON(data.responseText);
				
				if (data.status==200){
					$("#meal_edit_popup").css("display", "none");
					getMealList();
				} else {
					alert(obj.message);
				}
			}
		});
	});
	
	$('#meal_edit_close').click(function(){
		$("#meal_edit_popup").css("display", "none");
	});
	
	$("#meal_edit_calories").keypress(function(event) {
		var dec = /^[0-9]+$/;
        return dec.test(String.fromCharCode(event.which));
    });
	
	$('#meal_edit_meal_date').datetimepicker({
		dayOfWeekStart : 1,
		lang:'en',
		format:'Y-m-d H:i',
		formatDate:'Y-m-d',
		step:15
	});
	
	$('#meal_edit_delete').click(function(){
		if (confirm('Are you sure you wish to delete this meal?')){
			$.ajax({
				url: '/meals/',
				type : "POST",
				headers : {
					'AUTHORIZATION' : localStorage.authorization,
					'X_METHODOVERRIDE': 'DELETE'
				},
				dataType : 'json',
				data : {
					user_id : localStorage.user_id,
					meal_id : $("#meal_edit_meal_id").val()
				},
				complete : function(data) {
					var obj = $.parseJSON(data.responseText);
					
					if (data.status==200){
						alert(obj.message);
						$("#meal_edit_popup").css("display", "none");
						getMealList();
					} else {
						alert(obj.message);
					}
				}
			});
		}
	});

	/* filter functions */
	$('#meal-filter').click(function(){
		if (localStorage.meal_time_from !== undefined || localStorage.meal_time_to !== undefined) {
			if (localStorage.meal_time_from.length > 0 || localStorage.meal_time_to.length > 0) {
				$("#filter_meal_check").prop('checked', true);
				$('#time_container').css("display", "block");
			} else {
				$("#filter_meal_check").prop('checked', false);
				$('#time_container').css("display", "none");
			}
		} else {
			$("#filter_meal_check").prop('checked', false);
			$('#time_container').css("display", "none");
		}
		
		$("#filter_meal_date_from").val(localStorage.meal_date_from);
		$("#filter_meal_date_to").val(localStorage.meal_date_to);
		$("#filter_meal_time_from").val(localStorage.meal_time_from);
		$("#filter_meal_time_to").val(localStorage.meal_time_to);
		$("#filter_popup").css("display", "block");
	});
	
	$('#filter_meal_date_from').datetimepicker({
		dayOfWeekStart : 1,
		lang:'en',
		format:'Y-m-d',
		formatDate:'Y-m-d',
		timepicker:false
	});
	
	$('#filter_meal_date_to').datetimepicker({
		dayOfWeekStart : 1,
		lang:'en',
		format:'Y-m-d',
		formatDate:'Y-m-d',
		timepicker:false
	});
	
	$('#filter_meal_time_from').datetimepicker({
		datepicker:false,
		format:'H:i',
		step:15
	});
	
	$('#filter_meal_time_to').datetimepicker({
		datepicker:false,
		format:'H:i',
		step:15
	});
	
	$('#filter_meal_check').click(function(){
		$('#time_container').toggle();
	});
	
	$('#filter_filter').click(function(){
		localStorage.meal_date_from=$("#filter_meal_date_from").val();
		localStorage.meal_date_to=$("#filter_meal_date_to").val();
		
		if ($("#filter_meal_check").is(":checked")) {
			localStorage.meal_time_from=$("#filter_meal_time_from").val();
			localStorage.meal_time_to=$("#filter_meal_time_to").val();
		} else {
			localStorage.meal_time_from='';
			localStorage.meal_time_to='';
		}
		
		$("#filter_popup").css("display", "none");
		getMealList();
	});
	
	$('#filter_clear').click(function(){
		localStorage.meal_date_from='';
		localStorage.meal_date_to='';
		localStorage.meal_time_from='';
		localStorage.meal_time_to='';
		$("#filter_popup").css("display", "none");
		getMealList();
	});
	
	/* meal functions end */
});
