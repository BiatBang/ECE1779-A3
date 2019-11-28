$(document).ready(function () {
    var thisRate = ""

    $('[src$="%251.png"]').parent().addClass("active")

    $('[id^="star"]').on('click', function (event) {
        thisRate = event.target.id.substring(4)
        console.log("this time,", thisRate)
        $('#modalStar' + thisRate).prop('checked', true)
    })

    if (inCart == 1) {
        $('#addCartBtn').hide()
        $('#inCartMsg').show()
    } else {
        $('#addCartBtn').show()
        $('#inCartMsg').hide()
    }

    $('[id^="modalStar"]').on('click', function (event) {
        thisRate = event.target.id.substring(9)
        // $('#modalStar' + thisRate).prop('checked', true)
    })

    $('#addCartBtn').on('click', function (event) {
        addSpotIntoCart(spotId)
    })

    // $('[id^="saveRating"]').on('click', function(event) {
    //     let starNum = $('input[name=rate]:checked', "#rating").val()
    //     let spotId = event.target.id.substring(10)
    //     saveRating(spotId, starNum, thisRate)
    //     // alert('Save rating:' + starNum + spotId)
    // })

    // comes from database
    let curRate = userRating
    setRate(curRate)

    let starId = "star" + curRate.toString()
    if ($('#' + starId).is(':checked') === false) {
        $('#' + starId).prop('checked', true);
    }

    $('#callWriteReviewBtn').on('click', function (event) {
        let quote = userReview
        $('#newReview').empty()
        $('#newReview').append(quote)
    })

    $('[id^="saveReviewBtn"]').on('click', function (event) {
        // let spoId = event.target.id.substring(13)
        saveReview(spotId, thisRate, curRate)
    })

})

function setRate(curRate) {
    for(let i=1; i<=parseInt(curRate); i++) {
        $('#rate' + i.toString()).css('color', '#ffc700')
    }
}

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
        success: function (data) {
            let res = JSON.parse(data)
            console.log(res)
        }
    })
}


function saveReview(spotId, thisRate, curRate) {
    let content = $('#newReview').val()
    $.ajax({
        type: 'POST',
        url: '/dev/saveReview',
        data: JSON.stringify({
            spotId: spotId,
            newReview: content,
            starNum: thisRate,
            curRate: curRate
        }),
        contentType: 'application/json; charset=utf-8',
        success: function (data) {
            let res = JSON.parse(data)
            if (res.success == 1) {
                // save successfully
                console.log("save successfully")
                console.log('#saveReviewBtn' + spotId)
                $('#saveModal').modal('toggle')
                location.reload()
            } else if (res.success == 0) {
                // review empty
                $('#save-error-msg').text("*Schedule empty")
            }
        }
    })
}

function addSpotIntoCart(spotId) {
    $.ajax({
        type: 'POST',
        url: '/dev/addSpotToCart',
        data: JSON.stringify({
            spotId: spotId
        }),
        contentType: 'application/json; charset=utf-8',
        success: function (data) {
            let res = JSON.parse(data)
            if (res.success == 0) {
                window.location.href = "/dev/login"
            } else {
                $('#addCartBtn').hide()
                $('#inCartMsg').show()
            }
        }
    })
}