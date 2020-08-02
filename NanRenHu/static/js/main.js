$(function(){
    ts(".tabbed.menu .item").tab({
        onSwitch: (tabName, groupName) => {
            $("#" + tabName)
        }
    });

    $(".module").hide();

    $(".module.active").show();

    $("select.ts.basic.dropdown").on("change", function(){
        console.log(this.value);
        $(".module.active").toggle(250, function(){
            $(this).removeClass("active");
        });
        $(".module." + this.value).toggle(250, function(){
            $(this).addClass("active");
        });
    });
});
