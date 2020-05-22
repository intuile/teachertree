// 从login.html的modal获取两次密码信息和id信息;进行正确性验证;
function validateForm() {
    var pass1 = document.forms["form2"]["reg_password1"].value;
    var pass2 = document.forms["form2"]["reg_password2"].value;
    var id = document.forms["form2"]["reg_id"].value;
    var commit = document.forms["form2"]["reg_btn"].value;

    if ((pass1.length < 6 || pass1.length > 16) || (pass2.length < 6 || pass2.length > 16) || (id.length < 6 || id.length > 16)) {
        alert("Password and ID should longer than 5 an shorter than 17");
        return false;
    }
    else if(pass1!=pass2){        
        alert("Two passwords are not same, please try again");
        return false;
    }
    else{
        alert("right");
        return true;
    }
}