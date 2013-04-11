
$(document).ready(function() {

  // Press c to create in a detail or list view.
  $(document).bind('keydown', 'c', function(){
    $("#create").click();
  });

  // Press d to delete.
  $(document).bind('keydown', 'd', function(){
    var el = $("#delete");
    if(el.length !== 0) {
      el.click();
    } else {
     $('.selected .item-delete').submit();
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
    var el = $('.selected a').first();
    window.location.href = el.attr('href');
  });
});
