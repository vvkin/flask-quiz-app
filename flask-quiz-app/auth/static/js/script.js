function checkPasswords(){
    firstPassword = getElementsByName('u_passwd')[0];
    secondPassword = getElementsByName('us_passwd')[0];
    if (firstPassword !== secondPassword){
        getElementById('submit_button').enabled = false;
        getElementById('flash_message').innerHTML = 'Passwords mismatch!'
    }
    else{
        getElementById('submit_button').enabled = true;
    }
}

