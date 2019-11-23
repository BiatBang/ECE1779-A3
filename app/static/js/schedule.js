var appointments = new Array();

$(document).ready(function () {
  // $('#datePicker').val(new Date().toDateInputValue());

  $('[id^="addBtn"]').on("click", function (event) {
    addIntoSchedule(event.target.id);
  });

  // $.each($('[id^="sn"'), function(index, sn) {
  //   let old = sn.text
  //   console.log(old)
  //   sn.text(old.replaceAll('%20', ' '))
  // })

  $('[id^="sn"').on('click', function (event) {
    let scheduleName = event.target.id.substring(2)
    $('#dropdownMenuLink').text(scheduleName)
    window.location.href = "/dev/viewCart/" + scheduleName;
  })

  $('[id^="dl"]').on('click', function (event) {
    let spotId = event.target.id.substring(2)
    deleteSpotFromCart(spotId)
  })

  $('#callSaveScheduleBtn').on('click', function (event) {
    $('#saveScheduleContent').empty()
    $('#save-error-msg').text("")
    let scheduleName = $('#dropdownMenuLink').text()
    if (scheduleName == 'New Schedule') {
      let inputEl = "<div class='form-group row cart-input-row'><label class='col-sm-2 col-form-label cart-input-label'> New Schedule Name:</label><div class='col-sm-10 cart-input-div'><input type='text' class='form-control' id='newScheduleName'></input></div></div>"
      $('#saveScheduleContent').append(inputEl)
    } else {
      let inputEl = "<label class='col-sm-2 col-form-label cart-input-label' style='max-width:100% !important;'>Schedule: " + scheduleName + "</label>"
      $('#saveScheduleContent').append(inputEl)
    }
  })

  $('#saveScheduleBtn').on('click', function (event) {
    saveSchedule()
  })

  slots = JSON.parse(slots)
  if(slots.length > 0) {
    $.each(slots, function(index, app) {
      let fromStr = app['start']
      let min = fromStr.split(':')[1]
      let other = fromStr.split(':')[0].split('-')
      app['start'] = new Date(other[0], other[1] - 1, other[2], other[3], min, 0)

      let endStr = app['end']
      min = endStr.split(':')[1]
      other = endStr.split(':')[0].split('-')
      app['end'] = new Date(other[0], other[1] - 1, other[2], other[3], min, 0)

      appointments.push(app)
    })
  }

  // prepare the data
  var source = {
    dataType: "array",
    dataFields: [
      { name: 'id', type: 'string' },
      { name: 'subject', type: 'string' },
      { name: 'location', type: 'string' },
      { name: 'description', type: 'string' },
      { name: 'start', type: 'date' },
      { name: 'end', type: 'date' }
    ],
    id: 'id',
    localData: appointments
  };
  var adapter = new $.jqx.dataAdapter(source);

  var today = new Date();
  var dd = String(today.getDate()).padStart(2, '0');
  var mm = String(today.getMonth() + 1).padStart(2, '0'); //January is 0!
  var yyyy = today.getFullYear();

  $("#scheduler").jqxScheduler({
    date: new $.jqx.date(yyyy, mm, dd),
    width: 850,
    height: 600,
    source: adapter,
    view: 'weekView',
    showLegend: true,
    editDialog: false,
    ready: function () {
      $("#scheduler").jqxScheduler('ensureAppointmentVisible', 'id1');
    },
    resources:
    {
      colorScheme: "scheme05",
      dataField: "calendar",
      source: new $.jqx.dataAdapter(source)
    },
    appointmentDataFields:
    {
      from: "start",
      to: "end",
      id: "id",
      description: "description",
      subject: "subject",
      location: "place",
    },
    views:
      [
        // 'dayView',
        'weekView',
        // 'monthView'
      ]
  });

  $("#scheduler").on('appointmentDoubleClick', function (event) {
    $("#scheduler").jqxScheduler({ editDialog: true });
    $('#scheduler').jqxScheduler('openDialog');
  });

  $("#scheduler").on('editDialogClose', function (event) {
    $("#scheduler").jqxScheduler({ editDialog: false });
  });

  $("#scheduler").on('editDialogCreate', function (event) {
    var fields = event.args.fields;
    fields.repeatContainer.hide();
    // hide status option
    fields.statusContainer.hide();
    // hide timeZone option
    fields.timeZoneContainer.hide();
    // hide color option
    fields.colorContainer.hide();
    fields.subjectContainer.hide();
    fields.locationContainer.hide();
    fields.fromContainer.hide();
    fields.toContainer.hide();
    fields.resourceContainer.hide();
    fields.allDayContainer.hide();
    fields.repeatContainer.hide();
    fields.descriptionContainer.hide();
    fields.repeat.hide();
    fields.repeatLabel.hide();
    fields.saveButton.hide();
  });

});

