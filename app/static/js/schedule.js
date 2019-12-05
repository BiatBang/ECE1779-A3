var appointments = new Array();

$(document).ready(function () {
  // $('#datePicker').val(new Date().toDateInputValue());
  var today = new Date();
  var dd = String(today.getDate()).padStart(2, '0');
  var mm = String(today.getMonth() + 1).padStart(2, '0'); //January is 0!
  var yyyy = today.getFullYear();

  $('[id^="addBtn"]').on("click", function (event) {
    addIntoSchedule(event.target.id.substring(6));
  });
  // ascii in html will be transformed to normal character
  // js can't do that, so replace it manually
  sitems = JSON.parse(scheduleStr.replaceAll('&#39;', '\''))
  let dateFrom = ""
  let dateTo = ""
  $.each(sitems, function (index, item) {
    if (scheduleName == item['scheduleName']) {
      dateFrom = item['dateFrom']
      yyyy = parseInt(dateFrom.split('-')[0])
      mm = String(parseInt(dateFrom.split('-')[1])).padStart(2, '0');
      dd = dateFrom.split('-')[2].padStart(2, '0');
      dateTo = item['dateTo']
    }
  })
  $('#dropdownMenuLink').text(scheduleName + ": " + dateFrom + " - " + dateTo)

  $('[id^="sn"').on('click', function (event) {
    let scheduleName = event.target.id.substring(2)
    $('#dropdownMenuLink').text(scheduleName + ": " + dateFrom + " - " + dateTo)
    window.location.href = "/dev/viewCart/" + scheduleName;
  })

  $('[id^="dl"]').on('click', function (event) {
    let spotId = event.target.id.substring(2)
    deleteSpotFromCart(spotId)
  })

  $('#callSaveScheduleBtn').on('click', function (event) {
    $('#saveScheduleContent').empty()
    $('#save-error-msg').text("")
    let scheduleName = $('#dropdownMenuLink').text().split(':')[0]
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
  if (slots.length > 0) {
    $.each(slots, function (index, app) {
      app['subject'] = app['subject'].replaceAll('&#39;', '\'')
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
      { name: 'resourceId', type: 'string' },
      { name: 'end', type: 'date' }
    ],
    id: 'id',
    localData: appointments
  };
  var adapter = new $.jqx.dataAdapter(source);

  $("#scheduler").jqxScheduler({
    date: new $.jqx.date(yyyy, mm, dd),
    width: 850,
    height: 600,
    source: adapter,
    view: 'weekView',
    showLegend: true,
    editDialog: false,
    timeZone: 'Eastern Standard Time',
    ready: function () {
      $("#scheduler").jqxScheduler('ensureAppointmentVisible');
    },
    resources:
    {
      colorScheme: "scheme05",
      dataField: "calendar",
      source: new $.jqx.dataAdapter(source)
    },
    appointmentDataFields:
    {
      id: "id",
      subject: "subject",
      location: "location",
      description: "description",
      resourceId: "resourceId",
      from: "start",
      to: "end",
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
    // hide id option
    fields.statusContainer.hide();
    // hide timeZone option
    fields.timeZoneContainer.hide();
    // hide color option
    fields.colorContainer.hide();
    fields.resourceContainer.hide();
    fields.allDayContainer.hide();
    fields.repeatContainer.hide();
    fields.repeat.hide();
    fields.repeatLabel.hide();
  });

  $("#scheduler").on('editDialogOpen', function (event) {
    var fields = event.args.fields;
    // hide id option
    fields.statusContainer.hide();
    // hide timeZone option
    fields.timeZoneContainer.hide();
    // hide color option
    fields.colorContainer.hide();
    fields.allDayContainer.hide();
    fields.repeatContainer.hide();
    fields.repeat.hide();
    fields.repeatLabel.hide();
  });

});

Date.prototype.toDateInputValue = (function () {
  var local = new Date(this);
  local.setMinutes(this.getMinutes() - this.getTimezoneOffset());
  return local.toJSON().slice(0, 10);
});

function addIntoSchedule(spotId) {
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
  var scheduleName = $('#dropdownMenuLink').text().split(':')[0]
  $.ajax({
    type: 'POST',
    url: '/dev/addSpotToSchedule',
    data: JSON.stringify({
      spotId: spotId,
      date: date,
      startTime: startTime,
      endTime: endTime,
      scheduleName: scheduleName,
      description: "description"
    }),
    contentType: 'application/json; charset=utf-8',
    success: function (data) {
      res = JSON.parse(data)
      var appointment = {
        id: spotId,
        subject: res.name,
        location: res.location,
        description: "description",
        resourceId: "aaa",
        start: new Date(year, parseInt(month) - 1, day, sthour, stmin, 0),
        end: new Date(year, parseInt(month) - 1, day, ethour, etmin, 0)
      }
      $('#scheduler').jqxScheduler('addAppointment', appointment);
      appointments = $('#scheduler').jqxScheduler('getAppointments');
      $.each(appointments, function (index, app) {
        if (app['subject'] == res.name) {
          let curId = app['id']
          app['id'] = spotId
        }
      })
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
    }
  })
}

function saveSchedule() {
  let scheduleName = $('#dropdownMenuLink').text().split(':')[0]
  let isNewSchedule = false
  let isError = false
  if (scheduleName == "New Schedule") {
    isNewSchedule = true
    scheduleName = $('#newScheduleName').val() //.replaceAll(' ', '%20')
    if (scheduleName.length == 0 || scheduleName == null) {
      $('#save-error-msg').text("*Schedule name empty")
      isError = true
    }
  }
  if (!isError) {
    apps = $('#scheduler').jqxScheduler('getAppointments');

    let spotSlots = []
    $.each(appointments, function (index, app) {
      $.each(apps, function(index, ap) {
        if(ap['subject'] == app['subject']) {
          app['start'] = UTC2EST(ap['originalData']['start'])
          app['end'] = UTC2EST(ap['originalData']['end'])
          app['description'] = ap['description']
        }
      })
      spotSlot = {
        spotId: app['id'],
        name: app['subject'],
        from: app['start'],
        to: app['end'],
        description: app['description']
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

String.prototype.replaceAll = function (search, replacement) {
  var target = this;
  return target.split(search).join(replacement);
};

function UTC2EST(utcTime) {
  let offset = 5
  let est = utcTime.getTime() - 5*60*60*1000
  return new Date(est)
}