$(document).ready(function () {
    
    $(".date_from").datepicker({
        changeMonth: true,
        dateFormat :"dd/mm/yy",
		//dateFormat :"yy-m-d",
		
        numberOfMonths: 1,
        onClose: function (selectedDate) {
            $(".date_to").datepicker("option", "minDate", selectedDate);
			
        }
		
    });
    $(".date_to").datepicker({
        defaultDate: "+1w",
        dateFormat :"dd/mm/yy",
        changeMonth: true,
        numberOfMonths: 1,
        onClose: function (selectedDate) {
            $(".date_from").datepicker("option", "maxDate", selectedDate);
        }
    });

    $('.datepicker-input-clear').button();

    $('.datepicker-input-clear').click(function () {
        $(this).parent().find('input').val("");
        return false;
    });

});