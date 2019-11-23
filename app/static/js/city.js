$(document).ready(function() {
    $('#scheduleDiv').on('click', function() {
        window.location.href = "/dev/viewCart/New%20Schedule";
    })

    $('[src$="%251.png"]').parent().addClass("active")
    $('[id^="as"]').prop("disabled", false)

    $('[id^="as"]').on('click', function(event) {
        let spotId = event.target.id.substring(2)
        addSpotIntoCart(spotId)
        $('#as' + spotId).attr('src', '/dev/static/assets/checkmark.png')
        $('#as' + spotId).prop("disabled", true)
    })

    // let userCart = '{{userCart}}'
    userCart = userCart.replace('[','').replace(']','')
    userCart = userCart.replaceAll("&#39;",'')
    userCart = userCart.split(', ')
    $.each(userCart, function(index, spotId) {        
        addIcon = "as" + spotId
        console.log(addIcon)
        $('#' + addIcon).attr('src', '/dev/static/assets/checkmark.png')
        $('#' + addIcon).prop("disabled", true)
    })
})

String.prototype.replaceAll = function(search, replacement) {
    var target = this;
    return target.split(search).join(replacement);
};

function addSpotIntoCart(spotId) {
    $.ajax({
        type: 'POST',
        url: '/dev/addSpotToCart',
        data: JSON.stringify({
            spotId: spotId
        }),
        contentType: 'application/json; charset=utf-8',
        success: function(data) {
            let res = JSON.parse(data)
            console.log(res)
        }
    })

}