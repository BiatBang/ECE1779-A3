$(document).ready(function() {
    $('#scheduleDiv').on('click', function() {
        window.location.href = "/dev/viewCart/New%20Schedule";
    })

    $('#searchBtn').on('click', function() {
        let city = $('#myInput').val()
        window.location.href = "/dev/searchCity/" + city
    })
})