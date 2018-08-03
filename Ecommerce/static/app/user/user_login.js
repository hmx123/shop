function checklogin() {
    pwd = $('#password1').val()

    $('#password1').val(md5(pwd))
    return true
}