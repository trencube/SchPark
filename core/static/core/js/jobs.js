$(document).ready(function(){

  var table = $('#jobs_table');

  table.dataTable({
      "columns": [{
          "orderable": true
      }, {
          "orderable": true
      }, {
          "orderable": false
      }, {
          "orderable": true
      }, {
          "orderable": true
      }, {
          "orderable": false
      }, {
          "orderable": false
      }, {
          "orderable": true
      }, {
          "orderable": true
      }, {
          "orderable": false
      }],
      "lengthMenu": [
          [10, 30, -1],
          [10, 30, "All"]
      ],
      "pageLength": 10,
      "pagingType": "bootstrap_full_number",
      "language": {
          "lengthMenu": "  _MENU_ records",
          "paginate": {
              "previous":"Prev",
              "next": "Next",
              "last": "Last",
              "first": "First"
          }
      },
      "order": [
          [0, "desc"]
      ]
  });

  var tableWrapper = jQuery('#jobs_table_wrapper');

  tableWrapper.find('.dataTables_length select').addClass("form-control input-xsmall input-inline");

});
