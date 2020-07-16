$(function(){
    let percentSpan = $('.percent span');
    let percentDiv = percentSpan.parent();
    let percentValue = parseInt(percentSpan.text());
    console.log('aaa');
    if (percentValue > 90){
        percentDiv.addClass('nice');
    }
    else if (percentValue > 50){
        percentDiv.addClass('normal');
    }
    else{
        percentDiv.addClass('bad');
    };
});