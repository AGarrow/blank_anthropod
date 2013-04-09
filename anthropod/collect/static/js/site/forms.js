$(document).ready(function() {

  /* When the page loads, create a mapping of phrases
  like 'alternate-name' and 'contact' to row templates. */
  var row_templates = {};
  $('.row-template').each(function(){
    var key = $(this).data('fieldname');
    row_templates[key] = $(this).html();
  });

  function setup_row_events(){

    /* When user clicks the button to add a new row,
    create a new tr node, append the row template
    content to it, and append it to the table. */
    var add_another = $('.add-another'),
        last_input = $('.tab-add-row').children(),
        x_button = $('.remove-row');

    // Nuke old events.
    add_another.unbind('click');
    x_button.unbind('click');

    // Add a new row.
    add_another.click(function(){
      var row = $('<tr></tr>');
      row.append(row_templates[$(this).data('fieldname')]);
      $(this).find('~table:first tbody').append(row);
      $(document).trigger('row:add');
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
