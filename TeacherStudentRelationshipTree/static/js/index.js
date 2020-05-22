
function regclick(){ 
    //alert("1");
    var p1=document.getElementById("reg1").value;//获取密码框的值
    var p2=document.getElementById("reg2").value;//获取重新输入的密码值
    var p3=document.getElementById("reg3").value;
    if((p1.length<6 || p1.length>16)||(p2.length<6 || p2.length>16)||(p3.length<6 || p3.length>16) )
    {
        alert("Password and ID should longer than 5 an shorter than 17");
        return false;
    }
    else if((p1!=p2) || (p3=="Set a ID for reclaim pass")){//判断两次输入的值是否一致，不一致则显示错误信息
        //document.getElementById("msg").innerHTML="两次输入密码不一致，请重新输入";//在div显示错误信息
        alert("Two passwords are not agree and ID is must, please try again");
        return false;
    }   
    else{
       // document.getElementById("regbtn").removeAttr("disabled");//密码一致，可以继续下一步操作
       alert("Right");
       return true;
    }
}
function check(it)
{
    if (it.value == '') {
        it.value = "Set a ID for reclaim pass";
    }

}
