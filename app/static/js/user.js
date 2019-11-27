$(document).ready(function() {
    $('[id^="dl"]').on('click', function (event) {
        let scheduleName = event.target.id.substring(2)
        deleteScheduleFromList(scheduleName)
    })
})

function deleteScheduleFromList(scheduleName){
    $('#ci'+scheduleName).remove()
    $.ajax({
        type:'POST',
        url: '/dev/deleteSchedule',
        data: JSON.stringify({
            scheduleName: scheduleName
        }),
        contentType: "application/json, charset=utf-8",
        success: function(data){
            let res = JSON.parse(data)
            console.log(res)
        }
    })
}

