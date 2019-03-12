$(document).ready(function(){
    var sendInfo={};

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

});