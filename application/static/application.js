$(document).ready(function () {
    var requiredFields = [
      $('#id_email'),
      $('#id_first_name'),
      $('#id_last_name'),
      $('#id_home_address'),
      $('#id_home_city'),
      $('#id_home_state'),
      $('#id_home_zip'),
      $('#id_home_phone'),
      $('#id_work_phone'),
      $('#id_mobile_phone'),
      $('#id_occupation-occupation'),
      $('#id_occupation-business_name'),
      $('#id_occupation-address'),
      $('#id_occupation-city'),
      $('#id_occupation-state'),
      $('#id_occupation-zip'),
      $('#id_date_of_birth_month'),
      $('#id_date_of_birth_day'),
      $('#id_date_of_birth_year'),
      $('#id_city_of_birth'),
      $('#id_country_of_birth'),
      $('#id_sponsor')
    ]

    var requiredEmailAddresses = [
      $('#id_email')
    ]

    var notRequiredEmailAddresses = [
      $('#id_wife-email'),
    ]

    var requiredPhoneNumbers = [
      $('#id_home_phone'),
      $('#id_work_phone'),
      $('#id_mobile_phone')
    ]

    var notRequiredPhoneNumbers = [
      $('#id_wife-mobile_phone'),
      $('#id_sponsor_phone'),
      $('#id_occupation-phone')
    ]

    var twoCharactersRequired = [
      $('#id_home_state'),
      $('#id_state'),
      $('#id_postal_state'),
      $('#id_occupation-state')
    ]

    function runValidators (e, scope) {
      var valid = true;
      


      $(requiredFields).each(function () {
                var validatedElem = $(this);
                if (scope === 'all' || validatedElem.is(':visible')) {
                  removeError(validatedElem);
                  if (validatedElem.val() === undefined || validatedElem.val() === '') {
                      e.stopImmediatePropagation();
                      e.preventDefault();
                      valid = false;
                      addError(validatedElem, 'This field is required.');
                  } else {
                      removeError(validatedElem);
                  }
                }
            })

            $(requiredPhoneNumbers).each(function () {
                var validatedElem = $(this);
                if (scope === 'all' || validatedElem.is(':visible')) {
                  if (validatedElem.attr('class').indexOf('validation-error') === -1 && isValidTn(validatedElem.val()) === false) {
                      e.stopImmediatePropagation();
                      e.preventDefault();
                      valid = false;
                      addError(validatedElem, 'Please use a phone number in the format: 123-456-7890.')
                  }
                }
            })

            $(notRequiredPhoneNumbers).each(function () {
                var validatedElem = $(this);
                if (scope === 'all' || validatedElem.is(':visible')) {
                  if (isValidTn(validatedElem.val(), true) === false) {
                      removeError(validatedElem);
                      e.stopImmediatePropagation();
                      e.preventDefault();
                      valid = false;
                      addError(validatedElem, 'Please use a phone number in the format: 123-456-7890.')
                  } else {
                      removeError(validatedElem);
                  }
                }
            })

            $(twoCharactersRequired).each(function () {
                var validatedElem = $(this);
                if (scope === 'all' || validatedElem.is(':visible')) {
                  if (validatedElem.attr('class').indexOf('validation-error') === -1 && $.inArray(validatedElem.val().length, [0, 2]) === -1) {
                      e.stopImmediatePropagation();
                      e.preventDefault();
                      valid = false;
                      addError(validatedElem, 'Please use a 2 letter state code such as: TX')
                  } else if (validatedElem.val().length === 2) {
                      removeError(validatedElem);
                  };
                }
            })

            $(requiredEmailAddresses).each(function () {
                var validatedElem = $(this);
                if (scope === 'all' || validatedElem.is(':visible')) {
                  if (validatedElem.attr('class').indexOf('validation-error') === -1 && isValidEmail(validatedElem.val()) === false) {
                      e.stopImmediatePropagation();
                      e.preventDefault();
                      valid = false;
                      addError(validatedElem, 'Please use a valid email address.')
                  }
                }
            })

            $(notRequiredEmailAddresses).each(function () {
                var validatedElem = $(this);
                if (scope === 'all' || validatedElem.is(':visible')) {
                  if (isValidEmail(validatedElem.val(), true) === false) {
                      removeError(validatedElem);
                      e.stopImmediatePropagation();
                      e.preventDefault();
                      valid = false;
                      addError(validatedElem, 'Please use a valid email address.')
                  } else {
                      removeError(validatedElem);
                  }
                }
            })


      // test user email address to make sure it doesn't match existing email address
      var email = $('#id_email');
      if (scope === 'all' || email.is(':visible')) {
        $.ajax({
          url: '/accounts/existing_user',
          data: {email: email.val()},
          async: false
        }).done(function(data) {
          if (data.exists) {
            removeError(email);
            e.stopImmediatePropagation();
            e.preventDefault();
            valid = false;
            addError(email, 'An account with this email address already exists.');
          }
        }) 
      }

      if (scope === 'all' && !valid) {
        alert('Validation error. Please review all fields and try again.');
      }
    }

    // remove html requirement from required fields for better validation
    $('input').each(function() {$(this).attr({'required': false})});

    // ensure visible fields are valid on next
    $('#application-form').on('click', '.next', function (e) {
      runValidators(e, 'visible');      
    });

    // ensure fields are validated on submission
    $('#application-form').on('click', '.submit-application', function (e) {
      if (!$('.accept-terms').prop('checked')) {
        e.preventDefault();
        alert('You must accept the terms and conditions before submitting.');
      }
      runValidators(e, 'all');
    });

    // set initial postal same as home visibility
    togglePostalAddress();

    // handle postal same as home check box behavior
    $('#id_postal_same_as_home').on('change', function () {
        togglePostalAddress();
    })

    // initialize current committees formset
    $('#current-committees-formset').formset(
      {animateForms: true} 
    );

    // initialize children formset
    $('#children-formset').formset(
      {animateForms: true}
    );

    // children formset validators
    $('#children-formset').on('formAdded', function(e) {
      requiredFields.push($(e.target).find('.form-control[id$=name]').first());
    })
    
    $('#children-formset').on('formDeleted', function(e) {
      var nameId = $(e.target).find('.form-control[id$=name]').first().attr('id');
      $.grep(requiredFields, function(o, i) {
        if (o.attr('id') === nameId) {
          delete(requiredFields[i]);
        }
      }) 
      requiredFields = $.grep(requiredFields,function(n){ return(n) });
    })

    // committees formset validators
    $('#current-committees-formset').on('formAdded', function(e) {
      requiredFields.push($(e.target).find('.form-control[id$=committee]').first()); 
      requiredFields.push($(e.target).find('.form-control[id$=position]').first()); 
      requiredFields.push($(e.target).find('.form-control[id$=years]').first()); 
    })    
     
    $('#current-committees-formset').on('formDeleted', function(e) {
      var committeeId = $(e.target).find('.form-control[id$=committee]').first().attr('id');
      var positionId = $(e.target).find('.form-control[id$=position]').first().attr('id');
      var yearsId = $(e.target).find('.form-control[id$=years]').first().attr('id');
      $.grep(requiredFields, function(o, i) {
        if ([committeeId, positionId, yearsId].indexOf(o.attr('id')) >= 0) {
          delete(requiredFields[i]); 
        }
      })
      requiredFields = $.grep(requiredFields,function(n){ return(n) });
    })

    // only show wife section of wizard if wife is selected
    var marriedCheckbox = $('#id_married');
    var wifePill = $('.wife-pill');
    var wifeTab = $('#wife-tab');
    marriedCheckbox.on('change', function() {
      if (marriedCheckbox.prop('checked')) {
        wifePill.show();
      } else {
        wifePill.hide();
      }
    });
    if (!marriedCheckbox.prop('checked')) {wifePill.hide();}

    // only show children section of wizard if children is selected
    var childrenCheckbox = $('#id_children');
    var childrenPill = $('.children-pill');
    var childrenTab = $('.childrenTab');
    childrenCheckbox.on('change', function() {
      if (childrenCheckbox.prop('checked')) {
        childrenPill.show();
      } else {
        childrenPill.hide();
      }
    });
    if (!childrenCheckbox.prop('checked')) {childrenPill.hide();}

    // next button behavior
    $('form').on('click', '.next', function() {
      var activePill = $('.nav-pills > li.active');
      var activeIndex = $('.nav-pills> li:visible').index(activePill);
      activeIndex += 1;
      var activePill = $($('.nav-pills > li:visible')[activeIndex])
      activePill.find('a').removeClass('inactive').attr('data-toggle', 'tab').trigger('click');
    });
    
    // back button behavior
    $('form').on('click', '.back', function() {
      var activePill = $('.nav-pills > li.active');
      var activeIndex = $('.nav-pills> li:visible').index(activePill);
      activeIndex -= 1;
      var activePill = $($('.nav-pills > li:visible')[activeIndex])
      activePill.find('a').trigger('click');
    });
})



