$(document).ready(function() {

  var table = $("table.table-keys tbody");


  function down() {
    var tr,
        selected = $('.selected');
    if(selected.length === 0) {
      tr = table.find('tr:first');
      tr.addClass('selected');
    } else {
      tr = $('.selected');
      var next_tr = tr.next();
      if(next_tr.length !== 0) {
        tr.removeClass('selected');
        next_tr.addClass('selected');
      }
    }
  }

  function up() {
    var tr,
        selected = $('.selected');
    if(selected.length === 0) {
      tr = table.find('tr:last');
      tr.addClass('selected');
    } else {
      tr = $('.selected');
      var next_tr = tr.prev();
      if(next_tr.length !== 0) {
        tr.removeClass('selected');
        next_tr.addClass('selected');
      }
    }
  }

  $(document).bind('keydown', 'j', down);
  $(document).bind('keydown', 'down', down);
  $(document).bind('keydown', 'k', up);
  $(document).bind('keydown', 'up', up);

});
