function openSideNav() {
    document.getElementById("sideNavBarDiv").style.width = "250px";
}

/* Set the width of the side navigation to 0 */
function closeNav() {
    document.getElementById("sideNavBarDiv").style.width = "0";
}


// $("#menu-toggle").click(function (e) {
//     e.preventDefault();
//     $("#wrapper").toggleClass("toggled");
// });
// $("#menu-toggle-2").click(function (e) {
//     e.preventDefault();
//     $("#wrapper").toggleClass("toggled-2");
//     $('#menu ul').hide();
// });

/**
 * Init Menu
 */
function initMenu() {
    // alert("document loaded! Init menu")

    /**
     * Add click event to active menu item
     */
    $("li").click(function (event) {
        // event.preventDefault();
        // console.log(event);

        // alert("clicked on menu item: " + this.innerHTML);
        // iterate each element and toggle active class
        $("li").each(function (index, element) {
            // console.log(index + ": " + $(this).text());
            // console.log(element);
            if ($(this).hasClass("active")) {
                $(this).toggleClass("active");
            }
        });

        // toggleClass() switches the active class 
        // $("li").toggleClass("active");
        // $("li").addClass("active");
        $(this).addClass("active");

        // stop executing current event
        if ($(this).text() == 'Dropdown') {
            event.preventDefault();
        }
    });

    // $('#menu ul').hide();
    // $('#menu ul').children('.current').parent().show();
    // //$('#menu ul:first').show();
    // $('#menu li a').click(
    //     function () {
    //         var checkElement = $(this).next();
    //         if ((checkElement.is('ul')) && (checkElement.is(':visible'))) {
    //             return false;
    //         }
    //         if ((checkElement.is('ul')) && (!checkElement.is(':visible'))) {
    //             $('#menu ul:visible').slideUp('normal');
    //             checkElement.slideDown('normal');
    //             return false;
    //         }
    //     }
    // );

}

/**
 * On document ready
 */
$(document).ready(function () {
//    console.log($(this).text());
    initMenu();
});