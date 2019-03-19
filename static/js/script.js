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

        addInfo={
            responder_firstname : firstname,
            responder_middlename : middlename,
            responder_lastname : lastname,
        };

        if(firstname != "" && middlename != "" && lastname != ""){
             $.post("/responders",JSON.stringify(addInfo),function(response){
                window.location.replace("/responders?add="+response["add"]+"&message="+response["message"]);
            });
        }else{
            window.location.replace("/responders?all_fields=required");
        }
        e.preventDefault();
    });

});