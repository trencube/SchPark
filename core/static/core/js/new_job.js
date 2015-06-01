$(document).ready(function(){

  $('#interval-select').select2({
    buttonWidth: '100%',
    maxHeight: 300,
  });


  $('#interval-select').change(function() {
    var interval = this.value;
    if ( interval == 'Y') {
      $('#interval-options-help').text('DD-MM HH:mm (Day, month, hour and minute to execute)');
    }
    if ( interval == 'M') {
      $('#interval-options-help').text('DD HH:mm (Day of month, hour and minute to execute)');
    }
    if ( interval == 'W') {
      $('#interval-options-help').text('N HH:mm (Day of week, 0=Monday, 6=Sunday, hour and minute to execute)');
    }
    if ( interval == 'D') {
      $('#interval-options-help').text('HH:mm (Hour and minute to execute)');
    }
    if ( interval == 'H') {
      $('#interval-options-help').text('mm (Minute to execute)');
    }
    if ( interval == 'm') {
      $('#interval-options-help').text('X (Execute every X minutes)');
    }

  });


});
