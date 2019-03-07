$(document).ready(function(){
    var sendInfo = {}
    $("#btn_hospital_signup").click(function(event){
        var hospitalName = $("#hospital_name").val();
        var hospitalAddress = $("#hospital_address").val();
        var hospitalContact = $("#hospital_contact").val();
        var hospitalType = $("#hospital_type").val();

        sendInfo = {
            hospital_name : hospitalName,
            hospital_address : hospitalAddress,
            hospital_contact : hospitalContact,
            hospital_type : hospitalType
        }
        $.post("/",JSON.stringify(sendInfo),function(response){
            window.location.replace("/?message="+response["message"])
        });

        event.preventDefault();
    });
});