$(function () {
    // jiao yan mi ma shi fou xiang deng
    $('#password2').change(function () {
        //huoqu p1 he p2 de zhi
        p1 = $('#password1').val();
        p2 = $('#password2').val();
        //jin xing bi dui
        if (p1 == p2){
            $('#pwdmsg').html('sucess').css('color', 'green')
        }else{
            $('#pwdmsg').html('false').css('color', 'red')
        }

        //jie guo chu li
    })
    $('#username').change(function () {
        var name = $('#username').val()
        $.getJSON('/app/chkuser', {'name': name},function (data) {
            if(data.code == '200'){
                $("#userdesc").html(data.desc).css('color', 'green')
            }else if(data.code == '700'){
                $("#userdesc").html(data.desc).css('color', 'red')
            }
            // console.log(data)
        })
    })
});

function subform() {
    var temp = $('#pwdmsg').attr('style');
    var temp1 = $('#userdesc').attr('style');
    if(temp | temp1 == 'color: red;'){
        return false
    }
    // huo qu biao dian mi ma
    pwd = $('#password1').val();
    pwd = md5(pwd);
    $('#password1').val(pwd);
    return true;

}