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
      prefetch: '/collect/person/json/',
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
    input.attr('placeholder', 'Start typing an person name');
  }
  window.add_another = add_another;
});
