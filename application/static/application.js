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
        $('#id_occupation'),
        $('#id_business_name'),
        $('#id_business_address'),
        $('#id_business_city'),
        $('#id_business_state'),
        $('#id_business_zip'),
        $('#id_date_of_birth_month'),
        $('#id_date_of_birth_day'),
        $('#id_date_of_birth_year'),
        $('#id_city_of_birth'),
        $('#id_country_of_birth')
    ]

    var requiredPhoneNumbers = [
        $('#id_home_phone'),
        $('#id_work_phone'),
        $('#id_mobile_phone')
    ]

    var notRequiredPhoneNumbers = [
        $('#id_fax'),
        $('#id_wife_mobile_phone')
    ]

    var twoCharactersRequired = [
        $('#id_home_state'),
        $('#id_business_state'),
        $('#id_postal_state')
    ]

    // remove html requirement from required fields for better validation
    $('input').each(function() {$(this).attr({'required': false})});

    // ensure required fields are valid on submit
    $('#application-form').submit(function (e) {
        $(requiredFields).each(function () {
            var validatedElem = $(this);
            removeError(validatedElem);
            if (validatedElem.val() === undefined || validatedElem.val() === '') {
                e.preventDefault();
                addError(validatedElem, 'This field is required.');
            } else {
                removeError(validatedElem);
            }
        })

        $(requiredPhoneNumbers).each(function () {
            var validatedElem = $(this);
            if (validatedElem.attr('class').indexOf('validation-error') === -1 && isValidTn(validatedElem.val()) === false) {
                e.preventDefault();
                addError(validatedElem, 'Please use a phone number in the format: 123-456-7890.')
            }
        })

        $(notRequiredPhoneNumbers).each(function () {
            var validatedElem = $(this);
            if (isValidTn(validatedElem.val(), true) === false) {
                removeError(validatedElem);
                e.preventDefault();
                addError(validatedElem, 'Please use a phone number in the format: 123-456-7890.')
            } else {
                removeError(validatedElem);
            }
        })

        $(twoCharactersRequired).each(function () {
            var validatedElem = $(this);
            console.log(validatedElem);
            if (validatedElem.attr('class').indexOf('validation-error') === -1 && validatedElem.val().length !== 2) {
                e.preventDefault();
                addError(validatedElem, 'Please use a 2 letter state code such as: TX')
            };
        })
    })

    // set initial postal same as home visibility
    togglePostalAddress();

    // handle postal same as home check box behavior
    $('#id_postal_same_as_home').on('change', function () {
        togglePostalAddress();
    })
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