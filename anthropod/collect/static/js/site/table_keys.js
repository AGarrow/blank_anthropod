$(document).ready(function() {

  var table = $("table.table-keys tbody"),
      trs = table.find("tr");

  // Make table rows clickable.
  table.on('click', 'tr', function(){
      var location = $(this).find("a").attr("href");
      if (location) {
          window.location.href = location;
          return false;
      }
    });

  trs.on('click', '.btn', function(event){
    event.stopPropagation();
  });

  // If javascript is enabled, change cursor to pointer over table rows
  // and add selected class on hover.
  trs.css('cursor', 'pointer');
  trs.hover(function(){
          $(this).addClass('selected');
      },
      function(){
          $(this).removeClass('selected');
      }
  );

  function down() {
    var tr,
        selected = table.find('.selected');
    if(selected.length === 0) {
      tr = table.find('tr:first');
      tr.addClass('selected');
    } else {
      tr = table.find('tr.selected');
      var next_tr = tr.next();
      if(next_tr.length !== 0) {
        tr.removeClass('selected');
        next_tr.addClass('selected');
      }
    }
  }

  function up() {
    var tr,
        selected = table.find('.selected');
    if(selected.length === 0) {
      tr = table.find('tr:last');
      tr.addClass('selected');
    } else {
      tr = table.find('tr.selected');
      var next_tr = tr.prev();
      if(next_tr.length !== 0) {
        tr.removeClass('selected');
        next_tr.addClass('selected');
      }
    }
  }
  $(document).bind('keydown', 'j', down);
  // $(document).bind('keydown', 'down', down);
  $(document).bind('keydown', 'k', up);
  // $(document).bind('keydown', 'up', up);

});