function togglePostalAddress () {
    var postalAddress = $('#id_postal_address, #id_postal_city, #id_postal_state, #id_postal_zip');
    var shouldBeVisible = $('#id_postal_same_as_home:checked').length < 1;
    if (shouldBeVisible) {
        postalAddress.each(function () {
            $(this).closest('.form-group').show();
        })
    } else {
        postalAddress.each(function () {
            $(this).closest('.form-group').hide();
        }) 
    }
        
}

function addError (elem, error) {
    elem.addClass('validation-error');
    var errorMessage = $('<p>').addClass('error-message');
    errorMessage.html(error);
    elem.after(errorMessage);
}

function removeError (elem) {
    elem.removeClass('validation-error');
    errorMessage = elem.parent().find('.error-message');
    errorMessage.remove();
}

// given a tn string, return true if string matches regex or is an empty string if blank == true
function isValidTn(tnString, blank) {
    var regex = /^\d{3}-\d{3}-\d{4}$/;
    var validTN = false;
    if (tnString.match(regex) !== null) {
        validTN = true;
    }
    if (blank === true && !validTN && tnString === '') {
        validTN = true;
    }
    return validTN;
}

// given an email string, return true if string matches regex or is an empty string if blank == true
function isValidEmail(emailString, blank) {
    var regex = /(([a-zA-Z0-9\-?\.?]+)@(([a-zA-Z0-9\-_]+\.)+)([a-z]{2,3}))+$/;
    var validEmail = false;
    if (emailString.match(regex) !== null) {
        validEmail = true;
    }
    if (blank === true && !validEmail && emailString === '') {
        validEmail = true;
    }
    return validEmail;
}