Date.prototype.toDateInputValue = (function () {
  var local = new Date(this);
  local.setMinutes(this.getMinutes() - this.getTimezoneOffset());
  return local.toJSON().slice(0, 10);
});

function addIntoSchedule(btnId) {
  // userid get from session

  spotId = btnId.substring(6)
  let date = $('#dt' + spotId).val();
  let startTime = $('#st' + spotId).val();
  let endTime = $('#et' + spotId).val();
  var year = date.split("-")[0]
  var month = date.split("-")[1]
  var day = date.split("-")[2]
  var sthour = startTime.split(":")[0]
  var stmin = startTime.split(":")[1]
  var ethour = endTime.split(":")[0]
  var etmin = endTime.split(":")[1]
  var scheduleName = $('#dropdownMenuLink').text()

  $.ajax({
    type: 'POST',
    url: '/dev/addSpotToSchedule',
    data: JSON.stringify({
      spotId: spotId,
      date: date,
      startTime: startTime,
      endTime: endTime,
      scheduleName: scheduleName
    }),
    contentType: 'application/json; charset=utf-8',
    success: function (data) {
      res = JSON.parse(data)
      var appointment = {
        id: "id1",
        subject: res.name,
        location: res.location,
        description: res.spotId,
        start: new Date(year, parseInt(month) - 1, day, sthour, stmin, 0),
        end: new Date(year, parseInt(month) - 1, day, ethour, etmin, 0)
      }
      $('#scheduler').jqxScheduler('addAppointment', appointment);
    }
  })
  $('#ci' + spotId).remove()
  $('#op' + spotId).remove()
}

function deleteSpotFromCart(spotId) {
  $('#ci' + spotId).remove()
  $('#op' + spotId).remove()
  $.ajax({
    type: 'POST',
    url: '/dev/removeSpotFromCart',
    data: JSON.stringify({
      spotId: spotId
    }),
    contentType: "application/json, charset=utf-8",
    success: function (data) {
      let res = JSON.parse(data)
      console.log(res)
    }
  })
}

function saveSchedule() {
  let scheduleName = $('#dropdownMenuLink').text()
  let isNewSchedule = false
  let isError = false
  if (scheduleName == "New Schedule") {
    isNewSchedule = true
    scheduleName = $('#newScheduleName').val() //.replaceAll(' ', '%20')
    if (scheduleName.length == 0 || scheduleName == null) {
      $('#save-error-msg').text("*Schedule name empty")
      console.log("no name")
      isError = true
    }
  }

  if (!isError) {
    let appointments = $('#scheduler').jqxScheduler('getAppointments');
    let spotSlots = []

    $.each(appointments, function (index, app) {
      spotSlot = {
        spotId: app['originalData']['description'],
        name: app['originalData']['subject'],
        from: app['originalData']['start'],
        to: app['originalData']['end']
      }
      spotSlots.push(spotSlot)
    })
    $.ajax({
      type: 'POST',
      url: '/dev/saveSchedule',
      data: JSON.stringify({
        scheduleName: scheduleName,
        spotSlots: spotSlots,
        isNewSchedule, isNewSchedule
      }),
      contentType: 'application/json, charset=utf-8',
      success: function (data) {
        let res = JSON.parse(data)
        if (res.success == 2) {
          // schedule name existed
          $('#save-error-msg').text("*Schedule name existed")
        } else if (res.success == 1) {
          // save successfully
          console.log("save successfully")
          $('#saveModal').modal('toggle')
          window.location.href = "/dev/viewCart/" + scheduleName;
        } else if (res.success == 0) {
          // schedule empty
          $('#save-error-msg').text("*Schedule empty")
        }
      }
    })
  }
}

String.prototype.replaceAll = function(search, replacement) {
  var target = this;
  return target.split(search).join(replacement);
};