

.click(function(event){
    event.preventDefault();
    makeAjaxRequest();
  });
  function makeAjaxRequest() {
    $.ajax({
        url: '/connect/google',
        type: 'POST',
        success: function(data){
          //code to open in new window comes here
        }
    });
  }