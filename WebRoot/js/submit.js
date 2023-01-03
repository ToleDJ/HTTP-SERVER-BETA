

//$("#reset").hide();
//Submit

$("#PostImageSubmit").click(function() {
  funcURL = "upload" ;
  
  file = $("#PostImage").get(0).files[0];
  filename = $("#PostImage").val();
  console.log(file);
 
  if (file.length === 0) {
    file = "";
  } else {
    if (file.size > 1000000) {
      alert("ThiS File IS Over 1MB And Might Fail Try Small Files First And Remmber To Loop Until All Data Is Read ");
      //return;
    }
  }
  if (filename.length === 0) {
    filename = "";
  } else {
    filename = filename.substr(filename.lastIndexOf("\\") + 1);
  }
  
  funcURL += "?file-name=" + filename
  $("#PostImageSubmit").addClass("pro").html("");

  //Replace with your server function
  var request = $.ajax({
    url: funcURL,
    method: "POST",
    //data: { file : file, filename : filename },
    data: file,
    processData: false,
    async: false,
    contentType: 'text/plain',
    timeout : 20000
  });

  request.done(function( msg ) {
    console.log(msg);
    setTimeout(function() { 
    $('#PostImageSubmit').addClass("finish");
    $('#PostImageResult').html("You Sent File " + filename + " of size " + file.size + "<br/>Result Is " + msg);
    setTimeout(function() { 
      $("#PostImageSubmit").removeClass("pro").removeClass("finish").html("Submit");
      //$('#PostImageResult').html("Click Submit To See Result:");
    }, 500);
    }, 1000);
  });

  request.fail(function( jqXHR, textStatus, errorThrown ) {
    console.log(jqXHR);
    $('#PostImageSubmit').addClass("finish");
    $('#PostImageResult').html("Request failed: " + textStatus + " Error -  " + errorThrown + "</br> " + jqXHR.responseText);
    $("#PostImageSubmit").removeClass("pro").removeClass("finish").html("Submit");
  });

});

$("#GetImageSubmit").click(function() {
  funcURL = "image" ;
  filename = $("#GetImage").val();
  ext = ""
  
  if (filename.length === 0) {
    filename = "";
  } else {
    filename = filename.substr(filename.lastIndexOf("\\") + 1);
    ext = filename.split('.').pop();
  }

  if (ext == "") {
    alert("Please State The Full Name With Extension");
    return;
  };


  
  $("#GetImageSubmit").addClass("pro").html("");

  //Replace with your server function
  var request = $.ajax({
    url: funcURL,
    method: "GET",
    data: { "image-name" : filename },
    timeout: 20000
  });

  request.done(function( msg ) {
    setTimeout(function() { 
    $('#GetImageSubmit').addClass("finish");
    $('#GetImageResult').html('<a href="/image?image-name=' + filename + '"><img style="width:100%; height:100%;" src="/image?image-name=' + filename + '" /></a>');
    setTimeout(function() { 
      $("#GetImageSubmit").removeClass("pro").removeClass("finish").html("Submit");
      //$('#CalculateAreaResult').html("Click Submit To See Result:");
    }, 500);
    }, 1000);
  });

  request.fail(function( jqXHR, textStatus, errorThrown ) {
    $('#GetImageSubmit').addClass("finish");
    $('#GetImageResult').html("Request failed: " + textStatus + " Error -  " + errorThrown + "</br> " + jqXHR.responseText);
    $("#GetImageSubmit").removeClass("pro").removeClass("finish").html("Submit");
  });

});