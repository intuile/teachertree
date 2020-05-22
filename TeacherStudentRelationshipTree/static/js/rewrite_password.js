
function regclick(){ 
    //alert("1");
    var p1=document.getElementById("reg00").value;//获取密码框的值
    var p2=document.getElementById("reg01").value;//获取重新输入的密码值
    
    if((p1.length<6 || p1.length>16)||(p2.length<6 || p2.length>16) )
    {
        alert("Password  should longer than 5 an shorter than 17");
        return false;
    }
    else if((p1!=p2) ){//判断两次输入的值是否一致，不一致则显示错误信息
        //document.getElementById("msg").innerHTML="两次输入密码不一致，请重新输入";//在div显示错误信息
        alert("Two passwords are not agree,try again");
        return false;
    }   
    else{
       // document.getElementById("regbtn").removeAttr("disabled");//密码一致，可以继续下一步操作
       alert("Congradulation, you pass has rewritten");
       return true;
    }
}