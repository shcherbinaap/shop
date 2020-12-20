window.onload = function () {
    $('.basket_list').on('click', 'input[type="number"]', function () {
        var elem = event.target;
        console.log(elem)
        // console.log(t_href.value)

        $.ajax({
            url: "/baskets/edit/" + elem.name + "/" + elem.value + "/",

            success: function (data) {
                $('.basket_list').html(data.result);
            },
        });

        event.preventDefault();
    });
}