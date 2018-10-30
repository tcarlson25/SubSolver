$(document).ready(function() {
  $('#decryptButton').click(function(){
    postData = {ciphertextInput: $('#ciphertext-input').val()};
  	$.ajax({
  		url: '/decrypt',
  		data: postData,
  		type: 'POST',
  		success: function(response){
  			console.log(response);
  		},
  		error: function(error){
  			console.log(error);
  		}
  	});
  });
});
