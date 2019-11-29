$(document).ready(function () {
    var thisRate = ""
    userReview = userReview.replaceAll('&amp;#10;', '\n')
    // alert(userReview)
    $('[src$="%251.png"]').parent().addClass("active")

    $('[id^="star"]').on('click', function (event) {
        thisRate = event.target.id.substring(4)
        console.log("this time,", thisRate)
        $('#modalStar' + thisRate).prop('checked', true)

        $('#newReview').empty()
        $('#newReview').append(userReview)
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
    setRate(spotRating)

    let starId = "star" + userRating.toString()
    if ($('#' + starId).is(':checked') === false) {
        $('#' + starId).prop('checked', true);

    }


    $('[id^="saveReviewBtn"]').on('click', function (event) {
        // let spoId = event.target.id.substring(13)
        saveReview(spotId, thisRate, userRating)
    })

})

function setRate(userRating) {
    for(let i=1; i<=parseInt(userRating); i++) {
        $('#rate' + i.toString()).css('color', '#ffc700')
    }
}

function saveRating(spotId, starNum, userRating) {
    $.ajax({
        type: 'POST',
        url: '/dev/saveRating',
        data: JSON.stringify({
            spotId: spotId,
            starNum: starNum,
            curRate: userRating
        }),
        contentType: 'application/json; charset=utf-8',
        success: function (data) {
            let res = JSON.parse(data)
            console.log(res)
        }
    })
}


function saveReview(spotId, thisRate, userRating) {
    let content = $('#newReview').val()
    $.ajax({
        type: 'POST',
        url: '/dev/saveReview',
        data: JSON.stringify({
            spotId: spotId,
            newReview: content,
            starNum: thisRate,
            curRate: userRating
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


String.prototype.replaceAll = function (search, replacement) {
    var target = this;
    return target.split(search).join(replacement);
};
