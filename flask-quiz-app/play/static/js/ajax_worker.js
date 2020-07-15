$(document).ready(function() {
	$('.answer').click(function(event) {
        event.preventDefault();
        $.post("/play/answer/", {
            'answer' : $(this).val()
        }, function(response){
            $(`#btn-${response.correct}`).attr('id', 'correct');
            $(`#btn-${response.wrong}`).attr('id', 'wrong');
            $('.answer').attr('disabled', 'disabled');
            setTimeout(function(){
                $('.answer').removeAttr('disabled');
                window.location.reload();
            }, 2000);

        });
	});
});