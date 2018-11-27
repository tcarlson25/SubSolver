
$(document).ready(function() {
  $('#loader').hide();
  $("#plainTextLabel").hide();
  $('#key-input').hide();
  $('#randomKeyLabel').hide();
  $('#randomKeyOption').hide();

  $('#randomKeyOption').click(function() {
    var isRandom = $('#randomKeyOption').prop('checked');
    if (isRandom) {
      $('#key-input').val(generateRandomKey());
    } else {
      $('#key-input').val('');
    }
  });

  $('.main').click(function() {
      $('.main').not(this).prop('checked', false);
      methodSelected = getMethodSelected()
      if (methodSelected == "0") {
        // no method selected
        $('#ciphertext-input').attr('placeholder', 'Enter Ciphertext to Decrypt...');
        $('#cipherLabel').text('Ciphertext');
        $("#possibleKeyOrMapLabel").text('Choose a Method');
        $("#plainTextLabel").hide();
        $('#key-input').hide();
        $("#decryptButton").text("Decrypt");
        $('#randomKeyLabel').hide();
        $('#randomKeyOption').hide();
        resetResults();
      } else if (methodSelected == "7") {
        // manual
        $('#ciphertext-input').attr('placeholder', 'Enter Ciphertext to Decrypt...');
        $('#key-input').attr('placeholder', 'Enter Key to Decrypt with...');
        $('#cipherLabel').text('Ciphertext');
        $('#key-input').show();
        $("#possibleKeyOrMapLabel").text('Key');
        $("#plainTextLabel").text("Plaintext");
        $("#plainTextLabel").show();
        $("#decryptButton").text("Decrypt");
        $('#randomKeyLabel').hide();
        $('#randomKeyOption').hide();
        resetResults();
      } else if (methodSelected == "8") {
        // encrypt
        $('#ciphertext-input').attr('placeholder', 'Enter Ciphertext to Encrypt...');
        $('#key-input').attr('placeholder', 'Enter Key to Encrypt with...');
        $('#cipherLabel').text('Plaintext');
        $('#key-input').show();
        $("#plainTextLabel").show();
        $("#possibleKeyOrMapLabel").text('Key');
        $("#plainTextLabel").text("Ciphertext");
        $("#decryptButton").text("Encrypt");
        $('#randomKeyLabel').show();
        $('#randomKeyOption').show();
        resetResults();
      } else if (methodSelected != "5") {
        // ngrams
        $('#ciphertext-input').attr('placeholder', 'Enter Ciphertext to Decrypt...');
        $('#cipherLabel').text('Ciphertext');
        $('#key-input').hide();
        $("#possibleKeyOrMapLabel").text('Possible Key');
        $("#plainTextLabel").text("Plaintext");
        $("#plainTextLabel").show();
        $("#decryptButton").text("Decrypt");
        $('#randomKeyLabel').hide();
        $('#randomKeyOption').hide();
        resetResults();
      } else {
        // intersection
        $('#ciphertext-input').attr('placeholder', 'Enter Ciphertext to Decrypt...');
        $('#cipherLabel').text('Ciphertext');
        $('#key-input').hide();
        $("#possibleKeyOrMapLabel").text('Found Mapping');
        $("#plainTextLabel").text("Plaintext");
        $("#plainTextLabel").show();
        $('#randomKeyLabel').hide();
        $('#randomKeyOption').hide();
        resetResults();
      }
  });

  $('#decryptButton').click(function(){
    $('#loader').show();
    var methodSelected = getMethodSelected();
    postData = {ciphertextInput: $('#ciphertext-input').val(), methodOption: methodSelected, keyInput: $('#key-input').val()};
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
          // frequency
          mappings = responseJson.key_mapping;
          div = responseJson.barData;
          mappingsStr = responseJson.key_mapping;
          $("#possibleKeyOrMap").html(mappingsStr);
          $("#plaintextResult").text(responseJson.plaintext);
          $('#barGraph').html(div);
        } else if (methodSelected == "7") {
          // manual
          $("#plaintextResult").text(responseJson.plaintext);
          // encrypt
        } else if (methodSelected == "8") {
          $("#plaintextResult").text(responseJson.ciphertext);
        } else if (methodSelected != "5") {
          // ngrams
          $("#possibleKeyOrMap").text(responseJson.key_mapping);
          $("#plaintextResult").text(responseJson.plaintext);
          $('#barGraph').html('');
        } else {
          // intersection
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
  $('#barGraph').html('');
}

function generateRandomKey() {
  var letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ";
  return letters.split('').sort(randomsort).join('');
}

function randomsort(a, b) {
	return Math.random()>.5 ? -1 : 1;
}

function getMethodSelected() {
  var method1Checked = $('#method1Option').prop('checked');
  var method2Checked = $('#method2Option').prop('checked');
  var method3Checked = $('#method3Option').prop('checked');
  var method4Checked = $('#method4Option').prop('checked');
  var method5Checked = $('#method5Option').prop('checked');
  var method6Checked = $('#method6Option').prop('checked');
  var method7Checked = $('#method7Option').prop('checked');
  var method8Checked = $('#method8Option').prop('checked');
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
  } else if (method7Checked) {
    return 7;
  } else if (method8Checked) {
    return 8;
  } else {
    return 0;
  }
}
