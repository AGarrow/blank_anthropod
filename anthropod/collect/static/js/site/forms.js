$(document).ready(function() {

  /* When the page loads, create a mapping of phrases
  like 'alternate-name' and 'contact' to row templates. */
  var row_templates = {};
  $('.row-template').each(function(){
    var key = $(this).data('fieldname');
    row_templates[key] = $(this).html();
  });

  function setup_row_events(){

    console.log('binding...');

    /* When user clicks the button to add a new row,
    create a new tr node, append the row template
    content to it, and append it to the table. */
    var add_another = $('.add-another'),
        last_input = $('.tab-add-row :last').children(),
        x_button = $('.remove-row');

    // Nuke old events.
    add_another.unbind('click');
    last_input.unbind('keydown', 'tab');
    x_button.unbind('click');

    // Add a new one.
    add_another.click(function(){
      var row = $('<tr></tr>');
      row.append(row_templates[$(this).data('fieldname')]);
      $(this).find('~table:first tbody').append(row);
      $(document).trigger('row:add');
    });

    /* Add a new row when user presses tab in last cell of last row. */
    last_input.bind('keydown', 'tab', function(e){
      e.preventDefault();
      $(this).parents('div.row').find('a.btn').click();
      $(this).parents('tr').next().find(":input :first").focus();
      return false;
      });

    /* Remove the form row if user clicks the x button. */
    x_button.click(function(){
      $(this).parents('tr').remove();
    });

  }

  $(document).bind('row:add', {}, setup_row_events);
  $(document).trigger('row:add');

});
