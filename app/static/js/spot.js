// $(document).ready(function() {
//     $('').setfix
// })
var $stars;

jQuery(document).ready(function ($) {

  // Custom whitelist to allow for using HTML tags in popover content
  var myDefaultWhiteList = $.fn.tooltip.Constructor.Default.whiteList
  myDefaultWhiteList.textarea = [];
  myDefaultWhiteList.button = [];

  $stars = $('.rate-popover');

  $stars.on('mouseover', function () {
    var index = $(this).attr('data-index');
    markStarsAsActive(index);
  });

  function markStarsAsActive(index) {
    unmarkActive();

    for (var i = 0; i <= index; i++) {
      switch (index) {
        case '0':
          $($stars.get(i)).addClass('oneStar');
          break;
        case '1':
          $($stars.get(i)).addClass('twoStars');
          break;
        case '2':
          $($stars.get(i)).addClass('threeStars');
          break;
        case '3':
          $($stars.get(i)).addClass('fourStars');
          break;
        case '4':
          $($stars.get(i)).addClass('fiveStars');
          break;
      }
    }
  }

  function unmarkActive() {
    $stars.removeClass('oneStar twoStars threeStars fourStars fiveStars');
  }

  $stars.on('click', function () {
    $stars.popover('hide');
  });

  // Submit, you can add some extra custom code here
  // ex. to send the information to the server
  $('#rateMe').on('click', '#voteSubmitButton', function () {
    $stars.popover('hide');
  });

  // Cancel, just close the popover
  $('#rateMe').on('click', '#closePopoverButton', function () {
    $stars.popover('hide');
  });

});

$(function () {
  $('.rate-popover').popover({
    // Append popover to #rateMe to allow handling form inside the popover
    container: '#rateMe',
    // Custom content for popover
    content: `<div class="my-0 py-0"> <textarea type="text" style="font-size: 0.78rem" class="md-textarea form-control py-0" placeholder="Write us what can we improve" rows="3"></textarea> <button id="voteSubmitButton" type="submit" class="btn btn-sm btn-primary">Submit!</button> <button id="closePopoverButton" class="btn btn-flat btn-sm">Close</button>  </div>`
  });
  $('.rate-popover').tooltip();
});
