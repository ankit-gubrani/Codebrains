(function ($) {
    $.fn.wrapper = function () {
        return this.each(function () {
            var item = $(this);
            var reloadBtn = item.find('.reload-btn');
            reloadBtn.click(function () {
                var reloadParam = item.find('.reload-param').val();
                if (reloadParam == '') {
                    alert("Please enter value in Reload Param to see it Work !");
                } else {
                    var paths = $(".reload-id");
                    for (var i = 0; i < paths.length; i++) {
                        var eachComponent = paths[i];
                        var eachComponentPath = eachComponent.getAttribute("ajaxified-component-path");

                        $.get(eachComponentPath + ".html?reloadParam=" + reloadParam,
                            function (data) {
                                $(eachComponent).parent().html(data);
                            });

                    }
                }


            });
        });
    }
})(jQuery);
