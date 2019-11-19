var appointments = new Array();

$(document).ready(function () {
  // $('#datePicker').val(new Date().toDateInputValue());

  $('[id^="addBtn"]').on("click", function (event) {
    addIntoSchedule(event.target.id);
  });

  $('[id^="sn"').on('click', function (event) {
    let scheduleName = event.target.id.substring(2)
    $('#dropdownMenuLink').text(scheduleName)
  })

  $('#callSaveScheduleBtn').on('click', function (event) {
    $('#saveScheduleContent').empty()
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

  })

  // prepare the data
  var source = {
    dataType: "array",
    dataFields: [
      { name: 'id', type: 'string' },
      { name: 'subject', type: 'string' },
      { name: 'location', type: 'string' },
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
    // editDialogCreate: function (dialog, fields, editAppointment) {
    // add custom print button.
    // printButton = $("<button style='margin-left: 5px; float:right;'>Print</button>");
    // fields.buttons.append(printButton);
    // printButton.jqxButton({ theme: this.theme });
    // printButton.click(function () {
    //   var appointment = editAppointment;
    //   if (!appointment)
    //     return;
    //   var appointmentContent =
    //     "<table class='printTable'>" +
    //     "<tr>" +
    //     "<td class='label'>caonimade</td>" +
    //     "<td>" + fields.subject.val() + "</td>" +
    //     "</tr>" +
    //     "<tr>" +
    //     "<td class='label'>Start</td>" +
    //     "<td>" + fields.from.val() + "</td>" +
    //     "</tr>" +
    //     "<tr>" +
    //     "<td class='label'>End</td>" +
    //     "<td>" + 'caonima' + "</td>" +
    //     "</tr>" +
    //     "<tr>" +
    //     "<td class='label'>Where</td>" +
    //     "<td>" + fields.location.val() + "</td>" +
    //     "</tr>" +
    //     "<tr>" +
    //     "<td class='label'>Calendar</td>" +
    //     "<td>" + fields.resource.val() + "</td>" +
    //     "</tr>"
    //     + "</table>";
    //   var newWindow = window.open('', '', 'width=800, height=500'),
    //     document = newWindow.document.open(),
    //     pageContent =
    //       '<!DOCTYPE html>\n' +
    //       '<html>\n' +
    //       '<head>\n' +
    //       '<meta charset="utf-8" />\n' +
    //       '<title>jQWidgets Scheduler</title>\n' +
    //       '<style>\n' +
    //       '.printTable {\n' +
    //       'border-color: #aaa;\n' +
    //       '}\n' +
    //       '.printTable .label {\n' +
    //       'font-weight: bold;\n' +
    //       '}\n' +
    //       '.printTable td{\n' +
    //       'padding: 4px 3px;\n' +
    //       'border: 1px solid #DDD;\n' +
    //       'vertical-align: top;\n' +
    //       '}\n' +
    //       '</style>' +
    //       '</head>\n' +
    //       '<body>\n' + appointmentContent + '\n</body>\n</html>';
    //   document.write(pageContent);
    //   document.close();
    //   newWindow.print();
    // }
    // );
    // },
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
  console.log(scheduleName)

  $.ajax({
    type: 'POST',
    url: '/dev/addSpotToSchedule',
    data: JSON.stringify({
      userId: 'qwertyuiopoi',
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
        start: new Date(year, parseInt(month) - 1, day, sthour, stmin, 0),
        end: new Date(year, parseInt(month) - 1, day, ethour, etmin, 0)
      }
      console.log(res.name, month, day, sthour, stmin, 0)
      $('#scheduler').jqxScheduler('addAppointment', appointment);
    }

  })
}