
$(document).ready(function() {
  $('#loader').hide();

  $('input:checkbox').click(function() {
      $('input:checkbox').not(this).prop('checked', false);
      methodSelected = getMethodSelected()
      if (methodSelected == "0") {
        $("#possibleKeyOrMapLabel").text('Choose a Method');
        resetResults();
      } else if (methodSelected != "5") {
        $("#possibleKeyOrMapLabel").text('Possible Key');
        resetResults();
      } else {
        $("#possibleKeyOrMapLabel").text('Found Mapping');
        resetResults();
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
        responseJson = JSON.parse(response);
        $('#loader').hide();
        if (methodSelected == "0") {
          alert('Please Choose a Method');
        } else if (methodSelected == "6") {
          mappings = responseJson.key_mapping;
          div = responseJson.barData;
          mappingsStr = responseJson.key_mapping;
          $("#possibleKeyOrMap").html(mappingsStr);
          $("#plaintextResult").text(responseJson.plaintext);
          $('#barGraph').html(div);

        } else if (methodSelected != "5") {
          $("#possibleKeyOrMap").text(responseJson.key_mapping);
          $("#plaintextResult").text(responseJson.plaintext);
          $('#barGraph').html('');
        } else {
          mappings = responseJson.key_mapping;
          div = responseJson.tableData;
          mappingsStr = ""
          for (var mapping in mappings) {
            console.log(mapping + ":" + mappings[mapping]);
            mappingsStr += mapping + "  -->  [" + mappings[mapping] + "]<br />";
          }
          $("#plaintextResult").text(responseJson.plaintext);
          $('#barGraph').html('');
          $('#barGraph').html(div);
        }
  		},
  		error: function(error){
  			console.log(error);
        $('#loader').hide();
  		}
  	});
  });
});

function resetResults() {
  $("#possibleKeyOrMap").html('');
  $("#plaintextResult").html('');
}

function getMethodSelected() {
  var method1Checked = $('#method1Option').prop('checked');
  var method2Checked = $('#method2Option').prop('checked');
  var method3Checked = $('#method3Option').prop('checked');
  var method4Checked = $('#method4Option').prop('checked');
  var method5Checked = $('#method5Option').prop('checked');
  var method6Checked = $('#method6Option').prop('checked');
  if (method1Checked) {
    return 1;
  } else if (method2Checked) {
    return 2;
  } else if (method3Checked) {
    return 3;
  } else if (method4Checked) {
    return 4;
  } else if (method5Checked) {
    return 5;
  } else if (method6Checked) {
    return 6;
  } else {
    return 0;
  }
}
