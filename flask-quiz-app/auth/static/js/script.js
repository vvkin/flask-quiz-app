$(document).ready(function(){
    $('#f_passwd, #s_passwd').on('keyup', function(){
        $('.error').hide();
        if ($('#f_passwd').val() !== $('#s_passwd').val()){
            $('#s_passwd').after('<span class="error">Passwords does not match!</span>');
            $('#submit').attr('disabled', 'disabled');
        }
        else {
            $('#submit').removeAttr('disabled');
        }
    });
});