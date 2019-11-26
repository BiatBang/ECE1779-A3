$(document).ready(function() {
    $('[id^="star"]').on('click', function(evnet) {
        let starNum = event.target.id.substring(4)
        // take this to database
    })

    // comes from database
    let curRate = 4
    starId = "star" + curRate.toString()
    if($('#' + starId).is(':checked') === false) {
        $('#' + starId).prop('checked', true);
    }
})