$(document).ready(function() {

    $('[id^="saveRating"]').on('click', function(event) {
        let starNum = $('input[name=rate]:checked', "#rating").val()
        let spotId = event.target.id.substring(10)
        saveRating(spotId, starNum, curRate)
        alert('Save rating:' + starNum + spotId)
    })

    // comes from database
    let curRate = userRating
    let starId = "star" + curRate.toString()
    if($('#' + starId).is(':checked') === false) {
        $('#' + starId).prop('checked', true);
    }
    
    $('#callWriteReviewBtn').on('click', function (event) {
        // ------ Check the user wrote or not ---------
        preReview = checkPreReview(spotId) 
        $('#newReview').append(quote); 
    })

    $('[id^="saveReviewBtn"]').on('click', function (event) {
        let spoId = event.target.id.substring(13)
        saveReview(spoId)
    })

})

function saveRating(spotId, starNum, curRate) {
    $.ajax({
        type: 'POST',
        url: '/dev/saveRating',
        data: JSON.stringify({
            spotId: spotId,
            starNum: starNum,
            curRate: curRate
        }),
        contentType: 'application/json; charset=utf-8',
        success: function(data) {
            let res = JSON.parse(data)
            console.log(res)
        }
    })
}

function checkPreReview(spoId) {
    $.ajax({
        type: 'POST',
        url: '/dev/checkPreReview',
        data: JSON.stringify({
            spoId: spoId
        }),
        contentType: 'application/json; charset=utf-8',
        success: function(data) {
            let res = JSON.parse(data)
            console.log(res)
        }
    })
}

function saveReview(spotId) {
    let content = $('#newReview').val()
    $.ajax({
        type: 'POST',
        url: '/dev/saveReview',
        data: JSON.stringify({
            spotId: spotId,
            newReview: content
        }),
        contentType: 'application/json; charset=utf-8',
        success: function(data) {
            let res = JSON.parse(data)
            if (res.success == 1) {
                // save successfully
                console.log("save successfully")
                console.log('#saveReviewBtn'+spotId)
                $('#saveModal').modal('toggle')
            } else if (res.success == 0) {
                // review empty
                $('#save-error-msg').text("*Schedule empty")
            }
        }
    })
}