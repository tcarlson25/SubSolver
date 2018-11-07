
$(document).ready(function() {
  $('#loader').hide();

  $('input:checkbox').click(function() {
      $('input:checkbox').not(this).prop('checked', false);
  });

  $('#decryptButton').click(function(){
    $('#loader').show();
    postData = {ciphertextInput: $('#ciphertext-input').val(), methodOption: getMethodSelected()};
  	$.ajax({
  		url: '/decrypt',
  		data: postData,
  		type: 'POST',
  		success: function(response){
  			console.log(response);
        responseJson = JSON.parse(response);
        $("#possibleKey").text(responseJson.key);
        $("#plaintextResult").text(responseJson.plaintext);
        $('#loader').hide();
  		},
  		error: function(error){
  			console.log(error);
        $('#loader').hide();
  		}
  	});
  });
});

function getMethodSelected() {
  var method1Checked = $('#method1Option').prop('checked');
  var method2Checked = $('#method2Option').prop('checked');
  if (method1Checked) {
    return 1;
  } else if (method2Checked) {
    return 2;
  } else {
    return 0;
  }
}
