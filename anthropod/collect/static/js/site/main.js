
$(document).ready(function() {

  // Press c to create in a detail or list view.
  $(document).bind('keydown', 'c', function(){
    $("#create").click();
  });


  // Press d to delete.
  $(document).bind('keydown', 'd', function(){
    var el = $('.selected .item-delete');
    if(el.length !== 0) {
      el.submit();
    } else {
      el = $("#delete");
      el.click();
    }
  });

  // Press e to edit.
  $(document).bind('keydown', 'e', function(){
    var el = $("#edit");
    if(el.length !== 0) {
      el.click();
    } else {
      el = $('.selected .item-edit').click();
      window.location.href = el.attr('href');
    }
  });

  // Press esc to focus back on the document.
  $(':input').bind('keydown', 'esc', function(e){
    $("*:focus").blur();
  });

  $(document).bind('keydown', 'return', function(){
    var el = $('.selected a');
    if(el.length !== 0){
      el.first();
      window.location.href = el.attr('href');
    }
  });

  // Show key bindings.
  $(document).bind('keydown', 'shift+/', function(){
    $('#key_bindings').modal();
  });

  // View thing's memberships.
  $(document).bind('keydown', 'm', function(){
    window.location.href = $('#memberships').attr('href');
  });

  // View thing's json.
  $(document).bind('keydown', 'v', function(){
    window.location.href = $('#jsonview').attr('href');
  });

  // View thing's json.
  $(document).bind('keydown', 'a', function(){
    $('#add-memb').click();
  });

  $(document).bind('keydown', 'q', function(){
    localStorage.clear();
    console.log('Cleared local storage.');
    location.reload(true);
  });

  $(document).bind('keydown', 'f', function(){
    $('#find').click();
  });
});
