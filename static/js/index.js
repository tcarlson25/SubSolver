
$(document).ready(function() {
  $('#loader').hide();

  $('input:checkbox').click(function() {
      $('input:checkbox').not(this).prop('checked', false);
      methodSelected = getMethodSelected()
      if (methodSelected == "1") {
        $("#possibleKeyOrMapLabel").text('Possible Key');
      } else if (methodSelected == "2") {
        $("#possibleKeyOrMapLabel").text('Found Mapping');
      } else {
        $("#possibleKeyOrMapLabel").text('Choose a Method');
      }
  });

  $('#decryptButton').click(function(){
    $('#loader').show();
    var methodSelected = getMethodSelected();
    postData = {ciphertextInput: $('#ciphertext-input').val(), methodOption: methodSelected};
  	$.ajax({
  		url: '/decrypt',
  		data: postData,
  		type: 'POST',
  		success: function(response){
  			// console.log(response);
        responseJson = JSON.parse(response);
        if (methodSelected == "1") {
          $("#possibleKeyOrMap").text(responseJson.key_mapping);
        } else if (methodSelected == "2") {
          $("#possibleKeyOrMap").text(JSON.stringify(responseJson.key_mapping));
        }
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
