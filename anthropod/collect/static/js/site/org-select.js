$(document).ready(function(){

  /* Template used to format items in the suggestion drop-down. */
  var typeahead_templ = [
    '<div class="org-select">',
      '<input class="typeahead" type="text">',
    '</div>'
    ].join('');

  /* Adds another typeahead box. */
  function add_another(data){
    $('#inputs').append($(typeahead_templ));
    var input = $("input.typeahead").typeahead({
      name: data.name.replace(/[\/:-]/g, "_"),
      prefetch: '/collect/orgs/json_for_geo/'+ data.id,
      limit: 10,
      template: [
        '<div>',
        '<p>{{value}}</p>',
        '<p class="muted">{{_id}}</p>',
        '</div>'
        ].join(''),
      engine: Hogan
    });
    input.focus();
    input.attr('placeholder', 'Start typing an org name');
  }
  window.add_another = add_another;

  /* Template used to add text after geo is chosen. */
  var selected_tmpl = Hogan.compile([
        '<div>',
        '<p><i class="icon-user">',
        '</i>&nbsp;<strong>{{value}}</strong></p>',
        '<p class="muted">{{_id}}</p>',
        '</div>',
        '<hr/>'
        ].join(''));

  // Fires when a suggestion is chosen from the typeahead drop-down.
  $(document).bind('typeahead:selected', function(event, data){

    // Nuke all existing following typeaheads. Hide them and
    // switch the submit value to the id instead of the name.
    var old_inputs = $('input.typeahead'),
        input;
    old_inputs.typeahead('destroy');
    old_inputs.remove();
    console.log(data);
    input = $('<input type="hidden" name="org_id">');
    input.attr('value', data._id);
    $('#inputs').append(input);
    $('#inputs').append(selected_tmpl.render(data));
  });
});
