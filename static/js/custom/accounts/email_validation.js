$(document).ready(function () {
    // ajax email validation
    $(document).on("keyup", ".js-validate-email", function () {
        var form = $(this).closest("form");
        $.ajax({
            url: form.attr("data-validate-email-url"),
            data: {email: $(this).val()},
            dataType: 'json',
            success: function (data) {
                if (data.is_email_taken) {
                    $('.js-validate-email-error').text(data.error_message).show()
                    $('#submit-btn').attr('disabled', 'disabled');
                }
                else {
                    $('.js-validate-email-error').hide();
                    $('#submit-btn').removeAttr('disabled');
                }
            }
        });
    });
})    