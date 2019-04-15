 // Enable pusher logging - don't include this in production
    //  Pusher.logToConsole = true;

     var pusher = new Pusher('f6f266841f565e4e7b21', {
       cluster: 'ap1',
       forceTLS: true
     });
 
     var channel = pusher.subscribe('hospital_channel');
     channel.bind('alert_event', function(data) {
       console.log(JSON.stringify(data));
       $('#location').text(data.report_location);
       $('#emergency_type').text(data.report_type);
       $('#reportModal').modal('show');
     });

     var channel = pusher.subscribe('dispatch_channel');
     channel.bind('dispatch_event', function(data) {
        //  if(data["hospital_name"] == )
     });

     
$(document).ready(function(){
    var sendInfo={};

    //Hospital Sign Up
    $("#btnSignUp").click(function(e){
        var name = $("#hospital_name").val();
        var address = $("#hospital_address").val();
        var email = $("#hospital_email").val();
        var contact = $("#hospital_contact").val();
        var password = $("#hospital_password").val();
        var cpassword = $("#hospital_cpassword").val();
        var type = $("#hospital_type").val();

        sendInfo={
            hospital_name : name,
            hospital_address : address,
            hospital_email : email,
            hospital_contact : contact,
            hospital_password : password,
            hospital_type : type
        };

        if(name != "" && address != "" && email != "" && contact != "" && password != "" && cpassword != "" && type != ""){
            if(cpassword==password){
                $.post("/signup",JSON.stringify(sendInfo),function(response){
                    window.location.replace("/signup?signup="+response["signup"]+"&message="+response["message"]);
                });
            }else{
                window.location.replace("/signup?confirm_password=incorrect");
            }
        }else{
            window.location.replace("/signup?all_fields=required");
        }
        e.preventDefault();
    });
    //Hospital Sign In
    $("#btnSignIn").click(function(e){
        var email = $("#hospital_email").val();
        var password = $("#hospital_password").val();

        sendInfo={
            hospital_email : email,
            hospital_password : password
        };

        $.post("/signin",JSON.stringify(sendInfo),function(response){
            if(response['signin'] == "success"){
                window.location.replace("/");
            } else if(response['signin'] == "failed"){
                window.location.replace("/signin?signin="+response['signin']+"&message="+response['message']);
            }
        });
        
        e.preventDefault();
    });
    //Add Responder
    $("#btnAddResponder").click(function(e){
        var firstname = $("#responder_firstname").val();
        var middlename = $("#responder_middlename").val();
        var lastname = $("#responder_lastname").val();

        sendInfo={
            responder_firstname : firstname,
            responder_middlename : middlename,
            responder_lastname : lastname,
            responder_option: "add"

        };

        if(firstname != "" && middlename != "" && lastname != ""){
             $.post("/responders",JSON.stringify(sendInfo),function(response){
                window.location.replace("/responders?add="+response["add"]+"&message="+response["message"]);
            });
        }else{
            window.location.replace("/responders?all_fields=required");
        }
        e.preventDefault();
    });
    //Edit Responder
    $("#btnEdit1Responder").click(function(e){
        var id = $(this).data('responder-id');
        $("#edit_responder_id").val($(this).closest('tr').children('td.responder_id').text());
        $("#edit_responder_firstname").val($(this).closest('tr').children('td.responder_firstname').text());
        $("#edit_responder_middlename").val($(this).closest('tr').children('td.responder_middlename').text());
        $("#edit_responder_lastname").val($(this).closest('tr').children('td.responder_lastname').text());
    });
    
    $("#btnEditResponder").click(function(e){
        var id = $("#edit_responder_id").val().trim();
        var firstname = $("#edit_responder_firstname").val();
        var middlename = $("#edit_responder_middlename").val();
        var lastname = $("#edit_responder_lastname").val();

        sendInfo={
            responder_id : id,
            responder_firstname : firstname,
            responder_middlename : middlename,
            responder_lastname : lastname,
            responder_option : "edit"
        };

        if(firstname != "" && middlename != "" && lastname != ""){
             $.post("/responders",JSON.stringify(sendInfo),function(response){
                window.location.replace("/responders?edit="+response["edit"]+"&message="+response["message"]);
            });
        }else{
            window.location.replace("/responders?all_fields=required");
        }
        e.preventDefault();
    });
    //Delete Responder

    $("#btnDeleteResponder").click(function(e){
       if(confirm("Are you sure you want to delete?")){
         var id = $(this).closest('tr').children('td.responder_id').text();
         $(this).closest('tr').hide(1000);
         
         sendInfo={
             responder_id : id,
             responder_option: "delete"
         }

         $.post("/responders",JSON.stringify(sendInfo),function(response){
         });
       }
        e.preventDefault();
    });
    

    //Add Report
    $("#btnSubmitReport").click(function(e){
        var location = $("#report_location").val();
        var type= $("#report_type").val();
        var others = $("#report_others").val();

        sendInfo={
            report_location : location,
            report_type : type,
            report_others : others,
        };

        if(location != "" && type != "" && others != ""){
             $.post("/alert",JSON.stringify(sendInfo),function(response){
                window.location.replace("/reports?="+response["add_report"]+"&message="+response["message"]);
            });
        }else{
            window.location.replace("/reports?all_fields=required");
        }
        e.preventDefault();
    });

    $(".accept").click(function(){
        var btnAccept = $(this);
        var id = btnAccept.data("id");
        $('#titleModal').text("Deploy Response Unit");
        $('#reportid').val(id);
        $('#neutralModal').modal('show');
     });

    $(".decline").click(function(){
        var btnDecline = $(this);
        var id = btnDecline.data("id");

        sendInfo={
            report_id : id,
            report_option : "declined"
        };
        var channel = pusher.subscribe('decline_channel');
            channel.bind('decline_event', function(data) {
                btnDecline.closest('tr').children('td.status').text(data.report_status);
                $('#titleModal').text("Patient Declined");
                $('#neutralMessage').text(data.message);
                $('#neutralModal').modal('show');
            }); 

        $.post("/reports",JSON.stringify(sendInfo),function(response){
                
        });
    });

    $(".dispatch").click(function(){
        var reportid = $("#reportid").val();
        var responder = $("#selectResponder").val();
        sendInfo={
            report_id : reportid,
            report_option : "accepted",
            responder : responder
        };
        
        var channel = pusher.subscribe('accept_channel');
            channel.bind('accept_event', function(data) {
                $('tr#'+reportid).children('td.status').text(data.report_status);
                $(".accept").attr("disabled","disabled");
                $(".decline").attr("disabled","disabled");
            });

        $.post("/reports",JSON.stringify(sendInfo),function(response){
        });

    });

        

});