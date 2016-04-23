$(document).ready(function () {

$("#register-form").validate({
    rules: {
      reg_username: "required",
      reg_password: {
            required: true,
            minlength: 8
        },
        reg_password_confirm: {
            required: true,
            minlength: 8,
            equalTo: "#register-form [name=reg_password]"
        },
        reg_email: {
        required: true,
            email: true
        },
      first_name: "required",
      last_name: "required"
    }
  });

$("#reg_username").focusout(function(){
    if($("#reg_username").val() != ""){
      $.get("/tagging/check/", {"reg_username": $(this).val()}, function(data){
        if(data.code == 0)
          {
            $("#reg_user_status").html("");
          }
        else{
          $("#reg_user_status").html(data.message);
        }
      });
    }
});

});

function showReg(){
    $("#login_modal").fadeOut(0);
    $("#reg_modal").fadeIn(0);
}

function showLogin(){
    $("#reg_modal").fadeOut(0);
    $("#login_modal").fadeIn(0);
}