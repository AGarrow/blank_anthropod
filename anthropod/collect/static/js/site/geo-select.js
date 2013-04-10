$(document).ready(function(){

  /* Template used to format items in the suggestion drop-down. */
  var typeahead_templ = [
    '<div class="geo-select">',
      '<input class="typeahead" type="text">',
    '</div>'
    ].join('');

  /* Adds another typeahead box. */
  function add_another(data){
    $('#inputs').append($(typeahead_templ));
    var input = $("input.typeahead").typeahead({
      name: data.id.replace(/[\/:-]/g, "_"),
      prefetch: '/collect/geo/ids/'+ data.id,
      limit: 10,
      template: [
        '<div>',
        '<p>{{value}}</p>',
        '<p class="muted">{{id}}</p>',
        '</div>'
        ].join(''),
      engine: Hogan
    });
    input.focus();
    input.attr('placeholder', 'Start typing a place name');
  }

  /* Template used to add text after geo is chosen. */
  var selected_tmpl = Hogan.compile([
        '<div>',
        '<p><i class="icon-map-marker">',
        '</i>&nbsp;<strong>{{value}}</strong></p>',
        '<p class="muted">{{id}}</p>',
        '</div>',
        '<hr/>'
        ].join(''));

  // Fires when a suggestion is chosen from the typeahead drop-down.
  $(document).bind('typeahead:selected', function(event, data){

    // Nuke all existing follwing typeaheads. Hide them and
    // switch the submit value to the id instead of the name.
    var old_inputs = $('input.typeahead');
    old_inputs.typeahead('destroy');
    old_inputs.remove();
    $("#final-id").val(data.id);
    $('#inputs').append(selected_tmpl.render(data));

    // Then hit the server for more geo data. Add a new row.
    add_another(data);
  });

  add_another({id: 'ocd-division/country:us/', name: 'US'});
});
