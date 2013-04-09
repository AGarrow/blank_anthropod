
$(document).ready(function() {

  // Press c to create in a detail or list view.
  $(document).bind('keydown', 'c', function(){
    $("#create").click();
  });

  // Press d to delete in a detail view.
  $(document).bind('keydown', 'd', function(){
    $("#delete").click();
  });

  // Press e to edit in a detail view.
  $(document).bind('keydown', 'e', function(){
    $("#edit").click();
  });
});
