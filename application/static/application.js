$(document).ready(function () {
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